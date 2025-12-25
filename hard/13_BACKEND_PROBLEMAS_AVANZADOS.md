# Backend: Problemas Complejos y Soluciones Avanzadas

## Objetivo
Problemas reales y difíciles que enfrentan los arquitectos backend en producción, con soluciones prácticas y patrones probados.

---

## CATEGORÍA 1: Distributed Tracing y Observabilidad

### 1.1 OpenTelemetry - Tracing Distribuido
**Dificultad:** ⭐⭐⭐⭐⭐

**Python - FastAPI con OpenTelemetry**

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from fastapi import FastAPI, Request
import httpx

# Configurar provider
resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "user-service",
    ResourceAttributes.SERVICE_VERSION: "1.0.0",
    ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "production"
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Configurar exportador (Jaeger)
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Obtener tracer
tracer = trace.get_tracer(__name__)

app = FastAPI()

# Auto-instrumentación
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)
RedisInstrumentor().instrument()
HTTPXClientInstrumentor().instrument()

# Context propagation manual
from opentelemetry.propagate import extract, inject

@app.middleware("http")
async def trace_middleware(request: Request, call_next):
    # Extraer context del request entrante
    ctx = extract(request.headers)

    with tracer.start_as_current_span(
        f"{request.method} {request.url.path}",
        context=ctx,
        kind=trace.SpanKind.SERVER
    ) as span:
        # Agregar atributos
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.route", request.url.path)

        if hasattr(request.state, 'user_id'):
            span.set_attribute("user.id", request.state.user_id)

        response = await call_next(request)

        span.set_attribute("http.status_code", response.status_code)

        if response.status_code >= 500:
            span.set_status(trace.Status(trace.StatusCode.ERROR))

        return response

# Spans manuales para lógica de negocio
@app.post("/orders")
async def create_order(order_data: dict, request: Request):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("order.items_count", len(order_data['items']))
        span.set_attribute("order.total", order_data['total'])

        # Validar inventario
        with tracer.start_as_current_span("validate_inventory") as inventory_span:
            inventory_valid = await validate_inventory(order_data['items'])
            inventory_span.set_attribute("inventory.valid", inventory_valid)

            if not inventory_valid:
                span.add_event("inventory_validation_failed")
                raise HTTPException(status_code=400, detail="Insufficient inventory")

        # Procesar pago
        with tracer.start_as_current_span("process_payment") as payment_span:
            payment_result = await process_payment(order_data['payment'])
            payment_span.set_attribute("payment.method", order_data['payment']['method'])
            payment_span.set_attribute("payment.status", payment_result.status)

        # Crear orden en DB
        with tracer.start_as_current_span("save_order_to_db") as db_span:
            order = await save_order(order_data)
            db_span.set_attribute("order.id", order.id)

        # Llamar servicio externo con propagación de contexto
        with tracer.start_as_current_span(
            "call_notification_service",
            kind=trace.SpanKind.CLIENT
        ) as notification_span:
            headers = {}
            inject(headers)  # Inyectar trace context en headers

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://notification-service/send",
                    json={"order_id": order.id},
                    headers=headers
                )
                notification_span.set_attribute("notification.sent", response.status_code == 200)

        span.add_event("order_created", {
            "order.id": order.id,
            "user.id": request.state.user_id
        })

        return order

