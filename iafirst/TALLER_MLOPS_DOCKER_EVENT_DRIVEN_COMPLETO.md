# Taller Completo: MLOps con Docker, Event-Driven Architecture y RAG

## 📋 Tabla de Contenidos

1. [Introducción y Fundamentos](#1-introducción-y-fundamentos)
2. [Docker para ML/DL: TensorFlow y PyTorch](#2-docker-para-mldl-tensorflow-y-pytorch)
3. [Pipeline de ML con Event-Driven Architecture](#3-pipeline-de-ml-con-event-driven-architecture)
4. [RAG: Retrieval Augmented Generation](#4-rag-retrieval-augmented-generation)
5. [Proyecto Completo Integrado](#5-proyecto-completo-integrado)
6. [Testing, Monitoring y Deployment](#6-testing-monitoring-y-deployment)

---

## 1. Introducción y Fundamentos

### 1.1 ¿Qué es MLOps?

**MLOps** (Machine Learning Operations) es la práctica de combinar ML, DevOps y Data Engineering para:

- **Automatizar** el ciclo de vida de modelos ML
- **Versionar** datos, código y modelos
- **Monitorear** el rendimiento en producción
- **Escalar** de manera eficiente
- **Reproducir** experimentos

#### Pipeline MLOps Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    MLOps Pipeline                            │
└─────────────────────────────────────────────────────────────┘

  Data                Model              Deploy            Monitor
  ┌─────┐            ┌─────┐           ┌─────┐           ┌─────┐
  │     │──────►     │     │──────►    │     │──────►    │     │
  │ ETL │   Train    │ Val │  Package  │ Srv │  Metrics  │ Mon │
  │     │            │     │           │     │           │     │
  └─────┘            └─────┘           └─────┘           └─────┘
     ▲                  │                                    │
     │                  │                                    │
     └──────────────────┴────────────────────────────────────┘
                    Feedback Loop
```

### 1.2 Event-Driven Architecture para ML

**¿Por qué Event-Driven?**

- **Desacoplamiento**: Servicios independientes
- **Escalabilidad**: Procesamiento asíncrono
- **Resiliencia**: Tolerancia a fallos
- **Trazabilidad**: Audit trail completo

#### Arquitectura General

```
┌──────────────────────────────────────────────────────────────┐
│                    Event-Driven ML System                     │
└──────────────────────────────────────────────────────────────┘

    Producer          Message Broker         Consumers
  ┌─────────┐       ┌──────────────┐      ┌──────────┐
  │  Data   │       │    Kafka/    │      │ Training │
  │ Ingress │──────►│   RabbitMQ   │─────►│ Service  │
  └─────────┘       │   Redis      │      └──────────┘
                    └──────────────┘
                           │                ┌──────────┐
                           │                │ Inference│
                           └───────────────►│ Service  │
                           │                └──────────┘
                           │                ┌──────────┐
                           └───────────────►│   RAG    │
                                            │ Service  │
                                            └──────────┘
```

### 1.3 Stack Tecnológico

```yaml
# Frameworks ML/DL
ml_frameworks:
  - PyTorch: 2.1+
  - TensorFlow: 2.15+
  - Scikit-learn: 1.3+
  - Transformers (HuggingFace): 4.36+

# Containerización
containerization:
  - Docker: 24.0+
  - Docker Compose: 2.23+
  - Kubernetes (opcional): 1.28+

# Message Brokers
messaging:
  - RabbitMQ: 3.12+
  - Apache Kafka: 3.6+
  - Redis Streams: 7.2+

# MLOps Tools
mlops:
  - MLflow: 2.9+
  - DVC: 3.35+
  - Weights & Biases: 0.16+

# Serving
serving:
  - FastAPI: 0.108+
  - TorchServe: 0.9+
  - TensorFlow Serving: 2.15+

# RAG Components
rag:
  - LangChain: 0.1+
  - ChromaDB: 0.4+
  - FAISS: 1.7+
  - Sentence Transformers: 2.2+
```

---

## 2. Docker para ML/DL: TensorFlow y PyTorch

### 2.1 Base Images Optimizadas

#### PyTorch Dockerfile

```dockerfile
# Dockerfile.pytorch
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

# Metadata
LABEL maintainer="mlops@example.com"
LABEL version="1.0"
LABEL description="PyTorch ML Service with GPU Support"

# Argumentos de construcción
ARG PYTHON_VERSION=3.11
ARG WORKDIR=/app

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    CUDA_VISIBLE_DEVICES=0

WORKDIR ${WORKDIR}

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código de aplicación
COPY ./src ./src
COPY ./models ./models
COPY ./config ./config

# Usuario no-root para seguridad
RUN useradd -m -u 1000 mluser && \
    chown -R mluser:mluser ${WORKDIR}
USER mluser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Puerto de exposición
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### TensorFlow Dockerfile

```dockerfile
# Dockerfile.tensorflow
FROM tensorflow/tensorflow:2.15.0-gpu

LABEL maintainer="mlops@example.com"
LABEL version="1.0"
LABEL description="TensorFlow ML Service with GPU Support"

ARG WORKDIR=/app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    TF_ENABLE_ONEDNN_OPTS=0

WORKDIR ${WORKDIR}

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar requirements
COPY requirements-tf.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements-tf.txt

# Copiar código
COPY ./src ./src
COPY ./models ./models
COPY ./config ./config

# Usuario no-root
RUN useradd -m -u 1000 mluser && \
    chown -R mluser:mluser ${WORKDIR}
USER mluser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

EXPOSE 8001

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 2.2 Requirements Files

#### requirements.txt (PyTorch)

```txt
# Core ML/DL
torch==2.1.0
torchvision==0.16.0
transformers==4.36.0
sentencepiece==0.1.99

# API & Serving
fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.0
pydantic-settings==2.1.0

# MLOps
mlflow==2.9.2
dvc==3.35.0

# Data Processing
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
pillow==10.1.0

# Message Queue
pika==1.3.2  # RabbitMQ
kafka-python==2.0.2
redis==5.0.1

# RAG Components
langchain==0.1.0
chromadb==0.4.22
sentence-transformers==2.2.2
faiss-cpu==1.7.4  # o faiss-gpu para GPU

# Vector Stores
qdrant-client==1.7.0
pinecone-client==3.0.0

# Monitoring & Logging
prometheus-client==0.19.0
python-json-logger==2.0.7
structlog==23.3.0

# Utils
python-multipart==0.0.6
httpx==0.26.0
tenacity==8.2.3
```

#### requirements-tf.txt (TensorFlow)

```txt
# Core ML/DL
tensorflow==2.15.0
keras==2.15.0
tf-keras==2.15.0

# API & Serving
fastapi==0.108.0
uvicorn[standard]==0.25.0
pydantic==2.5.0

# MLOps
mlflow==2.9.2
tensorflow-serving-api==2.15.0

# Data Processing
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
pillow==10.1.0

# Message Queue
pika==1.3.2
kafka-python==2.0.2
redis==5.0.1

# Monitoring
prometheus-client==0.19.0
python-json-logger==2.0.7
```

### 2.3 Docker Compose para Desarrollo

```yaml
# docker-compose.yml
version: '3.8'

services:
  # RabbitMQ Message Broker
  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    container_name: mlops-rabbitmq
    ports:
      - "5672:5672"    # AMQP
      - "15672:15672"  # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - mlops-network

  # Redis para Cache y Streams
  redis:
    image: redis:7.2-alpine
    container_name: mlops-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - mlops-network

  # PostgreSQL para MLflow y metadata
  postgres:
    image: postgres:16-alpine
    container_name: mlops-postgres
    environment:
      POSTGRES_DB: mlflow
      POSTGRES_USER: mlflow
      POSTGRES_PASSWORD: mlflow123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mlflow"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - mlops-network

  # MLflow Tracking Server
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.9.2
    container_name: mlops-mlflow
    ports:
      - "5000:5000"
    environment:
      MLFLOW_BACKEND_STORE_URI: postgresql://mlflow:mlflow123@postgres:5432/mlflow
      MLFLOW_ARTIFACT_ROOT: /mlflow/artifacts
    volumes:
      - mlflow_data:/mlflow
    depends_on:
      postgres:
        condition: service_healthy
    command: >
      mlflow server
      --backend-store-uri postgresql://mlflow:mlflow123@postgres:5432/mlflow
      --default-artifact-root /mlflow/artifacts
      --host 0.0.0.0
      --port 5000
    networks:
      - mlops-network

  # ChromaDB Vector Store
  chromadb:
    image: ghcr.io/chroma-core/chroma:0.4.22
    container_name: mlops-chromadb
    ports:
      - "8100:8000"
    volumes:
      - chromadb_data:/chroma/chroma
    environment:
      IS_PERSISTENT: "TRUE"
      ANONYMIZED_TELEMETRY: "FALSE"
    networks:
      - mlops-network

  # PyTorch Service
  pytorch-service:
    build:
      context: .
      dockerfile: Dockerfile.pytorch
    container_name: mlops-pytorch
    ports:
      - "8000:8000"
    environment:
      SERVICE_NAME: pytorch-service
      RABBITMQ_URL: amqp://admin:admin123@rabbitmq:5672/
      REDIS_URL: redis://redis:6379/0
      MLFLOW_TRACKING_URI: http://mlflow:5000
      CHROMA_HOST: chromadb
      CHROMA_PORT: 8000
    volumes:
      - ./src:/app/src
      - ./models:/app/models
      - model_cache:/root/.cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on:
      rabbitmq:
        condition: service_healthy
      redis:
        condition: service_healthy
      mlflow:
        condition: service_started
    networks:
      - mlops-network

  # TensorFlow Service
  tensorflow-service:
    build:
      context: .
      dockerfile: Dockerfile.tensorflow
    container_name: mlops-tensorflow
    ports:
      - "8001:8001"
    environment:
      SERVICE_NAME: tensorflow-service
      RABBITMQ_URL: amqp://admin:admin123@rabbitmq:5672/
      REDIS_URL: redis://redis:6379/1
      MLFLOW_TRACKING_URI: http://mlflow:5000
    volumes:
      - ./src:/app/src
      - ./models:/app/models
      - tf_model_cache:/root/.cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on:
      rabbitmq:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - mlops-network

  # RAG Service
  rag-service:
    build:
      context: .
      dockerfile: Dockerfile.pytorch  # Usa PyTorch base
      args:
        WORKDIR: /app
    container_name: mlops-rag
    ports:
      - "8002:8002"
    environment:
      SERVICE_NAME: rag-service
      RABBITMQ_URL: amqp://admin:admin123@rabbitmq:5672/
      REDIS_URL: redis://redis:6379/2
      CHROMA_HOST: chromadb
      CHROMA_PORT: 8000
      MLFLOW_TRACKING_URI: http://mlflow:5000
    volumes:
      - ./src:/app/src
      - ./data:/app/data
    depends_on:
      rabbitmq:
        condition: service_healthy
      redis:
        condition: service_healthy
      chromadb:
        condition: service_started
    command: ["uvicorn", "src.rag_service:app", "--host", "0.0.0.0", "--port", "8002"]
    networks:
      - mlops-network

  # Prometheus para Monitoring
  prometheus:
    image: prom/prometheus:v2.48.1
    container_name: mlops-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - mlops-network

  # Grafana para Visualización
  grafana:
    image: grafana/grafana:10.2.3
    container_name: mlops-grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin123
      GF_INSTALL_PLUGINS: redis-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./config/grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    networks:
      - mlops-network

volumes:
  rabbitmq_data:
  redis_data:
  postgres_data:
  mlflow_data:
  chromadb_data:
  model_cache:
  tf_model_cache:
  prometheus_data:
  grafana_data:

networks:
  mlops-network:
    driver: bridge
```

### 2.4 Configuración de Prometheus

```yaml
# config/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'pytorch-service'
    static_configs:
      - targets: ['pytorch-service:8000']
    metrics_path: '/metrics'

  - job_name: 'tensorflow-service'
    static_configs:
      - targets: ['tensorflow-service:8001']
    metrics_path: '/metrics'

  - job_name: 'rag-service'
    static_configs:
      - targets: ['rag-service:8002']
    metrics_path: '/metrics'

  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['rabbitmq:15692']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

---

## 3. Pipeline de ML con Event-Driven Architecture

### 3.1 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                  ML Pipeline Event Flow                      │
└─────────────────────────────────────────────────────────────┘

┌──────────┐    event:      ┌──────────┐    event:     ┌──────────┐
│  Data    │  data.ingested │ Training │  model.trained│ Registry │
│ Ingress  │───────────────►│ Service  │──────────────►│ Service  │
└──────────┘                └──────────┘               └──────────┘
                                  │
                                  │ event:
                                  │ model.validated
                                  ▼
┌──────────┐    event:      ┌──────────┐
│Inference │◄───────────────│ Deploy   │
│ Service  │  model.deployed│ Service  │
└──────────┘                └──────────┘
     │
     │ event:
     │ prediction.made
     ▼
┌──────────┐
│ Monitor  │
│ Service  │
└──────────┘
```

### 3.2 Event Schema Definitions

```python
# src/events/schemas.py
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class EventType(str, Enum):
    """Tipos de eventos en el pipeline."""
    DATA_INGESTED = "data.ingested"
    DATA_VALIDATED = "data.validated"
    TRAINING_STARTED = "training.started"
    TRAINING_COMPLETED = "training.completed"
    TRAINING_FAILED = "training.failed"
    MODEL_VALIDATED = "model.validated"
    MODEL_REGISTERED = "model.registered"
    MODEL_DEPLOYED = "model.deployed"
    PREDICTION_REQUESTED = "prediction.requested"
    PREDICTION_COMPLETED = "prediction.completed"
    DRIFT_DETECTED = "drift.detected"


class EventMetadata(BaseModel):
    """Metadata común para todos los eventos."""
    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_service: str
    correlation_id: Optional[UUID] = None
    version: str = "1.0.0"


class BaseEvent(BaseModel):
    """Clase base para todos los eventos."""
    metadata: EventMetadata
    payload: Dict[str, Any]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }


class DataIngestedEvent(BaseEvent):
    """Evento cuando datos nuevos son ingeridos."""
    class Payload(BaseModel):
        dataset_id: str
        dataset_path: str
        num_samples: int
        features: list[str]
        dataset_type: str  # train, val, test

    payload: Payload


class TrainingStartedEvent(BaseEvent):
    """Evento cuando inicia entrenamiento."""
    class Payload(BaseModel):
        experiment_id: str
        run_id: str
        model_type: str  # pytorch, tensorflow
        dataset_id: str
        hyperparameters: Dict[str, Any]

    payload: Payload


class TrainingCompletedEvent(BaseEvent):
    """Evento cuando termina entrenamiento."""
    class Payload(BaseModel):
        experiment_id: str
        run_id: str
        model_path: str
        metrics: Dict[str, float]
        duration_seconds: float
        artifacts: Dict[str, str]

    payload: Payload


class ModelValidatedEvent(BaseEvent):
    """Evento cuando modelo es validado."""
    class Payload(BaseModel):
        model_id: str
        run_id: str
        validation_metrics: Dict[str, float]
        passed: bool
        threshold_criteria: Dict[str, float]

    payload: Payload


class ModelDeployedEvent(BaseEvent):
    """Evento cuando modelo es desplegado."""
    class Payload(BaseModel):
        model_id: str
        model_version: str
        deployment_env: str  # dev, staging, prod
        endpoint_url: str
        replicas: int

    payload: Payload


class PredictionRequestedEvent(BaseEvent):
    """Evento cuando se solicita predicción."""
    class Payload(BaseModel):
        request_id: str
        model_id: str
        model_version: str
        input_data: Dict[str, Any]
        priority: str = "normal"  # low, normal, high

    payload: Payload


class PredictionCompletedEvent(BaseEvent):
    """Evento cuando predicción es completada."""
    class Payload(BaseModel):
        request_id: str
        prediction: Any
        confidence: Optional[float] = None
        latency_ms: float
        model_version: str

    payload: Payload


class DriftDetectedEvent(BaseEvent):
    """Evento cuando se detecta drift en datos o modelo."""
    class Payload(BaseModel):
        drift_type: str  # data_drift, concept_drift, model_drift
        metric_name: str
        current_value: float
        baseline_value: float
        threshold: float
        severity: str  # low, medium, high

    payload: Payload
```

### 3.3 Event Bus Implementation

```python
# src/events/event_bus.py
import json
import logging
from typing import Callable, Dict, List, Optional
from uuid import UUID
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import redis
from redis import Redis

from .schemas import BaseEvent, EventType

logger = logging.getLogger(__name__)


class EventBus:
    """
    Event Bus usando RabbitMQ para pub/sub.
    Soporta routing por tipo de evento y dead letter queues.
    """

    def __init__(
        self,
        rabbitmq_url: str,
        exchange_name: str = "ml_events",
        exchange_type: str = "topic",
    ):
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[BlockingChannel] = None
        self._handlers: Dict[str, List[Callable]] = {}

    def connect(self):
        """Establece conexión con RabbitMQ."""
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.rabbitmq_url)
            )
            self.channel = self.connection.channel()

            # Declarar exchange
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type=self.exchange_type,
                durable=True,
            )

            # Declarar dead letter exchange
            self.channel.exchange_declare(
                exchange=f"{self.exchange_name}.dlx",
                exchange_type="fanout",
                durable=True,
            )

            logger.info(f"Connected to RabbitMQ: {self.exchange_name}")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def disconnect(self):
        """Cierra conexión con RabbitMQ."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("Disconnected from RabbitMQ")

    def publish(
        self,
        event: BaseEvent,
        routing_key: Optional[str] = None,
    ) -> bool:
        """
        Publica un evento al exchange.

        Args:
            event: Evento a publicar
            routing_key: Routing key (default: event_type)

        Returns:
            bool: True si se publicó exitosamente
        """
        if not self.channel:
            self.connect()

        try:
            routing_key = routing_key or event.metadata.event_type.value

            properties = BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # persistent
                message_id=str(event.metadata.event_id),
                correlation_id=str(event.metadata.correlation_id)
                if event.metadata.correlation_id
                else None,
                headers={
                    "source_service": event.metadata.source_service,
                    "event_type": event.metadata.event_type.value,
                    "timestamp": event.metadata.timestamp.isoformat(),
                },
            )

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=event.model_dump_json(),
                properties=properties,
            )

            logger.info(
                f"Published event {event.metadata.event_type.value} "
                f"with routing key {routing_key}"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to publish event: {e}")
            return False

    def subscribe(
        self,
        queue_name: str,
        routing_keys: List[str],
        callback: Callable[[BaseEvent], None],
        auto_ack: bool = False,
    ):
        """
        Suscribe a eventos con routing keys específicos.

        Args:
            queue_name: Nombre de la cola
            routing_keys: Lista de routing keys (soporta wildcards)
            callback: Función a llamar cuando llega un evento
            auto_ack: Auto-acknowledgement
        """
        if not self.channel:
            self.connect()

        try:
            # Declarar cola con dead letter exchange
            self.channel.queue_declare(
                queue=queue_name,
                durable=True,
                arguments={
                    "x-dead-letter-exchange": f"{self.exchange_name}.dlx",
                    "x-message-ttl": 86400000,  # 24 horas
                },
            )

            # Bind a routing keys
            for routing_key in routing_keys:
                self.channel.queue_bind(
                    exchange=self.exchange_name,
                    queue=queue_name,
                    routing_key=routing_key,
                )

            # Wrapper para callback
            def wrapped_callback(
                ch: BlockingChannel,
                method: Basic.Deliver,
                properties: BasicProperties,
                body: bytes,
            ):
                try:
                    event_data = json.loads(body)
                    event = BaseEvent(**event_data)

                    logger.info(
                        f"Received event {event.metadata.event_type.value} "
                        f"on queue {queue_name}"
                    )

                    callback(event)

                    if not auto_ack:
                        ch.basic_ack(delivery_tag=method.delivery_tag)

                except Exception as e:
                    logger.error(f"Error processing event: {e}")
                    if not auto_ack:
                        # Requeue=False envía a DLX
                        ch.basic_nack(
                            delivery_tag=method.delivery_tag, requeue=False
                        )

            # Configurar QoS
            self.channel.basic_qos(prefetch_count=10)

            # Comenzar consumo
            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=wrapped_callback,
                auto_ack=auto_ack,
            )

            logger.info(
                f"Subscribed to queue {queue_name} "
                f"with routing keys {routing_keys}"
            )

        except Exception as e:
            logger.error(f"Failed to subscribe: {e}")
            raise

    def start_consuming(self):
        """Inicia el loop de consumo de mensajes."""
        if not self.channel:
            raise RuntimeError("Not connected to RabbitMQ")

        logger.info("Starting to consume messages...")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.channel.stop_consuming()
        finally:
            self.disconnect()


class RedisEventStore:
    """
    Event Store usando Redis para almacenar historial de eventos.
    Útil para event sourcing y debugging.
    """

    def __init__(self, redis_url: str):
        self.redis_client: Redis = redis.from_url(redis_url, decode_responses=True)

    def store_event(self, event: BaseEvent) -> bool:
        """Almacena evento en Redis."""
        try:
            # Key por evento
            event_key = f"event:{event.metadata.event_id}"
            self.redis_client.setex(
                event_key,
                86400,  # TTL 24 horas
                event.model_dump_json(),
            )

            # Stream por tipo de evento
            stream_key = f"stream:{event.metadata.event_type.value}"
            self.redis_client.xadd(
                stream_key,
                {"event_id": str(event.metadata.event_id), "data": event.model_dump_json()},
                maxlen=10000,  # Mantener últimos 10k eventos
            )

            # Índice por correlation_id
            if event.metadata.correlation_id:
                corr_key = f"correlation:{event.metadata.correlation_id}"
                self.redis_client.rpush(corr_key, str(event.metadata.event_id))
                self.redis_client.expire(corr_key, 86400)

            return True

        except Exception as e:
            logger.error(f"Failed to store event: {e}")
            return False

    def get_event(self, event_id: UUID) -> Optional[BaseEvent]:
        """Recupera evento por ID."""
        try:
            event_key = f"event:{event_id}"
            event_data = self.redis_client.get(event_key)
            if event_data:
                return BaseEvent.model_validate_json(event_data)
            return None
        except Exception as e:
            logger.error(f"Failed to get event: {e}")
            return None

    def get_events_by_correlation(self, correlation_id: UUID) -> List[BaseEvent]:
        """Recupera todos los eventos de una correlación."""
        try:
            corr_key = f"correlation:{correlation_id}"
            event_ids = self.redis_client.lrange(corr_key, 0, -1)
            events = []
            for event_id in event_ids:
                event = self.get_event(UUID(event_id))
                if event:
                    events.append(event)
            return events
        except Exception as e:
            logger.error(f"Failed to get correlated events: {e}")
            return []

    def get_stream_events(
        self,
        event_type: EventType,
        count: int = 100,
    ) -> List[BaseEvent]:
        """Obtiene eventos recientes de un stream."""
        try:
            stream_key = f"stream:{event_type.value}"
            messages = self.redis_client.xrevrange(stream_key, count=count)
            events = []
            for _, message_data in messages:
                event_json = message_data.get("data")
                if event_json:
                    events.append(BaseEvent.model_validate_json(event_json))
            return events
        except Exception as e:
            logger.error(f"Failed to get stream events: {e}")
            return []
```

### 3.4 Training Service (PyTorch)

```python
# src/services/pytorch_training_service.py
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from prometheus_client import Counter, Histogram, Gauge

from ..events.event_bus import EventBus, RedisEventStore
from ..events.schemas import (
    EventMetadata,
    EventType,
    TrainingStartedEvent,
    TrainingCompletedEvent,
    TrainingFailedEvent,
)

logger = logging.getLogger(__name__)

# Métricas Prometheus
training_started_total = Counter(
    'training_started_total',
    'Total number of training jobs started'
)
training_completed_total = Counter(
    'training_completed_total',
    'Total number of training jobs completed',
    ['status']
)
training_duration = Histogram(
    'training_duration_seconds',
    'Training duration in seconds'
)
current_epoch = Gauge(
    'current_training_epoch',
    'Current training epoch',
    ['experiment_id']
)


class PyTorchTrainingService:
    """
    Servicio de entrenamiento para modelos PyTorch.
    Escucha eventos de data.validated y ejecuta entrenamiento.
    """

    def __init__(
        self,
        event_bus: EventBus,
        event_store: RedisEventStore,
        mlflow_tracking_uri: str,
        model_registry_path: Path,
    ):
        self.event_bus = event_bus
        self.event_store = event_store
        self.mlflow_tracking_uri = mlflow_tracking_uri
        self.model_registry_path = model_registry_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        mlflow.set_tracking_uri(mlflow_tracking_uri)

    def start(self):
        """Inicia el servicio y suscribe a eventos."""
        logger.info("Starting PyTorch Training Service...")

        self.event_bus.subscribe(
            queue_name="pytorch_training_queue",
            routing_keys=["data.validated", "training.requested"],
            callback=self.handle_training_event,
        )

        self.event_bus.start_consuming()

    def handle_training_event(self, event: BaseEvent):
        """Maneja eventos de entrenamiento."""
        logger.info(f"Handling training event: {event.metadata.event_type}")

        # Extraer parámetros del evento
        dataset_id = event.payload.get("dataset_id")
        hyperparameters = event.payload.get("hyperparameters", {})

        # Iniciar entrenamiento
        self.train_model(
            dataset_id=dataset_id,
            hyperparameters=hyperparameters,
            correlation_id=event.metadata.correlation_id or uuid4(),
        )

    def train_model(
        self,
        dataset_id: str,
        hyperparameters: Dict[str, Any],
        correlation_id: Any,
    ):
        """
        Entrena un modelo PyTorch.

        Args:
            dataset_id: ID del dataset
            hyperparameters: Hiperparámetros del modelo
            correlation_id: ID de correlación para tracking
        """
        experiment_id = f"pytorch_exp_{uuid4().hex[:8]}"
        run_id = f"run_{uuid4().hex[:8]}"

        training_started_total.inc()

        # Publicar evento training.started
        started_event = TrainingStartedEvent(
            metadata=EventMetadata(
                event_type=EventType.TRAINING_STARTED,
                source_service="pytorch-training-service",
                correlation_id=correlation_id,
            ),
            payload=TrainingStartedEvent.Payload(
                experiment_id=experiment_id,
                run_id=run_id,
                model_type="pytorch",
                dataset_id=dataset_id,
                hyperparameters=hyperparameters,
            ),
        )
        self.event_bus.publish(started_event)
        self.event_store.store_event(started_event)

        start_time = datetime.utcnow()

        try:
            # Iniciar MLflow run
            with mlflow.start_run(run_name=run_id) as run:
                # Log hyperparameters
                mlflow.log_params(hyperparameters)

                # Cargar datos (simulado)
                train_loader, val_loader = self._load_data(dataset_id)

                # Crear modelo
                model = self._create_model(hyperparameters)
                model.to(self.device)

                # Configurar entrenamiento
                criterion = nn.CrossEntropyLoss()
                optimizer = torch.optim.Adam(
                    model.parameters(),
                    lr=hyperparameters.get("learning_rate", 0.001),
                )

                # Training loop
                num_epochs = hyperparameters.get("num_epochs", 10)
                best_val_loss = float("inf")

                for epoch in range(num_epochs):
                    current_epoch.labels(experiment_id=experiment_id).set(epoch)

                    # Train
                    train_loss, train_acc = self._train_epoch(
                        model, train_loader, criterion, optimizer
                    )

                    # Validate
                    val_loss, val_acc = self._validate_epoch(
                        model, val_loader, criterion
                    )

                    # Log metrics
                    mlflow.log_metrics(
                        {
                            "train_loss": train_loss,
                            "train_accuracy": train_acc,
                            "val_loss": val_loss,
                            "val_accuracy": val_acc,
                        },
                        step=epoch,
                    )

                    logger.info(
                        f"Epoch {epoch + 1}/{num_epochs} - "
                        f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
                        f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}"
                    )

                    # Save best model
                    if val_loss < best_val_loss:
                        best_val_loss = val_loss
                        model_path = self.model_registry_path / experiment_id
                        model_path.mkdir(parents=True, exist_ok=True)
                        torch.save(
                            model.state_dict(),
                            model_path / f"model_epoch_{epoch}.pt",
                        )

                # Log modelo final
                mlflow.pytorch.log_model(model, "model")

                # Calcular métricas finales
                final_metrics = {
                    "final_train_loss": train_loss,
                    "final_train_accuracy": train_acc,
                    "final_val_loss": val_loss,
                    "final_val_accuracy": val_acc,
                    "best_val_loss": best_val_loss,
                }

                duration = (datetime.utcnow() - start_time).total_seconds()
                training_duration.observe(duration)

                # Publicar evento training.completed
                completed_event = TrainingCompletedEvent(
                    metadata=EventMetadata(
                        event_type=EventType.TRAINING_COMPLETED,
                        source_service="pytorch-training-service",
                        correlation_id=correlation_id,
                    ),
                    payload=TrainingCompletedEvent.Payload(
                        experiment_id=experiment_id,
                        run_id=run_id,
                        model_path=str(model_path),
                        metrics=final_metrics,
                        duration_seconds=duration,
                        artifacts={"mlflow_run_id": run.info.run_id},
                    ),
                )
                self.event_bus.publish(completed_event)
                self.event_store.store_event(completed_event)

                training_completed_total.labels(status="success").inc()

                logger.info(f"Training completed successfully: {experiment_id}")

        except Exception as e:
            logger.error(f"Training failed: {e}")
            training_completed_total.labels(status="failed").inc()

            # Publicar evento training.failed
            failed_event = TrainingFailedEvent(
                metadata=EventMetadata(
                    event_type=EventType.TRAINING_FAILED,
                    source_service="pytorch-training-service",
                    correlation_id=correlation_id,
                ),
                payload={
                    "experiment_id": experiment_id,
                    "run_id": run_id,
                    "error": str(e),
                },
            )
            self.event_bus.publish(failed_event)
            self.event_store.store_event(failed_event)

    def _load_data(self, dataset_id: str):
        """Carga datos para entrenamiento (implementación simulada)."""
        # En producción, cargar datos reales desde dataset_id
        # Por ahora, datos dummy
        from torch.utils.data import TensorDataset

        X_train = torch.randn(1000, 10)
        y_train = torch.randint(0, 2, (1000,))
        X_val = torch.randn(200, 10)
        y_val = torch.randint(0, 2, (200,))

        train_dataset = TensorDataset(X_train, y_train)
        val_dataset = TensorDataset(X_val, y_val)

        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=32)

        return train_loader, val_loader

    def _create_model(self, hyperparameters: Dict[str, Any]) -> nn.Module:
        """Crea modelo basado en hiperparámetros."""
        # Modelo simple de ejemplo
        class SimpleClassifier(nn.Module):
            def __init__(self, input_dim=10, hidden_dim=64, num_classes=2):
                super().__init__()
                self.fc1 = nn.Linear(input_dim, hidden_dim)
                self.relu = nn.ReLU()
                self.dropout = nn.Dropout(0.3)
                self.fc2 = nn.Linear(hidden_dim, num_classes)

            def forward(self, x):
                x = self.fc1(x)
                x = self.relu(x)
                x = self.dropout(x)
                x = self.fc2(x)
                return x

        return SimpleClassifier(
            hidden_dim=hyperparameters.get("hidden_dim", 64)
        )

    def _train_epoch(
        self,
        model: nn.Module,
        dataloader: DataLoader,
        criterion: nn.Module,
        optimizer: torch.optim.Optimizer,
    ):
        """Entrena una época."""
        model.train()
        total_loss = 0
        correct = 0
        total = 0

        for inputs, targets in dataloader:
            inputs, targets = inputs.to(self.device), targets.to(self.device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        return total_loss / len(dataloader), correct / total

    def _validate_epoch(
        self,
        model: nn.Module,
        dataloader: DataLoader,
        criterion: nn.Module,
    ):
        """Valida una época."""
        model.eval()
        total_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for inputs, targets in dataloader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)

                outputs = model(inputs)
                loss = criterion(outputs, targets)

                total_loss += loss.item()
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

        return total_loss / len(dataloader), correct / total
```

---

## 4. RAG: Retrieval Augmented Generation

### 4.1 ¿Qué es RAG?

**RAG** combina retrieval (búsqueda) con generation (generación) para:

1. **Buscar** información relevante en una base de conocimiento
2. **Aumentar** el contexto del LLM con esa información
3. **Generar** respuestas más precisas y actualizadas

#### Arquitectura RAG

```
┌──────────────────────────────────────────────────────────┐
│                    RAG Architecture                       │
└──────────────────────────────────────────────────────────┘

   User Query                 ┌────────────────┐
       │                      │  LLM Service   │
       │                      │  (Generation)  │
       ▼                      └────────▲───────┘
┌──────────────┐                      │
│   Embedding  │                      │
│    Model     │              ┌───────┴────────┐
└──────┬───────┘              │ Prompt Builder │
       │                      │  + Context     │
       │                      └───────▲────────┘
       │                              │
       ▼                              │
┌──────────────┐                      │
│Vector Store  │──────────────────────┘
│  (ChromaDB)  │     Retrieved Docs
└──────────────┘
       ▲
       │
  Documents
  + Metadata
```

### 4.2 RAG Service Implementation

```python
# src/services/rag_service.py
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from prometheus_client import Counter, Histogram, make_asgi_app

logger = logging.getLogger(__name__)

# Métricas
rag_queries_total = Counter(
    'rag_queries_total',
    'Total RAG queries'
)
rag_query_duration = Histogram(
    'rag_query_duration_seconds',
    'RAG query duration'
)
documents_indexed_total = Counter(
    'documents_indexed_total',
    'Total documents indexed'
)

# FastAPI App
app = FastAPI(title="RAG Service", version="1.0.0")

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


class DocumentInput(BaseModel):
    """Input para indexar documentos."""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    document_id: Optional[str] = None


class QueryInput(BaseModel):
    """Input para queries."""
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    filter: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    """Respuesta de query."""
    query: str
    results: List[Dict[str, Any]]
    num_results: int


class RAGService:
    """
    Servicio RAG con ChromaDB y Sentence Transformers.
    """

    def __init__(
        self,
        chroma_host: str = "localhost",
        chroma_port: int = 8000,
        collection_name: str = "documents",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        """
        Inicializa RAG Service.

        Args:
            chroma_host: Host de ChromaDB
            chroma_port: Puerto de ChromaDB
            collection_name: Nombre de la colección
            embedding_model: Modelo de embeddings
            chunk_size: Tamaño de chunks de texto
            chunk_overlap: Overlap entre chunks
        """
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # ChromaDB Client
        self.chroma_client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(anonymized_telemetry=False),
        )

        # Crear o obtener colección
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "RAG document collection"},
        )

        # Modelo de embeddings
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)

        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        logger.info("RAG Service initialized")

    def embed_text(self, text: str) -> List[float]:
        """Genera embeddings para texto."""
        embeddings = self.embedding_model.encode(text, convert_to_tensor=False)
        return embeddings.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Genera embeddings para batch de textos."""
        embeddings = self.embedding_model.encode(
            texts,
            batch_size=32,
            convert_to_tensor=False,
            show_progress_bar=True,
        )
        return embeddings.tolist()

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Divide documentos en chunks."""
        return self.text_splitter.split_documents(documents)

    def index_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        document_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Indexa un documento en ChromaDB.

        Args:
            content: Contenido del documento
            metadata: Metadata del documento
            document_id: ID del documento (opcional)

        Returns:
            Dict con información de indexación
        """
        try:
            # Crear documento
            doc = Document(page_content=content, metadata=metadata)

            # Dividir en chunks
            chunks = self.text_splitter.split_documents([doc])

            # Preparar datos para ChromaDB
            chunk_ids = []
            chunk_texts = []
            chunk_metadatas = []

            for i, chunk in enumerate(chunks):
                chunk_id = f"{document_id or 'doc'}_{i}" if document_id else f"chunk_{i}"
                chunk_ids.append(chunk_id)
                chunk_texts.append(chunk.page_content)

                # Metadata con chunk info
                chunk_metadata = metadata.copy()
                chunk_metadata.update({
                    "chunk_index": i,
                    "chunk_total": len(chunks),
                    "document_id": document_id or "unknown",
                })
                chunk_metadatas.append(chunk_metadata)

            # Generar embeddings
            embeddings = self.embed_batch(chunk_texts)

            # Agregar a ChromaDB
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=chunk_texts,
                metadatas=chunk_metadatas,
            )

            documents_indexed_total.inc()

            logger.info(
                f"Indexed document {document_id} with {len(chunks)} chunks"
            )

            return {
                "document_id": document_id,
                "num_chunks": len(chunks),
                "chunk_ids": chunk_ids,
            }

        except Exception as e:
            logger.error(f"Failed to index document: {e}")
            raise

    def query(
        self,
        query_text: str,
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Realiza query en la base de conocimiento.

        Args:
            query_text: Texto de búsqueda
            top_k: Número de resultados
            filter: Filtros de metadata

        Returns:
            Lista de resultados relevantes
        """
        rag_queries_total.inc()

        try:
            with rag_query_duration.time():
                # Generar embedding de query
                query_embedding = self.embed_text(query_text)

                # Buscar en ChromaDB
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=filter,
                    include=["documents", "metadatas", "distances"],
                )

                # Formatear resultados
                formatted_results = []
                for i in range(len(results["ids"][0])):
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i],
                        "relevance_score": 1 - results["distances"][0][i],  # Similarity
                    })

                logger.info(
                    f"Query '{query_text}' returned {len(formatted_results)} results"
                )

                return formatted_results

        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    def delete_document(self, document_id: str):
        """Elimina documento de la colección."""
        try:
            # Buscar chunks del documento
            results = self.collection.get(
                where={"document_id": document_id},
                include=["metadatas"],
            )

            if results["ids"]:
                self.collection.delete(ids=results["ids"])
                logger.info(f"Deleted document {document_id}")
            else:
                logger.warning(f"Document {document_id} not found")

        except Exception as e:
            logger.error(f"Failed to delete document: {e}")
            raise

    def get_collection_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la colección."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "num_documents": count,
                "embedding_model": self.embedding_model.get_sentence_embedding_dimension(),
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            raise


# Singleton instance
rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Dependency para obtener RAG service."""
    if rag_service is None:
        raise RuntimeError("RAG Service not initialized")
    return rag_service


@app.on_event("startup")
async def startup_event():
    """Inicializa RAG service al arrancar."""
    global rag_service

    import os

    chroma_host = os.getenv("CHROMA_HOST", "localhost")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))

    rag_service = RAGService(
        chroma_host=chroma_host,
        chroma_port=chroma_port,
    )

    logger.info("RAG Service started")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "rag-service"}


