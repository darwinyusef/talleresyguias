# Arquitectura Técnica Avanzada 2026: Decisiones de Diseño

## Objetivo
Decisiones técnicas profundas de arquitectura de software: patrones avanzados, trade-offs, y soluciones probadas para sistemas distribuidos modernos.

---

## CATEGORÍA 1: Domain-Driven Design Avanzado

### 1.1 Bounded Contexts y Context Mapping
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
La mayoría de proyectos fallan en DDD porque no definen bounded contexts correctamente.

**Patrones de Context Mapping:**

```
1. SHARED KERNEL
┌──────────────┐     ┌──────────────┐
│   Order      │────▶│   Billing    │
│   Context    │     │   Context    │
└──────────────┘     └──────────────┘
      │                     │
      └─────────┬───────────┘
            Shared Model
         (CustomerInfo)

✅ Usar cuando:
- Equipos muy colaborativos
- Modelo realmente compartido
- Cambios coordinados

❌ Evitar si:
- Equipos independientes
- Ritmos de deploy diferentes
```

```
2. CUSTOMER-SUPPLIER
┌──────────────┐     ┌──────────────┐
│   Catalog    │────▶│   Search     │
│  (Upstream)  │     │ (Downstream) │
└──────────────┘     └──────────────┘

Search depende de Catalog
Catalog publica contrato
Search consume contrato

✅ Usar cuando:
- Relación clara de dependencia
- Upstream tiene más poder
- Contratos bien definidos
```

```
3. ANTI-CORRUPTION LAYER
┌──────────────┐     ┌─────────┐     ┌──────────────┐
│   Modern     │────▶│   ACL   │────▶│   Legacy     │
│   System     │     │(Adapter)│     │   System     │
└──────────────┘     └─────────┘     └──────────────┘

ACL traduce entre modelos

✅ Usar cuando:
- Integrar con legacy
- Proteger modelo limpio
- Diferentes paradigmas
```

**Implementación Práctica:**

```python
# Bounded Context: Order Management
# contexts/order/domain/models.py

from dataclasses import dataclass
from decimal import Decimal
from typing import List
from enum import Enum

# Aggregate Root
@dataclass
class Order:
    """
    Order Aggregate - Consistency Boundary
    Todo lo relacionado a la orden debe pasar por aquí
    """
    id: OrderId
    customer_id: CustomerId
    items: List[OrderLine]
    status: OrderStatus
    total: Money
    _version: int  # Optimistic locking

    def add_item(self, product_id: ProductId, quantity: int, price: Money):
        """
        Business rule: No se puede agregar items a orden confirmada
        """
        if self.status != OrderStatus.DRAFT:
            raise OrderAlreadyConfirmedError()

        if quantity <= 0:
            raise InvalidQuantityError()

        # Domain event
        self._apply_event(ItemAddedToOrder(
            order_id=self.id,
            product_id=product_id,
            quantity=quantity,
            price=price
        ))

    def confirm(self):
        """
        Business rule: Solo se puede confirmar si hay items
        """
        if not self.items:
            raise EmptyOrderError()

        if self.status != OrderStatus.DRAFT:
            raise OrderAlreadyConfirmedError()

        self._apply_event(OrderConfirmed(
            order_id=self.id,
            confirmed_at=datetime.utcnow()
        ))

    def _apply_event(self, event: DomainEvent):
        """Apply event to aggregate state"""
        if isinstance(event, ItemAddedToOrder):
            self.items.append(OrderLine(
                product_id=event.product_id,
                quantity=event.quantity,
                price=event.price
            ))
            self._recalculate_total()

        elif isinstance(event, OrderConfirmed):
            self.status = OrderStatus.CONFIRMED

        self._version += 1
        self._uncommitted_events.append(event)

    def _recalculate_total(self):
        self.total = Money(
            sum(line.price.amount * line.quantity for line in self.items)
        )

# Value Objects
@dataclass(frozen=True)
class OrderId:
    value: str

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __add__(self, other):
        if self.currency != other.currency:
            raise CurrencyMismatchError()
        return Money(self.amount + other.amount, self.currency)

# Domain Events
@dataclass
class OrderConfirmed:
    order_id: OrderId
    confirmed_at: datetime
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

# Repository Interface (en dominio, implementación en infra)
class OrderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        pass

    @abstractmethod
    async def save(self, order: Order) -> None:
        pass

# Application Service (orquesta use cases)
class OrderApplicationService:
    def __init__(
        self,
        order_repo: OrderRepository,
        event_bus: EventBus,
        unit_of_work: UnitOfWork
    ):
        self.order_repo = order_repo
        self.event_bus = event_bus
        self.uow = unit_of_work

    async def confirm_order(self, command: ConfirmOrderCommand) -> OrderId:
        """
        Use case: Confirmar orden
        Garantías: Atomicidad (UoW), Eventos publicados
        """
        async with self.uow:
            # Load aggregate
            order = await self.order_repo.find_by_id(command.order_id)

            if not order:
                raise OrderNotFoundError(command.order_id)

            # Execute business logic
            order.confirm()

            # Save aggregate
            await self.order_repo.save(order)

            # Publish events
            for event in order.uncommitted_events:
                await self.event_bus.publish(event)

            # Commit transaction
            await self.uow.commit()

        return order.id
```

