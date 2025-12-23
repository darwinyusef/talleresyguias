# ☁️ Módulo 06: Spark + Object Storage (S3/MinIO)

Aprende a construir **Data Lakes modernos** con Spark y almacenamiento de objetos, escalando desde pruebas locales con MinIO hasta despliegues en producción con AWS S3.

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Entender los fundamentos de Object Storage vs sistemas de archivos tradicionales
- ✅ Construir Data Lakes con arquitectura Medallion (Bronze/Silver/Gold)
- ✅ Configurar Spark para integrarse con S3 y MinIO
- ✅ Implementar patrones de ingesta batch e incremental
- ✅ Optimizar performance en lectura/escritura de object storage
- ✅ Manejar particionamiento y compresión eficiente
- ✅ Diseñar pipelines de datos escalables y económicos
- ✅ Aplicar mejores prácticas de seguridad y governanza

---

## 📚 Fundamentos Teóricos

### ¿Qué es Object Storage?

**Object Storage** es un paradigma de almacenamiento donde los datos se gestionan como **objetos** (archivos completos con metadata) en lugar de bloques o archivos en un sistema jerárquico.

```
Sistemas Tradicionales          Object Storage
═══════════════════════════════════════════════════
/home/user/documents/           s3://my-bucket/
    file1.txt                      file1.txt
    folder1/                       folder1/file2.txt
        file2.txt

Jerarquía real de directorios   "Prefijos" simulados
Sistema de archivos local       Sistema distribuido
POSIX compliant                 HTTP API
```

**Características Clave:**

| Feature | Object Storage | Sistema de Archivos |
|---------|----------------|---------------------|
| **Escalabilidad** | Petabytes+ sin límites | Limitado por hardware |
| **Costo** | $0.023/GB/mes (S3) | $0.08-0.15/GB/mes (EBS) |
| **Durabilidad** | 99.999999999% (11 nines) | Depende de RAID |
| **Acceso** | HTTP REST API | Sistema de archivos local |
| **Concurrencia** | Múltiples lectores sin límite | Limitado |
| **Modificación** | Inmutable (reemplazar completo) | Modificación in-place |

---

### Object Storage en el Ecosistema Big Data

**Principales Proveedores:**

- **AWS S3** (Simple Storage Service): El estándar de facto (lanzado en 2006)
- **MinIO**: Implementación open-source compatible con S3 API
- **Google Cloud Storage**: Almacenamiento de objetos de Google
- **Azure Blob Storage**: Almacenamiento de objetos de Microsoft

**S3 API como Estándar:**

El API de S3 se ha convertido en el estándar de facto. MinIO, Wasabi, Backblaze B2, y otros implementan la misma API, permitiendo portabilidad.

```python
# El mismo código funciona con S3, MinIO, o cualquier S3-compatible
df = spark.read.parquet("s3a://bucket/path/")

# Solo cambia el endpoint
# AWS S3: s3.amazonaws.com (por defecto)
# MinIO: localhost:9000
# Wasabi: s3.wasabisys.com
```

---

## 🏗️ Arquitectura Medallion

La **Arquitectura Medallion** es un patrón de diseño de Data Lakes que organiza los datos en tres capas: Bronze, Silver y Gold.

```
Data Sources              Bronze Layer              Silver Layer              Gold Layer
════════════════         ═══════════════          ═══════════════          ═══════════════
APIs                         Raw Data                  Cleaned                 Aggregated
Databases          →     (Parquet/JSON)    →      Transformed      →        Analytics
Files                    No processing             Validated              Business Metrics
Streams                  Immutable                 Deduped                  ML Features
                         Historical                Standardized             Reports
```

### 1. Bronze Layer (Raw/Landing)

**Propósito:** Almacenar datos crudos tal como llegan de las fuentes.

```
s3://data-lake/bronze/
├── customers/
│   └── date=2024-01-15/
│       └── raw_customers.json
├── transactions/
│   └── date=2024-01-15/
│       └── raw_transactions.csv
└── logs/
    └── date=2024-01-15/
        └── application.log
```

**Características:**
- ✅ Datos sin modificar (append-only)
- ✅ Formato original o conversión básica (JSON/CSV → Parquet)
- ✅ Particionado por fecha de ingesta
- ✅ Immutable (nunca se modifica, solo se agregan nuevos archivos)

