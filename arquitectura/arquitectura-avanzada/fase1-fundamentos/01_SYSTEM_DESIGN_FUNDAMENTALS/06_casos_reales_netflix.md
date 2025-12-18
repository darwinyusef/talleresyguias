# System Design: NETFLIX - Video Streaming Platform

**Semana 6 - Caso Real Completo**
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
- **Video Streaming**: Usuarios pueden reproducir videos con adaptive bitrate
- **Content Catalog**: Browsing y búsqueda de películas/series
- **User Profiles**: Múltiples perfiles por cuenta (hasta 5)
- **Watch Progress**: Reanudar desde donde se quedó
- **Recommendations**: Sugerencias personalizadas basadas en historial
- **Download for Offline**: Descargar contenido para ver sin conexión

#### Secondary Features (P1)
- **Continue Watching**: Fila de contenido empezado
- **My List**: Guardar contenido para ver después
- **Ratings**: Usuarios pueden calificar contenido (👍👎)
- **Subtitles & Audio**: Múltiples idiomas disponibles
- **Parental Controls**: Restricciones por edad

#### Nice to Have (P2)
- **Watch Together**: Sincronizar reproducción entre usuarios
- **Previews**: Auto-play de trailers al navegar
- **Interactive Content**: Contenido con elecciones (Black Mirror: Bandersnatch)

### 1.2 Non-Functional Requirements

#### Scale
- **Subscribers**: 230M worldwide (dato real 2024)
- **DAU**: 100M usuarios activos diarios
- **Concurrent Viewers**: 20M durante peak hours (8-11 PM)
- **Content Library**: 15K títulos, 100K horas de video
- **Geographic Coverage**: 190+ países

#### Performance
- **Startup Time**: < 2 segundos para iniciar video
- **Buffering**: < 0.5% rebuffer ratio
- **Search Latency**: < 200ms
- **Recommendation Load**: < 500ms
- **CDN Hit Rate**: > 95%

#### Availability & Reliability
- **Availability**: 99.99% uptime
- **Video Delivery**: 99.9% success rate (no playback errors)
- **Geo-redundancy**: Multi-region, multi-CDN

#### Bandwidth & Quality
- **Video Quality**: 4K HDR support
- **Bitrates**:
  - SD (480p): 1 Mbps
  - HD (720p): 3 Mbps
  - Full HD (1080p): 5 Mbps
  - 4K (2160p): 25 Mbps
- **Total Bandwidth**: Netflix consume ~15% del tráfico global de internet

---

## 2. ESTIMATIONS

### 2.1 Traffic Estimations

#### Viewers
```
Total Subscribers: 230M
Daily Active Users (DAU): 100M (43% engagement)
Concurrent Peak Viewers: 20M (8-11 PM primetime)

Average Watch Time: 2 hours/day per DAU
Total watch hours/day: 100M × 2 = 200M hours/day
```

#### Content Requests (QPS)

**1. Video Playback Requests**
```
Concurrent viewers: 20M
Each player polls manifest every 10 seconds (for ABR updates)
QPS = 20M / 10 = 2M QPS

This is the HIGHEST QPS in the system!
```

**2. Search/Browse**
```
DAU: 100M
Average searches per session: 3
Total searches/day: 300M
Average QPS: 300M / 86,400 = 3.5K QPS
Peak QPS: 3.5K × 3 = 10.5K QPS
```

**3. Recommendations**
```
Each user loads homepage with recommendations:
- 100M page loads/day
- Average QPS: 100M / 86,400 = 1.2K QPS
- Peak QPS: 3.6K QPS
```

**4. Metadata API (title info, thumbnails)**
```
Each title card viewed = 1 metadata request
Average: 50 titles per session
Total: 100M users × 50 = 5B requests/day
Average QPS: 5B / 86,400 = 58K QPS
Peak QPS: 174K QPS
```

### 2.2 Storage Estimations

#### Video Content Storage

```
Content Library: 15,000 titles
Average movie: 2 hours
Average series: 10 episodes × 45 min = 7.5 hours

Assume 50/50 split:
- 7,500 movies × 2 hours = 15,000 hours
- 7,500 series × 7.5 hours = 56,250 hours
Total content: 71,250 hours

Encoding per title (multiple bitrates + resolutions):
- 4K (25 Mbps): 11.25 GB/hour
- 1080p (5 Mbps): 2.25 GB/hour
- 720p (3 Mbps): 1.35 GB/hour
- 480p (1 Mbps): 450 MB/hour
Total per hour: ~15 GB

Total Storage: 71,250 hours × 15 GB = 1.07 PB (raw video)

Add:
- Multiple audio tracks: +20% (1.28 PB)
- Subtitles (100+ languages): +5% (1.34 PB)
- Backups & redundancy (3x): 4 PB total
```

#### User Data
```
Users: 230M
Profile data per user: 10 KB (preferences, settings)
Total: 230M × 10 KB = 2.3 TB (negligible)

Watch history per user: 500 entries × 100 bytes = 50 KB
Total: 230M × 50 KB = 11.5 TB

Ratings: 230M users × 100 ratings × 20 bytes = 460 GB

Total User Data: ~15 TB
```

**Total Storage: ~4 PB (video) + 15 TB (metadata) = 4.015 PB**

### 2.3 Bandwidth Estimations

#### Egress (Video Delivery)

```
Concurrent viewers: 20M
Average bitrate: 5 Mbps (assume mostly 1080p)
Total bandwidth: 20M × 5 Mbps = 100 Tbps

Peak hour (primetime): 100 Tbps
Off-peak (average): 30 Tbps

Monthly data transfer:
- Average: 30 Tbps × 24 hours × 30 days = 21.6 EB/month
- Netflix real data: ~12-15 EB/month (matches!)
```

**Context**: Netflix is responsible for ~15% of global internet traffic.

#### Ingress (Content Upload)

```
New content added: 100 hours/day (original + licensed)
Upload size: 100 hours × 50 GB/hour (raw 4K) = 5 TB/day
Bandwidth: 5 TB / 86,400 sec = 58 MB/s = 464 Mbps (manageable)
```

### 2.4 Cost Estimation

#### CDN & Bandwidth (Biggest Cost!)
```
Netflix uses:
- Own CDN (Open Connect): Free CDN boxes placed at ISPs
- AWS CloudFront: For regions without Open Connect
- Third-party CDNs: Akamai, Cloudflare

Estimate:
- Open Connect (80% traffic): ~$0 (provided boxes to ISPs)
- CloudFront (15% traffic): 2.25 EB × $20/TB = $45M/month
- Other CDNs (5%): 750 PB × $30/TB = $22.5M/month

Total CDN: ~$67M/month
```

