# 🐳 Setup 100% con Docker - Sin instalar nada en el servidor

Todo corre en contenedores Docker. No se instala Nginx, Certbot, ni nada en el servidor.

---

## ✅ Qué incluye

```
┌─────────────────────────────────────────┐
│  Solo Docker instalado en el servidor  │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────┐          │
│  │  Contenedor 1: Nginx     │          │
│  │  Reverse Proxy + SSL     │          │
│  │  Puertos: 80, 443        │          │
│  └──────────────────────────┘          │
│             ↓                           │
│  ┌──────────────────────────┐          │
│  │  Contenedor 2: Portfolio │          │
│  │  Astro + Nginx Alpine    │          │
│  │  Puerto interno: 8080    │          │
│  └──────────────────────────┘          │
│                                         │
│  ┌──────────────────────────┐          │
│  │  Contenedor 3: Certbot   │          │
│  │  Renovación SSL auto     │          │
│  └──────────────────────────┘          │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🚀 Inicio Rápido

### Paso 1: Conectar al Servidor

```bash
ssh root@YOUR_SERVER_IP
```

### Paso 2: Instalar Docker (solo esto)

```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt install docker-compose -y

# Verificar
docker --version
docker-compose --version
```

### Paso 3: Clonar Proyecto

```bash
# Crear directorio
mkdir -p /opt/portfolio
cd /opt/portfolio

# Clonar
git clone https://github.com/darwinyusef/darwinyusef.portfolio.git .

# Ir al directorio
cd astro-portfolio
```

### Paso 4: Configurar Variables de Entorno

```bash
# Copiar ejemplo
cp .env.example .env

# Editar
nano .env
```

**Configuración mínima:**

```bash
# App
NODE_ENV=production
SITE_URL=https://darwinyusef.com

# Gmail SMTP
GMAIL_USER=wsgestor@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Email
EMAIL_FROM=no-reply@aquicreamos.com
EMAIL_FROM_NAME=Darwin Yusef
EMAIL_TO=wsgestor@gmail.com
EMAIL_REPLY_TO=contacto@aquicreamos.com
```

### Paso 5: Configurar Dominio

**En nginx-proxy.conf, actualiza:**

```nginx
server_name TU_DOMINIO.com www.TU_DOMINIO.com;
```

A:

```nginx
server_name darwinyusef.com www.darwinyusef.com;
```

### Paso 6: Deploy (Automático)

```bash
# Dar permisos al script
chmod +x scripts/setup-docker-only.sh

# Ejecutar
./scripts/setup-docker-only.sh
```

**O manual:**

```bash
# Crear directorios
mkdir -p certbot/conf certbot/www

# Build y deploy
docker-compose -f docker-compose.production.yml up -d --build

# Ver logs
docker-compose -f docker-compose.production.yml logs -f
```

---

## 🔐 Configurar SSL

### Método 1: Durante setup (automático)

El script `setup-docker-only.sh` te guiará.

### Método 2: Manual

```bash
# 1. Asegúrate de que los contenedores están corriendo
docker ps

# 2. Obtener certificado
docker-compose -f docker-compose.production.yml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email wsgestor@gmail.com \
  --agree-tos \
  --no-eff-email \
  -d darwinyusef.com \
  -d www.darwinyusef.com

# 3. Editar nginx-proxy.conf
nano nginx-proxy.conf
```

**Cambios en nginx-proxy.conf:**

1. En la sección HTTP, cambiar:
```nginx
location / {
    proxy_pass http://portfolio_backend;
    # ... resto
}
```

A:
```nginx
location / {
    return 301 https://$server_name$request_uri;
}
```

2. Descomentar toda la sección HTTPS (quitar los #)

```bash
# 4. Reiniciar nginx
docker-compose -f docker-compose.production.yml restart nginx

# 5. Verificar
curl -I https://darwinyusef.com
```

---

## 📋 Comandos Útiles

### Ver Estado

```bash
# Ver todos los contenedores del proyecto
docker ps --filter "label=com.docker.compose.project=portfolio"

# Ver logs
docker-compose -f docker-compose.production.yml logs -f

# Logs de un servicio específico
docker-compose -f docker-compose.production.yml logs -f portfolio
docker-compose -f docker-compose.production.yml logs -f nginx
docker-compose -f docker-compose.production.yml logs -f certbot
```

### Gestión

```bash
# Reiniciar todo
docker-compose -f docker-compose.production.yml restart

# Reiniciar un servicio
docker-compose -f docker-compose.production.yml restart nginx

# Detener todo
docker-compose -f docker-compose.production.yml down

# Rebuild y restart
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d --build
```

### SSL/Certificados

```bash
# Renovar certificados (manual)
docker-compose -f docker-compose.production.yml run --rm certbot renew

