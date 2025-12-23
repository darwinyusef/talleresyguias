"""
Cliente de ejemplo para Celery + Spark Tasks

Este script demuestra cómo enviar y monitorear tasks Celery que ejecutan Spark jobs.

Ejecutar:
    python celery_client_example.py
"""

from celery.result import AsyncResult
from celery_spark_tasks import (
    celery_app,
    etl_pipeline_task,
    train_model_task,
    batch_inference_task,
    data_quality_check_task,
    aggregate_metrics_task
)
import time
import json

def print_task_status(task_id, task_name):
    """
    Imprimir estado actual de una task
    """
    task = AsyncResult(task_id, app=celery_app)

    status_emoji = {
        'PENDING': '⏳',
        'PROGRESS': '🔄',
        'SUCCESS': '✅',
        'FAILURE': '❌',
        'RETRY': '🔁'
    }

    emoji = status_emoji.get(task.state, '❓')

    print(f"{emoji} {task_name} [{task_id[:8]}...]: {task.state}", end='')

    if task.state == 'PROGRESS' and task.info:
        stage = task.info.get('stage', '')
        print(f" - {stage}")
    elif task.state == 'SUCCESS':
        print(f" ✓")
    elif task.state == 'FAILURE':
        print(f" - Error: {task.info}")
    else:
        print()

def wait_for_task(task, task_name, check_interval=2):
    """
    Esperar a que una task complete y mostrar progreso
    """
    print(f"\n{'='*70}")
    print(f"Monitoring task: {task_name}")
    print(f"Task ID: {task.id}")
    print(f"{'='*70}")

    while not task.ready():
        print_task_status(task.id, task_name)
        time.sleep(check_interval)

    print_task_status(task.id, task_name)

    if task.successful():
        print(f"\n📊 Result:")
        result = task.result
        print(json.dumps(result, indent=2, default=str))
        return result
    else:
        print(f"\n❌ Task failed: {task.info}")
        return None

def example_1_etl_pipeline():
    """
    Ejemplo 1: ETL Pipeline
    """
    print("\n" + "🔹"*35)
    print("EJEMPLO 1: ETL PIPELINE")
    print("🔹"*35)

    task = etl_pipeline_task.delay(
        input_path="data/leads.parquet",
        output_path="data/etl_output.parquet",
        filters={'country': 'US'}
    )

    result = wait_for_task(task, "ETL Pipeline")

    return result

def example_2_train_model():
    """
    Ejemplo 2: Entrenar modelo ML
    """
    print("\n" + "🔹"*35)
    print("EJEMPLO 2: TRAIN MODEL")
    print("🔹"*35)

    task = train_model_task.delay(
        input_path="data/leads.parquet",
        model_output_path="/models/rf_model_celery",
        model_type="random_forest"
    )

    result = wait_for_task(task, "Model Training")

    return result

def example_3_batch_inference():
    """
    Ejemplo 3: Inferencia batch
    """
    print("\n" + "🔹"*35)
    print("EJEMPLO 3: BATCH INFERENCE")
    print("🔹"*35)

    task = batch_inference_task.delay(
        model_path="/models/rf_model_celery",
        input_path="data/new_leads.parquet",
        output_path="data/predictions.parquet"
    )

    result = wait_for_task(task, "Batch Inference")

    return result

def example_4_data_quality():
    """
    Ejemplo 4: Data quality check
    """
    print("\n" + "🔹"*35)
    print("EJEMPLO 4: DATA QUALITY CHECK")
    print("🔹"*35)

    task = data_quality_check_task.delay(
        input_path="data/leads.parquet"
    )

    result = wait_for_task(task, "Data Quality Check")

    return result

def example_5_parallel_tasks():
    """
    Ejemplo 5: Ejecutar múltiples tasks en paralelo
    """
    print("\n" + "🔹"*35)
    print("EJEMPLO 5: PARALLEL TASKS")
    print("🔹"*35)

    print("\n🚀 Launching 3 tasks in parallel...")

    task1 = etl_pipeline_task.delay(
        input_path="data/leads.parquet",
        output_path="data/etl_output_1.parquet",
        filters={'country': 'US'}
    )

    task2 = etl_pipeline_task.delay(
        input_path="data/leads.parquet",
        output_path="data/etl_output_2.parquet",
        filters={'country': 'UK'}
    )

    task3 = aggregate_metrics_task.delay(
        input_path="data/leads.parquet",
        metrics_output_path="data/metrics.parquet",
        group_by_cols=['country', 'age_group']
    )

    tasks = [
        (task1, "ETL Pipeline (US)"),
        (task2, "ETL Pipeline (UK)"),
        (task3, "Aggregate Metrics")
    ]

    print(f"\nMonitoring {len(tasks)} tasks...\n")

    all_done = False
    while not all_done:
        for task, name in tasks:
            print_task_status(task.id, name)

        all_done = all(t[0].ready() for t in tasks)

        if not all_done:
            print("\n" + "-"*70)
            time.sleep(2)

    print("\n✅ All tasks completed!")

    for task, name in tasks:
        if task.successful():
            print(f"\n📊 {name} Result:")
            print(json.dumps(task.result, indent=2, default=str))

