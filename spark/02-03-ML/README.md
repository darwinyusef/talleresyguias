# 🤖 Módulo 02-03: Machine Learning con Spark MLlib + MLflow

Domina el Machine Learning distribuido a escala con Apache Spark MLlib, el motor de ML diseñado para procesar terabytes de datos y entrenar modelos en clusters distribuidos.

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Entender la arquitectura de Spark MLlib y cómo difiere de scikit-learn
- ✅ Construir pipelines de ML reproducibles y escalables
- ✅ Implementar feature engineering distribuido para Big Data
- ✅ Entrenar modelos supervisados (clasificación) y no supervisados (clustering)
- ✅ Evaluar modelos con métricas apropiadas (AUC, Silhouette, etc.)
- ✅ Trackear experimentos con MLflow para reproducibilidad
- ✅ Comparar múltiples algoritmos y seleccionar el mejor
- ✅ Preparar modelos para producción y serving

---

## 📚 Fundamentos Teóricos

### ¿Qué es Spark MLlib?

**Spark MLlib** (Machine Learning Library) es la librería de aprendizaje automático distribuido de Apache Spark. Está diseñada para ejecutar algoritmos de ML a escala masiva aprovechando el procesamiento paralelo de Spark.

#### Evolución de MLlib

```
2014: spark.mllib (RDD-based API) → Legacy, basada en RDDs
         ↓
2016: spark.ml (DataFrame API) → Moderna, recomendada
         ↓
2024: spark.ml + MLflow → Estándar de producción
```

**⚠️ IMPORTANTE**: En este taller usamos **spark.ml** (DataFrame-based), NO `spark.mllib` (RDD-based que está deprecated).

---

### 🔑 Conceptos Clave de MLlib

#### 1. Transformers vs Estimators

Esta es la arquitectura fundamental de Spark ML:

```python
# TRANSFORMER: Transforma un DataFrame en otro
# Ejemplo: StringIndexer fitted, StandardScaler fitted
transformer.transform(df) → nuevo_df

# ESTIMATOR: Aprende de datos y produce un Transformer
# Ejemplo: StringIndexer, StandardScaler, RandomForest
estimator.fit(df) → transformer (modelo entrenado)
```

**Analogía con scikit-learn:**
```python
# Scikit-learn
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()        # Estimator
scaler.fit(X_train)               # fit() → devuelve self
X_scaled = scaler.transform(X)    # Transformer

# Spark MLlib
from pyspark.ml.feature import StandardScaler
scaler = StandardScaler()         # Estimator
scaler_model = scaler.fit(df)     # fit() → devuelve Transformer
df_scaled = scaler_model.transform(df)  # Transformer
```

#### 2. Pipelines: Workflows Reproducibles

Un **Pipeline** encadena múltiples transformadores y estimadores en un flujo único:

```
Raw Data
   ↓
[StringIndexer] → indexa categorías
   ↓
[OneHotEncoder] → codifica one-hot
   ↓
[VectorAssembler] → combina features en vector
   ↓
[StandardScaler] → normaliza features
   ↓
[RandomForest] → entrena modelo
   ↓
Predictions
```

**Ventajas de Pipelines:**
- ✅ **Reproducibilidad**: Mismo código, mismos resultados
- ✅ **No data leakage**: Las transformaciones del train no ven el test
- ✅ **Deployment fácil**: Serializar pipeline completo como un archivo
- ✅ **Hyperparameter tuning**: CrossValidator trabaja con pipelines enteros

**Código:**
```python
from pyspark.ml import Pipeline

pipeline = Pipeline(stages=[
    string_indexer,   # Estimator
    one_hot_encoder,  # Estimator
    vector_assembler, # Transformer
    scaler,           # Estimator
    classifier        # Estimator
])

# Entrenar TODO el pipeline
model = pipeline.fit(train_df)

# Usar en producción
predictions = model.transform(new_data)
```

#### 3. Vectorización: El Formato de MLlib

**TODOS** los algoritmos de MLlib requieren que las features estén en un **único vector denso o sparse**:

