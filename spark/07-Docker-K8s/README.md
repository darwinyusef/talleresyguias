# 🐳 Módulo 07: Spark en Docker + Kubernetes

Aprende a desplegar Apache Spark en entornos modernos de producción usando **containerización con Docker** y **orquestación con Kubernetes**, maximizando escalabilidad, eficiencia y portabilidad.

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Entender los fundamentos de containerización y orquestación
- ✅ Crear imágenes Docker optimizadas para Spark
- ✅ Configurar clusters Spark con Docker Compose
- ✅ Desplegar Spark en Kubernetes (native y Spark Operator)
- ✅ Implementar auto-scaling de executors
- ✅ Configurar storage persistente (PVCs, S3)
- ✅ Implementar monitoring con Prometheus + Grafana
- ✅ Aplicar mejores prácticas de DevOps para Big Data

---

## 📚 Fundamentos Teóricos

### ¿Por qué Containerización?

**Containerización** empaqueta una aplicación con todas sus dependencias en una unidad portable que funciona consistentemente en cualquier entorno.

```
Antes (Bare Metal/VMs)           Con Contenedores
═══════════════════════════════════════════════════════
Hardware                          Hardware
    ↓                                 ↓
Hypervisor (ESXi, KVM)           Docker Engine
    ↓                                 ↓
Multiple VMs                      Multiple Containers
    ↓                                 ↓
OS completo (GB)                  Shared OS kernel (MB)
    ↓                                 ↓
App + Dependencies                App + Dependencies
```

**Beneficios:**

| Feature | VMs | Containers |
|---------|-----|------------|
| **Startup time** | Minutos | Segundos |
| **Resource overhead** | GB (OS completo) | MB (solo app) |
| **Portabilidad** | Media | Alta |
| **Densidad** | 10-20 por host | 100+ por host |
| **Aislamiento** | Fuerte (hypervisor) | Medio (kernel namespaces) |

---

### ¿Por qué Kubernetes para Spark?

**Kubernetes** (K8s) es el estándar de facto para orquestación de contenedores en producción.

**Comparación de Cluster Managers:**

| Feature | Standalone | YARN | Mesos | Kubernetes |
|---------|-----------|------|-------|------------|
| **Dynamic allocation** | ✅ | ✅ | ✅ | ✅ |
| **Multi-tenancy** | ❌ | ✅ | ✅ | ✅ |
| **Resource isolation** | ⚠️ Débil | ✅ Fuerte | ✅ Fuerte | ✅ Fuerte |
| **Fault tolerance** | ⚠️ Manual | ✅ Auto | ✅ Auto | ✅ Auto |
| **Cloud-native** | ❌ | ❌ | ⚠️ | ✅ |
| **Ecosistema** | Solo Spark | Hadoop | Datacenter OS | Cloud-agnostic |
| **Vigencia** | 📉 Legado | 📉 Declinando | 📉 Declinando | 📈 Creciendo |

**Ventajas de Spark on Kubernetes:**

1. **Aislamiento por Job**: Cada Spark job corre en Pods aislados
2. **Dynamic Resource Allocation**: Escalamiento elástico de executors
3. **Separation of Compute & Storage**: Data Lakes (S3) + ephemeral compute
4. **Multi-tenancy**: Múltiples equipos/jobs compartiendo infraestructura
5. **Cloud Portability**: Funciona en AWS EKS, GCP GKE, Azure AKS, on-premise
6. **Unified Platform**: Spark + ML serving (FastAPI) + Airflow en el mismo cluster

---

## 🐳 Parte 1: Spark con Docker

### Conceptos de Docker

**Imagen**: Template inmutable (blueprint)
**Contenedor**: Instancia en ejecución de una imagen
**Dockerfile**: Receta para construir una imagen
**Registry**: Repositorio de imágenes (Docker Hub, ECR, GCR)

### Dockerfile para PySpark

```dockerfile
FROM bitnami/spark:3.4.0

# Metadata
LABEL maintainer="data-team@company.com"
LABEL version="1.0"
LABEL description="Custom Spark image con ML dependencies"

USER root

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar librerías Python
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copiar scripts y configs
COPY spark/jobs /opt/spark/jobs
COPY spark/config /opt/spark/conf

# JARs adicionales (JDBC, Kafka, AWS)
RUN cd /opt/bitnami/spark/jars && \
    curl -O https://repo1.maven.org/maven2/org/postgresql/postgresql/42.6.0/postgresql-42.6.0.jar && \
    curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

# Volver a usuario no-root
USER 1001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:4040/api/v1/applications || exit 1

# Entrypoint por defecto (puede ser sobrescrito)
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]
CMD ["/opt/bitnami/scripts/spark/run.sh"]
```

**requirements.txt:**
```txt
pyspark==3.4.0
mlflow==2.9.2
fastapi==0.108.0
uvicorn[standard]==0.25.0
pandas==2.1.4
pyarrow==14.0.2
scikit-learn==1.3.2
psycopg2-binary==2.9.9
redis==5.0.1
prometheus-client==0.19.0
```

### Construir y Publicar Imagen

```bash
# Construir imagen
docker build -t my-spark:3.4.0 -f Dockerfile .

# Probar localmente
docker run -it --rm my-spark:3.4.0 pyspark

# Tagear para registry
docker tag my-spark:3.4.0 myregistry.azurecr.io/my-spark:3.4.0

# Autenticar (ejemplo Azure)
az acr login --name myregistry

# Publicar
docker push myregistry.azurecr.io/my-spark:3.4.0
```

### Docker Compose: Cluster Spark Completo

```yaml
version: '3.8'

services:
  spark-master:
    image: bitnami/spark:3.4.0
    container_name: spark-master
    hostname: spark-master
    environment:
      - SPARK_MODE=master
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    ports:
      - "8080:8080"  # Spark Master UI
      - "7077:7077"  # Spark Master port
    volumes:
      - ./spark/jobs:/opt/spark/jobs
      - ./data:/opt/spark/data
    networks:
      - spark-network

  spark-worker-1:
    image: bitnami/spark:3.4.0
    container_name: spark-worker-1
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=4G
      - SPARK_WORKER_CORES=2
    volumes:
      - ./spark/jobs:/opt/spark/jobs
      - ./data:/opt/spark/data
    depends_on:
      - spark-master
    networks:
      - spark-network

  spark-worker-2:
    image: bitnami/spark:3.4.0
    container_name: spark-worker-2
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=4G
      - SPARK_WORKER_CORES=2
    volumes:
      - ./spark/jobs:/opt/spark/jobs
      - ./data:/opt/spark/data
    depends_on:
      - spark-master
    networks:
      - spark-network

  postgres:
    image: postgres:14
    container_name: postgres
    environment:
      POSTGRES_USER: spark
      POSTGRES_PASSWORD: spark123
      POSTGRES_DB: metastore
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - spark-network

  minio:
    image: minio/minio
    container_name: minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio-data:/data
    networks:
      - spark-network

volumes:
  postgres-data:
  minio-data:

networks:
  spark-network:
    driver: bridge
```

**Uso:**
```bash
# Levantar cluster completo
docker-compose up -d

# Verificar servicios
docker-compose ps

# Ver logs
docker-compose logs -f spark-master

# Acceder a UI
open http://localhost:8080  # Spark Master
open http://localhost:9001  # MinIO Console

# Ejecutar job
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  /opt/spark/jobs/lead_scoring.py

# Detener cluster
docker-compose down
```

---

## ☸️ Parte 2: Spark en Kubernetes

