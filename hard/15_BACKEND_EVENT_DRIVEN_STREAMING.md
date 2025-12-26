# Backend: Event-Driven Architecture y Stream Processing

## Objetivo
Patrones avanzados de arquitectura event-driven: Kafka, Event Sourcing, CQRS, API Gateway patterns, y service mesh.

---

## CATEGORÍA 1: Apache Kafka y Stream Processing

### 1.1 Kafka Producer Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

**Python - Kafka Producer con garantías de entrega**

```python
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from typing import Optional
import time

class ReliableKafkaProducer:
    """
    Kafka producer con:
    - Idempotencia
    - At-least-once/Exactly-once delivery
    - Retry logic
    - Monitoring
    """

    def __init__(
        self,
        bootstrap_servers: list,
        acks: str = 'all',  # 'all', '1', '0'
        enable_idempotence: bool = True,
        max_retries: int = 3
    ):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,

            # Serialización
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),

            # Garantías de entrega
            acks=acks,  # 'all' = espera a todos los replicas
            enable_idempotence=enable_idempotence,  # Exactly-once

            # Retry
            retries=max_retries,
            max_in_flight_requests_per_connection=5,

            # Batching para performance
            batch_size=16384,
            linger_ms=10,  # Espera 10ms para hacer batch

            # Compression
            compression_type='snappy',

            # Timeouts
            request_timeout_ms=30000,

            # Seguridad
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username='username',
            sasl_plain_password='password'
        )

    async def send_event(
        self,
        topic: str,
        event: dict,
        key: Optional[str] = None,
        partition: Optional[int] = None,
        headers: Optional[list] = None
    ) -> dict:
        """
        Send event to Kafka with delivery confirmation
        """

        # Add metadata
        event_with_metadata = {
            **event,
            '_timestamp': int(time.time() * 1000),
            '_producer': 'order-service',
            '_version': '1.0'
        }

        # Prepare headers
        kafka_headers = headers or []
        kafka_headers.extend([
            ('event_type', event.get('type', '').encode('utf-8')),
            ('trace_id', str(event.get('trace_id', '')).encode('utf-8'))
        ])

        try:
            # Send async
            future = self.producer.send(
                topic=topic,
                key=key,
                value=event_with_metadata,
                partition=partition,
                headers=kafka_headers
            )

            # Wait for confirmation (synchronous)
            record_metadata = future.get(timeout=30)

            return {
                'success': True,
                'topic': record_metadata.topic,
                'partition': record_metadata.partition,
                'offset': record_metadata.offset,
                'timestamp': record_metadata.timestamp
            }

        except KafkaError as e:
            logger.error(f"Failed to send event to Kafka: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def send_event_async(
        self,
        topic: str,
        event: dict,
        key: Optional[str] = None,
        callback=None
    ):
        """
        Send event asynchronously with callback
        """

        def on_send_success(record_metadata):
            logger.info(
                f"Event sent: {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}"
            )
            if callback:
                callback(record_metadata, None)

        def on_send_error(exc):
            logger.error(f"Event send failed: {exc}")
            if callback:
                callback(None, exc)

        future = self.producer.send(topic, key=key, value=event)
        future.add_callback(on_send_success)
        future.add_errback(on_send_error)

    def flush(self, timeout: int = 30):
        """Ensure all messages are sent"""
        self.producer.flush(timeout=timeout)

    def close(self):
        """Close producer"""
        self.producer.close()

# Uso en aplicación
producer = ReliableKafkaProducer(
    bootstrap_servers=['kafka1:9092', 'kafka2:9092', 'kafka3:9092'],
    acks='all',
    enable_idempotence=True
)

@app.post("/orders")
async def create_order(order_data: dict):
    # Crear orden en DB
    order = await db.create_order(order_data)

    # Publicar evento
    event = {
        'type': 'order.created',
        'order_id': order.id,
        'user_id': order.user_id,
        'total': order.total,
        'items': order.items
    }

    result = await producer.send_event(
        topic='orders',
        event=event,
        key=str(order.id)  # Partitioning key
    )

    if not result['success']:
        logger.error("Failed to publish order event")
        # Implementar compensación o retry

    return order

# Partitioning strategy
class CustomPartitioner:
    """Custom partitioner para distribución de carga"""

    def __init__(self, partitions):
        self.partitions = partitions

    def __call__(self, key, all_partitions, available_partitions):
        """
        Partition based on user_id to ensure:
        - Same user's events go to same partition (ordering)
        - Load balanced across partitions
        """
        if key is None:
            # Round-robin for events without key
            return random.choice(available_partitions)

        # Hash user_id to partition
        user_id = int(key.decode('utf-8'))
        return all_partitions[user_id % len(all_partitions)]

# Transactional producer (Exactly-once semantics)
class TransactionalKafkaProducer:
    """
    Producer with transactional semantics
    All messages in transaction are committed atomically
    """

    def __init__(self, bootstrap_servers: list, transactional_id: str):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),

            # Transaction config
            transactional_id=transactional_id,
            enable_idempotence=True,
            acks='all',
            max_in_flight_requests_per_connection=5
        )

        # Initialize transactions
        self.producer.init_transactions()

    def send_transactional(self, messages: list):
        """
        Send multiple messages in a transaction
        All or nothing
        """
        try:
            self.producer.begin_transaction()

            for msg in messages:
                self.producer.send(
                    topic=msg['topic'],
                    key=msg.get('key'),
                    value=msg['value']
                )

            self.producer.commit_transaction()
            logger.info(f"Transaction committed: {len(messages)} messages")

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            self.producer.abort_transaction()
            raise

# Example: Order saga with transactional outbox
async def create_order_with_outbox(order_data: dict):
    """
    Transactional outbox pattern:
    1. Write to DB and outbox table in same transaction
    2. Background process publishes from outbox to Kafka
    """

    async with db.transaction():
        # Create order
        order = await db.execute(
            "INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING *",
            order_data['user_id'], order_data['total']
        )

        # Write to outbox
        await db.execute(
            """
            INSERT INTO outbox (aggregate_id, event_type, payload, created_at)
            VALUES ($1, $2, $3, NOW())
            """,
            order[0]['id'],
            'order.created',
            json.dumps({
                'order_id': order[0]['id'],
                'user_id': order[0]['user_id'],
                'total': order[0]['total']
            })
        )

    return order[0]

# Outbox processor (background worker)
async def process_outbox():
    """
    Poll outbox table and publish events to Kafka
    """
    while True:
        try:
            # Get unpublished events
            events = await db.execute(
                """
                SELECT id, aggregate_id, event_type, payload
                FROM outbox
                WHERE published = false
                ORDER BY created_at
                LIMIT 100
                FOR UPDATE SKIP LOCKED
                """
            )

            for event in events:
                # Publish to Kafka
                result = await producer.send_event(
                    topic='orders',
                    event=json.loads(event['payload']),
                    key=str(event['aggregate_id'])
                )

                if result['success']:
                    # Mark as published
                    await db.execute(
                        "UPDATE outbox SET published = true WHERE id = $1",
                        event['id']
                    )

            await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Outbox processing error: {e}")
            await asyncio.sleep(5)
```

