#!/bin/bash

echo "========================================="
echo "Iniciando MLflow Tracking Server"
echo "========================================="
echo ""

if [ ! -d "venv" ]; then
    echo "Error: Entorno virtual no encontrado."
    echo "Por favor ejecuta ./setup.sh primero"
    exit 1
fi

source venv/bin/activate

echo "MLflow Tracking Server iniciándose en:"
echo "  URL: http://localhost:5000"
echo ""
echo "Para detener: Ctrl+C"
echo ""

mlflow server \
    --host 127.0.0.1 \
    --port 5000 \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlruns
