# 🔄 Guía Completa de MLflow para Spark MLlib

MLflow es la plataforma open-source líder para gestionar el ciclo de vida completo de Machine Learning, desde experimentación hasta producción.

---

## 📚 ¿Qué es MLflow?

**MLflow** es una plataforma que resuelve los 4 problemas principales del ML lifecycle:

```
Problema 1: Experimentación desorganizada
Problema 2: Reproducibilidad (¿cómo entrené ese modelo?)
Problema 3: Deployment (¿cómo sirvo el modelo?)
Problema 4: Gobierno de modelos (¿qué versión está en producción?)
           ↓
       MLflow soluciona TODO
```

### Los 4 Componentes de MLflow

```
┌─────────────────────────────────────────────────┐
│                   MLflow                        │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. MLflow Tracking                             │
│     └─ Log experiments, parameters, metrics     │
│                                                 │
│  2. MLflow Projects                             │
│     └─ Package ML code reproducibly             │
│                                                 │
│  3. MLflow Models                               │
│     └─ Deploy models to production              │
│                                                 │
│  4. MLflow Registry                             │
│     └─ Manage model lifecycle & versions        │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎯 MLflow Tracking: Experimentos Organizados

### Sin MLflow (Caos)

```python
# Experimento 1
model = train_model(lr=0.01, depth=5)
# AUC = 0.85 ... ¿con qué features? ¿qué fecha?

# 2 semanas después...
# ¿Cómo reproduzco AUC=0.85? 😱
# ¿Qué parámetros usé?
# ¿Qué versión del código?
```

### Con MLflow (Organizado)

```python
import mlflow

with mlflow.start_run():
    # 1. Log parámetros
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("max_depth", 5)

    # 2. Entrenar
    model = train_model(lr=0.01, depth=5)

    # 3. Log métricas
    mlflow.log_metric("auc", 0.85)
    mlflow.log_metric("accuracy", 0.82)

    # 4. Log modelo
    mlflow.spark.log_model(model, "model")

    # 5. Log artifacts (gráficos, archivos)
    mlflow.log_artifact("confusion_matrix.png")

# Resultado: Todo queda registrado automáticamente
```

---

## 🚀 Instalación y Setup

### 1. Instalación

```bash
# Básico
pip install mlflow

# Con extras para Spark
pip install mlflow[extras]
pip install pyspark

# Verificar
mlflow --version
```

### 2. Iniciar MLflow UI

```bash
# Opción 1: SQLite local (desarrollo)
mlflow ui

# Opción 2: PostgreSQL (producción)
mlflow server \
  --backend-store-uri postgresql://user:pass@localhost/mlflow \
  --default-artifact-root s3://my-bucket/mlflow-artifacts \
  --host 0.0.0.0 \
  --port 5000

# Abrir en navegador
open http://localhost:5000
```

### 3. Configurar Tracking URI

```python
import mlflow

# Opción 1: Local (desarrollo)
mlflow.set_tracking_uri("file:./mlruns")

# Opción 2: Server remoto (producción)
mlflow.set_tracking_uri("http://mlflow-server:5000")

# Opción 3: Databricks
mlflow.set_tracking_uri("databricks")
```

---

## 📊 MLflow Tracking: Ejemplos Prácticos

### Ejemplo 1: Experimento Básico

```python
import mlflow
from pyspark.ml.classification import RandomForestClassifier

# Configurar experimento
mlflow.set_experiment("Lead_Scoring_Experiment")

