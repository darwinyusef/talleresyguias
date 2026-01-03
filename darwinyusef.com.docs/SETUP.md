# 🚀 Setup Completo - Portfolio

Instalación en servidor con Docker (todo automatizado).

---

## 📋 Requisitos

- Servidor Ubuntu/Debian
- Dominio apuntando al servidor
- 1GB RAM mínimo

---

## 🎯 Instalación Rápida

### 1. Instalar Docker

```bash
# Conectar al servidor
ssh root@YOUR_SERVER_IP

# Instalar Docker
curl -fsSL https://get.docker.com | sh

# Instalar Docker Compose
apt install docker-compose -y

# Verificar
docker --version
```

### 2. Clonar Proyecto

```bash
# Crear directorio
mkdir -p /opt/portfolio
cd /opt/portfolio

# Clonar
git clone https://github.com/darwinyusef/darwinyusef.portfolio.git .
cd astro-portfolio
```

### 3. Configurar Variables

```bash
# Copiar ejemplo
cp .env.example .env

# Editar
nano .env
```

**Mínimo necesario en .env:**

```bash
# Gmail para enviar emails
GMAIL_USER=wsgestor@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Emails
EMAIL_FROM=no-reply@aquicreamos.com
EMAIL_TO=wsgestor@gmail.com

# Minio (opcional)
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=tu_password_seguro
```

### 4. Configurar Dominio

**En `nginx-proxy.conf`:**

```bash
nano nginx-proxy.conf
```

Cambiar:
```nginx
server_name TU_DOMINIO.com www.TU_DOMINIO.com;
```

A:
```nginx
server_name darwinyusef.com www.darwinyusef.com;
```

### 5. Deploy

```bash
# Opción A: Solo Portfolio + Nginx
docker-compose -f docker-compose.production.yml up -d

# Opción B: Con Auto-Deploy (Recomendado)
docker-compose -f docker-compose.full.yml up -d

# Ver logs
docker-compose -f docker-compose.full.yml logs -f
```

### 6. Configurar SSL

```bash
# Obtener certificado
docker-compose -f docker-compose.full.yml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email wsgestor@gmail.com \
  --agree-tos \
  -d darwinyusef.com \
  -d www.darwinyusef.com

# Editar nginx para habilitar HTTPS
nano nginx-proxy.conf
# Descomentar sección HTTPS y comentar HTTP

# Reiniciar nginx
docker-compose -f docker-compose.full.yml restart nginx
```

### 7. Configurar Auto-Deploy

**Ver:** [WEBHOOK-AUTODEPLOY.md](./WEBHOOK-AUTODEPLOY.md)

Resumen:
1. Generar secret: `openssl rand -hex 32`
2. Editar `webhook/hooks.json` con el secret
3. En GitHub: Settings → Webhooks → Add webhook
4. URL: `http://YOUR_SERVER_IP:9000/hooks/deploy-portfolio`
5. Secret: El que generaste
6. Push → Auto-deploy ✨

---

## ✅ Verificar

```bash
# Ver contenedores
docker ps

# Test HTTP
curl http://darwinyusef.com

# Test HTTPS
curl https://darwinyusef.com

# Ver logs
docker-compose -f docker-compose.full.yml logs
```

---

## 🔧 Comandos Útiles

```bash
# Ver estado
docker ps

# Logs
docker-compose -f docker-compose.full.yml logs -f

# Reiniciar
docker-compose -f docker-compose.full.yml restart

# Detener
docker-compose -f docker-compose.full.yml down

# Actualizar
cd /opt/portfolio/astro-portfolio
git pull
docker-compose -f docker-compose.full.yml up -d --build
```

---

## 📧 Configurar Email

**Ver:** [CONFIGURACION-EMAIL-GRATIS.md](./CONFIGURACION-EMAIL-GRATIS.md)

Resumen:
1. Cloudflare Email Routing para recibir
2. Gmail App Password para enviar
3. Configurar en `.env`

---

## 🐛 Problemas Comunes

### Puerto 80/443 en uso
```bash
# Detener servicios que usen esos puertos
systemctl stop nginx
systemctl stop apache2
```

### Certificado SSL falla
```bash
# Verificar DNS
dig darwinyusef.com +short

# Debe mostrar tu IP del servidor
```

### Webhook no funciona
```bash
# Ver logs
docker logs portfolio-webhook

# Test
curl http://localhost:9000/hooks/health-check
```

---

## 📚 Más Info

- **Auto-Deploy:** [WEBHOOK-AUTODEPLOY.md](./WEBHOOK-AUTODEPLOY.md)
- **Email:** [CONFIGURACION-EMAIL-GRATIS.md](./CONFIGURACION-EMAIL-GRATIS.md)
- **Comandos:** [COMANDOS-RAPIDOS.md](./COMANDOS-RAPIDOS.md)
