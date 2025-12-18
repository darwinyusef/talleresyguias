# 📚 Guía MLOps - Tomo 1: Fundamentos y Setup

> **Nivel:** Principiante
> **Duración estimada:** 2-3 horas
> **Requisitos:** Conocimientos básicos de terminal y Python

---

## 🎯 Objetivos de este Tomo

Al finalizar este tomo podrás:
- ✅ Entender qué es MLOps y por qué es importante
- ✅ Conocer la arquitectura completa del proyecto
- ✅ Instalar todas las herramientas necesarias
- ✅ Configurar tu entorno de desarrollo
- ✅ Ejecutar tu primer servicio

---

## 📖 Capítulo 1: ¿Qué es MLOps?

### 1.1 Definición

**MLOps** = **M**achine **L**earning + Dev**Ops**

Es una práctica que combina:
- 🤖 **Machine Learning**: Crear y entrenar modelos
- 🔧 **DevOps**: Automatización, CI/CD, deployment
- 📊 **Data Engineering**: Gestión de datos

### 1.2 ¿Por qué necesitamos MLOps?

**Problema tradicional:**
```
Científico de datos → Crea modelo en Jupyter
                    → Funciona en laptop
                    → ¿Cómo lo paso a producción? 🤷
                    → ¿Cómo lo monitoreo?
                    → ¿Cómo lo actualizo?
```

**Solución MLOps:**
```
Científico de datos → Crea modelo
                    ↓
        MLOps Pipeline Automatizado
                    ↓
        - Empaquetado en Docker ✅
        - Tests automáticos ✅
        - Deploy a producción ✅
        - Monitoreo continuo ✅
        - Re-entrenamiento automático ✅
```

### 1.3 Componentes del ciclo MLOps

```
┌─────────────────────────────────────────────┐
│         CICLO COMPLETO DE MLOps             │
└─────────────────────────────────────────────┘

1. 📥 DATA
   ↓ Ingesta, validación, versionado

2. 🔬 EXPERIMENTACIÓN
   ↓ Jupyter, notebooks, pruebas

3. 🎯 ENTRENAMIENTO
   ↓ Scripts, pipelines, GPU clusters

4. ✅ VALIDACIÓN
   ↓ Tests, métricas, benchmarks

5. 📦 EMPAQUETADO
   ↓ Docker, contenedores, artifacts

6. 🚀 DEPLOYMENT
   ↓ Kubernetes, servidores, APIs

7. 📊 MONITOREO
   ↓ Métricas, logs, alertas

8. 🔄 FEEDBACK
   └──> Volver a DATA (mejora continua)
```

---

## 📖 Capítulo 2: Arquitectura del Proyecto

### 2.1 Vista General

Nuestro proyecto tiene **11 servicios** trabajando juntos:

```
┌────────────────────────────────────────────────┐
│            ARQUITECTURA MLOps                   │
└────────────────────────────────────────────────┘

CAPA DE APLICACIÓN (Lo que ves):
├── 🔥 PyTorch Service      → Modelos PyTorch
├── 🧠 TensorFlow Service   → Modelos TensorFlow
└── 📚 RAG Service          → Búsqueda semántica

CAPA DE MENSAJERÍA (Comunicación):
└── 🐰 RabbitMQ             → Cola de mensajes

CAPA DE DATOS (Almacenamiento):
├── 🗄️ Redis                → Cache rápido
├── 🐘 PostgreSQL           → Base de datos
└── 🔍 ChromaDB             → Base vectorial

CAPA DE MLOPS (Tracking):
└── 📊 MLflow               → Experimentos

CAPA DE MONITOREO (Observabilidad):
├── 📈 Prometheus           → Métricas
└── 📉 Grafana              → Dashboards
```

### 2.2 ¿Qué hace cada servicio?

#### 🔥 **PyTorch Service** (Puerto 8000)
**¿Qué es?** Servicio de ML usando PyTorch
**¿Para qué sirve?** Ejecutar modelos de Deep Learning
**¿Cuándo usarlo?** Para predicciones, clasificación, NLP
**Ejemplo:** Clasificar imágenes, detectar objetos

