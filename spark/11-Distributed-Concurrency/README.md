# ⚡ Módulo 11: Aplicaciones Distribuidas Concurrentes + Spark

Domina patrones avanzados de **computación distribuida y concurrente** integrando Spark con frameworks modernos como Ray, Celery, Redis y Kafka para construir sistemas de ML y Big Data de alta performance.

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Entender los fundamentos de computación distribuida y concurrente
- ✅ Aplicar patrones de diseño para sistemas distribuidos
- ✅ Integrar Spark con Ray para ML distribuido avanzado
- ✅ Usar Celery para task queues con Spark jobs
- ✅ Implementar caching distribuido con Redis + Spark
- ✅ Diseñar arquitecturas event-driven con Kafka + Spark
- ✅ Ejecutar hyperparameter tuning distribuido a gran escala
- ✅ Construir feature stores distribuidos
- ✅ Manejar coordinación con Zookeeper/etcd
- ✅ Optimizar performance con paralelismo multinivel

---

## 📚 Fundamentos Teóricos

### Concurrencia vs Paralelismo vs Distribución

```
CONCURRENCIA                PARALELISMO                 DISTRIBUCIÓN
═══════════════════════════════════════════════════════════════════════
Múltiples tareas           Múltiples tareas            Múltiples nodos
progresando                ejecutándose                procesando datos
simultáneamente            realmente al mismo          en red
                          tiempo

1 CPU, time-slicing        Múltiples CPUs              Múltiples máquinas
Thread 1 → Thread 2        Core 1 | Core 2            Node A | Node B | Node C
      ↓         ↓              ↓         ↓                ↓       ↓       ↓
Context switching          True parallelism          Network communication

Ejemplo:                   Ejemplo:                    Ejemplo:
Async I/O                  Multi-core processing       Spark cluster
Event loops                GPU computing               MapReduce
Coroutines                 SIMD operations             Distributed cache
```

**Definiciones:**

| Concepto | Definición | Ejemplo con Spark |
|----------|-----------|-------------------|
| **Concurrencia** | Gestión de múltiples tareas que progresan en overlapping time periods | Driver ejecuta múltiples stages |
| **Paralelismo** | Ejecución simultánea de múltiples operaciones | Múltiples executors procesando particiones |
| **Distribución** | Cómputo en múltiples nodos conectados por red | Cluster Spark procesando TBs de datos |

---

### El Teorema CAP

En sistemas distribuidos, solo puedes garantizar 2 de estas 3 propiedades:

```
         Consistency
              ▲
             /│\
            / │ \
           /  │  \
          /   │   \
         / CA │ CP \
        /     │     \
       /      │      \
      /       │       \
     /________|________\
 Availability      Partition Tolerance
            \     │     /
             \ AP │   /
              \   │  /
               \  │ /
                \ |/
```

**CA (Consistency + Availability)**: Sistemas monolíticos (PostgreSQL single-node)
**CP (Consistency + Partition Tolerance)**: HBase, MongoDB, etcd
**AP (Availability + Partition Tolerance)**: Cassandra, DynamoDB, Redis Cluster

**Spark**: Típicamente CP con eventual consistency para metadata

---

### Patrones de Computación Distribuida

#### 1. Map-Reduce Pattern

```python
# Spark implementa Map-Reduce nativamente
rdd = sc.parallelize(range(1, 1000000))

# Map: Transformar cada elemento
mapped = rdd.map(lambda x: (x % 10, x))

# Reduce: Agregar por clave
result = mapped.reduceByKey(lambda a, b: a + b)

print(result.collect())
```

**Cuándo usar:**
- ✅ Agregaciones masivas
- ✅ ETL distribuido
- ✅ Joins de grandes datasets

#### 2. Scatter-Gather Pattern

```python
from concurrent.futures import ThreadPoolExecutor
from pyspark.sql import SparkSession

def scatter_gather_spark(spark, data_sources):
    """
    Scatter: Distribuir queries a múltiples fuentes
    Gather: Recolectar y combinar resultados
    """

    def read_source(source):
        return spark.read.parquet(source)

    # Scatter: Lanzar lecturas en paralelo
    with ThreadPoolExecutor(max_workers=len(data_sources)) as executor:
        futures = [executor.submit(read_source, src) for src in data_sources]
        dfs = [f.result() for f in futures]

    # Gather: Combinar todos los DataFrames
    from functools import reduce
    combined = reduce(lambda df1, df2: df1.union(df2), dfs)

    return combined

sources = [
    "s3://bucket/data/2024-01/",
    "s3://bucket/data/2024-02/",
    "s3://bucket/data/2024-03/"
]

result = scatter_gather_spark(spark, sources)
```

**Cuándo usar:**
- ✅ Consultas a múltiples databases/APIs
- ✅ Feature engineering desde múltiples fuentes
- ✅ Ensemble models (entrenar múltiples modelos en paralelo)

#### 3. Pipeline Pattern

```python
from pyspark.sql.functions import col, when

def pipeline_processing(df):
    """
    Pipeline de transformaciones donde cada stage
    depende del anterior
    """

    # Stage 1: Limpieza
    stage1 = df.filter(col("age").between(18, 100)) \
               .dropna(subset=["email"])

    # Stage 2: Feature engineering
    stage2 = stage1.withColumn(
        "age_group",
        when(col("age") < 30, "young")
        .when(col("age") < 50, "middle")
        .otherwise("senior")
    )

    # Stage 3: Agregaciones
    stage3 = stage2.groupBy("age_group").agg(
        {"salary": "avg", "age": "count"}
    )

    return stage3

result = pipeline_processing(df)
```