---

### 1.2 Kafka Consumer Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
import asyncio
from typing import Callable

class ReliableKafkaConsumer:
    """
    Kafka consumer con:
    - At-least-once processing
    - Manual offset management
    - Error handling y retry
    - Graceful shutdown
    """

    def __init__(
        self,
        topics: list,
        group_id: str,
        bootstrap_servers: list,
        handler: Callable,
        max_retries: int = 3
    ):
        self.topics = topics
        self.handler = handler
        self.max_retries = max_retries
        self.running = False

        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,

            # Deserialization
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),

            # Offset management
            enable_auto_commit=False,  # Manual commit
            auto_offset_reset='earliest',  # 'earliest', 'latest', 'none'

            # Session management
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,

            # Fetch config
            fetch_min_bytes=1,
            fetch_max_wait_ms=500,
            max_poll_records=500,
            max_poll_interval_ms=300000,  # 5 minutes

            # Security
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN'
        )

    async def start(self):
        """Start consuming messages"""
        self.running = True

        try:
            while self.running:
                # Poll for messages
                records = self.consumer.poll(timeout_ms=1000, max_records=100)

                for topic_partition, messages in records.items():
                    await self._process_batch(topic_partition, messages)

        except Exception as e:
            logger.error(f"Consumer error: {e}")
        finally:
            self.consumer.close()

    async def _process_batch(self, topic_partition, messages):
        """Process batch of messages"""

        for message in messages:
            success = await self._process_message(message)

            if success:
                # Commit offset after successful processing
                self.consumer.commit({
                    topic_partition: message.offset + 1
                })
            else:
                # Handle failure
                await self._handle_failed_message(message)
                # Option: stop processing this partition
                break

    async def _process_message(self, message) -> bool:
        """Process single message with retry"""

        for attempt in range(self.max_retries):
            try:
                logger.info(
                    f"Processing message: {message.topic}:{message.partition}:{message.offset}"
                )

                # Call handler
                await self.handler(message.value)

                logger.info(
                    f"Message processed successfully: {message.offset}"
                )
                return True

            except Exception as e:
                logger.error(
                    f"Message processing failed (attempt {attempt + 1}): {e}"
                )

                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff

        return False

    async def _handle_failed_message(self, message):
        """Handle message that failed all retries"""

        logger.error(
            f"Message failed after {self.max_retries} attempts: {message.offset}"
        )

        # Send to DLQ (Dead Letter Queue)
        await producer.send_event(
            topic='dlq.orders',
            event={
                'original_topic': message.topic,
                'original_partition': message.partition,
                'original_offset': message.offset,
                'value': message.value,
                'headers': message.headers
            }
        )

        # Still commit offset to avoid reprocessing
        # DLQ will be processed separately

    def stop(self):
        """Graceful shutdown"""
        logger.info("Stopping consumer...")
        self.running = False