### Arquitectura Spark on Kubernetes

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster                     │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────┐         ┌──────────────┐         │
│  │ Driver Pod   │ ◄─────► │ Executor Pod │         │
│  │              │         │              │         │
│  │  Spark App   │         │  Task 1-4    │         │
│  └──────┬───────┘         └──────────────┘         │
│         │                                            │
│         │  Creates & Manages                        │
│         ▼                                            │
│  ┌──────────────┐         ┌──────────────┐         │
│  │ Executor Pod │         │ Executor Pod │         │
│  │              │         │              │         │
│  │  Task 5-8    │         │  Task 9-12   │         │
│  └──────────────┘         └──────────────┘         │
│                                                       │
│  Storage:                                            │
│  ┌────────────────────────────────────┐             │
│  │  PersistentVolumeClaims (Checkpoints)           │
│  │  S3/GCS/Azure Blob (Data Lake)                  │
│  └────────────────────────────────────┘             │
└─────────────────────────────────────────────────────┘
```

### Opción 1: Spark Native Kubernetes Support

Desde Spark 2.3+, Spark puede lanzar jobs directamente en K8s sin software adicional.

**Configuración:**
```bash
# spark-submit en modo cluster
spark-submit \
  --master k8s://https://kubernetes.default.svc \
  --deploy-mode cluster \
  --name spark-pi \
  --conf spark.executor.instances=3 \
  --conf spark.kubernetes.container.image=my-spark:3.4.0 \
  --conf spark.kubernetes.namespace=spark \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.driver.request.cores=1 \
  --conf spark.kubernetes.driver.limit.cores=1 \
  --conf spark.kubernetes.executor.request.cores=2 \
  --conf spark.kubernetes.executor.limit.cores=2 \
  --conf spark.kubernetes.driver.memory=2g \
  --conf spark.kubernetes.executor.memory=4g \
  local:///opt/spark/examples/src/main/python/pi.py 1000
```

**RBAC (Service Account):**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: spark

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: spark-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: spark-role-binding
subjects:
- kind: ServiceAccount
  name: spark
  namespace: spark
roleRef:
  kind: ClusterRole
  name: spark-role
  apiGroup: rbac.authorization.k8s.io
```

### Opción 2: Spark Operator (Recomendado)

El **Spark Operator** es un Kubernetes operator que gestiona Spark jobs como recursos nativos de K8s usando CRDs (Custom Resource Definitions).

**Ventajas:**
- ✅ Declarativo (YAML)
- ✅ Integración con kubectl
- ✅ Auto-restart en fallos
- ✅ Monitoring integrado
- ✅ Spark History Server automático

**Instalación con Helm:**
```bash
# Agregar repo
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator

# Crear namespace
kubectl create namespace spark-operator

# Instalar operator
helm install spark-operator spark-operator/spark-operator \
  --namespace spark-operator \
  --set webhook.enable=true \
  --set serviceAccounts.spark.create=true \
  --set sparkJobNamespace=spark

# Verificar instalación
kubectl get pods -n spark-operator
```

**SparkApplication Example:**
```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: lead-scoring-job
  namespace: spark
spec:
  type: Python
  mode: cluster
  image: "myregistry.azurecr.io/my-spark:3.4.0"
  imagePullPolicy: Always
  mainApplicationFile: "local:///opt/spark/jobs/lead_scoring.py"
  arguments:
    - "--input-path"
    - "s3a://datalake/silver/leads/"
    - "--output-path"
    - "s3a://datalake/gold/predictions/"
    - "--date"
    - "2024-01-15"

  sparkVersion: "3.4.0"
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
    onFailureRetryInterval: 10
    onSubmissionFailureRetries: 5
    onSubmissionFailureRetryInterval: 20

  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "2g"
    labels:
      version: "3.4.0"
      app: "lead-scoring"
    serviceAccount: spark
    env:
      - name: AWS_ACCESS_KEY_ID
        valueFrom:
          secretKeyRef:
            name: aws-credentials
            key: access-key-id
      - name: AWS_SECRET_ACCESS_KEY
        valueFrom:
          secretKeyRef:
            name: aws-credentials
            key: secret-access-key

  executor:
    cores: 2
    coreLimit: "2400m"
    memory: "4g"
    instances: 3
    labels:
      version: "3.4.0"
      app: "lead-scoring"
    env:
      - name: AWS_ACCESS_KEY_ID
        valueFrom:
          secretKeyRef:
            name: aws-credentials
            key: access-key-id
      - name: AWS_SECRET_ACCESS_KEY
        valueFrom:
          secretKeyRef:
            name: aws-credentials
            key: secret-access-key

  deps:
    jars:
      - local:///opt/spark/jars/hadoop-aws-3.3.4.jar
      - local:///opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar

  sparkConf:
    "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem"
    "spark.hadoop.fs.s3a.endpoint": "s3.amazonaws.com"
    "spark.dynamicAllocation.enabled": "true"
    "spark.dynamicAllocation.shuffleTracking.enabled": "true"
    "spark.dynamicAllocation.minExecutors": "1"
    "spark.dynamicAllocation.maxExecutors": "10"
    "spark.dynamicAllocation.initialExecutors": "3"
    "spark.sql.adaptive.enabled": "true"
```

