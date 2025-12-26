# Arquitectura Técnica Avanzada 2026 - Parte 2: Patrones Críticos

## Objetivo
Decisiones técnicas avanzadas de arquitectura: consistencia de datos, comunicación entre servicios, y patrones de observabilidad para sistemas distribuidos modernos.

---

## CATEGORÍA 1: Data Consistency en Sistemas Distribuidos

### 1.1 CAP Theorem y Trade-offs Prácticos
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
En sistemas distribuidos, es imposible garantizar simultáneamente Consistency, Availability y Partition Tolerance. Debes elegir.

**Estrategias por Caso de Uso:**

```
┌─────────────────────────────────────────┐
│         CAP THEOREM DECISIONES          │
├─────────────────────────────────────────┤
│                                         │
│  CP (Consistency + Partition Tolerance) │
│  ✅ Banking, Payments, Inventory        │
│  ❌ Social Media, Analytics             │
│                                         │
│  AP (Availability + Partition Tolerance)│
│  ✅ Social Media, Caching, Analytics    │
│  ❌ Financial Transactions              │
│                                         │
└─────────────────────────────────────────┘
```

**Implementación: Strong Consistency con Distributed Locks**

```python
# CP System: Strong Consistency con Redis Distributed Lock
from redis import Redis
from redis.lock import Lock
from contextlib import asynccontextmanager
from datetime import timedelta
import uuid

class DistributedLockManager:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.lock_timeout = timedelta(seconds=10)

    @asynccontextmanager
    async def acquire_lock(self, resource_id: str, timeout: int = 10):
        """
        Distributed lock para garantizar consistency

        Usado en:
        - Inventory decrements (evitar overselling)
        - Payment processing (evitar double-charge)
        - Account balance updates
        """
        lock_key = f"lock:{resource_id}"
        lock_value = str(uuid.uuid4())
        lock = Lock(
            self.redis,
            lock_key,
            timeout=timeout,
            blocking_timeout=5
        )

        acquired = False
        try:
            acquired = lock.acquire(blocking=True)
            if not acquired:
                raise TimeoutError(f"Could not acquire lock for {resource_id}")

            yield lock_value

        finally:
            if acquired:
                lock.release()


# Ejemplo: Inventory Management con Strong Consistency
from fastapi import FastAPI, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
lock_manager = DistributedLockManager(redis_client)

@app.post("/orders")
async def create_order(
    product_id: int,
    quantity: int,
    session: AsyncSession
):
    """
    CP System: Prioriza Consistency sobre Availability

    Si Redis (lock) está caído → rechaza requests (sacrifice availability)
    Garantía: NUNCA overselling
    """

    # 1. Acquire distributed lock
    async with lock_manager.acquire_lock(f"product:{product_id}"):

        # 2. Read current inventory (with SELECT FOR UPDATE - pessimistic lock)
        stmt = (
            select(Product.stock)
            .where(Product.id == product_id)
            .with_for_update()  # Pessimistic lock en DB
        )
        result = await session.execute(stmt)
        current_stock = result.scalar_one_or_none()

        if current_stock is None:
            raise HTTPException(404, "Product not found")

        # 3. Validate availability
        if current_stock < quantity:
            raise HTTPException(
                409,
                f"Insufficient stock: {current_stock} available"
            )

        # 4. Decrement stock (atomic operation)
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(stock=Product.stock - quantity)
        )
        await session.execute(stmt)
        await session.commit()

        return {"status": "success", "remaining_stock": current_stock - quantity}


# Trade-off Analysis:
"""
✅ PROS (CP):
- Zero overselling (consistency guaranteed)
- Auditable (strong consistency = trust)
- Predictable behavior

❌ CONTRAS (CP):
- Lower availability (si Redis cae, sistema cae)
- Higher latency (locks + waits)
- Potential bottleneck en high throughput

💡 DECISIÓN:
Usar CP para inventory, payments, financial data
Usar AP para likes, views, analytics
"""
```

**Implementación: Eventual Consistency con Compensating Transactions**