**Cuándo usar:**
- ✅ ETL con múltiples transformaciones
- ✅ ML pipelines (preprocessing → training → evaluation)
- ✅ Data quality checks en cascada

#### 4. Fork-Join Pattern

```python
def fork_join_pattern(spark, df):
    """
    Fork: Dividir procesamiento en ramas paralelas
    Join: Combinar resultados
    """

    # Fork: Procesar diferentes aspectos en paralelo
    # Rama 1: Métricas de engagement
    engagement = df.groupBy("user_id").agg(
        {"page_views": "sum", "time_spent": "avg"}
    )

    # Rama 2: Métricas de conversión
    conversion = df.groupBy("user_id").agg(
        {"purchases": "sum", "revenue": "sum"}
    )

    # Rama 3: Métricas de retención
    retention = df.groupBy("user_id").agg(
        {"days_active": "countDistinct"}
    )

    # Join: Combinar todas las métricas
    result = engagement.join(conversion, "user_id") \
                      .join(retention, "user_id")

    return result
```

**Cuándo usar:**
- ✅ Cálculo de múltiples métricas independientes
- ✅ A/B testing con múltiples variantes
- ✅ Multi-model inference

---

## 🚀 Integración 1: Spark + Ray

**Ray** es un framework para computación distribuida que complementa perfectamente a Spark para ML avanzado.

### ¿Qué es Ray?

```
Spark                           Ray
═══════════════════════════════════════════════════════
Batch processing               Any Python workload
Structured data (DataFrames)   Arbitrary Python objects
Coarse-grained parallelism     Fine-grained parallelism
Disk-based shuffle             In-memory object store
```

**Casos de uso Ray + Spark:**
- Hyperparameter tuning distribuido
- Reinforcement Learning con datos de Spark
- Distributed inference de modelos complejos
- Distributed feature engineering

### Instalación

```bash
pip install ray[default] ray[tune] ray[train] pyspark
```

### Ejemplo: Hyperparameter Tuning Distribuido

```python
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import ray
from ray import tune
from ray.tune.search.optuna import OptunaSearch
import mlflow

# Inicializar Ray y Spark
ray.init(num_cpus=8)
spark = SparkSession.builder.appName("RaySpark").getOrCreate()

# Leer datos con Spark
df = spark.read.parquet("s3://datalake/silver/leads/")

# Convertir a Ray Dataset para procesamiento distribuido
ray_dataset = ray.data.from_spark(df)

def train_model(config):
    """
    Función de entrenamiento que Ray ejecutará
    en múltiples workers con diferentes hyperparams
    """

    # Obtener datos desde Ray Dataset
    train_data = ray_dataset.train_test_split(test_size=0.2)[0]

    # Convertir de vuelta a Spark para usar MLlib
    spark_df = train_data.to_spark(spark)

    # Preparar features
    assembler = VectorAssembler(
        inputCols=["age", "salary", "web_visits"],
        outputCol="features"
    )
    data = assembler.transform(spark_df)

    # Entrenar modelo con hyperparams de config
    rf = RandomForestClassifier(
        featuresCol="features",
        labelCol="conversion",
        numTrees=config["num_trees"],
        maxDepth=config["max_depth"],
        minInstancesPerNode=config["min_instances_per_node"],
    )

    model = rf.fit(data)

    # Evaluar
    predictions = model.transform(data)
    evaluator = BinaryClassificationEvaluator(
        labelCol="conversion",
        metricName="areaUnderROC"
    )
    auc = evaluator.evaluate(predictions)

    # Log a MLflow
    with mlflow.start_run(nested=True):
        mlflow.log_params(config)
        mlflow.log_metric("auc", auc)

    # Reportar a Ray Tune
    tune.report(auc=auc)

# Definir espacio de búsqueda
search_space = {
    "num_trees": tune.randint(50, 500),
    "max_depth": tune.randint(5, 30),
    "min_instances_per_node": tune.randint(1, 20),
}

# Configurar búsqueda con Optuna
search_algo = OptunaSearch()

# Ejecutar tuning distribuido
analysis = tune.run(
    train_model,
    config=search_space,
    search_alg=search_algo,
    num_samples=100,  # 100 configuraciones diferentes
    resources_per_trial={"cpu": 2},  # 4 trials en paralelo con 8 CPUs
    metric="auc",
    mode="max",
    name="spark_ray_tuning"
)

# Obtener mejor configuración
best_config = analysis.get_best_config(metric="auc", mode="max")
print(f"Best hyperparameters: {best_config}")

ray.shutdown()
spark.stop()
```

### Ray Train + Spark: Distributed Training