# Message handlers
async def handle_order_created(event: dict):
    """Handle order.created event"""
    order_id = event['order_id']
    user_id = event['user_id']

    logger.info(f"Processing order {order_id} for user {user_id}")

    # Business logic
    await send_order_confirmation_email(user_id, order_id)
    await update_inventory(event['items'])
    await create_shipment(order_id)

async def handle_order_paid(event: dict):
    """Handle order.paid event"""
    order_id = event['order_id']

    await update_order_status(order_id, 'paid')
    await trigger_fulfillment(order_id)

# Event router
class EventRouter:
    """Route events to appropriate handlers"""

    def __init__(self):
        self.handlers = {}

    def register(self, event_type: str, handler: Callable):
        self.handlers[event_type] = handler

    async def route(self, event: dict):
        event_type = event.get('type')

        if event_type not in self.handlers:
            logger.warning(f"No handler for event type: {event_type}")
            return

        handler = self.handlers[event_type]
        await handler(event)

router = EventRouter()
router.register('order.created', handle_order_created)
router.register('order.paid', handle_order_paid)

# Consumer con event router
consumer = ReliableKafkaConsumer(
    topics=['orders'],
    group_id='order-processor',
    bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
    handler=router.route
)

# Parallel processing con múltiples consumers
class ParallelKafkaConsumer:
    """
    Process messages in parallel while maintaining order per partition
    """

    def __init__(
        self,
        topics: list,
        group_id: str,
        bootstrap_servers: list,
        handler: Callable,
        num_workers: int = 5
    ):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=False
        )
        self.handler = handler
        self.num_workers = num_workers
        self.partition_queues = {}
        self.running = False

    async def start(self):
        """Start consuming with parallel workers"""
        self.running = True

        # Start worker tasks
        workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.num_workers)
        ]

        # Poll messages and distribute to workers
        try:
            while self.running:
                records = self.consumer.poll(timeout_ms=1000)

                for topic_partition, messages in records.items():
                    # Ensure queue exists for partition
                    if topic_partition not in self.partition_queues:
                        self.partition_queues[topic_partition] = asyncio.Queue()

                    # Add messages to partition queue
                    for message in messages:
                        await self.partition_queues[topic_partition].put(message)

        finally:
            # Stop workers
            for worker in workers:
                worker.cancel()

            await asyncio.gather(*workers, return_exceptions=True)
            self.consumer.close()

    async def _worker(self, worker_id: int):
        """Worker that processes messages from partition queues"""

        logger.info(f"Worker {worker_id} started")

        while self.running:
            try:
                # Process messages from any partition queue
                for topic_partition, queue in self.partition_queues.items():
                    if not queue.empty():
                        message = await queue.get()

                        try:
                            await self.handler(message.value)

                            # Commit offset
                            self.consumer.commit({
                                topic_partition: message.offset + 1
                            })

                        except Exception as e:
                            logger.error(f"Worker {worker_id} error: {e}")

                await asyncio.sleep(0.01)

            except asyncio.CancelledError:
                break

        logger.info(f"Worker {worker_id} stopped")

