#!/bin/bash

################################################################################
# SCRIPT 3: BUCLES E ITERACIONES
################################################################################
# Temas cubiertos:
# - For loops (tradicional, C-style, range)
# - While loops
# - Until loops
# - Break y continue
# - Iteración sobre arrays
# - Iteración sobre archivos
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 3: BUCLES E ITERACIONES"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. FOR LOOP - LISTA DE VALORES
echo "--- 1. For Loop con Lista de Valores ---"
for fruta in manzana naranja plátano uva; do
    echo "Fruta: $fruta"
done
echo ""

# 2. FOR LOOP - RANGO
echo "--- 2. For Loop con Rango ---"
echo "Números del 1 al 10:"
for i in {1..10}; do
    echo -n "$i "
done
echo ""
echo ""

echo "Números pares del 2 al 20 (con incremento de 2):"
for i in {2..20..2}; do
    echo -n "$i "
done
echo ""
echo ""

# 3. FOR LOOP - ESTILO C
echo "--- 3. For Loop Estilo C ---"
echo "Cuenta regresiva desde 10:"
for ((i=10; i>=1; i--)); do
    echo -n "$i "
    sleep 0.1
done
echo "¡Despegue!"
echo ""

# 4. WHILE LOOP
echo "--- 4. While Loop ---"
contador=1
echo "Contador con while (1 al 5):"
while [ $contador -le 5 ]; do
    echo "Iteración: $contador"
    ((contador++))
done
echo ""

# 5. UNTIL LOOP
echo "--- 5. Until Loop ---"
numero=1
echo "Contador con until (hasta llegar a 5):"
until [ $numero -gt 5 ]; do
    echo "Número: $numero"
    ((numero++))
done
echo ""

# 6. BREAK - SALIR DEL BUCLE
echo "--- 6. Break (salir del bucle) ---"
echo "Buscar el primer número divisible por 7:"
for i in {1..100}; do
    if [ $((i % 7)) -eq 0 ]; then
        echo "Encontrado: $i"
        break
    fi
done
echo ""

# 7. CONTINUE - SALTAR ITERACIÓN
echo "--- 7. Continue (saltar iteración) ---"
echo "Números del 1 al 10, saltando los pares:"
for i in {1..10}; do
    if [ $((i % 2)) -eq 0 ]; then
        continue
    fi
    echo -n "$i "
done
echo ""
echo ""

# 8. ITERAR SOBRE ARRAYS
echo "--- 8. Iterar sobre Arrays ---"
LENGUAJES=("Python" "JavaScript" "Go" "Rust" "C++")

echo "Lenguajes de programación:"
for lang in "${LENGUAJES[@]}"; do
    echo "  - $lang"
done
echo ""

echo "Con índices:"
for i in "${!LENGUAJES[@]}"; do
    echo "  [$i]: ${LENGUAJES[$i]}"
done
echo ""

# 9. ITERAR SOBRE ARCHIVOS
echo "--- 9. Iterar sobre Archivos ---"
echo "Archivos .sh en el directorio actual:"
contador=0
for archivo in *.sh; do
    if [ -f "$archivo" ]; then
        tamaño=$(wc -l < "$archivo")
        echo "  $archivo ($tamaño líneas)"
        ((contador++))
    fi
done
echo "Total: $contador archivos"
echo ""

# 10. NESTED LOOPS (BUCLES ANIDADOS)
echo "--- 10. Bucles Anidados - Tabla de Multiplicar ---"
echo "Tabla del 1 al 5:"
for i in {1..5}; do
    echo -n "Tabla del $i: "
    for j in {1..5}; do
        resultado=$((i * j))
        printf "%3d " $resultado
    done
    echo ""
done
echo ""

# 11. EJERCICIO: Suma de números
echo "--- 11. Ejercicio: Suma de Números del 1 al 100 ---"
suma=0
for i in {1..100}; do
    suma=$((suma + i))
done
echo "La suma de números del 1 al 100 es: $suma"
echo ""

# 12. EJERCICIO: Números primos
echo "--- 12. Ejercicio: Números Primos hasta 50 ---"
es_primo() {
    local num=$1
    if [ $num -lt 2 ]; then
        return 1
    fi
    for ((i=2; i*i<=num; i++)); do
        if [ $((num % i)) -eq 0 ]; then
            return 1
        fi
    done
    return 0
}

echo -n "Números primos: "
for num in {2..50}; do
    if es_primo $num; then
        echo -n "$num "
    fi
done
echo ""
echo ""

# 13. EJERCICIO: Factorial
echo "--- 13. Ejercicio: Factorial ---"
calcular_factorial() {
    local n=$1
    local resultado=1

    for ((i=1; i<=n; i++)); do
        resultado=$((resultado * i))
    done

    echo $resultado
}

for num in 5 10 12; do
    factorial=$(calcular_factorial $num)
    echo "Factorial de $num = $factorial"
done
echo ""

# 14. EJERCICIO: Secuencia de Fibonacci
echo "--- 14. Ejercicio: Secuencia de Fibonacci ---"
n=15
a=0
b=1

echo -n "Primeros $n números de Fibonacci: "
for ((i=0; i<n; i++)); do
    echo -n "$a "
    siguiente=$((a + b))
    a=$b
    b=$siguiente
done
echo ""
echo ""

# 15. EJERCICIO: Patrón de asteriscos
echo "--- 15. Ejercicio: Patrón de Asteriscos ---"
altura=5

echo "Triángulo:"
for ((i=1; i<=altura; i++)); do
    for ((j=1; j<=i; j++)); do
        echo -n "* "
    done
    echo ""
done
echo ""

echo "Pirámide:"
for ((i=1; i<=altura; i++)); do
    # Espacios
    for ((j=i; j<altura; j++)); do
        echo -n " "
    done
    # Asteriscos
    for ((j=1; j<=2*i-1; j++)); do
        echo -n "*"
    done
    echo ""
done
echo ""

# 16. EJERCICIO: Leer archivo línea por línea
echo "--- 16. Ejercicio: Procesar Archivo Línea por Línea ---"
if [ -f "01_variables_y_tipos.sh" ]; then
    lineas=0
    while IFS= read -r linea; do
        ((lineas++))
        # Contar solo líneas que no estén vacías ni sean comentarios
        if [[ ! -z "$linea" ]] && [[ ! "$linea" =~ ^[[:space:]]*# ]]; then
            ((codigo++))
        fi
    done < "01_variables_y_tipos.sh"
    echo "Líneas totales en 01_variables_y_tipos.sh: $lineas"
fi
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "💡 TIPS:"
echo "   - For es mejor para rangos conocidos"
echo "   - While es mejor para condiciones dinámicas"
echo "   - Until es lo contrario de while (ejecuta hasta que sea verdadero)"
echo "   - Usa break para salir completamente del bucle"
echo "   - Usa continue para saltar a la siguiente iteración"
echo "   - ((i++)) es más eficiente que i=\$((i+1))"
