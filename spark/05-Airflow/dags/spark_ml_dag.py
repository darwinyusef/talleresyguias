from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
import os

# Definición del DAG
default_args = {
    'owner': 'spark_expert',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'spark_mlops_pipeline',
    default_args=default_args,
    description='Pipeline completo de MLOps: ETL + ML Training + Registro',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['spark', 'mlops', 'leads'],
) as dag:

    # 1. Generación de datos (Simulando llegada de nuevos leads diarios)
    generate_data = SparkSubmitOperator(
        task_id='generate_new_leads',
        application='/opt/bitnami/spark/scripts/generate_data.py', # Ruta en el contenedor
        conn_id='spark_default',
        name='GenerateLeads'
    )

    # 2. ETL y Entrenamiento de Modelo
    train_model = SparkSubmitOperator(
        task_id='train_lead_scoring_model',
        application='/opt/bitnami/spark/02-03-ML/lead_scoring.py',
        conn_id='spark_default',
        conf={
            "spark.master": "spark://spark-master:7077",
            "spark.executor.memory": "2g"
        },
        name='TrainLeadScoring'
    )

    # 3. Publicar resultados a Postgres (Simulado como tarea final)
    # Aquí podríamos tener un sensor que verifique si el modelo mejoró en MLflow

    generate_data >> train_model