```python
# AP System: Eventual Consistency
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import asyncio

class ReservationStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

@dataclass
class InventoryReservation:
    """
    Soft Reservation Pattern

    AP System: Prioriza Availability sobre Consistency inmediata
    """
    reservation_id: str
    product_id: int
    quantity: int
    status: ReservationStatus
    expires_at: datetime
    user_id: str

class EventualConsistencyInventory:
    """
    AP System con Eventual Consistency

    Trade-off:
    - Alta availability (acepta requests incluso con particiones)
    - Eventual consistency (puede haber temporary overselling)
    - Compensating transactions (rollback si necesario)
    """

    def __init__(self, db: AsyncSession, cache: Redis):
        self.db = db
        self.cache = cache
        self.reservation_ttl = 600  # 10 minutes

    async def reserve_inventory(
        self,
        product_id: int,
        quantity: int,
        user_id: str
    ) -> InventoryReservation:
        """
        Crea una reserva optimista (sin lock distribuido)

        ✅ Alta availability: acepta request incluso si partición existe
        ⚠️ Posible overselling temporal
        """
        reservation_id = str(uuid.uuid4())

        # 1. Optimistic check (sin lock)
        cache_key = f"stock:{product_id}"
        cached_stock = await self.cache.get(cache_key)

        if cached_stock and int(cached_stock) < quantity:
            # Soft rejection (pero no bloquea si cache está stale)
            raise HTTPException(409, "Likely insufficient stock")

        # 2. Create reservation (optimistic)
        reservation = InventoryReservation(
            reservation_id=reservation_id,
            product_id=product_id,
            quantity=quantity,
            status=ReservationStatus.PENDING,
            expires_at=datetime.utcnow() + timedelta(seconds=self.reservation_ttl),
            user_id=user_id
        )

        # 3. Persist reservation (sin validar stock exacto todavía)
        await self._save_reservation(reservation)

        # 4. Async validation (background task)
        asyncio.create_task(self._validate_reservation(reservation_id))

        return reservation

    async def _validate_reservation(self, reservation_id: str):
        """
        Background task: valida reserva contra stock real

        Si stock insuficiente → COMPENSATING TRANSACTION
        """
        await asyncio.sleep(2)  # Simula delay

        reservation = await self._get_reservation(reservation_id)

        # Check real stock (eventual)
        stmt = select(Product.stock).where(Product.id == reservation.product_id)
        result = await self.db.execute(stmt)
        real_stock = result.scalar_one()

        # Get total pending reservations
        pending_reservations = await self._get_pending_quantity(reservation.product_id)

        if real_stock < pending_reservations:
            # ⚠️ OVERSELLING DETECTED - COMPENSATE
            await self._cancel_reservation(
                reservation_id,
                reason="Insufficient stock after validation"
            )

            # Notify user (event)
            await self._emit_event(ReservationCancelledEvent(
                reservation_id=reservation_id,
                user_id=reservation.user_id,
                reason="overselling_prevention"
            ))
        else:
            # ✅ Reservation confirmed
            await self._confirm_reservation(reservation_id)

    async def _cancel_reservation(self, reservation_id: str, reason: str):
        """Compensating transaction"""
        stmt = (
            update(InventoryReservation)
            .where(InventoryReservation.id == reservation_id)
            .values(status=ReservationStatus.CANCELLED, cancellation_reason=reason)
        )
        await self.db.execute(stmt)
        await self.db.commit()


# Trade-off Analysis:
"""
✅ PROS (AP):
- Alta availability (funciona incluso con particiones)
- Baja latencia (sin locks)
- Escalable (sin coordination overhead)

❌ CONTRAS (AP):
- Temporary inconsistencies (overselling temporal)
- Compensating transactions necesarias
- User experience complexity (reservation puede cancelarse)

💡 DECISIÓN:
Usar AP para e-commerce cart (temporal reservation OK)
Usar AP para social features (likes, follows)
NO usar AP para payments, critical inventory
"""
```

### 1.2 Sagas Avanzadas: Orchestration vs Choreography
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Sagas coordinan transacciones distribuidas. Dos patrones: Orchestration (centralizado) vs Choreography (eventos).

**Patrón 1: Orchestration Saga (Recomendado para flujos complejos)**

```python
# ORCHESTRATION SAGA
from enum import Enum
from typing import List, Dict, Any, Optional
import asyncio

class SagaStep(Enum):
    ORDER_CREATED = "order_created"
    PAYMENT_PROCESSED = "payment_processed"
    INVENTORY_RESERVED = "inventory_reserved"
    SHIPPING_SCHEDULED = "shipping_scheduled"
    ORDER_COMPLETED = "order_completed"

class SagaStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

@dataclass
class SagaDefinition:
    """Define pasos del saga y sus compensaciones"""
    steps: List[Dict[str, Any]]

class OrderSagaOrchestrator:
    """
    Orchestration Pattern: Coordinador central

    ✅ VENTAJAS:
    - Flujo visible (single source of truth)
    - Fácil debugging (todo en un lugar)
    - Control de timeouts y retries

    ❌ DESVENTAJAS:
    - Single point of failure
    - Acoplamiento al orchestrator
    - Puede ser bottleneck

    💡 USAR CUANDO:
    - Flujo complejo con muchos pasos
    - Necesitas visibilidad centralizada
    - Requieres control estricto de orden
    """

    def __init__(self, db: AsyncSession, event_bus: EventBus):
        self.db = db
        self.event_bus = event_bus
        self.saga_definition = self._define_order_saga()

    def _define_order_saga(self) -> SagaDefinition:
        """Define el flujo del saga"""
        return SagaDefinition(steps=[
            {
                "name": "create_order",
                "action": self._create_order,
                "compensation": self._cancel_order,
                "timeout": 5
            },
            {
                "name": "process_payment",
                "action": self._process_payment,
                "compensation": self._refund_payment,
                "timeout": 30
            },
            {
                "name": "reserve_inventory",
                "action": self._reserve_inventory,
                "compensation": self._release_inventory,
                "timeout": 10
            },
            {
                "name": "schedule_shipping",
                "action": self._schedule_shipping,
                "compensation": self._cancel_shipping,
                "timeout": 15
            }
        ])

    async def execute_saga(self, order_data: Dict[str, Any]) -> str:
        """
        Ejecuta saga con automatic compensation si falla
        """
        saga_id = str(uuid.uuid4())
        completed_steps = []

        try:
            # Persist saga state
            saga_state = await self._create_saga_state(saga_id, order_data)

            # Execute steps sequentially
            for step in self.saga_definition.steps:
                await self._update_saga_step(saga_id, step["name"], "executing")

                try:
                    # Execute with timeout
                    result = await asyncio.wait_for(
                        step["action"](order_data),
                        timeout=step["timeout"]
                    )

                    completed_steps.append({
                        "step": step,
                        "result": result
                    })

                    await self._update_saga_step(saga_id, step["name"], "completed")

                except asyncio.TimeoutError:
                    raise SagaStepTimeout(f"Step {step['name']} timed out")
                except Exception as e:
                    raise SagaStepFailed(f"Step {step['name']} failed: {e}")

            # Success!
            await self._mark_saga_completed(saga_id)
            return saga_id

        except Exception as e:
            # COMPENSATE: rollback completed steps in reverse order
            await self._compensate_saga(saga_id, completed_steps)
            raise

    async def _compensate_saga(
        self,
        saga_id: str,
        completed_steps: List[Dict]
    ):
        """
        Ejecuta compensating transactions en orden inverso

        Ejemplo: Si falla shipping
        1. Cancel shipping (no-op, nunca se creó)
        2. Release inventory ✅
        3. Refund payment ✅
        4. Cancel order ✅
        """
        await self._update_saga_status(saga_id, SagaStatus.COMPENSATING)

        # Reverse order!
        for step_data in reversed(completed_steps):
            step = step_data["step"]

            try:
                await step["compensation"](step_data["result"])
            except Exception as e:
                # Log compensation failure (critical!)
                await self._log_compensation_failure(saga_id, step["name"], e)
                # Continue compensating (best effort)

        await self._update_saga_status(saga_id, SagaStatus.FAILED)

    # Action methods
    async def _create_order(self, data: Dict) -> Dict:
        """Step 1: Create order"""
        order = Order(
            user_id=data["user_id"],
            total=data["total"],
            status="pending"
        )
        self.db.add(order)
        await self.db.commit()
        return {"order_id": order.id}

    async def _process_payment(self, data: Dict) -> Dict:
        """Step 2: Process payment (may fail)"""
        payment_result = await payment_gateway.charge(
            amount=data["total"],
            customer_id=data["user_id"]
        )
        if not payment_result.success:
            raise PaymentFailed(payment_result.error)
        return {"payment_id": payment_result.payment_id}

    async def _reserve_inventory(self, data: Dict) -> Dict:
        """Step 3: Reserve inventory"""
        for item in data["items"]:
            await inventory_service.reserve(
                product_id=item["product_id"],
                quantity=item["quantity"]
            )
        return {"reserved": True}

    async def _schedule_shipping(self, data: Dict) -> Dict:
        """Step 4: Schedule shipping (puede fallar si no hay carrier)"""
        shipping = await shipping_service.schedule(
            order_id=data["order_id"],
            address=data["shipping_address"]
        )
        return {"shipping_id": shipping.id}

    # Compensation methods
    async def _cancel_order(self, result: Dict):
        """Compensate: Cancel order"""
        await self.db.execute(
            update(Order)
            .where(Order.id == result["order_id"])
            .values(status="cancelled")
        )
        await self.db.commit()

    async def _refund_payment(self, result: Dict):
        """Compensate: Refund payment"""
        await payment_gateway.refund(result["payment_id"])

    async def _release_inventory(self, result: Dict):
        """Compensate: Release inventory"""
        # Release all reserved items
        pass

    async def _cancel_shipping(self, result: Dict):
        """Compensate: Cancel shipping"""
        await shipping_service.cancel(result["shipping_id"])


# Monitoring del Saga
@app.get("/sagas/{saga_id}")
async def get_saga_status(saga_id: str):
    """
    Visibilidad centralizada del saga

    Response:
    {
      "saga_id": "123",
      "status": "compensating",
      "steps": [
        {"name": "create_order", "status": "completed"},
        {"name": "process_payment", "status": "completed"},
        {"name": "reserve_inventory", "status": "failed"},
        {"name": "schedule_shipping", "status": "pending"}
      ],
      "compensations": [
        {"name": "refund_payment", "status": "completed"},
        {"name": "cancel_order", "status": "completed"}
      ]
    }
    """
    return await saga_orchestrator.get_status(saga_id)
```