# Agregar spans a funciones existentes
def traced(name: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            span_name = name or func.__name__
            with tracer.start_as_current_span(span_name):
                return await func(*args, **kwargs)
        return wrapper
    return decorator

@traced("calculate_shipping_cost")
async def calculate_shipping(items: list, address: dict):
    # Lógica compleja
    total_weight = sum(item['weight'] for item in items)

    current_span = trace.get_current_span()
    current_span.set_attribute("shipping.weight", total_weight)
    current_span.set_attribute("shipping.country", address['country'])

    cost = await shipping_api.calculate(total_weight, address)
    current_span.set_attribute("shipping.cost", cost)

    return cost

# Manejo de errores en spans
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span("get_user") as span:
        try:
            user = await db.get_user(user_id)
            if not user:
                span.set_status(trace.Status(trace.StatusCode.ERROR, "User not found"))
                raise HTTPException(status_code=404)

            span.set_status(trace.Status(trace.StatusCode.OK))
            return user

        except Exception as e:
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise

# Custom metrics con OpenTelemetry
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader

metric_reader = PrometheusMetricReader()
meter_provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

meter = metrics.get_meter(__name__)

# Counters
order_counter = meter.create_counter(
    "orders_created_total",
    description="Total orders created"
)

# Histograms
order_value_histogram = meter.create_histogram(
    "order_value_dollars",
    description="Order values in dollars"
)

# UpDownCounter
active_sessions = meter.create_up_down_counter(
    "active_sessions",
    description="Active user sessions"
)

@app.post("/orders")
async def create_order(order_data: dict):
    order = await save_order(order_data)

    # Incrementar métricas
    order_counter.add(1, {"payment_method": order_data['payment']['method']})
    order_value_histogram.record(order_data['total'], {"currency": "USD"})

    return order
```

**Go - OpenTelemetry con gRPC**

```go
package main

import (
    "context"
    "log"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/resource"
    "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
    oteltrace "go.opentelemetry.io/otel/trace"
    "go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"
    "google.golang.org/grpc"
)

func initTracer() (*trace.TracerProvider, error) {
    exporter, err := jaeger.New(jaeger.WithAgentEndpoint())
    if err != nil {
        return nil, err
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("order-service"),
            semconv.ServiceVersionKey.String("1.0.0"),
            attribute.String("environment", "production"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}

func main() {
    tp, err := initTracer()
    if err != nil {
        log.Fatal(err)
    }
    defer func() {
        if err := tp.Shutdown(context.Background()); err != nil {
            log.Printf("Error shutting down tracer provider: %v", err)
        }
    }()

    // gRPC server con tracing
    s := grpc.NewServer(
        grpc.UnaryInterceptor(otelgrpc.UnaryServerInterceptor()),
        grpc.StreamInterceptor(otelgrpc.StreamServerInterceptor()),
    )

    // gRPC client con tracing
    conn, err := grpc.Dial(
        "localhost:50051",
        grpc.WithUnaryInterceptor(otelgrpc.UnaryClientInterceptor()),
        grpc.WithStreamInterceptor(otelgrpc.StreamClientInterceptor()),
    )
}

// Uso en handlers
func processOrder(ctx context.Context, orderID string) error {
    tracer := otel.Tracer("order-processor")

    ctx, span := tracer.Start(ctx, "processOrder")
    defer span.End()

    span.SetAttributes(
        attribute.String("order.id", orderID),
    )

    // Validate order
    ctx, validateSpan := tracer.Start(ctx, "validateOrder")
    valid, err := validateOrder(ctx, orderID)
    validateSpan.SetAttributes(attribute.Bool("order.valid", valid))
    validateSpan.End()

    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }

    // Process payment
    ctx, paymentSpan := tracer.Start(ctx, "processPayment")
    payment, err := processPayment(ctx, orderID)
    paymentSpan.SetAttributes(
        attribute.String("payment.method", payment.Method),
        attribute.Float64("payment.amount", payment.Amount),
    )
    paymentSpan.End()

    if err != nil {
        span.RecordError(err)
        return err
    }

    span.AddEvent("order_processed", oteltrace.WithAttributes(
        attribute.String("order.id", orderID),
        attribute.String("status", "completed"),
    ))

    return nil
}
```

---

### 1.2 Structured Logging con Correlation IDs
**Dificultad:** ⭐⭐⭐⭐

```python
import logging
import structlog
from contextvars import ContextVar
import uuid

# Context vars para trace/correlation IDs
trace_id_var: ContextVar[str] = ContextVar('trace_id', default='')
request_id_var: ContextVar[str] = ContextVar('request_id', default='')
user_id_var: ContextVar[str] = ContextVar('user_id', default='')

# Configurar structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False
)

logger = structlog.get_logger()

# Middleware para correlation IDs
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # Generar o extraer IDs
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    trace_id = request.headers.get('X-Trace-ID', str(uuid.uuid4()))

    # Guardar en context vars
    request_id_var.set(request_id)
    trace_id_var.set(trace_id)

    # Bind to structlog
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        trace_id=trace_id,
        method=request.method,
        path=request.url.path
    )

    logger.info("request_started")

    response = await call_next(request)

    # Agregar headers a response
    response.headers['X-Request-ID'] = request_id
    response.headers['X-Trace-ID'] = trace_id

    logger.info(
        "request_completed",
        status_code=response.status_code,
        duration_ms=(time.time() - start) * 1000
    )

    return response

