# Backend: Arquitectura Distribuida y Patrones Avanzados

## Objetivo
Patrones y soluciones para sistemas distribuidos complejos: GraphQL optimization, database sharding, distributed transactions, y stream processing.

---

## CATEGORÍA 1: GraphQL Optimization

### 1.1 N+1 Problem y DataLoader Pattern
**Dificultad:** ⭐⭐⭐⭐⭐

**Python - Strawberry GraphQL con DataLoader**

```python
from strawberry import type, field
from strawberry.dataloader import DataLoader
from typing import List, Optional
import asyncio

@type
class User:
    id: int
    name: str
    email: str

    @field
    async def posts(self, info) -> List['Post']:
        # ❌ N+1 Problem - query por cada user
        # return await Post.get_by_user_id(self.id)

        # ✅ DataLoader - batch loading
        loader = info.context['post_loader']
        return await loader.load(self.id)

    @field
    async def organization(self, info) -> Optional['Organization']:
        loader = info.context['org_loader']
        return await loader.load(self.organization_id)

@type
class Post:
    id: int
    title: str
    content: str
    user_id: int

    @field
    async def author(self, info) -> User:
        loader = info.context['user_loader']
        return await loader.load(self.user_id)

    @field
    async def comments(self, info) -> List['Comment']:
        loader = info.context['comment_loader']
        return await loader.load(self.id)

# DataLoader implementation
class UserLoader(DataLoader):
    async def load_fn(self, user_ids: List[int]) -> List[User]:
        """Batch load users - single query para múltiples IDs"""
        print(f"Loading users: {user_ids}")

        # Single query con WHERE IN
        users = await db.execute(
            "SELECT * FROM users WHERE id = ANY($1)",
            user_ids
        )

        # Crear map para lookup rápido
        user_map = {user['id']: User(**user) for user in users}

        # Retornar en el mismo orden que user_ids
        return [user_map.get(uid) for uid in user_ids]

class PostLoader(DataLoader):
    async def load_fn(self, user_ids: List[int]) -> List[List[Post]]:
        """Batch load posts por user_id"""
        print(f"Loading posts for users: {user_ids}")

        posts = await db.execute(
            "SELECT * FROM posts WHERE user_id = ANY($1)",
            user_ids
        )

        # Group by user_id
        posts_by_user = {uid: [] for uid in user_ids}
        for post in posts:
            posts_by_user[post['user_id']].append(Post(**post))

        # Retornar lista de listas
        return [posts_by_user[uid] for uid in user_ids]

class CommentLoader(DataLoader):
    async def load_fn(self, post_ids: List[int]) -> List[List['Comment']]:
        """Batch load comments por post_id"""
        print(f"Loading comments for posts: {post_ids}")

        comments = await db.execute(
            "SELECT * FROM comments WHERE post_id = ANY($1)",
            post_ids
        )

        comments_by_post = {pid: [] for pid in post_ids}
        for comment in comments:
            comments_by_post[comment['post_id']].append(Comment(**comment))

        return [comments_by_post[pid] for pid in post_ids]

# Context con DataLoaders
def get_context():
    return {
        'user_loader': UserLoader(),
        'post_loader': PostLoader(),
        'comment_loader': CommentLoader(),
        'org_loader': OrganizationLoader()
    }

# GraphQL Schema
import strawberry

@strawberry.type
class Query:
    @field
    async def users(self, info) -> List[User]:
        return await db.query(User).all()

    @field
    async def user(self, info, id: int) -> Optional[User]:
        loader = info.context['user_loader']
        return await loader.load(id)

schema = strawberry.Schema(query=Query)

# Server
from strawberry.fastapi import GraphQLRouter

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app.include_router(graphql_app, prefix="/graphql")

# Ejemplo de query optimization
"""
query {
  users {
    id
    name
    posts {              # Sin DataLoader: N queries
      id                 # Con DataLoader: 1 query
      title
      comments {         # Sin DataLoader: N*M queries
        id               # Con DataLoader: 1 query
        content
        author {         # Sin DataLoader: N*M*K queries
          name           # Con DataLoader: 1 query
        }
      }
    }
    organization {
      name
    }
  }
}

Sin DataLoader: 1 + N + N*M + N*M*K queries
Con DataLoader: 4 queries total (users, posts, comments, orgs)
"""
```

**Advanced DataLoader patterns**