@app.post("/index", response_model=Dict[str, Any])
async def index_document(doc: DocumentInput):
    """Endpoint para indexar documentos."""
    service = get_rag_service()

    try:
        result = service.index_document(
            content=doc.content,
            metadata=doc.metadata,
            document_id=doc.document_id,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_documents(query: QueryInput):
    """Endpoint para queries."""
    service = get_rag_service()

    try:
        results = service.query(
            query_text=query.query,
            top_k=query.top_k,
            filter=query.filter,
        )

        return QueryResponse(
            query=query.query,
            results=results,
            num_results=len(results),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/document/{document_id}")
async def delete_document(document_id: str):
    """Endpoint para eliminar documentos."""
    service = get_rag_service()

    try:
        service.delete_document(document_id)
        return {"status": "deleted", "document_id": document_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Endpoint para estadísticas."""
    service = get_rag_service()

    try:
        return service.get_collection_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 4.3 RAG con LangChain Integration

```python
# src/services/rag_langchain.py
from typing import List, Optional
import os

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate


class LangChainRAG:
    """
    RAG implementation usando LangChain.
    """

    def __init__(
        self,
        chroma_host: str = "localhost",
        chroma_port: int = 8000,
        collection_name: str = "documents",
        llm_model: str = "gpt-3.5-turbo",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        # Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model
        )

        # Vector store
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            client_settings={
                "chroma_api_impl": "chromadb.api.fastapi.FastAPI",
                "chroma_server_host": chroma_host,
                "chroma_server_http_port": chroma_port,
            },
        )

        # LLM
        self.llm = OpenAI(
            model_name=llm_model,
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Prompt template
        self.prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Helpful Answer:"""

        self.PROMPT = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"],
        )

        # Retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 5}
            ),
            chain_type_kwargs={"prompt": self.PROMPT},
            return_source_documents=True,
        )

    def query(self, question: str) -> dict:
        """
        Realiza query usando RAG.

        Returns:
            dict con 'result' y 'source_documents'
        """
        response = self.qa_chain({"query": question})

        return {
            "answer": response["result"],
            "sources": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                }
                for doc in response["source_documents"]
            ],
        }