# Iniciar run
with mlflow.start_run(run_name="RF_baseline"):

    # Parámetros del modelo
    num_trees = 100
    max_depth = 5

    # Log parámetros
    mlflow.log_param("num_trees", num_trees)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("algorithm", "RandomForest")

    # Entrenar modelo
    rf = RandomForestClassifier(
        numTrees=num_trees,
        maxDepth=max_depth,
        labelCol="converted"
    )
    model = rf.fit(train_df)

    # Evaluar
    predictions = model.transform(test_df)
    auc = evaluator.evaluate(predictions)

    # Log métricas
    mlflow.log_metric("auc", auc)
    mlflow.log_metric("train_size", train_df.count())
    mlflow.log_metric("test_size", test_df.count())

    # Log modelo Spark
    mlflow.spark.log_model(
        model,
        artifact_path="random_forest_model",
        registered_model_name="LeadScoringRF"
    )

    print(f"Run ID: {mlflow.active_run().info.run_id}")
    print(f"AUC: {auc:.4f}")
```

### Ejemplo 2: Comparar Múltiples Modelos

```python
from pyspark.ml.classification import (
    RandomForestClassifier,
    GBTClassifier,
    LogisticRegression
)

mlflow.set_experiment("Model_Comparison")

# Configuración de modelos a probar
models_config = [
    {
        "name": "RandomForest",
        "model": RandomForestClassifier(numTrees=100, maxDepth=5)
    },
    {
        "name": "GBT",
        "model": GBTClassifier(maxIter=20, maxDepth=5)
    },
    {
        "name": "LogisticRegression",
        "model": LogisticRegression(maxIter=20)
    }
]

results = []

for config in models_config:
    with mlflow.start_run(run_name=config["name"]):

        # Log tipo de modelo
        mlflow.log_param("model_type", config["name"])

        # Entrenar
        model = config["model"].fit(train_df)
        predictions = model.transform(test_df)

        # Evaluar
        auc = auc_evaluator.evaluate(predictions)
        accuracy = accuracy_evaluator.evaluate(predictions)

        # Log métricas
        mlflow.log_metric("auc", auc)
        mlflow.log_metric("accuracy", accuracy)

        # Log modelo
        mlflow.spark.log_model(model, f"{config['name']}_model")

        results.append({
            "model": config["name"],
            "auc": auc,
            "accuracy": accuracy
        })

        print(f"{config['name']}: AUC={auc:.4f}, Accuracy={accuracy:.4f}")

# Encontrar mejor modelo
best_model = max(results, key=lambda x: x['auc'])
print(f"\n✅ Mejor modelo: {best_model['model']} con AUC={best_model['auc']:.4f}")
```

### Ejemplo 3: Hyperparameter Tuning con MLflow

```python
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

mlflow.set_experiment("Hyperparameter_Tuning")

with mlflow.start_run(run_name="GBT_GridSearch"):

    # Definir grid de parámetros
    gbt = GBTClassifier(labelCol="converted")

    paramGrid = ParamGridBuilder() \
        .addGrid(gbt.maxDepth, [3, 5, 7]) \
        .addGrid(gbt.maxIter, [10, 20, 30]) \
        .addGrid(gbt.stepSize, [0.1, 0.05]) \
        .build()

    # CrossValidator
    cv = CrossValidator(
        estimator=gbt,
        estimatorParamMaps=paramGrid,
        evaluator=BinaryClassificationEvaluator(labelCol="converted"),
        numFolds=3
    )

    # Entrenar (prueba todas las combinaciones)
    cv_model = cv.fit(train_df)

    # Mejor modelo
    best_model = cv_model.bestModel

    # Log mejores parámetros
    mlflow.log_param("best_maxDepth", best_model.getMaxDepth())
    mlflow.log_param("best_maxIter", best_model.getMaxIter())
    mlflow.log_param("best_stepSize", best_model.getStepSize())

    # Evaluar
    predictions = cv_model.transform(test_df)
    auc = evaluator.evaluate(predictions)

    mlflow.log_metric("best_auc", auc)
    mlflow.log_metric("num_combinations_tested", len(paramGrid))

    # Log modelo
    mlflow.spark.log_model(best_model, "best_gbt_model")

    print(f"✅ Best AUC: {auc:.4f}")
    print(f"   maxDepth={best_model.getMaxDepth()}")
    print(f"   maxIter={best_model.getMaxIter()}")