#### 🧠 **TensorFlow Service** (Puerto 8001)
**¿Qué es?** Servicio de ML usando TensorFlow
**¿Para qué sirve?** Ejecutar modelos alternativos
**¿Cuándo usarlo?** Si prefieres TensorFlow sobre PyTorch
**Ejemplo:** Predicción de series temporales

#### 📚 **RAG Service** (Puerto 8002)
**¿Qué es?** Retrieval Augmented Generation
**¿Para qué sirve?** Búsqueda semántica + IA generativa
**¿Cuándo usarlo?** Chatbots, Q&A systems, búsqueda inteligente
**Ejemplo:** "Busca información sobre MLOps"

#### 🐰 **RabbitMQ** (Puerto 5672, UI: 15672)
**¿Qué es?** Message Broker (buzón de mensajes)
**¿Para qué sirve?** Comunicación asíncrona entre servicios
**¿Cuándo usarlo?** Para desacoplar servicios
**Ejemplo:** "Cuando termines de entrenar, avísale al deploy"

#### 🗄️ **Redis** (Puerto 6379)
**¿Qué es?** Base de datos en memoria (caché)
**¿Para qué sirve?** Almacenar datos temporales rápidamente
**¿Cuándo usarlo?** Cache, sesiones, colas ligeras
**Ejemplo:** Guardar resultado de predicción por 1 hora

#### 🐘 **PostgreSQL** (Puerto 5432)
**¿Qué es?** Base de datos relacional
**¿Para qué sirve?** Almacenar datos estructurados
**¿Cuándo usarlo?** Metadata de modelos, usuarios, configs
**Ejemplo:** Historial de experimentos de MLflow

#### 📊 **MLflow** (Puerto 5000)
**¿Qué es?** Plataforma de tracking de experimentos ML
**¿Para qué sirve?** Registrar entrenamientos, comparar modelos
**¿Cuándo usarlo?** SIEMPRE en ML
**Ejemplo:** "Este modelo tiene 95% de accuracy"

#### 🔍 **ChromaDB** (Puerto 8100)
**¿Qué es?** Base de datos vectorial
**¿Para qué sirve?** Búsqueda por similitud semántica
**¿Cuándo usarlo?** RAG, recomendaciones, búsqueda
**Ejemplo:** "Encuentra documentos similares a este texto"

#### 📈 **Prometheus** (Puerto 9090)
**¿Qué es?** Sistema de monitoreo y alertas
**¿Para qué sirve?** Recolectar métricas de todos los servicios
**¿Cuándo usarlo?** Monitoreo en producción
**Ejemplo:** "¿Cuántas predicciones por segundo?"

#### 📉 **Grafana** (Puerto 3000)
**¿Qué es?** Plataforma de visualización
**¿Para qué sirve?** Crear dashboards bonitos
**¿Cuándo usarlo?** Para ver métricas visualmente
**Ejemplo:** Gráficas de uso de CPU, latencia, errores

### 2.3 Flujo de Trabajo Típico

```
📱 Usuario hace request
   ↓
🔥 PyTorch Service recibe request
   ↓
🗄️ Busca en Redis si ya tiene el resultado (cache)
   ↓
   ├─ SI existe → Devuelve resultado ✅
   └─ NO existe → Calcula predicción
                  ↓
               Guarda en Redis
                  ↓
               Publica evento en RabbitMQ
                  ↓
               Registra en MLflow
                  ↓
               Envía métricas a Prometheus
                  ↓
               Devuelve resultado ✅
```

---

## 📖 Capítulo 3: Instalación de Herramientas

### 3.1 Checklist de Pre-requisitos

Necesitas instalar:

#### ✅ **Docker Desktop**
**¿Qué es?** Plataforma para ejecutar contenedores
**¿Por qué?** Todo nuestro proyecto corre en Docker
**Versión mínima:** 24.0+

**Instalación:**
```bash
# macOS
brew install --cask docker

# Linux
curl -fsSL https://get.docker.com | sh

# Windows
# Descargar de https://www.docker.com/products/docker-desktop
```

**Verificar:**
```bash
docker --version
# Debe mostrar: Docker version 24.0.0 o superior

docker compose version
# Debe mostrar: Docker Compose version v2.23.0 o superior
```

