"""
Pytest configuration and shared fixtures.
"""
import pytest
import os


@pytest.fixture(scope="session")
def test_config():
    """Test configuration."""
    return {
        "rabbitmq_url": os.getenv("TEST_RABBITMQ_URL", "amqp://admin:admin123@localhost:5672/"),
        "redis_url": os.getenv("TEST_REDIS_URL", "redis://localhost:6379/15"),
        "mlflow_uri": os.getenv("TEST_MLFLOW_URI", "http://localhost:5000"),
    }


@pytest.fixture
def mock_event_data():
    """Mock event data for testing."""
    return {
        "dataset_id": "test_dataset",
        "model_type": "pytorch",
        "experiment_id": "test_exp",
    }
