package main

import (
	"context"
	"fmt"
	"log"
	"log/slog"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/jackc/pgx/v5/pgxpool"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
	"go.opentelemetry.io/otel/exporters/prometheus"
	"go.opentelemetry.io/otel/metric"
	"go.opentelemetry.io/otel/sdk/resource"
	sdkmetric "go.opentelemetry.io/otel/sdk/metric"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
	"go.opentelemetry.io/otel/trace"
)

type Item struct {
	ID          int       `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description"`
	CreatedAt   time.Time `json:"created_at"`
}

type CreateItemRequest struct {
	Name        string `json:"name"`
	Description string `json:"description"`
}

var (
	db     *pgxpool.Pool
	tracer trace.Tracer
	logger *slog.Logger

	requestCounter  metric.Int64Counter
	requestDuration metric.Float64Histogram
	dbQueryDuration metric.Float64Histogram
	itemsGauge      metric.Int64UpDownCounter
)

func initLogger() {
	opts := &slog.HandlerOptions{
		Level: slog.LevelInfo,
		AddSource: true,
	}

	handler := slog.NewJSONHandler(os.Stdout, opts)
	logger = slog.New(handler)
	slog.SetDefault(logger)
}

func initTracer() (*sdktrace.TracerProvider, error) {
	ctx := context.Background()

	otlpEndpoint := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
	if otlpEndpoint == "" {
		otlpEndpoint = "localhost:4318"
	}

	exporter, err := otlptracehttp.New(
		ctx,
		otlptracehttp.WithEndpoint(otlpEndpoint),
		otlptracehttp.WithInsecure(),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create OTLP trace exporter: %w", err)
	}

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName("crud-fiber-observability"),
			semconv.ServiceVersion("1.0.0"),
			attribute.String("environment", getEnv("ENVIRONMENT", "development")),
		)),
	)

	otel.SetTracerProvider(tp)
	tracer = tp.Tracer("crud-api")

	logger.Info("OpenTelemetry tracer initialized",
		slog.String("endpoint", otlpEndpoint))

	return tp, nil
}

func initMetrics() (*sdkmetric.MeterProvider, error) {
	exporter, err := prometheus.New()
	if err != nil {
		return nil, fmt.Errorf("failed to create Prometheus exporter: %w", err)
	}

	meterProvider := sdkmetric.NewMeterProvider(
		sdkmetric.WithReader(exporter),
		sdkmetric.WithResource(resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName("crud-fiber-observability"),
			semconv.ServiceVersion("1.0.0"),
		)),
	)

	otel.SetMeterProvider(meterProvider)
	meter := meterProvider.Meter("crud-api")

	requestCounter, err = meter.Int64Counter(
		"http_requests_total",
		metric.WithDescription("Total number of HTTP requests"),
		metric.WithUnit("{request}"),
	)
	if err != nil {
		return nil, err
	}

	requestDuration, err = meter.Float64Histogram(
		"http_request_duration_seconds",
		metric.WithDescription("HTTP request duration in seconds"),
		metric.WithUnit("s"),
	)
	if err != nil {
		return nil, err
	}

	dbQueryDuration, err = meter.Float64Histogram(
		"db_query_duration_seconds",
		metric.WithDescription("Database query duration in seconds"),
		metric.WithUnit("s"),
	)
	if err != nil {
		return nil, err
	}

	itemsGauge, err = meter.Int64UpDownCounter(
		"items_total",
		metric.WithDescription("Current number of items in database"),
		metric.WithUnit("{item}"),
	)
	if err != nil {
		return nil, err
	}

	logger.Info("Prometheus metrics initialized")

	return meterProvider, nil
}

func initDB() error {
	databaseURL := getEnv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/ai_goals_tracker")

	var err error
	db, err = pgxpool.New(context.Background(), databaseURL)
	if err != nil {
		logger.Error("Failed to connect to database",
			slog.String("error", err.Error()))
		return fmt.Errorf("unable to connect to database: %w", err)
	}

	createTableQuery := `
	CREATE TABLE IF NOT EXISTS items (
		id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		description TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);`

	_, err = db.Exec(context.Background(), createTableQuery)
	if err != nil {
		logger.Error("Failed to create table",
			slog.String("error", err.Error()))
		return fmt.Errorf("failed to create table: %w", err)
	}

	logger.Info("Database connected and table created successfully",
		slog.String("database", databaseURL))

	return nil
}

