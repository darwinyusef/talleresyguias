# Proyecto 3: API con FastAPI (Python)

## Objetivo
Crear y desplegar una API REST con FastAPI usando Docker.

## Prerrequisitos
- Proyectos anteriores completados
- Conocimientos básicos de Python
- Conocimientos básicos de APIs REST

---

## Paso 1: Estructura del Proyecto

```bash
mkdir -p ~/curso-docker/proyectos/03-fastapi
cd ~/curso-docker/proyectos/03-fastapi
mkdir -p app/{api,models,schemas,database}
```

**Estructura esperada:**
```
03-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   └── database/
│       ├── __init__.py
│       └── connection.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

## Paso 2: Crear requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
```

## Paso 3: Crear la Aplicación FastAPI

**app/main.py** (tú lo crearás, este es un ejemplo):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mi API con FastAPI",
    description="API REST con Docker",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "¡Bienvenido a mi API!",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Importar rutas adicionales
# from app.api import routes
# app.include_router(routes.router)
```

## Paso 4: Crear Dockerfile

```dockerfile
# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /code

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar código de la aplicación
COPY ./app /code/app

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Explicación:**
- `python:3.11-slim` - Imagen Python optimizada
- `WORKDIR /code` - Directorio de trabajo
- `pip install --no-cache-dir` - Instalar sin caché para imagen más pequeña
- `uvicorn` - Servidor ASGI para FastAPI
- `--host 0.0.0.0` - Escuchar en todas las interfaces
- `--port 8000` - Puerto de la aplicación

## Paso 5: Crear .dockerignore

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
.env
.git/
.gitignore
README.md
.DS_Store
*.log
.pytest_cache/
.coverage
htmlcov/
```

## Paso 6: Construir y Ejecutar

```bash
# Construir imagen
docker build -t fastapi-app:v1 .

# Ejecutar contenedor
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  fastapi-app:v1

# Verificar
docker ps
curl http://localhost:8000
```

## Paso 7: Probar la API

**En navegador:**
```
http://localhost:8000
http://localhost:8000/docs  # Documentación Swagger automática
http://localhost:8000/redoc # Documentación ReDoc
```

**Con curl:**
```bash
curl http://localhost:8000
curl http://localhost:8000/health
```

---

## Modo Desarrollo con Hot Reload

**Dockerfile.dev:**
```dockerfile
FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# No copiar código, se monta con volume

EXPOSE 8000

# Modo reload para desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Ejecutar en modo desarrollo:**
```bash
docker build -f Dockerfile.dev -t fastapi-dev .
docker run -d \
  --name fastapi-dev-container \
  -p 8000:8000 \
  -v $(pwd)/app:/code/app \
  fastapi-dev
```

**Ventaja:** Los cambios en código se reflejan automáticamente.

---

## Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    container_name: fastapi-api
    restart: unless-stopped
    environment:
      - ENV=production
    profiles:
      - production

  api-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./app:/code/app
    container_name: fastapi-dev
    environment:
      - ENV=development
    profiles:
      - development
```

**Comandos:**
```bash
# Desarrollo
docker compose --profile development up -d

# Producción
docker compose --profile production up -d

# Ver logs
docker compose logs -f

# Detener
docker compose down
```

---

## Agregar Endpoints CRUD

**app/api/routes.py** (ejemplo que debes adaptar):
```python
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(
    prefix="/api/v1",
    tags=["items"]
)

# Base de datos simulada (en memoria)
items_db = {}
item_id_counter = 1

@router.get("/items")
async def get_items():
    return {"items": list(items_db.values())}

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return items_db[item_id]

@router.post("/items")
async def create_item(name: str, description: str):
    global item_id_counter
    item = {
        "id": item_id_counter,
        "name": name,
        "description": description
    }
    items_db[item_id_counter] = item
    item_id_counter += 1
    return item

@router.put("/items/{item_id}")
async def update_item(item_id: int, name: str, description: str):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    items_db[item_id]["name"] = name
    items_db[item_id]["description"] = description
    return items_db[item_id]

@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    del items_db[item_id]
    return {"message": "Item eliminado"}
```

**Registrar en main.py:**
```python
from app.api import routes

app.include_router(routes.router)
```

---

## Variables de Entorno

**Crear .env:**
```env
ENV=production
API_KEY=tu-api-key-secreta
DATABASE_URL=postgresql://user:pass@db:5432/dbname
SECRET_KEY=tu-secret-key-muy-segura
```

**app/config.py:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "development"
    api_key: str
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

**Actualizar requirements.txt:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-dotenv==1.0.0
```

**Usar en Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app
COPY .env /code/.env

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**O pasar variables en docker run:**
```bash
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  -e API_KEY=mi-clave \
  -e DATABASE_URL=postgresql://... \
  fastapi-app:v1
```

