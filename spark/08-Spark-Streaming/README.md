# ⚡ Módulo 08: Spark Structured Streaming - Procesamiento en Tiempo Real

Aprende a procesar streams de datos en tiempo real con Apache Spark Structured Streaming, la API de streaming moderna de Spark que unifica batch y streaming.

## 🎯 Objetivos de Aprendizaje

- Entender los conceptos de Spark Structured Streaming
- Procesar datos en tiempo real desde múltiples fuentes (Kafka, sockets, archivos)
- Implementar agregaciones y ventanas temporales (windowing)
- Integrar ML en tiempo real para scoring de leads
- Manejar watermarks y late data
- Escribir resultados a diferentes sinks (consola, Parquet, Kafka, PostgreSQL)
- Implementar arquitecturas Lambda y Kappa

## 📚 ¿Qué es Structured Streaming?

**Structured Streaming** es el motor de procesamiento de streams de Spark construido sobre Spark SQL. Trata los streams como **tablas infinitas** donde continuamente llegan nuevas filas.

### Ventajas vs Spark Streaming (DStreams - Legacy):

| Característica | Structured Streaming | DStreams (Legacy) |
|---------------|---------------------|------------------|
| **API** | DataFrame/Dataset API | RDD API |
| **Modelo** | Tabla infinita | Micro-batches discretos |
| **Optimización** | Catalyst Optimizer | Manual |
| **Event Time** | Nativo | Complicado |
| **Late Data** | Watermarks automáticos | Manual |
| **SQL Support** | Sí | No |
| **Recomendado** | ✅ Sí | ❌ Deprecated |

## 🔑 Conceptos Clave

### 1. Input Sources (Fuentes de Datos)

```python
# Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "leads-events") \
    .load()

# Socket (testing)
df = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Archivos (File source)
df = spark.readStream \
    .format("json") \
    .schema(schema) \
    .load("data/incoming/")
```

### 2. Transformaciones

Las mismas transformaciones que usas en batch funcionan en streaming:

```python
# Filtros
filtered = stream_df.filter(col("action") == "purchase")

# Agregaciones
agg = stream_df.groupBy("user_id").count()

# Joins con datos estáticos (enrichment)
enriched = stream_df.join(user_profiles, "user_id")
```

### 3. Windowing (Ventanas Temporales)

Agrupa eventos por tiempo:

```python
from pyspark.sql.functions import window

# Conteo de eventos por ventana de 5 minutos
windowed = stream_df \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("user_id")
    ) \
    .count()
```

### 4. Watermarks (Manejo de Datos Tardíos)

Permite desechar datos muy antiguos:

```python
# Acepta datos con hasta 10 minutos de retraso
df_with_watermark = stream_df \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(window(col("timestamp"), "5 minutes")) \
    .count()
```

### 5. Output Modes

- **Append**: Solo nuevas filas (default para la mayoría)
- **Complete**: Toda la tabla resultado (solo agregaciones)
- **Update**: Solo filas actualizadas

### 6. Output Sinks

```python
# Console (debugging)
query = stream_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

# Parquet (data lake)
query = stream_df.writeStream \
    .format("parquet") \
    .option("path", "data/output/") \
    .option("checkpointLocation", "data/checkpoint/") \
    .start()

# Kafka (downstream processing)
query = stream_df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "processed-events") \
    .start()

# ForeachBatch (custom logic)
def process_batch(batch_df, batch_id):
    # Custom processing
    batch_df.write.jdbc(...)

query = stream_df.writeStream \
    .foreachBatch(process_batch) \
    .start()
```

## 🛠️ Scripts Incluidos

### 1. `kafka_producer.py` - Generador de Eventos

Simula eventos de leads en tiempo real y los envía a Kafka:

```bash
python 08-Spark-Streaming/kafka_producer.py
```

**Eventos generados:**
- Web visits
- Form submissions
- Email clicks
- Purchases

### 2. `streaming_word_count.py` - Ejemplo Básico

El "Hello World" de streaming - conteo de palabras en tiempo real:

