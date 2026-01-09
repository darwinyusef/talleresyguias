# Conocimientos Técnicos Avanzados: Backend Development II

## Objetivo
Temas avanzados y complejos de arquitectura backend que complementan el desarrollo de APIs y servicios distribuidos de alto rendimiento.

---

## CATEGORÍA 1: Microservicios y Service Mesh

### 1.1 Service-to-Service Communication
**Dificultad:** ⭐⭐⭐⭐⭐

**gRPC con Protocol Buffers**

```protobuf
// user.proto
syntax = "proto3";

package user;

service UserService {
    rpc GetUser(GetUserRequest) returns (User);
    rpc ListUsers(ListUsersRequest) returns (stream User);
    rpc CreateUser(CreateUserRequest) returns (User);
    rpc UpdateUser(UpdateUserRequest) returns (User);
    rpc SubscribeToUpdates(SubscribeRequest) returns (stream UserUpdate);
}

message User {
    int64 id = 1;
    string email = 2;
    string name = 3;
    int64 created_at = 4;
    repeated string roles = 5;
}

message GetUserRequest {
    int64 id = 1;
}

message ListUsersRequest {
    int32 page_size = 1;
    string page_token = 2;
    string filter = 3;
}

message CreateUserRequest {
    string email = 1;
    string name = 2;
    repeated string roles = 3;
}

message UpdateUserRequest {
    int64 id = 1;
    User user = 2;
    google.protobuf.FieldMask update_mask = 3;
}

message SubscribeRequest {
    repeated int64 user_ids = 1;
}

message UserUpdate {
    int64 user_id = 1;
    string event_type = 2;
    User user = 3;
    int64 timestamp = 4;
}
```

**Python - gRPC Server**

```python
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc
import asyncio

class UserService(user_pb2_grpc.UserServiceServicer):

    def __init__(self, db_pool):
        self.db = db_pool

    async def GetUser(self, request, context):
        try:
            user = await self.db.get_user(request.id)
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'User {request.id} not found')
                return user_pb2.User()

            return user_pb2.User(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=int(user.created_at.timestamp()),
                roles=user.roles
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_pb2.User()

    async def ListUsers(self, request, context):
        """Server streaming - envía usuarios uno por uno"""
        try:
            async for user in self.db.stream_users(
                page_size=request.page_size,
                filter=request.filter
            ):
                yield user_pb2.User(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    created_at=int(user.created_at.timestamp()),
                    roles=user.roles
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))

    async def SubscribeToUpdates(self, request, context):
        """Bidirectional streaming"""
        queue = asyncio.Queue()

        async def on_user_update(user_id, event_type, user_data):
            if user_id in request.user_ids:
                await queue.put(user_pb2.UserUpdate(
                    user_id=user_id,
                    event_type=event_type,
                    user=user_data,
                    timestamp=int(time.time())
                ))

        self.db.subscribe(on_user_update)

        try:
            while True:
                update = await queue.get()
                yield update
        finally:
            self.db.unsubscribe(on_user_update)

# Server setup con interceptores
class AuthInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)

        token = metadata.get('authorization', '')
        if not token.startswith('Bearer '):
            return grpc.aio.unary_unary_rpc_method_handler(
                lambda req, ctx: self._abort(ctx, grpc.StatusCode.UNAUTHENTICATED)
            )

        try:
            user = await verify_token(token[7:])
            handler_call_details.invocation_metadata.append(('user-id', str(user.id)))
        except:
            return grpc.aio.unary_unary_rpc_method_handler(
                lambda req, ctx: self._abort(ctx, grpc.StatusCode.UNAUTHENTICATED)
            )

        return await continuation(handler_call_details)

    def _abort(self, context, code):
        context.set_code(code)
        context.set_details('Authentication failed')
        return None

async def serve():
    interceptors = [AuthInterceptor()]
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors,
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),
            ('grpc.keepalive_time_ms', 10000),
            ('grpc.keepalive_timeout_ms', 5000),
        ]
    )

    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(db_pool),
        server
    )

    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
```

**Python - gRPC Client con retry y load balancing**

