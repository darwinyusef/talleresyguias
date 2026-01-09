# Arquitectura: Microservices Patterns Avanzados 2026

## Objetivo
Patrones avanzados para microservices: Strangler Pattern, BFF, API Gateway, Rate Limiting, Idempotency, y Workflow Orchestration con Temporal.

---

## CATEGORÍA 1: Strangler Pattern para Migration

### 1.1 Strangler Fig Pattern
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Migrar de monolito a microservices sin downtime. Strangler Pattern permite migración incremental.

**Estrategia: Migración Incremental**

```
┌────────────────────────────────────────────────────┐
│         STRANGLER PATTERN TIMELINE                 │
├────────────────────────────────────────────────────┤
│                                                    │
│ FASE 1: Legacy Monolith (100% traffic)            │
│ ┌──────────────────────────────────────────┐      │
│ │                                          │      │
│ │         MONOLITH                         │      │
│ │  - Orders                                │      │
│ │  - Customers                             │      │
│ │  - Products                              │      │
│ │  - Payments                              │      │
│ │                                          │      │
│ └──────────────────────────────────────────┘      │
│                                                    │
│ FASE 2: First Service Extracted (10% traffic)     │
│ ┌──────────────┐    ┌────────────────────┐        │
│ │              │    │                    │        │
│ │ NEW SERVICE  │    │    MONOLITH        │        │
│ │  - Orders    │    │  - Customers       │        │
│ │              │    │  - Products        │        │
│ │              │    │  - Payments        │        │
│ └──────────────┘    └────────────────────┘        │
│                                                    │
│ FASE 3: Progressive Migration (50% traffic)       │
│ ┌──────────┐ ┌──────────┐  ┌─────────────┐        │
│ │ Orders   │ │Customers │  │  MONOLITH   │        │
│ │ Service  │ │ Service  │  │  - Products │        │
│ │          │ │          │  │  - Payments │        │
│ └──────────┘ └──────────┘  └─────────────┘        │
│                                                    │
│ FASE 4: Legacy Strangled (0% traffic)             │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                   │
│ │Order│ │Cust │ │Prod │ │Pay  │                   │
│ └─────┘ └─────┘ └─────┘ └─────┘                   │
│                                                    │
│ ❌ Monolith decomissioned                         │
│                                                    │
└────────────────────────────────────────────────────┘
```

**Implementación: Proxy Layer con Routing**