# Kafka Streams (stateful processing)
from kafka import KafkaConsumer, KafkaProducer
from collections import defaultdict

class KafkaStreamProcessor:
    """
    Stateful stream processing
    Example: Count orders per user (windowed aggregation)
    """

    def __init__(self, bootstrap_servers: list):
        self.consumer = KafkaConsumer(
            'orders',
            bootstrap_servers=bootstrap_servers,
            group_id='order-aggregator',
            enable_auto_commit=False
        )

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        # In-memory state (in production, use RocksDB or Redis)
        self.state = defaultdict(int)
        self.window_size = 3600  # 1 hour

    async def process(self):
        """Process stream with stateful aggregations"""

        while True:
            records = self.consumer.poll(timeout_ms=1000)

            for topic_partition, messages in records.items():
                for message in messages:
                    event = message.value

                    if event['type'] == 'order.created':
                        user_id = event['user_id']

                        # Update state
                        self.state[user_id] += 1

                        # Emit aggregated event
                        self.producer.send(
                            'order-stats',
                            key=str(user_id).encode('utf-8'),
                            value={
                                'user_id': user_id,
                                'order_count': self.state[user_id],
                                'window_start': int(time.time() // self.window_size) * self.window_size
                            }
                        )

                    self.consumer.commit({
                        topic_partition: message.offset + 1
                    })
```

---

## CATEGORÍA 2: Event Sourcing y CQRS

### 2.1 Event Sourcing Pattern
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod

# Domain Events
@dataclass
class DomainEvent(ABC):
    """Base class for domain events"""
    aggregate_id: str
    timestamp: datetime
    version: int
    event_id: str

@dataclass
class OrderCreated(DomainEvent):
    user_id: int
    items: List[dict]
    total: float

@dataclass
class OrderPaid(DomainEvent):
    payment_id: str
    amount: float

@dataclass
class OrderShipped(DomainEvent):
    shipment_id: str
    tracking_number: str

@dataclass
class OrderCancelled(DomainEvent):
    reason: str

# Aggregate Root
class Order:
    """
    Order aggregate reconstructed from events
    State is derived from event history
    """

    def __init__(self, order_id: str):
        self.order_id = order_id
        self.user_id = None
        self.items = []
        self.total = 0.0
        self.status = 'pending'
        self.payment_id = None
        self.shipment_id = None

        # Event sourcing metadata
        self.version = 0
        self.uncommitted_events = []

    def create(self, user_id: int, items: List[dict], total: float):
        """Create new order - generates event"""

        if self.version > 0:
            raise ValueError("Order already exists")

        event = OrderCreated(
            aggregate_id=self.order_id,
            timestamp=datetime.utcnow(),
            version=self.version + 1,
            event_id=str(uuid.uuid4()),
            user_id=user_id,
            items=items,
            total=total
        )

        self._apply_event(event)
        self.uncommitted_events.append(event)

    def mark_paid(self, payment_id: str, amount: float):
        """Mark order as paid - generates event"""

        if self.status != 'pending':
            raise ValueError(f"Cannot mark order as paid, current status: {self.status}")

        event = OrderPaid(
            aggregate_id=self.order_id,
            timestamp=datetime.utcnow(),
            version=self.version + 1,
            event_id=str(uuid.uuid4()),
            payment_id=payment_id,
            amount=amount
        )

        self._apply_event(event)
        self.uncommitted_events.append(event)

    def mark_shipped(self, shipment_id: str, tracking_number: str):
        """Mark order as shipped - generates event"""

        if self.status != 'paid':
            raise ValueError(f"Cannot ship order, current status: {self.status}")

        event = OrderShipped(
            aggregate_id=self.order_id,
            timestamp=datetime.utcnow(),
            version=self.version + 1,
            event_id=str(uuid.uuid4()),
            shipment_id=shipment_id,
            tracking_number=tracking_number
        )

        self._apply_event(event)
        self.uncommitted_events.append(event)

    def cancel(self, reason: str):
        """Cancel order - generates event"""

        if self.status in ['shipped', 'delivered']:
            raise ValueError(f"Cannot cancel order, current status: {self.status}")

        event = OrderCancelled(
            aggregate_id=self.order_id,
            timestamp=datetime.utcnow(),
            version=self.version + 1,
            event_id=str(uuid.uuid4()),
            reason=reason
        )

        self._apply_event(event)
        self.uncommitted_events.append(event)

    def _apply_event(self, event: DomainEvent):
        """Apply event to update aggregate state"""

        if isinstance(event, OrderCreated):
            self.user_id = event.user_id
            self.items = event.items
            self.total = event.total
            self.status = 'pending'

        elif isinstance(event, OrderPaid):
            self.payment_id = event.payment_id
            self.status = 'paid'

        elif isinstance(event, OrderShipped):
            self.shipment_id = event.shipment_id
            self.status = 'shipped'

        elif isinstance(event, OrderCancelled):
            self.status = 'cancelled'

        self.version = event.version

    @classmethod
    def from_events(cls, order_id: str, events: List[DomainEvent]) -> 'Order':
        """Reconstruct aggregate from event history"""

        order = cls(order_id)

        for event in events:
            order._apply_event(event)

        return order

# Event Store
class EventStore:
    """
    Store and retrieve events
    This is the source of truth for aggregate state
    """

    def __init__(self, db):
        self.db = db

    async def save_events(
        self,
        aggregate_id: str,
        events: List[DomainEvent],
        expected_version: int
    ):
        """
        Save events with optimistic locking
        Ensures no concurrent modifications
        """

        async with self.db.transaction():
            # Check version for optimistic locking
            current_version = await self._get_current_version(aggregate_id)

            if current_version != expected_version:
                raise ConcurrencyError(
                    f"Expected version {expected_version}, "
                    f"but current is {current_version}"
                )

            # Store events
            for event in events:
                await self.db.execute(
                    """
                    INSERT INTO events (
                        event_id, aggregate_id, event_type, event_data,
                        version, timestamp
                    )
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    event.event_id,
                    event.aggregate_id,
                    event.__class__.__name__,
                    self._serialize_event(event),
                    event.version,
                    event.timestamp
                )

    async def get_events(
        self,
        aggregate_id: str,
        from_version: int = 0
    ) -> List[DomainEvent]:
        """Get event history for aggregate"""

        rows = await self.db.execute(
            """
            SELECT event_id, event_type, event_data, version, timestamp
            FROM events
            WHERE aggregate_id = $1 AND version > $2
            ORDER BY version ASC
            """,
            aggregate_id,
            from_version
        )

        events = []
        for row in rows:
            event = self._deserialize_event(
                row['event_type'],
                row['event_data'],
                row['version'],
                row['timestamp']
            )
            events.append(event)

        return events

    async def _get_current_version(self, aggregate_id: str) -> int:
        result = await self.db.execute(
            """
            SELECT MAX(version) as version
            FROM events
            WHERE aggregate_id = $1
            """,
            aggregate_id
        )

        return result[0]['version'] or 0

    def _serialize_event(self, event: DomainEvent) -> str:
        data = {
            k: v for k, v in event.__dict__.items()
            if k not in ['aggregate_id', 'timestamp', 'version', 'event_id']
        }
        return json.dumps(data)

    def _deserialize_event(
        self,
        event_type: str,
        event_data: str,
        version: int,
        timestamp: datetime
    ) -> DomainEvent:
        data = json.loads(event_data)

        event_classes = {
            'OrderCreated': OrderCreated,
            'OrderPaid': OrderPaid,
            'OrderShipped': OrderShipped,
            'OrderCancelled': OrderCancelled
        }

        event_class = event_classes[event_type]
        return event_class(
            version=version,
            timestamp=timestamp,
            **data
        )

# Repository
class OrderRepository:
    """Repository for Order aggregate"""

    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    async def get(self, order_id: str) -> Optional[Order]:
        """Reconstruct order from events"""

        events = await self.event_store.get_events(order_id)

        if not events:
            return None

        return Order.from_events(order_id, events)

    async def save(self, order: Order):
        """Save uncommitted events"""

        if not order.uncommitted_events:
            return

        await self.event_store.save_events(
            aggregate_id=order.order_id,
            events=order.uncommitted_events,
            expected_version=order.version - len(order.uncommitted_events)
        )

        order.uncommitted_events = []

# Usage
event_store = EventStore(db)
order_repo = OrderRepository(event_store)

@app.post("/orders")
async def create_order(order_data: dict):
    order_id = str(uuid.uuid4())

    # Create new order aggregate
    order = Order(order_id)
    order.create(
        user_id=order_data['user_id'],
        items=order_data['items'],
        total=order_data['total']
    )

    # Save events
    await order_repo.save(order)

    return {'order_id': order_id}

@app.post("/orders/{order_id}/pay")
async def pay_order(order_id: str, payment_data: dict):
    # Load order from events
    order = await order_repo.get(order_id)

    if not order:
        raise HTTPException(status_code=404)

    # Execute command
    order.mark_paid(
        payment_id=payment_data['payment_id'],
        amount=payment_data['amount']
    )

    # Save new events
    await order_repo.save(order)

    return {'status': 'paid'}
```

---

### 2.2 CQRS (Command Query Responsibility Segregation)
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# Write Model (Commands)
class OrderCommandService:
    """
    Handle commands - writes to event store
    """

    def __init__(self, order_repo: OrderRepository):
        self.repo = order_repo

    async def create_order(self, command: dict) -> str:
        order_id = str(uuid.uuid4())
        order = Order(order_id)

        order.create(
            user_id=command['user_id'],
            items=command['items'],
            total=command['total']
        )

        await self.repo.save(order)

        return order_id

    async def pay_order(self, command: dict):
        order = await self.repo.get(command['order_id'])

        if not order:
            raise ValueError("Order not found")

        order.mark_paid(
            payment_id=command['payment_id'],
            amount=command['amount']
        )

        await self.repo.save(order)

# Read Model (Queries)
class OrderQueryService:
    """
    Handle queries - reads from read-optimized projections
    """

    def __init__(self, db):
        self.db = db

    async def get_order(self, order_id: str) -> Optional[dict]:
        """Get order from read model (denormalized view)"""

        result = await self.db.execute(
            """
            SELECT o.*, u.name as user_name, u.email as user_email
            FROM orders_view o
            JOIN users u ON o.user_id = u.id
            WHERE o.id = $1
            """,
            order_id
        )

        return result[0] if result else None

    async def get_user_orders(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20
    ) -> List[dict]:
        """Get all orders for user (optimized query)"""

        offset = (page - 1) * page_size

        results = await self.db.execute(
            """
            SELECT id, total, status, created_at
            FROM orders_view
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2 OFFSET $3
            """,
            user_id, page_size, offset
        )

        return results

    async def get_order_stats(self, user_id: int) -> dict:
        """Get aggregated stats (pre-computed)"""

        result = await self.db.execute(
            """
            SELECT
                COUNT(*) as total_orders,
                SUM(total) as total_spent,
                AVG(total) as average_order
            FROM orders_view
            WHERE user_id = $1
            """,
            user_id
        )

        return result[0]

# Projection Builder (Event Handler)
class OrderProjectionBuilder:
    """
    Listen to events and update read models
    This runs asynchronously from write side
    """

    def __init__(self, db):
        self.db = db

    async def handle_order_created(self, event: OrderCreated):
        """Update read model when order is created"""

        await self.db.execute(
            """
            INSERT INTO orders_view (
                id, user_id, total, status, created_at
            )
            VALUES ($1, $2, $3, 'pending', $4)
            """,
            event.aggregate_id,
            event.user_id,
            event.total,
            event.timestamp
        )

    async def handle_order_paid(self, event: OrderPaid):
        """Update read model when order is paid"""

        await self.db.execute(
            """
            UPDATE orders_view
            SET status = 'paid', payment_id = $2, updated_at = $3
            WHERE id = $1
            """,
            event.aggregate_id,
            event.payment_id,
            event.timestamp
        )

    async def handle_order_shipped(self, event: OrderShipped):
        """Update read model when order is shipped"""

        await self.db.execute(
            """
            UPDATE orders_view
            SET status = 'shipped', shipment_id = $2, updated_at = $3
            WHERE id = $1
            """,
            event.aggregate_id,
            event.shipment_id,
            event.timestamp
        )

# Event Dispatcher
class EventDispatcher:
    """
    Read events from event store and dispatch to projections
    """

    def __init__(self, event_store: EventStore, projection_builder: OrderProjectionBuilder):
        self.event_store = event_store
        self.projection = projection_builder
        self.last_processed_position = 0

    async def start(self):
        """Start processing events"""

        while True:
            try:
                # Get new events
                events = await self.event_store.get_events_since(
                    self.last_processed_position
                )

                for event in events:
                    await self._dispatch_event(event)
                    self.last_processed_position = event.version

                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Event processing error: {e}")
                await asyncio.sleep(5)

    async def _dispatch_event(self, event: DomainEvent):
        """Dispatch event to appropriate handler"""

        if isinstance(event, OrderCreated):
            await self.projection.handle_order_created(event)

        elif isinstance(event, OrderPaid):
            await self.projection.handle_order_paid(event)

        elif isinstance(event, OrderShipped):
            await self.projection.handle_order_shipped(event)

# API endpoints - CQRS separation
command_service = OrderCommandService(order_repo)
query_service = OrderQueryService(db)

# Commands (writes)
@app.post("/commands/orders")
async def create_order_command(command: dict):
    order_id = await command_service.create_order(command)
    return {'order_id': order_id}

@app.post("/commands/orders/{order_id}/pay")
async def pay_order_command(order_id: str, command: dict):
    await command_service.pay_order({
        'order_id': order_id,
        **command
    })
    return {'status': 'accepted'}

# Queries (reads)
@app.get("/queries/orders/{order_id}")
async def get_order_query(order_id: str):
    order = await query_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404)
    return order

