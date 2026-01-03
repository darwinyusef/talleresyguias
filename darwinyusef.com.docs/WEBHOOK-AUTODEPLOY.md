# 🔄 Auto-Deploy con Webhook Worker

Configuración para que el servidor escuche cambios en GitHub y haga deploy automático.

---

## 🎯 Cómo Funciona

```
┌─────────────────────────────────────────────────────────┐
│  1. Developer push to GitHub (main branch)             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  2. GitHub envía webhook POST                           │
│     URL: http://YOUR_SERVER_IP:9000/hooks/deploy       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  3. Contenedor Webhook recibe y valida                  │
│     - Verifica signature (seguridad)                    │
│     - Verifica que es rama main                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  4. Ejecuta deploy.sh                                   │
│     - git pull                                          │
│     - docker build                                      │
│     - docker stop old container                         │
│     - docker start new container                        │
│     - health check                                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  5. Portfolio actualizado automáticamente! ✨           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup Completo

### Paso 1: Levantar todos los servicios

```bash
# En el servidor
cd /opt/portfolio/astro-portfolio

# Levantar servicios (Portfolio + Nginx + Webhook + Minio)
docker-compose -f docker-compose.full.yml up -d

# Ver logs
docker-compose -f docker-compose.full.yml logs -f
```

### Paso 2: Configurar Secret del Webhook

```bash
# Generar un secret aleatorio
SECRET=$(openssl rand -hex 32)
echo $SECRET

# Editar webhook/hooks.json
nano webhook/hooks.json
```

**Actualizar la línea:**

```json
"secret": "your-webhook-secret-here",
```

A:

```json
"secret": "EL_SECRET_QUE_GENERASTE",
```

**Guardar y reiniciar webhook:**

```bash
docker-compose -f docker-compose.full.yml restart webhook
```

### Paso 3: Configurar GitHub Webhook

1. **Ve a tu repositorio en GitHub:**
   ```
   https://github.com/darwinyusef/darwinyusef.portfolio/settings/hooks
   ```

2. **Add webhook:**
   ```
   Payload URL: http://YOUR_SERVER_IP:9000/hooks/deploy-portfolio
   Content type: application/json
   Secret: EL_SECRET_QUE_GENERASTE
   SSL verification: Disable (o usa HTTPS si tienes)
   Which events: Just the push event
   Active: ✅
   ```

3. **Add webhook**

### Paso 4: Test del Webhook

```bash
# Opción A: Hacer un push de prueba
echo "# Test" >> README.md
git add README.md
git commit -m "test: webhook autodeploy"
git push origin main

# Opción B: Test manual con curl
curl -X POST http://YOUR_SERVER_IP:9000/hooks/health-check

# Ver logs del webhook
docker logs -f portfolio-webhook
```

---

## 📊 Servicios Incluidos

### 1. Webhook (Puerto 9000)

**Escucha cambios de GitHub y ejecuta deploy.**

```bash
# Ver logs
docker logs -f portfolio-webhook

# Test endpoint
curl http://localhost:9000/hooks/health-check

# Reiniciar
docker-compose -f docker-compose.full.yml restart webhook
```

### 2. GitHub Actions (Recomendado)

**CI/CD completamente en la nube sin consumir recursos del servidor.**

```bash
# Ver la guía completa
cat GITHUB-ACTIONS-DEPLOY.md

# O en GitHub:
# https://github.com/darwinyusef/darwinyusef.portfolio/actions
```

**Ventajas:**
- Zero RAM en el servidor
- Build automático en cada push
- Logs detallados en GitHub
- No requiere mantenimiento

**Ver:** `GITHUB-ACTIONS-DEPLOY.md` para configuración completa.

### 3. Minio (Puertos 9001, 9090)

**Almacenamiento de assets.**

```bash
# Acceder
http://YOUR_SERVER_IP:9090

# Login:
# User: admin (o tu MINIO_ROOT_USER)
# Pass: changeme123 (o tu MINIO_ROOT_PASSWORD)

# Configurar en .env:
MINIO_ROOT_USER=tu_usuario
MINIO_ROOT_PASSWORD=tu_password_seguro

# Reiniciar
docker-compose -f docker-compose.full.yml restart minio
```

---

## 🔒 Seguridad

### Proteger Webhook con Firewall

```bash
# Solo permitir GitHub IPs (opcional)
# Lista de IPs: https://api.github.com/meta

# O usar nginx como proxy con HTTPS
```

### Cambiar Puerto del Webhook

En `docker-compose.full.yml`:

```yaml
webhook:
  ports:
    - "9876:9000"  # Cambiar puerto externo