**Anti-Corruption Layer (ACL) para Legacy:**

```python
# ACL entre nuevo sistema y legacy
class LegacyOrderAdapter:
    """
    ACL que traduce entre nuestro modelo limpio
    y el sistema legacy horrible
    """

    def __init__(self, legacy_client: LegacySystemClient):
        self.legacy_client = legacy_client

    async def fetch_order(self, order_id: OrderId) -> Order:
        """
        Traduce del formato legacy a nuestro modelo
        """
        # Legacy usa XML horrible
        legacy_xml = await self.legacy_client.get_order(order_id.value)

        # Parse XML nightmare
        legacy_data = self._parse_legacy_xml(legacy_xml)

        # Construir nuestro modelo limpio
        return Order(
            id=OrderId(legacy_data['ORDER_NUM']),
            customer_id=CustomerId(legacy_data['CUST_ID']),
            items=[
                OrderLine(
                    product_id=ProductId(item['PROD_CODE']),
                    quantity=int(item['QTY']),
                    price=Money(Decimal(item['PRICE']) / 100)  # Legacy usa centavos
                )
                for item in legacy_data['ITEMS']
            ],
            status=self._map_legacy_status(legacy_data['STATUS']),
            total=Money(Decimal(legacy_data['TOTAL_AMT']) / 100)
        )

    def _map_legacy_status(self, legacy_status: str) -> OrderStatus:
        """Mapeo de estados legacy a nuestro modelo"""
        mapping = {
            'PEND': OrderStatus.DRAFT,
            'CONF': OrderStatus.CONFIRMED,
            'SHIP': OrderStatus.SHIPPED,
            'CANC': OrderStatus.CANCELLED
        }
        return mapping.get(legacy_status, OrderStatus.DRAFT)

    async def save_order(self, order: Order):
        """
        Traduce de nuestro modelo al formato legacy
        Envuelve la complejidad del sistema viejo
        """
        legacy_data = {
            'ORDER_NUM': order.id.value,
            'CUST_ID': order.customer_id.value,
            'TOTAL_AMT': int(order.total.amount * 100),
            'STATUS': self._map_to_legacy_status(order.status),
            'ITEMS': [
                {
                    'PROD_CODE': line.product_id.value,
                    'QTY': line.quantity,
                    'PRICE': int(line.price.amount * 100)
                }
                for line in order.items
            ]
        }

        await self.legacy_client.update_order(legacy_data)
```

---

### 1.2 Aggregate Design: Tamaño y Transacciones
**Dificultad:** ⭐⭐⭐⭐⭐

