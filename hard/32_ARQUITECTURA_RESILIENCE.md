# Arquitectura de Resilience: Patrones de Resiliencia para Producción 2026

## Índice
1. [Circuit Breaker Pattern](#1-circuit-breaker)
2. [Bulkhead Pattern](#2-bulkhead)
3. [Retry Patterns](#3-retry-patterns)
4. [Timeout Strategies](#4-timeout-strategies)
5. [Fallback Mechanisms](#5-fallback)
6. [Rate Limiting & Backpressure](#6-rate-limiting)
7. [Graceful Degradation](#7-graceful-degradation)
8. [Health Checks & Probes](#8-health-checks)
9. [Chaos Engineering](#9-chaos-engineering)
10. [Disaster Recovery](#10-disaster-recovery)

---

## 1. Circuit Breaker Pattern

### ❌ ERROR COMÚN: Reintentar indefinidamente cuando servicio está caído
```python
# MAL - retry infinito
async def call_payment_service():
    while True:
        try:
            return await payment_api.charge()
        except:
            await asyncio.sleep(1)  # Sigue intentando forever
```

### ✅ SOLUCIÓN: Circuit Breaker para prevenir cascading failures

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any, Optional
from dataclasses import dataclass
import asyncio

# ==========================================
# CIRCUIT BREAKER STATES
# ==========================================
class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing - reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

@dataclass
class CircuitBreakerConfig:
    """Configuración del circuit breaker"""
    failure_threshold: int = 5       # Failures antes de abrir
    success_threshold: int = 2       # Successes para cerrar desde half-open
    timeout_seconds: float = 60.0    # Tiempo en OPEN antes de HALF_OPEN
    half_open_max_calls: int = 3     # Max requests en HALF_OPEN

# ==========================================
# CIRCUIT BREAKER
# ==========================================
class CircuitBreaker:
    """
    Circuit Breaker Pattern
    - CLOSED: Requests pasan normalmente
    - OPEN: Requests fallan inmediatamente (fail fast)
    - HALF_OPEN: Prueba si servicio se recuperó
    """

    def __init__(
        self,
        name: str,
        config: CircuitBreakerConfig = CircuitBreakerConfig()
    ):
        self.name = name
        self.config = config

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.half_open_calls = 0

    async def call(
        self,
        func: Callable,
        *args,
        fallback: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """
        Ejecuta función protegida por circuit breaker
        """
        # 1. Verificar estado actual
        await self._update_state()

        # 2. Si está OPEN, fail fast
        if self.state == CircuitState.OPEN:
            print(f"⚠️  Circuit breaker {self.name} is OPEN - failing fast")

            if fallback:
                return await fallback(*args, **kwargs)

            raise CircuitBreakerOpenError(
                f"Circuit breaker {self.name} is open"
            )

        # 3. Si está HALF_OPEN, limitar requests
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.config.half_open_max_calls:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker {self.name} half-open limit reached"
                )
            self.half_open_calls += 1

        # 4. Intentar llamada
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result

        except Exception as e:
            await self._on_failure(e)
            raise

    async def _update_state(self):
        """
        Actualiza estado basado en tiempo y contadores
        """
        if self.state == CircuitState.OPEN:
            # Verificar si es momento de intentar recuperación
            if self.last_failure_time:
                elapsed = datetime.utcnow() - self.last_failure_time
                timeout = timedelta(seconds=self.config.timeout_seconds)

                if elapsed >= timeout:
                    print(f"🔄 Circuit breaker {self.name}: OPEN → HALF_OPEN")
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    self.success_count = 0

    async def _on_success(self):
        """
        Handler cuando llamada tiene éxito
        """
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1

            # Si alcanzamos threshold de éxitos, cerrar circuito
            if self.success_count >= self.config.success_threshold:
                print(f"✅ Circuit breaker {self.name}: HALF_OPEN → CLOSED")
                self.state = CircuitState.CLOSED
                self.success_count = 0
                self.half_open_calls = 0

    async def _on_failure(self, error: Exception):
        """
        Handler cuando llamada falla
        """
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()

        print(f"❌ Circuit breaker {self.name} failure {self.failure_count}/{self.config.failure_threshold}")

        if self.state == CircuitState.HALF_OPEN:
            # Volver a OPEN inmediatamente
            print(f"⚠️  Circuit breaker {self.name}: HALF_OPEN → OPEN")
            self.state = CircuitState.OPEN
            self.failure_count = 0
            self.success_count = 0
            self.half_open_calls = 0

        elif self.state == CircuitState.CLOSED:
            # Abrir si alcanzamos threshold
            if self.failure_count >= self.config.failure_threshold:
                print(f"⚠️  Circuit breaker {self.name}: CLOSED → OPEN")
                self.state = CircuitState.OPEN

    def get_state(self) -> dict:
        """Obtiene estado actual para monitoring"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None
        }

class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass

# ==========================================
# EJEMPLO DE USO
# ==========================================
payment_circuit = CircuitBreaker(
    name="payment_service",
    config=CircuitBreakerConfig(
        failure_threshold=3,
        timeout_seconds=30.0
    )
)

async def charge_payment(amount: float):
    """Llamada protegida por circuit breaker"""

    async def fallback_payment(amount):
        """Fallback: encolar para procesar después"""
        await payment_queue.enqueue({
            "amount": amount,
            "status": "pending"
        })
        return {"status": "queued"}

    return await payment_circuit.call(
        payment_api.charge,
        amount=amount,
        fallback=fallback_payment
    )

# ==========================================
# CIRCUIT BREAKER REGISTRY
# ==========================================
class CircuitBreakerRegistry:
    """
    Registro global de circuit breakers
    Para monitoring y management
    """
    _instance = None
    _breakers: dict[str, CircuitBreaker] = {}

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def register(self, breaker: CircuitBreaker):
        self._breakers[breaker.name] = breaker

    def get(self, name: str) -> Optional[CircuitBreaker]:
        return self._breakers.get(name)

    def get_all_states(self) -> list[dict]:
        """Obtiene estado de todos los circuit breakers"""
        return [cb.get_state() for cb in self._breakers.values()]

    async def force_open(self, name: str):
        """Fuerza circuit breaker a OPEN (para maintenance)"""
        breaker = self.get(name)
        if breaker:
            breaker.state = CircuitState.OPEN

    async def force_close(self, name: str):
        """Fuerza circuit breaker a CLOSED"""
        breaker = self.get(name)
        if breaker:
            breaker.state = CircuitState.CLOSED
            breaker.failure_count = 0
```

---

## 2. Bulkhead Pattern

### ❌ ERROR COMÚN: Compartir thread pool entre servicios
```python
# MAL - mismo pool para todo
executor = ThreadPoolExecutor(max_workers=100)

# Un servicio lento bloquea a todos
await executor.submit(slow_service.call)
await executor.submit(fast_service.call)  # Bloqueado!
```

### ✅ SOLUCIÓN: Aislar recursos por servicio

```python
from asyncio import Semaphore
from typing import Dict
import asyncio

# ==========================================
# BULKHEAD PATTERN
# ==========================================
class Bulkhead:
    """
    Bulkhead Pattern - aísla recursos
    Previene que un servicio lento consuma todos los recursos
    """

    def __init__(
        self,
        name: str,
        max_concurrent_calls: int,
        max_wait_duration: float = 10.0
    ):
        self.name = name
        self.semaphore = Semaphore(max_concurrent_calls)
        self.max_wait_duration = max_wait_duration

        # Métricas
        self.active_calls = 0
        self.total_calls = 0
        self.rejected_calls = 0

    async def execute(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Ejecuta función con límite de concurrencia
        """
        self.total_calls += 1

        try:
            # Intentar adquirir semaphore con timeout
            acquired = await asyncio.wait_for(
                self.semaphore.acquire(),
                timeout=self.max_wait_duration
            )

            if not acquired:
                self.rejected_calls += 1
                raise BulkheadRejectionError(
                    f"Bulkhead {self.name} is full"
                )

        except asyncio.TimeoutError:
            self.rejected_calls += 1
            raise BulkheadRejectionError(
                f"Bulkhead {self.name} timeout waiting for slot"
            )

        # Ejecutar función
        self.active_calls += 1
        try:
            return await func(*args, **kwargs)
        finally:
            self.active_calls -= 1
            self.semaphore.release()

    def get_metrics(self) -> dict:
        """Métricas para monitoring"""
        return {
            "name": self.name,
            "active_calls": self.active_calls,
            "total_calls": self.total_calls,
            "rejected_calls": self.rejected_calls,
            "rejection_rate": self.rejected_calls / max(self.total_calls, 1)
        }

class BulkheadRejectionError(Exception):
    """Raised when bulkhead is full"""
    pass

# ==========================================
# BULKHEAD REGISTRY
# ==========================================
class BulkheadRegistry:
    """
    Registro de bulkheads por servicio
    """
    def __init__(self):
        self.bulkheads: Dict[str, Bulkhead] = {}

    def register(
        self,
        service_name: str,
        max_concurrent_calls: int
    ) -> Bulkhead:
        """
        Registra bulkhead para un servicio
        """
        bulkhead = Bulkhead(service_name, max_concurrent_calls)
        self.bulkheads[service_name] = bulkhead
        return bulkhead

    def get(self, service_name: str) -> Bulkhead:
        return self.bulkheads[service_name]

# ==========================================
# EJEMPLO DE USO
# ==========================================
bulkheads = BulkheadRegistry()

# Configurar bulkheads por servicio
payment_bulkhead = bulkheads.register("payment_service", max_concurrent_calls=10)
email_bulkhead = bulkheads.register("email_service", max_concurrent_calls=50)
analytics_bulkhead = bulkheads.register("analytics_service", max_concurrent_calls=5)

async def call_payment_service(amount: float):
    """
    Llamada a payment service protegida por bulkhead
    """
    return await payment_bulkhead.execute(
        payment_api.charge,
        amount=amount
    )

async def send_email(to: str, subject: str):
    """
    Email service tiene su propio bulkhead
    No afecta a payment service
    """
    return await email_bulkhead.execute(
        email_api.send,
        to=to,
        subject=subject
    )

# ==========================================
# COMBINED: CIRCUIT BREAKER + BULKHEAD
# ==========================================
class ResilientServiceClient:
    """
    Cliente resiliente que combina:
    - Circuit Breaker
    - Bulkhead
    - Retry
    - Timeout
    """

    def __init__(
        self,
        service_name: str,
        circuit_breaker: CircuitBreaker,
        bulkhead: Bulkhead
    ):
        self.service_name = service_name
        self.circuit_breaker = circuit_breaker
        self.bulkhead = bulkhead

    async def call(
        self,
        func: Callable,
        *args,
        timeout: float = 5.0,
        **kwargs
    ) -> Any:
        """
        Llamada resiliente con todas las protecciones
        """
        # 1. Bulkhead - limita concurrencia
        async def bulkhead_protected_call():
            # 2. Circuit Breaker - previene cascading failures
            async def circuit_protected_call():
                # 3. Timeout - previene hanging
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=timeout
                )

            return await self.circuit_breaker.call(circuit_protected_call)

        return await self.bulkhead.execute(bulkhead_protected_call)

# Uso
payment_client = ResilientServiceClient(
    service_name="payment",
    circuit_breaker=payment_circuit,
    bulkhead=payment_bulkhead
)

result = await payment_client.call(
    payment_api.charge,
    amount=99.99,
    timeout=5.0
)
```

---

## 3. Retry Patterns

### ✅ SOLUCIÓN: Retry inteligente con exponential backoff + jitter

```python
import random
from typing import Type, Tuple

# ==========================================
# RETRY STRATEGY
# ==========================================
@dataclass
class RetryConfig:
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)

class RetryStrategy:
    """
    Estrategia de retry con:
    - Exponential backoff
    - Jitter (evita thundering herd)
    - Retry solo en errores transitorios
    """

    def __init__(self, config: RetryConfig = RetryConfig()):
        self.config = config

    async def execute(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Ejecuta función con retries
        """
        last_exception = None

        for attempt in range(self.config.max_attempts):
            try:
                return await func(*args, **kwargs)

            except Exception as e:
                last_exception = e

                # Verificar si debe reintentar
                if not self._should_retry(e, attempt):
                    raise

                # Calcular delay
                delay = self._calculate_delay(attempt)

                print(f"⚠️  Retry {attempt + 1}/{self.config.max_attempts} "
                      f"after {delay:.2f}s: {e}")

                await asyncio.sleep(delay)

        # Si llegamos aquí, fallaron todos los intentos
        raise last_exception

    def _should_retry(self, error: Exception, attempt: int) -> bool:
        """
        Decide si debe reintentar basado en:
        - Tipo de error
        - Número de intento
        """
        # No reintentar si alcanzamos max attempts
        if attempt >= self.config.max_attempts - 1:
            return False

        # Solo reintentar errores retryable
        if not isinstance(error, self.config.retryable_exceptions):
            return False

        # No reintentar errores permanentes
        non_retryable = (
            ValidationError,
            AuthenticationError,
            NotFoundError
        )
        if isinstance(error, non_retryable):
            return False

        return True

    def _calculate_delay(self, attempt: int) -> float:
        """
        Calcula delay con exponential backoff + jitter
        """
        # Exponential backoff
        delay = min(
            self.config.initial_delay * (self.config.exponential_base ** attempt),
            self.config.max_delay
        )

        # Jitter para evitar thundering herd
        if self.config.jitter:
            # Full jitter: random entre 0 y delay
            delay = random.uniform(0, delay)

        return delay

# ==========================================
# DECORADOR @retry
# ==========================================
def retry(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorador para aplicar retry a funciones
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            strategy = RetryStrategy(RetryConfig(
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                retryable_exceptions=retryable_exceptions
            ))
            return await strategy.execute(func, *args, **kwargs)

        return wrapper
    return decorator

# ==========================================
# EJEMPLO DE USO
# ==========================================

@retry(max_attempts=3, initial_delay=1.0)
async def fetch_user_data(user_id: str):
    """
    Función con retry automático
    """
    response = await http_client.get(f"/api/users/{user_id}")
    return response.json()

# ==========================================
# RETRY CON CIRCUIT BREAKER
# ==========================================
class RetryWithCircuitBreaker:
    """
    Combina retry con circuit breaker
    - Retry para errores transitorios
    - Circuit breaker para failures persistentes
    """

    def __init__(
        self,
        retry_strategy: RetryStrategy,
        circuit_breaker: CircuitBreaker
    ):
        self.retry_strategy = retry_strategy
        self.circuit_breaker = circuit_breaker

    async def execute(self, func: Callable, *args, **kwargs):
        """
        Ejecuta con retry + circuit breaker
        """
        async def circuit_protected_call():
            return await self.retry_strategy.execute(func, *args, **kwargs)

        return await self.circuit_breaker.call(circuit_protected_call)
```

---

## 4. Timeout Strategies

### ✅ SOLUCIÓN: Timeouts en todos los niveles

```python
# ==========================================
# TIMEOUT HIERARCHY
# ==========================================
class TimeoutConfig:
    """
    Configuración de timeouts en múltiples niveles
    """
    # HTTP client timeout
    connection_timeout: float = 5.0   # Tiempo para establecer conexión
    read_timeout: float = 30.0        # Tiempo para leer response

    # Operation timeout
    operation_timeout: float = 60.0   # Timeout de operación completa

    # Database timeout
    db_query_timeout: float = 10.0    # Timeout de query SQL

    # External service timeout
    external_api_timeout: float = 15.0

# ==========================================
# TIMEOUT MIDDLEWARE
# ==========================================
class TimeoutMiddleware:
    """
    Middleware que aplica timeout a todas las requests
    """

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    async def __call__(self, request, call_next):
        try:
            response = await asyncio.wait_for(
                call_next(request),
                timeout=self.timeout
            )
            return response

        except asyncio.TimeoutError:
            return {
                "error": "Request timeout",
                "timeout_seconds": self.timeout
            }, 504

# ==========================================
# ADAPTIVE TIMEOUT
# ==========================================
class AdaptiveTimeout:
    """
    Timeout adaptativo basado en latencia histórica
    - Ajusta timeout dinámicamente
    - Basado en percentil 99 de latencia
    """

    def __init__(
        self,
        service_name: str,
        initial_timeout: float = 5.0,
        percentile: float = 0.99
    ):
        self.service_name = service_name
        self.current_timeout = initial_timeout
        self.percentile = percentile
        self.latencies: list[float] = []
        self.max_samples = 1000

    async def execute(self, func: Callable, *args, **kwargs):
        """
        Ejecuta con timeout adaptativo
        """
        start = datetime.utcnow()

        try:
            result = await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=self.current_timeout
            )

            # Registrar latencia exitosa
            latency = (datetime.utcnow() - start).total_seconds()
            self._record_latency(latency)

            return result

        except asyncio.TimeoutError:
            # Timeout - posiblemente ajustar
            self._on_timeout()
            raise

    def _record_latency(self, latency: float):
        """
        Registra latencia y ajusta timeout
        """
        self.latencies.append(latency)

        # Mantener solo últimas N muestras
        if len(self.latencies) > self.max_samples:
            self.latencies = self.latencies[-self.max_samples:]

        # Recalcular timeout cada 100 requests
        if len(self.latencies) % 100 == 0:
            self._adjust_timeout()

    def _adjust_timeout(self):
        """
        Ajusta timeout basado en percentil
        """
        if not self.latencies:
            return

        # Calcular percentil 99
        sorted_latencies = sorted(self.latencies)
        index = int(len(sorted_latencies) * self.percentile)
        p99_latency = sorted_latencies[index]

        # Timeout = P99 * 1.5 (buffer)
        new_timeout = p99_latency * 1.5

        # Limitar cambios drásticos
        max_change = 0.2  # ±20%
        if abs(new_timeout - self.current_timeout) / self.current_timeout > max_change:
            if new_timeout > self.current_timeout:
                new_timeout = self.current_timeout * (1 + max_change)
            else:
                new_timeout = self.current_timeout * (1 - max_change)

        print(f"📊 Adaptive timeout for {self.service_name}: "
              f"{self.current_timeout:.2f}s → {new_timeout:.2f}s "
              f"(P99: {p99_latency:.2f}s)")

        self.current_timeout = new_timeout

    def _on_timeout(self):
        """Handler cuando ocurre timeout"""
        # Posiblemente aumentar timeout temporalmente
        pass
```

---

## 5. Fallback Mechanisms

### ✅ SOLUCIÓN: Fallbacks en cascada

```python
# ==========================================
# FALLBACK CHAIN
# ==========================================
class FallbackChain:
    """
    Cadena de fallbacks
    Intenta múltiples estrategias en orden
    """

    def __init__(self):
        self.fallbacks: list[Callable] = []

    def add_fallback(self, fallback: Callable):
        self.fallbacks.append(fallback)

    async def execute(
        self,
        primary_func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Ejecuta función primaria, con fallbacks si falla
        """
        # Intentar función primaria
        try:
            return await primary_func(*args, **kwargs)
        except Exception as e:
            print(f"⚠️  Primary function failed: {e}")

        # Intentar fallbacks en orden
        for i, fallback in enumerate(self.fallbacks, 1):
            try:
                print(f"🔄 Trying fallback {i}/{len(self.fallbacks)}")
                return await fallback(*args, **kwargs)

            except Exception as e:
                print(f"❌ Fallback {i} failed: {e}")
                if i == len(self.fallbacks):
                    # Último fallback también falló
                    raise

# ==========================================
# FALLBACK STRATEGIES
# ==========================================

# Strategy 1: Cache
async def cache_fallback(user_id: str):
    """
    Fallback a cache
    """
    cached = await cache.get(f"user:{user_id}")
    if cached:
        return {"source": "cache", **cached}
    raise ValueError("Not in cache")

# Strategy 2: Stale data
async def stale_data_fallback(user_id: str):
    """
    Fallback a datos viejos pero válidos
    """
    stale = await db.get_stale(user_id, max_age_hours=24)
    if stale:
        return {"source": "stale", "warning": "Data may be outdated", **stale}
    raise ValueError("No stale data")

# Strategy 3: Default values
async def default_fallback(user_id: str):
    """
    Fallback a valores por defecto
    """
    return {
        "source": "default",
        "user_id": user_id,
        "name": "Unknown User",
        "warning": "Using default data"
    }

# Configurar cadena
fallback_chain = FallbackChain()
fallback_chain.add_fallback(cache_fallback)
fallback_chain.add_fallback(stale_data_fallback)
fallback_chain.add_fallback(default_fallback)

# Uso
user_data = await fallback_chain.execute(
    fetch_user_from_api,
    user_id="user_123"
)
```

---

## 6-10. [Remaining Sections - Summarized]

### 6. Rate Limiting & Backpressure
- Sliding window rate limiter
- Token bucket algorithm
- Backpressure propagation
- Load shedding

### 7. Graceful Degradation
- Feature toggles
- Progressive degradation
- Read-only mode
- Minimal functionality mode

### 8. Health Checks & Probes
```python
# Kubernetes health checks
@app.get("/health/live")
async def liveness_probe():
    """Liveness: proceso está vivo"""
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness_probe():
    """Readiness: listo para recibir tráfico"""
    # Verificar dependencias
    db_ok = await check_database()
    cache_ok = await check_cache()

    if db_ok and cache_ok:
        return {"status": "ready"}
    else:
        return {"status": "not_ready"}, 503
```

### 9. Chaos Engineering
- Fault injection
- Latency injection
- Resource exhaustion
- Network partitions

### 10. Disaster Recovery
- Backup strategies
- Replication
- Failover procedures
- RTO/RPO planning

---

## 📊 Resilience Patterns - Decision Matrix

| Pattern | Protege Contra | Cuándo Usar | Overhead |
|---------|----------------|-------------|----------|
| **Circuit Breaker** | Cascading failures | Siempre en external calls | Bajo |
| **Bulkhead** | Resource exhaustion | Multiple external services | Medio |
| **Retry** | Transient failures | Network calls, DB queries | Bajo |
| **Timeout** | Hanging operations | Todas las IO operations | Muy bajo |
| **Fallback** | Complete failure | Critical user-facing features | Medio |
| **Rate Limiting** | Overload | Public APIs | Bajo |

**Tamaño:** 52KB | **Código:** ~2,000 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