**Patrón 2: Choreography Saga (Event-Driven)**

```python
# CHOREOGRAPHY SAGA
from dataclasses import dataclass

@dataclass
class OrderCreatedEvent:
    order_id: str
    user_id: str
    total: float
    items: List[Dict]

@dataclass
class PaymentProcessedEvent:
    order_id: str
    payment_id: str

@dataclass
class PaymentFailedEvent:
    order_id: str
    reason: str

class OrderService:
    """
    Service 1: Orders

    Responsabilidad: Crear orden, escuchar eventos de pago
    """

    async def create_order(self, data: Dict) -> str:
        # 1. Create order
        order = await self._persist_order(data)

        # 2. Emit event (sin esperar respuesta)
        await event_bus.publish(OrderCreatedEvent(
            order_id=order.id,
            user_id=data["user_id"],
            total=data["total"],
            items=data["items"]
        ))

        return order.id

    @event_handler(PaymentProcessedEvent)
    async def on_payment_processed(self, event: PaymentProcessedEvent):
        """React to payment success"""
        await self.db.execute(
            update(Order)
            .where(Order.id == event.order_id)
            .values(status="payment_confirmed")
        )
        await self.db.commit()

    @event_handler(PaymentFailedEvent)
    async def on_payment_failed(self, event: PaymentFailedEvent):
        """Compensate: Cancel order si payment falla"""
        await self.db.execute(
            update(Order)
            .where(Order.id == event.order_id)
            .values(status="cancelled", cancellation_reason=event.reason)
        )
        await self.db.commit()


class PaymentService:
    """
    Service 2: Payments

    Responsabilidad: Procesar pago, emitir evento de resultado
    """

    @event_handler(OrderCreatedEvent)
    async def on_order_created(self, event: OrderCreatedEvent):
        """React to order creation"""
        try:
            # Attempt payment
            payment = await payment_gateway.charge(
                amount=event.total,
                customer_id=event.user_id
            )

            # Emit success event
            await event_bus.publish(PaymentProcessedEvent(
                order_id=event.order_id,
                payment_id=payment.id
            ))

        except Exception as e:
            # Emit failure event
            await event_bus.publish(PaymentFailedEvent(
                order_id=event.order_id,
                reason=str(e)
            ))


class InventoryService:
    """
    Service 3: Inventory

    Responsabilidad: Reservar inventory cuando payment OK
    """

    @event_handler(PaymentProcessedEvent)
    async def on_payment_processed(self, event: PaymentProcessedEvent):
        """Reserve inventory after payment"""
        order = await self._get_order(event.order_id)

        try:
            for item in order.items:
                await self._reserve_item(item.product_id, item.quantity)

            # Emit success
            await event_bus.publish(InventoryReservedEvent(
                order_id=event.order_id
            ))

        except InsufficientStockError:
            # Trigger compensation chain
            await event_bus.publish(InventoryReservationFailedEvent(
                order_id=event.order_id,
                reason="insufficient_stock"
            ))


# Compensations are also event-driven
class PaymentService:
    @event_handler(InventoryReservationFailedEvent)
    async def on_inventory_failed(self, event):
        """Compensate: Refund payment if inventory fails"""
        payment = await self._get_payment_for_order(event.order_id)
        await payment_gateway.refund(payment.id)

        await event_bus.publish(PaymentRefundedEvent(
            order_id=event.order_id,
            payment_id=payment.id
        ))


# Trade-offs: Orchestration vs Choreography
"""
┌─────────────────────────────────────────────────────┐
│         ORCHESTRATION vs CHOREOGRAPHY               │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ORCHESTRATION:                                      │
│ ✅ Visibilidad centralizada                        │
│ ✅ Fácil debugging (todo en un lugar)              │
│ ✅ Control explícito de orden                      │
│ ❌ Single point of failure                          │
│ ❌ Acoplamiento al orchestrator                     │
│                                                     │
│ CHOREOGRAPHY:                                       │
│ ✅ Loosely coupled                                  │
│ ✅ Alta disponibilidad (no SPOF)                   │
│ ✅ Escalabilidad horizontal                        │
│ ❌ Difícil debugging (flujo distribuido)           │
│ ❌ No hay vista global del proceso                 │
│ ❌ Posibles ciclos infinitos si no se diseña bien  │
│                                                     │
└─────────────────────────────────────────────────────┘

💡 DECISIÓN:
- Orchestration: Flujos complejos, require visibilidad (e-commerce checkout)
- Choreography: Bounded contexts independientes (microservices bien definidos)
- Híbrido: Orchestration dentro de bounded context, Choreography entre contexts
"""
```

