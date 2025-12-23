# 🗓️ Módulo 05: Orquestación con Apache Airflow + Spark

Aprende a orquestar pipelines complejos de Machine Learning y Big Data con **Apache Airflow**, el estándar de facto para workflow orchestration en producción.

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Entender los fundamentos de workflow orchestration
- ✅ Diseñar DAGs (Directed Acyclic Graphs) escalables
- ✅ Integrar Spark jobs con Airflow usando SparkSubmitOperator
- ✅ Implementar patrones de scheduling (diario, semanal, backfilling)
- ✅ Manejar dependencias entre tareas y pipelines
- ✅ Configurar retries, alertas y SLAs
- ✅ Monitorear pipelines en producción
- ✅ Aplicar mejores prácticas de DataOps y MLOps

---

## 📚 Fundamentos Teóricos

### ¿Qué es Workflow Orchestration?

**Workflow Orchestration** es el proceso de automatizar, coordinar y monitorear tareas que forman un pipeline de datos.

```
Sin Orquestación                    Con Airflow
═══════════════════════════════════════════════════════
cron job 1 → script1.py             DAG con dependencias
cron job 2 → script2.py      →      Retry automático
cron job 3 → script3.py             Monitoreo centralizado
bash scripts manuales               Lineage de datos
email si falla (maybe)              Alertas configurables
```

**Problemas que resuelve:**

| Sin Orquestador | Con Airflow |
|----------------|-------------|
| ❌ Scripts dispersos en cron | ✅ DAGs centralizados en código |
| ❌ Dependencias implícitas | ✅ Grafo de dependencias explícito |
| ❌ No hay historial | ✅ Logs y métricas por ejecución |
| ❌ Retries manuales | ✅ Retries configurables |
| ❌ Difícil debugging | ✅ UI con estado de cada tarea |
| ❌ No hay lineage | ✅ Visualización completa del flujo |

---

### ¿Qué es Apache Airflow?

**Apache Airflow** es una plataforma open-source para crear, programar y monitorear workflows programáticamente.

**Creado por:** Airbnb en 2014, donado a Apache en 2016

**Casos de uso:**
- 🏭 ETL/ELT pipelines (data warehouses)
- 🤖 ML training y re-training automático
- 📊 Generación de reportes y dashboards
- 🔄 Data Lake management (Bronze → Silver → Gold)
- 📡 Integración de sistemas (APIs, databases, S3)

**Características Clave:**
- ✅ **Workflows como código** (Python): Versionables en Git
- ✅ **DAG-based**: Grafos dirigidos acíclicos
- ✅ **Extensible**: 100+ operators built-in + custom
- ✅ **UI web interactiva**: Monitoreo y debugging
- ✅ **Scheduler robusto**: Cron-like con backfilling
- ✅ **Escalable**: Workers distribuidos con Celery/Kubernetes

---

## 🏗️ Arquitectura de Airflow