**Principios:**

1. **Aggregates pequeños**
   - Idealmente 1 entidad + value objects
   - Máximo 2-3 entidades relacionadas

2. **Modificar 1 aggregate por transacción**
   - Consistencia inmediata solo dentro del aggregate
   - Consistencia eventual entre aggregates

3. **Referencias por ID, no por objeto**

**❌ Mal diseño:**
```python
# Aggregate demasiado grande
class Customer:
    id: CustomerId
    orders: List[Order]  # ❌ No!
    payments: List[Payment]  # ❌ No!
    addresses: List[Address]  # ❌ No!
    preferences: UserPreferences  # ❌ No!

    # Transacción gigante que lockea todo
    def place_order(self, items):
        order = Order(...)
        self.orders.append(order)
        # Lockea customer, todos sus orders, payments, etc.
```

**✅ Buen diseño:**
```python
# Aggregates pequeños e independientes
class Customer:
    id: CustomerId
    email: Email
    name: PersonName
    # Solo datos de identidad

class Order:
    id: OrderId
    customer_id: CustomerId  # ✅ Referencia por ID
    items: List[OrderLine]
    status: OrderStatus
    # Solo datos de la orden

class Payment:
    id: PaymentId
    order_id: OrderId  # ✅ Referencia por ID
    amount: Money
    status: PaymentStatus
```

**Consistencia Eventual con Saga:**

```python
# Proceso de negocio que cruza aggregates
class OrderSaga:
    """
    Coordina proceso que involucra múltiples aggregates:
    1. Crear Order
    2. Reservar Inventory
    3. Procesar Payment
    4. Crear Shipment
    """

    async def handle_order_confirmed(self, event: OrderConfirmed):
        """
        Step 1: Order confirmado, ahora reservar inventario
        """
        try:
            # Cada operación modifica 1 solo aggregate
            await self.inventory_service.reserve(
                order_id=event.order_id,
                items=event.items
            )

            # Publish event para siguiente step
            await self.event_bus.publish(
                InventoryReserved(order_id=event.order_id)
            )

        except InsufficientInventoryError:
            # Compensate: cancelar orden
            await self.order_service.cancel(event.order_id)

    async def handle_inventory_reserved(self, event: InventoryReserved):
        """
        Step 2: Inventario reservado, procesar pago
        """
        try:
            await self.payment_service.charge(
                order_id=event.order_id
            )

            await self.event_bus.publish(
                PaymentCompleted(order_id=event.order_id)
            )

        except PaymentFailedError:
            # Compensate: liberar inventario
            await self.inventory_service.release(event.order_id)
            await self.order_service.cancel(event.order_id)

    # etc...
```

---

## CATEGORÍA 2: Multi-Tenancy Architecture

### 2.1 Estrategias de Multi-Tenancy
**Dificultad:** ⭐⭐⭐⭐⭐

**Patrones:**

```
1. DATABASE PER TENANT (Máximo aislamiento)
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Tenant A│  │ Tenant B│  │ Tenant C│
│   DB    │  │   DB    │  │   DB    │
└─────────┘  └─────────┘  └─────────┘

✅ Pro:
- Aislamiento total
- Performance predecible
- Fácil backup/restore por tenant
- Compliance (data residency)

❌ Con:
- Costo alto (N databases)
- Complejidad operacional
- Migrations complejas

Usar cuando:
- Tenants grandes (enterprise)
- Compliance estricto
- Pricing permite costo
```

```
2. SCHEMA PER TENANT (Balance)
┌───────────────────────────┐
│     PostgreSQL DB         │
├──────────┬────────┬───────┤
│ tenant_a │tenant_b│tenant_c│
│ (schema) │(schema)│(schema)│
└──────────┴────────┴───────┘

✅ Pro:
- Buen aislamiento
- Menor costo que DB per tenant
- Performance razonable

❌ Con:
- Límite de schemas en DB
- Migrations más complejas

Usar cuando:
- 10-1000 tenants
- Tenants medianos
```