# Propagación a servicios externos
async def call_external_service(url: str, data: dict):
    headers = {
        'X-Request-ID': request_id_var.get(),
        'X-Trace-ID': trace_id_var.get(),
        'Content-Type': 'application/json'
    }

    logger.info(
        "calling_external_service",
        url=url,
        service=url.split('/')[2]
    )

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    logger.info(
        "external_service_response",
        url=url,
        status_code=response.status_code
    )

    return response

# Logging con contexto de negocio
@app.post("/orders")
async def create_order(order_data: dict, user_id: int):
    # Bind user context
    structlog.contextvars.bind_contextvars(user_id=user_id)

    logger.info(
        "creating_order",
        items_count=len(order_data['items']),
        total_amount=order_data['total']
    )

    try:
        order = await process_order(order_data, user_id)

        logger.info(
            "order_created",
            order_id=order.id,
            status=order.status
        )

        return order

    except InsufficientInventoryError as e:
        logger.warning(
            "order_failed_inventory",
            reason="insufficient_inventory",
            missing_items=e.missing_items
        )
        raise

    except PaymentError as e:
        logger.error(
            "order_failed_payment",
            reason="payment_failed",
            payment_method=order_data['payment']['method'],
            error=str(e)
        )
        raise
```

---

## CATEGORÍA 2: API Versioning y Deprecation

### 2.1 API Versioning Strategies
**Dificultad:** ⭐⭐⭐⭐

```python
from fastapi import FastAPI, Header, Request, HTTPException
from typing import Optional
from enum import Enum

class APIVersion(str, Enum):
    V1 = "1.0"
    V2 = "2.0"
    V3 = "3.0"

app = FastAPI()

# Estrategia 1: URL Versioning
@app.get("/api/v1/users/{user_id}")
async def get_user_v1(user_id: int):
    # Legacy response format
    user = await db.get_user(user_id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.get("/api/v2/users/{user_id}")
async def get_user_v2(user_id: int):
    # New response format con más campos
    user = await db.get_user(user_id)
    return {
        "user": {
            "id": user.id,
            "profile": {
                "name": user.name,
                "email": user.email,
                "avatar_url": user.avatar_url
            },
            "metadata": {
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
        }
    }

# Estrategia 2: Header Versioning
class VersionedRoute:
    def __init__(self):
        self.handlers = {}

    def version(self, version: str):
        def decorator(func):
            self.handlers[version] = func
            return func
        return decorator

    async def __call__(self, request: Request, *args, **kwargs):
        # Obtener versión del header
        api_version = request.headers.get('API-Version', '1.0')

        if api_version not in self.handlers:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported API version: {api_version}"
            )

        handler = self.handlers[api_version]
        return await handler(request, *args, **kwargs)

# Uso
get_user_route = VersionedRoute()

@get_user_route.version("1.0")
async def get_user_v1(request: Request, user_id: int):
    return {"id": user_id, "name": "John"}

@get_user_route.version("2.0")
async def get_user_v2(request: Request, user_id: int):
    return {"user": {"id": user_id, "profile": {"name": "John"}}}

app.add_api_route("/users/{user_id}", get_user_route, methods=["GET"])

# Estrategia 3: Content Negotiation
from fastapi.responses import JSONResponse

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    request: Request
):
    accept_header = request.headers.get('Accept', 'application/vnd.api.v1+json')

    user = await db.get_user(user_id)

    if 'v1' in accept_header:
        return JSONResponse(
            content={"id": user.id, "name": user.name},
            headers={"API-Version": "1.0"}
        )
    elif 'v2' in accept_header:
        return JSONResponse(
            content={
                "user": {
                    "id": user.id,
                    "profile": {"name": user.name}
                }
            },
            headers={"API-Version": "2.0"}
        )
    else:
        raise HTTPException(status_code=406, detail="Unsupported media type")

# Deprecation warnings
import warnings
from datetime import datetime, timedelta

class DeprecationWarning:
    def __init__(
        self,
        version: str,
        sunset_date: datetime,
        migration_guide_url: str
    ):
        self.version = version
        self.sunset_date = sunset_date
        self.migration_guide_url = migration_guide_url

