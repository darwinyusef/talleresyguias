#!/bin/bash

################################################################################
# SCRIPT 9: DEBUGGING Y MANEJO DE ERRORES
################################################################################
# Temas cubiertos:
# - set -e, set -u, set -x, set -o pipefail
# - Manejo de errores con ||, &&
# - Exit codes
# - Funciones de logging
# - Debugging con PS4
# - errexit y error handling
# - Validación de entrada
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 9: DEBUGGING Y MANEJO DE ERRORES"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. EXIT CODES
echo "--- 1. Códigos de Salida (Exit Codes) ---"
comando_exitoso() {
    return 0  # Éxito
}

comando_fallido() {
    return 1  # Error
}

comando_exitoso
echo "Comando exitoso retornó: $?"

comando_fallido
echo "Comando fallido retornó: $?"

# Convención de códigos de salida
echo ""
echo "Convención de códigos:"
echo "  0   = Éxito"
echo "  1   = Error general"
echo "  2   = Uso incorrecto del comando"
echo "  126 = Comando no ejecutable"
echo "  127 = Comando no encontrado"
echo "  128+n = Terminado por señal n"
echo ""

# 2. OPERADORES && Y ||
echo "--- 2. Operadores && (AND) y || (OR) ---"
# && ejecuta si el anterior tuvo éxito
echo "Usando &&:"
true && echo "  Esto se ejecuta (true tuvo éxito)"
false && echo "  Esto NO se ejecuta (false falló)"
echo ""

# || ejecuta si el anterior falló
echo "Usando ||:"
true || echo "  Esto NO se ejecuta (true tuvo éxito)"
false || echo "  Esto se ejecuta (false falló)"
echo ""

# Combinación común
echo "Combinación &&/||:"
mkdir /tmp/test_dir 2>/dev/null && echo "  ✓ Directorio creado" || echo "  ℹ Directorio ya existe"
echo ""

# 3. SET -E (ERREXIT)
echo "--- 3. set -e (errexit) ---"
echo "Sin set -e, el script continúa después de errores"

demo_sin_set_e() {
    false
    echo "  Esta línea se ejecuta aunque false falló"
}

demo_sin_set_e
echo ""

echo "Con set -e, el script se detiene en el primer error"
echo "(No lo activamos aquí para continuar el tutorial)"
echo "Uso: set -e al inicio del script"
echo ""

# 4. SET -U (NOUNSET)
echo "--- 4. set -u (nounset) ---"
echo "Sin set -u, variables no definidas son vacías:"
echo "Variable no definida: '${VARIABLE_NO_DEFINIDA:-}'"
echo ""

echo "Con set -u, usar variables no definidas causa error"
echo "Uso: set -u al inicio del script"
echo "Mejor práctica: usar \${var:-default} para valores por defecto"
echo ""

# 5. SET -X (XTRACE)
echo "--- 5. set -x (xtrace) para debugging ---"
echo "Activando modo debug..."
set -x
suma=$((5 + 3))
multiplicacion=$((suma * 2))
set +x
echo "Debug desactivado"
echo "Resultado: $multiplicacion"
echo ""

# 6. SET -O PIPEFAIL
echo "--- 6. set -o pipefail ---"
echo "Sin pipefail:"
false | true
echo "  Código de salida: $? (solo ve el último comando del pipe)"
echo ""

echo "Con pipefail:"
set -o pipefail
false | true 2>/dev/null || echo "  Código de salida detectó el fallo en el pipe"
set +o pipefail
echo ""

# 7. CUSTOM PS4 PARA MEJOR DEBUGGING
echo "--- 7. PS4 Personalizado para Debugging ---"
echo "PS4 por defecto: '$PS4'"
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
echo "PS4 personalizado muestra archivo:línea:función"
echo ""

# 8. SISTEMA DE LOGGING
echo "--- 8. Sistema de Logging ---"
TEMP_DIR="/tmp/bash_ejercicios"
mkdir -p "$TEMP_DIR"
LOG_FILE="$TEMP_DIR/app.log"

# Niveles de log
readonly LOG_LEVEL_DEBUG=0
readonly LOG_LEVEL_INFO=1
readonly LOG_LEVEL_WARN=2
readonly LOG_LEVEL_ERROR=3

