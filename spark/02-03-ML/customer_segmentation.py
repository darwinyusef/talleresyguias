"""
Customer Segmentation usando Spark MLlib + MLflow
=================================================
Clustering no supervisado para identificar segmentos de clientes
basado en comportamiento y características demográficas.

Técnicas:
- K-Means Clustering
- StandardScaler para normalización
- Elbow Method para selección de K óptimo
- Análisis de clusters con estadísticas descriptivas
- Tracking de experimentos con MLflow
"""

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans, BisectingKMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql.functions import col, avg, count, min, max, stddev
import mlflow
import mlflow.spark
import os

def create_spark_session():
    """Crea sesión de Spark optimizada para ML"""
    return SparkSession.builder \
        .appName("CustomerSegmentation-KMeans") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.shuffle.partitions", "8") \
        .getOrCreate()

def load_and_prepare_data(spark, input_path="data/lead_conversions.csv"):
    """Carga y prepara datos para clustering"""
    print(f"📖 Cargando datos desde: {input_path}")

    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Remover filas con valores nulos en features importantes
    df_clean = df.dropna(subset=["age", "salary", "web_visits"])

    print(f"✅ Datos cargados: {df_clean.count()} filas")
    print("\n📊 Estadísticas descriptivas:")
    df_clean.select("age", "salary", "web_visits").describe().show()

    return df_clean

def build_clustering_pipeline(k=3, use_bisecting=False):
    """Construye pipeline de clustering con preprocesamiento"""

    # Features para clustering
    feature_cols = ["age", "salary", "web_visits"]

    # 1. Vector Assembler
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="unscaled_features",
        handleInvalid="skip"
    )

    # 2. StandardScaler (CRÍTICO para K-Means)
    # Sin escalar, 'salary' dominaría por su rango mayor
    scaler = StandardScaler(
        inputCol="unscaled_features",
        outputCol="features",
        withStd=True,
        withMean=False  # False para sparse vectors
    )

    # 3. Clustering Algorithm
    if use_bisecting:
        clusterer = BisectingKMeans(k=k, seed=42, maxIter=20)
    else:
        clusterer = KMeans(k=k, seed=42, maxIter=20)

    # Pipeline completo
    pipeline = Pipeline(stages=[assembler, scaler, clusterer])

    return pipeline

def analyze_clusters(predictions_df, k):
    """Analiza las características de cada cluster"""
    print(f"\n📊 Análisis de Clusters (K={k}):")
    print("=" * 70)

    # Distribución de clientes por cluster
    cluster_distribution = predictions_df.groupBy("prediction") \
        .agg(count("*").alias("num_customers")) \
        .orderBy("prediction")

    print("\n🔢 Distribución de clientes:")
    cluster_distribution.show()

    # Características promedio por cluster
    cluster_stats = predictions_df.groupBy("prediction").agg(
        avg("age").alias("avg_age"),
        avg("salary").alias("avg_salary"),
        avg("web_visits").alias("avg_web_visits"),
        count("*").alias("count")
    ).orderBy("prediction")

    print("\n📈 Perfil de cada cluster:")
    cluster_stats.show(truncate=False)

    # Interpretar clusters
    print("\n💡 Interpretación de Clusters:")
    for row in cluster_stats.collect():
        cluster_id = row['prediction']
        avg_age = row['avg_age']
        avg_salary = row['avg_salary']
        avg_visits = row['avg_web_visits']

        # Clasificar cluster
        if avg_salary > 80000:
            segment = "Premium (Alto valor)"
        elif avg_visits > 30:
            segment = "Engagement Alto (Potencial)"
        elif avg_age < 30:
            segment = "Jóvenes (Growth)"
        else:
            segment = "Regular (Nurturing)"

        print(f"   Cluster {cluster_id}: {segment}")
        print(f"      - Edad promedio: {avg_age:.1f} años")
        print(f"      - Salario promedio: ${avg_salary:,.0f}")
        print(f"      - Visitas promedio: {avg_visits:.1f}")
        print()

    return cluster_stats

