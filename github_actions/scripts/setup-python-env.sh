#!/bin/bash
# setup-python-env.sh - Automatiza la preparación y testeo de apps Python

APP_PATH=$1

if [ -z "$APP_PATH" ]; then
    echo "❌ Error: Debes especificar el path de la aplicación (ej: ejemplos/python-fastapi)"
    exit 1
fi

echo "🐍 Preparando entorno para: $APP_PATH"

cd "$APP_PATH" || exit 1

if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias..."
    pip install --no-cache-dir -r requirements.txt
else
    echo "⚠️ Advertencia: No se encontró requirements.txt"
fi

if [ -d "tests" ]; then
    echo "🧪 Ejecutando pruebas con Pytest..."
    pytest --maxfail=2 --disable-warnings
else
    echo "⚠️ Advertencia: No se encontró carpeta de tests."
fi

echo "✨ Proceso completado para $APP_PATH"