```python
# MAL: Features en columnas separadas
+-----+--------+----------+
| age | salary | category |
+-----+--------+----------+
|  25 |  50000 |     high |

# BIEN: Features en un vector
+--------------------+
|            features|
+--------------------+
|  [25.0, 50000.0, 1]|

# Usar VectorAssembler
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["age", "salary", "category_encoded"],
    outputCol="features"
)
```

**Vector Types:**
- **Dense Vector**: `[1.0, 2.0, 3.0, 4.0]` - Todos los valores almacenados
- **Sparse Vector**: `(4, [0, 2], [1.0, 3.0])` - Solo valores no-cero (eficiente)

---

### 🧠 Algoritmos Disponibles en MLlib

#### Clasificación (Supervised Learning)

| Algoritmo | Cuándo Usarlo | Pros | Contras |
|-----------|---------------|------|---------|
| **Logistic Regression** | Baseline rápido, relaciones lineales | Rápido, interpretable | Solo lineal, requiere scaling |
| **Decision Trees** | Features categóricas, no-linealidad | No requiere scaling, interpretable | Overfitting fácil |
| **Random Forest** | Datasets medianos, quieres robustez | Robusto, maneja no-linealidad | Menos interpretable, lento en predicción |
| **Gradient Boosted Trees (GBT)** | Máxima accuracy, competencias Kaggle | Muy preciso, feature importance | Lento de entrenar, hiperparámetros sensibles |
| **Linear SVM** | Clasificación binaria, datos high-dimensional | Funciona bien en alta dimensión | Solo lineal, solo binario |
| **Naive Bayes** | Text classification, baseline | Muy rápido, funciona con poco data | Asume independencia (naive) |

#### Regresión

- Linear Regression
- Generalized Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosted Trees Regressor
- Isotonic Regression

#### Clustering (Unsupervised Learning)

| Algoritmo | Uso | K requerido |
|-----------|-----|-------------|
| **K-Means** | Segmentación de clientes, compresión | Sí - usar Elbow Method |
| **Bisecting K-Means** | Más rápido que K-Means, jerárquico | Sí |
| **Gaussian Mixture Model (GMM)** | Clusters con forma elíptica | Sí |
| **LDA (Latent Dirichlet Allocation)** | Topic modeling en texto | Sí (número de topics) |

---

## 🔬 Caso de Uso 1: Lead Scoring (Clasificación)

### Problema de Negocio

**Contexto**: Una empresa B2B recibe 10,000 leads por mes. El equipo de ventas solo puede contactar 500. ¿Cómo priorizamos?

**Solución**: Modelo de ML que predice la probabilidad de conversión de cada lead.

### Datos

```python
# Dataset: lead_conversions.csv
Columns:
- id: Lead ID único
- age: Edad del prospect
- salary: Ingreso anual estimado
- web_visits: Número de visitas al sitio web
- last_action: Última acción (web_view, email_click, form_submit)
- converted: Target binario (0=no convirtió, 1=convirtió)
```

### Feature Engineering

#### 1. Variables Categóricas → Numéricas

**String Indexing**: Convierte strings a índices numéricos
```python
# Antes
last_action: ["email_click", "form_submit", "web_view"]

# Después de StringIndexer
last_action_index: [0.0, 1.0, 2.0]
```

**One-Hot Encoding**: Crea features binarias
```python
# Después de OneHotEncoder
last_action_vec:
  email_click  → [1, 0, 0]
  form_submit  → [0, 1, 0]
  web_view     → [0, 0, 1]
```

**¿Por qué One-Hot?** Muchos algoritmos asumen que números representan orden (0 < 1 < 2). One-hot elimina esta falsa ordenación.

#### 2. Feature Scaling

**StandardScaler**: Normaliza features a media=0, std=1

```python
# Antes del scaling
age: [25, 45, 65]       → rango: ~40
salary: [30000, 80000, 150000]  → rango: ~120,000

# Problema: salary domina la distancia euclidiana
# Solución: StandardScaler

# Después
age_scaled: [-1.0, 0.0, 1.0]
salary_scaled: [-1.0, 0.0, 1.0]
```

**⚠️ Cuándo es CRÍTICO escalar:**
- Logistic Regression
- SVM
- K-Means
- Redes Neuronales