```python
import grpc
from grpc_retry import RetryConfig

class UserClient:
    def __init__(self, service_urls):
        self.channels = []

        for url in service_urls:
            channel = grpc.aio.insecure_channel(
                url,
                options=[
                    ('grpc.lb_policy_name', 'round_robin'),
                    ('grpc.keepalive_time_ms', 10000),
                    ('grpc.initial_reconnect_backoff_ms', 1000),
                    ('grpc.max_reconnect_backoff_ms', 30000),
                ]
            )
            self.channels.append(channel)

        self.stub = user_pb2_grpc.UserServiceStub(self.channels[0])

    async def get_user(self, user_id: int, token: str):
        metadata = [('authorization', f'Bearer {token}')]

        retry_config = RetryConfig(
            max_attempts=3,
            initial_backoff_ms=100,
            max_backoff_ms=1000,
            backoff_multiplier=2,
            retryable_status_codes=[grpc.StatusCode.UNAVAILABLE]
        )

        try:
            response = await self.stub.GetUser(
                user_pb2.GetUserRequest(id=user_id),
                metadata=metadata,
                timeout=5.0
            )
            return response
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise

    async def subscribe_to_updates(self, user_ids, token):
        metadata = [('authorization', f'Bearer {token}')]

        async for update in self.stub.SubscribeToUpdates(
            user_pb2.SubscribeRequest(user_ids=user_ids),
            metadata=metadata
        ):
            yield update

    async def close(self):
        for channel in self.channels:
            await channel.close()

# Uso
async def main():
    client = UserClient(['localhost:50051', 'localhost:50052'])

    try:
        user = await client.get_user(123, 'my-token')
        print(f"User: {user.name}")

        async for update in client.subscribe_to_updates([123, 456], 'my-token'):
            print(f"Update: {update.event_type} for user {update.user_id}")
    finally:
        await client.close()
```

**Go - gRPC Server con middleware**

```go
package main

import (
    "context"
    "log"
    "net"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/metadata"
    "google.golang.org/grpc/status"
    pb "myapp/proto/user"
)

type userServer struct {
    pb.UnimplementedUserServiceServer
    db Database
}

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    user, err := s.db.GetUser(ctx, req.Id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, status.Error(codes.NotFound, "user not found")
        }
        return nil, status.Error(codes.Internal, err.Error())
    }

    return &pb.User{
        Id:        user.ID,
        Email:     user.Email,
        Name:      user.Name,
        CreatedAt: user.CreatedAt.Unix(),
        Roles:     user.Roles,
    }, nil
}

func (s *userServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
    ctx := stream.Context()

    users, err := s.db.ListUsers(ctx, req.PageSize, req.Filter)
    if err != nil {
        return status.Error(codes.Internal, err.Error())
    }

    for _, user := range users {
        if err := stream.Send(&pb.User{
            Id:        user.ID,
            Email:     user.Email,
            Name:      user.Name,
            CreatedAt: user.CreatedAt.Unix(),
            Roles:     user.Roles,
        }); err != nil {
            return err
        }
    }

    return nil
}

// Middleware de autenticación
func authInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    md, ok := metadata.FromIncomingContext(ctx)
    if !ok {
        return nil, status.Error(codes.Unauthenticated, "missing metadata")
    }

    tokens := md.Get("authorization")
    if len(tokens) == 0 {
        return nil, status.Error(codes.Unauthenticated, "missing token")
    }

    token := tokens[0]
    userID, err := verifyToken(token)
    if err != nil {
        return nil, status.Error(codes.Unauthenticated, "invalid token")
    }

    // Agregar user ID al context
    ctx = context.WithValue(ctx, "user_id", userID)

    return handler(ctx, req)
}

// Middleware de logging
func loggingInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    start := time.Now()

    resp, err := handler(ctx, req)

    duration := time.Since(start)
    log.Printf("Method: %s, Duration: %v, Error: %v", info.FullMethod, duration, err)

    return resp, err
}

// Rate limiting interceptor
func rateLimitInterceptor(limiter *rate.Limiter) grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
        if !limiter.Allow() {
            return nil, status.Error(codes.ResourceExhausted, "rate limit exceeded")
        }
        return handler(ctx, req)
    }
}

func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }

    limiter := rate.NewLimiter(100, 200)

    s := grpc.NewServer(
        grpc.ChainUnaryInterceptor(
            rateLimitInterceptor(limiter),
            loggingInterceptor,
            authInterceptor,
        ),
        grpc.MaxRecvMsgSize(50*1024*1024),
        grpc.MaxSendMsgSize(50*1024*1024),
        grpc.KeepaliveParams(keepalive.ServerParameters{
            Time:    10 * time.Second,
            Timeout: 5 * time.Second,
        }),
    )

    pb.RegisterUserServiceServer(s, &userServer{db: db})

    log.Printf("Server listening on %v", lis.Addr())
    if err := s.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
```

