# Módulo: Despliegue en Producción y Cloud

## Objetivo
Aprender a desplegar aplicaciones Docker en entornos de producción con SSL/HTTPS, en plataformas cloud (AWS, Azure) y Kubernetes gestionado.

---

## Parte 1: SSL/HTTPS con Let's Encrypt

### ¿Por qué SSL/HTTPS?

- **Seguridad**: Encripta datos entre cliente y servidor
- **SEO**: Google prioriza sitios HTTPS
- **Confianza**: Navegadores marcan HTTP como "No seguro"
- **Requisito**: Muchas APIs requieren HTTPS

### Opción 1: Nginx + Let's Encrypt + Certbot

#### Estructura del Proyecto

```
mi-app/
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   └── certbot/
├── app/
│   ├── Dockerfile
│   └── src/
└── .env
```

#### docker-compose.yml con Certbot

```yaml
version: '3.8'

services:
  app:
    build: ./app
    container_name: mi-app
    restart: unless-stopped
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
    networks:
      - app-network
    depends_on:
      - app

  certbot:
    image: certbot/certbot
    container_name: certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    # Renovación automática cada 12 horas
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

networks:
  app-network:
    driver: bridge
```

#### nginx/conf.d/default.conf (antes del certificado)

```nginx
server {
    listen 80;
    server_name midominio.com www.midominio.com;

    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect HTTP to HTTPS (después de obtener certificado)
    # location / {
    #     return 301 https://$host$request_uri;
    # }

    # Temporal: permitir tráfico HTTP
    location / {
        proxy_pass http://app:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Paso 1: Obtener Certificado SSL

```bash
# 1. Levantar servicios (sin HTTPS aún)
docker compose up -d nginx

# 2. Obtener certificado
docker compose run --rm certbot certonly \
  --webroot \
  --webroot-path /var/www/certbot \
  --email tu@email.com \
  --agree-tos \
  --no-eff-email \
  -d midominio.com \
  -d www.midominio.com

# 3. Verificar certificados
ls -la certbot/conf/live/midominio.com/
```

#### nginx/conf.d/default.conf (CON SSL)

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name midominio.com www.midominio.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name midominio.com www.midominio.com;

    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/midominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/midominio.com/privkey.pem;

    # SSL Configuration (Mozilla Intermediate)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS (opcional pero recomendado)
    add_header Strict-Transport-Security "max-age=63072000" always;

    # Proxy to app
    location / {
        proxy_pass http://app:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Paso 2: Activar HTTPS

```bash
# Recargar Nginx con nueva configuración
docker compose restart nginx

# Verificar
curl -I https://midominio.com
```

### Opción 2: Traefik con Let's Encrypt Automático

#### docker-compose.yml con Traefik

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./traefik/acme.json:/acme.json
    networks:
      - web

  app:
    build: ./app
    container_name: mi-app
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`midominio.com`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"
      - "traefik.http.services.app.loadbalancer.server.port=3000"
    networks:
      - web

networks:
  web:
    external: true
```

#### traefik/traefik.yml

```yaml
api:
  dashboard: true
  insecure: false

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

certificatesResolvers:
  letsencrypt:
    acme:
      email: tu@email.com
      storage: /acme.json
      httpChallenge:
        entryPoint: web

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
```

#### Configurar Traefik

```bash
# Crear red
docker network create web

# Crear archivo para certificados
touch traefik/acme.json
chmod 600 traefik/acme.json

# Levantar servicios
docker compose up -d
```

---

## Parte 2: AWS EC2 - Despliegue de Aplicaciones Docker

### Paso 1: Crear Instancia EC2

#### En AWS Console:

1. **Launch Instance**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (capa gratuita) o t2.medium
   - Key Pair: Crear y descargar `.pem`
   - Security Group:
     - SSH (22) - Tu IP
     - HTTP (80) - 0.0.0.0/0
     - HTTPS (443) - 0.0.0.0/0
     - Custom (tu app, ej: 3000) - 0.0.0.0/0

2. **Elastic IP** (opcional pero recomendado)
   - Allocate Elastic IP
   - Associate con tu instancia

### Paso 2: Conectar a EC2