```python
from ray.train.torch import TorchTrainer
from ray.train import ScalingConfig
import torch
import torch.nn as nn

def train_func_distributed(config):
    """
    Función de entrenamiento distribuida que Ray ejecuta
    en múltiples GPUs/workers
    """

    # Obtener datos de Spark via Ray
    train_dataset = ray.train.get_dataset_shard("train")

    # Convertir a PyTorch
    torch_dataset = train_dataset.to_torch(
        label_column="label",
        feature_columns=["feature_1", "feature_2", "feature_3"]
    )

    # Modelo
    model = nn.Sequential(
        nn.Linear(3, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 1),
        nn.Sigmoid()
    )

    # Configurar para distributed training
    model = ray.train.torch.prepare_model(model)

    optimizer = torch.optim.Adam(model.parameters(), lr=config["lr"])
    criterion = nn.BCELoss()

    # Training loop
    for epoch in range(config["epochs"]):
        for batch in torch_dataset:
            optimizer.zero_grad()
            outputs = model(batch["features"])
            loss = criterion(outputs, batch["labels"])
            loss.backward()
            optimizer.step()

        # Report metrics
        ray.train.report({"loss": loss.item(), "epoch": epoch})

# Leer datos con Spark
spark_df = spark.read.parquet("s3://datalake/training_data/")

# Convertir a Ray Dataset
ray_dataset = ray.data.from_spark(spark_df)
train_ds, val_ds = ray_dataset.train_test_split(test_size=0.2)

# Configurar trainer distribuido
trainer = TorchTrainer(
    train_func_distributed,
    train_loop_config={"lr": 0.001, "epochs": 10},
    scaling_config=ScalingConfig(
        num_workers=4,  # 4 workers distribuidos
        use_gpu=True,
        resources_per_worker={"CPU": 2, "GPU": 1}
    ),
    datasets={"train": train_ds, "val": val_ds}
)

# Ejecutar entrenamiento distribuido
result = trainer.fit()
print(f"Final metrics: {result.metrics}")
```

---

## 🔄 Integración 2: Spark + Celery

**Celery** es un sistema de task queue distribuido para ejecutar trabajos asíncronos.

### Arquitectura Spark + Celery

```
┌─────────────────────────────────────────────────────┐
│                 Application Layer                    │
│  ┌──────────────┐         ┌──────────────┐         │
│  │   FastAPI    │────────►│    Celery    │         │
│  │   Endpoint   │         │    Worker    │         │
│  └──────────────┘         └──────┬───────┘         │
│                                   │                  │
│                                   │ Submit Job       │
│                                   ▼                  │
│                          ┌──────────────┐           │
│                          │    Spark     │           │
│                          │   Cluster    │           │
│                          └──────────────┘           │
│                                                       │
│  Message Broker: RabbitMQ / Redis                   │
│  Result Backend: Redis / PostgreSQL                 │
└─────────────────────────────────────────────────────┘
```

### Configuración

```bash
pip install celery redis
```

**celery_config.py:**
```python
from celery import Celery
from pyspark.sql import SparkSession

# Configurar Celery
celery_app = Celery(
    'spark_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hora max
    worker_prefetch_multiplier=1,
)

def get_spark_session():
    """
    Crear sesión Spark que será usada por tasks Celery
    """
    return SparkSession.builder \
        .appName("CelerySpark") \
        .config("spark.executor.memory", "4g") \
        .config("spark.executor.cores", "2") \
        .getOrCreate()
```

### Ejemplo: Spark Jobs Asíncronos

```python
from celery_config import celery_app, get_spark_session
from pyspark.sql.functions import col, avg, count
import mlflow

@celery_app.task(bind=True, name='spark.train_model')
def train_model_async(self, input_path, output_path, model_type='gbt'):
    """
    Task Celery que ejecuta entrenamiento Spark de forma asíncrona
    """

    # Actualizar estado
    self.update_state(state='PROGRESS', meta={'status': 'Initializing Spark'})

    spark = get_spark_session()

    try:
        # Leer datos
        self.update_state(state='PROGRESS', meta={'status': 'Loading data'})
        df = spark.read.parquet(input_path)

        # Preparar features
        self.update_state(state='PROGRESS', meta={'status': 'Feature engineering'})
        from pyspark.ml.feature import VectorAssembler, StringIndexer

        assembler = VectorAssembler(
            inputCols=["age", "salary", "web_visits"],
            outputCol="features"
        )
        data = assembler.transform(df)

        # Entrenar
        self.update_state(state='PROGRESS', meta={'status': 'Training model'})

        if model_type == 'gbt':
            from pyspark.ml.classification import GBTClassifier
            model = GBTClassifier(
                featuresCol="features",
                labelCol="conversion",
                maxIter=50
            )
        else:
            from pyspark.ml.classification import RandomForestClassifier
            model = RandomForestClassifier(
                featuresCol="features",
                labelCol="conversion",
                numTrees=100
            )

        trained_model = model.fit(data)

        # Guardar
        self.update_state(state='PROGRESS', meta={'status': 'Saving model'})
        trained_model.write().overwrite().save(output_path)

        # Log a MLflow
        with mlflow.start_run():
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("input_path", input_path)
            mlflow.spark.log_model(trained_model, "model")

        return {
            'status': 'SUCCESS',
            'model_path': output_path,
            'model_type': model_type
        }

    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise

    finally:
        spark.stop()

@celery_app.task(name='spark.batch_inference')
def batch_inference_async(model_path, input_path, output_path):
    """
    Inferencia batch asíncrona con Spark
    """
    spark = get_spark_session()

    try:
        # Cargar modelo
        from pyspark.ml.classification import GBTClassificationModel
        model = GBTClassificationModel.load(model_path)

        # Leer datos
        df = spark.read.parquet(input_path)

        # Preparar features
        from pyspark.ml.feature import VectorAssembler
        assembler = VectorAssembler(
            inputCols=["age", "salary", "web_visits"],
            outputCol="features"
        )
        data = assembler.transform(df)

        # Predecir
        predictions = model.transform(data)

        # Guardar
        predictions.select("lead_id", "prediction", "probability") \
                   .write.mode("overwrite") \
                   .parquet(output_path)

        return {
            'status': 'SUCCESS',
            'output_path': output_path,
            'count': predictions.count()
        }

    finally:
        spark.stop()

@celery_app.task(name='spark.data_quality_check')
def data_quality_check_async(input_path):
    """
    Chequeo de calidad de datos distribuido
    """
    spark = get_spark_session()

    try:
        df = spark.read.parquet(input_path)

        # Calcular métricas de calidad
        total_count = df.count()
        null_counts = df.select([
            count(col(c)).alias(c) for c in df.columns
        ]).collect()[0].asDict()

        # Detectar duplicados
        duplicate_count = df.count() - df.dropDuplicates().count()

        # Outliers (ejemplo simple)
        from pyspark.sql.functions import stddev, mean
        numeric_cols = ["age", "salary", "web_visits"]

        outliers = {}
        for col_name in numeric_cols:
            stats = df.select(
                mean(col(col_name)).alias("mean"),
                stddev(col(col_name)).alias("stddev")
            ).collect()[0]

            outlier_count = df.filter(
                (col(col_name) > stats["mean"] + 3 * stats["stddev"]) |
                (col(col_name) < stats["mean"] - 3 * stats["stddev"])
            ).count()

            outliers[col_name] = outlier_count

        return {
            'status': 'SUCCESS',
            'total_rows': total_count,
            'null_counts': null_counts,
            'duplicate_count': duplicate_count,
            'outliers': outliers,
            'quality_score': 1.0 - (duplicate_count / total_count)
        }

    finally:
        spark.stop()
```

