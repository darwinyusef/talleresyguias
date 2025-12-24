# Contenido Completo del Taller MLOps con MLflow

## 📚 Resumen del Taller

Este taller completo de MLOps está centrado 100% en **MLflow** como herramienta principal de tracking, gestión de modelos y deployment, cubriendo múltiples frameworks de ML/DL y casos de uso avanzados.

### 🎯 Diferencias con otros talleres de MLOps

Este taller es único porque:
- **Foco exclusivo en MLflow**: Cada módulo profundiza en features específicas de MLflow
- **Multi-framework**: Cubre scikit-learn, TensorFlow, PyTorch y Spark
- **Teoría + Práctica**: Cada notebook incluye explicaciones teóricas detalladas
- **Airflow Integration**: Orquestación de pipelines ML completos
- **Spark para Big Data**: ML distribuido con tracking en MLflow
- **Ejemplos originales**: No reutiliza ejercicios de otros repos

---

## 📂 Estructura Completa del Proyecto

```
mlflow-mlops-workshop/
│
├── README.md                           # Descripción general del taller
├── GETTING_STARTED.md                  # Guía de inicio rápido
├── CONTENIDO_COMPLETO.md               # Este archivo
├── requirements.txt                    # Dependencias Python
├── setup.sh                            # Script de instalación automatizado
│
├── modulo1-sklearn/                    # ⭐ Fundamentos MLflow + scikit-learn
│   ├── 01_mlflow_basics.ipynb         # Conceptos básicos de MLflow
│   ├── 02_classification_pipeline.ipynb # Pipelines de clasificación
│   └── 03_regression_advanced.ipynb    # Regresión avanzada con regularización
│
├── modulo2-tensorflow/                 # ⭐ Deep Learning con TensorFlow/Keras
│   ├── 01_cnn_image_classification.ipynb # CNNs para visión por computadora
│   └── 02_rnn_time_series.ipynb       # RNN/LSTM para series temporales
│
├── modulo3-pytorch/                    # ⭐ PyTorch con MLflow
│   └── 01_pytorch_basics_mlflow.ipynb  # PyTorch basics + custom training loops
│
├── modulo7-spark-mlflow/               # ⭐ ML Distribuido con Spark
│   └── 01_spark_ml_basics.ipynb       # Spark MLlib + MLflow integration
│
└── modulo9-airflow-orchestration/      # ⭐ Orquestación con Airflow
    ├── README.md                       # Documentación de Airflow + MLflow
    ├── dags/
    │   ├── ml_training_pipeline.py     # Pipeline de entrenamiento automatizado
    │   └── batch_prediction_pipeline.py # Pipeline de predicciones en batch
    ├── plugins/                        # (Para custom operators)
    ├── config/                         # (Configuraciones)
    └── scripts/                        # (Scripts auxiliares)
```

---

## 📖 Detalle de Contenidos por Módulo

### Módulo 1: MLflow con scikit-learn (3 notebooks)

#### `01_mlflow_basics.ipynb` - Fundamentos de MLflow
**Duración**: ~1 hora
**Teoría cubierta**:
- ¿Qué es MLflow y por qué usarlo?
- 4 componentes de MLflow: Tracking, Projects, Models, Registry
- Conceptos de Run, Experiment, Artifact

**Práctica**:
- Configuración de tracking URI
- Crear y gestionar experiments
- Logging de parámetros con `mlflow.log_param()`
- Logging de métricas con `mlflow.log_metric()`
- Logging de artefactos (gráficos, archivos)
- Guardar modelos con `mlflow.sklearn.log_model()`
- Cargar modelos con `mlflow.sklearn.load_model()`
- Búsqueda y comparación de runs

**Datasets**: Iris, Wine

#### `02_classification_pipeline.ipynb` - Pipelines de Clasificación
**Duración**: ~1.5 horas
**Teoría cubierta**:
- Pipelines de scikit-learn
- Preprocesamiento reproducible
- Nested runs en MLflow
- Cross-validation

