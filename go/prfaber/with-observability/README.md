# CRUD API con Fiber y Stack Completo de Observabilidad

Este proyecto demuestra una implementación completa de una API REST CRUD construida con **Go Fiber** e integrada con un stack completo de observabilidad que incluye:

- **OpenTelemetry** para trazas distribuidas
- **Prometheus** para métricas
- **Grafana** para visualización
- **Loki** para agregación de logs
- **Jaeger** para visualización de trazas
- **Logs estructurados** con `slog` (biblioteca estándar de Go)

## Arquitectura de Observabilidad

```
┌─────────────┐
│  CRUD API   │
│   (Fiber)   │
└──────┬──────┘
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
┌──────────────┐                    ┌─────────────┐
│  Prometheus  │◄───────────────────┤   Metrics   │
│   (Métricas) │                    │  (Exporter) │
└──────┬───────┘                    └─────────────┘
       │
       ▼
┌──────────────┐                    ┌─────────────┐
│   Grafana    │◄───────────────────┤    Loki     │
│ (Dashboards) │                    │   (Logs)    │
└──────┬───────┘                    └──────▲──────┘
       │                                   │
       │                            ┌──────┴──────┐
       │                            │  Promtail   │
       │                            └─────────────┘
       │
       ▼
┌──────────────┐                    ┌─────────────┐
│    Jaeger    │◄───────────────────┤    OTLP     │
│   (Traces)   │                    │ Collector   │
└──────────────┘                    └─────────────┘
```

## Características

### 1. Trazas Distribuidas (Traces)
- OpenTelemetry OTLP exporter para enviar trazas
- Visualización en Jaeger UI
- Trazas de cada request HTTP con detalles completos
- Trazas de operaciones de base de datos
- Propagación de contexto entre servicios

### 2. Métricas (Metrics)
- **http_requests_total**: Contador de requests HTTP
- **http_request_duration_seconds**: Histograma de duración de requests
- **db_query_duration_seconds**: Histograma de duración de queries DB
- **items_total**: Gauge del número total de items

### 3. Logs Estructurados
- Formato JSON usando `slog` (biblioteca estándar de Go 1.21+)
- Logs con contexto enriquecido (método, path, duración, etc.)
- Niveles de log apropiados (Info, Warn, Error)
- Agregación en Loki
- Visualización en Grafana

## Requisitos Previos

- Go 1.21 o superior
- Docker y Docker Compose
- PostgreSQL (se levanta automáticamente con Docker Compose)

## Instalación y Configuración

### 1. Clonar y navegar al proyecto

```bash
cd prfaber/with-observability
```

### 2. Instalar dependencias de Go

```bash
go mod download
```

### 3. Levantar el stack de observabilidad

```bash
docker-compose up -d
```

Esto levantará los siguientes servicios:

- **PostgreSQL**: Puerto 5432
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (usuario: admin, password: admin)
- **Loki**: Puerto 3100
- **Promtail**: Recolector de logs
- **Jaeger**: http://localhost:16686
- **OTEL Collector**: Puertos 4317 (gRPC) y 4318 (HTTP)

### 4. Ejecutar la aplicación

```bash
go run main.go
```

La API estará disponible en: http://localhost:3000

## Endpoints de la API

### API CRUD

- `GET /` - Información de la API
- `GET /health` - Health check
- `GET /metrics` - Métricas de Prometheus
- `GET /api/v1/items` - Listar todos los items
- `GET /api/v1/items/:id` - Obtener un item por ID
- `POST /api/v1/items` - Crear un nuevo item
- `PUT /api/v1/items/:id` - Actualizar un item
- `DELETE /api/v1/items/:id` - Eliminar un item

### Ejemplo de Requests

**Crear un item:**
```bash
curl -X POST http://localhost:3000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Item de prueba",
    "description": "Descripción del item"
  }'
```

**Listar items:**
```bash
curl http://localhost:3000/api/v1/items
```

**Obtener un item:**
```bash
curl http://localhost:3000/api/v1/items/1
```

**Actualizar un item:**
```bash
curl -X PUT http://localhost:3000/api/v1/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Item actualizado",
    "description": "Nueva descripción"
  }'
```

**Eliminar un item:**
```bash
curl -X DELETE http://localhost:3000/api/v1/items/1
```

## Acceso a las Herramientas de Observabilidad

### Grafana
- **URL**: http://localhost:3001
- **Usuario**: admin
- **Password**: admin
- **Dashboard**: "CRUD API with Observability"

El dashboard incluye:
- Tasa de requests HTTP
- Latencia de requests (p95)
- Duración de queries a la base de datos (p50, p95, p99)
- Total de items en la base de datos
- Logs de la aplicación en tiempo real

### Prometheus
- **URL**: http://localhost:9090
- Consultas de métricas directas
- Explorar todas las métricas disponibles