func tracingMiddleware(c *fiber.Ctx) error {
	start := time.Now()

	ctx, span := tracer.Start(c.UserContext(), c.Method()+" "+c.Path())
	defer span.End()

	span.SetAttributes(
		attribute.String("http.method", c.Method()),
		attribute.String("http.url", c.OriginalURL()),
		attribute.String("http.route", c.Route().Path),
		attribute.String("http.client_ip", c.IP()),
	)

	c.SetUserContext(ctx)
	err := c.Next()

	duration := time.Since(start).Seconds()
	statusCode := c.Response().StatusCode()

	span.SetAttributes(
		attribute.Int("http.status_code", statusCode),
		attribute.Float64("http.duration_seconds", duration),
	)

	requestCounter.Add(ctx, 1,
		metric.WithAttributes(
			attribute.String("method", c.Method()),
			attribute.String("path", c.Route().Path),
			attribute.Int("status", statusCode),
		),
	)

	requestDuration.Record(ctx, duration,
		metric.WithAttributes(
			attribute.String("method", c.Method()),
			attribute.String("path", c.Route().Path),
			attribute.Int("status", statusCode),
		),
	)

	logger.Info("HTTP request completed",
		slog.String("method", c.Method()),
		slog.String("path", c.Path()),
		slog.Int("status", statusCode),
		slog.Float64("duration_ms", duration*1000),
		slog.String("ip", c.IP()),
	)

	return err
}

func getItems(c *fiber.Ctx) error {
	ctx, span := tracer.Start(c.UserContext(), "getItems")
	defer span.End()

	logger.Info("Fetching all items")

	queryStart := time.Now()
	rows, err := db.Query(ctx, "SELECT id, name, description, created_at FROM items ORDER BY id DESC")
	if err != nil {
		span.RecordError(err)
		logger.Error("Failed to fetch items from database",
			slog.String("error", err.Error()))
		return c.Status(500).JSON(fiber.Map{"error": "Failed to fetch items"})
	}
	defer rows.Close()

	dbQueryDuration.Record(ctx, time.Since(queryStart).Seconds(),
		metric.WithAttributes(
			attribute.String("operation", "SELECT"),
			attribute.String("table", "items"),
		),
	)

	items := []Item{}
	for rows.Next() {
		var item Item
		err := rows.Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)
		if err != nil {
			span.RecordError(err)
			logger.Warn("Failed to scan item",
				slog.String("error", err.Error()))
			continue
		}
		items = append(items, item)
	}

	span.SetAttributes(attribute.Int("items.count", len(items)))
	logger.Info("Items fetched successfully",
		slog.Int("count", len(items)))

	return c.JSON(items)
}

func getItem(c *fiber.Ctx) error {
	ctx, span := tracer.Start(c.UserContext(), "getItem")
	defer span.End()

	id := c.Params("id")
	span.SetAttributes(attribute.String("item.id", id))

	logger.Info("Fetching item",
		slog.String("item_id", id))

	queryStart := time.Now()
	var item Item
	err := db.QueryRow(ctx, "SELECT id, name, description, created_at FROM items WHERE id = $1", id).
		Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)

	dbQueryDuration.Record(ctx, time.Since(queryStart).Seconds(),
		metric.WithAttributes(
			attribute.String("operation", "SELECT"),
			attribute.String("table", "items"),
		),
	)

	if err != nil {
		span.RecordError(err)
		logger.Warn("Item not found",
			slog.String("item_id", id),
			slog.String("error", err.Error()))
		return c.Status(404).JSON(fiber.Map{"error": "Item not found"})
	}

	logger.Info("Item fetched successfully",
		slog.String("item_id", id),
		slog.String("item_name", item.Name))

	return c.JSON(item)
}

func createItem(c *fiber.Ctx) error {
	ctx, span := tracer.Start(c.UserContext(), "createItem")
	defer span.End()

	var req CreateItemRequest
	if err := c.BodyParser(&req); err != nil {
		span.RecordError(err)
		logger.Error("Invalid request body",
			slog.String("error", err.Error()))
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	span.SetAttributes(
		attribute.String("item.name", req.Name),
		attribute.String("item.description", req.Description),
	)

	logger.Info("Creating new item",
		slog.String("item_name", req.Name))

	queryStart := time.Now()
	var item Item
	err := db.QueryRow(ctx,
		"INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id, name, description, created_at",
		req.Name, req.Description).
		Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)

	dbQueryDuration.Record(ctx, time.Since(queryStart).Seconds(),
		metric.WithAttributes(
			attribute.String("operation", "INSERT"),
			attribute.String("table", "items"),
		),
	)

	if err != nil {
		span.RecordError(err)
		logger.Error("Failed to create item",
			slog.String("error", err.Error()),
			slog.String("item_name", req.Name))
		return c.Status(500).JSON(fiber.Map{"error": "Failed to create item"})
	}

	itemsGauge.Add(ctx, 1)

	span.SetAttributes(attribute.Int("item.id", item.ID))
	logger.Info("Item created successfully",
		slog.Int("item_id", item.ID),
		slog.String("item_name", item.Name))

	return c.Status(201).JSON(item)
}