def deprecated(
    deprecated_version: str,
    sunset_date: datetime,
    migration_guide: str
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Agregar headers de deprecation
            response = await func(*args, **kwargs)

            if isinstance(response, JSONResponse):
                response.headers['Deprecation'] = 'true'
                response.headers['Sunset'] = sunset_date.isoformat()
                response.headers['Link'] = f'<{migration_guide}>; rel="deprecation"'

            return response
        return wrapper
    return decorator

@app.get("/api/v1/users")
@deprecated(
    deprecated_version="1.0",
    sunset_date=datetime(2025, 12, 31),
    migration_guide="https://docs.api.com/migration/v1-to-v2"
)
async def list_users_v1():
    # Log deprecation metrics
    deprecation_metrics.increment('v1_users_list')

    return await db.list_users()

# Schema evolution con backward compatibility
from pydantic import BaseModel, Field

class UserV1(BaseModel):
    id: int
    name: str
    email: str

class UserV2(BaseModel):
    id: int
    name: str
    email: str
    avatar_url: Optional[str] = None  # Nuevo campo opcional
    phone: Optional[str] = None       # Nuevo campo opcional

    # Método para convertir a V1 (backward compatibility)
    def to_v1(self) -> UserV1:
        return UserV1(
            id=self.id,
            name=self.name,
            email=self.email
        )

# Response transformer basado en versión
class VersionedResponse:
    @staticmethod
    def transform(data: Any, version: str):
        if version == "1.0":
            if isinstance(data, UserV2):
                return data.to_v1()
            elif isinstance(data, list):
                return [item.to_v1() if isinstance(item, UserV2) else item for item in data]
        return data

@app.middleware("http")
async def version_transformer_middleware(request: Request, call_next):
    response = await call_next(request)

    api_version = request.headers.get('API-Version', '2.0')

    # Transform response based on version
    if hasattr(response, 'body'):
        # Parse and transform
        pass

    return response
```

---

## CATEGORÍA 3: Idempotency y Exactly-Once Semantics

### 3.1 Idempotent API Operations
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from fastapi import FastAPI, Header, HTTPException
import hashlib
import json
from datetime import datetime, timedelta

class IdempotencyManager:
    def __init__(self, redis_client, ttl: int = 86400):
        self.redis = redis_client
        self.ttl = ttl

    async def is_duplicate(self, idempotency_key: str) -> Optional[dict]:
        """Check if request was already processed"""
        result = await self.redis.get(f"idempotency:{idempotency_key}")
        if result:
            return json.loads(result)
        return None

    async def store_result(self, idempotency_key: str, response: dict, status_code: int):
        """Store result of idempotent operation"""
        data = {
            "response": response,
            "status_code": status_code,
            "created_at": datetime.utcnow().isoformat()
        }
        await self.redis.setex(
            f"idempotency:{idempotency_key}",
            self.ttl,
            json.dumps(data)
        )

    async def acquire_lock(self, idempotency_key: str, timeout: int = 10) -> bool:
        """Acquire lock to prevent concurrent duplicate requests"""
        lock_key = f"idempotency:lock:{idempotency_key}"
        acquired = await self.redis.set(lock_key, "1", nx=True, ex=timeout)
        return bool(acquired)

    async def release_lock(self, idempotency_key: str):
        """Release lock"""
        await self.redis.delete(f"idempotency:lock:{idempotency_key}")

idempotency_manager = IdempotencyManager(redis_client)

# Middleware de idempotencia
@app.middleware("http")
async def idempotency_middleware(request: Request, call_next):
    # Solo para operaciones mutables
    if request.method not in ['POST', 'PUT', 'PATCH', 'DELETE']:
        return await call_next(request)

    idempotency_key = request.headers.get('Idempotency-Key')

    if not idempotency_key:
        # Idempotency key requerido para operaciones críticas
        if request.url.path in ['/api/payments', '/api/orders']:
            raise HTTPException(
                status_code=400,
                detail="Idempotency-Key header required"
            )
        return await call_next(request)

    # Check for duplicate
    cached_result = await idempotency_manager.is_duplicate(idempotency_key)
    if cached_result:
        return JSONResponse(
            content=cached_result['response'],
            status_code=cached_result['status_code'],
            headers={'X-Idempotent-Replayed': 'true'}
        )

    # Acquire lock to prevent concurrent duplicates
    acquired = await idempotency_manager.acquire_lock(idempotency_key)
    if not acquired:
        # Another request with same key is processing
        raise HTTPException(
            status_code=409,
            detail="Concurrent request with same idempotency key"
        )

    try:
        # Process request
        response = await call_next(request)

        # Store result
        if response.status_code < 500:  # Don't cache server errors
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            response_data = json.loads(response_body)

            await idempotency_manager.store_result(
                idempotency_key,
                response_data,
                response.status_code
            )

            # Recreate response
            return JSONResponse(
                content=response_data,
                status_code=response.status_code
            )

        return response

    finally:
        await idempotency_manager.release_lock(idempotency_key)

# Generación automática de idempotency key
def generate_idempotency_key(method: str, url: str, body: dict) -> str:
    """Generate deterministic idempotency key from request"""
    data = f"{method}:{url}:{json.dumps(body, sort_keys=True)}"
    return hashlib.sha256(data.encode()).hexdigest()

# Uso en operaciones críticas
@app.post("/payments")
async def create_payment(
    payment_data: dict,
    idempotency_key: str = Header(..., alias="Idempotency-Key")
):
    # Idempotency ya manejado por middleware

    # Procesar pago
    payment = await payment_service.process(payment_data)

    return {
        "payment_id": payment.id,
        "status": payment.status,
        "amount": payment.amount
    }

# Database-level idempotency con unique constraints
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    idempotency_key = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('idempotency_key', name='uix_idempotency_key'),
    )

async def process_payment_idempotent(idempotency_key: str, payment_data: dict):
    try:
        # Try to insert
        payment = Payment(
            idempotency_key=idempotency_key,
            user_id=payment_data['user_id'],
            amount=payment_data['amount'],
            status='pending'
        )
        db.add(payment)
        await db.commit()

        # Process payment
        result = await payment_gateway.charge(payment)

        payment.status = result.status
        await db.commit()

        return payment

    except IntegrityError as e:
        # Duplicate idempotency key - return existing payment
        await db.rollback()
        payment = await db.query(Payment).filter(
            Payment.idempotency_key == idempotency_key
        ).first()
        return payment
```

---

## CATEGORÍA 4: WebSockets y Real-Time Communication

### 4.1 WebSocket Connection Management
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, List
import asyncio
import json

class ConnectionManager:
    def __init__(self):
        # user_id -> Set[WebSocket]
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # room_id -> Set[user_id]
        self.rooms: Dict[str, Set[str]] = {}
        # WebSocket -> user_id
        self.connection_to_user: Dict[WebSocket, str] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()

        async with self.lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()

            self.active_connections[user_id].add(websocket)
            self.connection_to_user[websocket] = user_id

        await self.broadcast_user_status(user_id, "online")

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            user_id = self.connection_to_user.pop(websocket, None)

            if user_id and user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)

                # Remove user if no more connections
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
                    await self.broadcast_user_status(user_id, "offline")

                    # Remove from all rooms
                    for room_id in list(self.rooms.keys()):
                        self.rooms[room_id].discard(user_id)
                        if not self.rooms[room_id]:
                            del self.rooms[room_id]

    async def send_personal_message(self, user_id: str, message: dict):
        """Send to all connections of a specific user"""
        if user_id not in self.active_connections:
            return

        # Send to all user's devices
        disconnected = set()
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)

        # Clean up dead connections
        if disconnected:
            async with self.lock:
                self.active_connections[user_id] -= disconnected

    async def broadcast_to_room(self, room_id: str, message: dict, exclude_user: str = None):
        """Broadcast to all users in a room"""
        if room_id not in self.rooms:
            return

        for user_id in self.rooms[room_id]:
            if user_id != exclude_user:
                await self.send_personal_message(user_id, message)

    async def join_room(self, user_id: str, room_id: str):
        async with self.lock:
            if room_id not in self.rooms:
                self.rooms[room_id] = set()
            self.rooms[room_id].add(user_id)

        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "room_id": room_id
        }, exclude_user=user_id)

    async def leave_room(self, user_id: str, room_id: str):
        async with self.lock:
            if room_id in self.rooms:
                self.rooms[room_id].discard(user_id)

        await self.broadcast_to_room(room_id, {
            "type": "user_left",
            "user_id": user_id,
            "room_id": room_id
        })

    async def broadcast_user_status(self, user_id: str, status: str):
        """Notify all connected users about status change"""
        message = {
            "type": "user_status",
            "user_id": user_id,
            "status": status
        }

        for uid in self.active_connections.keys():
            if uid != user_id:
                await self.send_personal_message(uid, message)

    def get_room_users(self, room_id: str) -> List[str]:
        return list(self.rooms.get(room_id, set()))

    def get_online_users(self) -> List[str]:
        return list(self.active_connections.keys())

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()

            message_type = data.get('type')

            if message_type == 'join_room':
                room_id = data['room_id']
                await manager.join_room(user_id, room_id)

            elif message_type == 'leave_room':
                room_id = data['room_id']
                await manager.leave_room(user_id, room_id)

            elif message_type == 'message':
                room_id = data['room_id']
                message = {
                    "type": "message",
                    "user_id": user_id,
                    "content": data['content'],
                    "timestamp": datetime.utcnow().isoformat()
                }
                await manager.broadcast_to_room(room_id, message)

            elif message_type == 'typing':
                room_id = data['room_id']
                await manager.broadcast_to_room(room_id, {
                    "type": "typing",
                    "user_id": user_id
                }, exclude_user=user_id)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

