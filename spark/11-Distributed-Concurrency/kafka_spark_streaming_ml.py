"""
Kafka + Spark Streaming: Real-time ML Inference

Este script implementa un pipeline completo de ML en tiempo real:
- Leer eventos desde Kafka
- Enriquecer con features de Redis
- Aplicar modelo ML
- Escribir resultados a múltiples sinks

Ejecutar:
    # Terminal 1: Iniciar Kafka
    docker-compose up kafka zookeeper

    # Terminal 2: Producir eventos
    python kafka_producer_example.py

    # Terminal 3: Ejecutar este script
    python kafka_spark_streaming_ml.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, udf, struct, to_json, current_timestamp,
    window, avg, count, sum as spark_sum
)
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType,
    DoubleType, TimestampType
)
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler
import redis
import json
from datetime import datetime

def create_spark_session():
    """
    Crear sesión Spark con configuración para streaming
    """
    return SparkSession.builder \
        .appName("KafkaSparkStreamingML") \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint_streaming_ml") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

def get_event_schema():
    """
    Schema de eventos de Kafka
    """
    return StructType([
        StructField("event_id", StringType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("timestamp", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("salary", DoubleType(), True),
        StructField("web_visits", IntegerType(), True),
        StructField("email_opens", IntegerType(), True),
    ])

def enrich_with_redis_features():
    """
    UDF para enriquecer eventos con features de Redis
    """
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def lookup(user_id):
        try:
            key = f"user_features:{user_id}"
            features_json = redis_client.get(key)

            if features_json:
                features = json.loads(features_json)
                return (
                    float(features.get('total_revenue', 0.0)),
                    float(features.get('avg_time_spent', 0.0)),
                    int(features.get('total_purchases', 0))
                )
        except:
            pass

        return (0.0, 0.0, 0)

    return udf(lookup, StructType([
        StructField("total_revenue", DoubleType()),
        StructField("avg_time_spent", DoubleType()),
        StructField("total_purchases", IntegerType())
    ]))

def setup_kafka_consumer(spark):
    """
    Configurar consumer de Kafka
    """
    print("📡 Connecting to Kafka...")

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "user-events") \
        .option("startingOffsets", "latest") \
        .option("maxOffsetsPerTrigger", 1000) \
        .load()

    print("✅ Connected to Kafka topic: user-events")

    return kafka_df

def parse_and_enrich_events(kafka_df):
    """
    Parse eventos JSON y enriquecer con Redis features
    """
    schema = get_event_schema()

    parsed_df = kafka_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    enrich_udf = enrich_with_redis_features()

    enriched_df = parsed_df.withColumn(
        "redis_features",
        enrich_udf(col("user_id"))
    )

    enriched_df = enriched_df.select(
        "*",
        col("redis_features.total_revenue").alias("user_total_revenue"),
        col("redis_features.avg_time_spent").alias("user_avg_time_spent"),
        col("redis_features.total_purchases").alias("user_total_purchases")
    ).drop("redis_features")

    return enriched_df

def apply_ml_model(enriched_df):
    """
    Aplicar modelo ML a eventos enriched
    """
    print("🤖 Loading ML model...")

    try:
        model = RandomForestClassificationModel.load("/models/user_churn_model")
        print("✅ Model loaded")
    except:
        print("⚠️  Model not found, using rule-based scoring")
        return apply_rule_based_scoring(enriched_df)

    assembler = VectorAssembler(
        inputCols=[
            "age",
            "salary",
            "web_visits",
            "email_opens",
            "user_total_revenue",
            "user_avg_time_spent"
        ],
        outputCol="features"
    )

    features_df = assembler.transform(enriched_df)

    predictions_df = model.transform(features_df)

    predictions_with_score = predictions_df.select(
        "event_id",
        "user_id",
        "timestamp",
        "event_type",
        "age",
        "salary",
        col("prediction").alias("churn_prediction"),
        col("probability")[1].alias("churn_probability")
    )

    return predictions_with_score

def apply_rule_based_scoring(enriched_df):
    """
    Scoring basado en reglas si no hay modelo
    """
    from pyspark.sql.functions import when, lit

    scored_df = enriched_df.withColumn(
        "churn_probability",
        (
            when(col("user_avg_time_spent") < 5, 0.3).otherwise(0.0) +
            when(col("web_visits") < 3, 0.2).otherwise(0.0) +
            when(col("user_total_purchases") == 0, 0.3).otherwise(0.0) +
            when(col("salary") < 50000, 0.2).otherwise(0.0)
        )
    )

    scored_df = scored_df.withColumn(
        "churn_prediction",
        when(col("churn_probability") > 0.5, 1).otherwise(0)
    )

    return scored_df

def setup_console_sink(scored_df):
    """
    Sink 1: Console (para debugging)
    """
    print("🖥️  Setting up console sink...")

    query = scored_df \
        .filter(col("churn_probability") > 0.6) \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .option("numRows", 5) \
        .trigger(processingTime='10 seconds') \
        .start()

    return query

def setup_kafka_sink(scored_df):
    """
    Sink 2: Kafka (para downstream consumers)
    """
    print("📤 Setting up Kafka sink...")

    high_risk_df = scored_df.filter(col("churn_probability") > 0.7)

    kafka_output = high_risk_df.select(
        col("event_id").cast("string").alias("key"),
        to_json(struct("*")).alias("value")
    )

    query = kafka_output.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "high-risk-churn") \
        .option("checkpointLocation", "/tmp/checkpoint_kafka") \
        .trigger(processingTime='5 seconds') \
        .start()

    return query

def setup_redis_sink(scored_df):
    """
    Sink 3: Redis (para API real-time)
    """
    print("💾 Setting up Redis sink...")

    def write_to_redis_batch(batch_df, batch_id):
        r = redis.Redis(host='localhost', port=6379, db=0)

        for row in batch_df.collect():
            key = f"churn_prediction:{row.user_id}"
            value = json.dumps({
                "churn_probability": float(row.churn_probability),
                "churn_prediction": int(row.churn_prediction),
                "last_event_time": str(row.timestamp),
                "event_id": str(row.event_id)
            })
            r.setex(key, 3600, value)

        print(f"✅ Batch {batch_id}: Wrote {batch_df.count()} predictions to Redis")

    query = scored_df \
        .filter(col("churn_probability") > 0.5) \
        .writeStream \
        .foreachBatch(write_to_redis_batch) \
        .trigger(processingTime='10 seconds') \
        .start()

    return query

def setup_parquet_sink(scored_df):
    """
    Sink 4: Parquet (para analytics)
    """
    print("📊 Setting up Parquet sink...")

    query = scored_df.writeStream \
        .format("parquet") \
        .option("path", "data/streaming_predictions/") \
        .option("checkpointLocation", "/tmp/checkpoint_parquet") \
        .partitionBy("event_type") \
        .trigger(processingTime='30 seconds') \
        .start()

    return query

def setup_aggregation_sink(scored_df):
    """
    Sink 5: Agregaciones en tiempo real
    """
    print("📈 Setting up aggregation sink...")

    from pyspark.sql.functions import to_timestamp

    scored_with_ts = scored_df.withColumn(
        "event_timestamp",
        to_timestamp(col("timestamp"))
    )

    aggregated = scored_with_ts \
        .withWatermark("event_timestamp", "1 minute") \
        .groupBy(
            window(col("event_timestamp"), "1 minute"),
            col("event_type")
        ).agg(
            count("*").alias("event_count"),
            avg("churn_probability").alias("avg_churn_prob"),
            spark_sum(col("churn_prediction").cast("int")).alias("total_high_risk")
        )

    query = aggregated.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime='30 seconds') \
        .start()

    return query

def main():
    """
    Main: Ejecutar pipeline completo
    """
    print("="*70)
    print("KAFKA + SPARK STREAMING: REAL-TIME ML INFERENCE")
    print("="*70)

    spark = create_spark_session()

    spark.sparkContext.setLogLevel("WARN")

    kafka_df = setup_kafka_consumer(spark)

    print("\n🔄 Parsing and enriching events...")
    enriched_df = parse_and_enrich_events(kafka_df)

    print("\n🤖 Applying ML model...")
    scored_df = apply_ml_model(enriched_df)

    print("\n📡 Setting up output sinks...")
    print("-" * 70)

    queries = []

    queries.append(setup_console_sink(scored_df))

    try:
        queries.append(setup_kafka_sink(scored_df))
    except Exception as e:
        print(f"⚠️  Kafka sink not available: {e}")

    try:
        queries.append(setup_redis_sink(scored_df))
    except Exception as e:
        print(f"⚠️  Redis sink not available: {e}")

    queries.append(setup_parquet_sink(scored_df))

    queries.append(setup_aggregation_sink(scored_df))

    print("-" * 70)
    print(f"\n✅ Started {len(queries)} streaming queries")
    print("\n📊 Monitoring streaming queries...")
    print("   Press Ctrl+C to stop\n")
    print("="*70)

    try:
        spark.streams.awaitAnyTermination()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping streaming queries...")

        for i, query in enumerate(queries):
            print(f"   Stopping query {i+1}...")
            query.stop()

        print("\n✅ All queries stopped")

    spark.stop()

if __name__ == "__main__":
    main()