---

### 1.2 Circuit Breaker Pattern
**Dificultad:** ⭐⭐⭐⭐⭐

**Python - Circuit Breaker con estados**

```python
import asyncio
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any
import time

class CircuitState(Enum):
    CLOSED = "closed"        # Normal operation
    OPEN = "open"            # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception,
        name: str = None
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.name = name or "CircuitBreaker"

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._lock = asyncio.Lock()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        async with self._lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    print(f"{self.name}: Attempting reset (HALF_OPEN)")
                else:
                    raise CircuitBreakerError(f"{self.name} is OPEN")

        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result

        except self.expected_exception as e:
            await self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        if not self.last_failure_time:
            return True
        return (datetime.now() - self.last_failure_time).seconds >= self.recovery_timeout

    async def _on_success(self):
        async with self._lock:
            self.failure_count = 0
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                print(f"{self.name}: Recovery successful (CLOSED)")

    async def _on_failure(self):
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
                print(f"{self.name}: Recovery failed (OPEN)")
            elif self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                print(f"{self.name}: Threshold reached (OPEN)")

class CircuitBreakerError(Exception):
    pass

# Uso con decorador
from functools import wraps

def circuit_breaker(
    failure_threshold=5,
    recovery_timeout=60,
    expected_exception=Exception
):
    breaker = CircuitBreaker(
        failure_threshold=failure_threshold,
        recovery_timeout=recovery_timeout,
        expected_exception=expected_exception
    )

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator

# Ejemplo de uso
import httpx

@circuit_breaker(
    failure_threshold=3,
    recovery_timeout=30,
    expected_exception=httpx.HTTPError
)
async def call_external_api(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5.0)
        response.raise_for_status()
        return response.json()

# Uso con fallback
async def get_user_data(user_id: int):
    try:
        return await call_external_api(f"https://api.example.com/users/{user_id}")
    except CircuitBreakerError:
        # Fallback a caché o respuesta default
        return await get_cached_user_data(user_id)
    except httpx.HTTPError as e:
        # Servicio respondió pero con error
        raise
```

**Go - Circuit Breaker con métricas**

```go
package circuitbreaker

import (
    "context"
    "errors"
    "sync"
    "time"
)

type State int

const (
    StateClosed State = iota
    StateOpen
    StateHalfOpen
)

type CircuitBreaker struct {
    name             string
    maxFailures      uint32
    timeout          time.Duration

    mu               sync.Mutex
    state            State
    failures         uint32
    lastFailureTime  time.Time
    lastSuccessTime  time.Time

    // Métricas
    totalRequests    uint64
    totalSuccesses   uint64
    totalFailures    uint64
    totalRejections  uint64
}

func New(name string, maxFailures uint32, timeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{
        name:        name,
        maxFailures: maxFailures,
        timeout:     timeout,
        state:       StateClosed,
    }
}

var ErrCircuitOpen = errors.New("circuit breaker is open")

func (cb *CircuitBreaker) Execute(fn func() error) error {
    cb.mu.Lock()

    cb.totalRequests++

    if cb.state == StateOpen {
        if time.Since(cb.lastFailureTime) > cb.timeout {
            cb.state = StateHalfOpen
            cb.failures = 0
            log.Printf("[%s] Circuit breaker entering HALF_OPEN state", cb.name)
        } else {
            cb.totalRejections++
            cb.mu.Unlock()
            return ErrCircuitOpen
        }
    }

    cb.mu.Unlock()

    err := fn()

    cb.mu.Lock()
    defer cb.mu.Unlock()

    if err != nil {
        cb.onFailure()
        return err
    }

    cb.onSuccess()
    return nil
}

func (cb *CircuitBreaker) onSuccess() {
    cb.totalSuccesses++
    cb.lastSuccessTime = time.Now()

    if cb.state == StateHalfOpen {
        cb.state = StateClosed
        cb.failures = 0
        log.Printf("[%s] Circuit breaker recovered (CLOSED)", cb.name)
    }
}

func (cb *CircuitBreaker) onFailure() {
    cb.totalFailures++
    cb.failures++
    cb.lastFailureTime = time.Now()

    if cb.state == StateHalfOpen {
        cb.state = StateOpen
        log.Printf("[%s] Circuit breaker failed recovery (OPEN)", cb.name)
        return
    }

    if cb.failures >= cb.maxFailures {
        cb.state = StateOpen
        log.Printf("[%s] Circuit breaker opened after %d failures", cb.name, cb.failures)
    }
}

func (cb *CircuitBreaker) GetMetrics() map[string]interface{} {
    cb.mu.Lock()
    defer cb.mu.Unlock()

    successRate := float64(0)
    if cb.totalRequests > 0 {
        successRate = float64(cb.totalSuccesses) / float64(cb.totalRequests) * 100
    }

    return map[string]interface{}{
        "name":            cb.name,
        "state":           cb.state.String(),
        "failures":        cb.failures,
        "total_requests":  cb.totalRequests,
        "total_successes": cb.totalSuccesses,
        "total_failures":  cb.totalFailures,
        "total_rejections": cb.totalRejections,
        "success_rate":    successRate,
    }
}

func (s State) String() string {
    switch s {
    case StateClosed:
        return "CLOSED"
    case StateOpen:
        return "OPEN"
    case StateHalfOpen:
        return "HALF_OPEN"
    default:
        return "UNKNOWN"
    }
}

// Uso
func main() {
    cb := New("payment-service", 5, 30*time.Second)

    err := cb.Execute(func() error {
        return callPaymentService()
    })

    if err != nil {
        if errors.Is(err, ErrCircuitOpen) {
            // Usar fallback
            return handlePaymentFallback()
        }
        return err
    }
}
```

