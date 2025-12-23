# ⚡ Taller de Apache Spark: De Cero a MLOps + Streaming

Bienvenidos a este taller integral de **Apache Spark**. Aprenderás desde los conceptos básicos hasta arquitecturas de producción modernas con Machine Learning, Streaming en tiempo real, y deployment con Docker/Kubernetes.

## 🚀 ¿Qué es Apache Spark?

**Apache Spark** es un motor de procesamiento de datos distribuido unificado y de código abierto, diseñado para velocidad y escala. Procesa datos **100x más rápido** que Hadoop MapReduce gracias a su procesamiento en memoria.

### 💡 ¿Para qué sirve?

| Caso de Uso | Tecnología Spark | Aplicación Real |
|-------------|------------------|-----------------|
| **ETL a Escala** | Spark Core + SQL | Procesar petabytes de logs diarios |
| **Machine Learning** | MLlib | Modelos de recomendación, fraud detection |
| **Streaming en Tiempo Real** | Structured Streaming | Alertas IoT, trading algorithms |
| **Analytics Interactivo** | Spark SQL | Consultas sobre Data Lakes |
| **Procesamiento de Grafos** | GraphX | Redes sociales, detección de comunidades |

### 🎯 ¿Por qué aprender Spark en 2024?

- ✅ **Estándar de facto** para Big Data en empresas Fortune 500
- ✅ **Unifica batch y streaming** (misma API para ambos)
- ✅ **Ecosistema rico**: Integración nativa con AWS, Azure, GCP, Databricks
- ✅ **Salario promedio**: $130K+ para Spark Engineers
- ✅ **Open Source**: Sin vendor lock-in

---

## 🛠️ Estructura del Taller

El taller está diseñado como un **journey progresivo** desde fundamentos hasta arquitecturas de producción:

### 📚 Fundamentos (Batch Processing)

1.  **[01-ETL-CSV-Parquet](./01-ETL-CSV-Parquet/README.md)**
    🎓 **Nivel**: Principiante
    📊 Optimización de almacenamiento con formato columnar Parquet
    🔑 **Conceptos**: DataFrames, transformaciones, particionamiento

2.  **[02-03-ML](./02-03-ML/README.md)**
    🎓 **Nivel**: Intermedio
    🤖 Machine Learning distribuido con MLlib + MLflow
    🔑 **Conceptos**: Pipelines ML, Feature Engineering, Model Tracking
    📁 **Incluye**:
    - `lead_scoring.py` - Clasificación supervisada (GBT, Random Forest, Logistic Regression)
    - `customer_segmentation.py` - Clustering no supervisado (K-Means, Elbow Method)

### 🌐 Integración y Serving

3.  **[04-FastAPI-Serving](./04-FastAPI-Serving/README.md)**
    🎓 **Nivel**: Intermedio
    🚀 API REST para servir predicciones de modelos Spark
    🔑 **Conceptos**: ML Serving, caching, batch predictions
    📁 **Features**:
    - Lectura de Parquet generado por Spark
    - Endpoints de predicción batch y realtime
    - Health checks y métricas

### ⚡ Procesamiento en Tiempo Real (NUEVO)

4.  **[08-Spark-Streaming](./08-Spark-Streaming/README.md)** ⭐ **DESTACADO**
    🎓 **Nivel**: Avanzado
    📡 Structured Streaming para procesamiento en tiempo real
    🔑 **Conceptos**: Windowing, watermarks, Kafka integration, streaming ML
    📁 **Scripts incluidos**:
    - `streaming_ml_scoring.py` - **ML scoring en tiempo real**
    - `kafka_producer.py` - Generador de eventos de leads
    - `streaming_word_count.py` - Hello World de streaming
    - `streaming_aggregations.py` - Ventanas temporales y agregaciones

### 🏗️ Infraestructura y Orquestación

5.  **[05-Airflow](./05-Airflow/README.md)**
    🎓 **Nivel**: Intermedio
    🗓️ Orquestación de pipelines Spark con Apache Airflow
    🔑 **Conceptos**: DAGs, scheduling, dependency management