# Heartbeat/Ping-Pong para detectar conexiones muertas
class HeartbeatManager:
    def __init__(self, connection_manager: ConnectionManager, interval: int = 30):
        self.manager = connection_manager
        self.interval = interval
        self.last_pong: Dict[WebSocket, float] = {}
        self.task = None

    async def start(self):
        self.task = asyncio.create_task(self._heartbeat_loop())

    async def stop(self):
        if self.task:
            self.task.cancel()

    async def _heartbeat_loop(self):
        while True:
            await asyncio.sleep(self.interval)
            await self._check_connections()

    async def _check_connections(self):
        now = time.time()
        dead_connections = []

        for websocket in list(self.manager.connection_to_user.keys()):
            try:
                await websocket.send_json({"type": "ping"})

                # Check if last pong was too long ago
                last_pong = self.last_pong.get(websocket, now)
                if now - last_pong > self.interval * 2:
                    dead_connections.append(websocket)

            except Exception:
                dead_connections.append(websocket)

        # Disconnect dead connections
        for websocket in dead_connections:
            await self.manager.disconnect(websocket)

    def record_pong(self, websocket: WebSocket):
        self.last_pong[websocket] = time.time()

heartbeat = HeartbeatManager(manager)

@app.on_event("startup")
async def startup():
    await heartbeat.start()