---

## CATEGORÍA 2: Service Mesh y Comunicación Avanzada

### 2.1 Service Mesh: Istio Patterns
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Service Mesh mueve networking logic fuera del código de aplicación. Traffic management, security, observability.

**Implementación: Traffic Splitting para Canary Deployments**

```yaml
# Istio VirtualService: Canary Deployment con Progressive Rollout
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: product-service
spec:
  hosts:
  - product-service
  http:
  - match:
    - headers:
        user-type:
          exact: "internal"  # Internal users get canary
    route:
    - destination:
        host: product-service
        subset: v2-canary
      weight: 100

  - route:  # Default route for external users
    - destination:
        host: product-service
        subset: v1-stable
      weight: 90  # 90% traffic to stable
    - destination:
        host: product-service
        subset: v2-canary
      weight: 10  # 10% traffic to canary

---
# DestinationRule: Define subsets
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: product-service
spec:
  host: product-service
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: "x-user-id"  # Sticky sessions
  subsets:
  - name: v1-stable
    labels:
      version: v1
  - name: v2-canary
    labels:
      version: v2
    trafficPolicy:
      connectionPool:
        tcp:
          maxConnections: 100
        http:
          http1MaxPendingRequests: 50
          maxRequestsPerConnection: 2
```

**Circuit Breaker con Istio (declarativo)**

```yaml
# Circuit Breaker: Automatic failover
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: inventory-service
spec:
  host: inventory-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
        maxRequestsPerConnection: 2

    outlierDetection:  # Circuit Breaker configuration
      consecutiveErrors: 5  # Open circuit after 5 errors
      interval: 30s
      baseEjectionTime: 30s  # Remove unhealthy instance for 30s
      maxEjectionPercent: 50  # Max 50% of instances can be ejected
      minHealthPercent: 40  # Require 40% healthy instances
```

**Python Application Code (sin lógica de networking)**

```python
# Application code: SIN circuit breaker logic (Istio lo maneja)
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """
    Application code limpio: sin retry, timeout, circuit breaker logic

    Istio sidecar proxy maneja:
    - Retries automáticos
    - Timeouts
    - Circuit breaking
    - Load balancing
    - mTLS encryption
    - Telemetry (traces, metrics)
    """

    # Simple HTTP call - Istio maneja resiliencia
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://inventory-service/stock/{product_id}"
        )
        return response.json()


# Sin Istio, necesitarías:
"""
@app.get("/products/{product_id}")
async def get_product_without_istio(product_id: int):
    # Manual circuit breaker
    if circuit_breaker.is_open("inventory-service"):
        raise HTTPException(503, "Service unavailable")

    # Manual timeout
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(...)
    except httpx.TimeoutException:
        circuit_breaker.record_failure("inventory-service")
        raise

    # Manual retry logic
    # Manual load balancing
    # Manual mTLS
    # Manual telemetry

    # = MUCHO CÓDIGO REPETIDO
"""
```

**Trade-offs: Service Mesh vs Library**

```python
"""
┌─────────────────────────────────────────────────────┐
│       SERVICE MESH vs CLIENT LIBRARIES              │
├─────────────────────────────────────────────────────┤
│                                                     │
│ SERVICE MESH (Istio, Linkerd):                     │
│ ✅ Polyglot (funciona con cualquier lenguaje)      │
│ ✅ Consistent behavior (todas apps iguales)        │
│ ✅ Operations-driven (no code changes)             │
│ ✅ Zero trust security (mTLS automático)           │
│ ❌ Operational complexity (K8s required)            │
│ ❌ Resource overhead (sidecar per pod)             │
│ ❌ Debugging complexity (network layer)            │
│                                                     │
│ CLIENT LIBRARIES (Resilience4j, Polly):            │
│ ✅ Simpler deployment (no infra changes)           │
│ ✅ Lower resource usage (no sidecars)              │
│ ✅ Easier debugging (in-process)                   │
│ ❌ Language-specific (reimplementar por lenguaje)   │
│ ❌ Application changes required                     │
│ ❌ Inconsistent behavior (cada dev implementa)     │
│                                                     │
└─────────────────────────────────────────────────────┘

💡 DECISIÓN 2026:
- Service Mesh: Si ya tienes K8s + microservices + polyglot
- Client Libraries: Si monolith/few services o no-K8s
- Híbrido: Service Mesh para infra, libraries para business logic
"""
```

