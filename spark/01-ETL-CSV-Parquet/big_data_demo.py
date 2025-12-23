from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import time

def big_data_simulation():
    spark = SparkSession.builder \
        .appName("BigDataPartitioningDemo") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()

    # 1. Crear un dataset "grande" en memoria (Millones de filas)
    print("🚀 Generando 10 millones de filas para demostración...")
    df = spark.range(0, 10000000) \
        .withColumn("category", (F.col("id") % 10).cast("string")) \
        .withColumn("timestamp", F.current_timestamp()) \
        .withColumn("value", F.rand() * 100)

    # 2. Análisis de Shuffling y Particionamiento
    print("📊 Estado inicial de particiones:", df.rdd.getNumPartitions())

    start_time = time.time()
    # Agregación pesada que disparará un Shuffle
    agg_df = df.groupBy("category").agg(
        F.sum("value").alias("total_value"),
        F.avg("value").alias("avg_value"),
        F.count("id").alias("count")
    )
    
    agg_df.show()
    print(f"⏱️ Tiempo procesado (sin particionar): {time.time() - start_time:.2f}s")

    # 3. Optimización con Particionamiento en disco
    # Escribir particionado por 'category'
    output_path = "data/partitioned_data.parquet"
    print(f"💾 Guardando datos particionados en {output_path}...")
    
    df.write.mode("overwrite") \
        .partitionBy("category") \
        .parquet(output_path)

    # 4. Beneficio de 'Partition Pruning'
    print("🔍 Demostrando Partition Pruning (Spark solo lee la carpeta necesaria)...")
    start_time = time.time()
    spark.read.parquet(output_path).filter(F.col("category") == "5").count()
    print(f"⏱️ Tiempo de conteo con filtro de partición: {time.time() - start_time:.4f}s")

    spark.stop()

if __name__ == "__main__":
    big_data_simulation()
