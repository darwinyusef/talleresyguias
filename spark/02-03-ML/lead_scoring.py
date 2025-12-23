"""
Lead Scoring con Spark MLlib + MLflow
=====================================
Modelo de clasificación supervisada para predecir la probabilidad
de conversión de leads basado en características demográficas y comportamiento.

Técnicas:
- Gradient Boosted Trees (GBT) - modelo ensemble potente
- Feature Engineering con StringIndexer y OneHotEncoder
- Evaluación con múltiples métricas (AUC, Accuracy, Precision, Recall)
- Análisis de importancia de features
- Tracking completo con MLflow
- Guardado de predicciones en PostgreSQL
"""

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler
from pyspark.ml.classification import GBTClassifier, RandomForestClassifier, LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.sql.functions import col, when
import mlflow
import mlflow.spark
import os

def create_spark_session():
    """Crea sesión de Spark optimizada para ML"""
    return SparkSession.builder \
        .appName("LeadScoring-GBT") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def load_and_analyze_data(spark, input_path="data/lead_conversions.csv"):
    """Carga datos y muestra análisis exploratorio"""
    print(f"📖 Cargando datos desde: {input_path}")

    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Limpieza básica
    df_clean = df.dropna()

    print(f"✅ Datos cargados: {df_clean.count()} filas")
    print(f"   Features: {', '.join(df_clean.columns)}")

    # Análisis de la variable target
    print("\n📊 Distribución de la variable target 'converted':")
    df_clean.groupBy("converted").count().show()

    # Calcular tasa de conversión
    conversion_rate = df_clean.filter(col("converted") == 1).count() / df_clean.count()
    print(f"   Tasa de conversión: {conversion_rate:.2%}")

    # Estadísticas por acción
    print("\n📈 Tasa de conversión por 'last_action':")
    df_clean.groupBy("last_action") \
        .agg({"converted": "avg", "*": "count"}) \
        .withColumnRenamed("avg(converted)", "conversion_rate") \
        .withColumnRenamed("count(1)", "count") \
        .orderBy(col("conversion_rate").desc()) \
        .show()

    return df_clean

def build_ml_pipeline(model_type="gbt"):
    """Construye pipeline de ML con diferentes modelos"""

    # 1. Feature Engineering para 'last_action' (categórica)
    indexer = StringIndexer(
        inputCol="last_action",
        outputCol="last_action_index",
        handleInvalid="keep"
    )

    encoder = OneHotEncoder(
        inputCol="last_action_index",
        outputCol="last_action_vec",
        dropLast=True
    )

    # 2. Vector Assembler - combinar todas las features
    feature_cols = ["age", "salary", "web_visits", "last_action_vec"]
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features",
        handleInvalid="skip"
    )

    # 3. Seleccionar modelo
    if model_type == "gbt":
        classifier = GBTClassifier(
            labelCol="converted",
            featuresCol="features",
            maxIter=20,
            maxDepth=5,
            seed=42
        )
    elif model_type == "rf":
        classifier = RandomForestClassifier(
            labelCol="converted",
            featuresCol="features",
            numTrees=100,
            maxDepth=5,
            seed=42
        )
    elif model_type == "lr":
        # Para Logistic Regression, agregar escalado
        scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
        classifier = LogisticRegression(
            labelCol="converted",
            featuresCol="scaled_features",
            maxIter=20,
            regParam=0.01
        )
        return Pipeline(stages=[indexer, encoder, assembler, scaler, classifier])
    else:
        raise ValueError(f"Modelo no soportado: {model_type}")

    # Pipeline completo
    pipeline = Pipeline(stages=[indexer, encoder, assembler, classifier])

    return pipeline

