#!/bin/bash
# docker-cleanup.sh - Limpia recursos de Docker para optimizar el Runner

echo "🧹 Iniciando limpieza de Docker..."

# Eliminar contenedores detenidos
echo "🗑️ Eliminando contenedores detenidos..."
docker container prune -f

# Eliminar imágenes huérfanas
echo "🖼️ Eliminando imágenes sin tag (dangling)..."
docker image prune -f

# Eliminar volúmenes no usados
echo "💿 Eliminando volúmenes no usados..."
docker volume prune -f

echo "✅ Limpieza completada. Espacio liberado:"
docker system df