#### ✅ **Python 3.11+**
**¿Qué es?** Lenguaje de programación
**¿Por qué?** Para ejecutar scripts locales

**Instalación:**
```bash
# macOS
brew install python@3.11

# Linux
sudo apt install python3.11

# Windows
# Descargar de https://www.python.org/downloads/
```

**Verificar:**
```bash
python3 --version
# Debe mostrar: Python 3.11.0 o superior
```

#### ✅ **Git**
**¿Qué es?** Control de versiones
**¿Por qué?** Para clonar y versionar código

**Instalación:**
```bash
# macOS
brew install git

# Linux
sudo apt install git

# Windows
# Descargar de https://git-scm.com/downloads
```

**Verificar:**
```bash
git --version
```

#### ✅ **Make** (Opcional pero recomendado)
**¿Qué es?** Herramienta de automatización
**¿Por qué?** Para usar comandos simplificados

**Instalación:**
```bash
# macOS (ya viene instalado)
xcode-select --install

# Linux
sudo apt install build-essential

# Windows
choco install make
```

**Verificar:**
```bash
make --version
```

#### ✅ **Editor de código**
Recomendados:
- **VSCode** (más popular): https://code.visualstudio.com/
- **PyCharm**: https://www.jetbrains.com/pycharm/
- **Cursor**: https://cursor.sh/

### 3.2 Verificación del Entorno

Ejecuta este script para verificar todo:

```bash
# Guardar como check-requirements.sh
cat << 'EOF' > check-requirements.sh
#!/bin/bash

echo "🔍 Verificando requisitos..."
echo ""

# Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker: $(docker --version)"
else
    echo "❌ Docker NO encontrado"
fi

# Docker Compose
if docker compose version &> /dev/null; then
    echo "✅ Docker Compose: $(docker compose version)"
else
    echo "❌ Docker Compose NO encontrado"
fi

# Python
if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
else
    echo "❌ Python NO encontrado"
fi

# Git
if command -v git &> /dev/null; then
    echo "✅ Git: $(git --version)"
else
    echo "❌ Git NO encontrado"
fi

# Make
if command -v make &> /dev/null; then
    echo "✅ Make: $(make --version | head -1)"
else
    echo "⚠️  Make NO encontrado (opcional)"
fi

echo ""
echo "🎯 Verificación completa!"
EOF

chmod +x check-requirements.sh
./check-requirements.sh
```

---

## 📖 Capítulo 4: Configuración Inicial

### 4.1 Estructura del Proyecto

Primero, familiarízate con la estructura:

```bash
cd mlops-project
ls -la
```

Verás:
```
mlops-project/
├── 📄 README.md              ← Lee esto primero
├── 📄 QUICK_START.md         ← Inicio rápido
├── 📄 .env.example           ← Configuración
├── 📄 Makefile               ← Comandos útiles
├── 🐳 docker-compose.yml     ← Orquestación
├── 🐳 Dockerfile.pytorch     ← Imagen PyTorch
├── 🐳 Dockerfile.tensorflow  ← Imagen TensorFlow
├── 📁 src/                   ← Código Python
├── 📁 scripts/               ← Scripts útiles
├── 📁 config/                ← Configuraciones
├── 📁 ansible/               ← Automatización
├── 📁 k8s/                   ← Kubernetes
└── 📁 tests/                 ← Tests
```

### 4.2 Configurar Variables de Entorno

**¿Qué son las variables de entorno?**
Son configuraciones que cambian según el ambiente (dev, prod).

**Paso 1:** Copiar el template
```bash
cp .env.example .env
```

**Paso 2:** Editar `.env`
```bash
# Puedes usar nano, vim, o tu editor favorito
nano .env
```

**Paso 3:** Configuraciones importantes

```bash
# .env
# ====================================
# CONFIGURACIÓN BÁSICA
# ====================================

# Ambiente (development, staging, production)
ENVIRONMENT=development

# URLs de servicios
RABBITMQ_URL=amqp://admin:admin123@rabbitmq:5672/
REDIS_URL=redis://redis:6379/0
MLFLOW_TRACKING_URI=http://mlflow:5000

# ChromaDB
CHROMA_HOST=chromadb
CHROMA_PORT=8000

# Logging
LOG_LEVEL=INFO

# GPU (cambiar a true si tienes GPU)
ENABLE_GPU=false
```