**Cuándo NO importa:**
- Tree-based models (Random Forest, GBT, Decision Trees)

### Algoritmos Usados

#### Gradient Boosted Trees (GBT)

**Cómo funciona:**
1. Entrena un árbol débil (shallow)
2. Calcula errores
3. Entrena otro árbol para predecir esos errores
4. Repite N veces
5. Predicción = suma de todos los árboles

**Hiperparámetros clave:**
```python
GBTClassifier(
    maxIter=20,        # Número de árboles (más = mejor, pero overfitting)
    maxDepth=5,        # Profundidad de cada árbol (3-7 típico)
    stepSize=0.1,      # Learning rate (0.01-0.3)
    subsamplingRate=0.8  # Fracción de datos por árbol (0.5-1.0)
)
```

**Feature Importance:**
GBT produce importancia de features automáticamente:
```python
model.featureImportances
# Output: [0.45, 0.30, 0.15, 0.10]
# Significa: feature 0 es 45% importante, etc.
```

### Métricas de Evaluación

#### AUC-ROC (Area Under ROC Curve)

**¿Qué mide?** Capacidad del modelo de distinguir entre clases.

```
AUC = 1.0  → Modelo perfecto
AUC = 0.9  → Excelente
AUC = 0.8  → Bueno
AUC = 0.7  → Aceptable
AUC = 0.5  → Aleatorio (inútil)
AUC < 0.5  → Peor que aleatorio
```

**¿Por qué AUC y no Accuracy?**

Ejemplo: Dataset con 95% negativos, 5% positivos
```python
# Modelo dummy que siempre predice "NO"
Accuracy = 95%  # ¡Parece excelente!
AUC = 0.5       # Revela que es aleatorio
```

#### Matriz de Confusión

```
                 Predicted
                 No    Yes
Actual  No      TN    FP    → Precision = TP/(TP+FP)
        Yes     FN    TP    → Recall = TP/(TP+FN)
```

**Trade-off Precision vs Recall:**
- **High Precision**: Pocas falsas alarmas (importante en spam detection)
- **High Recall**: No perder positivos (importante en fraud detection)

**F1 Score**: Promedio armónico de Precision y Recall
```python
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

---

## 🎨 Caso de Uso 2: Customer Segmentation (Clustering)

### Problema de Negocio

**Contexto**: E-commerce con 100,000 clientes. Queremos segmentarlos para marketing personalizado.

**Solución**: Clustering para descubrir grupos naturales de clientes con comportamiento similar.

### K-Means Clustering

#### Algoritmo

```
1. Inicializar K centroides aleatoriamente
2. Asignar cada punto al centroide más cercano
3. Recalcular centroides como media de puntos asignados
4. Repetir 2-3 hasta convergencia
```

**Visualización ASCII:**
```
Iteración 0:             Iteración 5:
  •  •  •  X             Clusters formados:
 •  X  •  •              ⚫⚫⚫  ⚪⚪⚪
  •  •  X                ⚫⚫⚫  ⚪⚪⚪
                         🔴🔴🔴
X = centroides           ⚫=cluster1, ⚪=cluster2, 🔴=cluster3
```

#### El Problema del K Óptimo

**Elbow Method**: Graficar WSSSE vs K

```
WSSSE
  ^
  |    *
  |      *
  |        *___
  |            *____*____*
  +-----------------------> K
       ↑
     "Elbow" - K óptimo ≈ 3
```

**WSSSE** = Within Set Sum of Squared Errors (menor es mejor)

#### Silhouette Score

Mide qué tan bien separados están los clusters:

```python
Silhouette = (b - a) / max(a, b)

a = distancia promedio intra-cluster
b = distancia promedio al cluster más cercano

Score:
  1.0  → Clusters perfectamente separados
  0.5  → Clusters razonables
  0.0  → Clusters overlapping
  <0.0 → Mal asignados
```

### Interpretación de Clusters

Después de clustering, SIEMPRE analiza:

```python
# Estadísticas por cluster
cluster_stats = df.groupBy("prediction").agg(
    avg("age"),
    avg("salary"),
    avg("web_visits"),
    count("*")
)

