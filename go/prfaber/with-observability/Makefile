.PHONY: help start stop restart logs build run clean test docker-up docker-down

help:
	@echo "Comandos disponibles:"
	@echo "  make start        - Levantar el stack completo (Docker + API)"
	@echo "  make stop         - Detener todos los servicios"
	@echo "  make restart      - Reiniciar todos los servicios"
	@echo "  make logs         - Ver logs de todos los servicios Docker"
	@echo "  make build        - Compilar la aplicación"
	@echo "  make run          - Ejecutar la aplicación"
	@echo "  make clean        - Limpiar archivos generados"
	@echo "  make docker-up    - Levantar solo servicios Docker"
	@echo "  make docker-down  - Detener servicios Docker"
	@echo "  make test         - Ejecutar tests"

docker-up:
	docker-compose up -d
	@echo "Servicios Docker iniciados"
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3001 (admin/admin)"
	@echo "Jaeger: http://localhost:16686"

docker-down:
	docker-compose down

start: docker-up
	@echo "Esperando que los servicios estén listos..."
	@sleep 5
	@echo "Iniciando la aplicación..."
	go run main.go

stop:
	@echo "Deteniendo servicios..."
	docker-compose down
	@pkill -f "go run main.go" || true

restart: stop start

logs:
	docker-compose logs -f

build:
	go build -o crud-fiber-observability main.go

run:
	go run main.go

clean:
	rm -f crud-fiber-observability
	rm -f logs/*.log logs/*.json
	docker-compose down -v

test:
	go test -v ./...

install-deps:
	go mod download
	go mod tidy
