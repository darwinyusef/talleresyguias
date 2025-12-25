#!/usr/bin/env bash

# Script de instalación automática de MyCLI
# Uso: curl -sSL https://example.com/install.sh | bash

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
BINARY_NAME="mycli"
REPO="tuuser/mycli"
INSTALL_DIR="${INSTALL_DIR:-$HOME/bin}"
GITHUB_URL="https://github.com/${REPO}"
RELEASES_URL="${GITHUB_URL}/releases"

# Funciones
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Detectar OS y arquitectura
detect_platform() {
    local os=$(uname -s | tr '[:upper:]' '[:lower:]')
    local arch=$(uname -m)

    case "$os" in
        linux)
            OS="linux"
            ;;
        darwin)
            OS="darwin"
            ;;
        mingw*|msys*|cygwin*)
            OS="windows"
            ;;
        *)
            error "Sistema operativo no soportado: $os"
            ;;
    esac

    case "$arch" in
        x86_64|amd64)
            ARCH="amd64"
            ;;
        aarch64|arm64)
            ARCH="arm64"
            ;;
        *)
            error "Arquitectura no soportada: $arch"
            ;;
    esac

    PLATFORM="${OS}-${ARCH}"
}

# Obtener última versión
get_latest_release() {
    log "Obteniendo última versión..."

    # Intenta obtener de GitHub API
    if command -v curl &> /dev/null; then
        VERSION=$(curl -s "${RELEASES_URL}/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    elif command -v wget &> /dev/null; then
        VERSION=$(wget -qO- "${RELEASES_URL}/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    else
        error "Se requiere curl o wget"
    fi

    if [ -z "$VERSION" ]; then
        warning "No se pudo obtener la versión, usando 'latest'"
        VERSION="latest"
    fi

    log "Versión: ${VERSION}"
}

# Descargar binario
download_binary() {
    local download_url
    local tmp_dir=$(mktemp -d)
    local archive_name="${BINARY_NAME}-${PLATFORM}"

    if [ "$OS" = "windows" ]; then
        archive_name="${archive_name}.zip"
    else
        archive_name="${archive_name}.tar.gz"
    fi

    if [ "$VERSION" = "latest" ]; then
        download_url="${RELEASES_URL}/latest/download/${archive_name}"
    else
        download_url="${RELEASES_URL}/download/${VERSION}/${archive_name}"
    fi

    log "Descargando de: ${download_url}"

    cd "$tmp_dir"

    if command -v curl &> /dev/null; then
        curl -sSL -o "$archive_name" "$download_url" || error "Error al descargar"
    elif command -v wget &> /dev/null; then
        wget -q -O "$archive_name" "$download_url" || error "Error al descargar"
    fi

    log "Extrayendo archivo..."

    if [ "$OS" = "windows" ]; then
        unzip -q "$archive_name" || error "Error al extraer"
        BINARY_PATH="${BINARY_NAME}.exe"
    else
        tar -xzf "$archive_name" || error "Error al extraer"
        BINARY_PATH="${BINARY_NAME}-${PLATFORM}"
    fi

    # Verificar que el binario existe
    if [ ! -f "$BINARY_PATH" ]; then
        error "Binario no encontrado después de la extracción"
    fi

    log "✓ Descarga completada"
    echo "$tmp_dir/$BINARY_PATH"
}

# Instalar binario
install_binary() {
    local binary_path=$1

    log "Instalando en ${INSTALL_DIR}..."

    # Crear directorio si no existe
    mkdir -p "$INSTALL_DIR"

    # Copiar binario
    cp "$binary_path" "${INSTALL_DIR}/${BINARY_NAME}"
    chmod +x "${INSTALL_DIR}/${BINARY_NAME}"

    log "✓ Instalación completada"
}

# Verificar PATH
check_path() {
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        warning "${INSTALL_DIR} no está en tu PATH"
        echo ""
        echo "Agrega esta línea a tu ~/.bashrc o ~/.zshrc:"
        echo "  export PATH=\"\$PATH:${INSTALL_DIR}\""
        echo ""
    fi
}

# Verificar instalación
verify_installation() {
    if command -v "$BINARY_NAME" &> /dev/null; then
        log "Verificando instalación..."
        "$BINARY_NAME" version
        echo ""
        log "🎉 ${BINARY_NAME} instalado correctamente!"
    else
        warning "El comando '${BINARY_NAME}' no está disponible aún"
        echo "Ejecuta: export PATH=\"\$PATH:${INSTALL_DIR}\""
    fi
}

# Main
main() {
    echo "=================================="
    echo "  MyCLI - Instalador Automático"
    echo "=================================="
    echo ""

    detect_platform
    log "Plataforma detectada: ${PLATFORM}"

    get_latest_release

    local binary_path=$(download_binary)

    install_binary "$binary_path"

    # Limpiar archivos temporales
    rm -rf "$(dirname "$binary_path")"

    check_path
    verify_installation

    echo ""
    echo "Para desinstalar: rm ${INSTALL_DIR}/${BINARY_NAME}"
}

# Ejecutar
main
