# Teoría de OpenTelemetry con Go

## ¿Qué es OpenTelemetry?

**OpenTelemetry** (OTel) es un framework de observabilidad open-source que proporciona APIs, SDKs y herramientas para instrumentar, generar, recolectar y exportar datos de telemetría (traces, métricas y logs) desde aplicaciones.

### Objetivos principales:
- Proporcionar visibilidad del comportamiento interno de aplicaciones distribuidas
- Estandarizar la recolección de telemetría entre diferentes lenguajes y frameworks
- Facilitar el diagnóstico de problemas de rendimiento y errores
- Rastrear requests a través de múltiples servicios

## Conceptos Fundamentales

### 1. Traces (Trazas)

Una **traza** representa el recorrido completo de un request a través de un sistema distribuido. Es como un "rastro de migas de pan" que muestra por dónde pasó una solicitud.

**Ejemplo:** Un usuario hace click en "Crear Item":
```
Usuario → API Gateway → CRUD Service → PostgreSQL
```

La traza captura todo este flujo completo.

### 2. Spans

Un **span** es una unidad individual de trabajo dentro de una traza. Cada operación importante crea un span.

**Características de un Span:**
- **Nombre:** Identifica la operación (ej: "createItem", "GET /api/v1/items")
- **Tiempo de inicio y fin:** Duración de la operación
- **Atributos:** Metadata adicional (ej: `http.method=POST`, `item.id=123`)
- **Estado:** Success, Error, etc.
- **Parent Span ID:** Para crear jerarquías (spans hijos)

**Ejemplo visual:**
```
Traza: POST /api/v1/items
│
├── Span 1: tracingMiddleware [15ms]
│   ├── Atributo: http.method = POST
│   ├── Atributo: http.url = /api/v1/items
│   └── Atributo: http.status_code = 201
│
└── Span 2: createItem [12ms] (hijo de Span 1)
    ├── Atributo: item.name = "Laptop"
    ├── Atributo: item.description = "MacBook Pro"
    └── Atributo: item.id = 5
```

### 3. Context Propagation (Propagación de Contexto)

El **contexto** es un objeto que lleva información de tracing entre diferentes partes del código. Permite que los spans hijos se asocien correctamente con sus padres.

En Go usamos `context.Context`:
```go
ctx, span := tracer.Start(c.UserContext(), "operationName")
defer span.End()
// Pasar ctx a operaciones subsecuentes
db.Query(ctx, "SELECT ...")
```

### 4. Attributes (Atributos)

Los **atributos** son pares clave-valor que agregan metadata a los spans.

**Ejemplos:**
```go
span.SetAttributes(
    attribute.String("http.method", "POST"),
    attribute.Int("http.status_code", 201),
    attribute.String("db.table", "items"),
)
```

### 5. Exporters

Los **exporters** son componentes que envían los datos de telemetría a diferentes destinos:
- `stdout` → Consola (para desarrollo)
- `Jaeger` → Sistema de trazas distribuidas
- `Zipkin` → Sistema de trazas
- `OTLP` → Protocolo estándar de OpenTelemetry

## Arquitectura de OpenTelemetry

```
┌─────────────────────────────────────────────┐
│          Tu Aplicación (main.go)            │
│  ┌──────────────────────────────────────┐   │
│  │   Instrumentación (tracer.Start)     │   │
│  │   - Crear spans                      │   │
│  │   - Agregar atributos                │   │
│  │   - Registrar errores                │   │
│  └──────────────────────────────────────┘   │
│                    ↓                         │
│  ┌──────────────────────────────────────┐   │
│  │       TracerProvider (SDK)           │   │
│  │   - Procesa spans                    │   │
│  │   - Batcher (agrupa en lotes)        │   │
│  │   - Samplers (decide qué trazar)     │   │
│  └──────────────────────────────────────┘   │
│                    ↓                         │
│  ┌──────────────────────────────────────┐   │
│  │          Exporter                    │   │
│  │   - stdout (consola)                 │   │
│  │   - Jaeger                           │   │
│  │   - Zipkin                           │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                     ↓
          ┌──────────────────────┐
          │  Backend de Trazas   │
          │  (Jaeger, Datadog)   │
          └──────────────────────┘
```

