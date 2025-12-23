"""
Spark Streaming: Word Count en Tiempo Real
==========================================
El "Hello World" de Spark Streaming.

Lee líneas de texto desde un socket y cuenta palabras en tiempo real.

Setup:
1. Terminal 1: nc -lk 9999
2. Terminal 2: python streaming_word_count.py
3. Terminal 1: Escribir frases y presionar Enter

Conceptos demostrados:
- readStream desde socket
- Transformaciones básicas (split, explode)
- Agregaciones con groupBy
- writeStream a consola
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, col

def main():
    print("🚀 Iniciando Word Count en Streaming...")
    print("=" * 70)

    # Crear sesión
    spark = SparkSession.builder \
        .appName("WordCount-Streaming") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("\n💡 Instrucciones:")
    print("   1. En otra terminal, ejecuta: nc -lk 9999")
    print("   2. Escribe frases y presiona Enter")
    print("   3. Observa el conteo de palabras aquí\n")

    try:
        # Leer líneas desde socket
        lines = spark.readStream \
            .format("socket") \
            .option("host", "localhost") \
            .option("port", 9999) \
            .load()

        print("✅ Conectado a socket localhost:9999")
        print("   Esperando datos...\n")

        # Split lines into words
        words = lines.select(
            explode(split(lines.value, " ")).alias("word")
        )

        # Limpiar: convertir a minúsculas y filtrar vacíos
        words_clean = words \
            .filter(col("word") != "") \
            .withColumn("word", lower(col("word")))

        # Contar palabras
        word_counts = words_clean.groupBy("word").count()

        # Ordenar por frecuencia
        word_counts_sorted = word_counts.orderBy(col("count").desc())

        # Escribir a consola
        query = word_counts_sorted.writeStream \
            .format("console") \
            .outputMode("complete") \
            .option("truncate", "false") \
            .trigger(processingTime="5 seconds") \
            .start()

        print("⚡ Streaming activo. Procesando palabras...\n")

        # Esperar terminación
        query.awaitTermination()

    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo streaming...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Asegúrate de ejecutar: nc -lk 9999 en otra terminal")
    finally:
        spark.stop()
        print("✅ Spark session cerrada")

if __name__ == "__main__":
    main()