```
┌─────────────────────────────────────────────────────────┐
│                    Airflow Architecture                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────────┐         ┌──────────────┐            │
│  │   Web Server  │ ◄───────┤   Metadata   │            │
│  │   (Flask)     │         │   Database   │            │
│  └───────┬───────┘         │  (Postgres)  │            │
│          │                 └──────▲───────┘            │
│          │                        │                     │
│  ┌───────▼───────┐                │                     │
│  │   Scheduler   │ ───────────────┘                     │
│  │  (DAG Parser) │                                      │
│  └───────┬───────┘                                      │
│          │                                               │
│          │  Enqueue Tasks                               │
│          ▼                                               │
│  ┌───────────────┐         ┌──────────────┐            │
│  │    Executor   │ ◄──────►│   Workers    │            │
│  │ (Local/Celery)│         │ (Task Exec)  │            │
│  └───────────────┘         └──────────────┘            │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Componentes Principales

**1. Web Server**
- UI para visualizar DAGs, tareas, logs
- Puerto default: 8080
- Framework: Flask

**2. Scheduler**
- Parsea archivos de DAGs (`dags/` folder)
- Determina qué tareas ejecutar y cuándo
- Envía tareas al Executor

**3. Metadata Database**
- Almacena estado de DAGs, tareas, variables, connections
- PostgreSQL (producción) o SQLite (desarrollo)

**4. Executor**
- **SequentialExecutor**: Una tarea a la vez (dev only)
- **LocalExecutor**: Múltiples tareas en paralelo (una máquina)
- **CeleryExecutor**: Workers distribuidos (producción)
- **KubernetesExecutor**: Cada tarea en un pod (cloud-native)

**5. Workers**
- Ejecutan las tareas asignadas por el Executor
- Pueden estar en múltiples máquinas

---

## 📊 Conceptos Fundamentales

### 1. DAG (Directed Acyclic Graph)

Un **DAG** define el flujo de trabajo: qué tareas ejecutar, en qué orden, y con qué frecuencia.

```python
from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'spark_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline con Spark',
    schedule_interval='0 2 * * *',  # Diario a las 2 AM
    catchup=False,
    tags=['spark', 'etl', 'production'],
)
```

**Parámetros Clave:**
- `dag_id`: Identificador único
- `schedule_interval`: Cron expression o preset (`@daily`, `@hourly`)
- `start_date`: Cuándo comenzar a ejecutar
- `catchup`: Si ejecutar runs pasados (backfill)
- `max_active_runs`: Ejecuciones concurrentes del DAG

### 2. Operators (Tareas)

Los **Operators** definen unidades de trabajo individuales.

**Operators más comunes:**

| Operator | Uso |
|----------|-----|
| `BashOperator` | Ejecutar comandos bash |
| `PythonOperator` | Ejecutar funciones Python |
| `SparkSubmitOperator` | Lanzar Spark jobs |
| `S3ToRedshiftOperator` | Mover datos S3 → Redshift |
| `PostgresOperator` | Ejecutar SQL en Postgres |
| `EmailOperator` | Enviar notificaciones |
| `HttpSensor` | Esperar endpoint HTTP |
| `ExternalTaskSensor` | Esperar otro DAG |

**Ejemplo:**
```python
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

task_1 = BashOperator(
    task_id='prepare_data',
    bash_command='python scripts/generate_data.py',
    dag=dag,
)

task_2 = SparkSubmitOperator(
    task_id='train_model',
    application='/path/to/lead_scoring.py',
    conn_id='spark_default',
    dag=dag,
)
```

### 3. Dependencias entre Tareas

Define el orden de ejecución:

```python
# Sintaxis 1: Bitshift operators (recomendado)
task_1 >> task_2 >> task_3

# Sintaxis 2: Método set_downstream
task_1.set_downstream(task_2)

# Fan-out (una tarea → múltiples)
task_1 >> [task_2, task_3, task_4]

# Fan-in (múltiples → una tarea)
[task_2, task_3, task_4] >> task_5
```

**Ejemplo de Pipeline Complejo:**
```python
start = BashOperator(task_id='start', ...)
extract_api = PythonOperator(task_id='extract_api', ...)
extract_db = PythonOperator(task_id='extract_db', ...)
transform = SparkSubmitOperator(task_id='transform', ...)
load_warehouse = PostgresOperator(task_id='load_warehouse', ...)
load_s3 = BashOperator(task_id='load_s3', ...)
notify = EmailOperator(task_id='notify_success', ...)

start >> [extract_api, extract_db] >> transform >> [load_warehouse, load_s3] >> notify
```

### 4. Schedule Interval (Cron Expressions)

```python
# Presets
schedule_interval='@daily'      # 00:00 cada día
schedule_interval='@hourly'     # Cada hora
schedule_interval='@weekly'     # Domingo 00:00
schedule_interval='@monthly'    # Día 1 del mes 00:00

