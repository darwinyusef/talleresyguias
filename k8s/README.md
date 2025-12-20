# Taller de Kubernetes: Orquestación de Microservicios ☸️

Guía definitiva para dominar Kubernetes (K8s) desde los conceptos fundamentales hasta la orquestación profesional de arquitecturas complejas.

---

## 📖 Índice del Taller

### 🏗️ Fundamentos de Kubernetes
1.  **[Arquitectura de K8s](#arquitectura-de-k8s)**: Control Plane y Nodes.
2.  **[Objetos Core](#objetos-core)**: Pods, Deployments y Services.
3.  **[Configuración y Secretos](#configuración-y-secretos)**: ConfigMaps y Secrets.
4.  **[Almacenamiento](#almacenamiento)**: Persistent Volumes (PV) y Claims (PVC).

### 🚀 Orquestación Avanzada
5.  **[Service Discovery & Networking](#service-discovery--networking)**: Ingress Controllers y DNS interno.
6.  **[Escalabilidad Holística](#escalabilidad-holística)**: Horizontal Pod Autoscaler (HPA).
7.  **[Estrategias de Despliegue](#estrategias-de-despliegue)**: Rolling Updates, Blue-Green y Canary.

### 🎯 Proyectos Prácticos (Orquestación Real)
- **[Proyecto 1: FullStack Completo](./proyectos/fullstack/)**: Node.js + PostgreSQL + Redis.
- **[Proyecto 2: Microservicios Distribuido](./proyectos/microservicios/)**: Go + Python + RabbitMQ.
- **[Proyecto 3: ML-Serving con Alta Disponibilidad](./proyectos/ml-serving/)**: FastAPI + TensorFlow.

---

## 🏗️ 1. Arquitectura de Kubernetes

Kubernetes es un sistema de código abierto para automatizar el despliegue, el escalado y la gestión de aplicaciones en contenedores.

### Componentes del Control Plane (Master)
-   **kube-apiserver**: La puerta de entrada al clúster (API REST).
-   **etcd**: Almacén de datos clave-valor para el estado del clúster.
-   **kube-scheduler**: Asigna Pods a los Nodos.
-   **kube-controller-manager**: Ejecuta procesos de control (Node Controller, Job Controller, etc.).

### Componentes del Nodo (Worker)
-   **kubelet**: El agente que asegura que los contenedores estén corriendo en el Pod.
-   **kube-proxy**: Mantiene las reglas de red en los nodos (Service Networking).
-   **Container Runtime**: El software que corre los contenedores (Docker, containerd, CRI-O).

---

## 🚀 2. Objetos Core (El Manifiesto YAML)

Todo en K8s se define mediante archivos YAML.

### El Pod
La unidad mínima de ejecución.
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
```

### El Deployment
Gestiona el estado deseado de los Pods (replicas, actualizaciones).
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: app
        image: my-app:v1
```

---

---

## 🏗️ 3. Configuración y Secretos (Separando el código de la configuración)

Kubernetes permite desacoplar los archivos de configuración y los datos sensibles de la imagen del contenedor.

### ConfigMaps
Se usan para datos no confidenciales (variables de entorno, archivos de configuración).
- **Ejemplo**: Definir la URL de una API o la configuración de un servidor Nginx.
- **Uso**: Inyección como variables de entorno o montaje como archivos.

### Secrets
Para datos sensibles (passwords, tokens, llaves API).
- **Tipo Opaque**: El más común (datos genéricos).
- **Codificación**: Los datos se guardan en base64 (no es cifrado, es codificación).
- **Uso Crítico**: Siempre usar RBAC para limitar quién puede leer secretos.

---

## 💾 4. Almacenamiento Persistente (Estado en un mundo efímero)

Por defecto, los contenedores son efímeros. Si un pod muere, sus datos mueren.

-   **Persistent Volume (PV)**: Un pedazo de almacenamiento físico en el clúster (provisto por el administrador).
-   **Persistent Volume Claim (PVC)**: Una "solicitud" de almacenamiento por parte de un usuario/pod.
-   **StorageClass**: Permite el aprovisionamiento dinámico de almacenamiento (ej: crear un disco en AWS/GCP automáticamente).

### Ciclo de vida:
1. El Admin crea un `StorageClass`.
2. El Desarrollador crea un `PVC` solicitando espacio.
3. K8s "machea" el `PVC` con un `PV` existente o crea uno nuevo.
4. El `Pod` monta el `PVC` como un volumen.

---

## 🌐 5. Networking y Service Discovery

### Services (La IP Estable)
Los pods tienen IPs dinámicas. Para hablar con ellos de forma estable usamos un **Service**.
-   **ClusterIP**: IP interna (solo accesible dentro del clúster). Default.
-   **NodePort**: Abre un puerto estático en cada nodo (30000-32767).
-   **LoadBalancer**: Crea un balanceador de carga en la nube (AWS, GCP, Azure).

### Ingress (El Portero del Clúster)
Gestiona el acceso externo a los servicios, típicamente mediante HTTP/HTTPS.
- Provee terminación SSL/TLS.
- Balanceo de carga L7 (basado en rutas o hosts).
- **Componentes**: Ingress Resource (definición) + Ingress Controller (el software que lo ejecuta, ej: Nginx Ingress).

---

## 📈 6. Escalabilidad y Alta Disponibilidad

### Horizontal Pod Autoscaler (HPA)
Ajusta automáticamente el número de réplicas de un deployment basado en:
- Uso de CPU.
- Uso de Memoria.
- Métricas personalizadas (ej: requests por segundo).

### Estrategias de Actualización
- **RollingUpdate**: Actualiza los pods de uno en uno (Zero Downtime).
- **Recreate**: Mata todos los pods viejos antes de crear los nuevos (Downtime, pero evita conflictos de versión de base de datos).

---

## 🩺 7. Health Checks (Autoreparación)

K8s usa "probes" para conocer el estado de salud del contenedor:

1.  **Liveness Probe**: ¿Está vivo? Si falla, K8s reinicia el contenedor.
2.  **Readiness Probe**: ¿Está listo para recibir tráfico? Si falla, se remueve del Service.
3.  **Startup Probe**: ¿Terminó de arrancar? Bloquea las otras probes hasta que esta pasa (ideal para apps lentas).

---

## 📦 8. Helm: El Gestor de Paquetes de K8s

Helm es equivalente a `apt`, `npm` o `pip` pero para Kubernetes.

- **Chart**: Un paquete de recursos de K8s.
- **Repository**: Donde se almacenan los charts.
- **Release**: Una instancia de un chart ejecutándose en el clúster.

### Comandos Clave:
```bash
helm repo add [name] [url]
helm install [release-name] [chart]
helm upgrade [release-name] [chart]
helm rollback [release-name] [revision]
```

---

## 🤖 9. GitOps y Entrega Continua

GitOps es el paradigma donde **Git es la única fuente de verdad** para la infraestructura.

- **Herramientas**: ArgoCD, Flux.
- **Workflow**:
    1. El dev hace push al repo de manifiestos.
    2. ArgoCD detecta el cambio ("drift").
    3. ArgoCD aplica los cambios en el clúster de forma automática.
- **Beneficio**: Trazabilidad total, facilidad de rollback y seguridad incrementada.

---

## 🐛 10. Guía de Troubleshooting (Depuración)

Cuando algo falla en K8s, sigue estos pasos:

1. **Ver estado**: `kubectl get pods` (Busca `CrashLoopBackOff`, `Pending` o `Error`).
2. **Describir**: `kubectl describe pod [name]` (Mira la sección de `Events`).
3. **Logs**: `kubectl logs [name] --previous` (Ver por qué falló antes).
4. **Shell**: `kubectl exec -it [name] -- sh` (Entrar a debuggear).

---

## 🏗️ 11. Proyectos Prácticos (Orquestación Real)

### [Proyecto 1: FullStack](./proyectos/fullstack/)
**Stack**: Node.js + PostgreSQL + Redis.
- Aprende a conectar servicios usando nombres DNS internos.
- Maneja la persistencia de datos de la base de datos.
- Usa Secrets para las credenciales de la DB.

### [Proyecto 2: Microservicios](./proyectos/microservicios/)
**Stack**: Go (Order Service) + Python (Worker) + RabbitMQ (Broker).
- Comunicación asíncrona entre servicios.
- Escalado independiente (más workers que APIs).

### [Proyecto 3: ML Serving](./proyectos/ml-serving/)
**Stack**: FastAPI + TensorFlow Serving.
- Implementación de `ReadinessProbes` para carga de modelos pesados.
- Autoscaling agresivo basado en carga de inferencia.

---

## ✅ Conclusión y Certificación

Felicidades por completar el taller. Kubernetes es el estándar de la industria y dominarlo te posiciona como un experto en infraestructura moderna.

**¿Qué sigue?**
- Practica los **[EJERCICIOS.md](./EJERCICIOS.md)**.
- Revisa el **[RESUMEN.md](./RESUMEN.md)** para entrevistas técnicas.
- Monta tu propio clúster en la nube (GKE, EKS, AKS).

---

[Ir al Índice Detallado](./INDICE.md) • [Ver Guía de Inicio Rápido](./INICIO_RAPIDO.md)

---

## 🎯 Objetivos de Aprendizaje

✅ **Desplegar** aplicaciones resilientes y autoreparables.  
✅ **Gestionar** el tráfico interno y externo mediante Services e Ingress.  
✅ **Centralizar** configuraciones y datos sensibles.  
✅ **Implementar** persistencia de datos en entornos dinámicos.  
✅ **Escalar** aplicaciones automáticamente según la demanda.  

---

### 🔥 8. Monitoreo y Observabilidad
- **Prometheus & Grafana**: Recolección de métricas del clúster y dashboards.
- **Loki & Fluentd**: Gestión centralizada de logs de contenedores.
- **Health Checks**: Liveness, Readiness y Startup Probes para autoreparación.

### 📦 9. Gestión de Paquetes con Helm
- ¿Por qué Helm? Templatización de manifiestos YAML.
- **Charts**: Estructura de un paquete de K8s.
- **Values**: Personalización de despliegues por entorno (Dev, Prod).

### 🤖 10. GitOps y Automatización
- Integración con **GitHub Actions**.
- Despliegue continuo al clúster mediante `kubectl apply` y `Helm`.
- Estrategias de Rollback automatizadas.

---

## 🏗️ 11. Proyecto Final: Orquestación Global

**Objetivo**: Desplegar un ecosistema completo que incluya:
1.  **Backend** replicado con balanceo de carga interno.
2.  **Base de datos** persistente con backup automático.
3.  **Sistema de Cache** compartido.
4.  **Ingress** para acceso externo seguro.
5.  **Autoscaling** configurado para soportar picos de tráfico.

---

## 📁 Estructura Final del Taller

```
k8s/
├── 📚 DOCUMENTACIÓN
│   ├── README.md                      # Esta guía maestra
│   ├── INDICE.md                      # Navegación rápida
│   ├── INICIO_RAPIDO.md               # Setup en 5 min (minikube/kind)
│   ├── EJERCICIOS.md                  # Retos por niveles
│   └── RESUMEN.md                     # Resumen ejecutivo
│
├── 📦 CHARTS/                         # Estructuras de Helm
│   └── fullstack-app/                 # Ejemplo de empaquetado
│
├── ⚙️ CONFIGURACIÓN/BASE              # Recursos globales (Namespace)
│
├── 🌐 NETWORKING/                      # Ingress y Network Policies
│
├── 🎯 PROYECTOS/                      # Aplicaciones completas
│   ├── fullstack/                     # App Web + DB + Cache
│   ├── microservicios/                # Comunicación asíncrona
│   └── ml-serving/                    # Inferencia escalable
│
└── 🛠️ SCRIPTS/                        # Automatización y Limpieza
```

---

## ✅ Conclusión del Curso

¡Felicidades! Has completado el **Taller Profesional de Kubernetes**. Ahora tienes las habilidades para:
- Diseñar infraestructuras escalables y resilientes.
- Gestionar microservicios con dependencias complejas.
- Automatizar el ciclo de vida de las aplicaciones en la nube.

**Próximos pasos**:
- Explora **Service Meshes** como Istio o Linkerd.
- Implementa **GitOps** con herramientas como ArgoCD o Flux.
- Certifícate como **CKAD** (Certified Kubernetes Application Developer).

---

[Ir al Índice Detallado](./INDICE.MD) • [Ver Guía de Inicio Rápido](./INICIO_RAPIDO.MD)