---

## CATEGORÍA 2: Caching Strategies

### 2.1 Multi-Level Cache
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from typing import Optional, Any
from abc import ABC, abstractmethod
import asyncio
import redis.asyncio as redis
from functools import wraps
import hashlib
import json

class CacheLayer(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = None):
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass

# L1: In-memory cache (LRU)
class MemoryCache(CacheLayer):
    def __init__(self, max_size: int = 1000):
        from collections import OrderedDict
        self.cache = OrderedDict()
        self.max_size = max_size
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return self.cache[key]['value']
            return None

    async def set(self, key: str, value: Any, ttl: int = None):
        async with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)

            self.cache[key] = {
                'value': value,
                'ttl': ttl,
                'set_at': asyncio.get_event_loop().time()
            }

            # Evict oldest if full
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

    async def delete(self, key: str):
        async with self.lock:
            self.cache.pop(key, None)

# L2: Redis cache
class RedisCache(CacheLayer):
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = None):
        serialized = json.dumps(value)
        if ttl:
            await self.redis.setex(key, ttl, serialized)
        else:
            await self.redis.set(key, serialized)

    async def delete(self, key: str):
        await self.redis.delete(key)

# Multi-level cache manager
class MultiLevelCache:
    def __init__(self, layers: list[CacheLayer]):
        self.layers = layers

    async def get(self, key: str) -> Optional[Any]:
        # Try each layer in order
        for i, layer in enumerate(self.layers):
            value = await layer.get(key)
            if value is not None:
                # Backfill previous layers
                await self._backfill(key, value, i)
                return value
        return None

    async def set(self, key: str, value: Any, ttl: int = None):
        # Set in all layers
        await asyncio.gather(*[
            layer.set(key, value, ttl)
            for layer in self.layers
        ])

    async def delete(self, key: str):
        # Delete from all layers
        await asyncio.gather(*[
            layer.delete(key)
            for layer in self.layers
        ])

    async def _backfill(self, key: str, value: Any, from_layer: int):
        # Backfill layers before the one that hit
        for layer in self.layers[:from_layer]:
            await layer.set(key, value)