```python
# ============================================
# STRANGLER PROXY: Route traffic incrementally
# ============================================

from enum import Enum
from typing import Optional
import httpx

class RoutingStrategy(Enum):
    LEGACY_ONLY = "legacy_only"
    NEW_SERVICE_ONLY = "new_service_only"
    PERCENTAGE_SPLIT = "percentage_split"
    HEADER_BASED = "header_based"
    USER_BASED = "user_based"

@dataclass
class RouteConfig:
    """Configuration for routing"""
    strategy: RoutingStrategy
    new_service_url: str
    legacy_url: str

    # For percentage split
    new_service_percentage: int = 0

    # For header-based routing
    routing_header: Optional[str] = None
    routing_header_value: Optional[str] = None

    # For user-based routing
    whitelisted_users: Optional[List[str]] = None


class StranglerProxy:
    """
    Strangler Proxy: Gradual migration proxy

    Routes traffic between legacy and new service
    Allows incremental rollout
    """

    def __init__(self, route_configs: Dict[str, RouteConfig]):
        self.route_configs = route_configs
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def proxy_request(
        self,
        path: str,
        method: str,
        headers: dict,
        body: Optional[bytes],
        user_id: Optional[str]
    ) -> httpx.Response:
        """
        Proxy request to legacy or new service

        Routing decision based on configuration
        """

        # Get route config for path
        route_config = self._get_route_config(path)

        if not route_config:
            raise RouteNotFoundError(path)

        # Decide target based on strategy
        target_url = self._decide_target(
            route_config,
            headers,
            user_id
        )

        logger.info(
            "proxy_routing",
            path=path,
            method=method,
            target=target_url,
            strategy=route_config.strategy.value
        )

        # Forward request
        response = await self.http_client.request(
            method=method,
            url=f"{target_url}{path}",
            headers=headers,
            content=body
        )

        return response

    def _decide_target(
        self,
        config: RouteConfig,
        headers: dict,
        user_id: Optional[str]
    ) -> str:
        """
        Decide routing target based on strategy

        Supports multiple routing strategies
        """

        # Strategy 1: Legacy only (initial state)
        if config.strategy == RoutingStrategy.LEGACY_ONLY:
            return config.legacy_url

        # Strategy 2: New service only (final state)
        if config.strategy == RoutingStrategy.NEW_SERVICE_ONLY:
            return config.new_service_url

        # Strategy 3: Percentage split (gradual rollout)
        if config.strategy == RoutingStrategy.PERCENTAGE_SPLIT:
            # Random percentage
            if random.randint(1, 100) <= config.new_service_percentage:
                return config.new_service_url
            return config.legacy_url

        # Strategy 4: Header-based (canary testing)
        if config.strategy == RoutingStrategy.HEADER_BASED:
            header_value = headers.get(config.routing_header)
            if header_value == config.routing_header_value:
                return config.new_service_url
            return config.legacy_url

        # Strategy 5: User-based (beta users)
        if config.strategy == RoutingStrategy.USER_BASED:
            if user_id and user_id in config.whitelisted_users:
                return config.new_service_url
            return config.legacy_url

        # Default: Legacy
        return config.legacy_url

    def _get_route_config(self, path: str) -> Optional[RouteConfig]:
        """Get route configuration for path"""
        # Match by prefix
        for route_prefix, config in self.route_configs.items():
            if path.startswith(route_prefix):
                return config
        return None


# ============================================
# CONFIGURATION MANAGEMENT
# ============================================

class StranglerConfigManager:
    """
    Manage strangler configuration

    Allows runtime updates (no redeploy)
    """

    def __init__(self, config_store):
        self.config_store = config_store

    async def get_route_config(self, path: str) -> RouteConfig:
        """Get current route config"""
        config_data = await self.config_store.get(f"route:{path}")
        return RouteConfig(**config_data)

    async def update_percentage(self, path: str, percentage: int):
        """
        Update traffic percentage

        Example migration:
        Day 1: 5%
        Day 3: 10%
        Day 7: 25%
        Day 14: 50%
        Day 21: 100%
        """
        config = await self.get_route_config(path)
        config.new_service_percentage = percentage

        await self.config_store.set(
            f"route:{path}",
            config.__dict__
        )

        logger.info(
            "strangler_percentage_updated",
            path=path,
            new_percentage=percentage
        )

    async def switch_to_new_service(self, path: str):
        """
        Complete migration: 100% to new service

        Final step in strangler pattern
        """
        config = await self.get_route_config(path)
        config.strategy = RoutingStrategy.NEW_SERVICE_ONLY

        await self.config_store.set(f"route:{path}", config.__dict__)

        logger.info(
            "strangler_migration_completed",
            path=path
        )


# ============================================
# FASTAPI INTEGRATION
# ============================================

app = FastAPI()

# Initialize strangler
route_configs = {
    "/api/orders": RouteConfig(
        strategy=RoutingStrategy.PERCENTAGE_SPLIT,
        new_service_url="http://orders-service:8000",
        legacy_url="http://monolith:8000",
        new_service_percentage=10  # Start with 10%
    ),
    "/api/customers": RouteConfig(
        strategy=RoutingStrategy.LEGACY_ONLY,
        new_service_url="http://customers-service:8000",
        legacy_url="http://monolith:8000"
    ),
    "/api/products": RouteConfig(
        strategy=RoutingStrategy.LEGACY_ONLY,
        new_service_url="http://products-service:8000",
        legacy_url="http://monolith:8000"
    )
}

strangler = StranglerProxy(route_configs)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def strangler_proxy(
    request: Request,
    path: str,
    user: User = Depends(get_current_user)
):
    """
    Strangler proxy endpoint

    Routes all traffic through strangler
    """

    # Get request body
    body = await request.body()

    # Proxy request
    response = await strangler.proxy_request(
        path=f"/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        user_id=user.id if user else None
    )

    # Return response
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )


# ============================================
# ADMIN ENDPOINTS: Control migration
# ============================================

config_manager = StranglerConfigManager(redis_client)

@app.post("/admin/strangler/rollout")
async def update_rollout(request: RolloutUpdateRequest):
    """
    Update traffic percentage

    POST /admin/strangler/rollout
    {
      "path": "/api/orders",
      "percentage": 25
    }
    """
    await config_manager.update_percentage(
        request.path,
        request.percentage
    )

    return {"status": "updated", "percentage": request.percentage}


@app.post("/admin/strangler/complete")
async def complete_migration(request: CompleteMigrationRequest):
    """
    Complete migration: 100% to new service

    POST /admin/strangler/complete
    {
      "path": "/api/orders"
    }
    """
    await config_manager.switch_to_new_service(request.path)

    return {"status": "migration_completed"}


# ============================================
# MONITORING: Compare legacy vs new
# ============================================

class StranglerMonitoring:
    """
    Monitor strangler traffic

    Compare response times, errors, etc.
    """

    def __init__(self, metrics_client):
        self.metrics = metrics_client

    async def record_request(
        self,
        path: str,
        target: str,  # 'legacy' or 'new'
        duration_ms: float,
        status_code: int
    ):
        """Record request metrics"""

        self.metrics.histogram(
            'strangler_request_duration_ms',
            duration_ms,
            tags={
                'path': path,
                'target': target,
                'status': status_code
            }
        )

        if status_code >= 500:
            self.metrics.increment(
                'strangler_errors_total',
                tags={'path': path, 'target': target}
            )


# Dashboard query:
"""
# Compare response times
SELECT
    target,
    AVG(duration_ms) as avg_duration,
    P50(duration_ms) as p50,
    P95(duration_ms) as p95,
    P99(duration_ms) as p99
FROM strangler_metrics
WHERE path = '/api/orders'
GROUP BY target

# Result:
target    avg_duration  p50   p95   p99
legacy    250ms         200   500   800
new       120ms         100   250   400

✅ New service is faster, safe to increase %
"""
```

---

## CATEGORÍA 2: Backend for Frontend (BFF) Pattern

### 2.1 BFF Pattern
**Dificultad:** ⭐⭐⭐⭐ **ALTA**

**Contexto:**
Un API genérica no es óptima para todos los clientes. BFF crea APIs específicas por cliente (web, mobile, etc).

**Arquitectura BFF**

