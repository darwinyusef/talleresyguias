# Patrones de Escalabilidad - Catálogo Completo

**Semana 7 - Síntesis de System Design Fundamentals**

---

## ÍNDICE

1. [Introducción](#1-introducción)
2. [Caching Patterns](#2-caching-patterns)
3. [Database Scaling](#3-database-scaling)
4. [Load Balancing](#4-load-balancing)
5. [Rate Limiting](#5-rate-limiting)
6. [Resilience Patterns](#6-resilience-patterns)
7. [Async Processing](#7-async-processing)
8. [Microservices Patterns](#8-microservices-patterns)
9. [CDN & Edge Computing](#9-cdn--edge-computing)
10. [Matriz de Decisión](#10-matriz-de-decisión)

---

## 1. INTRODUCCIÓN

Este documento es un **catálogo de referencia rápida** de patrones de escalabilidad aplicados en los casos reales estudiados (Twitter, Uber, Netflix) y patrones adicionales esenciales.

### Organización

Cada patrón incluye:
- **Problema** que resuelve
- **Solución** propuesta
- **Cuándo usar** (use cases)
- **Pros & Cons**
- **Ejemplo de código**
- **Casos reales** donde se aplicó

### Categorías de Patrones

```
┌──────────────────────────────────────────────────────────────┐
│                   ESCALABILIDAD                              │
├─────────────────┬────────────────┬──────────────────────────┤
│  Performance    │  Availability  │    Maintainability       │
│                 │                │                          │
│  • Caching      │  • Load        │  • Microservices         │
│  • Async        │    Balancing   │  • Service Mesh          │
│  • CDN          │  • Replication │  • API Gateway           │
│                 │  • Circuit     │  • Event-Driven          │
│                 │    Breaker     │                          │
└─────────────────┴────────────────┴──────────────────────────┘
```

---

## 2. CACHING PATTERNS

### 2.1 Cache-Aside (Lazy Loading)

**Problema**: Database queries son lentas y costosas.

**Solución**: La aplicación verifica cache primero, si falla (cache miss) consulta DB y actualiza cache.

**Flow**:
```
1. App → Cache: GET key
2. Cache HIT → Return data ✅
3. Cache MISS → App → DB: Query
4. DB → App: Data
5. App → Cache: SET key, data
6. App → User: Data
```

**Código**:
```python
def get_user(user_id):
    cache_key = f"user:{user_id}"

    # 1. Try cache
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)  # Cache HIT

    # 2. Cache MISS: Query database
    user = db.query("SELECT * FROM users WHERE user_id = %s", user_id)

    if user:
        # 3. Update cache
        redis.setex(cache_key, 3600, json.dumps(user))  # TTL: 1 hour

    return user
```

**Pros**:
- ✅ Simple de implementar
- ✅ Solo datos accedidos se cachean (eficiente)
- ✅ Cache puede caer sin afectar disponibilidad

**Cons**:
- ❌ Cache MISS penalty (doble latencia: cache + DB)
- ❌ Datos pueden quedar stale hasta TTL expira

**Cuándo usar**:
- Read-heavy workloads
- Datos que cambian poco
- Toleras eventual consistency

**Caso real**: Twitter (user profiles cache), Uber (driver metadata cache)

---

### 2.2 Write-Through Cache

**Problema**: Cache-aside puede tener datos stale. Necesitas strong consistency.

**Solución**: Al escribir, actualizar DB y cache **sincrónicamente**.

**Flow**:
```
1. App → Write (user, data)
2. App → DB: UPDATE
3. App → Cache: SET key, data (sync)
4. App → User: ACK
```

**Código**:
```python
def update_user(user_id, data):
    cache_key = f"user:{user_id}"

    # 1. Update database
    db.execute("UPDATE users SET name = %s WHERE user_id = %s", data['name'], user_id)

    # 2. Update cache (synchronously)
    redis.set(cache_key, json.dumps(data))

    return {"status": "success"}
```

**Pros**:
- ✅ Cache siempre consistente con DB
- ✅ Read latency siempre baja (cache hit)

**Cons**:
- ❌ Write latency mayor (doble escritura)
- ❌ Writes innecesarias si dato no se lee

**Cuándo usar**:
- Necesitas strong consistency
- Read-heavy con algunos writes
- Latencia de write no es crítica

**Caso real**: E-commerce (inventory updates), Banking (account balances)

---

### 2.3 Write-Behind (Write-Back) Cache

**Problema**: Write-through aumenta latencia de writes.

**Solución**: Escribir a cache inmediatamente, actualizar DB **asincrónicamente** después.

**Flow**:
```
1. App → Cache: SET key, data (sync) ✅ Fast!
2. App → User: ACK immediately
3. Background worker → DB: UPDATE (async)
```

**Código**:
```python
def update_user_async(user_id, data):
    cache_key = f"user:{user_id}"

    # 1. Update cache immediately
    redis.set(cache_key, json.dumps(data))

    # 2. Queue DB update asynchronously
    task_queue.enqueue('update_user_db', user_id, data)

    return {"status": "success"}  # Fast response!

# Background worker
def update_user_db(user_id, data):
    db.execute("UPDATE users SET name = %s WHERE user_id = %s", data['name'], user_id)
```

**Pros**:
- ✅ Writes muy rápidos (solo cache)
- ✅ Reduce carga en DB (batch writes posible)

**Cons**:
- ❌ Riesgo de pérdida de datos (si cache falla antes de DB update)
- ❌ Complejidad: necesitas background workers
- ❌ Eventual consistency

**Cuándo usar**:
- Write-heavy workloads
- OK perder algunos writes recientes (toleras riesgo)
- Necesitas máxima performance

**Caso real**: Social media (likes, views counters - eventual consistency OK)

---

### 2.4 Multi-Level Caching (L1/L2/L3)

**Problema**: Single cache layer no escala para workloads masivos.

**Solución**: Múltiples capas de cache (L1 = in-process, L2 = Redis, L3 = CDN).

**Architecture**:
```
User Request
    ↓
L1 Cache (In-Memory, 100ms TTL)  → 99% hit rate, 1ms latency
    ↓ miss
L2 Cache (Redis, 1 hour TTL)     → 90% hit rate, 5ms latency
    ↓ miss
L3 Cache (CDN, 24 hour TTL)      → 80% hit rate, 50ms latency
    ↓ miss
Origin Database                   → 500ms latency
```

**Código**:
```python
class MultiLevelCache:
    def __init__(self):
        self.l1 = {}  # In-memory dict (local to instance)
        self.l2 = redis.Redis()  # Shared Redis
        self.l3 = requests.Session()  # CDN

    def get(self, key):
        # L1: Local memory
        if key in self.l1:
            return self.l1[key]  # 1ms

        # L2: Redis
        l2_data = self.l2.get(key)
        if l2_data:
            self.l1[key] = l2_data  # Populate L1
            return l2_data  # 5ms

        # L3: CDN (for static assets)
        cdn_url = f"https://cdn.example.com/{key}"
        response = self.l3.get(cdn_url)
        if response.status_code == 200:
            data = response.content
            self.l2.setex(key, 3600, data)  # Populate L2
            self.l1[key] = data  # Populate L1
            return data  # 50ms

        # Cache miss: Query origin
        data = query_database(key)  # 500ms
        self.l2.setex(key, 3600, data)
        self.l1[key] = data
        return data
```

**Pros**:
- ✅ Extremely fast (L1 hits en 1ms)
- ✅ Reduces load on L2/L3/DB
- ✅ Fault tolerance (L1 miss → fallback L2)

**Cons**:
- ❌ Cache invalidation complejo (3 layers)
- ❌ Memory usage (L1 en cada instancia)
- ❌ Consistency challenges

**Cuándo usar**:
- Ultra-high traffic (millones RPS)
- Datos read-heavy e inmutables
- Budget para complejidad

**Caso real**: Twitter (timelines), Netflix (video manifests), Facebook (user profiles)

---

### 2.5 Cache Invalidation Strategies

**"There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton**

#### Strategy 1: TTL (Time-to-Live)

**Simplest approach**: Set expiration time.

```python
redis.setex("user:123", 3600, data)  # Expires in 1 hour
```

**Pros**: Simple, no coordinación
**Cons**: Stale data hasta TTL expira

---

#### Strategy 2: Write-Through Invalidation

**On write, delete cache entry**:

```python
def update_user(user_id, data):
    # Update DB
    db.execute("UPDATE users SET name = %s WHERE user_id = %s", data['name'], user_id)

    # Invalidate cache
    redis.delete(f"user:{user_id}")
```

**Pros**: Cache siempre fresh
**Cons**: Cache miss inmediato después de write

---

#### Strategy 3: Event-Based Invalidation

**Use Pub/Sub to notify cache invalidations**:

```python
# On write
def update_user(user_id, data):
    db.execute("UPDATE users SET name = %s WHERE user_id = %s", data['name'], user_id)

    # Publish invalidation event
    pubsub.publish('cache_invalidate', f"user:{user_id}")

# Subscribers (all app instances)
def on_invalidate_message(message):
    key = message['data']
    local_cache.delete(key)
```

**Pros**: Invalidación distribuida
**Cons**: Requiere pub/sub infrastructure

---

#### Strategy 4: Versioned Cache Keys

**Include version in cache key**:

```python
# Version stored in DB
user_version = db.query("SELECT version FROM users WHERE user_id = %s", user_id)['version']

# Cache key includes version
cache_key = f"user:{user_id}:v{user_version}"
cached = redis.get(cache_key)

# On write: increment version
db.execute("UPDATE users SET version = version + 1 WHERE user_id = %s", user_id)
# Old cache entries automatically stale (different key)
```

**Pros**: No explicit invalidation needed
**Cons**: Cache sprawl (old versions linger until TTL)

**Caso real**: Netflix (video manifests con versioning), AWS S3 ETags

---

## 3. DATABASE SCALING

### 3.1 Read Replicas

**Problema**: Single database saturado por read traffic.

**Solución**: Replicar datos a múltiples read-only replicas.

**Architecture**:
```
         ┌─────────────┐
         │   Primary   │
         │  (Read/Write)│
         └──────┬──────┘
                │ Replication
       ┌────────┼────────┐
       │        │        │
   ┌───▼───┐┌──▼───┐┌───▼───┐
   │Replica││Replica││Replica│
   │(Read) ││(Read) ││(Read) │
   └───────┘└──────┘└───────┘
```

**Código**:
```python
class DatabaseRouter:
    def __init__(self):
        self.primary = connect_db("primary.db.com")
        self.replicas = [
            connect_db("replica1.db.com"),
            connect_db("replica2.db.com"),
            connect_db("replica3.db.com")
        ]
        self.replica_index = 0

    def execute_write(self, query, params):
        # All writes go to primary
        return self.primary.execute(query, params)

    def execute_read(self, query, params):
        # Round-robin across replicas
        replica = self.replicas[self.replica_index]
        self.replica_index = (self.replica_index + 1) % len(self.replicas)
        return replica.execute(query, params)

# Usage
db = DatabaseRouter()

# Write
db.execute_write("INSERT INTO users (name) VALUES (%s)", "Alice")

# Read (distributed across replicas)
users = db.execute_read("SELECT * FROM users")
```

**Pros**:
- ✅ Escala reads horizontalmente
- ✅ Failover (si primary falla, promote replica)

**Cons**:
- ❌ Replication lag (replicas pueden estar 1-2 sec detrás)
- ❌ No escala writes (solo 1 primary)

**Cuándo usar**:
- Read-heavy workload (90%+ reads)
- OK eventual consistency (replication lag)

**Caso real**: Twitter (5 read replicas), Uber (PostgreSQL replicas)

---

### 3.2 Sharding (Horizontal Partitioning)

**Problema**: Single database no puede manejar writes y datos no caben en un servidor.

**Solución**: Particionar datos across múltiples databases (shards).

**Sharding Key**: Atributo usado para determinar qué shard (ej: `user_id % num_shards`).

**Architecture**:
```
        ┌─────────────────┐
        │  Application    │
        │  (Shard Router) │
        └────────┬─────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
┌────▼─────┐┌───▼────┐┌────▼─────┐
│ Shard 0  ││Shard 1 ││ Shard 2  │
│ users    ││users   ││ users    │
│ 0-333M   ││333-666M││ 666M-1B  │
└──────────┘└────────┘└──────────┘
```

**Sharding Strategies**:

#### 1. Hash-Based Sharding

```python
def get_shard(user_id, num_shards=3):
    shard_id = hash(user_id) % num_shards
    return shards[shard_id]

# Example
shard = get_shard(user_id=12345, num_shards=3)
shard.execute("SELECT * FROM users WHERE user_id = %s", 12345)
```

**Pros**: Even distribution
**Cons**: Resharding is hard (need to rehash all keys)

---

#### 2. Range-Based Sharding

```python
def get_shard_range(user_id):
    if user_id < 1_000_000:
        return shards[0]
    elif user_id < 2_000_000:
        return shards[1]
    else:
        return shards[2]
```

**Pros**: Easy to add shards (just new range)
**Cons**: Hotspots (if new users concentrated)

---

#### 3. Geographic Sharding

```python
def get_shard_geo(user_region):
    shard_map = {
        'US': shards[0],
        'EU': shards[1],
        'APAC': shards[2]
    }
    return shard_map[user_region]
```

**Pros**: Low latency (data near users)
**Cons**: Uneven distribution

**Cuándo usar**:
- Data > 1 TB (no cabe en single server)
- Write-heavy workload
- Need horizontal write scaling

**Caso real**: Twitter (users sharded by user_id), Uber (rides sharded by geo hash)

---

### 3.3 Consistent Hashing

**Problema**: Hash-based sharding con resharding es costoso (rehash todo).

**Solución**: Consistent hashing minimiza rehashing al agregar/quitar nodos.

**How it works**:
1. Hash nodes y keys al mismo espacio (0 - 2^32)
2. Key se almacena en el primer nodo en sentido horario

**Diagram**:
```
        Hash Ring (0 - 2^32)
           _______________
         /                 \
    Node A (100)           Node B (200)
         \                 /
          ---------------
                |
        Key X (150) → Goes to Node B
```

**Código**:
```python
import hashlib

class ConsistentHashing:
    def __init__(self, nodes, virtual_nodes=150):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []

        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        """Add node with virtual nodes for better distribution."""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_key = self._hash(virtual_key)
            self.ring[hash_key] = node
            self.sorted_keys.append(hash_key)

        self.sorted_keys.sort()

    def remove_node(self, node):
        """Remove node."""
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}:{i}"
            hash_key = self._hash(virtual_key)
            del self.ring[hash_key]
            self.sorted_keys.remove(hash_key)

    def get_node(self, key):
        """Get node for key."""
        if not self.ring:
            return None

        hash_key = self._hash(key)

        # Find first node clockwise
        for node_key in self.sorted_keys:
            if node_key >= hash_key:
                return self.ring[node_key]

        # Wrap around
        return self.ring[self.sorted_keys[0]]

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

# Usage
nodes = ['server1', 'server2', 'server3']
ch = ConsistentHashing(nodes)

# Route keys to nodes
print(ch.get_node('user:123'))  # server2
print(ch.get_node('user:456'))  # server1

# Add new node: Only ~1/4 keys rehash
ch.add_node('server4')
```

**Pros**:
- ✅ Minimal rehashing (only K/N keys, where K = keys, N = nodes)
- ✅ Easy to add/remove nodes

**Cons**:
- ❌ Complexity
- ❌ Virtual nodes overhead

**Cuándo usar**:
- Frequently adding/removing nodes
- Distributed caching (Memcached, Redis Cluster)

**Caso real**: DynamoDB, Cassandra, Redis Cluster

---

## 4. LOAD BALANCING

### 4.1 Round Robin

**Simplest algorithm**: Distribute requests sequentially.

```python
class RoundRobinLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.index = 0

    def get_server(self):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server

# Usage
lb = RoundRobinLoadBalancer(['server1', 'server2', 'server3'])
print(lb.get_server())  # server1
print(lb.get_server())  # server2
print(lb.get_server())  # server3
print(lb.get_server())  # server1 (wrap around)
```

**Pros**: Simple, fair distribution
**Cons**: No considera carga actual de servers

---

### 4.2 Least Connections

**Select server with fewest active connections**.

```python
class LeastConnectionsLoadBalancer:
    def __init__(self, servers):
        self.connections = {server: 0 for server in servers}

    def get_server(self):
        # Find server with least connections
        server = min(self.connections, key=self.connections.get)
        self.connections[server] += 1
        return server

    def release_connection(self, server):
        self.connections[server] -= 1

# Usage
lb = LeastConnectionsLoadBalancer(['server1', 'server2', 'server3'])
server = lb.get_server()
# ... handle request ...
lb.release_connection(server)
```

**Pros**: Better for long-lived connections
**Cons**: More complex, needs tracking

---

### 4.3 Weighted Load Balancing

**Servers con más capacidad reciben más tráfico**.

```python
class WeightedLoadBalancer:
    def __init__(self, servers_weights):
        """servers_weights = {'server1': 5, 'server2': 3, 'server3': 2}"""
        self.servers = []
        for server, weight in servers_weights.items():
            self.servers.extend([server] * weight)
        self.index = 0

    def get_server(self):
        server = self.servers[self.index]
        self.index = (self.index + 1) % len(self.servers)
        return server

# Usage
lb = WeightedLoadBalancer({'server1': 5, 'server2': 3, 'server3': 2})
# server1 gets 50% traffic, server2 gets 30%, server3 gets 20%
```

**Cuándo usar**: Heterogeneous servers (diferentes specs)

---

### 4.4 Health Checks

**Problema**: Load balancer routing a servidor muerto.

**Solución**: Active health checks.

```python
import requests
import threading
import time

class HealthCheckLoadBalancer:
    def __init__(self, servers, health_check_interval=10):
        self.servers = servers
        self.healthy_servers = set(servers)
        self.health_check_interval = health_check_interval

        # Start health check thread
        threading.Thread(target=self._health_check_loop, daemon=True).start()

    def _health_check_loop(self):
        while True:
            for server in self.servers:
                if self._is_healthy(server):
                    self.healthy_servers.add(server)
                else:
                    self.healthy_servers.discard(server)
                    print(f"Server {server} is DOWN")

            time.sleep(self.health_check_interval)

    def _is_healthy(self, server):
        try:
            response = requests.get(f"http://{server}/health", timeout=2)
            return response.status_code == 200
        except:
            return False

    def get_server(self):
        if not self.healthy_servers:
            raise Exception("No healthy servers available")

        # Round robin among healthy servers
        return list(self.healthy_servers)[0]
```

**Caso real**: AWS ELB, nginx, HAProxy

---

## 5. RATE LIMITING

### 5.1 Token Bucket Algorithm

**Idea**: Bucket se llena con tokens a rate constante. Request consume 1 token.

```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        """
        capacity: Max tokens in bucket
        refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def allow_request(self):
        # Refill tokens based on time elapsed
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

        # Try to consume 1 token
        if self.tokens >= 1:
            self.tokens -= 1
            return True  # Allow request
        else:
            return False  # Rate limit exceeded

# Usage
bucket = TokenBucket(capacity=10, refill_rate=2)  # 2 req/sec, burst of 10

for i in range(15):
    if bucket.allow_request():
        print(f"Request {i}: Allowed")
    else:
        print(f"Request {i}: Rate limited")
    time.sleep(0.1)
```

**Pros**:
- ✅ Allows bursts (up to capacity)
- ✅ Smooth rate limiting

**Cons**:
- ❌ Memory overhead (state per user)

**Cuándo usar**:
- API rate limiting (100 req/min)
- Allow occasional bursts

**Caso real**: Stripe API, GitHub API, AWS API Gateway

---

### 5.2 Leaky Bucket Algorithm

**Idea**: Requests go into queue. Queue drains at constant rate.

```python
from collections import deque
import time
import threading

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        """
        capacity: Max queue size
        leak_rate: Requests processed per second
        """
        self.capacity = capacity
        self.queue = deque()
        self.leak_rate = leak_rate

        # Start leak thread
        threading.Thread(target=self._leak, daemon=True).start()

    def add_request(self, request):
        if len(self.queue) < self.capacity:
            self.queue.append(request)
            return True  # Accepted
        else:
            return False  # Dropped (bucket full)

    def _leak(self):
        """Process requests at constant rate."""
        while True:
            if self.queue:
                request = self.queue.popleft()
                self._process_request(request)

            time.sleep(1 / self.leak_rate)

    def _process_request(self, request):
        print(f"Processing: {request}")

# Usage
bucket = LeakyBucket(capacity=5, leak_rate=2)  # Process 2 req/sec
bucket.add_request("Request 1")
bucket.add_request("Request 2")
```

**Pros**:
- ✅ Constant output rate (smooth)
- ✅ Prevents server overload

**Cons**:
- ❌ Bursts get queued (higher latency)

---

### 5.3 Sliding Window Log

**Accurate rate limiting usando timestamps**.

```python
import time
from collections import deque

class SlidingWindowLog:
    def __init__(self, window_size_seconds, max_requests):
        """
        window_size_seconds: Time window (e.g., 60 for 1 minute)
        max_requests: Max requests in window
        """
        self.window_size = window_size_seconds
        self.max_requests = max_requests
        self.request_log = deque()

    def allow_request(self):
        now = time.time()

        # Remove requests outside window
        while self.request_log and self.request_log[0] <= now - self.window_size:
            self.request_log.popleft()

        # Check if under limit
        if len(self.request_log) < self.max_requests:
            self.request_log.append(now)
            return True
        else:
            return False

# Usage: 10 requests per minute
limiter = SlidingWindowLog(window_size_seconds=60, max_requests=10)

for i in range(15):
    if limiter.allow_request():
        print(f"Request {i}: Allowed")
    else:
        print(f"Request {i}: Rate limited")
    time.sleep(5)
```

**Pros**:
- ✅ Accurate (no edge effects)

**Cons**:
- ❌ Memory overhead (store all timestamps)

---

### 5.4 Distributed Rate Limiting (Redis)

**Problema**: Rate limiting en distributed system (múltiples servers).

**Solución**: Shared state en Redis.

```python
import redis
import time

class DistributedRateLimiter:
    def __init__(self, redis_client, max_requests, window_seconds):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window_seconds

    def allow_request(self, user_id):
        key = f"ratelimit:{user_id}"
        now = time.time()

        # Use Redis sorted set (score = timestamp)
        pipe = self.redis.pipeline()

        # Remove old entries
        pipe.zremrangebyscore(key, 0, now - self.window)

        # Count requests in window
        pipe.zcard(key)

        # Add current request
        pipe.zadd(key, {now: now})

        # Set expiration
        pipe.expire(key, self.window)

        results = pipe.execute()
        request_count = results[1]

        return request_count < self.max_requests

# Usage
redis_client = redis.Redis()
limiter = DistributedRateLimiter(redis_client, max_requests=100, window_seconds=60)

if limiter.allow_request(user_id=123):
    # Process request
    pass
else:
    # Return 429 Too Many Requests
    pass
```

**Caso real**: Twitter API, Cloudflare rate limiting

---

## 6. RESILIENCE PATTERNS

### 6.1 Circuit Breaker

**Problema**: Calling a failing service repeatedly makes things worse.

**Solución**: Stop calling service temporarily after failures.

**States**:
```
CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing) → CLOSED
```

**Código**:
```python
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            # Check if timeout expired
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                print("Circuit HALF_OPEN: Testing service")
            else:
                raise Exception("Circuit OPEN: Service unavailable")

        try:
            result = func(*args, **kwargs)

            # Success: Reset if HALF_OPEN
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                print("Circuit CLOSED: Service recovered")

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"Circuit OPEN: Too many failures ({self.failure_count})")

            raise e

# Usage
def unreliable_service():
    import random
    if random.random() < 0.7:  # 70% failure rate
        raise Exception("Service error")
    return "Success"

cb = CircuitBreaker(failure_threshold=3, timeout=10)

for i in range(20):
    try:
        result = cb.call(unreliable_service)
        print(f"Request {i}: {result}")
    except Exception as e:
        print(f"Request {i}: {e}")
    time.sleep(1)
```

**Pros**:
- ✅ Prevents cascade failures
- ✅ Fast failure (don't wait for timeout)

**Cons**:
- ❌ May reject requests during recovery

**Cuándo usar**:
- Calling external services (payment gateway, API)
- Service with high latency/failure rate

**Caso real**: Netflix Hystrix, AWS Lambda

---

### 6.2 Retry with Exponential Backoff

**Problema**: Immediate retry after failure overloads server.

**Solución**: Retry con delays crecientes exponencialmente.

```python
import time
import random

def retry_with_backoff(func, max_retries=5, base_delay=1):
    """
    Retry function with exponential backoff.

    Delays: 1s, 2s, 4s, 8s, 16s (+ jitter)
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                # Last attempt failed
                raise e

            # Calculate delay: base * 2^attempt + jitter
            delay = base_delay * (2 ** attempt)
            jitter = random.uniform(0, delay * 0.1)  # ±10% jitter
            total_delay = delay + jitter

            print(f"Attempt {attempt + 1} failed. Retrying in {total_delay:.2f}s...")
            time.sleep(total_delay)

# Usage
def flaky_api_call():
    import random
    if random.random() < 0.8:  # 80% failure
        raise Exception("API error")
    return "Success"

result = retry_with_backoff(flaky_api_call, max_retries=5)
print(result)
```

**Jitter**: Randomness to avoid thundering herd (all clients retry at same time).

**Caso real**: AWS SDK, Stripe API

---

### 6.3 Bulkhead Pattern

**Problema**: One failing component exhausts all resources (thread pool).

**Solución**: Isolate resources para diferentes componentes.

**Analogy**: Ship compartments (if one floods, others stay dry).

```python
import concurrent.futures

class Bulkhead:
    def __init__(self, max_workers_per_service):
        """
        Separate thread pools per service.
        """
        self.executors = {}
        self.max_workers = max_workers_per_service

    def execute(self, service_name, func, *args):
        if service_name not in self.executors:
            self.executors[service_name] = concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers
            )

        executor = self.executors[service_name]
        future = executor.submit(func, *args)
        return future.result()

# Usage
bulkhead = Bulkhead(max_workers_per_service=5)

def slow_payment_service():
    time.sleep(10)  # Slow!
    return "Payment processed"

def fast_inventory_service():
    time.sleep(0.1)
    return "Inventory checked"

# Even if payment service is slow/failing, inventory service is unaffected
bulkhead.execute('payment', slow_payment_service)
bulkhead.execute('inventory', fast_inventory_service)  # Fast, not blocked
```

**Pros**:
- ✅ Fault isolation
- ✅ Prevents resource exhaustion

**Cons**:
- ❌ More resource usage (multiple pools)

**Caso real**: Netflix (service-specific thread pools)

---

## 7. ASYNC PROCESSING

### 7.1 Message Queues (Kafka, RabbitMQ)

**Problema**: Synchronous processing blocks user request.

**Solución**: Enqueue task, process asynchronously.

**Architecture**:
```
User Request → API → Enqueue → Queue → Worker → Process
                ↓
             Return ACK (fast!)
```

**Código**:
```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer (API)
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def create_order(order_data):
    # 1. Save order to DB (minimal write)
    order_id = db.insert("INSERT INTO orders (user_id, total) VALUES (%s, %s)",
                         order_data['user_id'], order_data['total'])

    # 2. Enqueue for async processing
    producer.send('order_processing', {
        'order_id': order_id,
        'user_id': order_data['user_id'],
        'items': order_data['items']
    })

    # 3. Return immediately
    return {'order_id': order_id, 'status': 'processing'}

# Consumer (Worker)
consumer = KafkaConsumer(
    'order_processing',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    order = message.value

    # Process order (slow operations)
    charge_payment(order['user_id'], order['total'])
    update_inventory(order['items'])
    send_confirmation_email(order['user_id'], order['order_id'])

    print(f"Order {order['order_id']} processed")
```

**Pros**:
- ✅ Fast user response
- ✅ Decouples services
- ✅ Handles traffic spikes (queue buffers)

**Cons**:
- ❌ Eventual consistency
- ❌ Need to handle failures (retries, dead letter queue)

**Cuándo usar**:
- Long-running tasks (video encoding, report generation)
- Non-critical operations (email, notifications)

**Caso real**: Twitter (tweet fanout), Uber (trip matching), Netflix (encoding pipeline)

---

### 7.2 Pub/Sub Pattern

**Diferencia vs Queue**: Multiple subscribers receive same message.

```python
# Kafka Pub/Sub example

# Publisher
producer.send('user_events', {
    'event_type': 'user_registered',
    'user_id': 123,
    'timestamp': datetime.now().isoformat()
})

# Multiple Subscribers
# Subscriber 1: Email Service
consumer_email = KafkaConsumer('user_events', group_id='email_service')
for msg in consumer_email:
    if msg.value['event_type'] == 'user_registered':
        send_welcome_email(msg.value['user_id'])

# Subscriber 2: Analytics Service
consumer_analytics = KafkaConsumer('user_events', group_id='analytics_service')
for msg in consumer_analytics:
    track_event(msg.value)

# Subscriber 3: Recommendation Service
consumer_recs = KafkaConsumer('user_events', group_id='recommendation_service')
for msg in consumer_recs:
    if msg.value['event_type'] == 'user_registered':
        generate_initial_recommendations(msg.value['user_id'])
```

**Caso real**: Event-driven microservices

---

## 8. MICROSERVICES PATTERNS

### 8.1 API Gateway

**Problema**: Clients need to call múltiples microservices.

**Solución**: Single entry point que routes requests.

**Architecture**:
```
Client → API Gateway → Auth Service
                    → User Service
                    → Order Service
                    → Payment Service
```

**Responsabilidades**:
- Request routing
- Authentication
- Rate limiting
- Response aggregation
- Protocol translation (REST → gRPC)

**Ejemplo (Kong, AWS API Gateway)**:
```yaml
# Kong configuration
services:
  - name: user-service
    url: http://user-service:8080

  - name: order-service
    url: http://order-service:8080

routes:
  - service: user-service
    paths: ["/api/users"]

  - service: order-service
    paths: ["/api/orders"]

plugins:
  - name: rate-limiting
    config:
      minute: 100

  - name: jwt
    config:
      secret_is_base64: false
```

**Caso real**: Netflix Zuul, AWS API Gateway, Kong

---

### 8.2 Service Mesh (Istio, Linkerd)

**Problema**: Microservices need observability, security, traffic management.

**Solución**: Sidecar proxy intercepta all traffic.

**Architecture**:
```
Service A → Sidecar Proxy A → Network → Sidecar Proxy B → Service B
              (Envoy)                      (Envoy)
```

**Features**:
- Traffic management (retries, timeouts, circuit breaker)
- Observability (metrics, tracing)
- Security (mTLS encryption)

**Caso real**: Uber (uses Envoy), Lyft (created Envoy)

---

## 9. CDN & EDGE COMPUTING

### 9.1 CDN (Content Delivery Network)

**Problema**: Serving static assets from single origin is slow for global users.

**Solución**: Cache assets at edge locations near users.

**Flow**:
```
User (Tokyo) → CDN Edge (Tokyo) → Cache HIT → Return ✅ Fast!
                                → Cache MISS → Origin (US-West) → Cache → Return
```

**What to CDN**:
- ✅ Static assets (images, CSS, JS)
- ✅ Video files
- ✅ API responses (if cacheable)

**What NOT to CDN**:
- ❌ User-specific data (without auth)
- ❌ Frequently changing data

**Cache Headers**:
```http
HTTP/1.1 200 OK
Cache-Control: public, max-age=3600
ETag: "abc123"
```

**Caso real**: Netflix (Open Connect), Cloudflare, AWS CloudFront

---

### 9.2 Edge Computing

**Push computation to edge** (not just cache).

**Example**: Cloudflare Workers

```javascript
// Run at edge (200+ locations worldwide)
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Personalize response at edge
  const country = request.headers.get('CF-IPCountry')

  if (country === 'US') {
    return new Response('Hello from USA!')
  } else {
    return new Response('Hello international user!')
  }
}
```

**Use cases**:
- A/B testing at edge
- Bot detection
- JWT validation
- Personalization

---

## 10. MATRIZ DE DECISIÓN

### Cuándo Usar Cada Patrón

| Problema | Patrón Recomendado | Cuándo NO usar |
|----------|-------------------|----------------|
| **Read latency alta** | Multi-level caching | Datos cambian constantemente |
| **Write latency alta** | Write-behind cache, Async queue | Necesitas strong consistency |
| **DB saturado (reads)** | Read replicas | Write-heavy workload |
| **DB saturado (writes)** | Sharding | Data < 100 GB |
| **Uneven load** | Consistent hashing | Static node pool |
| **External service failing** | Circuit breaker | Service is critical path |
| **Traffic spikes** | Rate limiting + Queue | All traffic is critical |
| **Global latency** | CDN + Edge computing | User-specific data |
| **Microservices complexity** | API Gateway + Service Mesh | Monolith (premature) |

---

### Performance vs Consistency Trade-offs

| Patrón | Latencia | Consistency | Complexity |
|--------|----------|-------------|------------|
| **Cache-aside** | Low (cache hit) | Eventual | Low |
| **Write-through** | Medium | Strong | Medium |
| **Write-behind** | Very Low | Eventual (risk) | High |
| **Read replicas** | Low | Eventual | Medium |
| **Sharding** | Low | Depends | High |

---

## 📚 CHEAT SHEET FINAL

### Números a Memorizar
```
L1 cache: 1 ms
Redis cache: 5 ms
PostgreSQL query: 50 ms
Cross-region API: 150 ms
Replication lag: 1-2 seconds
CDN edge: 20-50 ms
```

### Quick Decision Tree
```
High read traffic?
├─ Yes → Caching (L1/L2/L3)
│   └─ Still too slow? → Read replicas
└─ No → Check write traffic

High write traffic?
├─ Yes → Write-behind cache or Sharding
└─ No → Standard setup OK

Global users?
├─ Yes → CDN + Edge computing
└─ No → Single region OK

External dependencies?
├─ Yes → Circuit breaker + Retry
└─ No → Direct calls OK
```

---

## 🎯 CONCLUSIÓN

Has completado **System Design Fundamentals**! En 7 semanas cubriste:

1. ✅ Framework RESHADED (metodología)
2. ✅ Cálculos de capacidad (back-of-envelope)
3. ✅ Trade-offs fundamentales (CAP, consistency, etc.)
4. ✅ Twitter (fanout, Cassandra, timeline generation)
5. ✅ Uber (geospatial, matching, surge pricing)
6. ✅ Netflix (CDN, ABR streaming, recommendations)
7. ✅ Patrones de escalabilidad (síntesis de todo)

**Skills adquiridos**:
- Diseñar sistemas para 100M+ usuarios
- Calcular QPS, storage, bandwidth sin calculadora
- Aplicar caching, sharding, load balancing
- Identificar trade-offs rápidamente
- Implementar resilience patterns

**Próximo paso**: Fase 1 continúa con **Distributed Systems** (Mes 2), donde profundizarás en consensus algorithms, replication, partition tolerance, etc.

---

**Creado**: 2024-12-05
**Versión**: 1.0
**Parte de**: Fase 1 - System Design Fundamentals (Conclusión)
