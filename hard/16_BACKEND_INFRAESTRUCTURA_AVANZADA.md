# Backend: Infraestructura Avanzada y Service Mesh

## Objetivo
Patrones de infraestructura para microservicios: API Gateway, Service Discovery, Distributed Caching, Security patterns, y Chaos Engineering.

---

## CATEGORÍA 1: API Gateway Patterns

### 1.1 API Gateway Implementation
**Dificultad:** ⭐⭐⭐⭐⭐

**Python - Custom API Gateway**

```python
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
import httpx
from typing import Dict, List, Optional
import asyncio
import time
import hashlib

class RouteConfig:
    """Configuration for a route"""
    def __init__(
        self,
        path: str,
        backend_url: str,
        methods: List[str] = None,
        rate_limit: int = None,
        auth_required: bool = True,
        timeout: int = 30,
        retry_count: int = 3,
        cache_ttl: int = 0
    ):
        self.path = path
        self.backend_url = backend_url
        self.methods = methods or ['GET', 'POST', 'PUT', 'DELETE']
        self.rate_limit = rate_limit
        self.auth_required = auth_required
        self.timeout = timeout
        self.retry_count = retry_count
        self.cache_ttl = cache_ttl

class APIGateway:
    """
    Full-featured API Gateway with:
    - Routing
    - Rate limiting
    - Authentication
    - Caching
    - Load balancing
    - Circuit breaking
    - Request/Response transformation
    """

    def __init__(self, redis_client):
        self.routes: Dict[str, RouteConfig] = {}
        self.redis = redis_client
        self.circuit_breakers = {}
        self.service_instances = {}

    def add_route(self, route_config: RouteConfig):
        """Register a route"""
        self.routes[route_config.path] = route_config

    def add_service_instances(self, service_name: str, instances: List[str]):
        """Register service instances for load balancing"""
        self.service_instances[service_name] = {
            'instances': instances,
            'current_index': 0
        }

    async def handle_request(self, request: Request) -> Response:
        """Main request handler"""

        path = request.url.path
        method = request.method

        # 1. Find matching route
        route = self._find_route(path)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")

        if method not in route.methods:
            raise HTTPException(status_code=405, detail="Method not allowed")

        # 2. Authentication
        if route.auth_required:
            user = await self._authenticate(request)
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized")
            request.state.user = user

        # 3. Rate limiting
        if route.rate_limit:
            allowed = await self._check_rate_limit(
                request.state.user.id,
                route.path,
                route.rate_limit
            )
            if not allowed:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # 4. Check cache
        if method == 'GET' and route.cache_ttl > 0:
            cached_response = await self._get_cached_response(request)
            if cached_response:
                return cached_response

        # 5. Circuit breaker check
        circuit_breaker = self._get_circuit_breaker(route.backend_url)
        if circuit_breaker.is_open():
            raise HTTPException(
                status_code=503,
                detail="Service temporarily unavailable"
            )

        # 6. Load balancing
        backend_url = self._get_backend_instance(route.backend_url)

        # 7. Request transformation
        headers = await self._transform_request_headers(request)

        # 8. Forward request with retry
        response = await self._forward_request(
            backend_url=backend_url,
            request=request,
            headers=headers,
            timeout=route.timeout,
            retry_count=route.retry_count
        )

        # 9. Response transformation
        response = await self._transform_response(response)

        # 10. Cache response
        if method == 'GET' and route.cache_ttl > 0:
            await self._cache_response(request, response, route.cache_ttl)

        return response

    def _find_route(self, path: str) -> Optional[RouteConfig]:
        """Find matching route with pattern matching"""

        # Exact match
        if path in self.routes:
            return self.routes[path]

        # Pattern matching
        for route_path, route_config in self.routes.items():
            if self._path_matches(path, route_path):
                return route_config

        return None

    def _path_matches(self, path: str, pattern: str) -> bool:
        """Check if path matches pattern (supports wildcards)"""

        if '*' not in pattern:
            return path == pattern

        # Simple wildcard matching
        pattern_parts = pattern.split('/')
        path_parts = path.split('/')

        if len(pattern_parts) != len(path_parts):
            return False

        for pattern_part, path_part in zip(pattern_parts, path_parts):
            if pattern_part == '*':
                continue
            if pattern_part.startswith('{') and pattern_part.endswith('}'):
                continue
            if pattern_part != path_part:
                return False

        return True

    async def _authenticate(self, request: Request) -> Optional[dict]:
        """Authenticate request"""

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header[7:]

        # Verify JWT token
        try:
            user = await verify_jwt_token(token)
            return user
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return None

    async def _check_rate_limit(
        self,
        user_id: int,
        path: str,
        limit: int
    ) -> bool:
        """Check rate limit using Redis"""

        key = f"rate_limit:{user_id}:{path}"
        current_minute = int(time.time() / 60)
        rate_key = f"{key}:{current_minute}"

        current_count = await self.redis.get(rate_key)
        current_count = int(current_count) if current_count else 0

        if current_count >= limit:
            return False

        # Increment
        pipe = self.redis.pipeline()
        pipe.incr(rate_key)
        pipe.expire(rate_key, 60)
        await pipe.execute()

        return True

    async def _get_cached_response(self, request: Request) -> Optional[Response]:
        """Get cached response"""

        cache_key = self._generate_cache_key(request)
        cached = await self.redis.get(cache_key)

        if cached:
            data = json.loads(cached)
            return Response(
                content=data['content'],
                status_code=data['status_code'],
                headers={'X-Cache': 'HIT'}
            )

        return None

    async def _cache_response(
        self,
        request: Request,
        response: Response,
        ttl: int
    ):
        """Cache response"""

        cache_key = self._generate_cache_key(request)

        cache_data = {
            'content': response.body.decode() if response.body else '',
            'status_code': response.status_code
        }

        await self.redis.setex(
            cache_key,
            ttl,
            json.dumps(cache_data)
        )

    def _generate_cache_key(self, request: Request) -> str:
        """Generate cache key from request"""

        key_parts = [
            request.method,
            request.url.path,
            str(sorted(request.query_params.items()))
        ]

        key_string = ':'.join(key_parts)
        return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"

    def _get_circuit_breaker(self, service_url: str):
        """Get or create circuit breaker for service"""

        if service_url not in self.circuit_breakers:
            self.circuit_breakers[service_url] = CircuitBreaker(
                failure_threshold=5,
                recovery_timeout=30
            )

        return self.circuit_breakers[service_url]

    def _get_backend_instance(self, backend_url: str) -> str:
        """Get backend instance using round-robin load balancing"""

        # Extract service name
        service_name = backend_url.split('://')[1].split('/')[0]

        if service_name in self.service_instances:
            service_config = self.service_instances[service_name]
            instances = service_config['instances']

            # Round-robin
            index = service_config['current_index']
            instance = instances[index]

            # Update index
            service_config['current_index'] = (index + 1) % len(instances)

            # Replace service name with instance
            return backend_url.replace(service_name, instance)

        return backend_url

    async def _transform_request_headers(self, request: Request) -> dict:
        """Transform request headers"""

        headers = dict(request.headers)

        # Remove hop-by-hop headers
        hop_by_hop = [
            'connection', 'keep-alive', 'proxy-authenticate',
            'proxy-authorization', 'te', 'trailers',
            'transfer-encoding', 'upgrade'
        ]

        for header in hop_by_hop:
            headers.pop(header, None)

        # Add gateway headers
        headers['X-Forwarded-For'] = request.client.host
        headers['X-Gateway-Request-ID'] = str(uuid.uuid4())

        # Add user context
        if hasattr(request.state, 'user'):
            headers['X-User-ID'] = str(request.state.user.id)

        return headers

    async def _forward_request(
        self,
        backend_url: str,
        request: Request,
        headers: dict,
        timeout: int,
        retry_count: int
    ) -> Response:
        """Forward request to backend service with retry"""

        # Get request body
        body = await request.body()

        for attempt in range(retry_count):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.request(
                        method=request.method,
                        url=f"{backend_url}{request.url.path}",
                        params=request.query_params,
                        headers=headers,
                        content=body,
                        timeout=timeout
                    )

                    # Circuit breaker - record success
                    circuit_breaker = self._get_circuit_breaker(backend_url)
                    circuit_breaker.record_success()

                    return Response(
                        content=response.content,
                        status_code=response.status_code,
                        headers=dict(response.headers)
                    )

            except httpx.TimeoutException:
                logger.warning(
                    f"Request timeout to {backend_url} (attempt {attempt + 1})"
                )

                if attempt == retry_count - 1:
                    # Circuit breaker - record failure
                    circuit_breaker = self._get_circuit_breaker(backend_url)
                    circuit_breaker.record_failure()
                    raise HTTPException(status_code=504, detail="Gateway timeout")

                await asyncio.sleep(2 ** attempt)

            except Exception as e:
                logger.error(f"Request error: {e}")

                # Circuit breaker - record failure
                circuit_breaker = self._get_circuit_breaker(backend_url)
                circuit_breaker.record_failure()

                raise HTTPException(status_code=502, detail="Bad gateway")

    async def _transform_response(self, response: Response) -> Response:
        """Transform response"""

        # Add custom headers
        response.headers['X-Gateway'] = 'custom-gateway-v1'
        response.headers['X-Response-Time'] = str(time.time())

        return response

# Gateway setup
gateway = APIGateway(redis_client)

# Register routes
gateway.add_route(RouteConfig(
    path='/api/users/*',
    backend_url='http://user-service/users',
    rate_limit=100,
    timeout=10,
    cache_ttl=60
))

gateway.add_route(RouteConfig(
    path='/api/orders/*',
    backend_url='http://order-service/orders',
    rate_limit=50,
    timeout=30
))

gateway.add_route(RouteConfig(
    path='/api/public/*',
    backend_url='http://public-service/public',
    auth_required=False,
    rate_limit=1000,
    cache_ttl=300
))

# Register service instances for load balancing
gateway.add_service_instances('user-service', [
    'user-service-1:8000',
    'user-service-2:8000',
    'user-service-3:8000'
])

# Main gateway endpoint
app = FastAPI()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_handler(request: Request):
    return await gateway.handle_request(request)

# Request/Response logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    logger.info(
        "Gateway request",
        method=request.method,
        path=request.url.path,
        client=request.client.host
    )

    response = await call_next(request)

    duration = (time.time() - start_time) * 1000

    logger.info(
        "Gateway response",
        status=response.status_code,
        duration_ms=duration
    )

    return response
```