# Cache-aside pattern con decorador
def cached(
    cache: MultiLevelCache,
    ttl: int = 3600,
    key_prefix: str = "",
    invalidate_on: list[str] = None
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _generate_cache_key(key_prefix, func.__name__, args, kwargs)

            # Try to get from cache
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            await cache.set(cache_key, result, ttl)

            return result

        wrapper._cache_key_prefix = key_prefix
        wrapper._invalidate_on = invalidate_on or []

        return wrapper
    return decorator

def _generate_cache_key(prefix: str, func_name: str, args: tuple, kwargs: dict) -> str:
    # Create deterministic key from arguments
    key_data = {
        'func': func_name,
        'args': args,
        'kwargs': sorted(kwargs.items())
    }
    serialized = json.dumps(key_data, sort_keys=True, default=str)
    hash_key = hashlib.md5(serialized.encode()).hexdigest()
    return f"{prefix}:{func_name}:{hash_key}"

# Invalidación de caché
class CacheInvalidator:
    def __init__(self, cache: MultiLevelCache):
        self.cache = cache
        self.patterns = {}

    def register_pattern(self, event: str, pattern: str):
        if event not in self.patterns:
            self.patterns[event] = []
        self.patterns[event].append(pattern)

    async def invalidate(self, event: str, **kwargs):
        if event not in self.patterns:
            return

        for pattern in self.patterns[event]:
            key = pattern.format(**kwargs)
            await self.cache.delete(key)

# Uso completo
cache = MultiLevelCache([
    MemoryCache(max_size=1000),
    RedisCache("redis://localhost:6379")
])

invalidator = CacheInvalidator(cache)
invalidator.register_pattern('user_updated', 'user:{user_id}')
invalidator.register_pattern('user_updated', 'user_list:*')

@cached(cache, ttl=3600, key_prefix="user")
async def get_user(user_id: int):
    # Expensive database query
    return await db.query(User).filter(User.id == user_id).first()

@cached(cache, ttl=300, key_prefix="user_list")
async def list_users(page: int = 1, page_size: int = 20):
    offset = (page - 1) * page_size
    return await db.query(User).offset(offset).limit(page_size).all()

async def update_user(user_id: int, data: dict):
    user = await db.query(User).filter(User.id == user_id).first()
    for key, value in data.items():
        setattr(user, key, value)
    await db.commit()

    # Invalidar caché
    await invalidator.invalidate('user_updated', user_id=user_id)

    return user
```

---

### 2.2 Write-Through vs Write-Behind Caching
**Dificultad:** ⭐⭐⭐⭐

```python
import asyncio
from collections import deque
from dataclasses import dataclass
from typing import Any
import time

# Write-Through: Escribe en caché y DB síncronamente
class WriteThroughCache:
    def __init__(self, cache: CacheLayer, db):
        self.cache = cache
        self.db = db

    async def get(self, key: str) -> Optional[Any]:
        # Try cache first
        value = await self.cache.get(key)
        if value is not None:
            return value

        # Cache miss - get from DB
        value = await self.db.get(key)
        if value is not None:
            await self.cache.set(key, value)

        return value

    async def set(self, key: str, value: Any):
        # Write to both cache and DB
        await asyncio.gather(
            self.cache.set(key, value),
            self.db.set(key, value)
        )

    # Garantía: Caché y DB siempre consistentes
    # Desventaja: Latencia más alta en escrituras

# Write-Behind (Write-Back): Escribe en caché inmediatamente, DB async
@dataclass
class WriteOperation:
    key: str
    value: Any
    timestamp: float
    operation: str  # 'set' or 'delete'

class WriteBehindCache:
    def __init__(
        self,
        cache: CacheLayer,
        db,
        batch_size: int = 100,
        flush_interval: float = 5.0
    ):
        self.cache = cache
        self.db = db
        self.batch_size = batch_size
        self.flush_interval = flush_interval

        self.write_queue = deque()
        self.lock = asyncio.Lock()
        self.flush_task = None

    async def start(self):
        self.flush_task = asyncio.create_task(self._flush_worker())

    async def stop(self):
        if self.flush_task:
            self.flush_task.cancel()
            await self._flush()  # Flush remaining writes

    async def get(self, key: str) -> Optional[Any]:
        value = await self.cache.get(key)
        if value is not None:
            return value

        value = await self.db.get(key)
        if value is not None:
            await self.cache.set(key, value)

        return value

    async def set(self, key: str, value: Any):
        # Write to cache immediately
        await self.cache.set(key, value)

        # Queue DB write
        async with self.lock:
            self.write_queue.append(WriteOperation(
                key=key,
                value=value,
                timestamp=time.time(),
                operation='set'
            ))

        # Flush if batch full
        if len(self.write_queue) >= self.batch_size:
            await self._flush()

    async def delete(self, key: str):
        await self.cache.delete(key)

        async with self.lock:
            self.write_queue.append(WriteOperation(
                key=key,
                value=None,
                timestamp=time.time(),
                operation='delete'
            ))

    async def _flush_worker(self):
        while True:
            try:
                await asyncio.sleep(self.flush_interval)
                await self._flush()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Flush error: {e}")

    async def _flush(self):
        async with self.lock:
            if not self.write_queue:
                return

            operations = list(self.write_queue)
            self.write_queue.clear()

        # Coalesce operations - keep only last operation per key
        final_ops = {}
        for op in operations:
            final_ops[op.key] = op

        # Batch write to DB
        try:
            sets = [(op.key, op.value) for op in final_ops.values() if op.operation == 'set']
            deletes = [op.key for op in final_ops.values() if op.operation == 'delete']

            await asyncio.gather(
                self.db.batch_set(sets) if sets else asyncio.sleep(0),
                self.db.batch_delete(deletes) if deletes else asyncio.sleep(0)
            )

            print(f"Flushed {len(final_ops)} operations to DB")

        except Exception as e:
            # Rollback - put operations back in queue
            async with self.lock:
                self.write_queue.extendleft(reversed(list(final_ops.values())))
            raise

    # Ventajas: Baja latencia en escrituras, batch writes
    # Desventajas: Posible pérdida de datos si falla antes de flush

# Cache-Aside con Refresh-Ahead
class RefreshAheadCache:
    def __init__(self, cache: CacheLayer, db, ttl: int = 3600, refresh_threshold: float = 0.8):
        self.cache = cache
        self.db = db
        self.ttl = ttl
        self.refresh_threshold = refresh_threshold
        self.refresh_tasks = {}

    async def get(self, key: str) -> Optional[Any]:
        entry = await self.cache.get(key)

        if entry is not None:
            # Check if needs refresh
            age = time.time() - entry['set_at']
            if age > self.ttl * self.refresh_threshold:
                # Asynchronously refresh
                if key not in self.refresh_tasks:
                    self.refresh_tasks[key] = asyncio.create_task(
                        self._refresh(key)
                    )

            return entry['value']

        # Cache miss
        value = await self.db.get(key)
        if value is not None:
            await self._set_with_metadata(key, value)

        return value

    async def _refresh(self, key: str):
        try:
            value = await self.db.get(key)
            if value is not None:
                await self._set_with_metadata(key, value)
        finally:
            self.refresh_tasks.pop(key, None)

    async def _set_with_metadata(self, key: str, value: Any):
        entry = {
            'value': value,
            'set_at': time.time()
        }
        await self.cache.set(key, entry, self.ttl)
```

---

## CATEGORÍA 3: Message Queues y Event-Driven

### 3.1 RabbitMQ Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

```python
import aio_pika
import asyncio
import json
from typing import Callable
from dataclasses import dataclass

@dataclass
class MessageConfig:
    exchange: str
    exchange_type: str = 'topic'
    routing_key: str = ''
    durable: bool = True
    auto_delete: bool = False

class RabbitMQProducer:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None
        self.exchanges = {}

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            self.amqp_url,
            heartbeat=60
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

    async def declare_exchange(self, config: MessageConfig):
        if config.exchange not in self.exchanges:
            self.exchanges[config.exchange] = await self.channel.declare_exchange(
                config.exchange,
                type=aio_pika.ExchangeType(config.exchange_type),
                durable=config.durable,
                auto_delete=config.auto_delete
            )

    async def publish(
        self,
        message: dict,
        config: MessageConfig,
        priority: int = 0,
        expiration: int = None
    ):
        await self.declare_exchange(config)

        exchange = self.exchanges[config.exchange]

        message_body = json.dumps(message).encode()

        await exchange.publish(
            aio_pika.Message(
                body=message_body,
                content_type='application/json',
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                priority=priority,
                expiration=expiration
            ),
            routing_key=config.routing_key
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

class RabbitMQConsumer:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None
        self.handlers = {}

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            self.amqp_url,
            heartbeat=60
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

    async def consume(
        self,
        queue_name: str,
        handler: Callable,
        exchange: str = '',
        routing_keys: list = None,
        exchange_type: str = 'topic',
        prefetch_count: int = 10
    ):
        # Declare exchange
        if exchange:
            ex = await self.channel.declare_exchange(
                exchange,
                type=aio_pika.ExchangeType(exchange_type),
                durable=True
            )

        # Declare queue
        queue = await self.channel.declare_queue(
            queue_name,
            durable=True,
            arguments={
                'x-max-priority': 10,
                'x-message-ttl': 86400000  # 24 hours
            }
        )

        # Bind queue to exchange with routing keys
        if exchange and routing_keys:
            for routing_key in routing_keys:
                await queue.bind(ex, routing_key=routing_key)

        # Start consuming
        await queue.consume(
            lambda message: self._handle_message(message, handler)
        )

    async def _handle_message(self, message: aio_pika.IncomingMessage, handler: Callable):
        async with message.process(requeue=True):
            try:
                body = json.loads(message.body.decode())

                # Log message received
                print(f"Processing message: {message.routing_key}")

                # Execute handler
                await handler(body)

                # Auto-ack on success
                print(f"Message processed successfully")

            except Exception as e:
                print(f"Error processing message: {e}")

                # Check retry count
                retry_count = message.headers.get('x-retry-count', 0) if message.headers else 0

                if retry_count < 3:
                    # Requeue with delay (dead letter exchange)
                    await self._retry_message(message, retry_count + 1)
                else:
                    # Move to dead letter queue
                    await self._send_to_dlq(message)

                raise  # Requeue

    async def _retry_message(self, message: aio_pika.IncomingMessage, retry_count: int):
        # Publish to retry exchange with delay
        delay_seconds = min(2 ** retry_count * 10, 3600)  # Exponential backoff, max 1h

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.body,
                headers={'x-retry-count': retry_count},
                expiration=delay_seconds * 1000
            ),
            routing_key=f"{message.routing_key}.retry"
        )

    async def _send_to_dlq(self, message: aio_pika.IncomingMessage):
        dlq = await self.channel.declare_queue('dead_letter_queue', durable=True)

        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message.body,
                headers={
                    'x-original-routing-key': message.routing_key,
                    'x-death-reason': 'max-retries-exceeded'
                }
            ),
            routing_key='dead_letter_queue'
        )

    async def close(self):
        if self.connection:
            await self.connection.close()