```
┌────────────────────────────────────────────────┐
│                                                │
│              CLIENTS                           │
│                                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │   WEB   │  │  MOBILE │  │   IoT   │        │
│  │ Browser │  │   App   │  │ Devices │        │
│  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │             │             │
│       │            │             │             │
│  ┌────▼────┐  ┌───▼─────┐  ┌───▼─────┐        │
│  │  BFF    │  │  BFF    │  │  BFF    │        │
│  │  Web    │  │ Mobile  │  │  IoT    │        │
│  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │             │             │
│       └────────────┼─────────────┘             │
│                    │                           │
│  ┌─────────────────▼──────────────────┐        │
│  │                                    │        │
│  │      MICROSERVICES LAYER           │        │
│  │                                    │        │
│  │ ┌────────┐ ┌────────┐ ┌────────┐  │        │
│  │ │ Users  │ │ Orders │ │Products│  │        │
│  │ └────────┘ └────────┘ └────────┘  │        │
│  │                                    │        │
│  └────────────────────────────────────┘        │
│                                                │
└────────────────────────────────────────────────┘
```

**Implementación: BFF for Web vs Mobile**

```python
# ============================================
# MICROSERVICES (Backend services)
# ============================================

# Service 1: User Service
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Return full user data"""
    return {
        "id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "address": {...},
        "preferences": {...},
        "created_at": "2020-01-01",
        # ... many more fields
    }

# Service 2: Order Service
@app.get("/orders")
async def get_orders(user_id: str):
    """Return orders"""
    return [{
        "id": "order_1",
        "user_id": user_id,
        "items": [...],
        "total": 99.99,
        "status": "delivered",
        "created_at": "2024-01-15",
        # ... many more fields
    }]


# ============================================
# BFF FOR WEB
# ============================================

class WebBFF:
    """
    BFF for Web Client

    Web needs:
    - Rich data (full details)
    - Multiple aggregations
    - Real-time updates
    """

    def __init__(self, user_service, order_service, product_service):
        self.user_service = user_service
        self.order_service = order_service
        self.product_service = product_service

    async def get_user_dashboard(self, user_id: str) -> dict:
        """
        Web dashboard endpoint

        Aggregates data from multiple services
        Returns rich data for desktop browser
        """

        # Parallel requests to services
        user_task = self.user_service.get_user(user_id)
        orders_task = self.order_service.get_orders(user_id)
        recommendations_task = self.product_service.get_recommendations(user_id)

        user, orders, recommendations = await asyncio.gather(
            user_task,
            orders_task,
            recommendations_task
        )

        # Aggregate and enrich
        return {
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"],
                "member_since": user["created_at"],
                "loyalty_points": user.get("loyalty_points", 0),
                "preferences": user["preferences"]
            },
            "recent_orders": [
                {
                    "id": order["id"],
                    "date": order["created_at"],
                    "total": order["total"],
                    "status": order["status"],
                    "items_count": len(order["items"]),
                    "tracking_url": order.get("tracking_url"),
                    # Full order details for web
                    "items": order["items"]
                }
                for order in orders[:10]  # Last 10 orders
            ],
            "recommendations": recommendations,
            # Web-specific: Analytics data
            "analytics": {
                "total_spent": sum(o["total"] for o in orders),
                "order_count": len(orders),
                "favorite_categories": self._get_favorite_categories(orders)
            }
        }


# BFF Web API
web_bff = FastAPI()

@web_bff.get("/dashboard")
async def web_dashboard(user: User = Depends(get_current_user)):
    """
    Web dashboard endpoint

    Optimized for desktop browsers
    """
    bff = WebBFF(user_service, order_service, product_service)
    dashboard_data = await bff.get_user_dashboard(user.id)
    return dashboard_data


# ============================================
# BFF FOR MOBILE
# ============================================

class MobileBFF:
    """
    BFF for Mobile Client

    Mobile needs:
    - Minimal data (reduce bandwidth)
    - Optimized for small screens
    - Battery efficient (fewer requests)
    """

    def __init__(self, user_service, order_service):
        self.user_service = user_service
        self.order_service = order_service

    async def get_user_home(self, user_id: str) -> dict:
        """
        Mobile home endpoint

        Minimal data for mobile screen
        """

        # Parallel requests
        user, orders = await asyncio.gather(
            self.user_service.get_user(user_id),
            self.order_service.get_orders(user_id)
        )

        # Return minimal data (optimize bandwidth)
        return {
            # Minimal user info
            "user": {
                "name": user["name"],
                "avatar_url": user.get("avatar_url")
            },
            # Only recent orders, minimal fields
            "recent_orders": [
                {
                    "id": order["id"],
                    "date": order["created_at"],
                    "total": order["total"],
                    "status": order["status"],
                    # Mobile: No full item details (save bandwidth)
                    # User taps to see details
                }
                for order in orders[:5]  # Only 5 recent
            ],
            # Mobile-specific: Quick actions
            "quick_actions": [
                {"type": "reorder", "order_id": orders[0]["id"]},
                {"type": "track", "order_id": orders[0]["id"]}
            ]
        }

    async def get_order_details(self, order_id: str) -> dict:
        """
        Mobile order details

        Separate endpoint (lazy loading)
        Only fetched when user taps on order
        """
        order = await self.order_service.get_order(order_id)

        # Minimal response
        return {
            "id": order["id"],
            "status": order["status"],
            "total": order["total"],
            # Only essential item info
            "items": [
                {
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    # No full product details
                }
                for item in order["items"]
            ],
            "tracking_number": order.get("tracking_number")
        }


# BFF Mobile API
mobile_bff = FastAPI()

@mobile_bff.get("/home")
async def mobile_home(user: User = Depends(get_current_user)):
    """
    Mobile home endpoint

    Optimized for mobile:
    - Minimal data
    - Single request
    - Battery efficient
    """
    bff = MobileBFF(user_service, order_service)
    home_data = await bff.get_user_home(user.id)
    return home_data

@mobile_bff.get("/orders/{order_id}")
async def mobile_order_details(order_id: str):
    """
    Lazy loading for order details

    Only fetched when user taps
    """
    bff = MobileBFF(user_service, order_service)
    order = await bff.get_order_details(order_id)
    return order


# ============================================
# COMPARISON: Web BFF vs Mobile BFF
# ============================================

"""
┌────────────────────────────────────────────────────┐
│         WEB BFF vs MOBILE BFF                      │
├────────────────────────────────────────────────────┤
│                                                    │
│ WEB BFF:                                           │
│ - Response size: ~50KB (full data)                │
│ - Single request: All dashboard data              │
│ - Rich UI: Full order details, analytics          │
│ - Desktop optimized: Large screen, fast network   │
│                                                    │
│ MOBILE BFF:                                        │
│ - Response size: ~5KB (minimal data)              │
│ - Lazy loading: Details on demand                 │
│ - Simple UI: Only essentials                      │
│ - Mobile optimized: Battery, bandwidth            │
│                                                    │
│ BENEFITS:                                          │
│ ✅ Each client gets optimal API                   │
│ ✅ No over-fetching (mobile saves bandwidth)      │
│ ✅ No under-fetching (web gets all data)          │
│ ✅ Independent evolution (web vs mobile teams)    │
│                                                    │
└────────────────────────────────────────────────────┘
"""
```