**Ejemplo:**
```python
# Ingesta simple a Bronze
raw_df = spark.read.json("s3a://landing/customers/")
raw_df.write \
    .mode("append") \
    .partitionBy("ingestion_date") \
    .parquet("s3a://datalake/bronze/customers/")
```

### 2. Silver Layer (Cleaned/Curated)

**Propósito:** Datos limpios, validados y estandarizados.

```
s3://data-lake/silver/
├── customers/
│   └── country=US/year=2024/month=01/
│       └── cleaned_customers.parquet
└── transactions/
    └── year=2024/month=01/
        └── validated_transactions.parquet
```

**Transformaciones:**
- ✅ Limpieza de datos (nulls, duplicados, outliers)
- ✅ Validación de esquemas
- ✅ Standardización de tipos de datos
- ✅ Join de datos relacionados
- ✅ Particionado por dimensiones de negocio

**Ejemplo:**
```python
# Transformación Bronze → Silver
bronze_df = spark.read.parquet("s3a://datalake/bronze/customers/")

silver_df = bronze_df \
    .dropDuplicates(["customer_id"]) \
    .filter(col("age").between(18, 100)) \
    .withColumn("email", lower(col("email"))) \
    .withColumn("signup_date", to_date(col("signup_timestamp")))

silver_df.write \
    .mode("overwrite") \
    .partitionBy("country", "year", "month") \
    .parquet("s3a://datalake/silver/customers/")
```

### 3. Gold Layer (Business/Analytics)

**Propósito:** Datos agregados y optimizados para consumo analítico.

```
s3://data-lake/gold/
├── customer_360/
│   └── customer_lifetime_value.parquet
├── daily_sales/
│   └── sales_by_region.parquet
└── ml_features/
    └── lead_scoring_features.parquet
```

**Características:**
- ✅ Agregaciones de negocio
- ✅ Métricas pre-calculadas
- ✅ Features para ML
- ✅ Optimizado para BI tools (Tableau, Power BI)
- ✅ Desnormalizado para queries rápidas

**Ejemplo:**
```python
# Transformación Silver → Gold
silver_df = spark.read.parquet("s3a://datalake/silver/transactions/")

gold_df = silver_df \
    .groupBy("customer_id", "month") \
    .agg(
        sum("amount").alias("total_spent"),
        count("*").alias("num_transactions"),
        avg("amount").alias("avg_transaction_value")
    )

gold_df.write \
    .mode("overwrite") \
    .parquet("s3a://datalake/gold/customer_spending/")
```

---

## 🔧 Configuración de Spark con S3/MinIO

### Dependencias Necesarias

Para que Spark se conecte a S3, necesitas las librerías de Hadoop:

```bash
# Versiones compatibles con Spark 3.4
spark-submit \
  --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
  spark_s3_integration.py
```

**Si usas pip:**
```bash
pip install pyspark==3.4.0
```

Las JARs se descargan automáticamente la primera vez.

### Configuración para AWS S3

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Spark-S3-Production") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .getOrCreate()

# Leer datos desde S3
df = spark.read.parquet("s3a://my-bucket/data/")
```

**Autenticación en AWS:**

1. **IAM Roles (Recomendado en Producción):**
   - Asigna rol de IAM a instancias EC2 o pods de Kubernetes
   - No requiere credenciales hardcodeadas
   - Mejor seguridad y rotación automática

2. **AWS CLI Credentials:**
   ```bash
   # ~/.aws/credentials
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   region = us-east-1
   ```

3. **Environment Variables:**
   ```bash
   export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
   export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
   export AWS_DEFAULT_REGION=us-east-1
   ```

### Configuración para MinIO (Local/On-Premise)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Spark-MinIO-Local") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .getOrCreate()

# Mismo código que con S3
df = spark.read.parquet("s3a://my-bucket/data/")
```

**Diferencias Clave:**
- `fs.s3a.endpoint`: URL de MinIO (localhost:9000)
- `fs.s3a.path.style.access`: `true` (MinIO usa path-style URLs)
- `fs.s3a.connection.ssl.enabled`: `false` (si MinIO corre sin HTTPS)

### Iniciar MinIO con Docker

