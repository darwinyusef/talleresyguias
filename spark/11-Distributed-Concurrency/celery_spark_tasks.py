"""
Celery + Spark: Task Queue Distribuido

Este módulo define tasks Celery que ejecutan Spark jobs de forma asíncrona.

Para ejecutar:
1. Iniciar Redis:
   redis-server

2. Iniciar Celery worker:
   celery -A celery_spark_tasks worker --loglevel=info --concurrency=4

3. En otro terminal, ejecutar cliente:
   python celery_client_example.py
"""

from celery import Celery, Task
from celery.signals import task_prerun, task_postrun
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, sum as spark_sum, when
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    task_time_limit=7200,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

class SparkTask(Task):
    """
    Base task class que maneja ciclo de vida de Spark session
    """
    _spark = None

    @property
    def spark(self):
        if self._spark is None:
            logger.info("Creating new Spark session...")
            self._spark = SparkSession.builder \
                .appName(f"CeleryTask-{self.name}") \
                .config("spark.sql.adaptive.enabled", "true") \
                .config("spark.executor.memory", "4g") \
                .config("spark.driver.memory", "2g") \
                .getOrCreate()

            logger.info("Spark session created")

        return self._spark

    def after_return(self, *args, **kwargs):
        """Cleanup después de task"""
        if self._spark is not None:
            logger.info("Stopping Spark session...")
            self._spark.stop()
            self._spark = None

@celery_app.task(bind=True, base=SparkTask, name='spark.etl_pipeline')
def etl_pipeline_task(self, input_path, output_path, filters=None):
    """
    ETL pipeline distribuido con Spark
    """
    self.update_state(state='PROGRESS', meta={'stage': 'Loading data'})

    logger.info(f"ETL Pipeline: {input_path} -> {output_path}")

    df = self.spark.read.parquet(input_path)
    initial_count = df.count()

    logger.info(f"Loaded {initial_count} records")

    self.update_state(state='PROGRESS', meta={'stage': 'Applying filters'})

    if filters:
        for filter_col, filter_val in filters.items():
            df = df.filter(col(filter_col) == filter_val)

    self.update_state(state='PROGRESS', meta={'stage': 'Transforming data'})

    transformed = df.withColumn(
        "age_group",
        when(col("age") < 30, "young")
        .when(col("age") < 50, "middle")
        .otherwise("senior")
    ).withColumn(
        "salary_bracket",
        when(col("salary") < 50000, "low")
        .when(col("salary") < 100000, "medium")
        .otherwise("high")
    )

    self.update_state(state='PROGRESS', meta={'stage': 'Computing aggregations'})

    aggregated = transformed.groupBy("age_group", "salary_bracket").agg(
        count("*").alias("count"),
        avg("web_visits").alias("avg_web_visits"),
        avg("conversion").alias("conversion_rate")
    )

    self.update_state(state='PROGRESS', meta={'stage': 'Writing results'})

    aggregated.write.mode("overwrite").parquet(output_path)

    final_count = aggregated.count()

    logger.info(f"ETL complete: {initial_count} -> {final_count} records")

    return {
        'status': 'SUCCESS',
        'input_path': input_path,
        'output_path': output_path,
        'initial_count': initial_count,
        'final_count': final_count,
        'duration': self.request.runtime
    }

@celery_app.task(bind=True, base=SparkTask, name='spark.train_model')
def train_model_task(self, input_path, model_output_path, model_type='random_forest'):
    """
    Entrenar modelo ML con Spark MLlib
    """
    self.update_state(state='PROGRESS', meta={'stage': 'Loading training data'})

    logger.info(f"Training {model_type} model from {input_path}")

    df = self.spark.read.parquet(input_path)

    self.update_state(state='PROGRESS', meta={'stage': 'Feature engineering'})

    assembler = VectorAssembler(
        inputCols=["age", "salary", "web_visits", "email_opens"],
        outputCol="features"
    )
    data = assembler.transform(df)

    train, test = data.randomSplit([0.8, 0.2], seed=42)

    self.update_state(state='PROGRESS', meta={'stage': 'Training model'})

    if model_type == 'random_forest':
        from pyspark.ml.classification import RandomForestClassifier
        model = RandomForestClassifier(
            featuresCol="features",
            labelCol="conversion",
            numTrees=100,
            maxDepth=10,
            seed=42
        )
    else:
        from pyspark.ml.classification import GBTClassifier
        model = GBTClassifier(
            featuresCol="features",
            labelCol="conversion",
            maxIter=50,
            maxDepth=10,
            seed=42
        )

    start_time = time.time()
    trained_model = model.fit(train)
    training_time = time.time() - start_time

    self.update_state(state='PROGRESS', meta={'stage': 'Evaluating model'})

    predictions = trained_model.transform(test)

    from pyspark.ml.evaluation import BinaryClassificationEvaluator

    evaluator = BinaryClassificationEvaluator(
        labelCol="conversion",
        metricName="areaUnderROC"
    )
    auc = evaluator.evaluate(predictions)

    self.update_state(state='PROGRESS', meta={'stage': 'Saving model'})

    trained_model.write().overwrite().save(model_output_path)

    logger.info(f"Model trained: AUC={auc:.4f}, Time={training_time:.2f}s")

    return {
        'status': 'SUCCESS',
        'model_type': model_type,
        'model_path': model_output_path,
        'auc': auc,
        'training_time': training_time,
        'train_count': train.count(),
        'test_count': test.count()
    }