---

## CATEGORÍA 3: Advanced Rate Limiting & Throttling

### 3.1 Distributed Rate Limiting
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Rate limiting en distributed systems requiere coordinación entre instancias.

**Implementación: Sliding Window Rate Limiter con Redis**

```python
# ============================================
# SLIDING WINDOW RATE LIMITER
# ============================================

from datetime import datetime, timedelta
from typing import Optional
import time

class SlidingWindowRateLimiter:
    """
    Sliding Window Rate Limiter

    More accurate than fixed window
    Prevents burst at window boundaries
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def is_allowed(
        self,
        key: str,
        limit: int,
        window_seconds: int
    ) -> tuple[bool, dict]:
        """
        Check if request is allowed

        Algorithm: Sliding window log
        - Store timestamp of each request
        - Count requests in last N seconds
        - Remove old requests
        """

        now = time.time()
        window_start = now - window_seconds

        # Redis sorted set key
        sorted_set_key = f"rate_limit:{key}"

        # Pipeline for atomic operations
        pipe = self.redis.pipeline()

        # 1. Remove old requests (outside window)
        pipe.zremrangebyscore(
            sorted_set_key,
            min=0,
            max=window_start
        )

        # 2. Count requests in window
        pipe.zcard(sorted_set_key)

        # 3. Add current request
        pipe.zadd(sorted_set_key, {str(now): now})

        # 4. Set expiration (cleanup)
        pipe.expire(sorted_set_key, window_seconds + 1)

        # Execute pipeline
        results = await pipe.execute()

        request_count = results[1]

        # Check limit
        allowed = request_count < limit

        # Calculate retry after
        if not allowed:
            # Get oldest request in window
            oldest_requests = await self.redis.zrange(
                sorted_set_key,
                0,
                0,
                withscores=True
            )
            if oldest_requests:
                oldest_timestamp = oldest_requests[0][1]
                retry_after_seconds = int(
                    (oldest_timestamp + window_seconds) - now
                )
            else:
                retry_after_seconds = window_seconds
        else:
            retry_after_seconds = 0

        return allowed, {
            "limit": limit,
            "remaining": max(0, limit - request_count - 1),
            "reset_at": int(now + window_seconds),
            "retry_after_seconds": retry_after_seconds
        }


# ============================================
# TOKEN BUCKET RATE LIMITER
# ============================================

class TokenBucketRateLimiter:
    """
    Token Bucket Algorithm

    Allows bursts up to bucket size
    Refills at constant rate
    """

    def __init__(self, redis: Redis):
        self.redis = redis

    async def is_allowed(
        self,
        key: str,
        capacity: int,  # Bucket size
        refill_rate: float  # Tokens per second
    ) -> tuple[bool, dict]:
        """
        Check if request is allowed

        Algorithm:
        - Bucket has capacity tokens
        - Each request consumes 1 token
        - Tokens refill at refill_rate per second
        """

        now = time.time()
        bucket_key = f"token_bucket:{key}"

        # Get bucket state
        bucket_data = await self.redis.hgetall(bucket_key)

        if bucket_data:
            # Existing bucket
            tokens = float(bucket_data.get(b'tokens', capacity))
            last_refill = float(bucket_data.get(b'last_refill', now))

            # Calculate tokens to add
            time_passed = now - last_refill
            tokens_to_add = time_passed * refill_rate

            # Refill bucket (up to capacity)
            tokens = min(capacity, tokens + tokens_to_add)
        else:
            # New bucket
            tokens = capacity
            last_refill = now

        # Check if request allowed
        if tokens >= 1:
            # Consume token
            tokens -= 1
            allowed = True

            # Update bucket
            await self.redis.hset(
                bucket_key,
                mapping={
                    'tokens': tokens,
                    'last_refill': now
                }
            )
            await self.redis.expire(bucket_key, 3600)  # Cleanup

        else:
            # No tokens available
            allowed = False

        # Calculate when next token available
        if not allowed:
            time_to_next_token = (1 - tokens) / refill_rate
        else:
            time_to_next_token = 0

        return allowed, {
            "limit": capacity,
            "remaining": int(tokens),
            "retry_after_seconds": int(time_to_next_token)
        }


# ============================================
# TIERED RATE LIMITING
# ============================================

class TieredRateLimiter:
    """
    Tiered Rate Limiting

    Different limits for different user tiers
    """

    def __init__(self, redis: Redis):
        self.sliding_window = SlidingWindowRateLimiter(redis)

        # Tier configurations
        self.tier_limits = {
            'free': {
                'requests_per_minute': 10,
                'requests_per_hour': 100,
                'requests_per_day': 1000
            },
            'basic': {
                'requests_per_minute': 60,
                'requests_per_hour': 1000,
                'requests_per_day': 10000
            },
            'premium': {
                'requests_per_minute': 300,
                'requests_per_hour': 10000,
                'requests_per_day': 100000
            },
            'enterprise': {
                'requests_per_minute': None,  # Unlimited
                'requests_per_hour': None,
                'requests_per_day': None
            }
        }

    async def is_allowed(
        self,
        user_id: str,
        tier: str
    ) -> tuple[bool, dict]:
        """
        Check multiple rate limits

        Checks minute, hour, and day limits
        """

        tier_config = self.tier_limits.get(tier, self.tier_limits['free'])

        # Enterprise: unlimited
        if all(v is None for v in tier_config.values()):
            return True, {"tier": "enterprise", "unlimited": True}

        # Check all time windows
        checks = []

        # Minute limit
        if tier_config['requests_per_minute']:
            allowed, info = await self.sliding_window.is_allowed(
                key=f"user:{user_id}:minute",
                limit=tier_config['requests_per_minute'],
                window_seconds=60
            )
            checks.append((allowed, info, 'minute'))

        # Hour limit
        if tier_config['requests_per_hour']:
            allowed, info = await self.sliding_window.is_allowed(
                key=f"user:{user_id}:hour",
                limit=tier_config['requests_per_hour'],
                window_seconds=3600
            )
            checks.append((allowed, info, 'hour'))

        # Day limit
        if tier_config['requests_per_day']:
            allowed, info = await self.sliding_window.is_allowed(
                key=f"user:{user_id}:day",
                limit=tier_config['requests_per_day'],
                window_seconds=86400
            )
            checks.append((allowed, info, 'day'))

        # If any limit exceeded, deny
        for allowed, info, window in checks:
            if not allowed:
                return False, {
                    "tier": tier,
                    "window": window,
                    "limit": info['limit'],
                    "remaining": info['remaining'],
                    "retry_after_seconds": info['retry_after_seconds']
                }

        # All limits OK
        # Return most restrictive remaining count
        min_remaining = min(
            info['remaining']
            for allowed, info, _ in checks
        )

        return True, {
            "tier": tier,
            "remaining": min_remaining
        }


# ============================================
# FASTAPI INTEGRATION
# ============================================

rate_limiter = TieredRateLimiter(redis_client)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware

    Checks rate limits before processing request
    """

    # Get user
    user = await get_user_from_request(request)

    if not user:
        # Anonymous: strict limits
        user_id = request.client.host
        tier = 'free'
    else:
        user_id = user.id
        tier = user.tier

    # Check rate limit
    allowed, limit_info = await rate_limiter.is_allowed(user_id, tier)

    if not allowed:
        # Rate limit exceeded
        return JSONResponse(
            status_code=429,
            content={
                "error": "rate_limit_exceeded",
                "message": "Too many requests",
                "tier": limit_info['tier'],
                "limit": limit_info['limit'],
                "retry_after_seconds": limit_info['retry_after_seconds']
            },
            headers={
                "X-RateLimit-Limit": str(limit_info['limit']),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(limit_info['retry_after_seconds'])
            }
        )

    # Process request
    response = await call_next(request)

    # Add rate limit headers
    response.headers["X-RateLimit-Limit"] = str(limit_info.get('limit', 'unlimited'))
    response.headers["X-RateLimit-Remaining"] = str(limit_info.get('remaining', 'unlimited'))

    return response
```