# Ejemplo de output:
Cluster 0 (35%): Jóvenes de alto engagement
  - Edad: 28 años
  - Salary: $45K
  - Visitas: 35/mes
  → Estrategia: Contenido educativo, ofertas para startups

Cluster 1 (40%): Profesionales establecidos
  - Edad: 45 años
  - Salary: $95K
  - Visitas: 12/mes
  → Estrategia: ROI demos, enterprise features

Cluster 2 (25%): Low engagement
  - Edad: 38 años
  - Salary: $55K
  - Visitas: 3/mes
  → Estrategia: Re-engagement campaigns
```

---

## 🔄 MLflow: Experiment Tracking

> 📘 **Guía Completa**: Para una guía detallada de MLflow con ejemplos avanzados, instalación paso a paso, Model Registry, y deployment en producción, consulta **[MLFLOW_GUIDE.md](./MLFLOW_GUIDE.md)**

### ¿Por qué MLflow?

**Problema sin MLflow:**
```python
# Experimento 1
model_v1 = train(max_iter=10, max_depth=5)
# AUC = 0.85... pero ¿con qué parámetros exactamente?

# 2 semanas después...
# ¿Cómo reproduzco el modelo de AUC=0.85?
# ¿Qué features usé?
# 😱 No tengo idea
```

**Solución con MLflow:**
```python
import mlflow

# Configurar experimento
mlflow.set_experiment("Lead_Scoring_Production")

with mlflow.start_run(run_name="GBT_v2"):
    # Log parámetros
    mlflow.log_param("max_iter", 10)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("algorithm", "GBT")

    # Entrenar
    model = pipeline.fit(train)

    # Evaluar
    predictions = model.transform(test)
    auc = evaluator.evaluate(predictions)

    # Log métricas
    mlflow.log_metric("auc", auc)
    mlflow.log_metric("accuracy", 0.82)

    # Log modelo para producción
    mlflow.spark.log_model(
        model,
        "model",
        registered_model_name="LeadScoringModel"
    )

# Resultado: Todo trackado automáticamente
# UI: http://localhost:5000
```

### Inicio Rápido con MLflow

```bash
# 1. Instalar
pip install mlflow mlflow[extras]

# 2. Iniciar UI
mlflow ui

# 3. Abrir navegador
open http://localhost:5000

# 4. Ejecutar scripts (ya integrados con MLflow)
python 02-03-ML/lead_scoring.py
python 02-03-ML/customer_segmentation.py
```

### Los 4 Componentes de MLflow

```
┌─────────────────────────────────────┐
│           MLflow Platform           │
├─────────────────────────────────────┤
│ 1. Tracking                         │
│    └─ Log experiments & metrics     │
│                                     │
│ 2. Projects                         │
│    └─ Package code reproducibly     │
│                                     │
│ 3. Models                           │
│    └─ Deploy to production          │
│                                     │
│ 4. Registry                         │
│    └─ Version & govern models       │
└─────────────────────────────────────┘
```

**Ver detalles completos en [MLFLOW_GUIDE.md](./MLFLOW_GUIDE.md)**

### Flujo de Trabajo con MLflow

```
Experimentación
    ↓
[MLflow Tracking] → Log params, metrics, artifacts
    ↓
MLflow UI → Comparar runs
    ↓
Seleccionar mejor modelo
    ↓
[MLflow Registry] → Registrar versión
    ↓
Promover a "Production"
    ↓
[FastAPI/Serving] → Cargar modelo
    ↓
Aplicación en producción
```

### Cargar Modelo en Producción

```python
import mlflow

# Cargar modelo desde Registry
model_uri = "models:/LeadScoringModel/Production"
model = mlflow.spark.load_model(model_uri)

# Hacer predicciones
predictions = model.transform(new_leads_df)
```

---

## 🛠️ Scripts del Módulo

### 1. `lead_scoring.py` - Clasificación Supervisada

**Objetivo**: Predecir conversión de leads

**Flujo:**
```
1. Load data (lead_conversions.csv)
2. Exploratory Data Analysis (EDA)
3. Feature Engineering:
   - StringIndexer para last_action
   - OneHotEncoder
   - VectorAssembler
   - (Opcional) StandardScaler