```bash
# Dar permisos a la key
chmod 400 mi-key.pem

# Conectar via SSH
ssh -i mi-key.pem ubuntu@<ELASTIC-IP>
```

### Paso 3: Instalar Docker en EC2

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo apt install docker-compose-plugin -y

# Cerrar sesión y volver a conectar
exit
ssh -i mi-key.pem ubuntu@<ELASTIC-IP>

# Verificar
docker --version
docker compose version
```

### Paso 4: Desplegar Aplicación

#### Opción A: Clonar Repositorio

```bash
# Instalar git
sudo apt install git -y

# Clonar proyecto
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus valores

# Levantar servicios
docker compose up -d

# Ver logs
docker compose logs -f
```

#### Opción B: Docker Hub

```bash
# Crear docker-compose.yml en EC2
nano docker-compose.yml
```

```yaml
version: '3.8'

services:
  app:
    image: tu-usuario/tu-app:latest
    ports:
      - "80:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=miapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

```bash
# Levantar
docker compose up -d
```

### Paso 5: Configurar Dominio

#### En tu proveedor DNS (Namecheap, GoDaddy, Route53):

```
Tipo: A
Host: @
Value: <TU-ELASTIC-IP>
TTL: 3600

Tipo: A
Host: www
Value: <TU-ELASTIC-IP>
TTL: 3600
```

### Paso 6: SSL con Let's Encrypt en EC2

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Si usas Nginx en EC2 (no en Docker)
sudo certbot --nginx -d midominio.com -d www.midominio.com

# Si usas Docker, usar método anterior (Certbot container)
```

### Automatizar Despliegue con GitHub Actions

#### .github/workflows/deploy-ec2.yml

```yaml
name: Deploy to EC2

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to EC2
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/mi-proyecto
            git pull origin main
            docker compose pull
            docker compose up -d --build
            docker system prune -af
```

---

## Parte 3: Azure Virtual Machines

### Paso 1: Crear VM en Azure

```bash
# Usando Azure CLI
az login

# Crear grupo de recursos
az group create --name mi-app-rg --location eastus

# Crear VM
az vm create \
  --resource-group mi-app-rg \
  --name mi-app-vm \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Abrir puertos
az vm open-port --port 80 --resource-group mi-app-rg --name mi-app-vm
az vm open-port --port 443 --resource-group mi-app-rg --name mi-app-vm
az vm open-port --port 22 --resource-group mi-app-rg --name mi-app-vm

# Obtener IP pública
az vm show -d -g mi-app-rg -n mi-app-vm --query publicIps -o tsv
```

### Paso 2: Conectar y Configurar

```bash
# Conectar via SSH
ssh azureuser@<PUBLIC-IP>

# Instalar Docker (mismo proceso que EC2)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker azureuser
sudo apt install docker-compose-plugin -y

# Relogin
exit
ssh azureuser@<PUBLIC-IP>
```

### Paso 3: Azure Container Instances (Alternativa)

```bash
# Crear container instance directamente
az container create \
  --resource-group mi-app-rg \
  --name mi-app-container \
  --image tu-usuario/tu-app:latest \
  --dns-name-label mi-app-unica \
  --ports 80 443 \
  --environment-variables \
    NODE_ENV=production \
    DATABASE_URL=postgresql://... \
  --cpu 1 \
  --memory 1.5

# Ver estado
az container show \
  --resource-group mi-app-rg \
  --name mi-app-container \
  --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" \
  --out table

# Logs
az container logs --resource-group mi-app-rg --name mi-app-container
```

### Paso 4: Azure App Service con Docker

```bash
# Crear App Service Plan
az appservice plan create \
  --name mi-app-plan \
  --resource-group mi-app-rg \
  --is-linux \
  --sku B1

# Crear Web App con container
az webapp create \
  --resource-group mi-app-rg \
  --plan mi-app-plan \
  --name mi-app-web \
  --deployment-container-image-name tu-usuario/tu-app:latest

# Configurar variables de entorno
az webapp config appsettings set \
  --resource-group mi-app-rg \
  --name mi-app-web \
  --settings \
    NODE_ENV=production \
    DATABASE_URL=postgresql://...