# Cron custom
schedule_interval='0 2 * * *'   # Diario a las 2 AM
schedule_interval='*/15 * * * *'  # Cada 15 minutos
schedule_interval='0 0 * * 1'   # Lunes a medianoche
schedule_interval='0 8 1 * *'   # Día 1 del mes a las 8 AM

# Manual only
schedule_interval=None
```

**Formato Cron:**
```
 ┌────── minuto (0-59)
 │ ┌──── hora (0-23)
 │ │ ┌── día del mes (1-31)
 │ │ │ ┌─ mes (1-12)
 │ │ │ │ ┌─ día de la semana (0-6, 0=domingo)
 │ │ │ │ │
 * * * * *
```

### 5. Execution Date vs Logical Date

**Concepto clave:** El `execution_date` en Airflow NO es "cuándo se ejecuta", sino **el inicio del intervalo de datos procesados**.

```
DAG con schedule_interval='@daily'

execution_date: 2024-01-15 00:00:00
↓
Se ejecuta DESPUÉS del intervalo: 2024-01-16 00:00:00
↓
Procesa datos del día: 2024-01-15
```

**Ejemplo:**
```python
# DAG con schedule @daily que procesa datos del día anterior
execution_date = {{ ds }}  # 2024-01-15
data_date = execution_date  # Procesar datos de este día
```

---

## 🔗 Integración Spark + Airflow

### Opción 1: SparkSubmitOperator (Recomendado)

El **SparkSubmitOperator** ejecuta `spark-submit` remotamente.

```python
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

train_model = SparkSubmitOperator(
    task_id='train_lead_scoring_model',
    application='/opt/spark/jobs/lead_scoring.py',
    conn_id='spark_default',
    conf={
        'spark.executor.memory': '4g',
        'spark.executor.cores': '2',
        'spark.driver.memory': '2g',
    },
    application_args=[
        '--input-path', 's3a://datalake/silver/leads/',
        '--output-path', 's3a://datalake/gold/predictions/',
        '--model-type', 'gbt',
    ],
    dag=dag,
)
```

**Configurar Conexión en Airflow:**
1. Ir a Admin → Connections en la UI
2. Crear nueva conexión:
   - Conn Id: `spark_default`
   - Conn Type: `Spark`
   - Host: `spark://spark-master`
   - Port: `7077`

### Opción 2: BashOperator con spark-submit

Para control fino del comando:

```python
from airflow.operators.bash import BashOperator

train_model = BashOperator(
    task_id='train_model',
    bash_command="""
    spark-submit \
      --master spark://spark-master:7077 \
      --deploy-mode client \
      --executor-memory 4G \
      --num-executors 2 \
      /opt/spark/jobs/lead_scoring.py \
      --date {{ ds }}
    """,
    dag=dag,
)
```

### Opción 3: KubernetesPodOperator (Cloud Native)

Ejecuta cada Spark job en un pod de Kubernetes:

```python
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

train_model = KubernetesPodOperator(
    task_id='train_model_k8s',
    name='spark-ml-job',
    namespace='spark',
    image='my-spark-image:3.4.0',
    cmds=['spark-submit'],
    arguments=[
        '--master', 'k8s://https://kubernetes.default.svc',
        '/opt/spark/jobs/lead_scoring.py',
    ],
    get_logs=True,
    dag=dag,
)
```

---

## 📝 Ejemplo Completo: DAG de MLOps

Este DAG implementa un pipeline completo de ML: generación de datos, entrenamiento, evaluación y deployment.

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'ml_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['ml-team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

dag = DAG(
    'spark_mlops_pipeline',
    default_args=default_args,
    description='Pipeline MLOps: Train, Evaluate, Deploy',
    schedule_interval='0 2 * * *',  # Diario a las 2 AM
    catchup=False,
    tags=['spark', 'ml', 'production'],
)