4. Train 3 modelos:
   - Gradient Boosted Trees
   - Random Forest
   - Logistic Regression
5. Evaluar con 5 métricas:
   - AUC, Accuracy, Precision, Recall, F1
6. Comparar modelos en MLflow
7. Seleccionar mejor modelo
8. Guardar predicciones:
   - Parquet → data/lead_predictions.parquet
   - PostgreSQL → tabla lead_predictions
```

**Comandos:**
```bash
# Generar datos
python scripts/generate_data.py

# Entrenar modelos
python 02-03-ML/lead_scoring.py

# Ver resultados en MLflow UI
mlflow ui
# Abrir http://localhost:5000
```

**Output esperado:**
```
🚀 Iniciando Lead Scoring...
📖 Cargando datos...
✅ 1000 filas cargadas

📊 Tasa de conversión: 30%

🔬 Entrenando modelos...

══════════════════════════════════════════════════
🤖 Entrenando: GBT
📊 Evaluación del modelo: GBT
   AUC (ROC):      0.8234
   Accuracy:       0.7850
   Precision:      0.7456
   Recall:         0.7234
   F1 Score:       0.7343

══════════════════════════════════════════════════
🤖 Entrenando: RF
...

🏆 Resumen:
GBT  -> AUC: 0.8234
RF   -> AUC: 0.8156
LR   -> AUC: 0.7923

✅ Mejor modelo: GBT con AUC=0.8234
```

### 2. `customer_segmentation.py` - Clustering No Supervisado

**Objetivo**: Segmentar clientes en grupos

**Flujo:**
```
1. Load data
2. Feature selection (age, salary, web_visits)
3. StandardScaler (CRÍTICO para K-Means)
4. Elbow Method:
   - Probar K = 2, 3, 4, 5, 6
   - Calcular WSSSE y Silhouette por cada K
   - Graficar para encontrar "codo"
5. Entrenar modelo final con K óptimo
6. Analizar características de cada cluster
7. Asignar nombres interpretables
8. Guardar segmentos
```

**Comandos:**
```bash
python 02-03-ML/customer_segmentation.py
```

**Output esperado:**
```
🔍 Ejecutando Elbow Method...
K=2 -> Silhouette: 0.6234, WSSSE: 450000
K=3 -> Silhouette: 0.7123, WSSSE: 280000  ← Mejor
K=4 -> Silhouette: 0.6845, WSSSE: 220000
K=5 -> Silhouette: 0.6234, WSSSE: 180000

✅ Mejor K=3

🎯 Entrenando modelo final con K=3...

📊 Análisis de Clusters:
══════════════════════════════════════════════════

Cluster 0: Premium (Alto valor)
   - Edad promedio: 52 años
   - Salario promedio: $110,000
   - Visitas promedio: 8

Cluster 1: Engagement Alto (Potencial)
   - Edad promedio: 29 años
   - Salario promedio: $45,000
   - Visitas promedio: 32

Cluster 2: Regular (Nurturing)
   - Edad promedio: 38 años
   - Salario promedio: $62,000
   - Visitas promedio: 12
```

---

## 💡 Mejores Prácticas de ML con Spark

### 1. Train/Test Split

```python
# BIEN: Usar randomSplit con seed
train, test = df.randomSplit([0.8, 0.2], seed=42)

# MAL: Sin seed (no reproducible)
train, test = df.randomSplit([0.8, 0.2])
```

### 2. Avoid Data Leakage

```python
# BIEN: Fit en train, transform en train y test
scaler = StandardScaler()
scaler_model = scaler.fit(train_df)  # Solo aprende de train
train_scaled = scaler_model.transform(train_df)
test_scaled = scaler_model.transform(test_df)

# MAL: Fit en todo el dataset
scaler_model = scaler.fit(full_df)  # ❌ Data leakage!
```

### 3. Pipelines para Deployment

```python
# BIEN: Pipeline serializable
pipeline = Pipeline(stages=[indexer, encoder, assembler, model])
pipeline.fit(train).write().overwrite().save("model/")

# Cargar en producción
model = PipelineModel.load("model/")
predictions = model.transform(new_data)
```

### 4. Feature Importance

```python
# Solo para tree-based models
if hasattr(model.stages[-1], 'featureImportances'):
    importances = model.stages[-1].featureImportances
    print(f"Top feature: {importances.toArray().argmax()}")
