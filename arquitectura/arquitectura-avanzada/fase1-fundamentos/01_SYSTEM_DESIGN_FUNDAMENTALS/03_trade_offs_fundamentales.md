# Trade-offs Fundamentales en System Design
## La Habilidad de Tomar Decisiones Arquitectónicas Difíciles

**Autor:** Staff Software Architect
**Versión:** 1.0
**Fecha:** 2024-12-03
**Tiempo de lectura:** 75 minutos
**Nivel:** Avanzado

---

## 📋 ÍNDICE

1. [Introducción: Todo es Trade-off](#introduccion)
2. [CAP Theorem](#cap-theorem)
3. [Consistency vs Availability](#consistency-availability)
4. [Latency vs Throughput](#latency-throughput)
5. [Read-Heavy vs Write-Heavy](#read-write)
6. [Sync vs Async](#sync-async)
7. [Push vs Pull](#push-pull)
8. [Normalization vs Denormalization](#normalization)
9. [SQL vs NoSQL](#sql-nosql)
10. [Cost vs Performance](#cost-performance)
11. [Complexity vs Maintainability](#complexity)
12. [Matriz de Decisiones](#matriz-decisiones)

---

## 1. INTRODUCCIÓN: TODO ES TRADE-OFF {#introduccion}

### La Verdad Incómoda

> **No existe la arquitectura perfecta. Solo existen trade-offs.**

En system design, cada decisión tiene consecuencias:
- ✅ Optimizas para A
- ❌ Sacrificas B

### Por Qué Importa

**En entrevistas:**
```
Entrevistador: "¿Por qué elegiste Cassandra?"

Candidato A: "Porque es buena para escalabilidad"
→ ❌ Superficial

Candidato B: "Elegí Cassandra porque priorizo availability y partition tolerance sobre consistency. Para Twitter, es aceptable que un timeline tenga eventual consistency de ~1 segundo, pero NO es aceptable que el sistema esté caído. Trade-off: usuarios pueden no ver un tweet inmediatamente, pero el servicio siempre está disponible."
→ ✅ Profundo, muestra madurez
```

**En trabajo real:**
- Decisiones arquitectónicas costan millones
- Wrong trade-off = Technical debt
- Entender trade-offs = Credibilidad como arquitecto

### Estructura de Este Documento

Cada trade-off se explica con:
1. **Definición:** Qué es
2. **Escenarios:** Cuándo usar cada opción
3. **Ejemplos reales:** Empresas que lo usan
4. **Código:** Implementación concreta
5. **Matriz de decisión:** Framework para elegir

---

## 2. CAP THEOREM {#cap-theorem}

### Definición

**CAP Theorem** (Eric Brewer, 2000):
En un sistema distribuido, solo puedes garantizar **2 de 3** propiedades:

```
C - Consistency
A - Availability
P - Partition Tolerance
```

### Las 3 Propiedades

**Consistency (C):**
```
Todos los nodos ven los mismos datos al mismo tiempo.
Read siempre retorna el write más reciente.
```

**Availability (A):**
```
Cada request recibe respuesta (success o failure).
Sistema siempre está up, nunca rechaza requests.
```

**Partition Tolerance (P):**
```
Sistema continúa operando a pesar de particiones de red.
Si algunos nodos no pueden comunicarse, sistema sigue funcionando.
```

### Combinaciones Posibles

En realidad solo hay **2 opciones** (P es mandatorio en sistemas distribuidos):

```
┌─────────────────────────────────────┐
│ CP: Consistency + Partition Tolerance│
│ → Sacrifica Availability             │
│ Ejemplo: MongoDB, HBase               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ AP: Availability + Partition Tolerance│
│ → Sacrifica Consistency              │
│ Ejemplo: Cassandra, DynamoDB          │
└─────────────────────────────────────┘
```

### Escenario Concreto: Network Partition

```
Situación: Datacenter split (Network partition)

          ┌─────┐      ╳╳╳╳╳╳      ┌─────┐
          │ DC1 │      PARTITION    │ DC2 │
          │Node1│                   │Node2│
          └─────┘                   └─────┘

Write request llega a Node1: "Set X = 5"
```

**Opción CP (Consistency + Partition Tolerance):**
```python
# MongoDB approach (CP)

def write(key, value):
    try:
        # Intenta escribir en quorum (mayoría de nodos)
        replicas = [node1, node2, node3]
        acks = 0

        for node in replicas:
            if node.write(key, value):
                acks += 1

        if acks >= 2:  # Quorum (2 de 3)
            return "SUCCESS"
        else:
            # No hay quorum → RECHAZA write
            raise UnavailableError("Cannot reach quorum")

    except NetworkPartitionError:
        # Durante partition → Sistema se vuelve UNAVAILABLE
        raise UnavailableError("System unavailable during partition")

# Trade-off:
# ✅ Pro: Consistency garantizada
# ❌ Con: Sistema puede estar down durante partitions
```

**Opción AP (Availability + Partition Tolerance):**
```python
# Cassandra approach (AP)

def write(key, value):
    try:
        # Acepta write aunque no llegue a todos los nodos
        local_node.write(key, value)  # Write local siempre succeed

        # Intenta propagar a otros nodos (background)
        asyncio.create_task(replicate_to_replicas(key, value))

        return "SUCCESS"  # Siempre retorna success

    except Exception:
        # Incluso con errores → Acepta write localmente
        return "SUCCESS"

def read(key):
    # Lee de nodo local (puede estar desactualizado)
    return local_node.read(key)

# Trade-off:
# ✅ Pro: Sistema siempre disponible
# ❌ Con: Puede retornar datos desactualizados (eventual consistency)
```

### Ejemplos Reales por Categoría

**CP Systems:**
```
MongoDB (default)
  - Use case: Banking transactions
  - Why: Necesitas strong consistency para balances
  - Trade-off: Durante network partition, sistema unavailable

HBase
  - Use case: Real-time analytics
  - Why: Necesitas reads consistentes para reportes
  - Trade-off: Algunas regions pueden estar unavailable

Zookeeper
  - Use case: Distributed coordination
  - Why: Configuración debe ser consistente
  - Trade-off: Acepta downtime para mantener consistency
```

**AP Systems:**
```
Cassandra
  - Use case: Time-series data, logs
  - Why: Availability > Consistency
  - Trade-off: Eventual consistency (seconds)

DynamoDB
  - Use case: Session storage, shopping carts
  - Why: Cannot afford downtime
  - Trade-off: Puede leer writes antiguos

Riak
  - Use case: User profiles, product catalog
  - Why: High availability critical
  - Trade-off: Conflictos resolved por application
```

### Caso Real: Amazon DynamoDB (AP)

**Decisión:** Priorizar Availability sobre Consistency

**Justificación:**
```
Scenario: Black Friday shopping cart

Option 1 (CP - Strong Consistency):
- User adds item to cart
- System checks all replicas before confirming
- If partition → "Service Unavailable"
Result: Lost sale ❌

Option 2 (AP - Eventual Consistency):
- User adds item to cart
- System confirms immediately (writes locally)
- Replicates in background
- If partition → Cart might have slight delay syncing
Result: Sale completed, happy customer ✅

Trade-off:
- Occasional cart inconsistencies (rare)
- vs. Site downtime during high traffic (catastrophic)

Amazon chose AP: Eventual consistency acceptable, downtime NOT acceptable.
```

### Caso Real: Banking System (CP)

**Decisión:** Priorizar Consistency sobre Availability

**Justificación:**
```
Scenario: Bank account transfer

Option 1 (AP - Availability):
- Transfer $1000 from Account A to B
- Write accepted immediately
- During partition, both datacenters accept writes
Result: Duplicate transfer, balance incorrect ❌ UNACCEPTABLE

Option 2 (CP - Consistency):
- Transfer requires quorum
- During partition → "Service temporarily unavailable, try again"
- User waits 30 seconds
Result: Correct balance guaranteed ✅

Trade-off:
- Brief unavailability (30 seconds)
- vs. Incorrect balance (legal/financial risk)

Banks choose CP: Money correctness > uptime
```

### Matriz de Decisión: CP vs AP

| Factor | Elegir CP | Elegir AP |
|--------|-----------|-----------|
| **Data Type** | Financial, Critical | User-generated, Cacheable |
| **Tolerance to Stale Data** | Zero tolerance | Seconds-minutes OK |
| **Downtime Cost** | Medium-Low | Catastrophic |
| **Read:Write Ratio** | Any | Read-heavy better |
| **Regulatory** | Compliance required | No compliance |
| **Examples** | Banking, Inventory | Social media, Logs |

---

## 3. CONSISTENCY VS AVAILABILITY {#consistency-availability}

### Spectrum de Consistency

```
Strong Consistency ←────────────────────→ Eventual Consistency

Linearizable         Sequential      Causal       Eventual
    ↑                   ↑               ↑            ↑
    │                   │               │            │
Most Expensive    Expensive       Cheaper      Cheapest
Lowest Throughput                         Highest Throughput
```

### Modelos de Consistency

#### 1. Strong Consistency (Linearizable)

**Definición:** Read siempre retorna el valor del write más reciente.

```python
# Implementación con locks distribuidos

class StronglyConsistentStore:
    def __init__(self):
        self.data = {}
        self.lock = DistributedLock()

    def write(self, key, value):
        # Adquirir lock global
        with self.lock.acquire(key):
            # Write a TODOS los replicas (synchronous)
            for replica in replicas:
                replica.write(key, value)

            self.data[key] = value
            return "ACK"

    def read(self, key):
        # Leer del primary o quorum
        return self.data[key]

# Características:
# ✅ Correctness: Siempre correcto
# ❌ Latency: Alto (network round-trips)
# ❌ Availability: Baja (locks bloquean)
# ❌ Throughput: Bajo (serialized writes)

# Use case: Banking transactions
```

#### 2. Sequential Consistency

**Definición:** Todos los nodos ven writes en el mismo orden (pero no necesariamente inmediatamente).

```python
class SequentiallyConsistentStore:
    def __init__(self):
        self.data = {}
        self.version = 0
        self.write_log = []

    def write(self, key, value):
        self.version += 1

        # Log write con version
        write_entry = {
            "key": key,
            "value": value,
            "version": self.version
        }
        self.write_log.append(write_entry)

        # Propagar a replicas (async pero ordenado)
        for replica in replicas:
            replica.apply_write(write_entry)

        return "ACK"

    def read(self, key):
        # Puede leer de cualquier replica
        # Garantiza que verás writes en orden correcto
        return self.data[key]

# Use case: Collaborative editing (Google Docs)
```

#### 3. Causal Consistency

**Definición:** Writes causalmente relacionados se ven en orden correcto.

```python
class CausallyConsistentStore:
    def __init__(self):
        self.data = {}
        self.vector_clock = {}

    def write(self, key, value, dependencies=[]):
        # Increment vector clock
        self.vector_clock[key] = self.vector_clock.get(key, 0) + 1

        write_entry = {
            "key": key,
            "value": value,
            "vector_clock": self.vector_clock.copy(),
            "dependencies": dependencies  # Causally related writes
        }

        # Propagar respetando dependencies
        for replica in replicas:
            replica.apply_write_causal(write_entry)

        return "ACK"

    def read(self, key):
        # Lee considerando causalidad
        return self.data[key]

# Ejemplo: Social media comments
# Comment Reply debe aparecer DESPUÉS del comment original
# Pero likes de diferentes usuarios pueden aparecer en cualquier orden
```

#### 4. Eventual Consistency

**Definición:** Si no hay más writes, eventualmente todos los nodos convergerán.

```python
class EventuallyConsistentStore:
    def __init__(self):
        self.data = {}

    def write(self, key, value):
        # Write local INMEDIATAMENTE
        self.data[key] = value

        # Propagar async (no espera confirmación)
        asyncio.create_task(self.replicate(key, value))

        return "ACK"  # Instant response

    async def replicate(self, key, value):
        # Background replication
        for replica in replicas:
            try:
                await replica.write(key, value)
            except:
                # Retry later (queue)
                retry_queue.add((replica, key, value))

    def read(self, key):
        # Puede leer valor desactualizado
        return self.data.get(key)

# Características:
# ✅ Latency: Muy bajo (no espera replicas)
# ✅ Availability: Alta (siempre acepta writes)
# ✅ Throughput: Muy alto
# ❌ Correctness: Puede leer stale data

# Use case: Twitter timeline, Facebook feed
```

### Comparación con Ejemplos Reales

**Twitter Timeline:**
```
Decisión: Eventual Consistency

Scenario:
- Tweet creado a las 10:00:00
- User A lo ve a las 10:00:01
- User B lo ve a las 10:00:03 (2 segundos después)

Trade-off aceptable:
✅ Sistema siempre disponible (millones de tweets/sec)
✅ Latency ultra-baja
❌ Slight delay en ver tweets (nobody cares about 2 seconds)

Implementation:
- Write tweet to local DC
- Async replication to other DCs
- Cache pre-computed timelines
```

**Stock Trading:**
```
Decisión: Strong Consistency

Scenario:
- Stock price update
- MUST be reflected IMMEDIATELY in all systems
- Cannot have 2 different prices

Trade-off requerido:
❌ Sistema puede estar momentáneamente unavailable
❌ Latency más alta (decenas de ms)
✅ Correctness GARANTIZADA (no arbitrage opportunities)

Implementation:
- Synchronous replication con 2PC
- Quorum writes
- Lock durante update
```

---

## 4. LATENCY VS THROUGHPUT {#latency-throughput}

### Definiciones

**Latency:** Tiempo que toma procesar 1 request
**Throughput:** Cuántos requests puedes procesar por segundo

```
Latency = Time per request
Throughput = Requests per second

Trade-off: Optimizing one often hurts the other
```

### Visualización

```
Latency-Optimized:
────────────────────────────
Request 1: [██] 10ms
Request 2: [██] 10ms
Request 3: [██] 10ms

Latency: 10ms ✅
Throughput: 100 req/sec

Throughput-Optimized (Batching):
────────────────────────────
Request 1-10: [██████████] 50ms

Latency: 50ms per request ❌
Throughput: 200 req/sec ✅
```

### Técnicas para Latency

#### Técnica 1: Caching

```python
import redis
from functools import wraps

cache = redis.Redis()

def cached(ttl=60):
    def decorator(func):
        @wraps(func)
        def wrapper(key):
            # Check cache
            cached_value = cache.get(key)
            if cached_value:
                return cached_value  # ~1ms

            # Cache miss → Compute
            value = func(key)  # ~100ms

            # Store in cache
            cache.setex(key, ttl, value)

            return value
        return wrapper
    return decorator

@cached(ttl=300)
def get_user_profile(user_id):
    # Expensive DB query
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")

# Results:
# First call: 100ms (cache miss)
# Subsequent calls: 1ms (cache hit)
# Latency improved 100x ✅
```

#### Técnica 2: CDN para Media

```
Without CDN:
User (London) → Origin Server (US East) → 150ms round trip

With CDN:
User (London) → CDN Edge (London) → 5ms round trip

Latency reduced 30x ✅
```

#### Técnica 3: Read Replicas Geográficas

```python
class GeoDist distributedDB:
    def __init__(self):
        self.replicas = {
            "us-east": PostgreSQL("us-east-1"),
            "us-west": PostgreSQL("us-west-1"),
            "eu-west": PostgreSQL("eu-west-1"),
            "ap-south": PostgreSQL("ap-south-1"),
        }

    def read(self, key, user_location):
        # Route to closest replica
        replica = self.get_closest_replica(user_location)
        return replica.read(key)  # ~10ms local
        # vs 150ms cross-region

# Latency: Reduced from 150ms to 10ms ✅
# Trade-off: Eventual consistency across regions
```

### Técnicas para Throughput

#### Técnica 1: Batching

```python
class DatabaseBatcher:
    def __init__(self, batch_size=100, flush_interval=0.05):
        self.batch = []
        self.batch_size = batch_size
        self.flush_interval = flush_interval

    def insert(self, record):
        self.batch.append(record)

        if len(self.batch) >= self.batch_size:
            self.flush()

    def flush(self):
        if not self.batch:
            return

        # Batch insert (mucho más eficiente)
        db.execute(
            "INSERT INTO table VALUES " +
            ", ".join([f"({r})" for r in self.batch])
        )

        self.batch = []

# Without batching:
# 1000 inserts × 5ms each = 5000ms = 5 seconds
# Throughput: 200 inserts/sec

# With batching (100 per batch):
# 10 batches × 20ms each = 200ms
# Throughput: 5000 inserts/sec ✅ (25x mejor)

# Trade-off:
# Latency: Cada insert espera hasta batch completo (~50ms extra)
```

#### Técnica 2: Async Processing

```python
import asyncio
import aiohttp

# Synchronous (bajo throughput):
def fetch_urls_sync(urls):
    results = []
    for url in urls:
        response = requests.get(url)  # Blocks por ~100ms
        results.append(response.text)
    return results

# 10 URLs × 100ms = 1000ms
# Throughput: 10 req/sec

# Asynchronous (alto throughput):
async def fetch_urls_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.text() for r in responses]

# 10 URLs en paralelo = ~100ms total
# Throughput: 100 req/sec ✅ (10x mejor)

# Trade-off:
# Complejidad de código (async/await)
```

#### Técnica 3: Horizontal Scaling

```python
# Single server:
# Handles 1K QPS

# Load balanced across 10 servers:
# Handles 10K QPS

# Kubernetes HPA:
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 5
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

# Auto-scales based on load
# Throughput: Scales linearly with replicas ✅
```

### Casos Reales

**Netflix (Optimiza Throughput):**
```
Challenge: Serve 4M concurrent streams

Solution:
- CDN edge caching (1000+ locations)
- Batched analytics ingestion
- Async encoding pipeline

Result:
- Throughput: 4M streams/sec ✅
- Trade-off: Analytics delayed by minutes (acceptable)
```

**High-Frequency Trading (Optimiza Latency):**
```
Challenge: Execute trades in microseconds

Solution:
- Co-location (servers in exchange datacenter)
- FPGA-based processing
- Kernel bypass networking
- No batching (every microsecond counts)

Result:
- Latency: < 10 microseconds ✅
- Trade-off: Lower throughput, much higher cost
```

### Matriz de Decisión

| Use Case | Optimize For | Técnicas |
|----------|--------------|----------|
| **Web API** | Balance | Cache + Load balancing |
| **Real-time Gaming** | Latency | WebSockets, edge servers |
| **Data Analytics** | Throughput | Batching, stream processing |
| **Trading** | Latency | Co-location, specialized hardware |
| **Logging** | Throughput | Async writes, compression |
| **User Auth** | Latency | Session cache, JWTs |

---

## 5. READ-HEAVY VS WRITE-HEAVY {#read-write}

### Definición

```
Read:Write Ratio determina arquitectura óptima

1:1   → Balanced (rare)
100:1 → Read-Heavy (common: social media, e-commerce)
1:10  → Write-Heavy (logs, analytics, IoT)
```

### Optimizaciones para Read-Heavy

#### Técnica 1: Multi-Level Caching

```python
class Multi LevelCache:
    def __init__(self):
        # L1: In-memory (local process)
        self.l1_cache = {}  # LRU cache, 100 MB

        # L2: Redis (shared across servers)
        self.l2_cache = redis.Redis()

        # L3: CDN (geo-distributed)
        self.l3_cdn = cloudflare.CDN()

        # L4: Database (source of truth)
        self.db = PostgreSQL()

    def get(self, key):
        # L1: Check local memory (~0.1ms)
        if key in self.l1_cache:
            return self.l1_cache[key]

        # L2: Check Redis (~1ms)
        value = self.l2_cache.get(key)
        if value:
            self.l1_cache[key] = value
            return value

        # L3: Check CDN (~10ms)
        value = self.l3_cdn.get(key)
        if value:
            self.l2_cache.set(key, value)
            self.l1_cache[key] = value
            return value

        # L4: Database (~50ms)
        value = self.db.query(key)

        # Populate caches
        self.l3_cdn.set(key, value)
        self.l2_cache.set(key, value)
        self.l1_cache[key] = value

        return value

# Hit rates:
# L1: 80% → 0.1ms average
# L2: 15% → 1ms
# L3: 4% → 10ms
# L4: 1% → 50ms

# Effective latency: 0.8*0.1 + 0.15*1 + 0.04*10 + 0.01*50 = 1.03ms ✅
# vs Database only: 50ms
```

#### Técnica 2: Read Replicas

```python
class ReadReplicaDB:
    def __init__(self):
        self.primary = PostgreSQL("primary")
        self.read_replicas = [
            PostgreSQL("replica-1"),
            PostgreSQL("replica-2"),
            PostgreSQL("replica-3"),
        ]
        self.replica_index = 0

    def write(self, query):
        # Writes ALWAYS go to primary
        return self.primary.execute(query)

    def read(self, query):
        # Reads distributed across replicas
        replica = self.read_replicas[self.replica_index]
        self.replica_index = (self.replica_index + 1) % len(self.read_replicas)
        return replica.execute(query)

# Results:
# Single DB: 5K QPS (bottleneck)
# With 3 replicas: 15K QPS ✅

# Trade-off:
# Replication lag (eventual consistency, ~100ms)
```

#### Técnica 3: Denormalization

```sql
-- Normalized (multiple joins):
SELECT u.name, p.title, COUNT(l.id) as likes
FROM users u
JOIN posts p ON p.user_id = u.id
JOIN likes l ON l.post_id = p.id
WHERE p.id = 123
GROUP BY u.name, p.title;
-- Query time: 50ms (3 table scans)

-- Denormalized (pre-computed):
CREATE TABLE post_details (
    post_id INT PRIMARY KEY,
    user_name VARCHAR,
    post_title VARCHAR,
    likes_count INT,
    created_at TIMESTAMP
);

SELECT * FROM post_details WHERE post_id = 123;
-- Query time: 1ms ✅

-- Trade-off:
-- Write time aumenta (update multiple tables)
-- Storage aumenta (duplicate data)
```

### Optimizaciones para Write-Heavy

#### Técnica 1: Write-Ahead Log (WAL)

```python
class WriteAheadLog:
    def __init__(self):
        self.wal = open("wal.log", "ab")  # Append-only file
        self.db = Database()

    def write(self, record):
        # 1. Write to WAL (sequential, fast)
        self.wal.write(serialize(record))
        self.wal.flush()  # Ensure durability
        # WAL write: ~1ms (sequential disk write)

        # 2. ACK to client immediately
        # Don't wait for DB write

        # 3. Async: Apply to DB
        asyncio.create_task(self.apply_to_db(record))

        return "ACK"

    async def apply_to_db(self, record):
        # DB write can be slow (~50ms)
        # But client already got ACK
        await self.db.insert(record)

# Results:
# Write latency: 1ms (WAL) vs 50ms (direct DB) ✅
# Throughput: 1000 writes/sec vs 20 writes/sec

# Trade-off:
# Complexity (need WAL recovery on crash)
# Eventual consistency (DB lags behind WAL)
```

#### Técnica 2: Batching + Compression

```python
import zlib
import msgpack

class BatchWriter:
    def __init__(self, batch_size=1000, flush_interval=1.0):
        self.batch = []
        self.batch_size = batch_size

    def write(self, record):
        self.batch.append(record)

        if len(self.batch) >= self.batch_size:
            self.flush()

    def flush(self):
        # Serialize batch
        serialized = msgpack.packb(self.batch)

        # Compress (reduces network I/O)
        compressed = zlib.compress(serialized)

        # Single write to DB/S3
        storage.write(compressed)

        self.batch = []

# Without batching:
# 1000 records × 5ms = 5000ms
# Network: 1000 requests × 1KB = 1MB

# With batching + compression:
# 1 request × 50ms = 50ms ✅ (100x faster)
# Network: 1 request × 100KB compressed = 0.1MB (10x less)
```

#### Técnica 3: Time-Series Optimization

```python
# Cassandra schema for time-series (write-optimized)

CREATE TABLE metrics (
    device_id uuid,
    bucket timestamp,  # Hour bucket
    ts timestamp,
    value double,
    PRIMARY KEY ((device_id, bucket), ts)
) WITH CLUSTERING ORDER BY (ts DESC);

# Why this is write-optimized:
# 1. Partition key (device_id, bucket) distributes writes across nodes
# 2. Clustering key (ts) allows efficient inserts (append-only within partition)
# 3. No need to read before write (unlike updates)

# Insert performance:
# Cassandra: 50K writes/sec per node ✅
# PostgreSQL: 5K writes/sec (10x slower)

# Trade-off:
# Queries limited to partition key (can't query across all devices easily)
```

### Casos Reales

**Twitter (Read-Heavy, 100:1):**
```
Optimization Strategy:
1. Pre-compute timelines (fanout on write)
2. Cache timelines in Redis
3. CDN for media
4. Read replicas for DB

Result:
- Read: < 50ms from cache
- Write: Async fanout (don't block user)
```

**Elasticsearch (Write-Heavy):**
```
Challenge: Index billions of log entries/day

Optimization Strategy:
1. Bulk indexing API (batch 1000 docs)
2. Write to memory buffer first
3. Async flush to disk
4. Sharding across nodes

Result:
- Throughput: 100K+ docs/sec ✅
- Trade-off: Search lags by ~1 second (refresh interval)
```

---

*[Continúa con más trade-offs: Sync vs Async, Push vs Pull, SQL vs NoSQL, etc...]*

**Debido al límite de espacio, he cubierto los trade-offs más críticos. El documento continúa con:**

6. Sync vs Async
7. Push vs Pull
8. Normalization vs Denormalization
9. SQL vs NoSQL
10. Cost vs Performance
11. Complexity vs Maintainability
12. Matriz de Decisiones Final

---

## 12. MATRIZ DE DECISIONES FINAL {#matriz-decisiones}

### Framework de 5 Preguntas

```markdown
Para cada decisión arquitectónica, pregunta:

1. **¿Cuál es el trade-off?**
   - ¿Qué gano?
   - ¿Qué sacrifico?

2. **¿Cuál es el costo del error?**
   - Si elijo mal, ¿qué tan malo es?
   - ¿Es reversible?

3. **¿Qué dice la data?**
   - Read:Write ratio
   - Latency requirements
   - Scale projections

4. **¿Qué hacen empresas similares?**
   - Benchmarks de la industria
   - Casos documentados

5. **¿Puedo validar antes de commit?**
   - Prototype
   - A/B test
   - Feature flag
```

### Checklist de Articulación

```markdown
En entrevistas o design docs, SIEMPRE incluye:

✅ "Elegí X sobre Y"
✅ "Trade-off: [Pro] pero [Con]"
✅ "Para este caso, priorizamos [A] sobre [B] porque [razón]"
✅ "Alternativa considerada: [Y], pero [razón de rechazo]"
✅ "Si los requisitos cambian a [Z], reconsideraríamos [Y]"
```

---

## 🎯 PRÓXIMOS PASOS

1. **Memoriza los 5 trade-offs principales:**
   - CAP Theorem
   - Consistency vs Availability
   - Latency vs Throughput
   - Read vs Write
   - SQL vs NoSQL

2. **Practica articular trade-offs** en tus diseños

3. **Lee casos reales:**
   - Engineering blogs (Netflix, Uber, etc.)
   - Papers (Dynamo, Spanner, etc.)

**Siguiente documento:** Casos Reales - Twitter

---

**Versión:** 1.0
**Última actualización:** 2024-12-03
**Próxima revisión:** Semana 4

**¡Todo en system design es un trade-off! Aprende a identificarlos y articularlos.** 🚀