```

---

## 5. Proyecto Completo Integrado

### 5.1 Caso de Uso: Sistema de Clasificación de Documentos con RAG

Vamos a construir un sistema completo que:

1. **Ingesta documentos** (PDFs, textos)
2. **Clasifica automáticamente** usando modelo ML
3. **Indexa en RAG** para búsqueda semántica
4. **Genera respuestas** basadas en documentos

#### Arquitectura del Proyecto

```
┌──────────────────────────────────────────────────────────────┐
│          Document Classification & RAG System                 │
└──────────────────────────────────────────────────────────────┘

┌──────────┐     data.ingested    ┌──────────────┐
│ Document │────────────────────► │Classification│
│ Ingress  │                       │   Service    │
└──────────┘                       │  (PyTorch)   │
                                   └───────┬──────┘
                                           │ document.classified
                                           ▼
                                   ┌──────────────┐
                                   │     RAG      │
                                   │   Indexer    │
                                   └───────┬──────┘
                                           │
                                           ▼
                                   ┌──────────────┐
                                   │  ChromaDB    │
                                   │ Vector Store │
                                   └───────┬──────┘
                                           │
     Query API ◄───────────────────────────┘
```

### 5.2 Document Classification Service

```python
# src/services/document_classifier.py
import logging
from typing import Dict, List, Optional
from pathlib import Path

