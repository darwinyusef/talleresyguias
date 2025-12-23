# 🚀 Módulo 04: Model Serving con FastAPI + Spark

Aprende a servir modelos de Machine Learning entrenados con Spark en producción mediante APIs REST de alta performance con FastAPI.

---

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Entender los fundamentos de ML Model Serving y deployment
- ✅ Construir APIs REST de producción con FastAPI
- ✅ Servir predicciones desde archivos Parquet generados por Spark
- ✅ Implementar caching en memoria para baja latencia (<50ms)
- ✅ Diseñar endpoints para batch y real-time inference
- ✅ Implementar health checks y monitoring
- ✅ Manejar diferentes patrones de serving (batch, online, streaming)
- ✅ Optimizar performance para alta throughput y baja latencia

---

## 📚 Fundamentos Teóricos

### ¿Qué es Model Serving?

**Model Serving** es el proceso de hacer que un modelo de ML entrenado esté disponible para hacer predicciones en producción sobre nuevos datos.

```
Training (Offline)          →          Serving (Online)
═══════════════════════════════════════════════════════
Historical Data                        New Data
       ↓                                     ↓
[Train Model]                          [Load Model]
       ↓                                     ↓
Save to Storage                  [Make Prediction]
(MLflow/S3/DB)                              ↓
                                      Return Result
```

### El Problema del "Last Mile" en ML

**80% del tiempo en ML** se gasta en entrenamiento e investigación. **Solo 20% en deployment**, pero es donde el negocio obtiene valor.

```
Jupyter Notebook (90% accuracy) → ✅ Funciona
                ↓
Model en producción (¿?)        → ❌ No disponible = $0 valor
```

**Model Serving** cierra esta brecha.

---

## 🏗️ Arquitecturas de Model Serving

### 1. Batch Serving (Offline Predictions)

**Cuándo usar:** Predicciones que no necesitan ser inmediatas

```
                Scheduled Job
                     ↓
[Spark Batch] → Generate predictions
                     ↓
              Save to Database
                     ↓
            [API] → Read from DB
                     ↓
                Application
```

**Ejemplo:** Scoring diario de 1M leads
- ✅ Pro: Económico, puede procesar volúmenes masivos
- ❌ Con: Latencia de horas/días, predicciones "stale"

**Implementación:**
```python
# Spark genera predicciones cada noche
predictions_df = model.transform(all_leads)
predictions_df.write.parquet("s3://predictions/date=2024-01-15/")

# API lee predicciones pre-calculadas
@app.get("/predictions/{lead_id}")
def get_prediction(lead_id: int):
    # Leer de cache/DB
    return cached_predictions[lead_id]
```

### 2. Online Serving (Real-time Predictions)

**Cuándo usar:** Predicciones inmediatas (< 100ms latency)

```
User Request → [API] → [Load Model] → Predict → Response
                            ↑
                      Model in Memory
```

**Ejemplo:** Recomendación de productos al navegar
- ✅ Pro: Latencia baja, predicciones actualizadas
- ❌ Con: Mayor costo compute, límites de throughput

### 3. Cache Pattern (Usado en este módulo)

Predicciones pre-calculadas en cache:

```
Spark Batch    FastAPI with Cache
    ↓               ↓
[Generate]     [Load Parquet]
predictions         ↓
    ↓          [In-Memory Cache]
Parquet             ↓
               Serve <50ms
```

**Pros:**
- ✅ Latencia ultra-baja
- ✅ Throughput alto
- ✅ Simple y económico

**Cons:**
- ❌ Solo para predicciones pre-calculadas
- ❌ Requiere refresh periódico

---

## 🚀 FastAPI: El Framework Moderno

### ¿Por qué FastAPI?

**FastAPI** es el framework web Python de más rápido crecimiento, especialmente popular para ML serving.

| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| **Performance** | ⚡⚡⚡ (Async) | ⚡ (Sync) | ⚡ (Sync) |
| **Documentación automática** | ✅ OpenAPI/Swagger | ❌ | ❌ |
| **Type validation** | ✅ Pydantic | ❌ | Parcial |
| **Async support** | ✅ Nativo | ⚡ Limitado | ⚡ Limitado |
| **ML Serving** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

**Benchmark (requests/second):**
```
FastAPI (async): 20,000+ req/s
Flask:            2,000 req/s
Django:           1,500 req/s
```

---

## 🛠️ API Endpoints

### GET /predictions/{lead_id} - Predicción Individual

