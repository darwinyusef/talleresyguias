# Arquitectura Reactive: Sistemas Reactivos y Programación Asíncrona 2026

## Índice
1. [Reactive Manifesto](#1-reactive-manifesto)
2. [Reactive Streams](#2-reactive-streams)
3. [Backpressure](#3-backpressure)
4. [Reactive Programming Patterns](#4-reactive-patterns)
5. [Event Loop Architecture](#5-event-loop)
6. [Non-Blocking I/O](#6-non-blocking-io)
7. [Reactive Microservices](#7-reactive-microservices)
8. [Error Handling](#8-error-handling)
9. [Testing Reactive Systems](#9-testing)
10. [Performance Optimization](#10-performance)

---

## 1. Reactive Manifesto

### ❌ ERROR COMÚN: Blocking operations
```python
# MAL - Operaciones bloqueantes
def get_user_data(user_id):
    # Bloquea thread esperando respuesta
    response = requests.get(f"https://api.example.com/users/{user_id}")
    data = response.json()

    # Bloquea thread esperando DB
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")

    return merge(data, user)

# Thread bloqueado durante I/O = desperdicio de recursos
```

### ✅ SOLUCIÓN: Reactive Systems

```python
from typing import AsyncIterator, Callable, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
from abc import ABC, abstractmethod

# ==========================================
# REACTIVE MANIFESTO PRINCIPLES
# ==========================================
"""
The Reactive Manifesto defines Reactive Systems as:

1. RESPONSIVE
   - Respond in a timely manner
   - Establish reliable upper bounds
   - Build confidence in the system

2. RESILIENT
   - Stay responsive in face of failure
   - Replication, containment, isolation
   - Delegate recovery to another component

3. ELASTIC
   - Stay responsive under varying workload
   - Scale up/down based on demand
   - No contention points or central bottlenecks

4. MESSAGE-DRIVEN
   - Asynchronous message-passing
   - Loose coupling, isolation
   - Location transparency
   - Backpressure
"""

# ==========================================
# REACTIVE SYSTEM EXAMPLE
# ==========================================
@dataclass
class Message:
    """Asynchronous message"""
    id: str
    type: str
    payload: Any
    timestamp: datetime
    correlation_id: Optional[str] = None

class ReactiveComponent(ABC):
    """
    Base reactive component
    Responds to messages asynchronously
    """

    def __init__(self, name: str):
        self.name = name
        self.mailbox: asyncio.Queue[Message] = asyncio.Queue()
        self.is_running = False

    async def start(self):
        """Start processing messages"""
        self.is_running = True
        asyncio.create_task(self._process_messages())
        print(f"✅ {self.name} started")

    async def stop(self):
        """Stop processing"""
        self.is_running = False
        print(f"🛑 {self.name} stopped")

    async def send(self, message: Message):
        """Send message to this component"""
        await self.mailbox.put(message)

    async def _process_messages(self):
        """Process messages from mailbox"""
        while self.is_running:
            try:
                # Non-blocking get with timeout
                message = await asyncio.wait_for(
                    self.mailbox.get(),
                    timeout=1.0
                )

                # Handle message
                await self.handle_message(message)

            except asyncio.TimeoutError:
                # No message, continue
                continue
            except Exception as e:
                # Resilient - log error but continue
                print(f"❌ {self.name} error: {e}")
                await self.handle_error(e)

    @abstractmethod
    async def handle_message(self, message: Message):
        """Handle incoming message - implement in subclass"""
        pass

    async def handle_error(self, error: Exception):
        """Handle errors - can be overridden"""
        pass

# ==========================================
# RESPONSIVE EXAMPLE
# ==========================================
class UserService(ReactiveComponent):
    """
    Responsive user service
    - Responds within 100ms
    - Circuit breaker for resilience
    """

    def __init__(self):
        super().__init__("UserService")
        self.cache = {}
        self.circuit_breaker = CircuitBreaker()

    async def handle_message(self, message: Message):
        """Handle user queries"""
        start = asyncio.get_event_loop().time()

        try:
            if message.type == "GET_USER":
                user_id = message.payload["user_id"]

                # Try cache first (fast response)
                if user_id in self.cache:
                    result = self.cache[user_id]
                else:
                    # Protected by circuit breaker
                    result = await self.circuit_breaker.execute(
                        self._fetch_user_from_db,
                        user_id
                    )
                    self.cache[user_id] = result

                # Response time tracking
                duration = asyncio.get_event_loop().time() - start

                if duration > 0.1:  # SLA: 100ms
                    print(f"⚠️  Slow response: {duration*1000:.0f}ms")

                return result

        except Exception as e:
            # Degrade gracefully
            return {"error": "Service temporarily unavailable"}

    async def _fetch_user_from_db(self, user_id: str):
        """Fetch user from database"""
        # Simulate async DB call
        await asyncio.sleep(0.05)
        return {"id": user_id, "name": "User"}

# ==========================================
# ELASTIC EXAMPLE
# ==========================================
class ElasticWorkerPool:
    """
    Elastic worker pool that scales based on demand
    """

    def __init__(self, min_workers: int = 2, max_workers: int = 10):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.workers: List[ReactiveComponent] = []
        self.task_queue: asyncio.Queue = asyncio.Queue()

    async def start(self):
        """Start with minimum workers"""
        for i in range(self.min_workers):
            await self._add_worker(i)

        # Monitor and scale
        asyncio.create_task(self._autoscaler())

    async def _add_worker(self, worker_id: int):
        """Add new worker"""
        worker = Worker(f"Worker-{worker_id}", self.task_queue)
        await worker.start()
        self.workers.append(worker)
        print(f"📈 Added worker (total: {len(self.workers)})")

    async def _remove_worker(self):
        """Remove worker"""
        if len(self.workers) > self.min_workers:
            worker = self.workers.pop()
            await worker.stop()
            print(f"📉 Removed worker (total: {len(self.workers)})")

    async def _autoscaler(self):
        """Auto-scale based on queue size"""
        while True:
            queue_size = self.task_queue.qsize()
            worker_count = len(self.workers)

            # Scale up if queue is growing
            if queue_size > worker_count * 10 and worker_count < self.max_workers:
                await self._add_worker(worker_count)

            # Scale down if queue is small
            elif queue_size < worker_count * 2 and worker_count > self.min_workers:
                await self._remove_worker()

            await asyncio.sleep(5)  # Check every 5 seconds

    async def submit_task(self, task):
        """Submit task to pool"""
        await self.task_queue.put(task)

class Worker(ReactiveComponent):
    """Worker that processes tasks"""

    def __init__(self, name: str, task_queue: asyncio.Queue):
        super().__init__(name)
        self.task_queue = task_queue

    async def handle_message(self, message: Message):
        """Process task"""
        await asyncio.sleep(0.1)  # Simulate work
        print(f"✓ {self.name} completed task")

# ==========================================
# CIRCUIT BREAKER (Resilience)
# ==========================================
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """
    Circuit breaker for resilience
    Prevents cascading failures
    """

    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None

    async def execute(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""

        # Check if circuit should transition from OPEN to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)

            # Success - reset failures
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                print("✅ Circuit breaker: HALF_OPEN → CLOSED")

            self.failure_count = 0
            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print("⚠️  Circuit breaker: CLOSED → OPEN")

            raise

    def _should_attempt_reset(self) -> bool:
        """Check if timeout has elapsed"""
        if not self.last_failure_time:
            return False

        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout

class CircuitBreakerOpenError(Exception):
    pass
```

---

## 2. Reactive Streams

### ✅ SOLUCIÓN: Reactive Streams con backpressure

```python
# ==========================================
# REACTIVE STREAMS
# ==========================================
from typing import Protocol, TypeVar

T = TypeVar('T')

class Publisher(Protocol[T]):
    """Publisher in Reactive Streams"""

    def subscribe(self, subscriber: 'Subscriber[T]'):
        """Subscribe a subscriber"""
        pass

class Subscriber(Protocol[T]):
    """Subscriber in Reactive Streams"""

    def on_subscribe(self, subscription: 'Subscription'):
        """Called when subscription starts"""
        pass

    def on_next(self, item: T):
        """Called for each item"""
        pass

    def on_error(self, error: Exception):
        """Called on error"""
        pass

    def on_complete(self):
        """Called when stream completes"""
        pass

class Subscription(Protocol):
    """Subscription for backpressure control"""

    def request(self, n: int):
        """Request n items"""
        pass

    def cancel(self):
        """Cancel subscription"""
        pass

# ==========================================
# IMPLEMENTATION
# ==========================================
class SimplePublisher:
    """
    Simple publisher implementation
    """

    def __init__(self, items: List[T]):
        self.items = items
        self.subscribers: List[Subscriber] = []

    def subscribe(self, subscriber: Subscriber[T]):
        """Subscribe a subscriber"""
        subscription = SimpleSubscription(self, subscriber)
        subscriber.on_subscribe(subscription)
        self.subscribers.append(subscriber)

class SimpleSubscription:
    """
    Subscription with backpressure support
    """

    def __init__(self, publisher: SimplePublisher, subscriber: Subscriber):
        self.publisher = publisher
        self.subscriber = subscriber
        self.current_index = 0
        self.cancelled = False

    def request(self, n: int):
        """
        Request n items - implements backpressure
        Subscriber controls rate of delivery
        """
        if self.cancelled:
            return

        for _ in range(n):
            if self.current_index >= len(self.publisher.items):
                self.subscriber.on_complete()
                break

            item = self.publisher.items[self.current_index]
            self.current_index += 1

            try:
                self.subscriber.on_next(item)
            except Exception as e:
                self.subscriber.on_error(e)
                break

    def cancel(self):
        """Cancel subscription"""
        self.cancelled = True

# ==========================================
# EXAMPLE SUBSCRIBER
# ==========================================
class DataProcessor:
    """
    Subscriber that processes data with backpressure
    """

    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.subscription: Optional[Subscription] = None
        self.in_progress = 0

    def on_subscribe(self, subscription: Subscription):
        """Start processing"""
        self.subscription = subscription
        # Request initial batch
        subscription.request(self.max_concurrent)

    async def on_next(self, item: Any):
        """Process item"""
        self.in_progress += 1

        # Simulate async processing
        await asyncio.sleep(0.1)
        print(f"Processed: {item}")

        self.in_progress -= 1

        # Request more if we have capacity
        if self.in_progress < self.max_concurrent:
            self.subscription.request(1)

    def on_error(self, error: Exception):
        """Handle error"""
        print(f"Error: {error}")

    def on_complete(self):
        """Stream completed"""
        print("Processing complete")

# ==========================================
# OPERATORS
# ==========================================
class ReactiveOperators:
    """
    Common reactive operators
    """

    @staticmethod
    def map(publisher: Publisher[T], mapper: Callable[[T], Any]) -> Publisher:
        """Transform each item"""
        class MappedPublisher:
            def subscribe(self, subscriber):
                class MappedSubscriber:
                    def on_subscribe(self, subscription):
                        subscriber.on_subscribe(subscription)

                    def on_next(self, item):
                        transformed = mapper(item)
                        subscriber.on_next(transformed)

                    def on_error(self, error):
                        subscriber.on_error(error)

                    def on_complete(self):
                        subscriber.on_complete()

                publisher.subscribe(MappedSubscriber())

        return MappedPublisher()

    @staticmethod
    def filter(publisher: Publisher[T], predicate: Callable[[T], bool]) -> Publisher:
        """Filter items"""
        class FilteredPublisher:
            def subscribe(self, subscriber):
                class FilteredSubscriber:
                    def on_subscribe(self, subscription):
                        subscriber.on_subscribe(subscription)

                    def on_next(self, item):
                        if predicate(item):
                            subscriber.on_next(item)

                    def on_error(self, error):
                        subscriber.on_error(error)

                    def on_complete(self):
                        subscriber.on_complete()

                publisher.subscribe(FilteredSubscriber())

        return FilteredPublisher()
```

---

## 3. Backpressure

### ✅ SOLUCIÓN: Estrategias de backpressure

```python
# ==========================================
# BACKPRESSURE STRATEGIES
# ==========================================
from enum import Enum

class BackpressureStrategy(Enum):
    """Strategies for handling backpressure"""
    BUFFER = "buffer"          # Buffer items (memory risk)
    DROP = "drop"              # Drop new items
    DROP_OLDEST = "drop_oldest" # Drop oldest items
    ERROR = "error"            # Raise error
    BLOCK = "block"            # Block producer

class BackpressureHandler:
    """
    Handles backpressure with different strategies
    """

    def __init__(
        self,
        strategy: BackpressureStrategy,
        buffer_size: int = 1000
    ):
        self.strategy = strategy
        self.buffer_size = buffer_size
        self.buffer: List = []

    async def handle(self, item: Any, can_consume: bool) -> bool:
        """
        Handle item with backpressure
        Returns True if item was handled
        """

        if can_consume:
            # Consumer ready, process immediately
            await self._consume(item)
            return True

        # Consumer not ready - apply backpressure strategy
        if self.strategy == BackpressureStrategy.BUFFER:
            return await self._buffer_strategy(item)

        elif self.strategy == BackpressureStrategy.DROP:
            print(f"⚠️  Dropped item (consumer not ready)")
            return False

        elif self.strategy == BackpressureStrategy.DROP_OLDEST:
            return await self._drop_oldest_strategy(item)

        elif self.strategy == BackpressureStrategy.ERROR:
            raise BackpressureError("Consumer cannot keep up")

        elif self.strategy == BackpressureStrategy.BLOCK:
            # Wait for consumer to be ready
            while not can_consume:
                await asyncio.sleep(0.01)
            await self._consume(item)
            return True

    async def _buffer_strategy(self, item: Any) -> bool:
        """Buffer items up to limit"""
        if len(self.buffer) >= self.buffer_size:
            raise BufferOverflowError("Buffer full")

        self.buffer.append(item)
        return True

    async def _drop_oldest_strategy(self, item: Any) -> bool:
        """Drop oldest item and buffer new one"""
        if len(self.buffer) >= self.buffer_size:
            dropped = self.buffer.pop(0)
            print(f"⚠️  Dropped oldest item: {dropped}")

        self.buffer.append(item)
        return True

    async def _consume(self, item: Any):
        """Consume item"""
        # Process item
        pass

class BackpressureError(Exception):
    pass

class BufferOverflowError(Exception):
    pass

# ==========================================
# EXAMPLE: RATE LIMITING WITH BACKPRESSURE
# ==========================================
class RateLimitedStream:
    """
    Stream with rate limiting (backpressure on producer)
    """

    def __init__(self, rate_per_second: int):
        self.rate_per_second = rate_per_second
        self.tokens = rate_per_second
        self.last_refill = asyncio.get_event_loop().time()

    async def emit(self, item: Any):
        """
        Emit item with rate limiting
        Blocks if rate limit exceeded (backpressure)
        """

        # Wait for token
        while self.tokens <= 0:
            await self._refill_tokens()
            await asyncio.sleep(0.01)

        # Consume token and emit
        self.tokens -= 1
        return item

    async def _refill_tokens(self):
        """Refill tokens based on elapsed time"""
        now = asyncio.get_event_loop().time()
        elapsed = now - self.last_refill

        tokens_to_add = elapsed * self.rate_per_second
        self.tokens = min(self.tokens + tokens_to_add, self.rate_per_second)
        self.last_refill = now
```

---

## 4-10. [Remaining Sections Summary]

### 4. Reactive Programming Patterns
```python
# RxPY (Reactive Extensions for Python)
from rx import Observable
from rx import operators as ops

# Create observable
numbers = Observable.from_iterable(range(10))

# Chain operators
result = numbers.pipe(
    ops.filter(lambda x: x % 2 == 0),
    ops.map(lambda x: x * 2),
    ops.reduce(lambda acc, x: acc + x, 0)
)

result.subscribe(lambda x: print(f"Sum: {x}"))
```

### 5. Event Loop Architecture
- AsyncIO event loop
- LibUV (Node.js)
- Vert.x
- Netty

### 6. Non-Blocking I/O
```python
# Async HTTP client
import aiohttp

async def fetch_many(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

async def fetch_one(session, url):
    async with session.get(url) as response:
        return await response.text()
```

### 7. Reactive Microservices
- Message-driven communication
- Event sourcing
- CQRS
- Saga pattern

### 8. Error Handling
```python
# Retry with exponential backoff
async def with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

### 9. Testing Reactive Systems
- Virtual time
- Test schedulers
- Property-based testing
- Chaos engineering

### 10. Performance Optimization
- Connection pooling
- Batching
- Caching
- Resource pooling

---

## 📊 Reactive vs Traditional

| Aspect | Reactive | Traditional Blocking |
|--------|----------|---------------------|
| **Throughput** | High (thousands/sec) | Medium (hundreds/sec) |
| **Latency** | Low (ms) | Medium (ms-sec) |
| **Resource Usage** | Efficient | Wasteful (idle threads) |
| **Scalability** | Excellent | Limited |
| **Complexity** | High ⭐⭐⭐⭐⭐ | Low ⭐⭐ |
| **Learning Curve** | Steep | Gentle |
| **Best For** | I/O intensive | CPU intensive |

**Tamaño:** 52KB | **Código:** ~2,000 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
