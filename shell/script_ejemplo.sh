#!/bin/bash

# Script de ejemplo que recibe parámetros y realiza operaciones básicas

echo "=== Script Shell Iniciado ==="
echo "Fecha y hora: $(date)"
echo ""

# Verificar si se pasaron argumentos
if [ $# -eq 0 ]; then
    echo "⚠️  No se pasaron argumentos"
    echo "Uso: $0 <nombre> <edad>"
    exit 1
fi

# Recibir parámetros
NOMBRE=${1:-"Desconocido"}
EDAD=${2:-0}

echo "👤 Nombre: $NOMBRE"
echo "🎂 Edad: $EDAD"
echo ""

# Realizar alguna operación
if [ $EDAD -ge 18 ]; then
    echo "✅ $NOMBRE es mayor de edad"
else
    echo "❌ $NOMBRE es menor de edad"
fi

# Crear un archivo temporal con información
TIMESTAMP=$(date +%s)
OUTPUT_FILE="/tmp/script_output_${TIMESTAMP}.txt"
echo "Nombre: $NOMBRE" > $OUTPUT_FILE
echo "Edad: $EDAD" >> $OUTPUT_FILE
echo "Procesado: $(date)" >> $OUTPUT_FILE

echo ""
echo "📄 Archivo generado: $OUTPUT_FILE"
echo "=== Script Shell Finalizado ==="

exit 0