def example_6_task_chain():
    """
    Ejemplo 6: Chain de tasks (una después de otra)
    """
    print("\n" + "🔹"*35)
    print("EJEMPLO 6: TASK CHAIN")
    print("🔹"*35)

    from celery import chain

    pipeline = chain(
        etl_pipeline_task.si(
            input_path="data/leads.parquet",
            output_path="data/cleaned.parquet"
        ),
        train_model_task.si(
            input_path="data/cleaned.parquet",
            model_output_path="/models/chain_model",
            model_type="gbt"
        ),
        batch_inference_task.si(
            model_path="/models/chain_model",
            input_path="data/new_leads.parquet",
            output_path="data/chain_predictions.parquet"
        )
    )

    print("\n🔗 Executing task chain:")
    print("   1. ETL Pipeline")
    print("   2. Train Model")
    print("   3. Batch Inference\n")

    result = pipeline.apply_async()

    print(f"Chain ID: {result.id}")
    print(f"Waiting for chain to complete...\n")

    while not result.ready():
        print(".", end='', flush=True)
        time.sleep(1)

    print("\n\n✅ Chain completed!")

    if result.successful():
        print(f"\n📊 Final Result:")
        print(json.dumps(result.result, indent=2, default=str))

def list_active_tasks():
    """
    Listar todas las tasks activas
    """
    print("\n" + "🔹"*35)
    print("ACTIVE TASKS")
    print("🔹"*35)

    inspect = celery_app.control.inspect()

    active = inspect.active()
    scheduled = inspect.scheduled()
    reserved = inspect.reserved()

    if active:
        print("\n🔄 Active tasks:")
        for worker, tasks in active.items():
            print(f"\n  Worker: {worker}")
            for task in tasks:
                print(f"    - {task['name']} [{task['id'][:8]}...]")
    else:
        print("\n✓ No active tasks")

    if scheduled:
        print("\n⏰ Scheduled tasks:")
        for worker, tasks in scheduled.items():
            print(f"\n  Worker: {worker}")
            for task in tasks:
                print(f"    - {task['request']['name']} [{task['request']['id'][:8]}...]")

    if reserved:
        print("\n📥 Reserved tasks:")
        for worker, tasks in reserved.items():
            print(f"\n  Worker: {worker}")
            for task in tasks:
                print(f"    - {task['name']} [{task['id'][:8]}...]")

def show_menu():
    """
    Mostrar menú interactivo
    """
    print("\n" + "="*70)
    print("CELERY + SPARK: CLIENT EXAMPLES")
    print("="*70)
    print("\nSelect an example:")
    print("  1. ETL Pipeline")
    print("  2. Train Model")
    print("  3. Batch Inference")
    print("  4. Data Quality Check")
    print("  5. Parallel Tasks")
    print("  6. Task Chain (Pipeline)")
    print("  7. List Active Tasks")
    print("  0. Exit")
    print()

    choice = input("Enter choice (0-7): ")
    return choice

def main():
    """
    Main interactivo
    """
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                 CELERY + SPARK CLIENT EXAMPLE                    ║
║                                                                   ║
║  Make sure you have:                                             ║
║    1. Redis running: redis-server                                ║
║    2. Celery worker: celery -A celery_spark_tasks worker         ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

    ping = celery_app.control.inspect().ping()

    if not ping:
        print("❌ No Celery workers available!")
        print("   Start worker with: celery -A celery_spark_tasks worker --loglevel=info")
        return

    print(f"✅ Connected to {len(ping)} Celery worker(s)")

    while True:
        choice = show_menu()

        if choice == '0':
            print("\nGoodbye! 👋\n")
            break
        elif choice == '1':
            example_1_etl_pipeline()
        elif choice == '2':
            example_2_train_model()
        elif choice == '3':
            example_3_batch_inference()
        elif choice == '4':
            example_4_data_quality()
        elif choice == '5':
            example_5_parallel_tasks()
        elif choice == '6':
            example_6_task_chain()
        elif choice == '7':
            list_active_tasks()
        else:
            print("❌ Invalid choice")

        if choice != '0':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
