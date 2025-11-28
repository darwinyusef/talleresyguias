# Módulo 9: Seguridad en Docker

## Índice
1. [Principios de Seguridad](#principios)
2. [Imágenes Seguras](#imágenes)
3. [Contenedores Seguros](#contenedores)
4. [Redes y Secrets](#redes)
5. [Scanning y Auditoría](#scanning)

---

## Principios de Seguridad

### 1. Principio de Mínimo Privilegio

**NO hacer:**
```dockerfile
FROM ubuntu
USER root
# Todo como root
```

**HACER:**
```dockerfile
FROM ubuntu
RUN useradd -m -u 1001 appuser
USER appuser
WORKDIR /app
```

### 2. Imágenes Base Oficiales y Específicas

```dockerfile
# ✅ BIEN - Imagen oficial, versión específica, Alpine (mínima)
FROM node:18-alpine

# ❌ EVITAR - Latest, sin verificar
FROM node:latest
```

### 3. Multi-Stage Builds

```dockerfile
# Stage 1: Build (con herramientas de desarrollo)
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (solo runtime y archivos necesarios)
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

---

## Imágenes Seguras

### Mejores Prácticas

**1. No incluir secretos en imágenes:**
```dockerfile
# ❌ MAL
ENV API_KEY=mi_secret_key_12345

# ✅ BIEN - Pasar en runtime
# docker run -e API_KEY=$API_KEY myapp
```

**2. Minimizar capas y tamaño:**
```dockerfile
# ✅ Combinar comandos RUN
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
```

**3. Usar .dockerignore:**
```
.git
.env
node_modules
*.log
.DS_Store
secrets/
```

**4. No ejecutar como root:**
```dockerfile
FROM node:18-alpine

# Crear usuario no-root
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

# Cambiar ownership
WORKDIR /app
COPY --chown=nodejs:nodejs . .

# Cambiar a usuario no-root
USER nodejs

CMD ["node", "index.js"]
```

**5. Limitar capacidades:**
```bash
# Eliminar capacidades innecesarias
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
```

---

## Contenedores Seguros

### 1. Read-Only Filesystem

```bash
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /var/run \
  myapp
```

```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

### 2. Resource Limits

```yaml
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M
```

### 3. Security Options

```bash
docker run \
  --security-opt=no-new-privileges:true \
  --security-opt=seccomp=unconfined \
  myapp
```

### 4. AppArmor/SELinux

```bash
# Usar perfil de seguridad
docker run --security-opt apparmor=docker-default myapp
```

---

## Redes y Secrets

### 1. Redes Personalizadas

```yaml
version: '3.8'

services:
  frontend:
    networks:
      - frontend-network

  backend:
    networks:
      - frontend-network
      - backend-network

  database:
    networks:
      - backend-network  # No accesible desde frontend

networks:
  frontend-network:
  backend-network:
```

### 2. Docker Secrets

```bash
# Crear secret
echo "mi_password_seguro" | docker secret create db_password -

# Usar en service
docker service create \
  --name myapp \
  --secret db_password \
  myapp:latest
```

```yaml
# docker-compose.yml (Swarm mode)
version: '3.8'

services:
  app:
    image: myapp
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

### 3. Variables de Entorno Seguras

```bash
# ❌ NO hacer - visible en docker inspect
docker run -e DB_PASSWORD=secret123 myapp

# ✅ Usar secrets o archivos externos
docker run --env-file .env myapp
```

---

## Scanning y Auditoría

### 1. Docker Scout (Built-in)

```bash
# Habilitar Docker Scout
docker scout quickview myapp:latest

# Análisis de vulnerabilidades
docker scout cves myapp:latest

# Comparar con otra imagen
docker scout compare myapp:latest --to myapp:previous
```

### 2. Trivy

```bash
# Instalar Trivy
brew install trivy

# Escanear imagen
trivy image myapp:latest

# Solo vulnerabilidades críticas/altas
trivy image --severity HIGH,CRITICAL myapp:latest

# Generar reporte
trivy image --format json -o report.json myapp:latest
```

### 3. Snyk

```bash
# Instalar Snyk
npm install -g snyk

# Login
snyk auth

# Escanear imagen
snyk container test myapp:latest

# Monitorear imagen
snyk container monitor myapp:latest
```

### 4. Clair

```yaml
# docker-compose.yml
version: '3.8'

services:
  clair:
    image: quay.io/coreos/clair:latest
    ports:
      - "6060:6060"
      - "6061:6061"
```

### 5. Integrar en CI/CD

**.github/workflows/security.yml:**
```yaml
name: Security Scan

on: [push]

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          severity: 'CRITICAL,HIGH'
          exit-code: '1'  # Fallar si encuentra vulnerabilidades
```

---

## Hardening del Docker Daemon

### 1. Configurar TLS

```bash
# Generar certificados
openssl genrsa -out ca-key.pem 4096
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem

# Configurar daemon
# /etc/docker/daemon.json
{
  "tls": true,
  "tlscert": "/path/to/cert.pem",
  "tlskey": "/path/to/key.pem",
  "tlsverify": true,
  "tlscacert": "/path/to/ca.pem"
}
```

### 2. Limitar Acceso al Socket

```bash
# Solo root puede acceder
sudo chmod 600 /var/run/docker.sock

# Agregar usuario específico al grupo docker
sudo usermod -aG docker $USER
```

### 3. Content Trust (Firmar Imágenes)

```bash
# Habilitar content trust
export DOCKER_CONTENT_TRUST=1

# Solo permite pull de imágenes firmadas
docker pull myapp:latest  # Verifica firma
```

---

## Docker Bench Security

```bash
# Ejecutar Docker Bench
docker run -it --net host --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /var/lib:/var/lib \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc \
  --label docker_bench_security \
  docker/docker-bench-security
```

---

## Checklist de Seguridad

### Imágenes
- [ ] Usar imágenes base oficiales
- [ ] Especificar tags de versión
- [ ] Usar Alpine o distroless cuando sea posible
- [ ] Multi-stage builds
- [ ] No incluir secretos
- [ ] Escanear vulnerabilidades
- [ ] Firmar imágenes

### Contenedores
- [ ] No ejecutar como root
- [ ] Read-only filesystem
- [ ] Resource limits
- [ ] Drop capabilities innecesarias
- [ ] Usar security options

### Redes
- [ ] Redes personalizadas
- [ ] Aislamiento entre servicios
- [ ] Firewalls configurados

### Secrets
- [ ] Usar Docker secrets (Swarm) o alternativas
- [ ] No hard-codear en código
- [ ] Rotar regularmente

### Operaciones
- [ ] Actualizar Docker regularmente
- [ ] Auditar con Docker Bench
- [ ] Logs centralizados
- [ ] Monitoreo de seguridad
- [ ] Backups regulares

---

## Recursos

- [Docker Security](https://docs.docker.com/engine/security/)
- [OWASP Docker Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)

---

**Recuerda:** La seguridad es un proceso continuo, no un estado final.
