# Taller FastMCP + Spark + ML Pipeline + Airflow + MLOps

## Tabla de Contenidos

1. [Introducción a MLOps con FastMCP](#1-introducción-a-mlops-con-fastmcp)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [FastMCP + Spark Integration](#3-fastmcp--spark-integration)
4. [Feature Store con Feast](#4-feature-store-con-feast)
5. [ML Pipeline con MLflow](#5-ml-pipeline-con-mlflow)
6. [Orquestación con Airflow](#6-orquestación-con-airflow)
7. [Model Registry y Versioning](#7-model-registry-y-versioning)
8. [Deployment de Modelos](#8-deployment-de-modelos)
9. [Monitoring y Retraining](#9-monitoring-y-retraining)
10. [A/B Testing y Experimentación](#10-ab-testing-y-experimentación)
11. [Integración con MCPs Populares](#11-integración-con-mcps-populares)
12. [CI/CD para ML](#12-cicd-para-ml)

---

## 1. Introducción a MLOps con FastMCP

### 1.1 ¿Qué es MLOps?

MLOps (Machine Learning Operations) es la práctica de aplicar principios DevOps al ciclo de vida del Machine Learning:

- **Data Engineering**: Ingesta, transformación, validación
- **Feature Engineering**: Feature stores, transformaciones
- **Model Training**: Experimentación, hyperparameter tuning
- **Model Registry**: Versionado, metadata, lineage
- **Deployment**: Serving, APIs, batch inference
- **Monitoring**: Performance, drift, retraining

### 1.2 Stack Tecnológico

```
┌─────────────────────────────────────────────────────────┐
│              MLOps Platform con FastMCP                 │
└─────────────────────────────────────────────────────────┘

Data Layer:
- Apache Spark (procesamiento distribuido)
- Delta Lake (data lakehouse)
- Feast (feature store)

ML Layer:
- MLflow (experiment tracking, model registry)
- scikit-learn, PyTorch, TensorFlow
- Optuna (hyperparameter optimization)

Orchestration:
- Apache Airflow (workflow orchestration)
- FastMCP (tool integration)

Serving:
- FastAPI (model serving)
- Seldon Core / BentoML
- Redis (caching)

Monitoring:
- Prometheus + Grafana
- Evidently (model monitoring)
- Great Expectations (data quality)
```

---

## 2. Arquitectura del Sistema

```
┌────────────────────────────────────────────────────────────────┐
│                    MLOps Architecture                          │
└────────────────────────────────────────────────────────────────┘

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Claude    │────▶│   FastMCP   │────▶│   Airflow   │
│  Desktop    │     │   Server    │     │    DAGs     │
└─────────────┘     └──────┬──────┘     └──────┬──────┘
                           │                    │
                    ┌──────┴──────┐            │
                    │             │            │
              ┌─────▼─────┐ ┌────▼────┐       │
              │   Spark   │ │ MLflow  │       │
              │  Cluster  │ │ Tracking│       │
              └─────┬─────┘ └────┬────┘       │
                    │            │            │
              ┌─────▼─────┐      │            │
              │   Feast   │      │            │
              │  Feature  │      │            │
              │   Store   │      │            │
              └─────┬─────┘      │            │
                    │            │            │
       ┌────────────┼────────────┼────────────┘
       │            │            │
  ┌────▼────┐  ┌───▼───┐   ┌────▼────┐
  │ Delta   │  │Model  │   │ Model   │
  │  Lake   │  │Registry   │ Serving │
  └─────────┘  └───────┘   └─────────┘
       │                         │
  ┌────▼────┐              ┌────▼────┐
  │   S3    │              │ Redis   │
  │ MinIO   │              │ Cache   │
  └─────────┘              └─────────┘
```

---

## 3. FastMCP + Spark Integration

### 3.1 Servidor FastMCP para Spark

```python
# mcp_servers/spark_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import json

mcp = FastMCP("Spark Data Processing Server")

# Spark Session
spark = None

def get_spark_session():
    """Obtiene o crea Spark Session"""
    global spark
    if spark is None:
        spark = SparkSession.builder \
            .appName("FastMCP-MLOps") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
            .master("local[*]") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("WARN")

    return spark

@mcp.tool()
async def load_data_to_spark(
    source_path: str,
    format: str = "parquet",
    options: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Carga datos en Spark DataFrame

    Args:
        source_path: Ruta de los datos (S3, local, etc)
        format: Formato (parquet, csv, delta, json)
        options: Opciones de lectura
    """
    spark = get_spark_session()

    try:
        reader = spark.read.format(format)

        if options:
            for key, value in options.items():
                reader = reader.option(key, value)

        df = reader.load(source_path)

        # Registrar como tabla temporal
        table_name = f"data_{source_path.replace('/', '_').replace('.', '_')}"
        df.createOrReplaceTempView(table_name)

        return {
            "success": True,
            "source_path": source_path,
            "format": format,
            "table_name": table_name,
            "row_count": df.count(),
            "columns": df.columns,
            "schema": df.schema.json()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def run_spark_sql(
    query: str,
    output_path: Optional[str] = None,
    output_format: str = "delta"
) -> Dict[str, Any]:
    """
    Ejecuta query SQL en Spark

    Args:
        query: SQL query
        output_path: Ruta de salida (opcional)
        output_format: Formato de salida
    """
    spark = get_spark_session()

    try:
        result_df = spark.sql(query)

        response = {
            "success": True,
            "query": query,
            "row_count": result_df.count(),
            "columns": result_df.columns
        }

        # Guardar si se especifica output_path
        if output_path:
            result_df.write \
                .format(output_format) \
                .mode("overwrite") \
                .save(output_path)

            response["output_path"] = output_path
            response["output_format"] = output_format
        else:
            # Retornar muestra de datos
            sample = result_df.limit(10).toPandas().to_dict(orient='records')
            response["sample"] = sample

        return response
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_features_spark(
    input_table: str,
    transformations: List[Dict[str, Any]],
    output_path: str
) -> Dict[str, Any]:
    """
    Crea features usando Spark

    Args:
        input_table: Tabla de entrada
        transformations: Lista de transformaciones
        output_path: Ruta de salida
    """
    spark = get_spark_session()

    try:
        df = spark.table(input_table)

        # Aplicar transformaciones
        for transform in transformations:
            transform_type = transform.get("type")

            if transform_type == "select":
                df = df.select(*transform["columns"])

            elif transform_type == "filter":
                df = df.filter(transform["condition"])

            elif transform_type == "aggregate":
                group_cols = transform["group_by"]
                agg_exprs = transform["aggregations"]
                df = df.groupBy(*group_cols).agg(*[
                    F.expr(expr) for expr in agg_exprs
                ])

            elif transform_type == "join":
                right_table = spark.table(transform["right_table"])
                df = df.join(
                    right_table,
                    on=transform["on"],
                    how=transform.get("how", "inner")
                )

            elif transform_type == "add_column":
                df = df.withColumn(
                    transform["column_name"],
                    F.expr(transform["expression"])
                )

        # Guardar features
        df.write \
            .format("delta") \
            .mode("overwrite") \
            .save(output_path)

        return {
            "success": True,
            "input_table": input_table,
            "transformations_applied": len(transformations),
            "output_path": output_path,
            "row_count": df.count(),
            "columns": df.columns
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def train_test_split_spark(
    input_path: str,
    train_path: str,
    test_path: str,
    train_ratio: float = 0.8,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Split dataset en train/test usando Spark

    Args:
        input_path: Datos de entrada
        train_path: Ruta para datos de entrenamiento
        test_path: Ruta para datos de test
        train_ratio: Ratio de train
        seed: Semilla aleatoria
    """
    spark = get_spark_session()

    try:
        df = spark.read.format("delta").load(input_path)

        # Split
        train_df, test_df = df.randomSplit(
            [train_ratio, 1 - train_ratio],
            seed=seed
        )

        # Guardar
        train_df.write.format("delta").mode("overwrite").save(train_path)
        test_df.write.format("delta").mode("overwrite").save(test_path)

        return {
            "success": True,
            "input_path": input_path,
            "train_path": train_path,
            "test_path": test_path,
            "train_count": train_df.count(),
            "test_count": test_df.count(),
            "train_ratio": train_ratio
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_data_statistics(
    table_name: str
) -> Dict[str, Any]:
    """
    Calcula estadísticas de datos usando Spark

    Args:
        table_name: Nombre de la tabla
    """
    spark = get_spark_session()

    try:
        df = spark.table(table_name)

        # Estadísticas básicas
        stats = df.describe().toPandas().to_dict(orient='records')

        # Info adicional
        null_counts = df.select([
            F.count(F.when(F.col(c).isNull(), c)).alias(c)
            for c in df.columns
        ]).toPandas().to_dict(orient='records')[0]

        return {
            "success": True,
            "table_name": table_name,
            "row_count": df.count(),
            "column_count": len(df.columns),
            "columns": df.columns,
            "statistics": stats,
            "null_counts": null_counts
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

### 3.2 Data Quality con Great Expectations

```python
# mcp_servers/data_quality_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest
import json

mcp = FastMCP("Data Quality Server")

# Context de Great Expectations
context = None

def get_gx_context():
    """Obtiene Great Expectations context"""
    global context
    if context is None:
        context = gx.get_context()
    return context

@mcp.tool()
async def validate_data_quality(
    data_path: str,
    expectations: List[Dict[str, Any]],
    data_format: str = "parquet"
) -> Dict[str, Any]:
    """
    Valida calidad de datos con Great Expectations

    Args:
        data_path: Ruta de los datos
        expectations: Lista de expectativas
        data_format: Formato de datos
    """
    try:
        context = get_gx_context()

        # Crear datasource
        datasource = context.sources.add_or_update_pandas(name="pandas_datasource")

        # Cargar datos
        import pandas as pd
        if data_format == "parquet":
            df = pd.read_parquet(data_path)
        elif data_format == "csv":
            df = pd.read_csv(data_path)
        else:
            return {"success": False, "error": f"Unsupported format: {data_format}"}

        # Crear batch
        data_asset = datasource.add_dataframe_asset(name="dataframe_asset")
        batch_request = data_asset.build_batch_request(dataframe=df)

        # Crear expectation suite
        suite_name = f"validation_suite_{data_path.replace('/', '_')}"
        suite = context.add_expectation_suite(suite_name)

        # Agregar expectations
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=suite_name
        )

        results = []
        for exp in expectations:
            exp_type = exp.get("type")

            if exp_type == "expect_column_values_to_not_be_null":
                result = validator.expect_column_values_to_not_be_null(
                    column=exp["column"]
                )
                results.append(result.to_json_dict())

            elif exp_type == "expect_column_values_to_be_between":
                result = validator.expect_column_values_to_be_between(
                    column=exp["column"],
                    min_value=exp["min"],
                    max_value=exp["max"]
                )
                results.append(result.to_json_dict())

            elif exp_type == "expect_column_values_to_be_in_set":
                result = validator.expect_column_values_to_be_in_set(
                    column=exp["column"],
                    value_set=exp["values"]
                )
                results.append(result.to_json_dict())

        # Validar
        validation_result = validator.validate()

        return {
            "success": validation_result.success,
            "data_path": data_path,
            "expectations_tested": len(expectations),
            "expectations_passed": sum(1 for r in results if r.get("success")),
            "results": results,
            "statistics": validation_result.statistics
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 4. Feature Store con Feast

### 4.1 Configuración de Feast

```python
# feature_store/feature_definitions.py
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String
from datetime import timedelta

# Definir entidades
user_entity = Entity(
    name="user_id",
    description="User ID",
    value_type=String
)

product_entity = Entity(
    name="product_id",
    description="Product ID",
    value_type=String
)

# Feature sources
user_features_source = FileSource(
    path="data/user_features.parquet",
    timestamp_field="event_timestamp"
)

product_features_source = FileSource(
    path="data/product_features.parquet",
    timestamp_field="event_timestamp"
)

# Feature views
user_features_view = FeatureView(
    name="user_features",
    entities=[user_entity],
    ttl=timedelta(days=1),
    schema=[
        Field(name="age", dtype=Int64),
        Field(name="total_purchases", dtype=Int64),
        Field(name="avg_purchase_value", dtype=Float32),
        Field(name="days_since_last_purchase", dtype=Int64),
        Field(name="favorite_category", dtype=String),
    ],
    online=True,
    source=user_features_source
)

product_features_view = FeatureView(
    name="product_features",
    entities=[product_entity],
    ttl=timedelta(days=1),
    schema=[
        Field(name="price", dtype=Float32),
        Field(name="category", dtype=String),
        Field(name="avg_rating", dtype=Float32),
        Field(name="total_reviews", dtype=Int64),
        Field(name="stock_quantity", dtype=Int64),
    ],
    online=True,
    source=product_features_source
)
```

### 4.2 Servidor FastMCP para Feast

```python
# mcp_servers/feast_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List
from feast import FeatureStore
import pandas as pd
from datetime import datetime

mcp = FastMCP("Feast Feature Store Server")

# Feature Store
fs = FeatureStore(repo_path="feature_store/")

@mcp.tool()
async def get_online_features(
    entities: Dict[str, List[str]],
    features: List[str]
) -> Dict[str, Any]:
    """
    Obtiene features en tiempo real desde Feast

    Args:
        entities: Diccionario de entidades {entity_name: [values]}
        features: Lista de features a obtener
    """
    try:
        # Obtener features
        feature_vector = fs.get_online_features(
            entity_rows=[entities],
            features=features
        ).to_dict()

        return {
            "success": True,
            "entities": entities,
            "features_requested": features,
            "feature_vector": feature_vector
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_historical_features(
    entity_df_path: str,
    features: List[str],
    output_path: str
) -> Dict[str, Any]:
    """
    Obtiene features históricos para training

    Args:
        entity_df_path: Ruta del DataFrame con entidades y timestamps
        features: Lista de features
        output_path: Ruta de salida
    """
    try:
        # Cargar entity DataFrame
        entity_df = pd.read_parquet(entity_df_path)

        # Obtener features históricos
        training_df = fs.get_historical_features(
            entity_df=entity_df,
            features=features
        ).to_df()

        # Guardar
        training_df.to_parquet(output_path)

        return {
            "success": True,
            "entity_df_path": entity_df_path,
            "features_requested": len(features),
            "output_path": output_path,
            "rows_generated": len(training_df),
            "columns": list(training_df.columns)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def materialize_features(
    start_date: str,
    end_date: str,
    feature_views: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Materializa features al online store

    Args:
        start_date: Fecha inicio (ISO format)
        end_date: Fecha fin (ISO format)
        feature_views: Feature views a materializar
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)

        # Materializar
        fs.materialize(
            start_date=start,
            end_date=end,
            feature_views=feature_views
        )

        return {
            "success": True,
            "start_date": start_date,
            "end_date": end_date,
            "feature_views": feature_views or "all"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 5. ML Pipeline con MLflow

### 5.1 Servidor FastMCP para MLflow

```python
# mcp_servers/mlflow_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import numpy as np
import json

mcp = FastMCP("MLflow Training Server")

# Configurar MLflow
mlflow.set_tracking_uri("http://localhost:5000")

@mcp.tool()
async def train_model(
    experiment_name: str,
    model_type: str,
    train_data_path: str,
    target_column: str,
    hyperparameters: Dict[str, Any],
    tags: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Entrena un modelo de ML con MLflow tracking

    Args:
        experiment_name: Nombre del experimento
        model_type: Tipo de modelo (random_forest, gradient_boosting, logistic_regression)
        train_data_path: Ruta de datos de entrenamiento
        target_column: Columna target
        hyperparameters: Hiperparámetros del modelo
        tags: Tags adicionales
    """
    try:
        # Configurar experimento
        mlflow.set_experiment(experiment_name)

        # Cargar datos
        df = pd.read_parquet(train_data_path)
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Split train/val
        from sklearn.model_selection import train_test_split
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        with mlflow.start_run(tags=tags or {}) as run:
            # Log parámetros
            mlflow.log_params(hyperparameters)
            mlflow.log_param("model_type", model_type)
            mlflow.log_param("train_samples", len(X_train))
            mlflow.log_param("val_samples", len(X_val))

            # Crear modelo
            if model_type == "random_forest":
                model = RandomForestClassifier(**hyperparameters)
            elif model_type == "gradient_boosting":
                model = GradientBoostingClassifier(**hyperparameters)
            elif model_type == "logistic_regression":
                model = LogisticRegression(**hyperparameters)
            else:
                return {"success": False, "error": f"Unknown model type: {model_type}"}

            # Entrenar
            model.fit(X_train, y_train)

            # Evaluar
            y_pred_train = model.predict(X_train)
            y_pred_val = model.predict(X_val)

            # Métricas
            metrics = {
                "train_accuracy": accuracy_score(y_train, y_pred_train),
                "val_accuracy": accuracy_score(y_val, y_pred_val),
                "val_precision": precision_score(y_val, y_pred_val, average='weighted'),
                "val_recall": recall_score(y_val, y_pred_val, average='weighted'),
                "val_f1": f1_score(y_val, y_pred_val, average='weighted')
            }

            # Log métricas
            mlflow.log_metrics(metrics)

            # Log modelo
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=f"{experiment_name}_{model_type}"
            )

            # Log feature importance si está disponible
            if hasattr(model, 'feature_importances_'):
                feature_importance = pd.DataFrame({
                    'feature': X.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)

                mlflow.log_table(feature_importance, "feature_importance.json")

            return {
                "success": True,
                "experiment_name": experiment_name,
                "run_id": run.info.run_id,
                "model_type": model_type,
                "metrics": metrics,
                "artifact_uri": run.info.artifact_uri
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def hyperparameter_tuning(
    experiment_name: str,
    model_type: str,
    train_data_path: str,
    target_column: str,
    param_space: Dict[str, List[Any]],
    n_trials: int = 20
) -> Dict[str, Any]:
    """
    Optimización de hiperparámetros con Optuna

    Args:
        experiment_name: Nombre del experimento
        model_type: Tipo de modelo
        train_data_path: Ruta de datos
        target_column: Columna target
        param_space: Espacio de búsqueda de parámetros
        n_trials: Número de trials
    """
    try:
        import optuna
        from optuna.integration.mlflow import MLflowCallback

        # Cargar datos
        df = pd.read_parquet(train_data_path)
        X = df.drop(columns=[target_column])
        y = df[target_column]

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        def objective(trial):
            # Samplear hiperparámetros
            params = {}
            for param_name, param_range in param_space.items():
                if isinstance(param_range[0], int):
                    params[param_name] = trial.suggest_int(
                        param_name, param_range[0], param_range[1]
                    )
                elif isinstance(param_range[0], float):
                    params[param_name] = trial.suggest_float(
                        param_name, param_range[0], param_range[1]
                    )
                else:
                    params[param_name] = trial.suggest_categorical(
                        param_name, param_range
                    )

            # Crear y entrenar modelo
            if model_type == "random_forest":
                model = RandomForestClassifier(**params, random_state=42)
            elif model_type == "gradient_boosting":
                model = GradientBoostingClassifier(**params, random_state=42)
            else:
                model = LogisticRegression(**params, random_state=42)

            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)

            return f1_score(y_val, y_pred, average='weighted')

        # Configurar Optuna
        mlflow.set_experiment(f"{experiment_name}_tuning")
        mlflc = MLflowCallback(
            tracking_uri="http://localhost:5000",
            metric_name="f1_score"
        )

        study = optuna.create_study(
            direction="maximize",
            study_name=f"{experiment_name}_{model_type}_tuning"
        )

        study.optimize(objective, n_trials=n_trials, callbacks=[mlflc])

        return {
            "success": True,
            "experiment_name": experiment_name,
            "model_type": model_type,
            "n_trials": n_trials,
            "best_params": study.best_params,
            "best_score": study.best_value,
            "optimization_history": [
                {"trial": i, "value": trial.value}
                for i, trial in enumerate(study.trials)
            ]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def register_model(
    model_name: str,
    run_id: str,
    stage: str = "Staging"
) -> Dict[str, Any]:
    """
    Registra modelo en MLflow Model Registry

    Args:
        model_name: Nombre del modelo
        run_id: ID del run
        stage: Stage (Staging, Production, Archived)
    """
    try:
        client = mlflow.tracking.MlflowClient()

        # Obtener model URI
        model_uri = f"runs:/{run_id}/model"

        # Registrar
        model_details = mlflow.register_model(
            model_uri=model_uri,
            name=model_name
        )

        # Transicionar a stage
        client.transition_model_version_stage(
            name=model_name,
            version=model_details.version,
            stage=stage
        )

        return {
            "success": True,
            "model_name": model_name,
            "version": model_details.version,
            "stage": stage,
            "run_id": run_id
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def compare_models(
    experiment_name: str,
    metric: str = "val_f1",
    top_n: int = 5
) -> Dict[str, Any]:
    """
    Compara modelos de un experimento

    Args:
        experiment_name: Nombre del experimento
        metric: Métrica para comparar
        top_n: Top N modelos
    """
    try:
        # Buscar experimento
        experiment = mlflow.get_experiment_by_name(experiment_name)

        if not experiment:
            return {"success": False, "error": "Experiment not found"}

        # Obtener runs
        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=[f"metrics.{metric} DESC"],
            max_results=top_n
        )

        comparison = []
        for _, run in runs.iterrows():
            comparison.append({
                "run_id": run['run_id'],
                "start_time": str(run['start_time']),
                "model_type": run.get('params.model_type', 'unknown'),
                metric: run.get(f'metrics.{metric}', None),
                "parameters": {
                    k.replace('params.', ''): v
                    for k, v in run.items()
                    if k.startswith('params.')
                }
            })

        return {
            "success": True,
            "experiment_name": experiment_name,
            "metric": metric,
            "top_models": comparison
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 6. Orquestación con Airflow

### 6.1 DAG de ML Pipeline Completo

```python
# airflow/dags/ml_pipeline_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_pipeline_complete',
    default_args=default_args,
    description='Complete ML Pipeline with FastMCP',
    schedule_interval='@daily',
    catchup=False
)

async def call_mcp_tool(server_path, tool_name, arguments):
    """Helper para llamar tools MCP"""
    params = StdioServerParameters(
        command="python",
        args=[server_path]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            return result.content[0].text if result.content else None

def data_ingestion(**context):
    """Task 1: Ingestión de datos"""
    result = asyncio.run(call_mcp_tool(
        "mcp_servers/spark_server.py",
        "load_data_to_spark",
        {
            "source_path": "s3://data-lake/raw/daily_data.parquet",
            "format": "parquet"
        }
    ))

    context['ti'].xcom_push(key='data_table', value=result)
    return result

def data_quality_check(**context):
    """Task 2: Validación de calidad"""
    result = asyncio.run(call_mcp_tool(
        "mcp_servers/data_quality_server.py",
        "validate_data_quality",
        {
            "data_path": "s3://data-lake/raw/daily_data.parquet",
            "expectations": [
                {"type": "expect_column_values_to_not_be_null", "column": "user_id"},
                {"type": "expect_column_values_to_be_between", "column": "age", "min": 0, "max": 120},
                {"type": "expect_column_values_to_be_in_set", "column": "country", "values": ["US", "UK", "CA"]}
            ],
            "data_format": "parquet"
        }
    ))

    import json
    validation = json.loads(result)

    if not validation.get("success"):
        raise ValueError("Data quality check failed!")

    return result

def feature_engineering(**context):
    """Task 3: Feature engineering con Spark"""
    table_name = context['ti'].xcom_pull(key='data_table', task_ids='data_ingestion')

    result = asyncio.run(call_mcp_tool(
        "mcp_servers/spark_server.py",
        "create_features_spark",
        {
            "input_table": table_name,
            "transformations": [
                {
                    "type": "add_column",
                    "column_name": "age_group",
                    "expression": "CASE WHEN age < 25 THEN '18-24' WHEN age < 35 THEN '25-34' WHEN age < 50 THEN '35-49' ELSE '50+' END"
                },
                {
                    "type": "add_column",
                    "column_name": "purchase_frequency",
                    "expression": "total_purchases / DATEDIFF(current_date(), registration_date)"
                }
            ],
            "output_path": "s3://data-lake/features/user_features"
        }
    ))

    return result

def materialize_features(**context):
    """Task 4: Materializar features en Feast"""
    from datetime import datetime, timedelta

    result = asyncio.run(call_mcp_tool(
        "mcp_servers/feast_server.py",
        "materialize_features",
        {
            "start_date": (datetime.now() - timedelta(days=1)).isoformat(),
            "end_date": datetime.now().isoformat()
        }
    ))

    return result

def prepare_training_data(**context):
    """Task 5: Preparar datos de entrenamiento"""
    result = asyncio.run(call_mcp_tool(
        "mcp_servers/feast_server.py",
        "get_historical_features",
        {
            "entity_df_path": "s3://data-lake/entities/training_entities.parquet",
            "features": [
                "user_features:age",
                "user_features:total_purchases",
                "user_features:avg_purchase_value",
                "product_features:price",
                "product_features:category"
            ],
            "output_path": "s3://data-lake/training/features.parquet"
        }
    ))

    return result

def train_model(**context):
    """Task 6: Entrenar modelo"""
    result = asyncio.run(call_mcp_tool(
        "mcp_servers/mlflow_server.py",
        "train_model",
        {
            "experiment_name": "daily_recommendation_model",
            "model_type": "gradient_boosting",
            "train_data_path": "s3://data-lake/training/features.parquet",
            "target_column": "purchased",
            "hyperparameters": {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 5
            },
            "tags": {
                "pipeline": "airflow",
                "date": context['ds']
            }
        }
    ))

    import json
    training_result = json.loads(result)
    context['ti'].xcom_push(key='run_id', value=training_result['run_id'])

    return result

def evaluate_and_register(**context):
    """Task 7: Evaluar y registrar modelo"""
    run_id = context['ti'].xcom_pull(key='run_id', task_ids='train_model')

    result = asyncio.run(call_mcp_tool(
        "mcp_servers/mlflow_server.py",
        "register_model",
        {
            "model_name": "recommendation_model",
            "run_id": run_id,
            "stage": "Staging"
        }
    ))

    return result

def deploy_to_production(**context):
    """Task 8: Deploy a producción si pasa threshold"""
    import json

    # Obtener métricas del modelo
    run_id = context['ti'].xcom_pull(key='run_id', task_ids='train_model')

    # Lógica de promoción basada en métricas
    # Si val_f1 > 0.85, promover a Production

    result = asyncio.run(call_mcp_tool(
        "mcp_servers/model_serving_server.py",
        "deploy_model",
        {
            "model_name": "recommendation_model",
            "version": "latest",
            "environment": "production"
        }
    ))

    return result

# Definir tasks
task_1 = PythonOperator(
    task_id='data_ingestion',
    python_callable=data_ingestion,
    dag=dag
)

task_2 = PythonOperator(
    task_id='data_quality_check',
    python_callable=data_quality_check,
    dag=dag
)

task_3 = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering,
    dag=dag
)

task_4 = PythonOperator(
    task_id='materialize_features',
    python_callable=materialize_features,
    dag=dag
)

task_5 = PythonOperator(
    task_id='prepare_training_data',
    python_callable=prepare_training_data,
    dag=dag
)

task_6 = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

task_7 = PythonOperator(
    task_id='evaluate_and_register',
    python_callable=evaluate_and_register,
    dag=dag
)

task_8 = PythonOperator(
    task_id='deploy_to_production',
    python_callable=deploy_to_production,
    dag=dag
)

# Definir dependencias
task_1 >> task_2 >> task_3 >> task_4 >> task_5 >> task_6 >> task_7 >> task_8
```

### 6.2 DAG de Retraining Automático

```python
# airflow/dags/model_retraining_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
}

dag = DAG(
    'model_retraining',
    default_args=default_args,
    description='Automatic Model Retraining based on Performance',
    schedule_interval='@weekly',
    catchup=False
)

def check_model_drift(**context):
    """Detectar drift en el modelo"""
    result = asyncio.run(call_mcp_tool(
        "mcp_servers/monitoring_server.py",
        "detect_model_drift",
        {
            "model_name": "recommendation_model",
            "reference_data_path": "s3://data-lake/reference/baseline.parquet",
            "current_data_path": "s3://data-lake/current/predictions.parquet",
            "threshold": 0.1
        }
    ))

    import json
    drift_result = json.loads(result)

    if drift_result.get("drift_detected"):
        return "trigger_retraining"
    else:
        return "skip_retraining"

def trigger_retraining(**context):
    """Trigger del pipeline de entrenamiento"""
    from airflow.api.common.experimental.trigger_dag import trigger_dag

    trigger_dag(
        dag_id='ml_pipeline_complete',
        run_id=f"retraining_{context['ds']}",
        conf={"retraining": True}
    )

# Tasks
check_drift_task = PythonOperator(
    task_id='check_model_drift',
    python_callable=check_model_drift,
    dag=dag
)

retrain_task = PythonOperator(
    task_id='trigger_retraining',
    python_callable=trigger_retraining,
    dag=dag
)

check_drift_task >> retrain_task
```

---

## 7. Model Registry y Versioning

### 7.1 Servidor FastMCP para Model Registry

```python
# mcp_servers/model_registry_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime

mcp = FastMCP("Model Registry Server")

client = MlflowClient()

@mcp.tool()
async def list_registered_models(
    filter_string: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista modelos registrados

    Args:
        filter_string: Filtro opcional
    """
    try:
        models = client.search_registered_models(filter_string=filter_string)

        model_list = []
        for model in models:
            latest_versions = client.get_latest_versions(model.name)

            model_list.append({
                "name": model.name,
                "creation_timestamp": model.creation_timestamp,
                "last_updated_timestamp": model.last_updated_timestamp,
                "description": model.description,
                "latest_versions": [
                    {
                        "version": v.version,
                        "stage": v.current_stage,
                        "run_id": v.run_id
                    }
                    for v in latest_versions
                ]
            })

        return {
            "success": True,
            "models": model_list,
            "count": len(model_list)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_model_version_details(
    model_name: str,
    version: str
) -> Dict[str, Any]:
    """
    Obtiene detalles de una versión específica

    Args:
        model_name: Nombre del modelo
        version: Versión del modelo
    """
    try:
        model_version = client.get_model_version(model_name, version)

        # Obtener run info
        run = client.get_run(model_version.run_id)

        return {
            "success": True,
            "model_name": model_name,
            "version": version,
            "stage": model_version.current_stage,
            "description": model_version.description,
            "run_id": model_version.run_id,
            "creation_timestamp": model_version.creation_timestamp,
            "metrics": run.data.metrics,
            "params": run.data.params,
            "tags": run.data.tags
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def transition_model_stage(
    model_name: str,
    version: str,
    stage: str,
    archive_existing: bool = True
) -> Dict[str, Any]:
    """
    Transiciona modelo a un stage diferente

    Args:
        model_name: Nombre del modelo
        version: Versión
        stage: Nuevo stage (Staging, Production, Archived)
        archive_existing: Archivar versiones existentes en el stage
    """
    try:
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage,
            archive_existing_versions=archive_existing
        )

        return {
            "success": True,
            "model_name": model_name,
            "version": version,
            "new_stage": stage
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def update_model_description(
    model_name: str,
    version: str,
    description: str
) -> Dict[str, Any]:
    """
    Actualiza descripción del modelo

    Args:
        model_name: Nombre del modelo
        version: Versión
        description: Nueva descripción
    """
    try:
        client.update_model_version(
            name=model_name,
            version=version,
            description=description
        )

        return {
            "success": True,
            "model_name": model_name,
            "version": version,
            "description": description
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def delete_model_version(
    model_name: str,
    version: str
) -> Dict[str, Any]:
    """
    Elimina una versión del modelo

    Args:
        model_name: Nombre del modelo
        version: Versión a eliminar
    """
    try:
        client.delete_model_version(
            name=model_name,
            version=version
        )

        return {
            "success": True,
            "model_name": model_name,
            "version": version,
            "message": "Model version deleted"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 8. Deployment de Modelos

### 8.1 Servidor de Model Serving con FastAPI

```python
# serving/model_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import mlflow.pyfunc
import pandas as pd
import redis
import json
import hashlib

app = FastAPI(title="ML Model Serving API")

# Redis para caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Cargar modelo
current_model = None
model_version = None

class PredictionRequest(BaseModel):
    features: Dict[str, Any]
    use_cache: bool = True

class BatchPredictionRequest(BaseModel):
    instances: List[Dict[str, Any]]

def load_model(model_name: str, stage: str = "Production"):
    """Carga modelo desde MLflow"""
    global current_model, model_version

    model_uri = f"models:/{model_name}/{stage}"
    current_model = mlflow.pyfunc.load_model(model_uri)
    model_version = stage

    return current_model

@app.on_event("startup")
async def startup_event():
    """Cargar modelo al inicio"""
    load_model("recommendation_model", "Production")

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Predicción individual"""
    try:
        # Generar cache key
        cache_key = None
        if request.use_cache:
            cache_key = f"pred:{hashlib.md5(json.dumps(request.features, sort_keys=True).encode()).hexdigest()}"

            # Verificar cache
            cached = redis_client.get(cache_key)
            if cached:
                return {
                    "prediction": json.loads(cached),
                    "from_cache": True,
                    "model_version": model_version
                }

        # Hacer predicción
        input_df = pd.DataFrame([request.features])
        prediction = current_model.predict(input_df)[0]

        # Guardar en cache
        if cache_key:
            redis_client.setex(
                cache_key,
                3600,  # TTL 1 hora
                json.dumps(prediction.tolist() if hasattr(prediction, 'tolist') else prediction)
            )

        return {
            "prediction": prediction.tolist() if hasattr(prediction, 'tolist') else prediction,
            "from_cache": False,
            "model_version": model_version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """Predicción batch"""
    try:
        input_df = pd.DataFrame(request.instances)
        predictions = current_model.predict(input_df)

        return {
            "predictions": predictions.tolist() if hasattr(predictions, 'tolist') else predictions.tolist(),
            "count": len(predictions),
            "model_version": model_version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reload-model")
async def reload_model(model_name: str, stage: str = "Production"):
    """Recarga el modelo"""
    try:
        load_model(model_name, stage)

        # Limpiar cache
        redis_client.flushdb()

        return {
            "success": True,
            "model_name": model_name,
            "stage": stage,
            "message": "Model reloaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "model_loaded": current_model is not None,
        "model_version": model_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 8.2 Servidor FastMCP para Deployment

```python
# mcp_servers/model_serving_server.py
from fastmcp import FastMCP
from typing import Dict, Any, Optional
import subprocess
import json

mcp = FastMCP("Model Deployment Server")

@mcp.tool()
async def deploy_model(
    model_name: str,
    version: str,
    environment: str = "staging",
    replicas: int = 2
) -> Dict[str, Any]:
    """
    Deploya modelo a Kubernetes

    Args:
        model_name: Nombre del modelo
        version: Versión a deployar
        environment: Ambiente (staging, production)
        replicas: Número de réplicas
    """
    try:
        # Crear deployment manifest
        deployment_yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {model_name}-{environment}
  namespace: mlops
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {model_name}
      env: {environment}
  template:
    metadata:
      labels:
        app: {model_name}
        env: {environment}
        version: "{version}"
    spec:
      containers:
      - name: model-server
        image: mlops-registry/model-server:latest
        env:
        - name: MODEL_NAME
          value: "{model_name}"
        - name: MODEL_VERSION
          value: "{version}"
        - name: MLFLOW_TRACKING_URI
          value: "http://mlflow:5000"
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: {model_name}-{environment}-service
  namespace: mlops
spec:
  selector:
    app: {model_name}
    env: {environment}
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
"""

        # Guardar manifest
        manifest_path = f"/tmp/{model_name}-{environment}-deployment.yaml"
        with open(manifest_path, 'w') as f:
            f.write(deployment_yaml)

        # Aplicar deployment
        result = subprocess.run(
            ["kubectl", "apply", "-f", manifest_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr
            }

        return {
            "success": True,
            "model_name": model_name,
            "version": version,
            "environment": environment,
            "replicas": replicas,
            "kubectl_output": result.stdout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def rollback_deployment(
    model_name: str,
    environment: str
) -> Dict[str, Any]:
    """
    Rollback de deployment

    Args:
        model_name: Nombre del modelo
        environment: Ambiente
    """
    try:
        result = subprocess.run(
            [
                "kubectl", "rollout", "undo",
                f"deployment/{model_name}-{environment}",
                "-n", "mlops"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr
            }

        return {
            "success": True,
            "model_name": model_name,
            "environment": environment,
            "message": "Rollback successful",
            "kubectl_output": result.stdout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def scale_deployment(
    model_name: str,
    environment: str,
    replicas: int
) -> Dict[str, Any]:
    """
    Escala el deployment

    Args:
        model_name: Nombre del modelo
        environment: Ambiente
        replicas: Nuevo número de réplicas
    """
    try:
        result = subprocess.run(
            [
                "kubectl", "scale",
                f"deployment/{model_name}-{environment}",
                f"--replicas={replicas}",
                "-n", "mlops"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr
            }

        return {
            "success": True,
            "model_name": model_name,
            "environment": environment,
            "new_replicas": replicas,
            "kubectl_output": result.stdout
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 9. Monitoring y Retraining

### 9.1 Servidor de Monitoring

```python
# mcp_servers/monitoring_server.py
from fastmcp import FastMCP
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *
import json

mcp = FastMCP("Model Monitoring Server")

@mcp.tool()
async def detect_model_drift(
    model_name: str,
    reference_data_path: str,
    current_data_path: str,
    threshold: float = 0.1
) -> Dict[str, Any]:
    """
    Detecta drift en datos y predicciones

    Args:
        model_name: Nombre del modelo
        reference_data_path: Datos de referencia
        current_data_path: Datos actuales
        threshold: Umbral de drift
    """
    try:
        # Cargar datos
        reference_df = pd.read_parquet(reference_data_path)
        current_df = pd.read_parquet(current_data_path)

        # Crear reporte de drift
        data_drift_report = Report(metrics=[
            DataDriftPreset(),
        ])

        data_drift_report.run(
            reference_data=reference_df,
            current_data=current_df
        )

        # Obtener resultados
        report_dict = data_drift_report.as_dict()

        # Verificar drift
        drift_score = report_dict['metrics'][0]['result']['dataset_drift']
        drift_detected = drift_score > threshold

        # Detalles por feature
        drift_by_feature = {}
        if 'result' in report_dict['metrics'][0]:
            drift_by_column = report_dict['metrics'][0]['result'].get('drift_by_columns', {})
            for col, details in drift_by_column.items():
                drift_by_feature[col] = {
                    "drift_detected": details.get('drift_detected', False),
                    "drift_score": details.get('drift_score', 0)
                }

        return {
            "success": True,
            "model_name": model_name,
            "drift_detected": drift_detected,
            "drift_score": drift_score,
            "threshold": threshold,
            "drift_by_feature": drift_by_feature,
            "reference_samples": len(reference_df),
            "current_samples": len(current_df)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def monitor_model_performance(
    model_name: str,
    predictions_path: str,
    actuals_path: str,
    metrics: List[str] = ["accuracy", "precision", "recall", "f1"]
) -> Dict[str, Any]:
    """
    Monitorea performance del modelo en producción

    Args:
        model_name: Nombre del modelo
        predictions_path: Predicciones del modelo
        actuals_path: Valores reales
        metrics: Métricas a calcular
    """
    try:
        # Cargar datos
        predictions_df = pd.read_parquet(predictions_path)
        actuals_df = pd.read_parquet(actuals_path)

        # Merge
        combined_df = predictions_df.merge(
            actuals_df,
            left_index=True,
            right_index=True,
            how='inner'
        )

        y_true = combined_df['actual']
        y_pred = combined_df['prediction']

        # Calcular métricas
        from sklearn.metrics import (
            accuracy_score, precision_score,
            recall_score, f1_score
        )

        results = {}

        if "accuracy" in metrics:
            results["accuracy"] = accuracy_score(y_true, y_pred)

        if "precision" in metrics:
            results["precision"] = precision_score(
                y_true, y_pred, average='weighted'
            )

        if "recall" in metrics:
            results["recall"] = recall_score(
                y_true, y_pred, average='weighted'
            )

        if "f1" in metrics:
            results["f1"] = f1_score(
                y_true, y_pred, average='weighted'
            )

        # Log a MLflow
        import mlflow
        with mlflow.start_run(run_name=f"{model_name}_monitoring"):
            mlflow.log_metrics(results)
            mlflow.set_tag("model_name", model_name)
            mlflow.set_tag("monitoring", "production")

        return {
            "success": True,
            "model_name": model_name,
            "samples_evaluated": len(combined_df),
            "metrics": results
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def generate_monitoring_dashboard(
    model_name: str,
    data_path: str,
    output_path: str
) -> Dict[str, Any]:
    """
    Genera dashboard de monitoring con Evidently

    Args:
        model_name: Nombre del modelo
        data_path: Datos para el dashboard
        output_path: Ruta de salida HTML
    """
    try:
        df = pd.read_parquet(data_path)

        # Crear dashboard
        from evidently.ui.workspace import Workspace
        from evidently.ui.dashboards import DashboardConfig

        report = Report(metrics=[
            DataDriftPreset(),
            TargetDriftPreset(),
            DataQualityPreset(),
            RegressionPreset() if 'regression' in model_name else ClassificationPreset()
        ])

        # Split datos en referencia y actual
        split_idx = int(len(df) * 0.5)
        reference = df[:split_idx]
        current = df[split_idx:]

        report.run(
            reference_data=reference,
            current_data=current
        )

        # Guardar HTML
        report.save_html(output_path)

        return {
            "success": True,
            "model_name": model_name,
            "dashboard_path": output_path,
            "reference_samples": len(reference),
            "current_samples": len(current)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 10. A/B Testing y Experimentación

### 10.1 Servidor de A/B Testing

```python
# mcp_servers/ab_testing_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import random
import json
from datetime import datetime

mcp = FastMCP("A/B Testing Server")

# Configuración de experimentos activos
active_experiments = {}

@mcp.tool()
async def create_ab_test(
    experiment_name: str,
    model_a: Dict[str, str],
    model_b: Dict[str, str],
    traffic_split: float = 0.5,
    duration_days: int = 7
) -> Dict[str, Any]:
    """
    Crea un experimento A/B

    Args:
        experiment_name: Nombre del experimento
        model_a: Configuración modelo A {name, version}
        model_b: Configuración modelo B {name, version}
        traffic_split: % de tráfico para modelo B
        duration_days: Duración en días
    """
    try:
        experiment = {
            "name": experiment_name,
            "model_a": model_a,
            "model_b": model_b,
            "traffic_split": traffic_split,
            "start_date": datetime.now().isoformat(),
            "duration_days": duration_days,
            "metrics": {
                "model_a": {"requests": 0, "predictions": []},
                "model_b": {"requests": 0, "predictions": []}
            },
            "status": "active"
        }

        active_experiments[experiment_name] = experiment

        return {
            "success": True,
            "experiment_name": experiment_name,
            "experiment": experiment
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def route_prediction_request(
    experiment_name: str,
    user_id: str
) -> Dict[str, Any]:
    """
    Rutea request a modelo A o B

    Args:
        experiment_name: Nombre del experimento
        user_id: ID del usuario
    """
    try:
        if experiment_name not in active_experiments:
            return {
                "success": False,
                "error": "Experiment not found"
            }

        experiment = active_experiments[experiment_name]

        # Asignación consistente basada en user_id
        hash_value = hash(user_id)
        use_model_b = (hash_value % 100) < (experiment["traffic_split"] * 100)

        model_to_use = experiment["model_b"] if use_model_b else experiment["model_a"]
        variant = "B" if use_model_b else "A"

        # Actualizar métricas
        if use_model_b:
            experiment["metrics"]["model_b"]["requests"] += 1
        else:
            experiment["metrics"]["model_a"]["requests"] += 1

        return {
            "success": True,
            "experiment_name": experiment_name,
            "variant": variant,
            "model": model_to_use,
            "user_id": user_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def log_ab_test_result(
    experiment_name: str,
    variant: str,
    prediction: Any,
    actual: Optional[Any] = None,
    metrics: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Registra resultado de predicción

    Args:
        experiment_name: Nombre del experimento
        variant: Variante (A o B)
        prediction: Predicción del modelo
        actual: Valor real (opcional)
        metrics: Métricas adicionales
    """
    try:
        if experiment_name not in active_experiments:
            return {
                "success": False,
                "error": "Experiment not found"
            }

        experiment = active_experiments[experiment_name]
        model_key = "model_b" if variant == "B" else "model_a"

        # Guardar predicción
        experiment["metrics"][model_key]["predictions"].append({
            "prediction": prediction,
            "actual": actual,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics or {}
        })

        return {
            "success": True,
            "experiment_name": experiment_name,
            "variant": variant
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def analyze_ab_test(
    experiment_name: str,
    metric_name: str = "accuracy"
) -> Dict[str, Any]:
    """
    Analiza resultados de A/B test

    Args:
        experiment_name: Nombre del experimento
        metric_name: Métrica a comparar
    """
    try:
        if experiment_name not in active_experiments:
            return {
                "success": False,
                "error": "Experiment not found"
            }

        experiment = active_experiments[experiment_name]

        # Calcular métricas
        model_a_preds = experiment["metrics"]["model_a"]["predictions"]
        model_b_preds = experiment["metrics"]["model_b"]["predictions"]

        # Calcular accuracy si hay valores reales
        def calculate_accuracy(predictions):
            valid_preds = [p for p in predictions if p.get("actual") is not None]
            if not valid_preds:
                return None

            correct = sum(
                1 for p in valid_preds
                if p["prediction"] == p["actual"]
            )
            return correct / len(valid_preds)

        model_a_accuracy = calculate_accuracy(model_a_preds)
        model_b_accuracy = calculate_accuracy(model_b_preds)

        # Test estadístico (simplified z-test)
        if model_a_accuracy and model_b_accuracy:
            diff = model_b_accuracy - model_a_accuracy

            # Calcular varianza combinada (simplified)
            n_a = len(model_a_preds)
            n_b = len(model_b_preds)

            pooled_accuracy = (
                model_a_accuracy * n_a + model_b_accuracy * n_b
            ) / (n_a + n_b)

            pooled_variance = pooled_accuracy * (1 - pooled_accuracy)
            se = np.sqrt(pooled_variance * (1/n_a + 1/n_b))

            z_score = diff / se if se > 0 else 0

            # p-value aproximado
            from scipy import stats
            p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

            significant = p_value < 0.05
        else:
            diff = None
            z_score = None
            p_value = None
            significant = False

        return {
            "success": True,
            "experiment_name": experiment_name,
            "model_a": {
                "requests": experiment["metrics"]["model_a"]["requests"],
                "accuracy": model_a_accuracy
            },
            "model_b": {
                "requests": experiment["metrics"]["model_b"]["requests"],
                "accuracy": model_b_accuracy
            },
            "statistical_test": {
                "difference": diff,
                "z_score": z_score,
                "p_value": p_value,
                "significant": significant
            },
            "recommendation": "Promote Model B" if significant and diff > 0 else "Keep Model A"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 11. Integración con MCPs Populares

### 11.1 Orquestador MLOps con MCPs Externos

```python
# mcp_servers/mlops_orchestrator.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
from datetime import datetime

mcp = FastMCP("MLOps Orchestrator")

# Clientes MCP
mcp_clients = {}

EXTERNAL_MCPS = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/mlops/workspace"]
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"}
    },
    "slack": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-slack"],
        "env": {"SLACK_BOT_TOKEN": "your-token"}
    },
    "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
}

async def get_mcp_client(server_name: str) -> ClientSession:
    """Obtiene cliente MCP"""
    if server_name not in mcp_clients:
        config = EXTERNAL_MCPS[server_name]
        params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=config.get("env", {})
        )

        read, write = await stdio_client(params).__aenter__()
        session = await ClientSession(read, write).__aenter__()
        await session.initialize()

        mcp_clients[server_name] = session

    return mcp_clients[server_name]

@mcp.tool()
async def save_model_artifacts(
    model_name: str,
    run_id: str,
    artifacts_to_save: List[str]
) -> Dict[str, Any]:
    """
    Guarda artefactos del modelo usando Filesystem MCP

    Args:
        model_name: Nombre del modelo
        run_id: MLflow run ID
        artifacts_to_save: Lista de artefactos a guardar
    """
    try:
        import mlflow

        fs_client = await get_mcp_client("filesystem")

        # Obtener artefactos de MLflow
        client = mlflow.tracking.MlflowClient()
        artifacts = client.list_artifacts(run_id)

        saved_files = []

        for artifact in artifacts:
            if artifact.path in artifacts_to_save:
                # Descargar artifact
                local_path = client.download_artifacts(run_id, artifact.path)

                # Leer contenido
                with open(local_path, 'r') as f:
                    content = f.read()

                # Guardar usando Filesystem MCP
                remote_path = f"models/{model_name}/{run_id}/{artifact.path}"

                await fs_client.call_tool(
                    "write_file",
                    arguments={
                        "path": remote_path,
                        "content": content
                    }
                )

                saved_files.append(remote_path)

        return {
            "success": True,
            "model_name": model_name,
            "run_id": run_id,
            "files_saved": saved_files
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_model_deployment_issue(
    model_name: str,
    version: str,
    metrics: Dict[str, float],
    environment: str = "staging"
) -> Dict[str, Any]:
    """
    Crea issue en GitHub para deployment

    Args:
        model_name: Nombre del modelo
        version: Versión
        metrics: Métricas del modelo
        environment: Ambiente de deployment
    """
    try:
        gh_client = await get_mcp_client("github")

        title = f"[Deploy] {model_name} v{version} to {environment}"
        body = f"""
## Model Deployment Request

**Model**: {model_name}
**Version**: {version}
**Environment**: {environment}
**Date**: {datetime.now().isoformat()}

### Metrics
{json.dumps(metrics, indent=2)}

### Checklist
- [ ] Model artifacts saved
- [ ] Tests passed
- [ ] Performance validated
- [ ] Deployment manifest created
- [ ] Deployed to {environment}
- [ ] Smoke tests completed

Auto-generated by FastMCP MLOps Pipeline
"""

        issue = await gh_client.call_tool(
            "create_issue",
            arguments={
                "repo": "myorg/ml-models",
                "title": title,
                "body": body,
                "labels": ["deployment", environment, "automated"]
            }
        )

        issue_data = json.loads(issue.content[0].text) if issue.content else {}

        return {
            "success": True,
            "model_name": model_name,
            "version": version,
            "issue_number": issue_data.get("number"),
            "issue_url": issue_data.get("html_url")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def notify_model_deployment(
    model_name: str,
    version: str,
    environment: str,
    status: str,
    metrics: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Notifica deployment via Slack

    Args:
        model_name: Nombre del modelo
        version: Versión
        environment: Ambiente
        status: Estado (success, failed, in_progress)
        metrics: Métricas opcionales
    """
    try:
        slack_client = await get_mcp_client("slack")

        emoji_map = {
            "success": ":white_check_mark:",
            "failed": ":x:",
            "in_progress": ":hourglass:"
        }

        emoji = emoji_map.get(status, ":question:")

        message = f"""{emoji} *Model Deployment {status.upper()}*

*Model*: {model_name}
*Version*: {version}
*Environment*: {environment}
*Timestamp*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        if metrics:
            message += f"\n*Metrics*:\n```{json.dumps(metrics, indent=2)}```"

        await slack_client.call_tool(
            "post_message",
            arguments={
                "channel": "#ml-deployments",
                "text": message
            }
        )

        return {
            "success": True,
            "model_name": model_name,
            "notification_sent": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def store_experiment_results(
    experiment_name: str,
    results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Almacena resultados de experimentos en Memory MCP

    Args:
        experiment_name: Nombre del experimento
        results: Resultados a almacenar
    """
    try:
        memory_client = await get_mcp_client("memory")

        await memory_client.call_tool(
            "store_memory",
            arguments={
                "key": f"experiment_{experiment_name}",
                "value": json.dumps(results),
                "metadata": {
                    "type": "ml_experiment",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )

        return {
            "success": True,
            "experiment_name": experiment_name,
            "stored": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

---

## 12. CI/CD para ML

### 12.1 GitHub Actions Workflow

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

jobs:
  data-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Validate data quality
        run: |
          python scripts/validate_data.py \
            --data-path data/latest.parquet \
            --expectations config/expectations.json

      - name: Upload validation report
        uses: actions/upload-artifact@v3
        with:
          name: data-validation-report
          path: reports/data_validation.html

  model-training:
    runs-on: ubuntu-latest
    needs: data-validation
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Train model
        run: |
          python scripts/train_model.py \
            --experiment-name ci_cd_pipeline \
            --config config/model_config.yaml

      - name: Upload model artifacts
        uses: actions/upload-artifact@v3
        with:
          name: model-artifacts
          path: artifacts/

  model-evaluation:
    runs-on: ubuntu-latest
    needs: model-training
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Download model artifacts
        uses: actions/download-artifact@v3
        with:
          name: model-artifacts
          path: artifacts/

      - name: Evaluate model
        run: |
          python scripts/evaluate_model.py \
            --test-data data/test.parquet \
            --threshold 0.85

      - name: Upload evaluation report
        uses: actions/upload-artifact@v3
        with:
          name: evaluation-report
          path: reports/evaluation.html

  model-deployment-staging:
    runs-on: ubuntu-latest
    needs: model-evaluation
    if: github.ref == 'refs/heads/develop'
    steps:
      - uses: actions/checkout@v3

      - name: Configure kubectl
        uses: azure/setup-kubectl@v3

      - name: Deploy to staging
        run: |
          kubectl apply -f k8s/staging/deployment.yaml

      - name: Run smoke tests
        run: |
          python scripts/smoke_tests.py --environment staging

  model-deployment-production:
    runs-on: ubuntu-latest
    needs: model-evaluation
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Configure kubectl
        uses: azure/setup-kubectl@v3

      - name: Create GitHub Issue for Production Deployment
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Production Deployment Approval Required',
              body: 'Model is ready for production deployment. Please review and approve.',
              labels: ['deployment', 'production', 'needs-approval']
            })
```

### 12.2 Script de Validación de Datos

```python
# scripts/validate_data.py
import argparse
import json
import pandas as pd
import great_expectations as gx
from pathlib import Path

def validate_data(data_path: str, expectations_path: str):
    """Valida datos usando Great Expectations"""

    # Cargar datos
    df = pd.read_parquet(data_path)

    # Cargar expectations
    with open(expectations_path) as f:
        expectations_config = json.load(f)

    # Context de GX
    context = gx.get_context()

    # Crear datasource
    datasource = context.sources.add_or_update_pandas(name="validation_source")
    data_asset = datasource.add_dataframe_asset(name="validation_data")

    # Crear batch
    batch_request = data_asset.build_batch_request(dataframe=df)

    # Crear suite
    suite = context.add_expectation_suite("validation_suite")

    # Validator
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name="validation_suite"
    )

    # Aplicar expectations
    for exp in expectations_config["expectations"]:
        exp_type = exp["type"]
        exp_kwargs = exp["kwargs"]

        getattr(validator, exp_type)(**exp_kwargs)

    # Validar
    validation_result = validator.validate()

    # Guardar reporte
    Path("reports").mkdir(exist_ok=True)
    validation_result.save("reports/data_validation.html")

    # Exit code
    if not validation_result.success:
        print("Data validation failed!")
        exit(1)
    else:
        print("Data validation passed!")
        exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--expectations", required=True)

    args = parser.parse_args()

    validate_data(args.data_path, args.expectations)
```

---

## Conclusión

Este taller completo cubre:

✅ **FastMCP + Spark Integration** - Procesamiento distribuido de datos
✅ **Feature Store con Feast** - Gestión centralizada de features
✅ **ML Pipeline con MLflow** - Tracking, registro y gestión de experimentos
✅ **Orquestación con Airflow** - Workflows automatizados end-to-end
✅ **Model Registry** - Versionado y gestión de modelos
✅ **Deployment** - FastAPI serving + Kubernetes
✅ **Monitoring** - Drift detection con Evidently
✅ **A/B Testing** - Experimentación en producción
✅ **Integración MCPs** - GitHub, Slack, Filesystem, Memory
✅ **CI/CD** - GitHub Actions para ML
✅ **Data Quality** - Great Expectations
✅ **Hyperparameter Tuning** - Optuna + MLflow

**Stack Completo:**
- Apache Spark + Delta Lake
- Feast Feature Store
- MLflow (tracking, registry, serving)
- Apache Airflow
- FastAPI
- Kubernetes
- Prometheus + Grafana
- Evidently
- Great Expectations
- FastMCP (orquestación)

**Próximos Pasos:**

1. Configurar infraestructura (Spark, MLflow, Airflow)
2. Configurar Feature Store con Feast
3. Implementar servidores FastMCP
4. Crear DAGs de Airflow
5. Configurar CI/CD con GitHub Actions
6. Deployar modelo serving API
7. Configurar monitoring y alertas
8. Implementar A/B testing
9. Escalar a producción

**Recursos:**
- [Apache Spark](https://spark.apache.org/docs/latest/)
- [MLflow](https://mlflow.org/docs/latest/index.html)
- [Apache Airflow](https://airflow.apache.org/docs/)
- [Feast](https://docs.feast.dev/)
- [Evidently](https://docs.evidentlyai.com/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Great Expectations](https://docs.greatexpectations.io/)