start = BashOperator(
    task_id='start_pipeline',
    bash_command='echo "Starting MLOps pipeline for {{ ds }}"',
    dag=dag,
)

generate_data = BashOperator(
    task_id='generate_new_leads',
    bash_command='python /opt/spark/scripts/generate_data.py --date {{ ds }}',
    dag=dag,
)

train_model = SparkSubmitOperator(
    task_id='train_lead_scoring_model',
    application='/opt/spark/jobs/lead_scoring.py',
    conn_id='spark_default',
    conf={
        'spark.executor.memory': '4g',
        'spark.executor.cores': '2',
    },
    application_args=['--date', '{{ ds }}'],
    dag=dag,
)

evaluate_model = SparkSubmitOperator(
    task_id='evaluate_model',
    application='/opt/spark/jobs/evaluate_model.py',
    conn_id='spark_default',
    application_args=['--model-path', '/models/{{ ds }}'],
    dag=dag,
)

def check_model_quality(**context):
    """Valida métricas del modelo antes de deployment"""
    import json

    metrics_path = f"/models/{context['ds']}/metrics.json"
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)

    auc = metrics.get('auc', 0)

    if auc < 0.75:
        raise ValueError(f"Model AUC {auc} is below threshold 0.75")

    print(f"✅ Model quality OK: AUC = {auc}")
    return True

validate_metrics = PythonOperator(
    task_id='validate_model_metrics',
    python_callable=check_model_quality,
    provide_context=True,
    dag=dag,
)

deploy_model = BashOperator(
    task_id='deploy_to_production',
    bash_command="""
    cp /models/{{ ds }}/model /production/models/lead_scoring_latest
    aws s3 cp /models/{{ ds }}/model s3://ml-models/lead_scoring/{{ ds }}/
    """,
    dag=dag,
)

generate_predictions = SparkSubmitOperator(
    task_id='generate_batch_predictions',
    application='/opt/spark/jobs/batch_scoring.py',
    conn_id='spark_default',
    application_args=[
        '--model-path', '/production/models/lead_scoring_latest',
        '--output-path', 's3a://datalake/gold/predictions/{{ ds }}/',
    ],
    dag=dag,
)

notify_success = EmailOperator(
    task_id='notify_success',
    to='ml-team@company.com',
    subject='✅ MLOps Pipeline Success - {{ ds }}',
    html_content="""
    <h3>Pipeline ejecutado exitosamente</h3>
    <p>Fecha: {{ ds }}</p>
    <p>DAG: {{ dag.dag_id }}</p>
    <p>Run ID: {{ run_id }}</p>
    """,
    dag=dag,
)

start >> generate_data >> train_model >> evaluate_model >> validate_metrics
validate_metrics >> deploy_model >> generate_predictions >> notify_success
```

---

## 🎯 Patrones de Diseño de DAGs

### 1. ETL Pattern (Extract, Transform, Load)

```python
extract_api >> extract_db >> transform_spark >> load_warehouse >> notify
```

### 2. Branching (Conditional Execution)

```python
from airflow.operators.python import BranchPythonOperator

def decide_branch(**context):
    """Decide qué rama ejecutar basado en condiciones"""
    execution_date = context['execution_date']

    if execution_date.day == 1:
        return 'monthly_report'
    else:
        return 'daily_report'

branching = BranchPythonOperator(
    task_id='decide_branch',
    python_callable=decide_branch,
    dag=dag,
)

daily_report = BashOperator(task_id='daily_report', ...)
monthly_report = BashOperator(task_id='monthly_report', ...)

branching >> [daily_report, monthly_report]
```

### 3. Dynamic Task Generation

```python
from airflow.models import Variable

countries = Variable.get("countries", deserialize_json=True)

start = BashOperator(task_id='start', ...)

for country in countries:
    task = SparkSubmitOperator(
        task_id=f'process_{country}',
        application=f'/opt/spark/jobs/process_country.py',
        application_args=['--country', country],
        dag=dag,
    )
    start >> task
