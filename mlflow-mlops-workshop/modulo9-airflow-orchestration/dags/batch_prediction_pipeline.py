"""
DAG: Batch Prediction Pipeline
Descripción: Pipeline para hacer predicciones en batch usando modelo productivo de MLflow
Autor: MLOps Workshop
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import pickle
import json

MLFLOW_TRACKING_URI = "http://localhost:5000"
MODEL_NAME = "airflow_best_classifier"

default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'batch_prediction_pipeline',
    default_args=default_args,
    description='Pipeline de predicciones en batch con modelo productivo',
    schedule_interval='0 */6 * * *',
    catchup=False,
    tags=['ml', 'mlflow', 'prediction', 'batch'],
)


def check_production_model_exists(**context):
    """
    Verificar si existe un modelo en producción
    """
    print("Verificando modelo en producción...")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient()

    try:
        model_versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])

        if model_versions:
            model_version = model_versions[0]
            print(f"Modelo en producción encontrado:")
            print(f"  Nombre: {MODEL_NAME}")
            print(f"  Versión: {model_version.version}")
            print(f"  Run ID: {model_version.run_id}")

            context['ti'].xcom_push(key='model_version', value=model_version.version)
            context['ti'].xcom_push(key='model_uri', value=f"models:/{MODEL_NAME}/Production")

            return 'load_production_model'
        else:
            print("No hay modelo en producción. Intentando usar Staging...")

            staging_versions = client.get_latest_versions(MODEL_NAME, stages=["Staging"])
            if staging_versions:
                model_version = staging_versions[0]
                print(f"Usando modelo de Staging:")
                print(f"  Versión: {model_version.version}")

                context['ti'].xcom_push(key='model_version', value=model_version.version)
                context['ti'].xcom_push(key='model_uri', value=f"models:/{MODEL_NAME}/Staging")

                return 'load_production_model'
            else:
                print("No hay modelos disponibles")
                return 'no_model_available'

    except Exception as e:
        print(f"Error verificando modelo: {e}")
        return 'no_model_available'


def load_production_model(**context):
    """
    Cargar modelo de producción desde MLflow
    """
    print("Cargando modelo de producción...")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = context['ti'].xcom_pull(task_ids='check_model', key='model_uri')
    model_version = context['ti'].xcom_pull(task_ids='check_model', key='model_version')

    try:
        model = mlflow.sklearn.load_model(model_uri)

        print(f"Modelo cargado exitosamente:")
        print(f"  URI: {model_uri}")
        print(f"  Versión: {model_version}")
        print(f"  Tipo: {type(model).__name__}")

        model_path = '/tmp/production_model.pkl'
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        context['ti'].xcom_push(key='model_path', value=model_path)

        return model_path

    except Exception as e:
        print(f"Error cargando modelo: {e}")
        raise


def generate_batch_data(**context):
    """
    Generar datos para predicción en batch
    En producción, esto vendría de una DB, S3, etc.
    """
    print("Generando datos para predicción...")

    X, _ = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=2,
        random_state=int(datetime.now().timestamp())
    )

    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])

    df['batch_id'] = context['ds']
    df['timestamp'] = datetime.now().isoformat()

    batch_data_path = '/tmp/batch_data.csv'
    df.to_csv(batch_data_path, index=False)

    context['ti'].xcom_push(key='batch_data_path', value=batch_data_path)
    context['ti'].xcom_push(key='n_records', value=len(df))

    print(f"Datos generados: {len(df)} registros")

    return batch_data_path


def make_predictions(**context):
    """
    Hacer predicciones con el modelo de producción
    """
    print("Haciendo predicciones...")

    model_path = context['ti'].xcom_pull(task_ids='load_production_model', key='model_path')
    batch_data_path = context['ti'].xcom_pull(task_ids='generate_batch_data', key='batch_data_path')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    df = pd.read_csv(batch_data_path)

    feature_cols = [col for col in df.columns if col.startswith('feature_')]
    X = df[feature_cols]

    predictions = model.predict(X)
    prediction_probas = model.predict_proba(X)

    df['prediction'] = predictions
    df['probability_class_0'] = prediction_probas[:, 0]
    df['probability_class_1'] = prediction_probas[:, 1]
    df['confidence'] = prediction_probas.max(axis=1)

    predictions_path = '/tmp/batch_predictions.csv'
    df.to_csv(predictions_path, index=False)

    class_distribution = pd.Series(predictions).value_counts(normalize=True)
    avg_confidence = df['confidence'].mean()

    context['ti'].xcom_push(key='predictions_path', value=predictions_path)
    context['ti'].xcom_push(key='avg_confidence', value=avg_confidence)

    print(f"Predicciones completadas:")
    print(f"  Total: {len(predictions)}")
    print(f"  Clase 0: {(predictions == 0).sum()} ({class_distribution.get(0, 0)*100:.1f}%)")
    print(f"  Clase 1: {(predictions == 1).sum()} ({class_distribution.get(1, 0)*100:.1f}%)")
    print(f"  Confianza promedio: {avg_confidence:.4f}")

    return predictions_path


def log_predictions_to_mlflow(**context):
    """
    Registrar métricas de predicciones en MLflow
    """
    print("Registrando predicciones en MLflow...")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("batch-predictions")

    n_records = context['ti'].xcom_pull(task_ids='generate_batch_data', key='n_records')
    avg_confidence = context['ti'].xcom_pull(task_ids='make_predictions', key='avg_confidence')
    model_version = context['ti'].xcom_pull(task_ids='check_model', key='model_version')
    predictions_path = context['ti'].xcom_pull(task_ids='make_predictions', key='predictions_path')

    with mlflow.start_run(run_name=f"batch_predictions_{context['ds']}"):

        mlflow.log_param("batch_date", context['ds'])
        mlflow.log_param("model_name", MODEL_NAME)
        mlflow.log_param("model_version", model_version)

        mlflow.log_metric("n_predictions", n_records)
        mlflow.log_metric("avg_confidence", avg_confidence)

        df_predictions = pd.read_csv(predictions_path)
        class_0_count = (df_predictions['prediction'] == 0).sum()
        class_1_count = (df_predictions['prediction'] == 1).sum()

        mlflow.log_metric("class_0_count", class_0_count)
        mlflow.log_metric("class_1_count", class_1_count)
        mlflow.log_metric("class_balance", class_1_count / n_records)

        mlflow.log_artifact(predictions_path)

        mlflow.set_tag("pipeline", "batch_prediction")
        mlflow.set_tag("status", "success")

        run_id = mlflow.active_run().info.run_id

        print(f"Predicciones registradas en MLflow (Run ID: {run_id})")

        return run_id


def check_prediction_quality(**context):
    """
    Verificar calidad de predicciones y decidir si se necesita reentrenamiento
    """
    print("Verificando calidad de predicciones...")

    avg_confidence = context['ti'].xcom_pull(task_ids='make_predictions', key='avg_confidence')

    MIN_CONFIDENCE_THRESHOLD = 0.75

    if avg_confidence < MIN_CONFIDENCE_THRESHOLD:
        print(f"¡ALERTA! Confianza baja: {avg_confidence:.4f} < {MIN_CONFIDENCE_THRESHOLD}")
        print("Se recomienda reentrenar el modelo")

        context['ti'].xcom_push(key='needs_retraining', value=True)

        return 'trigger_retraining'
    else:
        print(f"Calidad de predicciones OK: {avg_confidence:.4f}")

        context['ti'].xcom_push(key='needs_retraining', value=False)

        return 'predictions_ok'


def trigger_retraining_notification(**context):
    """
    Notificar que se necesita reentrenamiento
    """
    print("Generando notificación de reentrenamiento...")

    avg_confidence = context['ti'].xcom_pull(task_ids='make_predictions', key='avg_confidence')

    message = f"""
    ⚠️ ALERTA: Se requiere reentrenamiento del modelo

    Fecha: {context['ds']}
    Modelo: {MODEL_NAME}
    Confianza promedio: {avg_confidence:.4f}

    Acción recomendada: Ejecutar pipeline de entrenamiento
    """

    print(message)

    notification_path = '/tmp/retraining_alert.txt'
    with open(notification_path, 'w') as f:
        f.write(message)

    return message


task_check_model = BranchPythonOperator(
    task_id='check_model',
    python_callable=check_production_model_exists,
    dag=dag,
)

task_no_model = DummyOperator(
    task_id='no_model_available',
    dag=dag,
)

task_load_model = PythonOperator(
    task_id='load_production_model',
    python_callable=load_production_model,
    dag=dag,
)

task_generate_data = PythonOperator(
    task_id='generate_batch_data',
    python_callable=generate_batch_data,
    dag=dag,
)

task_predict = PythonOperator(
    task_id='make_predictions',
    python_callable=make_predictions,
    dag=dag,
)

task_log = PythonOperator(
    task_id='log_predictions_to_mlflow',
    python_callable=log_predictions_to_mlflow,
    dag=dag,
)

task_check_quality = BranchPythonOperator(
    task_id='check_prediction_quality',
    python_callable=check_prediction_quality,
    dag=dag,
)

task_predictions_ok = DummyOperator(
    task_id='predictions_ok',
    dag=dag,
)

task_trigger_retraining = PythonOperator(
    task_id='trigger_retraining',
    python_callable=trigger_retraining_notification,
    dag=dag,
)

task_check_model >> [task_load_model, task_no_model]
task_load_model >> task_generate_data
task_generate_data >> task_predict >> task_log
task_log >> task_check_quality
task_check_quality >> [task_predictions_ok, task_trigger_retraining]