```bash
# Terminal 1: Enviar datos
nc -lk 9999

# Terminal 2: Procesar stream
python 08-Spark-Streaming/streaming_word_count.py
```

### 3. `streaming_aggregations.py` - Agregaciones en Tiempo Real

Demuestra agregaciones avanzadas con ventanas temporales:

```bash
python 08-Spark-Streaming/streaming_aggregations.py
```

**Características:**
- Conteo de eventos por ventana de 1 minuto
- Suma acumulativa por usuario
- Detección de anomalías en tiempo real

### 4. `streaming_ml_scoring.py` - ML en Tiempo Real

**El más importante**: Scoring de leads en tiempo real con modelo entrenado:

```bash
python 08-Spark-Streaming/streaming_ml_scoring.py
```

**Flujo:**
1. Lee eventos de leads desde Kafka
2. Enriquece con datos de PostgreSQL
3. Aplica modelo ML (MLflow) para scoring
4. Escribe hot leads a Kafka/PostgreSQL
5. Guarda métricas en tiempo real

### 5. `streaming_kafka_to_kafka.py` - Pipeline Kafka

Procesamiento Kafka → Transformación → Kafka:

```bash
python 08-Spark-Streaming/streaming_kafka_to_kafka.py
```

### 6. `streaming_file_monitor.py` - File Streaming

Monitorea un directorio y procesa archivos nuevos automáticamente:

```bash
python 08-Spark-Streaming/streaming_file_monitor.py
```

## 📖 Ejemplos Paso a Paso

### Ejemplo 1: Socket Stream Básico

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

spark = SparkSession.builder \
    .appName("BasicStreaming") \
    .getOrCreate()

# Leer desde socket
lines = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Dividir en palabras
words = lines.select(
    explode(split(lines.value, " ")).alias("word")
)

# Contar palabras
word_counts = words.groupBy("word").count()

# Escribir a consola
query = word_counts.writeStream \
    .format("console") \
    .outputMode("complete") \
    .start()

query.awaitTermination()
```

### Ejemplo 2: Agregación con Ventanas

```python
from pyspark.sql.functions import window, col

# Stream de eventos (JSON)
events = spark.readStream \
    .format("json") \
    .schema(schema) \
    .load("data/events/")

# Agregar por ventana de 5 minutos
windowed_counts = events \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),  # Ventana deslizante
        col("event_type")
    ) \
    .count()

# Guardar en Parquet
query = windowed_counts.writeStream \
    .format("parquet") \
    .option("path", "data/windowed_events/") \
    .option("checkpointLocation", "data/checkpoint/") \
    .outputMode("append") \
    .start()
```

### Ejemplo 3: Stream Join con Tabla Estática (Enrichment)

```python
# Cargar datos estáticos (user profiles)
user_profiles = spark.read \
    .format("parquet") \
    .load("data/user_profiles.parquet")

# Stream de eventos
events = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "events") \
    .load()

# Parse JSON
from pyspark.sql.functions import from_json

events_parsed = events.select(
    from_json(col("value").cast("string"), event_schema).alias("data")
).select("data.*")

# Enriquecer con datos estáticos
enriched = events_parsed.join(user_profiles, "user_id")

# Escribir resultado
query = enriched.writeStream \
    .format("console") \
    .start()
```

### Ejemplo 4: ML Scoring en Tiempo Real

```python
import mlflow

# Cargar modelo
model_uri = "models:/lead_scoring_production/latest"
model = mlflow.spark.load_model(model_uri)

# Stream de leads
leads_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "new-leads") \
    .load()

# Parse y preparar features
leads_prepared = leads_stream.select(
    from_json(col("value").cast("string"), lead_schema).alias("lead")
).select("lead.*")

# Aplicar modelo (en foreachBatch para usar ML)
def score_batch(batch_df, batch_id):
    if not batch_df.isEmpty():
        # Aplicar modelo
        predictions = model.transform(batch_df)

        # Filtrar solo hot leads (prob > 0.7)
        hot_leads = predictions.filter(col("probability")[1] > 0.7)

        # Guardar hot leads
        hot_leads.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/spark_db") \
            .option("dbtable", "hot_leads_realtime") \
            .mode("append") \
            .save()