```python
# 1. DataLoader con caching
class CachedUserLoader(DataLoader):
    def __init__(self, cache_ttl: int = 300):
        super().__init__()
        self.cache = {}
        self.cache_ttl = cache_ttl

    async def load_fn(self, user_ids: List[int]) -> List[User]:
        # Check cache first
        uncached_ids = []
        results = {}

        now = time.time()
        for uid in user_ids:
            if uid in self.cache:
                cached_at, user = self.cache[uid]
                if now - cached_at < self.cache_ttl:
                    results[uid] = user
                    continue
            uncached_ids.append(uid)

        # Load uncached from DB
        if uncached_ids:
            users = await db.execute(
                "SELECT * FROM users WHERE id = ANY($1)",
                uncached_ids
            )

            for user_data in users:
                user = User(**user_data)
                results[user.id] = user
                self.cache[user.id] = (now, user)

        return [results.get(uid) for uid in user_ids]

# 2. DataLoader con filtering/sorting
class FilteredPostLoader(DataLoader):
    def __init__(self, status: str = None, limit: int = None):
        super().__init__()
        self.status = status
        self.limit = limit

    async def load_fn(self, user_ids: List[int]) -> List[List[Post]]:
        query = "SELECT * FROM posts WHERE user_id = ANY($1)"
        params = [user_ids]

        if self.status:
            query += " AND status = $2"
            params.append(self.status)

        query += " ORDER BY created_at DESC"

        if self.limit:
            query += f" LIMIT {self.limit}"

        posts = await db.execute(query, *params)

        posts_by_user = {uid: [] for uid in user_ids}
        for post in posts:
            posts_by_user[post['user_id']].append(Post(**post))

        return [posts_by_user[uid] for uid in user_ids]

# Uso con argumentos
@type
class User:
    @field
    async def posts(
        self,
        info,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Post]:
        # Create loader específico con filtros
        cache_key = f"posts_{status}_{limit}"

        if cache_key not in info.context:
            info.context[cache_key] = FilteredPostLoader(status, limit)

        loader = info.context[cache_key]
        return await loader.load(self.id)

# 3. Prime DataLoader desde mutation
@strawberry.type
class Mutation:
    @field
    async def create_user(self, info, name: str, email: str) -> User:
        user_data = await db.execute(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
            name, email
        )

        user = User(**user_data[0])

        # Prime the loader con el nuevo user
        loader = info.context['user_loader']
        loader.prime(user.id, user)

        return user

# 4. DataLoader con error handling
class RobustUserLoader(DataLoader):
    async def load_fn(self, user_ids: List[int]) -> List[Optional[User]]:
        try:
            users = await db.execute(
                "SELECT * FROM users WHERE id = ANY($1)",
                user_ids
            )

            user_map = {user['id']: User(**user) for user in users}
            return [user_map.get(uid) for uid in user_ids]

        except Exception as e:
            logger.error(f"Error loading users: {e}")
            # Return None for all IDs on error
            return [None] * len(user_ids)

# 5. Composed DataLoaders
class UserWithStatsLoader(DataLoader):
    def __init__(self, user_loader: UserLoader, post_loader: PostLoader):
        super().__init__()
        self.user_loader = user_loader
        self.post_loader = post_loader

    async def load_fn(self, user_ids: List[int]) -> List[dict]:
        # Load users and posts in parallel
        users, posts_by_user = await asyncio.gather(
            self.user_loader.load_many(user_ids),
            self.post_loader.load_many(user_ids)
        )

        results = []
        for user, posts in zip(users, posts_by_user):
            results.append({
                'user': user,
                'post_count': len(posts),
                'latest_post': posts[0] if posts else None
            })

        return results
```

---

### 1.2 Query Complexity y Rate Limiting
**Dificultad:** ⭐⭐⭐⭐

