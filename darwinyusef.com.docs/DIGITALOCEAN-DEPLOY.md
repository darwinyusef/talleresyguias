# Guía de Deployment en DigitalOcean

Esta guía cubre las diferentes opciones para desplegar tu portfolio Astro en DigitalOcean.

## Índice
- [Opción 1: DigitalOcean App Platform (Recomendado)](#opción-1-digitalocean-app-platform)
- [Opción 2: Droplet con Docker](#opción-2-droplet-con-docker)
- [Opción 3: Kubernetes (DOKS)](#opción-3-digitalocean-kubernetes-doks)
- [Opción 4: Container Registry + Droplet](#opción-4-container-registry--droplet)

---

## Opción 1: DigitalOcean App Platform (Recomendado)

**Ventajas:**
- ✅ Más fácil y rápido
- ✅ Auto-scaling
- ✅ SSL automático
- ✅ CI/CD integrado con GitHub
- ✅ No necesitas gestionar servidores
- ✅ Desde $5/mes

**Costo:** $5-12/mes dependiendo recursos

### Paso 1: Preparar App Spec

Ya tienes el archivo `.do/app.yaml` configurado. Puedes ajustarlo según necesites.

### Paso 2: Deploy desde GitHub

```bash
# Opción A: Desde la UI de DigitalOcean
1. Ve a https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Conecta tu repositorio GitHub: darwinyusef/darwinyusef.portfolio
4. Selecciona la rama: main
5. DigitalOcean detectará automáticamente el Dockerfile
6. Click "Next" y sigue los pasos

# Opción B: Usando doctl CLI
doctl apps create --spec .do/app.yaml
```

### Paso 3: Configurar Variables de Entorno

En la UI de DigitalOcean App Platform:
1. Ve a Settings → Environment Variables
2. Agrega las variables del archivo `.env.example`

### Paso 4: Deploy Automático

Cada push a `main` desplegará automáticamente.

**URLs:**
- App URL: `https://tu-app-xxxxx.ondigitalocean.app`
- Custom Domain: Configurable en Settings → Domains

---

## Opción 2: Droplet con Docker

**Ventajas:**
- ✅ Control total del servidor
- ✅ Más barato para proyectos pequeños
- ✅ Fácil de entender

**Costo:** $4-6/mes (Droplet básico)

### Paso 1: Crear Droplet

```bash
# Crear Droplet con doctl
doctl compute droplet create portfolio \
  --image docker-20-04 \
  --size s-1vcpu-1gb \
  --region nyc1 \
  --ssh-keys YOUR_SSH_KEY_ID

# O desde la UI:
# 1. Ve a https://cloud.digitalocean.com/droplets
# 2. Create → Droplets
# 3. Selecciona "Docker on Ubuntu 22.04"
# 4. Plan: Basic $6/mes (1GB RAM)
# 5. Datacenter: New York / San Francisco
```

### Paso 2: Conectar al Droplet

```bash
# Obtener IP del droplet
doctl compute droplet list

# Conectar vía SSH
ssh root@YOUR_DROPLET_IP
```

### Paso 3: Configurar Droplet

```bash
# Actualizar sistema
apt update && apt upgrade -y

# Instalar Docker Compose (si no está)
apt install docker-compose -y

# Instalar Git
apt install git -y

# Crear usuario para la app (opcional pero recomendado)
adduser portfolio
usermod -aG docker portfolio
su - portfolio
```

### Paso 4: Clonar y Desplegar

```bash
# Clonar repositorio
cd ~
git clone https://github.com/darwinyusef/darwinyusef.portfolio.git
cd darwinyusef.portfolio/astro-portfolio

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar según necesites

# Build y deploy
docker-compose up -d --build

# Verificar
docker-compose ps
docker-compose logs -f
```

### Paso 5: Configurar Nginx como Reverse Proxy (Opcional)

```bash
# Instalar Nginx en el host
apt install nginx -y

# Configurar reverse proxy
cat > /etc/nginx/sites-available/portfolio << 'EOF'
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

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
EOF

# Activar sitio
ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### Paso 6: Configurar SSL con Certbot

```bash
# Instalar Certbot
apt install certbot python3-certbot-nginx -y

# Obtener certificado SSL
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# El certificado se renovará automáticamente
```

### Paso 7: Configurar Auto-Deploy con GitHub Webhooks

```bash
# Crear script de deploy
cat > ~/deploy.sh << 'EOF'
#!/bin/bash
cd ~/darwinyusef.portfolio/astro-portfolio
git pull origin main
docker-compose down
docker-compose up -d --build
docker image prune -f
EOF

chmod +x ~/deploy.sh
```

---

## Opción 3: DigitalOcean Kubernetes (DOKS)

**Ventajas:**
- ✅ Alta disponibilidad
- ✅ Auto-scaling
- ✅ Ideal para múltiples aplicaciones
- ✅ Kubernetes managed

**Costo:** ~$12/mes (cluster mínimo)

### Paso 1: Crear Cluster DOKS

```bash
# Con doctl
doctl kubernetes cluster create portfolio-cluster \
  --region nyc1 \
  --node-pool "name=worker-pool;size=s-1vcpu-2gb;count=2" \
  --version latest

# Configurar kubectl
doctl kubernetes cluster kubeconfig save portfolio-cluster
```

### Paso 2: Crear Container Registry

```bash
# Crear registry
doctl registry create portfolio-registry

# Login
doctl registry login
```

### Paso 3: Build y Push Imagen

```bash
cd astro-portfolio

# Build imagen
docker build -t registry.digitalocean.com/portfolio-registry/portfolio:latest .

# Push
docker push registry.digitalocean.com/portfolio-registry/portfolio:latest
```

### Paso 4: Actualizar manifiestos K8s

```bash
# Editar deploy/portfolio/k8s-deployment.yaml
# Cambiar la línea 27:
# image: registry.digitalocean.com/portfolio-registry/portfolio:latest
```

### Paso 5: Deploy en Kubernetes

```bash
# Aplicar namespaces
kubectl apply -f deploy/portfolio/k8s-namespace.yaml

# Aplicar deployment
kubectl apply -f deploy/portfolio/k8s-deployment.yaml

# Crear Ingress para exponer el servicio
kubectl apply -f deploy/portfolio/k8s-ingress.yaml

# Verificar
kubectl get pods -n production
kubectl get svc -n production
kubectl logs -f deployment/portfolio-deployment -n production
```

### Paso 6: Configurar Load Balancer

```yaml
# deploy/portfolio/k8s-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: portfolio-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - tu-dominio.com
    secretName: portfolio-tls
  rules:
  - host: tu-dominio.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: portfolio-service
            port:
              number: 80
```

---

## Opción 4: Container Registry + Droplet

Combina lo mejor de ambos mundos:

### Paso 1: Configurar Container Registry

```bash
# Crear registry
doctl registry create portfolio-registry

# Login
doctl registry login
```

### Paso 2: Automatizar Build y Push

```bash
# En tu máquina local o CI/CD
cd astro-portfolio

# Build
docker build -t registry.digitalocean.com/portfolio-registry/portfolio:latest .

# Push
docker push registry.digitalocean.com/portfolio-registry/portfolio:latest
```

### Paso 3: En el Droplet, Pull y Run

```bash
# SSH al droplet
ssh root@YOUR_DROPLET_IP

# Login al registry
doctl registry login

# Pull imagen
docker pull registry.digitalocean.com/portfolio-registry/portfolio:latest

# Run
docker run -d \
  --name portfolio \
  --restart always \
  -p 3000:8080 \
  registry.digitalocean.com/portfolio-registry/portfolio:latest

# O con docker-compose personalizado
```

---

## Comparación de Opciones

| Característica | App Platform | Droplet+Docker | DOKS | Registry+Droplet |
|----------------|--------------|----------------|------|------------------|
| **Costo/mes** | $5-12 | $4-6 | $12+ | $5-8 |
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Auto-scaling** | ✅ | ❌ | ✅ | ❌ |
| **SSL Auto** | ✅ | ❌ (manual) | ⚠️ (cert-manager) | ❌ (manual) |
| **CI/CD** | ✅ Built-in | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual |
| **Mantenimiento** | Bajo | Medio | Alto | Medio |
| **Control** | Medio | Alto | Muy Alto | Alto |

---

## Recomendación por Escenario

### Para empezar rápido:
**→ App Platform** (Opción 1)

### Para máximo control y costo mínimo:
**→ Droplet + Docker** (Opción 2)

### Para aplicaciones enterprise:
**→ DOKS** (Opción 3)

### Para CI/CD avanzado:
**→ Registry + Droplet** (Opción 4)

---

## Configuración de Dominio

Para todas las opciones, si tienes un dominio:

1. **En DigitalOcean Networking:**
   - Ve a Networking → Domains
   - Agrega tu dominio
   - Crea registros DNS:
     ```
     A Record: @ → IP_DEL_DROPLET o LOAD_BALANCER
     A Record: www → IP_DEL_DROPLET o LOAD_BALANCER
     ```

2. **En tu registrador de dominios:**
   - Configura los nameservers:
     ```
     ns1.digitalocean.com
     ns2.digitalocean.com
     ns3.digitalocean.com
     ```

---

## Monitoreo y Logs

```bash
# App Platform
doctl apps logs YOUR_APP_ID --type run --follow

# Droplet
ssh root@IP
docker-compose logs -f

# Kubernetes
kubectl logs -f deployment/portfolio-deployment -n production
```

---

## Costos Estimados

| Configuración | Componentes | Costo/mes |
|---------------|-------------|-----------|
| **Mínimo** | App Platform Starter | $5 |
| **Básico** | Droplet 1GB + Backup | $6-8 |
| **Medio** | App Platform Pro | $12 |
| **Avanzado** | DOKS (2 nodes) + Registry | $16-20 |

---

## Próximos Pasos

Después de elegir tu opción de deployment:

1. ✅ Configurar monitoring (DigitalOcean Monitoring es gratis)
2. ✅ Configurar backups automáticos
3. ✅ Implementar CI/CD con GitHub Actions
4. ✅ Configurar alertas
5. ✅ Optimizar costos

---

## Soporte

- **DigitalOcean Docs**: https://docs.digitalocean.com
- **Community**: https://www.digitalocean.com/community
- **Support**: Disponible desde el panel de control

**Última actualización**: Enero 2026
