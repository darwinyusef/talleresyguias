# MLOps Platform - Taller Completo

Plataforma completa de MLOps con Docker, Event-Driven Architecture, RAG, PyTorch y TensorFlow.

## 🚀 Quick Start

```bash
# 1. Clonar y setup
git clone <your-repo>
cd mlops-project
make quickstart

# 2. Verificar servicios
make ps

# 3. Ver logs
make logs

# 4. Probar RAG
python scripts/test_rag.py --index --interactive

# 5. Entrenar modelo
python scripts/train_model.py --epochs 5 --lr 0.001
```

## 📋 Servicios Disponibles

| Servicio | Puerto | Descripción | URL |
|----------|--------|-------------|-----|
| PyTorch Service | 8000 | Servicio de ML con PyTorch | http://localhost:8000 |
| TensorFlow Service | 8001 | Servicio de ML con TensorFlow | http://localhost:8001 |
| RAG Service | 8002 | Sistema RAG con ChromaDB | http://localhost:8002 |
| RabbitMQ | 5672 | Message Broker | amqp://localhost:5672 |
| RabbitMQ Management | 15672 | UI de RabbitMQ | http://localhost:15672 |
| Redis | 6379 | Cache y Event Store | redis://localhost:6379 |
| PostgreSQL | 5432 | Base de datos para MLflow | postgres://localhost:5432 |
| MLflow | 5000 | Tracking de experimentos | http://localhost:5000 |
| ChromaDB | 8100 | Vector Database | http://localhost:8100 |
| Prometheus | 9090 | Monitoring | http://localhost:9090 |
| Grafana | 3000 | Dashboards | http://localhost:3000 |

### Credenciales por Defecto

- **RabbitMQ**: `admin` / `admin123`
- **Grafana**: `admin` / `admin123`
- **PostgreSQL**: `mlflow` / `mlflow123`

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    MLOps Platform                            │
└─────────────────────────────────────────────────────────────┘

    API Gateway
        │
        ├─────► RabbitMQ ──────┬──────► PyTorch Service
        │          │            │
        │          │            ├──────► TensorFlow Service
        │          │            │
        │          │            └──────► RAG Service
        │          │                         │
        │          ▼                         ▼
        │      Redis Store              ChromaDB
        │
        ├─────► MLflow (Tracking)
        │
        └─────► Prometheus ──────► Grafana
```

## 📚 Estructura del Proyecto

```
mlops-project/
├── src/
│   ├── events/              # Event schemas y event bus
│   │   ├── schemas.py       # Definiciones de eventos
│   │   └── event_bus.py     # RabbitMQ + Redis implementation
│   ├── services/            # Servicios ML
│   │   ├── pytorch_training_service.py
│   │   ├── tensorflow_service.py
│   │   ├── rag_service.py
│   │   └── document_classifier.py
│   ├── models/              # Definiciones de modelos
│   └── main.py              # Aplicación principal
├── scripts/                 # Scripts utilitarios
│   ├── train_model.py       # Entrenamiento de modelos
│   ├── test_rag.py          # Testing de RAG
│   └── download_datasets.py
├── tests/                   # Tests
│   ├── unit/
│   └── integration/
├── config/                  # Configuraciones
│   ├── prometheus.yml
│   └── grafana/
├── data/                    # Datasets
├── models/                  # Modelos entrenados
├── k8s/                     # Kubernetes manifests
├── docker-compose.yml       # Orquestación de servicios
├── Dockerfile.pytorch       # Imagen de PyTorch
├── Dockerfile.tensorflow    # Imagen de TensorFlow
├── requirements.txt
├── Makefile                 # Comandos útiles
└── README.md
```

## 🔧 Comandos Útiles

### Setup y Build

```bash
make setup          # Setup inicial
make build          # Build Docker images
make up             # Iniciar servicios
make down           # Detener servicios
make restart        # Reiniciar servicios
```

### Desarrollo

```bash
make test           # Ejecutar todos los tests
make test-unit      # Tests unitarios
make test-integration  # Tests de integración
make format         # Formatear código
make lint           # Ejecutar linters
```

### Logs y Debugging

```bash
make logs           # Ver todos los logs
make logs-pytorch   # Logs de PyTorch service
make logs-rag       # Logs de RAG service
make ps             # Ver servicios activos
```

### Shell Access

```bash
make shell-pytorch     # Shell en contenedor PyTorch
make shell-tensorflow  # Shell en contenedor TensorFlow
make shell-rag         # Shell en contenedor RAG
```

### Monitoring

```bash
make mlflow-ui      # Abrir MLflow UI
make grafana-ui     # Abrir Grafana
make prometheus-ui  # Abrir Prometheus
```

### Cleanup

```bash
make clean          # Limpiar archivos temporales
make clean-docker   # Limpiar Docker resources
```

## 💡 Ejemplos de Uso

### 1. Entrenar un Modelo PyTorch

```bash
# Con dataset sintético
python scripts/train_model.py \
    --model-type pytorch \
    --epochs 10 \
    --lr 0.001 \
    --hidden-dim 128

# Con dataset existente
python scripts/train_model.py \
    --dataset-id my_dataset \
    --epochs 20 \
    --batch-size 64
```

### 2. Usar el Sistema RAG

```bash
# Indexar documentos
python scripts/test_rag.py --index

# Query simple
python scripts/test_rag.py --query "What is PyTorch?" --top-k 5

# Modo interactivo
python scripts/test_rag.py --interactive
```

### 3. API Requests

```bash
# Upload document
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@document.txt" \
  -F "category=technical"

# Query RAG
curl -X POST http://localhost:8002/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is MLOps?", "top_k": 3}'