# Habilitar HTTPS
az webapp update \
  --resource-group mi-app-rg \
  --name mi-app-web \
  --https-only true

# Custom domain
az webapp config hostname add \
  --webapp-name mi-app-web \
  --resource-group mi-app-rg \
  --hostname midominio.com
```

---

## Parte 4: Kubernetes en la Nube

### AWS EKS (Elastic Kubernetes Service)

#### Paso 1: Instalar herramientas

```bash
# Instalar eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Instalar kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Instalar AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configurar AWS
aws configure
```

#### Paso 2: Crear Cluster EKS

```bash
# Crear cluster (tarda ~15 minutos)
eksctl create cluster \
  --name mi-cluster \
  --region us-east-1 \
  --nodegroup-name mi-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed

# Verificar
kubectl get nodes
```

#### Paso 3: Desplegar Aplicación en EKS

**deployment.yml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mi-app
  template:
    metadata:
      labels:
        app: mi-app
    spec:
      containers:
      - name: mi-app
        image: tu-usuario/tu-app:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
---
apiVersion: v1
kind: Service
metadata:
  name: mi-app-service
spec:
  type: LoadBalancer
  selector:
    app: mi-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
```

```bash
# Crear secret
kubectl create secret generic app-secrets \
  --from-literal=database-url='postgresql://...'

# Aplicar deployment
kubectl apply -f deployment.yml

# Ver servicio (obtener EXTERNAL-IP)
kubectl get svc mi-app-service -w
```

#### Paso 4: Ingress Controller con SSL

```bash
# Instalar Nginx Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/aws/deploy.yaml

# Instalar cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

**ingress.yml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mi-app-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - midominio.com
    secretName: mi-app-tls
  rules:
  - host: midominio.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: mi-app-service
            port:
              number: 80
```

**cluster-issuer.yml:**
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: tu@email.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

```bash
# Aplicar
kubectl apply -f cluster-issuer.yml
kubectl apply -f ingress.yml

# Verificar certificado
kubectl get certificate
```

### Azure AKS (Azure Kubernetes Service)

```bash
# Crear cluster
az aks create \
  --resource-group mi-app-rg \
  --name mi-aks-cluster \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --enable-addons monitoring \
  --generate-ssh-keys

# Obtener credenciales
az aks get-credentials --resource-group mi-app-rg --name mi-aks-cluster

# Verificar
kubectl get nodes

# Desplegar (mismo proceso que EKS)
kubectl apply -f deployment.yml
```

### Google GKE (Google Kubernetes Engine)

```bash
# Instalar gcloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Crear cluster
gcloud container clusters create mi-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-medium

# Obtener credenciales
gcloud container clusters get-credentials mi-cluster --zone us-central1-a

# Verificar
kubectl get nodes
```

---

## Parte 5: Servicios Externos

### AWS RDS (Base de Datos Gestionada)

```bash
# Crear RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier mi-app-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password MiPassword123! \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxxxx \
  --publicly-accessible

# Obtener endpoint
aws rds describe-db-instances \
  --db-instance-identifier mi-app-db \
  --query 'DBInstances[0].Endpoint.Address'
```

### AWS S3 (Almacenamiento de Archivos)

```bash
# Crear bucket
aws s3 mb s3://mi-app-files

# Configurar política pública (si es necesario)
aws s3api put-bucket-policy --bucket mi-app-files --policy file://policy.json
```

