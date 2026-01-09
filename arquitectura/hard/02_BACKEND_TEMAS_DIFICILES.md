# Conocimientos Técnicos Difíciles: Backend Development

## Objetivo
Temas complejos del día a día backend que un arquitecto debe dominar para apoyar efectivamente a los desarrolladores de servidor y APIs.

---

## CATEGORÍA 1: Concurrency y Paralelismo

### 1.1 Threading y Async Programming
**Dificultad:** ⭐⭐⭐⭐⭐

**Python: Async/Await y Event Loop**

```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 1. Async I/O básico
async def fetch_user(session, user_id):
    async with session.get(f'https://api.example.com/users/{user_id}') as response:
        return await response.json()

async def fetch_all_users(user_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user(session, uid) for uid in user_ids]
        # Ejecutar concurrentemente
        users = await asyncio.gather(*tasks)
        return users

# 2. Mixing sync and async (blocking operations)
async def process_image(image_path):
    # CPU-bound operation - ejecutar en thread pool
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool,
            expensive_image_processing,  # función síncrona
            image_path
        )
    return result

# 3. Rate limiting con semáforos
async def fetch_with_rate_limit(urls, max_concurrent=5):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)

# 4. Timeout handling
async def fetch_with_timeout(url, timeout=5):
    try:
        async with asyncio.timeout(timeout):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()
    except asyncio.TimeoutError:
        print(f"Request to {url} timed out")
        return None

# 5. Background tasks
class BackgroundTasks:
    def __init__(self):
        self.tasks = set()

    def create_task(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)

    async def cleanup(self):
        await asyncio.gather(*self.tasks, return_exceptions=True)

# FastAPI background tasks
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def send_email(email: str, message: str):
    # Tarea pesada que se ejecuta en background
    time.sleep(5)
    print(f"Email sent to {email}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    # Response inmediato, email se envía después
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification queued"}

# 6. Process Pool para CPU-bound tasks
async def cpu_intensive_tasks(data_list):
    loop = asyncio.get_event_loop()

    with ProcessPoolExecutor(max_workers=4) as executor:
        # Distribuir trabajo entre procesos
        futures = [
            loop.run_in_executor(executor, cpu_bound_function, data)
            for data in data_list
        ]
        results = await asyncio.gather(*futures)

    return results

def cpu_bound_function(data):
    # Heavy computation (ML inference, image processing, etc.)
    result = complex_calculation(data)
    return result
```

**Node.js: Event Loop y Workers**

```javascript
// 1. Promise.all vs Promise.allSettled
async function fetchMultipleAPIs() {
    const urls = [
        'https://api1.com/data',
        'https://api2.com/data',
        'https://api3.com/data'
    ];

    // ❌ Promise.all - falla si UNA falla
    try {
        const results = await Promise.all(
            urls.map(url => fetch(url).then(r => r.json()))
        );
    } catch (error) {
        // Si una falla, todas fallan
    }

    // ✅ Promise.allSettled - continúa incluso con fallos
    const results = await Promise.allSettled(
        urls.map(url => fetch(url).then(r => r.json()))
    );

    // Separar exitosas de fallidas
    const successful = results
        .filter(r => r.status === 'fulfilled')
        .map(r => r.value);

    const failed = results
        .filter(r => r.status === 'rejected')
        .map(r => r.reason);

    return { successful, failed };
}

// 2. Worker Threads para CPU-intensive tasks
const { Worker } = require('worker_threads');

function runWorker(workerData) {
    return new Promise((resolve, reject) => {
        const worker = new Worker('./worker.js', { workerData });

        worker.on('message', resolve);
        worker.on('error', reject);
        worker.on('exit', (code) => {
            if (code !== 0) {
                reject(new Error(`Worker stopped with exit code ${code}`));
            }
        });
    });
}

// worker.js
const { parentPort, workerData } = require('worker_threads');

function heavyComputation(data) {
    // CPU-intensive work
    let result = 0;
    for (let i = 0; i < 1000000000; i++) {
        result += i * data;
    }
    return result;
}

const result = heavyComputation(workerData);
parentPort.postMessage(result);

// 3. Concurrency control con p-limit
const pLimit = require('p-limit');

async function processItemsWithLimit(items, concurrency = 5) {
    const limit = pLimit(concurrency);

    const promises = items.map(item => {
        return limit(() => processItem(item));
    });

    return Promise.all(promises);
}

// 4. Retry con exponential backoff
async function fetchWithRetry(url, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const response = await fetch(url);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            if (i === maxRetries - 1) throw error;

            // Exponential backoff: 1s, 2s, 4s
            const delay = Math.pow(2, i) * 1000;
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}

// 5. AbortController para cancelar requests
async function fetchWithCancel(url, timeoutMs = 5000) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(url, {
            signal: controller.signal
        });
        return await response.json();
    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Request was cancelled');
        }
        throw error;
    } finally {
        clearTimeout(timeout);
    }
}
```

