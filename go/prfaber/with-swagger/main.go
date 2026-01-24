package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/logger"
	swagger "github.com/gofiber/swagger"
	"github.com/jackc/pgx/v5/pgxpool"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
	"go.opentelemetry.io/otel/trace"

	_ "github.com/yusefgonzalez/crud-fiber-otel/docs"
)

// @title CRUD API with Fiber and OpenTelemetry
// @version 1.0
// @description API REST con operaciones CRUD, integración de OpenTelemetry para observabilidad y documentación Swagger
// @termsOfService http://swagger.io/terms/

// @contact.name API Support
// @contact.email support@example.com

// @license.name MIT
// @license.url https://opensource.org/licenses/MIT

// @host localhost:3000
// @BasePath /
// @schemes http

// Item representa un elemento en la base de datos
// Contiene los campos principales que se almacenan y retornan en las operaciones CRUD
type Item struct {
	ID          int       `json:"id"`          // ID único autogenerado por PostgreSQL
	Name        string    `json:"name"`        // Nombre del item
	Description string    `json:"description"` // Descripción detallada del item
	CreatedAt   time.Time `json:"created_at"`  // Fecha y hora de creación
}

// CreateItemRequest representa la estructura de datos para crear o actualizar un item
// Solo incluye los campos que el usuario debe proporcionar
type CreateItemRequest struct {
	Name        string `json:"name"`        // Nombre del item a crear
	Description string `json:"description"` // Descripción del item a crear
}

// Variables globales para compartir entre funciones
var (
	db     *pgxpool.Pool  // Pool de conexiones a PostgreSQL
	tracer trace.Tracer   // Tracer de OpenTelemetry para crear spans
)

// initTracer inicializa el sistema de trazas de OpenTelemetry
// Configura un exporter que imprime las trazas en stdout (consola)
// Retorna el TracerProvider que debe ser cerrado al finalizar la aplicación
func initTracer() (*sdktrace.TracerProvider, error) {
	// Crear un exporter que envía las trazas a stdout (consola) en formato JSON
	exporter, err := stdouttrace.New(stdouttrace.WithPrettyPrint())
	if err != nil {
		return nil, err
	}

	// Crear el TracerProvider con configuración del servicio
	tp := sdktrace.NewTracerProvider(
		// Batcher procesa y envía las trazas en lotes para mejor rendimiento
		sdktrace.WithBatcher(exporter),
		// Resource define los atributos del servicio que aparecen en cada traza
		sdktrace.WithResource(resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName("crud-fiber-otel"),    // Nombre del servicio
			semconv.ServiceVersion("1.0.0"),            // Versión del servicio
		)),
	)

	// Registrar el TracerProvider globalmente para que otel.Tracer() lo use
	otel.SetTracerProvider(tp)
	// Crear un tracer específico para esta API
	tracer = tp.Tracer("crud-api")

	return tp, nil
}

// initDB inicializa la conexión a PostgreSQL y crea la tabla si no existe
// Lee la URL de conexión desde variable de entorno DATABASE_URL
// Retorna error si no puede conectar o crear la tabla
func initDB() error {
	// Leer URL de conexión desde variable de entorno
	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		// Valor por defecto si no está definida la variable
		databaseURL = "postgresql://postgres:123456@localhost:5432/ai_goals_tracker"
	}

	// Crear pool de conexiones a PostgreSQL
	var err error
	db, err = pgxpool.New(context.Background(), databaseURL)
	if err != nil {
		return fmt.Errorf("unable to connect to database: %w", err)
	}

	// Crear tabla items si no existe
	createTableQuery := `
	CREATE TABLE IF NOT EXISTS items (
		id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		description TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);`

	_, err = db.Exec(context.Background(), createTableQuery)
	if err != nil {
		return fmt.Errorf("failed to create table: %w", err)
	}

	log.Println("Database connected and table created successfully")
	return nil
}

