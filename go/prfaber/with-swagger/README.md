# CRUD API con Fiber, OpenTelemetry y Swagger

API REST básica usando Go Fiber con observabilidad mediante OpenTelemetry, PostgreSQL y documentación automática con Swagger.

## Características

- Framework web: Fiber v2
- Observabilidad: OpenTelemetry con trazas en stdout
- Base de datos: PostgreSQL
- CRUD completo para entidad "Items"
- Documentación automática con Swagger/OpenAPI

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

### 2. Instalar swag CLI (para generar documentación Swagger)

```bash
go install github.com/swaggo/swag/cmd/swag@latest
```

Asegúrate de que `$GOPATH/bin` esté en tu PATH:
```bash
export PATH=$PATH:$(go env GOPATH)/bin
```

### 3. Generar documentación Swagger

Antes de ejecutar la aplicación, genera los archivos de documentación:
```bash
swag init
```

Esto creará una carpeta `docs/` con los archivos de Swagger generados automáticamente.

### 4. Configurar base de datos (opcional)

La aplicación usa por defecto:
```
postgresql://postgres:123456@localhost:5432/ai_goals_tracker
```

Si necesitas cambiar la conexión, usa la variable de entorno:
```bash
export DATABASE_URL="postgresql://usuario:password@localhost:5432/tu_db"
```

### 5. Ejecutar la aplicación

```bash
go run main.go
```

La aplicación inicia en `http://localhost:3000`

## Documentación Swagger

Una vez que la aplicación esté corriendo, puedes acceder a la documentación interactiva de Swagger en:

**http://localhost:3000/swagger/index.html**

Desde la interfaz de Swagger puedes:
- Ver todos los endpoints disponibles
- Probar cada endpoint directamente desde el navegador
- Ver los schemas de request/response
- Entender los códigos de estado HTTP de cada operación

## Endpoints disponibles

### GET /
Información de la API

```bash
curl http://localhost:3000/
```

Respuesta incluye el enlace a Swagger:
```json
{
  "message": "CRUD API with Fiber and OpenTelemetry",
  "version": "1.0.0",
  "swagger": "http://localhost:3000/swagger/index.html"
}
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
├── main.go       # Aplicación completa con anotaciones Swagger
├── go.mod        # Dependencias
├── docs/         # Archivos generados por swag (no editar manualmente)
│   ├── docs.go
│   ├── swagger.json
│   └── swagger.yaml
└── README.md     # Este archivo
```

**Nota:** La carpeta `docs/` se genera automáticamente con el comando `swag init` y no debe editarse manualmente.

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

## Actualizar documentación Swagger

Si modificas las anotaciones de Swagger en el código (comentarios con @), debes regenerar la documentación:

```bash
swag init
```

Luego reinicia la aplicación para ver los cambios reflejados en Swagger UI.

## Ejemplo de uso completo

```bash
# Generar documentación Swagger
swag init

# Ejecutar aplicación
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

# O usa Swagger UI: http://localhost:3000/swagger/index.html

Go mod donwnload xxxx
Go mod tidy
Swag init
go build
```
