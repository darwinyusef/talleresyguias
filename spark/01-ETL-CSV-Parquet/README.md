# 📊 Módulo 01: ETL - de CSV a Parquet con Spark

En este módulo aprenderemos por qué Parquet es el estándar de oro en Big Data y cómo convertir datos eficientemente usando Apache Spark.

## 🎯 Objetivos de Aprendizaje

- Entender las ventajas del formato Parquet vs CSV
- Implementar un pipeline ETL completo con PySpark
- Aplicar transformaciones y limpieza de datos
- Manejar particionamiento de datos para optimizar consultas
- Comprender el concepto de Shuffle en Spark

## 📚 ¿Por qué Parquet?

Parquet es un formato de almacenamiento columnar optimizado para Big Data:

| Característica | CSV | Parquet |
|---------------|-----|---------|
| **Formato** | Basado en filas | Columnar |
| **Compresión** | Mínima | 80-90% de reducción |
| **Lectura selectiva** | Lee todo el archivo | Solo columnas necesarias |
| **Esquema** | Sin tipo de datos | Esquema embebido |
| **Performance en Analytics** | Lenta | Muy rápida |

### Ventajas Principales:
- **Formato Columnar:** Solo lee las columnas necesarias, ahorrando I/O masivamente
- **Compresión Eficiente:** Reduce drásticamente el tamaño en disco (típicamente 80-90%)
- **Esquema Embebido:** Guarda metadatos y tipos de datos automáticamente
- **Compatible:** Funciona con todo el ecosistema Big Data (Spark, Hive, Presto, etc.)
- **Predicate Pushdown:** Filtra datos antes de leerlos completamente

## 🛠️ Scripts Incluidos

### 1. `etl_csv_to_parquet.py` - ETL Completo Producción

Script completo y robusto para ETL en ambientes reales:

**Funcionalidades:**
- ✅ Lectura de CSV con manejo de errores
- ✅ Transformaciones de limpieza de datos
- ✅ Normalización de texto
- ✅ Manejo de valores nulos
- ✅ Creación de columnas derivadas
- ✅ Escritura optimizada en Parquet
- ✅ Particionamiento inteligente
- ✅ Comparación de tamaños de archivo
- ✅ Validación de datos

**Ejecución:**
```bash
# Primero genera los datos de prueba
python scripts/generate_data.py

# Ejecuta el ETL
python 01-ETL-CSV-Parquet/etl_csv_to_parquet.py
```

**Configuración Personalizable:**
```python
INPUT_PATH = "data/lead_conversions.csv"
OUTPUT_PATH = "data/processed_leads.parquet"
PARTITION_COLUMN = "salary_range"  # Opcional
```

### 2. `big_data_demo.py` - Demo de Conceptos Avanzados

Demuestra conceptos críticos de Big Data a escala:

**Conceptos Demostrados:**
1. **Generación Masiva:** Crea 10 millones de filas in-memory
2. **Shuffle Operations:** Muestra cómo las agregaciones mueven datos entre nodos
3. **Partitioning:** Compara performance entre datos planos vs particionados
4. **Partition Pruning:** Optimización automática de lectura

**Ejecución:**
```bash
python 01-ETL-CSV-Parquet/big_data_demo.py
```

**Salida Esperada:**
```
🚀 Generando 10 millones de filas...
📊 Estado inicial de particiones: 8
⏱️ Tiempo procesado (sin particionar): 12.34s
💾 Guardando datos particionados...
🔍 Demostrando Partition Pruning...
⏱️ Tiempo de conteo con filtro de partición: 0.0123s
```

## 🔑 Conceptos Clave

### Particionamiento Físico

El particionamiento divide los datos en subdirectorios en disco:

```
data/partitioned_data.parquet/
├── category=0/
│   └── part-00000.parquet
├── category=1/
│   └── part-00001.parquet
└── category=2/
    └── part-00002.parquet
```

**Ventaja:** Cuando filtras por `category=1`, Spark solo lee ese directorio.

### Shuffle en Spark

**Shuffle** es el movimiento de datos entre particiones/nodos:

```python
# Esto causa un shuffle (datos se reorganizan por 'category')
df.groupBy("category").agg(sum("value"))
```

**Cuándo ocurre:**
- `groupBy()`, `join()`, `distinct()`, `repartition()`

**Costo:**
- I/O de red
- Serialización/Deserialización
- Escritura temporal en disco

## 📖 Ejemplo Paso a Paso

### 1. Crear Sesión de Spark
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ETL-CSV-Parquet") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()
```

### 2. Leer CSV
```python
df = spark.read.csv(
    "data/lead_conversions.csv",
    header=True,
    inferSchema=True,
    nullValue="NA"
)
```

### 3. Transformaciones
```python
from pyspark.sql.functions import col, when, trim

# Limpiar datos
df_clean = df.filter(col("id").isNotNull()) \
    .withColumn("age", col("age").cast("integer")) \
    .fillna({"salary": 0})

# Crear columna derivada
df_clean = df_clean.withColumn(
    "salary_range",
    when(col("salary") < 30000, "Low")
    .when(col("salary") < 70000, "Medium")
    .otherwise("High")
)
```

### 4. Guardar como Parquet
```python
# Sin particiones
df_clean.write.mode("overwrite") \
    .option("compression", "snappy") \
    .parquet("data/output.parquet")

# Con particiones (recomendado para datos grandes)
df_clean.write.mode("overwrite") \
    .partitionBy("salary_range") \
    .parquet("data/output_partitioned.parquet")
```

### 5. Leer Parquet
```python
# Lectura simple
df_parquet = spark.read.parquet("data/output.parquet")

# Lectura con filtro (aprovecha partition pruning)
df_filtered = spark.read.parquet("data/output_partitioned.parquet") \
    .filter(col("salary_range") == "High")
```

## 💡 Mejores Prácticas

1. **Usa Compresión Snappy:** Balance entre velocidad y ratio de compresión
   ```python
   .option("compression", "snappy")
   ```

2. **Particiona Inteligentemente:**
   - Usa columnas con cardinalidad media (10-10,000 valores únicos)
   - Evita sobre-particionamiento (archivos muy pequeños)
   - Columnas típicas: fecha, región, categoría

3. **Habilita Adaptive Query Execution:**
   ```python
   .config("spark.sql.adaptive.enabled", "true")
   ```

4. **Evita Particiones Muy Pequeñas:**
   - Archivos < 100MB son ineficientes
   - Usa `coalesce()` para reducir particiones si es necesario

5. **Infiere Schema con Cuidado:**
   - `inferSchema=True` lee el archivo dos veces
   - En producción, define el schema explícitamente

## 🚀 Próximos Pasos

Una vez que domines este módulo, continúa con:
- **[Módulo 02-03: Machine Learning](../02-03-ML/README.md)** - Entrena modelos sobre datos Parquet
- **[Módulo 06: S3/MinIO](../06-Storage-S3-MinIO/README.md)** - Almacena Parquet en object storage

## 📚 Referencias

- [Documentación oficial de Parquet](https://parquet.apache.org/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Best Practices for Writing Parquet](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html)