import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline,
)

from ..events.event_bus import EventBus
from ..events.schemas import BaseEvent, EventMetadata, EventType

logger = logging.getLogger(__name__)


class DocumentClassifier:
    """
    Clasificador de documentos usando transformers.
    """

    def __init__(
        self,
        event_bus: EventBus,
        model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
        categories: Optional[List[str]] = None,
    ):
        self.event_bus = event_bus
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Cargar modelo preentrenado
        logger.info(f"Loading model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        # Pipeline de clasificación
        self.classifier = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1,
        )

        self.categories = categories or [
            "technical",
            "business",
            "legal",
            "marketing",
            "other",
        ]

        logger.info("Document Classifier initialized")

    def start(self):
        """Inicia servicio y suscribe a eventos."""
        logger.info("Starting Document Classifier Service...")

        self.event_bus.subscribe(
            queue_name="document_classification_queue",
            routing_keys=["data.ingested"],
            callback=self.handle_document_event,
        )

        self.event_bus.start_consuming()

    def handle_document_event(self, event: BaseEvent):
        """Maneja eventos de documentos nuevos."""
        logger.info(f"Classifying document from event: {event.metadata.event_id}")

        document_id = event.payload.get("document_id")
        content = event.payload.get("content")

        if not content:
            logger.warning(f"No content in event {event.metadata.event_id}")
            return

        # Clasificar documento
        classification = self.classify(content)

        # Publicar evento document.classified
        classified_event = BaseEvent(
            metadata=EventMetadata(
                event_type=EventType.DOCUMENT_CLASSIFIED,
                source_service="document-classifier",
                correlation_id=event.metadata.correlation_id,
            ),
            payload={
                "document_id": document_id,
                "classification": classification,
                "content": content,
            },
        )

        self.event_bus.publish(classified_event)
        logger.info(
            f"Document {document_id} classified as: {classification['label']}"
        )

    def classify(self, text: str, top_k: int = 3) -> Dict:
        """
        Clasifica texto.

        Args:
            text: Texto a clasificar
            top_k: Top K categorías

        Returns:
            Dict con clasificación y scores
        """
        try:
            # Truncar si es muy largo
            max_length = 512
            text = text[:max_length]

            # Clasificar
            results = self.classifier(text, top_k=top_k)

            return {
                "label": results[0]["label"],
                "score": results[0]["score"],
                "top_k": results,
            }

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return {
                "label": "unknown",
                "score": 0.0,
                "error": str(e),
            }