**Con Docker Compose:**
```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - API_KEY=${API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env
```

---

## Integración con Base de Datos PostgreSQL

**Actualizar requirements.txt:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
```

**docker-compose.yml con PostgreSQL:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: password
      POSTGRES_DB: midb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U usuario"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    container_name: fastapi-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://usuario:password@db:5432/midb
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./app:/code/app

volumes:
  postgres_data:
```

**Comandos:**
```bash
docker compose up -d
docker compose logs -f api
docker compose exec db psql -U usuario -d midb
```

---

## Health Checks

**Agregar health check al Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Nota:** Necesitas instalar curl en la imagen:
```dockerfile
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

**Verificar health:**
```bash
docker inspect --format='{{.State.Health.Status}}' fastapi-container
```

---

## Multi-Stage Build para Producción

```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /code

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade --user -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim

WORKDIR /code

# Copiar dependencias instaladas
COPY --from=builder /root/.local /root/.local

# Asegurar que los scripts estén en PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar código
COPY ./app /code/app

# Usuario no-root
RUN useradd -m -u 1000 apiuser && chown -R apiuser:apiuser /code
USER apiuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Testing en Docker

**Agregar a requirements.txt:**
```txt
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

**tests/test_main.py:**
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

**Dockerfile.test:**
```dockerfile
FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests

CMD ["pytest", "-v"]
```

**Ejecutar tests:**
```bash
docker build -f Dockerfile.test -t fastapi-test .
docker run --rm fastapi-test
```

---

## Ejercicios Prácticos

### Ejercicio 1: CRUD Completo
Crea una API con:
- GET /users - Listar usuarios
- GET /users/{id} - Obtener usuario
- POST /users - Crear usuario
- PUT /users/{id} - Actualizar usuario
- DELETE /users/{id} - Eliminar usuario

### Ejercicio 2: Autenticación JWT
Implementa:
- POST /auth/register
- POST /auth/login
- GET /auth/me (protegido)

### Ejercicio 3: Validación con Pydantic
Usa schemas de Pydantic para validar:
- Email válido
- Password con requisitos mínimos
- Campos requeridos vs opcionales

### Ejercicio 4: Paginación
Implementa paginación en listados:
- GET /items?page=1&size=10
- Retornar total de items y páginas

---

## Logging y Monitoring

**app/main.py con logging:**
```python
import logging
from fastapi import FastAPI, Request
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {process_time:.2f}s "
        f"with status {response.status_code}"
    )

    return response
```

**Ver logs:**
```bash
docker logs -f fastapi-container
docker compose logs -f api
```

---

## Troubleshooting

### API no responde
```bash
# Verificar que contenedor está corriendo
docker ps

# Ver logs
docker logs fastapi-container

# Verificar puerto
netstat -tulpn | grep 8000
lsof -i :8000
```

### Errores de importación de módulos
```bash
# Verificar estructura en contenedor
docker exec fastapi-container ls -la /code/app

# Verificar __init__.py existen
docker exec fastapi-container find /code/app -name "__init__.py"
```

### Base de datos no conecta
```bash
# Verificar que db está corriendo
docker compose ps

# Probar conexión desde api
docker compose exec api ping db

# Ver logs de db
docker compose logs db
```

### Cambios no se reflejan
```bash
# Reconstruir imagen
docker compose build

# Reiniciar servicios
docker compose restart

# O forzar recreación
docker compose up -d --force-recreate
```

---

## Resumen de Comandos

```bash
# Build y run simple
docker build -t fastapi-app:v1 .
docker run -d --name fastapi-container -p 8000:8000 fastapi-app:v1

# Desarrollo con hot reload
docker run -d --name fastapi-dev -p 8000:8000 \
  -v $(pwd)/app:/code/app fastapi-dev

# Con Docker Compose
docker compose up -d
docker compose logs -f
docker compose down

# Testing
docker build -f Dockerfile.test -t fastapi-test .
docker run --rm fastapi-test

# Acceder a contenedor
docker exec -it fastapi-container bash

# Ver logs
docker logs -f fastapi-container
```

---

## Checklist del Proyecto

- [ ] Crear estructura de directorios
- [ ] Crear requirements.txt
- [ ] Desarrollar aplicación FastAPI
- [ ] Crear endpoints básicos (/, /health)
- [ ] Crear Dockerfile
- [ ] Crear .dockerignore
- [ ] Construir imagen
- [ ] Ejecutar contenedor
- [ ] Probar en navegador (localhost:8000)
- [ ] Verificar Swagger docs (/docs)
- [ ] Crear docker-compose.yml
- [ ] Agregar variables de entorno
- [ ] Implementar CRUD endpoints
- [ ] Escribir tests

---

## Siguiente Paso

Continúa con:
**[Proyecto 4: Frontend con React](./04-react-frontend.md)**
