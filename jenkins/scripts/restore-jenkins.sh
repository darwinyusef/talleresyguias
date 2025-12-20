#!/bin/bash

# Script para restaurar backup de Jenkins
# Uso: ./restore-jenkins.sh <archivo-backup.tar.gz>

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
JENKINS_CONTAINER="jenkins"
BACKUP_FILE="$1"

# Validar argumentos
if [ -z "${BACKUP_FILE}" ]; then
    echo -e "${RED}❌ Error: Debes especificar el archivo de backup${NC}"
    echo -e "${YELLOW}Uso: $0 <archivo-backup.tar.gz>${NC}"
    echo -e "\n${YELLOW}Backups disponibles:${NC}"
    ls -lh ./backups/*.tar.gz 2>/dev/null || echo "No hay backups disponibles"
    exit 1
fi

# Verificar que el archivo existe
if [ ! -f "${BACKUP_FILE}" ]; then
    echo -e "${RED}❌ Error: Archivo '${BACKUP_FILE}' no encontrado${NC}"
    exit 1
fi

echo -e "${YELLOW}⚠️  ADVERTENCIA: Esta operación sobrescribirá la configuración actual de Jenkins${NC}"
echo -e "${YELLOW}Archivo de backup: ${BACKUP_FILE}${NC}"
read -p "¿Continuar? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Operación cancelada${NC}"
    exit 0
fi

echo -e "${GREEN}🔄 Iniciando restauración de Jenkins...${NC}"

# Detener Jenkins si está corriendo
if docker ps | grep -q "${JENKINS_CONTAINER}"; then
    echo -e "${YELLOW}⏸️  Deteniendo Jenkins...${NC}"
    docker stop "${JENKINS_CONTAINER}"
fi

# Crear backup de seguridad antes de restaurar
echo -e "${YELLOW}📦 Creando backup de seguridad...${NC}"
SAFETY_BACKUP="./backups/pre-restore-backup-$(date +%Y%m%d_%H%M%S).tar.gz"
docker run --rm \
    -v jenkins_home:/var/jenkins_home \
    -v "$(pwd)/backups:/backup" \
    alpine \
    tar czf "/backup/$(basename ${SAFETY_BACKUP})" /var/jenkins_home 2>/dev/null || true

# Limpiar volumen actual
echo -e "${YELLOW}🗑️  Limpiando volumen jenkins_home...${NC}"
docker run --rm \
    -v jenkins_home:/var/jenkins_home \
    alpine \
    sh -c "rm -rf /var/jenkins_home/*"

# Restaurar backup
echo -e "${YELLOW}📥 Restaurando backup...${NC}"
docker run --rm \
    -v jenkins_home:/var/jenkins_home \
    -v "$(pwd)/$(dirname ${BACKUP_FILE}):/backup" \
    alpine \
    tar xzf "/backup/$(basename ${BACKUP_FILE})" -C /

# Ajustar permisos
echo -e "${YELLOW}🔧 Ajustando permisos...${NC}"
docker run --rm \
    -v jenkins_home:/var/jenkins_home \
    alpine \
    chown -R 1000:1000 /var/jenkins_home

# Iniciar Jenkins
echo -e "${YELLOW}▶️  Iniciando Jenkins...${NC}"
docker start "${JENKINS_CONTAINER}" || docker compose up -d

# Esperar a que Jenkins esté listo
echo -e "${YELLOW}⏳ Esperando a que Jenkins esté listo...${NC}"
sleep 10

# Verificar que Jenkins está corriendo
if docker ps | grep -q "${JENKINS_CONTAINER}"; then
    echo -e "${GREEN}✅ Restauración completada exitosamente!${NC}"
    echo -e "${GREEN}   Jenkins está corriendo en: http://localhost:8080${NC}"
    echo -e "${GREEN}   Backup de seguridad guardado en: ${SAFETY_BACKUP}${NC}"
else
    echo -e "${RED}❌ Error: Jenkins no se inició correctamente${NC}"
    echo -e "${YELLOW}Puedes restaurar el backup de seguridad con:${NC}"
    echo -e "${YELLOW}   $0 ${SAFETY_BACKUP}${NC}"
    exit 1
fi

echo -e "\n${GREEN}✨ Restauración completada!${NC}"
