#!/bin/bash

################################################################################
# SCRIPT 7: PROCESOS, JOBS Y SEÑALES
################################################################################
# Temas cubiertos:
# - Procesos en background (&)
# - Jobs (jobs, fg, bg)
# - Señales (trap, kill)
# - Subshells
# - Ejecución paralela
# - Control de procesos
# - Variables de proceso ($!, $?, $$)
################################################################################

echo "═══════════════════════════════════════════════════════════"
echo "  EJERCICIO 7: PROCESOS, JOBS Y SEÑALES"
echo "═══════════════════════════════════════════════════════════"
echo ""

# 1. INFORMACIÓN DE PROCESO ACTUAL
echo "--- 1. Información del Proceso ---"
echo "PID del script: $$"
echo "PID del proceso padre (PPID): $PPID"
echo "Usuario: $USER"
echo "Shell: $SHELL"
echo ""

# 2. EJECUCIÓN EN BACKGROUND
echo "--- 2. Procesos en Background ---"
proceso_largo() {
    echo "Proceso iniciado (PID: $$)"
    sleep 3
    echo "Proceso completado (PID: $$)"
}

# Ejecutar en background
proceso_largo &
PID_PROCESO=$!
echo "Proceso lanzado en background con PID: $PID_PROCESO"
echo "Esperando a que termine..."
wait $PID_PROCESO
echo "Código de salida: $?"
echo ""

# 3. MÚLTIPLES PROCESOS EN PARALELO
echo "--- 3. Ejecución Paralela ---"
tarea() {
    local id=$1
    local duracion=$2
    echo "  Tarea $id iniciada"
    sleep $duracion
    echo "  Tarea $id completada"
    return $id
}

echo "Lanzando 3 tareas en paralelo:"
tarea 1 2 &
PID1=$!
tarea 2 1 &
PID2=$!
tarea 3 3 &
PID3=$!

echo "Esperando a que todas las tareas terminen..."
wait $PID1 $PID2 $PID3
echo "Todas las tareas completadas"
echo ""

# 4. TRAP - MANEJO DE SEÑALES
echo "--- 4. Manejo de Señales con Trap ---"
# Crear función de limpieza
cleanup() {
    echo ""
    echo "🧹 Función de limpieza ejecutada"
    echo "   Señal recibida: $1"
    # Aquí podrías eliminar archivos temporales, cerrar conexiones, etc.
    exit 0
}

# Configurar trap para diferentes señales
trap 'cleanup SIGINT' SIGINT   # Ctrl+C
trap 'cleanup SIGTERM' SIGTERM # kill
trap 'echo "Script finalizado normalmente"' EXIT

echo "Trap configurado para SIGINT, SIGTERM y EXIT"
echo "(Presionar Ctrl+C probaría el trap, pero continuaremos...)"
echo ""

# 5. SUBSHELLS
echo "--- 5. Subshells ---"
VARIABLE="Valor original"
echo "Variable en shell principal: $VARIABLE"

# Subshell con ()
(
    VARIABLE="Valor en subshell"
    echo "Variable en subshell: $VARIABLE"
    exit 0
)

echo "Variable después de subshell: $VARIABLE (no cambió)"
echo ""

# Variables exportadas sí se heredan
export VAR_EXPORTADA="Valor exportado"
(
    echo "Variable exportada en subshell: $VAR_EXPORTADA"
)
echo ""

# 6. SUBSHELLS PARA CAMBIO DE DIRECTORIO
echo "--- 6. Subshells para Aislamiento ---"
echo "Directorio actual: $(pwd)"

# Cambiar directorio solo en subshell
(
    cd /tmp
    echo "Dentro de subshell: $(pwd)"
    ls -l bash_ejercicios 2>/dev/null | head -3
)

echo "Después de subshell: $(pwd) (no cambió)"
echo ""

# 7. EJERCICIO: Monitor de procesos
echo "--- 7. Ejercicio: Monitor de Procesos ---"
monitorear_proceso() {
    local nombre_proceso=$1
    local cuenta=$(ps aux | grep -v grep | grep -c "$nombre_proceso")

    echo "Procesos '$nombre_proceso' en ejecución: $cuenta"

    if [ $cuenta -gt 0 ]; then
        echo "Detalles:"
        ps aux | grep -v grep | grep "$nombre_proceso" | awk '{print "  PID: " $2 ", CPU: " $3 "%, MEM: " $4 "%, CMD: " $11}'
    fi
}

monitorear_proceso "bash"
echo ""

# 8. EJERCICIO: Ejecutor paralelo de tareas
echo "--- 8. Ejercicio: Ejecutor Paralelo ---"
ejecutar_paralelo() {
    local -a pids=()
    local -a comandos=("$@")

    echo "Ejecutando ${#comandos[@]} comandos en paralelo..."

    for cmd in "${comandos[@]}"; do
        eval "$cmd" &
        pids+=($!)
    done

    echo "PIDs: ${pids[@]}"

    # Esperar a todos
    for pid in "${pids[@]}"; do
        wait $pid
        echo "PID $pid completado con código: $?"
    done

    echo "Todas las tareas completadas"
}

ejecutar_paralelo "sleep 1 && echo 'Tarea A'" "sleep 2 && echo 'Tarea B'" "sleep 1 && echo 'Tarea C'"
echo ""

