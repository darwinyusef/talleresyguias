# Proyecto 4: Frontend con React

## Objetivo
Crear y desplegar una aplicación React usando Docker con builds optimizados.

## Prerrequisitos
- Proyectos anteriores completados
- Node.js instalado localmente (para crear el proyecto)
- Conocimientos básicos de React

---

## Paso 1: Crear Aplicación React

```bash
mkdir -p ~/curso-docker/proyectos/04-react-frontend
cd ~/curso-docker/proyectos/04-react-frontend

# Crear app con Vite (recomendado - más rápido)
npm create vite@latest . -- --template react

# O con Create React App (tradicional)
# npx create-react-app .

# Instalar dependencias
npm install
```

## Paso 2: Estructura del Proyecto

Después de crear con Vite:
```
04-react-frontend/
├── public/
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── ...
├── index.html
├── package.json
├── vite.config.js
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yml
├── .dockerignore
└── nginx.conf
```

## Paso 3: Dockerfile Multi-Stage para Producción

```dockerfile
# Stage 1: Build de la aplicación
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente
COPY . .

# Build de producción
RUN npm run build

# Stage 2: Servir con Nginx
FROM nginx:alpine

# Copiar build desde stage anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer puerto 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Nginx se ejecuta automáticamente
CMD ["nginx", "-g", "daemon off;"]
```

**Notas importantes:**
- `npm ci` es más rápido y confiable que `npm install` para CI/CD
- `dist/` es el directorio de output de Vite (con CRA sería `build/`)
- Multi-stage reduce significativamente el tamaño de la imagen

## Paso 4: Dockerfile para Desarrollo

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# El código se monta como volumen, no se copia

EXPOSE 5173

# Vite dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Si usas CRA en lugar de Vite:
# EXPOSE 3000
# CMD ["npm", "start"]
```

## Paso 5: Crear nginx.conf

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Manejar rutas de React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Caché para assets estáticos con hash
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # No cachear index.html
    location = /index.html {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }

    # Compresión gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/json
        application/x-javascript
        text/xml
        application/xml
        application/xml+rss
        image/svg+xml;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

## Paso 6: Crear .dockerignore

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.env.local
.env.development
.env.production
dist
build
.DS_Store
coverage
.vscode
.idea
*.log
```

## Paso 7: Docker Compose

```yaml
version: '3.8'

services:
  # Producción
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    container_name: react-app-prod
    restart: unless-stopped
    profiles:
      - production

  # Desarrollo con hot reload
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"  # Puerto de Vite (3000 para CRA)
    volumes:
      - ./src:/app/src
      - ./public:/app/public
      - ./index.html:/app/index.html
      - ./vite.config.js:/app/vite.config.js
    container_name: react-app-dev
    environment:
      - NODE_ENV=development
    profiles:
      - development
```

## Paso 8: Construir y Ejecutar

**Modo Producción:**
```bash
# Build
docker build -t react-app:v1 .

# Run
docker run -d \
  --name react-container \
  -p 8080:80 \
  react-app:v1

# Verificar
curl http://localhost:8080
```

**Modo Desarrollo:**
```bash
# Build dev image
docker build -f Dockerfile.dev -t react-app-dev .

# Run con hot reload
docker run -d \
  --name react-dev \
  -p 5173:5173 \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/public:/app/public \
  react-app-dev

# Con Docker Compose
docker compose --profile development up -d
```

**Probar en navegador:**
```
Producción: http://localhost:8080
Desarrollo: http://localhost:5173
```

---

## Variables de Entorno

### Con Vite

**Crear archivos .env:**

`.env.development`:
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Mi App React Dev
```

`.env.production`:
```env
VITE_API_URL=https://api.midominio.com
VITE_APP_NAME=Mi App React
```

**Usar en código:**
```javascript
// src/config.js
export const config = {
  apiUrl: import.meta.env.VITE_API_URL,
  appName: import.meta.env.VITE_APP_NAME,
}

// src/App.jsx
import { config } from './config'

function App() {
  console.log('API URL:', config.apiUrl)
  // ...
}
```

**Pasar variables en Docker:**

Método 1 - Build arguments:
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

ARG VITE_API_URL
ARG VITE_APP_NAME

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_APP_NAME=$VITE_APP_NAME

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ... resto del Dockerfile
```

```bash
docker build \
  --build-arg VITE_API_URL=https://api.ejemplo.com \
  --build-arg VITE_APP_NAME="Mi App" \
  -t react-app:v1 .
```

Método 2 - Runtime con script:
```dockerfile
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY env.sh /docker-entrypoint.d/env.sh
RUN chmod +x /docker-entrypoint.d/env.sh

EXPOSE 80
```

`env.sh`:
```bash
#!/bin/sh

# Reemplazar variables de entorno en archivos JS
for file in /usr/share/nginx/html/assets/*.js; do
  if [ -f "$file" ]; then
    sed -i "s|VITE_API_URL_PLACEHOLDER|${VITE_API_URL}|g" "$file"
  fi
done
```

---

## React Router

Si usas React Router, Nginx ya está configurado correctamente con:
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

**Instalar React Router:**
```bash
npm install react-router-dom
```

**Ejemplo básico:**
```javascript
// src/App.jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  )
}

function Home() {
  return <h1>Home Page</h1>
}

function About() {
  return <h1>About Page</h1>
}
```

---

## Integración con API (FastAPI del Proyecto 3)

