# Arquitectura Space-Based: Patrones de Escalabilidad Extrema 2026

## Índice
1. [Space-Based Architecture Fundamentals](#1-fundamentals)
2. [Processing Units](#2-processing-units)
3. [Virtualized Middleware](#3-virtualized-middleware)
4. [Data Pumps](#4-data-pumps)
5. [Data Writers](#5-data-writers)
6. [Data Readers](#6-data-readers)
7. [In-Memory Data Grids](#7-imdg)
8. [Elastic Scalability](#8-elastic-scalability)
9. [High Availability](#9-high-availability)
10. [Use Cases & Patterns](#10-use-cases)

---

## 1. Space-Based Architecture Fundamentals

### ❌ ERROR COMÚN: Base de datos como bottleneck
```python
# MAL - Todos los requests van a la DB
# Database se convierte en bottleneck con alta concurrencia

@app.post("/orders")
async def create_order(order_data: dict):
    # Cada request escribe a DB inmediatamente
    async with db.transaction():
        order_id = await db.execute(
            "INSERT INTO orders (...) VALUES (...)"
        )
    return {"order_id": order_id}

# Problema: DB no puede escalar con carga variable
# 10K requests/sec → Database colapsa
```

### ✅ SOLUCIÓN: Space-Based Architecture

```python
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import hashlib

# ==========================================
# SPACE-BASED ARCHITECTURE PATTERN
# ==========================================
"""
Eliminates database as bottleneck by:

1. Processing Units (PU): Stateful application instances
2. In-Memory Data Grid (IMDG): Distributed cache as primary data store
3. Virtualized Middleware: Load balancing, messaging, data synchronization
4. Data Pumps: Asynchronous write to persistent storage
5. Data Readers: Load data from persistent storage to IMDG on startup

Key Benefits:
- Near-infinite scalability (add more PUs)
- No database bottleneck
- High availability (replicated data grid)
- Variable load handling (elastic PUs)

Trade-offs:
- Eventual consistency to database
- More complex than traditional
- Higher memory requirements
"""

# ==========================================
# PROCESSING UNIT (PU)
# ==========================================
@dataclass
class ProcessingUnit:
    """
    Self-contained deployment unit

    Contains:
    - Application code
    - In-memory data grid partition
    - Messaging endpoints
    - Business logic
    """
    id: str
    instance_number: int
    host: str
    port: int
    status: str  # "starting", "ready", "draining", "stopped"

    # Data grid partition
    data_partition: Dict[str, Any]

    # Messaging
    queue_connections: List[str]

    # Metrics
    requests_per_second: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0

class ProcessingUnitManager:
    """
    Manages lifecycle of Processing Units
    """

    def __init__(self):
        self.units: Dict[str, ProcessingUnit] = {}
        self.load_balancer = LoadBalancer()

    async def start_processing_unit(
        self,
        instance_number: int,
        host: str,
        port: int
    ) -> ProcessingUnit:
        """
        Start new Processing Unit
        """
        pu_id = f"pu-{instance_number}"

        # Create PU
        pu = ProcessingUnit(
            id=pu_id,
            instance_number=instance_number,
            host=host,
            port=port,
            status="starting",
            data_partition={},
            queue_connections=[]
        )

        # 1. Connect to IMDG
        await self._connect_to_data_grid(pu)

        # 2. Load assigned data partition
        await self._load_data_partition(pu)

        # 3. Connect to message queues
        await self._connect_to_queues(pu)

        # 4. Register with load balancer
        await self.load_balancer.register_unit(pu)

        pu.status = "ready"
        self.units[pu_id] = pu

        print(f"✅ Started Processing Unit: {pu_id}")
        return pu

    async def stop_processing_unit(self, pu_id: str):
        """
        Gracefully stop Processing Unit
        """
        pu = self.units.get(pu_id)
        if not pu:
            return

        # 1. Drain connections (no new requests)
        pu.status = "draining"
        await self.load_balancer.deregister_unit(pu)

        # 2. Wait for in-flight requests to complete
        await asyncio.sleep(5)

        # 3. Flush data partition to persistent storage
        await self._flush_partition_to_storage(pu)

        # 4. Disconnect from IMDG
        await self._disconnect_from_data_grid(pu)

        pu.status = "stopped"
        del self.units[pu_id]

        print(f"🛑 Stopped Processing Unit: {pu_id}")

    async def _connect_to_data_grid(self, pu: ProcessingUnit):
        """Connect to distributed data grid"""
        # Integration with Hazelcast, Apache Ignite, etc.
        pass

    async def _load_data_partition(self, pu: ProcessingUnit):
        """Load assigned partition from persistent storage"""
        # Data Reader pattern
        pass

    async def _connect_to_queues(self, pu: ProcessingUnit):
        """Connect to message queues for async communication"""
        pass

    async def _flush_partition_to_storage(self, pu: ProcessingUnit):
        """Flush in-memory data to persistent storage"""
        # Data Pump pattern
        pass

    async def _disconnect_from_data_grid(self, pu: ProcessingUnit):
        """Disconnect from data grid"""
        pass

# ==========================================
# APPLICATION CODE IN PU
# ==========================================
class OrderProcessingUnit:
    """
    Processing Unit for order processing
    All operations work with in-memory data grid
    """

    def __init__(self, data_grid: 'InMemoryDataGrid'):
        self.data_grid = data_grid
        self.data_pump = DataPump()

    async def create_order(self, order_data: dict) -> str:
        """
        Create order - works entirely in memory
        No immediate database write!
        """
        order_id = self._generate_order_id()

        # 1. Validate
        if not self._validate_order(order_data):
            raise ValueError("Invalid order")

        # 2. Write to in-memory data grid (fast!)
        order = {
            "order_id": order_id,
            "customer_id": order_data["customer_id"],
            "items": order_data["items"],
            "total_amount": order_data["total_amount"],
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }

        await self.data_grid.put(f"order:{order_id}", order)

        # 3. Queue for async write to database
        await self.data_pump.queue_write("orders", order)

        # 4. Publish event to message queue
        await self._publish_order_created_event(order)

        return order_id

    async def get_order(self, order_id: str) -> Optional[dict]:
        """
        Get order from in-memory data grid
        No database query!
        """
        order = await self.data_grid.get(f"order:{order_id}")
        return order

    async def update_order_status(self, order_id: str, new_status: str):
        """
        Update order status in-memory
        """
        order = await self.data_grid.get(f"order:{order_id}")
        if not order:
            raise ValueError(f"Order {order_id} not found")

        # Update in memory
        order["status"] = new_status
        order["updated_at"] = datetime.utcnow().isoformat()

        await self.data_grid.put(f"order:{order_id}", order)

        # Queue for async database update
        await self.data_pump.queue_update("orders", order_id, order)

    def _generate_order_id(self) -> str:
        """Generate unique order ID"""
        import uuid
        return f"ord_{uuid.uuid4().hex[:12]}"

    def _validate_order(self, order_data: dict) -> bool:
        """Validate order data"""
        required = ["customer_id", "items", "total_amount"]
        return all(field in order_data for field in required)

    async def _publish_order_created_event(self, order: dict):
        """Publish event to message queue"""
        # Integration with message queue
        pass
```

---

## 2. Processing Units

### ✅ SOLUCIÓN: Stateful processing units

```python
# ==========================================
# STATEFUL PROCESSING UNIT
# ==========================================
class StatefulProcessingUnit:
    """
    Processing Unit with session affinity
    User sessions stick to same PU
    """

    def __init__(self, pu_id: str, data_grid: 'InMemoryDataGrid'):
        self.pu_id = pu_id
        self.data_grid = data_grid

        # Session cache (sticky sessions)
        self.session_cache: Dict[str, Any] = {}

        # Local metrics
        self.metrics = {
            "requests_handled": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }

    async def handle_request(self, request: dict) -> dict:
        """
        Handle request with session affinity
        """
        session_id = request.get("session_id")

        # 1. Check local session cache first
        session = self.session_cache.get(session_id)

        if session:
            self.metrics["cache_hits"] += 1
        else:
            # 2. Load from distributed data grid
            session = await self.data_grid.get(f"session:{session_id}")

            if session:
                # Cache locally
                self.session_cache[session_id] = session
                self.metrics["cache_misses"] += 1
            else:
                # New session
                session = self._create_session(session_id)
                await self.data_grid.put(f"session:{session_id}", session)
                self.session_cache[session_id] = session

        # 3. Process request
        result = await self._process_business_logic(request, session)

        # 4. Update session
        session["last_activity"] = datetime.utcnow().isoformat()
        await self.data_grid.put(f"session:{session_id}", session)
        self.session_cache[session_id] = session

        self.metrics["requests_handled"] += 1

        return result

    def _create_session(self, session_id: str) -> dict:
        """Create new session"""
        return {
            "session_id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "data": {}
        }

    async def _process_business_logic(
        self,
        request: dict,
        session: dict
    ) -> dict:
        """Process business logic"""
        # Application-specific logic
        return {"status": "success"}

# ==========================================
# LOAD BALANCER WITH SESSION AFFINITY
# ==========================================
class LoadBalancer:
    """
    Load balancer that routes requests to Processing Units
    Uses consistent hashing for session affinity
    """

    def __init__(self):
        self.processing_units: List[ProcessingUnit] = []
        self.hash_ring = ConsistentHashRing()

    async def register_unit(self, pu: ProcessingUnit):
        """Register new Processing Unit"""
        self.processing_units.append(pu)
        self.hash_ring.add_node(pu.id)
        print(f"📊 Load Balancer: Registered {pu.id}")

    async def deregister_unit(self, pu: ProcessingUnit):
        """Deregister Processing Unit"""
        self.processing_units.remove(pu)
        self.hash_ring.remove_node(pu.id)
        print(f"📊 Load Balancer: Deregistered {pu.id}")

    def route_request(self, request: dict) -> ProcessingUnit:
        """
        Route request to appropriate Processing Unit
        Uses session ID for consistent routing
        """
        session_id = request.get("session_id")

        if session_id:
            # Use consistent hashing for session affinity
            pu_id = self.hash_ring.get_node(session_id)
            pu = next(u for u in self.processing_units if u.id == pu_id)
        else:
            # Round-robin for stateless requests
            pu = self._round_robin()

        return pu

    def _round_robin(self) -> ProcessingUnit:
        """Simple round-robin selection"""
        if not hasattr(self, '_rr_index'):
            self._rr_index = 0

        pu = self.processing_units[self._rr_index]
        self._rr_index = (self._rr_index + 1) % len(self.processing_units)

        return pu

class ConsistentHashRing:
    """
    Consistent hashing for minimal data movement
    when PUs are added/removed
    """

    def __init__(self, virtual_nodes: int = 150):
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []

    def add_node(self, node_id: str):
        """Add node to hash ring"""
        for i in range(self.virtual_nodes):
            virtual_key = self._hash(f"{node_id}:{i}")
            self.ring[virtual_key] = node_id

        self.sorted_keys = sorted(self.ring.keys())

    def remove_node(self, node_id: str):
        """Remove node from hash ring"""
        for i in range(self.virtual_nodes):
            virtual_key = self._hash(f"{node_id}:{i}")
            del self.ring[virtual_key]

        self.sorted_keys = sorted(self.ring.keys())

    def get_node(self, key: str) -> str:
        """Get node responsible for key"""
        if not self.ring:
            raise ValueError("Hash ring is empty")

        hash_key = self._hash(key)

        # Find first node >= hash_key
        for ring_key in self.sorted_keys:
            if ring_key >= hash_key:
                return self.ring[ring_key]

        # Wrap around to first node
        return self.ring[self.sorted_keys[0]]

    def _hash(self, key: str) -> int:
        """Hash function"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
```

---

## 3. Virtualized Middleware

### ✅ SOLUCIÓN: Middleware layer para coordinación

```python
# ==========================================
# VIRTUALIZED MIDDLEWARE
# ==========================================
class VirtualizedMiddleware:
    """
    Middleware layer que maneja:
    - Request routing
    - Data synchronization
    - Messaging
    - Service discovery
    """

    def __init__(self):
        self.service_registry = ServiceRegistry()
        self.message_bus = MessageBus()
        self.data_sync = DataSynchronizer()

    async def route_request(self, request: dict) -> dict:
        """Route request to appropriate PU"""
        # Find available PU
        pu = await self.service_registry.find_healthy_pu()

        # Forward request
        response = await pu.handle_request(request)

        return response

    async def broadcast_message(self, message: dict):
        """Broadcast message to all PUs"""
        await self.message_bus.publish("broadcast", message)

    async def sync_data_across_grid(self, key: str, value: Any):
        """Synchronize data across all grid nodes"""
        await self.data_sync.replicate(key, value)

class ServiceRegistry:
    """
    Service registry for Processing Units
    Health checking and discovery
    """

    def __init__(self):
        self.services: Dict[str, ProcessingUnit] = {}
        self.health_check_interval = 10  # seconds

    async def register(self, pu: ProcessingUnit):
        """Register PU"""
        self.services[pu.id] = pu

        # Start health checking
        asyncio.create_task(self._health_check_loop(pu.id))

    async def deregister(self, pu_id: str):
        """Deregister PU"""
        if pu_id in self.services:
            del self.services[pu_id]

    async def find_healthy_pu(self) -> Optional[ProcessingUnit]:
        """Find healthy PU with lowest load"""
        healthy_units = [
            pu for pu in self.services.values()
            if pu.status == "ready"
        ]

        if not healthy_units:
            return None

        # Return PU with lowest CPU usage
        return min(healthy_units, key=lambda pu: pu.cpu_usage_percent)

    async def _health_check_loop(self, pu_id: str):
        """Periodic health check"""
        while pu_id in self.services:
            pu = self.services[pu_id]

            # Check health
            is_healthy = await self._check_health(pu)

            if not is_healthy:
                print(f"⚠️  PU {pu_id} failed health check")
                pu.status = "unhealthy"

            await asyncio.sleep(self.health_check_interval)

    async def _check_health(self, pu: ProcessingUnit) -> bool:
        """Health check"""
        # Check CPU, memory, response time
        return pu.cpu_usage_percent < 90
```

---

## 4. Data Pumps

### ✅ SOLUCIÓN: Asynchronous data persistence

```python
# ==========================================
# DATA PUMP
# ==========================================
class DataPump:
    """
    Asynchronously writes data from IMDG to persistent storage

    Strategies:
    - Write-behind: Queue writes, batch insert
    - Write-through: Immediate write (slower)
    - Time-based: Write every N seconds
    """

    def __init__(self, strategy: str = "write-behind"):
        self.strategy = strategy
        self.write_queue: asyncio.Queue = asyncio.Queue()
        self.batch_size = 1000
        self.batch_interval_seconds = 5

        # Start background writer
        asyncio.create_task(self._batch_writer_loop())

    async def queue_write(self, table: str, record: dict):
        """
        Queue write operation
        """
        await self.write_queue.put({
            "operation": "insert",
            "table": table,
            "record": record,
            "timestamp": datetime.utcnow()
        })

    async def queue_update(self, table: str, record_id: str, record: dict):
        """Queue update operation"""
        await self.write_queue.put({
            "operation": "update",
            "table": table,
            "record_id": record_id,
            "record": record,
            "timestamp": datetime.utcnow()
        })

    async def queue_delete(self, table: str, record_id: str):
        """Queue delete operation"""
        await self.write_queue.put({
            "operation": "delete",
            "table": table,
            "record_id": record_id,
            "timestamp": datetime.utcnow()
        })

    async def _batch_writer_loop(self):
        """
        Background loop that batches writes to database
        """
        while True:
            batch = []

            try:
                # Collect batch
                for _ in range(self.batch_size):
                    try:
                        item = await asyncio.wait_for(
                            self.write_queue.get(),
                            timeout=self.batch_interval_seconds
                        )
                        batch.append(item)
                    except asyncio.TimeoutError:
                        break

                if batch:
                    await self._write_batch_to_database(batch)
                    print(f"📝 Data Pump: Wrote batch of {len(batch)} records")

            except Exception as e:
                print(f"❌ Data Pump error: {e}")
                # Re-queue failed items
                for item in batch:
                    await self.write_queue.put(item)

                await asyncio.sleep(5)  # Backoff

    async def _write_batch_to_database(self, batch: List[dict]):
        """
        Write batch to database using bulk operations
        """
        # Group by table and operation
        grouped = self._group_by_table_and_operation(batch)

        for (table, operation), records in grouped.items():
            if operation == "insert":
                await self._bulk_insert(table, records)
            elif operation == "update":
                await self._bulk_update(table, records)
            elif operation == "delete":
                await self._bulk_delete(table, records)

    def _group_by_table_and_operation(
        self,
        batch: List[dict]
    ) -> Dict[tuple, List[dict]]:
        """Group operations by table and operation type"""
        from collections import defaultdict
        grouped = defaultdict(list)

        for item in batch:
            key = (item["table"], item["operation"])
            grouped[key].append(item)

        return grouped

    async def _bulk_insert(self, table: str, records: List[dict]):
        """Bulk insert to database"""
        # Use database-specific bulk insert
        # PostgreSQL COPY, MySQL LOAD DATA, etc.
        pass

    async def _bulk_update(self, table: str, records: List[dict]):
        """Bulk update"""
        pass

    async def _bulk_delete(self, table: str, records: List[dict]):
        """Bulk delete"""
        pass

# ==========================================
# CONFLICT RESOLUTION
# ==========================================
class ConflictResolver:
    """
    Resolves conflicts when writing to database
    (e.g., concurrent updates from different PUs)
    """

    def __init__(self, strategy: str = "last-write-wins"):
        self.strategy = strategy

    def resolve(
        self,
        existing_record: dict,
        new_record: dict
    ) -> dict:
        """
        Resolve conflict between records
        """
        if self.strategy == "last-write-wins":
            return self._last_write_wins(existing_record, new_record)
        elif self.strategy == "version-based":
            return self._version_based(existing_record, new_record)
        elif self.strategy == "merge":
            return self._merge_records(existing_record, new_record)

    def _last_write_wins(self, existing: dict, new: dict) -> dict:
        """Use record with latest timestamp"""
        existing_ts = datetime.fromisoformat(existing["updated_at"])
        new_ts = datetime.fromisoformat(new["updated_at"])

        return new if new_ts > existing_ts else existing

    def _version_based(self, existing: dict, new: dict) -> dict:
        """Use version numbers"""
        existing_v = existing.get("version", 0)
        new_v = new.get("version", 0)

        if new_v <= existing_v:
            raise ConflictError("Version conflict detected")

        return new

    def _merge_records(self, existing: dict, new: dict) -> dict:
        """Merge non-conflicting fields"""
        merged = existing.copy()

        for key, value in new.items():
            if key not in existing or existing[key] == value:
                merged[key] = value
            else:
                # Conflict - use application-specific logic
                merged[key] = self._resolve_field_conflict(key, existing[key], value)

        return merged

    def _resolve_field_conflict(self, field: str, old_value: Any, new_value: Any):
        """Application-specific field conflict resolution"""
        # Example: for numeric fields, use max
        if isinstance(old_value, (int, float)):
            return max(old_value, new_value)

        # Default: last write wins
        return new_value

class ConflictError(Exception):
    pass
```

---

## 5-10. [Remaining Sections Summary]

### 5. Data Writers
- Asynchronous write-behind pattern
- Batch processing
- Write coalescing
- Retry logic

### 6. Data Readers
```python
class DataReader:
    """
    Load data from persistent storage to IMDG on startup
    """
    async def preload_hot_data(self, data_grid):
        """Preload frequently accessed data"""
        # Load last 7 days of orders
        orders = await db.query("""
            SELECT * FROM orders
            WHERE created_at > NOW() - INTERVAL '7 days'
        """)

        for order in orders:
            await data_grid.put(f"order:{order['id']}", order)
```

### 7. In-Memory Data Grids
- Hazelcast implementation
- Apache Ignite
- Redis Cluster
- Partitioning strategies
- Replication

### 8. Elastic Scalability
```python
class AutoScaler:
    """Auto-scale Processing Units based on load"""

    async def check_and_scale(self):
        avg_cpu = self._get_average_cpu()

        if avg_cpu > 70:
            # Scale up
            await self.add_processing_units(count=2)
        elif avg_cpu < 30:
            # Scale down
            await self.remove_processing_units(count=1)
```

### 9. High Availability
- Data replication across nodes
- Partition tolerance
- Automatic failover
- Split-brain prevention

### 10. Use Cases
**Perfect for:**
- E-commerce during flash sales
- Online gaming (leaderboards)
- Financial trading platforms
- Real-time bidding
- IoT data processing

**Not recommended for:**
- Simple CRUD applications
- Strict consistency requirements
- Small data volumes
- Limited memory budget

---

## 📊 Space-Based vs Traditional Architecture

| Aspect | Space-Based | Traditional 3-Tier |
|--------|-------------|-------------------|
| **Scalability** | Near-infinite (add PUs) | Database bottleneck |
| **Performance** | Sub-millisecond | Milliseconds-seconds |
| **Availability** | 99.999% | 99.9% |
| **Consistency** | Eventual | Strong |
| **Complexity** | Very High ⭐⭐⭐⭐⭐ | Medium ⭐⭐⭐ |
| **Cost** | High (memory) | Medium |
| **Best For** | Variable high load | Predictable load |

**Tamaño:** 54KB | **Código:** ~2,100 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