```

### 4. SubDAGs (Modularización)

```python
from airflow.operators.subdag import SubDagOperator

def create_subdag(parent_dag_id, child_dag_id, args):
    subdag = DAG(
        dag_id=f'{parent_dag_id}.{child_dag_id}',
        default_args=args,
        schedule_interval='@daily',
    )

    task1 = BashOperator(task_id='task1', bash_command='echo 1', dag=subdag)
    task2 = BashOperator(task_id='task2', bash_command='echo 2', dag=subdag)
    task1 >> task2

    return subdag

data_quality_checks = SubDagOperator(
    task_id='data_quality_subdag',
    subdag=create_subdag('main_dag', 'data_quality_subdag', default_args),
    dag=dag,
)
```

### 5. Sensor Pattern (Esperar Recursos)

```python
from airflow.sensors.filesystem import FileSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

wait_for_file = S3KeySensor(
    task_id='wait_for_data',
    bucket_name='datalake',
    bucket_key='raw/data_{{ ds }}.csv',
    aws_conn_id='aws_default',
    timeout=3600,  # 1 hora máximo
    poke_interval=60,  # Chequear cada minuto
    dag=dag,
)

wait_for_file >> process_data
```

---

## 🔄 Variables y Templating (Jinja)

Airflow usa **Jinja templating** para valores dinámicos.

### Variables Built-in

```python
# Fecha de ejecución (ISO format)
{{ ds }}  # 2024-01-15

# Fecha de ejecución (datetime object)
{{ execution_date }}

# Yesterday
{{ yesterday_ds }}

# DAG info
{{ dag.dag_id }}
{{ run_id }}

# Custom date formatting
{{ execution_date.strftime('%Y/%m/%d') }}

# Macros
{{ macros.ds_add(ds, 7) }}  # Agregar 7 días
```

### Custom Variables

```python
from airflow.models import Variable

# Definir en UI o CLI
Variable.set("s3_bucket", "my-datalake")

# Usar en DAG
bucket = Variable.get("s3_bucket")

# O en template
{{ var.value.s3_bucket }}
```

### XCom (Cross-Communication)

Compartir datos entre tareas:

```python
def extract_data(**context):
    """Extrae datos y comparte resultado"""
    data_count = 1000
    context['task_instance'].xcom_push(key='data_count', value=data_count)

def process_data(**context):
    """Lee resultado de tarea anterior"""
    ti = context['task_instance']
    data_count = ti.xcom_pull(key='data_count', task_ids='extract_data')
    print(f"Processing {data_count} records")

extract = PythonOperator(task_id='extract_data', python_callable=extract_data)
process = PythonOperator(task_id='process_data', python_callable=process_data)

extract >> process
```

---

## 🛠️ Instalación y Configuración

### Opción 1: Docker Compose (Recomendado)

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data

  airflow-init:
    image: apache/airflow:2.8.0
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    command: >
      bash -c "airflow db init &&
               airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com"
    depends_on:
      - postgres

  airflow-webserver:
    image: apache/airflow:2.8.0
    command: webserver
    ports:
      - "8080:8080"
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
    depends_on:
      - postgres
      - airflow-init

  airflow-scheduler:
    image: apache/airflow:2.8.0
    command: scheduler
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
    depends_on:
      - postgres
      - airflow-init

volumes:
  postgres-db-volume:
```

```bash
# Iniciar Airflow
docker-compose up -d

# Acceder a UI
open http://localhost:8080
# User: admin / Password: admin
```

### Opción 2: Instalación Local (Desarrollo)

```bash
# Instalar Airflow
pip install apache-airflow==2.8.0

# Inicializar DB (SQLite por defecto)
airflow db init

# Crear usuario admin
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Iniciar webserver
airflow webserver --port 8080

# Iniciar scheduler (en otra terminal)
airflow scheduler
```

