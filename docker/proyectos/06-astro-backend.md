# Proyecto 6: Backend con Astro JS

## Objetivo
Crear una aplicación backend/fullstack con Astro JS usando Docker.

## Prerrequisitos
- Proyectos anteriores completados
- Conocimientos básicos de Astro
- Node.js instalado

---

## Paso 1: Crear Proyecto Astro

```bash
mkdir -p ~/curso-docker/proyectos/06-astro-backend
cd ~/curso-docker/proyectos/06-astro-backend

# Crear proyecto Astro
npm create astro@latest .
# Seleccionar: Empty o template de tu preferencia
# TypeScript: Yes (recomendado)
# Install dependencies: Yes
```

**Estructura del proyecto:**
```
06-astro-backend/
├── src/
│   ├── pages/
│   │   ├── index.astro
│   │   └── api/
│   │       └── users.ts
│   ├── layouts/
│   ├── components/
│   └── content/
├── public/
├── astro.config.mjs
├── package.json
├── tsconfig.json
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yml
└── .dockerignore
```

## Paso 2: Configurar Astro

**astro.config.mjs:**
```javascript
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',  // Modo servidor para API endpoints
  adapter: node({
    mode: 'standalone'
  }),
  server: {
    port: 3000,
    host: true  // Importante para Docker
  }
});
```

**Instalar adaptador Node:**
```bash
npx astro add node
```

## Paso 3: Crear API Endpoints

**src/pages/api/health.ts:**
```typescript
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  return new Response(
    JSON.stringify({ status: 'healthy', timestamp: new Date().toISOString() }),
    {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    }
  );
};
```

**src/pages/api/users/index.ts:**
```typescript
import type { APIRoute } from 'astro';

// Simulación de base de datos en memoria
let users = [
  { id: 1, name: 'Juan', email: 'juan@example.com' },
  { id: 2, name: 'María', email: 'maria@example.com' },
];

let nextId = 3;

// GET /api/users
export const GET: APIRoute = async () => {
  return new Response(JSON.stringify({ users }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};

// POST /api/users
export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const { name, email } = body;

    if (!name || !email) {
      return new Response(
        JSON.stringify({ error: 'Name and email are required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const newUser = { id: nextId++, name, email };
    users.push(newUser);

    return new Response(JSON.stringify(newUser), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Invalid JSON' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
```

**src/pages/api/users/[id].ts:**
```typescript
import type { APIRoute } from 'astro';

// GET /api/users/:id
export const GET: APIRoute = async ({ params }) => {
  const { id } = params;
  const user = users.find(u => u.id === parseInt(id));

  if (!user) {
    return new Response(
      JSON.stringify({ error: 'User not found' }),
      { status: 404, headers: { 'Content-Type': 'application/json' } }
    );
  }

  return new Response(JSON.stringify(user), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};

// PUT /api/users/:id
export const PUT: APIRoute = async ({ params, request }) => {
  const { id } = params;
  const body = await request.json();
  const { name, email } = body;

  const userIndex = users.findIndex(u => u.id === parseInt(id));

  if (userIndex === -1) {
    return new Response(
      JSON.stringify({ error: 'User not found' }),
      { status: 404, headers: { 'Content-Type': 'application/json' } }
    );
  }

  users[userIndex] = { ...users[userIndex], name, email };

  return new Response(JSON.stringify(users[userIndex]), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};

// DELETE /api/users/:id
export const DELETE: APIRoute = async ({ params }) => {
  const { id } = params;
  const userIndex = users.findIndex(u => u.id === parseInt(id));

  if (userIndex === -1) {
    return new Response(
      JSON.stringify({ error: 'User not found' }),
      { status: 404, headers: { 'Content-Type': 'application/json' } }
    );
  }

  users.splice(userIndex, 1);

  return new Response(
    JSON.stringify({ message: 'User deleted' }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
};
```

## Paso 4: Crear Página Frontend (Opcional)

**src/pages/index.astro:**
```astro
---
const title = 'Astro Backend API';
---

<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <title>{title}</title>
  </head>
  <body>
    <h1>{title}</h1>
    <p>API Endpoints disponibles:</p>
    <ul>
      <li>GET /api/health</li>
      <li>GET /api/users</li>
      <li>GET /api/users/:id</li>
      <li>POST /api/users</li>
      <li>PUT /api/users/:id</li>
      <li>DELETE /api/users/:id</li>
    </ul>

    <div id="app"></div>

    <script>
      async function testAPI() {
        try {
          const response = await fetch('/api/users');
          const data = await response.json();
          console.log('Users:', data);

          document.getElementById('app').innerHTML =
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        } catch (error) {
          console.error('Error:', error);
        }
      }

      testAPI();
    </script>
  </body>
</html>
```

## Paso 5: Dockerfile Multi-Stage

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente
COPY . .

# Build de la aplicación
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar solo dependencias de producción
RUN npm ci --only=production && npm cache clean --force

# Copiar build
COPY --from=builder /app/dist ./dist

# Exponer puerto
EXPOSE 3000

# Usuario no-root
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {r.statusCode === 200 ? process.exit(0) : process.exit(1)})"

# Comando de inicio
CMD ["node", "./dist/server/entry.mjs"]
```

## Paso 6: Dockerfile.dev

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# El código se monta como volumen

EXPOSE 3000

# Modo desarrollo
CMD ["npm", "run", "dev"]
```

## Paso 7: Crear .dockerignore

```
node_modules
dist
.git
.gitignore
README.md
.env
.env.local
.DS_Store
*.log
.vscode
.idea
coverage
```

## Paso 8: Docker Compose

```yaml
version: '3.8'

services:
  # Producción
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    container_name: astro-app-prod
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    profiles:
      - production

  # Desarrollo con hot reload
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - ./public:/app/public
      - ./astro.config.mjs:/app/astro.config.mjs
    container_name: astro-app-dev
    environment:
      - NODE_ENV=development
    profiles:
      - development
```

## Paso 9: Construir y Ejecutar

**Producción:**
```bash
# Build
docker build -t astro-app:v1 .

# Run
docker run -d \
  --name astro-container \
  -p 3000:3000 \
  astro-app:v1

# Verificar
curl http://localhost:3000/api/health
curl http://localhost:3000/api/users
```

**Desarrollo:**
```bash
docker compose --profile development up -d
docker compose logs -f app-dev
```

---

## Integración con Base de Datos

**Instalar Prisma:**
```bash
npm install @prisma/client
npm install -D prisma
```

**Inicializar Prisma:**
```bash
npx prisma init
```

**prisma/schema.prisma:**
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  name      String
  email     String   @unique
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

**src/lib/db.ts:**
```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

**Actualizar API endpoint:**
```typescript
import type { APIRoute } from 'astro';
import { prisma } from '../../../lib/db';

