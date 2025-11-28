#!/bin/bash

################################################################################
# SCRIPT 2: CONDICIONALES Y COMPARACIONES
################################################################################
# Temas cubiertos:
# - if/else/elif
# - Operadores de comparación (numéricos y strings)
# - Operadores lógicos (&&, ||, !)
# - Case/switch
# - Pruebas de archivos (-f, -d, -r, etc)
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 2: CONDICIONALES Y COMPARACIONES"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. IF BÁSICO
echo "--- 1. If Básico ---"
EDAD=20

if [ $EDAD -ge 18 ]; then
    echo "Eres mayor de edad (edad: $EDAD)"
else
    echo "Eres menor de edad (edad: $EDAD)"
fi
echo ""

# 2. IF-ELIF-ELSE
echo "--- 2. If-Elif-Else ---"
NOTA=85

if [ $NOTA -ge 90 ]; then
    echo "Calificación: A (Excelente)"
elif [ $NOTA -ge 80 ]; then
    echo "Calificación: B (Muy Bien)"
elif [ $NOTA -ge 70 ]; then
    echo "Calificación: C (Bien)"
elif [ $NOTA -ge 60 ]; then
    echo "Calificación: D (Suficiente)"
else
    echo "Calificación: F (Insuficiente)"
fi
echo ""

# 3. OPERADORES DE COMPARACIÓN NUMÉRICA
echo "--- 3. Operadores Numéricos ---"
A=10
B=20

echo "A=$A, B=$B"
[ $A -eq $B ] && echo "A igual a B" || echo "A no igual a B"
[ $A -ne $B ] && echo "A diferente de B" || echo "A no diferente de B"
[ $A -lt $B ] && echo "A menor que B" || echo "A no menor que B"
[ $A -le $B ] && echo "A menor o igual que B" || echo "A no menor o igual que B"
[ $A -gt $B ] && echo "A mayor que B" || echo "A no mayor que B"
[ $A -ge $B ] && echo "A mayor o igual que B" || echo "A no mayor o igual que B"
echo ""

# 4. OPERADORES DE COMPARACIÓN DE STRINGS
echo "--- 4. Operadores de Strings ---"
STR1="hola"
STR2="mundo"
STR3="hola"

echo "STR1='$STR1', STR2='$STR2', STR3='$STR3'"
[ "$STR1" = "$STR3" ] && echo "STR1 igual a STR3" || echo "STR1 diferente de STR3"
[ "$STR1" != "$STR2" ] && echo "STR1 diferente de STR2" || echo "STR1 igual a STR2"
[ -z "$STR1" ] && echo "STR1 está vacío" || echo "STR1 no está vacío"
[ -n "$STR1" ] && echo "STR1 tiene contenido" || echo "STR1 está vacío"

# Comparación lexicográfica
if [[ "$STR1" < "$STR2" ]]; then
    echo "'$STR1' es lexicográficamente menor que '$STR2'"
fi
echo ""

# 5. OPERADORES LÓGICOS
echo "--- 5. Operadores Lógicos ---"
NUM=15

if [ $NUM -gt 10 ] && [ $NUM -lt 20 ]; then
    echo "$NUM está entre 10 y 20"
fi

if [ $NUM -lt 10 ] || [ $NUM -gt 14 ]; then
    echo "$NUM es menor que 10 O mayor que 14"
fi

if [ ! $NUM -eq 10 ]; then
    echo "$NUM no es igual a 10"
fi
echo ""

# 6. PRUEBAS DE ARCHIVOS
echo "--- 6. Pruebas de Archivos ---"
TEST_FILE="01_variables_y_tipos.sh"
TEST_DIR="/tmp"

if [ -f "$TEST_FILE" ]; then
    echo "✓ $TEST_FILE existe y es un archivo regular"
else
    echo "✗ $TEST_FILE no existe o no es un archivo regular"
fi

if [ -d "$TEST_DIR" ]; then
    echo "✓ $TEST_DIR existe y es un directorio"
fi

if [ -r "$TEST_FILE" ]; then
    echo "✓ $TEST_FILE es legible"
fi

if [ -w "$TEST_FILE" ]; then
    echo "✓ $TEST_FILE es escribible"
fi

if [ -x "$TEST_FILE" ]; then
    echo "✓ $TEST_FILE es ejecutable"
fi

if [ -s "$TEST_FILE" ]; then
    echo "✓ $TEST_FILE no está vacío"
fi
echo ""

# 7. CASE (SWITCH)
echo "--- 7. Case Statement ---"
DIA=${1:-"lunes"}

case $DIA in
    lunes)
        echo "Inicio de semana laboral"
        ;;
    martes|miércoles|jueves)
        echo "Mitad de semana"
        ;;
    viernes)
        echo "Último día laboral"
        ;;
    sábado|domingo)
        echo "Fin de semana"
        ;;
    *)
        echo "Día no reconocido: $DIA"
        ;;
esac
echo ""

# 8. EJERCICIO: Clasificador de números
echo "--- 8. Ejercicio: Clasificador de Números ---"
clasificar_numero() {
    local num=$1
    local resultado=""

    # Positivo o negativo
    if [ $num -gt 0 ]; then
        resultado="positivo"
    elif [ $num -lt 0 ]; then
        resultado="negativo"
    else
        resultado="cero"
    fi

    # Par o impar (solo para no-cero)
    if [ $num -ne 0 ]; then
        if [ $((num % 2)) -eq 0 ]; then
            resultado="$resultado y par"
        else
            resultado="$resultado e impar"
        fi
    fi

    echo "El número $num es: $resultado"
}

clasificar_numero 15
clasificar_numero -8
clasificar_numero 0
clasificar_numero 42
echo ""

# 9. EJERCICIO: Validador de entrada
echo "--- 9. Ejercicio: Validador de Entrada ---"
validar_email() {
    local email=$1

    if [ -z "$email" ]; then
        echo "✗ Error: Email vacío"
        return 1
    fi

    if [[ "$email" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
        echo "✓ Email válido: $email"
        return 0
    else
        echo "✗ Email inválido: $email"
        return 1
    fi
}

validar_email "usuario@ejemplo.com"
validar_email "correo_invalido"
validar_email ""
echo ""

# 10. EJERCICIO: FizzBuzz (clásico de programación)
echo "--- 10. Ejercicio: FizzBuzz ---"
echo "Números del 1 al 30:"
for i in {1..30}; do
    resultado=""

    if [ $((i % 3)) -eq 0 ]; then
        resultado="Fizz"
    fi

    if [ $((i % 5)) -eq 0 ]; then
        resultado="${resultado}Buzz"
    fi

    if [ -z "$resultado" ]; then
        resultado=$i
    fi

    echo -n "$resultado "
done
echo ""
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "💡 TIPS:"
echo "   - Usa [[ ]] en lugar de [ ] para comparaciones avanzadas"
echo "   - Siempre usa comillas en strings: [ \"\$var\" = \"valor\" ]"
echo "   - Para números usa -eq, -ne, -lt, etc."
echo "   - Para strings usa =, !=, <, >"
echo "   - Case es más limpio que múltiples if-elif para valores discretos"
