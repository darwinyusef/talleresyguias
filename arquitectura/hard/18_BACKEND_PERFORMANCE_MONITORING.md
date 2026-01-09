# Backend: Performance Optimization y Monitoring

## Objetivo
Técnicas avanzadas de optimización de performance, monitoreo en producción, y tuning de bases de datos para sistemas de alta escala.

---

## CATEGORÍA 1: Database Performance Optimization

### 1.1 Query Optimization y Indexing
**Dificultad:** ⭐⭐⭐⭐⭐

**PostgreSQL - Advanced Indexing Strategies**

```sql
-- 1. B-Tree Index (default, best for equality and range queries)
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- 2. Partial Index (index only subset of data)
-- Only index active users
CREATE INDEX idx_active_users_email
ON users(email)
WHERE active = true;

-- Only index recent orders (last 30 days)
CREATE INDEX idx_recent_orders
ON orders(user_id, created_at)
WHERE created_at > NOW() - INTERVAL '30 days';

-- 3. Composite Index (multiple columns)
-- Order matters! Most selective column first
CREATE INDEX idx_orders_user_status_date
ON orders(user_id, status, created_at DESC);

-- This index supports queries:
-- WHERE user_id = X
-- WHERE user_id = X AND status = Y
-- WHERE user_id = X AND status = Y ORDER BY created_at DESC

-- 4. Covering Index (include additional columns)
CREATE INDEX idx_orders_user_covering
ON orders(user_id)
INCLUDE (total, status, created_at);

-- Query can be satisfied entirely from index (index-only scan)

-- 5. Expression Index (index on computed values)
CREATE INDEX idx_users_lower_email
ON users(LOWER(email));

-- Now case-insensitive search is fast:
-- WHERE LOWER(email) = 'user@example.com'

CREATE INDEX idx_orders_year_month
ON orders(EXTRACT(YEAR FROM created_at), EXTRACT(MONTH FROM created_at));

-- 6. GIN Index (for full-text search and JSONB)
CREATE INDEX idx_products_search
ON products USING GIN(to_tsvector('english', name || ' ' || description));

-- Full-text search
-- WHERE to_tsvector('english', name || ' ' || description) @@ to_tsquery('laptop');

CREATE INDEX idx_metadata_gin
ON users USING GIN(metadata jsonb_path_ops);

-- JSONB queries
-- WHERE metadata @> '{"country": "USA"}'

-- 7. GiST Index (for geometric and full-text)
CREATE INDEX idx_locations_gist
ON stores USING GIST(location);

-- Geographic queries
-- WHERE ST_DWithin(location, point, 1000)

-- 8. Hash Index (only for equality, smaller than B-tree)
CREATE INDEX idx_sessions_hash
ON sessions USING HASH(session_id);

-- Only for: WHERE session_id = 'abc123'

-- 9. BRIN Index (Block Range Index - for very large tables)
-- Efficient for naturally ordered data (timestamps, IDs)
CREATE INDEX idx_logs_brin
ON logs USING BRIN(created_at);

-- Much smaller than B-tree, good for append-only tables
```

**Python - Query Optimization Patterns**

