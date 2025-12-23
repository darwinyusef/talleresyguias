"""
Spark + S3/MinIO: Integración con Object Storage
================================================
Demuestra cómo leer y escribir datos en S3-compatible storage (AWS S3 o MinIO)
usando Spark.

Casos de uso:
- Data Lake: Almacenar datos procesados en formato Parquet
- Archivo histórico: Guardar datos antiguos en storage económico
- Compartir datos entre equipos
- Backup y disaster recovery

Requisitos:
- MinIO corriendo (o AWS S3 configurado)
- Hadoop AWS JARs en classpath
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth
import os

def create_spark_session_with_s3():
    """
    Crea sesión de Spark configurada para S3/MinIO.

    Configuración crítica:
    - spark.hadoop.fs.s3a.* para acceso S3
    - Credentials (mejor usar IAM roles en producción)
    - Endpoint para MinIO (no necesario para AWS S3)
    """

    # Configuración para MinIO local
    s3_endpoint = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    s3_access_key = os.getenv("S3_ACCESS_KEY", "minioadmin")
    s3_secret_key = os.getenv("S3_SECRET_KEY", "minioadmin")

    spark = SparkSession.builder \
        .appName("Spark-S3-Integration") \
        .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint) \
        .config("spark.hadoop.fs.s3a.access.key", s3_access_key) \
        .config("spark.hadoop.fs.s3a.secret.key", s3_secret_key) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .getOrCreate()

    # Para AWS S3, usar configuración diferente:
    # .config("spark.hadoop.fs.s3a.aws.credentials.provider",
    #         "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    # No especificar endpoint

    return spark

def write_to_s3(spark, df, s3_path, format="parquet", partition_by=None):
    """
    Escribe DataFrame a S3/MinIO.

    Args:
        spark: SparkSession
        df: DataFrame a escribir
        s3_path: Ruta S3 (ej: s3a://my-bucket/data/)
        format: Formato de archivo (parquet, csv, json)
        partition_by: Columnas para particionamiento
    """
    print(f"💾 Escribiendo datos a S3: {s3_path}")
    print(f"   Formato: {format}")
    print(f"   Particiones: {partition_by}")

    writer = df.write.mode("overwrite").format(format)

    if partition_by:
        writer = writer.partitionBy(*partition_by)

    if format == "parquet":
        writer = writer.option("compression", "snappy")

    writer.save(s3_path)

    print(f"✅ Datos escritos exitosamente")

def read_from_s3(spark, s3_path, format="parquet"):
    """
    Lee datos desde S3/MinIO.

    Args:
        spark: SparkSession
        s3_path: Ruta S3
        format: Formato de archivo

    Returns:
        DataFrame
    """
    print(f"📖 Leyendo datos desde S3: {s3_path}")

    df = spark.read.format(format).load(s3_path)

    print(f"✅ Datos leídos: {df.count()} filas, {len(df.columns)} columnas")

    return df

def example_etl_with_s3(spark):
    """
    Ejemplo completo de ETL con S3 como Data Lake.

    Pipeline:
    1. Leer datos raw desde local/S3
    2. Transformar y limpiar
    3. Escribir datos procesados a S3 en capas (Bronze/Silver/Gold)
    """
    print("\n" + "="*70)
    print("📊 Ejemplo: ETL con S3 Data Lake Architecture")
    print("="*70)

    # Generar datos de ejemplo
    print("\n1️⃣ Generando datos de ejemplo...")
    data = [
        (1, "2024-01-15", "Electronics", 999.99, "completed"),
        (2, "2024-01-15", "Clothing", 49.99, "completed"),
        (3, "2024-01-16", "Electronics", 1299.99, "pending"),
        (4, "2024-01-16", "Food", 29.99, "completed"),
        (5, "2024-01-17", "Electronics", 599.99, "completed"),
    ]

    df_raw = spark.createDataFrame(
        data,
        ["order_id", "date", "category", "amount", "status"]
    )

    print(f"   Datos raw: {df_raw.count()} filas")

    # BRONZE LAYER: Datos raw sin procesar
    print("\n2️⃣ BRONZE Layer: Guardando datos raw en S3...")
    bronze_path = "s3a://datalake/bronze/orders/"

    write_to_s3(
        spark,
        df_raw,
        bronze_path,
        format="parquet",
        partition_by=["date"]
    )

    # SILVER LAYER: Datos limpios y validados
    print("\n3️⃣ SILVER Layer: Limpiando y validando datos...")

    # Leer desde bronze
    df_bronze = read_from_s3(spark, bronze_path)

    # Transformaciones
    from pyspark.sql.functions import to_date, when

    df_silver = df_bronze \
        .withColumn("order_date", to_date(col("date"))) \
        .withColumn("amount_validated",
                   when(col("amount") > 0, col("amount")).otherwise(0)) \
        .filter(col("status") == "completed")

    silver_path = "s3a://datalake/silver/orders/"

    write_to_s3(
        spark,
        df_silver,
        silver_path,
        format="parquet",
        partition_by=["category"]
    )

    # GOLD LAYER: Datos agregados listos para analytics
    print("\n4️⃣ GOLD Layer: Agregando datos para analytics...")

    from pyspark.sql.functions import sum as spark_sum, count

    df_gold = df_silver.groupBy("category").agg(
        spark_sum("amount_validated").alias("total_revenue"),
        count("*").alias("num_orders")
    )

    gold_path = "s3a://datalake/gold/revenue_by_category/"

    write_to_s3(
        spark,
        df_gold,
        gold_path,
        format="parquet"
    )

    # Verificar datos en Gold
    print("\n5️⃣ Verificando datos en GOLD layer:")
    df_gold_read = read_from_s3(spark, gold_path)
    df_gold_read.show()

def example_incremental_load(spark):
    """
    Ejemplo de carga incremental: solo procesar datos nuevos.

    Útil para:
    - Procesar solo archivos nuevos en S3
    - Evitar re-procesar todo el dataset
    - Optimizar costos y tiempo
    """
    print("\n" + "="*70)
    print("📊 Ejemplo: Carga Incremental desde S3")
    print("="*70)

    # Usar Structured Streaming para procesar archivos nuevos
    # automáticamente cuando llegan a S3

    schema_path = "s3a://datalake/bronze/orders/"

    # Leer como stream (procesa archivos nuevos automáticamente)
    incremental_df = spark.readStream \
        .format("parquet") \
        .schema("order_id INT, date STRING, category STRING, amount DOUBLE, status STRING") \
        .load(schema_path)

    # Procesar y escribir
    query = incremental_df \
        .filter(col("status") == "completed") \
        .writeStream \
        .format("parquet") \
        .option("path", "s3a://datalake/silver/orders_incremental/") \
        .option("checkpointLocation", "s3a://datalake/checkpoints/orders/") \
        .trigger(processingTime="1 minute") \
        .start()

    print("⚡ Procesamiento incremental activo")
    print("   Nuevos archivos en S3 serán procesados automáticamente")

    # query.awaitTermination(timeout=60)  # Run for 1 minute
    query.stop()

def list_s3_files(spark, s3_path):
    """Lista archivos en un path de S3"""
    from pyspark import SparkFiles

    try:
        # Usar Hadoop FileSystem API
        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
        fs = spark.sparkContext._jvm.org.apache.hadoop.fs.FileSystem.get(
            spark.sparkContext._jvm.java.net.URI(s3_path),
            hadoop_conf
        )

        path = spark.sparkContext._jvm.org.apache.hadoop.fs.Path(s3_path)

        if fs.exists(path):
            files = fs.listStatus(path)
            print(f"\n📁 Archivos en {s3_path}:")
            for f in files:
                print(f"   - {f.getPath().getName()} ({f.getLen()} bytes)")
        else:
            print(f"⚠️  Path no existe: {s3_path}")

    except Exception as e:
        print(f"❌ Error listando archivos: {e}")

def main():
    """Función principal"""
    print("🚀 Spark + S3/MinIO Integration Demo")
    print("="*70)

    # Configurar
    print("\n⚙️  Configuración:")
    print(f"   S3 Endpoint: {os.getenv('S3_ENDPOINT', 'http://localhost:9000')}")
    print(f"   Access Key: {os.getenv('S3_ACCESS_KEY', 'minioadmin')}")

    # Crear sesión
    spark = create_spark_session_with_s3()
    spark.sparkContext.setLogLevel("WARN")

    try:
        # Ejemplo 1: ETL con Data Lake
        example_etl_with_s3(spark)

        # Ejemplo 2: Carga incremental (opcional)
        # example_incremental_load(spark)

        # Listar archivos
        list_s3_files(spark, "s3a://datalake/")

        print("\n✅ Demo completado exitosamente")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. ¿MinIO está corriendo? docker ps")
        print("   2. ¿Bucket 'datalake' existe? Crear con mc mb myminio/datalake")
        print("   3. ¿Hadoop AWS JARs en classpath?")
        raise

    finally:
        spark.stop()
        print("\n✅ Spark session cerrada")

if __name__ == "__main__":
    """
    Setup MinIO local:

    1. Iniciar MinIO:
       docker run -d -p 9000:9000 -p 9001:9001 \
         --name minio \
         -e "MINIO_ROOT_USER=minioadmin" \
         -e "MINIO_ROOT_PASSWORD=minioadmin" \
         minio/minio server /data --console-address ":9001"

    2. Crear bucket:
       docker exec minio mc alias set myminio http://localhost:9000 minioadmin minioadmin
       docker exec minio mc mb myminio/datalake

    3. Ejecutar este script:
       python 06-Storage-S3-MinIO/spark_s3_integration.py

    4. Ver archivos en MinIO Console:
       http://localhost:9001
       User: minioadmin
       Pass: minioadmin
    """
    main()
