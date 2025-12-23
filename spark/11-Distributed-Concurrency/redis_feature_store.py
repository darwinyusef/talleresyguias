"""
Redis Feature Store con Spark

Este script implementa un Feature Store distribuido usando Redis como cache
para features calculadas con Spark.

Ejecutar:
    python redis_feature_store.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum as spark_sum, max as spark_max, min as spark_min
from pyspark.sql.types import StringType, DoubleType, IntegerType, MapType
import redis
import json
import time
import pickle
from datetime import datetime, timedelta

class RedisFeatureStore:
    """
    Feature Store distribuido usando Redis
    """

    def __init__(self, host='localhost', port=6379, db=0, ttl=86400):
        """
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            ttl: Time to live en segundos (default 24 horas)
        """
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False
        )
        self.ttl = ttl

        print(f"✅ Connected to Redis: {host}:{port} (DB {db})")
        print(f"   TTL: {ttl}s ({ttl/3600:.1f} hours)")

    def write_features(self, entity_id, features_dict, namespace="features"):
        """
        Escribir features de una entidad
        """
        key = f"{namespace}:{entity_id}"
        value = json.dumps(features_dict)
        self.redis_client.setex(key, self.ttl, value)

    def read_features(self, entity_id, namespace="features"):
        """
        Leer features de una entidad
        """
        key = f"{namespace}:{entity_id}"
        value = self.redis_client.get(key)

        if value:
            return json.loads(value)
        return None

    def write_features_batch_spark(self, spark_df, entity_col, namespace="features"):
        """
        Escribir features en batch desde Spark DataFrame
        """
        print(f"\n📊 Writing {spark_df.count()} feature sets to Redis...")

        start_time = time.time()

        def write_partition(partition):
            r = redis.Redis(
                host=self.redis_client.connection_pool.connection_kwargs['host'],
                port=self.redis_client.connection_pool.connection_kwargs['port'],
                db=self.redis_client.connection_pool.connection_kwargs['db']
            )

            pipe = r.pipeline()
            count = 0

            for row in partition:
                entity_id = row[entity_col]
                features = {k: v for k, v in row.asDict().items() if k != entity_col}

                key = f"{namespace}:{entity_id}"
                value = json.dumps(features, default=str)

                pipe.setex(key, self.ttl, value)
                count += 1

                if count % 1000 == 0:
                    pipe.execute()
                    pipe = r.pipeline()

            if count % 1000 != 0:
                pipe.execute()

            yield count

        total_written = spark_df.rdd.mapPartitions(write_partition).sum()

        elapsed = time.time() - start_time

        print(f"✅ Wrote {int(total_written)} features in {elapsed:.2f}s")
        print(f"   Throughput: {int(total_written/elapsed)} writes/sec")

        return int(total_written)

    def read_features_batch(self, entity_ids, namespace="features"):
        """
        Leer features en batch para múltiples entidades
        """
        pipe = self.redis_client.pipeline()

        for entity_id in entity_ids:
            key = f"{namespace}:{entity_id}"
            pipe.get(key)

        results = pipe.execute()

        features_list = []
        for entity_id, value in zip(entity_ids, results):
            if value:
                features = json.loads(value)
                features['entity_id'] = entity_id
                features_list.append(features)

        return features_list

    def get_feature_stats(self, namespace="features"):
        """
        Obtener estadísticas de features en Redis
        """
        pattern = f"{namespace}:*"
        keys = list(self.redis_client.scan_iter(match=pattern, count=1000))

        return {
            'total_features': len(keys),
            'namespace': namespace,
            'memory_usage_mb': self.redis_client.info('memory')['used_memory'] / (1024 * 1024)
        }

    def delete_namespace(self, namespace="features"):
        """
        Eliminar todas las features de un namespace
        """
        pattern = f"{namespace}:*"
        keys = list(self.redis_client.scan_iter(match=pattern, count=1000))

        if keys:
            self.redis_client.delete(*keys)

        print(f"🗑️  Deleted {len(keys)} keys from namespace '{namespace}'")

        return len(keys)

def compute_user_features(spark, events_path):
    """
    Calcular features de usuario desde eventos con Spark
    """
    print("\n📊 Computing user features from events...")

    df = spark.read.parquet(events_path)

    features = df.groupBy("user_id").agg(
        count("*").alias("total_events"),
        spark_sum("page_views").alias("total_page_views"),
        avg("time_spent").alias("avg_time_spent"),
        spark_sum(col("purchase_amount")).alias("total_revenue"),
        count(col("purchase_amount")).alias("total_purchases"),
        spark_max("timestamp").alias("last_activity"),
        spark_min("timestamp").alias("first_activity")
    )

    features = features.withColumn(
        "avg_purchase_value",
        col("total_revenue") / col("total_purchases")
    ).withColumn(
        "is_active",
        (col("last_activity") > (datetime.now() - timedelta(days=30))).cast("int")
    )

    print(f"✅ Computed features for {features.count()} users")

    return features

def enrich_dataframe_with_redis_features(spark, df, feature_store, entity_col="user_id"):
    """
    Enriquecer DataFrame de Spark con features de Redis
    """
    print(f"\n🔗 Enriching DataFrame with Redis features...")

    from pyspark.sql.functions import udf
    from pyspark.sql.types import MapType, StringType

    def lookup_features_udf(entity_id):
        features = feature_store.read_features(entity_id, namespace="user_features")
        if features:
            return {k: str(v) for k, v in features.items()}
        return {}

    lookup_udf = udf(lookup_features_udf, MapType(StringType(), StringType()))

    enriched = df.withColumn("redis_features", lookup_udf(col(entity_col)))

    for feature_name in ["total_page_views", "avg_time_spent", "total_revenue"]:
        enriched = enriched.withColumn(
            feature_name,
            col("redis_features").getItem(feature_name).cast(DoubleType())
        )

    enriched = enriched.drop("redis_features")

    print(f"✅ Enriched {enriched.count()} records")

    return enriched

def example_real_time_feature_serving():
    """
    Ejemplo: Serving de features en tiempo real
    """
    print("\n" + "="*70)
    print("EXAMPLE: REAL-TIME FEATURE SERVING")
    print("="*70)

    spark = SparkSession.builder \
        .appName("RedisFeatureStore") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

    feature_store = RedisFeatureStore()

    print("\n1️⃣  Computing features with Spark...")
    user_features = compute_user_features(spark, "data/user_events.parquet")

    user_features.show(5, truncate=False)

    print("\n2️⃣  Writing features to Redis...")
    feature_store.write_features_batch_spark(
        user_features,
        entity_col="user_id",
        namespace="user_features"
    )

    print("\n3️⃣  Reading features from Redis (single user)...")
    user_id = 12345
    features = feature_store.read_features(user_id, namespace="user_features")

    if features:
        print(f"\n📦 Features for user {user_id}:")
        print(json.dumps(features, indent=2, default=str))
    else:
        print(f"❌ No features found for user {user_id}")

    print("\n4️⃣  Reading features in batch...")
    user_ids = [12345, 12346, 12347, 12348, 12349]
    batch_features = feature_store.read_features_batch(user_ids, namespace="user_features")

    print(f"📦 Retrieved features for {len(batch_features)} users")
    for feat in batch_features[:3]:
        print(f"   User {feat['entity_id']}: {feat}")

    print("\n5️⃣  Feature Store Statistics...")
    stats = feature_store.get_feature_stats(namespace="user_features")
    print(json.dumps(stats, indent=2))

    spark.stop()

def example_feature_lookup_in_inference():
    """
    Ejemplo: Usar features de Redis durante inferencia
    """
    print("\n" + "="*70)
    print("EXAMPLE: FEATURE LOOKUP DURING INFERENCE")
    print("="*70)

    spark = SparkSession.builder \
        .appName("FeatureLookupInference") \
        .getOrCreate()

    feature_store = RedisFeatureStore()

    print("\n1️⃣  Loading inference data...")
    inference_df = spark.read.parquet("data/inference_requests.parquet")

    print(f"   Loaded {inference_df.count()} inference requests")
    inference_df.show(5)

    print("\n2️⃣  Enriching with Redis features...")
    enriched_df = enrich_dataframe_with_redis_features(
        spark,
        inference_df,
        feature_store,
        entity_col="user_id"
    )

    enriched_df.show(5)

    print("\n3️⃣  Making predictions with enriched features...")

    from pyspark.ml.classification import RandomForestClassificationModel
    from pyspark.ml.feature import VectorAssembler

    assembler = VectorAssembler(
        inputCols=["age", "total_page_views", "avg_time_spent", "total_revenue"],
        outputCol="features"
    )

    features_df = assembler.transform(enriched_df)

    model = RandomForestClassificationModel.load("/models/user_churn_model")

    predictions = model.transform(features_df)

    print("\n📊 Predictions:")
    predictions.select(
        "user_id",
        "prediction",
        col("probability")[1].alias("churn_probability")
    ).show(10)

    spark.stop()

def example_distributed_rate_limiter():
    """
    Ejemplo: Rate limiter distribuido con Redis
    """
    print("\n" + "="*70)
    print("EXAMPLE: DISTRIBUTED RATE LIMITER")
    print("="*70)

    class DistributedRateLimiter:
        def __init__(self, redis_client):
            self.redis = redis_client

        def is_allowed(self, key, max_requests, window_seconds):
            current_time = time.time()
            window_start = current_time - window_seconds

            redis_key = f"rate_limit:{key}"

            self.redis.zremrangebyscore(redis_key, 0, window_start)

            request_count = self.redis.zcard(redis_key)

            if request_count < max_requests:
                self.redis.zadd(redis_key, {str(current_time): current_time})
                self.redis.expire(redis_key, window_seconds)
                return True

            return False

    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    limiter = DistributedRateLimiter(redis_client)

    api_key = "user_12345"
    max_requests = 10
    window_seconds = 5

    print(f"\n⚡ Rate limit: {max_requests} requests per {window_seconds} seconds")
    print(f"   Testing with key: {api_key}\n")

    for i in range(15):
        allowed = limiter.is_allowed(api_key, max_requests, window_seconds)

        status = "✅ Allowed" if allowed else "❌ Rate limited"
        print(f"   Request {i+1:2d}: {status}")

        if not allowed:
            print(f"      Waiting {window_seconds}s...")
            time.sleep(window_seconds)
        else:
            time.sleep(0.2)

def main():
    """
    Main con menú de ejemplos
    """
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║              REDIS FEATURE STORE WITH SPARK                      ║
║                                                                   ║
║  Prerequisites:                                                  ║
║    - Redis running: redis-server                                 ║
║    - Sample data in: data/user_events.parquet                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Connected to Redis\n")
    except:
        print("❌ Cannot connect to Redis. Start with: redis-server\n")
        return

    examples = {
        '1': ('Real-time Feature Serving', example_real_time_feature_serving),
        '2': ('Feature Lookup During Inference', example_feature_lookup_in_inference),
        '3': ('Distributed Rate Limiter', example_distributed_rate_limiter),
    }

    while True:
        print("\n" + "="*70)
        print("SELECT EXAMPLE:")
        print("="*70)

        for key, (name, _) in examples.items():
            print(f"  {key}. {name}")

        print("  0. Exit")
        print()

        choice = input("Enter choice: ")

        if choice == '0':
            print("\nGoodbye! 👋\n")
            break
        elif choice in examples:
            _, func = examples[choice]
            try:
                func()
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()

            input("\nPress Enter to continue...")
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