```python
from strawberry.extensions import Extension
from graphql import GraphQLError

class QueryComplexityExtension(Extension):
    """Prevent expensive queries"""

    def __init__(self, max_complexity: int = 1000):
        self.max_complexity = max_complexity

    async def on_execute(self):
        # Calculate query complexity
        complexity = self._calculate_complexity(
            self.execution_context.query,
            self.execution_context.variables
        )

        if complexity > self.max_complexity:
            raise GraphQLError(
                f"Query too complex: {complexity} (max: {self.max_complexity})"
            )

        yield

    def _calculate_complexity(self, query, variables) -> int:
        """
        Assign complexity points:
        - Simple field: 1 point
        - List field: multiplier based on 'limit' or default 10
        - Nested field: multiply parent complexity
        """
        complexity = 0

        # Parse query and calculate
        # Implementation depends on query structure

        return complexity

# Ejemplo de scoring
"""
query {
  users {              # 10 points (default list size)
    posts(limit: 100) {  # 10 * 100 = 1000 points
      comments(limit: 50) { # 1000 * 50 = 50,000 points
        author {
          posts {          # Nested explosion
          }
        }
      }
    }
  }
}

Total: 50,000+ points - REJECTED
"""

# Query depth limiting
class QueryDepthExtension(Extension):
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth

    async def on_execute(self):
        depth = self._calculate_depth(self.execution_context.query)

        if depth > self.max_depth:
            raise GraphQLError(
                f"Query too deep: {depth} (max: {self.max_depth})"
            )

        yield

    def _calculate_depth(self, query) -> int:
        # Count nesting levels
        max_depth = 0
        current_depth = 0

        # Walk AST and find maximum depth
        # Implementation details...

        return max_depth

# Schema con extensions
schema = strawberry.Schema(
    query=Query,
    extensions=[
        QueryComplexityExtension(max_complexity=1000),
        QueryDepthExtension(max_depth=7)
    ]
)

# Rate limiting por usuario
class GraphQLRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def check_rate_limit(self, user_id: str, complexity: int) -> bool:
        """
        Cost-based rate limiting:
        - Each user has 10,000 complexity points per hour
        - Queries consume points based on complexity
        """
        key = f"graphql_rate_limit:{user_id}"
        current_hour = int(time.time() / 3600)
        rate_key = f"{key}:{current_hour}"

        current_usage = await self.redis.get(rate_key)
        current_usage = int(current_usage) if current_usage else 0

        max_points = 10000

        if current_usage + complexity > max_points:
            return False

        # Increment usage
        pipe = self.redis.pipeline()
        pipe.incrby(rate_key, complexity)
        pipe.expire(rate_key, 3600)
        await pipe.execute()

        return True

rate_limiter = GraphQLRateLimiter(redis_client)

@app.middleware("http")
async def graphql_rate_limit_middleware(request: Request, call_next):
    if request.url.path == "/graphql":
        user_id = request.state.user_id

        # Calculate complexity (simplified)
        complexity = estimate_query_complexity(await request.body())

        if not await rate_limiter.check_rate_limit(user_id, complexity):
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

    return await call_next(request)
```

---

## CATEGORÍA 2: Database Sharding

### 2.1 Horizontal Sharding Strategies
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from typing import List, Optional
from enum import Enum
import hashlib

class ShardingStrategy(Enum):
    HASH = "hash"
    RANGE = "range"
    DIRECTORY = "directory"