---

## CATEGORÍA 4: Idempotency Patterns

### 4.1 Idempotency Keys
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
En sistemas distribuidos, requests pueden duplicarse (network retries, user double-click). Idempotency garantiza que procesar el mismo request múltiples veces produce el mismo resultado.

**Implementación: Idempotency Layer**

```python
# ============================================
# IDEMPOTENCY MANAGER
# ============================================

from enum import Enum
from typing import Optional, Any
import hashlib
import json

class IdempotencyStatus(Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class IdempotencyRecord:
    """Record of idempotent request"""
    idempotency_key: str
    status: IdempotencyStatus
    request_hash: str
    response_data: Optional[dict]
    error: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

class IdempotencyManager:
    """
    Manage idempotent requests

    Pattern:
    1. Client sends idempotency key
    2. Server checks if already processed
    3. If yes, return cached result
    4. If no, process and cache result
    """

    def __init__(self, redis: Redis, ttl: int = 86400):
        self.redis = redis
        self.ttl = ttl  # 24 hours

    def _compute_request_hash(self, request_data: dict) -> str:
        """
        Compute hash of request data

        Ensures request is identical
        """
        request_json = json.dumps(request_data, sort_keys=True)
        return hashlib.sha256(request_json.encode()).hexdigest()

    async def check_idempotency(
        self,
        idempotency_key: str,
        request_data: dict
    ) -> Optional[IdempotencyRecord]:
        """
        Check if request already processed

        Returns cached result if exists
        """

        redis_key = f"idempotency:{idempotency_key}"
        cached_data = await self.redis.get(redis_key)

        if not cached_data:
            # First time seeing this key
            return None

        record = IdempotencyRecord(**json.loads(cached_data))

        # Verify request matches
        request_hash = self._compute_request_hash(request_data)
        if record.request_hash != request_hash:
            raise IdempotencyKeyConflictError(
                "Same idempotency key with different request data"
            )

        return record

    async def start_processing(
        self,
        idempotency_key: str,
        request_data: dict
    ):
        """
        Mark request as processing

        Prevents concurrent processing
        """

        record = IdempotencyRecord(
            idempotency_key=idempotency_key,
            status=IdempotencyStatus.PROCESSING,
            request_hash=self._compute_request_hash(request_data),
            response_data=None,
            error=None,
            created_at=datetime.utcnow(),
            completed_at=None
        )

        redis_key = f"idempotency:{idempotency_key}"

        # Use SET NX (set if not exists) for atomic check
        was_set = await self.redis.set(
            redis_key,
            json.dumps(record.__dict__, default=str),
            ex=self.ttl,
            nx=True  # Only if key doesn't exist
        )

        if not was_set:
            # Someone else is processing
            # Wait and retry
            raise ConcurrentRequestError("Request already being processed")

    async def complete_success(
        self,
        idempotency_key: str,
        response_data: dict
    ):
        """Mark request as completed"""

        redis_key = f"idempotency:{idempotency_key}"
        cached_data = await self.redis.get(redis_key)

        if not cached_data:
            raise IdempotencyRecordNotFoundError()

        record = IdempotencyRecord(**json.loads(cached_data))
        record.status = IdempotencyStatus.COMPLETED
        record.response_data = response_data
        record.completed_at = datetime.utcnow()

        await self.redis.set(
            redis_key,
            json.dumps(record.__dict__, default=str),
            ex=self.ttl
        )

    async def complete_failure(
        self,
        idempotency_key: str,
        error: str
    ):
        """Mark request as failed"""

        redis_key = f"idempotency:{idempotency_key}"
        cached_data = await self.redis.get(redis_key)

        if cached_data:
            record = IdempotencyRecord(**json.loads(cached_data))
            record.status = IdempotencyStatus.FAILED
            record.error = error
            record.completed_at = datetime.utcnow()

            await self.redis.set(
                redis_key,
                json.dumps(record.__dict__, default=str),
                ex=self.ttl
            )


# ============================================
# IDEMPOTENT DECORATOR
# ============================================

def idempotent(idempotency_manager: IdempotencyManager):
    """
    Decorator: Make endpoint idempotent

    Usage:
    @app.post("/payments")
    @idempotent(idempotency_manager)
    async def create_payment(request: PaymentRequest, ...):
        ...
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(
            request: Any,
            idempotency_key: str = Header(..., alias="Idempotency-Key"),
            *args,
            **kwargs
        ):
            # 1. Check if already processed
            existing = await idempotency_manager.check_idempotency(
                idempotency_key,
                request.dict()
            )

            if existing:
                # Already processed
                if existing.status == IdempotencyStatus.PROCESSING:
                    # Still processing (concurrent request)
                    raise HTTPException(
                        status_code=409,
                        detail="Request is being processed"
                    )

                elif existing.status == IdempotencyStatus.COMPLETED:
                    # Return cached result
                    logger.info(
                        "idempotent_request_cached",
                        idempotency_key=idempotency_key
                    )
                    return existing.response_data

                elif existing.status == IdempotencyStatus.FAILED:
                    # Previous attempt failed, allow retry
                    pass

            # 2. Mark as processing
            await idempotency_manager.start_processing(
                idempotency_key,
                request.dict()
            )

            try:
                # 3. Execute actual function
                result = await func(request, *args, **kwargs)

                # 4. Cache success result
                await idempotency_manager.complete_success(
                    idempotency_key,
                    result if isinstance(result, dict) else result.dict()
                )

                return result

            except Exception as e:
                # 5. Cache failure
                await idempotency_manager.complete_failure(
                    idempotency_key,
                    str(e)
                )
                raise

        return wrapper
    return decorator


# ============================================
# USAGE EXAMPLE
# ============================================

idempotency_manager = IdempotencyManager(redis_client)

@app.post("/payments")
@idempotent(idempotency_manager)
async def create_payment(
    request: CreatePaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key")
):
    """
    Create payment (idempotent)

    Client provides Idempotency-Key header
    Duplicate requests return same result
    """

    # Process payment
    payment = await payment_service.charge(
        customer_id=request.customer_id,
        amount=request.amount,
        payment_method_id=request.payment_method_id
    )

    return {
        "payment_id": payment.id,
        "status": payment.status,
        "amount": payment.amount
    }


# CLIENT USAGE:
"""
import uuid

# Generate idempotency key
idempotency_key = str(uuid.uuid4())

# First request
response = requests.post(
    "https://api.example.com/payments",
    headers={
        "Idempotency-Key": idempotency_key
    },
    json={
        "customer_id": "cust_123",
        "amount": 99.99,
        "payment_method_id": "pm_456"
    }
)
# Result: payment_id = "pay_789"

# Duplicate request (network retry, user double-click)
response = requests.post(
    "https://api.example.com/payments",
    headers={
        "Idempotency-Key": idempotency_key  # SAME KEY
    },
    json={
        "customer_id": "cust_123",
        "amount": 99.99,
        "payment_method_id": "pm_456"
    }
)
# Result: payment_id = "pay_789" (SAME payment, not charged twice)
"""
```

