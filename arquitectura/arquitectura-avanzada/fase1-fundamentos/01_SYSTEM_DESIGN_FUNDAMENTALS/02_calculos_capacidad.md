# Cálculos de Capacidad (Back-of-Envelope Calculations)
## La Habilidad Más Importante de un Arquitecto

**Autor:** Staff Software Architect
**Versión:** 1.0
**Fecha:** 2024-12-03
**Tiempo de lectura:** 60 minutos
**Nivel:** Intermedio → Experto

---

## 📋 ÍNDICE

1. [¿Por Qué Son Críticos Estos Cálculos?](#por-que)
2. [Números que Debes Memorizar](#numeros-memorizar)
3. [Metodología de Estimación](#metodologia)
4. [Tipos de Cálculos](#tipos-calculos)
5. [20 Ejemplos Resueltos](#ejemplos-resueltos)
6. [Errores Comunes](#errores-comunes)
7. [Trucos y Atajos](#trucos)
8. [Ejercicios de Práctica](#ejercicios)
9. [Cheat Sheet](#cheat-sheet)

---

## 1. ¿POR QUÉ SON CRÍTICOS ESTOS CÁLCULOS? {#por-que}

### El Problema

**Escenario real en entrevista:**
```
Entrevistador: "¿Cuántos servidores necesitamos para manejar Instagram?"

Candidato A (sin cálculos):
"Mmm... ¿muchos? ¿100? ¿1000?"
→ ❌ RECHAZADO

Candidato B (con cálculos):
"Déjame calcular:
- 500M DAU × 50 photos viewed/day = 25B requests/day
- 25B / 86,400 sec = 290K QPS
- Si cada servidor maneja 1K QPS → 290 servidores mínimo
- Con redundancia 3x → ~900 servidores"
→ ✅ APROBADO
```

### Por Qué Importa

1. **Dimensionamiento de infraestructura**
   - ¿Cuántos servidores?
   - ¿Cuánto storage?
   - ¿Cuánto bandwidth?

2. **Estimación de costos**
   - AWS/GCP pricing
   - ROI de proyectos
   - Budget planning

3. **Identificación de bottlenecks**
   - ¿Dónde está el cuello de botella?
   - ¿DB? ¿Network? ¿CPU?

4. **Trade-offs informados**
   - "¿Vale la pena cachear esto?"
   - "¿Necesitamos sharding?"
   - "¿Cuándo necesitamos CDN?"

5. **Credibilidad técnica**
   - Demuestra profundidad técnica
   - Pensamiento estructurado
   - Experiencia real

---

## 2. NÚMEROS QUE DEBES MEMORIZAR {#numeros-memorizar}

### 🔢 Tabla Maestra de Latencias

| Operación | Latencia | Contexto |
|-----------|----------|----------|
| **CPU** | | |
| L1 cache reference | 0.5 ns | |
| Branch mispredict | 5 ns | |
| L2 cache reference | 7 ns | 14x L1 |
| Mutex lock/unlock | 100 ns | |
| **Memory** | | |
| Main memory reference | 100 ns | 20x L2, 200x L1 |
| **Disk/Network** | | |
| SSD random read | 150 μs | 1,000x memory |
| Send 1K bytes over 1 Gbps network | 10 μs | |
| Read 1 MB sequentially from memory | 250 μs | |
| Round trip within same datacenter | 500 μs | |
| Read 1 MB sequentially from SSD | 1 ms | 4x memory, 10x network |
| **Disk** | | |
| Disk seek | 10 ms | 20x datacenter RT, 80x SSD |
| Read 1 MB sequentially from disk | 30 ms | 3x disk seek |
| **Network** | | |
| Send packet CA → Netherlands → CA | 150 ms | |

### 📊 Potencias de 2 (Para Conversiones Rápidas)

```
2^10 = 1,024         ≈ 1 thousand (K)
2^20 = 1,048,576     ≈ 1 million (M)
2^30 = 1,073,741,824 ≈ 1 billion (B)
2^40 ≈ 1 trillion (T)
```

### 💾 Unidades de Almacenamiento

```
1 Byte = 8 bits
1 KB = 1,000 Bytes = 10^3 bytes
1 MB = 1,000 KB = 10^6 bytes
1 GB = 1,000 MB = 10^9 bytes
1 TB = 1,000 GB = 10^12 bytes
1 PB = 1,000 TB = 10^15 bytes
```

### ⏰ Conversiones de Tiempo

```
1 second = 1,000 ms = 1,000,000 μs = 1,000,000,000 ns

1 minute = 60 seconds
1 hour = 60 minutes = 3,600 seconds
1 day = 24 hours = 86,400 seconds ≈ 100,000 seconds (10^5)
1 week ≈ 600,000 seconds
1 month (30 días) ≈ 2.5 million seconds (2.5 × 10^6)
1 year (365 días) ≈ 31.5 million seconds (3 × 10^7)
```

### 🌐 Disponibilidad (Availability)

```
Availability    Downtime/Year    Downtime/Month    Downtime/Week
99%             3.65 days        7.31 hours        1.68 hours
99.9%           8.77 hours       43.83 minutes     10.08 minutes
99.99%          52.60 minutes    4.38 minutes      1.01 minutes
99.999%         5.26 minutes     26.30 seconds     6.05 seconds
99.9999%        31.56 seconds    2.63 seconds      604.80 ms
```

### 📈 Capacidades Típicas de Servidores

```
Single Server Capacity (Modern Hardware):
- CPU: 64 cores
- RAM: 256 GB
- Disk: 4 TB SSD
- Network: 10 Gbps
- Handles: 1K-10K QPS (depending on workload)

Database Server:
- MySQL: ~1K QPS (complex queries)
- PostgreSQL: ~1K-5K QPS
- Cassandra: ~10K-50K writes/sec per node
- Redis: ~100K ops/sec per node
- MongoDB: ~10K writes/sec

Web Server:
- NGINX: ~50K connections
- Apache: ~10K connections
```

---

## 3. METODOLOGÍA DE ESTIMACIÓN {#metodologia}

### Proceso de 5 Pasos

```
1. CLARIFY → Entender qué estimar
2. BREAKDOWN → Descomponer en partes
3. ESTIMATE → Calcular cada parte
4. AGGREGATE → Sumar todo
5. SANITY CHECK → Verificar razonabilidad
```

### Técnicas de Aproximación

#### ✅ Redondear Agresivamente

```
❌ Mal: "86,427 segundos por día"
✅ Bien: "~100,000 segundos por día (10^5)"

❌ Mal: "1,048,576"
✅ Bien: "~1 million (10^6)"
```

**Regla:** Usa potencias de 10 o factores simples (2, 5, 10)

#### ✅ Notación Científica

```
1,000 = 10^3 = 1K
1,000,000 = 10^6 = 1M
1,000,000,000 = 10^9 = 1B
```

#### ✅ Orden de Magnitud

```
"¿Es 100, 1,000, 10,000, o 100,000?"
```

Estar dentro de 1 orden de magnitud es suficiente en entrevistas.

---

## 4. TIPOS DE CÁLCULOS {#tipos-calculos}

### 4.1 Cálculo de QPS (Queries Per Second)

**Fórmula Base:**
```
QPS = (Total Daily Requests) / 86,400 seconds
```

**Con Peak Factor:**
```
Average QPS = Daily Requests / 86,400
Peak QPS = Average QPS × Peak Factor

Peak Factor típico:
- General: 2-3x
- E-commerce (Black Friday): 5-10x
- Streaming (live events): 10-20x
- Social (breaking news): 10-50x
```

**Ejemplo Completo: YouTube**

```
Datos:
- 2 billion logged-in users monthly
- 1 billion hours watched daily
- Average video length: 10 minutes

Paso 1: Calcular videos watched per day
= 1B hours × 60 minutes / 10 minutes per video
= 6B videos/day

Paso 2: Calcular video requests (considerando buffering)
= 6B videos × 20 requests (chunks) per video
= 120B requests/day

Paso 3: Calcular Average QPS
= 120B / 86,400
≈ 1.4M QPS

Paso 4: Calcular Peak QPS (factor 3x)
= 1.4M × 3
≈ 4M QPS
```

---

### 4.2 Cálculo de Storage

**Fórmula Base:**
```
Total Storage = Item Count × Item Size × Retention Period
```

**Con Replicación:**
```
Total Storage = Base Storage × Replication Factor × (1 + Overhead)

Replication Factor típico:
- Single region: 3 copies
- Multi-region: 3 copies per region

Overhead típico:
- Indexes: 10-20%
- Backups: 100% (1 full copy)
- Snapshots: 20-50%
```

**Ejemplo Completo: WhatsApp Messages**

```
Datos:
- 2B users
- 100 messages/day per user
- Message size: 100 bytes (text only)
- Retention: 30 days

Paso 1: Messages per day
= 2B users × 100 messages
= 200B messages/day

Paso 2: Storage per day
= 200B × 100 bytes
= 20 TB/day

Paso 3: Storage for 30 days
= 20 TB × 30
= 600 TB

Paso 4: With replication (3x)
= 600 TB × 3
= 1.8 PB

Paso 5: With overhead (indexes 20%)
= 1.8 PB × 1.2
≈ 2.2 PB

Final: ~2.2 PB for 30-day retention
```

---

### 4.3 Cálculo de Bandwidth

**Fórmula Base:**
```
Bandwidth = QPS × Payload Size

Incoming Bandwidth = Write QPS × Request Size
Outgoing Bandwidth = Read QPS × Response Size
```

**Ejemplo Completo: Instagram Feed**

```
Datos:
- 500M DAU
- 50 photos viewed per day
- Photo size: 500 KB (compressed)
- Users upload 0.5 photos/day
- Upload size: 2 MB (original)

Paso 1: Read QPS
= (500M × 50) / 86,400
= 290K QPS

Paso 2: Outgoing Bandwidth
= 290K QPS × 500 KB
= 145 GB/second

Paso 3: Write QPS
= (500M × 0.5) / 86,400
= 2.9K QPS

Paso 4: Incoming Bandwidth
= 2.9K QPS × 2 MB
= 5.8 GB/second

Paso 5: Total Bandwidth
= 145 GB/s + 5.8 GB/s
≈ 151 GB/s
```

**Conversión a Monthly Cost (AWS):**
```
Outgoing bandwidth (AWS pricing):
- First 10 TB: $0.09/GB
- Next 40 TB: $0.085/GB
- Next 100 TB: $0.07/GB
- Above 150 TB: $0.05/GB

Monthly data transfer:
= 145 GB/s × 86,400 sec/day × 30 days
= 376 PB/month

Cost (using $0.05/GB for bulk):
≈ $19 million/month just for bandwidth!
```

---

### 4.4 Cálculo de Memory (Cache)

**Regla 80-20:**
```
20% of content generates 80% of traffic
→ Cache the hot 20%
```

**Fórmula:**
```
Cache Size = Hot Data Size × Cache Coverage

Hot Data Size = Total Data × 0.2 (20%)
Cache Coverage = 0.8 (80% hit rate)
```

**Ejemplo Completo: Twitter Timeline Cache**

```
Datos:
- 200M DAU
- 10 timeline reads per day per user
- Timeline: 20 tweets × 500 bytes = 10 KB

Paso 1: Total timeline requests per day
= 200M × 10
= 2B requests/day

Paso 2: Unique users (hot 20%)
= 200M × 0.2
= 40M users

Paso 3: Cache size
= 40M users × 10 KB per timeline
= 400 GB

Paso 4: With Redis overhead (1.5x)
= 400 GB × 1.5
= 600 GB

Final: 600 GB Redis cache for 80% hit rate
```

---

### 4.5 Cálculo de Database Sharding

**Cuándo necesitas sharding:**
```
Single DB capacity:
- Storage: ~2-4 TB (practical limit before performance degrades)
- QPS: ~1K-5K (depending on query complexity)
- Connections: ~10K concurrent

If you exceed any of these → Need sharding
```

**Fórmula:**
```
Number of Shards = max(
    Total Storage / Single DB Capacity,
    Total QPS / Single DB QPS,
    Total Connections / Single DB Connections
)
```

**Ejemplo Completo: Facebook Posts**

```
Datos:
- 2B users
- 5 posts per user per month
- Post size: 1 KB
- Retention: 10 years
- Read:Write ratio: 100:1

Paso 1: Total posts
= 2B users × 5 posts/month × 12 months × 10 years
= 1.2 trillion posts

Paso 2: Total storage
= 1.2T posts × 1 KB
= 1.2 PB

Paso 3: Number of shards (storage-based)
= 1.2 PB / 2 TB per shard
= 600 shards

Paso 4: Write QPS
= (2B × 5) / (30 days × 86,400)
≈ 4K writes/sec

Paso 5: Read QPS
= 4K × 100
= 400K reads/sec

Paso 6: Number of shards (QPS-based)
= 400K / 5K per shard
= 80 shards

Final: Need 600 shards (storage is bottleneck)
```

---

## 5. 20 EJEMPLOS RESUELTOS {#ejemplos-resueltos}

### Ejemplo 1: Netflix Bandwidth

**Pregunta:** ¿Cuánto bandwidth necesita Netflix?

```
Datos:
- 200M subscribers
- 2 hours watched per day per subscriber
- Video quality: 5 Mbps (1080p)

Cálculo:
Concurrent viewers:
= 200M × (2 hours / 24 hours)
= 16.7M concurrent

Bandwidth:
= 16.7M × 5 Mbps
= 83.5 Tbps (Terabits per second)

En GB/second:
= 83.5 Tbps / 8
≈ 10.4 TB/second

Monthly data transfer:
= 10.4 TB/s × 86,400 × 30
≈ 27 EB (Exabytes) per month
```

---

### Ejemplo 2: Uber GPS Updates

**Pregunta:** ¿Cuántas GPS updates procesa Uber?

```
Datos:
- 5M drivers active simultaneously (peak)
- GPS update every 5 seconds

Cálculo:
Updates per second:
= 5M drivers / 5 seconds
= 1M updates/second

Updates per day:
= 1M × 86,400
= 86.4B updates/day

Storage per day (assuming 100 bytes per update):
= 86.4B × 100 bytes
= 8.6 TB/day

Storage per year:
= 8.6 TB × 365
≈ 3.1 PB/year
```

---

### Ejemplo 3: Google Search Index

**Pregunta:** ¿Cuánto storage necesita Google para su index?

```
Estimación:
- 1 trillion web pages indexed
- Average page size: 100 KB
- Compression ratio: 10:1
- Inverted index overhead: 2x

Cálculo:
Raw storage:
= 1T pages × 100 KB
= 100 PB

Compressed:
= 100 PB / 10
= 10 PB

With inverted index:
= 10 PB × 2
= 20 PB

With replication (3x):
= 20 PB × 3
= 60 PB

Final: ~60-100 PB for web index
```

---

### Ejemplo 4: Twitter Tweets Storage

**Pregunta:** ¿Cuánto cuesta almacenar todos los tweets?

```
Datos:
- 400M tweets per day
- Average tweet: 280 chars = 280 bytes
- Metadata: 200 bytes
- Total per tweet: 500 bytes
- Retention: Forever (15 years so far)

Cálculo:
Daily storage:
= 400M × 500 bytes
= 200 GB/day

15 years storage:
= 200 GB × 365 × 15
≈ 1.1 PB

With replication (3x):
= 1.1 PB × 3
= 3.3 PB

AWS S3 cost (Standard):
= 3.3 PB × $0.023/GB
= 3,300,000 GB × $0.023
≈ $76,000/month

With S3 Intelligent Tiering (avg $0.015/GB):
≈ $50,000/month

Final: ~$50K-$76K/month storage cost
```

---

### Ejemplo 5: Zoom Video Conferencing

**Pregunta:** ¿Cuánto bandwidth necesita Zoom?

```
Datos:
- 300M daily meeting participants (peak COVID)
- Average meeting: 45 minutes
- Video quality: 1.5 Mbps (720p)

Cálculo:
Concurrent users (assuming not all at once):
= 300M × (45 min / 480 min working day)
≈ 28M concurrent

Bandwidth per user:
= 1.5 Mbps upload + 1.5 Mbps download (1-to-1)
= 3 Mbps

For group calls (5 people):
= 1.5 Mbps upload + (1.5 Mbps × 4) download
= 7.5 Mbps per person

Average bandwidth per user:
≈ 5 Mbps

Total bandwidth:
= 28M × 5 Mbps
= 140 Tbps

Cost implications:
This is why Zoom uses:
- P2P for small calls (< 3 people)
- Selective forwarding for larger calls
- CDN for webinars
```

---

### Ejemplo 6: Spotify Music Storage

**Pregunta:** ¿Cuánto storage necesita Spotify?

```
Datos:
- 70M songs in catalog
- Average song: 4 minutes
- Bitrate: 320 kbps (high quality)
- Multiple quality levels: 320, 160, 96 kbps
- Multiple formats: Ogg Vorbis, AAC

Cálculo:
Storage per song (320 kbps):
= (320 kbps / 8) × 240 seconds
= 40 KB/s × 240s
= 9.6 MB

Total for 70M songs (single quality):
= 70M × 9.6 MB
= 672 TB

With 3 quality levels:
= 672 TB × 3
≈ 2 PB

With replication (3x):
= 2 PB × 3
= 6 PB

With backups and overhead:
≈ 10 PB total

Monthly cost (S3):
≈ $230K/month
```

---

### Ejemplo 7: GitHub Code Storage

**Pregunta:** ¿Cuánto storage usa GitHub?

```
Datos:
- 100M repositories
- Average repo size: 50 MB
- Git overhead: 2x (history, branches, etc.)

Cálculo:
Raw storage:
= 100M × 50 MB
= 5 PB

With Git overhead:
= 5 PB × 2
= 10 PB

With replication (3x):
= 10 PB × 3
= 30 PB

With incremental backups:
≈ 40 PB total

Note: GitHub usa deduplication agresiva
Real storage probably closer to 20-25 PB
```

---

### Ejemplo 8: TikTok Video Processing

**Pregunta:** ¿Cuánto cuesta procesar videos en TikTok?

```
Datos:
- 1B videos uploaded per day
- Average video: 30 seconds
- Raw upload: 1080p, 30 fps, ~50 MB
- Need to encode: 720p, 480p, 360p

Cálculo:
Daily uploads storage:
= 1B × 50 MB
= 50 PB/day

Encoding cost (AWS MediaConvert):
= $0.015 per minute of output

Total encoding minutes per day:
= 1B videos × 30 seconds × 3 outputs
= 1B × 1.5 minutes
= 1.5B minutes

Daily encoding cost:
= 1.5B × $0.015
= $22.5M/day
= $675M/month

This is why TikTok:
- Uses custom encoding pipeline
- Encodes on-demand (not all qualities upfront)
- Caches popular videos aggressively
```

---

### Ejemplo 9: Amazon Orders Database

**Pregunta:** ¿Cuántas rows tiene la orders table de Amazon?

```
Datos:
- 300M customers
- 10 orders per year per customer (average)
- Amazon history: 25 years

Cálculo:
Total orders:
= 300M customers × 10 orders/year × 25 years
= 75B orders

Each order:
- Order row: 500 bytes
- Order items (avg 3): 3 × 300 bytes = 900 bytes
- Total: 1.4 KB per order

Total storage:
= 75B × 1.4 KB
= 105 TB (orders data)

With indexes (3x):
= 105 TB × 3
= 315 TB

With replication (3x):
= 315 TB × 3
≈ 1 PB

Sharding strategy:
= 1 PB / 2 TB per shard
= 500 shards

Probably shard by: hash(customer_id)
```

---

### Ejemplo 10: LinkedIn Connections Graph

**Pregunta:** ¿Cuántas connections almacena LinkedIn?

```
Datos:
- 800M users
- Average connections: 500 per user
- Bidirectional (stored twice)

Cálculo:
Total connections:
= 800M × 500
= 400B connections

Each connection record: 16 bytes (user_id1, user_id2)

Total storage:
= 400B × 16 bytes
= 6.4 TB

With indexes (for queries like "mutual connections"):
= 6.4 TB × 5
= 32 TB

Graph database overhead (Neo4j):
≈ 10x raw data
= 64 TB

With replication:
= 64 TB × 3
≈ 200 TB

This fits in memory of a large cluster!
LinkedIn likely keeps this hot in RAM for fast queries.
```

---

### Ejemplo 11: WhatsApp Messages

**Pregunta:** ¿Cuántos mensajes procesa WhatsApp por segundo?

```
Datos:
- 2B users
- 100 messages per day per user
- Peak hours: 8am-10pm (14 hours)

Cálculo:
Messages per day:
= 2B × 100
= 200B messages/day

Average QPS:
= 200B / 86,400
≈ 2.3M messages/second

Peak QPS (assuming 14-hour active period):
= 200B / (14 hours × 3,600)
≈ 4M messages/second

With 5x spike during breaking news:
= 20M messages/second

This is why WhatsApp uses:
- Erlang (handles millions of connections)
- FreeBSD (custom network stack)
- Heavily sharded Mnesia database
```

---

### Ejemplo 12: Dropbox File Sync

**Pregunta:** ¿Cuánto bandwidth usa Dropbox?

```
Datos:
- 700M users
- 20% active daily
- Average upload: 50 MB/day
- Average download: 100 MB/day (sync across devices)

Cálculo:
Active users:
= 700M × 0.2
= 140M/day

Daily uploads:
= 140M × 50 MB
= 7 PB/day

Daily downloads:
= 140M × 100 MB
= 14 PB/day

Bandwidth:
Upload: 7 PB / 86,400 = 81 GB/second
Download: 14 PB / 86,400 = 162 GB/second

Monthly bandwidth cost (AWS):
= (7 + 14) PB × 30 days × $0.05/GB
= 630 PB × $0.05/GB
≈ $31.5M/month

This is why Dropbox:
- Built their own datacenters (Magic Pocket)
- Uses block-level deduplication
- Only syncs changed blocks, not whole files
```

---

### Ejemplo 13: Reddit Comments

**Pregunta:** ¿Cuántos comments se hacen en Reddit?

```
Datos:
- 52M DAU
- 10 comments per user per day
- Comment size: 500 bytes average

Cálculo:
Comments per day:
= 52M × 10
= 520M comments/day

Write QPS:
= 520M / 86,400
≈ 6K writes/second

Storage per day:
= 520M × 500 bytes
= 260 GB/day

Storage per year:
= 260 GB × 365
= 95 TB/year

Reddit history (15 years):
= 95 TB × 15
= 1.4 PB

With replication:
= 1.4 PB × 3
≈ 4.2 PB

Note: Old comments get archived (compressed + read-only)
Probably closer to 2-3 PB in practice
```

---

### Ejemplo 14: Steam Game Downloads

**Pregunta:** ¿Cuánto bandwidth necesita Steam?

```
Datos:
- 120M monthly active users
- 10% download a game per month
- Average game size: 50 GB

Cálculo:
Downloads per month:
= 120M × 0.1
= 12M downloads

Monthly data transfer:
= 12M × 50 GB
= 600 PB

Peak (new AAA game release):
= 10M downloads in first week
= 500 PB in one week
= 71 PB/day
= 823 GB/second

This is why Steam:
- Uses CDN (Akamai, CloudFlare)
- P2P downloads (Steam Datagram Relay)
- Regional download servers
- Download scheduling (off-peak hours)
```

---

### Ejemplo 15: Airbnb Search Queries

**Pregunta:** ¿Cuántas búsquedas procesa Airbnb?

```
Datos:
- 150M users
- 5% search per day
- 10 searches per session

Cálculo:
Searching users per day:
= 150M × 0.05
= 7.5M users

Searches per day:
= 7.5M × 10
= 75M searches/day

Search QPS:
= 75M / 86,400
≈ 868 searches/second

Peak (vacation planning season, 5x):
≈ 4,300 searches/second

Each search:
- Query Elasticsearch: 50ms
- Rank results: 50ms
- Fetch details: 100ms
- Total: 200ms

Server capacity needed:
= 4,300 QPS × 200ms
= 860 concurrent requests
≈ 100 servers (at 10 concurrent per server)
```

---

### Ejemplo 16: Tesla Autopilot Data

**Pregunta:** ¿Cuántos datos genera la flota de Tesla?

```
Datos:
- 3M Tesla vehicles with Autopilot
- 10% using Autopilot actively
- 8 cameras + sensors generating 1 GB/hour

Cálculo:
Active Autopilot vehicles:
= 3M × 0.1
= 300K vehicles

Data per hour:
= 300K × 1 GB
= 300 TB/hour

Data per day (assuming 2 hours average use):
= 300 TB × 2
= 600 TB/day

Data per year:
= 600 TB × 365
= 219 PB/year

Cost to upload (cellular data at $10/GB):
= 600 TB × $10/GB
= $6M/day
= $2.2B/year

This is why Tesla:
- Only uploads "interesting" events (shadow mode)
- Uploads over WiFi when parked at home
- Heavily compresses data
- Samples randomly (1% of trips)
Actual uploads probably 1-2 PB/year
```

---

### Ejemplo 17: ChatGPT Requests

**Pregunta:** ¿Cuántas requests procesa ChatGPT?

```
Datos:
- 100M weekly active users
- 10 prompts per session
- 2 sessions per week per user

Cálculo:
Prompts per week:
= 100M × 10 × 2
= 2B prompts/week

Prompts per day:
= 2B / 7
≈ 286M/day

Average QPS:
= 286M / 86,400
≈ 3,300 prompts/second

Peak QPS (3x):
≈ 10,000 prompts/second

Compute cost per prompt:
- GPT-3.5: $0.002 per 1K tokens
- Average: 1K tokens input + 500 tokens output = 1.5K tokens
- Cost: $0.003 per prompt

Daily compute cost:
= 286M × $0.003
= $858K/day
= $25.7M/month

This is why OpenAI:
- Has usage tiers (free, plus, enterprise)
- Rate limits aggressively
- Batch requests when possible
- Uses model distillation (smaller models)
```

---

### Ejemplo 18: Twitch Live Streaming

**Pregunta:** ¿Cuánto bandwidth usa Twitch?

```
Datos:
- 7M concurrent viewers (peak)
- 200K concurrent streamers
- Average bitrate: 6 Mbps (1080p60)

Cálculo:
Viewer bandwidth (download):
= 7M viewers × 6 Mbps
= 42 Tbps

Streamer bandwidth (upload):
= 200K streamers × 6 Mbps
= 1.2 Tbps

Total bandwidth:
≈ 43 Tbps

Monthly data transfer:
= 42 Tbps / 8 × 86,400 × 30
≈ 13.6 EB/month (viewers)

CDN cost (at $0.02/GB with volume discounts):
= 13.6 EB × $0.02/GB
≈ $272M/month

This is why Twitch:
- Uses Amazon CloudFront (owned by AWS)
- Transcodes to multiple qualities
- Aggressive caching of popular streams
- P2P for very popular streams
```

---

### Ejemplo 19: Stripe Payment Transactions

**Pregunta:** ¿Cuántas transacciones procesa Stripe?

```
Datos:
- Millions of businesses use Stripe
- Estimate: 1B transactions/year globally
- Peak (Black Friday): 10x normal

Cálculo:
Transactions per year:
= 1B

Transactions per day:
= 1B / 365
≈ 2.7M/day

Average TPS:
= 2.7M / 86,400
≈ 31 transactions/second

Peak TPS (Black Friday):
≈ 310 transactions/second

Each transaction record: 5 KB (payment details, metadata, etc.)

Storage per year:
= 1B × 5 KB
= 5 TB/year

10 years storage:
= 50 TB

With replication + backups:
≈ 200 TB

Database requirements:
- ACID compliance (financial data)
- Multi-region for compliance (GDPR)
- Point-in-time recovery
- Encryption at rest

Probably uses:
- PostgreSQL with Citus (sharding)
- Or Aurora with cross-region replication
```

---

### Ejemplo 20: Wikipedia Page Views

**Pregunta:** ¿Cuántos page views tiene Wikipedia?

```
Datos:
- 20B page views per month
- 60M articles
- Average article: 50 KB (HTML)

Cálculo:
Page views per day:
= 20B / 30
≈ 667M/day

Average QPS:
= 667M / 86,400
≈ 7,700 requests/second

Storage for articles:
= 60M × 50 KB
= 3 TB

With images and media:
≈ 100 TB total

With replication:
≈ 300 TB

Bandwidth:
= 7,700 QPS × 50 KB
= 385 MB/second
= 1 PB/month

Wikipedia optimizations:
- Varnish cache (99% hit rate)
- CDN for images
- Multiple edge locations
- Read-heavy, writes are rare
- Can cache aggressively (content doesn't change often)
```

---

## 6. ERRORES COMUNES {#errores-comunes}

### ❌ Error 1: No Redondear

```
Mal: "86,427 segundos por día"
Bien: "~100K segundos (10^5)"

Mal: "1,048,576 bytes"
Bien: "~1 MB"
```

### ❌ Error 2: Demasiada Precisión

```
Mal: "Se necesitan exactamente 284.7 servidores"
Bien: "Se necesitan ~300 servidores"
```

### ❌ Error 3: Olvidar Peak Factor

```
Mal: Average QPS = 1K → 1 servidor
Bien: Average 1K, Peak 3K → 3 servidores + buffer
```

### ❌ Error 4: Olvidar Replicación

```
Mal: Storage = 100 TB
Bien: Storage = 100 TB × 3 (replication) = 300 TB
```

### ❌ Error 5: No Hacer Sanity Check

```
Resultado: "Netflix necesita 1 Gbps"
Sanity check: ❌ Netflix tiene 200M usuarios
→ Obviamente necesita mucho más

Corrección: ~83 Tbps
```

---

## 7. TRUCOS Y ATAJOS {#trucos}

### Truco 1: Día ≈ 10^5 Segundos

```
86,400 ≈ 100,000 = 10^5

Fácil para dividir:
1M requests/day = 1M / 10^5 = 10 QPS
```

### Truco 2: Potencias de 2 ≈ Potencias de 10

```
2^10 ≈ 10^3 (1K)
2^20 ≈ 10^6 (1M)
2^30 ≈ 10^9 (1B)
```

### Truco 3: Regla 80-20 para Cache

```
Cache el 20% más popular
Obtendrás 80% hit rate
```

### Truco 4: Peak Factor

```
General: 2-3x
E-commerce: 5-10x
Live events: 10-20x
```

### Truco 5: Availability 9s

```
Cada "9" adicional = 10x mejor
99% = 3.65 days downtime/year
99.9% = 8.77 hours/year
99.99% = 52.6 minutes/year
```

---

## 8. EJERCICIOS DE PRÁCTICA {#ejercicios}

### Ejercicio 1: Disney+ Launch Day

```
Datos:
- 100M subscribers
- 50% watch on launch day
- Average watch time: 2 hours
- Video quality: 5 Mbps

Calcula:
1. Peak concurrent users
2. Total bandwidth needed
3. Storage for 1,000 movies (2 hours each, 5 qualities)
4. Number of servers (if each handles 10 Gbps)
```

<details>
<summary>Ver Solución</summary>

```
1. Peak concurrent:
   = 100M × 0.5 × (2h / 24h)
   ≈ 4M concurrent

2. Bandwidth:
   = 4M × 5 Mbps
   = 20 Tbps

3. Storage:
   - Per movie: 2 hours × 5 Mbps = 4.5 GB
   - 5 qualities: 4.5 GB × 5 = 22.5 GB
   - 1,000 movies: 22.5 TB
   - With replication (3x): 67.5 TB

4. Servers:
   = 20 Tbps / 10 Gbps
   = 2,000 servers minimum
```
</details>

---

### Ejercicio 2: Slack Messages

```
Datos:
- 20M DAU
- 200 messages per user per day
- Message size: 200 bytes
- Retention: 90 days

Calcula:
1. Write QPS
2. Storage for 90 days
3. Storage with replication (3x)
4. Monthly cost (S3 at $0.023/GB)
```

<details>
<summary>Ver Solución</summary>

```
1. Write QPS:
   = (20M × 200) / 86,400
   ≈ 46K messages/second

2. Storage for 90 days:
   = 20M × 200 × 200 bytes × 90
   = 72 TB

3. With replication:
   = 72 TB × 3
   = 216 TB

4. Monthly cost:
   = 216,000 GB × $0.023
   ≈ $4,968/month
```
</details>

---

### Ejercicio 3: Uber Ride Matching

```
Datos:
- 20M rides per day
- Average wait time: 3 minutes
- Need to calculate distance for 50 nearby drivers
- Calculation time: 10ms per driver

Calcula:
1. Concurrent ride requests (in matching state)
2. Calculations per second
3. Server CPU capacity needed (if 100 calcs/sec per server)
```

<details>
<summary>Ver Solución</summary>

```
1. Concurrent requests:
   = (20M / 86,400) × 180 seconds
   ≈ 41,666 concurrent

2. Calculations per second:
   = (20M / 86,400) × 50 drivers
   ≈ 11,574 calculations/second

3. Servers needed:
   = 11,574 / 100
   ≈ 116 servers
```
</details>

---

## 9. CHEAT SHEET {#cheat-sheet}

### 📊 Quick Reference Card

```
TIME CONVERSIONS
1 day = 10^5 seconds (86.4K actual)
1 month = 2.5M seconds
1 year = 31.5M seconds

STORAGE
1 KB = 10^3 bytes
1 MB = 10^6 bytes
1 GB = 10^9 bytes
1 TB = 10^12 bytes
1 PB = 10^15 bytes

QPS FORMULA
QPS = Daily Requests / 10^5

BANDWIDTH
Bandwidth = QPS × Payload Size

CACHE SIZE
Cache = Hot Data (20%) × Hit Rate (80%)

AVAILABILITY
99.9% = 8.77 hours downtime/year
99.99% = 52 minutes downtime/year

PEAK FACTOR
General: 2-3x
E-commerce: 5-10x
Live events: 10-20x
```

---

## 🎯 PRÓXIMOS PASOS

1. **Memoriza los números clave** (1 semana)
2. **Practica 20 cálculos** (1 por día, 3 semanas)
3. **Cronométrate** (debe tomar 3-5 minutos por cálculo)
4. **Aplica en system design** (integra en tus diseños)

**Siguiente documento:** Trade-offs Fundamentales

---

**Versión:** 1.0
**Última actualización:** 2024-12-03
**Próxima revisión:** Semana 3

**¡Con estos cálculos puedes dimensionar cualquier sistema!** 🚀