**🔐 IMPORTANTE - Seguridad:**
- ❌ **NUNCA** subas `.env` a Git
- ✅ Cambia las contraseñas por defecto en producción
- ✅ Usa contraseñas fuertes

### 4.3 Entender el Makefile

El **Makefile** contiene comandos pre-configurados.

**¿Por qué usar Makefile?**
En lugar de escribir:
```bash
docker-compose up -d && docker-compose ps && echo "Servicios iniciados"
```

Solo escribes:
```bash
make up
```

**Ver todos los comandos disponibles:**
```bash
make help
```

Verás algo como:
```
MLOps Platform - Comandos Disponibles:

  make setup          → Setup inicial del proyecto
  make build          → Construir imágenes Docker
  make up             → Iniciar todos los servicios
  make down           → Detener todos los servicios
  make logs           → Ver logs de todos los servicios
  make ps             → Ver estado de servicios
  make test           → Ejecutar tests
  make clean          → Limpiar archivos temporales
  make quickstart     → Setup + Build + Up (todo en uno)
```

---

## 📖 Capítulo 5: Primera Ejecución

### 5.1 Quick Start - La Forma Más Rápida

**Opción A: Con Make (recomendado)**
```bash
# Un solo comando hace todo
make quickstart
```

Esto ejecuta automáticamente:
1. ✅ Crea directorios necesarios
2. ✅ Instala dependencias Python
3. ✅ Construye imágenes Docker
4. ✅ Inicia todos los servicios
5. ✅ Verifica que todo esté corriendo

**Opción B: Paso a paso (para entender)**
```bash
# 1. Setup inicial
make setup

# 2. Construir imágenes Docker
make build

# 3. Iniciar servicios
make up

# 4. Verificar estado
make ps
```

### 5.2 ¿Qué está pasando?

Cuando ejecutas `make up`, Docker:

1. **Lee** `docker-compose.yml`
2. **Crea** redes virtuales
3. **Descarga** imágenes base (si no las tiene)
4. **Construye** nuestras imágenes custom
5. **Inicia** 11 contenedores
6. **Conecta** todo entre sí

**Tiempo estimado:** 5-10 minutos la primera vez

**Verás algo como:**
```
[+] Running 11/11
 ✔ Container mlops-rabbitmq       Started
 ✔ Container mlops-redis          Started
 ✔ Container mlops-postgres       Started
 ✔ Container mlops-mlflow         Started
 ✔ Container mlops-chromadb       Started
 ✔ Container mlops-pytorch        Started
 ✔ Container mlops-tensorflow     Started
 ✔ Container mlops-rag            Started
 ✔ Container mlops-prometheus     Started
 ✔ Container mlops-grafana        Started
```

### 5.3 Verificar que Todo Funciona

**Ver estado de servicios:**
```bash
make ps
```

Debes ver algo como:
```
NAME                  STATUS              PORTS
mlops-pytorch         Up 2 minutes        0.0.0.0:8000->8000/tcp
mlops-tensorflow      Up 2 minutes        0.0.0.0:8001->8001/tcp
mlops-rag             Up 2 minutes        0.0.0.0:8002->8002/tcp
mlops-rabbitmq        Up 2 minutes        0.0.0.0:5672->5672/tcp
mlops-redis           Up 2 minutes        0.0.0.0:6379->6379/tcp
...
```

**✅ STATUS debe decir "Up"** para todos

**Ver logs en tiempo real:**
```bash
make logs
```

Para salir: `Ctrl + C`

### 5.4 Probar los Servicios

#### Test 1: PyTorch Service

**En terminal:**
```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "pytorch-service"
}
```

#### Test 2: TensorFlow Service

```bash
curl http://localhost:8001/health
```

#### Test 3: RAG Service

```bash
curl http://localhost:8002/health
```

#### Test 4: Abrir UIs en Navegador

Abre estas URLs en tu navegador:

1. **MLflow**: http://localhost:5000
   - Debes ver la UI de MLflow
   - Panel de experimentos