class ShardRouter:
    """Route queries to appropriate shard"""

    def __init__(self, shards: List[dict], strategy: ShardingStrategy = ShardingStrategy.HASH):
        self.shards = shards
        self.strategy = strategy
        self.num_shards = len(shards)
        self.connections = {}

    async def connect(self):
        """Initialize connections to all shards"""
        for i, shard in enumerate(self.shards):
            self.connections[i] = await create_db_connection(
                host=shard['host'],
                port=shard['port'],
                database=shard['database']
            )

    def get_shard_id(self, shard_key: any) -> int:
        """Determine which shard to use"""
        if self.strategy == ShardingStrategy.HASH:
            return self._hash_shard(shard_key)
        elif self.strategy == ShardingStrategy.RANGE:
            return self._range_shard(shard_key)
        elif self.strategy == ShardingStrategy.DIRECTORY:
            return self._directory_shard(shard_key)

    def _hash_shard(self, key: any) -> int:
        """Consistent hashing"""
        key_str = str(key)
        hash_value = int(hashlib.md5(key_str.encode()).hexdigest(), 16)
        return hash_value % self.num_shards

    def _range_shard(self, key: int) -> int:
        """Range-based sharding"""
        # Example: users 1-1M on shard 0, 1M-2M on shard 1, etc.
        users_per_shard = 1_000_000
        return min(key // users_per_shard, self.num_shards - 1)

    def _directory_shard(self, key: any) -> int:
        """Lookup-based sharding (from Redis/cache)"""
        # Query directory service to find shard
        shard_id = lookup_shard_directory(key)
        return shard_id

    def get_connection(self, shard_key: any):
        """Get database connection for shard"""
        shard_id = self.get_shard_id(shard_key)
        return self.connections[shard_id]

    async def execute(self, shard_key: any, query: str, *params):
        """Execute query on appropriate shard"""
        conn = self.get_connection(shard_key)
        return await conn.execute(query, *params)

    async def execute_on_all_shards(self, query: str, *params) -> List:
        """Execute query on all shards and merge results"""
        tasks = [
            conn.execute(query, *params)
            for conn in self.connections.values()
        ]
        results = await asyncio.gather(*tasks)

        # Merge results
        merged = []
        for result in results:
            merged.extend(result)

        return merged

# Configuración de shards
shards_config = [
    {'host': 'shard0.db.example.com', 'port': 5432, 'database': 'app_shard_0'},
    {'host': 'shard1.db.example.com', 'port': 5432, 'database': 'app_shard_1'},
    {'host': 'shard2.db.example.com', 'port': 5432, 'database': 'app_shard_2'},
    {'host': 'shard3.db.example.com', 'port': 5432, 'database': 'app_shard_3'},
]

router = ShardRouter(shards_config, strategy=ShardingStrategy.HASH)
await router.connect()

# Repository con sharding
class UserRepository:
    def __init__(self, shard_router: ShardRouter):
        self.router = shard_router

    async def get_user(self, user_id: int) -> Optional[dict]:
        """Get user from appropriate shard"""
        result = await self.router.execute(
            user_id,  # shard key
            "SELECT * FROM users WHERE id = $1",
            user_id
        )
        return result[0] if result else None

    async def create_user(self, user_id: int, name: str, email: str) -> dict:
        """Create user in appropriate shard"""
        result = await self.router.execute(
            user_id,
            """
            INSERT INTO users (id, name, email)
            VALUES ($1, $2, $3)
            RETURNING *
            """,
            user_id, name, email
        )
        return result[0]

    async def get_users_by_email(self, email: str) -> List[dict]:
        """
        Query across all shards (expensive!)
        Email is not a shard key, so we need to check all shards
        """
        return await self.router.execute_on_all_shards(
            "SELECT * FROM users WHERE email = $1",
            email
        )

    async def get_user_posts(self, user_id: int) -> List[dict]:
        """
        Posts are co-located with users using same shard key
        """
        return await self.router.execute(
            user_id,
            "SELECT * FROM posts WHERE user_id = $1",
            user_id
        )

# Cross-shard operations
class CrossShardQuery:
    def __init__(self, shard_router: ShardRouter):
        self.router = shard_router

    async def get_latest_posts(self, limit: int = 100) -> List[dict]:
        """
        Get latest posts across all shards
        Challenge: merge and sort results from multiple shards
        """

        # Query each shard for top N posts
        tasks = []
        for shard_id, conn in self.router.connections.items():
            task = conn.execute(
                """
                SELECT * FROM posts
                ORDER BY created_at DESC
                LIMIT $1
                """,
                limit
            )
            tasks.append(task)

        shard_results = await asyncio.gather(*tasks)

        # Merge results from all shards
        all_posts = []
        for posts in shard_results:
            all_posts.extend(posts)

        # Sort merged results
        all_posts.sort(key=lambda p: p['created_at'], reverse=True)

        # Return top N
        return all_posts[:limit]

    async def count_all_users(self) -> int:
        """Count users across all shards"""
        tasks = [
            conn.execute("SELECT COUNT(*) as count FROM users")
            for conn in self.router.connections.values()
        ]

        results = await asyncio.gather(*tasks)
        return sum(r[0]['count'] for r in results)

# Resharding strategy
class ReshardingManager:
    """Manage resharding when adding new shards"""

    def __init__(self, old_router: ShardRouter, new_router: ShardRouter):
        self.old_router = old_router
        self.new_router = new_router

    async def migrate_data(self):
        """
        Migrate data from old shard configuration to new
        This is complex and requires careful planning
        """

        for old_shard_id, old_conn in self.old_router.connections.items():
            # Get all data from old shard
            users = await old_conn.execute("SELECT * FROM users")

            # Redistribute to new shards
            for user in users:
                user_id = user['id']
                new_shard_id = self.new_router.get_shard_id(user_id)

                # Only migrate if going to different shard
                if self._needs_migration(old_shard_id, new_shard_id):
                    await self._migrate_user(user, new_shard_id)

    async def _migrate_user(self, user: dict, new_shard_id: int):
        """Migrate user and related data to new shard"""
        new_conn = self.new_router.connections[new_shard_id]

        async with new_conn.transaction():
            # Insert user
            await new_conn.execute(
                "INSERT INTO users (id, name, email) VALUES ($1, $2, $3)",
                user['id'], user['name'], user['email']
            )

            # Migrate related data (posts, etc.)
            # ...

    def _needs_migration(self, old_shard: int, new_shard: int) -> bool:
        # Logic to determine if data needs to move
        return old_shard != new_shard
```

---

## CATEGORÍA 3: Distributed Transactions

### 3.1 Saga Pattern (Orchestration)
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Callable, Optional
import asyncio

class SagaStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

@dataclass
class SagaStep:
    """Single step in saga"""
    name: str
    action: Callable  # Forward action
    compensation: Callable  # Rollback action
    timeout: int = 30

class SagaOrchestrator:
    """
    Orchestrate distributed transaction using Saga pattern

    Example: Order creation saga
    1. Reserve inventory
    2. Process payment
    3. Create shipment
    4. Send notification

    If any step fails, compensate all previous steps
    """

    def __init__(self, saga_id: str, steps: List[SagaStep]):
        self.saga_id = saga_id
        self.steps = steps
        self.status = SagaStatus.PENDING
        self.completed_steps = []
        self.current_step_index = 0

    async def execute(self, context: dict) -> dict:
        """Execute saga"""
        self.status = SagaStatus.IN_PROGRESS

        try:
            # Execute each step
            for i, step in enumerate(self.steps):
                self.current_step_index = i

                logger.info(
                    f"Saga {self.saga_id}: Executing step {step.name}",
                    saga_id=self.saga_id,
                    step=step.name
                )

                # Execute with timeout
                try:
                    result = await asyncio.wait_for(
                        step.action(context),
                        timeout=step.timeout
                    )

                    # Store result in context
                    context[f"{step.name}_result"] = result
                    self.completed_steps.append(step)

                    # Persist saga state
                    await self._save_state(context)

                except asyncio.TimeoutError:
                    logger.error(
                        f"Saga {self.saga_id}: Step {step.name} timed out"
                    )
                    raise SagaTimeoutError(step.name)

                except Exception as e:
                    logger.error(
                        f"Saga {self.saga_id}: Step {step.name} failed: {e}"
                    )
                    raise SagaStepError(step.name, str(e))

            self.status = SagaStatus.COMPLETED
            await self._save_state(context)

            return context

        except Exception as e:
            # Compensate completed steps
            await self._compensate(context)
            raise

    async def _compensate(self, context: dict):
        """Rollback completed steps in reverse order"""
        self.status = SagaStatus.COMPENSATING

        logger.info(
            f"Saga {self.saga_id}: Starting compensation",
            completed_steps=len(self.completed_steps)
        )

        # Reverse order
        for step in reversed(self.completed_steps):
            try:
                logger.info(
                    f"Saga {self.saga_id}: Compensating {step.name}"
                )

                await asyncio.wait_for(
                    step.compensation(context),
                    timeout=step.timeout
                )

            except Exception as e:
                logger.error(
                    f"Saga {self.saga_id}: Compensation failed for {step.name}: {e}"
                )
                # Continue compensating other steps even if one fails

        self.status = SagaStatus.FAILED
        await self._save_state(context)

    async def _save_state(self, context: dict):
        """Persist saga state for recovery"""
        state = {
            'saga_id': self.saga_id,
            'status': self.status.value,
            'current_step': self.current_step_index,
            'completed_steps': [s.name for s in self.completed_steps],
            'context': context
        }

        await db.execute(
            """
            INSERT INTO saga_state (saga_id, state, updated_at)
            VALUES ($1, $2, NOW())
            ON CONFLICT (saga_id)
            DO UPDATE SET state = $2, updated_at = NOW()
            """,
            self.saga_id,
            json.dumps(state)
        )

class SagaStepError(Exception):
    def __init__(self, step_name: str, error: str):
        self.step_name = step_name
        self.error = error

class SagaTimeoutError(Exception):
    def __init__(self, step_name: str):
        self.step_name = step_name

# Example: Order Creation Saga
class OrderSaga:
    def __init__(
        self,
        inventory_service,
        payment_service,
        shipping_service,
        notification_service
    ):
        self.inventory = inventory_service
        self.payment = payment_service
        self.shipping = shipping_service
        self.notification = notification_service

    async def create_order(self, order_data: dict) -> dict:
        saga_id = f"order_{order_data['order_id']}"

        steps = [
            SagaStep(
                name="reserve_inventory",
                action=self._reserve_inventory,
                compensation=self._release_inventory
            ),
            SagaStep(
                name="process_payment",
                action=self._process_payment,
                compensation=self._refund_payment
            ),
            SagaStep(
                name="create_shipment",
                action=self._create_shipment,
                compensation=self._cancel_shipment
            ),
            SagaStep(
                name="send_notification",
                action=self._send_notification,
                compensation=self._send_cancellation_notification
            )
        ]

        orchestrator = SagaOrchestrator(saga_id, steps)

        context = {
            'order_id': order_data['order_id'],
            'user_id': order_data['user_id'],
            'items': order_data['items'],
            'payment': order_data['payment'],
            'shipping_address': order_data['shipping_address']
        }

        try:
            result = await orchestrator.execute(context)
            return {
                'success': True,
                'order_id': order_data['order_id'],
                'payment_id': result['process_payment_result']['payment_id'],
                'shipment_id': result['create_shipment_result']['shipment_id']
            }

        except Exception as e:
            logger.error(f"Order saga failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    # Forward actions
    async def _reserve_inventory(self, context: dict) -> dict:
        reservation = await self.inventory.reserve(
            items=context['items'],
            order_id=context['order_id']
        )
        return {'reservation_id': reservation.id}

    async def _process_payment(self, context: dict) -> dict:
        payment = await self.payment.charge(
            user_id=context['user_id'],
            amount=context['payment']['amount'],
            method=context['payment']['method'],
            order_id=context['order_id']
        )
        return {'payment_id': payment.id}

    async def _create_shipment(self, context: dict) -> dict:
        shipment = await self.shipping.create(
            order_id=context['order_id'],
            items=context['items'],
            address=context['shipping_address']
        )
        return {'shipment_id': shipment.id}

    async def _send_notification(self, context: dict) -> dict:
        await self.notification.send(
            user_id=context['user_id'],
            type='order_confirmed',
            data={
                'order_id': context['order_id'],
                'payment_id': context['process_payment_result']['payment_id']
            }
        )
        return {}

    # Compensations
    async def _release_inventory(self, context: dict):
        reservation_id = context['reserve_inventory_result']['reservation_id']
        await self.inventory.release(reservation_id)

    async def _refund_payment(self, context: dict):
        payment_id = context['process_payment_result']['payment_id']
        await self.payment.refund(payment_id)

    async def _cancel_shipment(self, context: dict):
        shipment_id = context['create_shipment_result']['shipment_id']
        await self.shipping.cancel(shipment_id)

    async def _send_cancellation_notification(self, context: dict):
        await self.notification.send(
            user_id=context['user_id'],
            type='order_cancelled',
            data={'order_id': context['order_id']}
        )

# Usage
order_saga = OrderSaga(
    inventory_service=InventoryService(),
    payment_service=PaymentService(),
    shipping_service=ShippingService(),
    notification_service=NotificationService()
)

result = await order_saga.create_order({
    'order_id': 'ORD-12345',
    'user_id': 123,
    'items': [
        {'product_id': 'PROD-1', 'quantity': 2},
        {'product_id': 'PROD-2', 'quantity': 1}
    ],
    'payment': {
        'amount': 99.99,
        'method': 'credit_card'
    },
    'shipping_address': {
        'street': '123 Main St',
        'city': 'San Francisco',
        'zip': '94102'
    }
})
```

---

### 3.2 Two-Phase Commit (2PC)
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from enum import Enum
from typing import List, Dict
import asyncio

class ParticipantState(Enum):
    READY = "ready"
    PREPARED = "prepared"
    COMMITTED = "committed"
    ABORTED = "aborted"

class TransactionParticipant:
    """Single participant in distributed transaction"""

    def __init__(self, name: str, connection):
        self.name = name
        self.connection = connection
        self.state = ParticipantState.READY

    async def prepare(self) -> bool:
        """Phase 1: Prepare to commit"""
        try:
            # Begin transaction and acquire locks
            await self.connection.execute("BEGIN")

            # Execute transaction operations
            # Lock resources needed
            # Flush to disk but don't commit

            self.state = ParticipantState.PREPARED
            return True

        except Exception as e:
            logger.error(f"Participant {self.name} prepare failed: {e}")
            await self.abort()
            return False

    async def commit(self):
        """Phase 2: Commit transaction"""
        try:
            await self.connection.execute("COMMIT")
            self.state = ParticipantState.COMMITTED

        except Exception as e:
            logger.error(f"Participant {self.name} commit failed: {e}")
            raise

    async def abort(self):
        """Rollback transaction"""
        try:
            await self.connection.execute("ROLLBACK")
            self.state = ParticipantState.ABORTED

        except Exception as e:
            logger.error(f"Participant {self.name} abort failed: {e}")

class TwoPhaseCommitCoordinator:
    """
    Coordinate 2PC across multiple databases

    Limitations:
    - Blocking protocol (not ideal for high availability)
    - Coordinator is single point of failure
    - Use Saga pattern for most microservices scenarios
    """

    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id
        self.participants: List[TransactionParticipant] = []

    def add_participant(self, participant: TransactionParticipant):
        self.participants.append(participant)

    async def execute(self) -> bool:
        """Execute 2PC protocol"""

        logger.info(
            f"2PC {self.transaction_id}: Starting with {len(self.participants)} participants"
        )

        # Phase 1: Prepare
        prepare_success = await self._prepare_phase()

        if not prepare_success:
            # At least one participant can't commit
            logger.warning(f"2PC {self.transaction_id}: Prepare phase failed, aborting")
            await self._abort_all()
            return False

        # Phase 2: Commit
        try:
            await self._commit_phase()
            logger.info(f"2PC {self.transaction_id}: Successfully committed")
            return True

        except Exception as e:
            logger.error(f"2PC {self.transaction_id}: Commit phase failed: {e}")
            # This is bad - some may have committed, some not
            # Need manual intervention or recovery protocol
            await self._handle_commit_failure()
            return False

    async def _prepare_phase(self) -> bool:
        """Phase 1: Ask all participants to prepare"""

        # Send prepare request to all participants
        prepare_tasks = [
            participant.prepare()
            for participant in self.participants
        ]

        results = await asyncio.gather(*prepare_tasks, return_exceptions=True)

        # Check if all prepared successfully
        for i, result in enumerate(results):
            if isinstance(result, Exception) or not result:
                logger.error(
                    f"Participant {self.participants[i].name} failed to prepare"
                )
                return False

        return True

    async def _commit_phase(self):
        """Phase 2: Tell all participants to commit"""

        commit_tasks = [
            participant.commit()
            for participant in self.participants
        ]

        await asyncio.gather(*commit_tasks)

    async def _abort_all(self):
        """Tell all participants to abort"""

        abort_tasks = [
            participant.abort()
            for participant in self.participants
        ]

        await asyncio.gather(*abort_tasks, return_exceptions=True)

    async def _handle_commit_failure(self):
        """
        Handle the case where commit phase partially failed
        This requires careful recovery logic
        """

        # Check state of each participant
        for participant in self.participants:
            if participant.state == ParticipantState.PREPARED:
                # Still waiting to commit - try again
                try:
                    await participant.commit()
                except:
                    # Log for manual recovery
                    logger.critical(
                        f"2PC {self.transaction_id}: "
                        f"Participant {participant.name} stuck in prepared state"
                    )

# Example usage
async def transfer_money_2pc(from_user_id: int, to_user_id: int, amount: float):
    """
    Transfer money between users potentially on different database shards
    """

    transaction_id = f"transfer_{from_user_id}_{to_user_id}_{int(time.time())}"
    coordinator = TwoPhaseCommitCoordinator(transaction_id)

    # Get connections to appropriate shards
    from_conn = shard_router.get_connection(from_user_id)
    to_conn = shard_router.get_connection(to_user_id)

    # Create participants
    from_participant = TransactionParticipant("from_account", from_conn)
    to_participant = TransactionParticipant("to_account", to_conn)

    # Setup transactions on each participant
    await from_conn.execute("BEGIN")
    await from_conn.execute(
        "UPDATE accounts SET balance = balance - $1 WHERE user_id = $2",
        amount, from_user_id
    )

    await to_conn.execute("BEGIN")
    await to_conn.execute(
        "UPDATE accounts SET balance = balance + $1 WHERE user_id = $2",
        amount, to_user_id
    )

    # Add to coordinator
    coordinator.add_participant(from_participant)
    coordinator.add_participant(to_participant)

    # Execute 2PC
    success = await coordinator.execute()

    return success
```

---

Continúa con más categorías...

---

## CATEGORÍA 4: Webhooks Management

### 4.1 Reliable Webhook Delivery
**Dificultad:** ⭐⭐⭐⭐

```python
import httpx
from typing import Optional
from datetime import datetime, timedelta
import hmac
import hashlib

class WebhookDelivery:
    """
    Reliable webhook delivery with:
    - Retry with exponential backoff
    - Signature verification
    - Dead letter queue
    - Delivery tracking
    """

    def __init__(self, redis_client, db):
        self.redis = redis_client
        self.db = db
        self.max_retries = 5
        self.initial_delay = 1  # seconds

    async def send(
        self,
        url: str,
        event_type: str,
        payload: dict,
        secret: str,
        webhook_id: str = None
    ) -> bool:
        """Send webhook with retry logic"""

        webhook_id = webhook_id or str(uuid.uuid4())

        # Store webhook attempt
        await self._store_webhook(webhook_id, url, event_type, payload)

        # Generate signature
        signature = self._generate_signature(payload, secret)

        # Try sending with retries
        for attempt in range(self.max_retries):
            try:
                delay = self.initial_delay * (2 ** attempt)

                if attempt > 0:
                    logger.info(
                        f"Webhook {webhook_id}: Retry attempt {attempt} after {delay}s"
                    )
                    await asyncio.sleep(delay)

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url,
                        json=payload,
                        headers={
                            'Content-Type': 'application/json',
                            'X-Webhook-Signature': signature,
                            'X-Webhook-ID': webhook_id,
                            'X-Webhook-Event': event_type,
                            'X-Webhook-Timestamp': str(int(time.time()))
                        },
                        timeout=10.0
                    )

                    if response.status_code < 300:
                        # Success
                        await self._mark_delivered(webhook_id, response.status_code)
                        return True

                    elif response.status_code < 500:
                        # Client error - don't retry
                        await self._mark_failed(
                            webhook_id,
                            f"Client error: {response.status_code}"
                        )
                        return False

                    # Server error - will retry

            except httpx.TimeoutException:
                logger.warning(f"Webhook {webhook_id}: Timeout on attempt {attempt}")

            except Exception as e:
                logger.error(f"Webhook {webhook_id}: Error on attempt {attempt}: {e}")

        # All retries failed
        await self._send_to_dlq(webhook_id, url, event_type, payload)
        return False

    def _generate_signature(self, payload: dict, secret: str) -> str:
        """Generate HMAC signature for webhook"""
        message = json.dumps(payload, sort_keys=True).encode()
        signature = hmac.new(
            secret.encode(),
            message,
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"

    async def _store_webhook(self, webhook_id: str, url: str, event_type: str, payload: dict):
        """Store webhook attempt in database"""
        await self.db.execute(
            """
            INSERT INTO webhooks (id, url, event_type, payload, status, created_at)
            VALUES ($1, $2, $3, $4, 'pending', NOW())
            """,
            webhook_id, url, event_type, json.dumps(payload)
        )

    async def _mark_delivered(self, webhook_id: str, status_code: int):
        await self.db.execute(
            """
            UPDATE webhooks
            SET status = 'delivered', status_code = $2, delivered_at = NOW()
            WHERE id = $1
            """,
            webhook_id, status_code
        )

    async def _mark_failed(self, webhook_id: str, error: str):
        await self.db.execute(
            """
            UPDATE webhooks
            SET status = 'failed', error = $2, failed_at = NOW()
            WHERE id = $1
            """,
            webhook_id, error
        )

    async def _send_to_dlq(self, webhook_id: str, url: str, event_type: str, payload: dict):
        """Send failed webhook to dead letter queue"""
        logger.error(f"Webhook {webhook_id}: Sending to DLQ after all retries failed")

        await self.redis.lpush(
            'webhooks:dlq',
            json.dumps({
                'webhook_id': webhook_id,
                'url': url,
                'event_type': event_type,
                'payload': payload,
                'failed_at': datetime.utcnow().isoformat()
            })
        )

        await self._mark_failed(webhook_id, "Max retries exceeded")

# Webhook subscription management
class WebhookManager:
    def __init__(self, db, webhook_delivery: WebhookDelivery):
        self.db = db
        self.delivery = webhook_delivery

    async def subscribe(
        self,
        user_id: int,
        url: str,
        events: List[str],
        secret: str
    ) -> dict:
        """Create webhook subscription"""

        subscription = await self.db.execute(
            """
            INSERT INTO webhook_subscriptions
            (user_id, url, events, secret, active, created_at)
            VALUES ($1, $2, $3, $4, true, NOW())
            RETURNING id
            """,
            user_id, url, events, secret
        )

        return {
            'subscription_id': subscription[0]['id'],
            'url': url,
            'events': events
        }

    async def trigger_event(self, event_type: str, payload: dict):
        """Trigger webhook event to all subscribers"""

        # Get all subscriptions for this event
        subscriptions = await self.db.execute(
            """
            SELECT id, user_id, url, secret
            FROM webhook_subscriptions
            WHERE active = true AND $1 = ANY(events)
            """,
            event_type
        )

        # Send to all subscribers
        tasks = []
        for sub in subscriptions:
            task = self.delivery.send(
                url=sub['url'],
                event_type=event_type,
                payload=payload,
                secret=sub['secret']
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)

# Webhook receiver (for testing/validation)
@app.post("/webhooks/receiver")
async def receive_webhook(request: Request):
    """Example webhook receiver"""

    # Verify signature
    signature = request.headers.get('X-Webhook-Signature')
    webhook_id = request.headers.get('X-Webhook-ID')
    event_type = request.headers.get('X-Webhook-Event')

    payload = await request.json()

    # Verify HMAC signature
    expected_signature = generate_signature(payload, WEBHOOK_SECRET)

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Process webhook
    logger.info(f"Received webhook {webhook_id}: {event_type}")

    # Return 200 to acknowledge
    return {"status": "received"}
```

---

## Resumen de Arquitectura Distribuida

| Tema | Dificultad | Complejidad | Impacto | Prioridad |
|------|------------|-------------|---------|-----------|
| GraphQL N+1 Problem | 5 | 5 | 5 | **CRÍTICA** |
| Database Sharding | 5 | 5 | 5 | **CRÍTICA** |
| Saga Pattern | 5 | 5 | 5 | **CRÍTICA** |
| Two-Phase Commit | 5 | 5 | 3 | **MEDIA** |
| Webhook Reliability | 4 | 4 | 4 | **ALTA** |
| Query Complexity Limiting | 4 | 3 | 4 | **ALTA** |

**El siguiente archivo continuará con:**
- Apache Kafka y Stream Processing
- Event Sourcing y CQRS
- API Gateway patterns
- Service Discovery y Health Checks
- Chaos Engineering
- Security avanzada (OAuth2 flows, JWT rotation, mTLS)
