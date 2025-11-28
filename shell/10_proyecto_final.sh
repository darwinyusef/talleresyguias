#!/bin/bash

################################################################################
# SCRIPT 10: PROYECTO FINAL - SISTEMA DE GESTIÓN DE TAREAS
################################################################################
# Proyecto integrador que combina todos los conceptos aprendidos:
# - Variables y arrays
# - Condicionales y bucles
# - Funciones
# - Manejo de archivos
# - Expresiones regulares
# - Procesos y señales
# - Operaciones aritméticas
# - Debugging y manejo de errores
################################################################################

# Configuración estricta
set -euo pipefail

################################################################################
# CONFIGURACIÓN Y VARIABLES GLOBALES
################################################################################

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly VERSION="1.0.0"
readonly DATA_DIR="${HOME}/.todo_bash"
readonly TODO_FILE="${DATA_DIR}/tareas.json"
readonly LOG_FILE="${DATA_DIR}/todo.log"

# Colores para output
readonly COLOR_RESET="\033[0m"
readonly COLOR_RED="\033[0;31m"
readonly COLOR_GREEN="\033[0;32m"
readonly COLOR_YELLOW="\033[0;33m"
readonly COLOR_BLUE="\033[0;34m"
readonly COLOR_CYAN="\033[0;36m"

# Prioridades
declare -A PRIORIDADES=(
    [1]="🔴 ALTA"
    [2]="🟡 MEDIA"
    [3]="🟢 BAJA"
)

################################################################################
# FUNCIONES DE LOGGING
################################################################################

log_info() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [INFO] $*" >> "$LOG_FILE"
}

log_error() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [ERROR] $*" >> "$LOG_FILE"
    echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $*" >&2
}

log_success() {
    echo -e "${COLOR_GREEN}✓${COLOR_RESET} $*"
}

log_warning() {
    echo -e "${COLOR_YELLOW}⚠${COLOR_RESET} $*"
}

################################################################################
# INICIALIZACIÓN
################################################################################

inicializar() {
    # Crear directorio de datos si no existe
    if [ ! -d "$DATA_DIR" ]; then
        mkdir -p "$DATA_DIR"
        log_info "Directorio de datos creado: $DATA_DIR"
    fi

    # Crear archivo de tareas si no existe
    if [ ! -f "$TODO_FILE" ]; then
        echo "[]" > "$TODO_FILE"
        log_info "Archivo de tareas creado: $TODO_FILE"
    fi

    # Crear archivo de log si no existe
    if [ ! -f "$LOG_FILE" ]; then
        touch "$LOG_FILE"
    fi
}

################################################################################
# FUNCIONES DE GESTIÓN DE TAREAS
################################################################################

# Agregar nueva tarea
agregar_tarea() {
    local descripcion="$1"
    local prioridad="${2:-2}"  # Por defecto: media

    # Validación
    if [ -z "$descripcion" ]; then
        log_error "La descripción no puede estar vacía"
        return 1
    fi

    if ! [[ "$prioridad" =~ ^[1-3]$ ]]; then
        log_error "Prioridad inválida. Usa 1 (alta), 2 (media) o 3 (baja)"
        return 1
    fi

    # Generar ID único
    local id=$(date +%s)$(( RANDOM % 1000 ))
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Crear tarea en formato JSON simplificado
    local nueva_tarea="ID:${id}|DESC:${descripcion}|PRI:${prioridad}|FECHA:${timestamp}|ESTADO:pendiente"

    # Agregar al archivo
    echo "$nueva_tarea" >> "$TODO_FILE"

    log_info "Tarea agregada: $descripcion (ID: $id)"
    log_success "Tarea agregada con ID: $id"
    return 0
}

# Listar todas las tareas
listar_tareas() {
    local filtro="${1:-todos}"  # todos, pendiente, completada

    if [ ! -s "$TODO_FILE" ]; then
        echo "No hay tareas registradas."
        return 0
    fi

    echo ""
    echo -e "${COLOR_CYAN}╔════════════════════════════════════════════════════════════╗${COLOR_RESET}"
    echo -e "${COLOR_CYAN}║              LISTA DE TAREAS                               ║${COLOR_RESET}"
    echo -e "${COLOR_CYAN}╚════════════════════════════════════════════════════════════╝${COLOR_RESET}"
    echo ""

    local contador=0

    while IFS= read -r linea; do
        # Parsear la línea
        local id=$(echo "$linea" | grep -oP 'ID:\K[^|]+')
        local desc=$(echo "$linea" | grep -oP 'DESC:\K[^|]+')
        local pri=$(echo "$linea" | grep -oP 'PRI:\K[^|]+')
        local fecha=$(echo "$linea" | grep -oP 'FECHA:\K[^|]+')
        local estado=$(echo "$linea" | grep -oP 'ESTADO:\K[^|]+')

        # Aplicar filtro
        if [ "$filtro" != "todos" ] && [ "$estado" != "$filtro" ]; then
            continue
        fi

        ((contador++))

        # Mostrar tarea
        local prioridad_texto="${PRIORIDADES[$pri]:-🟢 BAJA}"
        local estado_color=""
        local estado_icono=""

        if [ "$estado" = "completada" ]; then
            estado_color="$COLOR_GREEN"
            estado_icono="✓"
        else
            estado_color="$COLOR_YELLOW"
            estado_icono="○"
        fi

        echo -e "[$id] $prioridad_texto ${estado_color}${estado_icono}${COLOR_RESET} $desc"
        echo "      Creada: $fecha | Estado: $estado"
        echo ""
    done < "$TODO_FILE"

    if [ $contador -eq 0 ]; then
        echo "No hay tareas que coincidan con el filtro: $filtro"
    else
        echo "Total: $contador tarea(s)"
    fi

    echo ""
}

