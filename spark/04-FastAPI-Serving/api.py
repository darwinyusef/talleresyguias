"""
FastAPI Serving Layer para Predicciones de Spark ML
===================================================
API REST que sirve predicciones generadas por modelos de Spark MLlib.

Características:
- Lectura de predicciones desde Parquet (generadas por Spark)
- Cache en memoria para baja latencia
- Integración opcional con PostgreSQL
- Batch predictions endpoint
- Health checks y métricas
- Carga de modelos MLflow para inferencia en tiempo real
"""

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
import os
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Spark ML Serving API",
    description="API para servir predicciones de modelos Spark MLlib",
    version="1.0.0"
)

# ============================================================================
# Configuration
# ============================================================================

PARQUET_PATH = os.getenv("PREDICTIONS_PATH", "data/lead_predictions.parquet")
POSTGRES_ENABLED = os.getenv("POSTGRES_ENABLED", "false").lower() == "true"

# Cache global para predicciones (cargadas desde Parquet)
predictions_cache: Optional[pd.DataFrame] = None
cache_loaded_at: Optional[datetime] = None

# ============================================================================
# Models (Pydantic)
# ============================================================================

class LeadInput(BaseModel):
    """Input para predicción de un lead"""
    age: int = Field(..., ge=18, le=100, description="Edad del lead")
    salary: float = Field(..., ge=0, description="Salario anual")
    web_visits: int = Field(..., ge=0, description="Número de visitas al sitio")
    last_action: str = Field(..., description="Última acción realizada")

    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "salary": 75000,
                "web_visits": 15,
                "last_action": "form_submit"
            }
        }

class LeadPrediction(BaseModel):
    """Respuesta de predicción"""
    lead_id: int
    predicted_conversion: float
    conversion_probability: float
    segment: str
    timestamp: datetime

class BatchLeadInput(BaseModel):
    """Input para predicciones batch"""
    leads: List[LeadInput]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    predictions_loaded: bool
    predictions_count: int
    cache_age_seconds: Optional[float]

# ============================================================================
# Data Loading Functions
# ============================================================================

def load_predictions_from_parquet():
    """Carga predicciones desde archivo Parquet generado por Spark"""
    global predictions_cache, cache_loaded_at

    try:
        logger.info(f"Cargando predicciones desde: {PARQUET_PATH}")

        if not os.path.exists(PARQUET_PATH):
            logger.warning(f"Archivo no encontrado: {PARQUET_PATH}")
            return None

        # Leer Parquet (compatible con PyArrow generado por Spark)
        df = pd.read_parquet(PARQUET_PATH)

        predictions_cache = df
        cache_loaded_at = datetime.now()

        logger.info(f"✅ {len(df)} predicciones cargadas exitosamente")
        logger.info(f"   Columnas: {list(df.columns)}")

        return df

    except Exception as e:
        logger.error(f"❌ Error cargando predicciones: {e}")
        return None

def get_predictions_dataframe() -> pd.DataFrame:
    """Obtiene el DataFrame de predicciones (carga si es necesario)"""
    global predictions_cache

    if predictions_cache is None:
        load_predictions_from_parquet()

    if predictions_cache is None:
        raise HTTPException(
            status_code=503,
            detail="Predictions not available. Run Spark ML model first."
        )

    return predictions_cache

# ============================================================================
# Helper Functions
# ============================================================================

def categorize_lead(probability: float) -> str:
    """Categoriza un lead basado en su probabilidad de conversión"""
    if probability >= 0.7:
        return "Hot Lead"
    elif probability >= 0.4:
        return "Warm Lead"
    else:
        return "Cold Lead"

def load_postgres_connection():
    """Carga conexión a PostgreSQL si está habilitada"""
    if not POSTGRES_ENABLED:
        return None

    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor

        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            database="spark_db",
            user="postgres",
            password="password"
        )
        return conn
    except Exception as e:
        logger.error(f"Error conectando a PostgreSQL: {e}")
        return None