@app.on_event("shutdown")
async def shutdown():
    await heartbeat.stop()

# Rate limiting para WebSocket messages
class WebSocketRateLimiter:
    def __init__(self, max_messages: int = 10, window_seconds: int = 1):
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self.messages: Dict[str, List[float]] = {}

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()

        if user_id not in self.messages:
            self.messages[user_id] = []

        # Remove old messages
        self.messages[user_id] = [
            ts for ts in self.messages[user_id]
            if now - ts < self.window_seconds
        ]

        if len(self.messages[user_id]) >= self.max_messages:
            return False

        self.messages[user_id].append(now)
        return True

rate_limiter = WebSocketRateLimiter(max_messages=10, window_seconds=1)
```

---

Continúa con más categorías...

---

## Resumen de Problemas Backend Avanzados

| Problema | Dificultad | Impacto en Producción | Prioridad |
|----------|------------|----------------------|-----------|
| Distributed Tracing | 5 | 5 | **CRÍTICA** |
| Idempotency | 5 | 5 | **CRÍTICA** |
| WebSocket Management | 5 | 4 | **ALTA** |
| API Versioning | 4 | 4 | **ALTA** |
| Correlation IDs | 4 | 5 | **CRÍTICA** |
| Real-time Communication | 5 | 4 | **ALTA** |

**El siguiente archivo continuará con:**
- GraphQL N+1 Problem y DataLoader
- Database Sharding Strategies
- Distributed Transactions (Saga Pattern, 2PC)
- Webhooks con retry y security
- Stream Processing (Kafka, Apache Flink)
- Security: OAuth2, JWT, API Keys rotation