@celery_app.task(bind=True, base=SparkTask, name='spark.batch_inference')
def batch_inference_task(self, model_path, input_path, output_path):
    """
    Inferencia batch con modelo guardado
    """
    self.update_state(state='PROGRESS', meta={'stage': 'Loading model'})

    logger.info(f"Batch inference: {input_path} -> {output_path}")

    from pyspark.ml.classification import RandomForestClassificationModel
    model = RandomForestClassificationModel.load(model_path)

    self.update_state(state='PROGRESS', meta={'stage': 'Loading input data'})

    df = self.spark.read.parquet(input_path)
    record_count = df.count()

    self.update_state(state='PROGRESS', meta={'stage': 'Feature engineering'})

    assembler = VectorAssembler(
        inputCols=["age", "salary", "web_visits", "email_opens"],
        outputCol="features"
    )
    data = assembler.transform(df)

    self.update_state(state='PROGRESS', meta={'stage': 'Making predictions'})

    start_time = time.time()
    predictions = model.transform(data)
    inference_time = time.time() - start_time

    self.update_state(state='PROGRESS', meta={'stage': 'Writing predictions'})

    output_df = predictions.select(
        "lead_id",
        "age",
        "salary",
        col("prediction").alias("predicted_conversion"),
        col("probability")[1].alias("conversion_probability")
    )

    output_df.write.mode("overwrite").parquet(output_path)

    high_probability = output_df.filter(col("conversion_probability") > 0.7).count()

    logger.info(f"Inference complete: {record_count} predictions in {inference_time:.2f}s")

    return {
        'status': 'SUCCESS',
        'model_path': model_path,
        'input_path': input_path,
        'output_path': output_path,
        'record_count': record_count,
        'high_probability_count': high_probability,
        'inference_time': inference_time,
        'throughput': record_count / inference_time
    }

@celery_app.task(bind=True, base=SparkTask, name='spark.data_quality')
def data_quality_check_task(self, input_path):
    """
    Chequeo completo de calidad de datos
    """
    self.update_state(state='PROGRESS', meta={'stage': 'Loading data'})

    logger.info(f"Data quality check: {input_path}")

    df = self.spark.read.parquet(input_path)

    self.update_state(state='PROGRESS', meta={'stage': 'Computing metrics'})

    total_count = df.count()

    null_counts = {}
    for col_name in df.columns:
        null_count = df.filter(col(col_name).isNull()).count()
        null_counts[col_name] = {
            'count': null_count,
            'percentage': (null_count / total_count) * 100
        }

    duplicate_count = total_count - df.dropDuplicates().count()

    from pyspark.sql.functions import stddev, mean

    numeric_cols = ["age", "salary", "web_visits"]
    outliers = {}

    for col_name in numeric_cols:
        stats = df.select(
            mean(col(col_name)).alias("mean"),
            stddev(col(col_name)).alias("stddev")
        ).collect()[0]

        if stats["stddev"]:
            outlier_count = df.filter(
                (col(col_name) > stats["mean"] + 3 * stats["stddev"]) |
                (col(col_name) < stats["mean"] - 3 * stats["stddev"])
            ).count()

            outliers[col_name] = {
                'count': outlier_count,
                'percentage': (outlier_count / total_count) * 100
            }

    quality_score = 100.0 - (
        (duplicate_count / total_count) * 30 +
        sum(n['percentage'] for n in null_counts.values()) / len(null_counts) * 40 +
        sum(o['percentage'] for o in outliers.values()) / len(outliers) * 30
    )

    logger.info(f"Quality check complete: Score={quality_score:.2f}")

    return {
        'status': 'SUCCESS',
        'input_path': input_path,
        'total_records': total_count,
        'null_counts': null_counts,
        'duplicate_count': duplicate_count,
        'outliers': outliers,
        'quality_score': max(0, quality_score)
    }

@celery_app.task(bind=True, base=SparkTask, name='spark.aggregate_metrics')
def aggregate_metrics_task(self, input_path, metrics_output_path, group_by_cols):
    """
    Calcular métricas agregadas
    """
    self.update_state(state='PROGRESS', meta={'stage': 'Loading data'})

    logger.info(f"Computing metrics grouped by {group_by_cols}")

    df = self.spark.read.parquet(input_path)

    self.update_state(state='PROGRESS', meta={'stage': 'Computing aggregations'})

    metrics = df.groupBy(group_by_cols).agg(
        count("*").alias("total_count"),
        avg("age").alias("avg_age"),
        avg("salary").alias("avg_salary"),
        avg("web_visits").alias("avg_web_visits"),
        spark_sum(col("conversion").cast("int")).alias("total_conversions"),
        (spark_sum(col("conversion").cast("int")) / count("*")).alias("conversion_rate")
    )

    self.update_state(state='PROGRESS', meta={'stage': 'Writing metrics'})

    metrics.write.mode("overwrite").parquet(metrics_output_path)

    metric_count = metrics.count()

    logger.info(f"Metrics computed: {metric_count} groups")

    return {
        'status': 'SUCCESS',
        'input_path': input_path,
        'output_path': metrics_output_path,
        'group_by': group_by_cols,
        'metric_count': metric_count
    }

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, **kwargs):
    """Hook antes de ejecutar task"""
    logger.info(f"🚀 Starting task: {task.name} [{task_id}]")

@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, **kwargs):
    """Hook después de ejecutar task"""
    logger.info(f"✅ Completed task: {task.name} [{task_id}]")

if __name__ == "__main__":
    print("Celery Spark Tasks Module")
    print("Run with: celery -A celery_spark_tasks worker --loglevel=info")
