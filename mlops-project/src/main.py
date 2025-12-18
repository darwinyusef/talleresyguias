"""
Main FastAPI application for MLOps platform.
"""
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Config
SERVICE_NAME = os.getenv("SERVICE_NAME", "mlops-platform")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin123@localhost:5672/")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager."""
    logger.info(f"Starting {SERVICE_NAME}...")
    yield
    logger.info(f"Shutting down {SERVICE_NAME}...")


app = FastAPI(
    title="MLOps Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": SERVICE_NAME,
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
    }


@app.post("/predict")
async def predict(data: dict):
    """Prediction endpoint."""
    logger.info(f"Received prediction request: {data}")

    # Aquí iría la lógica de predicción real
    return {
        "prediction": "example_result",
        "confidence": 0.95,
        "model_version": "1.0.0",
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
    )
