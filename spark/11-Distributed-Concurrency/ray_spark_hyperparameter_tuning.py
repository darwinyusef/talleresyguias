"""
Ray + Spark: Hyperparameter Tuning Distribuido

Este script demuestra cómo usar Ray Tune para hacer hyperparameter tuning
de modelos Spark MLlib de forma distribuida.

Ejecutar:
    python ray_spark_hyperparameter_tuning.py
"""

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import RandomForestClassifier, GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col, when
import ray
from ray import tune
from ray.tune.search.optuna import OptunaSearch
from ray.tune.search import ConcurrencyLimiter
import mlflow
import time

def create_spark_session():
    """Crear sesión Spark optimizada"""
    return SparkSession.builder \
        .appName("RaySparkTuning") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

def prepare_data(spark, data_path="data/leads.parquet"):
    """
    Preparar datos para entrenamiento
    """
    print("📊 Loading and preparing data...")

    df = spark.read.parquet(data_path)

    assembler = VectorAssembler(
        inputCols=["age", "salary", "web_visits", "email_opens"],
        outputCol="features"
    )

    data = assembler.transform(df)

    train, test = data.randomSplit([0.8, 0.2], seed=42)

    print(f"✅ Training samples: {train.count()}")
    print(f"✅ Test samples: {test.count()}")

    return train, test

def train_model_with_config(config):
    """
    Función de entrenamiento que Ray ejecutará con diferentes configs
    """
    spark = create_spark_session()

    try:
        train, test = prepare_data(spark)

        model_type = config["model_type"]

        if model_type == "random_forest":
            model = RandomForestClassifier(
                featuresCol="features",
                labelCol="conversion",
                numTrees=config["num_trees"],
                maxDepth=config["max_depth"],
                minInstancesPerNode=config["min_instances_per_node"],
                seed=42
            )
        else:
            model = GBTClassifier(
                featuresCol="features",
                labelCol="conversion",
                maxIter=config["max_iter"],
                maxDepth=config["max_depth"],
                stepSize=config["step_size"],
                seed=42
            )

        start_time = time.time()
        trained_model = model.fit(train)
        training_time = time.time() - start_time

        predictions = trained_model.transform(test)

        evaluator = BinaryClassificationEvaluator(
            labelCol="conversion",
            metricName="areaUnderROC"
        )
        auc = evaluator.evaluate(predictions)

        evaluator_pr = BinaryClassificationEvaluator(
            labelCol="conversion",
            metricName="areaUnderPR"
        )
        pr = evaluator_pr.evaluate(predictions)

        with mlflow.start_run(nested=True):
            mlflow.log_params(config)
            mlflow.log_metric("auc", auc)
            mlflow.log_metric("pr", pr)
            mlflow.log_metric("training_time", training_time)

        tune.report(
            auc=auc,
            pr=pr,
            training_time=training_time
        )

    finally:
        spark.stop()

def run_hyperparameter_tuning():
    """
    Ejecutar búsqueda de hiperparámetros distribuida
    """
    print("🚀 Starting Ray...")
    ray.init(num_cpus=8, ignore_reinit_error=True)

    mlflow.set_experiment("spark_ray_hyperparameter_tuning")

    search_space = {
        "model_type": tune.choice(["random_forest", "gbt"]),
        "num_trees": tune.randint(50, 300),
        "max_depth": tune.randint(5, 20),
        "min_instances_per_node": tune.randint(1, 10),
        "max_iter": tune.randint(20, 100),
        "step_size": tune.loguniform(0.001, 0.3),
    }

    search_algo = OptunaSearch()

    search_algo = ConcurrencyLimiter(search_algo, max_concurrent=4)

    print("\n🔍 Starting hyperparameter search...")
    print(f"   - Search space: {len(search_space)} parameters")
    print(f"   - Number of trials: 50")
    print(f"   - Concurrent trials: 4")
    print()

    analysis = tune.run(
        train_model_with_config,
        config=search_space,
        search_alg=search_algo,
        num_samples=50,
        resources_per_trial={"cpu": 2},
        metric="auc",
        mode="max",
        verbose=1,
        name="spark_tuning_experiment"
    )

    best_config = analysis.get_best_config(metric="auc", mode="max")
    best_result = analysis.best_result

    print("\n" + "="*70)
    print("🏆 BEST CONFIGURATION FOUND:")
    print("="*70)
    for key, value in best_config.items():
        print(f"   {key:25} = {value}")

    print("\n📊 BEST METRICS:")
    print(f"   AUC:            {best_result['auc']:.4f}")
    print(f"   PR-AUC:         {best_result['pr']:.4f}")
    print(f"   Training time:  {best_result['training_time']:.2f}s")
    print("="*70 + "\n")

    results_df = analysis.results_df
    print("📈 Summary statistics:")
    print(results_df[["config.model_type", "auc", "pr", "training_time"]].describe())

    ray.shutdown()

    return best_config, best_result

def train_final_model(best_config):
    """
    Entrenar modelo final con la mejor configuración
    """
    print("\n🎓 Training final model with best configuration...")

    spark = create_spark_session()

    df = spark.read.parquet("data/leads.parquet")

    assembler = VectorAssembler(
        inputCols=["age", "salary", "web_visits", "email_opens"],
        outputCol="features"
    )
    data = assembler.transform(df)

    model_type = best_config["model_type"]

    if model_type == "random_forest":
        model = RandomForestClassifier(
            featuresCol="features",
            labelCol="conversion",
            numTrees=best_config["num_trees"],
            maxDepth=best_config["max_depth"],
            minInstancesPerNode=best_config["min_instances_per_node"],
            seed=42
        )
    else:
        model = GBTClassifier(
            featuresCol="features",
            labelCol="conversion",
            maxIter=best_config["max_iter"],
            maxDepth=best_config["max_depth"],
            stepSize=best_config["step_size"],
            seed=42
        )

    final_model = model.fit(data)

    model_path = f"/models/best_{model_type}_model"
    final_model.write().overwrite().save(model_path)

    print(f"✅ Final model saved to: {model_path}")

    spark.stop()

    return model_path

if __name__ == "__main__":
    print("="*70)
    print("RAY + SPARK: DISTRIBUTED HYPERPARAMETER TUNING")
    print("="*70)

    best_config, best_result = run_hyperparameter_tuning()

    model_path = train_final_model(best_config)

    print("\n✅ Hyperparameter tuning complete!")
    print(f"   Best model saved to: {model_path}")
    print(f"   Best AUC: {best_result['auc']:.4f}")