---

## CATEGORÍA 2: Service Discovery

### 2.1 Service Registry with Consul
**Dificultad:** ⭐⭐⭐⭐

```python
import consul
import asyncio
from typing import List, Optional

class ServiceRegistry:
    """
    Service discovery using Consul
    """

    def __init__(self, consul_host: str = 'localhost', consul_port: int = 8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)
        self.service_name = None
        self.service_id = None
        self.heartbeat_task = None

    async def register_service(
        self,
        service_name: str,
        service_port: int,
        service_address: str = None,
        health_check_interval: str = '10s',
        tags: List[str] = None
    ):
        """Register service with Consul"""

        self.service_name = service_name
        self.service_id = f"{service_name}-{service_port}"

        # Service definition
        service = {
            'name': service_name,
            'id': self.service_id,
            'address': service_address or self._get_local_ip(),
            'port': service_port,
            'tags': tags or [],
            'check': {
                'http': f'http://{service_address or "localhost"}:{service_port}/health',
                'interval': health_check_interval,
                'timeout': '5s',
                'deregister_critical_service_after': '1m'
            }
        }

        # Register
        self.consul.agent.service.register(**service)

        logger.info(
            f"Service registered: {self.service_id}",
            service_name=service_name,
            port=service_port
        )

        # Start heartbeat
        self.heartbeat_task = asyncio.create_task(self._heartbeat())

    async def deregister_service(self):
        """Deregister service from Consul"""

        if self.service_id:
            self.consul.agent.service.deregister(self.service_id)
            logger.info(f"Service deregistered: {self.service_id}")

        if self.heartbeat_task:
            self.heartbeat_task.cancel()

    async def discover_service(
        self,
        service_name: str,
        tag: str = None,
        passing_only: bool = True
    ) -> List[dict]:
        """Discover instances of a service"""

        # Query Consul for service instances
        _, services = self.consul.health.service(
            service_name,
            passing=passing_only,
            tag=tag
        )

        instances = []
        for service in services:
            instances.append({
                'id': service['Service']['ID'],
                'address': service['Service']['Address'],
                'port': service['Service']['Port'],
                'tags': service['Service']['Tags'],
                'health': service['Checks']
            })

        return instances

    async def get_service_address(
        self,
        service_name: str,
        load_balance: bool = True
    ) -> Optional[str]:
        """Get address of a service instance"""

        instances = await self.discover_service(service_name)

        if not instances:
            logger.warning(f"No instances found for service: {service_name}")
            return None

        if load_balance:
            # Simple round-robin (in production, use more sophisticated LB)
            instance = random.choice(instances)
        else:
            instance = instances[0]

        return f"http://{instance['address']}:{instance['port']}"

    async def _heartbeat(self):
        """Maintain service registration with periodic heartbeat"""

        while True:
            try:
                await asyncio.sleep(10)

                # Update TTL check
                self.consul.agent.check.ttl_pass(f"service:{self.service_id}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")

    def _get_local_ip(self) -> str:
        """Get local IP address"""
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    async def watch_service(
        self,
        service_name: str,
        callback: callable
    ):
        """Watch for changes in service instances"""

        index = None

        while True:
            try:
                # Blocking query with long polling
                index, services = self.consul.health.service(
                    service_name,
                    index=index,
                    wait='30s'
                )

                # Notify callback of changes
                instances = [
                    {
                        'address': s['Service']['Address'],
                        'port': s['Service']['Port']
                    }
                    for s in services
                ]

                await callback(service_name, instances)

            except Exception as e:
                logger.error(f"Service watch error: {e}")
                await asyncio.sleep(5)

# Usage
registry = ServiceRegistry(consul_host='consul.example.com')

# Register service on startup
@app.on_event("startup")
async def startup():
    await registry.register_service(
        service_name='order-service',
        service_port=8000,
        tags=['v1', 'production']
    )

# Deregister on shutdown
@app.on_event("shutdown")
async def shutdown():
    await registry.deregister_service()

# Health check endpoint (required by Consul)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Using service discovery in client
class ServiceClient:
    """Client that uses service discovery"""

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry

    async def call_user_service(self, endpoint: str, **kwargs):
        """Call user service using service discovery"""

        # Discover service
        service_url = await self.registry.get_service_address('user-service')

        if not service_url:
            raise Exception("User service not available")

        # Make request
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{service_url}{endpoint}", **kwargs)
            return response.json()

# Service mesh integration
class ServiceMeshClient:
    """
    Client with service mesh features:
    - Service discovery
    - Circuit breaking
    - Retry
    - Load balancing
    """

    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.circuit_breakers = {}

    async def call(
        self,
        service_name: str,
        endpoint: str,
        method: str = 'GET',
        **kwargs
    ):
        """Make service call with resilience patterns"""

        # Get service instances
        instances = await self.registry.discover_service(service_name)

        if not instances:
            raise ServiceUnavailableError(service_name)

        # Try instances with retry
        for attempt in range(3):
            # Round-robin load balancing
            instance = instances[attempt % len(instances)]
            url = f"http://{instance['address']}:{instance['port']}{endpoint}"

            # Check circuit breaker
            circuit_breaker = self._get_circuit_breaker(service_name)
            if circuit_breaker.is_open():
                continue

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.request(method, url, timeout=10, **kwargs)

                    circuit_breaker.record_success()
                    return response.json()

            except Exception as e:
                circuit_breaker.record_failure()
                logger.warning(f"Service call failed: {service_name}, attempt {attempt}")

                if attempt < 2:
                    await asyncio.sleep(2 ** attempt)

        raise ServiceCallError(service_name)

    def _get_circuit_breaker(self, service_name: str):
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker(
                failure_threshold=5,
                recovery_timeout=30
            )
        return self.circuit_breakers[service_name]
```

