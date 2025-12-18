# K8s Admin Scripts

Scripts de administración para el cluster de Kubernetes.

## 🚀 Uso del Contenedor K8s Admin

### Opción 1: Docker Compose

```bash
# Construir imagen
docker-compose -f docker-compose.admin.yml build

# Ejecutar contenedor interactivo
docker-compose -f docker-compose.admin.yml run --rm k8s-admin

# Dentro del contenedor tendrás todas las herramientas
```

### Opción 2: Docker directo

```bash
# Build
docker build -f Dockerfile.k8s-admin -t mlops-k8s-admin .

# Run
docker run -it --rm \
  -v $HOME/.kube:/root/.kube:ro \
  -v $(pwd)/k8s:/workspace/k8s \
  -v $(pwd)/ansible:/workspace/ansible \
  mlops-k8s-admin
```

## 📜 Scripts Disponibles

### deploy.sh - Deploy completo

```bash
# Dentro del contenedor admin
cd /workspace/k8s-admin-scripts
chmod +x deploy.sh
./deploy.sh
```

Despliega toda la plataforma MLOps en Kubernetes.

### monitor.sh - Monitoreo

```bash
chmod +x monitor.sh
./monitor.sh
```

Muestra estado completo del cluster.

## 🛠️ Herramientas Incluidas

El contenedor incluye:

- **kubectl** - CLI de Kubernetes
- **helm** - Package manager K8s
- **k9s** - UI interactiva para K8s
- **terraform** - Infrastructure as Code
- **ansible** - Automation
- **kubectx/kubens** - Cambiar contextos fácilmente
- **kustomize** - Template-free customization
- **Docker CLI** - Para Docker-in-Docker
- **AWS/Azure/GCloud CLI** - Cloud providers

## 📝 Comandos Útiles

### Dentro del contenedor

```bash
# Ver cluster info
kubectl cluster-info

# Cambiar namespace por defecto
kubens mlops

# UI interactiva
k9s

# Listar helm releases
helm list -A

# Ver logs
kubectl logs -f deployment/pytorch-service -n mlops

# Shell en pod
kubectl exec -it <pod-name> -n mlops -- /bin/bash

# Port forward
kubectl port-forward svc/pytorch-service 8000:8000 -n mlops
```

### Alias preconfigurados

```bash
k         # kubectl
kgp       # kubectl get pods
kgs       # kubectl get svc
kgd       # kubectl get deployments
kga       # kubectl get all
klf       # kubectl logs -f
kex       # kubectl exec -it
```

## 🔐 Configuración

### Kubeconfig

El contenedor monta automáticamente `~/.kube/config` desde tu máquina host.

Para usar múltiples clusters:

```bash
# Ver contextos
kubectl config get-contexts

# Cambiar contexto
kubectx <context-name>

# O con kubectl
kubectl config use-context <context-name>
```

### Cloud Credentials

Monta las credenciales necesarias:

```yaml
# En docker-compose.admin.yml
volumes:
  - ${HOME}/.aws:/root/.aws:ro      # AWS
  - ${HOME}/.azure:/root/.azure:ro  # Azure
  - ${HOME}/.config/gcloud:/root/.config/gcloud:ro  # GCP
```

## 📊 Ejemplos de Uso

### Deploy inicial

```bash
# 1. Entrar al contenedor
docker-compose -f docker-compose.admin.yml run --rm k8s-admin

# 2. Verificar conexión
kubectl cluster-info

# 3. Deploy
cd /workspace/k8s-admin-scripts
./deploy.sh

# 4. Monitorear
./monitor.sh
```

### Actualizar deployment

```bash
# Actualizar imagen
kubectl set image deployment/pytorch-service \
  pytorch-service=ghcr.io/org/pytorch-service:v2.0 \
  -n mlops

# Ver rollout
kubectl rollout status deployment/pytorch-service -n mlops
```

### Debug de problemas

```bash
# Ver eventos
kubectl get events -n mlops --sort-by='.lastTimestamp'

# Describe pod con problemas
kubectl describe pod <pod-name> -n mlops

# Logs
kubectl logs <pod-name> -n mlops --previous

# Shell interactivo
kubectl exec -it <pod-name> -n mlops -- /bin/bash
```

## 🚀 Workflows Comunes

### 1. Deploy desde cero

```bash
./deploy.sh
./monitor.sh
```

### 2. Update de servicio

```bash
kubectl apply -f /workspace/k8s/pytorch-deployment.yaml
kubectl rollout status deployment/pytorch-service -n mlops
```

### 3. Rollback

```bash
kubectl rollout undo deployment/pytorch-service -n mlops
```

### 4. Scale manual

```bash
kubectl scale deployment/pytorch-service --replicas=5 -n mlops
```

## 🔧 Personalización

### Añadir herramientas adicionales

Edita `Dockerfile.k8s-admin`:

```dockerfile
# Añadir herramienta custom
RUN pip3 install my-custom-tool
```

Rebuild:

```bash
docker-compose -f docker-compose.admin.yml build
```

---

**Happy Kubernetes Administration! ⎈**