---

## CATEGORÍA 5: Temporal Workflow Orchestration

### 5.1 Temporal for Long-Running Workflows
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Long-running business workflows (order fulfillment, onboarding) requieren orchestration confiable. Temporal provee durable execution.

**Implementación: Order Fulfillment Workflow con Temporal**

```python
# ============================================
# TEMPORAL WORKFLOW: Order Fulfillment
# ============================================

from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
from datetime import timedelta

# ============================================
# ACTIVITIES (Side effects)
# ============================================

@activity.defn
async def reserve_inventory(order_id: str, items: List[dict]) -> dict:
    """
    Activity: Reserve inventory

    Activities can fail and retry
    """
    logger.info("reserve_inventory", order_id=order_id)

    for item in items:
        await inventory_service.reserve(
            product_id=item['product_id'],
            quantity=item['quantity'],
            order_id=order_id
        )

    return {"reserved": True}


@activity.defn
async def charge_payment(order_id: str, amount: Decimal) -> dict:
    """Activity: Charge payment"""
    logger.info("charge_payment", order_id=order_id, amount=amount)

    payment = await payment_gateway.charge(amount)

    if not payment.success:
        raise PaymentFailedError(payment.error)

    return {"payment_id": payment.id}


@activity.defn
async def ship_order(order_id: str) -> dict:
    """Activity: Ship order"""
    logger.info("ship_order", order_id=order_id)

    shipment = await shipping_service.create_shipment(order_id)

    return {"tracking_number": shipment.tracking_number}


@activity.defn
async def send_confirmation_email(order_id: str, email: str):
    """Activity: Send email"""
    await email_service.send_order_confirmation(email, order_id)


@activity.defn
async def refund_payment(payment_id: str):
    """Activity: Refund (compensation)"""
    await payment_gateway.refund(payment_id)


@activity.defn
async def release_inventory(order_id: str):
    """Activity: Release inventory (compensation)"""
    await inventory_service.release(order_id)


# ============================================
# WORKFLOW: Order Fulfillment
# ============================================

@workflow.defn
class OrderFulfillmentWorkflow:
    """
    Temporal Workflow: Order Fulfillment

    Long-running workflow:
    1. Reserve inventory
    2. Charge payment
    3. Wait for warehouse confirmation (hours/days)
    4. Ship order
    5. Send notifications

    Temporal guarantees:
    - Durable execution (survives crashes)
    - Automatic retries
    - Compensation on failure
    - Timeout handling
    """

    @workflow.run
    async def run(
        self,
        order_id: str,
        customer_email: str,
        items: List[dict],
        total_amount: Decimal
    ) -> dict:
        """
        Execute order fulfillment workflow

        Temporal ensures this completes even if:
        - Process crashes
        - Server restarts
        - Takes days to complete
        """

        workflow.logger.info(
            "OrderFulfillmentWorkflow started",
            order_id=order_id
        )

        payment_id = None
        inventory_reserved = False

        try:
            # Step 1: Reserve inventory
            # Retry policy: retry for 5 minutes
            result = await workflow.execute_activity(
                reserve_inventory,
                args=[order_id, items],
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy={
                    "initial_interval": timedelta(seconds=1),
                    "maximum_interval": timedelta(seconds=30),
                    "maximum_attempts": 10
                }
            )
            inventory_reserved = True

            # Step 2: Charge payment
            payment_result = await workflow.execute_activity(
                charge_payment,
                args=[order_id, total_amount],
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy={
                    "initial_interval": timedelta(seconds=1),
                    "maximum_attempts": 3  # Don't retry payment too many times
                }
            )
            payment_id = payment_result['payment_id']

            # Step 3: Wait for warehouse confirmation
            # This could take hours/days
            # Temporal handles the wait durably
            warehouse_confirmed = await workflow.wait_condition(
                lambda: self.warehouse_confirmed,
                timeout=timedelta(hours=48)  # 48 hour timeout
            )

            if not warehouse_confirmed:
                raise WarehouseTimeoutError("Warehouse didn't confirm in 48 hours")

            # Step 4: Ship order
            shipment_result = await workflow.execute_activity(
                ship_order,
                args=[order_id],
                start_to_close_timeout=timedelta(minutes=5)
            )

            # Step 5: Send confirmation email
            await workflow.execute_activity(
                send_confirmation_email,
                args=[order_id, customer_email],
                start_to_close_timeout=timedelta(minutes=1)
            )

            workflow.logger.info(
                "OrderFulfillmentWorkflow completed",
                order_id=order_id,
                tracking_number=shipment_result['tracking_number']
            )

            return {
                "status": "completed",
                "payment_id": payment_id,
                "tracking_number": shipment_result['tracking_number']
            }

        except Exception as e:
            # COMPENSATION: Rollback on failure
            workflow.logger.error(
                "OrderFulfillmentWorkflow failed",
                order_id=order_id,
                error=str(e)
            )

            # Refund payment if charged
            if payment_id:
                await workflow.execute_activity(
                    refund_payment,
                    args=[payment_id],
                    start_to_close_timeout=timedelta(minutes=2)
                )

            # Release inventory if reserved
            if inventory_reserved:
                await workflow.execute_activity(
                    release_inventory,
                    args=[order_id],
                    start_to_close_timeout=timedelta(minutes=2)
                )

            raise

    # Signals (external events)
    warehouse_confirmed = False

    @workflow.signal
    def confirm_warehouse(self):
        """
        Signal from warehouse service

        External event can trigger workflow continuation
        """
        self.warehouse_confirmed = True


# ============================================
# START WORKFLOW
# ============================================

async def start_order_fulfillment(
    order_id: str,
    customer_email: str,
    items: List[dict],
    total_amount: Decimal
):
    """
    Start order fulfillment workflow

    Workflow runs in background
    Survives crashes, restarts
    """

    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Start workflow
    handle = await client.start_workflow(
        OrderFulfillmentWorkflow.run,
        args=[order_id, customer_email, items, total_amount],
        id=f"order-fulfillment-{order_id}",
        task_queue="order-fulfillment"
    )

    logger.info(
        "workflow_started",
        workflow_id=handle.id,
        run_id=handle.result_run_id
    )

    return handle.id


# ============================================
# WAREHOUSE CONFIRMATION (Signal)
# ============================================

async def confirm_warehouse_ready(order_id: str):
    """
    Warehouse confirms order ready to ship

    Sends signal to workflow
    """

    client = await Client.connect("localhost:7233")

    # Get workflow handle
    handle = client.get_workflow_handle(f"order-fulfillment-{order_id}")

    # Send signal
    await handle.signal(OrderFulfillmentWorkflow.confirm_warehouse)

    logger.info("warehouse_confirmed", order_id=order_id)


# ============================================
# BENEFITS OF TEMPORAL
# ============================================

"""
┌────────────────────────────────────────────────────┐
│         TEMPORAL WORKFLOW BENEFITS                 │
├────────────────────────────────────────────────────┤
│                                                    │
│ ✅ DURABLE EXECUTION                               │
│    - Workflow survives process crashes            │
│    - Survives server restarts                     │
│    - State persisted automatically                │
│                                                    │
│ ✅ AUTOMATIC RETRIES                               │
│    - Activities retry on failure                  │
│    - Configurable retry policies                  │
│    - Exponential backoff                          │
│                                                    │
│ ✅ LONG-RUNNING WORKFLOWS                          │
│    - Can run for days, weeks, months              │
│    - Timers and waits handled durably             │
│    - No cron jobs needed                          │
│                                                    │
│ ✅ COMPENSATION                                    │
│    - Saga pattern built-in                        │
│    - Automatic rollback on failure                │
│    - Consistent state guarantees                  │
│                                                    │
│ ✅ VISIBILITY                                      │
│    - Workflow history visible in UI               │
│    - Current state queryable                      │
│    - Debugging is easy                            │
│                                                    │
│ ❌ DOWNSIDES                                       │
│    - Operational complexity (run Temporal server) │
│    - Learning curve                               │
│    - Deterministic constraints                    │
│                                                    │
└────────────────────────────────────────────────────┘
"""
```