### Estructura de Directorios

```
airflow/
├── dags/
│   ├── spark_ml_dag.py
│   ├── etl_pipeline.py
│   └── data_quality_dag.py
├── logs/
│   └── dag_id/
│       └── task_id/
│           └── execution_date/
├── plugins/
│   └── custom_operators/
├── airflow.cfg
└── airflow.db
```

---

## 📊 Monitoreo y Alertas

### Estados de Tareas

| Estado | Significado |
|--------|-------------|
| `success` | Completada exitosamente |
| `running` | En ejecución |
| `failed` | Falló (después de retries) |
| `upstream_failed` | Fallo en tarea dependiente |
| `skipped` | Omitida por branching |
| `up_for_retry` | Esperando retry |
| `queued` | En cola para ejecutar |

### SLAs (Service Level Agreements)

```python
from datetime import timedelta

task = SparkSubmitOperator(
    task_id='critical_task',
    application='job.py',
    sla=timedelta(hours=2),  # Alerta si toma > 2 horas
    dag=dag,
)

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Callback cuando se rompe SLA"""
    print(f"SLA miss! Tasks: {task_list}")
    # Enviar alerta a Slack, PagerDuty, etc.

dag.sla_miss_callback = sla_miss_callback
```

### Callbacks de Fallos

```python
def on_failure_callback(context):
    """Se ejecuta cuando una tarea falla"""
    task = context['task_instance']
    exception = context.get('exception')

    message = f"""
    Task Failed: {task.task_id}
    DAG: {task.dag_id}
    Execution Date: {context['execution_date']}
    Error: {exception}
    """
    # Enviar a Slack, email, etc.
    print(message)

task = SparkSubmitOperator(
    task_id='my_task',
    application='job.py',
    on_failure_callback=on_failure_callback,
    dag=dag,
)
```

### Integración con Prometheus

```python
from airflow.providers.prometheus.operators.prometheus import PrometheusOperator

push_metrics = PrometheusOperator(
    task_id='push_metrics_to_prometheus',
    url='http://pushgateway:9091',
    metrics={
        'pipeline_duration': '{{ ti.duration }}',
        'records_processed': '{{ ti.xcom_pull("process_data", key="count") }}',
    },
    dag=dag,
)
```

---

## 💡 Mejores Prácticas

### 1. DAG Design

**✅ DO:**
- Mantener DAGs simples y enfocados (single responsibility)
- Usar nombres descriptivos para task_id y dag_id
- Documentar con `doc_md` o docstrings
- Versionarlos en Git

**❌ DON'T:**
- No hacer DAGs demasiado largos (>30 tareas)
- No usar imports dinámicos en el scope global
- No acceder a bases de datos en el código del DAG (solo en tasks)

```python
# ✅ BIEN
with DAG('etl_pipeline', ...) as dag:
    extract = BashOperator(task_id='extract', ...)
    transform = SparkSubmitOperator(task_id='transform', ...)
    extract >> transform

# ❌ MAL
for i in range(100):  # Demasiadas tareas
    task = BashOperator(task_id=f'task_{i}', ...)
```

### 2. Idempotencia

Cada tarea debe ser **idempotente**: ejecutarla múltiples veces con los mismos parámetros produce el mismo resultado.

```python
# ✅ Idempotente
df.write.mode("overwrite").partitionBy("date").parquet(f"s3://data/{date}/")

# ❌ No idempotente
df.write.mode("append").parquet("s3://data/")  # Duplica datos en re-run
```

### 3. Configuración Externalizada

```python
# ❌ Hardcoded
s3_bucket = "my-production-bucket"

# ✅ Variables de Airflow
from airflow.models import Variable
s3_bucket = Variable.get("s3_bucket")

# ✅ Templating
application_args=['--bucket', '{{ var.value.s3_bucket }}']
```

### 4. Manejo de Errores