```python
from sqlalchemy import select, func, literal_column
from sqlalchemy.orm import joinedload, selectinload, subqueryload

class OptimizedQueryService:
    """
    Advanced query optimization techniques
    """

    def __init__(self, db):
        self.db = db

    async def get_users_with_orders_optimized(self, user_ids: List[int]):
        """
        Avoid N+1 queries using eager loading
        """

        # ❌ Bad: N+1 query problem
        # users = await self.db.query(User).filter(User.id.in_(user_ids)).all()
        # for user in users:
        #     orders = user.orders  # Triggers N additional queries!

        # ✅ Good: Eager loading with joinedload
        stmt = (
            select(User)
            .options(joinedload(User.orders))
            .filter(User.id.in_(user_ids))
        )
        result = await self.db.execute(stmt)
        users = result.scalars().unique().all()

        return users

    async def get_users_with_many_orders(self, user_ids: List[int]):
        """
        For one-to-many with many items, use selectinload
        Generates 2 queries instead of N+1
        """

        stmt = (
            select(User)
            .options(selectinload(User.orders))
            .filter(User.id.in_(user_ids))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_order_statistics_optimized(self, user_id: int):
        """
        Compute aggregates in database, not in Python
        """

        # ❌ Bad: Fetch all data and compute in Python
        # orders = await self.db.query(Order).filter(Order.user_id == user_id).all()
        # total = sum(order.total for order in orders)
        # count = len(orders)

        # ✅ Good: Compute in database
        stmt = (
            select(
                func.count(Order.id).label('order_count'),
                func.sum(Order.total).label('total_spent'),
                func.avg(Order.total).label('average_order'),
                func.max(Order.created_at).label('last_order_date')
            )
            .filter(Order.user_id == user_id)
        )

        result = await self.db.execute(stmt)
        return result.first()

    async def get_paginated_results_optimized(
        self,
        page: int,
        page_size: int
    ):
        """
        Efficient pagination with cursor-based approach
        """

        # ❌ Bad: OFFSET pagination (slow for large offsets)
        # offset = (page - 1) * page_size
        # stmt = select(Order).offset(offset).limit(page_size)

        # ✅ Good: Cursor-based pagination
        # Assumes last_id from previous page
        last_id = get_last_id_from_previous_page()

        stmt = (
            select(Order)
            .filter(Order.id > last_id)
            .order_by(Order.id)
            .limit(page_size)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def bulk_insert_optimized(self, users_data: List[dict]):
        """
        Bulk insert for better performance
        """

        # ❌ Bad: Individual inserts
        # for user_data in users_data:
        #     user = User(**user_data)
        #     self.db.add(user)
        #     await self.db.commit()

        # ✅ Good: Bulk insert
        await self.db.execute(
            insert(User),
            users_data
        )
        await self.db.commit()

    async def update_in_batches(self, user_ids: List[int], data: dict):
        """
        Batch updates to avoid long-running transactions
        """

        batch_size = 1000

        for i in range(0, len(user_ids), batch_size):
            batch = user_ids[i:i + batch_size]

            await self.db.execute(
                update(User)
                .filter(User.id.in_(batch))
                .values(**data)
            )
            await self.db.commit()

    async def complex_query_with_cte(self):
        """
        Use CTE (Common Table Expression) for complex queries
        """

        # CTE for recent orders
        recent_orders_cte = (
            select(
                Order.user_id,
                func.count(Order.id).label('order_count'),
                func.sum(Order.total).label('total_spent')
            )
            .filter(Order.created_at > func.now() - timedelta(days=30))
            .group_by(Order.user_id)
            .cte('recent_orders')
        )

        # Main query joining with CTE
        stmt = (
            select(
                User.id,
                User.name,
                recent_orders_cte.c.order_count,
                recent_orders_cte.c.total_spent
            )
            .join(recent_orders_cte, User.id == recent_orders_cte.c.user_id)
            .filter(recent_orders_cte.c.order_count > 5)
        )

        result = await self.db.execute(stmt)
        return result.all()

    async def use_prepared_statement(self, user_id: int):
        """
        Prepared statements for frequently executed queries
        """

        # PostgreSQL will cache the query plan
        stmt = text("""
            SELECT u.*, COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE u.id = :user_id
            GROUP BY u.id
        """).bindparams(user_id=user_id)

        result = await self.db.execute(stmt)
        return result.first()

    async def materialized_view_pattern(self):
        """
        Create materialized view for expensive aggregations
        """

        # Create materialized view (run once)
        await self.db.execute(text("""
            CREATE MATERIALIZED VIEW user_stats AS
            SELECT
                u.id,
                u.name,
                COUNT(o.id) as total_orders,
                SUM(o.total) as total_spent,
                MAX(o.created_at) as last_order_date
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id, u.name
        """))

        # Create index on materialized view
        await self.db.execute(text("""
            CREATE INDEX idx_user_stats_id ON user_stats(id)
        """))

        # Query materialized view (very fast)
        result = await self.db.execute(
            text("SELECT * FROM user_stats WHERE id = :user_id"),
            {"user_id": 123}
        )

        return result.first()

    async def refresh_materialized_view(self):
        """
        Refresh materialized view (run periodically)
        """

        # Concurrent refresh (doesn't block reads)
        await self.db.execute(
            text("REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats")
        )

# Query performance analysis
class QueryAnalyzer:
    """
    Analyze and optimize slow queries
    """

    def __init__(self, db):
        self.db = db

    async def explain_query(self, stmt):
        """
        Get query execution plan
        """

        explain_stmt = text(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {stmt}")
        result = await self.db.execute(explain_stmt)

        plan = result.scalar()
        return json.loads(plan)

    async def find_missing_indexes(self):
        """
        Find tables that might benefit from indexes
        """

        query = text("""
            SELECT
                schemaname,
                tablename,
                seq_scan,
                seq_tup_read,
                idx_scan,
                seq_tup_read / seq_scan as avg_seq_tup_read
            FROM pg_stat_user_tables
            WHERE seq_scan > 0
            ORDER BY seq_tup_read DESC
            LIMIT 20
        """)

        result = await self.db.execute(query)
        return result.all()

    async def find_unused_indexes(self):
        """
        Find indexes that are never used
        """

        query = text("""
            SELECT
                schemaname,
                tablename,
                indexname,
                idx_scan,
                pg_size_pretty(pg_relation_size(indexrelid)) as index_size
            FROM pg_stat_user_indexes
            WHERE idx_scan = 0
            AND indexrelname NOT LIKE 'pg_toast%'
            ORDER BY pg_relation_size(indexrelid) DESC
        """)

        result = await self.db.execute(query)
        return result.all()

    async def get_slow_queries(self, min_duration_ms: int = 1000):
        """
        Get slow queries from pg_stat_statements
        Requires: CREATE EXTENSION pg_stat_statements;
        """

        query = text("""
            SELECT
                query,
                calls,
                total_exec_time,
                mean_exec_time,
                max_exec_time,
                rows
            FROM pg_stat_statements
            WHERE mean_exec_time > :min_duration
            ORDER BY mean_exec_time DESC
            LIMIT 20
        """)

        result = await self.db.execute(
            query,
            {"min_duration": min_duration_ms}
        )
        return result.all()

    async def analyze_table_bloat(self):
        """
        Check for table bloat (wasted space)
        """

        query = text("""
            SELECT
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
                pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) -
                               pg_relation_size(schemaname||'.'||tablename)) as indexes_size
            FROM pg_tables
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
        """)

        result = await self.db.execute(query)
        return result.all()
```

