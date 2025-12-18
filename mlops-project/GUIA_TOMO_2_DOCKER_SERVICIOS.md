# 📚 Guía MLOps - Tomo 2: Docker y Servicios Básicos

> **Nivel:** Principiante-Intermedio
> **Duración estimada:** 3-4 horas
> **Prerequisito:** Tomo 1 completado

---

## 🎯 Objetivos de este Tomo

Al finalizar este tomo podrás:
- ✅ Entender cómo funcionan los contenedores Docker
- ✅ Usar PyTorch Service para hacer predicciones
- ✅ Registrar experimentos en MLflow
- ✅ Trabajar con FastAPI y APIs REST
- ✅ Leer y entender logs
- ✅ Monitorear métricas con Prometheus

---

## 📖 Capítulo 1: Fundamentos de Docker

### 1.1 ¿Qué es un Contenedor?

**Analogía:** Un contenedor es como una caja de LEGO completa

```
🏠 Tu Computadora (Host)
└── 📦 Contenedor 1: PyTorch Service
    ├── Ubuntu Linux
    ├── Python 3.11
    ├── PyTorch 2.1
    ├── Tu código
    └── SOLO lo necesario

└── 📦 Contenedor 2: PostgreSQL
    ├── Linux
    ├── PostgreSQL 16
    └── Datos de MLflow
```

**Ventajas:**
- ✅ **Aislamiento**: Cada contenedor es independiente
- ✅ **Portabilidad**: Funciona igual en cualquier lugar
- ✅ **Ligero**: Comparte el kernel del sistema
- ✅ **Rápido**: Inicia en segundos

### 1.2 Imagen vs Contenedor

**Imagen** = Receta 📄
- Template read-only
- Se construye una vez
- Se puede compartir

**Contenedor** = Plato cocinado 🍽️
- Instancia de una imagen
- Se ejecuta y puede cambiar
- Temporal (se puede crear/destruir)

```bash
# Ver imágenes disponibles
docker images

# Ver contenedores corriendo
docker ps

# Ver TODOS los contenedores (incluso parados)
docker ps -a
```

### 1.3 Anatomía de un Dockerfile

Nuestro `Dockerfile.pytorch`:

```dockerfile
# ============================================
# PASO 1: Imagen base
# ============================================
FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
# ↑ Partimos de una imagen que ya tiene PyTorch

# ============================================
# PASO 2: Metadata
# ============================================
LABEL maintainer="mlops@example.com"
LABEL description="PyTorch ML Service"
# ↑ Información sobre la imagen

# ============================================
# PASO 3: Variables de entorno
# ============================================
ENV PYTHONUNBUFFERED=1
# ↑ Configuraciones del ambiente

# ============================================
# PASO 4: Instalar dependencias del sistema
# ============================================
RUN apt-get update && apt-get install -y \
    curl \
    git
# ↑ Instala software necesario

# ============================================
# PASO 5: Copiar código
# ============================================
COPY ./src ./src
COPY requirements.txt .
# ↑ Copia archivos de tu máquina al contenedor

# ============================================
# PASO 6: Instalar dependencias Python
# ============================================
RUN pip install -r requirements.txt
# ↑ Instala librerías de Python

# ============================================
# PASO 7: Puerto
# ============================================
EXPOSE 8000
# ↑ Declara qué puerto usa el servicio

# ============================================
# PASO 8: Comando de inicio
# ============================================
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
# ↑ Qué ejecutar cuando inicia el contenedor
```

### 1.4 Docker Compose - Orquestación

**docker-compose.yml** define TODOS los servicios:

```yaml
services:
  # Cada servicio es un contenedor

  pytorch-service:
    build: .                    # Construir desde Dockerfile
    ports:
      - "8000:8000"            # Puerto host:container
    environment:
      - SERVICE_NAME=pytorch   # Variables de entorno
    volumes:
      - ./src:/app/src         # Montar carpetas
    depends_on:
      - rabbitmq               # Esperar a RabbitMQ
      - redis
    networks:
      - mlops-network          # Red compartida
```

**¿Por qué Docker Compose?**
- Un solo comando para manejar 11 servicios
- Define dependencias entre servicios
- Crea redes automáticamente
- Gestiona volúmenes de datos

---

## 📖 Capítulo 2: PyTorch Service en Profundidad

### 2.1 Arquitectura del Servicio

```
┌──────────────────────────────────────┐
│      PyTorch Service (FastAPI)       │
└──────────────────────────────────────┘

Puerto 8000
    │
    ├── GET /              → Info del servicio
    ├── GET /health        → Health check
    ├── POST /predict      → Hacer predicción
    └── GET /metrics       → Métricas Prometheus
```