### FastAPI + Celery + Spark

```python
from fastapi import FastAPI, BackgroundTasks, HTTPException
from celery.result import AsyncResult
from celery_config import celery_app
from pydantic import BaseModel

app = FastAPI(title="Spark ML API with Celery")

class TrainingRequest(BaseModel):
    input_path: str
    output_path: str
    model_type: str = "gbt"

class InferenceRequest(BaseModel):
    model_path: str
    input_path: str
    output_path: str

@app.post("/train")
def submit_training_job(request: TrainingRequest):
    """
    Enviar job de entrenamiento Spark a Celery queue
    """
    task = train_model_async.delay(
        input_path=request.input_path,
        output_path=request.output_path,
        model_type=request.model_type
    )

    return {
        "task_id": task.id,
        "status": "PENDING",
        "message": "Training job submitted"
    }

@app.get("/train/{task_id}")
def get_training_status(task_id: str):
    """
    Consultar estado de job de entrenamiento
    """
    task = AsyncResult(task_id, app=celery_app)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Job is waiting in queue'
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.result
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }

    return response

@app.post("/inference")
def submit_inference_job(request: InferenceRequest):
    """
    Enviar job de inferencia batch
    """
    task = batch_inference_async.delay(
        model_path=request.model_path,
        input_path=request.input_path,
        output_path=request.output_path
    )

    return {
        "task_id": task.id,
        "status": "PENDING"
    }

@app.post("/data-quality")
def submit_quality_check(input_path: str):
    """
    Enviar chequeo de calidad de datos
    """
    task = data_quality_check_async.delay(input_path=input_path)

    return {
        "task_id": task.id,
        "status": "PENDING"
    }

@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """
    Consultar estado de cualquier task
    """
    task = AsyncResult(task_id, app=celery_app)

    return {
        "task_id": task_id,
        "state": task.state,
        "result": task.result if task.state == 'SUCCESS' else None,
        "error": str(task.info) if task.state == 'FAILURE' else None
    }

@app.get("/tasks")
def list_active_tasks():
    """
    Listar todas las tasks activas
    """
    inspect = celery_app.control.inspect()

    return {
        "active": inspect.active(),
        "scheduled": inspect.scheduled(),
        "reserved": inspect.reserved()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Iniciar Workers:**
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery worker
celery -A celery_config worker --loglevel=info --concurrency=4

# Terminal 3: FastAPI
python api.py

# Terminal 4: Probar API
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "input_path": "s3://datalake/silver/leads/",
    "output_path": "/models/gbt_model",
    "model_type": "gbt"
  }'

# Respuesta: {"task_id": "abc-123-def", "status": "PENDING"}

# Consultar estado
curl http://localhost:8000/train/abc-123-def
```

---

## 💾 Integración 3: Spark + Redis (Distributed Cache)

**Redis** como cache distribuido para optimizar lookups y compartir estado entre Spark jobs.

### Casos de Uso

1. **Feature Store**: Cache de features calculadas
2. **Model Registry**: Cache de modelos en memoria
3. **Lookup Tables**: Broadcast joins optimizados
4. **Rate Limiting**: Controlar rate de procesamiento
5. **Distributed Locks**: Coordinación entre jobs

### Ejemplo: Feature Store con Redis

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DoubleType, ArrayType
import redis
import json
import pickle
import numpy as np