## Implementación en Nuestro Código

### Paso 1: Inicializar el Tracer

```go
func initTracer() (*sdktrace.TracerProvider, error) {
    // 1. Crear exporter (stdout para desarrollo)
    exporter, err := stdouttrace.New(stdouttrace.WithPrettyPrint())

    // 2. Crear TracerProvider con configuración
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exporter),  // Envía en lotes
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.ServiceName("crud-fiber-otel"),
            semconv.ServiceVersion("1.0.0"),
        )),
    )

    // 3. Registrar globalmente
    otel.SetTracerProvider(tp)

    // 4. Crear tracer para usar en la app
    tracer = tp.Tracer("crud-api")

    return tp, nil
}
```

**¿Qué hace?**
- Crea un sistema de trazas que imprime en consola
- Define el nombre del servicio ("crud-fiber-otel")
- Retorna `TracerProvider` para cerrarlo al finalizar

### Paso 2: Crear Middleware de Tracing

```go
func tracingMiddleware(c *fiber.Ctx) error {
    // Crear span raíz para este HTTP request
    ctx, span := tracer.Start(c.UserContext(), c.Method()+" "+c.Path())
    defer span.End()

    // Agregar atributos HTTP
    span.SetAttributes(
        attribute.String("http.method", c.Method()),
        attribute.String("http.url", c.OriginalURL()),
    )

    // Propagar contexto a handlers siguientes
    c.SetUserContext(ctx)
    err := c.Next()

    // Después del request, agregar status code
    span.SetAttributes(
        attribute.Int("http.status_code", c.Response().StatusCode())
    )

    return err
}
```

**¿Qué hace?**
- Intercepta TODOS los requests HTTP
- Crea un span padre con método y ruta
- Propaga el contexto a las funciones siguientes
- Captura el código de estado HTTP al finalizar

### Paso 3: Crear Spans en Operaciones

```go
func createItem(c *fiber.Ctx) error {
    // Crear span hijo del span HTTP
    ctx, span := tracer.Start(c.UserContext(), "createItem")
    defer span.End()

    // Parsear request
    var req CreateItemRequest
    if err := c.BodyParser(&req); err != nil {
        span.RecordError(err)  // Registrar error
        return c.Status(400).JSON(...)
    }

    // Agregar atributos de negocio
    span.SetAttributes(
        attribute.String("item.name", req.Name),
    )

    // Usar ctx en operaciones de DB
    err := db.QueryRow(ctx, "INSERT INTO...")

    return c.JSON(item)
}
```

**¿Qué hace?**
- Crea un span hijo llamado "createItem"
- Usa `c.UserContext()` para obtener el contexto del middleware (que ya tiene el span HTTP)
- Registra errores con `span.RecordError(err)`
- Agrega atributos personalizados

### Paso 4: Shutdown Graceful

```go
func main() {
    tp, _ := initTracer()
    defer func() {
        tp.Shutdown(context.Background())  // Asegurar exportación de trazas
    }()

    // ... resto del código
}
```

**¿Por qué es importante?**
- El batcher acumula spans en memoria
- `Shutdown()` asegura que todos los spans se exporten antes de cerrar

## Paso a Paso para Ejecutar la Aplicación

### Prerrequisitos

1. **Go instalado** (versión 1.21 o superior)
```bash
go version
```

2. **PostgreSQL corriendo**
```bash
# Verificar que PostgreSQL está corriendo
brew services list | grep postgresql

# Si no está corriendo, iniciarlo
brew services start postgresql@17
```

3. **Base de datos configurada**
```bash
# Conectar a PostgreSQL
psql -U postgres -d ai_goals_tracker

# Si la base de datos no existe, crearla
psql -U postgres
CREATE DATABASE ai_goals_tracker;
\q
```