// tracingMiddleware es un middleware de Fiber que crea un span para cada request HTTP
// Captura información como método HTTP, URL, ruta y código de estado
// Propaga el contexto con el span a los siguientes handlers
func tracingMiddleware(c *fiber.Ctx) error {
	// Crear un nuevo span para este request HTTP
	// El nombre del span es "METODO /ruta" (ej: "GET /api/v1/items")
	ctx, span := tracer.Start(c.UserContext(), c.Method()+" "+c.Path())
	defer span.End() // Asegurar que el span se cierre al terminar

	// Agregar atributos del request HTTP al span
	span.SetAttributes(
		attribute.String("http.method", c.Method()),        // GET, POST, PUT, DELETE
		attribute.String("http.url", c.OriginalURL()),      // URL completa con query params
		attribute.String("http.route", c.Route().Path),     // Ruta del endpoint
	)

	// Propagar el contexto con el span a los siguientes handlers
	c.SetUserContext(ctx)
	// Ejecutar el siguiente handler en la cadena
	err := c.Next()

	// Después de ejecutar el handler, agregar el código de estado HTTP
	span.SetAttributes(attribute.Int("http.status_code", c.Response().StatusCode()))

	return err
}

// getItems retorna todos los items de la base de datos
// @Summary Listar todos los items
// @Description Obtiene todos los items almacenados en la base de datos
// @Tags items
// @Accept json
// @Produce json
// @Success 200 {array} Item
// @Failure 500 {object} map[string]string
// @Router /api/v1/items [get]
func getItems(c *fiber.Ctx) error {
	// Crear span hijo usando el contexto del request (que ya tiene un span padre)
	ctx, span := tracer.Start(c.UserContext(), "getItems")
	defer span.End()

	// Consultar todos los items ordenados por ID descendente (más recientes primero)
	rows, err := db.Query(ctx, "SELECT id, name, description, created_at FROM items ORDER BY id DESC")
	if err != nil {
		// Registrar el error en el span para observabilidad
		span.RecordError(err)
		return c.Status(500).JSON(fiber.Map{"error": "Failed to fetch items"})
	}
	defer rows.Close()

	// Construir slice de items a partir de los resultados
	items := []Item{}
	for rows.Next() {
		var item Item
		err := rows.Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)
		if err != nil {
			span.RecordError(err)
			continue // Continuar con el siguiente item si hay error
		}
		items = append(items, item)
	}

	// Agregar metadata útil al span (cantidad de items retornados)
	span.SetAttributes(attribute.Int("items.count", len(items)))
	return c.JSON(items)
}

// getItem retorna un item específico por su ID
// @Summary Obtener un item por ID
// @Description Obtiene un item específico mediante su ID
// @Tags items
// @Accept json
// @Produce json
// @Param id path int true "ID del item"
// @Success 200 {object} Item
// @Failure 404 {object} map[string]string
// @Router /api/v1/items/{id} [get]
func getItem(c *fiber.Ctx) error {
	// Crear span para esta operación
	ctx, span := tracer.Start(c.UserContext(), "getItem")
	defer span.End()

	// Obtener ID desde parámetros de ruta
	id := c.Params("id")
	span.SetAttributes(attribute.String("item.id", id))

	// Buscar item en la base de datos
	var item Item
	err := db.QueryRow(ctx, "SELECT id, name, description, created_at FROM items WHERE id = $1", id).
		Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)

	if err != nil {
		// Si no se encuentra, registrar error y retornar 404
		span.RecordError(err)
		return c.Status(404).JSON(fiber.Map{"error": "Item not found"})
	}

	return c.JSON(item)
}

// createItem crea un nuevo item en la base de datos
// @Summary Crear un nuevo item
// @Description Crea un nuevo item con nombre y descripción
// @Tags items
// @Accept json
// @Produce json
// @Param item body CreateItemRequest true "Datos del item a crear"
// @Success 201 {object} Item
// @Failure 400 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /api/v1/items [post]
func createItem(c *fiber.Ctx) error {
	// Crear span para esta operación
	ctx, span := tracer.Start(c.UserContext(), "createItem")
	defer span.End()

	// Parsear el body JSON a la estructura CreateItemRequest
	var req CreateItemRequest
	if err := c.BodyParser(&req); err != nil {
		span.RecordError(err)
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	// Agregar los datos del request al span para trazabilidad
	span.SetAttributes(
		attribute.String("item.name", req.Name),
		attribute.String("item.description", req.Description),
	)

	// Insertar en la base de datos y retornar el item completo con RETURNING
	var item Item
	err := db.QueryRow(ctx,
		"INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id, name, description, created_at",
		req.Name, req.Description).
		Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)

	if err != nil {
		span.RecordError(err)
		return c.Status(500).JSON(fiber.Map{"error": "Failed to create item"})
	}

	// Agregar el ID generado al span
	span.SetAttributes(attribute.Int("item.id", item.ID))
	return c.Status(201).JSON(item) // 201 Created
}