```

### 5.3 Main Application

```python
# src/main.py
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from .events.event_bus import EventBus, RedisEventStore
from .events.schemas import BaseEvent, EventMetadata, EventType
from .services.document_classifier import DocumentClassifier
from .services.rag_service import RAGService

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Config
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin123@localhost:5672/")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# Global instances
event_bus: Optional[EventBus] = None
event_store: Optional[RedisEventStore] = None
rag_service: Optional[RAGService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager."""
    global event_bus, event_store, rag_service

    # Startup
    logger.info("Starting MLOps services...")

    event_bus = EventBus(RABBITMQ_URL)
    event_bus.connect()

    event_store = RedisEventStore(REDIS_URL)

    rag_service = RAGService(
        chroma_host=CHROMA_HOST,
        chroma_port=CHROMA_PORT,
    )

    logger.info("All services started successfully")

    yield

    # Shutdown
    logger.info("Shutting down services...")
    if event_bus:
        event_bus.disconnect()


app = FastAPI(
    title="MLOps Platform",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: Optional[str] = None,
):
    """
    Endpoint para subir documentos.
    Publica evento data.ingested para procesamiento.
    """
    try:
        # Leer contenido
        content = await file.read()
        text_content = content.decode("utf-8")

        # Generar ID
        import uuid
        document_id = str(uuid.uuid4())

        # Publicar evento
        event = BaseEvent(
            metadata=EventMetadata(
                event_type=EventType.DATA_INGESTED,
                source_service="api-gateway",
            ),
            payload={
                "document_id": document_id,
                "filename": file.filename,
                "content": text_content,
                "size": len(content),
                "category": category,
            },
        )

        event_bus.publish(event)
        event_store.store_event(event)

        logger.info(f"Document uploaded: {document_id}")

        return {
            "document_id": document_id,
            "filename": file.filename,
            "status": "processing",
        }

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/query")
async def query_documents(query: str, top_k: int = 5):
    """Query RAG system."""
    try:
        results = rag_service.query(
            query_text=query,
            top_k=top_k,
        )

        return {
            "query": query,
            "results": results,
            "num_results": len(results),
        }

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
```

---

## 6. Testing, Monitoring y Deployment

### 6.1 Testing Strategy

```python
# tests/test_rag_service.py
import pytest
from src.services.rag_service import RAGService


@pytest.fixture
def rag_service():
    """Fixture para RAG service."""
    return RAGService(
        chroma_host="localhost",
        chroma_port=8000,
        collection_name="test_collection",
    )


def test_index_document(rag_service):
    """Test indexing de documentos."""
    result = rag_service.index_document(
        content="This is a test document about machine learning.",
        metadata={"category": "technical", "author": "test"},
        document_id="test_doc_1",
    )

    assert result["document_id"] == "test_doc_1"
    assert result["num_chunks"] > 0


def test_query(rag_service):
    """Test query."""
    # Indexar primero
    rag_service.index_document(
        content="PyTorch is a deep learning framework.",
        metadata={"category": "technical"},
        document_id="pytorch_doc",
    )

    # Query
    results = rag_service.query(
        query_text="deep learning framework",
        top_k=1,
    )

    assert len(results) > 0
    assert "PyTorch" in results[0]["content"]


# tests/test_event_bus.py
import pytest
from src.events.event_bus import EventBus
from src.events.schemas import BaseEvent, EventMetadata, EventType


@pytest.fixture
def event_bus():
    """Fixture para event bus."""
    bus = EventBus("amqp://admin:admin123@localhost:5672/")
    bus.connect()
    yield bus
    bus.disconnect()


def test_publish_event(event_bus):
    """Test publicación de eventos."""
    event = BaseEvent(
        metadata=EventMetadata(
            event_type=EventType.DATA_INGESTED,
            source_service="test",
        ),
        payload={"test": "data"},
    )

    result = event_bus.publish(event)
    assert result is True


def test_subscribe_event(event_bus):
    """Test suscripción a eventos."""
    received_events = []

    def callback(event: BaseEvent):
        received_events.append(event)

    event_bus.subscribe(
        queue_name="test_queue",
        routing_keys=["test.*"],
        callback=callback,
    )

    # Publicar evento
    event = BaseEvent(
        metadata=EventMetadata(
            event_type="test.event",
            source_service="test",
        ),
        payload={"test": "data"},
    )
    event_bus.publish(event, routing_key="test.event")

    # Verificar (requiere consumo asíncrono)
    # Este test requiere más setup para consumo real
```

### 6.2 Monitoring con Prometheus + Grafana

```yaml
# config/grafana/dashboards/mlops_dashboard.json
{
  "dashboard": {
    "title": "MLOps Platform Monitoring",
    "panels": [
      {
        "title": "Training Jobs",
        "targets": [
          {
            "expr": "training_started_total",
            "legendFormat": "Started"
          },
          {
            "expr": "training_completed_total",
            "legendFormat": "Completed ({{status}})"
          }
        ]
      },
      {
        "title": "RAG Query Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(rag_query_duration_seconds_bucket[5m]))",
            "legendFormat": "P95"
          }
        ]
      },
      {
        "title": "Model Inference Latency",
        "targets": [
          {
            "expr": "histogram_quantile(0.99, rate(inference_duration_seconds_bucket[5m]))",
            "legendFormat": "P99"
          }
        ]
      }
    ]
  }
}
```

### 6.3 Deployment con Kubernetes (Opcional)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pytorch-service
  labels:
    app: pytorch-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pytorch-service
  template:
    metadata:
      labels:
        app: pytorch-service
    spec:
      containers:
      - name: pytorch-service
        image: mlops-platform/pytorch-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: RABBITMQ_URL
          valueFrom:
            secretKeyRef:
              name: mlops-secrets
              key: rabbitmq-url
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow-service:5000"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: 1
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: pytorch-service
spec:
  selector:
    app: pytorch-service
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: LoadBalancer
```

### 6.4 CI/CD Pipeline

```yaml
# .github/workflows/mlops-ci.yml
name: MLOps CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      rabbitmq:
        image: rabbitmq:3.12-management-alpine
        ports:
          - 5672:5672
          - 15672:15672
        env:
          RABBITMQ_DEFAULT_USER: admin
          RABBITMQ_DEFAULT_PASS: admin123

      redis:
        image: redis:7.2-alpine
        ports:
          - 6379:6379

      chromadb:
        image: ghcr.io/chroma-core/chroma:0.4.22
        ports:
          - 8000:8000

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-asyncio

    - name: Run tests
      env:
        RABBITMQ_URL: amqp://admin:admin123@localhost:5672/
        REDIS_URL: redis://localhost:6379/0
        CHROMA_HOST: localhost
        CHROMA_PORT: 8000
      run: |
        pytest tests/ -v --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Build and push PyTorch service
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile.pytorch
        push: true
        tags: |
          mlops-platform/pytorch-service:latest
          mlops-platform/pytorch-service:${{ github.sha }}

    - name: Build and push TensorFlow service
      uses: docker/build-push-action@v4
      with:
        context: .
        file: ./Dockerfile.tensorflow
        push: true
        tags: |
          mlops-platform/tensorflow-service:latest
          mlops-platform/tensorflow-service:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/
        kubectl rollout status deployment/pytorch-service
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- **PyTorch**: https://pytorch.org/docs/
- **TensorFlow**: https://www.tensorflow.org/guide
- **LangChain**: https://python.langchain.com/docs/
- **ChromaDB**: https://docs.trychroma.com/
- **MLflow**: https://mlflow.org/docs/latest/index.html
- **RabbitMQ**: https://www.rabbitmq.com/documentation.html

### Libros Recomendados

1. **"Designing Machine Learning Systems"** - Chip Huyen
2. **"Building Machine Learning Powered Applications"** - Emmanuel Ameisen
3. **"Machine Learning Design Patterns"** - Lakshmanan, Robinson, Munn

### Cursos Online

- **MLOps Specialization** (DeepLearning.AI)
- **Full Stack Deep Learning** (UC Berkeley)
- **Practical Deep Learning** (fast.ai)

---

## 🎯 Ejercicios Prácticos

### Ejercicio 1: Implementar Data Drift Detection

Añade un servicio que detecte drift en los datos de entrada:

```python
# TODO: Implementar servicio de drift detection
# - Monitorear distribuciones de features
# - Comparar con baseline
# - Publicar eventos drift.detected
```

### Ejercicio 2: A/B Testing de Modelos

Implementa sistema para comparar dos versiones de modelo en producción:

```python
# TODO: Implementar A/B testing
# - Router de tráfico
# - Métricas por versión
# - Statistical significance testing
```

### Ejercicio 3: RAG con Multi-Query

Mejora el RAG para generar múltiples queries y fusionar resultados:

```python
# TODO: Multi-query RAG
# - Generar variaciones de query
# - Fusionar resultados (MMR, reciprocal rank fusion)
# - Re-ranking
```

---

## 🚀 Siguiente Nivel

### Temas Avanzados

1. **Feature Stores** (Feast, Tecton)
2. **Model Registry** (MLflow, DVC)
3. **Online Learning** y continuous training
4. **Federated Learning**
5. **Model Compression** (quantization, pruning, distillation)
6. **Explainability** (SHAP, LIME, integrated gradients)
7. **Multi-Modal Models** (CLIP, Flamingo)
8. **LLM Fine-tuning** (LoRA, QLoRA, PEFT)

---

## 📞 Soporte y Comunidad

¿Preguntas? ¿Problemas?

- **GitHub Issues**: Para bugs y features
- **Discord**: Comunidad de MLOps
- **Stack Overflow**: Tag `mlops`, `pytorch`, `tensorflow`

---

**¡Happy MLOps! 🚀🤖**