**Go: Goroutines y Channels**

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// 1. Basic goroutines con WaitGroup
func processItems(items []string) {
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)
        go func(item string) {
            defer wg.Done()
            processItem(item)
        }(item)
    }

    wg.Wait() // Esperar a que todas terminen
}

// 2. Worker Pool pattern
func workerPool(jobs <-chan Job, results chan<- Result, numWorkers int) {
    var wg sync.WaitGroup

    // Crear workers
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for job := range jobs {
                result := processJob(job)
                results <- result
            }
        }(i)
    }

    // Cerrar results cuando todos los workers terminen
    go func() {
        wg.Wait()
        close(results)
    }()
}

// Uso
func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)

    // Iniciar worker pool
    go workerPool(jobs, results, 5)

    // Enviar jobs
    go func() {
        for i := 0; i < 100; i++ {
            jobs <- Job{ID: i}
        }
        close(jobs)
    }()

    // Procesar results
    for result := range results {
        fmt.Printf("Result: %v\n", result)
    }
}

// 3. Context para cancelación y timeouts
func fetchWithContext(ctx context.Context, url string) error {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return err
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    // Process response...
    return nil
}

// Uso con timeout
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := fetchWithContext(ctx, "https://api.example.com"); err != nil {
        if err == context.DeadlineExceeded {
            fmt.Println("Request timed out")
        }
    }
}

// 4. Select para múltiples channels
func fanIn(ch1, ch2 <-chan string) <-chan string {
    out := make(chan string)

    go func() {
        defer close(out)
        for {
            select {
            case msg, ok := <-ch1:
                if !ok {
                    ch1 = nil
                    continue
                }
                out <- msg
            case msg, ok := <-ch2:
                if !ok {
                    ch2 = nil
                    continue
                }
                out <- msg
            }

            // Salir si ambos channels están cerrados
            if ch1 == nil && ch2 == nil {
                return
            }
        }
    }()

    return out
}

// 5. Rate limiting con ticker
func rateLimitedWorker(jobs <-chan Job, rateLimit time.Duration) {
    ticker := time.NewTicker(rateLimit)
    defer ticker.Stop()

    for job := range jobs {
        <-ticker.C // Esperar al próximo tick
        processJob(job)
    }
}

// 6. Errgroup para manejo de errores
import "golang.org/x/sync/errgroup"

func fetchMultiple(urls []string) error {
    g := new(errgroup.Group)

    for _, url := range urls {
        url := url // Capture variable
        g.Go(func() error {
            resp, err := http.Get(url)
            if err != nil {
                return err
            }
            defer resp.Body.Close()
            // Process response...
            return nil
        })
    }

    // Esperar y retornar primer error
    return g.Wait()
}
```

---

### 1.2 Database Connection Pooling
**Dificultad:** ⭐⭐⭐⭐

**Python - SQLAlchemy**

```python
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker
import time