**Deploy y Monitoreo:**
```bash
# Aplicar SparkApplication
kubectl apply -f lead_scoring_job.yaml

# Ver status
kubectl get sparkapplications -n spark
kubectl describe sparkapplication lead-scoring-job -n spark

# Ver logs del driver
kubectl logs -n spark lead-scoring-job-driver -f

# Ver ejecutores
kubectl get pods -n spark -l spark-role=executor

# Cancelar job
kubectl delete sparkapplication lead-scoring-job -n spark
```

### Dynamic Allocation (Auto-Scaling)

Escalamiento automático de executors según carga de trabajo:

```yaml
sparkConf:
  # Habilitar dynamic allocation
  "spark.dynamicAllocation.enabled": "true"
  "spark.dynamicAllocation.shuffleTracking.enabled": "true"

  # Límites de executors
  "spark.dynamicAllocation.minExecutors": "1"
  "spark.dynamicAllocation.maxExecutors": "20"
  "spark.dynamicAllocation.initialExecutors": "5"

  # Timeouts
  "spark.dynamicAllocation.executorIdleTimeout": "60s"
  "spark.dynamicAllocation.cachedExecutorIdleTimeout": "300s"
  "spark.dynamicAllocation.schedulerBacklogTimeout": "5s"
```

**Beneficios:**
- 💰 **Ahorro de costos**: Solo pagas por recursos usados
- ⚡ **Performance**: Scale-up rápido durante picos
- 🎯 **Eficiencia**: Scale-down cuando carga baja

---

## 💾 Storage en Kubernetes

### 1. PersistentVolumeClaims (Checkpoints, Logs)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: spark-checkpoint-pvc
  namespace: spark
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: efs-sc  # AWS EFS / Azure Files / GCP Filestore
  resources:
    requests:
      storage: 100Gi

---
# Usar en SparkApplication
spec:
  driver:
    volumeMounts:
      - name: checkpoint-volume
        mountPath: /checkpoints
  executor:
    volumeMounts:
      - name: checkpoint-volume
        mountPath: /checkpoints
  volumes:
    - name: checkpoint-volume
      persistentVolumeClaim:
        claimName: spark-checkpoint-pvc
```

### 2. S3/GCS/Azure Blob (Data Lake)

**Configurar credenciales con Secrets:**
```bash
# Crear secret con credenciales AWS
kubectl create secret generic aws-credentials \
  --from-literal=access-key-id=AKIAIOSFODNN7EXAMPLE \
  --from-literal=secret-access-key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
  -n spark

# O desde archivo
kubectl create secret generic aws-credentials \
  --from-file=credentials=~/.aws/credentials \
  -n spark
```

**Montar en Pods:**
```yaml
spec:
  driver:
    env:
      - name: AWS_ACCESS_KEY_ID
        valueFrom:
          secretKeyRef:
            name: aws-credentials
            key: access-key-id
      - name: AWS_SECRET_ACCESS_KEY
        valueFrom:
          secretKeyRef:
            name: aws-credentials
            key: secret-access-key
