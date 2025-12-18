"""
Event schemas for the MLOps platform.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class EventType(str, Enum):
    """Tipos de eventos en el pipeline."""
    DATA_INGESTED = "data.ingested"
    DATA_VALIDATED = "data.validated"
    TRAINING_STARTED = "training.started"
    TRAINING_COMPLETED = "training.completed"
    TRAINING_FAILED = "training.failed"
    MODEL_VALIDATED = "model.validated"
    MODEL_REGISTERED = "model.registered"
    MODEL_DEPLOYED = "model.deployed"
    PREDICTION_REQUESTED = "prediction.requested"
    PREDICTION_COMPLETED = "prediction.completed"
    DRIFT_DETECTED = "drift.detected"
    DOCUMENT_CLASSIFIED = "document.classified"


class EventMetadata(BaseModel):
    """Metadata común para todos los eventos."""
    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_service: str
    correlation_id: Optional[UUID] = None
    version: str = "1.0.0"


class BaseEvent(BaseModel):
    """Clase base para todos los eventos."""
    metadata: EventMetadata
    payload: Dict[str, Any]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }


class DataIngestedEvent(BaseEvent):
    """Evento cuando datos nuevos son ingeridos."""
    class Payload(BaseModel):
        dataset_id: str
        dataset_path: str
        num_samples: int
        features: list[str]
        dataset_type: str  # train, val, test

    payload: Payload


class TrainingStartedEvent(BaseEvent):
    """Evento cuando inicia entrenamiento."""
    class Payload(BaseModel):
        experiment_id: str
        run_id: str
        model_type: str  # pytorch, tensorflow
        dataset_id: str
        hyperparameters: Dict[str, Any]

    payload: Payload


class TrainingCompletedEvent(BaseEvent):
    """Evento cuando termina entrenamiento."""
    class Payload(BaseModel):
        experiment_id: str
        run_id: str
        model_path: str
        metrics: Dict[str, float]
        duration_seconds: float
        artifacts: Dict[str, str]

    payload: Payload


class PredictionRequestedEvent(BaseEvent):
    """Evento cuando se solicita predicción."""
    class Payload(BaseModel):
        request_id: str
        model_id: str
        model_version: str
        input_data: Dict[str, Any]
        priority: str = "normal"

    payload: Payload


class PredictionCompletedEvent(BaseEvent):
    """Evento cuando predicción es completada."""
    class Payload(BaseModel):
        request_id: str
        prediction: Any
        confidence: Optional[float] = None
        latency_ms: float
        model_version: str

    payload: Payload