```bash
# Opción 1: Docker Run
docker run -d \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio \
  -e "MINIO_ROOT_USER=minioadmin" \
  -e "MINIO_ROOT_PASSWORD=minioadmin" \
  -v /data:/data \
  minio/minio server /data --console-address ":9001"

# Opción 2: Docker Compose (recomendado)
# Ver docker-compose.yml en la raíz del taller
docker-compose up -d minio

# Acceder a la UI de MinIO
open http://localhost:9001
# User: minioadmin
# Password: minioadmin
```

**Crear Bucket desde UI o CLI:**

```bash
# Instalar mc (MinIO Client)
brew install minio/stable/mc  # macOS
# o
wget https://dl.min.io/client/mc/release/linux-amd64/mc

# Configurar alias
mc alias set local http://localhost:9000 minioadmin minioadmin

# Crear bucket
mc mb local/datalake

# Listar buckets
mc ls local/

# Copiar archivos
mc cp data/leads.csv local/datalake/bronze/leads/
```

---

## 🚀 Patrones de Ingesta de Datos

### 1. Batch Full Load (Carga Completa)

**Cuándo usar:** Primera carga o cuando el dataset completo cambia.

```python
def full_load_to_bronze(source_path, s3_bucket, table_name):
    """Carga completa de datos a capa Bronze"""
    df = spark.read.csv(source_path, header=True, inferSchema=True)

    df_with_metadata = df.withColumn("ingestion_date", current_date()) \
                         .withColumn("ingestion_timestamp", current_timestamp())

    bronze_path = f"s3a://{s3_bucket}/bronze/{table_name}/"

    df_with_metadata.write \
        .mode("overwrite") \
        .partitionBy("ingestion_date") \
        .parquet(bronze_path)

    print(f"✅ Loaded {df.count()} records to {bronze_path}")
```

### 2. Incremental Append (Datos Nuevos)

**Cuándo usar:** Logs, eventos, time-series data que solo crece.

```python
def incremental_append(new_data_path, s3_bucket, table_name):
    """Append de nuevos datos sin duplicar"""
    new_df = spark.read.json(new_data_path)

    new_df_with_metadata = new_df.withColumn("ingestion_date", current_date())

    bronze_path = f"s3a://{s3_bucket}/bronze/{table_name}/"

    new_df_with_metadata.write \
        .mode("append") \
        .partitionBy("ingestion_date") \
        .parquet(bronze_path)

    print(f"✅ Appended {new_df.count()} new records")
```

### 3. Merge/Upsert (Actualización de Registros)

**Cuándo usar:** Cuando los registros pueden actualizarse (SCD Type 1).

```python
from delta import *

def merge_updates(updates_df, s3_bucket, table_name, key_column):
    """Merge con Delta Lake para upserts eficientes"""

    delta_path = f"s3a://{s3_bucket}/silver/{table_name}/"

    # Crear tabla Delta si no existe
    if not DeltaTable.isDeltaTable(spark, delta_path):
        updates_df.write.format("delta").save(delta_path)
        return

    delta_table = DeltaTable.forPath(spark, delta_path)

    delta_table.alias("target").merge(
        updates_df.alias("source"),
        f"target.{key_column} = source.{key_column}"
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()

    print(f"✅ Merged updates into {delta_path}")
```

### 4. Streaming Incremental (Structured Streaming)

**Cuándo usar:** Datos que llegan continuamente (Kafka, Kinesis, archivos nuevos).

```python
def streaming_to_bronze(source_path, s3_bucket, table_name, checkpoint_path):
    """Ingesta streaming con checkpoint"""

    streaming_df = spark.readStream \
        .schema(schema) \
        .option("maxFilesPerTrigger", 1) \
        .json(source_path)

    bronze_path = f"s3a://{s3_bucket}/bronze/{table_name}/"

    query = streaming_df.writeStream \
        .format("parquet") \
        .option("checkpointLocation", checkpoint_path) \
        .option("path", bronze_path) \
        .partitionBy("ingestion_date") \
        .trigger(processingTime="5 minutes") \
        .start()

    query.awaitTermination()
```

---

## ⚡ Optimización de Performance

### 1. Particionamiento Efectivo