```python
task = SparkSubmitOperator(
    task_id='spark_job',
    application='job.py',
    retries=3,  # Reintentar 3 veces
    retry_delay=timedelta(minutes=5),  # Esperar 5 min entre retries
    retry_exponential_backoff=True,  # Backoff exponencial
    max_retry_delay=timedelta(hours=1),  # Max 1 hora de backoff
    execution_timeout=timedelta(hours=2),  # Timeout total
    on_failure_callback=alert_team,
    dag=dag,
)
```

### 5. Testing DAGs

```python
import pytest
from airflow.models import DagBag

def test_dag_loading():
    """Verifica que el DAG se carga sin errores"""
    dagbag = DagBag(dag_folder='dags/', include_examples=False)
    assert len(dagbag.import_errors) == 0

def test_dag_structure():
    """Verifica estructura del DAG"""
    from dags.spark_ml_dag import dag

    assert len(dag.tasks) == 5
    assert 'train_model' in [t.task_id for t in dag.tasks]
```

### 6. Seguridad

```bash
# Usar Connections para credenciales (NO hardcodear)
# Admin → Connections en UI

# O CLI
airflow connections add 'spark_default' \
    --conn-type 'spark' \
    --conn-host 'spark://spark-master' \
    --conn-port '7077'

# Encriptar metadata DB (airflow.cfg)
fernet_key = $(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

---

## 🔍 Comparación con Otras Herramientas

| Feature | Airflow | Prefect | Dagster | Luigi |
|---------|---------|---------|---------|-------|
| **Lenguaje** | Python | Python | Python | Python |
| **UI** | ✅ Web UI | ✅ Cloud/Self-hosted | ✅ Dagit | ⚠️ Básico |
| **Scheduling** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **DAG-based** | ✅ | ✅ | ✅ | ✅ |
| **Distributed** | ✅ Celery/K8s | ✅ Cloud | ✅ | ⚠️ Limitado |
| **Retries** | ✅ | ✅ | ✅ | ✅ |
| **Monitoreo** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Comunidad** | 🔥 Enorme | 📈 Creciente | 📈 Creciente | 📉 Decreciente |
| **Madurez** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Curva aprendizaje** | Media | Baja | Media-Alta | Baja |

**Cuándo usar Airflow:**
- ✅ Necesitas scheduling robusto (cron-like)
- ✅ Múltiples equipos/DAGs complejos
- ✅ Integración con 100+ servicios (AWS, GCP, Spark, etc.)
- ✅ Requisito de open-source self-hosted

**Alternativas:**
- **Prefect**: UI más moderna, mejor para workflows dinámicos
- **Dagster**: Mejor para software-defined assets y data quality
- **Luigi**: Más simple, pero menos features

---

## 🚀 Inicio Rápido

### 1. Levantar Infraestructura

```bash
# Desde la raíz del taller
cd spark/
docker-compose up -d postgres airflow-webserver airflow-scheduler

# Verificar servicios
docker ps | grep airflow
```

### 2. Acceder a UI

```bash
open http://localhost:8080
# Usuario: admin
# Password: admin
```

### 3. Activar DAG de Ejemplo

1. En la UI, buscar el DAG `spark_mlops_pipeline`
2. Toggle el switch para activarlo
3. Click en "Trigger DAG" para ejecutar manualmente
4. Monitorear en "Graph View" o "Tree View"

### 4. Ver Logs

```bash
# Desde UI: Click en task → View Log

# O desde CLI
airflow tasks logs spark_mlops_pipeline train_model 2024-01-15
```

---

## 📚 Referencias

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Astronomer Guides](https://www.astronomer.io/guides/)
- [Awesome Apache Airflow](https://github.com/jghoman/awesome-apache-airflow)

---

**¡Siguiente paso! 👉 [Módulo 07: Docker + Kubernetes](../07-Docker-K8s/README.md) para desplegar Spark en producción**