query = leads_prepared.writeStream \
    .foreachBatch(score_batch) \
    .start()

query.awaitTermination()
```

## 🏗️ Arquitecturas de Streaming

### Arquitectura Lambda

Combina batch y streaming para mejor precisión:

```
Eventos → [Kafka] → ┬→ Speed Layer (Streaming) → Views en tiempo real
                     └→ Batch Layer (Spark Batch) → Views históricas
```

### Arquitectura Kappa (Recomendada)

Solo streaming, más simple:

```
Eventos → [Kafka] → Spark Streaming → ┬→ Storage (Parquet/Delta)
                                       └→ Serving Layer (FastAPI)
```

## 💡 Mejores Prácticas

### 1. Checkpointing

**Siempre** usa checkpoints para recuperación ante fallos:

```python
.option("checkpointLocation", "s3://my-bucket/checkpoints/app1/")
```

### 2. Trigger Intervals

Controla la frecuencia de micro-batches:

```python
# Procesar cada 30 segundos
.trigger(processingTime='30 seconds')

# Procesar tan rápido como sea posible
.trigger(continuous='1 second')  # Experimental

# Una sola vez (testing)
.trigger(once=True)
```

### 3. Watermarks para Agregaciones

```python
# Espera hasta 10 minutos de datos tardíos
.withWatermark("event_time", "10 minutes")
```

### 4. Manejo de Esquemas

No uses `inferSchema` en streaming - define explícitamente:

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("user_id", IntegerType(), False),
    StructField("event_type", StringType(), False),
    StructField("timestamp", TimestampType(), False)
])
```

### 5. Monitoreo

```python
# Acceder a métricas
query.lastProgress  # Último batch
query.status        # Estado actual
query.recentProgress  # Últimos batches
```

## 🚨 Casos de Uso Reales

1. **Fraud Detection**: Detectar transacciones fraudulentas en tiempo real
2. **IoT Analytics**: Procesar telemetría de sensores
3. **Real-time Recommendations**: Actualizar recomendaciones basadas en comportamiento actual
4. **Log Aggregation**: Agregar y analizar logs de aplicaciones
5. **Lead Scoring en Tiempo Real**: Priorizar leads calientes inmediatamente
6. **Alertas y Notificaciones**: Disparar alertas basadas en patrones

## 🔗 Integración con Kafka

### Setup rápido con Docker:

```bash
# Kafka + Zookeeper
docker run -d --name zookeeper -p 2181:2181 zookeeper:3.7
docker run -d --name kafka -p 9092:9092 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  wurstmeister/kafka
```

### Crear topic:

```bash
kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --topic leads-events \
  --partitions 3 \
  --replication-factor 1
```

## 📊 Comparación: Batch vs Streaming

| Aspecto | Batch | Streaming |
|---------|-------|-----------|
| **Latencia** | Minutos - Horas | Segundos - Subsegundos |
| **Volumen** | Todo el dataset | Eventos incrementales |
| **Complejidad** | Menor | Mayor |
| **Costo** | Procesa 1 vez | Procesa continuamente |
| **Uso** | Análisis históricos | Decisiones en tiempo real |

## 🚀 Próximos Pasos

Después de dominar streaming:
1. **[Módulo 05: Airflow](../05-Airflow/README.md)** - Orquesta jobs batch y streaming
2. **[Módulo 06: S3/MinIO](../06-Storage-S3-MinIO/README.md)** - Almacena streams en Data Lake
3. **[Módulo 07: Docker/K8s](../07-Docker-K8s/README.md)** - Deploy streaming apps en K8s

## 📚 Referencias

- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Structured Streaming + Kafka Integration](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
- [Event Time vs Processing Time](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/)
- [Watermarks and Late Data](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#handling-late-data-and-watermarking)
