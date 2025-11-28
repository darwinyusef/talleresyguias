#!/bin/bash

################################################################################
# SCRIPT 4: FUNCIONES Y MODULARIZACIÓN
################################################################################
# Temas cubiertos:
# - Declaración de funciones
# - Parámetros y argumentos
# - Variables locales y globales
# - Retorno de valores
# - Recursión
# - Scope de variables
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 4: FUNCIONES Y MODULARIZACIÓN"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. FUNCIÓN BÁSICA
echo "--- 1. Función Básica ---"
saludar() {
    echo "¡Hola desde una función!"
}

saludar
echo ""

# 2. FUNCIÓN CON PARÁMETROS
echo "--- 2. Función con Parámetros ---"
saludar_persona() {
    local nombre=$1
    local edad=$2
    echo "Hola, $nombre! Tienes $edad años."
}

saludar_persona "Carlos" 25
saludar_persona "Ana" 30
echo ""

# 3. ARGUMENTOS ESPECIALES EN FUNCIONES
echo "--- 3. Argumentos Especiales ---"
mostrar_args() {
    echo "Nombre de la función: $FUNCNAME"
    echo "Número de argumentos: $#"
    echo "Todos los argumentos: $@"
    echo "Primer argumento: $1"
    echo "Segundo argumento: $2"
    echo "Todos como string: $*"
}

mostrar_args uno dos tres cuatro
echo ""

# 4. VARIABLES LOCALES VS GLOBALES
echo "--- 4. Variables Locales vs Globales ---"
GLOBAL="Variable global"

funcion_scope() {
    local LOCAL="Variable local"
    GLOBAL="Global modificada"
    OTRA_GLOBAL="Nueva global"

    echo "Dentro de función:"
    echo "  LOCAL: $LOCAL"
    echo "  GLOBAL: $GLOBAL"
}

echo "Antes de la función:"
echo "  GLOBAL: $GLOBAL"

funcion_scope

echo "Después de la función:"
echo "  GLOBAL: $GLOBAL"
echo "  OTRA_GLOBAL: $OTRA_GLOBAL"
# echo "  LOCAL: $LOCAL"  # Esto daría error o vacío
echo ""

# 5. RETORNO DE VALORES
echo "--- 5. Retorno de Valores ---"
# Método 1: Usando return (solo números 0-255)
es_par() {
    local num=$1
    if [ $((num % 2)) -eq 0 ]; then
        return 0  # true
    else
        return 1  # false
    fi
}

if es_par 10; then
    echo "10 es par"
fi

if ! es_par 7; then
    echo "7 es impar"
fi
echo ""

# Método 2: Usando echo y captura de salida
sumar() {
    local a=$1
    local b=$2
    echo $((a + b))
}

resultado=$(sumar 15 25)
echo "15 + 25 = $resultado"
echo ""

# 6. FUNCIÓN CON VALORES POR DEFECTO
echo "--- 6. Valores por Defecto ---"
crear_usuario() {
    local nombre=${1:-"usuario"}
    local rol=${2:-"invitado"}
    local activo=${3:-"true"}

    echo "Usuario creado:"
    echo "  Nombre: $nombre"
    echo "  Rol: $rol"
    echo "  Activo: $activo"
}

crear_usuario "admin" "administrador" "true"
crear_usuario "juan"
crear_usuario
echo ""

# 7. RECURSIÓN
echo "--- 7. Recursión ---"
# Factorial recursivo
factorial() {
    local n=$1
    if [ $n -le 1 ]; then
        echo 1
    else
        local prev=$(factorial $((n - 1)))
        echo $((n * prev))
    fi
}

echo "Factorial de 5: $(factorial 5)"
echo "Factorial de 7: $(factorial 7)"
echo ""

# 8. FIBONACCI RECURSIVO
echo "--- 8. Fibonacci Recursivo ---"
fibonacci() {
    local n=$1
    if [ $n -le 1 ]; then
        echo $n
    else
        local a=$(fibonacci $((n - 1)))
        local b=$(fibonacci $((n - 2)))
        echo $((a + b))
    fi
}

echo -n "Secuencia Fibonacci: "
for i in {0..10}; do
    echo -n "$(fibonacci $i) "
done
echo ""
echo ""

# 9. FUNCIÓN QUE DEVUELVE ARRAY
echo "--- 9. Función que Devuelve Array ---"
obtener_archivos_sh() {
    local archivos=(*.sh)
    echo "${archivos[@]}"
}

IFS=' ' read -r -a archivos <<< "$(obtener_archivos_sh)"
echo "Archivos .sh encontrados:"
for archivo in "${archivos[@]}"; do
    echo "  - $archivo"