2. **Grafana**: http://localhost:3000
   - Usuario: `admin`
   - Password: `admin123`

3. **Prometheus**: http://localhost:9090
   - Dashboard de métricas

4. **RabbitMQ**: http://localhost:15672
   - Usuario: `admin`
   - Password: `admin123`

### 5.5 ¡Felicitaciones! 🎉

Si todos los tests pasaron, tienes una plataforma MLOps funcionando.

---

## 📖 Capítulo 6: Comandos Esenciales

### 6.1 Gestión de Servicios

```bash
# Iniciar servicios
make up

# Detener servicios (mantiene datos)
make down

# Detener y borrar todo (incluye datos)
docker-compose down -v

# Reiniciar servicios
make restart

# Ver estado
make ps

# Ver logs de todos
make logs

# Ver logs de uno específico
docker-compose logs -f pytorch-service
```

### 6.2 Debugging

```bash
# Entrar a un contenedor
docker-compose exec pytorch-service /bin/bash

# Ver logs de errores
docker-compose logs pytorch-service | grep ERROR

# Reiniciar un servicio específico
docker-compose restart pytorch-service

# Ver recursos usados
docker stats
```

### 6.3 Limpieza

```bash
# Limpiar archivos temporales
make clean

# Limpiar todo Docker
make clean-docker

# Liberar espacio en disco
docker system prune -a
```

---

## 📖 Capítulo 7: Troubleshooting

### Problema 1: "Puerto ya en uso"

**Error:**
```
Error: bind: address already in use
```

**Solución:**
```bash
# Ver qué está usando el puerto
lsof -i :8000

# Matar el proceso
kill -9 <PID>

# O cambiar puerto en docker-compose.yml
```

### Problema 2: "Docker no inicia"

**Error:**
```
Cannot connect to Docker daemon
```

**Solución:**
```bash
# Iniciar Docker Desktop
open -a Docker

# O en Linux
sudo systemctl start docker
```

### Problema 3: "No hay espacio en disco"

**Error:**
```
no space left on device
```

**Solución:**
```bash
# Ver uso de Docker
docker system df

# Limpiar
docker system prune -a
```

### Problema 4: "Servicios no healthy"

**Solución:**
```bash
# Ver logs específicos
make logs-pytorch

# Reiniciar servicio
docker-compose restart pytorch-service

# Si persiste, rebuild
make build
make up
```

---

## 📖 Capítulo 8: Próximos Pasos

### ✅ Has Completado el Tomo 1

Ahora sabes:
- ✅ Qué es MLOps y por qué es importante
- ✅ La arquitectura de 11 servicios
- ✅ Cómo instalar todas las herramientas
- ✅ Cómo iniciar y verificar servicios
- ✅ Comandos esenciales de gestión
- ✅ Cómo resolver problemas comunes

### 🎯 Siguiente: Tomo 2

En el **Tomo 2: Docker y Servicios Básicos** aprenderás:
- 🐳 Cómo funcionan los contenedores Docker
- 🔥 Usar PyTorch Service en detalle
- 📊 Registrar experimentos en MLflow
- 🧪 Hacer predicciones reales
- 🔍 Entender los logs y métricas

### 📝 Ejercicio de Consolidación

Antes de continuar, asegúrate de poder hacer esto sin ayuda:

1. ☐ Iniciar todos los servicios con un comando
2. ☐ Verificar que los 11 servicios estén "Up"
3. ☐ Abrir Grafana en el navegador
4. ☐ Hacer un request a PyTorch Service
5. ☐ Ver los logs de un servicio
6. ☐ Detener todos los servicios

### 🎓 Recursos Adicionales

- 📖 [Docker Documentation](https://docs.docker.com/)
- 📖 [MLflow Documentation](https://mlflow.org/docs/)
- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 📚 Índice de Tomos

- ✅ **Tomo 1: Fundamentos y Setup** ← Estás aquí
- ⏭️ **Tomo 2: Docker y Servicios Básicos**
- ⏭️ **Tomo 3: Event-Driven y RAG**
- ⏭️ **Tomo 4: Deployment con Ansible**
- ⏭️ **Tomo 5: Kubernetes y Producción**

---

**¡Listo para el Tomo 2! 🚀**
