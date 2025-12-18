# Caso Real: Diseñar Twitter/X
## Aplicando Framework RESHADED Completo

**Autor:** Staff Software Architect
**Versión:** 1.0
**Fecha:** 2024-12-03
**Tiempo de lectura:** 90 minutos
**Nivel:** Avanzado

---

## 📋 ÍNDICE

1. [Introducción](#introduccion)
2. [FASE R: Requirements](#requirements)
3. [FASE E: Estimations](#estimations)
4. [FASE S: System Interface](#system-interface)
5. [FASE H: High-Level Design](#high-level-design)
6. [FASE A: API Design](#api-design)
7. [FASE D: Data Model](#data-model)
8. [FASE E: Deep Dive](#deep-dive)
9. [FASE D: Discussion](#discussion)
10. [Implementación en Código](#implementacion)
11. [Conclusión](#conclusion)

---

## 1. INTRODUCCIÓN {#introduccion}

### El Problema

**Pregunta de Entrevista:**
> "Diseña Twitter. Usuarios pueden crear tweets, seguir a otros usuarios, y ver timeline de tweets de personas que siguen."

### Alcance de Este Documento

Este es un **diseño completo end-to-end** que cubre:
- ✅ Todos los pasos de RESHADED
- ✅ Cálculos detallados
- ✅ Trade-offs explícitos
- ✅ Código de implementación
- ✅ Diagramas de arquitectura
- ✅ Consideraciones de producción

### Tiempo de Diseño

**En entrevista:** 45-60 minutos
**En trabajo real:** Semanas de diseño + iteración

---

## 2. FASE R: REQUIREMENTS (7 minutos) {#requirements}

### 2.1 Clarificación Inicial

**Arquitecto:** "Antes de empezar, necesito clarificar algunos puntos..."

### 2.2 Functional Requirements

**Features Core (In Scope):**
```markdown
1. ✅ Tweet Creation
   - Users can create tweets (up to 280 characters)
   - Support text only (no media for MVP)

2. ✅ Following System
   - Users can follow other users
   - Unfollow functionality

3. ✅ Timeline Generation
   - Home timeline: tweets from followed users
   - Chronological order (newest first)

4. ✅ Tweet Interactions
   - Like tweets
   - Retweet tweets

5. ✅ User Profile
   - View user's tweets
   - View follower/following counts
```

**Out of Scope (Nice to Have):**
```markdown
❌ Direct Messages
❌ Notifications
❌ Search functionality
❌ Trending topics
❌ Media uploads (images/videos)
❌ Hashtags and mentions
```

### 2.3 Non-Functional Requirements

**Scale:**
```markdown
- Daily Active Users (DAU): 200 million
- Tweets per day: 500 million
- Follows per day: 100 million
- Read:Write ratio: 100:1 (very read-heavy)
```

**Performance:**
```markdown
- Timeline load: < 500ms (p95)
- Tweet creation: < 200ms (p95)
- Follow action: < 100ms (p95)
```

**Availability:**
```markdown
- Target: 99.99% (52 minutes downtime/year)
- No data loss for tweets (durability)
```

**Consistency:**
```markdown
- Eventual consistency acceptable for timelines (~1 second lag)
- Strong consistency for tweet creation (user must see their own tweet immediately)
```

**Geographic:**
```markdown
- Global service
- Multi-region deployment
- Latency-sensitive (need CDN + edge caching)
```

---

## 3. FASE E: ESTIMATIONS (5 minutos) {#estimations}

### 3.1 Traffic Estimates

**Daily Numbers:**
```
DAU: 200M users

Tweets:
- 500M tweets/day
- Average: 2.5 tweets/user/day

Timeline reads:
- Each user checks timeline 10 times/day
- 200M × 10 = 2B timeline loads/day

Tweet reads (per timeline):
- Each timeline shows 20 tweets
- 2B timelines × 20 tweets = 40B tweet reads/day
```

**QPS Calculations:**
```
Tweet Writes:
= 500M / 86,400 seconds
≈ 5,800 writes/second (average)
≈ 12,000 writes/second (peak, 2x factor)

Timeline Reads:
= 2B / 86,400
≈ 23,000 reads/second (average)
≈ 70,000 reads/second (peak, 3x factor during events)

Tweet Detail Reads:
= 40B / 86,400
≈ 463,000 reads/second (average)
```

**Read:Write Ratio:**
```
Reads: 463K QPS
Writes: 5.8K QPS
Ratio: 80:1 (very read-heavy) ✅ Confirms caching is critical
```

### 3.2 Storage Estimates

**Tweet Storage:**
```
Per Tweet:
- tweet_id: 8 bytes (BIGINT)
- user_id: 8 bytes
- content: 280 bytes (280 chars)
- timestamp: 8 bytes
- metadata: 100 bytes (likes_count, retweets_count, etc.)
─────────────
Total: ~400 bytes per tweet

Daily Storage:
= 500M tweets × 400 bytes
= 200 GB/day

5 Years Storage:
= 200 GB × 365 × 5
= 365 TB

With Replication (3x):
= 365 TB × 3
≈ 1.1 PB
```

**Follow Relationships Storage:**
```
Per Follow:
- follower_id: 8 bytes
- followee_id: 8 bytes
- timestamp: 8 bytes
─────────────
Total: 24 bytes per follow

Assumptions:
- 200M users
- Average 200 follows per user (some have millions, most have dozens)
- Total relationships: 200M × 200 = 40B follows

Storage:
= 40B × 24 bytes
= 960 GB
≈ 1 TB

With Replication:
= 1 TB × 3
= 3 TB
```

**Timeline Cache Storage:**
```
Per Timeline:
- user_id: 8 bytes
- tweet_ids array: 20 tweets × 8 bytes = 160 bytes
- metadata: 32 bytes
─────────────
Total: 200 bytes per cached timeline

Active Users Caching (80/20 rule):
= 200M DAU × 0.8 (80% active)
= 160M timelines

Cache Storage:
= 160M × 200 bytes
= 32 GB (feasible for Redis cluster!) ✅
```

### 3.3 Bandwidth Estimates

**Outgoing (Timeline Reads):**
```
Timeline response size:
- 20 tweets × 400 bytes = 8 KB per timeline
- Plus user info, metadata: ~12 KB total per response

Bandwidth:
= 23,000 timeline reads/sec × 12 KB
= 276 MB/second
= 22 TB/day
```

**Incoming (Tweet Writes):**
```
Tweet size: ~400 bytes

Bandwidth:
= 5,800 tweets/sec × 400 bytes
= 2.3 MB/second
= 200 GB/day
```

**Total Bandwidth:**
```
= 22 TB + 0.2 TB
≈ 22 TB/day outgoing (dominant)
```

### 3.4 Summary Table

| Metric | Value |
|--------|-------|
| **Write QPS** | 5.8K (avg), 12K (peak) |
| **Read QPS** | 463K (avg), 1.4M (peak) |
| **Storage (5 years)** | 1.1 PB |
| **Cache Size** | 32 GB (timelines) |
| **Bandwidth** | 22 TB/day |
| **Servers Needed** | ~500-1000 (API) |
| **DB Shards** | 50-100 (based on write load) |

---

## 4. FASE S: SYSTEM INTERFACE (5 minutos) {#system-interface}

### 4.1 Core APIs

**1. Tweet Creation**
```http
POST /api/v1/tweets
```

**Request:**
```json
{
  "user_id": "123456789",
  "content": "Hello World! This is my first tweet.",
  "created_at": "2024-12-03T10:30:00Z"
}
```

**Response (201 Created):**
```json
{
  "tweet_id": "987654321",
  "user_id": "123456789",
  "content": "Hello World! This is my first tweet.",
  "created_at": "2024-12-03T10:30:00Z",
  "likes_count": 0,
  "retweets_count": 0
}
```

**Rate Limit:** 300 tweets per 3 hours per user

---

**2. Get Timeline**
```http
GET /api/v1/timeline?user_id={user_id}&cursor={cursor}&limit=20
```

**Response (200 OK):**
```json
{
  "tweets": [
    {
      "tweet_id": "987654321",
      "user_id": "123456789",
      "username": "johndoe",
      "content": "Hello World!",
      "created_at": "2024-12-03T10:30:00Z",
      "likes_count": 42,
      "retweets_count": 7
    },
    // ... 19 more tweets
  ],
  "next_cursor": "eyJpZCI6OTg3NjU0MzIxfQ=="
}
```

---

**3. Follow User**
```http
POST /api/v1/users/{user_id}/follow
```

**Request:**
```json
{
  "follower_id": "111111",
  "followee_id": "222222"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "relationship": {
    "follower_id": "111111",
    "followee_id": "222222",
    "created_at": "2024-12-03T10:30:00Z"
  }
}
```

---

**4. Like Tweet**
```http
POST /api/v1/tweets/{tweet_id}/like
```

**Request:**
```json
{
  "user_id": "111111"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "likes_count": 43
}
```

---

**5. Get User Tweets**
```http
GET /api/v1/users/{user_id}/tweets?cursor={cursor}&limit=20
```

---

### 4.2 API Design Principles

**Pagination:**
- Cursor-based (not offset) for scalability
- Cursor encodes tweet_id + timestamp for efficient DB queries

**Rate Limiting:**
- Per-user limits (prevent abuse)
- Per-IP limits (prevent DDoS)
- Tiered limits (verified users get higher limits)

**Authentication:**
- JWT tokens
- Short-lived access tokens (15 min)
- Long-lived refresh tokens (30 days)

**Error Codes:**
```
400 Bad Request: Invalid tweet content (>280 chars)
401 Unauthorized: Invalid or expired token
403 Forbidden: User blocked or suspended
429 Too Many Requests: Rate limit exceeded
500 Internal Server Error: Server error
503 Service Unavailable: System overloaded
```

---

## 5. FASE H: HIGH-LEVEL DESIGN (12 minutos) {#high-level-design}

### 5.1 Architecture Diagram

```
                          ┌──────────────┐
                          │   Clients    │
                          │ (Web/Mobile) │
                          └───────┬──────┘
                                  │
                          ┌───────▼──────┐
                          │     CDN      │
                          │  (CloudFront)│
                          └───────┬──────┘
                                  │
                     ┌────────────▼─────────────┐
                     │    Load Balancer (ALB)   │
                     │   (Multi-AZ, Auto-scale) │
                     └────┬──────────────┬──────┘
                          │              │
               ┌──────────▼────┐    ┌───▼───────────────┐
               │  API Gateway   │    │  API Gateway      │
               │  (us-east-1)   │    │  (us-west-2)      │
               └────┬───────────┘    └───┬───────────────┘
                    │                    │
        ┌───────────▼─────────┐   ┌──────▼──────────────┐
        │  Service Layer      │   │  Service Layer      │
        │  ┌──────────────┐   │   │  ┌──────────────┐   │
        │  │ Tweet Service│   │   │  │ Tweet Service│   │
        │  └──────────────┘   │   │  └──────────────┘   │
        │  ┌──────────────┐   │   │  ┌──────────────┐   │
        │  │Timeline Svc  │   │   │  │Timeline Svc  │   │
        │  └──────────────┘   │   │  └──────────────┘   │
        │  ┌──────────────┐   │   │  ┌──────────────┐   │
        │  │ User Service │   │   │  │ User Service │   │
        │  └──────────────┘   │   │  └──────────────┘   │
        └─────┬─────────┬─────┘   └──────┬─────────┬────┘
              │         │                │         │
        ┌─────▼──┐  ┌───▼───────┐  ┌────▼──┐  ┌───▼────────┐
        │ Redis  │  │   Kafka    │  │ Redis │  │   Kafka    │
        │ Cache  │  │  (Events)  │  │ Cache │  │  (Events)  │
        └─────┬──┘  └───┬────────┘  └────┬──┘  └───┬────────┘
              │         │                │         │
        ┌─────▼─────────▼─────┐    ┌────▼─────────▼─────┐
        │  Data Layer          │    │  Data Layer        │
        │  ┌──────────────┐    │    │  ┌──────────────┐  │
        │  │  Cassandra   │    │    │  │  Cassandra   │  │
        │  │  (Tweets DB) │    │    │  │  (Tweets DB) │  │
        │  └──────────────┘    │    │  └──────────────┘  │
        │  ┌──────────────┐    │    │  ┌──────────────┐  │
        │  │  PostgreSQL  │    │    │  │  PostgreSQL  │  │
        │  │  (Users/Follows)  │    │  │  (Users/Follows)│
        │  └──────────────┘    │    │  └──────────────┘  │
        └──────────────────────┘    └────────────────────┘
                    │                        │
           ┌────────▼────────────────────────▼─────┐
           │      Fan-out Workers (Async)          │
           │  (Timeline Pre-computation)           │
           └───────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │    Object Store    │
                    │  (S3 - Media)      │
                    └────────────────────┘
```

### 5.2 Component Breakdown

#### 1. CDN (CloudFront)
**Purpose:** Cache static assets and popular content
- Profile images
- Popular tweets (trending)
- JS/CSS/HTML assets

**Benefits:**
- Reduces origin load
- Lower latency globally
- DDoS protection

#### 2. Load Balancer (ALB)
**Purpose:** Distribute traffic across API servers
- Health checks
- SSL termination
- Geographic routing
- Auto-scaling integration

#### 3. API Gateway
**Purpose:** Entry point for all API requests
- Authentication (JWT validation)
- Rate limiting
- Request routing
- API versioning

#### 4. Service Layer (Microservices)

**Tweet Service:**
- Create tweets
- Get tweet details
- Update tweet stats (likes, retweets)

**Timeline Service:**
- Generate timelines
- Cache management
- Fanout coordination

**User Service:**
- User profiles
- Follow/unfollow
- User stats

**Why Microservices:**
```
Pros:
✅ Independent scaling (Timeline read-heavy, Tweet write-heavy)
✅ Independent deployment
✅ Team ownership

Cons:
❌ Network latency between services
❌ Distributed transactions complexity
❌ Operational overhead

Decision: Benefits outweigh costs at Twitter's scale
```

#### 5. Caching Layer (Redis)

**What to cache:**
```
Timeline Cache:
- Key: user_id
- Value: Array of tweet_ids (last 100 tweets)
- TTL: 1 hour
- Size: 32 GB (calculated earlier)

Tweet Cache:
- Key: tweet_id
- Value: Tweet object (full details)
- TTL: 24 hours
- Size: Hot tweets (~1% of all) ≈ 200 GB

User Cache:
- Key: user_id
- Value: User profile + stats
- TTL: 1 hour
- Size: ~50 GB
```

**Cache Strategy:**
```
Write-Through: Tweet creation updates cache immediately
Cache-Aside: Timeline reads check cache first, DB on miss
```

#### 6. Message Queue (Kafka)

**Events Published:**
```
1. TweetCreated
2. TweetLiked
3. TweetRetweeted
4. UserFollowed
5. UserUnfollowed
```

**Consumers:**
```
- Fan-out Service (timeline pre-computation)
- Analytics Service
- Notification Service (future)
- Search Indexer (future)
```

**Why Kafka:**
```
✅ High throughput (millions of events/sec)
✅ Persistent (replay events if needed)
✅ Partitioned (parallelizable consumers)
✅ Ordered within partition
```

#### 7. Database Layer

**Cassandra (Tweets):**
```
Why Cassandra:
✅ Write-optimized (500M tweets/day)
✅ Horizontally scalable
✅ High availability (AP in CAP)
✅ Time-series data fit (tweets ordered by time)

Trade-offs:
❌ Eventually consistent
❌ Limited query flexibility (no joins)
❌ Larger storage footprint

Decision: Write scale > Query flexibility
```

**PostgreSQL (Users & Follows):**
```
Why PostgreSQL:
✅ ACID transactions (important for follows)
✅ Rich queries (e.g., "mutual follows")
✅ Strong consistency
✅ Mature tooling

Trade-offs:
❌ Harder to scale writes (need sharding)
❌ Single-master bottleneck

Decision: User/follow data fits in scaled PostgreSQL
```

---

## 6. FASE A: API DESIGN (5 minutos) {#api-design}

*(Already covered in System Interface section)*

---

## 7. FASE D: DATA MODEL (7 minutos) {#data-model}

### 7.1 Tweets Table (Cassandra)

```cql
CREATE TABLE tweets (
    user_id uuid,
    tweet_id timeuuid,  -- Time-based UUID (sortable)
    content text,
    created_at timestamp,
    likes_count counter,
    retweets_count counter,
    reply_to_tweet_id timeuuid,
    PRIMARY KEY (user_id, tweet_id)
) WITH CLUSTERING ORDER BY (tweet_id DESC);

-- Partition key: user_id (all tweets by user in same partition)
-- Clustering key: tweet_id (sorted descending, newest first)
```

**Query Patterns Supported:**
```cql
-- Get all tweets by user (efficient)
SELECT * FROM tweets WHERE user_id = ? LIMIT 20;

-- Get specific tweet (need both user_id and tweet_id)
SELECT * FROM tweets WHERE user_id = ? AND tweet_id = ?;
```

**Query Patterns NOT Supported:**
```cql
-- Get tweet by tweet_id alone (❌ requires ALLOW FILTERING)
SELECT * FROM tweets WHERE tweet_id = ?;  -- Inefficient!

-- Solution: Additional table with tweet_id as partition key
CREATE TABLE tweets_by_id (
    tweet_id timeuuid PRIMARY KEY,
    user_id uuid,
    content text,
    created_at timestamp,
    likes_count counter,
    retweets_count counter
);
-- Denormalized data, but enables efficient lookups
```

### 7.2 Timeline Table (Cassandra)

```cql
CREATE TABLE user_timelines (
    user_id uuid,
    tweet_id timeuuid,
    tweet_user_id uuid,  -- Denormalized: who wrote the tweet
    tweet_content text,  -- Denormalized: avoid extra lookups
    created_at timestamp,
    PRIMARY KEY (user_id, created_at, tweet_id)
) WITH CLUSTERING ORDER BY (created_at DESC, tweet_id DESC);

-- Partition key: user_id (each user's timeline in one partition)
-- Clustering: created_at DESC (newest first)
```

**Fanout on Write:**
```
When @alice creates a tweet:
1. Store in tweets table (alice's partition)
2. Get @alice's followers (100K users)
3. For each follower, insert into their timeline table
   - INSERT INTO user_timelines (user_id, tweet_id, ...)
     VALUES (follower_1, tweet_id, ...);
   - INSERT INTO user_timelines (user_id, tweet_id, ...)
     VALUES (follower_2, tweet_id, ...);
   - ... (100K inserts via Kafka workers)
```

**Trade-off:**
```
Pros:
✅ Timeline read is O(1) - just partition scan
✅ No complex joins needed
✅ Fast reads (< 10ms from Cassandra)

Cons:
❌ Write amplification (1 tweet → 100K writes)
❌ Storage duplication
❌ Eventual consistency (timeline lags by ~1 second)

Decision: Optimized for reads (100:1 read:write ratio)
```

### 7.3 Users Table (PostgreSQL)

```sql
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    bio TEXT,
    verified BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_username ON users(username);
CREATE INDEX idx_email ON users(email);
```

### 7.4 Follows Table (PostgreSQL)

```sql
CREATE TABLE follows (
    follower_id BIGINT REFERENCES users(user_id),
    followee_id BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (follower_id, followee_id)
);

CREATE INDEX idx_follower ON follows(follower_id);
CREATE INDEX idx_followee ON follows(followee_id);
```

**Query Patterns:**
```sql
-- Get all users that @alice follows
SELECT followee_id FROM follows WHERE follower_id = ?;

-- Get all followers of @bob
SELECT follower_id FROM follows WHERE followee_id = ?;

-- Check if @alice follows @bob
SELECT 1 FROM follows
WHERE follower_id = ? AND followee_id = ?;

-- Mutual follows (complex query, okay for PostgreSQL)
SELECT f1.followee_id
FROM follows f1
JOIN follows f2 ON f1.followee_id = f2.follower_id
WHERE f1.follower_id = ? AND f2.followee_id = ?;
```

### 7.5 Sharding Strategy

**Cassandra Sharding (Built-in):**
```
Partition key: user_id
Cassandra automatically distributes partitions across nodes
Consistent hashing ensures even distribution
```

**PostgreSQL Sharding (Manual):**
```python
# Hash-based sharding for users
NUM_SHARDS = 16

def get_user_shard(user_id):
    return user_id % NUM_SHARDS

# User 12345 → Shard 9
# All queries for user 12345 go to shard 9
```

**Sharding Trade-offs:**
```
Pros:
✅ Horizontal scalability
✅ Each shard handles 1/N of load

Cons:
❌ Cross-shard queries expensive (e.g., global trends)
❌ Rebalancing shards is complex

Mitigation:
- Shard on user_id (most queries are user-scoped)
- Avoid cross-shard joins
- Use separate analytics DB for global queries
```

---

## 8. FASE E: DEEP DIVE (15 minutos) {#deep-dive}

### 8.1 Timeline Generation: The Core Challenge

**Problem:**
```
How to generate timeline for user with 5,000 follows in < 500ms?
```

**Option 1: Pull Model (Fan-out on Read)**

```python
def get_timeline_pull(user_id, limit=20):
    """
    Pull model: Fetch tweets when user requests timeline
    """
    # 1. Get list of users that this user follows
    following = db.query(
        "SELECT followee_id FROM follows WHERE follower_id = ?",
        [user_id]
    )  # 5,000 users

    # 2. Fetch recent tweets from each followed user
    all_tweets = []
    for followed_user in following:
        tweets = cassandra.query(
            "SELECT * FROM tweets WHERE user_id = ? LIMIT 10",
            [followed_user]
        )
        all_tweets.extend(tweets)

    # 3. Sort by timestamp (merge-sort from multiple sources)
    all_tweets.sort(key=lambda t: t.created_at, reverse=True)

    # 4. Return top N
    return all_tweets[:limit]

# Analysis:
# - 5,000 Cassandra queries (one per followed user)
# - Each query: ~5ms
# - Total: 5,000 × 5ms = 25 seconds ❌ WAY TOO SLOW!
```

**Optimization: Parallel Fetching**

```python
import asyncio

async def get_timeline_pull_parallel(user_id, limit=20):
    following = get_following(user_id)  # 5,000 users

    # Fetch in parallel
    tasks = [
        cassandra.query_async(
            "SELECT * FROM tweets WHERE user_id = ? LIMIT 10",
            [user]
        )
        for user in following
    ]

    results = await asyncio.gather(*tasks)

    all_tweets = [tweet for result in results for tweet in result]
    all_tweets.sort(key=lambda t: t.created_at, reverse=True)

    return all_tweets[:limit]

# Analysis:
# - Still makes 5,000 queries, but in parallel
# - Time: ~100ms (limited by slowest query)
# - Still too slow for users with many follows ❌
# - Cassandra cluster gets hammered (5,000 QPS per timeline!)
```

**Option 2: Push Model (Fan-out on Write)**

```python
def create_tweet_push(user_id, content):
    """
    Push model: When tweet created, push to all followers' timelines
    """
    # 1. Create tweet
    tweet = Tweet(user_id=user_id, content=content)
    cassandra.insert("tweets", tweet)

    # 2. Get all followers
    followers = get_followers(user_id)  # Could be MILLIONS for celebrities!

    # 3. Push tweet to each follower's timeline (async via Kafka)
    for follower in followers:
        kafka.publish("timeline_fanout", {
            "follower_id": follower,
            "tweet": tweet
        })

    return tweet

# Kafka Consumer (Timeline Fanout Worker):
def fanout_worker():
    for message in kafka.consume("timeline_fanout"):
        follower_id = message["follower_id"]
        tweet = message["tweet"]

        # Insert into follower's timeline
        cassandra.insert("user_timelines", {
            "user_id": follower_id,
            "tweet_id": tweet.id,
            "tweet_content": tweet.content,
            "created_at": tweet.created_at
        })

def get_timeline_push(user_id, limit=20):
    """
    Read timeline (pre-computed)
    """
    return cassandra.query(
        "SELECT * FROM user_timelines WHERE user_id = ? LIMIT ?",
        [user_id, limit]
    )  # Single query, ~5ms ✅ FAST!

# Analysis Push Model:
# Pros:
# ✅ Read is extremely fast (single query, ~5ms)
# ✅ Timeline pre-computed

# Cons:
# ❌ Write amplification (1 tweet → 1M writes for celebrities)
# ❌ Tweet creation slow for users with many followers
# ❌ Wasted work if follower doesn't read timeline
```

**Option 3: Hybrid Model (The Real Solution)**

```python
CELEBRITY_THRESHOLD = 100_000  # 100K followers

def create_tweet_hybrid(user_id, content):
    """
    Hybrid: Push for normal users, pull for celebrities
    """
    tweet = Tweet(user_id=user_id, content=content)
    cassandra.insert("tweets", tweet)

    follower_count = get_follower_count(user_id)

    if follower_count < CELEBRITY_THRESHOLD:
        # PUSH: Fan-out to all followers
        followers = get_followers(user_id)
        for follower in followers:
            kafka.publish("timeline_fanout", {
                "follower_id": follower,
                "tweet": tweet
            })
    else:
        # PULL: Don't fan-out, mark as celebrity tweet
        # Followers will fetch these tweets on-demand
        redis.sadd(f"celebrity_users", user_id)

    return tweet

def get_timeline_hybrid(user_id, limit=20):
    """
    Read timeline (hybrid approach)
    """
    # 1. Get pre-computed timeline (from push)
    timeline_tweets = cassandra.query(
        "SELECT * FROM user_timelines WHERE user_id = ? LIMIT ?",
        [user_id, limit * 2]  # Fetch extra to merge with celebrity tweets
    )

    # 2. Get followed celebrities
    following = get_following(user_id)
    celebrities = [u for u in following if is_celebrity(u)]

    # 3. Fetch recent tweets from celebrities (pull)
    celebrity_tweets = []
    for celeb in celebrities:
        tweets = cassandra.query(
            "SELECT * FROM tweets WHERE user_id = ? LIMIT 10",
            [celeb]
        )
        celebrity_tweets.extend(tweets)

    # 4. Merge and sort
    all_tweets = timeline_tweets + celebrity_tweets
    all_tweets.sort(key=lambda t: t.created_at, reverse=True)

    return all_tweets[:limit]

# Analysis Hybrid:
# ✅ Fast reads for most users (~5ms from cache)
# ✅ No write amplification for celebrities
# ✅ Acceptable latency for users following celebrities (~50ms)

# Trade-offs:
# ⚠️ Complexity: Two code paths
# ⚠️ Need to categorize users (celebrity detection)

# This is what Twitter actually uses! ✅
```

### 8.2 Performance Optimization Deep Dive

**Caching Strategy:**

```python
class TimelineCache:
    """
    Multi-level caching for timeline
    """
    def __init__(self):
        self.l1_cache = {}  # In-memory LRU (100MB per server)
        self.l2_cache = redis.Redis()  # Shared Redis cluster

    def get_timeline(self, user_id):
        # L1: Check local memory (~0.1ms)
        if user_id in self.l1_cache:
            return self.l1_cache[user_id]

        # L2: Check Redis (~1ms)
        cached = self.l2_cache.get(f"timeline:{user_id}")
        if cached:
            timeline = json.loads(cached)
            self.l1_cache[user_id] = timeline
            return timeline

        # L3: Fetch from Cassandra (~5ms)
        timeline = cassandra.query(
            "SELECT * FROM user_timelines WHERE user_id = ? LIMIT 20",
            [user_id]
        )

        # Populate caches
        self.l2_cache.setex(
            f"timeline:{user_id}",
            3600,  # 1 hour TTL
            json.dumps(timeline)
        )
        self.l1_cache[user_id] = timeline

        return timeline

# Cache hit rates (typical):
# L1: 60% → 0.1ms
# L2: 30% → 1ms
# L3: 10% → 5ms
# Effective latency: 0.6*0.1 + 0.3*1 + 0.1*5 = 0.86ms ✅
```

**Database Optimization:**

```python
# Connection pooling
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy

cluster = Cluster(
    contact_points=['cassandra1', 'cassandra2', 'cassandra3'],
    load_balancing_policy=RoundRobinPolicy(),
    protocol_version=4
)
session = cluster.connect('twitter')

# Prepared statements (compiled once, reused)
TIMELINE_QUERY = session.prepare(
    "SELECT * FROM user_timelines WHERE user_id = ? LIMIT ?"
)

def get_timeline_optimized(user_id):
    return session.execute(TIMELINE_QUERY, [user_id, 20])

# Benefits:
# ✅ Statement parsed once, not per query
# ✅ Reduced network overhead
# ✅ 2-3x faster than simple queries
```

---

## 9. FASE D: DISCUSSION (10 minutos) {#discussion}

### 9.1 Trade-offs Summary

**1. Cassandra vs PostgreSQL for Tweets**
```
Decision: Cassandra

Trade-off:
✅ Pro: Write scalability (500M tweets/day)
✅ Pro: High availability (no single point of failure)
❌ Con: Eventually consistent (tweets visible after ~1 second)
❌ Con: Limited query patterns (no complex joins)

Justification:
- Write volume is primary concern
- Eventual consistency acceptable for social media
- Query patterns are simple (timeline, user tweets)
```

**2. Fanout on Write (Push) vs Read (Pull)**
```
Decision: Hybrid (push for normal, pull for celebrities)

Trade-off:
✅ Pro: Fast timeline reads (< 10ms) for 99% of users
✅ Pro: No write amplification for celebrities
❌ Con: Increased complexity (two code paths)
❌ Con: Need celebrity detection logic

Justification:
- Optimizes for common case (users with < 100K followers)
- Read latency is critical (checked frequently)
- Write latency less critical (can be async)
```

**3. Strong vs Eventual Consistency**
```
Decision: Eventual consistency for timelines

Trade-off:
✅ Pro: High availability (no system downtime)
✅ Pro: Better performance (no coordination overhead)
❌ Con: User might not see own tweet immediately
❌ Con: Stale timeline for ~1 second

Justification:
- Twitter prioritizes availability over consistency
- 1-second lag acceptable for social media
- User can always check own profile to see new tweet
```

### 9.2 Bottlenecks and Mitigations

**Bottleneck 1: Fanout Workers**
```
Problem: 1 celebrity tweet → 10M fanout writes

Mitigation:
- Horizontal scaling (100+ worker instances)
- Kafka partitioning (parallel processing)
- Rate limiting per worker (don't overwhelm Cassandra)
- Batch writes to Cassandra (100 inserts per batch)

Result: 10M fanout completes in ~5 seconds
```

**Bottleneck 2: Cassandra Write Hot Spots**
```
Problem: Popular users (high follower count) create write hot spots

Mitigation:
- Partition by user_id (distributes writes)
- Use time-series partition keys for timelines
- Example: (user_id, bucket_hour) as partition key
  - user_123_2024120310 (hour bucket)
  - Distributes writes across time
```

**Bottleneck 3: Cache Invalidation**
```
Problem: User unfollows someone, timeline cache is stale

Mitigation:
- Set reasonable TTL (1 hour)
- On follow/unfollow, delete timeline cache
- Accept brief staleness (Twitter's approach)

Alternative:
- Real-time invalidation (complex, not worth it)
```

### 9.3 Single Points of Failure (SPOF)

**SPOF 1: Load Balancer**
```
Mitigation:
- Multiple load balancers across AZs
- DNS-based failover
- Health checks and automatic rerouting
```

**SPOF 2: Kafka**
```
Mitigation:
- Kafka cluster (3+ brokers)
- Replication factor = 3
- Multi-AZ deployment
- Consumer groups for redundancy
```

**SPOF 3: Cassandra**
```
Mitigation:
- Replication factor = 3 (3 copies of each partition)
- Multi-datacenter replication
- No single node failure affects availability
```

**SPOF 4: Redis Cache**
```
Mitigation:
- Redis Cluster (not single instance)
- Redis Sentinel for automatic failover
- Cache miss = degraded performance, not failure
- Fallback to database
```

### 9.4 Cost Optimization

**Current Cost Estimate (AWS):**
```
Compute (EC2 for services):
- 500 instances × $0.10/hour × 730 hours/month
= $36,500/month

Database (Cassandra on EC2):
- 100 i3.2xlarge instances × $0.624/hour × 730 hours
= $45,552/month

Cache (ElastiCache Redis):
- 50 cache.r6g.xlarge × $0.25/hour × 730 hours
= $9,125/month

Bandwidth:
- 22 TB/day × 30 days = 660 TB/month
- 660,000 GB × $0.05/GB
= $33,000/month

Storage (S3 for backups):
- 1 PB × $0.023/GB
= $23,000/month

Total: ~$147,000/month

For 200M users: $0.00074 per user per month ✅
```

**Optimization Opportunities:**
```
1. Reserved Instances (save 30-50%)
2. Spot Instances for non-critical workers
3. S3 Intelligent Tiering (save 20-40% on storage)
4. Compress data (save 50% on storage + bandwidth)
5. Edge caching (CDN reduces origin bandwidth by 80%)

Optimized cost: ~$80K-$100K/month
```

---

## 10. IMPLEMENTACIÓN EN CÓDIGO {#implementacion}

### 10.1 Tweet Service (Python/FastAPI)

```python
# tweet_service.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from cassandra.cluster import Cluster
import redis
import kafka
from datetime import datetime
import uuid

app = FastAPI()

# Connections
cassandra_session = Cluster(['cassandra1', 'cassandra2']).connect('twitter')
redis_client = redis.Redis(host='redis', decode_responses=True)
kafka_producer = kafka.KafkaProducer(bootstrap_servers=['kafka:9092'])

class TweetCreate(BaseModel):
    user_id: str
    content: str

@app.post("/tweets")
async def create_tweet(tweet: TweetCreate):
    """Create a new tweet"""

    # Validate
    if len(tweet.content) > 280:
        raise HTTPException(400, "Tweet exceeds 280 characters")

    # Generate tweet_id (time-based UUID)
    tweet_id = uuid.uuid1()  # UUID v1 (time-based)

    # Insert into Cassandra
    cassandra_session.execute(
        """
        INSERT INTO tweets (user_id, tweet_id, content, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (uuid.UUID(tweet.user_id), tweet_id, tweet.content, datetime.now())
    )

    # Publish event to Kafka (for fanout)
    kafka_producer.send('tweet_created', {
        'tweet_id': str(tweet_id),
        'user_id': tweet.user_id,
        'content': tweet.content,
        'created_at': datetime.now().isoformat()
    })

    # Invalidate user's timeline cache
    redis_client.delete(f"timeline:{tweet.user_id}")

    return {
        "tweet_id": str(tweet_id),
        "user_id": tweet.user_id,
        "content": tweet.content,
        "created_at": datetime.now().isoformat()
    }

@app.get("/timeline/{user_id}")
async def get_timeline(user_id: str, limit: int = 20):
    """Get user's timeline"""

    # Check cache
    cached = redis_client.get(f"timeline:{user_id}")
    if cached:
        return json.loads(cached)

    # Fetch from Cassandra
    rows = cassandra_session.execute(
        """
        SELECT tweet_id, tweet_content, created_at
        FROM user_timelines
        WHERE user_id = ?
        LIMIT ?
        """,
        (uuid.UUID(user_id), limit)
    )

    timeline = [
        {
            "tweet_id": str(row.tweet_id),
            "content": row.tweet_content,
            "created_at": row.created_at.isoformat()
        }
        for row in rows
    ]

    # Cache for 1 hour
    redis_client.setex(
        f"timeline:{user_id}",
        3600,
        json.dumps(timeline)
    )

    return timeline
```

### 10.2 Fanout Worker (Python/Kafka Consumer)

```python
# fanout_worker.py
from kafka import KafkaConsumer
from cassandra.cluster import Cluster
import json
import uuid

cassandra_session = Cluster(['cassandra1']).connect('twitter')
consumer = KafkaConsumer(
    'tweet_created',
    bootstrap_servers=['kafka:9092'],
    group_id='timeline_fanout_workers',  # Consumer group for parallelism
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def get_followers(user_id):
    """Get all followers of a user"""
    # Query PostgreSQL
    return db.query(
        "SELECT follower_id FROM follows WHERE followee_id = ?",
        [user_id]
    )

def fanout_tweet_to_followers(tweet_event):
    """Fan-out tweet to all followers' timelines"""

    user_id = tweet_event['user_id']
    tweet_id = tweet_event['tweet_id']
    content = tweet_event['content']
    created_at = tweet_event['created_at']

    # Get followers
    followers = get_followers(user_id)

    # Check if celebrity (> 100K followers)
    if len(followers) > 100_000:
        print(f"Celebrity tweet {tweet_id}, skipping fanout")
        return

    # Batch insert to Cassandra (100 at a time)
    batch_size = 100
    for i in range(0, len(followers), batch_size):
        batch = followers[i:i+batch_size]

        # Prepare batch statement
        for follower_id in batch:
            cassandra_session.execute(
                """
                INSERT INTO user_timelines
                (user_id, tweet_id, tweet_user_id, tweet_content, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    uuid.UUID(follower_id),
                    uuid.UUID(tweet_id),
                    uuid.UUID(user_id),
                    content,
                    created_at
                )
            )

    print(f"Fanned out tweet {tweet_id} to {len(followers)} followers")

# Main loop
print("Fanout worker starting...")
for message in consumer:
    tweet_event = message.value
    fanout_tweet_to_followers(tweet_event)
```

---

## 11. CONCLUSIÓN {#conclusion}

### 11.1 Resumen de Decisiones Clave

| Aspecto | Decisión | Razón |
|---------|----------|-------|
| **Database** | Cassandra (tweets) + PostgreSQL (users) | Write scale + ACID for critical data |
| **Cache** | Redis (multi-level) | Read-heavy, 80% cache hit |
| **Timeline** | Hybrid fanout (push + pull) | Balance write/read performance |
| **Consistency** | Eventual (timelines) | Availability > strong consistency |
| **Architecture** | Microservices | Independent scaling |
| **Queue** | Kafka | High throughput, durability |

### 11.2 Key Learnings

**1. Optimize for the Common Case:**
- 99% of users have < 10K followers → Optimize push model for them
- 1% celebrities → Special handling

**2. Read:Write Ratio Drives Architecture:**
- 100:1 read-heavy → Aggressive caching, denormalization

**3. Trade-offs Are Inevitable:**
- No perfect solution
- Every choice has costs
- Articulate them clearly

**4. Scale Requires Distribution:**
- Single machine is never enough
- Sharding, replication, caching essential

### 11.3 Próximos Pasos

**Para Profundizar:**
1. Estudiar Twitter Engineering Blog
2. Implementar un prototipo (simplificado)
3. Benchmarking de opciones (pull vs push)
4. Estudiar Cassandra internals
5. Practicar otros casos (Instagram, YouTube, etc.)

---

**Versión:** 1.0
**Última actualización:** 2024-12-03
**Tiempo estimado de estudio:** 3-4 horas

**¡Has completado un diseño completo de sistema a escala de Twitter!** 🚀

**Siguiente caso:** Uber (Sistema de Ride-Sharing)