done
echo ""

# 10. VALIDACIÓN DE PARÁMETROS
echo "--- 10. Validación de Parámetros ---"
dividir() {
    if [ $# -ne 2 ]; then
        echo "Error: Se requieren exactamente 2 argumentos"
        return 1
    fi

    local dividendo=$1
    local divisor=$2

    if [ $divisor -eq 0 ]; then
        echo "Error: No se puede dividir por cero"
        return 1
    fi

    echo $((dividendo / divisor))
    return 0
}

echo "100 / 5 = $(dividir 100 5)"
dividir 10 0
dividir 10
echo ""

# 11. EJERCICIO: Calculadora
echo "--- 11. Ejercicio: Calculadora ---"
calculadora() {
    local num1=$1
    local operador=$2
    local num2=$3

    case $operador in
        +)
            echo $((num1 + num2))
            ;;
        -)
            echo $((num1 - num2))
            ;;
        x|\*)
            echo $((num1 * num2))
            ;;
        /)
            if [ $num2 -eq 0 ]; then
                echo "Error: División por cero"
                return 1
            fi
            echo $((num1 / num2))
            ;;
        %)
            echo $((num1 % num2))
            ;;
        **)
            local resultado=1
            for ((i=0; i<num2; i++)); do
                resultado=$((resultado * num1))
            done
            echo $resultado
            ;;
        *)
            echo "Operador no válido: $operador"
            return 1
            ;;
    esac
}

echo "10 + 5 = $(calculadora 10 + 5)"
echo "20 - 8 = $(calculadora 20 - 8)"
echo "6 x 7 = $(calculadora 6 x 7)"
echo "100 / 4 = $(calculadora 100 / 4)"
echo "17 % 5 = $(calculadora 17 % 5)"
echo "2 ** 8 = $(calculadora 2 '**' 8)"
echo ""

# 12. EJERCICIO: Validador de cadenas
echo "--- 12. Ejercicio: Validador de Cadenas ---"
es_palindromo() {
    local texto=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr -d ' ')
    local reverso=$(echo "$texto" | rev)

    if [ "$texto" = "$reverso" ]; then
        echo "✓ '$1' es un palíndromo"
        return 0
    else
        echo "✗ '$1' no es un palíndromo"
        return 1
    fi
}

es_palindromo "anilina"
es_palindromo "radar"
es_palindromo "hola"
es_palindromo "Anita lava la tina"
echo ""

# 13. EJERCICIO: Búsqueda en array
echo "--- 13. Ejercicio: Búsqueda en Array ---"
buscar_en_array() {
    local buscar=$1
    shift  # Remover primer argumento
    local array=("$@")

    for i in "${!array[@]}"; do
        if [ "${array[$i]}" = "$buscar" ]; then
            echo "Encontrado '$buscar' en índice $i"
            return 0
        fi
    done

    echo "'$buscar' no encontrado"
    return 1
}

FRUTAS=("manzana" "naranja" "plátano" "uva" "pera")
buscar_en_array "plátano" "${FRUTAS[@]}"
buscar_en_array "sandía" "${FRUTAS[@]}"
echo ""

# 14. EJERCICIO: Máximo Común Divisor (MCD)
echo "--- 14. Ejercicio: MCD (Algoritmo de Euclides) ---"
mcd() {
    local a=$1
    local b=$2

    while [ $b -ne 0 ]; do
        local temp=$b
        b=$((a % b))
        a=$temp
    done

    echo $a
}

echo "MCD(48, 18) = $(mcd 48 18)"
echo "MCD(100, 35) = $(mcd 100 35)"
echo "MCD(17, 19) = $(mcd 17 19)"
echo ""

# 15. EJERCICIO: Generador de contraseñas
echo "--- 15. Ejercicio: Generador de Contraseñas ---"
generar_password() {
    local longitud=${1:-12}
    local password=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#$%^&*' | fold -w $longitud | head -n 1)
    echo "$password"
}

echo "Contraseña de 8 caracteres: $(generar_password 8)"
echo "Contraseña de 16 caracteres: $(generar_password 16)"
echo "Contraseña por defecto: $(generar_password)"
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "💡 TIPS:"
echo "   - Usa 'local' para variables dentro de funciones"
echo "   - 'return' solo acepta códigos 0-255 (0=éxito, >0=error)"
echo "   - Usa echo + captura para retornar strings/números"
echo "   - Siempre valida los parámetros antes de usarlos"
echo "   - Las funciones pueden llamarse a sí mismas (recursión)"
echo "   - Documenta tus funciones con comentarios"
