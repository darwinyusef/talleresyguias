# Kubernetes Deployment

Manifests de Kubernetes para desplegar la plataforma MLOps.

## 📁 Archivos

```
k8s/
├── namespace.yaml              # Namespace mlops
├── configmap.yaml             # Configuración
├── secrets.yaml               # Secretos (NO commitear en producción)
├── storage.yaml               # PersistentVolumeClaims
├── pytorch-deployment.yaml    # PyTorch Service + HPA
├── ingress.yaml               # Ingress NGINX
└── README.md                  # Esta documentación
```

## 🚀 Quick Deploy

### 1. Crear Namespace y Configuración

```bash
# Crear namespace
kubectl apply -f namespace.yaml

# Configuración
kubectl apply -f configmap.yaml

# Secretos (usa kubectl create secret en producción)
kubectl apply -f secrets.yaml
```

### 2. Storage

```bash
# Crear PVCs
kubectl apply -f storage.yaml

# Verificar
kubectl get pvc -n mlops
```

### 3. Deploy Services

```bash
# PyTorch Service
kubectl apply -f pytorch-deployment.yaml

# TensorFlow Service (crear similar)
# kubectl apply -f tensorflow-deployment.yaml

# RAG Service
# kubectl apply -f rag-deployment.yaml
```

### 4. Ingress

```bash
# Ingress
kubectl apply -f ingress.yaml

# Verificar
kubectl get ingress -n mlops
```

## 📊 Verificar Deployment

```bash
# Ver todos los recursos
kubectl get all -n mlops

# Ver pods
kubectl get pods -n mlops

# Ver servicios
kubectl get svc -n mlops

# Logs
kubectl logs -f deployment/pytorch-service -n mlops

# Describir pod
kubectl describe pod <pod-name> -n mlops
```

## 🔧 Configuración GPU

### NVIDIA GPU Operator

```bash
# Instalar NVIDIA GPU Operator
helm repo add nvidia https://nvidia.github.io/gpu-operator
helm repo update

helm install gpu-operator nvidia/gpu-operator \
  --namespace gpu-operator \
  --create-namespace \
  --wait

# Verificar
kubectl get pods -n gpu-operator
```

### Node Labels

```bash
# Label nodes con GPU
kubectl label nodes <node-name> nvidia.com/gpu=true

# Verificar
kubectl get nodes -l nvidia.com/gpu=true
```

## 📈 Autoscaling

### HPA (Horizontal Pod Autoscaler)

```bash
# Ver HPA
kubectl get hpa -n mlops

# Describir
kubectl describe hpa pytorch-service-hpa -n mlops

# Editar
kubectl edit hpa pytorch-service-hpa -n mlops
```

### VPA (Vertical Pod Autoscaler)

```bash
# Instalar VPA
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler
./hack/vpa-up.sh
```

## 🔐 Secrets Management

### Usar Sealed Secrets (Recomendado)

```bash
# Instalar Sealed Secrets
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Encriptar secret
kubeseal --format yaml < secrets.yaml > sealed-secrets.yaml

# Aplicar
kubectl apply -f sealed-secrets.yaml
```

### Usar External Secrets

```bash
# Instalar External Secrets Operator
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets-system \
  --create-namespace
```

## 🌐 Networking

### Service Mesh (Istio)

```bash
# Instalar Istio
istioctl install --set profile=default

# Label namespace
kubectl label namespace mlops istio-injection=enabled

# Re-deploy pods
kubectl rollout restart deployment -n mlops
```

## 📊 Monitoring

### Prometheus Operator

```bash
# Instalar Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: pytorch-service
  namespace: mlops
spec:
  selector:
    matchLabels:
      app: pytorch-service
  endpoints:
  - port: http
    path: /metrics
```

## 🔄 Updates y Rollbacks

### Rolling Update

```bash
# Update imagen
kubectl set image deployment/pytorch-service \
  pytorch-service=ghcr.io/your-org/pytorch-service:v2.0.0 \
  -n mlops

# Ver rollout status
kubectl rollout status deployment/pytorch-service -n mlops

# Ver history
kubectl rollout history deployment/pytorch-service -n mlops
```

### Rollback

```bash
# Rollback a versión anterior
kubectl rollout undo deployment/pytorch-service -n mlops

# Rollback a revisión específica
kubectl rollout undo deployment/pytorch-service --to-revision=2 -n mlops
```

## 🐛 Troubleshooting

### Pods no inician

```bash
# Ver eventos
kubectl get events -n mlops --sort-by='.lastTimestamp'

# Describe pod
kubectl describe pod <pod-name> -n mlops

# Logs
kubectl logs <pod-name> -n mlops

# Shell en pod
kubectl exec -it <pod-name> -n mlops -- /bin/bash
```

### GPU no detectada

```bash
# Verificar GPU en node
kubectl get nodes -o yaml | grep -A 5 nvidia.com/gpu

# Ver logs de GPU operator
kubectl logs -n gpu-operator -l app=nvidia-device-plugin-daemonset

# Ejecutar nvidia-smi en pod
kubectl exec -it <pod-name> -n mlops -- nvidia-smi
```

### PVC stuck en Pending

```bash
# Ver PVC
kubectl describe pvc <pvc-name> -n mlops

# Ver storage class
kubectl get storageclass

# Ver PV
kubectl get pv
```

## 🎯 Best Practices

1. **Resources**: Siempre define requests y limits
2. **Health Checks**: Configura liveness y readiness probes
3. **Secrets**: Nunca commitees secrets en Git
4. **Labels**: Usa labels consistentes
5. **Namespaces**: Separa ambientes por namespace
6. **Monitoring**: Implementa logging y metrics
7. **Backups**: Backup regular de PVs y configs

## 📚 Recursos

- [Kubernetes Docs](https://kubernetes.io/docs/)
- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/)
- [Helm Charts](https://helm.sh/docs/)

---

**Production-ready Kubernetes deployment! 🚀**
