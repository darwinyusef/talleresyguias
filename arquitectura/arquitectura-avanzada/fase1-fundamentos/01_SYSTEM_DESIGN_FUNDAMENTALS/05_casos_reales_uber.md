# System Design: UBER - Ride Sharing Platform

**Semana 5 - Caso Real Completo**
**Aplicación del Framework RESHADED**

---

## ÍNDICE

1. [Requirements](#1-requirements)
2. [Estimations](#2-estimations)
3. [System Interface](#3-system-interface)
4. [High-level Design](#4-high-level-design)
5. [API Design](#5-api-design)
6. [Data Model](#6-data-model)
7. [Deep Dive](#7-deep-dive)
8. [Discussion](#8-discussion)
9. [Implementación](#9-implementación)
10. [Ejercicios](#10-ejercicios)

---

## 1. REQUIREMENTS

### 1.1 Functional Requirements

#### Core Features (P0)
- **Request Ride**: Pasajeros pueden solicitar viajes especificando pickup/dropoff
- **Driver Matching**: Sistema encuentra conductor cercano disponible
- **Real-time Tracking**: Pasajeros rastrean ubicación del conductor en tiempo real
- **Trip Management**: Inicio, finalización, y gestión del viaje
- **Payment Processing**: Procesamiento de pagos al finalizar viaje
- **Rating System**: Pasajeros y conductores se califican mutuamente

#### Secondary Features (P1)
- **Surge Pricing**: Precios dinámicos basados en demanda/oferta
- **ETA Calculation**: Estimación de tiempo de llegada y duración del viaje
- **Ride History**: Historial de viajes para usuarios
- **Driver Availability**: Conductores pueden marcar disponibilidad online/offline

#### Nice to Have (P2)
- **Ride Scheduling**: Programar viajes con anticipación
- **Shared Rides**: Pool de múltiples pasajeros
- **Multi-stop Routes**: Viajes con múltiples paradas

### 1.2 Non-Functional Requirements

#### Scale
- **MAU (Monthly Active Users)**: 100M pasajeros, 5M conductores
- **DAU (Daily Active Users)**: 30M pasajeros, 1.5M conductores
- **Concurrent Rides**: 1M viajes simultáneos en peak
- **Geographic Coverage**: 600+ ciudades, 70+ países

#### Performance
- **Driver Matching Latency**: < 5 segundos para encontrar conductor
- **Location Update Latency**: < 1 segundo para actualizar mapa
- **ETA Calculation**: < 2 segundos
- **Payment Processing**: < 3 segundos

#### Availability & Reliability
- **Availability**: 99.99% uptime (4.38 minutos downtime/mes)
- **Data Durability**: 99.999999999% (11 nines) para datos de viajes
- **Geo-redundancy**: Multi-region deployment

#### Consistency
- **Ride Matching**: Fuerte consistencia (un conductor no puede aceptar 2 viajes)
- **Location Updates**: Eventual consistency aceptable (1-2 segundos stale OK)
- **Payments**: Fuerte consistencia (transacciones ACID)

---

## 2. ESTIMATIONS

### 2.1 Traffic Estimations

#### Active Users
```
Total Users:
- Pasajeros: 100M MAU
- Conductores: 5M MAU
- DAU/MAU ratio: 30%
- Daily Active Riders: 30M
- Daily Active Drivers: 1.5M
```

#### Rides per Day
```
Assumptions:
- Average rides per active rider: 1.5 rides/day
- Total daily rides: 30M × 1.5 = 45M rides/day

Peak Factor: 3x average
- Peak hour rides: (45M / 24) × 3 = 5.6M rides/hour
- Peak rides/second: 5.6M / 3600 = 1,556 rides/sec
```

#### Request Rates (QPS)

**1. Ride Requests**
```
Average QPS: 45M rides / 86,400 sec = 520 QPS
Peak QPS: 520 × 3 = 1,560 QPS
```

**2. Location Updates (Critical!)**
```
Active drivers sending location every 4 seconds:
- Peak concurrent drivers: 600K (40% of 1.5M DAU)
- Updates/second: 600K / 4 = 150K QPS

Active riders viewing map (during ride):
- Concurrent riders in trip: 1M
- Polling interval: 2 seconds
- Read QPS: 1M / 2 = 500K QPS

Total Location QPS: 650K QPS (!)
```

**3. Driver Matching Queries**
```
Each ride request searches for nearby drivers:
- Search QPS = Ride Request QPS = 1,560 QPS peak
- Each search queries geospatial index
```

### 2.2 Storage Estimations

#### Ride Data
```
Data per ride:
- Ride ID: 8 bytes (bigint)
- User IDs (rider, driver): 16 bytes
- Locations (pickup, dropoff): 32 bytes (4 coordinates)
- Timestamps (requested, started, ended): 24 bytes
- Pricing (fare, surge): 8 bytes
- Status, payment: 16 bytes
- Metadata (JSON): 100 bytes
Total per ride: ~200 bytes

Daily storage: 45M rides × 200 bytes = 9 GB/day
Yearly: 9 GB × 365 = 3.3 TB/year
5-year retention: 16.5 TB
```

#### Location History (Huge!)
```
Location updates during trip:
- Average trip duration: 20 minutes
- Update interval: 4 seconds
- Updates per trip: 20 × 60 / 4 = 300 updates

Data per update:
- Driver ID: 8 bytes
- Latitude, Longitude: 16 bytes
- Timestamp: 8 bytes
- Heading, speed: 8 bytes
Total: 40 bytes per update

Daily location data:
- 45M rides × 300 updates × 40 bytes = 540 GB/day
- Yearly: 197 TB/year
- 90-day retention: 48.6 TB
```

#### User Data
```
Users: 105M (100M riders + 5M drivers)
Data per user: ~1 KB (profile, preferences, payment methods)
Total: 105 GB (negligible)
```

**Total Storage: ~50 TB (mostly location history)**

### 2.3 Bandwidth Estimations

#### Ingress (Write)
```
Location updates: 150K QPS × 40 bytes = 6 MB/s
Ride requests: 1.6K QPS × 500 bytes = 0.8 MB/s
Total Ingress: ~7 MB/s = 56 Mbps
```

#### Egress (Read)
```
Location reads: 500K QPS × 40 bytes = 20 MB/s
Driver search results: 1.6K QPS × 10 KB = 16 MB/s
ETA/pricing calculations: 1.6K QPS × 2 KB = 3.2 MB/s
Total Egress: ~40 MB/s = 320 Mbps
```

### 2.4 Cost Estimation (Ballpark)

#### Compute
```
Application servers: 500 instances × $100/month = $50K
Geospatial processing: 200 instances × $200/month = $40K
WebSocket servers: 300 instances × $150/month = $45K
Total Compute: $135K/month
```

#### Storage
```
Hot storage (PostgreSQL): 20 TB × $100/TB = $2K
Warm storage (S3): 30 TB × $23/TB = $0.7K
Total Storage: $2.7K/month
```

#### Data Transfer
```
Egress: 100 TB/month × $90/TB = $9K
```

#### Cache (Redis)
```
Memory: 500 GB × $100/TB = $50/month
Negligible
```

**Total: ~$147K/month = $1.76M/year**

---

## 3. SYSTEM INTERFACE

### 3.1 Actors

- **Rider**: Usuario solicitando viaje
- **Driver**: Conductor proveyendo servicio
- **Admin**: Personal de Uber monitoreando sistema
- **Payment Gateway**: Sistema externo (Stripe, Adyen)
- **Maps Service**: Proveedor de mapas (Google Maps API)

### 3.2 High-Level APIs

#### For Riders
```
POST   /api/v1/rides/request          # Request a ride
GET    /api/v1/rides/{rideId}         # Get ride details
GET    /api/v1/rides/{rideId}/location # Track driver location
POST   /api/v1/rides/{rideId}/cancel  # Cancel ride
POST   /api/v1/rides/{rideId}/rate    # Rate driver
GET    /api/v1/rides/history          # Ride history
```

#### For Drivers
```
POST   /api/v1/drivers/status         # Update online/offline status
GET    /api/v1/drivers/ride-requests  # Get nearby ride requests
POST   /api/v1/rides/{rideId}/accept  # Accept ride
POST   /api/v1/rides/{rideId}/start   # Start trip
POST   /api/v1/rides/{rideId}/complete # Complete trip
POST   /api/v1/drivers/location       # Update current location
```

#### Internal APIs
```
POST   /api/internal/matching/find-driver    # Find nearby available drivers
POST   /api/internal/pricing/calculate       # Calculate fare with surge
POST   /api/internal/eta/calculate           # Calculate ETA
POST   /api/internal/payment/process         # Process payment
```

---

## 4. HIGH-LEVEL DESIGN

### 4.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENTS                                     │
├──────────────────────────┬──────────────────────────────────────────┤
│   Rider Mobile App       │        Driver Mobile App                 │
│   (iOS/Android)          │        (iOS/Android)                     │
└──────────┬───────────────┴────────────────┬─────────────────────────┘
           │                                 │
           │ REST/WebSocket                  │ REST/WebSocket
           ▼                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        API GATEWAY (Kong)                             │
│  - Authentication (JWT)                                               │
│  - Rate Limiting                                                      │
│  - Load Balancing                                                     │
└──────────┬────────────────────────────┬──────────────┬───────────────┘
           │                            │              │
    ┌──────▼──────┐            ┌───────▼──────┐  ┌───▼───────┐
    │  Ride       │            │  Driver      │  │ Location  │
    │  Service    │            │  Service     │  │ Service   │
    │             │            │              │  │(WebSocket)│
    │ - Request   │            │ - Status     │  │           │
    │ - Cancel    │            │ - Accept     │  │ - Track   │
    │ - Complete  │            │ - Update     │  │ - Stream  │
    └──────┬──────┘            └───────┬──────┘  └───┬───────┘
           │                           │             │
           │         ┌─────────────────┴─────┐       │
           │         │                       │       │
    ┌──────▼─────────▼──┐            ┌──────▼───────▼─────┐
    │  Matching Service  │            │  Geospatial Index  │
    │                    │            │   (Redis GEO)      │
    │ - Find Drivers     │◄───────────┤                    │
    │ - Optimize Match   │            │ - GEOADD           │
    │ - Scoring          │            │ - GEORADIUS        │
    └────────────────────┘            │ - Driver positions │
                                      └────────────────────┘
           │
    ┌──────▼──────┐       ┌────────────┐      ┌──────────────┐
    │  Pricing    │       │    ETA     │      │   Payment    │
    │  Service    │       │  Service   │      │   Service    │
    │             │       │            │      │              │
    │ - Base Fare │       │ - Maps API │      │ - Stripe     │
    │ - Surge     │       │ - Duration │      │ - Refunds    │
    └─────────────┘       └────────────┘      └──────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                    │
├────────────────┬────────────────┬─────────────────┬──────────────────┤
│  PostgreSQL    │  Cassandra     │   Redis Cache   │   Kafka          │
│  (Rides, Users)│  (Location     │   (Driver       │   (Events)       │
│                │   History)     │    Positions)   │                  │
└────────────────┴────────────────┴─────────────────┴──────────────────┘
```

### 4.2 Component Responsibilities

#### API Gateway
- Authentication & authorization (JWT tokens)
- Rate limiting per user (100 req/min riders, 1000 req/min drivers)
- TLS termination
- Request routing to services

#### Ride Service
- Manages ride lifecycle (requested → matched → started → completed)
- Coordinates with matching service
- Publishes events to Kafka

#### Driver Service
- Driver registration and profiles
- Availability management (online/offline)
- Driver location updates
- Background checks and compliance

#### Location Service
- Real-time location streaming via WebSockets
- Updates driver positions in geospatial index
- Broadcasts location to riders tracking trip

#### Matching Service
- **Critical component!** Finds best driver for ride request
- Queries geospatial index for nearby drivers
- Scoring algorithm (distance, rating, acceptance rate)
- Timeout: 5 seconds max

#### Pricing Service
- Calculates base fare (distance × rate + time × rate)
- Applies surge pricing multiplier
- Discount codes and promotions

#### ETA Service
- Integrates with Google Maps API
- Calculates pickup ETA and trip duration
- Traffic-aware routing

#### Payment Service
- Processes payments via Stripe/Adyen
- Handles refunds and disputes
- Driver payouts

---

## 5. API DESIGN

### 5.1 Request Ride

**Endpoint**: `POST /api/v1/rides/request`

**Request**:
```json
{
  "riderId": "user_123",
  "pickup": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "address": "123 Market St, SF"
  },
  "dropoff": {
    "latitude": 37.7849,
    "longitude": -122.4094,
    "address": "456 Mission St, SF"
  },
  "rideType": "uberX",  // uberX, uberXL, uberBlack
  "paymentMethodId": "pm_123"
}
```

**Response**:
```json
{
  "rideId": "ride_789",
  "status": "searching",
  "estimatedPickupTime": "2024-12-05T10:05:00Z",
  "estimatedFare": {
    "amount": 15.50,
    "currency": "USD",
    "surgeMultiplier": 1.5
  },
  "searchTimeout": 30
}
```

**Status Codes**:
- `200 OK`: Ride request created
- `400 Bad Request`: Invalid input
- `402 Payment Required`: Payment method failed
- `429 Too Many Requests`: Rate limit exceeded

### 5.2 Update Driver Location

**Endpoint**: `POST /api/v1/drivers/location`

**Request**:
```json
{
  "driverId": "driver_456",
  "latitude": 37.7750,
  "longitude": -122.4195,
  "heading": 90,
  "speed": 15.5,
  "timestamp": "2024-12-05T10:00:00Z"
}
```

**Response**:
```json
{
  "acknowledged": true,
  "nearbyRequests": 3
}
```

**Notes**:
- Called every 4 seconds when driver is online
- 150K QPS at peak!
- Must be extremely fast (< 100ms)

### 5.3 Find Driver (Internal)

**Endpoint**: `POST /api/internal/matching/find-driver`

**Request**:
```json
{
  "rideId": "ride_789",
  "pickup": {
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "rideType": "uberX",
  "radius": 5000  // meters
}
```

**Response**:
```json
{
  "driverId": "driver_456",
  "eta": 180,  // seconds
  "distance": 2500,  // meters
  "score": 0.87,
  "driver": {
    "name": "John Doe",
    "rating": 4.8,
    "vehicle": "Toyota Camry 2020"
  }
}
```

---

## 6. DATA MODEL

### 6.1 PostgreSQL (Transactional Data)

#### Users Table
```sql
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    user_type VARCHAR(20) NOT NULL,  -- 'rider' or 'driver'
    rating DECIMAL(3,2) DEFAULT 5.00,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    INDEX idx_phone (phone),
    INDEX idx_email (email)
);

CREATE TABLE drivers (
    driver_id BIGINT PRIMARY KEY REFERENCES users(user_id),
    license_number VARCHAR(50) UNIQUE NOT NULL,
    vehicle_id BIGINT REFERENCES vehicles(vehicle_id),
    status VARCHAR(20) DEFAULT 'offline',  -- online, offline, on_trip
    total_trips INT DEFAULT 0,
    acceptance_rate DECIMAL(5,2) DEFAULT 100.00,
    INDEX idx_status (status)
);

CREATE TABLE vehicles (
    vehicle_id BIGSERIAL PRIMARY KEY,
    driver_id BIGINT REFERENCES drivers(driver_id),
    make VARCHAR(50),
    model VARCHAR(50),
    year INT,
    license_plate VARCHAR(20) UNIQUE,
    vehicle_type VARCHAR(20),  -- uberX, uberXL, uberBlack
    color VARCHAR(30)
);
```

#### Rides Table
```sql
CREATE TABLE rides (
    ride_id BIGSERIAL PRIMARY KEY,
    rider_id BIGINT NOT NULL REFERENCES users(user_id),
    driver_id BIGINT REFERENCES drivers(driver_id),

    -- Locations
    pickup_lat DECIMAL(10,7) NOT NULL,
    pickup_lng DECIMAL(10,7) NOT NULL,
    pickup_address TEXT,
    dropoff_lat DECIMAL(10,7) NOT NULL,
    dropoff_lng DECIMAL(10,7) NOT NULL,
    dropoff_address TEXT,

    -- Status
    status VARCHAR(20) NOT NULL,  -- requested, matched, started, completed, cancelled
    ride_type VARCHAR(20) NOT NULL,

    -- Timing
    requested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    matched_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,

    -- Pricing
    estimated_fare DECIMAL(10,2),
    final_fare DECIMAL(10,2),
    surge_multiplier DECIMAL(3,2) DEFAULT 1.00,
    distance_km DECIMAL(8,2),
    duration_seconds INT,

    -- Payment
    payment_method_id VARCHAR(100),
    payment_status VARCHAR(20),  -- pending, paid, failed

    INDEX idx_rider (rider_id, created_at DESC),
    INDEX idx_driver (driver_id, created_at DESC),
    INDEX idx_status (status),
    INDEX idx_requested_at (requested_at)
);
```

#### Ratings Table
```sql
CREATE TABLE ratings (
    rating_id BIGSERIAL PRIMARY KEY,
    ride_id BIGINT NOT NULL REFERENCES rides(ride_id),
    from_user_id BIGINT NOT NULL REFERENCES users(user_id),
    to_user_id BIGINT NOT NULL REFERENCES users(user_id),
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (ride_id, from_user_id)
);
```

### 6.2 Redis (Geospatial Index)

#### Driver Positions
```redis
# Store driver locations in geo index
GEOADD drivers:online {longitude} {latitude} {driver_id}

# Example
GEOADD drivers:online -122.4194 37.7749 driver_456

# Find drivers within 5km radius
GEORADIUS drivers:online -122.4194 37.7749 5 km WITHDIST WITHCOORD ASC COUNT 20

# Remove offline driver
ZREM drivers:online driver_456
```

**Data Structure**:
- Key: `drivers:online` (sorted set with geohash scores)
- Member: `driver_id`
- Score: Geohash of (lat, lng)

#### Driver Metadata Cache
```redis
# Cache driver details for fast lookups
HSET driver:456 name "John Doe" rating 4.8 vehicle "Toyota Camry" status "online"

# Get driver info
HGETALL driver:456

# TTL: 1 hour
EXPIRE driver:456 3600
```

### 6.3 Cassandra (Location History)

```cql
CREATE TABLE location_history (
    driver_id BIGINT,
    timestamp TIMESTAMP,
    latitude DECIMAL,
    longitude DECIMAL,
    heading INT,
    speed DECIMAL,
    PRIMARY KEY (driver_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Query recent locations for driver
SELECT * FROM location_history
WHERE driver_id = 456
  AND timestamp > '2024-12-05 09:00:00'
LIMIT 100;
```

**Why Cassandra?**
- Write-heavy workload (150K writes/sec)
- Time-series data
- Append-only (no updates)
- Horizontal scalability
- Partition by driver_id for even distribution

---

## 7. DEEP DIVE

### 7.1 Driver-Rider Matching Algorithm

Este es el componente más crítico del sistema. Debe ser:
- **Rápido**: < 5 segundos
- **Justo**: No discriminar conductores
- **Eficiente**: Minimizar distancia/tiempo vacío
- **Escalable**: Manejar 1.5K requests/sec

#### Step 1: Geospatial Search

```python
def find_nearby_drivers(pickup_lat, pickup_lng, radius_km=5):
    """
    Find drivers within radius using Redis GEORADIUS.

    Time Complexity: O(N + log(M))
    - N = drivers within radius
    - M = total drivers in sorted set
    """
    redis_key = "drivers:online"

    # GEORADIUS returns drivers sorted by distance
    nearby = redis_client.georadius(
        redis_key,
        pickup_lng,  # Redis uses (lng, lat) order!
        pickup_lat,
        radius_km,
        unit='km',
        withdist=True,
        withcoord=True,
        sort='ASC',
        count=50  # Limit candidates
    )

    # nearby = [
    #   (driver_id, distance_km, (lng, lat)),
    #   ...
    # ]
    return nearby
```

**Redis GEORADIUS Performance**:
- 1M drivers indexed
- Query time: ~5ms (in-memory)
- Returns sorted by distance

#### Step 2: Candidate Filtering

```python
def filter_candidates(candidates, ride_type):
    """
    Filter drivers by:
    - Vehicle type matches ride request
    - Status is 'online' (not on another trip)
    - Acceptance rate > 80%
    """
    eligible = []

    for driver_id, distance, coords in candidates:
        # Fetch driver metadata from cache
        driver_info = redis_client.hgetall(f"driver:{driver_id}")

        if (driver_info['status'] == 'online' and
            driver_info['vehicle_type'] == ride_type and
            float(driver_info['acceptance_rate']) > 80.0):

            eligible.append({
                'driver_id': driver_id,
                'distance': distance,
                'coords': coords,
                'rating': float(driver_info['rating']),
                'acceptance_rate': float(driver_info['acceptance_rate'])
            })

    return eligible
```

#### Step 3: Scoring & Selection

```python
def score_driver(driver, distance):
    """
    Score formula:
    score = w1*(1 - distance/max_distance) + w2*rating/5 + w3*acceptance_rate/100

    Weights:
    - Distance: 50%
    - Rating: 30%
    - Acceptance rate: 20%
    """
    MAX_DISTANCE = 10.0  # km
    W_DISTANCE = 0.5
    W_RATING = 0.3
    W_ACCEPTANCE = 0.2

    distance_score = 1 - min(distance / MAX_DISTANCE, 1.0)
    rating_score = driver['rating'] / 5.0
    acceptance_score = driver['acceptance_rate'] / 100.0

    total_score = (
        W_DISTANCE * distance_score +
        W_RATING * rating_score +
        W_ACCEPTANCE * acceptance_score
    )

    return total_score

def select_best_driver(eligible_drivers):
    """Select driver with highest score."""
    if not eligible_drivers:
        return None

    scored = [
        (driver, score_driver(driver, driver['distance']))
        for driver in eligible_drivers
    ]

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    best_driver, best_score = scored[0]
    return best_driver
```

#### Step 4: Atomic Assignment

**Problem**: Evitar que un conductor acepte 2 viajes simultáneamente.

**Solution**: Distributed lock con Redis.

```python
def assign_driver_to_ride(ride_id, driver_id):
    """
    Atomically assign driver to ride using Redis distributed lock.
    """
    lock_key = f"driver_lock:{driver_id}"
    lock_value = f"ride:{ride_id}"

    # Try to acquire lock (expires in 10 seconds)
    acquired = redis_client.set(
        lock_key,
        lock_value,
        nx=True,  # Only set if not exists
        ex=10     # Expire in 10 seconds
    )

    if not acquired:
        # Driver already locked by another ride
        return False

    try:
        # Update database: assign driver to ride
        with db.transaction():
            ride = db.query("SELECT * FROM rides WHERE ride_id = %s FOR UPDATE", ride_id)
            if ride['status'] != 'requested':
                return False

            driver = db.query("SELECT * FROM drivers WHERE driver_id = %s FOR UPDATE", driver_id)
            if driver['status'] != 'online':
                return False

            # Assign
            db.execute("""
                UPDATE rides
                SET driver_id = %s, status = 'matched', matched_at = NOW()
                WHERE ride_id = %s
            """, (driver_id, ride_id))

            db.execute("""
                UPDATE drivers
                SET status = 'on_trip'
                WHERE driver_id = %s
            """, (driver_id,))

        # Notify driver via push notification
        send_push_notification(driver_id, {
            'type': 'ride_request',
            'ride_id': ride_id
        })

        return True

    finally:
        # Release lock
        redis_client.delete(lock_key)
```

#### Complete Matching Flow

```python
class MatchingService:
    def find_driver_for_ride(self, ride_id):
        """
        Complete matching algorithm.
        Timeout: 5 seconds max.
        """
        start_time = time.time()
        TIMEOUT = 5.0

        # Get ride details
        ride = self.get_ride(ride_id)

        # Step 1: Geospatial search (5ms)
        candidates = find_nearby_drivers(
            ride['pickup_lat'],
            ride['pickup_lng'],
            radius_km=5
        )

        if not candidates:
            # Expand search radius
            candidates = find_nearby_drivers(
                ride['pickup_lat'],
                ride['pickup_lng'],
                radius_km=10
            )

        if not candidates:
            return None  # No drivers available

        # Step 2: Filter (10ms for 50 candidates)
        eligible = filter_candidates(candidates, ride['ride_type'])

        # Step 3: Score & select (1ms)
        best_driver = select_best_driver(eligible)

        if not best_driver:
            return None

        # Step 4: Atomic assignment (50ms - DB transaction)
        success = assign_driver_to_ride(ride_id, best_driver['driver_id'])

        if not success:
            # Driver was taken, try next best
            eligible.remove(best_driver)
            if eligible:
                next_best = select_best_driver(eligible)
                success = assign_driver_to_ride(ride_id, next_best['driver_id'])

        elapsed = time.time() - start_time
        print(f"Matching completed in {elapsed:.3f}s")

        return best_driver if success else None
```

**Performance Breakdown**:
```
Geospatial search: 5ms
Candidate filtering: 10ms (50 drivers × 0.2ms cache lookup)
Scoring: 1ms
DB transaction: 50ms (pessimistic locking)
Total: ~66ms ✅
```

### 7.2 Surge Pricing Algorithm

**Objetivo**: Ajustar precios dinámicamente basado en oferta/demanda.

#### Demand Calculation

```python
def calculate_demand_supply_ratio(lat, lng, radius_km=3):
    """
    Calculate demand/supply ratio in area.

    Demand = # of recent ride requests (last 5 min)
    Supply = # of online drivers
    """
    # Query recent requests in area (from PostgreSQL)
    recent_requests = db.query("""
        SELECT COUNT(*) as count
        FROM rides
        WHERE status IN ('requested', 'searching')
          AND requested_at > NOW() - INTERVAL '5 minutes'
          AND ST_DWithin(
              ST_MakePoint(pickup_lng, pickup_lat)::geography,
              ST_MakePoint(%s, %s)::geography,
              %s
          )
    """, (lng, lat, radius_km * 1000))

    demand = recent_requests['count']

    # Count online drivers in area (from Redis)
    supply = redis_client.georadius(
        'drivers:online',
        lng,
        lat,
        radius_km,
        unit='km',
        count=True
    )

    if supply == 0:
        return float('inf')

    ratio = demand / supply
    return ratio

def calculate_surge_multiplier(demand_supply_ratio):
    """
    Calculate surge multiplier based on ratio.

    Ratio    | Surge
    ---------|-------
    < 1.0    | 1.0x (no surge)
    1.0-2.0  | 1.2x
    2.0-3.0  | 1.5x
    3.0-5.0  | 2.0x
    > 5.0    | 2.5x (max)
    """
    if demand_supply_ratio < 1.0:
        return 1.0
    elif demand_supply_ratio < 2.0:
        return 1.2
    elif demand_supply_ratio < 3.0:
        return 1.5
    elif demand_supply_ratio < 5.0:
        return 2.0
    else:
        return 2.5  # Cap at 2.5x

def get_surge_multiplier(lat, lng):
    """
    Get surge with caching (update every 1 minute).
    """
    cache_key = f"surge:{lat:.2f}:{lng:.2f}"

    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return float(cached)

    # Calculate
    ratio = calculate_demand_supply_ratio(lat, lng)
    multiplier = calculate_surge_multiplier(ratio)

    # Cache for 1 minute
    redis_client.setex(cache_key, 60, multiplier)

    return multiplier
```

#### Fare Calculation

```python
def calculate_fare(distance_km, duration_minutes, surge_multiplier):
    """
    Base fare formula:
    fare = base + (distance × rate_per_km) + (duration × rate_per_min)

    Then apply surge multiplier.
    """
    BASE_FARE = 2.50
    RATE_PER_KM = 1.50
    RATE_PER_MIN = 0.30
    MIN_FARE = 5.00

    base_fare = (
        BASE_FARE +
        distance_km * RATE_PER_KM +
        duration_minutes * RATE_PER_MIN
    )

    # Apply surge
    surge_fare = base_fare * surge_multiplier

    # Apply minimum
    final_fare = max(surge_fare, MIN_FARE)

    return round(final_fare, 2)
```

### 7.3 Real-time Location Tracking

**Desafío**: 1M usuarios concurrentes rastreando conductores en tiempo real.

#### Architecture Choice: WebSockets

**Why WebSockets?**
- Bidirectional communication
- Low latency (< 100ms)
- Efficient (one connection per client)
- Persistent connection

**Alternatives Rejected**:
- ❌ HTTP Polling: Ineficiente (muchas requests vacías)
- ❌ Server-Sent Events (SSE): Unidirectional only

#### WebSocket Server Design

```python
# Using FastAPI + WebSockets

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from collections import defaultdict

app = FastAPI()

# In-memory mapping: ride_id -> [websocket_connections]
active_connections = defaultdict(list)

@app.websocket("/ws/rides/{ride_id}/track")
async def track_ride(websocket: WebSocket, ride_id: int):
    """
    Rider connects to track driver location during trip.
    """
    await websocket.accept()
    active_connections[ride_id].append(websocket)

    try:
        # Send initial driver location
        location = await get_current_driver_location(ride_id)
        await websocket.send_json(location)

        # Keep connection alive
        while True:
            # Receive ping from client (keep-alive)
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        # Client disconnected
        active_connections[ride_id].remove(websocket)

async def broadcast_location_update(ride_id, location_data):
    """
    Broadcast location update to all riders tracking this ride.
    Called when driver sends location update.
    """
    connections = active_connections.get(ride_id, [])

    # Send to all connected clients
    dead_connections = []
    for websocket in connections:
        try:
            await websocket.send_json(location_data)
        except:
            # Connection broken
            dead_connections.append(websocket)

    # Cleanup dead connections
    for dead in dead_connections:
        connections.remove(dead)
```

#### Driver Location Update Flow

```python
@app.post("/api/v1/drivers/location")
async def update_driver_location(location: DriverLocation):
    """
    Driver sends location update every 4 seconds.

    Must be VERY fast: < 50ms
    """
    # 1. Update Redis geospatial index (3ms)
    redis_client.geoadd(
        'drivers:online',
        location.longitude,
        location.latitude,
        location.driver_id
    )

    # 2. If driver is on a trip, broadcast to rider (5ms)
    current_ride = get_driver_current_ride(location.driver_id)  # from cache
    if current_ride:
        await broadcast_location_update(current_ride['ride_id'], {
            'latitude': location.latitude,
            'longitude': location.longitude,
            'heading': location.heading,
            'timestamp': location.timestamp
        })

    # 3. Asynchronously save to Cassandra (don't wait)
    asyncio.create_task(save_location_history(location))

    return {'acknowledged': True}

async def save_location_history(location):
    """
    Save to Cassandra asynchronously (20ms).
    """
    cassandra_session.execute("""
        INSERT INTO location_history
        (driver_id, timestamp, latitude, longitude, heading, speed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        location.driver_id,
        location.timestamp,
        location.latitude,
        location.longitude,
        location.heading,
        location.speed
    ))
```

**Performance**:
```
Update Redis: 3ms
Broadcast WebSocket: 5ms
Total: 8ms ✅ (target < 50ms)
```

#### Scaling WebSocket Servers

**Problem**: Cómo escalar a 1M conexiones concurrentes?

**Solution**: Sharding + Redis Pub/Sub

```
┌────────────┐       ┌────────────┐       ┌────────────┐
│ WebSocket  │       │ WebSocket  │       │ WebSocket  │
│ Server 1   │       │ Server 2   │       │ Server 3   │
│ (300K conn)│       │ (300K conn)│       │ (400K conn)│
└──────┬─────┘       └──────┬─────┘       └──────┬─────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                            │
                     ┌──────▼─────┐
                     │   Redis    │
                     │  Pub/Sub   │
                     └────────────┘
```

**How it works**:
1. Driver sends location to any WebSocket server
2. Server publishes to Redis channel: `ride:{ride_id}:location`
3. All WebSocket servers subscribe to relevant channels
4. Server broadcasts to its connected clients

```python
# Subscribe to Redis channels for active rides
async def subscribe_to_ride_updates():
    pubsub = redis_client.pubsub()

    # Subscribe to all ride channels
    # (In practice, subscribe dynamically as clients connect)
    await pubsub.psubscribe('ride:*:location')

    async for message in pubsub.listen():
        if message['type'] == 'pmessage':
            # Parse ride_id from channel name
            channel = message['channel']  # 'ride:789:location'
            ride_id = int(channel.split(':')[1])

            # Broadcast to connected clients
            location_data = json.loads(message['data'])
            await broadcast_location_update(ride_id, location_data)
```

---

## 8. DISCUSSION

### 8.1 Trade-offs

#### 1. Eventual Consistency en Location Updates

**Trade-off**: Priorizar availability sobre strong consistency.

**Justificación**:
- Location updates pueden estar 1-2 segundos desactualizados
- No crítico para seguridad (usuario ve conductor "acercándose")
- Permite sistema AP (alta disponibilidad)

**Pro**:
- ✅ Sistema más rápido (sin coordinación distribuida)
- ✅ Tolera particiones de red
- ✅ Menor latencia para usuarios

**Con**:
- ❌ Mapa puede mostrar posición ligeramente desactualizada
- ❌ ETA puede ser menos preciso

#### 2. Redis Geospatial vs PostgreSQL PostGIS

**Opción A: Redis GEORADIUS**
- ✅ In-memory: < 5ms latency
- ✅ Simple API
- ❌ No durability (datos en RAM)
- ❌ Limitado a 1 dimension (distancia)

**Opción B: PostgreSQL + PostGIS**
- ✅ ACID transactions
- ✅ Durability
- ✅ Advanced geospatial queries
- ❌ Slower: ~50ms latency
- ❌ Harder to scale writes

**Decisión**: **Redis GEORADIUS**
- Matching speed es crítico (< 5s total)
- Driver positions son ephemeral (no necesitan durability)
- Escribimos a Cassandra para histórico

#### 3. WebSockets vs HTTP Polling para Tracking

**WebSockets**:
- ✅ Latencia baja (< 100ms)
- ✅ Eficiente (una conexión)
- ❌ Stateful (más difícil de escalar)
- ❌ Requiere sticky sessions

**HTTP Polling**:
- ✅ Stateless (fácil balanceo)
- ✅ Simple
- ❌ Latencia alta (1-2 segundos)
- ❌ Ineficiente (muchas requests vacías)

**Decisión**: **WebSockets**
- Real-time experience es clave
- Escalar con Redis Pub/Sub

#### 4. Surge Pricing: Real-time vs Cached

**Real-time Calculation**:
- ✅ Siempre actualizado
- ❌ Query costoso por request
- ❌ Sobrecarga en DB

**Cached (1 minuto)**:
- ✅ Fast (< 1ms)
- ✅ Reduce load
- ❌ Puede estar desactualizado 1 min

**Decisión**: **Cached con TTL 1 minuto**
- Precios no cambian cada segundo
- Reducir 99% de queries

### 8.2 Alternativas Descartadas

#### 1. Single Database para Todo

**Rejected**: Usar solo PostgreSQL para location tracking.

**Razón**:
- 150K writes/sec excede capacidad de single instance
- Sharding por driver_id es complejo
- Cassandra es mejor para time-series

#### 2. Fanout on Read para Location Updates

**Rejected**: Rider hace polling a driver location.

**Razón**:
- Latencia alta (2-3 segundos)
- Overhead en driver service (500K QPS)
- Mala UX (mapa no "smooth")

#### 3. Broadcast Location a Todos los Riders Nearby

**Rejected**: Mostrar todos los conductores cercanos en mapa.

**Razón**:
- Privacy concern (revelar posiciones de todos)
- Overhead de bandwidth (muchas ubicaciones innecesarias)
- Solo mostrar conductor asignado

### 8.3 Scaling Considerations

#### Horizontal Scaling

**Stateless Services** (fácil escalar):
- Ride Service
- Driver Service
- Matching Service
- Pricing Service

Simplemente agregar más instancias detrás de load balancer.

**Stateful Services** (más complejo):
- WebSocket Servers: usar Redis Pub/Sub para coordinar
- Redis Cluster: sharding por key prefix

#### Database Scaling

**PostgreSQL**:
- Read replicas para queries (5 replicas)
- Sharding por `user_id` si crece mucho

**Cassandra**:
- Already distributed (6 nodos inicialmente)
- Add nodes as needed
- Replication factor: 3

**Redis**:
- Redis Cluster con 10 nodos
- Sharding automático por key hash

#### Geographic Distribution

Deploy en múltiples regiones:
```
US-West:    San Francisco, Los Angeles
US-East:    New York, Miami
Europe:     London, Amsterdam
Asia:       Singapore, Mumbai
```

**Routing Strategy**:
- API Gateway route por geolocation
- Driver/rider interactúa con datacenter más cercano
- Cross-region replication para durability

---

## 9. IMPLEMENTACIÓN

### 9.1 Matching Service (Completo)

```python
# matching_service.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Tuple
import redis
import psycopg2
import time
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# Connections
redis_client = redis.Redis(host='redis-cluster', port=6379, decode_responses=True)
db_conn = psycopg2.connect("postgresql://user:pass@postgres:5432/uber")

# Models
class MatchRequest(BaseModel):
    ride_id: int
    pickup_lat: float
    pickup_lng: float
    ride_type: str  # uberX, uberXL, uberBlack

class MatchResponse(BaseModel):
    driver_id: int
    distance_km: float
    eta_seconds: int
    driver_name: str
    driver_rating: float
    vehicle_info: str

# Configuration
GEOSPATIAL_KEY = "drivers:online"
SEARCH_RADIUS_KM = 5
MAX_SEARCH_RADIUS_KM = 10
MATCHING_TIMEOUT_SECONDS = 5
MIN_ACCEPTANCE_RATE = 80.0

def find_nearby_drivers(lat: float, lng: float, radius_km: float, limit: int = 50) -> List[Tuple]:
    """
    Query Redis GEORADIUS to find drivers within radius.
    Returns: [(driver_id, distance_km, (lng, lat)), ...]
    """
    try:
        results = redis_client.georadius(
            GEOSPATIAL_KEY,
            lng,  # Redis uses (lng, lat) order
            lat,
            radius_km,
            unit='km',
            withdist=True,
            withcoord=True,
            sort='ASC',
            count=limit
        )
        return results
    except Exception as e:
        logger.error(f"Redis GEORADIUS error: {e}")
        return []

def get_driver_metadata(driver_id: str) -> Optional[dict]:
    """Fetch driver details from Redis cache."""
    try:
        data = redis_client.hgetall(f"driver:{driver_id}")
        if not data:
            return None
        return {
            'driver_id': int(driver_id),
            'name': data.get('name'),
            'rating': float(data.get('rating', 5.0)),
            'vehicle_type': data.get('vehicle_type'),
            'vehicle_info': data.get('vehicle_info'),
            'status': data.get('status'),
            'acceptance_rate': float(data.get('acceptance_rate', 100.0))
        }
    except Exception as e:
        logger.error(f"Error fetching driver metadata: {e}")
        return None

def filter_eligible_drivers(candidates: List[Tuple], ride_type: str) -> List[dict]:
    """
    Filter candidates by:
    - Vehicle type matches
    - Status is online
    - Acceptance rate > threshold
    """
    eligible = []

    for driver_id, distance, coords in candidates:
        metadata = get_driver_metadata(driver_id)

        if not metadata:
            continue

        if (metadata['status'] == 'online' and
            metadata['vehicle_type'] == ride_type and
            metadata['acceptance_rate'] >= MIN_ACCEPTANCE_RATE):

            metadata['distance_km'] = distance
            metadata['coords'] = coords
            eligible.append(metadata)

    return eligible

def calculate_driver_score(driver: dict) -> float:
    """
    Multi-factor scoring:
    score = 0.5 * distance_score + 0.3 * rating_score + 0.2 * acceptance_score
    """
    MAX_DISTANCE = 10.0

    # Normalize distance (closer = better)
    distance_score = max(0, 1 - driver['distance_km'] / MAX_DISTANCE)

    # Normalize rating (higher = better)
    rating_score = driver['rating'] / 5.0

    # Normalize acceptance rate
    acceptance_score = driver['acceptance_rate'] / 100.0

    total_score = (
        0.5 * distance_score +
        0.3 * rating_score +
        0.2 * acceptance_score
    )

    return total_score

def select_best_driver(eligible_drivers: List[dict]) -> Optional[dict]:
    """Select driver with highest score."""
    if not eligible_drivers:
        return None

    # Score all drivers
    scored = [(driver, calculate_driver_score(driver)) for driver in eligible_drivers]

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    best_driver, best_score = scored[0]
    logger.info(f"Best driver: {best_driver['driver_id']} with score {best_score:.3f}")

    return best_driver

def acquire_driver_lock(driver_id: int, ride_id: int) -> bool:
    """
    Acquire distributed lock for driver.
    Returns True if lock acquired, False if driver already locked.
    """
    lock_key = f"driver_lock:{driver_id}"
    lock_value = f"ride:{ride_id}"

    # NX = only set if not exists, EX = expiration in seconds
    acquired = redis_client.set(lock_key, lock_value, nx=True, ex=10)

    return acquired is not None

def release_driver_lock(driver_id: int):
    """Release distributed lock."""
    lock_key = f"driver_lock:{driver_id}"
    redis_client.delete(lock_key)

def assign_driver_to_ride_db(ride_id: int, driver_id: int) -> bool:
    """
    Atomically assign driver to ride in database.
    Uses pessimistic locking (SELECT FOR UPDATE).
    """
    cursor = db_conn.cursor()

    try:
        cursor.execute("BEGIN")

        # Lock ride row
        cursor.execute("""
            SELECT status FROM rides
            WHERE ride_id = %s
            FOR UPDATE
        """, (ride_id,))

        ride = cursor.fetchone()
        if not ride or ride[0] != 'requested':
            cursor.execute("ROLLBACK")
            return False

        # Lock driver row
        cursor.execute("""
            SELECT status FROM drivers
            WHERE driver_id = %s
            FOR UPDATE
        """, (driver_id,))

        driver = cursor.fetchone()
        if not driver or driver[0] != 'online':
            cursor.execute("ROLLBACK")
            return False

        # Assign driver to ride
        cursor.execute("""
            UPDATE rides
            SET driver_id = %s, status = 'matched', matched_at = NOW()
            WHERE ride_id = %s
        """, (driver_id, ride_id))

        # Update driver status
        cursor.execute("""
            UPDATE drivers
            SET status = 'on_trip'
            WHERE driver_id = %s
        """, (driver_id,))

        cursor.execute("COMMIT")
        return True

    except Exception as e:
        cursor.execute("ROLLBACK")
        logger.error(f"DB assignment error: {e}")
        return False

    finally:
        cursor.close()

def calculate_eta(driver_coords: Tuple[float, float], pickup_coords: Tuple[float, float]) -> int:
    """
    Calculate ETA in seconds.
    Simplified: assume average speed 30 km/h in city.
    In production: call Google Maps API.
    """
    from math import radians, sin, cos, sqrt, atan2

    # Haversine formula for distance
    lat1, lon1 = radians(pickup_coords[0]), radians(pickup_coords[1])
    lat2, lon2 = radians(driver_coords[1]), radians(driver_coords[0])  # coords are (lng, lat)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance_km = 6371 * c  # Earth radius

    # Average city speed: 30 km/h
    AVERAGE_SPEED_KMH = 30
    eta_hours = distance_km / AVERAGE_SPEED_KMH
    eta_seconds = int(eta_hours * 3600)

    return eta_seconds

@app.post("/find-driver", response_model=MatchResponse)
def find_driver_for_ride(request: MatchRequest):
    """
    Main endpoint: Find and assign best driver for ride.

    Steps:
    1. Geospatial search (5ms)
    2. Filter candidates (10ms)
    3. Score and select (1ms)
    4. Atomic assignment (50ms)

    Total: ~66ms
    """
    start_time = time.time()

    logger.info(f"Finding driver for ride {request.ride_id}")

    # Step 1: Geospatial search
    candidates = find_nearby_drivers(
        request.pickup_lat,
        request.pickup_lng,
        SEARCH_RADIUS_KM
    )

    if not candidates:
        # Expand search radius
        logger.info("No drivers in 5km, expanding to 10km")
        candidates = find_nearby_drivers(
            request.pickup_lat,
            request.pickup_lng,
            MAX_SEARCH_RADIUS_KM
        )

    if not candidates:
        raise HTTPException(status_code=404, detail="No drivers available")

    # Step 2: Filter eligible drivers
    eligible = filter_eligible_drivers(candidates, request.ride_type)

    if not eligible:
        raise HTTPException(status_code=404, detail="No eligible drivers found")

    # Step 3: Select best driver
    best_driver = select_best_driver(eligible)

    if not best_driver:
        raise HTTPException(status_code=500, detail="Driver selection failed")

    # Step 4: Atomic assignment with retry
    MAX_RETRIES = 3
    assigned = False

    for attempt in range(MAX_RETRIES):
        # Acquire lock
        if not acquire_driver_lock(best_driver['driver_id'], request.ride_id):
            logger.warning(f"Driver {best_driver['driver_id']} locked, trying next")

            # Try next best driver
            eligible.remove(best_driver)
            best_driver = select_best_driver(eligible)

            if not best_driver:
                break
            continue

        try:
            # Assign in database
            assigned = assign_driver_to_ride_db(request.ride_id, best_driver['driver_id'])

            if assigned:
                break
        finally:
            release_driver_lock(best_driver['driver_id'])

    if not assigned:
        raise HTTPException(status_code=409, detail="Failed to assign driver")

    # Calculate ETA
    eta = calculate_eta(
        best_driver['coords'],
        (request.pickup_lat, request.pickup_lng)
    )

    elapsed = time.time() - start_time
    logger.info(f"Driver matched in {elapsed:.3f}s")

    return MatchResponse(
        driver_id=best_driver['driver_id'],
        distance_km=best_driver['distance_km'],
        eta_seconds=eta,
        driver_name=best_driver['name'],
        driver_rating=best_driver['rating'],
        vehicle_info=best_driver['vehicle_info']
    )

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

### 9.2 Surge Pricing Service

```python
# pricing_service.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import psycopg2
from datetime import datetime, timedelta

app = FastAPI()

redis_client = redis.Redis(host='redis', decode_responses=True)
db_conn = psycopg2.connect("postgresql://user:pass@postgres:5432/uber")

class FareRequest(BaseModel):
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float
    ride_type: str
    distance_km: float
    duration_minutes: int

class FareResponse(BaseModel):
    base_fare: float
    surge_multiplier: float
    final_fare: float
    currency: str

# Pricing constants
PRICING_CONFIG = {
    'uberX': {
        'base': 2.50,
        'per_km': 1.50,
        'per_min': 0.30,
        'min_fare': 5.00
    },
    'uberXL': {
        'base': 3.50,
        'per_km': 2.00,
        'per_min': 0.40,
        'min_fare': 7.00
    },
    'uberBlack': {
        'base': 5.00,
        'per_km': 3.00,
        'per_min': 0.60,
        'min_fare': 12.00
    }
}

def calculate_demand_supply_ratio(lat: float, lng: float, radius_km: float = 3) -> float:
    """Calculate demand/supply ratio in area."""
    cursor = db_conn.cursor()

    # Count recent ride requests
    cursor.execute("""
        SELECT COUNT(*) FROM rides
        WHERE status IN ('requested', 'searching')
          AND requested_at > %s
          AND ST_DWithin(
              ST_MakePoint(pickup_lng, pickup_lat)::geography,
              ST_MakePoint(%s, %s)::geography,
              %s
          )
    """, (datetime.now() - timedelta(minutes=5), lng, lat, radius_km * 1000))

    demand = cursor.fetchone()[0]
    cursor.close()

    # Count online drivers
    supply = len(redis_client.georadius(
        'drivers:online',
        lng,
        lat,
        radius_km,
        unit='km'
    ) or [])

    if supply == 0:
        return 10.0  # High ratio if no drivers

    return demand / supply

def calculate_surge_multiplier(ratio: float) -> float:
    """Map demand/supply ratio to surge multiplier."""
    if ratio < 1.0:
        return 1.0
    elif ratio < 2.0:
        return 1.2
    elif ratio < 3.0:
        return 1.5
    elif ratio < 5.0:
        return 2.0
    else:
        return 2.5  # Max surge

def get_surge_multiplier_cached(lat: float, lng: float) -> float:
    """Get surge with 1-minute cache."""
    cache_key = f"surge:{lat:.2f}:{lng:.2f}"

    cached = redis_client.get(cache_key)
    if cached:
        return float(cached)

    # Calculate
    ratio = calculate_demand_supply_ratio(lat, lng)
    multiplier = calculate_surge_multiplier(ratio)

    # Cache for 1 minute
    redis_client.setex(cache_key, 60, multiplier)

    return multiplier

@app.post("/calculate-fare", response_model=FareResponse)
def calculate_fare(request: FareRequest):
    """Calculate fare with surge pricing."""

    if request.ride_type not in PRICING_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid ride type")

    config = PRICING_CONFIG[request.ride_type]

    # Base fare calculation
    base_fare = (
        config['base'] +
        request.distance_km * config['per_km'] +
        request.duration_minutes * config['per_min']
    )

    # Apply minimum fare
    base_fare = max(base_fare, config['min_fare'])

    # Get surge multiplier
    surge = get_surge_multiplier_cached(request.pickup_lat, request.pickup_lng)

    # Final fare
    final_fare = round(base_fare * surge, 2)

    return FareResponse(
        base_fare=round(base_fare, 2),
        surge_multiplier=surge,
        final_fare=final_fare,
        currency='USD'
    )
```

---

## 10. EJERCICIOS

### Ejercicio 1: Optimizar Matching Algorithm

**Pregunta**: El algoritmo de matching actual tiene complejidad O(N) donde N = número de candidatos (50). ¿Cómo optimizarías si hubiera 10K conductores online en una ciudad?

**Hints**:
- Grid-based sharding (H3 hexagonal cells)
- Pre-scoring de conductores
- Machine learning para predecir acceptance

### Ejercicio 2: Handle Driver Rejection

**Escenario**: Un conductor rechaza el viaje después de ser matched. ¿Cómo rediseñarías el flow?

**Considera**:
- Timeout para aceptación (30 segundos)
- Fallback a siguiente mejor conductor
- Penalización por rechazo (reducir score)

### Ejercicio 3: Cross-Region Trips

**Pregunta**: ¿Cómo manejarías un viaje que cruza boundaries de regiones (ej: San Francisco → San Jose, 80 km)?

**Considera**:
- Conductor debe poder operar en múltiples regiones
- Pricing puede variar por región
- Data residency requirements

### Ejercicio 4: Fraud Detection

**Escenario**: Detectar viajes falsos (conductor y pasajero coludidos para generar viajes ficticios).

**Señales a detectar**:
- Mismo conductor-pasajero repetidamente
- Viajes muy cortos con pago alto
- GPS spoofing (ubicación no coincide con celltower)

### Ejercicio 5: Disaster Recovery

**Pregunta**: Redis cluster que mantiene posiciones de conductores falla completamente. ¿Cómo recuperarías?

**Opciones**:
- Reconstruir desde location_history en Cassandra
- Pedir a conductores reenviar posición
- Failover a región backup

---

## 📚 CHEAT SHEET

### Números Clave
```
DAU: 30M riders, 1.5M drivers
Concurrent rides: 1M
Location update QPS: 650K
Matching QPS: 1.6K
Storage: 50 TB (90% location history)
Cost: $147K/month
```

### Redis Commands
```bash
# Add driver location
GEOADD drivers:online -122.4194 37.7749 driver_456

# Find drivers within 5km
GEORADIUS drivers:online -122.4194 37.7749 5 km WITHDIST ASC COUNT 20

# Set driver metadata
HSET driver:456 name "John" rating 4.8 status "online"

# Distributed lock
SET driver_lock:456 ride:789 NX EX 10
```

### SQL Queries
```sql
-- Get user ride history
SELECT * FROM rides
WHERE rider_id = 123
ORDER BY requested_at DESC
LIMIT 20;

-- Count rides by status
SELECT status, COUNT(*)
FROM rides
WHERE requested_at > NOW() - INTERVAL '1 hour'
GROUP BY status;

-- Average driver rating
SELECT AVG(rating)
FROM ratings
WHERE to_user_id = 456;
```

### Performance Targets
```
Driver matching: < 5 seconds
Location update: < 100ms
ETA calculation: < 2 seconds
Payment processing: < 3 seconds
WebSocket latency: < 100ms
```

---

## 🎯 PRÓXIMOS PASOS

Has completado el diseño completo de Uber. **Key Takeaways**:

1. **Geospatial indexing** es crucial para ride-sharing (Redis GEORADIUS)
2. **Distributed locking** previene race conditions en matching
3. **WebSockets** para real-time tracking a escala
4. **Surge pricing** balancea oferta/demanda
5. **Hybrid storage**: PostgreSQL (transaccional) + Cassandra (time-series) + Redis (cache)

**Siguiente**: Semana 6 - Caso Real Netflix (CDN, Video Streaming, Recommendation Engine)

---

**Creado**: 2024-12-05
**Versión**: 1.0
**Parte de**: Fase 1 - System Design Fundamentals