### 2.2 Explorar el Código

**Abrir el archivo:** `src/main.py`

```python
# ============================================
# IMPORTACIONES
# ============================================
from fastapi import FastAPI
# ↑ Framework web moderno y rápido

import uvicorn
# ↑ Servidor ASGI para FastAPI

# ============================================
# CREAR APLICACIÓN
# ============================================
app = FastAPI(
    title="MLOps Platform",
    version="1.0.0",
)
# ↑ Instancia de FastAPI con metadata

# ============================================
# ENDPOINT RAÍZ
# ============================================
@app.get("/")
async def root():
    """
    Endpoint principal
    Responde con información del servicio
    """
    return {
        "service": "pytorch-service",
        "version": "1.0.0",
        "status": "running",
    }

# ============================================
# HEALTH CHECK
# ============================================
@app.get("/health")
async def health():
    """
    Health check para Kubernetes/monitoring
    Verifica que el servicio esté vivo
    """
    return {
        "status": "healthy",
        "service": "pytorch-service",
    }

# ============================================
# PREDICCIÓN
# ============================================
@app.post("/predict")
async def predict(data: dict):
    """
    Endpoint principal de predicción

    Args:
        data: Diccionario con datos de entrada

    Returns:
        Diccionario con predicción
    """
    # Aquí iría tu modelo ML real
    return {
        "prediction": "example_result",
        "confidence": 0.95,
        "model_version": "1.0.0",
    }
```

### 2.3 Probar los Endpoints

#### Método 1: Con curl (Terminal)

```bash
# 1. Root endpoint
curl http://localhost:8000/

# Respuesta:
# {
#   "service": "pytorch-service",
#   "version": "1.0.0",
#   "status": "running"
# }

# 2. Health check
curl http://localhost:8000/health

# 3. Predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

#### Método 2: Con Python

Crear archivo `test_pytorch.py`:

```python
import requests

# URL base del servicio
BASE_URL = "http://localhost:8000"

