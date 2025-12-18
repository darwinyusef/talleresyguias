# Fundamentos de Sistemas Distribuidos

**Mes 2 - Semana 8**
**Distributed Systems Core**

---

## ÍNDICE

1. [Introducción](#1-introducción)
2. [Definición y Características](#2-definición-y-características)
3. [Desafíos Fundamentales](#3-desafíos-fundamentales)
4. [Fallacies of Distributed Computing](#4-fallacies-of-distributed-computing)
5. [Modelos de Comunicación](#5-modelos-de-comunicación)
6. [Failure Models](#6-failure-models)
7. [Teorema CAP (Revisited)](#7-teorema-cap-revisited)
8. [Time & Ordering](#8-time--ordering)
9. [Casos de Estudio](#9-casos-de-estudio)
10. [Ejercicios](#10-ejercicios)

---

## 1. INTRODUCCIÓN

### ¿Qué es un Sistema Distribuido?

> **Definición (Leslie Lamport)**:
> "Un sistema distribuido es aquel en el que el fallo de un ordenador que ni siquiera sabías que existía puede hacer que tu propio ordenador sea inutilizable."

**Definición formal**: Un sistema distribuido es una colección de entidades computacionales autónomas que aparecen ante los usuarios como un sistema único y coherente.

### ¿Por qué Sistemas Distribuidos?

**Razones para distribuir**:

1. **Escalabilidad**
   - Vertical scaling tiene límites físicos
   - Horizontal scaling es prácticamente ilimitado
   ```
   Single server max: ~1M requests/sec
   Distributed system: Billones de requests/sec (Google, Facebook)
   ```

2. **Disponibilidad**
   - Single point of failure (SPOF) → 99.9% uptime
   - Distributed system con replication → 99.99% uptime
   - 99.9% = 8.76 horas downtime/año
   - 99.99% = 52.6 minutos downtime/año

3. **Latencia Geográfica**
   - Data center en California → Usuario en Tokyo: 150ms RTT
   - Data center local en Tokyo → Usuario en Tokyo: 5ms RTT
   - 30x mejora en latencia

4. **Fault Tolerance**
   - Hardware falla (discos, RAM, red)
   - Software tiene bugs
   - Humanos cometen errores
   - Distribución permite tolerar fallos

### Ejemplos de Sistemas Distribuidos

```
Ejemplos cotidianos:
- Google Search (millones de servers)
- WhatsApp (mensajería distribuida)
- Netflix (CDN global, streaming)
- Bitcoin (blockchain distribuido)
- Uber (geospatial distribuido)
- DNS (sistema de nombres distribuido)
```

---

## 2. DEFINICIÓN Y CARACTERÍSTICAS

### Características Deseables

#### 1. Transparency (Transparencia)

**Tipos de transparencia**:

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Access** | Mismo acceso a recursos locales/remotos | NFS (Network File System) |
| **Location** | Usuario no necesita saber dónde está el recurso | DNS, CDN |
| **Migration** | Recurso puede moverse sin afectar acceso | VM live migration |
| **Replication** | Usuario no sabe si hay múltiples copias | Read replicas |
| **Concurrency** | Múltiples usuarios acceden sin interferencia | Database transactions |
| **Failure** | Usuario no ve fallos (sistema se recupera) | Auto-failover |

**Ejemplo de Transparency**:
```python
# Access Transparency: Mismo código para local/remote
file = open('/data/file.txt', 'r')  # ¿Local o NFS? Usuario no sabe.

# Location Transparency: No importa dónde está el server
response = requests.get('https://api.example.com/users')  # ¿US? ¿EU? ¿APAC?

# Replication Transparency:
user = db.query("SELECT * FROM users WHERE id = 123")  # ¿Primary? ¿Replica? No importa.
```

---

#### 2. Scalability (Escalabilidad)

**Dimensiones de escalabilidad**:

**Size Scalability**: Agregar más usuarios/recursos
```
Twitter en 2006: 20K usuarios
Twitter en 2024: 500M usuarios
25,000x crecimiento
```

**Geographic Scalability**: Distribuir geográficamente
```
Latencia sin CDN:
  Usuario Tokyo → Server California: 150ms

Latencia con CDN:
  Usuario Tokyo → CDN Tokyo: 5ms
  30x mejora
```

**Administrative Scalability**: Múltiples organizaciones
```
Ejemplo: Internet
  - Miles de ISPs independientes
  - Diferentes políticas de seguridad
  - BGP para coordinar routing
```

**Técnicas de Escalabilidad**:
1. **Hiding communication latencies**: Async processing, caching
2. **Partitioning**: Sharding, consistent hashing
3. **Replication**: Read replicas, CDN

---

#### 3. Reliability & Availability

**Reliability**: Probabilidad de que el sistema funcione correctamente durante un período.

**Availability**: Proporción de tiempo que el sistema está operativo.

```
Availability = MTBF / (MTBF + MTTR)

MTBF: Mean Time Between Failures
MTTR: Mean Time To Repair

Ejemplo:
MTBF = 1000 horas
MTTR = 10 horas
Availability = 1000 / (1000 + 10) = 99%
```

**Improving Availability**:
- ⬆️ MTBF: Mejor hardware, testing
- ⬇️ MTTR: Auto-failover, monitoring

**Nines of Availability**:
```
99%     (two nines)   = 3.65 days downtime/year
99.9%   (three nines) = 8.76 hours downtime/year
99.99%  (four nines)  = 52.6 minutes downtime/year
99.999% (five nines)  = 5.26 minutes downtime/year
```

Google SRE target: **99.95% - 99.99%**

---

## 3. DESAFÍOS FUNDAMENTALES

### 3.1 Network is Unreliable

**Problemas de red**:
- Packets se pierden
- Packets llegan fuera de orden
- Packets se duplican
- Network partition (split brain)
- High latency / variable latency

**Ejemplo: Detecting Failure**

```python
import socket
import time

def check_server_health(host, port, timeout=5):
    """
    ¿Cómo saber si un server está muerto o solo lento?

    Problema: Timeout de 5 segundos.
    - Si no responde en 5s, ¿está muerto?
    - O simplemente latencia alta?
    - O network partition?
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return True  # Server alive
    except socket.timeout:
        return False  # Server dead? Or slow network?
    except socket.error:
        return False  # Definitely dead (connection refused)

# Dilema del timeout:
# - Timeout corto (1s): False positives (declarar muerto server vivo)
# - Timeout largo (30s): Slow to detect real failures
```

**No hay forma perfecta de distinguir "slow" vs "dead"!**

---

### 3.2 Clocks are Not Synchronized

**Problema**: Cada máquina tiene su propio reloj.

```python
# Server A timestamp
event_a = {'timestamp': 1638360000.123, 'event': 'User login'}

# Server B timestamp (reloj adelantado 2 segundos)
event_b = {'timestamp': 1638360002.456, 'event': 'User logout'}

# ¿Qué pasó primero?
# Según timestamps: Login → Logout
# Realidad: ¿Quién sabe? Relojes no sincronizados.
```

**Clock Skew**: Relojes se desvían (~100ms por día sin NTP).

**Soluciones**:
1. **NTP (Network Time Protocol)**: Sincronizar relojes (accuracy ~10ms)
2. **Logical Clocks**: No usar timestamps físicos (Lamport clocks, vector clocks)
3. **TrueTime (Google Spanner)**: Atomic clocks + GPS para bounded uncertainty

---

### 3.3 Partial Failures

**Problema**: Parte del sistema falla, resto funciona.

```
Ejemplo: Microservices
  Frontend → API Gateway → Auth Service ✅
                         → User Service ❌ (crashed)
                         → Order Service ✅

¿Qué hacer?
- ¿Fallar toda la request?
- ¿Degraded mode (funcionalidad limitada)?
- ¿Retry?
```

**Handling Partial Failures**:
1. **Circuit Breaker**: Stop calling failing service
2. **Graceful Degradation**: Continuar sin ese servicio
3. **Timeouts & Retries**: Con backoff exponencial

---

### 3.4 Concurrency

**Problema**: Múltiples procesos acceden al mismo recurso.

**Race Condition Example**:

```python
# Two servers incrementing counter simultaneously

# Server A
counter = redis.get('counter')  # Read: 10
counter += 1                    # Compute: 11
redis.set('counter', counter)   # Write: 11

# Server B (at the same time)
counter = redis.get('counter')  # Read: 10
counter += 1                    # Compute: 11
redis.set('counter', counter)   # Write: 11

# Expected: 12
# Actual: 11
# Lost update!
```

**Soluciones**:
1. **Locks**: Distributed locks (Redis, ZooKeeper)
2. **CAS (Compare-And-Swap)**: Atomic operations
3. **Optimistic Concurrency Control**: Version numbers

```python
# Solution: Redis atomic increment
redis.incr('counter')  # Atomic: guaranteed correct
```

---

## 4. FALLACIES OF DISTRIBUTED COMPUTING

**8 Fallacies** (Peter Deutsch, Sun Microsystems):

### 1. The Network is Reliable

❌ **Falso**: Packets se pierden (~1% packet loss típico).

**Implicación**: Siempre use retries, timeouts, idempotency.

---

### 2. Latency is Zero

❌ **Falso**: Network latency es significativa.

```
Same datacenter: 1-5ms
Cross-region: 50-150ms
Cross-continent: 150-300ms
```

**Implicación**: Minimize network calls, batch requests, cache aggressively.

---

### 3. Bandwidth is Infinite

❌ **Falso**: Network tiene límites.

```
Single server NIC: 10 Gbps
Saturated with: 10 Gbps / 1KB per request = 1.25M requests/sec
```

**Implicación**: Compress data, optimize payloads.

---

### 4. The Network is Secure

❌ **Falso**: Network can be intercepted (MITM attacks).

**Implicación**: Always encrypt (TLS), authenticate, authorize.

---

### 5. Topology Doesn't Change

❌ **Falso**: Servers added/removed, networks reconfigured.

**Implicación**: Service discovery (Consul, etcd), health checks.

---

### 6. There is One Administrator

❌ **Falso**: Multiple teams, organizations.

**Implicación**: Coordination protocols, SLAs, monitoring.

---

### 7. Transport Cost is Zero

❌ **Falso**: Network infrastructure costs money.

```
AWS data transfer out: $0.09/GB
Netflix streaming 15 EB/month → $1.35 billion/month (if using CloudFront alone)
Reason they built Open Connect!
```

---

### 8. The Network is Homogeneous

❌ **Falso**: Different protocols, hardware, OS.

**Implicación**: Use standard protocols (HTTP, gRPC), abstraction layers.

---

## 5. MODELOS DE COMUNICACIÓN

### 5.1 Synchronous vs Asynchronous

#### Synchronous Model

**Assumptions**:
- Message delivery time bounded (≤ D)
- Process execution speed bounded
- Clock drift bounded

**Pros**: Easier to reason about (can use timeouts to detect failures)
**Cons**: Unrealistic for real networks

---

#### Asynchronous Model

**Assumptions**:
- Message can take arbitrarily long (no bound)
- Process can be arbitrarily slow
- No clock synchronization

**Pros**: Realistic model
**Cons**: Harder to detect failures (can't distinguish slow vs dead)

**FLP Impossibility**: In async model, consensus is impossible if even 1 process can fail.

---

### 5.2 RPC (Remote Procedure Call)

**Idea**: Make remote call look like local function.

```python
# Local call
result = calculate_sum(a, b)

# RPC call (looks the same!)
result = remote_service.calculate_sum(a, b)
```

**Implementation (gRPC example)**:

```protobuf
// Define service
service Calculator {
  rpc Add(AddRequest) returns (AddResponse);
}

message AddRequest {
  int32 a = 1;
  int32 b = 2;
}

message AddResponse {
  int32 result = 1;
}
```

```python
# Server
class CalculatorServicer:
    def Add(self, request, context):
        result = request.a + request.b
        return AddResponse(result=result)

# Client
stub = CalculatorStub(channel)
response = stub.Add(AddRequest(a=5, b=3))
print(response.result)  # 8
```

**Challenges**:
- **Failure handling**: What if network fails mid-call?
- **Idempotency**: Can we retry safely?
- **Timeouts**: How long to wait?

---

### 5.3 Message Passing

**Alternatives to RPC**:

#### 1. Message Queue (Async)

```python
# Producer
queue.send('order_processing', {'order_id': 123, 'user_id': 456})
# Returns immediately, no blocking

# Consumer (different process/server)
for message in queue.receive('order_processing'):
    process_order(message)
```

**Pros**: Decoupled, handles backpressure
**Cons**: Eventual consistency, more complex

---

#### 2. Pub/Sub

```python
# Publisher
pubsub.publish('user_events', {'type': 'signup', 'user_id': 789})

# Multiple Subscribers
subscriber_1.subscribe('user_events')  # Email service
subscriber_2.subscribe('user_events')  # Analytics
subscriber_3.subscribe('user_events')  # Recommendations
```

---

## 6. FAILURE MODELS

### Taxonomy of Failures

```
Byzantine Failures (worst)
    ↑
Omission Failures
    ↑
Crash Failures
    ↑
Fail-Stop (ideal)
```

---

### 6.1 Fail-Stop Failures

**Definition**: Process stops, and others can detect it immediately.

**Example**: Process crashes, monitoring detects within 1 second.

**Reality**: Rarely exists (detection takes time).

---

### 6.2 Crash Failures (Fail-Silent)

**Definition**: Process stops, but others can't detect immediately.

**Example**: Server loses power, takes 30 seconds for healthcheck to timeout.

**Challenge**: Hard to distinguish crash vs slow network.

---

### 6.3 Omission Failures

**Types**:
- **Send Omission**: Process fails to send message
- **Receive Omission**: Process fails to receive message

**Example**: Network congestion causes packet loss.

---

### 6.4 Timing Failures

**Definition**: Process responds, but too late.

**Example**: Database query takes 10 seconds instead of 100ms.

**Impact**: Can trigger cascading failures if clients timeout.

---

### 6.5 Byzantine Failures

**Definition**: Process behaves arbitrarily (malicious or buggy).

**Examples**:
- Sends different messages to different processes
- Sends corrupted data
- Lies about its state

**Most difficult to handle**: Requires Byzantine Fault Tolerance (BFT).

**Use cases**: Blockchain, military systems, aerospace.

**Byzantine Generals Problem**: How to achieve consensus when some generals are traitors?

**Solution (simplified)**: Need **3f + 1** nodes to tolerate **f** Byzantine failures.

```
Example: Tolerate 1 Byzantine node → Need 4 nodes total
f = 1
3f + 1 = 3(1) + 1 = 4
```

---

## 7. TEOREMA CAP (REVISITED)

### CAP Theorem (Eric Brewer, 2000)

**Enunciado**: En un sistema distribuido con particiones de red, solo puedes garantizar 2 de 3:
- **C**onsistency (todos leen el último write)
- **A**vailability (todas las requests reciben respuesta)
- **P**artition Tolerance (sistema funciona a pesar de network partition)

### Deep Dive

**Realidad**: P (Partition tolerance) es inevitable.
- Networks WILL fail
- So the real choice is: **C vs A** durante partición.

---

### CP Systems

**Choice**: Consistency over Availability.

**Behavior during partition**:
- Some requests fail (unavailability)
- But all successful requests see consistent data

**Examples**:
- **HBase**: Si no puede alcanzar mayoría, rechaza writes
- **MongoDB**: Primary election, si no hay mayoría → read-only
- **ZooKeeper**: Quorum-based, no writes sin mayoría

**Use cases**: Banking, inventory management (correctness > availability)

---

### AP Systems

**Choice**: Availability over Consistency.

**Behavior during partition**:
- All requests succeed
- But data may be inconsistent (stale reads, conflicting writes)

**Examples**:
- **Cassandra**: Eventual consistency, always accepts writes
- **DynamoDB**: Multi-master, resolves conflicts later
- **Riak**: Vector clocks for conflict resolution

**Use cases**: Social media (like counters), DNS, caching

---

### CAP Trade-offs in Practice

**Reality**: Not binary. It's a spectrum.

```
Strong Consistency ←→ Eventual Consistency
                      ↑
                Most systems here
```

**Tunable Consistency** (Cassandra example):

```python
# Consistency level for reads/writes
session.execute(query, consistency_level=ConsistencyLevel.QUORUM)

# Options:
# ONE: Fastest, least consistent
# QUORUM: Balance (majority)
# ALL: Slowest, strongest consistency
```

---

## 8. TIME & ORDERING

### 8.1 Why Time Matters

**Use cases**:
- Ordering events (which happened first?)
- Detecting conflicts
- Cache expiration
- Distributed debugging

**Problem**: Physical clocks unreliable.

---

### 8.2 Happened-Before Relation (→)

**Definition** (Lamport, 1978):

Event A → Event B (A happened before B) if:
1. A and B in same process, A before B
2. A is send event, B is receive event (same message)
3. Transitivity: A → B and B → C implies A → C

If neither A → B nor B → A, events are **concurrent** (A || B).

---

### 8.3 Lamport Clocks

**Idea**: Logical clock that captures happened-before relationship.

**Rules**:
1. Each process has counter LC, initially 0
2. Before each event, increment: LC = LC + 1
3. When sending message, include LC in message
4. When receiving message with timestamp t: LC = max(LC, t) + 1

**Example**:

```
Process P:  Event   LC
            e1      1
            send(m) 2  (m.timestamp = 2)

Process Q:  Event      LC
            e2         1
            receive(m) 3  (max(1, 2) + 1)
            e3         4
```

**Implementation**:

```python
class LamportClock:
    def __init__(self):
        self.time = 0

    def tick(self):
        """Increment clock before local event."""
        self.time += 1
        return self.time

    def send(self, message):
        """Attach timestamp to message."""
        self.time += 1
        message['timestamp'] = self.time
        return message

    def receive(self, message):
        """Update clock on receive."""
        self.time = max(self.time, message['timestamp']) + 1
        return self.time

# Usage
clock = LamportClock()

# Local event
clock.tick()  # time = 1

# Send message
msg = clock.send({'data': 'hello'})  # time = 2, msg['timestamp'] = 2

# Receive message
incoming = {'data': 'world', 'timestamp': 5}
clock.receive(incoming)  # time = 6 (max(2, 5) + 1)
```

**Limitation**: LC(A) < LC(B) does NOT imply A → B (only necessary, not sufficient).

---

### 8.4 Vector Clocks

**Improvement**: Capture full causality.

**Idea**: Each process maintains vector of clocks for all processes.

**Rules**:
1. Process Pi increments VC[i] before each event
2. When sending, attach full vector VC
3. When receiving message with vector VC_m:
   - VC[j] = max(VC[j], VC_m[j]) for all j
   - VC[i] = VC[i] + 1

**Example** (3 processes):

```
Process P1: VC = [1, 0, 0]  (event e1)
            VC = [2, 0, 0]  (send to P2)

Process P2: VC = [0, 1, 0]  (event e2)
            VC = [2, 2, 0]  (receive from P1, then increment)
            VC = [2, 3, 0]  (event e3)

Process P3: VC = [0, 0, 1]  (event e4)
            VC = [2, 3, 2]  (receive from P2)
```

**Comparing Vector Clocks**:

```python
def vector_clock_compare(vc1, vc2):
    """
    Returns:
    - 'before' if vc1 < vc2 (vc1 happened before vc2)
    - 'after' if vc1 > vc2
    - 'concurrent' if concurrent
    """
    less_equal = all(vc1[i] <= vc2[i] for i in range(len(vc1)))
    greater_equal = all(vc1[i] >= vc2[i] for i in range(len(vc1)))

    if less_equal and not greater_equal:
        return 'before'
    elif greater_equal and not less_equal:
        return 'after'
    else:
        return 'concurrent'

# Example
vc1 = [2, 1, 0]
vc2 = [2, 2, 1]
print(vector_clock_compare(vc1, vc2))  # 'before'

vc3 = [1, 2, 0]
vc4 = [2, 1, 0]
print(vector_clock_compare(vc3, vc4))  # 'concurrent'
```

**Use case**: DynamoDB, Riak (conflict detection).

---

## 9. CASOS DE ESTUDIO

### 9.1 Amazon DynamoDB

**Architecture**:
- Distributed key-value store
- **AP system** (availability over consistency)
- Eventual consistency
- Vector clocks for conflict resolution

**Partitioning**: Consistent hashing
**Replication**: N replicas (typically N=3)
**Quorum**: R + W > N (R = read quorum, W = write quorum)

**Example**:
```
N = 3 replicas
W = 2 (write to 2 replicas)
R = 2 (read from 2 replicas)
R + W = 4 > 3 ✅ Guarantees overlap
```

**Conflict Resolution**: Application-level (using vector clocks).

---

### 9.2 Google Spanner

**Architecture**:
- Globally distributed SQL database
- **CP system** (consistency over availability during partition)
- Strong consistency (linearizability)
- Uses TrueTime API

**TrueTime**:
- API returns time interval: [earliest, latest]
- Uncertainty typically < 7ms
- Uses atomic clocks + GPS

**Example**:
```
TT.now() = [10:00:00.123, 10:00:00.130]
Uncertainty = 7ms

Spanner waits for uncertainty window before committing
→ Guarantees external consistency
```

---

### 9.3 Apache Kafka

**Architecture**:
- Distributed commit log
- **Partitioned** topics
- **Replicated** for fault tolerance

**Ordering Guarantees**:
- Per-partition ordering (not global)
- Consumer groups for parallel processing

**Example**:

```python
# Producer: Messages to same partition are ordered
producer.send('orders', key='user_123', value=order_data)
# key='user_123' → always goes to same partition → ordering guaranteed

# Consumer
consumer = KafkaConsumer('orders', group_id='order_processors')
for message in consumer:
    process_order(message.value)
```

---

## 10. EJERCICIOS

### Ejercicio 1: Detecting Failure

**Pregunta**: Diseña un sistema para detectar si un server está muerto.

**Considera**:
- Network puede ser lento (50-200ms variable latency)
- Tolerar false positives (declarar muerto cuando está vivo) costaría $10K
- Tolerar false negatives (no detectar muerte) costaría $1K
- ¿Qué timeout usarías?

---

### Ejercicio 2: Implementing Distributed Counter

**Tarea**: Implementa un contador distribuido que incremente atómicamente.

```python
# Múltiples servers incrementan concurrentemente
# Requiere: Correctness (sin lost updates)

def distributed_increment(key):
    # TODO: Implement using Redis
    pass
```

**Hints**: Redis INCR, Lua scripts, optimistic locking

---

### Ejercicio 3: Event Ordering

**Escenario**:
```
User A: Post tweet (Server 1, timestamp 12:00:00.500)
User B: Like tweet (Server 2, timestamp 12:00:00.480)

Server 2 clock está adelantado 50ms.
```

**Preguntas**:
1. ¿Cómo detectar que Like ocurrió ANTES de Post (imposible)?
2. ¿Qué sistema usarías? (Lamport clocks, Vector clocks, o TrueTime)

---

### Ejercicio 4: CAP Trade-off

**Escenario**: Diseñas un shopping cart system.

**Requirements**:
- Users add items to cart
- Checkout process
- Global deployment (US, EU, APAC)

**Pregunta**: ¿CP o AP? Justifica.

**Hints**:
- Consider: ¿Qué pasa si user agrega item en cart durante network partition?
- ¿Es aceptable perder items? (AP → eventual consistency, posibles lost updates)
- ¿O mejor rechazar request? (CP → strong consistency, pero disponibilidad reducida)

---

## 📚 CHEAT SHEET

### Conceptos Clave

```
Distributed System: Colección de entidades autónomas que aparecen como sistema único

Challenges:
- Network unreliable
- Clocks not synchronized
- Partial failures
- Concurrency

CAP Theorem: C + A + P, pick 2 (realidad: P inevitable, choose C o A)

Consistency Models:
Strong → Linearizability → Sequential → Causal → Eventual
```

### Failure Models

```
Byzantine (worst) → Omission → Crash → Fail-Stop (ideal)

Byzantine: 3f + 1 nodes needed to tolerate f failures
```

### Time & Ordering

```
Lamport Clocks: Capture happened-before (partial order)
Vector Clocks: Capture full causality (detect concurrency)
TrueTime: Bounded uncertainty (Spanner)
```

### Comparison

| Aspecto | CP Systems | AP Systems |
|---------|-----------|------------|
| **Consistency** | Strong | Eventual |
| **Availability** | Lower | Higher |
| **Partition** | Reject requests | Accept all |
| **Use cases** | Banking, inventory | Social media, DNS |
| **Examples** | Spanner, MongoDB | Cassandra, DynamoDB |

---

## 🎯 PRÓXIMOS PASOS

Has completado **Fundamentos de Sistemas Distribuidos**. Key takeaways:

1. ✅ **Distributed systems** son inevitables para escalar
2. ✅ **Network is unreliable** - diseña para fallos
3. ✅ **Clocks can't be trusted** - use logical clocks
4. ✅ **CAP theorem** - choose C or A during partition
5. ✅ **Fallacies** - no asumas nada sobre la red
6. ✅ **Failure models** - desde crash hasta Byzantine

**Próximo**: Semana 9 - **Consensus Algorithms** (Paxos, Raft)

Consensus es el problema central en distributed systems:
- ¿Cómo múltiples nodes acuerdan un valor?
- A pesar de fallos, latencia, particiones
- Usado en: Leader election, replication, distributed locks

---

**Creado**: 2024-12-08
**Versión**: 1.0
**Parte de**: Fase 1 - Distributed Systems Core