**Reglas de Oro:**
- 📏 **Tamaño de partición ideal:** 128MB - 1GB
- 🎯 **Evitar over-partitioning:** No más de 10,000 particiones
- 📅 **Particionar por columnas de filtro frecuente:** fecha, región, país

```python
# ❌ MAL: Demasiadas particiones pequeñas
df.write.partitionBy("user_id").parquet("s3a://bucket/data/")
# 1M usuarios = 1M particiones de 1KB cada una

# ✅ BIEN: Particionamiento balanceado
df.write.partitionBy("year", "month", "day").parquet("s3a://bucket/data/")
# 365 particiones/año, 10-100MB cada una
```

### 2. Compresión

**Comparación de Codecs:**

| Codec | Ratio Compresión | Speed | Splittable | Uso |
|-------|------------------|-------|------------|-----|
| **Snappy** | 2:1 | ⚡⚡⚡ Rápido | ✅ | Default (balance) |
| **Gzip** | 4:1 | ⚡ Lento | ❌ | Archivos pequeños |
| **LZ4** | 2:1 | ⚡⚡⚡ Muy rápido | ✅ | Real-time |
| **Zstd** | 3:1 | ⚡⚡ Medio | ✅ | Mejor balance |

```python
# Snappy (default para Parquet)
df.write.option("compression", "snappy").parquet("s3a://bucket/data/")

# Zstd (mejor compresión, buen speed)
df.write.option("compression", "zstd").parquet("s3a://bucket/data/")
```

### 3. File Size Control

```python
# Control de tamaño de archivos
df.repartition(10) \
  .write \
  .option("maxRecordsPerFile", 1000000) \
  .parquet("s3a://bucket/data/")

# Coalesce para reducir archivos pequeños
df.coalesce(5).write.parquet("s3a://bucket/data/")
```

### 4. S3A Performance Tuning

```python
spark = SparkSession.builder \
    .config("spark.hadoop.fs.s3a.fast.upload", "true") \
    .config("spark.hadoop.fs.s3a.fast.upload.buffer", "bytebuffer") \
    .config("spark.hadoop.fs.s3a.multipart.size", "104857600")  # 100MB \
    .config("spark.hadoop.fs.s3a.threads.max", "64") \
    .config("spark.hadoop.fs.s3a.connection.maximum", "100") \
    .config("spark.hadoop.fs.s3a.block.size", "134217728")  # 128MB \
    .getOrCreate()
```

**Parámetros Clave:**
- `fast.upload`: Usa buffering en memoria para uploads rápidos
- `multipart.size`: Tamaño de cada parte en multipart upload (min 5MB)
- `threads.max`: Threads concurrentes para I/O
- `connection.maximum`: Conexiones HTTP máximas al pool

---

## 📊 Ejemplo Completo: Pipeline Bronze → Silver → Gold

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def create_spark_session_with_s3():
    return SparkSession.builder \
        .appName("Medallion-Pipeline") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

spark = create_spark_session_with_s3()

# BRONZE: Ingesta raw
raw_df = spark.read.csv("data/raw_customers.csv", header=True)
raw_df.write \
    .mode("append") \
    .partitionBy("ingestion_date") \
    .parquet("s3a://datalake/bronze/customers/")

# SILVER: Limpieza y validación
bronze_df = spark.read.parquet("s3a://datalake/bronze/customers/")

silver_df = bronze_df \
    .dropDuplicates(["customer_id"]) \
    .filter(col("age").between(18, 100)) \
    .filter(col("email").isNotNull()) \
    .withColumn("email", lower(trim(col("email")))) \
    .withColumn("country", upper(col("country"))) \
    .withColumn("signup_year", year(col("signup_date")))

silver_df.write \
    .mode("overwrite") \
    .partitionBy("country", "signup_year") \
    .parquet("s3a://datalake/silver/customers/")

# GOLD: Agregaciones de negocio
silver_df = spark.read.parquet("s3a://datalake/silver/customers/")

gold_df = silver_df \
    .groupBy("country", "signup_year") \
    .agg(
        count("*").alias("total_customers"),
        avg("age").alias("avg_age"),
        countDistinct("email").alias("unique_emails")
    )

gold_df.write \
    .mode("overwrite") \
    .parquet("s3a://datalake/gold/customer_stats/")

