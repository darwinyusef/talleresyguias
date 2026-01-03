# Guía de Despliegue con Docker

## Índice
- [Requisitos Previos](#requisitos-previos)
- [Desarrollo Local](#desarrollo-local)
- [Producción](#producción)
- [Comandos Útiles](#comandos-útiles)
- [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

- Docker v20.10 o superior
- Docker Compose v2.0 o superior
- 2GB de RAM libre (mínimo)
- 1GB de espacio en disco

### Verificar instalación

```bash
docker --version
docker-compose --version
```

---

## Desarrollo Local

### 1. Build y ejecución

```bash
# Construir y levantar contenedor de desarrollo
docker-compose -f docker-compose.dev.yml up --build

# En segundo plano
docker-compose -f docker-compose.dev.yml up -d --build
```

### 2. Acceder a la aplicación

- **URL local**: http://localhost:4321
- **Hot reload**: Activado automáticamente
- **Logs en tiempo real**:
  ```bash
  docker-compose -f docker-compose.dev.yml logs -f
  ```

### 3. Detener desarrollo

```bash
# Detener contenedores
docker-compose -f docker-compose.dev.yml down

# Detener y eliminar volúmenes
docker-compose -f docker-compose.dev.yml down -v
```

---

## Producción

### 1. Build optimizado para producción

```bash
# Construir imagen de producción
docker-compose up --build -d
```

**Características del build de producción:**
- Multi-stage build (3 etapas)
- Usuario no-root para seguridad
- Compresión gzip habilitada
- Cache agresivo de assets
- Health checks configurados
- Logging limitado (10MB max)

### 2. Acceder a la aplicación

- **URL local**: http://localhost:3000
- **Puerto interno**: 8080 (nginx)
- **Puerto expuesto**: 3000 (configurable)

### 3. Verificar estado

```bash
# Ver estado del contenedor
docker-compose ps

# Ver logs
docker-compose logs -f portfolio

# Ver health check
docker inspect astro-portfolio --format='{{.State.Health.Status}}'
```

### 4. Detener producción

```bash
# Detener
docker-compose down

# Detener y limpiar todo
docker-compose down -v --rmi all
```

---

## Comandos Útiles

### Gestión de Contenedores

```bash
# Listar contenedores activos
docker ps

# Listar todos los contenedores
docker ps -a

# Ver logs en tiempo real
docker logs -f astro-portfolio

# Acceder al contenedor
docker exec -it astro-portfolio sh

# Reiniciar contenedor
docker-compose restart
```

### Limpieza y Mantenimiento

```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune -a

# Eliminar volúmenes sin usar
docker volume prune

# Limpieza completa del sistema
docker system prune -a --volumes
```

### Build y Cache

```bash
# Build sin cache
docker-compose build --no-cache

# Ver tamaño de la imagen
docker images astro-portfolio

# Inspeccionar capas de la imagen
docker history astro-portfolio:latest
```

---

## Despliegue en Producción

### Opción 1: Docker Compose en Servidor

```bash
# 1. Clonar repositorio en servidor
git clone <repo-url>
cd astro-portfolio

# 2. Construir y ejecutar
docker-compose up -d --build

# 3. Verificar
docker-compose ps
docker-compose logs -f
```

### Opción 2: Con Proxy Reverso (Nginx/Caddy)

**Ejemplo con nginx como proxy:**

```nginx
server {
    listen 80;
    server_name darwinyusef.com www.darwinyusef.com;

    location / {
        proxy_pass http://localhost:3000;
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

### Opción 3: Docker Registry

```bash
# 1. Tag de la imagen
docker tag astro-portfolio:latest registry.example.com/astro-portfolio:1.0.0

# 2. Push al registry
docker push registry.example.com/astro-portfolio:1.0.0

# 3. Pull y ejecutar en servidor
docker pull registry.example.com/astro-portfolio:1.0.0
docker run -d -p 3000:8080 --name portfolio registry.example.com/astro-portfolio:1.0.0
```

---

## Configuración de Variables de Entorno

### Crear archivo .env

```bash
# .env.production
NODE_ENV=production
PORT=8080
```

### Usar en docker-compose

```yaml
services:
  portfolio:
    env_file:
      - .env.production
```

---

## Troubleshooting

### Problema: El contenedor no inicia

```bash
# Ver logs completos
docker-compose logs portfolio

# Verificar si hay puertos en uso
lsof -i :3000

# Reconstruir desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Cambios no se reflejan

**En desarrollo:**
```bash
# Verificar volúmenes
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up --build
```

**En producción:**
```bash
# Rebuild completo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Health check falla

```bash
# Verificar health check
docker inspect astro-portfolio --format='{{json .State.Health}}'

# Verificar que nginx esté corriendo
docker exec astro-portfolio ps aux | grep nginx

# Verificar puerto interno
docker exec astro-portfolio curl -f http://localhost:8080/
```

### Problema: Permisos en nginx

```bash
# Verificar permisos
docker exec astro-portfolio ls -la /usr/share/nginx/html

# Verificar usuario
docker exec astro-portfolio whoami
# Debe mostrar: nginx-app
```

### Problema: Out of memory

```bash
# Limitar memoria en docker-compose.yml
services:
  portfolio:
    deploy:
      resources:
        limits:
          memory: 512M
```

---

## Optimizaciones

### 1. Build más rápido con BuildKit

```bash
# Habilitar BuildKit
export DOCKER_BUILDKIT=1

# Build
docker-compose build
```

### 2. Cache de dependencias

El Dockerfile ya está optimizado con:
- Cache de `node_modules` por etapas
- `npm ci` en lugar de `npm install`
- Limpieza de cache con `npm cache clean --force`

### 3. Imagen más pequeña

**Tamaño actual esperado:**
- Imagen final (nginx): ~25-30MB
- Imagen de desarrollo: ~400-500MB

```bash
# Ver tamaño
docker images astro-portfolio
```

---

## Seguridad

### Prácticas implementadas:

1. ✅ Usuario no-root (nginx-app)
2. ✅ Multi-stage build (menos superficie de ataque)
3. ✅ Health checks configurados
4. ✅ Security headers en nginx
5. ✅ Logs con rotación
6. ✅ .dockerignore completo

### Recomendaciones adicionales:

```bash
# Escanear vulnerabilidades
docker scan astro-portfolio:latest

# O con Trivy
trivy image astro-portfolio:latest
```

---

## Monitoreo

### Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Últimas 100 líneas
docker-compose logs --tail=100

# Desde una fecha
docker-compose logs --since 2024-01-01T00:00:00
```

### Métricas

```bash
# Ver uso de recursos
docker stats astro-portfolio

# Inspeccionar contenedor
docker inspect astro-portfolio
```

---

## CI/CD

### GitHub Actions Example

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker-compose build

      - name: Run tests
        run: docker-compose run portfolio npm test

      - name: Push to registry
        run: |
          docker tag astro-portfolio:latest ${{ secrets.REGISTRY }}/astro-portfolio:${{ github.sha }}
          docker push ${{ secrets.REGISTRY }}/astro-portfolio:${{ github.sha }}
```

---

## Contacto y Soporte

- **Documentación**: [Astro Docs](https://docs.astro.build)
- **Docker Docs**: [Docker Documentation](https://docs.docker.com)
- **Repositorio**: https://github.com/darwinyusef/darwinyusef.portfolio

---

**Última actualización**: Diciembre 2024
**Versión**: 1.0.0