// updateItem actualiza un item existente por su ID
// @Summary Actualizar un item
// @Description Actualiza un item existente mediante su ID
// @Tags items
// @Accept json
// @Produce json
// @Param id path int true "ID del item"
// @Param item body CreateItemRequest true "Datos actualizados del item"
// @Success 200 {object} Item
// @Failure 400 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Router /api/v1/items/{id} [put]
func updateItem(c *fiber.Ctx) error {
	// Crear span para esta operación
	ctx, span := tracer.Start(c.UserContext(), "updateItem")
	defer span.End()

	// Obtener ID desde parámetros de ruta
	id := c.Params("id")
	span.SetAttributes(attribute.String("item.id", id))

	// Parsear el body JSON
	var req CreateItemRequest
	if err := c.BodyParser(&req); err != nil {
		span.RecordError(err)
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	// Actualizar en la base de datos y retornar el item actualizado
	var item Item
	err := db.QueryRow(ctx,
		"UPDATE items SET name = $1, description = $2 WHERE id = $3 RETURNING id, name, description, created_at",
		req.Name, req.Description, id).
		Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)

	if err != nil {
		// Si no se encuentra el item, PostgreSQL retorna error
		span.RecordError(err)
		return c.Status(404).JSON(fiber.Map{"error": "Item not found"})
	}

	return c.JSON(item)
}

// deleteItem elimina un item por su ID
// @Summary Eliminar un item
// @Description Elimina un item mediante su ID
// @Tags items
// @Accept json
// @Produce json
// @Param id path int true "ID del item"
// @Success 200 {object} map[string]string
// @Failure 404 {object} map[string]string
// @Failure 500 {object} map[string]string
// @Router /api/v1/items/{id} [delete]
func deleteItem(c *fiber.Ctx) error {
	// Crear span para esta operación
	ctx, span := tracer.Start(c.UserContext(), "deleteItem")
	defer span.End()

	// Obtener ID desde parámetros de ruta
	id := c.Params("id")
	span.SetAttributes(attribute.String("item.id", id))

	// Ejecutar DELETE en la base de datos
	result, err := db.Exec(ctx, "DELETE FROM items WHERE id = $1", id)
	if err != nil {
		span.RecordError(err)
		return c.Status(500).JSON(fiber.Map{"error": "Failed to delete item"})
	}

	// Verificar si se eliminó algún registro
	if result.RowsAffected() == 0 {
		return c.Status(404).JSON(fiber.Map{"error": "Item not found"})
	}

	return c.JSON(fiber.Map{"message": "Item deleted successfully"})
}

// main es el punto de entrada de la aplicación
// Inicializa OpenTelemetry, la base de datos y el servidor Fiber
func main() {
	// Inicializar OpenTelemetry Tracer
	tp, err := initTracer()
	if err != nil {
		log.Fatal("Failed to initialize tracer:", err)
	}
	// Asegurar que el TracerProvider se cierre correctamente al finalizar
	defer func() {
		if err := tp.Shutdown(context.Background()); err != nil {
			log.Printf("Error shutting down tracer provider: %v", err)
		}
	}()

	// Inicializar conexión a la base de datos
	if err := initDB(); err != nil {
		log.Fatal("Failed to initialize database:", err)
	}
	defer db.Close()

	// Crear aplicación Fiber
	app := fiber.New(fiber.Config{
		AppName: "CRUD API with OpenTelemetry",
	})

	// Registrar middlewares globales
	app.Use(logger.New())          // Logger de requests HTTP en consola
	app.Use(tracingMiddleware)     // Middleware de OpenTelemetry para crear spans

	// Endpoint raíz para verificar que la API está funcionando
	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"message": "CRUD API with Fiber and OpenTelemetry",
			"version": "1.0.0",
			"swagger": "http://localhost:3000/swagger/index.html",
		})
	})

	// Swagger endpoint
	app.Get("/swagger/*", swagger.HandlerDefault)

	// Agrupar endpoints bajo /api/v1
	api := app.Group("/api/v1")
	api.Get("/items", getItems)          // Listar todos los items
	api.Get("/items/:id", getItem)       // Obtener un item por ID
	api.Post("/items", createItem)       // Crear nuevo item
	api.Put("/items/:id", updateItem)    // Actualizar item existente
	api.Delete("/items/:id", deleteItem) // Eliminar item

	// Leer puerto desde variable de entorno o usar 3000 por defecto
	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}

	// Iniciar servidor HTTP
	log.Printf("Server starting on port %s...", port)
	if err := app.Listen(":" + port); err != nil {
		log.Fatal(err)
	}
}
