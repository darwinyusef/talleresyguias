# 📚 Índice Completo - Documentación Portfolio

Guía de navegación de toda la documentación del proyecto.

---

## 🚀 INICIO RÁPIDO

| Documento | Para qué sirve |
|-----------|----------------|
| **[README.md](./README.md)** | 📖 Documentación principal del proyecto |
| **[PASO-A-PASO.md](./PASO-A-PASO.md)** | ⭐ **EMPEZAR AQUÍ** - Setup completo paso a paso |
| **[RESUMEN-SETUP.md](./RESUMEN-SETUP.md)** | 📋 Resumen de todo lo configurado |

---

## 🌐 DOMINIO Y DEPLOYMENT

### Configuración de Dominio

| Documento | Descripción |
|-----------|-------------|
| **[CONFIGURACION-DOMINIO-HTTPS.md](./CONFIGURACION-DOMINIO-HTTPS.md)** | 🔐 Configurar darwinyusef.com con HTTPS |
| **[DIGITALOCEAN-DEPLOY.md](./DIGITALOCEAN-DEPLOY.md)** | ☁️ Opciones de deployment en DigitalOcean |
| **[SERVIDOR-ACTUAL.md](./SERVIDOR-ACTUAL.md)** | 🖥️ Config específica del servidor YOUR_SERVER_IP |

### Docker

| Documento | Descripción |
|-----------|-------------|
| **[DOCKER-DEPLOY.md](./DOCKER-DEPLOY.md)** | 🐳 Guía completa de Docker y Docker Compose |
| `Dockerfile` | 📦 Multi-stage build de producción |
| `docker-compose.yml` | 🔧 Compose para producción |
| `docker-compose.dev.yml` | 🔧 Compose para desarrollo |

---

## 📧 EMAIL Y CONTACTO

| Documento | Descripción |
|-----------|-------------|
| **[CONFIGURACION-EMAIL-GRATIS.md](./CONFIGURACION-EMAIL-GRATIS.md)** | ✉️ **RECOMENDADO** - Email gratis con Cloudflare + Gmail |
| **[CONFIGURACION-CLOUDFLARE-EMAIL.md](./CONFIGURACION-CLOUDFLARE-EMAIL.md)** | ☁️ Alternativa con Resend + Cloudflare |
| **[CONFIGURACION-EMAIL-CALENDARIO.md](./CONFIGURACION-EMAIL-CALENDARIO.md)** | 📅 Email + Google Calendar (opcional) |

**Usa:** `CONFIGURACION-EMAIL-GRATIS.md` (100% gratis con Cloudflare Email Routing + Gmail SMTP)

---

## 🔄 CI/CD Y AUTOMATIZACIÓN

### Jenkins

| Archivo | Descripción |
|---------|-------------|
| `Jenkinsfile` | 🔨 Pipeline para Kubernetes |
| `Jenkinsfile.docker` | 🔨 Pipeline para Docker (tu servidor) |

### GitHub Actions

| Archivo | Descripción |
|---------|-------------|
| `.github/workflows/deploy.yml` | 🔄 Pipeline de CI/CD automático |
| `.github/SECRETS-SETUP.md` | 🔐 Configurar secrets de GitHub |

---

## 📦 DATOS Y CONTENIDO

| Documento | Descripción |
|-----------|-------------|
| **[INTEGRACION-DATOS.md](./INTEGRACION-DATOS.md)** | 📦 JSON externos en GitHub + Minio |

---

## 🛠️ SCRIPTS Y UTILIDADES

### Scripts de Setup

| Script | Descripción |
|--------|-------------|
| `scripts/setup-server.sh` | 🚀 **Setup automático completo** (ejecutar en servidor) |
| `scripts/deploy-server.sh` | 📤 Deploy manual |
| `start.sh` | ▶️ Script de inicio del contenedor |

### Comandos Rápidos

| Documento | Descripción |
|-----------|-------------|
| **[COMANDOS-RAPIDOS.md](./COMANDOS-RAPIDOS.md)** | ⚡ Referencia rápida de todos los comandos |
| `Makefile` | 🛠️ Comandos útiles (make dev, make prod, etc.) |

---

## ⚙️ CONFIGURACIÓN

### Nginx

| Archivo | Descripción |
|---------|-------------|
| `nginx.conf` | 🌐 Config de nginx para el contenedor |
| `nginx-reverse-proxy.conf` | 🔀 Config de reverse proxy para servidor |

### Kubernetes (Opcional)

| Archivo | Descripción |
|---------|-------------|
| `deploy/portfolio/k8s-namespace.yaml` | 📦 Namespaces (production, staging) |
| `deploy/portfolio/k8s-deployment.yaml` | 🚀 Deployment y Service |

### Variables de Entorno