# ============================================================================
# API Endpoints
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Carga datos al iniciar la API"""
    logger.info("🚀 Iniciando Spark ML Serving API...")
    load_predictions_from_parquet()

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "Spark ML Serving API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "prediction_by_id": "/predictions/{lead_id}",
            "all_predictions": "/predictions",
            "batch_predict": "/predict/batch (POST)",
            "realtime_predict": "/predict (POST)",
            "stats": "/stats"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    predictions_loaded = predictions_cache is not None
    predictions_count = len(predictions_cache) if predictions_loaded else 0

    cache_age = None
    if cache_loaded_at:
        cache_age = (datetime.now() - cache_loaded_at).total_seconds()

    return HealthResponse(
        status="healthy" if predictions_loaded else "degraded",
        predictions_loaded=predictions_loaded,
        predictions_count=predictions_count,
        cache_age_seconds=cache_age
    )

@app.get("/predictions/{lead_id}", tags=["Predictions"])
async def get_lead_prediction(lead_id: int):
    """
    Obtiene la predicción de un lead específico por ID.

    Args:
        lead_id: ID del lead

    Returns:
        Predicción y probabilidad de conversión
    """
    df = get_predictions_dataframe()

    # Buscar lead
    lead_data = df[df['lead_id'] == lead_id]

    if lead_data.empty:
        raise HTTPException(status_code=404, detail=f"Lead {lead_id} not found")

    # Obtener primera fila
    row = lead_data.iloc[0]

    return {
        "lead_id": int(row['lead_id']),
        "predicted_conversion": float(row['predicted_conversion']),
        "conversion_probability": float(row['conversion_probability']),
        "segment": categorize_lead(float(row['conversion_probability'])),
        "timestamp": datetime.now()
    }

@app.get("/predictions", tags=["Predictions"])
async def get_all_predictions(
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de resultados"),
    min_probability: float = Query(0.0, ge=0.0, le=1.0, description="Probabilidad mínima"),
    segment: Optional[str] = Query(None, description="Filtrar por segmento: hot, warm, cold")
):
    """
    Obtiene todas las predicciones con filtros opcionales.

    Args:
        limit: Número máximo de resultados
        min_probability: Filtrar por probabilidad mínima
        segment: Filtrar por segmento (hot, warm, cold)

    Returns:
        Lista de predicciones
    """
    df = get_predictions_dataframe()

    # Aplicar filtros
    filtered_df = df[df['conversion_probability'] >= min_probability]

    # Filtrar por segmento
    if segment:
        segment_map = {
            "hot": 0.7,
            "warm": 0.4,
            "cold": 0.0
        }

        if segment.lower() not in segment_map:
            raise HTTPException(status_code=400, detail="Segment must be: hot, warm, or cold")

        min_prob = segment_map[segment.lower()]
        if segment.lower() == "hot":
            filtered_df = filtered_df[filtered_df['conversion_probability'] >= 0.7]
        elif segment.lower() == "warm":
            filtered_df = filtered_df[
                (filtered_df['conversion_probability'] >= 0.4) &
                (filtered_df['conversion_probability'] < 0.7)
            ]
        else:  # cold
            filtered_df = filtered_df[filtered_df['conversion_probability'] < 0.4]

    # Ordenar por probabilidad descendente
    filtered_df = filtered_df.sort_values('conversion_probability', ascending=False)

    # Limitar resultados
    results = filtered_df.head(limit).to_dict('records')

    # Agregar segmento
    for result in results:
        result['segment'] = categorize_lead(result['conversion_probability'])
        result['timestamp'] = datetime.now()

    return {
        "total_count": len(filtered_df),
        "returned_count": len(results),
        "predictions": results
    }

@app.get("/stats", tags=["Analytics"])
async def get_statistics():
    """
    Obtiene estadísticas sobre las predicciones.

    Returns:
        Estadísticas agregadas
    """
    df = get_predictions_dataframe()

    stats = {
        "total_leads": len(df),
        "avg_probability": float(df['conversion_probability'].mean()),
        "median_probability": float(df['conversion_probability'].median()),
        "high_probability_count": len(df[df['conversion_probability'] >= 0.7]),
        "medium_probability_count": len(df[
            (df['conversion_probability'] >= 0.4) &
            (df['conversion_probability'] < 0.7)
        ]),
        "low_probability_count": len(df[df['conversion_probability'] < 0.4]),
        "predicted_conversions": int(df['predicted_conversion'].sum()),
        "segments": {
            "hot_leads": len(df[df['conversion_probability'] >= 0.7]),
            "warm_leads": len(df[
                (df['conversion_probability'] >= 0.4) &
                (df['conversion_probability'] < 0.7)
            ]),
            "cold_leads": len(df[df['conversion_probability'] < 0.4])
        }
    }

    return stats

@app.post("/predict", tags=["Realtime Inference"])
async def realtime_predict(lead: LeadInput):
    """
    Predicción en tiempo real usando modelo cargado.

    NOTA: Requiere modelo MLflow cargado. Por ahora retorna predicción mock.
    Para producción real, cargar modelo con mlflow.pyfunc.load_model()
    """

    # TODO: Cargar modelo MLflow y hacer predicción real
    # Por ahora, retornamos predicción simulada basada en reglas simples

    # Regla simple de scoring
    score = 0.0

    # Basado en salary
    if lead.salary > 80000:
        score += 0.3
    elif lead.salary > 50000:
        score += 0.2

    # Basado en visitas
    if lead.web_visits > 20:
        score += 0.3
    elif lead.web_visits > 10:
        score += 0.2

    # Basado en acción
    if lead.last_action == "form_submit":
        score += 0.4
    elif lead.last_action == "email_click":
        score += 0.2

    # Normalizar
    probability = min(score, 0.95)

    return {
        "lead_input": lead.dict(),
        "conversion_probability": round(probability, 4),
        "predicted_conversion": 1 if probability >= 0.5 else 0,
        "segment": categorize_lead(probability),
        "timestamp": datetime.now(),
        "note": "Mock prediction - Load MLflow model for real inference"
    }

@app.post("/reload-predictions", tags=["Admin"])
async def reload_predictions(background_tasks: BackgroundTasks):
    """
    Recarga las predicciones desde Parquet en background.

    Útil cuando Spark genera nuevas predicciones.
    """
    background_tasks.add_task(load_predictions_from_parquet)

    return {
        "message": "Predictions reload scheduled",
        "timestamp": datetime.now()
    }

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Iniciando servidor FastAPI...")
    logger.info(f"📁 Predictions path: {PARQUET_PATH}")
    logger.info(f"🔌 PostgreSQL: {'Enabled' if POSTGRES_ENABLED else 'Disabled'}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