```

### Usar HTTPS para Webhook

Agregar a `nginx-proxy.conf`:

```nginx
server {
    listen 443 ssl http2;
    server_name webhook.darwinyusef.com;

    ssl_certificate /etc/letsencrypt/live/darwinyusef.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/darwinyusef.com/privkey.pem;

    location / {
        proxy_pass http://webhook:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📋 Comandos Útiles

### Ver Estado de Todos los Servicios

```bash
docker-compose -f docker-compose.full.yml ps

# O más detallado
docker ps --filter "label=com.docker.compose.project=portfolio"
```

### Ver Logs de Deploy

```bash
# Logs del webhook
docker logs -f portfolio-webhook

# Logs del portfolio durante deploy
docker logs -f astro-portfolio

# Logs de nginx
docker logs -f portfolio-nginx
```

### Reiniciar un Servicio Específico

```bash
docker-compose -f docker-compose.full.yml restart webhook
docker-compose -f docker-compose.full.yml restart portfolio
docker-compose -f docker-compose.full.yml restart nginx
```

### Deploy Manual (Sin webhook)

```bash
# Ejecutar el script de deploy directamente
docker exec portfolio-webhook /scripts/deploy.sh "manual" "admin" "Manual deploy"

# O desde el servidor
cd /opt/portfolio/astro-portfolio
./webhook/deploy.sh
```

---

## 🐛 Troubleshooting

### Webhook no recibe eventos

```bash
# 1. Verificar que el contenedor está corriendo
docker ps | grep webhook

# 2. Test local
curl http://localhost:9000/hooks/health-check

# 3. Verificar firewall
ufw status | grep 9000

# 4. Ver logs
docker logs portfolio-webhook

# 5. En GitHub, ver deliveries del webhook
# Settings → Webhooks → Recent Deliveries
```

### Deploy falla

```bash
# Ver logs del script
docker logs portfolio-webhook

# Ver logs del portfolio
docker logs astro-portfolio

# Ejecutar deploy manualmente para debug
docker exec -it portfolio-webhook /bin/sh
cd /workspace/astro-portfolio
sh /scripts/deploy.sh "debug" "test" "debug"
```

### Permisos de Docker Socket

```bash
# Si hay error de permisos en Docker
docker-compose -f docker-compose.full.yml down
docker-compose -f docker-compose.full.yml up -d
```

---

## 🎯 Flujo Completo de Trabajo

### Desarrollo Local

```bash
# 1. Hacer cambios
code astro-portfolio/

# 2. Test local
npm run dev

# 3. Commit
git add .
git commit -m "feat: nueva funcionalidad"

# 4. Push
git push origin main
```

### Auto-Deploy

```
✅ GitHub recibe el push
✅ GitHub envía webhook al servidor
✅ Webhook valida y ejecuta deploy.sh
✅ Git pull en el servidor
✅ Docker build nueva imagen
✅ Detiene contenedor viejo
✅ Inicia contenedor nuevo
✅ Health check
✅ Limpia imágenes viejas
✅ Portfolio actualizado! 🎉
```

---

## 📊 Monitoreo

### Ver Última Ejecución

```bash
# Logs del webhook
docker logs --tail 100 portfolio-webhook | grep "Deployment"

# Estado actual del portfolio
docker inspect astro-portfolio | grep -A 5 "State"
```

### Notificaciones (Opcional)

Editar `webhook/deploy.sh` y descomentar al final:

```bash
# Slack
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"✅ Portfolio deployed"}' \
  YOUR_SLACK_WEBHOOK

# Discord
curl -X POST -H 'Content-type: application/json' \
  --data '{"content":"✅ Portfolio deployed"}' \
  YOUR_DISCORD_WEBHOOK

# Email (usando el SMTP ya configurado)
# Agregar script que envíe email
```

---

## ✅ Checklist Final

- [ ] docker-compose.full.yml ejecutándose
- [ ] Webhook secret generado y configurado
- [ ] GitHub webhook configurado
- [ ] Puerto 9000 abierto en firewall
- [ ] Test push realizado
- [ ] Deploy automático funcionó
- [ ] Logs sin errores
- [ ] Portfolio actualizado correctamente

---

## 🎉 Resultado

Ahora cada vez que hagas `git push origin main`:

1. ⚡ GitHub notifica al servidor
2. 🔄 Servidor ejecuta deploy automático
3. ✨ Portfolio actualizado en ~2 minutos
4. 🚀 Sin intervención manual

**¡Auto-deploy configurado! 🎊**