| Archivo | Descripción |
|---------|-------------|
| `.env.example` | 📝 Template de variables de entorno |
| `.env` | 🔒 Variables de entorno (no commiteado) |

---

## 📖 GUÍAS POR TEMA

### Para Empezar

```
1. Lee: README.md
2. Sigue: PASO-A-PASO.md
3. Ejecuta: scripts/setup-server.sh
```

### Configurar Dominio y HTTPS

```
1. Lee: CONFIGURACION-DOMINIO-HTTPS.md
2. Configura DNS en DigitalOcean
3. Ejecuta certbot para SSL
```

### Configurar Email

```
1. Lee: CONFIGURACION-EMAIL-GRATIS.md
2. Configura Cloudflare Email Routing
3. Genera Gmail App Password
4. Actualiza .env
```

### Deploy Manual

```
1. Conecta: ssh root@YOUR_SERVER_IP
2. Ejecuta: portfolio-deploy
   O
   Ejecuta: cd /opt/portfolio/astro-portfolio && docker-compose down && docker-compose up -d --build
```

### CI/CD Automático

```
1. Lee: .github/SECRETS-SETUP.md
2. Configura secrets en GitHub
3. Push a main → Deploy automático
```

### Datos Externos

```
1. Lee: INTEGRACION-DATOS.md
2. Crea repo de datos en GitHub
3. Configura Minio para assets
4. Actualiza código para fetch
```

---

## 🎯 FLUJOS DE TRABAJO COMUNES

### Desarrollo Local

```bash
cd astro-portfolio
npm install
npm run dev

# Con Docker
make dev
# o
docker-compose -f docker-compose.dev.yml up
```

Ver: **COMANDOS-RAPIDOS.md** sección "En tu Computadora Local"

### Deploy a Producción

**Opción 1: Automático (Recomendado)**
```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main
# GitHub Actions + Jenkins harán el deploy automáticamente
```

**Opción 2: Manual**
```bash
ssh root@YOUR_SERVER_IP
portfolio-deploy
```

Ver: **SERVIDOR-ACTUAL.md** sección "Deployment Manual"

### Actualizar Contenido

```bash
# Editar JSON externos
cd portfolio-data  # Tu repo de datos
nano projects.json
git commit -m "update: nuevo proyecto"
git push
# Webhook limpiará el caché automáticamente
```

Ver: **INTEGRACION-DATOS.md** sección "Workflow Completo"

### Troubleshooting

1. **Contenedor no inicia:**
   - Ver: COMANDOS-RAPIDOS.md → "Troubleshooting"
   - Ejecutar: `docker logs astro-portfolio`

2. **Nginx error:**
   - Ver: CONFIGURACION-DOMINIO-HTTPS.md → "Troubleshooting"
   - Ejecutar: `nginx -t && systemctl status nginx`

3. **Email no funciona:**
   - Ver: CONFIGURACION-EMAIL-GRATIS.md → "Troubleshooting"
   - Verificar: variables de entorno y DNS

---

## 📊 ARQUITECTURA DEL PROYECTO

```
Portfolio Astro - Darwin Yusef
├── 📚 Documentación
│   ├── README.md (Inicio)
│   ├── PASO-A-PASO.md (Setup)
│   ├── RESUMEN-SETUP.md (Resumen)
│   ├── INDICE-COMPLETO.md (Este archivo)
│   ├── COMANDOS-RAPIDOS.md (Referencia)
│   │
│   ├── 🌐 Deployment
│   │   ├── CONFIGURACION-DOMINIO-HTTPS.md
│   │   ├── DIGITALOCEAN-DEPLOY.md
│   │   ├── SERVIDOR-ACTUAL.md
│   │   └── DOCKER-DEPLOY.md
│   │
│   ├── 📧 Email
│   │   ├── CONFIGURACION-EMAIL-GRATIS.md
│   │   ├── CONFIGURACION-CLOUDFLARE-EMAIL.md
│   │   └── CONFIGURACION-EMAIL-CALENDARIO.md
│   │
│   └── 📦 Datos
│       └── INTEGRACION-DATOS.md
│
├── 🔧 Configuración
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── nginx.conf
│   ├── .env.example
│   └── Makefile
│
├── 🔄 CI/CD
│   ├── .github/workflows/deploy.yml
│   ├── .github/SECRETS-SETUP.md
│   ├── Jenkinsfile
│   └── Jenkinsfile.docker
│
├── 🛠️ Scripts
│   ├── scripts/setup-server.sh
│   ├── scripts/deploy-server.sh
│   └── start.sh
│
├── 📦 Código Fuente
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   │   └── api/
│   │   │       ├── contact.ts
│   │   │       └── schedule.ts
│   │   ├── utils/
│   │   └── types/
│   │
│   └── public/
│
└── ☸️ Kubernetes (Opcional)
    └── deploy/portfolio/
        ├── k8s-namespace.yaml
        └── k8s-deployment.yaml
```