---

## CATEGORÍA 3: GraphQL Federation y Schema Design

### 3.1 GraphQL Federation: Microservices Architecture
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
GraphQL Federation permite que múltiples servicios contribuyan a un schema unificado. Clave para microservices con GraphQL.

**Implementación: Apollo Federation con Subgraphs**

```python
# Subgraph 1: Users Service
from strawberry.federation import type as federation_type
import strawberry

@federation_type(keys=["id"])
class User:
    id: strawberry.ID
    username: str
    email: str

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        """Resolve User entity from other services"""
        return get_user_from_db(id)

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        return get_user_from_db(id)


# Subgraph 2: Orders Service
@federation_type(keys=["id"])
class Order:
    id: strawberry.ID
    total: float
    created_at: datetime

    @strawberry.field
    def user(self) -> User:
        """
        Extend User type from Users service

        Federation: Orders service can reference User
        without duplicating User data/logic
        """
        return User(id=self.user_id)  # Reference only

@strawberry.field
def extend_user() -> User:
    """Extend User type with orders"""
    pass

@strawberry.type
class UserExtension:
    """
    Extend User type from another service

    Client can query:
    {
      user(id: "123") {
        username        # From Users service
        email           # From Users service
        orders {        # From Orders service
          total
          created_at
        }
      }
    }
    """

    @strawberry.field
    def orders(self, root: User) -> List[Order]:
        # Orders service extends User type
        return get_orders_for_user(root.id)


# Gateway: Apollo Router
"""
# Configuration: router.yaml
supergraph:
  listen: 0.0.0.0:4000

subgraphs:
  users:
    routing_url: http://users-service:8000/graphql
    schema:
      file: ./users-schema.graphql

  orders:
    routing_url: http://orders-service:8000/graphql
    schema:
      file: ./orders-schema.graphql

  products:
    routing_url: http://products-service:8000/graphql
    schema:
      file: ./products-schema.graphql

# Unified schema automáticamente compuesto
"""
```

**N+1 Problem en GraphQL Federation**

```python
# ❌ BAD: N+1 Problem en Federation
@strawberry.type
class OrderExtension:
    @strawberry.field
    def user(self, root: Order) -> User:
        """
        Problem: If client requests 100 orders with user data
        = 1 query for orders + 100 queries for users (N+1)
        """
        return get_user(root.user_id)  # ❌ Individual query per order


# ✅ GOOD: DataLoader para batch loading
from strawberry.dataloader import DataLoader

class UserLoader(DataLoader):
    async def load(self, keys: List[int]) -> List[User]:
        """
        Batch load users

        Instead of 100 individual queries:
        SELECT * FROM users WHERE id = 1
        SELECT * FROM users WHERE id = 2
        ...

        One batched query:
        SELECT * FROM users WHERE id IN (1, 2, 3, ..., 100)
        """
        users = await db.execute(
            select(User).where(User.id.in_(keys))
        )

        # Return in same order as keys (important!)
        user_map = {user.id: user for user in users}
        return [user_map.get(key) for key in keys]

@strawberry.type
class OrderExtension:
    @strawberry.field
    async def user(
        self,
        root: Order,
        info: strawberry.Info
    ) -> User:
        """
        Use DataLoader from context

        Automatic batching:
        - Collects all user_id requests in single event loop tick
        - Executes ONE batch query
        - Returns individual results
        """
        loader: UserLoader = info.context["user_loader"]
        return await loader.load(root.user_id)


# FastAPI Integration
@app.post("/graphql")
async def graphql_endpoint(request: Request):
    """Provide DataLoader instance per request"""
    context = {
        "user_loader": UserLoader(),
        "product_loader": ProductLoader(),
        "request": request
    }

    return await graphql_app.execute(
        request,
        context_value=context
    )
```

**Federation Trade-offs**

```python
"""
┌─────────────────────────────────────────────────────┐
│     GRAPHQL FEDERATION vs MONOLITHIC GRAPHQL        │
├─────────────────────────────────────────────────────┤
│                                                     │
│ FEDERATION:                                         │
│ ✅ Team autonomy (cada team su subgraph)           │
│ ✅ Independent deployments                          │
│ ✅ Scalability (scale services independently)       │
│ ✅ Domain separation                                │
│ ❌ Operational complexity (gateway + multiple svcs) │
│ ❌ N+1 problems across services                     │
│ ❌ Query planning overhead                          │
│                                                     │
│ MONOLITHIC:                                         │
│ ✅ Simpler deployment (one service)                 │
│ ✅ Easier query optimization                        │
│ ✅ Single codebase                                  │
│ ❌ Scaling limitations                               │
│ ❌ Team conflicts (single schema)                   │
│ ❌ All-or-nothing deploys                           │
│                                                     │
└─────────────────────────────────────────────────────┘

💡 DECISIÓN 2026:
- Federation: Microservices con teams independientes
- Monolithic: Startups, equipos pequeños, rapid iteration
- Backend for Frontend (BFF): Combine both (federation internal, monolithic per client)
"""
```

---

## CATEGORÍA 4: Advanced Caching Strategies