```
3. SHARED SCHEMA (Máxima densidad)
┌─────────────────────────┐
│   Table: orders         │
├──────────┬──────────────┤
│tenant_id │ order_data   │
├──────────┼──────────────┤
│    A     │  {...}       │
│    A     │  {...}       │
│    B     │  {...}       │
│    C     │  {...}       │
└──────────┴──────────────┘

✅ Pro:
- Mínimo costo
- Escala a millones de tenants
- Operaciones simples

❌ Con:
- Noisy neighbor problem
- Difícil garantizar performance
- Risk de data leakage

Usar cuando:
- SaaS con millones de tenants pequeños
- Free tier / freemium
```

**Implementación Shared Schema:**

```python
# Context Manager para Row-Level Security
class TenantContext:
    """
    Maneja tenant_id en request context
    Previene data leakage entre tenants
    """

    _tenant_id: ContextVar[str] = ContextVar('tenant_id')

    @classmethod
    def set_current_tenant(cls, tenant_id: str):
        cls._tenant_id.set(tenant_id)

    @classmethod
    def get_current_tenant(cls) -> str:
        tenant_id = cls._tenant_id.get(None)
        if not tenant_id:
            raise NoTenantContextError()
        return tenant_id

    @classmethod
    def clear(cls):
        cls._tenant_id.set(None)

# Middleware
@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    """
    Extrae tenant_id de request y lo setea en context
    """
    # Opción 1: Subdomain (acme.myapp.com)
    tenant_id = extract_tenant_from_subdomain(request.url.host)

    # Opción 2: Header
    # tenant_id = request.headers.get('X-Tenant-ID')

    # Opción 3: JWT claim
    # tenant_id = request.state.user.tenant_id

    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant not identified")

    TenantContext.set_current_tenant(tenant_id)

    try:
        response = await call_next(request)
        return response
    finally:
        TenantContext.clear()

# Repository con tenant filtering automático
class TenantAwareRepository:
    """
    Todos los queries automáticamente filtran por tenant
    """

    async def find_by_id(self, order_id: str) -> Optional[Order]:
        tenant_id = TenantContext.get_current_tenant()

        result = await db.execute(
            """
            SELECT * FROM orders
            WHERE id = :order_id AND tenant_id = :tenant_id
            """,
            {"order_id": order_id, "tenant_id": tenant_id}
        )

        return result.first()

    async def save(self, order: Order):
        tenant_id = TenantContext.get_current_tenant()

        # Siempre inyectar tenant_id
        await db.execute(
            """
            INSERT INTO orders (id, tenant_id, customer_id, total, status)
            VALUES (:id, :tenant_id, :customer_id, :total, :status)
            """,
            {
                "id": order.id,
                "tenant_id": tenant_id,  # ✅ Automático
                "customer_id": order.customer_id,
                "total": order.total,
                "status": order.status
            }
        )

# PostgreSQL Row-Level Security (RLS)
"""
-- Habilitar RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Policy: solo ver orders de tu tenant
CREATE POLICY tenant_isolation_policy ON orders
    USING (tenant_id = current_setting('app.current_tenant_id')::text);

-- En application code:
-- SET app.current_tenant_id = 'tenant_123';
"""

# SQLAlchemy con tenant filter automático
from sqlalchemy import event
from sqlalchemy.orm import Session

@event.listens_for(Session, "before_flush")
def inject_tenant_id(session, flush_context, instances):
    """Inject tenant_id antes de save"""
    tenant_id = TenantContext.get_current_tenant()

    for instance in session.new:
        if hasattr(instance, 'tenant_id'):
            instance.tenant_id = tenant_id
```

**Isolation Testing:**

