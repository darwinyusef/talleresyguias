"""
ETL: Convertir CSV a Parquet con Spark
======================================
Este script demuestra el proceso completo de ETL usando Apache Spark:
1. Lectura de datos CSV
2. Transformaciones y limpieza
3. Escritura en formato Parquet particionado

Ventajas de Parquet:
- Formato columnar: Solo lee las columnas necesarias
- Compresión eficiente: Reduce el tamaño en disco ~80%
- Esquema embebido: Metadatos incluidos
- Compatible con todo el ecosistema Big Data
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, trim, upper, year, month
from pyspark.sql.types import DoubleType
import os

def create_spark_session():
    """Crea una sesión de Spark con configuración optimizada"""
    return SparkSession.builder \
        .appName("ETL-CSV-to-Parquet") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def read_csv_data(spark, input_path):
    """Lee datos CSV con inferencia de esquema"""
    print(f"📖 Leyendo datos desde: {input_path}")

    df = spark.read.csv(
        input_path,
        header=True,
        inferSchema=True,
        nullValue="NA",
        nanValue="NaN"
    )

    print(f"✅ Datos cargados: {df.count()} filas, {len(df.columns)} columnas")
    print("\n📊 Esquema de datos:")
    df.printSchema()

    return df

def clean_and_transform(df):
    """Aplica transformaciones de limpieza y enriquecimiento"""
    print("\n🔧 Aplicando transformaciones...")

    # 1. Eliminar filas con ID nulo (clave primaria)
    df_clean = df.filter(col("id").isNotNull())

    # 2. Normalizar columnas de texto (si existen)
    text_columns = [field.name for field in df.schema.fields
                   if str(field.dataType) == "StringType"]

    for col_name in text_columns:
        df_clean = df_clean.withColumn(
            col_name,
            trim(col(col_name))
        )

    # 3. Manejar valores nulos en columnas numéricas (rellenar con 0 o media)
    numeric_columns = [field.name for field in df.schema.fields
                      if str(field.dataType) in ["IntegerType", "DoubleType", "LongType"]]

    for col_name in numeric_columns:
        if col_name != "id":  # No modificar ID
            df_clean = df_clean.fillna({col_name: 0})

    # 4. Crear columna derivada (ejemplo: categorización)
    # Si existe columna 'salary', categorizar en rangos
    if "salary" in df.columns:
        df_clean = df_clean.withColumn(
            "salary_range",
            when(col("salary") < 30000, "Low")
            .when((col("salary") >= 30000) & (col("salary") < 70000), "Medium")
            .when(col("salary") >= 70000, "High")
            .otherwise("Unknown")
        )

    # 5. Agregar particiones temporales si hay timestamp
    # (útil para particionar los datos)

    print(f"✅ Transformaciones completadas")
    print(f"   Filas después de limpieza: {df_clean.count()}")

    return df_clean

def write_to_parquet(df, output_path, partition_by=None):
    """Escribe datos en formato Parquet con particionamiento opcional"""
    print(f"\n💾 Guardando datos en: {output_path}")

    writer = df.write.mode("overwrite") \
        .option("compression", "snappy")  # Compresión eficiente

    if partition_by:
        print(f"   Particionando por: {partition_by}")
        writer = writer.partitionBy(partition_by)

    writer.parquet(output_path)

    print("✅ Datos guardados exitosamente en Parquet")

def compare_file_sizes(input_path, output_path):
    """Compara tamaños de archivos CSV vs Parquet"""
    try:
        # Obtener tamaño del CSV
        csv_size = os.path.getsize(input_path) if os.path.isfile(input_path) else 0

        # Obtener tamaño del Parquet (suma de todos los archivos)
        parquet_size = 0
        if os.path.exists(output_path):
            for root, dirs, files in os.walk(output_path):
                for file in files:
                    if file.endswith('.parquet'):
                        parquet_size += os.path.getsize(os.path.join(root, file))

        if csv_size > 0 and parquet_size > 0:
            reduction = ((csv_size - parquet_size) / csv_size) * 100
            print(f"\n📊 Comparación de tamaños:")
            print(f"   CSV: {csv_size / 1024:.2f} KB")
            print(f"   Parquet: {parquet_size / 1024:.2f} KB")
            print(f"   Reducción: {reduction:.2f}%")
    except Exception as e:
        print(f"⚠️  No se pudo comparar tamaños: {e}")

def main():
    """Función principal del ETL"""
    # Configuración
    INPUT_PATH = "data/lead_conversions.csv"
    OUTPUT_PATH = "data/processed_leads.parquet"
    PARTITION_COLUMN = None  # Cambiar a "salary_range" si quieres particionar

    # Crear sesión de Spark
    spark = create_spark_session()

    try:
        # Paso 1: Leer datos
        df = read_csv_data(spark, INPUT_PATH)

        # Paso 2: Mostrar muestra de datos
        print("\n🔍 Muestra de datos originales:")
        df.show(5, truncate=False)

        # Paso 3: Transformar y limpiar
        df_transformed = clean_and_transform(df)

        # Paso 4: Mostrar muestra de datos transformados
        print("\n🔍 Muestra de datos transformados:")
        df_transformed.show(5, truncate=False)

        # Paso 5: Guardar como Parquet
        write_to_parquet(df_transformed, OUTPUT_PATH, PARTITION_COLUMN)

        # Paso 6: Verificar lectura de Parquet
        print("\n🔄 Verificando lectura de Parquet...")
        df_parquet = spark.read.parquet(OUTPUT_PATH)
        print(f"✅ Lectura exitosa: {df_parquet.count()} filas")

        # Paso 7: Comparar tamaños
        compare_file_sizes(INPUT_PATH, OUTPUT_PATH)

        # Paso 8: Mostrar estadísticas finales
        print("\n📈 Estadísticas descriptivas:")
        df_parquet.describe().show()

    except Exception as e:
        print(f"❌ Error durante el ETL: {e}")
        raise
    finally:
        spark.stop()
        print("\n✨ Proceso ETL completado")

if __name__ == "__main__":
    main()
