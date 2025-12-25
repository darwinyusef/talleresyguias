# Multi-stage build para crear imagen mínima

# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Instalar dependencias de build
RUN apk add --no-cache git make

# Copiar módulos primero (caching de dependencias)
COPY go.mod go.sum ./
RUN go mod download

# Copiar código fuente
COPY . .

# Build del binario
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w -X main.version=$(git describe --tags --always --dirty 2>/dev/null || echo dev)" \
    -o mycli .

# Stage 2: Runtime (imagen minimal)
FROM scratch

# Copiar binario desde builder
COPY --from=builder /app/mycli /mycli

# Copiar certificados SSL (necesario para HTTPS)
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Usuario no-root (seguridad)
USER 1000:1000

# Entrypoint
ENTRYPOINT ["/mycli"]

# Comando por defecto
CMD ["--help"]

# Labels (metadata)
LABEL org.opencontainers.image.title="mycli"
LABEL org.opencontainers.image.description="Mi CLI de ejemplo en Go"
LABEL org.opencontainers.image.source="https://github.com/tuuser/mycli"
LABEL org.opencontainers.image.licenses="MIT"
