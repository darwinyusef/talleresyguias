# 🌐 Configuración de Dominio y HTTPS

Guía rápida para configurar `darwinyusef.com` con HTTPS en DigitalOcean.

---

## 🎯 Resumen

- **Dominio:** darwinyusef.com
- **Servidor:** YOUR_SERVER_IP (DigitalOcean)
- **SSL:** Let's Encrypt (Gratis, Automático)
- **Puerto:** 443 (HTTPS)

---

## 📋 Opción 1: DNS en DigitalOcean (Recomendado)

### Paso 1: Agregar Dominio en DigitalOcean

1. **Ve a DigitalOcean Dashboard:**
   ```
   https://cloud.digitalocean.com/networking/domains
   ```

2. **Add Domain:**
   - Click **"Add Domain"**
   - Domain: `darwinyusef.com`
   - Click **"Add Domain"**

3. **Crear Registros DNS:**

   Click en `darwinyusef.com` y agrega estos registros:

   | Type | Hostname | Value | TTL |
   |------|----------|-------|-----|
   | **A** | `@` | `YOUR_SERVER_IP` | 3600 |
   | **A** | `www` | `YOUR_SERVER_IP` | 3600 |

   Opcional (para subdominios):
   | Type | Hostname | Value | TTL |
   |------|----------|-------|-----|
   | **A** | `jenkins` | `YOUR_SERVER_IP` | 3600 |
   | **A** | `minio` | `YOUR_SERVER_IP` | 3600 |

### Paso 2: Configurar Nameservers en tu Registrador

En el sitio donde compraste `darwinyusef.com` (GoDaddy, Namecheap, etc.):

1. **Ir a DNS Settings**
2. **Cambiar Nameservers a:**
   ```
   ns1.digitalocean.com
   ns2.digitalocean.com
   ns3.digitalocean.com
   ```

3. **Guardar cambios**

**⏱️ Propagación DNS:** 1-48 horas (usualmente 1-4 horas)

### Paso 3: Verificar DNS

```bash
# En tu terminal local (Mac)
# Espera 10-15 minutos después de configurar

# Verificar DNS
nslookup darwinyusef.com

# Debe mostrar:
# Name:   darwinyusef.com
# Address: YOUR_SERVER_IP

# O usar dig
dig darwinyusef.com +short
# Debe mostrar: YOUR_SERVER_IP

# Ping
ping darwinyusef.com
```

---

## 📋 Opción 2: DNS en tu Registrador

Si NO quieres usar DigitalOcean DNS:

En tu registrador de dominios, agrega estos registros A:

```
Type   Hostname                 Value              TTL
────────────────────────────────────────────────────────
A      darwinyusef.com          YOUR_SERVER_IP     3600
A      www.darwinyusef.com      YOUR_SERVER_IP     3600
```

---

## 🔧 Configurar Nginx en el Servidor

### Paso 1: Conectar al Servidor

```bash
ssh root@YOUR_SERVER_IP
```

### Paso 2: Instalar Nginx (si no está)

```bash
# Verificar si Nginx está instalado
nginx -v

# Si no está instalado:
apt update
apt install nginx -y

# Iniciar y habilitar
systemctl start nginx
systemctl enable nginx
```

### Paso 3: Crear Configuración de Nginx

```bash
# Crear archivo de configuración
nano /etc/nginx/sites-available/darwinyusef
```

**Pega esta configuración INICIAL (sin SSL):**

```nginx
# Upstream para el contenedor
upstream portfolio_backend {
    server localhost:3000;
}

# HTTP - Puerto 80
server {
    listen 80;
    listen [::]:80;
    server_name darwinyusef.com www.darwinyusef.com;

    # Para Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Proxy al contenedor Docker
    location / {
        proxy_pass http://portfolio_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Cache para assets estáticos
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2)$ {
        proxy_pass http://portfolio_backend;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Guardar:** `Ctrl+O`, Enter, `Ctrl+X`

### Paso 4: Activar el Sitio

```bash
# Crear symlink
ln -s /etc/nginx/sites-available/darwinyusef /etc/nginx/sites-enabled/