#### Compute (Encoding, Transcoding, ML)
```
Encoding farm: 10,000 instances × $500/month = $5M
Recommendation ML: 500 GPU instances × $2K/month = $1M
Backend services: 5,000 instances × $200/month = $1M
Total Compute: $7M/month
```

#### Storage (S3, S3 Glacier)
```
Hot storage (recent content): 500 TB × $23/TB = $11.5K
Warm storage (S3): 1.5 PB × $10/TB = $15K
Cold storage (Glacier): 2 PB × $1/TB = $2K
Total Storage: $28.5K/month (negligible!)
```

**Total: ~$74M/month = $888M/year**

(Netflix actual content & technology spending: ~$2B/year, includes content acquisition)

---

## 3. SYSTEM INTERFACE

### 3.1 Actors

- **Viewer**: Usuario final viendo contenido
- **Content Team**: Sube y gestiona contenido
- **CDN**: Red de distribución de contenido
- **Encoding Service**: Transcodifica videos
- **Recommendation Engine**: Genera sugerencias personalizadas
- **Analytics**: Tracking de métricas de viewing

### 3.2 High-Level APIs

#### For Viewers
```
GET    /api/v1/browse/home                # Homepage con recomendaciones
GET    /api/v1/search?q={query}           # Buscar contenido
GET    /api/v1/titles/{titleId}           # Detalles de título
POST   /api/v1/playback/start             # Iniciar reproducción
GET    /api/v1/playback/{videoId}/manifest # ABR manifest (MPD/HLS)
POST   /api/v1/playback/progress          # Actualizar progreso
GET    /api/v1/profiles/{profileId}/list  # My List
POST   /api/v1/ratings                    # Calificar contenido
```

#### For Content Management
```
POST   /api/v1/content/upload             # Subir video fuente
GET    /api/v1/content/{contentId}/status # Estado de encoding
POST   /api/v1/content/{contentId}/publish # Publicar a catálogo
PUT    /api/v1/content/{contentId}/metadata # Actualizar metadatos
```

#### Internal APIs
```
POST   /api/internal/encoding/transcode    # Iniciar transcoding job
GET    /api/internal/recommendations/generate # Generar recomendaciones
POST   /api/internal/cdn/invalidate        # Cache invalidation
GET    /api/internal/analytics/metrics     # Viewing metrics
```

---

## 4. HIGH-LEVEL DESIGN

### 4.1 Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                          VIEWERS (CLIENTS)                            │
│  Smart TV | Web Browser | Mobile App | Game Console                  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   API Gateway   │
                    │   (CloudFront)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│  Video Player  │  │   Catalog      │  │ Recommendation │
│  Service       │  │   Service      │  │   Service      │
│                │  │                │  │                │
│ - Manifest     │  │ - Browse       │  │ - Personalized │
│ - License      │  │ - Search       │  │ - ML Models    │
│ - Telemetry    │  │ - Metadata     │  │ - A/B Testing  │
└───────┬────────┘  └───────┬────────┘  └───────┬────────┘
        │                   │                    │
        │           ┌───────▼────────┐           │
        │           │  PostgreSQL    │           │
        │           │  (Metadata DB) │           │
        │           └────────────────┘           │
        │                                        │
┌───────▼─────────────────────────────────────┐ │
│        CDN LAYER (Open Connect)             │ │
├─────────────────────────────────────────────┤ │
│  Regional CDN Nodes (10,000+ locations)     │ │
│  - Stores encoded videos (all bitrates)     │ │
│  - Serves 95%+ of requests from cache       │ │
└───────┬─────────────────────────────────────┘ │
        │                                        │
┌───────▼────────────────────────────────┐      │
│  Origin Storage (AWS S3)               │      │
│  - Master copies of all content        │      │
│  - Multi-region replication            │      │
└───────┬────────────────────────────────┘      │
        │                                        │
┌───────▼────────────────────────────────┐      │
│  Encoding Pipeline                     │      │
│  ┌──────────┐   ┌──────────┐          │      │
│  │ Source   │──▶│Transcode │──┐       │      │
│  │ Video    │   │ (ffmpeg) │  │       │      │
│  └──────────┘   └──────────┘  │       │      │
│                                │       │      │
│  ┌─────────────────────────────▼──┐   │      │
│  │  Output: 4K, 1080p, 720p, 480p│   │      │
│  │  Audio: Multiple languages     │   │      │
│  │  Subtitles: 100+ languages     │   │      │
│  └────────────────────────────────┘   │      │
└────────────────────────────────────────┘      │
                                                 │
┌────────────────────────────────────────────────▼──┐
│  Recommendation Engine (Apache Spark + ML)        │
│  - Collaborative Filtering                        │
│  - Content-based Filtering                        │
│  - Deep Learning Models                           │
│  - A/B Testing Framework                          │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│  Analytics & Monitoring                           │
│  - Kafka: Real-time event streaming               │
│  - Elasticsearch: Logging & search                │
│  - Prometheus + Grafana: Metrics                  │
└───────────────────────────────────────────────────┘
```

### 4.2 Component Responsibilities

#### API Gateway (AWS CloudFront / Custom)
- TLS termination
- Authentication (JWT tokens)
- Rate limiting
- Request routing
- Static asset serving (thumbnails, metadata)

#### Video Player Service
- Generate ABR manifests (DASH MPD or HLS m3u8)
- DRM license management (Widevine, PlayReady, FairPlay)
- Playback telemetry collection
- Session management

#### Catalog Service
- Browse & search functionality
- Metadata management (title, description, cast, genre)
- Thumbnail generation & serving
- Content availability by region

#### Recommendation Service
- Personalized homepage rows
- "Because you watched X" suggestions
- Trending & popular content
- A/B testing of algorithms

#### CDN (Open Connect)
- **Critical component!** 95%+ of traffic served from edge
- Netflix deploys servers to ISP datacenters (free for ISPs)
- Stores all encoded video chunks
- Prefetch popular content based on predictions

#### Encoding Pipeline
- Transcode source video to multiple bitrates/resolutions
- Generate thumbnails & preview clips
- Extract metadata (duration, aspect ratio, etc.)
- Quality control checks

#### Origin Storage (S3)
- Master copies of all content
- Multi-region replication (US, EU, APAC)
- Lifecycle policies (archive to Glacier)

---

## 5. API DESIGN

### 5.1 Start Playback

**Endpoint**: `POST /api/v1/playback/start`

**Request**:
```json
{
  "profileId": "profile_123",
  "titleId": "title_456",
  "episodeId": "episode_789",  // For series
  "deviceId": "device_abc",
  "clientCapabilities": {
    "maxResolution": "4K",
    "supportedCodecs": ["h264", "h265", "vp9", "av1"],
    "drmSystems": ["widevine"]
  }
}
```

**Response**:
```json
{
  "playbackId": "playback_xyz",
  "manifestUrl": "https://cdn.netflix.com/videos/12345/manifest.mpd",
  "licenseUrl": "https://license.netflix.com/widevine",
  "resumePosition": 320,  // seconds (if previously watched)
  "expiresAt": "2024-12-05T12:00:00Z"
}
```

### 5.2 Get ABR Manifest

**Endpoint**: `GET /api/v1/playback/{videoId}/manifest.mpd`

**Response** (DASH MPD - XML):
```xml
<?xml version="1.0"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011">
  <Period duration="PT2H">
    <!-- 4K Video Representation -->
    <AdaptationSet mimeType="video/mp4" codecs="h264">
      <Representation id="4k" bandwidth="25000000" width="3840" height="2160">
        <BaseURL>https://cdn.netflix.com/videos/12345/4k/</BaseURL>
        <SegmentTemplate media="chunk_$Number$.m4s" startNumber="1" duration="4"/>
      </Representation>

      <!-- 1080p Video Representation -->
      <Representation id="1080p" bandwidth="5000000" width="1920" height="1080">
        <BaseURL>https://cdn.netflix.com/videos/12345/1080p/</BaseURL>
        <SegmentTemplate media="chunk_$Number$.m4s" startNumber="1" duration="4"/>
      </Representation>

      <!-- 720p, 480p omitted for brevity -->
    </AdaptationSet>

    <!-- Audio Adaptation Set -->
    <AdaptationSet mimeType="audio/mp4" codecs="aac" lang="en">
      <Representation id="audio_en" bandwidth="128000">
        <BaseURL>https://cdn.netflix.com/videos/12345/audio_en/</BaseURL>
        <SegmentTemplate media="chunk_$Number$.m4s" startNumber="1" duration="4"/>
      </Representation>
    </AdaptationSet>

    <!-- Subtitles -->
    <AdaptationSet mimeType="text/vtt" lang="en">
      <Representation id="subtitle_en">
        <BaseURL>https://cdn.netflix.com/videos/12345/subtitles_en.vtt</BaseURL>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
