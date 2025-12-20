#!/bin/bash

# Script para limpiar builds antiguos de Jenkins
# Uso: ./cleanup-old-builds.sh [días]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
JENKINS_CONTAINER="jenkins"
DAYS_TO_KEEP="${1:-30}"  # Por defecto mantener últimos 30 días

echo -e "${GREEN}🧹 Limpiando builds antiguos de Jenkins...${NC}"
echo -e "${YELLOW}Manteniendo builds de los últimos ${DAYS_TO_KEEP} días${NC}"

# Verificar que el contenedor existe
if ! docker ps | grep -q "${JENKINS_CONTAINER}"; then
    echo -e "${RED}❌ Error: Contenedor '${JENKINS_CONTAINER}' no está corriendo${NC}"
    exit 1
fi

# Limpiar builds antiguos
echo -e "${YELLOW}🗑️  Eliminando builds antiguos...${NC}"
docker exec "${JENKINS_CONTAINER}" bash -c "
    find /var/jenkins_home/jobs/*/builds/* -type d -mtime +${DAYS_TO_KEEP} -exec rm -rf {} + 2>/dev/null || true
"

# Limpiar workspaces
echo -e "${YELLOW}🗑️  Limpiando workspaces...${NC}"
docker exec "${JENKINS_CONTAINER}" bash -c "
    find /var/jenkins_home/workspace/* -type d -mtime +${DAYS_TO_KEEP} -exec rm -rf {} + 2>/dev/null || true
"

# Limpiar logs antiguos
echo -e "${YELLOW}📋 Limpiando logs antiguos...${NC}"
docker exec "${JENKINS_CONTAINER}" bash -c "
    find /var/jenkins_home/jobs/*/builds/*/log -type f -mtime +${DAYS_TO_KEEP} -delete 2>/dev/null || true
"

# Limpiar imágenes Docker no utilizadas
echo -e "${YELLOW}🐳 Limpiando imágenes Docker no utilizadas...${NC}"
docker image prune -a --filter "until=${DAYS_TO_KEEP}d" -f

# Limpiar contenedores detenidos
echo -e "${YELLOW}📦 Limpiando contenedores detenidos...${NC}"
docker container prune -f

# Limpiar volúmenes no utilizados
echo -e "${YELLOW}💾 Limpiando volúmenes no utilizados...${NC}"
docker volume prune -f

# Mostrar espacio liberado
echo -e "\n${GREEN}📊 Espacio en disco:${NC}"
df -h | grep -E "Filesystem|/var/lib/docker" || df -h /

echo -e "\n${GREEN}✅ Limpieza completada!${NC}"

# Mostrar tamaño del volumen de Jenkins
JENKINS_SIZE=$(docker run --rm -v jenkins_home:/data alpine du -sh /data | cut -f1)
echo -e "${GREEN}   Tamaño de jenkins_home: ${JENKINS_SIZE}${NC}"