export const GET: APIRoute = async () => {
  const users = await prisma.user.findMany();
  return new Response(JSON.stringify({ users }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};

export const POST: APIRoute = async ({ request }) => {
  const { name, email } = await request.json();

  const user = await prisma.user.create({
    data: { name, email }
  });

  return new Response(JSON.stringify(user), {
    status: 201,
    headers: { 'Content-Type': 'application/json' }
  });
};
```

**docker-compose.yml con PostgreSQL:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: password
      POSTGRES_DB: astrodb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U usuario"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  app:
    build: .
    container_name: astro-app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://usuario:password@db:5432/astrodb
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

**Actualizar Dockerfile para Prisma:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
COPY prisma ./prisma/

RUN npm ci
RUN npx prisma generate

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/prisma ./prisma

EXPOSE 3000

CMD ["sh", "-c", "npx prisma migrate deploy && node ./dist/server/entry.mjs"]
```

---

## Middleware en Astro

**src/middleware.ts:**
```typescript
import { defineMiddleware } from 'astro:middleware';

export const onRequest = defineMiddleware(async (context, next) => {
  const start = Date.now();

  // Logging
  console.log(`${context.request.method} ${context.url.pathname}`);

  // CORS
  if (context.request.method === 'OPTIONS') {
    return new Response(null, {
      status: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      }
    });
  }

  const response = await next();

  // Add CORS headers to response
  response.headers.set('Access-Control-Allow-Origin', '*');

  const duration = Date.now() - start;
  console.log(`Request completed in ${duration}ms`);

  return response;
});
```

---

## Variables de Entorno

**.env:**
```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/astrodb
API_SECRET=your-secret-key
NODE_ENV=development
```

**Uso en código:**
```typescript
// En API endpoints
const apiSecret = import.meta.env.API_SECRET;

// En componentes .astro
const databaseUrl = import.meta.env.DATABASE_URL;
```

**Pasar en Docker:**
```bash
docker run -d \
  --name astro-app \
  -p 3000:3000 \
  -e DATABASE_URL=postgresql://... \
  -e API_SECRET=secret \
  astro-app:v1
```

---

## Content Collections (CMS-like)

**src/content/config.ts:**
```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string(),
  }),
});

export const collections = { blog };
```

**src/content/blog/post-1.md:**
```markdown
---
title: 'Mi primer post'
description: 'Descripción del post'
pubDate: 2024-01-01
author: 'Juan'
---

# Contenido del post

Este es el contenido de mi primer post.
```

**API endpoint para content:**
```typescript
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async () => {
  const posts = await getCollection('blog');

  return new Response(JSON.stringify({ posts }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};
```

---

## SSR vs Static

Astro puede generar páginas estáticas o servir dinámicamente:

**Configurar modo híbrido:**
```javascript
// astro.config.mjs
export default defineConfig({
  output: 'hybrid',  // Permite mezclar static y server
  adapter: node()
});
```

**Marcar página como estática:**
```astro
---
export const prerender = true;
---
```

**Marcar como servidor:**
```astro
---
export const prerender = false;
---
```

---

## Ejercicios Prácticos

### Ejercicio 1: Blog API
Crea una API REST completa para un blog:
- CRUD de posts
- CRUD de comentarios
- Relaciones entre posts y comentarios
- Paginación

### Ejercicio 2: Autenticación
Implementa autenticación con:
- JWT tokens
- Login/Register endpoints
- Rutas protegidas
- Session middleware

### Ejercicio 3: File Upload
```bash
npm install @astrojs/node formidable
```

Implementa upload de archivos:
- POST /api/upload
- Guardar en /public/uploads
- Retornar URL pública

### Ejercicio 4: WebSockets
Implementa real-time con WebSockets:
- Chat en tiempo real
- Notificaciones
- Live updates

---

## Testing

**Instalar Vitest:**
```bash
npm install -D vitest @vitest/ui
```

**vitest.config.ts:**
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
  },
});
```

**src/api/users.test.ts:**
```typescript
import { describe, it, expect } from 'vitest';

describe('Users API', () => {
  it('should return users', async () => {
    // Test implementation
    expect(true).toBe(true);
  });
});
```

**package.json:**
```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui"
  }
}
```

---

## Optimizaciones

### 1. Comprimir respuestas
```bash
npm install compression
```

### 2. Caché
```typescript
// Middleware de caché
export const onRequest = defineMiddleware(async (context, next) => {
  const response = await next();

  if (context.url.pathname.startsWith('/api/static')) {
    response.headers.set('Cache-Control', 'public, max-age=3600');
  }

  return response;
});
```

### 3. Rate Limiting
```bash
npm install express-rate-limit
```

---

## Troubleshooting

### Puerto ya en uso
```bash
lsof -i :3000
kill -9 PID
```

### Build falla
```bash
# Limpiar y reinstalar
rm -rf node_modules dist .astro
npm install
npm run build
```

### API no responde
```bash
# Verificar logs
docker logs astro-container

# Verificar health
curl http://localhost:3000/api/health
```

---

## Resumen de Comandos

```bash
# Crear proyecto
npm create astro@latest .

# Desarrollo local
npm run dev

# Build
npm run build

# Preview build
npm run preview

# Docker producción
docker build -t astro-app:v1 .
docker run -d --name astro-app -p 3000:3000 astro-app:v1

# Docker desarrollo
docker compose --profile development up -d

# Logs
docker logs -f astro-app
docker compose logs -f
```

---

## Checklist del Proyecto

- [ ] Crear proyecto Astro
- [ ] Configurar modo servidor
- [ ] Instalar adaptador Node
- [ ] Crear API endpoints
- [ ] Crear Dockerfile multi-stage
- [ ] Crear Dockerfile.dev
- [ ] Crear .dockerignore
- [ ] Construir y probar imagen
- [ ] Crear docker-compose.yml
- [ ] Integrar base de datos (opcional)
- [ ] Agregar middleware
- [ ] Configurar variables de entorno
- [ ] Escribir tests
- [ ] Documentar endpoints

---

## Siguiente Paso

Continúa con:
**[Proyecto 7: Backend con Java (Spring Boot)](./07-java-spring.md)**