### Instalación y Ejecución

#### Opción 1: Ejecutar con `go run`

```bash
# 1. Ir al directorio del proyecto
cd /Users/yusefgonzalez/proyectos/talleres/go/prfaber

# 2. Descargar dependencias
go mod download

# 3. Ejecutar la aplicación
go run main.go
```

**Salida esperada:**
```
2025/01/24 01:00:00 Database connected and table created successfully
2025/01/24 01:00:00 Server starting on port 3000...
```

#### Opción 2: Compilar y ejecutar binario

```bash
# 1. Compilar
go build -o crud-api main.go

# 2. Ejecutar
./crud-api
```

#### Opción 3: Con variables de entorno personalizadas

```bash
# Usar una base de datos diferente
export DATABASE_URL="postgresql://usuario:password@localhost:5432/mi_db"
export PORT="8080"
go run main.go
```

### Verificar que Funciona

#### 1. Verificar endpoint raíz

```bash
curl http://localhost:3000/
```

**Respuesta esperada:**
```json
{
  "message": "CRUD API with Fiber and OpenTelemetry",
  "version": "1.0.0"
}
```

#### 2. Crear un item de prueba

```bash
curl -X POST http://localhost:3000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "MacBook Pro 16 pulgadas"
  }'
```

**Respuesta esperada:**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "MacBook Pro 16 pulgadas",
  "created_at": "2025-01-24T01:05:23.123Z"
}
```

#### 3. Ver las trazas en consola

Después de ejecutar el request anterior, en la consola donde corre la aplicación verás:

```json
{
  "Name": "POST /api/v1/items",
  "SpanContext": {
    "TraceID": "a1b2c3d4e5f6...",
    "SpanID": "1234567890ab...",
    "TraceFlags": "01",
    "TraceState": ""
  },
  "Parent": {...},
  "SpanKind": 1,
  "StartTime": "2025-01-24T01:05:23.120Z",
  "EndTime": "2025-01-24T01:05:23.135Z",
  "Attributes": [
    {
      "Key": "http.method",
      "Value": { "Type": "STRING", "Value": "POST" }
    },
    {
      "Key": "http.url",
      "Value": { "Type": "STRING", "Value": "/api/v1/items" }
    },
    {
      "Key": "http.status_code",
      "Value": { "Type": "INT64", "Value": 201 }
    }
  ],
  "Status": { "Code": "Unset" }
}
```

Y otro span para la operación de base de datos:

```json
{
  "Name": "createItem",
  "Parent": {...},
  "Attributes": [
    {
      "Key": "item.name",
      "Value": { "Type": "STRING", "Value": "Laptop" }
    },
    {
      "Key": "item.description",
      "Value": { "Type": "STRING", "Value": "MacBook Pro 16 pulgadas" }
    },
    {
      "Key": "item.id",
      "Value": { "Type": "INT64", "Value": 1 }
    }
  ]
}
```

## Entendiendo la Salida de Trazas

### Estructura de un Span

```json
{
  "Name": "createItem",           // Nombre de la operación
  "SpanContext": {
    "TraceID": "...",              // ID único de la traza completa
    "SpanID": "...",               // ID único de este span
    "TraceFlags": "01"             // Flags (01 = sampled)
  },
  "Parent": {
    "SpanID": "..."                // ID del span padre
  },
  "SpanKind": 1,                   // Tipo: Internal, Server, Client, etc.
  "StartTime": "...",              // Cuándo empezó
  "EndTime": "...",                // Cuándo terminó
  "Attributes": [                  // Metadata personalizada
    {"Key": "item.name", "Value": "Laptop"}
  ],
  "Status": {
    "Code": "Unset"                // Ok, Error, Unset
  },
  "Events": [],                    // Eventos durante el span
  "Links": []                      // Links a otras trazas
}
```

### Jerarquía de Spans

```
TraceID: a1b2c3d4e5f6...