# 1. Configuración óptima de pool
engine = create_engine(
    'postgresql://user:password@localhost/db',
    # Tamaño del pool
    pool_size=20,               # Conexiones persistentes
    max_overflow=10,            # Conexiones adicionales temporales
    # Timeouts
    pool_timeout=30,            # Timeout esperando conexión del pool
    pool_recycle=3600,          # Reciclar conexión después de 1h
    pool_pre_ping=True,         # Verificar conexión antes de usar
    # Estrategia de pool
    poolclass=pool.QueuePool,
    # Logging
    echo_pool='debug'
)

# 2. Context manager para garantizar cierre
from contextlib import contextmanager

Session = sessionmaker(bind=engine)

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()  # Devuelve conexión al pool

# Uso
def create_user(name, email):
    with get_db_session() as session:
        user = User(name=name, email=email)
        session.add(user)
        # Commit automático al salir del context

# 3. Monitoreo del pool
def check_pool_status(engine):
    pool = engine.pool
    return {
        'size': pool.size(),
        'checked_in': pool.checkedin(),
        'checked_out': pool.checkedout(),
        'overflow': pool.overflow(),
        'total': pool.checkedout() + pool.checkedin()
    }

# 4. Detectar connection leaks
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

# Buscar en logs: "Connection <...> being returned to pool"
# Si no aparece, hay leak

# 5. Custom pool con límite de tiempo
class TimedQueuePool(pool.QueuePool):
    def __init__(self, *args, **kwargs):
        self.connection_times = {}
        super().__init__(*args, **kwargs)

    def _checkout(self, *args, **kwargs):
        conn = super()._checkout(*args, **kwargs)
        self.connection_times[id(conn)] = time.time()
        return conn

    def _checkin(self, conn):
        checkout_time = self.connection_times.pop(id(conn), None)
        if checkout_time:
            duration = time.time() - checkout_time
            if duration > 10:  # Más de 10s
                logging.warning(f"Connection held for {duration}s")
        super()._checkin(conn)
```

**Node.js - PostgreSQL (node-postgres)**

```javascript
const { Pool } = require('pg');

// 1. Configuración óptima
const pool = new Pool({
    host: 'localhost',
    port: 5432,
    database: 'mydb',
    user: 'user',
    password: 'password',

    // Pool configuration
    min: 5,                    // Mínimo de conexiones idle
    max: 20,                   // Máximo de conexiones
    idleTimeoutMillis: 30000,  // Cerrar idle después de 30s
    connectionTimeoutMillis: 2000, // Timeout esperando conexión

    // Keep-alive
    keepAlive: true,
    keepAliveInitialDelayMillis: 10000
});

// 2. Query helper con manejo de errores
async function query(text, params) {
    const start = Date.now();
    try {
        const res = await pool.query(text, params);
        const duration = Date.now() - start;

        // Log queries lentas
        if (duration > 1000) {
            console.warn('Slow query', { text, duration, rows: res.rowCount });
        }

        return res;
    } catch (error) {
        console.error('Query error', { text, error });
        throw error;
    }
}

// 3. Transacciones con cliente dedicado
async function transferMoney(fromId, toId, amount) {
    const client = await pool.connect();

    try {
        await client.query('BEGIN');

        await client.query(
            'UPDATE accounts SET balance = balance - $1 WHERE id = $2',
            [amount, fromId]
        );

        await client.query(
            'UPDATE accounts SET balance = balance + $1 WHERE id = $2',
            [amount, toId]
        );

        await client.query('COMMIT');
    } catch (error) {
        await client.query('ROLLBACK');
        throw error;
    } finally {
        client.release(); // CRÍTICO: devolver al pool
    }
}

// 4. Monitoreo del pool
function getPoolStats() {
    return {
        total: pool.totalCount,
        idle: pool.idleCount,
        waiting: pool.waitingCount
    };
}

// Log stats cada 30 segundos
setInterval(() => {
    const stats = getPoolStats();
    console.log('Pool stats:', stats);

    if (stats.waiting > 0) {
        console.warn('Pool exhaustion detected!');
    }
}, 30000);

// 5. Graceful shutdown
async function closePool() {
    await pool.end();
    console.log('Pool has ended');
}

process.on('SIGINT', async () => {
    await closePool();
    process.exit(0);
});

// 6. Connection leak detection
const activeConnections = new Map();

