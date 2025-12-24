# Taller Completo de MLOps con MLflow

Taller práctico intensivo de MLOps centrado en MLflow, cubriendo múltiples frameworks (TensorFlow, PyTorch, scikit-learn) y tipos de modelos (ML, DL, RL).

## Objetivos del Taller

- Dominar el tracking de experimentos con MLflow
- Implementar pipelines de ML/DL reproducibles
- Gestionar modelos con MLflow Model Registry
- Integrar MLflow con diferentes frameworks
- Desplegar modelos en producción
- Escalar con Spark + MLflow

## Estructura del Taller

### Módulo 1: Introducción a MLflow con scikit-learn
- Tracking básico de experimentos
- Logging de parámetros, métricas y artefactos
- Modelos de clasificación y regresión
- Pipelines de preprocesamiento

### Módulo 2: MLflow con TensorFlow/Keras
- Tracking de modelos de Deep Learning
- Redes convolucionales (CNN) para visión
- Redes recurrentes (RNN/LSTM) para series temporales
- Callbacks personalizados para logging automático

### Módulo 3: MLflow con PyTorch
- Integración de PyTorch con MLflow
- Transfer Learning con modelos preentrenados
- Arquitecturas personalizadas
- Tracking de gradientes y embeddings

### Módulo 4: Reinforcement Learning con MLflow
- DQN (Deep Q-Network) para juegos
- Policy Gradient methods
- Tracking de episodios y recompensas
- Visualización de políticas aprendidas

### Módulo 5: Pipelines Avanzados
- Hyperparameter tuning con Optuna + MLflow
- AutoML workflows
- Nested runs para experimentos complejos
- Feature engineering pipelines

### Módulo 6: Model Registry
- Gestión del ciclo de vida de modelos
- Versionado y staging (Dev/Staging/Production)
- Transiciones de modelos
- Comparación de versiones

### Módulo 7: MLflow + Spark
- ML distribuido con Spark MLlib
- Logging de modelos Spark
- Pipelines distribuidos
- Entrenamiento a escala

### Módulo 8: Deployment
- Serving de modelos con MLflow
- API REST para inferencia
- Dockerización de modelos
- Monitoring en producción

## Requisitos Previos

- Python 3.8+
- Conocimientos básicos de ML/DL
- Familiaridad con Jupyter notebooks
- (Opcional) Apache Spark para módulo 7

## Instalación

```bash
cd mlflow-mlops-workshop
pip install -r requirements.txt
```

## Configuración de MLflow

```bash
mlflow ui
```

El servidor UI estará disponible en http://localhost:5000

## Ejecución de los Módulos

Cada módulo contiene notebooks numerados que deben ejecutarse en orden:

```bash
cd modulo1-sklearn
jupyter notebook
```

## Datasets

Los datasets se descargan automáticamente o se encuentran en la carpeta `datasets/`.

## Estructura de Archivos

```
mlflow-mlops-workshop/
├── modulo1-sklearn/
│   ├── 01_mlflow_basics.ipynb
│   ├── 02_classification_pipeline.ipynb
│   └── 03_regression_advanced.ipynb
├── modulo2-tensorflow/
│   ├── 01_cnn_image_classification.ipynb
│   ├── 02_rnn_time_series.ipynb
│   └── 03_transfer_learning.ipynb
├── modulo3-pytorch/
│   ├── 01_pytorch_basics_mlflow.ipynb
│   ├── 02_custom_architectures.ipynb
│   └── 03_lightning_integration.ipynb
├── modulo4-reinforcement-learning/
│   ├── 01_dqn_cartpole.ipynb
│   ├── 02_policy_gradient.ipynb
│   └── 03_advanced_rl.ipynb
├── modulo5-pipelines-avanzados/
│   ├── 01_hyperparameter_tuning.ipynb
│   ├── 02_automl_workflows.ipynb
│   └── 03_nested_runs.ipynb
├── modulo6-model-registry/
│   ├── 01_registry_basics.ipynb
│   ├── 02_model_lifecycle.ipynb
│   └── 03_production_deployment.ipynb
├── modulo7-spark-mlflow/
│   ├── 01_spark_ml_basics.ipynb
│   ├── 02_distributed_training.ipynb
│   └── 03_large_scale_pipeline.ipynb
└── modulo8-deployment/
    ├── 01_model_serving.ipynb
    ├── 02_rest_api.ipynb
    └── 03_docker_deployment.ipynb
```

## Recursos Adicionales

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow GitHub](https://github.com/mlflow/mlflow)
- Presentaciones y slides en cada módulo

## Contribuciones

Este taller es de código abierto. Pull requests y sugerencias son bienvenidas.

## Licencia

MIT License