**policy.json:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::mi-app-files/*"
    }
  ]
}
```

**En tu aplicación (Node.js):**
```javascript
const AWS = require('aws-sdk');
const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY,
  secretAccessKey: process.env.AWS_SECRET_KEY,
  region: 'us-east-1'
});

// Upload
const uploadFile = async (file) => {
  const params = {
    Bucket: 'mi-app-files',
    Key: file.name,
    Body: file.data,
    ContentType: file.mimetype
  };
  return s3.upload(params).promise();
};
```

### Azure Blob Storage

```bash
# Crear storage account
az storage account create \
  --name miappstorage \
  --resource-group mi-app-rg \
  --location eastus \
  --sku Standard_LRS

# Crear container
az storage container create \
  --name files \
  --account-name miappstorage \
  --public-access blob
```

### Redis Cloud (Caché Externa)

**Redis Labs / Upstash:**

```bash
# En tu aplicación
docker-compose.yml:
```

```yaml
services:
  app:
    environment:
      - REDIS_URL=redis://username:password@redis-xxxxx.cloud.redislabs.com:12345
```

### SendGrid / AWS SES (Email)

**SendGrid:**
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const msg = {
  to: 'user@example.com',
  from: 'noreply@miapp.com',
  subject: 'Bienvenido',
  text: 'Gracias por registrarte'
};

await sgMail.send(msg);
```

---

## Parte 6: Mejores Prácticas en Producción

### 1. Variables de Entorno y Secretos

```bash
# NUNCA en código
DATABASE_URL=postgresql://user:pass@host:5432/db

# Usar servicios de secretos
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name mi-app/database-url \
  --secret-string "postgresql://..."

# En tu app (Node.js)
const AWS = require('aws-sdk');
const client = new AWS.SecretsManager({region: 'us-east-1'});

const secret = await client.getSecretValue({SecretId: 'mi-app/database-url'}).promise();
const DATABASE_URL = secret.SecretString;
```

### 2. Health Checks

```javascript
// Express.js
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

app.get('/ready', async (req, res) => {
  try {
    await db.query('SELECT 1');
    res.status(200).json({ status: 'ready' });
  } catch (error) {
    res.status(503).json({ status: 'not ready' });
  }
});
```

### 3. Logging en Producción

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Uso
logger.info('User logged in', { userId: 123 });
logger.error('Database error', { error: err.message });
```

### 4. Backups Automáticos

```bash
# Backup de PostgreSQL
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="miapp"

docker exec postgres pg_dump -U postgres $DB_NAME > $BACKUP_DIR/backup_$DATE.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/backup_$DATE.sql s3://mi-app-backups/

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

**Cron job:**
```bash
# Editar crontab
crontab -e

# Backup diario a las 2 AM
0 2 * * * /home/ubuntu/backup.sh
```

### 5. Monitoreo en Producción

```yaml
# docker-compose.yml con monitoreo
version: '3.8'

services:
  app:
    # ...
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=3000"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123

volumes:
  prometheus_data:
  grafana_data:
```

---

## Resumen de Comandos Útiles

### SSL/HTTPS
```bash
# Renovar certificados manualmente
docker compose run --rm certbot renew

# Verificar certificado
openssl s_client -connect midominio.com:443 -servername midominio.com
```

### AWS EC2
```bash
# Ver instancias
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]'

# Conectar
ssh -i mi-key.pem ubuntu@<IP>

# Ver logs de aplicación
docker compose logs -f app
```

### Azure
```bash
# Listar VMs
az vm list -o table

# Iniciar/Detener VM
az vm start --resource-group mi-app-rg --name mi-app-vm
az vm stop --resource-group mi-app-rg --name mi-app-vm

# Deallocate (deja de cobrar)
az vm deallocate --resource-group mi-app-rg --name mi-app-vm
```

### Kubernetes
```bash
# Ver pods
kubectl get pods

# Logs
kubectl logs -f <pod-name>

# Escalar
kubectl scale deployment mi-app --replicas=5

# Actualizar imagen
kubectl set image deployment/mi-app mi-app=tu-usuario/tu-app:v2

# Rollback
kubectl rollout undo deployment/mi-app
```

---

## Checklist de Producción

- [ ] SSL/HTTPS configurado
- [ ] Variables de entorno en secretos (no en código)
- [ ] Health checks implementados
- [ ] Logging centralizado
- [ ] Backups automáticos configurados
- [ ] Monitoreo activo (Prometheus/Grafana o similar)
- [ ] Alertas configuradas
- [ ] Firewall/Security Groups configurados
- [ ] Auto-scaling configurado (si aplica)
- [ ] Disaster recovery plan documentado
- [ ] CI/CD pipeline funcionando
- [ ] Dominio apuntando correctamente
- [ ] DNS configurado
- [ ] Rate limiting implementado
- [ ] CORS configurado apropiadamente

---

¡Tu aplicación está lista para producción! 🚀