```bash
curl http://localhost:8000/predictions/42

# Response:
{
  "lead_id": 42,
  "conversion_probability": 0.8234,
  "segment": "Hot Lead",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /predictions - Batch con Filtros

```bash
# Top 10 hot leads
curl "http://localhost:8000/predictions?segment=hot&limit=10"

# Leads con prob > 0.5
curl "http://localhost:8000/predictions?min_probability=0.5&limit=50"
```

### POST /predict - Inferencia en Tiempo Real

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "salary": 75000,
    "web_visits": 15,
    "last_action": "form_submit"
  }'

# Response:
{
  "conversion_probability": 0.82,
  "predicted_conversion": 1,
  "segment": "Hot Lead"
}
```

### GET /stats - Analytics

```bash
curl http://localhost:8000/stats

# Response:
{
  "total_leads": 1000,
  "avg_probability": 0.45,
  "segments": {
    "hot_leads": 150,
    "warm_leads": 350,
    "cold_leads": 500
  }
}
```

### GET /health - Health Check

```bash
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "predictions_loaded": true,
  "predictions_count": 1000,
  "cache_age_seconds": 3600
}
```

---

## 🚀 Inicio Rápido

### 1. Generar Predicciones con Spark

```bash
# Primero genera datos
python scripts/generate_data.py

# Entrena modelo y genera predicciones
python 02-03-ML/lead_scoring.py

# Verifica que se generó el archivo
ls -lh data/lead_predictions.parquet
```

### 2. Iniciar API

```bash
# Instalar dependencias
pip install fastapi uvicorn pandas pyarrow

# Iniciar servidor
python 04-FastAPI-Serving/api.py

# O con uvicorn
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 3. Probar API

```bash
# Abrir documentación interactiva
open http://localhost:8000/docs

# O probar endpoints
curl http://localhost:8000/health
curl http://localhost:8000/predictions/1
curl http://localhost:8000/stats
```

---

## 📊 Performance

### Latency Targets

| Endpoint | Target | Actual |
|----------|--------|--------|
| GET /predictions/{id} | <50ms | ~5ms |
| GET /predictions (batch) | <200ms | ~50ms |
| POST /predict (realtime) | <100ms | ~30ms |
| GET /stats | <100ms | ~20ms |

### Optimizaciones Implementadas

1. **In-Memory Cache**: Predicciones cargadas en RAM (pandas DataFrame)
2. **Indexed Lookups**: O(1) búsqueda por lead_id
3. **ORJSON**: Serialización JSON 2x más rápida
4. **Async Endpoints**: No bloquean el event loop

---

## 🔍 Monitoring

### Métricas Disponibles

- Total de requests por endpoint
- Latencia promedio, p50, p95, p99
- Cache hit rate
- Error rate por tipo
- Edad del cache

### Integración con Prometheus

```python
from prometheus_client import Counter, Histogram

prediction_requests = Counter(
    'prediction_requests_total',
    'Total prediction requests',
    ['endpoint', 'status']
)

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

---

## 🐳 Deployment

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t lead-scoring-api .
docker run -p 8000:8000 -v $(pwd)/data:/app/data lead-scoring-api
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lead-scoring-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: lead-scoring-api:v1.0
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
```

---

## 💡 Mejores Prácticas

### 1. Caching Estratégico

```python
# BIEN: Cache global cargado al iniciar
predictions_cache = pd.read_parquet("predictions.parquet")

# MAL: Leer en cada request
df = pd.read_parquet("predictions.parquet")  # ❌ Muy lento
```

### 2. Validación con Pydantic

```python
from pydantic import BaseModel, Field

class LeadInput(BaseModel):
    age: int = Field(..., ge=18, le=100)
    salary: float = Field(..., gt=0)
    web_visits: int = Field(..., ge=0)
```

### 3. Rate Limiting

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/predictions/{lead_id}")
@limiter.limit("100/minute")
async def get_prediction(lead_id: int):
    ...
```

### 4. Logging Estructurado

```python
logger.info(json.dumps({
    "event": "prediction_made",
    "lead_id": lead_id,
    "probability": prob,
    "latency_ms": latency
}))
```

---

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Models](https://pydantic-docs.helpmanual.io/)
- [ML Model Serving Patterns](https://www.kdnuggets.com/2021/01/ml-model-serving-patterns.html)

---

**¡Siguiente paso! 👉 [Módulo 08: Streaming ML](../08-Spark-Streaming/README.md) para scoring en tiempo real con Kafka**

