# Módulo 9: Orquestación de Pipelines ML con Airflow + MLflow

## Teoría: Orquestación de Pipelines de ML

### ¿Qué es la orquestación?
La orquestación en MLOps se refiere a la automatización y coordinación de flujos de trabajo (workflows) de machine learning. Esto incluye:
- Entrenamiento programado de modelos
- Pipelines de datos ETL
- Validación y testing automatizado
- Deployment condicional
- Monitoreo y reentrenamiento

### ¿Por qué Apache Airflow?

**Apache Airflow** es un orquestador de workflows de código abierto que permite:
- Definir workflows como código (Python)
- Programación con cron expressions
- Gestión de dependencias entre tareas
- Monitoreo visual de pipelines
- Retry automático en caso de fallos
- Escalabilidad horizontal

### Conceptos Clave de Airflow

1. **DAG (Directed Acyclic Graph)**: Definición del workflow completo
2. **Task**: Unidad individual de trabajo
3. **Operator**: Plantilla para definir tareas
4. **Sensor**: Espera a que se cumpla una condición
5. **XCom**: Comunicación entre tareas
6. **Schedule**: Frecuencia de ejecución

### Integración Airflow + MLflow

**MLflow** para tracking y **Airflow** para orchestration:
- Airflow ejecuta pipelines ML
- MLflow trackea experimentos dentro de cada tarea
- Registro automático de modelos
- Transiciones de estado en Model Registry
- Deployment condicional basado en métricas

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    Airflow Scheduler                    │
│  (Ejecuta DAGs según schedule)                         │
└────────────┬────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────┐
│                    Airflow DAG                          │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Extract │→ │Transform │→ │  Train  │→ │ Deploy  │ │
│  │  Data   │  │   Data   │  │  Model  │  │  Model  │ │
│  └─────────┘  └──────────┘  └────┬────┘  └─────────┘ │
└────────────────────────────────────│────────────────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    MLflow Tracking    │
                         │  - Parámetros         │
                         │  - Métricas           │
                         │  - Artefactos         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │  MLflow Model Registry│
                         │  - Staging            │
                         │  - Production         │
                         └───────────────────────┘
```

## Estructura del Módulo

```
modulo9-airflow-orchestration/
├── dags/
│   ├── ml_training_pipeline.py
│   ├── etl_feature_engineering.py
│   ├── model_monitoring_pipeline.py
│   └── batch_prediction_pipeline.py
├── plugins/
│   ├── mlflow_operator.py
│   └── custom_sensors.py
├── config/
│   ├── airflow.cfg
│   └── docker-compose.yml
├── scripts/
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── deploy_model.py
└── notebooks/
    ├── 01_airflow_setup.ipynb
    ├── 02_simple_dag.ipynb
    ├── 03_ml_pipeline_dag.ipynb
    └── 04_advanced_orchestration.ipynb
```

## Instalación

```bash
pip install apache-airflow==2.8.1
pip install apache-airflow-providers-docker
pip install mlflow
```

### Inicializar Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

### Iniciar Servicios

```bash
airflow webserver --port 8080
airflow scheduler
```

Airflow UI: http://localhost:8080
MLflow UI: http://localhost:5000

## Casos de Uso

### 1. Pipeline de Entrenamiento Diario
- Extracción de datos nuevos
- Feature engineering
- Entrenamiento de modelo
- Evaluación y comparación
- Registro en MLflow

### 2. Pipeline de Reentrenamiento Condicional
- Monitoreo de métricas en producción
- Detección de drift
- Reentrenamiento automático
- A/B testing

### 3. Pipeline de Batch Predictions
- Carga de datos para scoring
- Inferencia con modelo productivo
- Almacenamiento de resultados
- Notificaciones

## Mejores Prácticas

1. **Idempotencia**: DAGs deben poder ejecutarse múltiples veces sin efectos colaterales
2. **Atomicidad**: Cada tarea debe ser una unidad atómica de trabajo
3. **Logging**: Logging exhaustivo para debugging
4. **Testing**: Test de DAGs antes de deploy
5. **Monitoring**: Alertas en caso de fallos
6. **Versioning**: Control de versiones de DAGs

## Recursos Adicionales

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
- [Best Practices for ML Pipelines](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