# Index document
curl -X POST http://localhost:8002/index \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your document content here",
    "metadata": {"category": "technical", "author": "John Doe"},
    "document_id": "doc_001"
  }'
```

### 4. Monitoring con Prometheus

```python
from prometheus_client import Counter, Histogram, Gauge

# Definir métricas
requests_total = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
active_users = Gauge('active_users', 'Active users')

# Usar métricas
requests_total.inc()
with request_duration.time():
    # Tu código aquí
    pass
active_users.set(42)
```

### 5. Event-Driven Training

```python
from src.events.event_bus import EventBus
from src.events.schemas import BaseEvent, EventMetadata, EventType

# Conectar a event bus
event_bus = EventBus("amqp://admin:admin123@localhost:5672/")
event_bus.connect()

# Publicar evento de entrenamiento
event = BaseEvent(
    metadata=EventMetadata(
        event_type=EventType.TRAINING_REQUESTED,
        source_service="my-app",
    ),
    payload={
        "dataset_id": "my_dataset",
        "hyperparameters": {
            "epochs": 10,
            "lr": 0.001,
        },
    },
)

event_bus.publish(event, routing_key="training.requested")
```

## 🧪 Testing

### Unit Tests

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=src --cov-report=html

# Solo tests de RAG
pytest tests/unit/test_rag_service.py -v

# Solo tests de events
pytest tests/unit/test_event_bus.py -v
```

### Integration Tests

```bash
# Tests de integración (requiere servicios activos)
make up
pytest tests/integration/ -v
```

### Load Testing

```bash
# Instalar locust
pip install locust

# Ejecutar load test
locust -f tests/load/locustfile.py --host http://localhost:8000
```

## 📊 MLflow Tracking

### Logging Experiments

```python
import mlflow

# Iniciar run
with mlflow.start_run(run_name="my_experiment"):
    # Log parámetros
    mlflow.log_param("epochs", 10)
    mlflow.log_param("learning_rate", 0.001)

    # Log métricas
    for epoch in range(10):
        mlflow.log_metric("loss", loss, step=epoch)
        mlflow.log_metric("accuracy", acc, step=epoch)

    # Log modelo
    mlflow.pytorch.log_model(model, "model")

    # Log artifacts
    mlflow.log_artifact("plot.png")
```

### Comparar Experimentos

```bash
# En MLflow UI (http://localhost:5000)
# 1. Seleccionar múltiples runs
# 2. Click en "Compare"
# 3. Visualizar métricas y parámetros
```

## 🔐 Seguridad

### Environment Variables

```bash
# Copiar .env.example y configurar
cp .env.example .env

# Editar variables sensibles
nano .env
```

### Secrets Management

```yaml
# docker-compose.yml
services:
  pytorch-service:
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## 🚀 Deployment

### Docker Compose (Development)

```bash
# Iniciar todos los servicios
make up

# Verificar
make ps
```

### Kubernetes (Production)

```bash
# Crear namespace
kubectl create namespace mlops

# Deploy
make deploy-prod

# Verificar
kubectl get pods -n mlops
kubectl get services -n mlops

# Logs
kubectl logs -f deployment/pytorch-service -n mlops
```

### Scaling

```bash
# Docker Compose
docker-compose up -d --scale pytorch-service=3

# Kubernetes
kubectl scale deployment pytorch-service --replicas=3 -n mlops
```

## 📈 Monitoring y Alerting

### Prometheus Queries

```promql
# Request rate
rate(requests_total[5m])

# Latency P95
histogram_quantile(0.95, rate(request_duration_seconds_bucket[5m]))

# Error rate
rate(requests_total{status="error"}[5m]) / rate(requests_total[5m])
```

### Grafana Dashboards

1. Acceder a http://localhost:3000
2. Login: `admin` / `admin123`
3. Importar dashboard desde `config/grafana/dashboards/`

### Alerts

```yaml
# config/prometheus/alerts.yml
groups:
  - name: mlops_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(requests_total{status="error"}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

## 🐛 Troubleshooting

### Servicios no inician

```bash
# Ver logs
make logs

# Verificar recursos Docker
docker system df
docker system prune

# Reiniciar
make down
make clean-docker
make up
```

### GPU no detectada

```bash
# Verificar NVIDIA driver
nvidia-smi

# Verificar Docker GPU support
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# Verificar en contenedor
make shell-pytorch
python -c "import torch; print(torch.cuda.is_available())"
```

### RabbitMQ connection issues

```bash
# Verificar RabbitMQ
curl http://localhost:15672/api/overview

# Verificar queues
docker-compose exec rabbitmq rabbitmqctl list_queues

# Reset
docker-compose restart rabbitmq
```

### ChromaDB problemas

```bash
# Verificar ChromaDB
curl http://localhost:8100/api/v1/heartbeat

# Reset collections
curl -X DELETE http://localhost:8100/api/v1/collections/documents

# Recrear
docker-compose restart chromadb
```

## 📖 Documentación Adicional

- [PyTorch Docs](https://pytorch.org/docs/)
- [TensorFlow Docs](https://www.tensorflow.org/guide)
- [MLflow Docs](https://mlflow.org/docs/latest/)
- [RabbitMQ Docs](https://www.rabbitmq.com/documentation.html)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [LangChain Docs](https://python.langchain.com/docs/)

## 🤝 Contribuciones

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto es de código abierto bajo la licencia MIT.

## 👥 Autores

- **Tu Nombre** - *Initial work*

## 🙏 Agradecimientos

- PyTorch Team
- TensorFlow Team
- LangChain Community
- MLOps Community

---

**¡Happy MLOps! 🚀🤖**