CURRENT_LOG_LEVEL=$LOG_LEVEL_INFO

log() {
    local level=$1
    shift
    local mensaje="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local level_name=""
    local color=""

    case $level in
        $LOG_LEVEL_DEBUG)
            level_name="DEBUG"
            color="\033[0;36m"  # Cyan
            ;;
        $LOG_LEVEL_INFO)
            level_name="INFO "
            color="\033[0;32m"  # Green
            ;;
        $LOG_LEVEL_WARN)
            level_name="WARN "
            color="\033[0;33m"  # Yellow
            ;;
        $LOG_LEVEL_ERROR)
            level_name="ERROR"
            color="\033[0;31m"  # Red
            ;;
    esac

    if [ $level -ge $CURRENT_LOG_LEVEL ]; then
        local log_message="[$timestamp] [$level_name] $mensaje"
        echo -e "${color}${log_message}\033[0m"
        echo "$log_message" >> "$LOG_FILE"
    fi
}

# Funciones helper
log_debug() { log $LOG_LEVEL_DEBUG "$@"; }
log_info()  { log $LOG_LEVEL_INFO "$@"; }
log_warn()  { log $LOG_LEVEL_WARN "$@"; }
log_error() { log $LOG_LEVEL_ERROR "$@"; }

# Prueba del sistema de logging
log_debug "Este es un mensaje DEBUG (no se ve con nivel INFO)"
log_info "Aplicación iniciada"
log_warn "Advertencia: uso de memoria alto"
log_error "Error al conectar con la base de datos"
echo ""

# 9. VALIDACIÓN DE ENTRADA
echo "--- 9. Validación de Entrada ---"
validar_numero() {
    local input=$1

    if [[ -z "$input" ]]; then
        log_error "Error: entrada vacía"
        return 1
    fi

    if ! [[ "$input" =~ ^[0-9]+$ ]]; then
        log_error "Error: '$input' no es un número válido"
        return 1
    fi

    log_info "Número válido: $input"
    return 0
}

validar_numero "123"
validar_numero "abc"
validar_numero ""
echo ""