@app.get("/queries/users/{user_id}/orders")
async def get_user_orders_query(user_id: int, page: int = 1):
    orders = await query_service.get_user_orders(user_id, page)
    return {'orders': orders}

@app.get("/queries/users/{user_id}/stats")
async def get_user_stats_query(user_id: int):
    stats = await query_service.get_order_stats(user_id)
    return stats
```

---

Continúa en siguiente sección...

---

## Resumen Event-Driven y Streaming

| Tema | Dificultad | Complejidad | Impacto | Prioridad |
|------|------------|-------------|---------|-----------|
| Kafka Producer/Consumer | 5 | 5 | 5 | **CRÍTICA** |
| Event Sourcing | 5 | 5 | 4 | **ALTA** |
| CQRS | 5 | 5 | 4 | **ALTA** |
| Stream Processing | 5 | 5 | 4 | **ALTA** |
| Transactional Outbox | 4 | 4 | 5 | **CRÍTICA** |
| Event Projection | 4 | 4 | 4 | **ALTA** |

**El siguiente archivo continuará con:**
- API Gateway patterns (rate limiting, authentication, routing)
- Service Discovery (Consul, etcd)
- Circuit Breaker con Hystrix/Resilience4j
- Distributed Caching (Redis Cluster)
- Security avanzada (OAuth2 flows, mTLS, JWT rotation)
- Chaos Engineering