pool.on('acquire', (client) => {
    const stack = new Error().stack;
    activeConnections.set(client, {
        acquiredAt: Date.now(),
        stack
    });
});

pool.on('release', (client) => {
    activeConnections.delete(client);
});

// Check for leaks cada minuto
setInterval(() => {
    const now = Date.now();
    for (const [client, info] of activeConnections) {
        const duration = now - info.acquiredAt;
        if (duration > 60000) { // 1 minuto
            console.error('Connection leak detected!', {
                duration,
                stack: info.stack
            });
        }
    }
}, 60000);
```

---

## CATEGORÍA 2: API Design Patterns

### 2.1 Rate Limiting Implementation
**Dificultad:** ⭐⭐⭐⭐

```python
# FastAPI con Redis
from fastapi import FastAPI, HTTPException, Request
from redis import Redis
import time

redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# 1. Token Bucket con Redis
class TokenBucket:
    def __init__(self, redis_client, capacity=100, refill_rate=10):
        self.redis = redis_client
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second

    async def consume(self, key: str, tokens: int = 1) -> bool:
        now = time.time()

        # Lua script para atomicidad
        script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local tokens_to_consume = tonumber(ARGV[3])
        local now = tonumber(ARGV[4])

        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1]) or capacity
        local last_refill = tonumber(bucket[2]) or now

        -- Refill tokens
        local time_passed = now - last_refill
        local refill = time_passed * refill_rate
        tokens = math.min(capacity, tokens + refill)

        -- Consume tokens
        if tokens >= tokens_to_consume then
            tokens = tokens - tokens_to_consume
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
            redis.call('EXPIRE', key, 86400)  -- 24h TTL
            return 1
        else
            return 0
        end
        """

        result = self.redis.eval(
            script,
            1,
            key,
            self.capacity,
            self.refill_rate,
            tokens,
            now
        )

        return bool(result)

# Middleware
bucket = TokenBucket(redis_client)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    if not await bucket.consume(key):
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
            headers={"Retry-After": "60"}
        )

    response = await call_next(request)
    return response

# 2. Sliding Window Log
class SlidingWindowLog:
    def __init__(self, redis_client, max_requests=100, window_seconds=60):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window_seconds

    async def allow_request(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window

        pipeline = self.redis.pipeline()

        # Remover requests antiguas
        pipeline.zremrangebyscore(key, 0, window_start)

        # Contar requests en ventana
        pipeline.zcard(key)

        # Agregar request actual
        pipeline.zadd(key, {str(now): now})

        # Expirar después de ventana
        pipeline.expire(key, self.window)

        results = pipeline.execute()
        request_count = results[1]

        return request_count < self.max_requests

# 3. Rate limiting por usuario y endpoint
from functools import wraps

def rate_limit(max_calls: int, period: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            user_id = request.state.user_id
            endpoint = request.url.path

            key = f"rate_limit:{user_id}:{endpoint}"
            limiter = SlidingWindowLog(redis_client, max_calls, period)

            if not await limiter.allow_request(key):
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded: {max_calls} requests per {period}s"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Uso
@app.get("/api/data")
@rate_limit(max_calls=10, period=60)
async def get_data(request: Request):
    return {"data": "..."}
```

---

### 2.2 API Pagination Strategies
**Dificultad:** ⭐⭐⭐⭐

```python
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Query

T = TypeVar('T')

# 1. Offset Pagination (simple pero problemático)
class OffsetPagination(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

def paginate_offset(query: Query, page: int, page_size: int) -> OffsetPagination:
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return OffsetPagination(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=page * page_size < total,
        has_prev=page > 1
    )

# ⚠️ Problemas:
# - Lento con offset grande
# - Inconsistente si datos cambian entre páginas
# - Salta/duplica items si hay inserts/deletes

# 2. Cursor Pagination (mejor para feeds infinitos)
class CursorPagination(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[str]
    prev_cursor: Optional[str]

import base64
import json

def encode_cursor(data: dict) -> str:
    json_str = json.dumps(data)
    return base64.urlsafe_b64encode(json_str.encode()).decode()

def decode_cursor(cursor: str) -> dict:
    json_str = base64.urlsafe_b64decode(cursor.encode()).decode()
    return json.loads(json_str)

def paginate_cursor(
    query: Query,
    cursor: Optional[str],
    page_size: int,
    sort_field='created_at'
) -> CursorPagination:

    if cursor:
        cursor_data = decode_cursor(cursor)
        sort_value = cursor_data['value']
        item_id = cursor_data['id']

        # WHERE (created_at, id) > (cursor_value, cursor_id)
        query = query.filter(
            or_(
                getattr(Model, sort_field) > sort_value,
                and_(
                    getattr(Model, sort_field) == sort_value,
                    Model.id > item_id
                )
            )
        )

    # Fetch one extra para saber si hay más
    items = query.order_by(
        getattr(Model, sort_field),
        Model.id
    ).limit(page_size + 1).all()

    has_next = len(items) > page_size
    items = items[:page_size]

    next_cursor = None
    if has_next and items:
        last_item = items[-1]
        next_cursor = encode_cursor({
            'value': getattr(last_item, sort_field),
            'id': last_item.id
        })

    return CursorPagination(
        items=items,
        next_cursor=next_cursor,
        prev_cursor=None  # Implementar si necesario
    )

# 3. Keyset Pagination (más eficiente)
@app.get("/users")
async def get_users(
    last_id: Optional[int] = None,
    last_created_at: Optional[datetime] = None,
    limit: int = 20
):
    query = db.query(User)

    if last_id and last_created_at:
        # Continuar desde último item
        query = query.filter(
            or_(
                User.created_at < last_created_at,
                and_(
                    User.created_at == last_created_at,
                    User.id < last_id
                )
            )
        )

    users = query.order_by(
        User.created_at.desc(),
        User.id.desc()
    ).limit(limit + 1).all()

    has_more = len(users) > limit
    users = users[:limit]

    response = {
        "users": users,
        "has_more": has_more
    }

    if users and has_more:
        last = users[-1]
        response["next_params"] = {
            "last_id": last.id,
            "last_created_at": last.created_at.isoformat()
        }

    return response

# ✅ Ventajas:
# - Muy rápido (usa índices)
# - Consistente incluso con cambios
# - No salta items
```

---

## CATEGORÍA 3: Error Handling y Logging

### 3.1 Structured Logging
**Dificultad:** ⭐⭐⭐⭐

```python
import logging
import json
from datetime import datetime
from contextvars import ContextVar

# Context para request tracing
request_id_var: ContextVar[str] = ContextVar('request_id', default='')

# 1. Custom JSON formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'request_id': request_id_var.get(''),
        }

        # Agregar contexto adicional
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id

        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms

        # Exception info
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }

        # Campos custom
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)

        return json.dumps(log_data)

# Configuración
logger = logging.getLogger('app')
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 2. Middleware para request logging
from fastapi import Request
import time
import uuid

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)

    start_time = time.time()

    # Log request
    logger.info(
        "Request started",
        extra={
            'extra_data': {
                'method': request.method,
                'path': request.url.path,
                'client_ip': request.client.host
            }
        }
    )

    try:
        response = await call_next(request)
        duration = (time.time() - start_time) * 1000

        # Log response
        logger.info(
            "Request completed",
            extra={
                'extra_data': {
                    'status_code': response.status_code,
                    'duration_ms': duration
                }
            }
        )

        response.headers['X-Request-ID'] = request_id
        return response

    except Exception as e:
        duration = (time.time() - start_time) * 1000
        logger.error(
            "Request failed",
            exc_info=True,
            extra={
                'extra_data': {
                    'duration_ms': duration,
                    'error_type': type(e).__name__
                }
            }
        )
        raise

# 3. Structured logging con contexto
class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def log(self, level: str, message: str, **kwargs):
        extra = {'extra_data': kwargs}
        getattr(self.logger, level)(message, extra=extra)

    def info(self, message: str, **kwargs):
        self.log('info', message, **kwargs)

    def error(self, message: str, **kwargs):
        self.log('error', message, **kwargs)

    def warn(self, message: str, **kwargs):
        self.log('warning', message, **kwargs)

# Uso
logger = Logger('api')

@app.post("/orders")
async def create_order(order_data: dict, user_id: int):
    logger.info(
        "Creating order",
        user_id=user_id,
        items_count=len(order_data['items']),
        total_amount=order_data['total']
    )

    try:
        order = await create_order_in_db(order_data)
        logger.info(
            "Order created successfully",
            order_id=order.id,
            user_id=user_id
        )
        return order
    except Exception as e:
        logger.error(
            "Failed to create order",
            user_id=user_id,
            error=str(e),
            exc_info=True
        )
        raise
```

---

### 3.2 Error Handling Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from typing import Union, TypeVar, Generic
from dataclasses import dataclass

# 1. Result pattern (evitar exceptions para control de flujo)
T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Ok(Generic[T]):
    value: T
    def is_ok(self) -> bool: return True
    def is_err(self) -> bool: return False

@dataclass
class Err(Generic[E]):
    error: E
    def is_ok(self) -> bool: return False
    def is_err(self) -> bool: return True

Result = Union[Ok[T], Err[E]]

# Uso
def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

result = divide(10, 2)
if result.is_ok():
    print(f"Result: {result.value}")
else:
    print(f"Error: {result.error}")

# 2. Custom exception hierarchy
class APIError(Exception):
    """Base exception"""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(APIError):
    def __init__(self, message: str, field_errors: dict = None):
        super().__init__(
            message=message,
            status_code=400,
            details={'field_errors': field_errors or {}}
        )

class NotFoundError(APIError):
    def __init__(self, resource: str, id: any):
        super().__init__(
            message=f"{resource} not found",
            status_code=404,
            details={'resource': resource, 'id': id}
        )

class UnauthorizedError(APIError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message=message, status_code=401)

# 3. Global exception handler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': {
                'message': exc.message,
                'type': exc.__class__.__name__,
                'details': exc.details
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = '.'.join(str(loc) for loc in error['loc'])
        errors[field] = error['msg']

    return JSONResponse(
        status_code=422,
        content={
            'error': {
                'message': 'Validation failed',
                'type': 'ValidationError',
                'details': {'field_errors': errors}
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=True)

    # En producción, no exponer detalles internos
    if settings.ENV == 'production':
        message = "Internal server error"
        details = {}
    else:
        message = str(exc)
        details = {'type': exc.__class__.__name__}

    return JSONResponse(
        status_code=500,
        content={
            'error': {
                'message': message,
                'type': 'InternalError',
                'details': details
            }
        }
    )

# 4. Retry con decorador
from functools import wraps
import time

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 1
            current_delay = delay

            while attempt <= max_attempts:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        logger.error(
                            f"Failed after {max_attempts} attempts",
                            function=func.__name__,
                            error=str(e)
                        )
                        raise

                    logger.warn(
                        f"Attempt {attempt} failed, retrying...",
                        function=func.__name__,
                        error=str(e),
                        next_retry_in=current_delay
                    )

                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
                    attempt += 1

        return wrapper
    return decorator

# Uso
@retry(max_attempts=3, delay=1.0, exceptions=(HTTPError, TimeoutError))
async def fetch_external_api(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5.0)
        response.raise_for_status()
        return response.json()
```

Continúa en siguiente archivo...

---

## Resumen de Prioridades Backend

| Tema | Dificultad | Criticidad | Frecuencia | Prioridad |
|------|------------|------------|------------|-----------|
| Concurrency/Async | 5 | 5 | 5 | **CRÍTICA** |
| Connection Pooling | 4 | 5 | 5 | **CRÍTICA** |
| Error Handling | 5 | 5 | 5 | **CRÍTICA** |
| Rate Limiting | 4 | 4 | 4 | **ALTA** |
| Structured Logging | 4 | 4 | 5 | **ALTA** |
| API Pagination | 4 | 3 | 4 | **ALTA** |

**Continuará con más categorías...**
