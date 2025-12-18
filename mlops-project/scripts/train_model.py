#!/usr/bin/env python3
"""
Script para entrenar modelos ML usando el pipeline event-driven.
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, Any
from uuid import uuid4

import mlflow
import torch
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.events.event_bus import EventBus, RedisEventStore
from src.events.schemas import BaseEvent, EventMetadata, EventType

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def generate_synthetic_dataset(
    n_samples: int = 10000,
    n_features: int = 20,
    n_classes: int = 2,
) -> tuple:
    """Genera dataset sintético para clasificación."""
    logger.info(
        f"Generating synthetic dataset: {n_samples} samples, "
        f"{n_features} features, {n_classes} classes"
    )

    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_features // 2,
        n_redundant=n_features // 4,
        n_classes=n_classes,
        random_state=42,
    )

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )

    logger.info(
        f"Dataset split - Train: {len(X_train)}, "
        f"Val: {len(X_val)}, Test: {len(X_test)}"
    )

    return (X_train, y_train), (X_val, y_val), (X_test, y_test)


def save_dataset(data: tuple, path: Path, name: str):
    """Guarda dataset en disco."""
    X, y = data
    path.mkdir(parents=True, exist_ok=True)

    torch.save({"X": torch.tensor(X, dtype=torch.float32), "y": torch.tensor(y)}, path / f"{name}.pt")

    logger.info(f"Saved {name} dataset to {path / name}.pt")


def publish_training_request(
    event_bus: EventBus,
    event_store: RedisEventStore,
    dataset_id: str,
    hyperparameters: Dict[str, Any],
):
    """Publica evento para iniciar entrenamiento."""
    correlation_id = uuid4()

    # Crear evento de datos validados (trigger para training)
    event = BaseEvent(
        metadata=EventMetadata(
            event_type=EventType.DATA_VALIDATED,
            source_service="training-script",
            correlation_id=correlation_id,
        ),
        payload={
            "dataset_id": dataset_id,
            "hyperparameters": hyperparameters,
            "status": "ready_for_training",
        },
    )

    # Publicar
    event_bus.publish(event, routing_key="data.validated")
    event_store.store_event(event)

    logger.info(
        f"Published training request with correlation_id: {correlation_id}"
    )

    return correlation_id


def main():
    parser = argparse.ArgumentParser(
        description="Train ML model using event-driven pipeline"
    )
    parser.add_argument(
        "--dataset-id",
        type=str,
        default=None,
        help="Dataset ID (will generate synthetic if not provided)",
    )
    parser.add_argument(
        "--model-type",
        type=str,
        choices=["pytorch", "tensorflow"],
        default="pytorch",
        help="Model framework",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of training epochs",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.001,
        help="Learning rate",
    )
    parser.add_argument(
        "--hidden-dim",
        type=int,
        default=64,
        help="Hidden layer dimension",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size",
    )
    parser.add_argument(
        "--rabbitmq-url",
        type=str,
        default="amqp://admin:admin123@localhost:5672/",
        help="RabbitMQ URL",
    )
    parser.add_argument(
        "--redis-url",
        type=str,
        default="redis://localhost:6379/0",
        help="Redis URL",
    )

    args = parser.parse_args()

    # Generar o usar dataset existente
    if args.dataset_id is None:
        # Generar dataset sintético
        dataset_id = f"synthetic_{uuid4().hex[:8]}"
        logger.info(f"Generating synthetic dataset with ID: {dataset_id}")

        train_data, val_data, test_data = generate_synthetic_dataset()

        # Guardar datasets
        data_path = Path("data") / dataset_id
        save_dataset(train_data, data_path, "train")
        save_dataset(val_data, data_path, "val")
        save_dataset(test_data, data_path, "test")

    else:
        dataset_id = args.dataset_id
        logger.info(f"Using existing dataset: {dataset_id}")

    # Configurar hiperparámetros
    hyperparameters = {
        "model_type": args.model_type,
        "num_epochs": args.epochs,
        "learning_rate": args.lr,
        "hidden_dim": args.hidden_dim,
        "batch_size": args.batch_size,
    }

    logger.info(f"Hyperparameters: {hyperparameters}")

    # Conectar a event bus
    logger.info("Connecting to event bus...")
    event_bus = EventBus(args.rabbitmq_url)
    event_bus.connect()

    event_store = RedisEventStore(args.redis_url)

    # Publicar request de entrenamiento
    correlation_id = publish_training_request(
        event_bus, event_store, dataset_id, hyperparameters
    )

    logger.info("=" * 60)
    logger.info("Training request submitted successfully!")
    logger.info(f"Dataset ID: {dataset_id}")
    logger.info(f"Correlation ID: {correlation_id}")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Check training progress:")
    logger.info("  - MLflow UI: http://localhost:5000")
    logger.info("  - Service logs: docker-compose logs -f pytorch-service")
    logger.info("  - Metrics: http://localhost:9090")
    logger.info("")
    logger.info("Track events with correlation ID:")
    logger.info(f"  redis-cli LRANGE correlation:{correlation_id} 0 -1")

    # Cleanup
    event_bus.disconnect()


if __name__ == "__main__":
    main()