# Test 1: Root
print("🧪 Test 1: Root endpoint")
response = requests.get(f"{BASE_URL}/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Test 2: Health
print("🧪 Test 2: Health check")
response = requests.get(f"{BASE_URL}/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

# Test 3: Predicción
print("🧪 Test 3: Predicción")
data = {"data": "test input"}
response = requests.post(f"{BASE_URL}/predict", json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

Ejecutar:
```bash
python test_pytorch.py
```

#### Método 3: Swagger UI (Navegador)

FastAPI genera documentación interactiva automáticamente:

1. Abrir: http://localhost:8000/docs
2. Ver todos los endpoints
3. Probar directamente desde el navegador
4. Ver esquemas de request/response

### 2.4 Ver Logs en Tiempo Real

```bash
# Logs del servicio PyTorch
docker-compose logs -f pytorch-service

# Ver solo últimas 50 líneas
docker-compose logs --tail=50 pytorch-service

# Filtrar por ERROR
docker-compose logs pytorch-service | grep ERROR

# Ver múltiples servicios
docker-compose logs -f pytorch-service tensorflow-service
```

**Interpretar logs:**
```
mlops-pytorch | INFO:     Started server process [1]
                ↑ Nombre     ↑ Level  ↑ Mensaje
               contenedor
```

---

## 📖 Capítulo 3: MLflow - Tracking de Experimentos

### 3.1 ¿Qué es MLflow?

MLflow es tu **laboratorio digital** para ML:

```
🔬 EXPERIMENTO
├── Run 1: learning_rate=0.001 → accuracy=0.85
├── Run 2: learning_rate=0.01  → accuracy=0.92 ✅ Mejor
└── Run 3: learning_rate=0.1   → accuracy=0.78
```

**Problema sin MLflow:**
```
experimento_v1.ipynb
experimento_v2_final.ipynb
experimento_v2_final_REAL.ipynb
experimento_v3_ahora_si.ipynb
```

**Con MLflow:**
- ✅ Todos los experimentos organizados
- ✅ Comparar visualmente
- ✅ Reproducir cualquier run
- ✅ Compartir con el equipo

### 3.2 Componentes de MLflow

```
┌──────────────────────────────────────┐
│             MLflow                    │
└──────────────────────────────────────┘

1. TRACKING
   → Registrar parámetros, métricas, modelos

2. PROJECTS
   → Empaquetar código reproducible

3. MODELS
   → Gestionar modelos en producción

4. REGISTRY
   → Versionado central de modelos
```

### 3.3 Acceder a MLflow UI

1. Abrir: http://localhost:5000
2. Verás el dashboard principal
3. Por ahora está vacío (sin experimentos)

**Elementos de la UI:**
- **Experiments**: Lista de experimentos
- **Runs**: Ejecuciones dentro de un experimento
- **Compare**: Comparar múltiples runs
- **Models**: Modelos registrados

### 3.4 Primer Experimento con MLflow

Crear `scripts/my_first_experiment.py`:

```python
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ============================================
# CONFIGURAR MLFLOW
# ============================================
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("iris-classification")

# ============================================
# CARGAR DATOS
# ============================================
print("📊 Cargando datos...")
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# ============================================
# EXPERIMENTO
# ============================================
# Probar diferentes hiperparámetros
params_to_test = [
    {"n_estimators": 10, "max_depth": 3},
    {"n_estimators": 50, "max_depth": 5},
    {"n_estimators": 100, "max_depth": 10},
]

for params in params_to_test:
    # Iniciar un "run" en MLflow
    with mlflow.start_run(run_name=f"rf_{params['n_estimators']}"):

        print(f"\n🧪 Entrenando con {params}")

        # ============================================
        # 1. LOG PARÁMETROS
        # ============================================
        mlflow.log_params(params)

        # ============================================
        # 2. ENTRENAR MODELO
        # ============================================
        model = RandomForestClassifier(**params, random_state=42)
        model.fit(X_train, y_train)

        # ============================================
        # 3. EVALUAR
        # ============================================
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))

        # ============================================
        # 4. LOG MÉTRICAS
        # ============================================
        mlflow.log_metric("train_accuracy", train_acc)
        mlflow.log_metric("test_accuracy", test_acc)

        # ============================================
        # 5. LOG MODELO
        # ============================================
        mlflow.sklearn.log_model(model, "random_forest_model")

        print(f"  ✓ Train Accuracy: {train_acc:.4f}")
        print(f"  ✓ Test Accuracy: {test_acc:.4f}")

print("\n🎉 ¡Experimentos completados!")
print("👉 Ver resultados en: http://localhost:5000")
```

**Ejecutar:**
```bash
python scripts/my_first_experiment.py
```

**Ver en MLflow UI:**
1. Refresh http://localhost:5000
2. Ver experimento "iris-classification"
3. Ver los 3 runs
4. Compararlos visualmente

### 3.5 Comparar Runs en MLflow

En la UI de MLflow:

1. Seleccionar múltiples runs (checkbox)
2. Click en "Compare"
3. Ver tabla de comparación:

```
Run             | n_estimators | max_depth | test_accuracy
----------------|--------------|-----------|---------------
rf_10           | 10           | 3         | 0.9333
rf_50           | 50           | 5         | 0.9667
rf_100          | 100          | 10        | 1.0000  ✅ Mejor
```

4. Ver gráficas paralelas
5. Analizar diferencias

---

## 📖 Capítulo 4: Prometheus y Métricas

### 4.1 ¿Qué es Prometheus?

Prometheus es un **sistema de monitoreo** que:
- Recolecta métricas cada X segundos
- Almacena en base de datos de series temporales
- Permite hacer queries y alertas

**Métricas típicas:**
- 🔢 **Counters**: Cuentan eventos (requests totales)
- 📊 **Gauges**: Valores que suben/bajan (CPU usage)
- ⏱️ **Histograms**: Distribuciones (latencia)

### 4.2 Acceder a Prometheus

1. Abrir: http://localhost:9090
2. Ver el dashboard
3. Ir a "Graph"

### 4.3 Queries Básicas

En la UI de Prometheus, probar estas queries:

#### Query 1: Ver métricas disponibles
```promql
{job="pytorch-service"}
```

#### Query 2: Requests por segundo
```promql
rate(requests_total[5m])
```

#### Query 3: Latencia promedio
```promql
avg(request_duration_seconds)
```

#### Query 4: Uso de CPU
```promql
process_cpu_seconds_total{job="pytorch-service"}
```

### 4.4 Añadir Métricas Custom

Editar `src/main.py`:

```python
from prometheus_client import Counter, Histogram, make_asgi_app

# ============================================
# DEFINIR MÉTRICAS
# ============================================
# Counter: Solo incrementa
requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint']
)

# Histogram: Para latencias
request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration'
)

# ============================================
# USAR EN ENDPOINTS
# ============================================
@app.get("/")
async def root():
    # Incrementar contador
    requests_total.labels(method='GET', endpoint='/').inc()

    return {"service": "pytorch-service"}

@app.post("/predict")
async def predict(data: dict):
    # Medir tiempo
    with request_duration.time():
        # Tu código aquí
        result = {"prediction": "example"}

    requests_total.labels(method='POST', endpoint='/predict').inc()
    return result

# ============================================
# ENDPOINT DE MÉTRICAS
# ============================================
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

**Ver métricas:**
```bash
curl http://localhost:8000/metrics
```

Verás algo como:
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{endpoint="/",method="GET"} 42.0
api_requests_total{endpoint="/predict",method="POST"} 15.0

# HELP api_request_duration_seconds API request duration
# TYPE api_request_duration_seconds histogram
api_request_duration_seconds_bucket{le="0.005"} 10.0
api_request_duration_seconds_sum 1.234
api_request_duration_seconds_count 57.0
```

---

## 📖 Capítulo 5: Trabajando con Datos

### 5.1 Estructura de Datos

```
mlops-project/
├── data/              ← Datasets
│   ├── raw/           ← Datos originales
│   ├── processed/     ← Datos procesados
│   └── models/        ← Modelos guardados
```

### 5.2 Montar Volúmenes

En `docker-compose.yml`:

```yaml
pytorch-service:
  volumes:
    - ./data:/app/data      # Carpeta local → carpeta en contenedor
    - ./models:/app/models
```

**¿Qué significa esto?**
- Cambios en `./data` se ven en el contenedor
- Modelos guardados persisten después de detener el contenedor

### 5.3 Ejemplo: Guardar un Modelo

```python
import torch
import torch.nn as nn

# ============================================
# CREAR MODELO SIMPLE
# ============================================
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 2)

    def forward(self, x):
        return self.linear(x)

# Instanciar
model = SimpleModel()

# ============================================
# GUARDAR MODELO
# ============================================
# Dentro del contenedor: /app/models/my_model.pth
# En tu máquina: ./models/my_model.pth
torch.save(model.state_dict(), '/app/models/my_model.pth')

print("✅ Modelo guardado en ./models/my_model.pth")
```

**Verificar en tu máquina:**
```bash
ls -lh models/
# Debes ver my_model.pth
```

---

## 📖 Capítulo 6: Proyecto Práctico

### 6.1 Objetivo

Crear un clasificador de imágenes:
1. Entrenar modelo con PyTorch
2. Registrar en MLflow
3. Exponer como API
4. Monitorear con Prometheus

### 6.2 Paso 1: Entrenar Modelo

Crear `scripts/train_image_classifier.py`:

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import mlflow
import mlflow.pytorch

# ============================================
# CONFIGURACIÓN
# ============================================
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("image-classifier")

# ============================================
# PREPARAR DATOS
# ============================================
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Descargar MNIST
train_dataset = datasets.MNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

# DataLoader
train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True
)

# ============================================
# MODELO
# ============================================
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# ============================================
# ENTRENAR
# ============================================
with mlflow.start_run(run_name="mnist-classifier"):

    # Hiperparámetros
    params = {
        "epochs": 3,
        "lr": 0.001,
        "batch_size": 64
    }
    mlflow.log_params(params)

    # Modelo
    model = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=params["lr"])

    # Training loop
    for epoch in range(params["epochs"]):
        running_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if i % 100 == 99:
                avg_loss = running_loss / 100
                print(f'Epoch {epoch+1}, Batch {i+1}: Loss = {avg_loss:.4f}')
                mlflow.log_metric("loss", avg_loss, step=i)
                running_loss = 0.0

    # Guardar modelo
    mlflow.pytorch.log_model(model, "mnist_model")
    torch.save(model.state_dict(), './models/mnist_classifier.pth')

    print("✅ Entrenamiento completado!")
```

**Ejecutar:**
```bash
python scripts/train_image_classifier.py
```

### 6.3 Paso 2: Cargar y Usar Modelo

Crear `scripts/predict_image.py`:

```python
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# ============================================
# DEFINIR MODELO (misma arquitectura)
# ============================================
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# ============================================
# CARGAR MODELO
# ============================================
model = Net()
model.load_state_dict(torch.load('./models/mnist_classifier.pth'))
model.eval()

print("✅ Modelo cargado")

# ============================================
# PREPARAR IMAGEN
# ============================================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# ============================================
# PREDECIR
# ============================================
def predict_digit(image_path):
    """Predice qué dígito es una imagen"""

    # Cargar imagen
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)

    # Predecir
    with torch.no_grad():
        output = model(image)
        prediction = output.argmax(dim=1).item()
        confidence = torch.softmax(output, dim=1).max().item()

    return prediction, confidence