---

## CATEGORÍA 3: Distributed Caching

### 3.1 Redis Cluster Pattern
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from redis.cluster import RedisCluster
from redis.exceptions import RedisClusterException
import hashlib
import pickle
from typing import Optional, Any
import asyncio

class DistributedCache:
    """
    Distributed caching with Redis Cluster
    Features:
    - Automatic sharding
    - High availability
    - Cache-aside pattern
    - Write-through pattern
    - Cache stampede prevention
    """

    def __init__(self, startup_nodes: List[dict]):
        self.cluster = RedisCluster(
            startup_nodes=startup_nodes,
            decode_responses=False,
            skip_full_coverage_check=False,
            max_connections_per_node=50,
            socket_keepalive=True,
            socket_connect_timeout=5,
            retry_on_timeout=True,
            cluster_error_retry_attempts=3
        )

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""

        try:
            value = self.cluster.get(key)
            if value:
                return pickle.loads(value)
            return None

        except RedisClusterException as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600,
        nx: bool = False,
        xx: bool = False
    ) -> bool:
        """Set value in cache"""

        try:
            serialized = pickle.dumps(value)

            return self.cluster.set(
                key,
                serialized,
                ex=ttl,
                nx=nx,  # Set only if not exists
                xx=xx   # Set only if exists
            )

        except RedisClusterException as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from cache"""

        try:
            return bool(self.cluster.delete(key))
        except RedisClusterException as e:
            logger.error(f"Cache delete error: {e}")
            return False

    async def get_or_set(
        self,
        key: str,
        factory: callable,
        ttl: int = 3600
    ) -> Any:
        """
        Cache-aside pattern with stampede prevention
        """

        # Try to get from cache
        value = await self.get(key)
        if value is not None:
            return value

        # Acquire lock to prevent cache stampede
        lock_key = f"lock:{key}"
        lock_acquired = await self.set(lock_key, "1", ttl=10, nx=True)

        if lock_acquired:
            try:
                # Generate value
                value = await factory()

                # Store in cache
                await self.set(key, value, ttl)

                return value

            finally:
                # Release lock
                await self.delete(lock_key)

        else:
            # Another process is generating the value
            # Wait and retry
            for _ in range(10):
                await asyncio.sleep(0.1)

                value = await self.get(key)
                if value is not None:
                    return value

            # Fallback: generate value without caching
            return await factory()

    async def invalidate_pattern(self, pattern: str):
        """
        Invalidate all keys matching pattern
        Warning: This can be expensive in large clusters
        """

        cursor = 0
        keys_deleted = 0

        while True:
            cursor, keys = self.cluster.scan(
                cursor=cursor,
                match=pattern,
                count=100
            )

            if keys:
                self.cluster.delete(*keys)
                keys_deleted += len(keys)

            if cursor == 0:
                break

        logger.info(f"Invalidated {keys_deleted} keys matching {pattern}")

    async def get_multi(self, keys: List[str]) -> dict:
        """Get multiple keys (uses pipeline for efficiency)"""

        try:
            # Group keys by slot for efficient pipelining
            keys_by_slot = self._group_keys_by_slot(keys)

            results = {}

            for slot_keys in keys_by_slot.values():
                # Use pipeline for keys in same slot
                pipe = self.cluster.pipeline()

                for key in slot_keys:
                    pipe.get(key)

                values = pipe.execute()

                for key, value in zip(slot_keys, values):
                    if value:
                        results[key] = pickle.loads(value)

            return results

        except RedisClusterException as e:
            logger.error(f"Cache get_multi error: {e}")
            return {}

    async def set_multi(self, data: dict, ttl: int = 3600):
        """Set multiple keys"""

        try:
            keys_by_slot = self._group_keys_by_slot(list(data.keys()))

            for slot_keys in keys_by_slot.values():
                pipe = self.cluster.pipeline()

                for key in slot_keys:
                    value = pickle.dumps(data[key])
                    pipe.setex(key, ttl, value)

                pipe.execute()

        except RedisClusterException as e:
            logger.error(f"Cache set_multi error: {e}")

    def _group_keys_by_slot(self, keys: List[str]) -> dict:
        """Group keys by Redis slot for efficient pipelining"""

        keys_by_slot = {}

        for key in keys:
            slot = self.cluster.connection_pool.nodes.keyslot(key)

            if slot not in keys_by_slot:
                keys_by_slot[slot] = []

            keys_by_slot[slot].append(key)

        return keys_by_slot

    async def increment(self, key: str, amount: int = 1) -> int:
        """Atomic increment"""
        return self.cluster.incrby(key, amount)

    async def decrement(self, key: str, amount: int = 1) -> int:
        """Atomic decrement"""
        return self.cluster.decrby(key, amount)

    async def add_to_set(self, key: str, *members):
        """Add members to set"""
        return self.cluster.sadd(key, *members)

    async def get_set_members(self, key: str) -> set:
        """Get all members of set"""
        return self.cluster.smembers(key)

    async def push_to_list(self, key: str, *values):
        """Push values to list (queue)"""
        return self.cluster.lpush(key, *values)

    async def pop_from_list(self, key: str) -> Optional[Any]:
        """Pop value from list"""
        value = self.cluster.rpop(key)
        if value:
            return pickle.loads(value)
        return None

# Usage examples
cache = DistributedCache(startup_nodes=[
    {"host": "redis-1", "port": 7000},
    {"host": "redis-2", "port": 7001},
    {"host": "redis-3", "port": 7002}
])

# Cache-aside pattern
@cache_aside(cache, ttl=3600, key_prefix="user")
async def get_user(user_id: int):
    """
    Decorator automatically handles caching
    Key: user:{user_id}
    """
    return await db.query(User).filter(User.id == user_id).first()

def cache_aside(cache: DistributedCache, ttl: int, key_prefix: str):
    """Decorator for cache-aside pattern"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{':'.join(map(str, args))}"

            # Try cache first
            result = await cache.get(cache_key)
            if result is not None:
                logger.info(f"Cache hit: {cache_key}")
                return result

            # Cache miss - call function
            logger.info(f"Cache miss: {cache_key}")
            result = await func(*args, **kwargs)

            # Store in cache
            await cache.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator

# Write-through pattern
async def update_user(user_id: int, data: dict):
    """Update user with write-through caching"""

    # Update database
    user = await db.query(User).filter(User.id == user_id).first()
    for key, value in data.items():
        setattr(user, key, value)
    await db.commit()

    # Update cache
    cache_key = f"user:{user_id}"
    await cache.set(cache_key, user, ttl=3600)

    return user

# Multi-level caching
class MultiLevelCache:
    """
    L1: In-memory (LRU)
    L2: Redis Cluster
    """

    def __init__(self, redis_cache: DistributedCache, l1_size: int = 1000):
        from functools import lru_cache
        self.redis = redis_cache
        self.l1_cache = {}
        self.l1_size = l1_size

    async def get(self, key: str) -> Optional[Any]:
        # Try L1 first
        if key in self.l1_cache:
            return self.l1_cache[key]

        # Try L2
        value = await self.redis.get(key)

        if value is not None:
            # Backfill L1
            self._l1_set(key, value)

        return value

    async def set(self, key: str, value: Any, ttl: int = 3600):
        # Set in both levels
        self._l1_set(key, value)
        await self.redis.set(key, value, ttl)

    def _l1_set(self, key: str, value: Any):
        if len(self.l1_cache) >= self.l1_size:
            # Evict oldest
            self.l1_cache.pop(next(iter(self.l1_cache)))

        self.l1_cache[key] = value
```

---

Continúa en siguiente sección...

---

## Resumen Infraestructura Avanzada

| Tema | Dificultad | Complejidad | Impacto | Prioridad |
|------|------------|-------------|---------|-----------|
| API Gateway | 5 | 5 | 5 | **CRÍTICA** |
| Service Discovery | 4 | 4 | 5 | **CRÍTICA** |
| Distributed Caching | 5 | 5 | 5 | **CRÍTICA** |
| Load Balancing | 4 | 4 | 5 | **CRÍTICA** |
| Circuit Breaker | 4 | 4 | 5 | **CRÍTICA** |
| Cache Stampede Prevention | 5 | 4 | 4 | **ALTA** |

**El siguiente archivo continuará con:**
- Security avanzada (OAuth2, mTLS, API Key rotation)
- Chaos Engineering patterns
- Performance optimization (database indexing, query optimization)
- Monitoring y Alerting (Prometheus, Grafana)
- Backup y Disaster Recovery
