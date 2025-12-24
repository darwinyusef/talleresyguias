"""
DAG: ML Training Pipeline with MLflow
Descripción: Pipeline completo de entrenamiento ML con tracking en MLflow
Autor: MLOps Workshop
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn
import pickle
import json
from pathlib import Path

MLFLOW_TRACKING_URI = "http://localhost:5000"
EXPERIMENT_NAME = "airflow-ml-pipeline"

default_args = {
    'owner': 'mlops-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    description='Pipeline completo de ML con MLflow tracking',
    schedule_interval='0 2 * * *',
    catchup=False,
    tags=['ml', 'mlflow', 'training'],
)


def extract_data(**context):
    """
    Tarea 1: Extracción de datos
    En producción, esto podría ser una query a DB, API, etc.
    """
    print("Extrayendo datos...")

    X, y = make_classification(
        n_samples=10000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        n_classes=2,
        random_state=42
    )

    df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    df['target'] = y

    data_path = '/tmp/raw_data.csv'
    df.to_csv(data_path, index=False)

    context['ti'].xcom_push(key='data_path', value=data_path)
    context['ti'].xcom_push(key='n_samples', value=len(df))

    print(f"Datos extraídos: {len(df)} muestras, {X.shape[1]} features")
    return data_path


def preprocess_data(**context):
    """
    Tarea 2: Preprocesamiento y feature engineering
    """
    print("Preprocesando datos...")

    data_path = context['ti'].xcom_pull(task_ids='extract_data', key='data_path')
    df = pd.read_csv(data_path)

    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    train_data = {
        'X_train': X_train.values.tolist(),
        'y_train': y_train.values.tolist(),
        'X_test': X_test.values.tolist(),
        'y_test': y_test.values.tolist(),
        'feature_names': X.columns.tolist()
    }

    train_path = '/tmp/train_data.pkl'
    with open(train_path, 'wb') as f:
        pickle.dump(train_data, f)

    context['ti'].xcom_push(key='train_path', value=train_path)
    context['ti'].xcom_push(key='train_size', value=len(X_train))
    context['ti'].xcom_push(key='test_size', value=len(X_test))

    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    return train_path


def train_model_rf(**context):
    """
    Tarea 3a: Entrenar Random Forest con MLflow tracking
    """
    print("Entrenando Random Forest...")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    train_path = context['ti'].xcom_pull(task_ids='preprocess_data', key='train_path')
    with open(train_path, 'rb') as f:
        train_data = pickle.load(f)

    X_train = np.array(train_data['X_train'])
    y_train = np.array(train_data['y_train'])
    X_test = np.array(train_data['X_test'])
    y_test = np.array(train_data['y_test'])

    with mlflow.start_run(run_name=f"random_forest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):

        params = {
            'n_estimators': 100,
            'max_depth': 10,
            'min_samples_split': 5,
            'random_state': 42
        }
        mlflow.log_params(params)

        mlflow.set_tag("model_type", "RandomForest")
        mlflow.set_tag("pipeline", "airflow_automated")
        mlflow.set_tag("execution_date", context['ds'])

        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(model, "random_forest_model")

        run_id = mlflow.active_run().info.run_id

        context['ti'].xcom_push(key='rf_run_id', value=run_id)
        context['ti'].xcom_push(key='rf_accuracy', value=accuracy)
        context['ti'].xcom_push(key='rf_f1', value=f1)

        print(f"Random Forest - Accuracy: {accuracy:.4f}, F1: {f1:.4f}, Run ID: {run_id}")

        return {'run_id': run_id, 'accuracy': accuracy, 'f1': f1}


def train_model_gb(**context):
    """
    Tarea 3b: Entrenar Gradient Boosting con MLflow tracking
    """
    print("Entrenando Gradient Boosting...")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    train_path = context['ti'].xcom_pull(task_ids='preprocess_data', key='train_path')
    with open(train_path, 'rb') as f:
        train_data = pickle.load(f)

    X_train = np.array(train_data['X_train'])
    y_train = np.array(train_data['y_train'])
    X_test = np.array(train_data['X_test'])
    y_test = np.array(train_data['y_test'])

    with mlflow.start_run(run_name=f"gradient_boosting_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):

        params = {
            'n_estimators': 100,
            'learning_rate': 0.1,
            'max_depth': 5,
            'random_state': 42
        }
        mlflow.log_params(params)

        mlflow.set_tag("model_type", "GradientBoosting")
        mlflow.set_tag("pipeline", "airflow_automated")
        mlflow.set_tag("execution_date", context['ds'])

        model = GradientBoostingClassifier(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(model, "gradient_boosting_model")

        run_id = mlflow.active_run().info.run_id

        context['ti'].xcom_push(key='gb_run_id', value=run_id)
        context['ti'].xcom_push(key='gb_accuracy', value=accuracy)
        context['ti'].xcom_push(key='gb_f1', value=f1)

        print(f"Gradient Boosting - Accuracy: {accuracy:.4f}, F1: {f1:.4f}, Run ID: {run_id}")

        return {'run_id': run_id, 'accuracy': accuracy, 'f1': f1}


def train_model_lr(**context):
    """
    Tarea 3c: Entrenar Logistic Regression con MLflow tracking
    """
    print("Entrenando Logistic Regression...")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    train_path = context['ti'].xcom_pull(task_ids='preprocess_data', key='train_path')
    with open(train_path, 'rb') as f:
        train_data = pickle.load(f)

    X_train = np.array(train_data['X_train'])
    y_train = np.array(train_data['y_train'])
    X_test = np.array(train_data['X_test'])
    y_test = np.array(train_data['y_test'])

    with mlflow.start_run(run_name=f"logistic_regression_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):

        params = {
            'max_iter': 1000,
            'random_state': 42,
            'solver': 'lbfgs'
        }
        mlflow.log_params(params)

        mlflow.set_tag("model_type", "LogisticRegression")
        mlflow.set_tag("pipeline", "airflow_automated")
        mlflow.set_tag("execution_date", context['ds'])

        model = LogisticRegression(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(model, "logistic_regression_model")

        run_id = mlflow.active_run().info.run_id

        context['ti'].xcom_push(key='lr_run_id', value=run_id)
        context['ti'].xcom_push(key='lr_accuracy', value=accuracy)
        context['ti'].xcom_push(key='lr_f1', value=f1)

        print(f"Logistic Regression - Accuracy: {accuracy:.4f}, F1: {f1:.4f}, Run ID: {run_id}")

        return {'run_id': run_id, 'accuracy': accuracy, 'f1': f1}


def compare_models(**context):
    """
    Tarea 4: Comparar modelos y seleccionar el mejor
    """
    print("Comparando modelos...")

    rf_accuracy = context['ti'].xcom_pull(task_ids='train_random_forest', key='rf_accuracy')
    gb_accuracy = context['ti'].xcom_pull(task_ids='train_gradient_boosting', key='gb_accuracy')
    lr_accuracy = context['ti'].xcom_pull(task_ids='train_logistic_regression', key='lr_accuracy')

    rf_run_id = context['ti'].xcom_pull(task_ids='train_random_forest', key='rf_run_id')
    gb_run_id = context['ti'].xcom_pull(task_ids='train_gradient_boosting', key='gb_run_id')
    lr_run_id = context['ti'].xcom_pull(task_ids='train_logistic_regression', key='lr_run_id')

    models = [
        {'name': 'RandomForest', 'accuracy': rf_accuracy, 'run_id': rf_run_id},
        {'name': 'GradientBoosting', 'accuracy': gb_accuracy, 'run_id': gb_run_id},
        {'name': 'LogisticRegression', 'accuracy': lr_accuracy, 'run_id': lr_run_id}
    ]

    best_model = max(models, key=lambda x: x['accuracy'])

    print(f"\\nComparación de Modelos:")
    for model in sorted(models, key=lambda x: x['accuracy'], reverse=True):
        print(f"  {model['name']}: {model['accuracy']:.4f}")

    print(f"\\nMejor modelo: {best_model['name']} con accuracy {best_model['accuracy']:.4f}")

    context['ti'].xcom_push(key='best_model_name', value=best_model['name'])
    context['ti'].xcom_push(key='best_model_run_id', value=best_model['run_id'])
    context['ti'].xcom_push(key='best_model_accuracy', value=best_model['accuracy'])

    comparison_path = '/tmp/model_comparison.json'
    with open(comparison_path, 'w') as f:
        json.dump(models, f, indent=2)

    return best_model


def register_best_model(**context):
    """
    Tarea 5: Registrar el mejor modelo en MLflow Model Registry
    """
    print("Registrando mejor modelo...")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    best_model_name = context['ti'].xcom_pull(task_ids='compare_models', key='best_model_name')
    best_run_id = context['ti'].xcom_pull(task_ids='compare_models', key='best_model_run_id')
    best_accuracy = context['ti'].xcom_pull(task_ids='compare_models', key='best_model_accuracy')

    model_uri = f"runs:/{best_run_id}/{best_model_name.lower()}_model"
    registered_model_name = "airflow_best_classifier"

    try:
        model_details = mlflow.register_model(model_uri, registered_model_name)

        print(f"Modelo registrado:")
        print(f"  Nombre: {registered_model_name}")
        print(f"  Versión: {model_details.version}")
        print(f"  Run ID: {best_run_id}")
        print(f"  Accuracy: {best_accuracy:.4f}")

        if best_accuracy >= 0.80:
            from mlflow.tracking import MlflowClient
            client = MlflowClient()
            client.transition_model_version_stage(
                name=registered_model_name,
                version=model_details.version,
                stage="Staging"
            )
            print(f"Modelo promovido a Staging (accuracy >= 0.80)")
        else:
            print(f"Modelo no promovido (accuracy < 0.80)")

        context['ti'].xcom_push(key='registered_version', value=model_details.version)

        return {
            'model_name': registered_model_name,
            'version': model_details.version,
            'accuracy': best_accuracy
        }

    except Exception as e:
        print(f"Error registrando modelo: {e}")
        raise


def send_notification(**context):
    """
    Tarea 6: Enviar notificación de completado
    """
    print("Enviando notificación...")

    best_model_name = context['ti'].xcom_pull(task_ids='compare_models', key='best_model_name')
    best_accuracy = context['ti'].xcom_pull(task_ids='compare_models', key='best_model_accuracy')
    registered_version = context['ti'].xcom_pull(task_ids='register_best_model', key='registered_version')

    message = f"""
    Pipeline ML Completado con Éxito

    Fecha: {context['ds']}
    Mejor Modelo: {best_model_name}
    Accuracy: {best_accuracy:.4f}
    Versión Registrada: {registered_version}

    Revisa MLflow UI: {MLFLOW_TRACKING_URI}
    """

    print(message)

    notification_path = '/tmp/pipeline_notification.txt'
    with open(notification_path, 'w') as f:
        f.write(message)

    return message


task_extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

task_preprocess = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

task_train_rf = PythonOperator(
    task_id='train_random_forest',
    python_callable=train_model_rf,
    dag=dag,
)

task_train_gb = PythonOperator(
    task_id='train_gradient_boosting',
    python_callable=train_model_gb,
    dag=dag,
)

task_train_lr = PythonOperator(
    task_id='train_logistic_regression',
    python_callable=train_model_lr,
    dag=dag,
)

task_compare = PythonOperator(
    task_id='compare_models',
    python_callable=compare_models,
    dag=dag,
)

task_register = PythonOperator(
    task_id='register_best_model',
    python_callable=register_best_model,
    dag=dag,
)

task_notify = PythonOperator(
    task_id='send_notification',
    python_callable=send_notification,
    dag=dag,
)

task_extract >> task_preprocess
task_preprocess >> [task_train_rf, task_train_gb, task_train_lr]
[task_train_rf, task_train_gb, task_train_lr] >> task_compare
task_compare >> task_register >> task_notify