6.  **[06-Storage-S3-MinIO](./06-Storage-S3-MinIO/README.md)**
    🎓 **Nivel**: Intermedio
    ☁️ Data Lake con S3-compatible storage
    🔑 **Conceptos**: Bronze/Silver/Gold architecture, incremental loads
    📁 **Incluye**: `spark_s3_integration.py` con ejemplos completos

7.  **[07-Docker-K8s](./07-Docker-K8s/README.md)**
    🎓 **Nivel**: Avanzado
    🐳 Deployment en producción con Kubernetes
    🔑 **Conceptos**: Containerización, Spark Operator, auto-scaling

---

## 🏁 Inicio Rápido (Quick Start)

### Opción 1: Setup Local (Recomendado para aprender)

#### Requisitos Previos
- **Python 3.9+** (verificar: `python --version`)
- **Java 11+** (requerido para Spark runtime: `java -version`)
- **Docker Desktop** (opcional, para infraestructura)

#### Pasos:

```bash
# 1. Clonar o navegar al directorio del taller
cd spark/

# 2. Instalar dependencias Python
pip install pyspark==3.4.0 mlflow fastapi uvicorn pandas pyarrow

# Para streaming (opcional):
pip install kafka-python

# 3. Generar datos de ejemplo
python scripts/generate_data.py

# 4. Ejecutar tu primer script de Spark
python 01-ETL-CSV-Parquet/etl_csv_to_parquet.py

# 5. Ver los resultados
ls -lh data/processed_leads.parquet
```

#### Verificar Instalación:

```bash
# Test Spark
python -c "from pyspark.sql import SparkSession; print('Spark OK')"

# Test MLflow
mlflow --version
```

### Opción 2: Infraestructura Completa con Docker

Para acceder a **todo** el ecosistema (MinIO, PostgreSQL, MLflow, Airflow):

```bash
# Levantar servicios
docker-compose up -d

# Verificar que estén corriendo
docker ps

# Acceder a UIs:
# - MLflow: http://localhost:5000
# - MinIO Console: http://localhost:9001 (user/pass: minioadmin/minioadmin)
# - Airflow: http://localhost:8081
# - Spark Master UI: http://localhost:8080
```

**Nota**: Docker Compose puede requerir recursos significativos. Para aprendizaje inicial, usa Opción 1.

---

## 🎓 Rutas de Aprendizaje Recomendadas

### 🟢 Para Principiantes en Spark

**Objetivo**: Entender fundamentos de procesamiento distribuido

```
Día 1-2: Módulo 01 (ETL CSV→Parquet)
  ↓
Día 3-4: Módulo 02-03 (Machine Learning básico)
  ↓
Día 5: Módulo 04 (FastAPI Serving)
```

**Habilidades obtenidas**: DataFrames, transformaciones, ML pipelines, serving

### 🟡 Para Data Engineers

**Objetivo**: Arquitecturas de producción end-to-end

```
Módulo 01 → Módulo 06 (S3/MinIO Data Lake)
  ↓
Módulo 08 (Streaming) ← CRÍTICO
  ↓
Módulo 05 (Airflow para orquestación)
  ↓
Módulo 07 (Deployment K8s)
```

**Habilidades obtenidas**: Data Lakes, streaming pipelines, orquestación, deployment

### 🔴 Para ML Engineers

**Objetivo**: MLOps y serving de modelos a escala

```
Módulo 01 → Módulo 02-03 (ML + MLflow)
  ↓
Módulo 04 (FastAPI Serving)
  ↓
Módulo 08 (Streaming ML - scoring en tiempo real)
  ↓
Módulo 05 (Re-training con Airflow)
```

**Habilidades obtenidas**: Feature engineering distribuido, model tracking, serving, online learning

---

## 🏗️ Arquitecturas de Referencia

### Arquitectura 1: Batch ML Pipeline (Básica)

```
Raw Data (CSV)
    ↓
[Spark ETL] → Parquet (Data Lake)
    ↓
[Spark MLlib] → Train Model
    ↓
[MLflow] → Model Registry
    ↓
[FastAPI] → Serving Layer
```

**Módulos**: 01 → 02-03 → 04

### Arquitectura 2: Real-time ML Scoring (Avanzada)