**Práctica**:
- Crear pipelines con VectorAssembler + Scaler + Model
- Nested runs para experimentos jerárquicos
- Comparación sistemática de scalers
- Comparación de 7 algoritmos de clasificación
- Cross-validation con tracking
- Visualizaciones automáticas
- Feature importance

**Datasets**: Breast Cancer Wisconsin
**Modelos**: LogisticRegression, DecisionTree, RandomForest, GradientBoosting, SVM, KNN, NaiveBayes

#### `03_regression_advanced.ipynb` - Regresión Avanzada
**Duración**: ~1.5 horas
**Teoría cubierta**:
- Tipos de regresión (Linear, Ridge, Lasso, ElasticNet)
- Regularización L1 y L2
- Modelos basados en árboles para regresión
- Métricas de regresión (MAE, MSE, RMSE, R², MAPE)
- Análisis de residuos

**Práctica**:
- Comparación de métodos de regularización
- Feature selection con Lasso
- Tree-based regressors
- Análisis de residuos (scatter plots, histogramas, Q-Q plots)
- Feature importance tracking
- Comparación global de modelos

**Datasets**: California Housing
**Modelos**: LinearRegression, Ridge, Lasso, ElasticNet, RandomForest, GradientBoosting, ExtraTrees

**Total Módulo 1**: ~4 horas | 3 notebooks | 15+ modelos trackeados

---

### Módulo 2: Deep Learning con TensorFlow/Keras (2 notebooks)

#### `01_cnn_image_classification.ipynb` - CNNs
**Duración**: ~2 horas
**Teoría cubierta**:
- Redes Neuronales Convolucionales (CNNs)
- Capas convolucionales y pooling
- Batch Normalization
- Dropout
- Data Augmentation
- Funciones de activación

**Práctica**:
- CNN simple (2 capas conv)
- CNN avanzada (Batch Normalization + Dropout)
- Custom MLflow callbacks para logging automático
- Logging de métricas por época
- Confusion matrices
- Training history plots
- EarlyStopping y ReduceLROnPlateau
- ImageDataGenerator para augmentation

**Datasets**: MNIST
**Arquitecturas**: SimpleCNN, AdvancedCNN

#### `02_rnn_time_series.ipynb` - RNN/LSTM
**Duración**: ~2 horas
**Teoría cubierta**:
- Redes Neuronales Recurrentes (RNN)
- LSTM y GRU
- Vanishing gradients
- Bidirectional RNNs
- Sequence prediction
- Multi-step forecasting

**Práctica**:
- Generación de series temporales sintéticas
- Preparación de secuencias para RNN
- LSTM simple
- Stacked Bidirectional LSTM
- Multi-step forecasting
- Logging de métricas por horizonte
- Visualización de predicciones temporales

**Datasets**: Serie temporal sintética (tendencia + estacionalidad + ruido)
**Arquitecturas**: SimpleLSTM, StackedBidirectionalLSTM, MultistepLSTM

**Total Módulo 2**: ~4 horas | 2 notebooks | 6+ arquitecturas de DL

---

### Módulo 3: PyTorch (1 notebook)

#### `01_pytorch_basics_mlflow.ipynb` - PyTorch Fundamentals
**Duración**: ~2 horas
**Teoría cubierta**:
- PyTorch vs TensorFlow
- nn.Module
- Autograd
- Training loops explícitos
- DataLoader y Dataset
- GPU acceleration

**Práctica**:
- Fully Connected Network (SimpleNN)
- Custom training loop
- Evaluation loop
- CNN con PyTorch (ConvNet)
- Learning rate scheduling
- Model checkpointing
- Logging manual de métricas
- GPU/CPU device handling

**Datasets**: Fashion MNIST
**Arquitecturas**: SimpleNN, ConvNet

**Total Módulo 3**: ~2 horas | 1 notebook | 2 arquitecturas PyTorch

---

### Módulo 7: Spark + MLflow (1 notebook)

#### `01_spark_ml_basics.ipynb` - ML Distribuido
**Duración**: ~2.5 horas
**Teoría cubierta**:
- Apache Spark para ML
- Arquitectura distribuida
- Spark MLlib
- Pipelines de Spark
- CrossValidator para tuning distribuido