# Marcar tarea como completada
completar_tarea() {
    local id=$1

    if [ -z "$id" ]; then
        log_error "Debes especificar el ID de la tarea"
        return 1
    fi

    # Buscar y actualizar la tarea
    local temp_file="${TODO_FILE}.tmp"
    local encontrada=false

    while IFS= read -r linea; do
        if [[ "$linea" =~ ID:${id}\| ]]; then
            # Cambiar estado a completada
            linea=$(echo "$linea" | sed 's/ESTADO:[^|]*/ESTADO:completada/')
            encontrada=true
        fi
        echo "$linea" >> "$temp_file"
    done < "$TODO_FILE"

    mv "$temp_file" "$TODO_FILE"

    if $encontrada; then
        log_info "Tarea $id marcada como completada"
        log_success "Tarea $id marcada como completada"
        return 0
    else
        log_error "No se encontró tarea con ID: $id"
        return 1
    fi
}

# Eliminar tarea
eliminar_tarea() {
    local id=$1

    if [ -z "$id" ]; then
        log_error "Debes especificar el ID de la tarea"
        return 1
    fi

    # Crear archivo temporal sin la tarea
    local temp_file="${TODO_FILE}.tmp"
    local encontrada=false

    while IFS= read -r linea; do
        if [[ ! "$linea" =~ ID:${id}\| ]]; then
            echo "$linea" >> "$temp_file"
        else
            encontrada=true
        fi
    done < "$TODO_FILE"

    mv "$temp_file" "$TODO_FILE"

    if $encontrada; then
        log_info "Tarea $id eliminada"
        log_success "Tarea $id eliminada"
        return 0
    else
        log_error "No se encontró tarea con ID: $id"
        return 1
    fi
}

# Buscar tareas
buscar_tareas() {
    local termino="$1"

    if [ -z "$termino" ]; then
        log_error "Debes especificar un término de búsqueda"
        return 1
    fi

    echo ""
    echo -e "${COLOR_CYAN}Buscando: '$termino'${COLOR_RESET}"
    echo ""

    local contador=0

    while IFS= read -r linea; do
        if echo "$linea" | grep -iq "$termino"; then
            local id=$(echo "$linea" | grep -oP 'ID:\K[^|]+')
            local desc=$(echo "$linea" | grep -oP 'DESC:\K[^|]+')
            local estado=$(echo "$linea" | grep -oP 'ESTADO:\K[^|]+')

            ((contador++))
            echo "[$id] $desc ($estado)"
        fi
    done < "$TODO_FILE"

    if [ $contador -eq 0 ]; then
        echo "No se encontraron tareas que coincidan con '$termino'"
    else
        echo ""
        echo "Encontradas: $contador tarea(s)"
    fi

    echo ""
}

# Estadísticas
mostrar_estadisticas() {
    local total=0
    local completadas=0
    local pendientes=0
    local alta=0
    local media=0
    local baja=0

    while IFS= read -r linea; do
        ((total++))

        local estado=$(echo "$linea" | grep -oP 'ESTADO:\K[^|]+')
        local pri=$(echo "$linea" | grep -oP 'PRI:\K[^|]+')

        if [ "$estado" = "completada" ]; then
            ((completadas++))
        else
            ((pendientes++))
        fi

        case $pri in
            1) ((alta++)) ;;
            2) ((media++)) ;;
            3) ((baja++)) ;;
        esac
    done < "$TODO_FILE"

    echo ""
    echo -e "${COLOR_CYAN}╔════════════════════════════════════════════════════════════╗${COLOR_RESET}"
    echo -e "${COLOR_CYAN}║              ESTADÍSTICAS                                  ║${COLOR_RESET}"
    echo -e "${COLOR_CYAN}╚════════════════════════════════════════════════════════════╝${COLOR_RESET}"
    echo ""
    echo "Total de tareas:     $total"
    echo ""
    echo -e "${COLOR_GREEN}Completadas:${COLOR_RESET}         $completadas"
    echo -e "${COLOR_YELLOW}Pendientes:${COLOR_RESET}          $pendientes"
    echo ""
    echo "Por prioridad:"
    echo "  🔴 Alta:            $alta"
    echo "  🟡 Media:           $media"
    echo "  🟢 Baja:            $baja"

    if [ $total -gt 0 ]; then
        local porcentaje=$((completadas * 100 / total))
        echo ""
        echo "Progreso: $porcentaje%"

        # Barra de progreso
        local barra_llena=$((porcentaje / 2))
        local barra_vacia=$((50 - barra_llena))

        echo -n "["
        for ((i=0; i<barra_llena; i++)); do echo -n "█"; done
        for ((i=0; i<barra_vacia; i++)); do echo -n "░"; done
        echo "]"
    fi

    echo ""
}

