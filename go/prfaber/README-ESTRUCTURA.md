# Ejercicio CRUD API - Fiber + OpenTelemetry

Este ejercicio está organizado en dos versiones para facilitar el aprendizaje progresivo de Swagger/OpenAPI.

## Estructura de carpetas

```
prfaber/
├── base/              # Versión base sin Swagger
│   ├── main.go
│   ├── go.mod
│   ├── go.sum
│   ├── README.md
│   ├── CRUD-API-OpenTelemetry.postman_collection.json
│   └── teoria-opentelemetry.md
│
├── with-swagger/      # Versión con Swagger configurado
│   ├── main.go        (con anotaciones Swagger)
│   ├── go.mod         (incluye dependencias de Swagger)
│   ├── go.sum
│   ├── README.md      (instrucciones para Swagger)
│   ├── .gitignore     (ignora carpeta docs/)
│   ├── CRUD-API-OpenTelemetry.postman_collection.json
│   └── teoria-opentelemetry.md
│
└── README-ESTRUCTURA.md  # Este archivo
```

## Versiones

### 📁 base/
**Propósito:** Versión inicial del ejercicio sin Swagger

**Características:**
- API REST con Fiber
- OpenTelemetry para observabilidad
- PostgreSQL como base de datos
- CRUD completo para entidad "Items"
- Colección de Postman para pruebas

**Ideal para:**
- Aprender los fundamentos de Fiber y OpenTelemetry
- Entender la estructura básica de una API REST en Go
- Practicar operaciones CRUD con PostgreSQL

### 📁 with-swagger/
**Propósito:** Misma funcionalidad pero con documentación Swagger/OpenAPI

**Diferencias vs base:**
- ✅ Anotaciones Swagger en el código
- ✅ Dependencias de Swagger en go.mod
- ✅ Endpoint `/swagger/index.html` para documentación interactiva
- ✅ README actualizado con instrucciones de Swagger
- ✅ .gitignore para archivos generados

**Ideal para:**
- Aprender a documentar APIs con Swagger
- Ver cómo agregar Swagger a un proyecto existente
- Comparar ambas versiones para entender los cambios necesarios

## Cómo usar este ejercicio

### Opción 1: Empezar desde cero (base)
1. Navega a la carpeta `base/`
2. Sigue el README.md de esa carpeta
3. Una vez dominado, compara con `with-swagger/` para ver las diferencias

### Opción 2: Ir directo a Swagger (with-swagger)
1. Navega a la carpeta `with-swagger/`
2. Instala swag CLI: `go install github.com/swaggo/swag/cmd/swag@latest`
3. Genera docs: `swag init`
4. Ejecuta: `go run main.go`
5. Visita: http://localhost:3000/swagger/index.html

## Comparación de archivos

| Archivo | base/ | with-swagger/ | Diferencia |
|---------|-------|---------------|------------|
| main.go | ✅ | ✅ | with-swagger tiene anotaciones @Summary, @Description, etc. |
| go.mod | ✅ | ✅ | with-swagger incluye github.com/gofiber/swagger y swaggo/* |
| README.md | ✅ | ✅ | with-swagger tiene sección de Swagger |
| .gitignore | ❌ | ✅ | Solo en with-swagger para ignorar docs/ |
| docs/ | ❌ | ⚠️ | Se genera con `swag init` en with-swagger |

## Archivos compartidos

Los siguientes archivos son idénticos en ambas versiones:
- `CRUD-API-OpenTelemetry.postman_collection.json`
- `teoria-opentelemetry.md`
- `go.sum` (excepto por dependencias de Swagger)

## Requisitos previos (para ambas versiones)

- Go 1.21 o superior
- PostgreSQL corriendo en localhost:5432
- Usuario: `postgres` / Password: `123456`
- Base de datos: `ai_goals_tracker`

**Adicional para with-swagger:**
- swag CLI: `go install github.com/swaggo/swag/cmd/swag@latest`

## Recursos adicionales

- [Documentación de Fiber](https://docs.gofiber.io/)
- [OpenTelemetry Go](https://opentelemetry.io/docs/instrumentation/go/)
- [Swaggo](https://github.com/swaggo/swag)
- [OpenAPI Specification](https://swagger.io/specification/)

## Próximos pasos sugeridos

1. ✅ Completar el ejercicio base
2. ✅ Migrar manualmente a Swagger (opcional: buen ejercicio)
3. ✅ O revisar la versión with-swagger
4. 🎯 Extender con más endpoints
5. 🎯 Agregar autenticación
6. 🎯 Implementar paginación
7. 🎯 Agregar más observabilidad (métricas, logs)