# 9. EJERCICIO: Sistema de timeouts
echo "--- 9. Ejercicio: Timeout para Comandos ---"
ejecutar_con_timeout() {
    local timeout=$1
    shift
    local comando="$@"

    # Ejecutar comando en background
    eval "$comando" &
    local pid=$!

    # Esperar con timeout
    local contador=0
    while kill -0 $pid 2>/dev/null; do
        if [ $contador -ge $timeout ]; then
            echo "⏱️  Timeout alcanzado, terminando proceso $pid"
            kill $pid 2>/dev/null
            wait $pid 2>/dev/null
            return 124  # Código estándar de timeout
        fi
        sleep 1
        ((contador++))
    done

    wait $pid
    return $?
}

echo "Comando rápido (timeout 5s):"
ejecutar_con_timeout 5 "sleep 2 && echo 'Completado a tiempo'"
echo "Resultado: $?"
echo ""

echo "Comando lento (timeout 3s):"
ejecutar_con_timeout 3 "sleep 10 && echo 'Esto no se verá'"
echo "Resultado: $?"
echo ""

# 10. EJERCICIO: Control de concurrencia
echo "--- 10. Ejercicio: Pool de Workers ---"
MAX_WORKERS=3

worker_pool() {
    local max_concurrent=$1
    shift
    local -a tareas=("$@")
    local activos=0
    local completados=0

    echo "Ejecutando ${#tareas[@]} tareas con máximo $max_concurrent workers"

    for tarea in "${tareas[@]}"; do
        # Esperar si llegamos al máximo
        while [ $activos -ge $max_concurrent ]; do
            wait -n 2>/dev/null  # Esperar a que termine cualquier proceso
            ((activos--))
            ((completados++))
        done

        # Lanzar nueva tarea
        (
            echo "  → Ejecutando: $tarea"
            eval "$tarea"
            echo "  ✓ Completado: $tarea"
        ) &

        ((activos++))
    done

    # Esperar a los últimos
    wait
    completados=$((completados + activos))

    echo "Pool completado: $completados tareas"
}

TAREAS=(
    "sleep 1"
    "sleep 2"
    "sleep 1"
    "sleep 2"
    "sleep 1"
)

worker_pool $MAX_WORKERS "${TAREAS[@]}"
echo ""

# 11. EJERCICIO: Sistema de logs con timestamp
echo "--- 11. Ejercicio: Logger con Proceso Background ---"
TEMP_DIR="/tmp/bash_ejercicios"
LOG_FILE="$TEMP_DIR/app.log"
mkdir -p "$TEMP_DIR"

# Función logger
logger_daemon() {
    local log_file=$1
    while IFS= read -r mensaje; do
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $mensaje" >> "$log_file"
    done
}

# Iniciar logger en background con named pipe
PIPE="$TEMP_DIR/log.pipe"
mkfifo "$PIPE" 2>/dev/null || true

logger_daemon "$LOG_FILE" < "$PIPE" &
LOGGER_PID=$!

# Función para escribir logs
log() {
    echo "$1" > "$PIPE"
}

echo "Logger iniciado (PID: $LOGGER_PID)"
log "Aplicación iniciada"
log "Procesando datos..."
sleep 1
log "Datos procesados exitosamente"
log "Aplicación finalizada"

# Cerrar logger
kill $LOGGER_PID 2>/dev/null
wait $LOGGER_PID 2>/dev/null

echo "Contenido del log:"
cat "$LOG_FILE"
rm -f "$PIPE"
echo ""

# 12. EJERCICIO: Reinicio automático de procesos
echo "--- 12. Ejercicio: Watchdog (Auto-restart) ---"
proceso_inestable() {
    echo "  Proceso iniciado (PID: $$)"
    sleep 2
    # Simular fallo aleatorio
    if [ $((RANDOM % 2)) -eq 0 ]; then
        echo "  ❌ Proceso falló"
        exit 1
    else
        echo "  ✅ Proceso completado"
        exit 0
    fi
}

watchdog() {
    local max_reintentos=5
    local reintentos=0

    while [ $reintentos -lt $max_reintentos ]; do
        echo "Intento $((reintentos + 1))/$max_reintentos"

        proceso_inestable
        local codigo=$?

        if [ $codigo -eq 0 ]; then
            echo "Proceso exitoso"
            return 0
        fi

        ((reintentos++))
        echo "Reintentando en 1 segundo..."
        sleep 1
    done

    echo "❌ Máximo de reintentos alcanzado"
    return 1
}

watchdog
echo ""

# 13. INFORMACIÓN DEL SISTEMA
echo "--- 13. Información del Sistema de Procesos ---"
echo "Procesos totales: $(ps aux | wc -l)"
echo "Procesos del usuario $USER: $(ps -u $USER | wc -l)"
echo "Load average: $(uptime | awk -F'load average:' '{print $2}')"
echo ""

echo "✅ Script completado exitosamente"
echo ""
echo "💡 TIPS:"
echo "   - & ejecuta comando en background"
echo "   - \$! contiene el PID del último proceso background"
echo "   - \$? contiene el código de salida del último comando"
echo "   - wait [PID] espera a que termine un proceso"
echo "   - trap 'comando' SIGNAL captura señales"
echo "   - kill -SIGNAL PID envía señales a procesos"
echo "   - () crea subshell, {} ejecuta en shell actual"
echo "   - Usa wait -n para esperar al siguiente que termine"
