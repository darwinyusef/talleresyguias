# ⚡ Comandos Rápidos - Portfolio

Referencia rápida de comandos para desarrollo y producción.

---

## 🏠 En tu Computadora Local

### Desarrollo

```bash
# Instalar dependencias
npm install

# Iniciar servidor desarrollo
npm run dev                    # http://localhost:4321

# Build
npm run build

# Preview del build
npm run preview                # http://localhost:4321

# Lint
npm run lint

# Format
npm run format
```

### Docker Local

```bash
# Desarrollo
docker-compose -f docker-compose.dev.yml up
docker-compose -f docker-compose.dev.yml up -d        # Background
docker-compose -f docker-compose.dev.yml down         # Detener

# Producción local
docker-compose up -d --build
docker-compose down
docker-compose logs -f

# Rebuild desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Makefile (Shortcuts)

```bash
make dev           # Docker desarrollo
make dev-d         # Docker desarrollo (background)
make dev-down      # Detener desarrollo
make dev-logs      # Ver logs desarrollo

make build         # Build producción
make prod          # Iniciar producción
make up            # Alias de prod
make down          # Detener
make restart       # Reiniciar

make logs          # Ver logs
make ps            # Ver estado contenedores
make shell         # Acceder al contenedor
make health        # Ver health check
make stats         # Ver estadísticas

make clean         # Limpiar contenedores y volúmenes
make clean-all     # Limpieza completa
make prune         # Limpiar recursos no usados

make info          # Info del proyecto
make help          # Ver ayuda
```

---

## 🖥️ En el Servidor (YOUR_SERVER_IP)

### Conexión

```bash
# Conectar
ssh root@YOUR_SERVER_IP

# SCP (copiar archivos)
scp archivo.txt root@YOUR_SERVER_IP:/opt/portfolio/
scp -r carpeta/ root@YOUR_SERVER_IP:/opt/portfolio/
```

### Navegación

```bash
# Ir al proyecto
cd /opt/portfolio/astro-portfolio

# Ver estructura
ls -la
tree -L 2

# Buscar archivos
find . -name "*.astro"
find . -type f -name "package.json"
```

### Git

```bash
# Pull últimos cambios
git pull origin main

# Ver estado
git status
git log --oneline -5

# Ver diferencias
git diff

# Cambiar de rama
git checkout develop
git checkout main
```

### Docker

```bash
# Ver contenedores
docker ps
docker ps -a

# Logs
docker logs astro-portfolio
docker logs -f astro-portfolio              # Follow
docker logs --tail 50 astro-portfolio       # Últimas 50 líneas
docker logs --since 10m astro-portfolio     # Últimos 10 minutos

# Ejecutar comandos en contenedor
docker exec -it astro-portfolio sh
docker exec astro-portfolio ls -la /usr/share/nginx/html

# Reiniciar
docker restart astro-portfolio

# Detener/Iniciar
docker stop astro-portfolio
docker start astro-portfolio

# Eliminar
docker stop astro-portfolio
docker rm astro-portfolio

# Stats
docker stats astro-portfolio
docker stats --no-stream

# Inspect
docker inspect astro-portfolio
docker inspect astro-portfolio | grep IPAddress
```

### Docker Compose

```bash
# En /opt/portfolio/astro-portfolio
cd /opt/portfolio/astro-portfolio

# Up
docker-compose up -d
docker-compose up -d --build                # Build + Up

# Down
docker-compose down
docker-compose down -v                      # Con volúmenes

# Logs
docker-compose logs
docker-compose logs -f
docker-compose logs -f portfolio

# Restart
docker-compose restart
docker-compose restart portfolio

# Estado
docker-compose ps

# Rebuild
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

### Deployment

```bash
# Deploy completo (script)
portfolio-deploy

# O manualmente
cd /opt/portfolio
git pull
cd astro-portfolio
docker-compose down
docker-compose up -d --build

# Verificar
docker ps
curl http://localhost:3000
```

### Nginx

```bash
# Test configuración
nginx -t

# Reload (sin downtime)
systemctl reload nginx

# Restart
systemctl restart nginx

# Estado
systemctl status nginx

# Logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/portfolio-access.log
tail -f /var/log/nginx/portfolio-error.log

# Ver últimas 50 líneas
tail -50 /var/log/nginx/portfolio-error.log

# Buscar errores
grep "error" /var/log/nginx/portfolio-error.log
grep "502" /var/log/nginx/portfolio-access.log
```

### SSL / Certbot

```bash
# Ver certificados
certbot certificates

# Renovar manualmente
certbot renew

# Test renovación
certbot renew --dry-run

# Forzar renovación
certbot renew --force-renewal

# Renovar dominio específico
certbot renew --cert-name darwinyusef.com

# Eliminar certificado
certbot delete --cert-name darwinyusef.com
```

### Firewall (UFW)