```

**Key Points**:
- Each video is split into 4-second chunks
- Player fetches manifest, then requests chunks adaptively
- Player monitors bandwidth and switches quality on-the-fly

### 5.3 Update Watch Progress

**Endpoint**: `POST /api/v1/playback/progress`

**Request**:
```json
{
  "playbackId": "playback_xyz",
  "profileId": "profile_123",
  "titleId": "title_456",
  "position": 450,  // seconds
  "duration": 7200,
  "timestamp": "2024-12-05T10:30:00Z"
}
```

**Response**:
```json
{
  "acknowledged": true
}
```

**Notes**:
- Called every 30 seconds during playback
- Allows "Continue Watching" functionality
- Used for analytics (watch time, engagement)

### 5.4 Get Recommendations

**Endpoint**: `GET /api/v1/browse/home?profileId={profileId}`

**Response**:
```json
{
  "rows": [
    {
      "id": "row_1",
      "title": "Trending Now",
      "items": [
        {
          "titleId": "title_123",
          "type": "movie",
          "title": "Inception",
          "thumbnail": "https://cdn.netflix.com/thumbnails/inception_large.jpg",
          "matchScore": 0.95,
          "duration": 148,
          "releaseYear": 2010
        },
        // ... more titles
      ]
    },
    {
      "id": "row_2",
      "title": "Because You Watched 'Stranger Things'",
      "items": [...]
    },
    {
      "id": "row_3",
      "title": "Top 10 in Your Country",
      "items": [...]
    }
  ]
}
```

---

## 6. DATA MODEL

### 6.1 PostgreSQL (Metadata)

#### Titles Table
```sql
CREATE TABLE titles (
    title_id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    type VARCHAR(20) NOT NULL,  -- 'movie' or 'series'
    release_year INT,
    duration_minutes INT,  -- For movies
    maturity_rating VARCHAR(10),  -- G, PG, PG-13, R, etc.
    genres VARCHAR(100)[],  -- Array of genres
    cast_members TEXT[],
    director VARCHAR(255),
    thumbnail_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_type (type),
    INDEX idx_genres USING GIN (genres)
);