```

### Ejemplo 4: Log de Artifacts (Archivos)

```python
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

with mlflow.start_run():

    # ... entrenar modelo ...

    # 1. Crear gráfico de confusion matrix
    y_true = predictions.select("converted").toPandas()
    y_pred = predictions.select("prediction").toPandas()

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig("confusion_matrix.png")
    plt.close()

    # Log imagen
    mlflow.log_artifact("confusion_matrix.png")

    # 2. Log feature importance como CSV
    if hasattr(model, 'featureImportances'):
        import pandas as pd

        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.featureImportances.toArray()
        }).sort_values('importance', ascending=False)

        importance_df.to_csv("feature_importance.csv", index=False)
        mlflow.log_artifact("feature_importance.csv")

    # 3. Log dataset stats
    stats = {
        'train_size': train_df.count(),
        'test_size': test_df.count(),
        'num_features': len(feature_names),
        'class_balance': train_df.groupBy('converted').count().toPandas()
    }

    import json
    with open("dataset_stats.json", "w") as f:
        json.dump(stats, f, default=str, indent=2)

    mlflow.log_artifact("dataset_stats.json")
```

---

## 🏷️ MLflow Registry: Model Versioning

### ¿Por qué Model Registry?

```
Problema:
  - Tienes 50 modelos entrenados
  - ¿Cuál está en producción?
  - ¿Cuál es la versión anterior por si necesitas rollback?
  - ¿Quién aprobó el modelo actual?

Solución: MLflow Model Registry
  - Versionado automático
  - Staging (Development → Staging → Production)
  - Aprobaciones y transiciones
  - Lineage completo
```

### Registro de Modelos

```python
# Durante entrenamiento
with mlflow.start_run():
    # ... entrenar modelo ...

    # Registrar modelo
    mlflow.spark.log_model(
        spark_model=model,
        artifact_path="model",
        registered_model_name="LeadScoringModel"  # ← Nombre en registry
    )
```

### Transiciones de Stage

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# 1. Promover modelo a Staging
client.transition_model_version_stage(
    name="LeadScoringModel",
    version=3,
    stage="Staging"
)

# 2. Después de validación, promover a Production
client.transition_model_version_stage(
    name="LeadScoringModel",
    version=3,
    stage="Production"
)

# 3. Archivar versión antigua
client.transition_model_version_stage(
    name="LeadScoringModel",
    version=2,
    stage="Archived"
)
```

### Cargar Modelo desde Registry

```python
# Opción 1: Por versión específica
model_uri = "models:/LeadScoringModel/3"
model = mlflow.spark.load_model(model_uri)

# Opción 2: Por stage (recomendado para producción)
model_uri = "models:/LeadScoringModel/Production"
model = mlflow.spark.load_model(model_uri)

# Opción 3: Última versión
model_uri = "models:/LeadScoringModel/latest"
model = mlflow.spark.load_model(model_uri)

# Usar modelo
predictions = model.transform(new_data)
```

---

## 🔍 MLflow UI: Exploración

### Vista de Experimentos

```
MLflow UI (http://localhost:5000)
├── Experiments
│   ├── Lead_Scoring_Experiment
│   │   ├── Run 1: RF_baseline (AUC: 0.82)
│   │   ├── Run 2: GBT_v1 (AUC: 0.85) ← Mejor
│   │   └── Run 3: LogReg (AUC: 0.78)
│   │
│   └── Hyperparameter_Tuning
│       └── Run 1: GBT_GridSearch (27 combinaciones)
│
└── Models (Registry)
    └── LeadScoringModel
        ├── Version 1 (Archived)
        ├── Version 2 (Staging)
        └── Version 3 (Production) ← Actual
```

### Comparación de Runs

En la UI puedes:
1. ✅ Comparar métricas lado a lado
2. ✅ Ver diferencias de parámetros
3. ✅ Graficar métricas (scatter plots, parallel coordinates)
4. ✅ Descargar modelos
5. ✅ Ver lineage completo