---

## Decisiones Consolidadas 2026

```
┌──────────────────────────────────────────────────────────────┐
│    MICROSERVICES PATTERNS AVANZADOS - CHECKLIST 2026         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. STRANGLER PATTERN                                         │
│    ├─ [ ] Proxy layer para routing incremental              │
│    ├─ [ ] Percentage-based rollout                          │
│    ├─ [ ] Monitoring: legacy vs new comparison              │
│    ├─ [ ] Rollback capability                               │
│    └─ [ ] Legacy decommission plan                          │
│                                                              │
│ 2. BACKEND FOR FRONTEND (BFF)                                │
│    ├─ [ ] Separate BFF per client type                      │
│    ├─ [ ] Web BFF (rich data, aggregations)                 │
│    ├─ [ ] Mobile BFF (minimal data, lazy loading)           │
│    └─ [ ] API composition in BFF layer                      │
│                                                              │
│ 3. RATE LIMITING                                             │
│    ├─ [ ] Distributed rate limiting con Redis               │
│    ├─ [ ] Sliding window algorithm                          │
│    ├─ [ ] Tiered limits (free, premium, enterprise)         │
│    ├─ [ ] Token bucket for burst handling                   │
│    └─ [ ] Rate limit headers (X-RateLimit-*)                │
│                                                              │
│ 4. IDEMPOTENCY                                               │
│    ├─ [ ] Idempotency keys en critical endpoints            │
│    ├─ [ ] Request deduplication                             │
│    ├─ [ ] Cached responses (24h TTL)                        │
│    └─ [ ] Conflict detection (same key, different request)  │
│                                                              │
│ 5. WORKFLOW ORCHESTRATION                                    │
│    ├─ [ ] Temporal for long-running workflows               │
│    ├─ [ ] Durable execution guarantees                      │
│    ├─ [ ] Automatic compensation (Saga)                     │
│    ├─ [ ] Signals for external events                       │
│    └─ [ ] Workflow visibility & debugging                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Conclusión:**

Este archivo cubre patrones avanzados de microservices para 2026:

1. **Strangler Pattern**: Migración incremental de monolito a microservices sin downtime
2. **BFF Pattern**: APIs optimizadas por tipo de cliente (Web vs Mobile)
3. **Advanced Rate Limiting**: Sliding window, token bucket, tiered limits
4. **Idempotency**: Garantizar exactly-once processing con idempotency keys
5. **Temporal Workflows**: Orchestration confiable para workflows de días/semanas

Todos los patrones incluyen implementaciones completas en Python con ejemplos de producción, configuración, y trade-offs detallados.