```

### 5. Cross-Validation (para datos pequeños-medianos)

```python
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

paramGrid = ParamGridBuilder() \
    .addGrid(gbt.maxDepth, [3, 5, 7]) \
    .addGrid(gbt.maxIter, [10, 20]) \
    .build()

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=paramGrid,
    evaluator=BinaryClassificationEvaluator(),
    numFolds=3
)

cv_model = cv.fit(train)
best_model = cv_model.bestModel
```

---

## 📊 Comparación: MLlib vs Scikit-learn vs PyTorch

| Feature | Spark MLlib | Scikit-learn | PyTorch/TensorFlow |
|---------|-------------|--------------|---------------------|
| **Tamaño de datos** | TB-PB | GB | GB (con dataloader) |
| **Distribución** | Nativa | No (Dask parcial) | Sí (DDL, Horovod) |
| **Algoritmos** | ~20 core | 100+ | Deep Learning |
| **Velocidad (small data)** | Lenta (overhead) | Rápida | Media |
| **Velocidad (big data)** | Rápida | No cabe en RAM | Depende de GPU |
| **Deep Learning** | No | No | Sí |
| **Producción** | MLflow, Spark Serving | Flask, FastAPI | TorchServe, TF Serving |
| **Learning curve** | Media | Baja | Alta |

**Cuándo usar cada uno:**
- **MLlib**: Datos > 100GB, features estructuradas, modelos clásicos
- **Scikit-learn**: Datos < 10GB, prototipado rápido, algoritmos variados
- **PyTorch**: Deep learning, imágenes, texto, series de tiempo complejas

---

## 🚀 Próximos Pasos

Después de dominar este módulo:

1. **[Módulo 04: FastAPI Serving](../04-FastAPI-Serving/README.md)**
   Sirve tus modelos via API REST

2. **[Módulo 08: Streaming ML](../08-Spark-Streaming/README.md)**
   Scoring de leads en tiempo real con Kafka

3. **Avanzado: Hyperparameter Tuning**
   - CrossValidator para grid search
   - TrainValidationSplit para datasets grandes
   - Random search con MLflow

4. **Avanzado: Feature Stores**
   - Feast para feature management
   - Delta Lake para features versionadas

---

## 📚 Referencias y Recursos

### Documentación Oficial
- [Spark MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- [MLlib API Docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.ml.html)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)

### Libros Recomendados
- **"Advanced Analytics with Spark"** - O'Reilly (Capítulos 3-5)
- **"Spark: The Definitive Guide"** - Capítulo 24-27 (ML)
- **"Machine Learning with PySpark"** - Pramod Singh

### Cursos Online
- [Databricks Academy - ML with Spark](https://www.databricks.com/learn/training/lakehouse-fundamentals)
- [Coursera - Big Data Analysis with Scala and Spark](https://www.coursera.org/learn/scala-spark-big-data)

### Papers
- [MLlib: Machine Learning in Apache Spark](https://arxiv.org/abs/1505.06807) - Paper original

---

## ❓ FAQ

**P: ¿MLlib puede competir con XGBoost o LightGBM?**
R: En accuracy pura, no. Pero MLlib GBT es ~80-90% tan bueno y maneja 100x más datos.

**P: ¿Puedo usar modelos de scikit-learn en Spark?**
R: Sí, con Pandas UDFs, pero pierdes distribución. Mejor entrenar en MLlib o usar Ray.

**P: ¿Spark MLlib soporta deep learning?**
R: Limitado. Usa TensorFlow on Spark o PyTorch Lightning para DL distribuido.

**P: ¿Cómo cargo un modelo MLflow en producción?**
R: `mlflow.spark.load_model(model_uri)` o `mlflow.pyfunc.load_model()` para serving sin Spark.

**P: ¿Cuántos datos necesito para que valga la pena Spark?**
R: Regla general: >50GB o >10M filas. Para menos, scikit-learn es más rápido.

---

**¡Comienza con el primer script! 👉 `python 02-03-ML/lead_scoring.py`**
