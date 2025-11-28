#!/bin/bash

################################################################################
# SCRIPT 8: OPERACIONES ARITMÉTICAS Y MATEMÁTICAS
################################################################################
# Temas cubiertos:
# - Aritmética con (( ))
# - Aritmética con $((  ))
# - let comando
# - expr comando
# - bc para cálculos con decimales
# - Operadores aritméticos
# - Operaciones bit a bit
# - Números aleatorios
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 8: OPERACIONES ARITMÉTICAS Y MATEMÁTICAS"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. OPERADORES BÁSICOS
echo "--- 1. Operadores Aritméticos Básicos ---"
a=10
b=3

echo "a = $a, b = $b"
echo "Suma: a + b = $((a + b))"
echo "Resta: a - b = $((a - b))"
echo "Multiplicación: a * b = $((a * b))"
echo "División: a / b = $((a / b))"
echo "Módulo: a % b = $((a % b))"
echo "Potencia: a ** b = $((a ** b))"
echo ""

# 2. DIFERENTES MÉTODOS DE ARITMÉTICA
echo "--- 2. Diferentes Métodos ---"
x=5
y=2

# Método 1: $(( ))
resultado=$((x + y))
echo "Con \$(( )): $x + $y = $resultado"

# Método 2: (( ))
((resultado = x * y))
echo "Con (( )): $x * $y = $resultado"

# Método 3: let
let resultado=x**y
echo "Con let: $x ** $y = $resultado"

# Método 4: expr (antiguo, menos usado)
resultado=$(expr $x + $y)
echo "Con expr: $x + $y = $resultado"
echo ""

# 3. OPERADORES DE ASIGNACIÓN
echo "--- 3. Operadores de Asignación Compuestos ---"
num=10
echo "num inicial = $num"

((num += 5))
echo "num += 5 → $num"

((num -= 3))
echo "num -= 3 → $num"

((num *= 2))
echo "num *= 2 → $num"

((num /= 4))
echo "num /= 4 → $num"

((num %= 5))
echo "num %= 5 → $num"
echo ""

# 4. INCREMENTO Y DECREMENTO
echo "--- 4. Incremento y Decremento ---"
contador=5
echo "contador = $contador"

echo "contador++ = $((contador++))"
echo "Después: $contador"

echo "++contador = $((++contador))"
echo "Después: $contador"

echo "contador-- = $((contador--))"
echo "Después: $contador"

echo "--contador = $((--contador))"
echo "Después: $contador"
echo ""

# 5. OPERACIONES BIT A BIT
echo "--- 5. Operaciones Bit a Bit ---"
a=12  # 1100 en binario
b=10  # 1010 en binario

echo "a = $a (binario: 1100)"
echo "b = $b (binario: 1010)"
echo ""
echo "AND: a & b = $((a & b))   ($(echo "obase=2; $((a & b))" | bc))"
echo "OR:  a | b = $((a | b))  ($(echo "obase=2; $((a | b))" | bc))"
echo "XOR: a ^ b = $((a ^ b))    ($(echo "obase=2; $((a ^ b))" | bc))"
echo "NOT: ~a = $((~a))"
echo "Shift izq: a << 2 = $((a << 2))"
echo "Shift der: a >> 2 = $((a >> 2))"
echo ""

# 6. ARITMÉTICA CON DECIMALES (bc)
echo "--- 6. Aritmética con Decimales (bc) ---"
num1=10.5
num2=3.2

echo "num1 = $num1, num2 = $num2"
echo "Suma: $(echo "$num1 + $num2" | bc)"
echo "Resta: $(echo "$num1 - $num2" | bc)"
echo "Multiplicación: $(echo "$num1 * $num2" | bc)"
echo "División (2 decimales): $(echo "scale=2; $num1 / $num2" | bc)"
echo "División (4 decimales): $(echo "scale=4; $num1 / $num2" | bc)"
echo "Raíz cuadrada de 16: $(echo "sqrt(16)" | bc)"
echo "Potencia 2^10: $(echo "2^10" | bc)"
echo ""

