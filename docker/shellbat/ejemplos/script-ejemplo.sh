#!/bin/bash

# Script de ejemplo para el taller
# Este script demuestra funcionalidades básicas de shell

echo "=========================================="
echo "Script de Ejemplo - Shell (.sh)"
echo "=========================================="
echo ""

# Variables
NOMBRE="Usuario"
FECHA=$(date +"%Y-%m-%d %H:%M:%S")

echo "Hola $NOMBRE"
echo "Fecha actual: $FECHA"
echo ""

# Argumentos
echo "Procesando argumentos..."
echo "Primer argumento: $1"
echo "Segundo argumento: $2"
echo "Número total de argumentos: $#"
echo "Todos los argumentos: $@"
echo ""

# Directorio actual
echo "Directorio actual:"
pwd
echo ""

# Listar archivos
echo "Archivos en el directorio actual:"
ls -lh
echo ""

# Verificar si existe un archivo
ARCHIVO="datos.txt"
if [ -f "$ARCHIVO" ]; then
    echo "El archivo $ARCHIVO existe"
    echo "Contenido:"
    cat "$ARCHIVO"
else
    echo "El archivo $ARCHIVO NO existe"
    echo "Creando archivo de ejemplo..."
    echo "Este es un archivo de ejemplo creado por el script" > "$ARCHIVO"
    echo "Archivo creado exitosamente"
fi
echo ""

# Bucle simple
echo "Contando del 1 al 5:"
for i in 1 2 3 4 5; do
    echo "  Número: $i"
done
echo ""

# Variables de entorno
echo "Variables de entorno personalizadas:"
echo "MI_VARIABLE: ${MI_VARIABLE:-'No definida'}"
echo "API_KEY: ${API_KEY:-'No definida'}"
echo ""

# Operaciones con archivos
echo "Información del sistema:"
echo "Usuario: $(whoami)"
echo "Hostname: $(hostname)"
echo "Sistema operativo: $(uname -s)"
echo ""

echo "=========================================="
echo "Script completado exitosamente"
echo "=========================================="

exit 0