print("✅ Pipeline Medallion completado")
```

---

## 🛡️ Seguridad y Governanza

### 1. Encryption at Rest

**AWS S3:**
```python
# Server-Side Encryption con S3-managed keys (SSE-S3)
df.write \
    .option("fs.s3a.server-side-encryption-algorithm", "AES256") \
    .parquet("s3a://bucket/data/")

# Server-Side Encryption con KMS (SSE-KMS)
spark.conf.set("fs.s3a.server-side-encryption-algorithm", "SSE-KMS")
spark.conf.set("fs.s3a.server-side-encryption.key", "arn:aws:kms:...")
```

### 2. Encryption in Transit

```python
# Forzar HTTPS
spark.conf.set("fs.s3a.connection.ssl.enabled", "true")
```

### 3. Access Control

**Bucket Policies (AWS S3):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::123456789:role/DataEngineerRole"},
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::datalake/silver/*"
    }
  ]
}
```

**MinIO Policies:**
```bash
# Crear policy de read-only
mc admin policy add local readonly readonly-policy.json

# Asignar a usuario
mc admin user add local dataanalyst secretpassword
mc admin policy set local readonly user=dataanalyst
```

### 4. Data Catalog (AWS Glue / Hive Metastore)

```python
# Integración con Glue Catalog
spark.conf.set("spark.sql.catalogImplementation", "hive")
spark.conf.set("hive.metastore.client.factory.class",
               "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory")

# Crear tabla externa
spark.sql("""
    CREATE EXTERNAL TABLE IF NOT EXISTS customers (
        customer_id INT,
        name STRING,
        email STRING
    )
    PARTITIONED BY (country STRING, year INT)
    STORED AS PARQUET
    LOCATION 's3a://datalake/silver/customers/'
""")

# Query con Catalog
df = spark.sql("SELECT * FROM customers WHERE country='US' AND year=2024")
```

---

## 💡 Mejores Prácticas

### 1. Gestión de Costos

**S3 Storage Classes:**
- **S3 Standard:** Datos de acceso frecuente ($0.023/GB/mes)
- **S3 Intelligent-Tiering:** Movimiento automático entre tiers
- **S3 Glacier:** Archival ($0.004/GB/mes, retrieval time de horas)

```bash
# Lifecycle policy para mover Bronze a Glacier después de 90 días
aws s3api put-bucket-lifecycle-configuration --bucket datalake --lifecycle-configuration '{
  "Rules": [{
    "Id": "ArchiveBronze",
    "Status": "Enabled",
    "Prefix": "bronze/",
    "Transitions": [{
      "Days": 90,
      "StorageClass": "GLACIER"
    }]
  }]
}'
```

### 2. Monitoreo

**Métricas Clave:**
- Read/Write throughput (MB/s)
- Request rate (requests/second)
- Error rate (4xx, 5xx)
- Data transfer costs

**CloudWatch (AWS):**
```python
# Habilitar métricas de S3 request
import boto3

s3 = boto3.client('s3')
s3.put_bucket_metrics_configuration(
    Bucket='datalake',
    Id='EntireBucket',
    MetricsConfiguration={'Id': 'EntireBucket'}
)
```

### 3. Data Quality

```python
from pyspark.sql.functions import col

def validate_silver_data(df):
    """Validaciones de calidad de datos"""

    # Verificar nulls en columnas críticas
    null_counts = df.select([
        count(when(col(c).isNull(), c)).alias(c)
        for c in df.columns
    ])

    # Verificar duplicados
    total_count = df.count()
    unique_count = df.dropDuplicates(["id"]).count()
    duplicate_rate = 1 - (unique_count / total_count)

    # Verificar valores fuera de rango
    invalid_age = df.filter(~col("age").between(0, 120)).count()

    print(f"Duplicate rate: {duplicate_rate:.2%}")
    print(f"Invalid age records: {invalid_age}")

    return duplicate_rate < 0.01 and invalid_age == 0
```

### 4. Versionado de Datos

**Delta Lake (recomendado):**
```python
from delta import DeltaTable

# Escribir con Delta
df.write.format("delta").save("s3a://datalake/delta/customers/")

# Time travel
df_yesterday = spark.read.format("delta") \
    .option("versionAsOf", 1) \
    .load("s3a://datalake/delta/customers/")

# Ver historial
delta_table = DeltaTable.forPath(spark, "s3a://datalake/delta/customers/")
delta_table.history().show()
```