# 7. NÚMEROS ALEATORIOS
echo "--- 7. Números Aleatorios ---"
echo "Número aleatorio (0-32767): $RANDOM"
echo "Número aleatorio (0-32767): $RANDOM"

# Número aleatorio en rango específico
min=1
max=100
aleatorio=$((RANDOM % (max - min + 1) + min))
echo "Número aleatorio entre $min y $max: $aleatorio"

# Múltiples números aleatorios
echo -n "5 números aleatorios (1-10): "
for i in {1..5}; do
    echo -n "$((RANDOM % 10 + 1)) "
done
echo ""
echo ""

# 8. EJERCICIO: Calculadora avanzada
echo "--- 8. Ejercicio: Calculadora Avanzada ---"
calc() {
    local expresion="$*"
    local resultado=$(echo "scale=4; $expresion" | bc)
    echo "$expresion = $resultado"
}

calc "10 + 5 * 2"
calc "(10 + 5) * 2"
calc "100 / 3"
calc "sqrt(144)"
calc "s(0)"  # seno de 0 (requiere -l en bc)
calc "l(2.718)"  # logaritmo natural
echo ""

# 9. EJERCICIO: Conversión de bases
echo "--- 9. Ejercicio: Conversión de Bases ---"
decimal=255

echo "Decimal: $decimal"
echo "Binario: $(echo "obase=2; $decimal" | bc)"
echo "Octal: $(echo "obase=8; $decimal" | bc)"
echo "Hexadecimal: $(echo "obase=16; $decimal" | bc)"
echo ""

