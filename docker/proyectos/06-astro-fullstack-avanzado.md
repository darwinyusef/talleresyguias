# Proyecto 6B: Astro Full Stack con Nginx + PostgreSQL

## Objetivo
Crear una aplicación Astro completa con Nginx sirviendo archivos estáticos, PostgreSQL como base de datos, todo orquestado con Docker Compose.

---

## Arquitectura del Proyecto

```
┌─────────────────┐
│   Navegador     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Nginx (80/443) │ ← Proxy reverso + archivos estáticos
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Astro (3000)  │ ← API + SSR
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL:5432 │ ← Base de datos
└─────────────────┘
```

---

## Paso 1: Estructura del Proyecto

```
06-astro-fullstack/
├── app/                          # Aplicación Astro
│   ├── src/
│   │   ├── pages/
│   │   │   ├── index.astro
│   │   │   ├── users.astro
│   │   │   └── api/
│   │   │       ├── health.ts
│   │   │       └── users/
│   │   │           ├── index.ts
│   │   │           └── [id].ts
│   │   ├── components/
│   │   │   └── UserCard.astro
│   │   ├── layouts/
│   │   │   └── Layout.astro
│   │   ├── lib/
│   │   │   └── db.ts
│   │   └── middleware.ts
│   ├── public/
│   │   ├── images/
│   │   └── assets/
│   ├── prisma/
│   │   └── schema.prisma
│   ├── astro.config.mjs
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── nginx/
│   ├── nginx.conf
│   └── default.conf
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Paso 2: Configurar Proyecto Astro

### Crear proyecto
```bash
mkdir -p ~/curso-docker/proyectos/06-astro-fullstack
cd ~/curso-docker/proyectos/06-astro-fullstack
mkdir app nginx