├─ Span 1: POST /api/v1/items [15ms]
│  SpanID: 1111...
│  Parent: null
│  Attributes:
│    - http.method: POST
│    - http.status_code: 201
│
└─ Span 2: createItem [12ms]
   SpanID: 2222...
   Parent: 1111...  ← Hijo del Span 1
   Attributes:
     - item.name: Laptop
     - item.id: 1
```

## Casos de Uso Prácticos

### 1. Debugging de Latencia

Si un request es lento, las trazas muestran exactamente dónde:

```
POST /api/v1/items [500ms]
├─ tracingMiddleware [500ms]
│  └─ createItem [495ms]
│     ├─ BodyParser [1ms]
│     └─ db.QueryRow [490ms]  ← Aquí está el problema!
```

### 2. Rastreo de Errores

Cuando ocurre un error, se registra en el span:

```json
{
  "Name": "createItem",
  "Status": {
    "Code": "Error",
    "Description": "pq: duplicate key value violates unique constraint"
  },
  "Events": [
    {
      "Name": "exception",
      "Attributes": [
        {"Key": "exception.type", "Value": "DatabaseError"},
        {"Key": "exception.message", "Value": "duplicate key..."}
      ]
    }
  ]
}
```

### 3. Análisis de Flujo de Requests

Ver cómo los requests fluyen a través del sistema:

```
Usuario → POST /items → createItem → INSERT INTO items
Usuario → GET /items → getItems → SELECT FROM items
Usuario → PUT /items/1 → updateItem → UPDATE items
```

## Mejores Prácticas

### 1. Nombrar Spans Consistentemente
```go
// Bueno
tracer.Start(ctx, "createItem")
tracer.Start(ctx, "database.query")

// Malo
tracer.Start(ctx, "create")
tracer.Start(ctx, "db")
```

### 2. Agregar Atributos Útiles
```go
// Útil para debugging
span.SetAttributes(
    attribute.String("item.id", id),
    attribute.String("user.id", userID),
    attribute.String("db.table", "items"),
)
```

### 3. Siempre Registrar Errores
```go
if err != nil {
    span.RecordError(err)  // ¡Importante!
    return err
}
```

### 4. Cerrar Spans con defer
```go
ctx, span := tracer.Start(ctx, "operation")
defer span.End()  // Asegura cierre incluso con errores
```

## Próximos Pasos

### Integrar con Jaeger (Visualizador de Trazas)

```bash
# Correr Jaeger con Docker
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest

# Cambiar exporter en código:
import "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"

exporter, _ := otlptracehttp.New(ctx,
    otlptracehttp.WithEndpoint("localhost:4318"),
    otlptracehttp.WithInsecure(),
)
```

### Agregar Métricas

```go
import "go.opentelemetry.io/otel/metric"

meter := otel.Meter("crud-api")
counter, _ := meter.Int64Counter("items.created")

// En createItem:
counter.Add(ctx, 1)
```

### Correlación de Logs

```go
import "log/slog"

spanCtx := span.SpanContext()
slog.InfoContext(ctx, "Item created",
    "trace_id", spanCtx.TraceID().String(),
    "span_id", spanCtx.SpanID().String(),
    "item.id", item.ID,
)
```

## Recursos Adicionales

- **OpenTelemetry Docs:** https://opentelemetry.io/docs/
- **Go SDK:** https://pkg.go.dev/go.opentelemetry.io/otel
- **Fiber Framework:** https://docs.gofiber.io/
- **Jaeger:** https://www.jaegertracing.io/

## Conclusión

OpenTelemetry proporciona visibilidad profunda en el comportamiento de tu aplicación:
- **Traces** muestran el flujo de requests
- **Spans** miden duración de operaciones
- **Attributes** agregan contexto valioso
- **Context** conecta todo junto

Esta implementación básica te permite empezar a instrumentar tus aplicaciones Go y entender cómo se comportan en producción.
