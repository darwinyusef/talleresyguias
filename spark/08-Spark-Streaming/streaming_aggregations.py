"""
Spark Streaming: Agregaciones con Ventanas Temporales
=====================================================
Demuestra agregaciones avanzadas en tiempo real:
- Ventanas temporales (tumbling y sliding windows)
- Watermarks para late data
- Múltiples agregaciones simultáneas

Procesa eventos de ventas en tiempo real y calcula:
1. Total de ventas por ventana de 1 minuto
2. Ventas por categoría cada 30 segundos
3. Top productos en ventanas deslizantes de 2 minutos
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    window, col, sum as spark_sum, count, avg,
    current_timestamp, from_json, to_timestamp
)
from pyspark.sql.types import (
    StructType, StructField, StringType,
    IntegerType, DoubleType, TimestampType
)
import json

def create_spark_session():
    """Crea sesión de Spark para streaming"""
    return SparkSession.builder \
        .appName("Streaming-Aggregations") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

def get_sales_schema():
    """Define esquema de eventos de ventas"""
    return StructType([
        StructField("transaction_id", StringType(), False),
        StructField("timestamp", StringType(), False),
        StructField("product", StringType(), False),
        StructField("category", StringType(), False),
        StructField("amount", DoubleType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("customer_id", StringType(), True)
    ])

def read_sales_stream_from_socket(spark):
    """
    Lee stream de ventas desde socket.

    Para testing: enviar JSON por socket con nc
    """
    lines = spark.readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # Parse JSON
    schema = get_sales_schema()

    sales = lines.select(
        from_json(col("value"), schema).alias("sale")
    ).select("sale.*")

    # Convertir timestamp
    sales = sales.withColumn(
        "event_time",
        to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss")
    )

    return sales

def tumbling_window_aggregation(sales_df):
    """
    Agregación con ventana tumbling (no overlapping).

    Ventana de 1 minuto - cada minuto es independiente.
    """
    print("\n📊 Configurando agregación con Tumbling Window (1 minuto)...")

    windowed = sales_df \
        .withWatermark("event_time", "10 seconds") \
        .groupBy(
            window(col("event_time"), "1 minute")
        ) \
        .agg(
            spark_sum("amount").alias("total_sales"),
            count("*").alias("num_transactions"),
            avg("amount").alias("avg_transaction")
        ) \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("total_sales"),
            col("num_transactions"),
            col("avg_transaction")
        )

    query = windowed.writeStream \
        .format("console") \
        .outputMode("update") \
        .option("truncate", "false") \
        .queryName("tumbling_window") \
        .trigger(processingTime="5 seconds") \
        .start()

    return query

def sliding_window_aggregation(sales_df):
    """
    Agregación con ventana sliding (overlapping).

    Ventana de 2 minutos, deslizando cada 30 segundos.
    """
    print("📊 Configurando agregación con Sliding Window (2 min, slide 30s)...")

    windowed = sales_df \
        .withWatermark("event_time", "10 seconds") \
        .groupBy(
            window(col("event_time"), "2 minutes", "30 seconds"),
            col("category")
        ) \
        .agg(
            spark_sum("amount").alias("total_sales"),
            count("*").alias("num_transactions")
        ) \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("category"),
            col("total_sales"),
            col("num_transactions")
        ) \
        .orderBy(col("window_start").desc(), col("total_sales").desc())

    query = windowed.writeStream \
        .format("console") \
        .outputMode("update") \
        .option("truncate", "false") \
        .queryName("sliding_window") \
        .trigger(processingTime="10 seconds") \
        .start()

    return query

def category_stats(sales_df):
    """Estadísticas por categoría sin ventanas temporales"""
    print("📊 Configurando estadísticas por categoría...")

    stats = sales_df.groupBy("category").agg(
        spark_sum("amount").alias("total_sales"),
        avg("amount").alias("avg_sale"),
        count("*").alias("num_sales")
    ).orderBy(col("total_sales").desc())

    query = stats.writeStream \
        .format("console") \
        .outputMode("complete") \
        .option("truncate", "false") \
        .queryName("category_stats") \
        .trigger(processingTime="10 seconds") \
        .start()

    return query

def generate_mock_sales_data():
    """
    Genera datos de ventas mock para testing sin Kafka.

    Para usar este generador:
    1. Ejecuta este script
    2. En otra terminal, ejecuta el generador:
       python 08-Spark-Streaming/sales_data_generator.py
    """
    import random
    import time
    from datetime import datetime

    categories = ["Electronics", "Clothing", "Food", "Books", "Sports"]
    products = {
        "Electronics": ["Laptop", "Phone", "Tablet", "Headphones"],
        "Clothing": ["Shirt", "Pants", "Jacket", "Shoes"],
        "Food": ["Pizza", "Burger", "Salad", "Sushi"],
        "Books": ["Fiction", "Science", "History", "Biography"],
        "Sports": ["Ball", "Racket", "Shoes", "Gloves"]
    }

    while True:
        category = random.choice(categories)
        product = random.choice(products[category])

        sale = {
            "transaction_id": f"TXN{random.randint(10000, 99999)}",
            "timestamp": datetime.now().isoformat(),
            "product": product,
            "category": category,
            "amount": round(random.uniform(10, 500), 2),
            "quantity": random.randint(1, 5),
            "customer_id": f"CUST{random.randint(100, 999)}"
        }

        print(json.dumps(sale))
        time.sleep(random.uniform(0.5, 2.0))

def main():
    """Función principal"""
    print("🚀 Iniciando Streaming Aggregations...")
    print("=" * 70)

    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    print("\n💡 Instrucciones:")
    print("   1. En otra terminal, ejecuta: nc -lk 9999")
    print("   2. Envía eventos JSON de ventas (ver ejemplo abajo)")
    print("   3. Observa las agregaciones aquí\n")

    print("📝 Ejemplo de evento JSON:")
    print(json.dumps({
        "transaction_id": "TXN12345",
        "timestamp": "2024-01-15T10:30:00",
        "product": "Laptop",
        "category": "Electronics",
        "amount": 999.99,
        "quantity": 1,
        "customer_id": "CUST123"
    }, indent=2))
    print()

    try:
        # Leer stream
        sales_stream = read_sales_stream_from_socket(spark)

        print("✅ Stream configurado")
        print("   Esperando datos...\n")

        # Múltiples agregaciones
        query1 = tumbling_window_aggregation(sales_stream)
        query2 = category_stats(sales_stream)
        # query3 = sliding_window_aggregation(sales_stream)  # Opcional

        print("⚡ Streaming activo con múltiples agregaciones")
        print("   Presiona Ctrl+C para detener\n")

        # Esperar terminación
        query1.awaitTermination()

    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo streaming...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        spark.stop()
        print("✅ Spark session cerrada")

if __name__ == "__main__":
    """
    Para ejecutar:

    1. Terminal 1 - Netcat:
       nc -lk 9999

    2. Terminal 2 - Este script:
       python streaming_aggregations.py

    3. Terminal 1 - Enviar eventos (pegar líneas JSON):
       {"transaction_id":"TXN001","timestamp":"2024-01-15T10:30:00","product":"Laptop","category":"Electronics","amount":999.99,"quantity":1,"customer_id":"CUST123"}
       {"transaction_id":"TXN002","timestamp":"2024-01-15T10:30:05","product":"Phone","category":"Electronics","amount":599.99,"quantity":1,"customer_id":"CUST124"}

    O usar el generador automático (crear sales_data_generator.py)
    """
    main()