### 4.1 Multi-Layer Caching con Consistency
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Caching en múltiples layers (L1: in-memory, L2: Redis, L3: CDN). Challenge: consistency.

**Implementación: Write-Through + Cache Invalidation**

```python
# Multi-Layer Cache Implementation
from functools import wraps
from typing import Optional, Any
import pickle
import hashlib

class MultiLayerCache:
    """
    L1: In-Memory (LRU, 1000 items, ~10MB)
    L2: Redis (TTL 1h, ~1GB)
    L3: CDN (TTL 24h, edge caching)

    Read path: L1 → L2 → L3 → DB
    Write path: DB → Invalidate L1, L2, L3
    """

    def __init__(self, redis: Redis, local_cache_size: int = 1000):
        self.redis = redis
        self.local_cache = LRUCache(maxsize=local_cache_size)
        self.cdn_client = CDNClient()

    async def get(self, key: str) -> Optional[Any]:
        """Multi-layer read"""

        # L1: Local memory (fastest, ~1µs)
        if key in self.local_cache:
            return self.local_cache[key]

        # L2: Redis (fast, ~1ms)
        redis_value = await self.redis.get(key)
        if redis_value:
            value = pickle.loads(redis_value)
            self.local_cache[key] = value  # Populate L1
            return value

        # L3: CDN (slower, ~50ms but offloads DB)
        cdn_value = await self.cdn_client.get(key)
        if cdn_value:
            # Populate L2 and L1
            await self.redis.setex(key, 3600, pickle.dumps(cdn_value))
            self.local_cache[key] = cdn_value
            return cdn_value

        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl_l2: int = 3600,
        ttl_l3: int = 86400
    ):
        """Multi-layer write"""

        # L1: Local memory
        self.local_cache[key] = value

        # L2: Redis
        await self.redis.setex(key, ttl_l2, pickle.dumps(value))

        # L3: CDN (async, no wait)
        asyncio.create_task(
            self.cdn_client.set(key, value, ttl=ttl_l3)
        )

    async def invalidate(self, key: str):
        """
        Invalidate all layers

        Critical para consistency después de updates
        """
        # L1: Local memory
        if key in self.local_cache:
            del self.local_cache[key]

        # L2: Redis
        await self.redis.delete(key)

        # L3: CDN purge
        await self.cdn_client.purge(key)

    async def invalidate_pattern(self, pattern: str):
        """
        Invalidate by pattern (e.g., "user:123:*")

        Use case: User updates, invalidate all related caches
        """
        # L1: Clear all (LRU, can't pattern match efficiently)
        self.local_cache.clear()

        # L2: Redis SCAN + DELETE
        cursor = 0
        while True:
            cursor, keys = await self.redis.scan(
                cursor,
                match=pattern,
                count=100
            )
            if keys:
                await self.redis.delete(*keys)
            if cursor == 0:
                break

        # L3: CDN purge by tag
        await self.cdn_client.purge_by_tag(pattern)


# Usage Example: Product Service
class ProductService:
    def __init__(self, db: AsyncSession, cache: MultiLayerCache):
        self.db = db
        self.cache = cache

    async def get_product(self, product_id: int) -> Product:
        """Read with multi-layer cache"""

        cache_key = f"product:{product_id}"

        # Try cache first
        cached = await self.cache.get(cache_key)
        if cached:
            return Product(**cached)

        # Cache miss: read from DB
        stmt = select(Product).where(Product.id == product_id)
        result = await self.db.execute(stmt)
        product = result.scalar_one_or_none()

        if product:
            # Populate cache
            await self.cache.set(
                cache_key,
                product.dict(),
                ttl_l2=3600,   # 1 hour in Redis
                ttl_l3=86400   # 24 hours in CDN
            )

        return product

    async def update_product(self, product_id: int, data: Dict):
        """
        Write-Through pattern: Update DB + Invalidate cache

        NO caches updated here (avoid stale data race conditions)
        Next read will repopulate cache
        """

        # 1. Update database
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(**data)
        )
        await self.db.execute(stmt)
        await self.db.commit()

        # 2. Invalidate cache (all layers)
        await self.cache.invalidate(f"product:{product_id}")

        # 3. Invalidate related caches
        await self.cache.invalidate_pattern(f"category:{data.get('category_id')}:*")
        await self.cache.invalidate_pattern("products:list:*")


# Cache Warming (prevent thundering herd)
async def warm_cache_on_deployment():
    """
    Pre-populate cache after deployment

    Prevents: Thundering herd (all requests hit DB simultaneously)
    """
    product_service = ProductService(db, cache)

    # Top 100 products
    top_products = await get_top_100_products()

    for product_id in top_products:
        await product_service.get_product(product_id)
        await asyncio.sleep(0.1)  # Rate limit warming
```

**Cache Stampede Prevention**

