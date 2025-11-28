# Módulo: Optimización de Imágenes Docker

## Objetivo
Reducir el tamaño de imágenes Docker y mejorar tiempos de build.

---

## Índice
1. [Análisis de Imágenes](#análisis)
2. [Técnicas de Optimización](#técnicas)
3. [Multi-Stage Builds Avanzado](#multi-stage)
4. [Imágenes Base Ligeras](#imágenes-base)
5. [Build Cache](#build-cache)
6. [BuildKit](#buildkit)

---

## Análisis de Imágenes

### Ver Tamaño de Imágenes

```bash
# Listar imágenes con tamaños
docker images

# Ver capas de una imagen
docker history myapp:latest

# Análisis detallado con dive
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest myapp:latest
```

### Instalar dive (herramienta de análisis)

```bash
# macOS
brew install dive

# Linux
wget https://github.com/wagoodman/dive/releases/download/v0.11.0/dive_0.11.0_linux_amd64.deb
sudo apt install ./dive_0.11.0_linux_amd64.deb

# Uso
dive myapp:latest
```

---

## Técnicas de Optimización

### 1. Usar Imágenes Base Pequeñas

**Comparación de tamaños:**
```
ubuntu:latest        → ~77 MB
debian:slim          → ~27 MB
alpine:latest        → ~7 MB
scratch              → 0 MB (vacía)
distroless           → ~20 MB
```

**Ejemplo:**
```dockerfile
# ❌ Grande: 900 MB
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "index.js"]

# ✅ Optimizado: 150 MB
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "index.js"]
```

### 2. Multi-Stage Builds

```dockerfile
# Stage 1: Build (1.2 GB)
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production (150 MB)
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### 3. Minimizar Capas

```dockerfile
# ❌ Muchas capas
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# ✅ Una capa
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*
```

### 4. .dockerignore

```
# .dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
*.log
dist/
build/
coverage/
.vscode/
.idea/
```

### 5. Ordenar Comandos por Frecuencia de Cambio

```dockerfile
FROM node:18-alpine

WORKDIR /app

# 1. Dependencias (cambian poco) → caché
COPY package*.json ./
RUN npm ci --only=production

# 2. Código (cambia frecuentemente)
COPY . .

CMD ["node", "index.js"]
```

### 6. Limpiar en la Misma Capa

```dockerfile
# ❌ Archivos temporales permanecen en capas anteriores
FROM alpine
RUN apk add --no-cache curl
RUN curl -o archivo.tar.gz https://ejemplo.com/archivo.tar.gz
RUN tar -xzf archivo.tar.gz
RUN rm archivo.tar.gz  # No reduce tamaño de imagen

# ✅ Limpiar en la misma capa
FROM alpine
RUN apk add --no-cache curl && \
    curl -o archivo.tar.gz https://ejemplo.com/archivo.tar.gz && \
    tar -xzf archivo.tar.gz && \
    rm archivo.tar.gz
```

---

## Multi-Stage Builds Avanzado

### Ejemplo Python con Poetry

```dockerfile
# Stage 1: Dependencias
FROM python:3.11-slim AS deps
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY --from=deps /app/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 3: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "app.py"]
```

### Ejemplo React Optimizado

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Comprimir archivos estáticos
RUN apk add --no-cache gzip && \
    find /usr/share/nginx/html -type f \
    \( -name '*.js' -o -name '*.css' -o -name '*.html' \) \
    -exec gzip -k {} \;

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Imágenes Base Ligeras

### Alpine Linux

```dockerfile
FROM alpine:3.18

# Instalar dependencias
RUN apk add --no-cache \
    python3 \
    py3-pip

WORKDIR /app
COPY . .

CMD ["python3", "app.py"]
```

**Ventajas:** Muy pequeña (~7 MB)
**Desventajas:** Usa musl libc (no glibc), puede tener incompatibilidades

### Distroless (Google)

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Runtime stage
FROM gcr.io/distroless/nodejs18-debian11
WORKDIR /app
COPY --from=builder /app /app
CMD ["index.js"]
```

**Ventajas:** Sin shell, muy seguro, pequeña
**Desventajas:** Difícil de debuggear (no hay shell)

### Scratch (vacía)

```dockerfile
# Solo para binarios estáticos (Go, Rust)
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM scratch
COPY --from=builder /app/main /
CMD ["/main"]
```

---

## Build Cache

### Aprovechar el Caché de Capas

```dockerfile
FROM node:18-alpine

WORKDIR /app

# ✅ Copiar package.json primero (cambia raramente)
COPY package*.json ./
RUN npm ci

# Copiar código después (cambia frecuentemente)
COPY . .

CMD ["node", "index.js"]
```

### Cache Mounts (BuildKit)

```dockerfile
# syntax=docker/dockerfile:1

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Cache de npm
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .

CMD ["node", "index.js"]
```

### Invalidar Caché Selectivamente

```dockerfile
# Usar ARG para forzar rebuild de capas específicas
ARG CACHEBUST=1

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y package-${CACHEBUST}
```

---

## BuildKit

BuildKit es el motor de build moderno de Docker con features avanzadas.

### Habilitar BuildKit

```bash
# Una vez
DOCKER_BUILDKIT=1 docker build -t myapp .

# Permanente
echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc
```

### Features de BuildKit

**1. Build Secrets:**
```dockerfile
# syntax=docker/dockerfile:1

FROM node:18-alpine

WORKDIR /app

# Usar secret sin incluirlo en la imagen
RUN --mount=type=secret,id=npm_token \
    echo "//registry.npmjs.org/:_authToken=$(cat /run/secrets/npm_token)" > .npmrc && \
    npm install && \
    rm .npmrc
```

```bash
# Build con secret
docker build --secret id=npm_token,src=.npm_token -t myapp .
```

**2. SSH Mounts:**
```dockerfile
# syntax=docker/dockerfile:1

FROM alpine

RUN apk add --no-cache git openssh-client

# Usar SSH key del host
RUN --mount=type=ssh \
    git clone git@github.com:user/private-repo.git
```

```bash
docker build --ssh default -t myapp .
```

**3. Parallel Builds:**
BuildKit ejecuta stages independientes en paralelo automáticamente.

---

## Optimización por Lenguaje

### Node.js

```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "index.js"]
```

**Tamaño:** ~150 MB

### Python

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
USER nobody
CMD ["python", "app.py"]
```

**Tamaño:** ~200 MB

### Go

```dockerfile
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o main .

FROM scratch
COPY --from=builder /app/main /
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
CMD ["/main"]
```

**Tamaño:** ~10-20 MB

### Java

```dockerfile
FROM eclipse-temurin:17-jdk AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
CMD ["java", "-jar", "app.jar"]
```

**Tamaño:** ~200 MB

---

## Checklist de Optimización

- [ ] Usar imagen base pequeña (Alpine, Distroless)
- [ ] Multi-stage builds
- [ ] .dockerignore configurado
- [ ] Combinar comandos RUN
- [ ] Ordenar por frecuencia de cambio
- [ ] Limpiar archivos temporales en misma capa
- [ ] Usar --no-cache para package managers
- [ ] No incluir archivos de desarrollo
- [ ] Ejecutar como usuario no-root
- [ ] Analizar con dive
- [ ] Habilitar BuildKit
- [ ] Usar cache mounts cuando sea posible

---

## Comparación Antes/Después

### Antes (2.1 GB):
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build
CMD ["node", "dist/index.js"]
```

### Después (80 MB):
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

**Reducción: 96%**

---

## Herramientas Útiles

```bash
# Analizar capas
docker history --no-trunc myapp:latest

# Ver espacio usado
docker system df

# Limpiar todo
docker system prune -a

# Dive (análisis interactivo)
dive myapp:latest

# Docker slim (optimización automática)
docker-slim build --target myapp:latest
```

---

¡Optimizar imágenes reduce costos de almacenamiento, ancho de banda y tiempos de despliegue!