```bash
# Estado
ufw status
ufw status verbose

# Habilitar/Deshabilitar
ufw enable
ufw disable

# Permitir puerto
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow ssh

# Denegar puerto
ufw deny 8080/tcp

# Eliminar regla
ufw delete allow 8080/tcp

# Reset (cuidado!)
ufw reset
```

### Sistema

```bash
# Actualizar
apt update
apt upgrade -y

# Ver espacio en disco
df -h
du -sh /opt/portfolio
du -sh /var/lib/docker

# Ver memoria
free -h
cat /proc/meminfo

# Ver CPU
top
htop
nproc

# Ver procesos
ps aux | grep docker
ps aux | grep nginx

# Ver puertos abiertos
netstat -tulpn
ss -tulpn
lsof -i :3000
```

### Limpieza

```bash
# Docker
docker system prune -a              # Todo
docker image prune -a               # Imágenes
docker container prune              # Contenedores
docker volume prune                 # Volúmenes

# Logs
journalctl --vacuum-time=7d         # Logs sistema
truncate -s 0 /var/log/nginx/access.log

# APT
apt autoremove
apt autoclean
```

### Backups

```bash
# Backup manual
tar -czf portfolio-backup-$(date +%Y%m%d).tar.gz /opt/portfolio

# Backup de .env
cp /opt/portfolio/astro-portfolio/.env /opt/backups/.env-$(date +%Y%m%d)

# Backup de base de datos (si aplica)
# mysqldump -u root -p database > backup.sql

# Restaurar
tar -xzf portfolio-backup-20260102.tar.gz -C /
```

---

## 🔧 Jenkins

### Navegador
```
http://YOUR_SERVER_IP:8080
```

### CLI (en servidor)

```bash
# Si Jenkins está en Docker
docker logs jenkins
docker exec -it jenkins bash

# Trigger build manualmente
curl -X POST http://localhost:8080/job/portfolio-deploy/build \
  --user USER:TOKEN
```

---

## 📦 Minio

### Navegador
```
http://YOUR_SERVER_IP:9000
```

### CLI (mc - Minio Client)

```bash
# Instalar
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
mv mc /usr/local/bin/

# Configurar alias
mc alias set myminio http://localhost:9000 ACCESS_KEY SECRET_KEY

# Listar buckets
mc ls myminio

# Listar archivos
mc ls myminio/portfolio

# Upload
mc cp image.jpg myminio/portfolio/images/
mc cp --recursive ./images/ myminio/portfolio/

# Download
mc cp myminio/portfolio/image.jpg ./

# Eliminar
mc rm myminio/portfolio/old-image.jpg

# Permisos públicos
mc policy set download myminio/portfolio
```

---

## 🐛 Troubleshooting

### Contenedor no inicia
```bash
docker logs astro-portfolio
docker-compose down -v
docker-compose up -d --build
```

### Puerto 3000 en uso
```bash
lsof -i :3000
kill -9 <PID>
```

### Nginx 502 Bad Gateway
```bash
# Verificar que contenedor está corriendo
docker ps | grep astro-portfolio

# Test endpoint
curl http://localhost:3000

# Restart
docker restart astro-portfolio
systemctl reload nginx
```

### Sin espacio en disco
```bash
df -h
docker system prune -a
apt autoremove
journalctl --vacuum-time=3d
```

### Certificado SSL expirado
```bash
certbot renew --force-renewal
systemctl reload nginx
```

---

## 📊 Monitoreo

```bash
# Watch (actualizar cada 2 segundos)
watch -n 2 docker ps

# Logs en tiempo real
tail -f /var/log/nginx/portfolio-access.log | grep -v "bot"

# Stats en tiempo real
docker stats astro-portfolio

# Requests por minuto
tail -10000 /var/log/nginx/portfolio-access.log | awk '{print $4}' | cut -d: -f1-2 | sort | uniq -c

# Top IPs
awk '{print $1}' /var/log/nginx/portfolio-access.log | sort | uniq -c | sort -nr | head -10

# Errores 404
grep "404" /var/log/nginx/portfolio-access.log | tail -20
```

---

## 🚀 Deploy Rápido

### Método 1: Script automático
```bash
ssh root@YOUR_SERVER_IP
portfolio-deploy
```

### Método 2: Manual
```bash
ssh root@YOUR_SERVER_IP
cd /opt/portfolio && git pull && cd astro-portfolio && docker-compose down && docker-compose up -d --build
```

### Método 3: Desde local
```bash
git push origin main
# GitHub Actions + Jenkins harán el resto automáticamente
```

---

## 📱 URLs Rápidas

```bash
# Portfolio
https://darwinyusef.com
http://YOUR_SERVER_IP:3000

# Jenkins
http://YOUR_SERVER_IP:8080

# Minio
http://YOUR_SERVER_IP:9000

# GitHub
https://github.com/darwinyusef/darwinyusef.portfolio
```

---

**💡 Tip:** Guarda este archivo como referencia o imprime la sección que más uses.