func updateItem(c *fiber.Ctx) error {
	ctx, span := tracer.Start(c.UserContext(), "updateItem")
	defer span.End()

	id := c.Params("id")
	span.SetAttributes(attribute.String("item.id", id))

	var req CreateItemRequest
	if err := c.BodyParser(&req); err != nil {
		span.RecordError(err)
		logger.Error("Invalid request body",
			slog.String("error", err.Error()),
			slog.String("item_id", id))
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	logger.Info("Updating item",
		slog.String("item_id", id),
		slog.String("item_name", req.Name))

	queryStart := time.Now()
	var item Item
	err := db.QueryRow(ctx,
		"UPDATE items SET name = $1, description = $2 WHERE id = $3 RETURNING id, name, description, created_at",
		req.Name, req.Description, id).
		Scan(&item.ID, &item.Name, &item.Description, &item.CreatedAt)

	dbQueryDuration.Record(ctx, time.Since(queryStart).Seconds(),
		metric.WithAttributes(
			attribute.String("operation", "UPDATE"),
			attribute.String("table", "items"),
		),
	)

	if err != nil {
		span.RecordError(err)
		logger.Warn("Item not found for update",
			slog.String("item_id", id),
			slog.String("error", err.Error()))
		return c.Status(404).JSON(fiber.Map{"error": "Item not found"})
	}

	logger.Info("Item updated successfully",
		slog.String("item_id", id),
		slog.String("item_name", item.Name))

	return c.JSON(item)
}

func deleteItem(c *fiber.Ctx) error {
	ctx, span := tracer.Start(c.UserContext(), "deleteItem")
	defer span.End()

	id := c.Params("id")
	span.SetAttributes(attribute.String("item.id", id))

	logger.Info("Deleting item",
		slog.String("item_id", id))

	queryStart := time.Now()
	result, err := db.Exec(ctx, "DELETE FROM items WHERE id = $1", id)

	dbQueryDuration.Record(ctx, time.Since(queryStart).Seconds(),
		metric.WithAttributes(
			attribute.String("operation", "DELETE"),
			attribute.String("table", "items"),
		),
	)

	if err != nil {
		span.RecordError(err)
		logger.Error("Failed to delete item",
			slog.String("item_id", id),
			slog.String("error", err.Error()))
		return c.Status(500).JSON(fiber.Map{"error": "Failed to delete item"})
	}

	if result.RowsAffected() == 0 {
		logger.Warn("Item not found for deletion",
			slog.String("item_id", id))
		return c.Status(404).JSON(fiber.Map{"error": "Item not found"})
	}

	itemsGauge.Add(ctx, -1)

	logger.Info("Item deleted successfully",
		slog.String("item_id", id))

	return c.JSON(fiber.Map{"message": "Item deleted successfully"})
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func main() {
	initLogger()
	logger.Info("Starting CRUD API with full observability stack")

	tp, err := initTracer()
	if err != nil {
		log.Fatal("Failed to initialize tracer:", err)
	}
	defer func() {
		if err := tp.Shutdown(context.Background()); err != nil {
			logger.Error("Error shutting down tracer provider",
				slog.String("error", err.Error()))
		}
	}()

	mp, err := initMetrics()
	if err != nil {
		log.Fatal("Failed to initialize metrics:", err)
	}
	defer func() {
		if err := mp.Shutdown(context.Background()); err != nil {
			logger.Error("Error shutting down meter provider",
				slog.String("error", err.Error()))
		}
	}()

	if err := initDB(); err != nil {
		log.Fatal("Failed to initialize database:", err)
	}
	defer db.Close()

	app := fiber.New(fiber.Config{
		AppName: "CRUD API with Observability",
	})

	app.Use(tracingMiddleware)

	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"message": "CRUD API with Full Observability Stack",
			"version": "1.0.0",
			"endpoints": fiber.Map{
				"api":        "/api/v1/items",
				"metrics":    "/metrics",
				"health":     "/health",
			},
		})
	})

	app.Get("/metrics", func(c *fiber.Ctx) error {
		c.Set("Content-Type", "text/plain")
		return c.SendString("# Prometheus metrics available\n")
	})

	app.Get("/health", func(c *fiber.Ctx) error {
		ctx := context.Background()
		if err := db.Ping(ctx); err != nil {
			logger.Error("Health check failed - database unhealthy",
				slog.String("error", err.Error()))
			return c.Status(503).JSON(fiber.Map{
				"status": "unhealthy",
				"database": "down",
			})
		}

		return c.JSON(fiber.Map{
			"status": "healthy",
			"database": "up",
			"timestamp": time.Now(),
		})
	})

	api := app.Group("/api/v1")
	api.Get("/items", getItems)
	api.Get("/items/:id", getItem)
	api.Post("/items", createItem)
	api.Put("/items/:id", updateItem)
	api.Delete("/items/:id", deleteItem)

	port := getEnv("PORT", "3000")

	logger.Info("Server starting",
		slog.String("port", port),
		slog.String("environment", getEnv("ENVIRONMENT", "development")))

	if err := app.Listen(":" + port); err != nil {
		logger.Error("Server failed to start",
			slog.String("error", err.Error()))
		log.Fatal(err)
	}
}