# Ejemplo de uso
if __name__ == "__main__":
    # Necesitas una imagen de prueba
    # prediction, confidence = predict_digit("test_image.png")
    # print(f"Predicción: {prediction}, Confianza: {confidence:.2%}")

    print("👉 Usa: predict_digit('path/to/image.png')")
```

### 6.4 Paso 3: Integrar en API

Editar `src/main.py` para añadir endpoint:

```python
from fastapi import FastAPI, File, UploadFile
import torch
from PIL import Image
import io

app = FastAPI()

# Cargar modelo al inicio
model = load_model()  # Tu función

@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    """
    Predice qué dígito contiene una imagen
    """
    # Leer imagen
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Predecir
    prediction, confidence = predict_digit(image)

    return {
        "digit": prediction,
        "confidence": confidence,
        "model": "mnist-classifier"
    }
```

**Probar:**
```bash
curl -X POST http://localhost:8000/predict/image \
  -F "file=@test_digit.png"
```

---

## 📖 Capítulo 7: Ejercicios Prácticos

### Ejercicio 1: Añadir Logging

Modificar `src/main.py` para añadir logs estructurados:

```python
import logging
import structlog

# Configurar logger
logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger()

@app.post("/predict")
async def predict(data: dict):
    logger.info("prediction_request", data=data)

    # Tu código
    result = {"prediction": "example"}

    logger.info("prediction_response", result=result)
    return result