class RedisFeatureStore:
    """
    Feature Store distribuido usando Redis como cache
    """

    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False  # Para almacenar bytes
        )
        self.ttl = 86400  # 24 horas

    def write_features(self, entity_id, features_dict):
        """
        Escribir features de una entidad a Redis
        """
        key = f"features:{entity_id}"
        value = json.dumps(features_dict)
        self.redis_client.setex(key, self.ttl, value)

    def read_features(self, entity_id):
        """
        Leer features de una entidad desde Redis
        """
        key = f"features:{entity_id}"
        value = self.redis_client.get(key)

        if value:
            return json.loads(value)
        return None

    def write_features_batch(self, features_df):
        """
        Escribir features en batch desde Spark DataFrame
        """
        # Convertir DataFrame a lista de diccionarios
        features_list = features_df.collect()

        # Usar pipeline para batch writes
        pipe = self.redis_client.pipeline()

        for row in features_list:
            entity_id = row['entity_id']
            features = {k: v for k, v in row.asDict().items() if k != 'entity_id'}
            key = f"features:{entity_id}"
            value = json.dumps(features)
            pipe.setex(key, self.ttl, value)

        pipe.execute()
        print(f"✅ Wrote {len(features_list)} feature sets to Redis")

    def write_model(self, model_name, model_bytes):
        """
        Escribir modelo serializado a Redis
        """
        key = f"model:{model_name}"
        self.redis_client.setex(key, self.ttl, model_bytes)

    def read_model(self, model_name):
        """
        Leer modelo desde Redis
        """
        key = f"model:{model_name}"
        return self.redis_client.get(key)

# Uso con Spark
spark = SparkSession.builder.appName("RedisFeatureStore").getOrCreate()

# Calcular features con Spark
df = spark.read.parquet("s3://datalake/raw/events/")

features_df = df.groupBy("user_id").agg({
    "page_views": "sum",
    "time_spent": "avg",
    "purchases": "count",
    "revenue": "sum"
}).withColumnRenamed("user_id", "entity_id")

# Guardar en Redis
feature_store = RedisFeatureStore()
feature_store.write_features_batch(features_df)

# Leer features desde Redis en tiempo real
user_features = feature_store.read_features(entity_id=12345)
print(user_features)
```

### Ejemplo: Distributed Lookup con Redis

```python
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, StructType, StructField
import redis

def create_redis_lookup_udf(redis_host='localhost', redis_port=6379):
    """
    Crear UDF que hace lookup en Redis
    Más eficiente que broadcast join para lookups pequeños
    """

    def lookup_in_redis(key):
        # Cada partition tiene su propia conexión Redis
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        value = r.get(f"lookup:{key}")
        return value if value else "unknown"

    return udf(lookup_in_redis, StringType())

# Usar UDF en Spark
spark = SparkSession.builder.appName("RedisLookup").getOrCreate()

df = spark.read.parquet("s3://datalake/transactions/")

# Aplicar lookup usando Redis (más rápido que join para tablas pequeñas)
redis_lookup_udf = create_redis_lookup_udf()

enriched_df = df.withColumn(
    "category_name",
    redis_lookup_udf(col("category_id"))
)

enriched_df.write.parquet("s3://datalake/transactions_enriched/")
```

### Ejemplo: Rate Limiting con Redis

```python
import redis
import time
from functools import wraps

class DistributedRateLimiter:
    """
    Rate limiter distribuido usando Redis
    Útil para controlar rate de API calls desde Spark
    """

    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    def is_allowed(self, key, max_requests, window_seconds):
        """
        Verificar si request está permitido bajo rate limit

        Args:
            key: Identificador (user_id, api_key, etc.)
            max_requests: Máximo número de requests
            window_seconds: Ventana de tiempo en segundos
        """
        current_time = time.time()
        window_start = current_time - window_seconds

        # Usar sorted set para tracking de requests
        redis_key = f"rate_limit:{key}"

        # Remover requests fuera de la ventana
        self.redis_client.zremrangebyscore(redis_key, 0, window_start)

        # Contar requests en ventana actual
        request_count = self.redis_client.zcard(redis_key)

        if request_count < max_requests:
            # Agregar request actual
            self.redis_client.zadd(redis_key, {str(current_time): current_time})
            self.redis_client.expire(redis_key, window_seconds)
            return True

        return False

# Usar en Spark UDF
def rate_limited_api_call(api_key, endpoint, payload):
    """
    API call con rate limiting distribuido
    """
    limiter = DistributedRateLimiter()

    # 100 requests por minuto
    if limiter.is_allowed(api_key, max_requests=100, window_seconds=60):
        # Hacer API call
        import requests
        response = requests.post(endpoint, json=payload)
        return response.json()
    else:
        # Rate limit excedido, esperar
        time.sleep(1)
        return rate_limited_api_call(api_key, endpoint, payload)

# Aplicar en Spark con mapPartitions para reutilizar conexión
def process_partition_with_rate_limit(partition):
    limiter = DistributedRateLimiter()

    for row in partition:
        if limiter.is_allowed(row.api_key, max_requests=100, window_seconds=60):
            # Procesar
            yield process_row(row)
        else:
            time.sleep(0.1)  # Backoff
            yield process_row(row)