def elbow_method(spark, df, k_range=range(2, 8)):
    """Implementa Elbow Method para encontrar K óptimo"""
    print("\n🔍 Ejecutando Elbow Method para encontrar K óptimo...")
    print("=" * 70)

    mlflow.set_experiment("Customer_Segmentation_Elbow")

    results = []

    for k in k_range:
        with mlflow.start_run(run_name=f"Elbow_K={k}"):
            # Entrenar modelo
            pipeline = build_clustering_pipeline(k=k)
            model = pipeline.fit(df)
            predictions = model.transform(df)

            # Evaluar
            evaluator = ClusteringEvaluator(
                predictionCol="prediction",
                featuresCol="features",
                metricName="silhouette"
            )
            silhouette = evaluator.evaluate(predictions)

            # Obtener WSSSE (Within Set Sum of Squared Errors)
            kmeans_model = model.stages[-1]
            wssse = kmeans_model.summary.trainingCost

            # Log en MLflow
            mlflow.log_param("k", k)
            mlflow.log_metric("silhouette_score", silhouette)
            mlflow.log_metric("wssse", wssse)

            results.append({
                'k': k,
                'silhouette': silhouette,
                'wssse': wssse
            })

            print(f"K={k} -> Silhouette: {silhouette:.4f}, WSSSE: {wssse:.2f}")

    # Encontrar mejor K (mayor silhouette)
    best_result = max(results, key=lambda x: x['silhouette'])
    print(f"\n✅ Mejor K={best_result['k']} con Silhouette={best_result['silhouette']:.4f}")

    return best_result['k']

def train_final_model(spark, df, k):
    """Entrena modelo final con K óptimo y lo registra en MLflow"""
    print(f"\n🎯 Entrenando modelo final con K={k}...")

    mlflow.set_experiment("Customer_Segmentation_Final")

    with mlflow.start_run(run_name=f"Final_KMeans_K={k}"):
        # Build y entrenar pipeline
        pipeline = build_clustering_pipeline(k=k)
        model = pipeline.fit(df)

        # Predicciones
        predictions = model.transform(df)

        # Evaluación
        evaluator = ClusteringEvaluator()
        silhouette = evaluator.evaluate(predictions)

        # Análisis detallado
        cluster_stats = analyze_clusters(predictions, k)

        # Log en MLflow
        mlflow.log_param("k", k)
        mlflow.log_param("algorithm", "KMeans")
        mlflow.log_param("max_iter", 20)
        mlflow.log_metric("silhouette_score", silhouette)

        # Guardar modelo
        mlflow.spark.log_model(model, "customer_segmentation_model")

        # Guardar predicciones
        output_path = "data/customer_segments.parquet"
        predictions.write.mode("overwrite").parquet(output_path)
        print(f"\n💾 Segmentos guardados en: {output_path}")

        print(f"\n✅ Modelo entrenado exitosamente")
        print(f"   Silhouette Score: {silhouette:.4f}")
        print(f"   MLflow Run ID: {mlflow.active_run().info.run_id}")

    return model, predictions

def main():
    """Función principal"""
    print("🚀 Iniciando Customer Segmentation con Spark MLlib + MLflow")
    print("=" * 70)

    # Configurar MLflow (opcional: usar servidor remoto)
    mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    print(f"📊 MLflow Tracking URI: {mlflow_tracking_uri}")

    # Crear sesión
    spark = create_spark_session()

    try:
        # 1. Cargar datos
        df = load_and_prepare_data(spark)

        # 2. Elbow Method (encontrar K óptimo)
        best_k = elbow_method(spark, df, k_range=range(2, 7))

        # 3. Entrenar modelo final
        model, predictions = train_final_model(spark, df, k=best_k)

        print("\n🎉 Proceso completado exitosamente!")
        print(f"\n💡 Siguiente paso: Visualiza los resultados en MLflow UI:")
        print(f"   {mlflow_tracking_uri}")

    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
