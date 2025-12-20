#!/bin/bash

# Script para hacer backup de Jenkins
# Uso: ./backup-jenkins.sh [nombre-backup]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
JENKINS_CONTAINER="jenkins"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="${1:-jenkins-backup-${TIMESTAMP}}"

echo -e "${GREEN}🔄 Iniciando backup de Jenkins...${NC}"

# Crear directorio de backups si no existe
mkdir -p "${BACKUP_DIR}"

# Verificar que el contenedor existe
if ! docker ps -a | grep -q "${JENKINS_CONTAINER}"; then
    echo -e "${RED}❌ Error: Contenedor '${JENKINS_CONTAINER}' no encontrado${NC}"
    exit 1
fi

# Crear backup del volumen jenkins_home
echo -e "${YELLOW}📦 Creando backup del volumen jenkins_home...${NC}"
docker run --rm \
    -v jenkins_home:/var/jenkins_home \
    -v "$(pwd)/${BACKUP_DIR}:/backup" \
    alpine \
    tar czf "/backup/${BACKUP_NAME}.tar.gz" /var/jenkins_home

# Verificar que el backup se creó correctamente
if [ -f "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" ]; then
    BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)
    echo -e "${GREEN}✅ Backup creado exitosamente!${NC}"
    echo -e "${GREEN}   Archivo: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz${NC}"
    echo -e "${GREEN}   Tamaño: ${BACKUP_SIZE}${NC}"
    
    # Crear archivo de metadata
    cat > "${BACKUP_DIR}/${BACKUP_NAME}.info" << EOF
Backup de Jenkins
Fecha: $(date)
Contenedor: ${JENKINS_CONTAINER}
Archivo: ${BACKUP_NAME}.tar.gz
Tamaño: ${BACKUP_SIZE}
EOF
    
    echo -e "${GREEN}   Metadata: ${BACKUP_DIR}/${BACKUP_NAME}.info${NC}"
else
    echo -e "${RED}❌ Error: No se pudo crear el backup${NC}"
    exit 1
fi

# Listar backups existentes
echo -e "\n${YELLOW}📋 Backups disponibles:${NC}"
ls -lh "${BACKUP_DIR}"/*.tar.gz 2>/dev/null || echo "No hay backups previos"

echo -e "\n${GREEN}✨ Backup completado!${NC}"