Ejemplos de queries:
```promql
rate(http_requests_total[5m])
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
sum(items_total)
```

### Jaeger
- **URL**: http://localhost:16686
- Visualización de trazas distribuidas
- Búsqueda de trazas por servicio, operación o tags
- Análisis de latencia y dependencias

### Loki (a través de Grafana)
- Acceder desde Grafana → Explore → Seleccionar datasource "Loki"
- Query de ejemplo: `{job="crud-api"}`

## Variables de Entorno

```bash
DATABASE_URL=postgresql://postgres:123456@localhost:5432/ai_goals_tracker
PORT=3000
ENVIRONMENT=development
OTEL_EXPORTER_OTLP_ENDPOINT=localhost:4318
```

## Logs Estructurados

La aplicación utiliza `slog` para generar logs estructurados en formato JSON:

```json
{
  "time": "2024-01-24T10:30:45.123456Z",
  "level": "INFO",
  "msg": "HTTP request completed",
  "method": "GET",
  "path": "/api/v1/items",
  "status": 200,
  "duration_ms": 12.34,
  "ip": "127.0.0.1"
}
```

## Métricas Disponibles

### HTTP Metrics
- `http_requests_total{method, path, status}` - Total de requests
- `http_request_duration_seconds{method, path, status}` - Duración de requests

### Database Metrics
- `db_query_duration_seconds{operation, table}` - Duración de queries

### Application Metrics
- `items_total` - Número total de items en la base de datos

## Trazas (Traces)

Cada request HTTP genera una traza que incluye:

1. **Span padre**: Request HTTP completo
   - Método HTTP, URL, ruta
   - Código de estado
   - Duración total
   - IP del cliente

2. **Spans hijos**: Operaciones individuales
   - Operaciones CRUD (getItems, createItem, etc.)
   - Queries a la base de datos
   - Atributos específicos (item.id, items.count, etc.)

## Detener los Servicios

```bash
docker-compose down
```

Para eliminar también los volúmenes:
```bash
docker-compose down -v
```

## Arquitectura del Código

```
with-observability/
├── main.go                    # Aplicación principal
├── go.mod                     # Dependencias de Go
├── docker-compose.yml         # Definición de servicios
├── prometheus.yml             # Configuración de Prometheus
├── otel-collector-config.yml  # Configuración del OTEL Collector
├── loki-config.yml            # Configuración de Loki
├── promtail-config.yml        # Configuración de Promtail
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/       # Datasources de Grafana
│   │   └── dashboards/        # Provisioning de dashboards
│   └── dashboards/            # Dashboards JSON
└── logs/                      # Directorio de logs
```

## Comparación con Proyectos Anteriores

| Característica | base | with-swagger | with-observability |
|---------------|------|--------------|-------------------|
| API CRUD | ✅ | ✅ | ✅ |
| OpenTelemetry | ✅ (stdout) | ✅ (stdout) | ✅ (OTLP) |
| Swagger | ❌ | ✅ | ❌ |
| Prometheus | ❌ | ❌ | ✅ |
| Grafana | ❌ | ❌ | ✅ |
| Jaeger | ❌ | ❌ | ✅ |
| Loki | ❌ | ❌ | ✅ |
| Logs estructurados | ❌ | ❌ | ✅ |
| Dashboards | ❌ | ❌ | ✅ |

## Mejores Prácticas Implementadas

1. **Observabilidad completa**: Logs, métricas y trazas (los 3 pilares)
2. **Logs estructurados**: Formato JSON para fácil parsing
3. **Contexto enriquecido**: Cada evento tiene metadata relevante
4. **Métricas de negocio**: No solo métricas técnicas
5. **Trazas distribuidas**: Visibilidad end-to-end de requests
6. **Dashboards preconstruidos**: Visualización inmediata
7. **Health checks**: Endpoint para verificar salud del servicio

## Troubleshooting

### La API no puede conectarse a OTEL Collector
Verifica que el collector esté corriendo:
```bash
docker ps | grep otel
```

Revisa los logs:
```bash
docker logs otel_collector
```

### No veo métricas en Prometheus
1. Verifica que Prometheus esté scrapeando la API: http://localhost:9090/targets
2. Asegúrate de que la API esté exponiendo métricas: http://localhost:3000/metrics

### No veo logs en Grafana
1. Verifica que Promtail esté corriendo: `docker ps | grep promtail`
2. Revisa la configuración de Loki datasource en Grafana
3. Asegúrate de que haya archivos de log en el directorio `./logs`

### No veo trazas en Jaeger
1. Verifica que Jaeger esté corriendo: `docker ps | grep jaeger`
2. Revisa los logs del OTEL Collector
3. Asegúrate de que la variable `OTEL_EXPORTER_OTLP_ENDPOINT` esté correcta

## Recursos Adicionales

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Go Fiber Documentation](https://docs.gofiber.io/)

## Licencia

MIT
