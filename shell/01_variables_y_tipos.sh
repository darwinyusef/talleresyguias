#!/bin/bash

################################################################################
# SCRIPT 1: VARIABLES Y TIPOS DE DATOS EN BASH
################################################################################
# Temas cubiertos:
# - Declaración de variables
# - Variables de entorno
# - Arrays (arreglos)
# - Operaciones con strings
# - Variables especiales ($#, $@, $?, etc)
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 1: VARIABLES Y TIPOS DE DATOS EN BASH"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. VARIABLES SIMPLES
# En Bash no hay tipos explícitos, todo es texto por defecto
echo "--- 1. Variables Simples ---"
NOMBRE="Bash"
VERSION=5.0
ES_SHELL=true

echo "Lenguaje: $NOMBRE"
echo "Versión: $VERSION"
echo "Es un shell: $ES_SHELL"
echo ""

# 2. VARIABLES DE SOLO LECTURA (constantes)
echo "--- 2. Variables de Solo Lectura ---"
readonly PI=3.14159
echo "Valor de PI: $PI"
# Descomentar la siguiente línea causaría error:
# PI=3.14  # Error: PI: readonly variable
echo ""

# 3. ARRAYS (ARREGLOS)
echo "--- 3. Arrays ---"
# Array indexado
LENGUAJES=("Python" "JavaScript" "Go" "Rust" "C++")

echo "Primer lenguaje: ${LENGUAJES[0]}"
echo "Tercer lenguaje: ${LENGUAJES[2]}"
echo "Todos los lenguajes: ${LENGUAJES[@]}"
echo "Cantidad de lenguajes: ${#LENGUAJES[@]}"
echo ""

# Añadir elemento al array
LENGUAJES+=("Java")
echo "Después de añadir Java: ${LENGUAJES[@]}"
echo ""

# 4. ARRAYS ASOCIATIVOS (diccionarios)
echo "--- 4. Arrays Asociativos ---"
declare -A CAPITALES
CAPITALES[Colombia]="Bogotá"
CAPITALES[Argentina]="Buenos Aires"
CAPITALES[México]="Ciudad de México"
CAPITALES[España]="Madrid"

echo "Capital de Colombia: ${CAPITALES[Colombia]}"
echo "Capital de México: ${CAPITALES[México]}"
echo "Todas las claves: ${!CAPITALES[@]}"
echo "Todos los valores: ${CAPITALES[@]}"
echo ""

# 5. OPERACIONES CON STRINGS
echo "--- 5. Operaciones con Strings ---"
TEXTO="Hola Mundo desde Bash"

# Longitud de string
echo "Texto original: '$TEXTO'"
echo "Longitud: ${#TEXTO}"

# Subcadenas
echo "Desde posición 5: '${TEXTO:5}'"
echo "5 caracteres desde pos 5: '${TEXTO:5:5}'"

# Reemplazo
echo "Reemplazar 'Bash' por 'Shell': '${TEXTO/Bash/Shell}'"

# Mayúsculas/Minúsculas
echo "A mayúsculas: '${TEXTO^^}'"
echo "A minúsculas: '${TEXTO,,}'"
echo ""

# 6. VARIABLES ESPECIALES
echo "--- 6. Variables Especiales ---"
echo "Nombre del script: $0"
echo "Cantidad de argumentos: $#"
echo "Todos los argumentos: $@"
echo "PID del script: $$"
echo "Último código de retorno: $?"
echo ""

# 7. VARIABLES DE ENTORNO
echo "--- 7. Variables de Entorno ---"
echo "Usuario actual: $USER"
echo "Directorio HOME: $HOME"
echo "PATH: ${PATH:0:50}..."  # Mostrar solo primeros 50 caracteres
echo "Shell actual: $SHELL"
echo ""

# 8. EJERCICIO PRÁCTICO: Calculadora de edad
echo "--- 8. Ejercicio Práctico: Calculadora de Edad ---"
ANIO_ACTUAL=$(date +%Y)
ANIO_NACIMIENTO=${1:-1990}  # Usar argumento o 1990 por defecto

EDAD=$((ANIO_ACTUAL - ANIO_NACIMIENTO))

echo "Año actual: $ANIO_ACTUAL"
echo "Año de nacimiento: $ANIO_NACIMIENTO"
echo "Edad aproximada: $EDAD años"
echo ""

# 9. EJERCICIO: Procesamiento de lista de números
echo "--- 9. Ejercicio: Estadísticas de Array ---"
NUMEROS=(45 23 67 12 89 34 56 78 90 11)

echo "Números: ${NUMEROS[@]}"

# Calcular suma y promedio
SUMA=0
for num in "${NUMEROS[@]}"; do
    SUMA=$((SUMA + num))
done

PROMEDIO=$((SUMA / ${#NUMEROS[@]}))

echo "Cantidad: ${#NUMEROS[@]}"
echo "Suma: $SUMA"
echo "Promedio: $PROMEDIO"

# Encontrar máximo y mínimo
MAX=${NUMEROS[0]}
MIN=${NUMEROS[0]}

for num in "${NUMEROS[@]}"; do
    if [ $num -gt $MAX ]; then
        MAX=$num
    fi
    if [ $num -lt $MIN ]; then
        MIN=$num
    fi
done

echo "Máximo: $MAX"
echo "Mínimo: $MIN"
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "💡 TIPS:"
echo "   - Usa \${variable} en lugar de \$variable para mayor claridad"
echo "   - Las variables son globales por defecto, usa 'local' en funciones"
echo "   - Usa 'readonly' para constantes"
echo "   - Los arrays indexados empiezan en 0"
echo "   - Usa comillas dobles para preservar espacios en strings"