CREATE TABLE episodes (
    episode_id BIGSERIAL PRIMARY KEY,
    series_id BIGINT REFERENCES titles(title_id),
    season_number INT NOT NULL,
    episode_number INT NOT NULL,
    title VARCHAR(255),
    description TEXT,
    duration_minutes INT,
    release_date DATE,
    thumbnail_url VARCHAR(500),
    UNIQUE (series_id, season_number, episode_number)
);
```

#### Video Assets Table
```sql
CREATE TABLE video_assets (
    asset_id BIGSERIAL PRIMARY KEY,
    title_id BIGINT REFERENCES titles(title_id),
    episode_id BIGINT REFERENCES episodes(episode_id),
    encoding_profile VARCHAR(50),  -- '4k_h265', '1080p_h264', etc.
    bitrate_kbps INT,
    resolution VARCHAR(20),  -- '3840x2160', '1920x1080', etc.
    codec VARCHAR(20),
    file_size_bytes BIGINT,
    manifest_url VARCHAR(500),
    cdn_status VARCHAR(20),  -- 'pending', 'distributed', 'ready'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE audio_tracks (
    track_id BIGSERIAL PRIMARY KEY,
    title_id BIGINT,
    language VARCHAR(10),  -- 'en', 'es', 'fr', etc.
    codec VARCHAR(20),
    bitrate_kbps INT,
    file_url VARCHAR(500)
);

CREATE TABLE subtitles (
    subtitle_id BIGSERIAL PRIMARY KEY,
    title_id BIGINT,
    language VARCHAR(10),
    format VARCHAR(20),  -- 'vtt', 'srt'
    file_url VARCHAR(500)
);
```

#### User Data
```sql
CREATE TABLE accounts (
    account_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    subscription_plan VARCHAR(50),  -- 'basic', 'standard', 'premium'
    billing_date DATE,
    status VARCHAR(20),  -- 'active', 'cancelled', 'suspended'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE profiles (
    profile_id BIGSERIAL PRIMARY KEY,
    account_id BIGINT REFERENCES accounts(account_id),
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    is_kids BOOLEAN DEFAULT FALSE,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE watch_history (
    id BIGSERIAL PRIMARY KEY,
    profile_id BIGINT REFERENCES profiles(profile_id),
    title_id BIGINT REFERENCES titles(title_id),
    episode_id BIGINT REFERENCES episodes(episode_id),
    position_seconds INT,  -- Current position
    duration_seconds INT,  -- Total duration
    watched_at TIMESTAMP DEFAULT NOW(),
    completed BOOLEAN DEFAULT FALSE,
    INDEX idx_profile_watched (profile_id, watched_at DESC)
);

CREATE TABLE ratings (
    rating_id BIGSERIAL PRIMARY KEY,
    profile_id BIGINT REFERENCES profiles(profile_id),
    title_id BIGINT REFERENCES titles(title_id),
    rating SMALLINT CHECK (rating IN (0, 1)),  -- 0 = thumbs down, 1 = thumbs up
    rated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (profile_id, title_id)
);

CREATE TABLE my_list (
    id BIGSERIAL PRIMARY KEY,
    profile_id BIGINT REFERENCES profiles(profile_id),
    title_id BIGINT REFERENCES titles(title_id),
    added_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (profile_id, title_id)
);
```

### 6.2 Elasticsearch (Search)

**Index**: `titles`

```json
{
  "mappings": {
    "properties": {
      "title_id": { "type": "long" },
      "title": { "type": "text", "analyzer": "standard" },
      "description": { "type": "text" },
      "type": { "type": "keyword" },
      "genres": { "type": "keyword" },
      "cast_members": { "type": "text" },
      "director": { "type": "text" },
      "release_year": { "type": "integer" },
      "popularity_score": { "type": "float" }
    }
  }
}
```

**Example Query**:
```json
GET /titles/_search
{
  "query": {
    "multi_match": {
      "query": "stranger things",
      "fields": ["title^3", "description", "cast_members"],
      "fuzziness": "AUTO"
    }
  },
  "sort": [
    { "popularity_score": "desc" }
  ]
}
```

### 6.3 Cassandra (Watch Events - Time Series)

```cql
CREATE TABLE playback_events (
    profile_id BIGINT,
    event_time TIMESTAMP,
    event_id UUID,
    title_id BIGINT,
    episode_id BIGINT,
    event_type VARCHAR,  -- 'play', 'pause', 'seek', 'stop', 'quality_change'
    position_seconds INT,
    bitrate_kbps INT,
    buffer_duration_ms INT,
    device_type VARCHAR,
    PRIMARY KEY (profile_id, event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC);
```

**Why Cassandra?**
- Massive write volume (20M concurrent viewers × events)
- Time-series data (don't need transactions)
- Partition by profile_id for fast user queries
- Analytics pipeline reads from here

---

## 7. DEEP DIVE

### 7.1 CDN Architecture & Video Delivery

Netflix's CDN strategy is unique: **Open Connect**.

#### Why Build Own CDN?

**Economics**:
```
Serving 12 EB/month through third-party CDN:
- CloudFront: 12 EB × $20/TB = $240M/month (!!)
- This is 80%+ of costs

Open Connect:
- Build servers ($5K each), place at ISPs for FREE
- ISPs get benefit: reduced upstream bandwidth
- Netflix pays ~$0 for bandwidth
- Savings: ~$200M/month
```

#### Open Connect Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Netflix Control Plane (AWS)                   │
│  - Content manifest generation                              │
│  - Which servers have which content                         │
│  - Health monitoring of all OCAs                            │
└────────────────┬────────────────────────────────────────────┘
                 │
       ┌─────────┴─────────┐
       │                   │
┌──────▼──────┐    ┌──────▼──────┐
│  OCA Tier 1 │    │  OCA Tier 2 │
│  (ISP POP)  │    │ (IXP/Region)│
│             │    │             │
│ - 200 TB    │    │ - 500 TB    │
│ - 100 Gbps  │    │ - 400 Gbps  │
│ - 99% cache │    │ - Fill Tier1│
└──────┬──────┘    └──────┬──────┘
       │                  │
       └──────────┬───────┘
                  │
         ┌────────▼────────┐
         │  Client Player  │
         │  (Smart TV, etc)│
         └─────────────────┘
```

**OCA (Open Connect Appliance)**:
- FreeBSD servers with 200-500 TB of SSD/HDD storage
- 100-400 Gbps network capacity
- Deployed at 10,000+ locations worldwide
- Placed at ISP points-of-presence (POPs) for free

#### Content Prefetching Algorithm

```python
def prefetch_content_to_oca(oca_location):
    """
    Predict which content will be popular at this location
    and prefetch overnight.
    """
    # 1. Analyze historical viewing patterns
    popular_titles = analyze_viewing_patterns(
        location=oca_location,
        lookback_days=7
    )

    # 2. Detect trending content globally
    trending = get_trending_titles(region=oca_location.region)

    # 3. Predict new releases popularity
    upcoming = predict_new_release_popularity(
        releases_next_7_days=get_upcoming_releases(),
        demographics=oca_location.demographics
    )

    # 4. Combine scores
    titles_to_prefetch = []
    for title in set(popular_titles + trending + upcoming):
        score = (
            0.5 * popularity_score(title, oca_location) +
            0.3 * trending_score(title) +
            0.2 * predicted_score(title, oca_location)
        )
        titles_to_prefetch.append((title, score))

    # 5. Sort by score, fit within storage capacity
    titles_to_prefetch.sort(key=lambda x: x[1], reverse=True)

    oca_capacity = get_oca_capacity(oca_location)
    current_storage = get_current_storage(oca_location)
    available = oca_capacity - current_storage

    # 6. Schedule prefetch jobs (during off-peak hours: 2-6 AM)
    prefetch_queue = []
    total_size = 0
    for title, score in titles_to_prefetch:
        title_size = get_title_total_size(title)  # All bitrates
        if total_size + title_size <= available:
            prefetch_queue.append(title)
            total_size += title_size

    # 7. Execute overnight
    schedule_prefetch_jobs(oca_location, prefetch_queue, time="02:00")

    return prefetch_queue
```

**Result**: 95%+ cache hit rate. Only 5% of requests go to origin (S3).

### 7.2 Adaptive Bitrate Streaming (ABR)

**Goal**: Deliver highest quality video without buffering.

#### How ABR Works

1. **Video Encoding**: Encode video at multiple bitrates
   ```
   Source (4K raw) → Encoder → Multiple outputs:
   - 4K @ 25 Mbps
   - 1080p @ 5 Mbps
   - 720p @ 3 Mbps
   - 480p @ 1 Mbps
   ```

2. **Chunking**: Split each bitrate into 4-second chunks
   ```
   2-hour movie = 7,200 seconds = 1,800 chunks per bitrate
   Total chunks: 1,800 × 4 bitrates = 7,200 chunks
   ```

3. **Manifest Generation**: Create MPD/HLS manifest listing all chunks

4. **Client Player Logic**:
   - Start at low bitrate (fast startup)
   - Measure bandwidth every 4 seconds
   - Switch to higher/lower bitrate adaptively

#### ABR Algorithm (Client-Side)

```python
class AdaptiveBitratePlayer:
    def __init__(self, manifest_url):
        self.manifest = self.fetch_manifest(manifest_url)
        self.available_bitrates = [25000, 5000, 3000, 1000]  # kbps
        self.current_bitrate = 1000  # Start low
        self.buffer_level = 0  # seconds of video buffered
        self.bandwidth_estimate = 0  # kbps

    def select_next_bitrate(self):
        """
        ABR algorithm: Balance quality vs buffer stability.

        Rules:
        1. If buffer > 30s: Can afford to increase quality
        2. If buffer < 10s: Decrease quality to avoid rebuffer
        3. Don't switch too frequently (hysteresis)
        """
        # Update bandwidth estimate (exponential moving average)
        recent_throughput = self.measure_last_chunk_throughput()
        self.bandwidth_estimate = (
            0.8 * self.bandwidth_estimate +
            0.2 * recent_throughput
        )

        # Calculate safe bitrate (use 80% of measured bandwidth)
        safe_bandwidth = self.bandwidth_estimate * 0.8

        # Select highest bitrate that's safe
        candidate_bitrates = [
            br for br in self.available_bitrates
            if br <= safe_bandwidth
        ]

        if not candidate_bitrates:
            # Bandwidth too low, use minimum
            target_bitrate = min(self.available_bitrates)
        else:
            target_bitrate = max(candidate_bitrates)

        # Apply buffer-based rules
        if self.buffer_level < 10:
            # Low buffer: play it safe, decrease quality
            target_bitrate = min(target_bitrate, self.current_bitrate)
        elif self.buffer_level > 30:
            # High buffer: can afford to increase
            target_bitrate = max(target_bitrate, self.current_bitrate)

        # Hysteresis: Don't switch too often (wait 10 seconds)
        time_since_last_switch = self.get_time_since_last_switch()
        if time_since_last_switch < 10:
            target_bitrate = self.current_bitrate

        return target_bitrate

    def fetch_next_chunk(self):
        """
        Main playback loop: fetch chunks and adapt quality.
        """
        while not self.end_of_video():
            # Select bitrate for next chunk
            next_bitrate = self.select_next_bitrate()

            if next_bitrate != self.current_bitrate:
                print(f"Switching quality: {self.current_bitrate} → {next_bitrate} kbps")
                self.current_bitrate = next_bitrate

            # Fetch next chunk at selected bitrate
            chunk_url = self.get_chunk_url(
                current_position=self.position,
                bitrate=self.current_bitrate
            )

            chunk_data = self.download_chunk(chunk_url)

            # Append to playback buffer
            self.buffer.append(chunk_data)
            self.buffer_level += 4  # Each chunk is 4 seconds

            # Update position
            self.position += 4

            # Player consumes buffer (4 sec / 4 sec = stable)
            time.sleep(4)
            self.buffer_level -= 4

            # Send telemetry
            self.send_telemetry({
                'position': self.position,
                'bitrate': self.current_bitrate,
                'buffer': self.buffer_level,
                'bandwidth': self.bandwidth_estimate
            })
```

**Key Metrics**:
- **Rebuffer Ratio**: % of time spent buffering. Target: < 0.5%
- **Average Bitrate**: Higher = better quality. Maximize without rebuffering.
- **Bitrate Switches**: Fewer = smoother experience.

### 7.3 Recommendation Engine

Netflix recommendation system drives 80% of viewing. How does it work?

#### Architecture

```
┌────────────────────────────────────────────────────┐
│           Data Collection Layer                    │
├────────────────────────────────────────────────────┤
│  Kafka: Ingest events (play, pause, rate, search) │
│  Volume: 500B events/day                           │
└────────────┬───────────────────────────────────────┘
             │
┌────────────▼───────────────────────────────────────┐
│         Feature Engineering (Spark)                │
├────────────────────────────────────────────────────┤
│  User features:                                    │
│  - Watch history (last 100 titles)                 │
│  - Genres watched                                  │
│  - Time of day patterns                            │
│  - Device types                                    │
│                                                     │
│  Item features:                                    │
│  - Genres, cast, director                          │
│  - Popularity (global + regional)                  │
│  - Recency (release date)                          │
└────────────┬───────────────────────────────────────┘
             │
┌────────────▼───────────────────────────────────────┐
│         ML Models (Multiple Algorithms)            │
├────────────────────────────────────────────────────┤
│  1. Collaborative Filtering (Matrix Factorization)│
│     - Learn user embeddings & item embeddings      │
│     - Score = dot(user_vector, item_vector)        │
│                                                     │
│  2. Content-Based Filtering                        │
│     - "You watched action movies → recommend more" │
│                                                     │
│  3. Deep Learning (Two-Tower Model)                │
│     - User tower: encode user features → vector    │
│     - Item tower: encode item features → vector    │
│     - Score = cosine_similarity(user, item)        │
│                                                     │
│  4. Ranking Model (XGBoost)                        │
│     - Combine all signals → final ranking          │
└────────────┬───────────────────────────────────────┘
             │
┌────────────▼───────────────────────────────────────┐
│      Online Serving (Low Latency < 100ms)         │
├────────────────────────────────────────────────────┤
│  Redis: Cache recommendations per profile          │
│  Compute: Fetch top-K from each model, blend       │
└────────────────────────────────────────────────────┘
```

#### Collaborative Filtering (Matrix Factorization)

```python
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import NMF

class CollaborativeFiltering:
    def __init__(self, n_factors=50):
        """
        Matrix Factorization using Non-negative Matrix Factorization.

        Idea: Decompose user-item interaction matrix into:
        R ≈ U × V^T

        Where:
        - R: user-item ratings (sparse matrix)
        - U: user embeddings (users × n_factors)
        - V: item embeddings (items × n_factors)
        """
        self.n_factors = n_factors
        self.model = NMF(n_components=n_factors, init='random', random_state=42)

    def train(self, watch_history_df):
        """
        Train on implicit feedback (watch history).

        Input: DataFrame with columns [user_id, title_id, watch_count]
        """
        # Create sparse matrix
        user_ids = watch_history_df['user_id'].astype('category')
        title_ids = watch_history_df['title_id'].astype('category')

        interaction_matrix = csr_matrix(
            (watch_history_df['watch_count'],
             (user_ids.cat.codes, title_ids.cat.codes))
        )

        # Fit model: R ≈ U × V^T
        self.user_embeddings = self.model.fit_transform(interaction_matrix)  # U
        self.item_embeddings = self.model.components_.T  # V

        self.user_id_map = dict(enumerate(user_ids.cat.categories))
        self.title_id_map = dict(enumerate(title_ids.cat.categories))

    def recommend(self, user_id, top_k=20):
        """
        Recommend top-K titles for user.
        """
        # Get user embedding
        user_idx = list(self.user_id_map.values()).index(user_id)
        user_vector = self.user_embeddings[user_idx]

        # Compute scores for all items: score = U_user · V_item^T
        scores = np.dot(user_vector, self.item_embeddings.T)

        # Get top-K
        top_indices = np.argsort(scores)[::-1][:top_k]
        top_titles = [self.title_id_map[idx] for idx in top_indices]

        return top_titles
```

#### Deep Learning: Two-Tower Model

```python
import torch
import torch.nn as nn

class TwoTowerModel(nn.Module):
    """
    Two-tower architecture:
    - User tower: encodes user features → user_embedding
    - Item tower: encodes item features → item_embedding
    - Score = cosine_similarity(user_embedding, item_embedding)
    """
    def __init__(self, user_feature_dim, item_feature_dim, embedding_dim=128):
        super().__init__()

        # User tower
        self.user_tower = nn.Sequential(
            nn.Linear(user_feature_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, embedding_dim)
        )

        # Item tower
        self.item_tower = nn.Sequential(
            nn.Linear(item_feature_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, embedding_dim)
        )

    def forward(self, user_features, item_features):
        # Encode user
        user_emb = self.user_tower(user_features)  # (batch, 128)

        # Encode item
        item_emb = self.item_tower(item_features)  # (batch, 128)

        # Normalize embeddings
        user_emb = nn.functional.normalize(user_emb, dim=1)
        item_emb = nn.functional.normalize(item_emb, dim=1)

        # Compute similarity (dot product)
        scores = torch.sum(user_emb * item_emb, dim=1)  # (batch,)

        return scores

# Training loop (simplified)
def train_two_tower_model(model, train_loader, epochs=10):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCEWithLogitsLoss()  # Binary classification (watch/not watch)

    for epoch in range(epochs):
        for user_features, item_features, labels in train_loader:
            # Forward pass
            scores = model(user_features, item_features)

            # Compute loss
            loss = criterion(scores, labels)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# Inference: Retrieve top-K recommendations
def retrieve_recommendations(model, user_features, all_item_embeddings, top_k=20):
    """
    Given user, find top-K items with highest similarity.

    Using approximate nearest neighbor search (FAISS).
    """
    import faiss

    # Encode user
    user_emb = model.user_tower(user_features).detach().numpy()
    user_emb = user_emb / np.linalg.norm(user_emb)  # Normalize

    # Build FAISS index for fast search
    index = faiss.IndexFlatIP(all_item_embeddings.shape[1])  # Inner product
    index.add(all_item_embeddings)

    # Search top-K
    distances, indices = index.search(user_emb, top_k)

    return indices[0]  # Top-K item indices
```

#### Blending Multiple Models

```python
def generate_recommendations(profile_id, top_k=50):
    """
    Blend recommendations from multiple models.
    """
    # 1. Collaborative Filtering
    cf_recs = collaborative_filtering_model.recommend(profile_id, top_k=100)

    # 2. Content-Based
    user_history = get_watch_history(profile_id)
    cb_recs = content_based_model.recommend(user_history, top_k=100)

    # 3. Deep Learning
    user_features = extract_user_features(profile_id)
    dl_recs = deep_learning_model.recommend(user_features, top_k=100)

    # 4. Trending (popularity)
    trending_recs = get_trending_titles(profile_region, top_k=50)

    # Combine with weights
    all_candidates = []

    for title in set(cf_recs + cb_recs + dl_recs + trending_recs):
        score = (
            0.4 * (1.0 if title in cf_recs else 0.0) +
            0.3 * (1.0 if title in dl_recs else 0.0) +
            0.2 * (1.0 if title in cb_recs else 0.0) +
            0.1 * (1.0 if title in trending_recs else 0.0)
        )
        all_candidates.append((title, score))

    # Sort by blended score
    all_candidates.sort(key=lambda x: x[1], reverse=True)

    # Return top-K
    final_recs = [title for title, score in all_candidates[:top_k]]

    # Cache for 1 hour
    redis_client.setex(f"recs:{profile_id}", 3600, json.dumps(final_recs))

    return final_recs
```

---

## 8. DISCUSSION

### 8.1 Trade-offs

#### 1. Own CDN (Open Connect) vs Third-Party CDN

**Open Connect (Chosen)**:
- ✅ Cost savings: ~$200M/month
- ✅ Control over deployment & optimization
- ✅ Better peering with ISPs
- ❌ High upfront investment (build servers)
- ❌ Operational complexity (manage 10K+ servers)

**Third-Party CDN (CloudFront, Akamai)**:
- ✅ No upfront cost
- ✅ Global coverage immediately
- ❌ Very expensive at Netflix scale ($240M/month)
- ❌ Less control

**Decision**: Build Open Connect for cost & control at scale.

#### 2. Adaptive Bitrate Streaming (ABR)

**Why not Fixed Bitrate?**
- Users on slow connections would buffer constantly
- Users on fast connections wouldn't get best quality
- Waste bandwidth delivering high quality to users who can't use it

**ABR Advantages**:
- ✅ Smooth playback (< 0.5% rebuffer ratio)
- ✅ Maximize quality per user's bandwidth
- ✅ Better user experience

**Complexity Cost**:
- ❌ Must encode at multiple bitrates (4x storage)
- ❌ Complex client player logic
- ❌ More CDN metadata to manage

#### 3. Prefetching Content to OCAs

**Aggressive Prefetching (Chosen)**:
- ✅ 95%+ cache hit rate
- ✅ Users served from edge (low latency)
- ❌ Some prefetched content never watched (wasted storage)

**On-Demand Fetching**:
- ✅ Only store what's actually requested
- ❌ Lower cache hit rate (70-80%)
- ❌ Higher latency for cache misses

**Decision**: Prefetch aggressively. Storage is cheap, user experience is priceless.

#### 4. Recommendation System: Accuracy vs Latency

**Complex Deep Learning Models**:
- ✅ Higher accuracy (+5% engagement)
- ❌ Slower inference (200ms)

**Simple Collaborative Filtering**:
- ✅ Fast inference (10ms)
- ❌ Lower accuracy

**Decision**: Use ensemble of models, cache recommendations.
- Deep learning runs offline (batch), results cached
- Cached recs served instantly (< 50ms)
- Acceptable staleness (1 hour TTL)

### 8.2 Bottlenecks & Solutions

#### Bottleneck 1: Encoding Pipeline

**Problem**: Encoding a 2-hour 4K movie takes ~8 hours on single machine.

**Solution**:
- Parallelize encoding: Split movie into 10-minute segments
- Encode each segment independently
- Merge outputs
- Time reduced: 8 hours → 30 minutes

**Implementation**:
```python
# Distributed encoding with AWS Batch
def encode_title_distributed(source_video_url, title_id):
    # 1. Split video into segments
    segments = split_video_into_segments(source_video_url, segment_duration=600)  # 10 min

    # 2. Submit encoding jobs (one per segment per bitrate)
    jobs = []
    for segment_id, segment_url in enumerate(segments):
        for bitrate_profile in ['4k', '1080p', '720p', '480p']:
            job = submit_encoding_job(
                input_url=segment_url,
                output_profile=bitrate_profile,
                job_name=f"{title_id}_{segment_id}_{bitrate_profile}"
            )
            jobs.append(job)

    # 3. Wait for all jobs to complete (parallel execution)
    wait_for_jobs(jobs)

    # 4. Concatenate segments for each bitrate
    for bitrate_profile in ['4k', '1080p', '720p', '480p']:
        segment_files = [f"{title_id}_{i}_{bitrate_profile}.mp4" for i in range(len(segments))]
        concatenate_video_segments(segment_files, output=f"{title_id}_{bitrate_profile}.mp4")

    # 5. Generate DASH manifest
    generate_dash_manifest(title_id)
```

#### Bottleneck 2: Recommendation Latency

**Problem**: Computing recommendations in real-time (scoring 15K titles) takes 2+ seconds.

**Solution**:
- **Precompute**: Generate recommendations offline every hour
- **Cache**: Store in Redis (TTL = 1 hour)
- **Incremental Updates**: When user watches new title, update recs in background

```python
# Precompute job (runs every hour via cron)
def precompute_recommendations_batch():
    all_profiles = get_all_profile_ids()  # 100M+ profiles

    # Process in batches
    for batch in chunks(all_profiles, batch_size=10000):
        for profile_id in batch:
            recs = generate_recommendations(profile_id, top_k=50)
            redis_client.setex(f"recs:{profile_id}", 3600, json.dumps(recs))

    print("Precompute complete")

# Online serving (instant)
def get_recommendations_cached(profile_id):
    cached = redis_client.get(f"recs:{profile_id}")
    if cached:
        return json.loads(cached)
    else:
        # Fallback: compute on-demand (rare, only for new users)
        recs = generate_recommendations(profile_id, top_k=50)
        redis_client.setex(f"recs:{profile_id}", 3600, json.dumps(recs))
        return recs
```

---

## 9. IMPLEMENTACIÓN

### 9.1 Video Player Service (ABR)

```python
# video_player_service.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import redis

app = FastAPI()
s3_client = boto3.client('s3')
redis_client = redis.Redis(host='redis', decode_responses=True)

class PlaybackRequest(BaseModel):
    profile_id: int
    title_id: int
    episode_id: int = None
    device_capabilities: dict

@app.post("/playback/start")
def start_playback(request: PlaybackRequest):
    """
    Start video playback session.
    Returns ABR manifest URL and license URL.
    """
    # 1. Validate user has access
    if not has_active_subscription(request.profile_id):
        raise HTTPException(status_code=403, detail="Subscription required")

    # 2. Check content availability in user's region
    region = get_user_region(request.profile_id)
    if not is_content_available(request.title_id, region):
        raise HTTPException(status_code=451, detail="Content not available in your region")

    # 3. Get video asset metadata
    video_asset = get_video_asset(request.title_id, request.episode_id)

    # 4. Generate playback session
    playback_id = generate_playback_id()

    # 5. Get ABR manifest URL (from CDN)
    manifest_url = f"https://cdn.netflix.com/{video_asset['cdn_path']}/manifest.mpd"

    # 6. Generate DRM license URL
    license_url = generate_license_url(playback_id, request.device_capabilities)

    # 7. Get resume position (if previously watched)
    resume_position = get_watch_progress(request.profile_id, request.title_id)

    # 8. Track playback session (for analytics)
    redis_client.setex(
        f"playback:{playback_id}",
        7200,  # 2 hour TTL
        json.dumps({
            'profile_id': request.profile_id,
            'title_id': request.title_id,
            'started_at': datetime.now().isoformat()
        })
    )

    return {
        'playback_id': playback_id,
        'manifest_url': manifest_url,
        'license_url': license_url,
        'resume_position': resume_position,
        'expires_at': (datetime.now() + timedelta(hours=2)).isoformat()
    }

@app.get("/playback/{video_id}/manifest.mpd")
def get_manifest(video_id: str):
    """
    Generate DASH MPD manifest dynamically.
    Lists all available bitrates, audio tracks, subtitles.
    """
    video_assets = get_video_assets(video_id)

    # Build MPD XML
    mpd = '<?xml version="1.0"?>\n'
    mpd += '<MPD xmlns="urn:mpeg:dash:schema:mpd:2011">\n'
    mpd += '  <Period duration="PT2H">\n'

    # Video adaptation set
    mpd += '    <AdaptationSet mimeType="video/mp4" codecs="h264">\n'
    for asset in video_assets['video']:
        mpd += f'''
      <Representation id="{asset['id']}" bandwidth="{asset['bitrate']}" width="{asset['width']}" height="{asset['height']}">
        <BaseURL>{asset['base_url']}</BaseURL>
        <SegmentTemplate media="chunk_$Number$.m4s" startNumber="1" duration="4"/>
      </Representation>
        '''
    mpd += '    </AdaptationSet>\n'

    # Audio adaptation sets (multiple languages)
    for audio in video_assets['audio']:
        mpd += f'''
    <AdaptationSet mimeType="audio/mp4" codecs="aac" lang="{audio['language']}">
      <Representation id="{audio['id']}" bandwidth="{audio['bitrate']}">
        <BaseURL>{audio['base_url']}</BaseURL>
        <SegmentTemplate media="chunk_$Number$.m4s" startNumber="1" duration="4"/>
      </Representation>
    </AdaptationSet>
        '''

    # Subtitles
    for subtitle in video_assets['subtitles']:
        mpd += f'''
    <AdaptationSet mimeType="text/vtt" lang="{subtitle['language']}">
      <Representation id="{subtitle['id']}">
        <BaseURL>{subtitle['url']}</BaseURL>
      </Representation>
    </AdaptationSet>
        '''

    mpd += '  </Period>\n'
    mpd += '</MPD>'

    return Response(content=mpd, media_type="application/dash+xml")

@app.post("/playback/progress")
def update_progress(progress: dict):
    """
    Update watch progress (called every 30 seconds).
    """
    profile_id = progress['profile_id']
    title_id = progress['title_id']
    position = progress['position']

    # Update in database
    update_watch_progress(profile_id, title_id, position)

    # Also send to Kafka for analytics
    kafka_producer.send('playback_events', value={
        'profile_id': profile_id,
        'title_id': title_id,
        'position': position,
        'timestamp': datetime.now().isoformat()
    })

    return {'acknowledged': True}
```

### 9.2 Recommendation Service (Simplified)

```python
# recommendation_service.py

from fastapi import FastAPI
import redis
import json

app = FastAPI()
redis_client = redis.Redis(host='redis', decode_responses=True)

@app.get("/recommendations/{profile_id}")
def get_recommendations(profile_id: int):
    """
    Get personalized recommendations for profile.
    Served from cache (precomputed hourly).
    """
    # Try cache
    cache_key = f"recs:{profile_id}"
    cached = redis_client.get(cache_key)

    if cached:
        recommendations = json.loads(cached)
    else:
        # Cache miss: compute on-demand (fallback)
        recommendations = compute_recommendations_realtime(profile_id)
        redis_client.setex(cache_key, 3600, json.dumps(recommendations))

    # Format as homepage rows
    rows = []

    # Row 1: Personalized picks
    rows.append({
        'title': 'Top Picks for You',
        'items': recommendations[:10]
    })

    # Row 2: Because you watched X
    last_watched = get_last_watched_title(profile_id)
    if last_watched:
        similar = get_similar_titles(last_watched['title_id'], limit=10)
        rows.append({
            'title': f"Because You Watched '{last_watched['title']}'",
            'items': similar
        })

    # Row 3: Trending
    trending = get_trending_titles(limit=10)
    rows.append({
        'title': 'Trending Now',
        'items': trending
    })

    # Row 4: Continue watching
    continue_watching = get_continue_watching(profile_id, limit=10)
    if continue_watching:
        rows.insert(0, {
            'title': 'Continue Watching',
            'items': continue_watching
        })

    return {'rows': rows}

def compute_recommendations_realtime(profile_id):
    """
    Fallback: compute recommendations on-demand.
    (Normally precomputed offline)
    """
    # Get user watch history
    watch_history = get_watch_history(profile_id, limit=100)

    # Get collaborative filtering recommendations
    cf_model = load_cf_model()
    cf_recs = cf_model.recommend(profile_id, top_k=50)

    # Get content-based recommendations
    cb_recs = []
    for title_id in watch_history:
        similar = get_similar_titles(title_id, limit=5)
        cb_recs.extend(similar)

    # Combine & deduplicate
    all_recs = list(set(cf_recs + cb_recs))

    # Fetch metadata for each title
    recommendations = []
    for title_id in all_recs[:50]:
        title_metadata = get_title_metadata(title_id)
        recommendations.append(title_metadata)

    return recommendations
```

---

## 10. EJERCICIOS

### Ejercicio 1: Handle CDN Failure

**Escenario**: Un OCA (Open Connect Appliance) completo falla. ¿Cómo redirigir tráfico?

**Solución esperada**:
- Health checks detect OCA failure
- DNS updates to redirect traffic to next closest OCA
- Or fallback to origin (S3) temporarily

### Ejercicio 2: Optimize Cold Start

**Problema**: Usuarios en nueva región tienen cache frío (0% hit rate). ¿Cómo mejorar?

**Hints**:
- Prefetch top 100 global popular titles
- Analyze demographics to predict local preferences
- Gradual warmup over 24 hours

### Ejercicio 3: Handle Viral Content

**Escenario**: Nueva serie lanza y 50M usuarios intentan ver simultáneamente. ¿Qué problemas anticipar?

**Considera**:
- CDN cache misses (content not prefetched)
- Origin bandwidth saturation
- Database load (progress updates)

### Ejercicio 4: Recommendation Diversity

**Problema**: Recommendations son demasiado similares (filter bubble). ¿Cómo diversificar?

**Approaches**:
- Inject random titles (10% exploration)
- Use different genres across rows
- Penalty for similar titles in same row

### Ejercicio 5: Multi-Region Disaster Recovery

**Escenario**: AWS us-east-1 falla completamente. ¿Cómo mantener servicio?

**Solución**:
- All services deployed in 3 regions (US, EU, APAC)
- Route53 health checks auto-failover
- Database replication (PostgreSQL read replicas)
- CDN already multi-region (no SPOFfail)

---

## 📚 CHEAT SHEET

### Números Clave
```
Subscribers: 230M
DAU: 100M
Concurrent viewers: 20M
Content library: 15K titles, 71K hours
Storage: 4 PB (video)
Bandwidth: 100 Tbps peak, 12-15 EB/month
Cost: ~$74M/month ($888M/year)
CDN hit rate: 95%+
```

### Video Encoding
```
Bitrates:
- 4K: 25 Mbps (11.25 GB/hour)
- 1080p: 5 Mbps (2.25 GB/hour)
- 720p: 3 Mbps (1.35 GB/hour)
- 480p: 1 Mbps (450 MB/hour)

Chunk size: 4 seconds
2-hour movie = 1,800 chunks per bitrate
```

### ABR Algorithm
```python
# Simplified ABR logic
if buffer_level < 10s:
    decrease_quality()
elif buffer_level > 30s and bandwidth_high:
    increase_quality()
else:
    maintain_quality()
```

### Recommendation Models
```
1. Collaborative Filtering (Matrix Factorization)
2. Content-Based Filtering
3. Deep Learning (Two-Tower)
4. Popularity/Trending

Blending weights: 40% CF, 30% DL, 20% CB, 10% Trending
```

### Performance Targets
```
Startup time: < 2s
Rebuffer ratio: < 0.5%
Search latency: < 200ms
Recommendation load: < 500ms
CDN hit rate: > 95%
```

---

## 🎯 PRÓXIMOS PASOS

Has completado 3 casos reales complejos: Twitter, Uber, Netflix. **Key Takeaways**:

1. **CDN is king** para video streaming (95%+ cache hit rate crítico)
2. **ABR** permite smooth playback adaptándose a bandwidth
3. **Open Connect** es estrategia única de Netflix (savings de $200M/mes)
4. **Recommendations** drive 80% viewing (ML crítico para engagement)
5. **Prefetching** inteligente maximiza cache hits

**Comparación de los 3 casos**:

| Aspecto | Twitter | Uber | Netflix |
|---------|---------|------|---------|
| **QPS crítico** | 463K reads | 650K location | 2M manifest |
| **Storage** | 1.1 PB | 50 TB | 4 PB |
| **Bandwidth** | Bajo | Medio | Extremo (100 Tbps) |
| **Consistency** | Eventual OK | Strong (matching) | Eventual OK |
| **Tech clave** | Fanout, Cassandra | Geospatial, Redis | CDN, ABR, ML |

**Siguiente**: Semana 7 - Patrones de Escalabilidad (síntesis de todos los conceptos)

---

**Creado**: 2024-12-05
**Versión**: 1.0
**Parte de**: Fase 1 - System Design Fundamentals