```python
# Test crítico: prevenir data leakage
@pytest.mark.asyncio
async def test_tenant_isolation():
    """
    Asegurar que tenant A no puede ver datos de tenant B
    """

    # Setup: Crear datos para tenant A
    TenantContext.set_current_tenant('tenant_a')
    order_a = await order_service.create_order(...)

    # Setup: Crear datos para tenant B
    TenantContext.set_current_tenant('tenant_b')
    order_b = await order_service.create_order(...)

    # Test: Tenant A no debe ver order de tenant B
    TenantContext.set_current_tenant('tenant_a')
    result = await order_service.get_order(order_b.id)

    assert result is None  # ✅ No data leakage

    # Test: Tenant B no debe ver order de tenant A
    TenantContext.set_current_tenant('tenant_b')
    result = await order_service.get_order(order_a.id)

    assert result is None  # ✅ No data leakage
```

---

### 2.2 Tenant-Specific Configuration
**Dificultad:** ⭐⭐⭐⭐

```python
# Feature flags y config por tenant
class TenantConfigManager:
    """
    Manejar configuración específica por tenant
    - Feature flags
    - Rate limits
    - Customizations
    - Pricing tier
    """

    def __init__(self, cache: Redis, db):
        self.cache = cache
        self.db = db

    async def get_feature_flags(self, tenant_id: str) -> dict:
        """
        Get feature flags para tenant
        Cached agresivamente
        """

        cache_key = f"tenant_config:{tenant_id}:features"
        cached = await self.cache.get(cache_key)

        if cached:
            return json.loads(cached)

        # Load from DB
        config = await self.db.execute(
            "SELECT features FROM tenant_config WHERE tenant_id = $1",
            tenant_id
        )

        features = config.first()['features'] if config else {}

        # Cache por 5 minutos
        await self.cache.setex(cache_key, 300, json.dumps(features))

        return features

    async def is_feature_enabled(
        self,
        tenant_id: str,
        feature: str
    ) -> bool:
        """
        Check if feature habilitado para tenant
        """
        features = await self.get_feature_flags(tenant_id)
        return features.get(feature, False)

# Usage
@app.post("/api/orders")
async def create_order(order_data: dict):
    tenant_id = TenantContext.get_current_tenant()

    # Feature flag check
    if await config_manager.is_feature_enabled(tenant_id, 'bulk_orders'):
        # Feature available para este tenant
        return await create_bulk_order(order_data)
    else:
        # Feature no disponible
        raise HTTPException(
            status_code=403,
            detail="Bulk orders not available in your plan"
        )

# Tenant-specific rate limits
class TenantRateLimiter:
    async def check_limit(self, tenant_id: str, endpoint: str) -> bool:
        """
        Rate limit basado en tier del tenant
        """

        tier = await self._get_tenant_tier(tenant_id)

        limits = {
            'free': 100,      # 100 req/min
            'pro': 1000,      # 1000 req/min
            'enterprise': None  # Sin límite
        }

        limit = limits.get(tier, 100)

        if limit is None:
            return True  # Enterprise sin límite

        # Check Redis
        key = f"rate_limit:{tenant_id}:{endpoint}"
        current = await redis.incr(key)

        if current == 1:
            await redis.expire(key, 60)  # 1 minuto

        return current <= limit
```

---

## CATEGORÍA 3: Real-Time Architecture

### 3.1 WebSocket Scaling Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

**Challenge: Sticky Sessions en Kubernetes**

```yaml
# Problema: WebSockets requieren sticky sessions
# User → Pod A (websocket abierto)
# Si Pod A muere, conexión se pierde

# Solución 1: Redis PubSub para broadcast
┌────────┐    ┌────────┐    ┌────────┐
│ Pod A  │───▶│ Redis  │◀───│ Pod B  │
│ (WS)   │    │ PubSub │    │ (WS)   │
└────────┘    └────────┘    └────────┘
    │                           │
    │                           │
┌───▼──┐                   ┌───▼──┐
│User A│                   │User B│
└──────┘                   └──────┘

# User A envía mensaje
# Pod A publica a Redis
# Redis broadcast a todos los Pods
# Pod B recibe y envía a User B
```