```

---

## 📊 Monitoring en Kubernetes

### 1. Spark History Server

Deploy permanente para ver logs de jobs completados:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-history-server
  namespace: spark
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-history-server
  template:
    metadata:
      labels:
        app: spark-history-server
    spec:
      containers:
      - name: spark-history-server
        image: bitnami/spark:3.4.0
        command: ["/opt/bitnami/spark/sbin/start-history-server.sh"]
        env:
        - name: SPARK_HISTORY_OPTS
          value: "-Dspark.history.fs.logDirectory=s3a://spark-logs/history"
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: access-key-id
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: secret-access-key
        ports:
        - containerPort: 18080
          name: web-ui

---
apiVersion: v1
kind: Service
metadata:
  name: spark-history-server
  namespace: spark
spec:
  type: LoadBalancer
  ports:
  - port: 18080
    targetPort: 18080
    name: web-ui
  selector:
    app: spark-history-server
```

### 2. Prometheus + Grafana

**Configurar Spark para exportar métricas:**
```yaml
sparkConf:
  "spark.metrics.conf.*.sink.prometheus.class": "org.apache.spark.metrics.sink.PrometheusSink"
  "spark.metrics.conf.*.sink.prometheus.pushgateway-address": "prometheus-pushgateway:9091"
  "spark.metrics.conf.*.sink.prometheus.period": "10"
  "spark.metrics.conf.*.sink.prometheus.metrics-name-capture-regex": "([\\w_]+_[mM]icros|[\\w_]+_[nN]anos)"
```