# Uso: Work Queue Pattern
async def worker_example():
    consumer = RabbitMQConsumer('amqp://guest:guest@localhost/')
    await consumer.connect()

    async def process_task(message):
        task_id = message['task_id']
        print(f"Processing task {task_id}")
        await asyncio.sleep(2)  # Simulate work
        print(f"Task {task_id} completed")

    await consumer.consume(
        queue_name='tasks',
        handler=process_task,
        prefetch_count=5
    )

    # Keep running
    await asyncio.Future()

# Uso: Pub/Sub Pattern
async def pubsub_example():
    consumer = RabbitMQConsumer('amqp://guest:guest@localhost/')
    await consumer.connect()

    async def handle_user_event(message):
        event_type = message['event_type']
        user_id = message['user_id']
        print(f"User event: {event_type} for user {user_id}")

    await consumer.consume(
        queue_name='email_service_queue',
        handler=handle_user_event,
        exchange='user_events',
        exchange_type='fanout'
    )

    await asyncio.Future()

# Uso: Topic Exchange Pattern
async def topic_example():
    consumer = RabbitMQConsumer('amqp://guest:guest@localhost/')
    await consumer.connect()

    async def handle_order_event(message):
        print(f"Order event: {message}")

    # Subscribe to specific topics
    await consumer.consume(
        queue_name='payment_processor',
        handler=handle_order_event,
        exchange='orders',
        exchange_type='topic',
        routing_keys=['order.created', 'order.paid']
    )

    await asyncio.Future()
```

---

Continúa con más categorías...

---

## Resumen de Prioridades Backend Avanzado

| Tema | Dificultad | Criticidad | Impacto | Prioridad |
|------|------------|------------|---------|-----------|
| gRPC & Service Communication | 5 | 5 | 5 | **CRÍTICA** |
| Circuit Breaker | 5 | 5 | 5 | **CRÍTICA** |
| Multi-Level Caching | 5 | 4 | 5 | **CRÍTICA** |
| Message Queues | 5 | 5 | 4 | **CRÍTICA** |
| Write-Behind Caching | 4 | 3 | 4 | **ALTA** |
| RabbitMQ Patterns | 5 | 4 | 4 | **ALTA** |

**Siguiente archivo continuará con:**
- Distributed Tracing (OpenTelemetry, Jaeger)
- API Versioning & Deprecation
- WebSockets & Server-Sent Events
- GraphQL Federation
- Distributed Transactions (Saga Pattern)
- Security: OAuth2, JWT, API Keys
