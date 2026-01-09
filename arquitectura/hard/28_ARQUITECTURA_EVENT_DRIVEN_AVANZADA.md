# Arquitectura Event-Driven Avanzada: Patrones de Producción 2026

## Índice
1. [Tipos de Eventos y Clasificación](#1-tipos-de-eventos)
2. [Event Store Avanzado](#2-event-store-avanzado)
3. [Event Versioning y Schema Evolution](#3-event-versioning)
4. [Event Replay y Time Travel](#4-event-replay)
5. [Sagas Event-Driven](#5-sagas-event-driven)
6. [Dead Letter Queues y Error Handling](#6-dlq-error-handling)
7. [Projections y Read Models](#7-projections)
8. [Event Collaboration Patterns](#8-event-collaboration)
9. [Testing Event-Driven Systems](#9-testing-eventos)
10. [Observabilidad en Event-Driven](#10-observabilidad)

---

## 1. Tipos de Eventos y Clasificación

### ❌ ERROR COMÚN: Mezclar todos los tipos de eventos
```python
# MAL - todos los eventos son iguales
class UserCreated(BaseModel):
    user_id: str
    email: str

class OrderPlaced(BaseModel):
    order_id: str
    user_id: str
```

### ✅ SOLUCIÓN: Clasificar eventos por tipo y propósito

```python
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import uuid

# ==========================================
# 1. DOMAIN EVENTS
# ==========================================
class DomainEvent(BaseModel):
    """
    Event emitido dentro de un bounded context
    - Private to bounded context
    - Rich domain language
    - Can change frequently
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    aggregate_id: str
    aggregate_type: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
    metadata: Dict[str, Any] = {}

    class Config:
        frozen = True  # Inmutables

class OrderPlacedDomainEvent(DomainEvent):
    """Domain event dentro del contexto Orders"""
    event_type: str = "OrderPlaced"
    aggregate_type: str = "Order"

    # Rich domain data
    order_id: str
    customer_id: str
    items: list[dict]
    total_amount: float
    payment_method: str
    shipping_address: dict

# ==========================================
# 2. INTEGRATION EVENTS
# ==========================================
class IntegrationEvent(BaseModel):
    """
    Event publicado entre bounded contexts
    - Public contract
    - Stable schema
    - Backward compatible
    - Versioned
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    source_context: str
    published_at: datetime = Field(default_factory=datetime.utcnow)
    schema_version: str
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        frozen = True

class OrderPlacedIntegrationEvent(IntegrationEvent):
    """
    Integration event - solo datos esenciales
    Schema estable para otros bounded contexts
    """
    event_type: str = "order.placed"
    source_context: str = "orders"
    schema_version: str = "1.0.0"

    # Minimal public contract
    order_id: str
    customer_id: str
    total_amount: float
    currency: str
    placed_at: datetime

# ==========================================
# 3. SYSTEM EVENTS
# ==========================================
class SystemEvent(BaseModel):
    """
    Event de infraestructura/sistema
    - Monitoring
    - Alerting
    - Auditing
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    severity: str  # INFO, WARNING, ERROR, CRITICAL
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str

class PaymentGatewayTimeoutSystemEvent(SystemEvent):
    event_type: str = "payment.gateway.timeout"
    severity: str = "ERROR"
    source: str = "payment-service"

    gateway_name: str
    timeout_seconds: float
    retry_count: int

# ==========================================
# 4. EVENT TRANSFORMER
# ==========================================
class EventTransformer:
    """
    Transforma Domain Events → Integration Events
    """
    @staticmethod
    def domain_to_integration(
        domain_event: OrderPlacedDomainEvent,
        correlation_id: Optional[str] = None
    ) -> OrderPlacedIntegrationEvent:
        """
        Transforma evento rico del dominio
        a evento público con contrato estable
        """
        return OrderPlacedIntegrationEvent(
            event_id=domain_event.event_id,
            correlation_id=correlation_id,
            causation_id=domain_event.event_id,
            order_id=domain_event.order_id,
            customer_id=domain_event.customer_id,
            total_amount=domain_event.total_amount,
            currency="USD",
            placed_at=domain_event.occurred_at
        )

# ==========================================
# 5. EVENT CLASSIFICATION
# ==========================================
class EventClassification(Enum):
    """
    Clasificación por propósito de negocio
    """
    # State changes
    STATE_CHANGED = "state_changed"  # OrderPlaced, UserRegistered

    # Commands that happened
    COMMAND_EXECUTED = "command_executed"  # PaymentProcessed

    # Business milestones
    MILESTONE_REACHED = "milestone_reached"  # OrderShipped, GoalAchieved

    # Compensating actions
    COMPENSATION = "compensation"  # OrderCancelled, PaymentRefunded

    # Notifications
    NOTIFICATION = "notification"  # EmailSent, SMSSent

class ClassifiedEvent(BaseModel):
    classification: EventClassification
    event: DomainEvent

    @property
    def is_compensating(self) -> bool:
        return self.classification == EventClassification.COMPENSATION
```

**📊 Cuándo usar cada tipo:**

| Tipo | Scope | Estabilidad | Uso |
|------|-------|-------------|-----|
| **Domain Event** | Bounded Context | Alta volatilidad | Event Sourcing, Domain Logic |
| **Integration Event** | Entre Contexts | Muy estable | Microservices Communication |
| **System Event** | Infraestructura | Variable | Monitoring, Alerting |

---

## 2. Event Store Avanzado

### ❌ ERROR COMÚN: Base de datos normal para eventos
```python
# MAL - tabla SQL normal
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSON
);
```

### ✅ SOLUCIÓN: Event Store optimizado con snapshots

```python
from typing import List, Optional
from dataclasses import dataclass
import asyncpg
import json

# ==========================================
# EVENT STORE AVANZADO
# ==========================================
@dataclass
class EventStreamMetadata:
    stream_id: str
    version: int
    snapshot_version: Optional[int] = None
    event_count: int = 0
    created_at: datetime = None
    updated_at: datetime = None

class EventStore:
    """
    Event Store con optimizaciones de producción:
    - Snapshots para performance
    - Optimistic concurrency control
    - Stream versioning
    - Indexes optimizados
    """

    def __init__(self, db_pool: asyncpg.Pool):
        self.db = db_pool

    async def initialize_schema(self):
        """
        Schema optimizado para event sourcing
        """
        await self.db.execute("""
            -- Tabla principal de eventos
            CREATE TABLE IF NOT EXISTS events (
                event_id UUID PRIMARY KEY,
                stream_id VARCHAR(255) NOT NULL,
                stream_version INTEGER NOT NULL,
                event_type VARCHAR(255) NOT NULL,
                event_data JSONB NOT NULL,
                metadata JSONB,
                occurred_at TIMESTAMP NOT NULL,

                -- Optimistic concurrency
                UNIQUE(stream_id, stream_version)
            );

            -- Índices críticos
            CREATE INDEX IF NOT EXISTS idx_stream_id
                ON events(stream_id, stream_version);
            CREATE INDEX IF NOT EXISTS idx_event_type
                ON events(event_type);
            CREATE INDEX IF NOT EXISTS idx_occurred_at
                ON events(occurred_at);

            -- GIN index para búsquedas en JSONB
            CREATE INDEX IF NOT EXISTS idx_event_data
                ON events USING GIN(event_data);

            -- Tabla de snapshots
            CREATE TABLE IF NOT EXISTS snapshots (
                stream_id VARCHAR(255) PRIMARY KEY,
                version INTEGER NOT NULL,
                state JSONB NOT NULL,
                created_at TIMESTAMP NOT NULL
            );

            -- Tabla de metadata de streams
            CREATE TABLE IF NOT EXISTS stream_metadata (
                stream_id VARCHAR(255) PRIMARY KEY,
                current_version INTEGER NOT NULL,
                snapshot_version INTEGER,
                event_count INTEGER DEFAULT 0,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            );
        """)

    async def append_events(
        self,
        stream_id: str,
        events: List[DomainEvent],
        expected_version: int
    ) -> int:
        """
        Append events con optimistic concurrency control

        Raises:
            ConcurrencyError: Si expected_version no coincide
        """
        async with self.db.acquire() as conn:
            async with conn.transaction():
                # 1. Verificar versión actual (optimistic lock)
                current = await conn.fetchval(
                    """
                    SELECT current_version
                    FROM stream_metadata
                    WHERE stream_id = $1
                    FOR UPDATE
                    """,
                    stream_id
                )

                if current is None:
                    current = 0
                elif current != expected_version:
                    raise ConcurrencyError(
                        f"Stream {stream_id} version mismatch. "
                        f"Expected {expected_version}, got {current}"
                    )

                # 2. Insertar eventos
                new_version = current
                for event in events:
                    new_version += 1
                    await conn.execute(
                        """
                        INSERT INTO events (
                            event_id, stream_id, stream_version,
                            event_type, event_data, metadata, occurred_at
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                        """,
                        event.event_id,
                        stream_id,
                        new_version,
                        event.event_type,
                        json.dumps(event.dict(exclude={'event_id', 'event_type'})),
                        json.dumps(event.metadata),
                        event.occurred_at
                    )

                # 3. Actualizar metadata
                if current == 0:
                    await conn.execute(
                        """
                        INSERT INTO stream_metadata
                        (stream_id, current_version, event_count, created_at, updated_at)
                        VALUES ($1, $2, $3, NOW(), NOW())
                        """,
                        stream_id, new_version, len(events)
                    )
                else:
                    await conn.execute(
                        """
                        UPDATE stream_metadata
                        SET current_version = $2,
                            event_count = event_count + $3,
                            updated_at = NOW()
                        WHERE stream_id = $1
                        """,
                        stream_id, new_version, len(events)
                    )

                return new_version

    async def get_events(
        self,
        stream_id: str,
        from_version: int = 0,
        to_version: Optional[int] = None
    ) -> List[DomainEvent]:
        """
        Obtiene eventos de un stream
        Usa snapshot si está disponible
        """
        # 1. Verificar si hay snapshot
        snapshot = await self._get_snapshot(stream_id)

        if snapshot and snapshot.version >= from_version:
            from_version = snapshot.version + 1

        # 2. Obtener eventos desde versión
        query = """
            SELECT event_id, event_type, event_data, metadata, occurred_at, stream_version
            FROM events
            WHERE stream_id = $1
              AND stream_version >= $2
        """
        params = [stream_id, from_version]

        if to_version:
            query += " AND stream_version <= $3"
            params.append(to_version)

        query += " ORDER BY stream_version ASC"

        rows = await self.db.fetch(query, *params)

        # 3. Reconstruir eventos
        events = []
        for row in rows:
            event_data = json.loads(row['event_data'])
            event_data['event_id'] = str(row['event_id'])
            event_data['event_type'] = row['event_type']

            # Reconstruir evento (usar registry de tipos)
            event = DomainEvent(**event_data)
            events.append(event)

        return events

    async def save_snapshot(
        self,
        stream_id: str,
        version: int,
        state: dict
    ):
        """
        Guarda snapshot del estado del aggregate
        """
        await self.db.execute(
            """
            INSERT INTO snapshots (stream_id, version, state, created_at)
            VALUES ($1, $2, $3, NOW())
            ON CONFLICT (stream_id) DO UPDATE
            SET version = $2, state = $3, created_at = NOW()
            """,
            stream_id,
            version,
            json.dumps(state)
        )

        # Actualizar metadata
        await self.db.execute(
            """
            UPDATE stream_metadata
            SET snapshot_version = $2
            WHERE stream_id = $1
            """,
            stream_id, version
        )

    async def _get_snapshot(self, stream_id: str) -> Optional[dict]:
        """Obtiene último snapshot si existe"""
        row = await self.db.fetchrow(
            "SELECT version, state FROM snapshots WHERE stream_id = $1",
            stream_id
        )
        if row:
            return {
                'version': row['version'],
                'state': json.loads(row['state'])
            }
        return None

# ==========================================
# SNAPSHOT STRATEGY
# ==========================================
class SnapshotStrategy:
    """
    Estrategia para decidir cuándo crear snapshots
    """
    def __init__(self, threshold: int = 100):
        self.threshold = threshold

    def should_snapshot(
        self,
        event_count: int,
        last_snapshot_version: Optional[int]
    ) -> bool:
        """
        Crear snapshot cada N eventos
        """
        if last_snapshot_version is None:
            return event_count >= self.threshold

        events_since_snapshot = event_count - last_snapshot_version
        return events_since_snapshot >= self.threshold

class ConcurrencyError(Exception):
    """Error de concurrencia en event store"""
    pass
```

**🎯 Optimizaciones clave:**

1. **Optimistic Concurrency**: `UNIQUE(stream_id, stream_version)` + `FOR UPDATE`
2. **Snapshots**: Reduce reconstrucción de aggregates de O(n) a O(1)
3. **Índices**: GIN para JSONB, composite para stream queries
4. **Transacciones**: Atomicidad en append de múltiples eventos

---

## 3. Event Versioning y Schema Evolution

### ❌ ERROR COMÚN: Cambiar eventos existentes
```python
# MAL - modificar evento ya publicado
class OrderPlaced(BaseModel):
    order_id: str
    # Agregar nuevo campo rompe consumers
    priority: str  # BREAKING CHANGE!
```

### ✅ SOLUCIÓN: Versioning explícito con upcasting

```python
from typing import Union
from abc import ABC, abstractmethod

# ==========================================
# EVENT VERSIONING
# ==========================================

# Versión 1 (original)
class OrderPlacedV1(IntegrationEvent):
    schema_version: str = "1.0.0"
    event_type: str = "order.placed"

    order_id: str
    customer_id: str
    total_amount: float

# Versión 2 (con nuevo campo)
class OrderPlacedV2(IntegrationEvent):
    schema_version: str = "2.0.0"
    event_type: str = "order.placed"

    order_id: str
    customer_id: str
    total_amount: float
    currency: str = "USD"  # Nuevo campo con default
    payment_method: str = "credit_card"  # Nuevo campo

# Versión 3 (campo renombrado)
class OrderPlacedV3(IntegrationEvent):
    schema_version: str = "3.0.0"
    event_type: str = "order.placed"

    order_id: str
    customer_id: str
    amount: float  # Renombrado de total_amount
    currency: str = "USD"
    payment_method: str

# ==========================================
# UPCASTER PATTERN
# ==========================================
class EventUpcaster(ABC):
    """
    Transforma eventos viejos a versiones nuevas
    """
    @abstractmethod
    def upcast(self, old_event: dict) -> dict:
        pass

class OrderPlacedV1ToV2Upcaster(EventUpcaster):
    """
    Upcast de V1 → V2
    Agrega campos con defaults seguros
    """
    def upcast(self, old_event: dict) -> dict:
        return {
            **old_event,
            "schema_version": "2.0.0",
            "currency": "USD",
            "payment_method": "credit_card"
        }

class OrderPlacedV2ToV3Upcaster(EventUpcaster):
    """
    Upcast de V2 → V3
    Renombra total_amount → amount
    """
    def upcast(self, old_event: dict) -> dict:
        return {
            **old_event,
            "schema_version": "3.0.0",
            "amount": old_event.pop("total_amount")
        }

# ==========================================
# UPCASTER CHAIN
# ==========================================
class UpcasterChain:
    """
    Cadena de upcasters para migrar desde cualquier versión
    """
    def __init__(self):
        self.upcasters: Dict[tuple, EventUpcaster] = {}

    def register(
        self,
        from_version: str,
        to_version: str,
        upcaster: EventUpcaster
    ):
        self.upcasters[(from_version, to_version)] = upcaster

    def upcast_to_latest(
        self,
        event_data: dict,
        current_version: str,
        target_version: str
    ) -> dict:
        """
        Upcast desde current_version hasta target_version
        siguiendo la cadena de upcasters
        """
        result = event_data.copy()
        version = current_version

        # BFS para encontrar path de upcasting
        path = self._find_upcast_path(version, target_version)

        for from_v, to_v in path:
            upcaster = self.upcasters[(from_v, to_v)]
            result = upcaster.upcast(result)
            version = to_v

        return result

    def _find_upcast_path(
        self,
        from_version: str,
        to_version: str
    ) -> List[tuple]:
        """
        Encuentra secuencia de upcasts necesarios
        """
        # Simplified - en producción usar BFS real
        paths = {
            ("1.0.0", "3.0.0"): [("1.0.0", "2.0.0"), ("2.0.0", "3.0.0")],
            ("2.0.0", "3.0.0"): [("2.0.0", "3.0.0")],
        }
        return paths.get((from_version, to_version), [])

# ==========================================
# EVENT DESERIALIZER CON UPCASTING
# ==========================================
class EventDeserializer:
    """
    Deserializa eventos aplicando upcasting automático
    """
    def __init__(self, upcaster_chain: UpcasterChain):
        self.upcaster_chain = upcaster_chain
        self.latest_versions = {
            "order.placed": "3.0.0"
        }
        self.event_classes = {
            ("order.placed", "1.0.0"): OrderPlacedV1,
            ("order.placed", "2.0.0"): OrderPlacedV2,
            ("order.placed", "3.0.0"): OrderPlacedV3,
        }

    def deserialize(self, event_data: dict) -> IntegrationEvent:
        """
        Deserializa evento, aplicando upcasting si es necesario
        """
        event_type = event_data["event_type"]
        current_version = event_data["schema_version"]
        target_version = self.latest_versions[event_type]

        # Upcast si es necesario
        if current_version != target_version:
            event_data = self.upcaster_chain.upcast_to_latest(
                event_data,
                current_version,
                target_version
            )

        # Obtener clase correcta
        event_class = self.event_classes[(event_type, target_version)]
        return event_class(**event_data)

# ==========================================
# EJEMPLO DE USO
# ==========================================
async def example_event_versioning():
    # Setup
    chain = UpcasterChain()
    chain.register("1.0.0", "2.0.0", OrderPlacedV1ToV2Upcaster())
    chain.register("2.0.0", "3.0.0", OrderPlacedV2ToV3Upcaster())

    deserializer = EventDeserializer(chain)

    # Evento viejo de la base de datos (V1)
    old_event_data = {
        "event_id": "123",
        "event_type": "order.placed",
        "schema_version": "1.0.0",
        "source_context": "orders",
        "published_at": "2025-01-01T00:00:00",
        "order_id": "ord_001",
        "customer_id": "cust_001",
        "total_amount": 99.99
    }

    # Deserializa automáticamente a V3
    event = deserializer.deserialize(old_event_data)

    assert isinstance(event, OrderPlacedV3)
    assert event.amount == 99.99  # Renombrado de total_amount
    assert event.currency == "USD"  # Default agregado
```

**📋 Estrategias de Versionado:**

| Estrategia | Cuándo Usar | Ejemplo |
|-----------|-------------|---------|
| **Lazy Transformation** | Read-time upcasting | Aplicar upcaster al deserializar |
| **Eager Transformation** | Background migration | Job que actualiza eventos viejos |
| **Copy & Transform** | Eventos inmutables | Crear nuevo stream con eventos migrados |

---

## 4. Event Replay y Time Travel

### ✅ SOLUCIÓN: Capacidad de replay para debugging y auditing

```python
from typing import AsyncIterator
from datetime import datetime, timedelta

# ==========================================
# EVENT REPLAY ENGINE
# ==========================================
class EventReplayEngine:
    """
    Reproduce eventos para:
    - Debugging
    - Reconstruir projections
    - Migrar datos
    - Auditoría
    """

    def __init__(
        self,
        event_store: EventStore,
        event_bus: 'EventBus'
    ):
        self.event_store = event_store
        self.event_bus = event_bus

    async def replay_stream(
        self,
        stream_id: str,
        from_version: int = 0,
        to_version: Optional[int] = None,
        speed_multiplier: float = 1.0
    ):
        """
        Reproduce eventos de un stream

        Args:
            stream_id: ID del stream
            from_version: Versión inicial
            to_version: Versión final (None = todas)
            speed_multiplier: 1.0 = tiempo real, 10.0 = 10x más rápido
        """
        events = await self.event_store.get_events(
            stream_id,
            from_version,
            to_version
        )

        print(f"🔁 Replaying {len(events)} events from stream {stream_id}")

        prev_timestamp = None
        for i, event in enumerate(events, 1):
            # Respetar timing original (escalado)
            if prev_timestamp and speed_multiplier < float('inf'):
                delta = event.occurred_at - prev_timestamp
                await asyncio.sleep(delta.total_seconds() / speed_multiplier)

            await self.event_bus.publish(event)
            prev_timestamp = event.occurred_at

            if i % 100 == 0:
                print(f"  ✓ Replayed {i}/{len(events)} events")

    async def replay_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        event_types: Optional[List[str]] = None
    ):
        """
        Reproduce eventos en un rango de tiempo
        """
        query = """
            SELECT event_id, stream_id, event_type, event_data, occurred_at
            FROM events
            WHERE occurred_at BETWEEN $1 AND $2
        """
        params = [start_time, end_time]

        if event_types:
            query += " AND event_type = ANY($3)"
            params.append(event_types)

        query += " ORDER BY occurred_at ASC"

        rows = await self.event_store.db.fetch(query, *params)

        print(f"🔁 Replaying {len(rows)} events between {start_time} and {end_time}")

        for row in rows:
            event_data = json.loads(row['event_data'])
            event = self._deserialize_event(row['event_type'], event_data)
            await self.event_bus.publish(event)

    async def time_travel_to(
        self,
        stream_id: str,
        target_time: datetime
    ) -> dict:
        """
        "Viaja en el tiempo" - reconstruye estado del aggregate
        en un momento específico del pasado
        """
        events = await self.event_store.get_events(stream_id)

        # Filtrar eventos hasta target_time
        past_events = [
            e for e in events
            if e.occurred_at <= target_time
        ]

        # Reconstruir aggregate state
        aggregate_state = {}
        for event in past_events:
            aggregate_state = self._apply_event(aggregate_state, event)

        return aggregate_state

    def _apply_event(self, state: dict, event: DomainEvent) -> dict:
        """Aplica evento al estado (simplified)"""
        # En producción: delegar al aggregate correspondiente
        return {**state, **event.dict()}

    def _deserialize_event(self, event_type: str, data: dict) -> DomainEvent:
        """Deserializa evento desde storage"""
        # Usar registry de tipos
        return DomainEvent(**data)

# ==========================================
# PROJECTION REBUILDER
# ==========================================
class ProjectionRebuilder:
    """
    Reconstruye projections desde cero
    Útil para:
    - Migrar schema de projection
    - Corregir bugs en handlers
    - Crear nuevas projections
    """

    def __init__(
        self,
        event_store: EventStore,
        projection_store: 'ProjectionStore'
    ):
        self.event_store = event_store
        self.projection_store = projection_store

    async def rebuild_projection(
        self,
        projection_name: str,
        event_handler: 'ProjectionHandler',
        batch_size: int = 1000
    ):
        """
        Reconstruye projection desde eventos históricos
        """
        print(f"🔨 Rebuilding projection: {projection_name}")

        # 1. Limpiar projection existente
        await self.projection_store.clear(projection_name)

        # 2. Procesar eventos en batches
        offset = 0
        total_processed = 0

        while True:
            # Obtener batch de eventos
            events = await self._get_events_batch(offset, batch_size)
            if not events:
                break

            # Procesar cada evento
            for event in events:
                await event_handler.handle(event)
                total_processed += 1

            offset += batch_size

            if total_processed % 10000 == 0:
                print(f"  ✓ Processed {total_processed} events")

        print(f"✅ Projection rebuilt: {total_processed} events processed")

    async def _get_events_batch(
        self,
        offset: int,
        limit: int
    ) -> List[DomainEvent]:
        """Obtiene batch de eventos ordenados por tiempo"""
        rows = await self.event_store.db.fetch(
            """
            SELECT event_id, event_type, event_data, occurred_at
            FROM events
            ORDER BY occurred_at ASC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )

        return [
            DomainEvent(**json.loads(row['event_data']))
            for row in rows
        ]

# ==========================================
# EJEMPLO: DEBUGGING CON REPLAY
# ==========================================
async def example_debug_with_replay():
    """
    Caso de uso: Bug en production
    - Replay eventos para reproducir bug
    - Fix bug en handler
    - Rebuild projection
    """

    # 1. Identificar tiempo del bug
    bug_start = datetime(2025, 12, 26, 10, 0, 0)
    bug_end = datetime(2025, 12, 26, 11, 0, 0)

    # 2. Replay eventos en ese rango
    replay_engine = EventReplayEngine(event_store, event_bus)

    await replay_engine.replay_by_time_range(
        start_time=bug_start,
        end_time=bug_end,
        event_types=["OrderPlaced", "PaymentProcessed"]
    )

    # 3. Verificar en ambiente de staging
    # 4. Fix bug
    # 5. Rebuild projection en producción
    rebuilder = ProjectionRebuilder(event_store, projection_store)

    await rebuilder.rebuild_projection(
        projection_name="order_summary",
        event_handler=OrderSummaryProjectionHandler()
    )
```

---

## 5. Sagas Event-Driven

### ✅ SOLUCIÓN: Saga Pattern con eventos para transacciones distribuidas

```python
from enum import Enum
from typing import List, Callable, Awaitable

# ==========================================
# SAGA STATE
# ==========================================
class SagaStatus(Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"

@dataclass
class SagaState:
    saga_id: str
    saga_type: str
    status: SagaStatus
    current_step: int
    data: dict
    compensation_needed: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

# ==========================================
# SAGA STEP
# ==========================================
@dataclass
class SagaStep:
    """
    Paso de una saga
    - action: Comando a ejecutar
    - compensation: Comando de compensación si falla
    - event_to_wait: Evento de éxito a esperar
    """
    name: str
    action: Callable[[dict], Awaitable[None]]
    compensation: Callable[[dict], Awaitable[None]]
    success_event_type: str
    failure_event_type: Optional[str] = None

# ==========================================
# SAGA ORCHESTRATOR (Event-Driven)
# ==========================================
class EventDrivenSagaOrchestrator:
    """
    Orquesta saga respondiendo a eventos
    """

    def __init__(
        self,
        event_bus: 'EventBus',
        saga_store: 'SagaStore'
    ):
        self.event_bus = event_bus
        self.saga_store = saga_store
        self.saga_definitions: Dict[str, List[SagaStep]] = {}

    def define_saga(
        self,
        saga_type: str,
        steps: List[SagaStep]
    ):
        """
        Define una saga con sus pasos
        """
        self.saga_definitions[saga_type] = steps

        # Suscribirse a eventos de éxito/fallo de cada paso
        for step in steps:
            self.event_bus.subscribe(
                step.success_event_type,
                self._on_step_succeeded
            )
            if step.failure_event_type:
                self.event_bus.subscribe(
                    step.failure_event_type,
                    self._on_step_failed
                )

    async def start_saga(
        self,
        saga_type: str,
        saga_id: str,
        data: dict
    ):
        """
        Inicia una saga
        """
        steps = self.saga_definitions[saga_type]

        # Crear state
        state = SagaState(
            saga_id=saga_id,
            saga_type=saga_type,
            status=SagaStatus.STARTED,
            current_step=0,
            data=data
        )
        await self.saga_store.save(state)

        # Ejecutar primer paso
        await self._execute_step(state, steps[0])

    async def _execute_step(
        self,
        state: SagaState,
        step: SagaStep
    ):
        """
        Ejecuta un paso de la saga
        """
        print(f"🎯 Executing saga step: {step.name} (saga: {state.saga_id})")

        try:
            await step.action(state.data)

            # Agregar a lista de compensación
            state.compensation_needed.append(step.name)
            state.status = SagaStatus.IN_PROGRESS
            await self.saga_store.save(state)

        except Exception as e:
            print(f"❌ Step {step.name} failed: {e}")
            await self._start_compensation(state)

    async def _on_step_succeeded(self, event: DomainEvent):
        """
        Handler cuando un paso tiene éxito
        """
        # Obtener saga asociada
        saga_id = event.metadata.get("saga_id")
        if not saga_id:
            return

        state = await self.saga_store.get(saga_id)
        if not state:
            return

        steps = self.saga_definitions[state.saga_type]
        current_step = steps[state.current_step]

        # Verificar que es el evento esperado
        if event.event_type != current_step.success_event_type:
            return

        # Avanzar al siguiente paso
        state.current_step += 1

        if state.current_step >= len(steps):
            # Saga completada
            state.status = SagaStatus.COMPLETED
            state.completed_at = datetime.utcnow()
            await self.saga_store.save(state)
            print(f"✅ Saga completed: {saga_id}")
        else:
            # Ejecutar siguiente paso
            next_step = steps[state.current_step]
            await self._execute_step(state, next_step)

    async def _on_step_failed(self, event: DomainEvent):
        """
        Handler cuando un paso falla
        """
        saga_id = event.metadata.get("saga_id")
        if not saga_id:
            return

        state = await self.saga_store.get(saga_id)
        if not state:
            return

        await self._start_compensation(state)

    async def _start_compensation(self, state: SagaState):
        """
        Inicia proceso de compensación (rollback distribuido)
        """
        print(f"🔄 Starting compensation for saga: {state.saga_id}")

        state.status = SagaStatus.COMPENSATING
        await self.saga_store.save(state)

        steps = self.saga_definitions[state.saga_type]

        # Compensar en orden inverso
        for step_name in reversed(state.compensation_needed):
            step = next(s for s in steps if s.name == step_name)

            print(f"  🔙 Compensating: {step.name}")
            try:
                await step.compensation(state.data)
            except Exception as e:
                print(f"❌ Compensation failed for {step.name}: {e}")
                # Log y alertar - compensación crítica

        state.status = SagaStatus.COMPENSATED
        await self.saga_store.save(state)
        print(f"✅ Saga compensated: {state.saga_id}")

# ==========================================
# EJEMPLO: SAGA DE ORDER CHECKOUT
# ==========================================

# Commands
async def reserve_inventory(data: dict):
    """Paso 1: Reservar inventario"""
    # Publicar comando
    await event_bus.publish(ReserveInventoryCommand(
        order_id=data["order_id"],
        items=data["items"]
    ))

async def compensate_reserve_inventory(data: dict):
    """Compensación: Liberar inventario"""
    await event_bus.publish(ReleaseInventoryCommand(
        order_id=data["order_id"]
    ))

async def charge_payment(data: dict):
    """Paso 2: Cobrar pago"""
    await event_bus.publish(ChargePaymentCommand(
        order_id=data["order_id"],
        amount=data["total_amount"]
    ))

async def compensate_charge_payment(data: dict):
    """Compensación: Reembolsar pago"""
    await event_bus.publish(RefundPaymentCommand(
        order_id=data["order_id"]
    ))

async def ship_order(data: dict):
    """Paso 3: Enviar orden"""
    await event_bus.publish(ShipOrderCommand(
        order_id=data["order_id"]
    ))

async def compensate_ship_order(data: dict):
    """Compensación: Cancelar envío"""
    await event_bus.publish(CancelShipmentCommand(
        order_id=data["order_id"]
    ))

# Definir saga
orchestrator = EventDrivenSagaOrchestrator(event_bus, saga_store)

orchestrator.define_saga(
    saga_type="order_checkout",
    steps=[
        SagaStep(
            name="reserve_inventory",
            action=reserve_inventory,
            compensation=compensate_reserve_inventory,
            success_event_type="InventoryReserved",
            failure_event_type="InventoryReservationFailed"
        ),
        SagaStep(
            name="charge_payment",
            action=charge_payment,
            compensation=compensate_charge_payment,
            success_event_type="PaymentCharged",
            failure_event_type="PaymentFailed"
        ),
        SagaStep(
            name="ship_order",
            action=ship_order,
            compensation=compensate_ship_order,
            success_event_type="OrderShipped",
            failure_event_type="ShipmentFailed"
        ),
    ]
)

# Iniciar saga
await orchestrator.start_saga(
    saga_type="order_checkout",
    saga_id="saga_001",
    data={
        "order_id": "ord_001",
        "items": [{"sku": "ITEM1", "qty": 2}],
        "total_amount": 99.99
    }
)
```

**🎯 Ventajas de Sagas Event-Driven:**

- **Desacoplamiento**: Servicios no se conocen entre sí
- **Resiliencia**: Cada paso puede reintentar independientemente
- **Observabilidad**: Eventos auditables de cada paso
- **Flexibilidad**: Fácil agregar pasos o modificar flujo

---

## 6. Dead Letter Queues y Error Handling

### ✅ SOLUCIÓN: Manejo robusto de errores con DLQ y retry policies

```python
from typing import Protocol
import asyncio

# ==========================================
# RETRY POLICY
# ==========================================
@dataclass
class RetryPolicy:
    max_retries: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

class RetryStrategy:
    """
    Estrategias de retry:
    - Exponential backoff
    - Jitter para evitar thundering herd
    """

    def __init__(self, policy: RetryPolicy):
        self.policy = policy

    def get_delay(self, attempt: int) -> float:
        """
        Calcula delay para retry con exponential backoff + jitter
        """
        delay = min(
            self.policy.initial_delay_seconds * (self.policy.exponential_base ** attempt),
            self.policy.max_delay_seconds
        )

        if self.policy.jitter:
            # Random jitter ±25%
            jitter_factor = 0.75 + (random.random() * 0.5)
            delay *= jitter_factor

        return delay

    def should_retry(self, attempt: int, error: Exception) -> bool:
        """
        Decide si debe reintentar basado en:
        - Número de intentos
        - Tipo de error
        """
        if attempt >= self.policy.max_retries:
            return False

        # No reintentar errores permanentes
        if isinstance(error, (ValidationError, UnauthorizedError)):
            return False

        return True

# ==========================================
# DEAD LETTER QUEUE
# ==========================================
class DeadLetterQueue:
    """
    Almacena eventos que fallaron después de todos los retries
    """

    def __init__(self, db: asyncpg.Pool):
        self.db = db

    async def initialize_schema(self):
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS dead_letter_queue (
                id SERIAL PRIMARY KEY,
                event_id UUID NOT NULL,
                event_type VARCHAR(255) NOT NULL,
                event_data JSONB NOT NULL,
                error_message TEXT NOT NULL,
                error_stacktrace TEXT,
                retry_count INTEGER NOT NULL,
                failed_at TIMESTAMP NOT NULL,
                last_retry_at TIMESTAMP NOT NULL,

                -- Clasificación del error
                error_category VARCHAR(100),
                is_recoverable BOOLEAN DEFAULT true,

                -- Para replay manual
                replayed BOOLEAN DEFAULT false,
                replayed_at TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_dlq_event_type
                ON dead_letter_queue(event_type);
            CREATE INDEX IF NOT EXISTS idx_dlq_failed_at
                ON dead_letter_queue(failed_at);
            CREATE INDEX IF NOT EXISTS idx_dlq_not_replayed
                ON dead_letter_queue(replayed) WHERE NOT replayed;
        """)

    async def add(
        self,
        event: DomainEvent,
        error: Exception,
        retry_count: int
    ):
        """
        Agrega evento fallido a DLQ
        """
        await self.db.execute(
            """
            INSERT INTO dead_letter_queue (
                event_id, event_type, event_data,
                error_message, error_stacktrace,
                retry_count, failed_at, last_retry_at,
                error_category, is_recoverable
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            """,
            event.event_id,
            event.event_type,
            json.dumps(event.dict()),
            str(error),
            traceback.format_exc(),
            retry_count,
            datetime.utcnow(),
            datetime.utcnow(),
            self._categorize_error(error),
            self._is_recoverable(error)
        )

        # Alertar equipo
        await self._alert_team(event, error, retry_count)

    def _categorize_error(self, error: Exception) -> str:
        """Categoriza tipo de error"""
        if isinstance(error, TimeoutError):
            return "TIMEOUT"
        elif isinstance(error, ConnectionError):
            return "CONNECTION"
        elif isinstance(error, ValidationError):
            return "VALIDATION"
        else:
            return "UNKNOWN"

    def _is_recoverable(self, error: Exception) -> bool:
        """Determina si error es recuperable"""
        # Timeouts y errores de conexión son recuperables
        # Errores de validación no
        return isinstance(error, (TimeoutError, ConnectionError))

    async def _alert_team(
        self,
        event: DomainEvent,
        error: Exception,
        retry_count: int
    ):
        """Alerta al equipo sobre evento en DLQ"""
        # Integrar con sistema de alertas (Slack, PagerDuty)
        print(f"🚨 DLQ Alert: Event {event.event_type} failed after {retry_count} retries")
        print(f"   Error: {error}")

    async def get_failed_events(
        self,
        limit: int = 100,
        error_category: Optional[str] = None
    ) -> List[dict]:
        """Obtiene eventos en DLQ para análisis"""
        query = """
            SELECT * FROM dead_letter_queue
            WHERE NOT replayed
        """
        params = []

        if error_category:
            query += " AND error_category = $1"
            params.append(error_category)

        query += " ORDER BY failed_at DESC LIMIT $2"
        params.append(limit)

        rows = await self.db.fetch(query, *params)
        return [dict(row) for row in rows]

    async def replay_event(self, dlq_id: int):
        """Reintenta procesar evento desde DLQ"""
        row = await self.db.fetchrow(
            "SELECT event_data FROM dead_letter_queue WHERE id = $1",
            dlq_id
        )

        if not row:
            raise ValueError(f"DLQ event {dlq_id} not found")

        event_data = json.loads(row['event_data'])
        event = DomainEvent(**event_data)

        # Publicar de nuevo
        await event_bus.publish(event)

        # Marcar como replayed
        await self.db.execute(
            """
            UPDATE dead_letter_queue
            SET replayed = true, replayed_at = NOW()
            WHERE id = $1
            """,
            dlq_id
        )

# ==========================================
# RESILIENT EVENT HANDLER
# ==========================================
class ResilientEventHandler:
    """
    Wrapper que agrega retry logic y DLQ a event handlers
    """

    def __init__(
        self,
        handler: Callable,
        retry_policy: RetryPolicy,
        dlq: DeadLetterQueue
    ):
        self.handler = handler
        self.retry_strategy = RetryStrategy(retry_policy)
        self.dlq = dlq

    async def handle(self, event: DomainEvent):
        """
        Ejecuta handler con retry logic
        """
        attempt = 0

        while True:
            try:
                await self.handler(event)
                return  # Success

            except Exception as e:
                attempt += 1

                if not self.retry_strategy.should_retry(attempt, e):
                    # Dar up - enviar a DLQ
                    await self.dlq.add(event, e, attempt)
                    raise

                # Retry con backoff
                delay = self.retry_strategy.get_delay(attempt)
                print(f"⚠️  Retry {attempt}/{self.retry_strategy.policy.max_retries} "
                      f"after {delay:.1f}s: {e}")

                await asyncio.sleep(delay)

# ==========================================
# EJEMPLO DE USO
# ==========================================

# Handler que puede fallar
async def process_payment(event: PaymentRequestedEvent):
    # Llamada a API externa que puede fallar
    response = await payment_gateway.charge(
        amount=event.amount,
        token=event.payment_token
    )

    if not response.success:
        raise PaymentFailedError(response.error)

# Wrapper con resilencia
resilient_handler = ResilientEventHandler(
    handler=process_payment,
    retry_policy=RetryPolicy(
        max_retries=3,
        initial_delay_seconds=1.0,
        max_delay_seconds=30.0
    ),
    dlq=dead_letter_queue
)

# Registrar en event bus
event_bus.subscribe("PaymentRequested", resilient_handler.handle)
```

---

## 7. Projections y Read Models

### ✅ SOLUCIÓN: Projections optimizadas para queries

```python
# ==========================================
# PROJECTION HANDLER
# ==========================================
class ProjectionHandler(ABC):
    """
    Base para projection handlers
    """
    @abstractmethod
    async def handle(self, event: DomainEvent):
        pass

    @abstractmethod
    async def reset(self):
        """Limpia projection para rebuild"""
        pass

# ==========================================
# EJEMPLO: ORDER SUMMARY PROJECTION
# ==========================================
class OrderSummaryProjection(ProjectionHandler):
    """
    Projection optimizada para dashboard de órdenes

    Denormaliza datos de múltiples aggregates:
    - Orders
    - Customers
    - Products
    """

    def __init__(self, db: asyncpg.Pool):
        self.db = db

    async def initialize_schema(self):
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS order_summary (
                order_id VARCHAR(255) PRIMARY KEY,
                customer_id VARCHAR(255) NOT NULL,
                customer_name VARCHAR(255),
                customer_email VARCHAR(255),

                status VARCHAR(50) NOT NULL,
                total_amount DECIMAL(10, 2),
                currency VARCHAR(3),

                item_count INTEGER DEFAULT 0,
                items JSONB,

                placed_at TIMESTAMP,
                shipped_at TIMESTAMP,
                delivered_at TIMESTAMP,

                -- Para queries
                last_updated TIMESTAMP NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_order_summary_customer
                ON order_summary(customer_id);
            CREATE INDEX IF NOT EXISTS idx_order_summary_status
                ON order_summary(status);
            CREATE INDEX IF NOT EXISTS idx_order_summary_placed_at
                ON order_summary(placed_at DESC);
        """)

    async def handle(self, event: DomainEvent):
        """
        Actualiza projection basado en eventos
        """
        if event.event_type == "OrderPlaced":
            await self._on_order_placed(event)
        elif event.event_type == "OrderShipped":
            await self._on_order_shipped(event)
        elif event.event_type == "OrderDelivered":
            await self._on_order_delivered(event)
        elif event.event_type == "OrderCancelled":
            await self._on_order_cancelled(event)

    async def _on_order_placed(self, event: 'OrderPlacedEvent'):
        """Crea nuevo registro en projection"""
        await self.db.execute(
            """
            INSERT INTO order_summary (
                order_id, customer_id, status,
                total_amount, currency, item_count, items,
                placed_at, last_updated
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
            """,
            event.order_id,
            event.customer_id,
            "PLACED",
            event.total_amount,
            event.currency,
            len(event.items),
            json.dumps(event.items)
        )

    async def _on_order_shipped(self, event: 'OrderShippedEvent'):
        """Actualiza status y timestamp"""
        await self.db.execute(
            """
            UPDATE order_summary
            SET status = 'SHIPPED',
                shipped_at = $2,
                last_updated = NOW()
            WHERE order_id = $1
            """,
            event.order_id,
            event.shipped_at
        )

    async def _on_order_delivered(self, event: 'OrderDeliveredEvent'):
        await self.db.execute(
            """
            UPDATE order_summary
            SET status = 'DELIVERED',
                delivered_at = $2,
                last_updated = NOW()
            WHERE order_id = $1
            """,
            event.order_id,
            event.delivered_at
        )

    async def _on_order_cancelled(self, event: 'OrderCancelledEvent'):
        await self.db.execute(
            """
            UPDATE order_summary
            SET status = 'CANCELLED',
                last_updated = NOW()
            WHERE order_id = $1
            """,
            event.order_id
        )

    async def reset(self):
        """Limpia projection"""
        await self.db.execute("TRUNCATE TABLE order_summary")

    # Query methods (uso desde API)
    async def get_order(self, order_id: str) -> Optional[dict]:
        """Query optimizado - single lookup"""
        row = await self.db.fetchrow(
            "SELECT * FROM order_summary WHERE order_id = $1",
            order_id
        )
        return dict(row) if row else None

    async def get_customer_orders(
        self,
        customer_id: str,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[dict]:
        """Query optimizado con índice"""
        query = "SELECT * FROM order_summary WHERE customer_id = $1"
        params = [customer_id]

        if status:
            query += " AND status = $2"
            params.append(status)

        query += " ORDER BY placed_at DESC LIMIT $" + str(len(params) + 1)
        params.append(limit)

        rows = await self.db.fetch(query, *params)
        return [dict(row) for row in rows]

# ==========================================
# PROJECTION CONSISTENCY TRACKER
# ==========================================
class ProjectionConsistencyTracker:
    """
    Trackea qué eventos han sido procesados por cada projection
    Para garantizar exactly-once processing
    """

    def __init__(self, db: asyncpg.Pool):
        self.db = db

    async def initialize_schema(self):
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS projection_checkpoints (
                projection_name VARCHAR(255) PRIMARY KEY,
                last_processed_event_id UUID NOT NULL,
                last_processed_at TIMESTAMP NOT NULL,
                events_processed_count BIGINT DEFAULT 0
            );
        """)

    async def has_processed(
        self,
        projection_name: str,
        event_id: str
    ) -> bool:
        """Verifica si evento ya fue procesado"""
        # Implementación depende de garantías del event store
        # Opción 1: Trackear por event_id (idempotencia)
        # Opción 2: Trackear por sequence number
        pass

    async def mark_processed(
        self,
        projection_name: str,
        event_id: str
    ):
        """Marca evento como procesado"""
        await self.db.execute(
            """
            INSERT INTO projection_checkpoints
            (projection_name, last_processed_event_id, last_processed_at, events_processed_count)
            VALUES ($1, $2, NOW(), 1)
            ON CONFLICT (projection_name) DO UPDATE
            SET last_processed_event_id = $2,
                last_processed_at = NOW(),
                events_processed_count = projection_checkpoints.events_processed_count + 1
            """,
            projection_name, event_id
        )
```

**🎯 Ventajas de Projections:**

- **Performance**: Queries O(1) vs reconstruir aggregate O(n)
- **Flexibilidad**: Múltiples vistas del mismo dato
- **Escalabilidad**: Read models separados pueden escalar independientemente

---

## 8. Event Collaboration Patterns

### ✅ SOLUCIÓN: Patrones de colaboración entre bounded contexts

```python
# ==========================================
# PATTERN 1: EVENT NOTIFICATION
# ==========================================
"""
Caso: Notificar otros contexts de cambios
- Minimal data en evento
- Consumers hacen query si necesitan más info
"""

class UserRegisteredNotification(IntegrationEvent):
    """Event notification - solo ID"""
    event_type: str = "user.registered"
    user_id: str  # Solo ID, no datos completos

# Consumer hace query si necesita más datos
async def on_user_registered(event: UserRegisteredNotification):
    # Query API de Users para obtener datos completos
    user = await users_api.get_user(event.user_id)
    await send_welcome_email(user.email)

# ==========================================
# PATTERN 2: EVENT-CARRIED STATE TRANSFER
# ==========================================
"""
Caso: Evitar queries entre servicios
- Evento lleva datos completos
- Consumer guarda copia local
"""

class UserDetailsChangedEvent(IntegrationEvent):
    """Event con estado completo"""
    event_type: str = "user.details_changed"

    user_id: str
    email: str
    name: str
    preferences: dict
    # Todos los datos que consumers necesiten

# Consumer guarda copia local - no necesita query
async def on_user_details_changed(event: UserDetailsChangedEvent):
    # Guardar en cache/DB local
    await local_user_cache.update(
        user_id=event.user_id,
        email=event.email,
        name=event.name
    )

# ==========================================
# PATTERN 3: DOMAIN EVENT SOURCING
# ==========================================
"""
Caso: Event Sourcing completo
- Eventos como source of truth
- Consumers reconstruyen estado
"""

class ShoppingCartEvents:
    """Serie de eventos del dominio"""
    pass

class ItemAddedToCart(DomainEvent):
    cart_id: str
    item_id: str
    quantity: int
    added_at: datetime

class ItemRemovedFromCart(DomainEvent):
    cart_id: str
    item_id: str
    removed_at: datetime

# Reconstruir estado desde eventos
class ShoppingCart:
    def __init__(self, cart_id: str):
        self.cart_id = cart_id
        self.items: Dict[str, int] = {}

    def apply_event(self, event: DomainEvent):
        if isinstance(event, ItemAddedToCart):
            self.items[event.item_id] = self.items.get(event.item_id, 0) + event.quantity
        elif isinstance(event, ItemRemovedFromCart):
            self.items.pop(event.item_id, None)

# ==========================================
# PATTERN 4: EVENT COLLABORATION
# ==========================================
"""
Caso: Workflow distribuido sin orquestador central
- Servicios reaccionan a eventos de otros
- Choreography vs Orchestration
"""

# Service A: Orders
async def on_order_placed(event: OrderPlacedEvent):
    # Emitir evento para otros servicios
    await event_bus.publish(
        InventoryReservationRequested(
            order_id=event.order_id,
            items=event.items
        )
    )

# Service B: Inventory
async def on_inventory_reservation_requested(event: InventoryReservationRequested):
    # Procesar y emitir resultado
    success = await reserve_inventory(event.items)

    if success:
        await event_bus.publish(
            InventoryReserved(order_id=event.order_id)
        )
    else:
        await event_bus.publish(
            InventoryReservationFailed(order_id=event.order_id)
        )

# Service C: Payments
async def on_inventory_reserved(event: InventoryReserved):
    # Procesar pago
    await process_payment(event.order_id)
```

---

## 9. Testing Event-Driven Systems

### ✅ SOLUCIÓN: Estrategias de testing

```python
import pytest
from unittest.mock import AsyncMock

# ==========================================
# UNIT TESTS: Event Handlers
# ==========================================
@pytest.mark.asyncio
async def test_order_placed_handler():
    """Test unitario de event handler"""

    # Arrange
    mock_db = AsyncMock()
    handler = OrderSummaryProjection(mock_db)

    event = OrderPlacedEvent(
        order_id="ord_001",
        customer_id="cust_001",
        total_amount=99.99,
        currency="USD",
        items=[{"sku": "ITEM1", "qty": 1}],
        placed_at=datetime.utcnow()
    )

    # Act
    await handler.handle(event)

    # Assert
    mock_db.execute.assert_called_once()
    call_args = mock_db.execute.call_args[0]
    assert "INSERT INTO order_summary" in call_args[0]
    assert call_args[1] == "ord_001"

# ==========================================
# INTEGRATION TESTS: Event Flow
# ==========================================
@pytest.mark.asyncio
async def test_order_checkout_saga_success():
    """Test de flujo completo de saga"""

    # Arrange
    event_bus = InMemoryEventBus()
    saga_store = InMemorySagaStore()
    orchestrator = EventDrivenSagaOrchestrator(event_bus, saga_store)

    # Mocks para servicios externos
    inventory_service = AsyncMock()
    payment_service = AsyncMock()
    shipping_service = AsyncMock()

    # Act
    await orchestrator.start_saga(
        saga_type="order_checkout",
        saga_id="saga_001",
        data={"order_id": "ord_001", "total_amount": 99.99}
    )

    # Simular eventos de éxito
    await event_bus.publish(InventoryReserved(order_id="ord_001"))
    await event_bus.publish(PaymentCharged(order_id="ord_001"))
    await event_bus.publish(OrderShipped(order_id="ord_001"))

    # Assert
    state = await saga_store.get("saga_001")
    assert state.status == SagaStatus.COMPLETED

# ==========================================
# CONTRACT TESTS: Integration Events
# ==========================================
def test_order_placed_event_schema():
    """
    Test de contrato de Integration Event
    Garantiza backward compatibility
    """
    # Evento V1 (viejo)
    old_event = {
        "event_id": "123",
        "event_type": "order.placed",
        "schema_version": "1.0.0",
        "order_id": "ord_001",
        "customer_id": "cust_001",
        "total_amount": 99.99
    }

    # Debe poder deserializarse en V2
    event = OrderPlacedV2(**old_event)
    assert event.currency == "USD"  # Default value
    assert event.total_amount == 99.99

# ==========================================
# PROPERTY-BASED TESTS
# ==========================================
from hypothesis import given, strategies as st

@given(
    order_id=st.text(min_size=1),
    amount=st.floats(min_value=0.01, max_value=10000.0)
)
def test_order_placed_event_always_valid(order_id: str, amount: float):
    """
    Property: OrderPlacedEvent siempre debe ser válido
    con cualquier input válido
    """
    event = OrderPlacedEvent(
        order_id=order_id,
        customer_id="cust_001",
        total_amount=amount,
        currency="USD",
        items=[],
        placed_at=datetime.utcnow()
    )

    assert event.order_id == order_id
    assert event.total_amount == amount
    assert event.event_id is not None
```

---

## 10. Observabilidad en Event-Driven

### ✅ SOLUCIÓN: Tracing, metrics y logs para eventos

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

# ==========================================
# DISTRIBUTED TRACING
# ==========================================
class TracedEventBus:
    """
    Event bus con distributed tracing
    """

    async def publish(self, event: DomainEvent):
        """Publish con tracing automático"""

        with tracer.start_as_current_span(
            f"event.publish.{event.event_type}",
            attributes={
                "event.id": event.event_id,
                "event.type": event.event_type,
                "event.aggregate_id": event.aggregate_id,
            }
        ) as span:
            try:
                # Agregar trace context a metadata
                event.metadata["trace_id"] = format(span.get_span_context().trace_id, '032x')
                event.metadata["span_id"] = format(span.get_span_context().span_id, '016x')

                await self._do_publish(event)

                span.set_status(Status(StatusCode.OK))

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    async def _do_publish(self, event: DomainEvent):
        # Lógica real de publicación
        pass

# ==========================================
# METRICS
# ==========================================
from prometheus_client import Counter, Histogram

# Métricas de eventos
events_published = Counter(
    'events_published_total',
    'Total events published',
    ['event_type']
)

events_processed = Counter(
    'events_processed_total',
    'Total events processed',
    ['event_type', 'handler', 'status']
)

event_processing_duration = Histogram(
    'event_processing_duration_seconds',
    'Time to process event',
    ['event_type', 'handler']
)

# Handler con métricas
async def process_order_placed(event: OrderPlacedEvent):
    events_processed.labels(
        event_type="OrderPlaced",
        handler="process_order_placed",
        status="started"
    ).inc()

    with event_processing_duration.labels(
        event_type="OrderPlaced",
        handler="process_order_placed"
    ).time():
        try:
            # Process
            await do_process(event)

            events_processed.labels(
                event_type="OrderPlaced",
                handler="process_order_placed",
                status="success"
            ).inc()

        except Exception as e:
            events_processed.labels(
                event_type="OrderPlaced",
                handler="process_order_placed",
                status="failure"
            ).inc()
            raise

# ==========================================
# STRUCTURED LOGGING
# ==========================================
import structlog

logger = structlog.get_logger()

async def traced_event_handler(event: DomainEvent):
    """Handler con logging estructurado"""

    logger = structlog.get_logger().bind(
        event_id=event.event_id,
        event_type=event.event_type,
        aggregate_id=event.aggregate_id,
        trace_id=event.metadata.get("trace_id")
    )

    logger.info("event.processing.started")

    try:
        await process_event(event)
        logger.info("event.processing.completed")

    except Exception as e:
        logger.error(
            "event.processing.failed",
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

---

## 📊 Resumen: Decision Matrix

| Patrón | Usar Cuando | No Usar Cuando |
|--------|-------------|----------------|
| **Event Sourcing** | Auditoría completa necesaria | CRUD simple |
| **CQRS** | Read/Write patterns diferentes | Dominios simples |
| **Saga** | Transacciones distribuidas | Transacción local suficiente |
| **Event Collaboration** | Desacoplamiento crítico | Baja latencia crítica |
| **DLQ** | Procesamiento asíncrono | Operaciones síncronas |

**Tamaño:** 58KB | **Código:** ~2,400 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