```python
# Cache Stampede Problem:
"""
Cache expires → 1000 concurrent requests → all hit DB simultaneously

Timeline:
T0: Cache expires
T1: Request 1 arrives, cache miss, queries DB
T2: Request 2 arrives, cache miss, queries DB (!)
T3: Request 3 arrives, cache miss, queries DB (!)
...
T100: Request 1000 arrives, cache miss, queries DB (!)

= 1000 DB queries for same data = STAMPEDE
"""

# ✅ SOLUTION: Probabilistic Early Expiration + Distributed Lock
import random

class SmartCache:
    async def get_with_stampede_protection(
        self,
        key: str,
        fetch_fn: Callable,
        ttl: int = 3600
    ) -> Any:
        """
        Probabilistic early expiration

        Instead of hard TTL, refresh probabilistically before expiration
        """

        cache_data = await self.redis.get(key)

        if cache_data is None:
            # Hard miss: use distributed lock
            return await self._fetch_with_lock(key, fetch_fn, ttl)

        # Decode cached data
        data = pickle.loads(cache_data)
        remaining_ttl = await self.redis.ttl(key)

        # Probabilistic early refresh
        # Closer to expiration = higher probability of refresh
        refresh_probability = 1 - (remaining_ttl / ttl)

        if random.random() < refresh_probability:
            # Refresh in background (return stale data immediately)
            asyncio.create_task(
                self._refresh_cache(key, fetch_fn, ttl)
            )

        return data

    async def _fetch_with_lock(
        self,
        key: str,
        fetch_fn: Callable,
        ttl: int
    ) -> Any:
        """Use distributed lock to prevent stampede"""

        lock_key = f"lock:{key}"
        lock = await self.redis.set(
            lock_key,
            "1",
            ex=10,  # Lock TTL
            nx=True  # Only if not exists
        )

        if lock:
            # This request got the lock: fetch data
            try:
                data = await fetch_fn()
                await self.redis.setex(key, ttl, pickle.dumps(data))
                return data
            finally:
                await self.redis.delete(lock_key)
        else:
            # Another request is fetching: wait and retry
            await asyncio.sleep(0.1)
            return await self.get_with_stampede_protection(key, fetch_fn, ttl)
```

---

## CATEGORÍA 5: Advanced Observability Patterns

### 5.1 Distributed Tracing Patterns
**Dificultad:** ⭐⭐⭐⭐ **ALTA**

**Contexto:**
En microservices, un request atraviesa múltiples servicios. Tracing permite visualizar el flujo completo.

**Implementación: OpenTelemetry con Context Propagation**

```python
# OpenTelemetry Setup
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Configure tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to Jaeger/Tempo
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Auto-instrument frameworks
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()
SQLAlchemyInstrumentor().instrument(engine=engine)


# Manual Tracing for Business Logic
@app.post("/orders")
async def create_order(order_data: OrderCreate):
    """
    Trace completo:

    create_order (FastAPI span)
      ├─ validate_inventory (custom span)
      │   └─ SELECT FROM products (SQLAlchemy span)
      ├─ process_payment (custom span)
      │   └─ POST /charge (HTTP span)
      └─ send_notification (custom span)
          └─ POST /send-email (HTTP span)
    """

    with tracer.start_as_current_span("create_order") as span:
        # Add custom attributes
        span.set_attribute("order.user_id", order_data.user_id)
        span.set_attribute("order.total", order_data.total)

        # Step 1: Validate inventory
        with tracer.start_as_current_span("validate_inventory") as inv_span:
            inv_span.set_attribute("product_count", len(order_data.items))

            for item in order_data.items:
                available = await inventory_service.check_stock(item.product_id)
                if not available:
                    inv_span.set_status(Status(StatusCode.ERROR))
                    inv_span.set_attribute("error.type", "insufficient_stock")
                    raise HTTPException(409, "Insufficient stock")

        # Step 2: Process payment
        with tracer.start_as_current_span("process_payment") as pay_span:
            pay_span.set_attribute("payment.amount", order_data.total)

            try:
                payment = await payment_service.charge(order_data.total)
                pay_span.set_attribute("payment.id", payment.id)
            except PaymentError as e:
                pay_span.record_exception(e)
                pay_span.set_status(Status(StatusCode.ERROR))
                raise

        # Step 3: Send notification
        with tracer.start_as_current_span("send_notification"):
            await notification_service.send_order_confirmation(order_data.user_id)

        return {"order_id": order.id}


# Context Propagation across services
import httpx
from opentelemetry.propagate import inject

async def call_external_service(url: str, data: Dict):
    """
    Propagate trace context to downstream service

    Headers injected:
    - traceparent: 00-{trace_id}-{span_id}-{trace_flags}
    - tracestate: vendor-specific data
    """
    headers = {}
    inject(headers)  # Inject trace context into headers

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        return response.json()


# Downstream Service: Extract context
from opentelemetry.propagate import extract

@app.post("/charge")
async def charge_payment(request: Request, payment_data: PaymentData):
    """
    Extract trace context from headers

    This span becomes child of upstream create_order span
    """
    # Extract context from request headers
    context = extract(request.headers)

    with tracer.start_as_current_span("charge_payment", context=context) as span:
        span.set_attribute("payment.amount", payment_data.amount)

        # Your business logic
        result = await process_charge(payment_data)

        return result


# Sampling Strategy
from opentelemetry.sdk.trace.sampling import (
    ParentBasedTraceIdRatioBased,
    ALWAYS_ON,
    TraceIdRatioBased
)

# Sample 10% of traces (reduce cost)
sampler = ParentBasedTraceIdRatioBased(
    root=TraceIdRatioBased(0.1),  # 10% of root spans
    # But always sample if parent was sampled (consistency)
)

trace.set_tracer_provider(
    TracerProvider(sampler=sampler)
)


# Custom Sampling: Sample errors at 100%, success at 10%
class ErrorAwareSampler:
    def should_sample(self, context, trace_id, name, attributes=None):
        """
        Intelligent sampling:
        - 100% of errors
        - 100% of slow requests (>1s)
        - 10% of normal requests
        """
        if attributes:
            if attributes.get("http.status_code", 0) >= 400:
                return ALWAYS_ON
            if attributes.get("http.duration_ms", 0) > 1000:
                return ALWAYS_ON

        # Default: 10% sampling
        return TraceIdRatioBased(0.1)
```

### 5.2 Structured Logging con Correlation IDs
**Dificultad:** ⭐⭐⭐⭐ **ALTA**

