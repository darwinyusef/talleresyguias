#!/bin/bash

################################################################################
# SCRIPT 5: MANEJO DE ARCHIVOS Y E/S (INPUT/OUTPUT)
################################################################################
# Temas cubiertos:
# - Lectura y escritura de archivos
# - Redirección (>, >>, <, 2>, &>)
# - Pipes (|)
# - Here documents (<<)
# - Here strings (<<<)
# - Lectura de input del usuario
# - Procesamiento de archivos de texto
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 5: MANEJO DE ARCHIVOS Y E/S"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Directorio temporal para ejercicios
TEMP_DIR="/tmp/bash_ejercicios"
mkdir -p "$TEMP_DIR"

# 1. ESCRITURA BÁSICA A ARCHIVO
echo "--- 1. Escritura a Archivo ---"
echo "Esta es la primera línea" > "$TEMP_DIR/archivo1.txt"
echo "Esta es la segunda línea" >> "$TEMP_DIR/archivo1.txt"
echo "Esta es la tercera línea" >> "$TEMP_DIR/archivo1.txt"

echo "Archivo creado: $TEMP_DIR/archivo1.txt"
cat "$TEMP_DIR/archivo1.txt"
echo ""

# 2. LECTURA DE ARCHIVO LÍNEA POR LÍNEA
echo "--- 2. Lectura Línea por Línea ---"
echo "Leyendo el archivo anterior:"
while IFS= read -r linea; do
    echo "  → $linea"
done < "$TEMP_DIR/archivo1.txt"
echo ""

# 3. REDIRECCIÓN DE ERRORES
echo "--- 3. Redirección de Errores ---"
# Redirigir stdout y stderr a archivos diferentes
ls /existente /noexiste > "$TEMP_DIR/stdout.txt" 2> "$TEMP_DIR/stderr.txt"

echo "Contenido de stdout:"
cat "$TEMP_DIR/stdout.txt" 2>/dev/null || echo "  (vacío o sin permisos)"

echo "Contenido de stderr:"
cat "$TEMP_DIR/stderr.txt"
echo ""

# Redirigir ambos al mismo archivo
ls /existente /noexiste &> "$TEMP_DIR/combined.txt"
echo "Contenido combinado:"
cat "$TEMP_DIR/combined.txt"
echo ""

# 4. HERE DOCUMENTS
echo "--- 4. Here Documents ---"
cat > "$TEMP_DIR/multi_linea.txt" << 'EOF'
Este es un documento
de múltiples líneas
creado con heredoc.

Puede contener variables: $HOME
Y comandos: $(date)
EOF

echo "Archivo creado con heredoc:"
cat "$TEMP_DIR/multi_linea.txt"
echo ""

# Here document con expansión de variables
NOMBRE="Usuario"
cat > "$TEMP_DIR/con_variables.txt" << EOF
Hola, $NOMBRE!
Tu directorio home es: $HOME
Fecha actual: $(date +%Y-%m-%d)
EOF

echo "Heredoc con expansión:"
cat "$TEMP_DIR/con_variables.txt"
echo ""

# 5. HERE STRINGS
echo "--- 5. Here Strings ---"
# Pasar string directamente a stdin
read palabra1 palabra2 palabra3 <<< "uno dos tres"
echo "Palabras leídas: $palabra1, $palabra2, $palabra3"

# Útil para procesar strings
tr 'a-z' 'A-Z' <<< "convertir a mayúsculas"
echo ""

# 6. PIPES (TUBERÍAS)
echo "--- 6. Pipes ---"
echo "Archivos .sh ordenados por tamaño:"
ls -lh *.sh 2>/dev/null | grep "^-" | awk '{print $5, $9}' | sort -h
echo ""

# 7. LECTURA DE INPUT DEL USUARIO
echo "--- 7. Lectura de Input ---"
# Simulación de input (en uso real esperaría entrada del usuario)
echo "Ejemplo de lectura de input:"
echo '  read -p "Tu nombre: " nombre'
echo '  echo "Hola, $nombre"'
echo ""

# Lectura con timeout
echo "Lectura con timeout (simulado):"
if echo "respuesta" | read -t 5 respuesta 2>/dev/null; then
    echo "  Respuesta recibida: $respuesta"
fi
echo ""

# 8. PROCESAMIENTO DE ARCHIVOS CSV
echo "--- 8. Procesamiento de CSV ---"
cat > "$TEMP_DIR/datos.csv" << 'EOF'
nombre,edad,ciudad
Juan,25,Madrid
Ana,30,Barcelona
Pedro,28,Valencia
María,32,Sevilla
EOF

echo "Datos del CSV:"
cat "$TEMP_DIR/datos.csv"
echo ""

echo "Procesando CSV:"
while IFS=',' read -r nombre edad ciudad; do
    if [ "$nombre" != "nombre" ]; then  # Saltar encabezado
        echo "  $nombre tiene $edad años y vive en $ciudad"
    fi
done < "$TEMP_DIR/datos.csv"
echo ""

# 9. CONTAR LÍNEAS, PALABRAS, CARACTERES
echo "--- 9. Estadísticas de Archivo ---"
archivo="$TEMP_DIR/datos.csv"
lineas=$(wc -l < "$archivo")
palabras=$(wc -w < "$archivo")
caracteres=$(wc -c < "$archivo")

echo "Estadísticas de $archivo:"
echo "  Líneas: $lineas"
echo "  Palabras: $palabras"
echo "  Caracteres: $caracteres"
echo ""

# 10. BÚSQUEDA Y FILTRADO
echo "--- 10. Búsqueda con grep ---"
cat > "$TEMP_DIR/logs.txt" << 'EOF'
[INFO] Aplicación iniciada
[ERROR] Fallo en conexión a base de datos
[WARNING] Memoria baja
[INFO] Procesando solicitud
[ERROR] Timeout en respuesta
[INFO] Operación completada
EOF