---

## 🔗 Links Importantes

### URLs del Proyecto

| Recurso | URL |
|---------|-----|
| **Portfolio Producción** | https://darwinyusef.com |
| **Repositorio GitHub** | https://github.com/darwinyusef/darwinyusef.portfolio |
| **Servidor (Directo)** | http://YOUR_SERVER_IP:3000 |
| **Jenkins** | http://YOUR_SERVER_IP:8080 |
| **Minio** | http://YOUR_SERVER_IP:9000 |

### Recursos Externos

| Recurso | URL |
|---------|-----|
| **DigitalOcean Dashboard** | https://cloud.digitalocean.com |
| **Cloudflare Dashboard** | https://dash.cloudflare.com |
| **GitHub Actions** | https://github.com/darwinyusef/darwinyusef.portfolio/actions |
| **Astro Docs** | https://docs.astro.build |
| **Docker Docs** | https://docs.docker.com |

---

## ✅ Checklists

### Checklist: Primera Instalación

- [ ] Leer README.md
- [ ] Seguir PASO-A-PASO.md
- [ ] Configurar DNS (CONFIGURACION-DOMINIO-HTTPS.md)
- [ ] Ejecutar setup-server.sh en servidor
- [ ] Configurar variables .env
- [ ] Obtener SSL con certbot
- [ ] Configurar email (CONFIGURACION-EMAIL-GRATIS.md)
- [ ] Configurar GitHub Secrets (.github/SECRETS-SETUP.md)
- [ ] Probar CI/CD con un push
- [ ] Verificar todo funciona

### Checklist: Mantenimiento

- [ ] Verificar certificado SSL (cada 3 meses)
- [ ] Actualizar dependencias (npm update)
- [ ] Revisar logs de error
- [ ] Backup de datos (.env, configuraciones)
- [ ] Verificar espacio en disco
- [ ] Limpiar imágenes Docker viejas

---

## 🆘 Soporte y Ayuda

### Documentación por Problema

| Problema | Ver Documento |
|----------|---------------|
| No puedo acceder al sitio | CONFIGURACION-DOMINIO-HTTPS.md → Troubleshooting |
| Docker no funciona | DOCKER-DEPLOY.md → Troubleshooting |
| Email no se envía | CONFIGURACION-EMAIL-GRATIS.md → Troubleshooting |
| CI/CD falla | .github/SECRETS-SETUP.md → Troubleshooting |
| No sé qué comando usar | COMANDOS-RAPIDOS.md |

### Comandos de Diagnóstico

```bash
# En el servidor
ssh root@YOUR_SERVER_IP

# Estado general
docker ps
systemctl status nginx
ufw status

# Logs
docker logs astro-portfolio
tail -f /var/log/nginx/error.log

# DNS
dig darwinyusef.com +short

# SSL
certbot certificates

# Espacio
df -h
docker system df
```

---

## 📞 Contacto

- **Email:** wsgestor@gmail.com
- **Portfolio:** https://darwinyusef.com
- **GitHub:** https://github.com/darwinyusef
- **Empresa:** https://aquicreamos.com

---

## 🎓 Notas Finales

### Tecnologías Utilizadas

- **Frontend:** Astro 5, Tailwind CSS 4
- **Backend:** Node.js, Nodemailer
- **Container:** Docker, Docker Compose
- **Web Server:** Nginx
- **CI/CD:** GitHub Actions, Jenkins
- **Email:** Cloudflare Email Routing, Gmail SMTP
- **Storage:** Minio (S3-compatible)
- **SSL:** Let's Encrypt (Certbot)
- **Hosting:** DigitalOcean Droplet
- **DNS:** Cloudflare / DigitalOcean

### Costos

```
Portfolio hosting (DigitalOcean Droplet):  $4-6/mes
Dominio (darwinyusef.com):                 $12/año
SSL (Let's Encrypt):                       GRATIS
Email (Cloudflare + Gmail):                GRATIS
DNS (Cloudflare):                          GRATIS
CI/CD (GitHub Actions free tier):          GRATIS
────────────────────────────────────────────────────
Total mensual:                             ~$5/mes
```

### Siguientes Pasos Sugeridos

1. ✅ Agregar contenido al portfolio
2. ✅ Configurar Google Analytics
3. ✅ Implementar blog con MDX
4. ✅ Agregar proyectos destacados
5. ✅ Optimizar SEO
6. ✅ Implementar dark mode
7. ✅ Agregar i18n completo (EN, ES, PT)
8. ✅ Configurar backups automáticos

---

**📚 Esta documentación está completa y lista para usar!**

**Última actualización:** Enero 2026

**Versión:** 1.0.0