# 10. MANEJO DE ERRORES EN FUNCIONES
echo "--- 10. Manejo de Errores en Funciones ---"
dividir() {
    local dividendo=$1
    local divisor=$2

    # Validaciones
    if [ $# -ne 2 ]; then
        log_error "Uso: dividir <dividendo> <divisor>"
        return 2
    fi

    if ! [[ "$dividendo" =~ ^[0-9]+$ ]] || ! [[ "$divisor" =~ ^[0-9]+$ ]]; then
        log_error "Ambos argumentos deben ser números"
        return 2
    fi

    if [ $divisor -eq 0 ]; then
        log_error "Error: división por cero"
        return 1
    fi

    local resultado=$((dividendo / divisor))
    echo $resultado
    return 0
}

echo "División 10 / 2:"
if resultado=$(dividir 10 2); then
    log_info "Resultado: $resultado"
fi
echo ""

echo "División 10 / 0:"
if ! resultado=$(dividir 10 0 2>&1); then
    log_error "La división falló como se esperaba"
fi
echo ""

# 11. EJERCICIO: Try-Catch simulado
echo "--- 11. Ejercicio: Simulación Try-Catch ---"
try() {
    [[ $- = *e* ]]; SAVED_OPT_E=$?
    set +e
}

catch() {
    export exception_code=$?
    (( SAVED_OPT_E )) && set +e
    return $exception_code
}

throw() {
    exit $1
}

# Ejemplo de uso
echo "Ejemplo de try-catch:"
(
    try
    (
        log_info "Intentando operación riesgosa..."
        false  # Simular fallo
        log_info "Esta línea no se ejecuta"
    )
    catch || {
        log_error "Capturado error con código: $exception_code"
    }
)
echo ""

# 12. EJERCICIO: Verificador de dependencias
echo "--- 12. Ejercicio: Verificador de Dependencias ---"
verificar_comando() {
    local comando=$1

    if command -v "$comando" &> /dev/null; then
        log_info "✓ $comando está instalado"
        return 0
    else
        log_error "✗ $comando NO está instalado"
        return 1
    fi
}

verificar_dependencias() {
    local all_ok=true

    for cmd in "$@"; do
        verificar_comando "$cmd" || all_ok=false
    done

    if $all_ok; then
        log_info "Todas las dependencias están instaladas"
        return 0
    else
        log_error "Faltan algunas dependencias"
        return 1
    fi
}

echo "Verificando dependencias:"
verificar_dependencias bash grep sed awk comando_inexistente
echo ""

# 13. EJERCICIO: Timeout y retry
echo "--- 13. Ejercicio: Retry con Backoff ---"
retry_con_backoff() {
    local max_intentos=$1
    local delay=$2
    shift 2
    local comando="$@"
    local intento=1

    while [ $intento -le $max_intentos ]; do
        log_info "Intento $intento/$max_intentos: $comando"

        if eval "$comando"; then
            log_info "✓ Comando exitoso"
            return 0
        fi

        if [ $intento -lt $max_intentos ]; then
            log_warn "Fallo. Reintentando en ${delay}s..."
            sleep $delay
            ((delay *= 2))  # Backoff exponencial
        fi

        ((intento++))
    done

    log_error "✗ Comando falló después de $max_intentos intentos"
    return 1
}

echo "Simulando comando que falla:"
CONTADOR=0
comando_flaky() {
    ((CONTADOR++))
    if [ $CONTADOR -lt 3 ]; then
        return 1
    fi
    echo "  Comando exitoso en intento $CONTADOR"
    return 0
}

retry_con_backoff 5 1 "comando_flaky"
echo ""

# 14. EJERCICIO: Stack trace
echo "--- 14. Ejercicio: Stack Trace ---"
print_stack_trace() {
    local frame=0
    echo "Stack trace:"
    while caller $frame; do
        ((frame++))
    done | while read line func file; do
        echo "  en $func() ($file:$line)"
    done
}

funcion_c() {
    log_error "Error en funcion_c"
    print_stack_trace
}

funcion_b() {
    funcion_c
}

funcion_a() {
    funcion_b
}

funcion_a
echo ""

# 15. EJERCICIO: Cleanup automático
echo "--- 15. Ejercicio: Cleanup Automático ---"
TEMP_FILES=()

crear_temp() {
    local temp_file=$(mktemp)
    TEMP_FILES+=("$temp_file")
    echo "$temp_file"
}

cleanup() {
    log_info "Ejecutando limpieza..."
    for file in "${TEMP_FILES[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
            log_info "  Eliminado: $file"
        fi
    done
}

# Registrar cleanup para ejecutar al salir
trap cleanup EXIT

# Crear algunos archivos temporales
temp1=$(crear_temp)
temp2=$(crear_temp)
log_info "Creados archivos temporales: $temp1, $temp2"
echo "Datos de prueba" > "$temp1"
echo "Más datos" > "$temp2"
echo ""

# 16. MEJORES PRÁCTICAS
echo "--- 16. Mejores Prácticas ---"
cat << 'EOF'
#!/bin/bash
# Template de script con mejores prácticas

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Variables globales
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Logging
log_error() { echo "[ERROR] $*" >&2; }
log_info()  { echo "[INFO] $*"; }

# Cleanup
cleanup() {
    # Limpieza aquí
    :
}
trap cleanup EXIT

# Validación de argumentos
if [ $# -lt 1 ]; then
    log_error "Uso: $SCRIPT_NAME <argumento>"
    exit 1
fi

# Main
main() {
    log_info "Iniciando script..."
    # Tu código aquí
}

main "$@"
EOF
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "📝 Log guardado en: $LOG_FILE"
echo ""
echo "💡 TIPS:"
echo "   - Usa 'set -euo pipefail' al inicio de scripts"
echo "   - Siempre valida entrada de usuario"
echo "   - Implementa logging para debugging"
echo "   - Usa trap para cleanup automático"
echo "   - Retorna códigos de error apropiados (0=ok, >0=error)"
echo "   - Usa && y || para control de flujo basado en éxito/fallo"
echo "   - set -x para debugging, set +x para desactivar"
echo "   - Personaliza PS4 para mejor output de debugging"
