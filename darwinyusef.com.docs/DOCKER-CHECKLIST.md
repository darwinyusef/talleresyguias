# Checklist de Verificación Docker

## Pre-despliegue

### 1. Archivos Creados ✓

- [x] `Dockerfile` - Producción optimizado
- [x] `Dockerfile.dev` - Desarrollo con hot reload
- [x] `docker-compose.yml` - Configuración de producción
- [x] `docker-compose.dev.yml` - Configuración de desarrollo
- [x] `.dockerignore` - Archivos a ignorar en build
- [x] `nginx.conf` - Configuración de nginx
- [x] `.env.example` - Variables de entorno ejemplo
- [x] `Makefile` - Comandos simplificados
- [x] `start.sh` - Script de inicio interactivo
- [x] `DOCKER-DEPLOY.md` - Documentación completa

### 2. Validación de Configuración

```bash
# Verificar sintaxis de docker-compose
docker compose config --quiet

# Verificar que el Dockerfile es válido
docker build -t test-build .

# Limpiar test
docker rmi test-build
```

### 3. Test Local

#### Desarrollo
```bash
# Opción 1: Usando Makefile
make dev

# Opción 2: Usando script
./start.sh

# Opción 3: Docker compose directo
docker compose -f docker-compose.dev.yml up --build

# Verificar en: http://localhost:4321
```

#### Producción
```bash
# Opción 1: Usando Makefile
make prod

# Opción 2: Usando script
./start.sh

# Opción 3: Docker compose directo
docker compose up -d --build

# Verificar en: http://localhost:3000
```

### 4. Verificaciones de Seguridad

```bash
# 1. Verificar que no corre como root
docker exec astro-portfolio whoami
# Debe mostrar: nginx-app

# 2. Verificar health check
docker inspect astro-portfolio --format='{{.State.Health.Status}}'
# Debe mostrar: healthy

# 3. Verificar puerto (no debe ser 80 privilegiado)
docker inspect astro-portfolio --format='{{.Config.ExposedPorts}}'
# Debe mostrar: 8080/tcp

# 4. Escanear vulnerabilidades (opcional pero recomendado)
docker scan astro-portfolio:latest
# o
trivy image astro-portfolio:latest
```

### 5. Verificaciones de Performance

```bash
# 1. Tamaño de imagen (debe ser <50MB para producción)
docker images astro-portfolio
# Esperado: ~25-30MB

# 2. Ver capas de la imagen
docker history astro-portfolio:latest

# 3. Tiempo de build (primera vez)
time docker compose build

# 4. Tiempo de inicio del contenedor
docker stats astro-portfolio --no-stream
```

### 6. Verificaciones Funcionales

```bash
# 1. Verificar que los assets se sirven correctamente
curl -I http://localhost:3000/

# 2. Verificar compresión gzip
curl -H "Accept-Encoding: gzip" -I http://localhost:3000/

# 3. Verificar headers de seguridad
curl -I http://localhost:3000/ | grep -i "x-frame-options\|x-content-type"

# 4. Verificar que el routing funciona (SPA)
curl http://localhost:3000/about
curl http://localhost:3000/projects

# 5. Verificar logs
docker compose logs --tail=50
```

### 7. Tests Multi-idioma

```bash
# Si tienes configurado subdominios locales:

# Español
curl http://localhost:3000/

# Inglés (si aplica)
curl http://en.localhost:3000/

# Portugués (si aplica)
curl http://br.localhost:3000/
```

## Despliegue

### Pre-despliegue

- [ ] Variables de entorno configuradas
- [ ] Dominio apuntando al servidor
- [ ] SSL/TLS configurado (Certbot/Let's Encrypt)
- [ ] Firewall configurado (puertos 80, 443)
- [ ] Backup del servidor configurado

### Comandos de Despliegue

```bash
# 1. En el servidor, clonar el repo
git clone <repo-url>
cd astro-portfolio

# 2. Configurar variables de entorno
cp .env.example .env
nano .env

# 3. Construir y ejecutar
docker compose up -d --build

# 4. Verificar que está corriendo
docker compose ps
docker compose logs -f

# 5. Verificar health check
docker inspect astro-portfolio --format='{{.State.Health.Status}}'
```

### Post-despliegue

```bash
# 1. Verificar desde internet
curl https://darwinyusef.com

# 2. Verificar SSL
curl -I https://darwinyusef.com | grep -i "strict-transport"

# 3. Test de rendimiento
curl -w "@curl-format.txt" -o /dev/null -s https://darwinyusef.com

# 4. Configurar auto-restart
docker update --restart=always astro-portfolio
```

## Monitoreo Continuo

### Comandos útiles

```bash
# Ver logs en tiempo real
docker compose logs -f

# Ver uso de recursos
docker stats astro-portfolio

# Ver health check
watch -n 5 'docker inspect astro-portfolio --format="{{.State.Health.Status}}"'

# Backup de logs
docker compose logs > logs-$(date +%Y%m%d).txt
```

### Alertas a configurar

- [ ] Monitor de uptime (UptimeRobot, Pingdom, etc.)
- [ ] Alertas de uso de CPU/memoria
- [ ] Alertas de espacio en disco
- [ ] Logs centralizados (opcional)

## Troubleshooting

### Si el contenedor no inicia:

```bash
# 1. Ver logs detallados
docker compose logs portfolio

# 2. Verificar permisos
docker exec astro-portfolio ls -la /usr/share/nginx/html

# 3. Rebuild desde cero
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Si el health check falla:

```bash
# 1. Verificar nginx está corriendo
docker exec astro-portfolio ps aux | grep nginx

# 2. Test manual del health check
docker exec astro-portfolio curl -f http://localhost:8080/

# 3. Ver logs de nginx
docker exec astro-portfolio cat /var/log/nginx/error.log
```

### Si hay problemas de performance:

```bash
# 1. Ver stats en tiempo real
docker stats astro-portfolio

# 2. Limitar recursos (si es necesario)
# Editar docker-compose.yml:
#   deploy:
#     resources:
#       limits:
#         cpus: '0.5'
#         memory: 512M

# 3. Verificar cache de nginx
curl -I http://localhost:3000/assets/main.js | grep -i cache
```

## Comandos Rápidos de Referencia

```bash
# Ver todos los comandos disponibles
make help

# Inicio rápido desarrollo
make dev

# Inicio rápido producción
make prod

# Ver estado
make ps

# Ver logs
make logs

# Limpiar todo
make clean

# Acceder al shell del contenedor
make shell

# Ver health check
make health

# Ver estadísticas
make stats
```

## Notas Importantes

1. **Puerto 3000 vs 8080**:
   - Puerto expuesto al host: 3000
   - Puerto interno del contenedor: 8080
   - En producción con proxy reverso, mapear según necesidad

2. **Usuario no-root**:
   - El contenedor corre como `nginx-app` (UID 1001)
   - Esto mejora la seguridad pero requiere permisos correctos

3. **Health checks**:
   - Intervalo: 30s
   - Timeout: 3s
   - Reintentos: 3
   - Start period: 10s (para dar tiempo al inicio)

4. **Logs**:
   - Rotación automática (max 10MB por archivo)
   - Máximo 3 archivos
   - Limpiar periódicamente con `docker system prune`

5. **Build cache**:
   - El Dockerfile usa multi-stage build
   - Cache de npm optimizado por etapas
   - Si hay problemas, usar `--no-cache`

---

**Última actualización**: Diciembre 2024
**Versión**: 1.0.0
