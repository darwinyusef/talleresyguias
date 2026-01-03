# Guía de Deployment en tu Servidor DigitalOcean

**Servidor IP:** YOUR_SERVER_IP
**Infraestructura existente:** Jenkins + Minio + Docker

## Índice
- [Arquitectura Actual](#arquitectura-actual)
- [Setup Inicial del Portfolio](#setup-inicial-del-portfolio)
- [Configuración de Jenkins CI/CD](#configuración-de-jenkins-cicd)
- [Configuración de Nginx](#configuración-de-nginx)
- [Deployment Manual](#deployment-manual)
- [Troubleshooting](#troubleshooting)

---

## Arquitectura Actual

```
┌─────────────────────────────────────────┐
│   Servidor: YOUR_SERVER_IP              │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │ Jenkins  │  │  Minio   │            │
│  │  :8080   │  │  :9000   │            │
│  └──────────┘  └──────────┘            │
│                                         │
│  ┌──────────────────────────┐          │
│  │   Portfolio (Nuevo)      │          │
│  │   Nginx + Astro          │          │
│  │   Puerto: 3000 -> 8080   │          │
│  └──────────────────────────┘          │
│                                         │
│  ┌──────────────────────────┐          │
│  │   Nginx Reverse Proxy    │          │
│  │   Puerto: 80, 443        │          │
│  └──────────────────────────┘          │
└─────────────────────────────────────────┘
```

---

## Setup Inicial del Portfolio

### 1. Conectar al Servidor

```bash
# Desde tu máquina local
ssh root@YOUR_SERVER_IP

# Verificar Docker
docker --version
docker-compose --version
docker ps
```

### 2. Crear Directorio para el Portfolio

```bash
# En el servidor
mkdir -p /opt/portfolio
cd /opt/portfolio

# Clonar el repositorio
git clone https://github.com/darwinyusef/darwinyusef.portfolio.git .
cd astro-portfolio

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar según necesites
```

### 3. Build y Deploy Inicial

```bash
# En /opt/portfolio/astro-portfolio
docker-compose -f docker-compose.yml up -d --build

# Verificar que está corriendo
docker ps | grep portfolio
docker logs -f astro-portfolio
```

El contenedor debería estar corriendo en el puerto 3000 (interno 8080).

---

## Configuración de Jenkins CI/CD

Ya tienes un `Jenkinsfile` en el proyecto. Vamos a configurarlo:

### 1. Configurar Jenkins

```bash
# Acceder a Jenkins
http://YOUR_SERVER_IP:8080

# Login con tus credenciales
```

### 2. Crear Pipeline Job

1. **En Jenkins UI:**
   - New Item → Pipeline
   - Name: `portfolio-deploy`
   - Pipeline script from SCM
   - SCM: Git
   - Repository URL: `https://github.com/darwinyusef/darwinyusef.portfolio.git`
   - Branch: `*/main`
   - Script Path: `astro-portfolio/Jenkinsfile`

2. **Configurar Webhooks en GitHub:**
   - Ve a tu repo → Settings → Webhooks
   - Add webhook:
     ```
     Payload URL: http://YOUR_SERVER_IP:8080/github-webhook/
     Content type: application/json
     Events: Just the push event
     ```

### 3. Configurar Credenciales en Jenkins

```bash
# En Jenkins UI
Manage Jenkins → Credentials → System → Global credentials

# Agregar:
1. GitHub credentials (si el repo es privado)
2. Docker registry credentials (si usas registry privado)
```

### 4. Actualizar Jenkinsfile para tu Servidor

El Jenkinsfile actual está listo, pero revisa estas configuraciones:

```groovy
// En astro-portfolio/Jenkinsfile
environment {
    DOCKER_IMAGE = 'portfolio'
    CONTAINER_NAME = 'astro-portfolio'
    DEPLOY_PATH = '/opt/portfolio/astro-portfolio'
}
```

### 5. Ejecutar Pipeline

```bash
# En Jenkins
- Ve al job "portfolio-deploy"
- Click "Build Now"
- Ver "Console Output" para logs
```

---

## Configuración de Nginx

### 1. Instalar Nginx (si no está instalado)

```bash
# En el servidor
apt update
apt install nginx -y
systemctl enable nginx
systemctl start nginx
```

### 2. Configurar Reverse Proxy

```bash
# Crear configuración del sitio
cat > /etc/nginx/sites-available/portfolio << 'EOF'
# Upstream para el contenedor del portfolio
upstream portfolio_backend {
    server localhost:3000;
}

# HTTP - Redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name darwinyusef.com www.darwinyusef.com;

    # Para Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect todo a HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS - Portfolio
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name darwinyusef.com www.darwinyusef.com;

    # SSL certificates (configurar después con certbot)
    # ssl_certificate /etc/letsencrypt/live/darwinyusef.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/darwinyusef.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Logging
    access_log /var/log/nginx/portfolio-access.log;
    error_log /var/log/nginx/portfolio-error.log;

    # Proxy al contenedor
    location / {
        proxy_pass http://portfolio_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Cache para assets estáticos
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://portfolio_backend;
        proxy_cache_valid 200 30d;
        add_header Cache-Control "public, immutable";
    }
}

# Jenkins (opcional - para acceso web)
server {
    listen 80;
    server_name jenkins.darwinyusef.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Para Jenkins WebSocket
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# Minio (opcional - para acceso web)
server {
    listen 80;
    server_name minio.darwinyusef.com;

    location / {
        proxy_pass http://localhost:9000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Activar el sitio
ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/

# Test configuración
nginx -t

# Reload nginx
systemctl reload nginx
```

### 3. Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Obtener certificado SSL para el dominio principal
certbot --nginx -d darwinyusef.com -d www.darwinyusef.com

# Para subdominios (opcional)
certbot --nginx -d jenkins.darwinyusef.com
certbot --nginx -d minio.darwinyusef.com

# Auto-renovación (ya configurado automáticamente)
certbot renew --dry-run
```

### 4. Configurar Firewall

```bash
# Permitir puertos necesarios
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8080/tcp  # Jenkins (opcional, solo si necesitas acceso directo)
ufw allow 9000/tcp  # Minio (opcional)
ufw enable

# Ver estado
ufw status
```

---

## Configuración DNS

En DigitalOcean Networking o tu registrador de dominios:

```
# Registros A
@ (root)              → YOUR_SERVER_IP
www                   → YOUR_SERVER_IP
jenkins               → YOUR_SERVER_IP (opcional)
minio                 → YOUR_SERVER_IP (opcional)
```

---

## Deployment Manual (Sin Jenkins)

Si prefieres hacer deploy manual:

### 1. Script de Deploy

```bash
# Crear script en el servidor
cat > /opt/portfolio/deploy.sh << 'EOF'
#!/bin/bash

set -e

echo "🚀 Iniciando deployment del portfolio..."

# Variables
REPO_DIR="/opt/portfolio"
APP_DIR="$REPO_DIR/astro-portfolio"

# Ir al directorio
cd $REPO_DIR

# Pull último código
echo "📥 Pulling latest code..."
git pull origin main

# Ir al directorio de la app
cd $APP_DIR

# Detener contenedor actual
echo "🛑 Stopping current container..."
docker-compose down

# Limpiar imágenes antiguas
echo "🧹 Cleaning old images..."
docker image prune -f

# Build nueva imagen
echo "🔨 Building new image..."
docker-compose build --no-cache

# Iniciar contenedor
echo "▶️  Starting container..."
docker-compose up -d

# Verificar estado
echo "✅ Checking status..."
docker-compose ps

# Ver logs
echo "📋 Container logs:"
docker-compose logs --tail=20

echo "✨ Deployment completed!"
echo "🌐 Site: http://YOUR_SERVER_IP:3000"
EOF

# Dar permisos de ejecución
chmod +x /opt/portfolio/deploy.sh
```

### 2. Ejecutar Deploy

```bash
# En el servidor
/opt/portfolio/deploy.sh
```

---

## Automatización con GitHub Webhooks (Sin Jenkins)

Si no quieres usar Jenkins, puedes usar webhooks directamente:

### 1. Instalar webhook server

```bash
# En el servidor
apt install webhook -y

# Crear configuración
cat > /etc/webhook/hooks.json << 'EOF'
[
  {
    "id": "deploy-portfolio",
    "execute-command": "/opt/portfolio/deploy.sh",
    "command-working-directory": "/opt/portfolio",
    "response-message": "Deploying portfolio...",
    "trigger-rule": {
      "match": {
        "type": "payload-hash-sha1",
        "secret": "TU_SECRET_AQUI_123",
        "parameter": {
          "source": "header",
          "name": "X-Hub-Signature"
        }
      }
    }
  }
]
EOF

# Iniciar webhook server
webhook -hooks /etc/webhook/hooks.json -verbose -port 9876
```

### 2. Configurar systemd para webhook

```bash
cat > /etc/systemd/system/webhook.service << 'EOF'
[Unit]
Description=Webhook Server
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/webhook -hooks /etc/webhook/hooks.json -verbose -port 9876
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable webhook
systemctl start webhook
```

---

## Gestión de Contenedores

### Comandos Útiles

```bash
# Ver contenedores corriendo
docker ps

# Ver logs del portfolio
docker logs -f astro-portfolio

# Reiniciar contenedor
docker restart astro-portfolio

# Acceder al contenedor
docker exec -it astro-portfolio sh

# Ver estadísticas de recursos
docker stats astro-portfolio

# Limpiar recursos no usados
docker system prune -a
```

### Monitoreo

```bash
# Ver uso de disco
df -h

# Ver memoria
free -h

# Ver procesos
top

# Ver logs de nginx
tail -f /var/log/nginx/portfolio-access.log
tail -f /var/log/nginx/portfolio-error.log
```

---

## Backups

### 1. Backup del Portfolio

```bash
# Crear script de backup
cat > /opt/portfolio/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/backups/portfolio"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup del código
tar -czf $BACKUP_DIR/portfolio-code-$DATE.tar.gz /opt/portfolio

# Backup de configuración nginx
tar -czf $BACKUP_DIR/nginx-config-$DATE.tar.gz /etc/nginx/sites-available/portfolio

# Backup de .env
cp /opt/portfolio/astro-portfolio/.env $BACKUP_DIR/.env-$DATE

# Backup a Minio (opcional)
# Instalar minio client: wget https://dl.min.io/client/mc/release/linux-amd64/mc
# chmod +x mc
# ./mc alias set myminio http://localhost:9000 ACCESO SECRETO
# ./mc cp $BACKUP_DIR/portfolio-code-$DATE.tar.gz myminio/backups/

echo "Backup completado: $DATE"

# Limpiar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /opt/portfolio/backup.sh
```

### 2. Automatizar con Cron

```bash
# Editar crontab
crontab -e

# Agregar:
# Backup diario a las 2 AM
0 2 * * * /opt/portfolio/backup.sh >> /var/log/portfolio-backup.log 2>&1
```

---

## Troubleshooting

### Problema: Contenedor no inicia

```bash
# Ver logs detallados
docker logs astro-portfolio

# Verificar puertos
netstat -tulpn | grep 3000

# Reconstruir desde cero
cd /opt/portfolio/astro-portfolio
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Nginx no sirve el sitio

```bash
# Test configuración
nginx -t

# Ver logs de error
tail -50 /var/log/nginx/portfolio-error.log

# Verificar que nginx puede conectar al contenedor
curl http://localhost:3000
```

### Problema: SSL no funciona

```bash
# Renovar certificados
certbot renew

# Verificar certificados
certbot certificates

# Probar configuración SSL
nginx -t
systemctl reload nginx
```

### Problema: Out of disk space

```bash
# Ver uso de disco
df -h

# Limpiar Docker
docker system prune -a --volumes

# Limpiar logs
journalctl --vacuum-time=7d

# Limpiar APT cache
apt clean
```

---

## Actualización del Portfolio

### Vía Jenkins (Recomendado)
1. Hacer push a GitHub
2. Jenkins detecta el push automáticamente
3. Ejecuta el pipeline
4. Deploy automático

### Vía Manual
```bash
ssh root@YOUR_SERVER_IP
/opt/portfolio/deploy.sh
```

---

## Checklist de Seguridad

- [ ] Firewall configurado (UFW)
- [ ] SSL/TLS habilitado
- [ ] Usuario no-root para aplicaciones
- [ ] Backups automáticos
- [ ] Logs rotados
- [ ] Fail2ban instalado (recomendado)
- [ ] SSH con clave pública (no password)
- [ ] Variables de entorno seguras
- [ ] Contenedores con health checks

---

## URLs del Proyecto

```
Portfolio: https://darwinyusef.com
Jenkins: http://YOUR_SERVER_IP:8080
Minio: http://YOUR_SERVER_IP:9000
```

---

**Última actualización**: Enero 2026