**Grafana Dashboard:**
- [Spark on Kubernetes Dashboard](https://grafana.com/grafana/dashboards/11459)
- Métricas: Executor count, memory usage, task duration, shuffle I/O

### 3. Logging

**FluentBit para centralizar logs:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: spark
data:
  fluent-bit.conf: |
    [INPUT]
        Name              tail
        Path              /var/log/containers/*spark*.log
        Parser            docker
        Tag               kube.*

    [OUTPUT]
        Name              es
        Match             *
        Host              elasticsearch.logging.svc
        Port              9200
        Index             spark-logs
```

---

## 💡 Mejores Prácticas

### 1. Resource Requests y Limits

```yaml
# ✅ BIEN: Definir requests y limits
driver:
  cores: 1
  coreLimit: "1200m"     # 20% overhead
  memory: "2g"
  memoryOverhead: "512m"  # 25% overhead

executor:
  cores: 2
  coreLimit: "2400m"
  memory: "4g"
  memoryOverhead: "1g"
```

**Reglas:**
- `coreLimit` ≈ `cores * 1.2` (overhead para GC, etc.)
- `memoryOverhead` ≈ `memory * 0.25` (off-heap, network buffers)

### 2. Node Affinity y Taints

```yaml
# Ejecutar Spark solo en nodos dedicados
spec:
  driver:
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
          - matchExpressions:
            - key: workload-type
              operator: In
              values:
              - spark
    tolerations:
    - key: "spark-workload"
      operator: "Equal"
      value: "true"
      effect: "NoSchedule"
```

### 3. Pod Priorities

```yaml
# Priorizar jobs críticos
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: spark-critical
value: 1000
globalDefault: false
description: "High priority for production Spark jobs"

---
# Usar en SparkApplication
spec:
  driver:
    priorityClassName: spark-critical
  executor:
    priorityClassName: spark-critical
```

### 4. Secrets Management

```bash
# ❌ MAL: Credenciales en código
spark.conf.set("fs.s3a.access.key", "AKIAIOSFODNN7EXAMPLE")

# ✅ BIEN: Usar Secrets de K8s
# O aún mejor: Usar IRSA (IAM Roles for Service Accounts) en AWS
```

**AWS IRSA Example:**
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: spark
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/SparkS3AccessRole
```

### 5. Auto-Scaling de Cluster (Cloud)

**AWS EKS Cluster Autoscaler:**
```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: spark-executor-hpa
  namespace: spark
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: spark-executors
  minReplicas: 2
  maxReplicas: 50
  targetCPUUtilizationPercentage: 80
```

### 6. Cost Optimization

```yaml
# Usar Spot Instances (AWS) / Preemptible (GCP)
spec:
  executor:
    nodeSelector:
      node.kubernetes.io/instance-type: "spot"
    tolerations:
    - key: "node.kubernetes.io/unreliable"
      operator: "Exists"
      effect: "NoSchedule"

  # Configurar graceful decommission
  sparkConf:
    "spark.decommission.enabled": "true"
    "spark.storage.decommission.rddBlocks.enabled": "true"
    "spark.storage.decommission.shuffleBlocks.enabled": "true"
```

**Ahorro potencial:** 60-90% vs On-Demand

---

## 🚀 Ejemplo Completo: Pipeline MLOps en K8s

**1. CronJob para Entrenamiento Diario:**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-ml-training
  namespace: spark
spec:
  schedule: "0 2 * * *"  # Diario a las 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: spark-operator
          containers:
          - name: trigger-spark-job
            image: bitnami/kubectl:latest
            command:
            - /bin/sh
            - -c
            - |
              cat <<EOF | kubectl apply -f -
              apiVersion: sparkoperator.k8s.io/v1beta2
              kind: SparkApplication
              metadata:
                name: ml-training-$(date +%Y%m%d-%H%M%S)
                namespace: spark
              spec:
                type: Python
                mode: cluster
                image: "myregistry.azurecr.io/my-spark:3.4.0"
                mainApplicationFile: "local:///opt/spark/jobs/lead_scoring.py"
                arguments:
                  - "--date"
                  - "$(date -d yesterday +%Y-%m-%d)"
                sparkVersion: "3.4.0"
                driver:
                  cores: 1
                  memory: "2g"
                executor:
                  cores: 2
                  memory: "4g"
                  instances: 5
              EOF
          restartPolicy: OnFailure
```

**2. Deployment de API Serving:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-serving
  namespace: spark
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-serving
  template:
    metadata:
      labels:
        app: fastapi-serving
    spec:
      containers:
      - name: fastapi
        image: myregistry.azurecr.io/fastapi-serving:latest
        ports:
        - containerPort: 8000
        env:
        - name: PREDICTIONS_PATH
          value: "s3a://datalake/gold/predictions/latest/"
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: access-key-id
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-serving
  namespace: spark
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: fastapi-serving

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
  namespace: spark
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-serving
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 🔍 Troubleshooting

### Problemas Comunes

**1. Pods en Pending:**
```bash
# Ver eventos
kubectl describe pod <pod-name> -n spark

# Causas comunes:
# - Insuficientes recursos en nodos
# - ImagePullBackOff (imagen no existe)
# - PVC no puede ser montado
```

**2. Executors muriendo (OOMKilled):**
```yaml
# Aumentar memoryOverhead
executor:
  memory: "4g"
  memoryOverhead: "2g"  # De 1g a 2g
```

**3. Logs no accesibles:**
```bash
# Configurar event logging a S3
sparkConf:
  "spark.eventLog.enabled": "true"
  "spark.eventLog.dir": "s3a://spark-logs/event-logs"
```

---

## 📚 Referencias

- [Spark on Kubernetes Official Docs](https://spark.apache.org/docs/latest/running-on-kubernetes.html)
- [Spark Operator GitHub](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator)
- [Kubernetes Best Practices for Spark](https://kubernetes.io/blog/2019/03/running-apache-spark-on-kubernetes/)
- [Bitnami Spark Images](https://github.com/bitnami/containers/tree/main/bitnami/spark)

---

**¡Taller Completo! 🎉 Ahora dominas Spark desde desarrollo local hasta producción en Kubernetes**