df = spark.read.parquet("s3://datalake/api_requests/")
result = df.rdd.mapPartitions(process_partition_with_rate_limit).toDF()
```

---

## 🌊 Integración 4: Spark Streaming + Kafka (Event-Driven)

Arquitectura event-driven completamente asíncrona.

### Ejemplo: Real-time ML Inference Pipeline

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, struct, to_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.ml.classification import GBTClassificationModel
import redis
import json

spark = SparkSession.builder \
    .appName("RealtimeMLPipeline") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .getOrCreate()

# Schema de eventos
event_schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("timestamp", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", DoubleType(), True),
    StructField("web_visits", IntegerType(), True),
])

# Leer stream desde Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user-events") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON
parsed_df = kafka_df.select(
    from_json(col("value").cast("string"), event_schema).alias("data")
).select("data.*")

# Enriquecer con features de Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def enrich_with_redis_features(user_id):
    """
    UDF para enriquecer eventos con features de Redis
    """
    key = f"features:{user_id}"
    features_json = redis_client.get(key)

    if features_json:
        features = json.loads(features_json)
        return features.get('lifetime_value', 0.0)
    return 0.0

enrich_udf = udf(enrich_with_redis_features, DoubleType())

enriched_df = parsed_df.withColumn(
    "lifetime_value",
    enrich_udf(col("user_id"))
)

# Cargar modelo ML
model = GBTClassificationModel.load("/models/lead_scoring_model")

# Preparar features para predicción
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["age", "salary", "web_visits", "lifetime_value"],
    outputCol="features"
)

features_df = assembler.transform(enriched_df)

# Aplicar modelo en streaming
predictions_df = model.transform(features_df)

# Extraer probabilidades
predictions_with_prob = predictions_df.select(
    "event_id",
    "user_id",
    "prediction",
    col("probability")[1].alias("conversion_probability")
)

# Filtrar solo high-value predictions
hot_leads_df = predictions_with_prob.filter(
    col("conversion_probability") > 0.7
)

# Escribir resultados a múltiples sinks

# Sink 1: Kafka (para downstream consumers)
kafka_output = hot_leads_df.select(
    col("event_id").cast("string").alias("key"),
    to_json(struct("*")).alias("value")
)

query1 = kafka_output.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "hot-leads") \
    .option("checkpointLocation", "/tmp/checkpoint/kafka") \
    .start()

# Sink 2: Console (para debugging)
query2 = hot_leads_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# Sink 3: Redis (para API real-time)
def write_to_redis(batch_df, batch_id):
    """
    ForeachBatch para escribir a Redis
    """
    r = redis.Redis(host='localhost', port=6379)

    for row in batch_df.collect():
        key = f"prediction:{row.user_id}"
        value = json.dumps({
            "conversion_probability": float(row.conversion_probability),
            "timestamp": str(row.timestamp)
        })
        r.setex(key, 3600, value)  # TTL 1 hora

query3 = hot_leads_df.writeStream \
    .foreachBatch(write_to_redis) \
    .start()

# Sink 4: Parquet (para analytics)
query4 = hot_leads_df.writeStream \
    .format("parquet") \
    .option("path", "s3://datalake/streaming/hot_leads/") \
    .option("checkpointLocation", "/tmp/checkpoint/parquet") \
    .partitionBy("date") \
    .start()

# Await termination
spark.streams.awaitAnyTermination()
```

---

## 🎛️ Coordinación Distribuida con Zookeeper

**Zookeeper** para coordinación y locks distribuidos.

### Ejemplo: Distributed Lock

```python
from kazoo.client import KazooClient
from kazoo.recipe.lock import Lock
import time

class DistributedJobCoordinator:
    """
    Coordinador para evitar que múltiples Spark jobs
    procesen los mismos datos simultáneamente
    """

    def __init__(self, zk_hosts='localhost:2181'):
        self.zk = KazooClient(hosts=zk_hosts)
        self.zk.start()

    def run_exclusive_job(self, job_name, job_func, *args, **kwargs):
        """
        Ejecutar job solo si no hay otro corriendo
        """
        lock_path = f"/locks/{job_name}"
        lock = Lock(self.zk, lock_path)

        if lock.acquire(blocking=False):
            try:
                print(f"🔒 Lock acquired for {job_name}")
                result = job_func(*args, **kwargs)
                return result
            finally:
                lock.release()
                print(f"🔓 Lock released for {job_name}")
        else:
            print(f"⏰ Job {job_name} already running, skipping")
            return None

    def register_job(self, job_name, metadata):
        """
        Registrar job running en Zookeeper
        """
        path = f"/jobs/{job_name}"
        self.zk.ensure_path(path)
        self.zk.set(path, json.dumps(metadata).encode())

    def get_running_jobs(self):
        """
        Obtener lista de jobs actualmente corriendo
        """
        if self.zk.exists("/jobs"):
            return self.zk.get_children("/jobs")
        return []

    def close(self):
        self.zk.stop()

# Uso con Spark
def spark_etl_job(input_path, output_path):
    """
    Spark ETL job que debe correr exclusivamente
    """
    spark = SparkSession.builder.appName("ETL").getOrCreate()

    df = spark.read.parquet(input_path)

    # Transformaciones
    transformed = df.filter(col("age") > 18).groupBy("country").count()

    # Escribir
    transformed.write.mode("overwrite").parquet(output_path)

    spark.stop()

    return {"status": "success", "rows": transformed.count()}

# Coordinar ejecución
coordinator = DistributedJobCoordinator()

result = coordinator.run_exclusive_job(
    job_name="daily_etl",
    job_func=spark_etl_job,
    input_path="s3://bucket/raw/",
    output_path="s3://bucket/processed/"
)

coordinator.close()
```

---

## 🧪 Caso de Uso Completo: AutoML Distribuido

Sistema completo de AutoML que combina Spark + Ray + Celery + Redis + Kafka.