**Práctica**:
- Configuración de SparkSession
- DataFrames distribuidos
- VectorAssembler y transformers
- Pipelines de Spark
- Comparación de modelos distribuidos
- CrossValidator con grid search
- Logging de modelos Spark en MLflow
- Carga de modelos Spark desde MLflow

**Datasets**: Synthetic (100,000 muestras)
**Modelos**: LogisticRegression, RandomForest, GBTClassifier (Spark versions)

**Total Módulo 7**: ~2.5 horas | 1 notebook | ML a escala

---

### Módulo 9: Airflow Orchestration (2 DAGs)

#### `ml_training_pipeline.py` - Pipeline de Entrenamiento
**Duración setup**: ~1 hora
**Componentes**:
- Extract: Generación de datos
- Preprocess: Feature engineering
- Train: Entrenamiento paralelo de 3 modelos (RF, GB, LR)
- Compare: Selección del mejor modelo
- Register: Registro en Model Registry
- Notify: Notificaciones

**Features MLflow**:
- Logging automático desde Airflow tasks
- XCom para pasar run_ids
- Registro condicional en Model Registry
- Transición a Staging basada en métricas
- Nested runs desde Airflow

**Tecnologías**: Airflow + MLflow + scikit-learn

#### `batch_prediction_pipeline.py` - Predicciones en Batch
**Duración setup**: ~1 hora
**Componentes**:
- Check model: Verificar modelo en Production/Staging
- Load model: Cargar desde MLflow
- Generate data: Datos para scoring
- Predict: Inferencia en batch
- Log predictions: Tracking de batch runs
- Quality check: Detección de drift
- Alert: Notificación de reentrenamiento

**Features MLflow**:
- Carga de modelos productivos
- Logging de batch predictions
- Monitoring de confianza
- Conditional workflows

**Total Módulo 9**: ~2 horas setup | 2 DAGs | Orchestration completa

---

## 📊 Resumen Cuantitativo del Taller

| Métrica | Cantidad |
|---------|----------|
| **Módulos** | 5 módulos principales |
| **Notebooks** | 8 notebooks interactivos |
| **DAGs de Airflow** | 2 pipelines completos |
| **Frameworks** | 4 (scikit-learn, TensorFlow, PyTorch, Spark) |
| **Modelos entrenados** | 30+ modelos diferentes |
| **Datasets** | 8 datasets distintos |
| **Horas de contenido** | 15-20 horas |
| **Líneas de código** | ~5,000+ líneas |
| **Teoría** | Explicaciones detalladas en cada notebook |

---

## 🎓 Habilidades que Adquirirás

### Nivel Básico
- ✅ Configurar MLflow tracking server
- ✅ Crear y gestionar experiments
- ✅ Logging de parámetros, métricas y artefactos
- ✅ Guardar y cargar modelos
- ✅ Navegar MLflow UI

### Nivel Intermedio
- ✅ Pipelines reproducibles con scikit-learn
- ✅ Nested runs para experimentos complejos
- ✅ Custom callbacks para TensorFlow/Keras
- ✅ Training loops personalizados con PyTorch
- ✅ Model Registry básico
- ✅ Comparación sistemática de modelos

### Nivel Avanzado
- ✅ Deep Learning tracking (CNN, RNN/LSTM)
- ✅ ML distribuido con Spark + MLflow
- ✅ Orquestación con Airflow
- ✅ Pipelines de producción
- ✅ Batch predictions con monitoring
- ✅ Conditional workflows
- ✅ Model lifecycle management

---

## 🔧 Tecnologías y Herramientas

### Core MLOps
- **MLflow 2.10.2**: Tracking, Registry, Models, Projects
- **Apache Airflow 2.8.1**: Workflow orchestration
- **Apache Spark 3.5.0**: Distributed ML

### ML/DL Frameworks
- **scikit-learn 1.3.0**: ML clásico
- **TensorFlow 2.15.0**: Deep Learning
- **Keras 2.15.0**: High-level DL API
- **PyTorch 2.1.2**: Deep Learning research
- **PyTorch Lightning 2.1.3**: Structured PyTorch

