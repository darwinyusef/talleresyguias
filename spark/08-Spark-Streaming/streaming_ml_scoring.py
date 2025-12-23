"""
Spark Streaming: ML Scoring en Tiempo Real
==========================================
Procesa leads en tiempo real desde Kafka, aplica modelo ML y enruta
leads calientes para acción inmediata.

Flujo:
1. Leer eventos de leads desde Kafka
2. Parse JSON y validación
3. Enriquecimiento con datos históricos (PostgreSQL/Parquet)
4. Aplicar modelo ML para scoring
5. Filtrar hot leads (prob > 0.7)
6. Escribir a múltiples sinks:
   - Hot leads → Kafka topic (para CRM)
   - Todas las predicciones → Parquet (analytics)
   - Métricas → Consola

Requisitos:
- Kafka corriendo en localhost:9092
- Modelo MLflow entrenado
- Topic 'leads-events' creado
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, current_timestamp, window,
    count, avg, sum as spark_sum, when, lit
)
from pyspark.sql.types import (
    StructType, StructField, StringType,
    IntegerType, DoubleType, TimestampType
)
import os

def create_spark_session():
    """Crea sesión de Spark con paquetes de Kafka"""
    return SparkSession.builder \
        .appName("LeadScoring-Streaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.streaming.checkpointLocation", "data/checkpoint/ml_scoring/") \
        .getOrCreate()

def get_lead_schema():
    """Define el esquema de eventos de leads"""
    return StructType([
        StructField("lead_id", IntegerType(), False),
        StructField("timestamp", StringType(), False),  # ISO format
        StructField("age", IntegerType(), False),
        StructField("salary", DoubleType(), False),
        StructField("web_visits", IntegerType(), False),
        StructField("last_action", StringType(), False),
        StructField("source", StringType(), True)
    ])

def read_kafka_stream(spark):
    """Lee stream de eventos desde Kafka"""
    print("📖 Conectando a Kafka...")

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "leads-events") \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()

    print("✅ Conectado a Kafka topic: leads-events")

    return kafka_df

def parse_lead_events(kafka_df):
    """Parse eventos JSON desde Kafka"""
    schema = get_lead_schema()

    # Extraer value y parsear JSON
    parsed_df = kafka_df.select(
        from_json(col("value").cast("string"), schema).alias("lead"),
        col("timestamp").alias("kafka_timestamp")
    ).select("lead.*", "kafka_timestamp")

    # Convertir timestamp string a Timestamp type
    from pyspark.sql.functions import to_timestamp

    parsed_df = parsed_df.withColumn(
        "event_timestamp",
        to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss")
    )

    return parsed_df

def enrich_with_static_data(stream_df, spark):
    """
    Enriquece stream con datos estáticos (opcional).

    Por ejemplo, perfil histórico del lead si existe.
    """
    # Cargar datos históricos (mock - en producción sería de DB)
    # Esta es una operación batch que se une con el stream

    # Por ahora, solo agregamos features derivadas
    enriched_df = stream_df \
        .withColumn(
            "salary_category",
            when(col("salary") < 30000, "low")
            .when(col("salary") < 70000, "medium")
            .otherwise("high")
        ) \
        .withColumn(
            "visit_frequency",
            when(col("web_visits") < 5, "low")
            .when(col("web_visits") < 20, "medium")
            .otherwise("high")
        )

    return enriched_df

def apply_ml_model_simple(df):
    """
    Aplica modelo ML simplificado (reglas de negocio).

    En producción, usar modelo MLflow cargado:
    model = mlflow.spark.load_model("models:/lead_scoring/production")
    predictions = model.transform(df)

    NOTA: foreachBatch permite cargar modelos PyFunc/Scikit-learn
    """

    # Scoring basado en reglas (simulado)
    scored_df = df.withColumn(
        "ml_score",
        # Iniciar con 0
        lit(0.0)
        # Bonus por salary
        + when(col("salary") > 80000, 0.3)
          .when(col("salary") > 50000, 0.2)
          .otherwise(0.1)
        # Bonus por visitas
        + when(col("web_visits") > 25, 0.3)
          .when(col("web_visits") > 10, 0.2)
          .otherwise(0.05)
        # Bonus por acción
        + when(col("last_action") == "form_submit", 0.35)
          .when(col("last_action") == "email_click", 0.2)
          .when(col("last_action") == "web_view", 0.1)
          .otherwise(0.0)
    )

    # Clasificar
    scored_df = scored_df \
        .withColumn("conversion_probability", col("ml_score")) \
        .withColumn(
            "predicted_conversion",
            when(col("ml_score") >= 0.5, 1).otherwise(0)
        ) \
        .withColumn(
            "lead_segment",
            when(col("ml_score") >= 0.7, "hot")
            .when(col("ml_score") >= 0.4, "warm")
            .otherwise("cold")
        )

    return scored_df

def write_to_console(scored_df):
    """Escribe métricas a consola para monitoreo"""

    # Agregaciones en ventanas de 30 segundos
    metrics_df = scored_df \
        .withWatermark("event_timestamp", "1 minute") \
        .groupBy(
            window(col("event_timestamp"), "30 seconds"),
            col("lead_segment")
        ) \
        .agg(
            count("*").alias("count"),
            avg("conversion_probability").alias("avg_probability")
        )

    query = metrics_df.writeStream \
        .format("console") \
        .outputMode("update") \
        .option("truncate", "false") \
        .trigger(processingTime="10 seconds") \
        .start()

    return query

def write_to_parquet(scored_df):
    """Guarda todas las predicciones en Parquet para analytics"""

    query = scored_df \
        .select(
            "lead_id", "event_timestamp", "age", "salary",
            "web_visits", "last_action", "conversion_probability",
            "predicted_conversion", "lead_segment"
        ) \
        .writeStream \
        .format("parquet") \
        .option("path", "data/streaming_predictions/") \
        .option("checkpointLocation", "data/checkpoint/parquet_sink/") \
        .outputMode("append") \
        .trigger(processingTime="30 seconds") \
        .start()

    return query

def write_hot_leads_to_kafka(scored_df):
    """
    Envía solo HOT LEADS a Kafka para procesamiento downstream
    (ej: envío inmediato a CRM, notificación a sales team)
    """

    # Filtrar solo hot leads
    hot_leads = scored_df.filter(col("lead_segment") == "hot")

    # Preparar mensaje para Kafka
    from pyspark.sql.functions import to_json, struct

    kafka_output = hot_leads.select(
        to_json(struct(
            col("lead_id"),
            col("event_timestamp").cast("string").alias("timestamp"),
            col("conversion_probability"),
            col("lead_segment"),
            col("age"),
            col("salary"),
            col("last_action")
        )).alias("value")
    )

    query = kafka_output.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "hot-leads-alerts") \
        .option("checkpointLocation", "data/checkpoint/kafka_hot_leads/") \
        .outputMode("append") \
        .trigger(processingTime="5 seconds") \
        .start()

    return query

def process_with_foreachbatch(scored_df):
    """
    Procesa cada micro-batch con lógica custom.

    Útil para:
    - Cargar modelos Scikit-learn/PyTorch
    - Escribir a múltiples sinks en una transacción
    - Lógica de negocio compleja
    """

    def process_batch(batch_df, batch_id):
        print(f"\n{'='*70}")
        print(f"📦 Procesando Batch ID: {batch_id}")
        print(f"   Filas: {batch_df.count()}")

        if not batch_df.isEmpty():
            # Mostrar estadísticas del batch
            batch_df.groupBy("lead_segment").count().show()

            # Aquí puedes:
            # 1. Cargar modelo ML y aplicar
            # 2. Escribir a PostgreSQL
            # 3. Enviar notificaciones
            # 4. Actualizar cache

            # Ejemplo: Guardar hot leads en PostgreSQL
            hot_leads = batch_df.filter(col("lead_segment") == "hot")

            if hot_leads.count() > 0:
                print(f"🔥 {hot_leads.count()} HOT LEADS detectados en batch {batch_id}")

                # En producción:
                # hot_leads.write \
                #     .format("jdbc") \
                #     .option("url", "jdbc:postgresql://localhost:5432/spark_db") \
                #     .option("dbtable", "hot_leads_streaming") \
                #     .mode("append") \
                #     .save()

    query = scored_df.writeStream \
        .foreachBatch(process_batch) \
        .trigger(processingTime="15 seconds") \
        .start()

    return query

def main():
    """Función principal"""
    print("🚀 Iniciando Spark Streaming ML Scoring...")
    print("=" * 70)

    # Crear sesión
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. Leer desde Kafka
        kafka_stream = read_kafka_stream(spark)

        # 2. Parse eventos
        parsed_stream = parse_lead_events(kafka_stream)

        print("\n📋 Esquema del stream:")
        parsed_stream.printSchema()

        # 3. Enriquecer datos
        enriched_stream = enrich_with_static_data(parsed_stream, spark)

        # 4. Aplicar ML scoring
        scored_stream = apply_ml_model_simple(enriched_stream)

        print("\n✅ Pipeline de streaming configurado")
        print("\n📊 Iniciando múltiples outputs:")
        print("   1. Consola (métricas agregadas)")
        print("   2. Parquet (todas las predicciones)")
        print("   3. Kafka (hot leads)")
        print("   4. ForEachBatch (procesamiento custom)")

        # 5. Escribir a múltiples sinks
        query_console = write_to_console(scored_stream)
        query_parquet = write_to_parquet(scored_stream)
        query_foreachbatch = process_with_foreachbatch(scored_stream)

        # Si Kafka está disponible, descomentar:
        # query_kafka = write_hot_leads_to_kafka(scored_stream)

        print("\n⚡ Streaming activo. Procesando leads en tiempo real...")
        print("   Presiona Ctrl+C para detener\n")

        # Esperar por terminación
        query_console.awaitTermination()

    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo streaming...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        spark.stop()
        print("✅ Spark session cerrada")

if __name__ == "__main__":
    """
    Para ejecutar este script:

    1. Iniciar Kafka:
       docker run -d --name kafka -p 9092:9092 \
         -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
         wurstmeister/kafka

    2. Crear topic:
       kafka-topics.sh --create --topic leads-events \
         --bootstrap-server localhost:9092

    3. Ejecutar producer (08-Spark-Streaming/kafka_producer.py)

    4. Ejecutar este script:
       python 08-Spark-Streaming/streaming_ml_scoring.py
    """
    main()