**Implementación:**

```python
import redis.asyncio as redis
from fastapi import WebSocket
import json

class WebSocketManager:
    """
    Maneja WebSocket connections con Redis PubSub
    Permite broadcast entre múltiples pods/servers
    """

    def __init__(self, redis_url: str):
        self.redis_pub = redis.from_url(redis_url)
        self.redis_sub = redis.from_url(redis_url)
        self.connections: Dict[str, Set[WebSocket]] = {}
        self.pubsub = None

    async def start(self):
        """Start listening to Redis PubSub"""
        self.pubsub = self.redis_sub.pubsub()
        await self.pubsub.subscribe('chat_messages')

        # Background task para recibir mensajes
        asyncio.create_task(self._listen_redis())

    async def connect(self, websocket: WebSocket, user_id: str):
        """Connect new WebSocket client"""
        await websocket.accept()

        if user_id not in self.connections:
            self.connections[user_id] = set()

        self.connections[user_id].add(websocket)

        logger.info(f"User {user_id} connected (total connections: {len(self.connections[user_id])})")

    async def disconnect(self, websocket: WebSocket, user_id: str):
        """Disconnect WebSocket client"""
        if user_id in self.connections:
            self.connections[user_id].discard(websocket)

            if not self.connections[user_id]:
                del self.connections[user_id]

    async def send_message(
        self,
        room_id: str,
        message: dict,
        sender_id: str
    ):
        """
        Send message to room
        Publishes to Redis so all pods receive it
        """

        payload = {
            'room_id': room_id,
            'message': message,
            'sender_id': sender_id,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Publish to Redis
        await self.redis_pub.publish(
            'chat_messages',
            json.dumps(payload)
        )

    async def _listen_redis(self):
        """
        Listen to Redis PubSub
        Distribute messages to local WebSocket connections
        """

        async for message in self.pubsub.listen():
            if message['type'] != 'message':
                continue

            try:
                payload = json.loads(message['data'])

                room_id = payload['room_id']
                sender_id = payload['sender_id']

                # Get users in room (from DB/cache)
                user_ids = await self._get_room_users(room_id)

                # Send to local connections
                for user_id in user_ids:
                    if user_id == sender_id:
                        continue  # Don't echo back to sender

                    if user_id in self.connections:
                        await self._send_to_user(user_id, payload)

            except Exception as e:
                logger.error(f"Error processing Redis message: {e}")

    async def _send_to_user(self, user_id: str, payload: dict):
        """Send message to all connections of a user"""

        if user_id not in self.connections:
            return

        disconnected = set()

        for websocket in self.connections[user_id]:
            try:
                await websocket.send_json(payload)
            except Exception:
                disconnected.add(websocket)

        # Clean up dead connections
        self.connections[user_id] -= disconnected

# WebSocket endpoint
ws_manager = WebSocketManager("redis://localhost:6379")

@app.on_event("startup")
async def startup():
    await ws_manager.start()

@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await ws_manager.connect(websocket, user_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            # Broadcast to room
            await ws_manager.send_message(
                room_id=data['room_id'],
                message=data['message'],
                sender_id=user_id
            )

    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, user_id)
```

**Alternative: Server-Sent Events (SSE)**

```python
# SSE para notificaciones unidireccionales (server → client)
# Más simple que WebSockets si no necesitas bidireccional

from fastapi import Request
from sse_starlette.sse import EventSourceResponse

@app.get("/sse/notifications/{user_id}")
async def sse_notifications(request: Request, user_id: str):
    """
    SSE endpoint para notificaciones en tiempo real
    Más ligero que WebSocket
    """

    async def event_generator():
        # Subscribe to Redis for this user
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f'notifications:{user_id}')

        try:
            async for message in pubsub.listen():
                if message['type'] != 'message':
                    continue

                # Check if client disconnected
                if await request.is_disconnected():
                    break

                # Send event to client
                yield {
                    "event": "notification",
                    "data": message['data'].decode()
                }

        finally:
            await pubsub.unsubscribe(f'notifications:{user_id}')

    return EventSourceResponse(event_generator())

# Client-side (JavaScript)
"""
const eventSource = new EventSource('/sse/notifications/123');

eventSource.addEventListener('notification', (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
});
"""
```

