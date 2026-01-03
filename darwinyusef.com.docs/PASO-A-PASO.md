# 🚀 Guía Paso a Paso - Deployment en DigitalOcean

**Servidor IP:** YOUR_SERVER_IP
**Dominio:** darwinyusef.com
**Infraestructura:** GitHub Actions + Docker + Minio

---

## 📋 Índice

1. [Configurar DNS del Dominio](#1-configurar-dns-del-dominio)
2. [Conectar al Servidor](#2-conectar-al-servidor)
3. [Preparar el Servidor](#3-preparar-el-servidor)
4. [Clonar y Configurar el Proyecto](#4-clonar-y-configurar-el-proyecto)
5. [Deploy Inicial con Docker](#5-deploy-inicial-con-docker)
6. [Configurar Nginx](#6-configurar-nginx)
7. [Configurar SSL (Let's Encrypt)](#7-configurar-ssl-lets-encrypt)
8. [Configurar GitHub Actions para CI/CD](#8-configurar-github-actions-para-cicd)
9. [Verificar Todo Funciona](#9-verificar-todo-funciona)
10. [Configuración Adicional Opcional](#10-configuración-adicional-opcional)

---

## 1. Configurar DNS del Dominio

### Opción A: DNS en DigitalOcean (Recomendado)

1. **Ve a DigitalOcean Dashboard:**
   - https://cloud.digitalocean.com/networking/domains

2. **Agrega tu dominio:**
   ```
   Click "Add Domain"
   Domain: darwinyusef.com
   Click "Add Domain"
   ```

3. **Crear registros DNS:**
   ```
   Tipo    Nombre    Valor              TTL
   ─────────────────────────────────────────────
   A       @         YOUR_SERVER_IP     3600
   A       www       YOUR_SERVER_IP     3600
   A       jenkins   YOUR_SERVER_IP     3600  (opcional)
   A       minio     YOUR_SERVER_IP     3600  (opcional)
   ```

4. **En tu registrador de dominios** (GoDaddy, Namecheap, etc.):
   - Cambia los nameservers a:
     ```
     ns1.digitalocean.com
     ns2.digitalocean.com
     ns3.digitalocean.com
     ```
   - **Nota:** Esto puede tardar 24-48 horas en propagarse

### Opción B: DNS en tu Registrador

Si prefieres mantener el DNS en tu registrador:

```
Tipo    Nombre                 Valor              TTL
──────────────────────────────────────────────────────
A       darwinyusef.com        YOUR_SERVER_IP     3600
A       www.darwinyusef.com    YOUR_SERVER_IP     3600
A       jenkins.darwinyusef.com YOUR_SERVER_IP    3600  (opcional)
A       minio.darwinyusef.com   YOUR_SERVER_IP    3600  (opcional)
```

### Verificar DNS

Espera 5-10 minutos y verifica:

```bash
# En tu computadora local
nslookup darwinyusef.com
ping darwinyusef.com

# Debería mostrar YOUR_SERVER_IP
```

---

## 2. Conectar al Servidor

```bash
# Desde tu terminal local
ssh root@YOUR_SERVER_IP
```

**✅ Deberías estar conectado al servidor ahora**

---

## 3. Preparar el Servidor

### 3.1 Actualizar Sistema

```bash
# En el servidor
apt update && apt upgrade -y
```

### 3.2 Verificar Docker

```bash
# Verificar que Docker está instalado
docker --version
docker-compose --version

# Ver contenedores actuales
docker ps
```

### 3.3 Instalar Nginx (si no está instalado)

```bash
# Instalar Nginx
apt install nginx -y

# Habilitar y arrancar
systemctl enable nginx
systemctl start nginx
systemctl status nginx

# Verificar
curl http://localhost
```

### 3.4 Instalar Certbot para SSL

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Verificar
certbot --version
```

### 3.5 Instalar Git (si no está)

```bash
apt install git -y
git --version
```

---

## 4. Clonar y Configurar el Proyecto

### 4.1 Crear Directorio y Clonar

```bash
# Crear directorio para el proyecto
mkdir -p /opt/portfolio
cd /opt/portfolio

# Clonar repositorio
git clone https://github.com/darwinyusef/darwinyusef.portfolio.git .

# Verificar
ls -la
```

### 4.2 Ir al Directorio de la Aplicación

```bash
cd /opt/portfolio/astro-portfolio
pwd
# Debe mostrar: /opt/portfolio/astro-portfolio
```

### 4.3 Configurar Variables de Entorno

```bash
# Copiar ejemplo de .env
cp .env.example .env

# Editar .env
nano .env
```

**Contenido de .env:**
```bash
NODE_ENV=production
PORT=8080
SITE_URL=https://darwinyusef.com

# Si tienes más variables, agrégalas aquí
```

**Guardar:** `Ctrl+O`, Enter, `Ctrl+X`

---

## 5. Deploy Inicial con Docker

### 5.1 Hacer Build Inicial

```bash
# En /opt/portfolio/astro-portfolio

# Build y deploy
docker-compose up -d --build

# Esto tomará unos minutos...
```

### 5.2 Verificar que Está Corriendo

```bash
# Ver contenedores
docker ps

# Debes ver algo como:
# CONTAINER ID   IMAGE              PORTS                    NAMES
# xxxxxxxxxxxx   astro-portfolio    0.0.0.0:3000->8080/tcp   astro-portfolio

# Ver logs
docker logs -f astro-portfolio

# Presiona Ctrl+C para salir de los logs
```

### 5.3 Probar Localmente

```bash
# Test en el servidor
curl http://localhost:3000

# Deberías ver HTML del portfolio
```

### 5.4 Probar desde tu Computadora

```bash
# En tu computadora local (nueva terminal)
curl http://YOUR_SERVER_IP:3000

# O abre en navegador:
# http://YOUR_SERVER_IP:3000
```

**✅ Si ves el portfolio, el Docker está funcionando correctamente**

---

## 6. Configurar Nginx

### 6.1 Crear Configuración de Nginx

```bash
# En el servidor
nano /etc/nginx/sites-available/portfolio
```

**Pega esta configuración:**

```nginx
# Upstream para el contenedor
upstream portfolio_backend {
    server localhost:3000;
}

# HTTP - Redirect to HTTPS (temporalmente comentado)
server {
    listen 80;
    listen [::]:80;
    server_name darwinyusef.com www.darwinyusef.com;

    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Temporalmente servir HTTP hasta configurar SSL
    location / {
        proxy_pass http://portfolio_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Guardar:** `Ctrl+O`, Enter, `Ctrl+X`

### 6.2 Activar el Sitio

```bash
# Crear symlink
ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/

# Verificar configuración
nginx -t

# Debe decir: "syntax is ok" y "test is successful"
```

### 6.3 Desactivar Sitio Default (opcional)

```bash
# Si quieres que darwinyusef.com sea el sitio principal
rm /etc/nginx/sites-enabled/default

# O simplemente déjalo si no interfiere
```

### 6.4 Reload Nginx

```bash
systemctl reload nginx

# Verificar que está corriendo
systemctl status nginx
```

### 6.5 Probar HTTP

```bash
# En tu navegador, visita:
http://darwinyusef.com

# Deberías ver tu portfolio
```

**✅ Si funciona, continúa con SSL**

---

## 7. Configurar SSL (Let's Encrypt)

### 7.1 Obtener Certificado SSL

```bash
# Obtener certificado para el dominio principal
certbot --nginx -d darwinyusef.com -d www.darwinyusef.com

# Seguir las instrucciones:
# 1. Ingresa tu email
# 2. Acepta términos (Y)
# 3. Compartir email (opcional, N)
# 4. Cuando pregunte redirect HTTP to HTTPS, elige: 2 (Redirect)
```

### 7.2 Verificar Certificados

```bash
# Ver certificados instalados
certbot certificates

# Debes ver:
# Certificate Name: darwinyusef.com
# Domains: darwinyusef.com www.darwinyusef.com
# Expiry Date: ...
```

### 7.3 Test Auto-Renovación

```bash
# Probar que la renovación automática funciona
certbot renew --dry-run

# Debe decir: "Congratulations, all simulated renewals succeeded"
```

### 7.4 Probar HTTPS

```bash
# En tu navegador:
https://darwinyusef.com

# Debe cargar con el candado de seguridad 🔒
```

**✅ SSL configurado correctamente**

---

## 7.5 SSL para Subdominios (Opcional)

Si quieres SSL para Jenkins y Minio:

```bash
# Para Jenkins
certbot --nginx -d jenkins.darwinyusef.com

# Para Minio
certbot --nginx -d minio.darwinyusef.com
```

---

## 8. Configurar GitHub Actions para CI/CD

### 8.1 ¿Por qué GitHub Actions?

**Ventajas:**
- ✅ Zero RAM consumido en el servidor (vs ~1GB con Jenkins)
- ✅ Build en runners de GitHub (no en tu servidor)
- ✅ Configuración via código (archivo YAML)
- ✅ Sin mantenimiento (no actualizar plugins, etc)
- ✅ Integración nativa con GitHub

### 8.2 Generar SSH Key para Deployment

```bash
# En el servidor
cd ~/.ssh

# Generar key para GitHub Actions
ssh-keygen -t ed25519 -C "github-actions" -f github_actions_deploy

# Agregar clave pública a authorized_keys
cat github_actions_deploy.pub >> authorized_keys

# Copiar clave PRIVADA (para GitHub Secrets)
cat github_actions_deploy
# Copia TODO el output (incluye BEGIN/END)
```

### 8.3 Configurar GitHub Secrets

1. **Ve a tu repositorio:**
   ```
   https://github.com/darwinyusef/darwinyusef.portfolio/settings/secrets/actions
   ```

2. **Agregar estos secrets:**

   **SSH_HOST**
   ```
   YOUR_SERVER_IP
   ```

   **SSH_USERNAME**
   ```
   root
   ```

   **SSH_PRIVATE_KEY**
   ```
   -----BEGIN OPENSSH PRIVATE KEY-----
   [pega TODO el contenido de github_actions_deploy]
   -----END OPENSSH PRIVATE KEY-----
   ```

   **SITE_URL**
   ```
   https://darwinyusef.com
   ```

### 8.4 Verificar Workflow File

El archivo `.github/workflows/deploy.yml` ya está configurado. Verifica:

```bash
# En tu repositorio local
cat .github/workflows/deploy.yml

# Debe existir y contener el workflow de deployment
```

### 8.5 Test del Deployment

```bash
# Hacer un cambio pequeño
echo "# Test GitHub Actions" >> README.md
git add README.md
git commit -m "test: GitHub Actions deployment"
git push origin main

# Ver en GitHub:
# https://github.com/darwinyusef/darwinyusef.portfolio/actions
```

**✅ Si el workflow ejecuta exitosamente, GitHub Actions está configurado**

---

**📚 Ver guía completa:** `GITHUB-ACTIONS-DEPLOY.md`

---

## 9. Verificar Todo Funciona

### 9.1 Checklist Final

```bash
# En el servidor, ejecuta cada comando:

# 1. Verificar Docker
docker ps | grep astro-portfolio
# Debe mostrar el contenedor corriendo

# 2. Verificar Nginx
systemctl status nginx
# Debe estar "active (running)"

# 3. Verificar SSL
certbot certificates
# Debe mostrar el certificado para darwinyusef.com

# 4. Test del portfolio
curl -I https://darwinyusef.com
# Debe devolver HTTP/2 200

# 5. Ver logs
docker logs --tail 50 astro-portfolio
```

### 9.2 URLs para Verificar

Abre en tu navegador:

- ✅ https://darwinyusef.com
- ✅ https://www.darwinyusef.com
- ✅ https://github.com/darwinyusef/darwinyusef.portfolio/actions (GitHub Actions)
- ✅ http://YOUR_SERVER_IP:9000 (Minio, opcional)

---

## 10. Configuración Adicional Opcional

### 10.1 Configurar Firewall (UFW)

```bash
# Habilitar firewall
ufw allow ssh
ufw allow http
ufw allow https
ufw allow 8080/tcp  # Jenkins
ufw allow 9000/tcp  # Minio
ufw allow 3000/tcp  # Portfolio directo (opcional)

# Habilitar
ufw enable

# Ver status
ufw status
```

### 10.2 Configurar Backups Automáticos

```bash
# Copiar script de backup
cp /opt/portfolio/astro-portfolio/scripts/deploy-server.sh /usr/local/bin/portfolio-deploy
chmod +x /usr/local/bin/portfolio-deploy

# Crear script de backup
nano /usr/local/bin/portfolio-backup
```

**Contenido:**
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/portfolio"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup código
tar -czf $BACKUP_DIR/code-$DATE.tar.gz /opt/portfolio

# Backup .env
cp /opt/portfolio/astro-portfolio/.env $BACKUP_DIR/.env-$DATE

# Limpiar backups antiguos (>7 días)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completado: $DATE"
```

**Guardar y hacer ejecutable:**
```bash
chmod +x /usr/local/bin/portfolio-backup
```

**Agregar a crontab:**
```bash
crontab -e

# Agregar:
0 2 * * * /usr/local/bin/portfolio-backup >> /var/log/portfolio-backup.log 2>&1
```

### 10.3 Monitoreo de Logs

```bash
# Ver logs en tiempo real
tail -f /var/log/nginx/portfolio-access.log
tail -f /var/log/nginx/portfolio-error.log
docker logs -f astro-portfolio
```

---

## 🎯 Comandos Rápidos para el Día a Día

```bash
# Conectar al servidor
ssh root@YOUR_SERVER_IP

# Ver logs del portfolio
docker logs -f astro-portfolio

# Reiniciar portfolio
docker restart astro-portfolio

# Actualizar código manualmente
cd /opt/portfolio
git pull
cd astro-portfolio
docker-compose down
docker-compose up -d --build

# Ver estado de servicios
systemctl status nginx
docker ps

# Reload nginx
systemctl reload nginx

# Ver certificados SSL
certbot certificates

# Renovar SSL (manual)
certbot renew
```

---

## 🆘 Troubleshooting

### Problema: El sitio no carga

```bash
# 1. Verificar Docker
docker ps
docker logs astro-portfolio

# 2. Verificar Nginx
nginx -t
systemctl status nginx

# 3. Verificar DNS
nslookup darwinyusef.com

# 4. Verificar firewall
ufw status
```

### Problema: SSL no funciona

```bash
# Renovar certificado
certbot renew --force-renewal

# Reload nginx
systemctl reload nginx
```

### Problema: GitHub Actions no se ejecuta

```bash
# 1. Verificar secrets en GitHub
# Settings → Secrets and variables → Actions

# 2. Verificar workflow file
cat .github/workflows/deploy.yml

# 3. Ver logs en GitHub Actions tab
# https://github.com/darwinyusef/darwinyusef.portfolio/actions
```

---

## 📞 Siguiente Paso

Cuando completes estos pasos:

1. ✅ Dominio apuntando a tu servidor
2. ✅ Portfolio corriendo en Docker
3. ✅ Nginx configurado
4. ✅ SSL activo
5. ✅ GitHub Actions funcionando

**Tu portfolio estará en producción en:** https://darwinyusef.com 🎉

---

**¿Necesitas ayuda?**
- Revisa los logs: `docker logs astro-portfolio`
- Revisa nginx: `/var/log/nginx/portfolio-error.log`
- Contacto del proyecto en GitHub

---

**Última actualización:** Enero 2026