### Hyperparameter Tuning
- **Optuna 3.5.0**: AutoML optimization
- **Hyperopt 0.2.7**: Distributed tuning

### Boosting Libraries
- **XGBoost 2.0.3**: Gradient boosting
- **LightGBM 4.1.0**: Fast boosting
- **CatBoost 1.2.2**: Categorical boosting

### Utilities
- **Pandas 2.0.3**: Data manipulation
- **NumPy 1.24.3**: Numerical computing
- **Matplotlib 3.7.2**: Visualization
- **Seaborn 0.12.2**: Statistical viz

---

## 🚀 Quick Start (3 comandos)

```bash
cd mlflow-mlops-workshop

./setup.sh

./start_mlflow.sh
```

Abre http://localhost:5000 y empieza con `modulo1-sklearn/01_mlflow_basics.ipynb`

---

## 📈 Roadmap de Aprendizaje Sugerido

### Semana 1: Fundamentos
- Día 1-2: Módulo 1 (scikit-learn + MLflow basics)
- Día 3-4: Módulo 2 (TensorFlow/Keras)
- Día 5: Revisión y práctica

### Semana 2: Avanzado
- Día 1-2: Módulo 3 (PyTorch)
- Día 3: Módulo 7 (Spark)
- Día 4-5: Módulo 9 (Airflow)

### Semana 3: Proyecto
- Aplicar conceptos a proyecto personal
- Implementar CI/CD
- Deploy en cloud

---

## 🎯 Casos de Uso Cubiertos

1. **Clasificación binaria y multiclase**
   - Iris classification
   - Breast cancer detection
   - Fashion MNIST

2. **Regresión**
   - House price prediction
   - Feature importance analysis

3. **Computer Vision**
   - Image classification con CNNs
   - Data augmentation

4. **Time Series**
   - Forecasting con LSTM
   - Multi-step predictions

5. **Distributed ML**
   - Large-scale classification con Spark
   - Hyperparameter tuning distribuido

6. **Production Pipelines**
   - Automated training workflows
   - Batch predictions
   - Model monitoring

---

## 💡 Mejores Prácticas Enseñadas

1. **Experiment Organization**
   - Naming conventions
   - Nested runs para comparaciones
   - Tags para categorización

2. **Reproducibilidad**
   - Logging de random seeds
   - Tracking de versions de librerías
   - Pipelines determinísticos

3. **Model Governance**
   - Model Registry stages
   - Version control
   - Approval workflows

4. **Performance**
   - Distributed training con Spark
   - GPU acceleration
   - Efficient data loading

5. **Production**
   - Automated pipelines
   - Monitoring y alerting
   - Conditional deployment

---

## 📚 Recursos Adicionales Incluidos

- **GETTING_STARTED.md**: Guía de instalación detallada
- **setup.sh**: Script de instalación automatizado
- **start_mlflow.sh**: Script para iniciar MLflow (generado)
- **start_airflow.sh**: Script para iniciar Airflow (generado)
- **Documentación inline**: Cada notebook incluye teoría y explicaciones

---

## ✨ Características Únicas de este Taller

1. **100% MLflow-centric**: Todo gira alrededor de MLflow
2. **Multi-framework**: No te limita a un solo framework
3. **Teoría integrada**: No solo código, aprende los conceptos
4. **Ejemplos originales**: Código escrito específicamente para este taller
5. **Producción-ready**: No solo experimentación, también deployment
6. **Escalable**: Desde laptop hasta cluster Spark
7. **Airflow integration**: Orquestación real de pipelines

---

## 🎓 Certificación Informal

Al completar este taller, habrás:

✅ Trackeado 30+ modelos de ML/DL
✅ Trabajado con 4 frameworks diferentes
✅ Implementado pipelines de producción
✅ Usado ML distribuido con Spark
✅ Orquestado workflows con Airflow
✅ Aplicado mejores prácticas de MLOps

**¡Estás listo para implementar MLflow en proyectos reales!**

---

**Autor**: MLOps Workshop Team
**Versión**: 1.0
**Fecha**: Diciembre 2024
**Licencia**: MIT

Para preguntas o contribuciones, consulta el README.md principal.