echo "Logs originales:"
cat "$TEMP_DIR/logs.txt"
echo ""

echo "Solo errores:"
grep "ERROR" "$TEMP_DIR/logs.txt"
echo ""

echo "Contar errores:"
grep -c "ERROR" "$TEMP_DIR/logs.txt"
echo ""

# 11. EJERCICIO: Procesador de logs
echo "--- 11. Ejercicio: Análisis de Logs ---"
analizar_logs() {
    local archivo=$1

    local total=$(wc -l < "$archivo")
    local errores=$(grep -c "ERROR" "$archivo")
    local warnings=$(grep -c "WARNING" "$archivo")
    local info=$(grep -c "INFO" "$archivo")

    echo "Análisis de $archivo:"
    echo "  Total de líneas: $total"
    echo "  Errores: $errores"
    echo "  Advertencias: $warnings"
    echo "  Informativos: $info"
}

analizar_logs "$TEMP_DIR/logs.txt"
echo ""

# 12. EJERCICIO: Backup de archivos
echo "--- 12. Ejercicio: Sistema de Backup ---"
hacer_backup() {
    local origen=$1
    local destino="${TEMP_DIR}/backup"

    mkdir -p "$destino"

    if [ -f "$origen" ]; then
        local timestamp=$(date +%Y%m%d_%H%M%S)
        local nombre_archivo=$(basename "$origen")
        local backup_file="${destino}/${nombre_archivo}.${timestamp}.bak"

        cp "$origen" "$backup_file"
        echo "✓ Backup creado: $backup_file"
        return 0
    else
        echo "✗ Error: Archivo no encontrado: $origen"
        return 1
    fi
}

hacer_backup "$TEMP_DIR/datos.csv"
hacer_backup "$TEMP_DIR/logs.txt"
echo ""

echo "Backups creados:"
ls -lh "${TEMP_DIR}/backup/"
echo ""

# 13. EJERCICIO: Merge de archivos
echo "--- 13. Ejercicio: Combinar Archivos ---"
echo "Archivo 1" > "$TEMP_DIR/parte1.txt"
echo "Línea 1 del archivo 1" >> "$TEMP_DIR/parte1.txt"
echo "Línea 2 del archivo 1" >> "$TEMP_DIR/parte1.txt"

echo "Archivo 2" > "$TEMP_DIR/parte2.txt"
echo "Línea 1 del archivo 2" >> "$TEMP_DIR/parte2.txt"
echo "Línea 2 del archivo 2" >> "$TEMP_DIR/parte2.txt"

# Método 1: Concatenación simple
cat "$TEMP_DIR/parte1.txt" "$TEMP_DIR/parte2.txt" > "$TEMP_DIR/combinado.txt"

echo "Archivos combinados:"
cat "$TEMP_DIR/combinado.txt"
echo ""

# 14. EJERCICIO: Filtrado y transformación
echo "--- 14. Ejercicio: Procesamiento de Texto ---"
cat > "$TEMP_DIR/texto.txt" << 'EOF'
El rápido zorro marrón
salta sobre el perro perezoso
en un día soleado
EOF

echo "Texto original:"
cat "$TEMP_DIR/texto.txt"
echo ""

echo "Convertido a mayúsculas:"
tr 'a-z' 'A-Z' < "$TEMP_DIR/texto.txt"
echo ""

echo "Reemplazar 'perro' por 'gato':"
sed 's/perro/gato/g' "$TEMP_DIR/texto.txt"
echo ""

echo "Solo líneas que contienen 'el':"
grep "el" "$TEMP_DIR/texto.txt"
echo ""

# 15. EJERCICIO: Ordenar y eliminar duplicados
echo "--- 15. Ejercicio: Ordenar y Deduplicar ---"
cat > "$TEMP_DIR/numeros.txt" << 'EOF'
5
2
8
2
1
9
5
3
8
1
EOF

echo "Números originales:"
cat "$TEMP_DIR/numeros.txt"
echo ""

echo "Ordenados sin duplicados:"
sort -n "$TEMP_DIR/numeros.txt" | uniq
echo ""

# 16. EJERCICIO: Generador de reportes
echo "--- 16. Ejercicio: Generador de Reportes ---"
generar_reporte() {
    local archivo_salida="$TEMP_DIR/reporte.txt"

    {
        echo "╔════════════════════════════════════════════════════════╗"
        echo "║           REPORTE DEL SISTEMA                          ║"
        echo "╚════════════════════════════════════════════════════════╝"
        echo ""
        echo "Fecha: $(date)"
        echo "Usuario: $USER"
        echo "Hostname: $(hostname)"
        echo ""
        echo "--- Archivos en $TEMP_DIR ---"
        ls -lh "$TEMP_DIR" | tail -n +2
        echo ""
        echo "--- Uso de disco ---"
        df -h "$TEMP_DIR" | tail -n 1
        echo ""
        echo "════════════════════════════════════════════════════════"
    } > "$archivo_salida"

    echo "✓ Reporte generado: $archivo_salida"
    cat "$archivo_salida"
}

generar_reporte
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "📁 Archivos creados en: $TEMP_DIR"
echo ""
echo "💡 TIPS:"
echo "   - '>' sobrescribe, '>>' añade al final"
echo "   - '2>' redirige stderr, '&>' redirige todo"
echo "   - 'command < file' usa file como entrada"
echo "   - '|' conecta la salida de un comando con la entrada de otro"
echo "   - Usa IFS= read -r para leer líneas preservando espacios"
echo "   - '<<' crea documentos multi-línea (heredoc)"
echo "   - '<<<' pasa strings directamente (herestring)"
