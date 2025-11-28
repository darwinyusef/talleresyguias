# Módulo 7: Kubernetes - Orquestación de Contenedores a Escala

## Objetivo
Aprender a desplegar, escalar y administrar aplicaciones containerizadas usando Kubernetes.

---

## Índice

1. [¿Qué es Kubernetes?](#qué-es-kubernetes)
2. [Arquitectura de Kubernetes](#arquitectura-de-kubernetes)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Conceptos Fundamentales](#conceptos-fundamentales)
5. [Recursos de Kubernetes](#recursos-de-kubernetes)
6. [Despliegue de Aplicaciones](#despliegue-de-aplicaciones)
7. [Networking y Servicios](#networking-y-servicios)
8. [Volúmenes y Almacenamiento](#volúmenes-y-almacenamiento)
9. [ConfigMaps y Secrets](#configmaps-y-secrets)
10. [Escalado y Auto-scaling](#escalado-y-auto-scaling)
11. [Helm - Package Manager](#helm---package-manager)

---

## ¿Qué es Kubernetes?

Kubernetes (K8s) es un sistema open-source para automatizar el despliegue, escalado y gestión de aplicaciones containerizadas.

### Características Principales

- **Orquestación de contenedores** - Administra múltiples contenedores
- **Auto-scaling** - Escala automáticamente según demanda
- **Auto-healing** - Reemplaza contenedores fallidos
- **Service discovery** - Descubrimiento automático de servicios
- **Load balancing** - Distribución de carga
- **Rolling updates** - Actualizaciones sin downtime
- **Rollbacks** - Reversión a versiones anteriores

### Cuándo Usar Kubernetes

**Usar K8s cuando:**
- Aplicación distribuida con múltiples servicios
- Necesitas alta disponibilidad
- Escalado automático requerido
- Múltiples ambientes (dev, staging, prod)
- Equipo grande, múltiples deployments

**NO usar K8s cuando:**
- Aplicación simple, monolítica
- Tráfico bajo, predecible
- Equipo pequeño sin experiencia K8s
- Recursos limitados
- Prototipo o MVP rápido

---

## Arquitectura de Kubernetes

### Componentes del Control Plane (Master)

**1. API Server** - Frontend del control plane, expone API de K8s
**2. etcd** - Base de datos key-value, almacena estado del cluster
**3. Scheduler** - Asigna Pods a Nodes
**4. Controller Manager** - Ejecuta controladores (Deployment, ReplicaSet, etc.)
**5. Cloud Controller Manager** - Integración con proveedores cloud

### Componentes del Node (Worker)

**1. kubelet** - Agente que corre en cada node, administra Pods
**2. kube-proxy** - Proxy de red, maneja reglas de red
**3. Container Runtime** - Docker, containerd, CRI-O

### Arquitectura Visual

```
┌─────────────────── Control Plane ───────────────────┐
│                                                      │
│  ┌──────────┐  ┌──────┐  ┌───────────┐  ┌────────┐ │
│  │API Server├─→│ etcd │  │ Scheduler │  │Controller│ │
│  └──────────┘  └──────┘  └───────────┘  └────────┘ │
└──────────────────────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        ↓                                 ↓
┌──── Node 1 ────┐              ┌──── Node 2 ────┐
│                │              │                │
│  ┌────────┐   │              │  ┌────────┐   │
│  │kubelet │   │              │  │kubelet │   │
│  └────────┘   │              │  └────────┘   │
│               │              │               │
│  ┌──────────┐ │              │  ┌──────────┐ │
│  │Pod │Pod  │ │              │  │Pod │Pod  │ │
│  └──────────┘ │              │  └──────────┘ │
└────────────────┘              └────────────────┘
```

---

## Instalación y Configuración

### 1. Minikube (Local, Desarrollo)

**Instalación en macOS:**
```bash
brew install minikube
```

**Instalación en Linux:**
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**Iniciar Minikube:**
```bash
minikube start
minikube status
minikube dashboard
```

**Detener/Eliminar:**
```bash
minikube stop
minikube delete
```

### 2. kubectl - Cliente de Kubernetes

**Instalación:**
```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

**Verificar:**
```bash
kubectl version --client
kubectl cluster-info
kubectl get nodes
```

**Autocompletado (Bash):**
```bash
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'alias k=kubectl' >> ~/.bashrc
echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc
```

### 3. Kind (Kubernetes in Docker)

```bash
# Instalar
brew install kind

# Crear cluster
kind create cluster --name mi-cluster

# Listar clusters
kind get clusters

# Eliminar
kind delete cluster --name mi-cluster
```

### 4. K3s (Lightweight Kubernetes)

```bash
# Instalar
curl -sfL https://get.k3s.io | sh -

# Verificar
sudo k3s kubectl get nodes
```

---

## Conceptos Fundamentales

### Namespace
Agrupación lógica de recursos.

```bash
# Listar namespaces
kubectl get namespaces

# Crear namespace
kubectl create namespace desarrollo

# Usar namespace
kubectl get pods -n desarrollo
```

### Pod
Unidad más pequeña de deployment. Uno o más contenedores.

### ReplicaSet
Asegura que un número específico de Pods esté corriendo.

### Deployment
Gestiona ReplicaSets y Pods, permite updates y rollbacks.

### Service
Expone Pods para acceso de red.

### Ingress
Gestiona acceso externo a servicios HTTP/HTTPS.

---

## Recursos de Kubernetes

### Pod

**pod.yaml:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    ports:
    - containerPort: 80
```

**Comandos:**
```bash
# Crear Pod
kubectl apply -f pod.yaml

# Listar Pods
kubectl get pods
kubectl get pods -o wide

# Describir Pod
kubectl describe pod nginx-pod

# Ver logs
kubectl logs nginx-pod

# Entrar al Pod
kubectl exec -it nginx-pod -- /bin/sh

# Eliminar Pod
kubectl delete pod nginx-pod
```

### Deployment

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

**Comandos:**
```bash
# Crear Deployment
kubectl apply -f deployment.yaml

# Listar Deployments
kubectl get deployments

# Ver detalles
kubectl describe deployment nginx-deployment

# Escalar
kubectl scale deployment nginx-deployment --replicas=5

# Actualizar imagen
kubectl set image deployment/nginx-deployment nginx=nginx:1.26

# Ver historial de rollout
kubectl rollout history deployment/nginx-deployment

# Rollback
kubectl rollout undo deployment/nginx-deployment

# Ver estado de rollout
kubectl rollout status deployment/nginx-deployment

# Eliminar
kubectl delete deployment nginx-deployment
```

### Service

**service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: LoadBalancer  # ClusterIP, NodePort, LoadBalancer
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30080  # Solo para NodePort
```

**Tipos de Service:**

1. **ClusterIP** (default) - Solo accesible dentro del cluster
2. **NodePort** - Expone en puerto del node
3. **LoadBalancer** - Crea balanceador externo
4. **ExternalName** - DNS CNAME

**Comandos:**
```bash
kubectl apply -f service.yaml
kubectl get services
kubectl describe service nginx-service

# Port-forward (desarrollo)
kubectl port-forward service/nginx-service 8080:80
```

---

## Despliegue de Aplicaciones

### Ejemplo Completo: Aplicación React + Node + PostgreSQL

**namespace.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
```

**postgres.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_USER
          value: "usuario"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: POSTGRES_DB
          value: "appdb"
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: myapp
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

**backend.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: username/backend:latest
        env:
        - name: DATABASE_URL
          value: "postgresql://usuario:password@postgres-service:5432/appdb"
        - name: NODE_ENV
          value: "production"
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: myapp
spec:
  selector:
    app: backend
  ports:
  - port: 3000
    targetPort: 3000
```

**frontend.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: username/frontend:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: myapp
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
```

**Desplegar:**
```bash
kubectl apply -f namespace.yaml
kubectl apply -f postgres.yaml
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml

# Ver recursos
kubectl get all -n myapp

# Ver logs
kubectl logs -f deployment/backend -n myapp
```

---

## Networking y Servicios

### Ingress

**ingress.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  namespace: myapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 3000
```

**Instalar Ingress Controller (Nginx):**
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

---

## Volúmenes y Almacenamiento

### PersistentVolume (PV)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/postgres
```

### PersistentVolumeClaim (PVC)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: myapp
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

---

## ConfigMaps y Secrets

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp
data:
  API_URL: "https://api.example.com"
  LOG_LEVEL: "info"
  database.conf: |
    max_connections=100
    shared_buffers=256MB
```

**Usar en Pod:**
```yaml
env:
- name: API_URL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: API_URL
```

### Secret

```bash
# Crear Secret desde literal
kubectl create secret generic postgres-secret \
  --from-literal=password=mi_password_secreto \
  -n myapp

# Crear Secret desde archivo
kubectl create secret generic tls-secret \
  --from-file=tls.crt=./cert.crt \
  --from-file=tls.key=./cert.key \
  -n myapp
```

**secret.yaml:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: myapp
type: Opaque
data:
  password: bWlfcGFzc3dvcmRfc2VjcmV0bw==  # base64 encoded
```

**Usar en Pod:**
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: postgres-secret
      key: password
```

---

## Escalado y Auto-scaling

### HorizontalPodAutoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Comandos:**
```bash
# Crear HPA
kubectl apply -f hpa.yaml

# Ver HPA
kubectl get hpa -n myapp

# Autoscale con comando
kubectl autoscale deployment backend \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n myapp
```

---

## Helm - Package Manager

### Instalación

```bash
# macOS
brew install helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Usar Helm Charts

```bash
# Agregar repositorio
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Buscar charts
helm search repo postgresql

# Instalar chart
helm install my-postgres bitnami/postgresql \
  --namespace myapp \
  --create-namespace

# Listar releases
helm list -n myapp

# Actualizar release
helm upgrade my-postgres bitnami/postgresql \
  --set auth.postgresPassword=newpassword

# Desinstalar
helm uninstall my-postgres -n myapp
```

### Crear tu propio Chart

```bash
# Crear estructura de chart
helm create myapp

# Estructura:
myapp/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── charts/
```

**values.yaml:**
```yaml
replicaCount: 3

image:
  repository: username/myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

**Instalar tu chart:**
```bash
helm install myapp ./myapp -n myapp
```

---

## Comandos Esenciales

```bash
# Cluster
kubectl cluster-info
kubectl get nodes

# Pods
kubectl get pods
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs -f <pod-name>
kubectl exec -it <pod-name> -- /bin/bash

# Deployments
kubectl get deployments
kubectl scale deployment <name> --replicas=5
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>

# Services
kubectl get services
kubectl get svc

# Ver todo
kubectl get all
kubectl get all -n <namespace>

# Aplicar manifiestos
kubectl apply -f file.yaml
kubectl apply -f directory/

# Eliminar
kubectl delete -f file.yaml
kubectl delete pod <pod-name>
kubectl delete deployment <deployment-name>

# Debugging
kubectl describe <resource> <name>
kubectl logs <pod-name>
kubectl top nodes
kubectl top pods
```

---

## Mejores Prácticas

1. **Usar namespaces** para organizar recursos
2. **Definir resource limits** para evitar overconsumption
3. **Implementar health checks** (liveness, readiness)
4. **Usar labels** consistentes
5. **Versionar imágenes** (no usar :latest en prod)
6. **Usar Secrets** para información sensible
7. **Implementar HPA** para escalado automático
8. **Backups regulares** de etcd
9. **Monitoreo y logging** centralizado
10. **GitOps** para deployments

---

## Troubleshooting

```bash
# Pod no inicia
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Ver eventos
kubectl get events --sort-by=.metadata.creationTimestamp

# Pod stuck en Pending
kubectl describe pod <pod-name>  # Ver razón en Events

# Service no accesible
kubectl get endpoints <service-name>
kubectl describe service <service-name>

# Ver recursos del cluster
kubectl top nodes
kubectl top pods

# Verificar conectividad
kubectl run test --rm -it --image=busybox -- sh
> wget -O- http://service-name
```

---

## Recursos

- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Kubernetes by Example](https://kubernetesbyexample.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

---

Este módulo te ha introducido a Kubernetes. El siguiente paso es practicar desplegando tus propias aplicaciones y explorando temas avanzados como StatefulSets, DaemonSets, y operadores de Kubernetes.