################################################################################
# AYUDA Y USO
################################################################################

mostrar_ayuda() {
    cat << EOF

${COLOR_CYAN}Sistema de Gestión de Tareas${COLOR_RESET} v${VERSION}

${COLOR_YELLOW}USO:${COLOR_RESET}
    $SCRIPT_NAME <comando> [opciones]

${COLOR_YELLOW}COMANDOS:${COLOR_RESET}
    add <descripción> [prioridad]   Agregar nueva tarea (prioridad: 1-3)
    list [filtro]                   Listar tareas (filtro: todos|pendiente|completada)
    complete <id>                   Marcar tarea como completada
    delete <id>                     Eliminar tarea
    search <término>                Buscar tareas
    stats                           Mostrar estadísticas
    help                            Mostrar esta ayuda

${COLOR_YELLOW}EJEMPLOS:${COLOR_RESET}
    $SCRIPT_NAME add "Comprar leche" 1
    $SCRIPT_NAME list pendiente
    $SCRIPT_NAME complete 1234567890123
    $SCRIPT_NAME search "reunión"
    $SCRIPT_NAME stats

${COLOR_YELLOW}PRIORIDADES:${COLOR_RESET}
    1 = 🔴 Alta
    2 = 🟡 Media (por defecto)
    3 = 🟢 Baja

EOF
}

################################################################################
# CLEANUP
################################################################################

cleanup() {
    # Realizar limpieza si es necesario
    :
}

trap cleanup EXIT

################################################################################
# MAIN
################################################################################

main() {
    inicializar

    # Verificar si se pasó un comando
    if [ $# -eq 0 ]; then
        mostrar_ayuda
        exit 0
    fi

    local comando=$1
    shift

    case $comando in
        add|agregar)
            if [ $# -lt 1 ]; then
                log_error "Uso: $SCRIPT_NAME add <descripción> [prioridad]"
                exit 1
            fi
            agregar_tarea "$1" "${2:-2}"
            ;;

        list|listar)
            listar_tareas "${1:-todos}"
            ;;

        complete|completar)
            if [ $# -lt 1 ]; then
                log_error "Uso: $SCRIPT_NAME complete <id>"
                exit 1
            fi
            completar_tarea "$1"
            ;;

        delete|eliminar)
            if [ $# -lt 1 ]; then
                log_error "Uso: $SCRIPT_NAME delete <id>"
                exit 1
            fi
            eliminar_tarea "$1"
            ;;

        search|buscar)
            if [ $# -lt 1 ]; then
                log_error "Uso: $SCRIPT_NAME search <término>"
                exit 1
            fi
            buscar_tareas "$1"
            ;;

        stats|estadisticas)
            mostrar_estadisticas
            ;;

        help|ayuda|-h|--help)
            mostrar_ayuda
            ;;

        *)
            log_error "Comando desconocido: $comando"
            echo ""
            mostrar_ayuda
            exit 1
            ;;
    esac
}

# Ejecutar main solo si el script se ejecuta directamente
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi

################################################################################
# FIN DEL PROYECTO
################################################################################

echo ""
echo "💡 CONCEPTOS UTILIZADOS EN ESTE PROYECTO:"
echo ""
echo "   ✓ Variables y arrays asociativos (PRIORIDADES)"
echo "   ✓ Condicionales y case statements"
echo "   ✓ Bucles while para procesar archivos"
echo "   ✓ Funciones modulares y reutilizables"
echo "   ✓ Manejo de archivos (lectura/escritura)"
echo "   ✓ Expresiones regulares (grep -oP)"
echo "   ✓ Manejo de señales (trap)"
echo "   ✓ Operaciones aritméticas (contadores, porcentajes)"
echo "   ✓ set -euo pipefail para robustez"
echo "   ✓ Logging y manejo de errores"
echo "   ✓ Validación de entrada"
echo "   ✓ Colorización de output"
echo "   ✓ Argumentos de línea de comandos"
echo ""
echo "✅ Has completado todos los ejercicios de Bash!"