# Conversión de binario a decimal
binario="11111111"
decimal_desde_bin=$((2#$binario))
echo "Binario $binario = Decimal $decimal_desde_bin"

# Conversión de hexadecimal a decimal
hex="FF"
decimal_desde_hex=$((16#$hex))
echo "Hexadecimal $hex = Decimal $decimal_desde_hex"
echo ""

# 10. EJERCICIO: Estadísticas de array
echo "--- 10. Ejercicio: Estadísticas de un Array ---"
NUMEROS=(45 23 67 12 89 34 56 78 90 11)

calcular_estadisticas() {
    local nums=("$@")
    local suma=0
    local max=${nums[0]}
    local min=${nums[0]}

    # Calcular suma, max y min
    for num in "${nums[@]}"; do
        ((suma += num))
        ((num > max)) && max=$num
        ((num < min)) && min=$num
    done

    local cantidad=${#nums[@]}
    local promedio=$((suma / cantidad))
    local rango=$((max - min))

    echo "Números: ${nums[@]}"
    echo "Cantidad: $cantidad"
    echo "Suma: $suma"
    echo "Promedio: $promedio"
    echo "Máximo: $max"
    echo "Mínimo: $min"
    echo "Rango: $rango"

    # Calcular mediana (array ordenado)
    local sorted=($(printf '%s\n' "${nums[@]}" | sort -n))
    local mediana
    if ((cantidad % 2 == 0)); then
        local mid=$((cantidad / 2))
        mediana=$(( (sorted[mid-1] + sorted[mid]) / 2 ))
    else
        mediana=${sorted[$((cantidad / 2))]}
    fi
    echo "Mediana: $mediana"
}

calcular_estadisticas "${NUMEROS[@]}"
echo ""

# 11. EJERCICIO: Números de Fibonacci
echo "--- 11. Ejercicio: Secuencia Fibonacci ---"
fibonacci() {
    local n=$1
    local a=0
    local b=1

    for ((i=0; i<n; i++)); do
        echo -n "$a "
        ((siguiente = a + b))
        ((a = b))
        ((b = siguiente))
    done
    echo ""
}

echo "Primeros 15 números de Fibonacci:"
fibonacci 15
echo ""

# 12. EJERCICIO: Números primos
echo "--- 12. Ejercicio: Verificador de Números Primos ---"
es_primo() {
    local num=$1

    if ((num < 2)); then
        return 1
    fi

    if ((num == 2)); then
        return 0
    fi

    if ((num % 2 == 0)); then
        return 1
    fi

    local i
    for ((i=3; i*i<=num; i+=2)); do
        if ((num % i == 0)); then
            return 1
        fi
    done

    return 0
}

echo "Números primos entre 1 y 50:"
for num in {1..50}; do
    if es_primo $num; then
        echo -n "$num "
    fi
done
echo ""
echo ""

# 13. EJERCICIO: Factorial
echo "--- 13. Ejercicio: Cálculo de Factorial ---"
factorial() {
    local n=$1
    local resultado=1

    for ((i=2; i<=n; i++)); do
        ((resultado *= i))
    done

    echo $resultado
}

for n in 5 10 15 20; do
    echo "Factorial de $n = $(factorial $n)"
done
echo ""

# 14. EJERCICIO: Conversor de unidades
echo "--- 14. Ejercicio: Conversor de Temperatura ---"
celsius_a_fahrenheit() {
    local celsius=$1
    echo "scale=2; ($celsius * 9/5) + 32" | bc
}

fahrenheit_a_celsius() {
    local fahrenheit=$1
    echo "scale=2; ($fahrenheit - 32) * 5/9" | bc
}

echo "Conversión de temperaturas:"
echo "0°C = $(celsius_a_fahrenheit 0)°F"
echo "25°C = $(celsius_a_fahrenheit 25)°F"
echo "100°C = $(celsius_a_fahrenheit 100)°F"
echo ""
echo "32°F = $(fahrenheit_a_celsius 32)°C"
echo "77°F = $(fahrenheit_a_celsius 77)°C"
echo "212°F = $(fahrenheit_a_celsius 212)°C"
echo ""

# 15. EJERCICIO: Máximo Común Divisor y Mínimo Común Múltiplo
echo "--- 15. Ejercicio: MCD y MCM ---"
mcd() {
    local a=$1
    local b=$2

    while ((b != 0)); do
        local temp=$b
        ((b = a % b))
        ((a = temp))
    done

    echo $a
}

mcm() {
    local a=$1
    local b=$2
    local mcd_valor=$(mcd $a $b)
    echo $((a * b / mcd_valor))
}

a=48
b=18
echo "MCD($a, $b) = $(mcd $a $b)"
echo "MCM($a, $b) = $(mcm $a $b)"
echo ""

a=100
b=35
echo "MCD($a, $b) = $(mcd $a $b)"
echo "MCM($a, $b) = $(mcm $a $b)"
echo ""

# 16. EJERCICIO: Juego de adivinanza
echo "--- 16. Ejercicio: Simulación de Juego de Adivinanza ---"
juego_adivinanza() {
    local numero_secreto=$((RANDOM % 100 + 1))
    local intentos=0
    local max_intentos=7

    echo "He pensado un número entre 1 y 100"
    echo "(Simulación con 3 intentos aleatorios)"

    for ((i=1; i<=3; i++)); do
        local intento=$((RANDOM % 100 + 1))
        ((intentos++))

        echo "Intento $intentos: $intento"

        if ((intento == numero_secreto)); then
            echo "¡Correcto! El número era $numero_secreto"
            echo "Adivinado en $intentos intentos"
            return 0
        elif ((intento < numero_secreto)); then
            echo "  → Muy bajo"
        else
            echo "  → Muy alto"
        fi
    done

    echo "El número era: $numero_secreto"
}

juego_adivinanza
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "💡 TIPS:"
echo "   - (( )) para aritmética y comparaciones numéricas"
echo "   - \$(( )) para aritmética con captura de resultado"
echo "   - bc para cálculos con decimales y funciones matemáticas"
echo "   - RANDOM genera números aleatorios 0-32767"
echo "   - Use scale=N en bc para controlar decimales"
echo "   - Operadores: + - * / % ** (potencia)"
echo "   - Operadores bit: & | ^ ~ << >>"
echo "   - No uses espacios en expresiones: \$((a+b)) no \$((a + b))"
