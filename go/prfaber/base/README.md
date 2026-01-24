# CRUD API con Fiber y OpenTelemetry

API REST básica usando Go Fiber con observabilidad mediante OpenTelemetry y PostgreSQL.

## Características

- Framework web: Fiber v2
- Observabilidad: OpenTelemetry con trazas en stdout
- Base de datos: PostgreSQL
- CRUD completo para entidad "Items"

## Requisitos previos

- Go 1.21 o superior
- PostgreSQL corriendo en localhost:5432
- Usuario: `postgres` / Password: `123456`
- Base de datos: `ai_goals_tracker`

## Instalación

### 1. Instalar dependencias

```bash
go mod download
```

### 2. Configurar base de datos (opcional)

La aplicación usa por defecto:
```
postgresql://postgres:123456@localhost:5432/ai_goals_tracker
```

Si necesitas cambiar la conexión, usa la variable de entorno:
```bash
export DATABASE_URL="postgresql://usuario:password@localhost:5432/tu_db"
```

### 3. Ejecutar la aplicación

```bash
go run main.go
```

La aplicación inicia en `http://localhost:3000`

## Endpoints disponibles

### GET /
Información de la API

```bash
curl http://localhost:3000/
```

### GET /api/v1/items
Obtener todos los items

```bash
curl http://localhost:3000/api/v1/items
```

### GET /api/v1/items/:id
Obtener un item por ID

```bash
curl http://localhost:3000/api/v1/items/1
```

### POST /api/v1/items
Crear un nuevo item

```bash
curl -X POST http://localhost:3000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi primer item",
    "description": "Esta es una descripción de prueba"
  }'
```

### PUT /api/v1/items/:id
Actualizar un item

```bash
curl -X PUT http://localhost:3000/api/v1/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Item actualizado",
    "description": "Descripción actualizada"
  }'
```

### DELETE /api/v1/items/:id
Eliminar un item

```bash
curl -X DELETE http://localhost:3000/api/v1/items/1
```

## Estructura del proyecto

```
.
├── main.go       # Aplicación completa en un solo archivo
├── go.mod        # Dependencias
└── README.md     # Este archivo
```

## OpenTelemetry

Las trazas se exportan a stdout en formato JSON. Cada request HTTP genera:
- Span del middleware de tracing
- Span de la operación de base de datos
- Atributos HTTP (método, URL, status code)
- Información de errores si ocurren

Para ver las trazas, simplemente observa la salida en la consola mientras usas la API.

## Esquema de base de datos

La tabla `items` se crea automáticamente al iniciar:

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Compilar para producción

```bash
go build -o crud-api main.go
./crud-api
```

## Variables de entorno

- `DATABASE_URL`: Conexión a PostgreSQL (default: `postgresql://postgres:123456@localhost:5432/ai_goals_tracker`)
- `PORT`: Puerto del servidor (default: `3000`)

## Ejemplo de uso completo

```bash
go run main.go

# En otra terminal:
# Crear item
curl -X POST http://localhost:3000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "MacBook Pro 16"}'

# Listar items
curl http://localhost:3000/api/v1/items

# Actualizar item
curl -X PUT http://localhost:3000/api/v1/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Dell", "description": "Dell XPS 15"}'

# Eliminar item
curl -X DELETE http://localhost:3000/api/v1/items/1
```