---

### 1.2 Connection Pool Optimization
**Dificultad:** ⭐⭐⭐⭐

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool, QueuePool, StaticPool
import time

class OptimizedConnectionPool:
    """
    Advanced connection pool configuration
    """

    def __init__(self, database_url: str, environment: str):
        self.database_url = database_url
        self.environment = environment

        # Configuration based on environment
        if environment == 'production':
            pool_config = {
                'pool_size': 20,           # Permanent connections
                'max_overflow': 10,        # Additional temporary connections
                'pool_timeout': 30,        # Wait time for connection
                'pool_recycle': 3600,      # Recycle connections after 1 hour
                'pool_pre_ping': True,     # Verify connection before use
                'echo_pool': False,        # Don't log pool operations
            }
        elif environment == 'testing':
            pool_config = {
                'poolclass': NullPool,     # No pooling in tests
            }
        else:  # development
            pool_config = {
                'pool_size': 5,
                'max_overflow': 5,
                'echo_pool': 'debug',      # Log pool operations
            }

        self.engine = create_async_engine(
            database_url,
            **pool_config,
            # Performance options
            execution_options={
                "isolation_level": "READ COMMITTED"
            }
        )

        self.SessionLocal = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_pool_status(self) -> dict:
        """
        Get current pool status
        """

        pool = self.engine.pool

        return {
            'size': pool.size(),
            'checked_in': pool.checkedin(),
            'checked_out': pool.checkedout(),
            'overflow': pool.overflow(),
            'total_connections': pool.size() + pool.overflow()
        }

    async def monitor_pool_health(self):
        """
        Monitor pool health and log warnings
        """

        while True:
            await asyncio.sleep(60)  # Check every minute

            status = await self.get_pool_status()

            # Calculate utilization
            total = status['size'] + status['overflow']
            in_use = status['checked_out']
            utilization = (in_use / total) * 100 if total > 0 else 0

            logger.info(
                "Connection pool status",
                **status,
                utilization_percent=utilization
            )

            # Alert if utilization is high
            if utilization > 80:
                logger.warning(
                    "High connection pool utilization",
                    utilization=utilization
                )

            # Alert if overflow is being used
            if status['overflow'] > 0:
                logger.warning(
                    "Connection pool overflow in use",
                    overflow=status['overflow']
                )

    async def warm_up_pool(self):
        """
        Pre-create connections to avoid cold start
        """

        logger.info("Warming up connection pool")

        sessions = []

        # Create initial connections
        for _ in range(self.engine.pool.size()):
            session = self.SessionLocal()
            sessions.append(session)

        # Close all sessions (returns to pool)
        for session in sessions:
            await session.close()

        logger.info("Connection pool warmed up")