---

## CATEGORÍA 4: API Versioning Strategies

### 4.1 Backward Compatibility Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

**Principio: Expand-Contract Pattern**

```
Phase 1: EXPAND (Agregar nueva versión sin romper vieja)
┌─────────────────────────────────┐
│  API v1 (deprecated)            │
│  /api/v1/users                  │
│  { id, name, email }            │
└─────────────────────────────────┘
┌─────────────────────────────────┐
│  API v2 (new)                   │
│  /api/v2/users                  │
│  { id, profile: {name, email} } │
└─────────────────────────────────┘
     ↓ Ambos funcionan
     ↓ Database maneja ambos formatos

Phase 2: CONTRACT (Remover versión vieja)
- Migrar clientes a v2
- Deprecar v1
- Eventualmente remover v1
```

**Implementación con Schema Evolution:**

```python
# Schema versioning con Pydantic
from pydantic import BaseModel, Field
from typing import Optional

# V1 Schema (deprecated)
class UserV1(BaseModel):
    id: int
    name: str
    email: str

# V2 Schema (current)
class UserV2(BaseModel):
    id: int
    profile: UserProfile
    settings: Optional[UserSettings] = None  # New field

class UserProfile(BaseModel):
    name: str
    email: str
    avatar_url: Optional[str] = None  # New field

# Internal model (lo que realmente guardamos)
class UserInternal(BaseModel):
    id: int
    name: str
    email: str
    avatar_url: Optional[str] = None
    settings: Optional[dict] = None

    def to_v1(self) -> UserV1:
        """Convert to V1 format"""
        return UserV1(
            id=self.id,
            name=self.name,
            email=self.email
        )

    def to_v2(self) -> UserV2:
        """Convert to V2 format"""
        return UserV2(
            id=self.id,
            profile=UserProfile(
                name=self.name,
                email=self.email,
                avatar_url=self.avatar_url
            ),
            settings=UserSettings(**self.settings) if self.settings else None
        )

# API Endpoints
@app.get("/api/v1/users/{user_id}", response_model=UserV1)
async def get_user_v1(user_id: int):
    """
    V1 endpoint (deprecated)
    """
    user = await user_repo.get(user_id)

    # Add deprecation warning header
    headers = {
        "Deprecation": "true",
        "Sunset": "2026-12-31",
        "Link": '<https://docs.api.com/migration/v2>; rel="deprecation"'
    }

    return Response(
        content=user.to_v1().json(),
        headers=headers
    )

@app.get("/api/v2/users/{user_id}", response_model=UserV2)
async def get_user_v2(user_id: int):
    """
    V2 endpoint (current)
    """
    user = await user_repo.get(user_id)
    return user.to_v2()

# Accept both formats for updates
@app.put("/api/v2/users/{user_id}")
async def update_user_v2(
    user_id: int,
    user_data: Union[UserV1, UserV2]
):
    """
    Accept both V1 and V2 formats
    Internally convert to UserInternal
    """

    if isinstance(user_data, UserV1):
        # V1 format - convert to internal
        internal_data = UserInternal(
            id=user_id,
            name=user_data.name,
            email=user_data.email
        )
    else:
        # V2 format
        internal_data = UserInternal(
            id=user_id,
            name=user_data.profile.name,
            email=user_data.profile.email,
            avatar_url=user_data.profile.avatar_url,
            settings=user_data.settings.dict() if user_data.settings else None
        )

    await user_repo.update(internal_data)
    return internal_data.to_v2()
```

**GraphQL Schema Evolution:**

