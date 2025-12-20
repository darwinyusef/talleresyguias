# ⚡ Inicio Rápido: Kubernetes

Pónte en marcha con un clúster local y despliega tu primera aplicación en minutos.

## 1. Prerrequisitos

Instala las herramientas necesarias:
- **Docker**
- **kubectl**: `brew install kubectl`
- **minikube**: `brew install minikube`

## 2. Iniciar el Clúster Local

```bash
# Iniciar minikube con el driver de docker
minikube start --driver=docker

# Verificar que el clúster está listo
kubectl cluster-info

# Ver los nodos
kubectl get nodes
```

## 3. Tu primer despliegue (Nginx)

```bash
# Crear un deployment
kubectl create deployment nginx-demo --image=nginx

# Exponerlo como servicio
kubectl expose deployment nginx-demo --port=80 --type=NodePort

# Obtener la URL para acceder
minikube service nginx-demo --url
```

## 4. Desplegar mediante Manifiestos (YAML)

Crea un archivo llamado `pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: nginx:alpine
```

Aplícalo al clúster:
```bash
# Crear el recurso
kubectl apply -f pod.yaml

# Listar pods
kubectl get pods

# Ver logs del pod
kubectl logs my-pod

# Entrar al pod (Shell)
kubectl exec -it my-pod -- sh
```

## 5. Dashboard Visual

```bash
# Iniciar el Dashboard oficial
minikube dashboard

# (Opcional) Instala K9s para una terminal pro
# brew install k9s
# k9s
```

## 6. Comandos de Supervivencia (Cheatsheet)

### Gestión de Recursos
- **Listar todo**: `kubectl get all -n workshop-k8s`
- **Ver eventos recientes**: `kubectl get events --sort-by='.lastTimestamp'`
- **Editar recurso en vivo**: `kubectl edit deployment my-app`
- **Escalar**: `kubectl scale deployment my-app --replicas=5`

### Depuración (Troubleshooting)
- **Ver logs**: `kubectl logs -f [pod-name]`
- **Ver logs de un contenedor específico**: `kubectl logs [pod-name] -c [container-name]`
- **Logs del contenedor anterior (si crasheó)**: `kubectl logs [pod-name] --previous`
- **Describir errores**: `kubectl describe [resource-type] [name]`
- **Copiar archivos**: `kubectl cp local-file [pod-name]:/remote-path`
- **Port-forward (Acceso rápido)**: `kubectl port-forward svc/api-service 8080:80`

## 7. Limpieza

---

[Ver Proyectos Prácticos](./README.md#proyectos-prácticos) • [Ir a Ejercicios](./EJERCICIOS.md)