**docker-compose.yml completo:**
```yaml
version: '3.8'

services:
  # Backend API (FastAPI)
  api:
    build: ../03-fastapi
    container_name: fastapi-api
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    networks:
      - app-network

  # Frontend React (Producción)
  frontend:
    build: .
    container_name: react-frontend
    ports:
      - "80:80"
    depends_on:
      - api
    networks:
      - app-network
    environment:
      - VITE_API_URL=http://api:8000

networks:
  app-network:
    driver: bridge
```

**Proxy API con Nginx:**

Actualizar `nginx.conf`:
```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    # Servir React app
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy a API backend
    location /api/ {
        proxy_pass http://api:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Uso en React:**
```javascript
// En lugar de http://localhost:8000/items
// Usa /api/items

async function fetchItems() {
  const response = await fetch('/api/items')
  const data = await response.json()
  return data
}
```

---

## Optimizaciones de Build

### 1. Análisis de Bundle

```bash
# Instalar analizador
npm install -D vite-plugin-visualizer

# Agregar a vite.config.js
import { visualizer } from 'vite-plugin-visualizer'

export default {
  plugins: [
    visualizer({ open: true })
  ]
}
```

### 2. Code Splitting

```javascript
// Lazy loading de componentes
import { lazy, Suspense } from 'react'

const About = lazy(() => import('./pages/About'))

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <About />
    </Suspense>
  )
}
```

### 3. Optimizar Dockerfile

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Cachear dependencias
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .

# Build optimizado
RUN npm run build

# Stage mínimo
FROM nginx:alpine

# Copiar solo archivos necesarios
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Comprimir assets
RUN apk add --no-cache gzip && \
    find /usr/share/nginx/html -type f \( -name '*.js' -o -name '*.css' \) \
    -exec gzip -k {} \;

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Testing en Docker

**Dockerfile.test:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Ejecutar tests
CMD ["npm", "run", "test"]
```

**Configurar Vitest (para Vite):**
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

**vite.config.js:**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
  },
})
```

**Ejecutar tests:**
```bash
docker build -f Dockerfile.test -t react-test .
docker run --rm react-test
```

---

## Deployment con Nginx Optimizado

**Configuración avanzada nginx.conf:**
```nginx
# Configuración de compresión
gzip on;
gzip_static on;  # Servir archivos .gz pre-comprimidos
gzip_types text/plain text/css text/js text/xml text/javascript application/javascript application/json application/xml+rss;
gzip_vary on;

# Límites
client_max_body_size 10M;

server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Caché para assets
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # No caché para index.html
    location = /index.html {
        expires -1;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}
```

---

## Ejercicios Prácticos

### Ejercicio 1: App con Fetch
Crea una app que:
- Consuma la API de FastAPI del Proyecto 3
- Muestre lista de items
- Permita crear, editar, eliminar items
- Use loading states
- Maneje errores

### Ejercicio 2: Estado Global
Implementa estado global con Context API o Zustand:
```bash
npm install zustand
```

### Ejercicio 3: Dark Mode
- Agregar toggle de dark/light mode
- Persistir preferencia en localStorage
- Usar CSS variables

### Ejercicio 4: PWA
Convierte tu app en PWA:
```bash
npm install vite-plugin-pwa -D
```

---

## Debugging

**Ver logs de Nginx:**
```bash
docker exec react-container cat /var/log/nginx/access.log
docker exec react-container cat /var/log/nginx/error.log
```

**Inspeccionar build:**
```bash
# Entrar al contenedor
docker run -it --rm react-app:v1 sh

# Ver archivos
ls -la /usr/share/nginx/html

# Ver tamaño
du -sh /usr/share/nginx/html/*
```

**Verificar variables de entorno:**
```bash
docker exec react-container env
```

---

## Troubleshooting

### Página en blanco
```bash
# Verificar logs de Nginx
docker logs react-container

# Verificar que archivos están en el contenedor
docker exec react-container ls -la /usr/share/nginx/html

# Verificar consola del navegador (F12)
```

### React Router no funciona (404 en refresh)
Verificar nginx.conf tiene:
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

### Build muy lento
```bash
# Limpiar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install

# Usar .dockerignore correctamente
# Verificar que node_modules está excluido
```

### Imagen muy grande
```bash
# Ver tamaño de imagen
docker images react-app:v1

# Usar multi-stage build
# Usar Alpine en lugar de full Node
# Limpiar caché de npm
```

---

## Resumen de Comandos

```bash
# Crear proyecto
npm create vite@latest . -- --template react
npm install

# Build Docker producción
docker build -t react-app:v1 .
docker run -d --name react-container -p 8080:80 react-app:v1

# Desarrollo
docker build -f Dockerfile.dev -t react-app-dev .
docker run -d --name react-dev -p 5173:5173 \
  -v $(pwd)/src:/app/src react-app-dev

# Docker Compose
docker compose --profile development up -d  # Desarrollo
docker compose --profile production up -d   # Producción

# Ver logs
docker logs -f react-container

# Limpiar
docker stop react-container && docker rm react-container
docker compose down
```

---

## Checklist del Proyecto

- [ ] Crear proyecto React con Vite
- [ ] Desarrollar componentes y funcionalidad
- [ ] Crear Dockerfile multi-stage
- [ ] Crear Dockerfile.dev
- [ ] Crear nginx.conf
- [ ] Crear .dockerignore
- [ ] Construir imagen de producción
- [ ] Probar en modo producción (puerto 8080)
- [ ] Configurar modo desarrollo con hot reload
- [ ] Crear docker-compose.yml
- [ ] Integrar con API backend
- [ ] Configurar variables de entorno
- [ ] Implementar React Router
- [ ] Optimizar bundle size
- [ ] Escribir tests

---

## Siguiente Paso

Continúa con:
**[Proyecto 5: Backend con Node.js + TypeScript](./05-node-typescript.md)**