# Desactivar default (opcional)
rm /etc/nginx/sites-enabled/default

# Test configuración
nginx -t

# Debe mostrar:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Reload Nginx
systemctl reload nginx
```

### Paso 5: Verificar HTTP

```bash
# En el servidor
curl http://localhost

# Desde tu computadora
curl http://darwinyusef.com
# O abre en navegador: http://darwinyusef.com

# Si no funciona, verifica que Docker esté corriendo:
docker ps | grep astro-portfolio
```

---

## 🔒 Configurar SSL (HTTPS) con Let's Encrypt

### Paso 1: Instalar Certbot

```bash
# En el servidor
apt update
apt install certbot python3-certbot-nginx -y

# Verificar
certbot --version
```

### Paso 2: Obtener Certificado SSL

```bash
# IMPORTANTE: Asegúrate de que el DNS esté propagado primero
# Verifica: nslookup darwinyusef.com (debe mostrar YOUR_SERVER_IP)

# Obtener certificado
certbot --nginx -d darwinyusef.com -d www.darwinyusef.com
```

**Certbot te preguntará:**

1. **Email:** `wsgestor@gmail.com` (para notificaciones de renovación)
2. **Terms of Service:** `Y` (aceptar)
3. **Share email:** `N` (opcional)
4. **Redirect HTTP to HTTPS:** `2` (sí, redirect)

**Certbot hará automáticamente:**
- Obtener certificado SSL
- Configurar Nginx con HTTPS
- Configurar redirect HTTP → HTTPS
- Configurar renovación automática

### Paso 3: Verificar Certificado

```bash
# Ver certificados
certbot certificates

# Debe mostrar:
# Certificate Name: darwinyusef.com
# Domains: darwinyusef.com www.darwinyusef.com
# Expiry Date: (90 días desde hoy)
# Certificate Path: /etc/letsencrypt/live/darwinyusef.com/fullchain.pem
# Private Key Path: /etc/letsencrypt/live/darwinyusef.com/privkey.pem
```

### Paso 4: Test HTTPS

```bash
# En navegador
https://darwinyusef.com

# Debe mostrar:
# - Tu portfolio
# - Candado verde 🔒 en la barra de direcciones
# - Certificado válido

# Test automático
curl -I https://darwinyusef.com

# Debe devolver:
# HTTP/2 200
```

### Paso 5: Test Auto-Renovación

```bash
# Probar renovación automática (modo simulación)
certbot renew --dry-run

# Debe mostrar:
# Congratulations, all simulated renewals succeeded

# La renovación se ejecuta automáticamente via cron
# No necesitas hacer nada más
```

---

## 🔥 Configurar Firewall

```bash
# En el servidor

# Permitir puertos necesarios
ufw allow ssh
ufw allow http      # Puerto 80
ufw allow https     # Puerto 443

# Habilitar firewall
ufw enable

# Ver estado
ufw status

# Debe mostrar:
# Status: active
# 22/tcp    ALLOW    Anywhere
# 80/tcp    ALLOW    Anywhere
# 443/tcp   ALLOW    Anywhere
```

---

## ✅ Verificación Final

### Checklist

```bash
# En el servidor, ejecuta:

# 1. DNS
dig darwinyusef.com +short
# Debe mostrar: YOUR_SERVER_IP

# 2. Docker
docker ps | grep astro-portfolio
# Debe mostrar el contenedor corriendo

# 3. Nginx
systemctl status nginx
# Debe mostrar: active (running)

# 4. Nginx config
nginx -t
# Debe mostrar: syntax is ok

# 5. Certificado SSL
certbot certificates
# Debe mostrar el certificado válido

# 6. HTTP
curl http://darwinyusef.com
# Debe devolver HTML o redirect a HTTPS

