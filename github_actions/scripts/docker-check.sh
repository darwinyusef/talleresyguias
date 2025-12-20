#!/bin/bash
# docker-check.sh - Verifica el estado de Docker y los contenedores del taller

echo "🐳 Verificando entorno Docker..."

docker version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Error: Docker no está instalado o el daemon no está corriendo."
    exit 1
fi

echo "✅ Docker está activo."

# Listar contenedores corriendo del taller
echo "📊 Contenedores activos del taller 'workshop-ga':"
docker ps --filter "label=workshop=ga" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Verificar uso de disco
echo "💾 Espacio utilizado por imágenes Docker:"
docker system df | grep "Images"