def evaluate_model(predictions, model_name="Model"):
    """Evalúa modelo con múltiples métricas"""
    print(f"\n📊 Evaluación del modelo: {model_name}")
    print("=" * 70)

    # 1. AUC (Area Under ROC Curve)
    auc_evaluator = BinaryClassificationEvaluator(
        labelCol="converted",
        metricName="areaUnderROC"
    )
    auc = auc_evaluator.evaluate(predictions)

    # 2. Accuracy
    accuracy_evaluator = MulticlassClassificationEvaluator(
        labelCol="converted",
        predictionCol="prediction",
        metricName="accuracy"
    )
    accuracy = accuracy_evaluator.evaluate(predictions)

    # 3. Precision
    precision_evaluator = MulticlassClassificationEvaluator(
        labelCol="converted",
        predictionCol="prediction",
        metricName="weightedPrecision"
    )
    precision = precision_evaluator.evaluate(predictions)

    # 4. Recall
    recall_evaluator = MulticlassClassificationEvaluator(
        labelCol="converted",
        predictionCol="prediction",
        metricName="weightedRecall"
    )
    recall = recall_evaluator.evaluate(predictions)

    # 5. F1 Score
    f1_evaluator = MulticlassClassificationEvaluator(
        labelCol="converted",
        predictionCol="prediction",
        metricName="f1"
    )
    f1 = f1_evaluator.evaluate(predictions)

    # Mostrar resultados
    print(f"   AUC (ROC):      {auc:.4f}")
    print(f"   Accuracy:       {accuracy:.4f}")
    print(f"   Precision:      {precision:.4f}")
    print(f"   Recall:         {recall:.4f}")
    print(f"   F1 Score:       {f1:.4f}")

    # Matriz de confusión simplificada
    print("\n📋 Distribución de predicciones:")
    predictions.groupBy("converted", "prediction").count().show()

    metrics = {
        "auc": auc,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

    return metrics

def show_feature_importance(model, feature_names):
    """Muestra importancia de features (solo para tree-based models)"""
    try:
        # Obtener el clasificador del pipeline
        classifier = model.stages[-1]

        if hasattr(classifier, 'featureImportances'):
            importances = classifier.featureImportances.toArray()

            print("\n🎯 Importancia de Features:")
            print("=" * 70)

            # Expandir nombres de features (considerar one-hot encoding)
            expanded_names = feature_names.copy()

            for i, (name, importance) in enumerate(zip(expanded_names, importances)):
                print(f"   {i+1}. {name:20s}: {importance:.4f}")

    except Exception as e:
        print(f"⚠️  No se pudo calcular feature importance: {e}")

def save_predictions_to_postgres(predictions, table_name="lead_predictions"):
    """Guarda predicciones en PostgreSQL para servir via API"""
    print(f"\n💾 Guardando predicciones en PostgreSQL...")

    jdbc_url = "jdbc:postgresql://localhost:5432/spark_db"
    connection_properties = {
        "user": "postgres",
        "password": "password",
        "driver": "org.postgresql.Driver"
    }

    try:
        # Seleccionar columnas relevantes
        output_df = predictions.select(
            col("id").alias("lead_id"),
            col("prediction").alias("predicted_conversion"),
            col("probability").getItem(1).alias("conversion_probability")
        )

        # Escribir a PostgreSQL
        output_df.write.jdbc(
            url=jdbc_url,
            table=table_name,
            mode="overwrite",
            properties=connection_properties
        )

        print(f"✅ Predicciones guardadas en tabla '{table_name}'")

    except Exception as e:
        print(f"⚠️  No se pudo guardar en PostgreSQL: {e}")
        print("   (Asegúrate de que PostgreSQL esté corriendo y el driver JDBC esté disponible)")

def train_and_compare_models(spark, df):
    """Entrena múltiples modelos y compara resultados"""
    print("\n🔬 Entrenando y comparando modelos...")
    print("=" * 70)

    mlflow.set_experiment("Lead_Scoring_Model_Comparison")

    # Split data
    train, test = df.randomSplit([0.8, 0.2], seed=42)
    print(f"\n📊 Train: {train.count()} | Test: {test.count()}")

    models_to_try = ["gbt", "rf", "lr"]
    results = []

    for model_type in models_to_try:
        print(f"\n{'='*70}")
        print(f"🤖 Entrenando: {model_type.upper()}")

        with mlflow.start_run(run_name=f"LeadScoring_{model_type.upper()}"):
            # Build pipeline
            pipeline = build_ml_pipeline(model_type=model_type)

            # Train
            print("   Entrenando modelo...")
            model = pipeline.fit(train)

            # Predict
            predictions = model.transform(test)

            # Evaluate
            metrics = evaluate_model(predictions, model_name=model_type.upper())

            # Log en MLflow
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("train_size", train.count())
            mlflow.log_param("test_size", test.count())

            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)

            # Guardar modelo
            mlflow.spark.log_model(model, f"lead_scoring_{model_type}")

            # Feature importance (solo para tree models)
            if model_type in ["gbt", "rf"]:
                feature_names = ["age", "salary", "web_visits", "last_action"]
                show_feature_importance(model, feature_names)

            results.append({
                "model": model_type,
                "auc": metrics["auc"],
                "accuracy": metrics["accuracy"],
                "f1": metrics["f1"]
            })

    # Mostrar comparación final
    print(f"\n{'='*70}")
    print("🏆 Resumen de Resultados:")
    print("=" * 70)
    for result in results:
        print(f"{result['model'].upper():5s} -> AUC: {result['auc']:.4f}, "
              f"Accuracy: {result['accuracy']:.4f}, F1: {result['f1']:.4f}")

    # Mejor modelo
    best_model = max(results, key=lambda x: x['auc'])
    print(f"\n✅ Mejor modelo: {best_model['model'].upper()} con AUC={best_model['auc']:.4f}")

    return best_model['model']

def train_final_model(spark, df, model_type="gbt"):
    """Entrena modelo final optimizado y guarda predicciones"""
    print(f"\n🎯 Entrenando modelo final: {model_type.upper()}")

    mlflow.set_experiment("Lead_Scoring_Production")

    with mlflow.start_run(run_name=f"Production_{model_type.upper()}"):
        # Split data
        train, test = df.randomSplit([0.8, 0.2], seed=42)

        # Build y entrenar
        pipeline = build_ml_pipeline(model_type=model_type)
        model = pipeline.fit(train)

        # Predicciones
        predictions = model.transform(test)

        # Evaluar
        metrics = evaluate_model(predictions, model_name=f"FINAL-{model_type.upper()}")

        # Log en MLflow
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("is_production", True)

        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)

        # Guardar modelo
        mlflow.spark.log_model(model, "lead_scoring_production_model")

        # Guardar predicciones en Parquet
        output_parquet = "data/lead_predictions.parquet"
        predictions.write.mode("overwrite").parquet(output_parquet)
        print(f"\n💾 Predicciones guardadas en: {output_parquet}")

        # Guardar en PostgreSQL (opcional)
        save_predictions_to_postgres(predictions)

        print(f"\n✅ Modelo de producción entrenado exitosamente")
        print(f"   MLflow Run ID: {mlflow.active_run().info.run_id}")

    return model, predictions

def main():
    """Función principal"""
    print("🚀 Iniciando Lead Scoring con Spark MLlib + MLflow")
    print("=" * 70)

    # Configurar MLflow
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    print(f"📊 MLflow Tracking URI: {mlflow_tracking_uri}")

    # Crear sesión
    spark = create_spark_session()

    try:
        # 1. Cargar y analizar datos
        df = load_and_analyze_data(spark)

        # 2. Comparar modelos
        best_model_type = train_and_compare_models(spark, df)

        # 3. Entrenar modelo final
        model, predictions = train_final_model(spark, df, model_type=best_model_type)

        print("\n🎉 Proceso completado exitosamente!")
        print(f"\n💡 Siguiente paso:")
        print(f"   1. Visualiza experimentos en MLflow: {mlflow_tracking_uri}")
        print(f"   2. Las predicciones están listas para servir via FastAPI")
        print(f"   3. Continúa con el módulo 04-FastAPI-Serving")

    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