```

### Ejercicio 2: Cacheo con Redis

Usar Redis para cachear predicciones:

```python
import redis
import json
import hashlib

redis_client = redis.from_url("redis://redis:6379/0")

@app.post("/predict")
async def predict(data: dict):
    # Crear key del cache
    cache_key = hashlib.md5(
        json.dumps(data).encode()
    ).hexdigest()

    # Buscar en cache
    cached = redis_client.get(cache_key)
    if cached:
        logger.info("cache_hit", key=cache_key)
        return json.loads(cached)

    # Si no existe, calcular
    result = calculate_prediction(data)

    # Guardar en cache (1 hora)
    redis_client.setex(
        cache_key,
        3600,
        json.dumps(result)
    )

    return result
```

### Ejercicio 3: Rate Limiting

Limitar número de requests por usuario:

```python
from fastapi import HTTPException
from collections import defaultdict
import time

# Contador de requests por IP
request_counts = defaultdict(list)
MAX_REQUESTS = 10  # por minuto

@app.post("/predict")
async def predict(request: Request, data: dict):
    # Obtener IP del cliente
    client_ip = request.client.host

    # Limpiar requests antiguos
    now = time.time()
    request_counts[client_ip] = [
        t for t in request_counts[client_ip]
        if now - t < 60
    ]

    # Verificar límite
    if len(request_counts[client_ip]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )

    # Registrar request
    request_counts[client_ip].append(now)

    # Procesar
    return {"prediction": "ok"}
```

---

## 📖 Capítulo 8: Resumen y Próximos Pasos

### ✅ Has Completado el Tomo 2

Ahora sabes:
- ✅ Cómo funcionan contenedores Docker
- ✅ Anatomía de Dockerfiles
- ✅ Usar PyTorch Service
- ✅ Registrar experimentos en MLflow
- ✅ Trabajar con FastAPI
- ✅ Monitorear con Prometheus
- ✅ Entrenar y servir modelos
- ✅ Integrar logging y caching

### 🎯 Siguiente: Tomo 3

En el **Tomo 3: Event-Driven y RAG** aprenderás:
- 🐰 Event-Driven Architecture con RabbitMQ
- 📨 Comunicación asíncrona entre servicios
- 🔍 RAG (Retrieval Augmented Generation)
- 📚 ChromaDB y búsqueda semántica
- 🤖 Construir un chatbot inteligente

### 📝 Checklist de Consolidación

Antes de continuar, verifica que puedes:

- ☐ Construir una imagen Docker
- ☐ Modificar código y ver cambios (hot reload)
- ☐ Hacer requests a la API
- ☐ Ver logs de un servicio
- ☐ Entrenar un modelo y registrarlo en MLflow
- ☐ Comparar experimentos en MLflow UI
- ☐ Ver métricas en Prometheus
- ☐ Guardar y cargar modelos

---

## 📚 Índice de Tomos

- ✅ **Tomo 1: Fundamentos y Setup**
- ✅ **Tomo 2: Docker y Servicios Básicos** ← Estás aquí
- ⏭️ **Tomo 3: Event-Driven y RAG**
- ⏭️ **Tomo 4: Deployment con Ansible**
- ⏭️ **Tomo 5: Kubernetes y Producción**

---

**¡Excelente progreso! 🎉 Listo para el Tomo 3! 🚀**