---

## 🚀 MLflow en Producción

### Arquitectura de Producción

```
┌─────────────────────────────────────────────────┐
│         MLflow Tracking Server                  │
│  (Backend: PostgreSQL, Artifacts: S3)           │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
┌──────────────┐   ┌──────────────┐
│  Data        │   │  ML Engineer │
│  Scientists  │   │  (API)       │
│              │   │              │
│ • Entrenan   │   │ • Carga      │
│ • Log runs   │   │   modelos    │
│ • Comparan   │   │ • Sirve      │
└──────────────┘   └──────────────┘
```

### Docker Compose para MLflow Server

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: mlflow
      POSTGRES_USER: mlflow
      POSTGRES_PASSWORD: mlflow
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_BACKEND_STORE_URI=postgresql://mlflow:mlflow@postgres/mlflow
      - MLFLOW_DEFAULT_ARTIFACT_ROOT=s3://my-bucket/mlflow-artifacts
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    depends_on:
      - postgres
    command: >
      mlflow server
      --backend-store-uri postgresql://mlflow:mlflow@postgres/mlflow
      --default-artifact-root s3://my-bucket/mlflow-artifacts
      --host 0.0.0.0
      --port 5000

volumes:
  postgres_data:
```

### Configuración de Cliente

```python
import mlflow
import os

# Configurar tracking URI
mlflow.set_tracking_uri("http://mlflow-server:5000")

# Configurar AWS credentials para artifacts
os.environ["AWS_ACCESS_KEY_ID"] = "your-key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your-secret"

# Resto del código igual
with mlflow.start_run():
    # ... entrenar ...
    mlflow.spark.log_model(model, "model")
```

---

## 💡 Mejores Prácticas

### 1. Naming Conventions

```python
# BIEN: Nombres descriptivos
mlflow.set_experiment("CRM_LeadScoring_Production")
with mlflow.start_run(run_name="GBT_v2.3_feature_eng_improved"):
    ...

# MAL: Nombres genéricos
mlflow.set_experiment("Experiment1")
with mlflow.start_run(run_name="test"):
    ...
```

### 2. Log Todo lo Relevante

```python
with mlflow.start_run():
    # Parámetros del modelo
    mlflow.log_params({
        "max_depth": 5,
        "num_trees": 100,
        "min_instances_per_node": 10
    })

    # Parámetros del dataset
    mlflow.log_params({
        "train_start_date": "2024-01-01",
        "train_end_date": "2024-06-30",
        "feature_set_version": "v2.1"
    })

    # Métricas de evaluación
    mlflow.log_metrics({
        "auc": 0.85,
        "accuracy": 0.82,
        "precision": 0.78,
        "recall": 0.81,
        "f1": 0.79
    })

    # Métricas de negocio
    mlflow.log_metrics({
        "expected_revenue_lift": 150000,
        "false_positive_rate": 0.12
    })

    # Metadata
    mlflow.set_tags({
        "team": "data-science",
        "project": "lead-scoring",
        "model_type": "classification",
        "framework": "spark-mllib"
    })
```

### 3. Nested Runs para Pipelines Complejos

```python
# Parent run: Todo el pipeline
with mlflow.start_run(run_name="Complete_Pipeline"):

    # Child run 1: Feature Engineering
    with mlflow.start_run(run_name="Feature_Engineering", nested=True):
        mlflow.log_param("feature_version", "v2.0")
        features_df = create_features(raw_df)
        mlflow.log_metric("num_features", len(features_df.columns))

    # Child run 2: Model Training
    with mlflow.start_run(run_name="Model_Training", nested=True):
        model = train_model(features_df)
        mlflow.log_metric("auc", 0.85)
        mlflow.spark.log_model(model, "model")

    # Child run 3: Model Evaluation
    with mlflow.start_run(run_name="Model_Evaluation", nested=True):
        metrics = evaluate_model(model, test_df)
        mlflow.log_metrics(metrics)