# Middleware for connection management
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Provide database session per request
    Ensures connections are properly returned to pool
    """

    session = None

    try:
        # Create session
        session = SessionLocal()
        request.state.db = session

        # Track connection checkout time
        start_time = time.time()

        response = await call_next(request)

        # Log long-held connections
        duration = time.time() - start_time
        if duration > 5:
            logger.warning(
                "Long database session",
                duration_seconds=duration,
                path=request.url.path
            )

        return response

    finally:
        if session:
            await session.close()

# Connection retry logic
class DatabaseConnectionRetry:
    """
    Retry database operations with exponential backoff
    """

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay

    async def execute_with_retry(self, operation: Callable):
        """
        Execute database operation with retry
        """

        for attempt in range(self.max_retries):
            try:
                return await operation()

            except (OperationalError, ConnectionError) as e:
                if attempt == self.max_retries - 1:
                    logger.error(
                        f"Database operation failed after {self.max_retries} attempts",
                        error=str(e)
                    )
                    raise

                delay = self.base_delay * (2 ** attempt)

                logger.warning(
                    f"Database operation failed, retrying in {delay}s",
                    attempt=attempt + 1,
                    error=str(e)
                )

                await asyncio.sleep(delay)

# Usage
retry_handler = DatabaseConnectionRetry()

async def get_user_with_retry(user_id: int):
    async def operation():
        async with SessionLocal() as session:
            result = await session.execute(
                select(User).filter(User.id == user_id)
            )
            return result.scalar_one_or_none()

    return await retry_handler.execute_with_retry(operation)
```

---

## CATEGORÍA 2: Application Performance Monitoring

### 2.1 Prometheus Metrics Integration
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import time

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently in progress',
    ['method', 'endpoint']
)

database_query_duration = Histogram(
    'database_query_duration_seconds',
    'Database query duration',
    ['query_type'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]
)

cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_name']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_name']
)

active_users = Gauge(
    'active_users',
    'Number of currently active users'
)

background_tasks_total = Counter(
    'background_tasks_total',
    'Total background tasks executed',
    ['task_name', 'status']
)

external_api_calls = Counter(
    'external_api_calls_total',
    'Total external API calls',
    ['service', 'endpoint', 'status']
)

external_api_duration = Histogram(
    'external_api_duration_seconds',
    'External API call duration',
    ['service', 'endpoint']
)

# Middleware for automatic metrics collection
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """
    Collect metrics for all HTTP requests
    """

    method = request.method
    endpoint = request.url.path

    # Track in-progress requests
    http_requests_in_progress.labels(method=method, endpoint=endpoint).inc()

    # Track request duration
    start_time = time.time()

    try:
        response = await call_next(request)
        status = response.status_code

        # Record metrics
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        duration = time.time() - start_time
        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

        return response

    finally:
        http_requests_in_progress.labels(method=method, endpoint=endpoint).dec()

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Custom metrics collection
class MetricsCollector:
    """
    Collect custom business metrics
    """

    @staticmethod
    def track_database_query(query_type: str):
        """
        Decorator to track database query performance
        """

        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()

                try:
                    result = await func(*args, **kwargs)
                    return result

                finally:
                    duration = time.time() - start_time
                    database_query_duration.labels(
                        query_type=query_type
                    ).observe(duration)

            return wrapper
        return decorator

    @staticmethod
    def track_cache_operation(cache_name: str):
        """
        Track cache hits and misses
        """

        def decorator(func):
            async def wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)

                if result is not None:
                    cache_hits_total.labels(cache_name=cache_name).inc()
                else:
                    cache_misses_total.labels(cache_name=cache_name).inc()

                return result

            return wrapper
        return decorator

    @staticmethod
    async def track_external_api_call(service: str, endpoint: str, operation: Callable):
        """
        Track external API call metrics
        """

        start_time = time.time()

        try:
            result = await operation()

            external_api_calls.labels(
                service=service,
                endpoint=endpoint,
                status='success'
            ).inc()

            return result

        except Exception as e:
            external_api_calls.labels(
                service=service,
                endpoint=endpoint,
                status='error'
            ).inc()
            raise

        finally:
            duration = time.time() - start_time
            external_api_duration.labels(
                service=service,
                endpoint=endpoint
            ).observe(duration)

# Usage examples
@MetricsCollector.track_database_query('get_user')
async def get_user(user_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).filter(User.id == user_id)
        )
        return result.scalar_one_or_none()

@MetricsCollector.track_cache_operation('user_cache')
async def get_cached_user(user_id: int):
    return await cache.get(f"user:{user_id}")

async def call_payment_service(payment_data: dict):
    async def operation():
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://payment-service/charge",
                json=payment_data
            )
            return response.json()

    return await MetricsCollector.track_external_api_call(
        service='payment_service',
        endpoint='/charge',
        operation=operation
    )

# Background task to update gauge metrics
async def update_active_users_metric():
    """
    Periodically update active users gauge
    """

    while True:
        try:
            count = await get_active_user_count()
            active_users.set(count)

            await asyncio.sleep(60)  # Update every minute

        except Exception as e:
            logger.error(f"Error updating active users metric: {e}")
            await asyncio.sleep(60)

@app.on_event("startup")
async def startup_metrics():
    """
    Start background metric collectors
    """
    asyncio.create_task(update_active_users_metric())
```

---

### 2.2 Distributed Tracing con Jaeger
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

# Setup tracing
def setup_tracing(service_name: str):
    """
    Configure distributed tracing with Jaeger
    """

    resource = Resource(attributes={
        ResourceAttributes.SERVICE_NAME: service_name,
        ResourceAttributes.SERVICE_VERSION: "1.0.0",
        ResourceAttributes.DEPLOYMENT_ENVIRONMENT: os.getenv('ENV', 'development')
    })

    provider = TracerProvider(resource=resource)

    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.getenv('JAEGER_AGENT_HOST', 'localhost'),
        agent_port=int(os.getenv('JAEGER_AGENT_PORT', 6831)),
    )

    # Add span processor
    provider.add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )

    trace.set_tracer_provider(provider)

    # Auto-instrument frameworks
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=engine)
    HTTPXClientInstrumentor().instrument()

    return trace.get_tracer(service_name)

tracer = setup_tracing("order-service")

# Custom spans for business logic
@app.post("/orders")
async def create_order(order_data: dict):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("order.user_id", order_data['user_id'])
        span.set_attribute("order.items_count", len(order_data['items']))
        span.set_attribute("order.total", order_data['total'])

        # Validate inventory
        with tracer.start_as_current_span("validate_inventory"):
            inventory_valid = await validate_inventory(order_data['items'])

            if not inventory_valid:
                span.add_event("inventory_validation_failed")
                raise HTTPException(status_code=400, detail="Insufficient inventory")

        # Process payment
        with tracer.start_as_current_span("process_payment") as payment_span:
            payment_result = await process_payment(order_data['payment'])
            payment_span.set_attribute("payment.method", order_data['payment']['method'])
            payment_span.set_attribute("payment.status", payment_result.status)

        # Save order
        with tracer.start_as_current_span("save_order"):
            order = await save_order(order_data)
            span.set_attribute("order.id", order.id)

        span.add_event("order_created", {
            "order.id": order.id
        })

        return order
```

---

Continúa en siguiente sección...

---

## CATEGORÍA 3: Performance Profiling

### 3.1 Application Profiling
**Dificultad:** ⭐⭐⭐⭐

```python
import cProfile
import pstats
from io import StringIO
from functools import wraps
import tracemalloc
import linecache

class PerformanceProfiler:
    """
    Profile application performance
    """

    @staticmethod
    def profile_function(func):
        """
        Profile function execution time
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()

            try:
                result = await func(*args, **kwargs)
                return result

            finally:
                profiler.disable()

                # Print stats
                stream = StringIO()
                stats = pstats.Stats(profiler, stream=stream)
                stats.sort_stats('cumulative')
                stats.print_stats(20)  # Top 20 functions

                logger.info(
                    f"Profile for {func.__name__}",
                    profile=stream.getvalue()
                )

        return wrapper

    @staticmethod
    def profile_memory(func):
        """
        Profile memory usage
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracemalloc.start()

            try:
                result = await func(*args, **kwargs)
                return result

            finally:
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                logger.info(
                    f"Memory profile for {func.__name__}",
                    current_mb=current / 1024 / 1024,
                    peak_mb=peak / 1024 / 1024
                )

        return wrapper

    @staticmethod
    async def snapshot_memory():
        """
        Take memory snapshot and show top allocations
        """

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        logger.info("Top 10 memory allocations:")

        for stat in top_stats[:10]:
            logger.info(
                f"{stat.filename}:{stat.lineno}: "
                f"{stat.size / 1024:.1f} KB, "
                f"{stat.count} blocks"
            )

# Usage
@PerformanceProfiler.profile_function
@PerformanceProfiler.profile_memory
async def expensive_operation(data: list):
    # Complex processing
    result = await process_large_dataset(data)
    return result
```

---

## Resumen Performance y Monitoring

| Tema | Dificultad | Complejidad | Impacto | Prioridad |
|------|------------|-------------|---------|-----------|
| Database Indexing | 5 | 5 | 5 | **CRÍTICA** |
| Query Optimization | 5 | 5 | 5 | **CRÍTICA** |
| Connection Pooling | 4 | 4 | 5 | **CRÍTICA** |
| Prometheus Metrics | 4 | 4 | 5 | **CRÍTICA** |
| Distributed Tracing | 5 | 5 | 4 | **ALTA** |
| Performance Profiling | 4 | 4 | 4 | **ALTA** |

**Próximos temas para archivo 19:**
- Load Testing (Locust, K6)
- Backup y Disaster Recovery
- Database Replication y Failover
- Blue-Green Deployments
- Feature Flags
- A/B Testing Infrastructure