# Ver certificados
docker-compose -f docker-compose.production.yml run --rm certbot certificates

# Test de renovación
docker-compose -f docker-compose.production.yml run --rm certbot renew --dry-run
```

### Acceder a Contenedores

```bash
# Nginx
docker exec -it portfolio-nginx sh

# Portfolio
docker exec -it astro-portfolio sh

# Ver archivos nginx
docker exec portfolio-nginx cat /etc/nginx/conf.d/default.conf

# Ver logs nginx
docker exec portfolio-nginx tail -f /var/log/nginx/portfolio-access.log
```

### Limpieza

```bash
# Limpiar todo
docker-compose -f docker-compose.production.yml down -v

# Limpiar imágenes antiguas
docker image prune -a -f

# Limpiar todo Docker
docker system prune -a --volumes
```

---

## 🔄 Actualizar Código

```bash
# En el servidor
cd /opt/portfolio/astro-portfolio

# Pull cambios
git pull origin main

# Rebuild y restart
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d --build

# Ver logs
docker-compose -f docker-compose.production.yml logs -f portfolio
```

---

## 🐛 Troubleshooting

### Contenedor no inicia

```bash
# Ver logs
docker-compose -f docker-compose.production.yml logs portfolio

# Ver estado
docker ps -a

# Rebuild sin cache
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d
```

### Nginx error

```bash
# Test configuración
docker exec portfolio-nginx nginx -t

# Ver logs
docker logs portfolio-nginx

# Restart
docker-compose -f docker-compose.production.yml restart nginx
```

### SSL no funciona

```bash
# Verificar certificados
ls -la certbot/conf/live/darwinyusef.com/

# Ver logs certbot
docker-compose -f docker-compose.production.yml logs certbot

# Intentar obtener certificado manualmente
docker-compose -f docker-compose.production.yml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email wsgestor@gmail.com \
  --agree-tos \
  -d darwinyusef.com \
  -d www.darwinyusef.com \
  --dry-run  # Quitar --dry-run cuando funcione
```

### Puerto 80/443 en uso

```bash
# Ver qué está usando los puertos
netstat -tulpn | grep :80
netstat -tulpn | grep :443

# O con ss
ss -tulpn | grep :80

# Detener lo que esté usando esos puertos
systemctl stop nginx  # Si hay nginx instalado en el host
```

---

## 📊 Verificación Final

```bash
# 1. DNS
dig darwinyusef.com +short
# Debe mostrar: YOUR_SERVER_IP

# 2. Contenedores
docker ps
# Debe mostrar: portfolio-nginx, astro-portfolio, portfolio-certbot

# 3. HTTP
curl -I http://darwinyusef.com
# Debe devolver 200 o 301 (redirect a HTTPS)

# 4. HTTPS
curl -I https://darwinyusef.com
# Debe devolver 200

# 5. Certificado
docker-compose -f docker-compose.production.yml run --rm certbot certificates
# Debe mostrar certificado válido

# 6. Logs
docker-compose -f docker-compose.production.yml logs --tail=50
# No debe haber errores
```

---

## ✅ Checklist

- [ ] Docker instalado en servidor
- [ ] Proyecto clonado en /opt/portfolio/astro-portfolio
- [ ] .env configurado
- [ ] nginx-proxy.conf actualizado con tu dominio
- [ ] DNS apunta a tu servidor
- [ ] Contenedores corriendo (docker ps)
- [ ] HTTP funciona (curl http://darwinyusef.com)
- [ ] Certificado SSL obtenido
- [ ] nginx-proxy.conf actualizado para HTTPS
- [ ] HTTPS funciona (curl https://darwinyusef.com)
- [ ] Firewall configurado (puertos 80, 443)

---

## 🎯 Ventajas de este Setup

✅ **Todo aislado en contenedores**
✅ **Fácil de respaldar** (solo volúmenes)
✅ **Fácil de migrar** (llevar a otro servidor)
✅ **No contamina el servidor** (solo Docker)
✅ **Actualizaciones simples** (rebuild contenedores)
✅ **Rollback fácil** (volver a imagen anterior)
✅ **SSL automático** (certbot en contenedor)

---

## 📞 Comandos de Emergencia

```bash
# Todo dejó de funcionar
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d

# Logs en tiempo real
docker-compose -f docker-compose.production.yml logs -f

# Reinicio completo
docker-compose -f docker-compose.production.yml down -v
docker-compose -f docker-compose.production.yml up -d --build

# Ver qué está consumiendo recursos
docker stats
```

---

**¡Listo! Todo corre en Docker, nada instalado en el servidor excepto Docker mismo! 🐳**