# 7. HTTPS
curl -I https://darwinyusef.com
# Debe devolver HTTP/2 200

# 8. Firewall
ufw status
# Debe mostrar puertos 80 y 443 permitidos
```

### En Navegador

1. **HTTP:** http://darwinyusef.com
   - ✅ Debe redireccionar automáticamente a HTTPS

2. **HTTPS:** https://darwinyusef.com
   - ✅ Candado verde 🔒
   - ✅ Portfolio visible
   - ✅ Sin warnings de seguridad

3. **WWW:** https://www.darwinyusef.com
   - ✅ Debe funcionar igual

---

## 🔄 Configuración Nginx Completa (Después de SSL)

Después de ejecutar certbot, tu configuración de Nginx se verá así:

```nginx
# /etc/nginx/sites-available/darwinyusef

upstream portfolio_backend {
    server localhost:3000;
}

# HTTP - Redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name darwinyusef.com www.darwinyusef.com;

    # Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Redirect to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name darwinyusef.com www.darwinyusef.com;

    # SSL Certificate (agregado por certbot)
    ssl_certificate /etc/letsencrypt/live/darwinyusef.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/darwinyusef.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Logs
    access_log /var/log/nginx/darwinyusef-access.log;
    error_log /var/log/nginx/darwinyusef-error.log;

    # Proxy to Docker container
    location / {
        proxy_pass http://portfolio_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static assets cache
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://portfolio_backend;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 🐛 Troubleshooting

### DNS no resuelve

```bash
# Espera más tiempo (propagación puede tomar hasta 48h)

# Verifica nameservers
dig NS darwinyusef.com

# Flush DNS local (en tu Mac)
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

### Certbot falla

**Error: "Failed authorization"**

```bash
# Asegúrate de que DNS apunta a tu servidor
dig darwinyusef.com +short
# Debe mostrar: YOUR_SERVER_IP

# Asegúrate de que el puerto 80 esté abierto
curl http://YOUR_SERVER_IP

# Verifica que Nginx esté corriendo
systemctl status nginx
```

### HTTPS no funciona

```bash
# Verifica certificado
certbot certificates

# Renovar si está expirado
certbot renew

# Reload nginx
systemctl reload nginx

# Ver logs
tail -f /var/log/nginx/error.log
```

---

## 📊 Resumen de Configuración

```
┌─────────────────────────────────────────────┐
│  DNS                                        │
├─────────────────────────────────────────────┤
│  darwinyusef.com  →  YOUR_SERVER_IP         │
│  www.darwinyusef.com  →  YOUR_SERVER_IP     │
└─────────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  Nginx (Puerto 80, 443)                     │
├─────────────────────────────────────────────┤
│  HTTP (80)  →  Redirect to HTTPS            │
│  HTTPS (443)  →  Proxy to Docker            │
│  SSL: Let's Encrypt (Auto-renew)            │
└─────────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  Docker Container (Puerto 3000)             │
├─────────────────────────────────────────────┤
│  astro-portfolio                            │
│  Nginx Alpine serving static files          │
└─────────────────────────────────────────────┘
```

---

## 🚀 Resumen de Comandos

```bash
# 1. Conectar al servidor
ssh root@YOUR_SERVER_IP

# 2. Configurar Nginx
nano /etc/nginx/sites-available/darwinyusef
ln -s /etc/nginx/sites-available/darwinyusef /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# 3. Obtener SSL
certbot --nginx -d darwinyusef.com -d www.darwinyusef.com

# 4. Configurar firewall
ufw allow http
ufw allow https
ufw enable

# 5. Verificar
curl -I https://darwinyusef.com
```

---

**✅ ¡Dominio y HTTPS configurados!**

**URLs:**
- 🌐 https://darwinyusef.com
- 🔐 SSL válido y activo
- 🔄 Auto-renovación configurada

**Última actualización:** Enero 2026