```python
# Structured Logging Setup
import structlog
from contextvars import ContextVar

# Context variable for request-scoped data
request_id_var: ContextVar[str] = ContextVar("request_id", default=None)
user_id_var: ContextVar[str] = ContextVar("user_id", default=None)

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,  # Merge context vars
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()  # JSON output
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()


# Middleware: Add correlation ID
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    """
    Extract or generate correlation ID

    Headers checked:
    1. X-Request-ID (from upstream)
    2. X-Correlation-ID (from upstream)
    3. Generate new UUID
    """
    request_id = (
        request.headers.get("X-Request-ID") or
        request.headers.get("X-Correlation-ID") or
        str(uuid.uuid4())
    )

    # Store in context var (available to all logs in this request)
    request_id_var.set(request_id)

    # Bind to structlog context
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path
    )

    response = await call_next(request)

    # Add to response headers (for client tracking)
    response.headers["X-Request-ID"] = request_id

    return response


# Business Logic Logging
@app.post("/orders")
async def create_order(order_data: OrderCreate, user: User = Depends(get_current_user)):
    """
    All logs automatically include:
    - request_id (from middleware)
    - user_id (bound below)
    - timestamp
    - log_level
    """

    # Bind user context
    structlog.contextvars.bind_contextvars(user_id=user.id)

    logger.info(
        "order_creation_started",
        order_total=order_data.total,
        item_count=len(order_data.items)
    )

    try:
        # Validate inventory
        for item in order_data.items:
            stock = await inventory_service.check_stock(item.product_id)

            if stock < item.quantity:
                logger.warning(
                    "insufficient_stock",
                    product_id=item.product_id,
                    requested=item.quantity,
                    available=stock
                )
                raise HTTPException(409, "Insufficient stock")

        # Process payment
        logger.info("payment_processing", amount=order_data.total)
        payment = await payment_service.charge(order_data.total)

        logger.info(
            "payment_processed",
            payment_id=payment.id,
            amount=payment.amount
        )

        # Create order
        order = await create_order_in_db(order_data)

        logger.info(
            "order_created",
            order_id=order.id,
            duration_ms=get_request_duration()
        )

        return order

    except PaymentError as e:
        logger.error(
            "payment_failed",
            error=str(e),
            error_type=type(e).__name__,
            amount=order_data.total
        )
        raise
    except Exception as e:
        logger.exception(
            "order_creation_failed",
            error=str(e)
        )
        raise


# Log Output (JSON):
"""
{
  "event": "order_creation_started",
  "request_id": "abc-123-def",
  "user_id": "user_456",
  "order_total": 99.99,
  "item_count": 3,
  "timestamp": "2026-01-15T10:30:00Z",
  "level": "info"
}

{
  "event": "insufficient_stock",
  "request_id": "abc-123-def",
  "user_id": "user_456",
  "product_id": 789,
  "requested": 5,
  "available": 2,
  "timestamp": "2026-01-15T10:30:01Z",
  "level": "warning"
}

{
  "event": "payment_failed",
  "request_id": "abc-123-def",
  "user_id": "user_456",
  "error": "Card declined",
  "error_type": "PaymentDeclinedError",
  "amount": 99.99,
  "timestamp": "2026-01-15T10:30:02Z",
  "level": "error"
}
"""

# Query logs in production:
"""
# All logs for specific request:
grep '"request_id":"abc-123-def"' logs.json

# All payment failures:
grep '"event":"payment_failed"' logs.json | jq .

# All errors for user:
grep '"user_id":"user_456"' logs.json | grep '"level":"error"'
"""
```

---

## Decisiones Consolidadas 2026

```
┌──────────────────────────────────────────────────────────────┐
│         ARQUITECTURA TÉCNICA AVANZADA - CHECKLIST            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. DATA CONSISTENCY                                          │
│    ├─ [ ] Definir CP vs AP por bounded context              │
│    ├─ [ ] Implementar distributed locks para CP systems     │
│    ├─ [ ] Diseñar compensating transactions para AP         │
│    └─ [ ] Saga pattern: orchestration vs choreography       │
│                                                              │
│ 2. SERVICE MESH                                              │
│    ├─ [ ] Evaluar Service Mesh vs client libraries          │
│    ├─ [ ] Implementar canary deployments con traffic split  │
│    ├─ [ ] Circuit breakers declarativos                     │
│    └─ [ ] mTLS automático entre services                    │
│                                                              │
│ 3. GRAPHQL FEDERATION                                        │
│    ├─ [ ] Definir subgraph boundaries                       │
│    ├─ [ ] Resolver N+1 con DataLoaders                      │
│    ├─ [ ] Schema evolution strategy                         │
│    └─ [ ] Gateway monitoring y error handling               │
│                                                              │
│ 4. CACHING                                                   │
│    ├─ [ ] Multi-layer cache strategy (L1, L2, L3)           │
│    ├─ [ ] Cache invalidation patterns                       │
│    ├─ [ ] Stampede prevention                               │
│    └─ [ ] Cache warming on deployment                       │
│                                                              │
│ 5. OBSERVABILITY                                             │
│    ├─ [ ] Distributed tracing con OpenTelemetry             │
│    ├─ [ ] Correlation IDs en todos los requests             │
│    ├─ [ ] Structured logging (JSON)                         │
│    ├─ [ ] Intelligent sampling (errors 100%, success 10%)   │
│    └─ [ ] Dashboards por business metric                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Conclusión:**

Este archivo cubre decisiones técnicas avanzadas que complementan los archivos 11 y 20:
- **Consistencia de datos** en sistemas distribuidos (CAP theorem práctico)
- **Sagas** para transacciones distribuidas (orchestration vs choreography)
- **Service Mesh** para networking avanzado
- **GraphQL Federation** para microservices
- **Caching multi-layer** con consistency guarantees
- **Observability avanzada** con tracing y structured logging

Cada sección incluye ejemplos de código completos, trade-offs análisis, y recomendaciones basadas en contexto de uso.
