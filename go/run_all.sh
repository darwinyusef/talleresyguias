#!/bin/bash

# Script para ejecutar todos los ejercicios de Go
# Uso: ./run_all.sh [numero_ejercicio]

echo "🚀 Ejercicios de Go - Ejecutor"
echo "=============================="
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Si se proporciona un número, ejecutar solo ese ejercicio
if [ ! -z "$1" ]; then
    file=$(printf "%02d_*.go" $1)
    if ls $file 1> /dev/null 2>&1; then
        echo -e "${BLUE}Ejecutando ejercicio $1...${NC}"
        echo ""
        go run $file
        exit 0
    else
        echo -e "${RED}Error: No se encontró el ejercicio $1${NC}"
        exit 1
    fi
fi

# Ejecutar todos los ejercicios
count=0
success=0
failed=0

for file in [0-9][0-9]_*.go; do
    if [ -f "$file" ]; then
        count=$((count + 1))
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}Ejecutando: $file${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        
        if go run "$file"; then
            success=$((success + 1))
            echo ""
            echo -e "${GREEN}✓ Completado exitosamente${NC}"
        else
            failed=$((failed + 1))
            echo ""
            echo -e "${RED}✗ Error en la ejecución${NC}"
        fi
        
        echo ""
        echo ""
        
        # Pequeña pausa entre ejercicios
        sleep 1
    fi
done

# Resumen
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}RESUMEN${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "Total de ejercicios: $count"
echo -e "${GREEN}Exitosos: $success${NC}"
if [ $failed -gt 0 ]; then
    echo -e "${RED}Fallidos: $failed${NC}"
fi
echo ""