```

### 4. Autolog (Automático)

```python
# MLflow puede log automáticamente para algunos frameworks
import mlflow.spark

# Habilitar autolog
mlflow.spark.autolog()

# Ahora entrenar normalmente - MLflow registra todo automáticamente
with mlflow.start_run():
    model = RandomForestClassifier(numTrees=100).fit(train_df)
    predictions = model.transform(test_df)
    # ✅ Parámetros, métricas y modelo logged automáticamente
```

---

## 📊 Queries Programáticas

### Buscar Runs

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Buscar runs por experimento
experiment = client.get_experiment_by_name("Lead_Scoring_Experiment")
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="metrics.auc > 0.8",
    order_by=["metrics.auc DESC"],
    max_results=10
)

for run in runs:
    print(f"Run ID: {run.info.run_id}")
    print(f"  AUC: {run.data.metrics['auc']}")
    print(f"  Params: {run.data.params}")
```

### Comparar Modelos

```python
# Obtener top 3 modelos
top_runs = client.search_runs(
    experiment_ids=[experiment_id],
    order_by=["metrics.auc DESC"],
    max_results=3
)

import pandas as pd

comparison_df = pd.DataFrame([
    {
        'run_id': run.info.run_id[:8],
        'auc': run.data.metrics.get('auc'),
        'max_depth': run.data.params.get('max_depth'),
        'num_trees': run.data.params.get('num_trees')
    }
    for run in top_runs
])

print(comparison_df)
```

---

## 🔧 Troubleshooting

### Problema 1: "No module named 'mlflow'"

```bash
pip install mlflow
# O con conda
conda install -c conda-forge mlflow
```

### Problema 2: "Connection refused to tracking server"

```python
# Verificar que el server esté corriendo
# En terminal 1:
mlflow ui

# En terminal 2:
curl http://localhost:5000/health

# En código:
mlflow.set_tracking_uri("http://localhost:5000")
```

### Problema 3: "Cannot log Spark model"

```bash
# Instalar con soporte Spark
pip install mlflow[extras]
pip install pyspark
```

### Problema 4: Artifacts no se guardan

```python
# Verificar artifact location
print(mlflow.get_artifact_uri())

# Asegurar que el directorio existe
import os
os.makedirs("mlruns", exist_ok=True)
```

---

## 📚 Referencias

### Documentación Oficial
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
- [MLflow Models](https://mlflow.org/docs/latest/models.html)
- [MLflow Registry](https://mlflow.org/docs/latest/model-registry.html)

### Tutoriales
- [MLflow Quickstart](https://mlflow.org/docs/latest/quickstart.html)
- [Managing ML Lifecycle with MLflow](https://www.databricks.com/blog/2020/06/25/announcing-mlflow-1-9-improved-ml-lifecycle-management.html)

### Videos
- [MLflow Tutorial - Full Course](https://www.youtube.com/watch?v=x3cxvsUFVZA)
- [Databricks: MLflow in Production](https://www.youtube.com/watch?v=QJW_kkRWAUs)

---

## 🎯 Checklist de MLflow

Antes de deployment, verifica:

- [ ] Todos los experimentos tienen nombres descriptivos
- [ ] Todos los runs tienen parámetros logged
- [ ] Métricas de evaluación están trackeadas
- [ ] Modelos están registrados en Registry
- [ ] Modelo de producción está en stage "Production"
- [ ] Artifacts importantes están guardados (confusion matrix, etc.)
- [ ] Tags están asignados (team, project, etc.)
- [ ] Tracking server está configurado para producción
- [ ] Backup de PostgreSQL está configurado
- [ ] Artifacts están en S3/storage persistente

---

**¡Ahora estás listo para usar MLflow como un pro! 🚀**

Vuelve al [README del Módulo 02-03](./README.md) para continuar con el entrenamiento de modelos.