```graphql
# GraphQL tiene ventaja: clientes piden solo lo que necesitan
# Más fácil agregar campos sin romper

type User {
  id: ID!
  name: String!
  email: String!

  # New fields - clientes viejos los ignoran
  avatarUrl: String
  createdAt: DateTime
  settings: UserSettings

  # Deprecated field
  fullName: String @deprecated(reason: "Use 'name' instead")
}

# Evolution sin breaking changes:
# 1. Agregar campos opcionales (nullable)
# 2. Deprecar campos (no remover inmediatamente)
# 3. Renombrar con alias para backward compatibility

type Query {
  # V1 (deprecated)
  user(id: ID!): User @deprecated(reason: "Use 'getUser' instead")

  # V2 (current)
  getUser(id: ID!): User
}
```

---

Continúa en siguiente sección...

---

## CATEGORÍA 5: Resilience Patterns Avanzados

### 5.1 Bulkhead Pattern
**Dificultad:** ⭐⭐⭐⭐

**Concepto: Aislamiento de recursos**

```
Sin Bulkhead:
┌─────────────────────────────┐
│   Thread Pool (100)         │
│  ████████████████████████   │
│  ↑ Heavy API consumió todo  │
└─────────────────────────────┘
❌ Otros endpoints no pueden procesar

Con Bulkhead:
┌──────────┬──────────┬────────┐
│Payment(20)│Search(30)│Auth(50)│
│  ███     │  ████    │  ██    │
└──────────┴──────────┴────────┘
✅ Falla aislada, resto sigue funcionando
```

**Implementación:**

```python
import asyncio
from asyncio import Semaphore

class Bulkhead:
    """
    Limita recursos por servicio
    Previene que un servicio lento consuma todos los recursos
    """

    def __init__(self, max_concurrent: int, max_queued: int = 0):
        self.semaphore = Semaphore(max_concurrent)
        self.max_queued = max_queued
        self.queue_semaphore = Semaphore(max_queued) if max_queued > 0 else None
        self.active = 0
        self.queued = 0

    async def execute(self, coro):
        """
        Execute coroutine with bulkhead protection
        """

        # Check if queue is full
        if self.max_queued > 0:
            if not self.queue_semaphore.locked():
                async with self.queue_semaphore:
                    self.queued += 1
                    try:
                        return await self._execute_with_semaphore(coro)
                    finally:
                        self.queued -= 1
            else:
                raise BulkheadFullError("Queue is full")
        else:
            return await self._execute_with_semaphore(coro)

    async def _execute_with_semaphore(self, coro):
        async with self.semaphore:
            self.active += 1
            try:
                return await coro
            finally:
                self.active -= 1

# Service-specific bulkheads
payment_bulkhead = Bulkhead(max_concurrent=20, max_queued=10)
search_bulkhead = Bulkhead(max_concurrent=30, max_queued=50)
heavy_report_bulkhead = Bulkhead(max_concurrent=5, max_queued=5)

# Usage
@app.post("/api/payment")
async def process_payment(payment_data: dict):
    try:
        result = await payment_bulkhead.execute(
            payment_service.process(payment_data)
        )
        return result

    except BulkheadFullError:
        raise HTTPException(
            status_code=503,
            detail="Payment service at capacity, please retry later"
        )
```

---

## Resumen Arquitectura Técnica Avanzada

| Tema | Dificultad | Impacto | Prioridad |
|------|------------|---------|-----------|
| Bounded Contexts & DDD | 5 | 5 | **CRÍTICA** |
| Aggregate Design | 5 | 5 | **CRÍTICA** |
| Multi-Tenancy Patterns | 5 | 5 | **CRÍTICA** |
| WebSocket Scaling | 5 | 4 | **ALTA** |
| API Versioning | 4 | 5 | **CRÍTICA** |
| Bulkhead Pattern | 4 | 4 | **ALTA** |

**Última actualización:** 2025-12-26
**Versión:** 1.0
**Enfoque:** Decisiones técnicas profundas con código de producción
