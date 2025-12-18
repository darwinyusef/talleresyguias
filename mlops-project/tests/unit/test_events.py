"""
Unit tests for event system.
"""
import pytest
from datetime import datetime
from uuid import uuid4

from src.events.schemas import (
    EventType,
    EventMetadata,
    BaseEvent,
    DataIngestedEvent,
    TrainingStartedEvent,
)


class TestEventSchemas:
    """Test event schemas."""

    def test_event_metadata_creation(self):
        """Test creating event metadata."""
        metadata = EventMetadata(
            event_type=EventType.DATA_INGESTED,
            source_service="test-service",
        )

        assert metadata.event_type == EventType.DATA_INGESTED
        assert metadata.source_service == "test-service"
        assert isinstance(metadata.event_id, type(uuid4()))
        assert isinstance(metadata.timestamp, datetime)
        assert metadata.version == "1.0.0"

    def test_base_event_creation(self):
        """Test creating base event."""
        metadata = EventMetadata(
            event_type=EventType.DATA_INGESTED,
            source_service="test-service",
        )

        event = BaseEvent(
            metadata=metadata,
            payload={"test": "data"},
        )

        assert event.metadata.event_type == EventType.DATA_INGESTED
        assert event.payload == {"test": "data"}

    def test_data_ingested_event(self):
        """Test DataIngestedEvent."""
        metadata = EventMetadata(
            event_type=EventType.DATA_INGESTED,
            source_service="test-service",
        )

        payload = DataIngestedEvent.Payload(
            dataset_id="test_dataset",
            dataset_path="/data/test",
            num_samples=1000,
            features=["feature1", "feature2"],
            dataset_type="train",
        )

        event = DataIngestedEvent(
            metadata=metadata,
            payload=payload,
        )

        assert event.payload.dataset_id == "test_dataset"
        assert event.payload.num_samples == 1000
        assert len(event.payload.features) == 2

    def test_training_started_event(self):
        """Test TrainingStartedEvent."""
        metadata = EventMetadata(
            event_type=EventType.TRAINING_STARTED,
            source_service="training-service",
        )

        payload = TrainingStartedEvent.Payload(
            experiment_id="exp_001",
            run_id="run_001",
            model_type="pytorch",
            dataset_id="dataset_001",
            hyperparameters={"lr": 0.001, "epochs": 10},
        )

        event = TrainingStartedEvent(
            metadata=metadata,
            payload=payload,
        )

        assert event.payload.experiment_id == "exp_001"
        assert event.payload.model_type == "pytorch"
        assert event.payload.hyperparameters["lr"] == 0.001

    def test_event_json_serialization(self):
        """Test event JSON serialization."""
        metadata = EventMetadata(
            event_type=EventType.DATA_INGESTED,
            source_service="test-service",
        )

        event = BaseEvent(
            metadata=metadata,
            payload={"test": "data"},
        )

        json_str = event.model_dump_json()
        assert isinstance(json_str, str)
        assert "test" in json_str
        assert "data" in json_str

    def test_event_correlation_id(self):
        """Test event correlation ID."""
        correlation_id = uuid4()

        metadata = EventMetadata(
            event_type=EventType.TRAINING_STARTED,
            source_service="test-service",
            correlation_id=correlation_id,
        )

        event = BaseEvent(
            metadata=metadata,
            payload={"test": "data"},
        )

        assert event.metadata.correlation_id == correlation_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