cd app
npm create astro@latest . -- --template minimal --yes --typescript strict
npm install
```

### Instalar dependencias
```bash
npm install @astrojs/node
npm install @prisma/client
npm install -D prisma
npm install dotenv
```

### astro.config.mjs
```javascript
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server',
  adapter: node({
    mode: 'standalone'
  }),
  server: {
    port: 3000,
    host: '0.0.0.0'  // Importante para Docker
  },
  vite: {
    server: {
      watch: {
        usePolling: true  // Para hot reload en Docker
      }
    }
  }
});
```

---

## Paso 3: Configurar PostgreSQL con Prisma

### Inicializar Prisma
```bash
npx prisma init
```

### prisma/schema.prisma
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
  bio       String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  posts     Post[]
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String
  published Boolean  @default(false)
  authorId  Int
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### app/src/lib/db.ts
```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: ['query', 'error', 'warn'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

// Graceful shutdown
if (typeof window === 'undefined') {
  process.on('beforeExit', async () => {
    await prisma.$disconnect();
  });
}
```

---

## Paso 4: Crear API Endpoints

### app/src/pages/api/health.ts
```typescript
import type { APIRoute } from 'astro';
import { prisma } from '../../lib/db';

export const GET: APIRoute = async () => {
  try {
    // Test database connection
    await prisma.$queryRaw`SELECT 1`;

    return new Response(
      JSON.stringify({
        status: 'healthy',
        database: 'connected',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
      }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({
        status: 'unhealthy',
        database: 'disconnected',
        error: error instanceof Error ? error.message : 'Unknown error'
      }),
      {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
};
```

### app/src/pages/api/users/index.ts
```typescript
import type { APIRoute } from 'astro';
import { prisma } from '../../../lib/db';

// GET /api/users
export const GET: APIRoute = async ({ url }) => {
  try {
    const page = parseInt(url.searchParams.get('page') || '1');
    const limit = parseInt(url.searchParams.get('limit') || '10');
    const skip = (page - 1) * limit;

    const [users, total] = await Promise.all([
      prisma.user.findMany({
        skip,
        take: limit,
        orderBy: { createdAt: 'desc' },
        include: {
          posts: {
            where: { published: true },
            select: { id: true, title: true }
          }
        }
      }),
      prisma.user.count()
    ]);

    return new Response(
      JSON.stringify({
        users,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit)
        }
      }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    console.error('Error fetching users:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to fetch users' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};

// POST /api/users
export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const { name, email, bio } = body;

    if (!name || !email) {
      return new Response(
        JSON.stringify({ error: 'Name and email are required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const user = await prisma.user.create({
      data: { name, email, bio }
    });

    return new Response(JSON.stringify(user), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error: any) {
    if (error.code === 'P2002') {
      return new Response(
        JSON.stringify({ error: 'Email already exists' }),
        { status: 409, headers: { 'Content-Type': 'application/json' } }
      );
    }

    console.error('Error creating user:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to create user' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
```

### app/src/pages/api/users/[id].ts
```typescript
import type { APIRoute } from 'astro';
import { prisma } from '../../../lib/db';

// GET /api/users/:id
export const GET: APIRoute = async ({ params }) => {
  try {
    const id = parseInt(params.id as string);

    const user = await prisma.user.findUnique({
      where: { id },
      include: {
        posts: {
          orderBy: { createdAt: 'desc' }
        }
      }
    });

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
  } catch (error) {
    console.error('Error fetching user:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to fetch user' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};

// PUT /api/users/:id
export const PUT: APIRoute = async ({ params, request }) => {
  try {
    const id = parseInt(params.id as string);
    const body = await request.json();
    const { name, email, bio } = body;

    const user = await prisma.user.update({
      where: { id },
      data: { name, email, bio }
    });

    return new Response(JSON.stringify(user), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error: any) {
    if (error.code === 'P2025') {
      return new Response(
        JSON.stringify({ error: 'User not found' }),
        { status: 404, headers: { 'Content-Type': 'application/json' } }
      );
    }

    console.error('Error updating user:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to update user' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};

// DELETE /api/users/:id
export const DELETE: APIRoute = async ({ params }) => {
  try {
    const id = parseInt(params.id as string);

    await prisma.user.delete({
      where: { id }
    });

    return new Response(
      JSON.stringify({ message: 'User deleted successfully' }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error: any) {
    if (error.code === 'P2025') {
      return new Response(
        JSON.stringify({ error: 'User not found' }),
        { status: 404, headers: { 'Content-Type': 'application/json' } }
      );
    }

    console.error('Error deleting user:', error);
    return new Response(
      JSON.stringify({ error: 'Failed to delete user' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
```

---

## Paso 5: Crear Páginas Frontend

### app/src/layouts/Layout.astro
```astro
---
interface Props {
  title: string;
}

const { title } = Astro.props;
---

<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>{title}</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: system-ui, -apple-system, sans-serif;
        background: #f5f5f5;
        color: #333;
        line-height: 1.6;
      }

      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
      }

      nav {
        background: #2563eb;
        color: white;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
      }

      nav ul {
        list-style: none;
        display: flex;
        gap: 2rem;
      }

      nav a {
        color: white;
        text-decoration: none;
        font-weight: 500;
      }

      nav a:hover {
        text-decoration: underline;
      }

      .card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      }

      .btn {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        text-decoration: none;
        font-size: 1rem;
      }

      .btn:hover {
        background: #1d4ed8;
      }

      .btn-danger {
        background: #dc2626;
      }

      .btn-danger:hover {
        background: #b91c1c;
      }

      input, textarea {
        width: 100%;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 1rem;
      }

      label {
        display: block;
        margin-top: 1rem;
        font-weight: 500;
      }
    </style>
  </head>
  <body>
    <nav>
      <ul>
        <li><a href="/">Inicio</a></li>
        <li><a href="/users">Usuarios</a></li>
        <li><a href="/api/health">Health Check</a></li>
      </ul>
    </nav>
    <div class="container">
      <slot />
    </div>
  </body>
</html>
```

### app/src/pages/index.astro
```astro
---
import Layout from '../layouts/Layout.astro';
---

<Layout title="Astro Full Stack App">
  <h1>Astro Full Stack con Nginx + PostgreSQL</h1>

  <div class="card">
    <h2>Arquitectura</h2>
    <ul>
      <li><strong>Frontend:</strong> Astro SSR</li>
      <li><strong>Backend:</strong> Astro API Routes</li>
      <li><strong>Base de datos:</strong> PostgreSQL</li>
      <li><strong>Proxy/Static:</strong> Nginx</li>
      <li><strong>Orquestación:</strong> Docker Compose</li>
    </ul>
  </div>

  <div class="card">
    <h2>Endpoints Disponibles</h2>
    <ul>
      <li><a href="/api/health">GET /api/health</a> - Health check</li>
      <li><a href="/api/users">GET /api/users</a> - Listar usuarios</li>
      <li>POST /api/users - Crear usuario</li>
      <li>GET /api/users/:id - Obtener usuario</li>
      <li>PUT /api/users/:id - Actualizar usuario</li>
      <li>DELETE /api/users/:id - Eliminar usuario</li>
    </ul>
  </div>

  <a href="/users" class="btn">Ver Usuarios</a>
</Layout>
```

### app/src/pages/users.astro
```astro
---
import Layout from '../layouts/Layout.astro';
import { prisma } from '../lib/db';

const users = await prisma.user.findMany({
  include: {
    posts: true
  },
  orderBy: { createdAt: 'desc' }
});
---

<Layout title="Usuarios">
  <h1>Gestión de Usuarios</h1>

  <div class="card">
    <h2>Crear Usuario</h2>
    <form id="create-form">
      <label>Nombre:</label>
      <input type="text" name="name" required />

      <label>Email:</label>
      <input type="email" name="email" required />

      <label>Bio:</label>
      <textarea name="bio" rows="3"></textarea>

      <button type="submit" class="btn">Crear Usuario</button>
    </form>
  </div>

  <h2>Lista de Usuarios ({users.length})</h2>

  {users.map(user => (
    <div class="card">
      <h3>{user.name}</h3>
      <p><strong>Email:</strong> {user.email}</p>
      {user.bio && <p><strong>Bio:</strong> {user.bio}</p>}
      <p><strong>Posts:</strong> {user.posts.length}</p>
      <p><small>Creado: {new Date(user.createdAt).toLocaleDateString()}</small></p>
      <div style="margin-top: 1rem;">
        <button class="btn btn-danger delete-btn" data-id={user.id}>
          Eliminar
        </button>
      </div>
    </div>
  ))}
</Layout>

<script>
  // Create user
  const form = document.getElementById('create-form') as HTMLFormElement;
  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        alert('Usuario creado exitosamente');
        window.location.reload();
      } else {
        const error = await response.json();
        alert(error.error || 'Error al crear usuario');
      }
    } catch (error) {
      alert('Error al crear usuario');
    }
  });

  // Delete user
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const id = (e.target as HTMLElement).dataset.id;
      if (!confirm('¿Eliminar este usuario?')) return;

      try {
        const response = await fetch(`/api/users/${id}`, {
          method: 'DELETE'
        });

        if (response.ok) {
          alert('Usuario eliminado');
          window.location.reload();
        } else {
          alert('Error al eliminar usuario');
        }
      } catch (error) {
        alert('Error al eliminar usuario');
      }
    });
  });
</script>
```

---

## Paso 6: Configurar Nginx

### nginx/nginx.conf
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    include /etc/nginx/conf.d/*.conf;
}
```

### nginx/default.conf
```nginx
# Cache zone
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=astro_cache:10m max_size=100m inactive=60m;

upstream astro_app {
    server app:3000;
    keepalive 32;
}

server {
    listen 80;
    server_name localhost;

    # Logs
    access_log /var/log/nginx/astro_access.log;
    error_log /var/log/nginx/astro_error.log;

    # Root para archivos estáticos
    root /usr/share/nginx/html;

    # Archivos estáticos - servidos directamente por Nginx
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
        try_files $uri @astro;
    }

    # Favicon
    location = /favicon.ico {
        expires 1y;
        access_log off;
        log_not_found off;
        try_files $uri @astro;
    }

    # API routes - proxy a Astro sin caché
    location /api/ {
        proxy_pass http://astro_app;
        proxy_http_version 1.1;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_cache_bypass $http_upgrade;
        proxy_buffering off;
    }

    # SSR pages - proxy a Astro con caché opcional
    location / {
        proxy_pass http://astro_app;
        proxy_http_version 1.1;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_cache_bypass $http_upgrade;

        # Cache para páginas estáticas (opcional)
        # proxy_cache astro_cache;
        # proxy_cache_valid 200 10m;
        # proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
    }

    # Fallback a Astro
    location @astro {
        proxy_pass http://astro_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Health check directo
    location /nginx-health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

---

## Paso 7: Dockerfile para Astro

### app/Dockerfile
```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps

WORKDIR /app

COPY package*.json ./
RUN npm ci

# Stage 2: Builder
FROM node:18-alpine AS builder

WORKDIR /app

# Copy dependencies
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Generate Prisma Client
RUN npx prisma generate

# Build application
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner

WORKDIR /app

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Copy necessary files
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/prisma ./prisma

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S astro -u 1001

# Set ownership
RUN chown -R astro:nodejs /app

USER astro

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {r.statusCode === 200 ? process.exit(0) : process.exit(1)})"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start with migrations
CMD ["sh", "-c", "npx prisma migrate deploy && node ./dist/server/entry.mjs"]
```

---

## Paso 8: Docker Compose

### docker-compose.yml
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: astro-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-astro}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-astro_password}
      POSTGRES_DB: ${POSTGRES_DB:-astrodb}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-astro}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - astro-network

  # Astro Application
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: astro-app
    restart: unless-stopped
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://${POSTGRES_USER:-astro}:${POSTGRES_PASSWORD:-astro_password}@db:5432/${POSTGRES_DB:-astrodb}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - astro-network
    # Solo exponer internamente
    expose:
      - 3000

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: astro-nginx
    restart: unless-stopped
    ports:
      - "${HTTP_PORT:-80}:80"
      # - "443:443"  # Para SSL
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ./app/public:/usr/share/nginx/html:ro
      - nginx_cache:/var/cache/nginx
    depends_on:
      - app
    networks:
      - astro-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/nginx-health"]
      interval: 30s
      timeout: 3s
      retries: 3

volumes:
  postgres_data:
    driver: local
  nginx_cache:
    driver: local

networks:
  astro-network:
    driver: bridge
```

---

## Paso 9: Variables de Entorno

### .env.example
```env
# PostgreSQL
POSTGRES_USER=astro
POSTGRES_PASSWORD=astro_password
POSTGRES_DB=astrodb
POSTGRES_PORT=5432

# App
NODE_ENV=production
DATABASE_URL=postgresql://astro:astro_password@db:5432/astrodb

# Nginx
HTTP_PORT=80
```

### Crear .env
```bash
cp .env.example .env
```

---

## Paso 10: Script de Inicialización de DB (Opcional)

### init-db.sql
```sql
-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Crear función de timestamp automático
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW."updatedAt" = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

---

## Paso 11: Migración de Prisma

### Crear migración
```bash
# En desarrollo local
cd app
npx prisma migrate dev --name init

# En producción (dentro del contenedor)
docker compose exec app npx prisma migrate deploy
```

### Seed data (opcional)

### app/prisma/seed.ts
```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('Seeding database...');

  const user1 = await prisma.user.create({
    data: {
      name: 'Juan Pérez',
      email: 'juan@example.com',
      bio: 'Desarrollador Full Stack',
      posts: {
        create: [
          {
            title: 'Mi primer post',
            content: 'Contenido del primer post',
            published: true
          },
          {
            title: 'Segundo post',
            content: 'Más contenido',
            published: false
          }
        ]
      }
    }
  });

  const user2 = await prisma.user.create({
    data: {
      name: 'María García',
      email: 'maria@example.com',
      bio: 'Backend Developer',
      posts: {
        create: [
          {
            title: 'Hola mundo',
            content: 'Mi primer blog post',
            published: true
          }
        ]
      }
    }
  });

  console.log('Seed completed:', { user1, user2 });
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

### package.json (agregar script)
```json
{
  "scripts": {
    "seed": "tsx prisma/seed.ts"
  },
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

---

## Paso 12: Ejecutar el Proyecto

### Iniciar servicios
```bash
# Build y start
docker compose up -d --build

# Ver logs
docker compose logs -f

# Ver logs específicos
docker compose logs -f app
docker compose logs -f nginx
```

### Ejecutar migraciones
```bash
docker compose exec app npx prisma migrate deploy
```

### Seed database (opcional)
```bash
docker compose exec app npm run seed
```

### Verificar
```bash
# Health check
curl http://localhost/api/health

# Listar usuarios
curl http://localhost/api/users

# Crear usuario
curl -X POST http://localhost/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","bio":"Test bio"}'
```

### Abrir en navegador
```
http://localhost/
http://localhost/users
http://localhost/api/health
```

---

## Paso 13: Comandos Útiles

```bash
# Ver servicios corriendo
docker compose ps

# Reiniciar servicio específico
docker compose restart app

# Ver logs en tiempo real
docker compose logs -f app

# Ejecutar comando en contenedor
docker compose exec app sh

# Detener todo
docker compose down

# Detener y borrar volúmenes
docker compose down -v

# Rebuild sin cache
docker compose build --no-cache

# Escalar app (load balancing)
docker compose up -d --scale app=3

# Ver uso de recursos
docker stats

# Prisma Studio (GUI para DB)
docker compose exec app npx prisma studio
```

---

## Paso 14: Optimizaciones de Nginx

### Caché avanzado
```nginx
# En default.conf, agregar:
location / {
    proxy_cache astro_cache;
    proxy_cache_valid 200 10m;
    proxy_cache_valid 404 1m;
    proxy_cache_bypass $http_cache_control;
    add_header X-Cache-Status $upstream_cache_status;

    proxy_pass http://astro_app;
}
```

### Compresión Brotli (mejor que gzip)
```dockerfile
# Crear nginx/Dockerfile personalizado
FROM nginx:alpine

RUN apk add --no-cache nginx-mod-http-brotli

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
```

---

## Paso 15: Monitoreo y Logging

### Prometheus metrics (opcional)
```typescript
// app/src/pages/api/metrics.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  const metrics = `
# HELP app_uptime_seconds Application uptime in seconds
# TYPE app_uptime_seconds gauge
app_uptime_seconds ${process.uptime()}

# HELP nodejs_memory_usage_bytes Memory usage
# TYPE nodejs_memory_usage_bytes gauge
nodejs_memory_usage_bytes{type="heapUsed"} ${process.memoryUsage().heapUsed}
nodejs_memory_usage_bytes{type="heapTotal"} ${process.memoryUsage().heapTotal}
  `.trim();

  return new Response(metrics, {
    headers: { 'Content-Type': 'text/plain' }
  });
};
```

---

## Resumen de la Arquitectura

1. **Nginx (Puerto 80)**
   - Sirve archivos estáticos directamente
   - Proxy reverso para SSR y API
   - Compresión gzip
   - Caché de contenido
   - Load balancing (si escalas)

2. **Astro App (Puerto 3000 interno)**
   - API REST endpoints
   - Server-Side Rendering
   - Prisma ORM
   - Conexión a PostgreSQL

3. **PostgreSQL (Puerto 5432 interno)**
   - Base de datos relacional
   - Volumen persistente
   - Health checks

4. **Docker Network**
   - Comunicación interna entre servicios
   - Aislamiento de red

---

## Checklist del Proyecto

- [ ] Crear estructura de carpetas
- [ ] Configurar proyecto Astro
- [ ] Instalar Prisma y dependencias
- [ ] Configurar schema de Prisma
- [ ] Crear API endpoints
- [ ] Crear páginas frontend
- [ ] Configurar Nginx
- [ ] Crear Dockerfile
- [ ] Crear docker-compose.yml
- [ ] Configurar .env
- [ ] Ejecutar migraciones
- [ ] Seed database
- [ ] Probar endpoints
- [ ] Verificar archivos estáticos
- [ ] Optimizar Nginx
- [ ] Agregar monitoreo

---

¡Proyecto completo con Nginx + Astro + PostgreSQL funcionando en Docker! 🚀