---

## 🚀 Inicio Rápido

### 1. Levantar MinIO Localmente

```bash
# Con Docker Compose
cd /path/to/talleres/spark
docker-compose up -d minio

# Verificar que esté corriendo
docker ps | grep minio

# Acceder a UI
open http://localhost:9001
# Login: minioadmin / minioadmin
```

### 2. Crear Bucket y Cargar Datos

```bash
# Desde la UI de MinIO (http://localhost:9001):
# 1. Click en "Buckets" → "Create Bucket"
# 2. Nombre: "datalake"
# 3. Click en "Create"

# O desde CLI
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/datalake
mc ls local/
```

### 3. Ejecutar Script de Integración

```bash
# Generar datos de prueba
cd spark
python scripts/generate_data.py

# Ejecutar pipeline Medallion con S3
python 06-Storage-S3-MinIO/spark_s3_integration.py
```

### 4. Verificar Resultados

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Leer datos de Gold
gold_df = spark.read.parquet("s3a://datalake/gold/customer_stats/")
gold_df.show()
```

---

## 📊 Comparación: Object Storage vs HDFS

| Aspecto | Object Storage (S3) | HDFS |
|---------|---------------------|------|
| **Escalabilidad** | Ilimitada | Limitada por cluster |
| **Costo** | Pay-as-you-go (~$0.023/GB) | CapEx hardware |
| **Durabilidad** | 99.999999999% | Depende de replication factor |
| **Latencia** | ~20-100ms | ~5-20ms (local) |
| **Throughput** | Alto (paralelo) | Muy alto (co-located) |
| **Mantenimiento** | Cero (managed) | Alto (operacional) |
| **Mutabilidad** | Inmutable | Append + modificación |
| **Metastore** | Externo (Glue/Hive) | Integrado (NameNode) |
| **Separación compute/storage** | ✅ Sí | ❌ No (acoplado) |

**Cuándo usar cada uno:**

**Object Storage (S3/MinIO):**
- ✅ Data Lakes modernos
- ✅ Workloads esporádicos (no 24/7)
- ✅ Necesidad de escalabilidad elástica
- ✅ Compartir datos entre múltiples clusters
- ✅ Retención a largo plazo

**HDFS:**
- ✅ Workloads con latencia ultra-baja
- ✅ Clusters on-premise existentes
- ✅ Modificaciones frecuentes de archivos
- ✅ Strict data locality requirements

---

## 🔗 Integración con Otras Herramientas

### Spark + S3 + Athena (AWS)

```python
# Escribir datos particionados
df.write \
    .partitionBy("year", "month", "day") \
    .parquet("s3a://datalake/silver/events/")

# Crear tabla en Glue Catalog
spark.sql("""
    CREATE EXTERNAL TABLE events (
        user_id INT,
        event_type STRING,
        timestamp TIMESTAMP
    )
    PARTITIONED BY (year INT, month INT, day INT)
    STORED AS PARQUET
    LOCATION 's3://datalake/silver/events/'
""")

# Reparar particiones
spark.sql("MSCK REPAIR TABLE events")

# Ahora puedes hacer queries desde Athena
# SELECT COUNT(*) FROM events WHERE year=2024 AND month=1
```

### Spark + S3 + Databricks

```python
# Databricks tiene configuración simplificada
df = spark.read.parquet("s3a://bucket/data/")

# O usar dbfs mounts
dbutils.fs.mount(
    source = "s3a://my-bucket",
    mount_point = "/mnt/datalake",
    extra_configs = {"fs.s3a.access.key": "...", "fs.s3a.secret.key": "..."}
)

df = spark.read.parquet("/mnt/datalake/silver/customers/")
```

---

## 📚 Referencias

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [Spark S3A Connector](https://hadoop.apache.org/docs/stable/hadoop-aws/tools/hadoop-aws/index.html)
- [Medallion Architecture (Databricks)](https://www.databricks.com/glossary/medallion-architecture)
- [Delta Lake](https://delta.io/)

---

**¡Siguiente paso! 👉 [Módulo 05: Airflow](../05-Airflow/README.md) para orquestar pipelines con Spark + S3**
