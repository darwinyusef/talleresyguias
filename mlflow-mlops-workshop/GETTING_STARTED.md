# Guía de Inicio Rápido - Taller MLOps con MLflow

## Configuración del Entorno

### Paso 1: Requisitos Previos

```bash
python --version
```

Asegúrate de tener Python 3.8 o superior.

### Paso 2: Crear Entorno Virtual

```bash
cd mlflow-mlops-workshop
python -m venv venv

source venv/bin/activate
```

En Windows:
```bash
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota**: La instalación puede tomar 10-15 minutos.

### Paso 4: Iniciar MLflow Tracking Server

En una terminal separada:

```bash
cd mlflow-mlops-workshop
source venv/bin/activate
mlflow server --host 127.0.0.1 --port 5000
```

Abre tu navegador en: http://localhost:5000

### Paso 5: (Opcional) Configurar Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init

airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

Iniciar Airflow (en terminales separadas):

```bash
airflow webserver --port 8080

airflow scheduler
```

Airflow UI: http://localhost:8080

## Estructura del Taller

```
mlflow-mlops-workshop/
├── modulo1-sklearn/           # scikit-learn + MLflow
│   ├── 01_mlflow_basics.ipynb
│   ├── 02_classification_pipeline.ipynb
│   └── 03_regression_advanced.ipynb
│
├── modulo2-tensorflow/        # Deep Learning con TensorFlow
│   ├── 01_cnn_image_classification.ipynb
│   └── 02_rnn_time_series.ipynb
│
├── modulo3-pytorch/           # PyTorch
│   └── 01_pytorch_basics_mlflow.ipynb
│
├── modulo7-spark-mlflow/      # Spark MLlib
│   └── 01_spark_ml_basics.ipynb
│
└── modulo9-airflow-orchestration/  # Airflow
    └── dags/
        ├── ml_training_pipeline.py
        └── batch_prediction_pipeline.py
```

## Ejecución de Módulos

### Módulo 1: scikit-learn

```bash
cd modulo1-sklearn
jupyter notebook
```

Abre y ejecuta en orden:
1. `01_mlflow_basics.ipynb`
2. `02_classification_pipeline.ipynb`
3. `03_regression_advanced.ipynb`

**Duración estimada**: 2-3 horas

**Conceptos que aprenderás**:
- Configuración de MLflow
- Tracking de experimentos
- Logging de parámetros, métricas y artefactos
- Comparación de modelos
- Model Registry básico

### Módulo 2: TensorFlow/Keras

```bash
cd modulo2-tensorflow
jupyter notebook
```

**Duración estimada**: 3-4 horas

**Conceptos que aprenderás**:
- CNNs para clasificación de imágenes
- RNN/LSTM para series temporales
- Custom callbacks de MLflow
- Tracking de Deep Learning
- Data augmentation

### Módulo 3: PyTorch

```bash
cd modulo3-pytorch
jupyter notebook
```

**Duración estimada**: 2-3 horas

**Conceptos que aprenderás**:
- PyTorch basics con MLflow
- Training loops personalizados
- GPU acceleration
- Model checkpointing

### Módulo 7: Spark MLlib

**Prerequisito**: Asegúrate de tener Java instalado:
```bash
java -version
```

```bash
cd modulo7-spark-mlflow
jupyter notebook
```

**Duración estimada**: 2-3 horas

**Conceptos que aprenderás**:
- ML distribuido con Spark
- Pipelines de Spark
- CrossValidation distribuido
- Integración Spark + MLflow

### Módulo 9: Airflow

**Prerequisito**: MLflow server debe estar corriendo

1. Copiar DAGs al directorio de Airflow:
```bash
cp modulo9-airflow-orchestration/dags/*.py $AIRFLOW_HOME/dags/
```

2. Activar DAG en Airflow UI
3. Ejecutar manualmente o esperar schedule

**Duración estimada**: 2-3 horas

**Conceptos que aprenderás**:
- Orquestación de pipelines ML
- Airflow + MLflow integration
- Pipelines de entrenamiento automatizados
- Batch predictions
- Conditional workflows

## Flujo de Trabajo Recomendado

### Día 1: Fundamentos (4-5 horas)
- ✅ Configuración del entorno
- ✅ Módulo 1: scikit-learn básico
- ✅ Exploración de MLflow UI

### Día 2: Deep Learning (6-7 horas)
- ✅ Módulo 2: TensorFlow/Keras
- ✅ Módulo 3: PyTorch básico

### Día 3: Avanzado (5-6 horas)
- ✅ Módulo 7: Spark + MLflow
- ✅ Módulo 9: Airflow orchestration

## Recursos Adicionales

### Documentación Oficial
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Spark MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)

### Comandos Útiles de MLflow

#### Ver experimentos:
```bash
mlflow experiments list
```

#### Servir modelo:
```bash
mlflow models serve -m runs:/<RUN_ID>/model -p 5001
```

#### Hacer predicción:
```bash
curl -X POST http://127.0.0.1:5001/invocations \
  -H 'Content-Type: application/json' \
  -d '{"columns": ["feature1", "feature2"], "data": [[1.0, 2.0]]}'
```

#### Limpiar runs antiguos:
```python
import mlflow
client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name("experiment-name")
runs = client.search_runs(experiment.experiment_id)
for run in runs:
    client.delete_run(run.info.run_id)
```

## Troubleshooting

### Problema: MLflow UI no carga

**Solución**:
```bash
pkill -f "mlflow server"

mlflow server --host 127.0.0.1 --port 5000
```

### Problema: Error de memoria con Spark

**Solución**: Reducir memoria en SparkSession:
```python
spark = SparkSession.builder \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()
```

### Problema: ImportError con TensorFlow

**Solución**:
```bash
pip uninstall tensorflow
pip install tensorflow==2.15.0
```

### Problema: Airflow DAGs no aparecen

**Solución**:
```bash
airflow dags list

airflow dags trigger <dag_id>
```

## Limpieza

Para limpiar el entorno después del taller:

```bash
deactivate

rm -rf venv/
rm -rf mlruns/
rm -rf airflow/
rm -rf data/
```

## Próximos Pasos

Después de completar el taller:

1. **Proyecto Personal**: Aplica MLflow a tu propio proyecto de ML
2. **CI/CD**: Integra MLflow con GitHub Actions o Jenkins
3. **Producción**: Despliega modelos en AWS, Azure o GCP
4. **Monitoreo**: Implementa drift detection y retraining automático
5. **Comunidad**: Contribuye a MLflow en GitHub

## Soporte

Si encuentras problemas:
1. Revisa los logs de MLflow: `mlflow server` output
2. Verifica versiones de librerías: `pip list`
3. Consulta la documentación oficial de MLflow
4. Revisa issues en GitHub: https://github.com/mlflow/mlflow/issues

## Certificado

¡Felicitaciones por completar el taller!

Has adquirido habilidades en:
- ✅ MLOps fundamentals
- ✅ Experiment tracking
- ✅ Model versioning
- ✅ Pipeline orchestration
- ✅ Distributed ML
- ✅ Model deployment

Continúa practicando y construyendo proyectos MLOps.

---

**Autor**: MLOps Workshop Team
**Versión**: 1.0
**Última actualización**: 2024