```python
from pyspark.sql import SparkSession
import ray
from ray import tune
from ray.tune.search.optuna import OptunaSearch
import mlflow
import redis
from celery import Celery
import json

class DistributedAutoML:
    """
    Sistema AutoML completamente distribuido
    """

    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("DistributedAutoML") \
            .getOrCreate()

        ray.init()

        self.redis_client = redis.Redis(host='localhost', port=6379)

        mlflow.set_tracking_uri("http://localhost:5000")
        mlflow.set_experiment("distributed_automl")

    def load_data_spark(self, data_path):
        """
        Cargar y preparar datos con Spark
        """
        df = self.spark.read.parquet(data_path)

        # Feature engineering distribuido
        from pyspark.ml.feature import VectorAssembler, StandardScaler

        feature_cols = ["age", "salary", "web_visits", "time_on_site"]

        assembler = VectorAssembler(
            inputCols=feature_cols,
            outputCol="features_raw"
        )

        scaler = StandardScaler(
            inputCol="features_raw",
            outputCol="features"
        )

        df_assembled = assembler.transform(df)
        scaler_model = scaler.fit(df_assembled)
        df_scaled = scaler_model.transform(df_assembled)

        # Convertir a Ray Dataset para tuning distribuido
        ray_dataset = ray.data.from_spark(df_scaled)

        return ray_dataset, scaler_model

    def train_with_config(self, config, ray_dataset):
        """
        Entrenar modelo con configuración específica
        """
        # Convertir Ray Dataset a Spark
        spark_df = ray_dataset.to_spark(self.spark)

        # Split
        train, test = spark_df.randomSplit([0.8, 0.2], seed=42)

        # Seleccionar algoritmo
        if config["algorithm"] == "gbt":
            from pyspark.ml.classification import GBTClassifier
            model = GBTClassifier(
                featuresCol="features",
                labelCol="conversion",
                maxIter=config["max_iter"],
                maxDepth=config["max_depth"],
                stepSize=config["step_size"]
            )
        elif config["algorithm"] == "rf":
            from pyspark.ml.classification import RandomForestClassifier
            model = RandomForestClassifier(
                featuresCol="features",
                labelCol="conversion",
                numTrees=config["num_trees"],
                maxDepth=config["max_depth"]
            )
        else:
            from pyspark.ml.classification import LogisticRegression
            model = LogisticRegression(
                featuresCol="features",
                labelCol="conversion",
                maxIter=config["max_iter"],
                regParam=config["reg_param"]
            )

        # Entrenar
        trained_model = model.fit(train)

        # Evaluar
        predictions = trained_model.transform(test)

        from pyspark.ml.evaluation import BinaryClassificationEvaluator
        evaluator = BinaryClassificationEvaluator(
            labelCol="conversion",
            metricName="areaUnderROC"
        )
        auc = evaluator.evaluate(predictions)

        # Log a MLflow
        with mlflow.start_run(nested=True):
            mlflow.log_params(config)
            mlflow.log_metric("auc", auc)
            mlflow.spark.log_model(trained_model, "model")

        # Cache resultado en Redis
        result_key = f"automl_result:{hash(str(config))}"
        self.redis_client.setex(
            result_key,
            3600,
            json.dumps({"config": config, "auc": auc})
        )

        return auc

    def run_automl(self, data_path, num_trials=50):
        """
        Ejecutar AutoML distribuido
        """
        # Cargar datos
        ray_dataset, scaler = self.load_data_spark(data_path)

        # Definir espacio de búsqueda
        search_space = {
            "algorithm": tune.choice(["gbt", "rf", "lr"]),
            "max_iter": tune.randint(10, 100),
            "max_depth": tune.randint(3, 20),
            "step_size": tune.loguniform(0.001, 0.1),
            "num_trees": tune.randint(50, 300),
            "reg_param": tune.loguniform(0.0001, 1.0)
        }

        # Configurar búsqueda
        search_algo = OptunaSearch()

        # Función objetivo
        def objective(config):
            auc = self.train_with_config(config, ray_dataset)
            tune.report(auc=auc)

        # Ejecutar tuning distribuido con Ray
        analysis = tune.run(
            objective,
            config=search_space,
            search_alg=search_algo,
            num_samples=num_trials,
            resources_per_trial={"cpu": 4},
            metric="auc",
            mode="max",
            verbose=1
        )

        # Obtener mejor configuración
        best_config = analysis.get_best_config(metric="auc", mode="max")
        best_auc = analysis.best_result["auc"]

        print(f"\n🏆 Best Configuration:")
        print(json.dumps(best_config, indent=2))
        print(f"Best AUC: {best_auc:.4f}")

        # Entrenar modelo final con mejor config
        final_ray_dataset, _ = self.load_data_spark(data_path)
        final_model_auc = self.train_with_config(best_config, final_ray_dataset)

        # Guardar en Redis para API serving
        self.redis_client.setex(
            "automl_best_model",
            86400,
            json.dumps({
                "config": best_config,
                "auc": final_model_auc,
                "timestamp": time.time()
            })
        )

        return best_config, final_model_auc

    def cleanup(self):
        self.spark.stop()
        ray.shutdown()

# Ejecutar AutoML
automl = DistributedAutoML()

best_config, best_auc = automl.run_automl(
    data_path="s3://datalake/silver/leads/",
    num_trials=100
)

automl.cleanup()
```

---

## 📊 Monitoring y Observabilidad

### Prometheus Metrics para Aplicaciones Distribuidas

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Métricas
spark_jobs_total = Counter(
    'spark_jobs_total',
    'Total Spark jobs executed',
    ['job_type', 'status']
)

