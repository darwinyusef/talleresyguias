# Variables
BINARY_NAME=mycli
VERSION?=$(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
COMMIT=$(shell git rev-parse --short HEAD 2>/dev/null || echo "none")
DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
LDFLAGS=-ldflags "-X main.version=$(VERSION) -X main.commit=$(COMMIT) -X main.date=$(DATE) -s -w"

# Directorios
BUILD_DIR=build
DIST_DIR=dist

# Plataformas para cross-compilation
PLATFORMS=linux/amd64 linux/arm64 darwin/amd64 darwin/arm64 windows/amd64

.PHONY: all build clean install test build-all dist help

help: ## Muestra esta ayuda
	@echo "Targets disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

deps: ## Instala dependencias
	@echo "📦 Instalando dependencias..."
	go mod download
	go mod verify

build: deps ## Build para la plataforma actual
	@echo "🔨 Building $(BINARY_NAME) para $(shell go env GOOS)/$(shell go env GOARCH)..."
	go build $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) .
	@echo "✅ Binary creado en $(BUILD_DIR)/$(BINARY_NAME)"

build-all: clean deps ## Build para todas las plataformas
	@echo "🔨 Building para todas las plataformas..."
	@mkdir -p $(DIST_DIR)
	@$(foreach platform,$(PLATFORMS), \
		echo "Building $(platform)..."; \
		GOOS=$(word 1,$(subst /, ,$(platform))) \
		GOARCH=$(word 2,$(subst /, ,$(platform))) \
		go build $(LDFLAGS) \
		-o $(DIST_DIR)/$(BINARY_NAME)-$(word 1,$(subst /, ,$(platform)))-$(word 2,$(subst /, ,$(platform)))$(if $(filter windows,$(word 1,$(subst /, ,$(platform)))),.exe) . ; \
	)
	@echo "✅ Binarios creados en $(DIST_DIR)/"

dist: build-all ## Crea distribuciones comprimidas
	@echo "📦 Creando archivos de distribución..."
	@cd $(DIST_DIR) && \
	for file in mycli-*; do \
		if [[ $$file == *.exe ]]; then \
			zip $${file%.exe}.zip $$file; \
		else \
			tar -czf $$file.tar.gz $$file; \
		fi; \
		echo "  ✓ Creado: $$file"; \
	done
	@echo "✅ Distribuciones creadas en $(DIST_DIR)/"

install: build ## Instala el binario localmente
	@echo "📥 Instalando $(BINARY_NAME)..."
	@mkdir -p ~/bin
	@cp $(BUILD_DIR)/$(BINARY_NAME) ~/bin/
	@echo "✅ Instalado en ~/bin/$(BINARY_NAME)"
	@echo "💡 Asegúrate de que ~/bin esté en tu PATH"

clean: ## Limpia archivos de build
	@echo "🧹 Limpiando..."
	@rm -rf $(BUILD_DIR) $(DIST_DIR)
	@echo "✅ Limpieza completada"

test: ## Ejecuta tests
	@echo "🧪 Ejecutando tests..."
	go test -v ./...

run: build ## Build y ejecuta
	@echo "🚀 Ejecutando $(BINARY_NAME)..."
	@$(BUILD_DIR)/$(BINARY_NAME)

size: build ## Muestra el tamaño del binario
	@echo "📊 Tamaño del binario:"
	@ls -lh $(BUILD_DIR)/$(BINARY_NAME) | awk '{print "  " $$9 ": " $$5}'
	@file $(BUILD_DIR)/$(BINARY_NAME)

checksums: dist ## Genera checksums SHA256
	@echo "🔐 Generando checksums..."
	@cd $(DIST_DIR) && \
	shasum -a 256 *.tar.gz *.zip > SHA256SUMS 2>/dev/null || true
	@echo "✅ Checksums en $(DIST_DIR)/SHA256SUMS"

release: clean build-all dist checksums ## Crea un release completo
	@echo "🎉 Release $(VERSION) creado"
	@echo ""
	@echo "Archivos generados:"
	@ls -lh $(DIST_DIR)/