```
Events (Kafka)
    ↓
[Spark Streaming] → Parse & Enrich
    ↓
[ML Model (MLflow)] → Real-time Scoring
    ↓
Hot Leads → [Kafka] → CRM Integration
All Predictions → [S3/MinIO] → Analytics
```

**Módulos**: 02-03 → 06 → 08 ⭐

### Arquitectura 3: Medallion Architecture (Producción)

```
Sources → [Bronze Layer (Raw)] → S3/MinIO
              ↓
         [Spark ETL]
              ↓
         [Silver Layer (Cleaned)] → S3/MinIO
              ↓
         [Spark Aggregations]
              ↓
         [Gold Layer (Analytics)] → S3/MinIO
              ↓
         [FastAPI / BI Tools]
```

**Módulos**: 01 → 06 → 04

### Arquitectura 4: Complete MLOps Platform

```
                    ┌─ Batch Jobs (Airflow)
                    │
Data Sources → [Kafka] → Spark Streaming
                    │         ↓
                    │    Feature Store (S3)
                    │         ↓
                    └→ ML Training (Spark MLlib)
                              ↓
                         MLflow Registry
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
            Batch Inference      Real-time API
            (Spark Batch)         (FastAPI)
                    ↓                   ↓
                Application / Dashboard
```

**Módulos**: TODOS (Proyecto final)

---

## 📦 Datasets Incluidos

Este taller incluye datasets sintéticos realistas:

1. **`lead_conversions.csv`** (1000 filas)
   - Leads de CRM con características demográficas
   - Features: age, salary, web_visits, last_action
   - Target: converted (0/1)
   - Uso: Módulos 01, 02-03, 04, 08

2. **Eventos de streaming** (generados en tiempo real)
   - Producidos por `kafka_producer.py`
   - Simula eventos de leads con timestamps reales
   - Uso: Módulo 08

---

## 💡 Mejores Prácticas del Taller

### ✅ DO's (Haz esto)

- ✅ **Ejecuta cada script** - No solo leas, ejecuta el código
- ✅ **Experimenta** - Modifica parámetros, rompe cosas, aprende
- ✅ **Lee los comentarios** - Cada script está documentado
- ✅ **Revisa los logs** - Entiende qué hace Spark internamente
- ✅ **Usa Spark UI** - http://localhost:4040 cuando ejecutes scripts

### ❌ DON'Ts (Evita esto)

- ❌ No saltarte módulos - son progresivos
- ❌ No copiar/pegar sin entender
- ❌ No usar `collect()` en producción con datos grandes
- ❌ No hardcodear credentials en código

---

## 🚀 Próximos Pasos Después del Taller

Una vez completado el taller, continúa tu aprendizaje con:

1. **Databricks Academy** (gratis) - Certificación Apache Spark
2. **Spark: The Definitive Guide** (libro) - O'Reilly
3. **Proyecto Real**: Implementa un pipeline end-to-end con tus propios datos
4. **Contribuye a Open Source**: Apache Spark o proyectos relacionados
5. **Especialízate**:
   - Delta Lake para ACID en Data Lakes
   - Apache Iceberg / Apache Hudi
   - Databricks / AWS EMR / GCP Dataproc
   - Ray para distributed ML más avanzado

---

## 🤝 Contribuciones y Feedback

Este taller es de código abierto y está en constante mejora:

- 🐛 **Issues**: Reporta bugs o mejoras
- 💡 **Ideas**: Propón nuevos módulos
- 📝 **PRs**: Contribuye con código o documentación

---

## 📚 Recursos Adicionales

- [Documentación Oficial Spark](https://spark.apache.org/docs/latest/)
- [Spark By Examples](https://sparkbyexamples.com/)
- [Awesome Spark](https://github.com/awesome-spark/awesome-spark)
- [Stack Overflow - Tag: apache-spark](https://stackoverflow.com/questions/tagged/apache-spark)

---

## 📄 Licencia

Este taller es de código abierto y uso educativo.

---

**¡Comencemos! 👉 [Módulo 01: ETL CSV a Parquet](./01-ETL-CSV-Parquet/README.md)**