spark_job_duration = Histogram(
    'spark_job_duration_seconds',
    'Spark job duration',
    ['job_type']
)

active_spark_executors = Gauge(
    'active_spark_executors',
    'Number of active Spark executors'
)

redis_cache_hits = Counter(
    'redis_cache_hits_total',
    'Total Redis cache hits'
)

redis_cache_misses = Counter(
    'redis_cache_misses_total',
    'Total Redis cache misses'
)

def monitored_spark_job(job_func, job_type):
    """
    Decorator para monitorear Spark jobs
    """
    def wrapper(*args, **kwargs):
        start = time.time()

        try:
            result = job_func(*args, **kwargs)
            spark_jobs_total.labels(job_type=job_type, status='success').inc()
            return result
        except Exception as e:
            spark_jobs_total.labels(job_type=job_type, status='failure').inc()
            raise
        finally:
            duration = time.time() - start
            spark_job_duration.labels(job_type=job_type).observe(duration)

    return wrapper

# Iniciar servidor de métricas
start_http_server(8001)

# Uso
@monitored_spark_job
def etl_job(input_path, output_path):
    spark = SparkSession.builder.appName("ETL").getOrCreate()
    df = spark.read.parquet(input_path)

    # Actualizar gauge de executors
    active_executors = len(spark.sparkContext._jsc.sc().getExecutorMemoryStatus())
    active_spark_executors.set(active_executors)

    transformed = df.filter(col("age") > 18)
    transformed.write.parquet(output_path)

    spark.stop()

etl_job("s3://bucket/input/", "s3://bucket/output/")
```

---

## 💡 Mejores Prácticas

### 1. Idempotencia en Sistemas Distribuidos

```python
import hashlib
import json

def make_idempotent(spark, df, output_path, partition_keys):
    """
    Escribir datos de forma idempotente usando content hashing
    """

    # Calcular hash de contenido por partición
    def compute_partition_hash(rows):
        content = json.dumps([row.asDict() for row in rows], sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    # Escribir solo si hash cambió
    from pyspark.sql.functions import spark_partition_id

    df_with_partition = df.withColumn("_partition_id", spark_partition_id())

    existing_hashes = {}
    if os.path.exists(f"{output_path}/_hashes.json"):
        with open(f"{output_path}/_hashes.json", 'r') as f:
            existing_hashes = json.load(f)

    # Filtrar particiones que cambiaron
    changed_partitions = []
    for partition_id in df_with_partition.select("_partition_id").distinct().collect():
        pid = partition_id._partition_id
        partition_data = df_with_partition.filter(col("_partition_id") == pid)
        new_hash = compute_partition_hash(partition_data.collect())

        if existing_hashes.get(str(pid)) != new_hash:
            changed_partitions.append(pid)
            existing_hashes[str(pid)] = new_hash

    # Escribir solo particiones cambiadas
    if changed_partitions:
        df_to_write = df_with_partition.filter(
            col("_partition_id").isin(changed_partitions)
        ).drop("_partition_id")

        df_to_write.write.mode("overwrite").partitionBy(partition_keys).parquet(output_path)

        # Guardar hashes
        with open(f"{output_path}/_hashes.json", 'w') as f:
            json.dump(existing_hashes, f)

        return len(changed_partitions)

    return 0
```

### 2. Circuit Breaker Pattern

```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failures detected, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """
    Circuit breaker para llamadas a servicios externos desde Spark
    """

    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Uso en Spark
def call_external_api_with_breaker(partition):
    breaker = CircuitBreaker(failure_threshold=3, timeout=30)

    for row in partition:
        try:
            result = breaker.call(external_api_call, row.data)
            yield result
        except Exception as e:
            # Log error y continuar
            yield {"error": str(e), "row": row}

df = spark.read.parquet("s3://data/")
result = df.rdd.mapPartitions(call_external_api_with_breaker).toDF()
```

### 3. Backpressure Handling

```python
from pyspark.sql.streaming import StreamingQuery

def streaming_with_backpressure(spark):
    """
    Structured Streaming con backpressure management
    """

    # Configurar backpressure
    query = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "events") \
        .option("maxOffsetsPerTrigger", 10000)  # Limitar throughput \
        .load() \
        .select(from_json(col("value").cast("string"), schema).alias("data")) \
        .select("data.*") \
        .writeStream \
        .foreachBatch(process_batch_with_backpressure) \
        .option("checkpointLocation", "/tmp/checkpoint") \
        .trigger(processingTime='10 seconds')  # Rate limiting \
        .start()

    return query

def process_batch_with_backpressure(batch_df, batch_id):
    """
    Procesar batch con control de backpressure
    """
    batch_size = batch_df.count()

    if batch_size > 50000:
        # Si batch es muy grande, procesar en sub-batches
        num_partitions = (batch_size // 10000) + 1
        batch_df = batch_df.repartition(num_partitions)

    # Procesar
    result = batch_df.filter(col("value") > 0)
    result.write.mode("append").parquet(f"s3://output/batch_{batch_id}/")
```

---

## 📚 Referencias

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Ray Documentation](https://docs.ray.io/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Redis Documentation](https://redis.io/docs/)
- [Distributed Systems Patterns](https://www.patterns.dev/posts/classic-design-patterns/)
- [CAP Theorem Explained](https://en.wikipedia.org/wiki/CAP_theorem)

---

**¡Siguiente nivel! 👉 Domina los patrones más avanzados de computación distribuida y construye sistemas ML escalables de clase mundial**
