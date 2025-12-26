# Arquitectura Técnica Avanzada 2026 - Parte 3: Deployment & Migrations

## Objetivo
Patrones avanzados de deployment, feature flags, zero-downtime migrations, y secrets management para sistemas en producción.

---

## CATEGORÍA 1: Feature Flags y Progressive Delivery

### 1.1 Feature Flags Architecture
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Feature flags desacoplan deploy de release. Permiten progressive rollout, A/B testing, y kill switches.

**Niveles de Feature Flags:**

```
┌──────────────────────────────────────────────────┐
│         FEATURE FLAG MATURITY LEVELS             │
├──────────────────────────────────────────────────┤
│                                                  │
│ NIVEL 1: Static Flags (Environment Variables)   │
│ ✅ Simple                                        │
│ ❌ Require redeploy para cambios                 │
│ ❌ No runtime control                            │
│                                                  │
│ NIVEL 2: Database Flags                         │
│ ✅ Runtime toggles (no redeploy)                │
│ ❌ No percentage rollout                         │
│ ❌ No user targeting                             │
│                                                  │
│ NIVEL 3: Feature Flag Service (LaunchDarkly)    │
│ ✅ Percentage rollout                            │
│ ✅ User targeting                                │
│ ✅ A/B testing                                   │
│ ✅ Analytics integration                         │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Implementación: Feature Flag Service con Redis**

```python
# Feature Flag Service Implementation
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum
import hashlib
import json

class RolloutStrategy(Enum):
    ALL = "all"  # 100% rollout
    PERCENTAGE = "percentage"  # % of users
    USER_LIST = "user_list"  # Specific users
    USER_ATTRIBUTE = "user_attribute"  # e.g., country=US
    GRADUAL = "gradual"  # Time-based gradual rollout

@dataclass
class FeatureFlagConfig:
    """Feature flag configuration"""
    name: str
    enabled: bool
    strategy: RolloutStrategy

    # For percentage rollout
    percentage: Optional[int] = None

    # For user targeting
    user_ids: Optional[List[str]] = None

    # For attribute targeting
    attributes: Optional[Dict[str, Any]] = None

    # For gradual rollout
    start_percentage: Optional[int] = None
    end_percentage: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class FeatureFlagService:
    """
    Production-grade feature flag service

    Features:
    - Percentage rollout (consistent hashing)
    - User targeting
    - Attribute-based targeting
    - Gradual rollout over time
    - Redis caching (L1 + L2)
    - Fallback to defaults if Redis down
    """

    def __init__(self, redis: Redis, db: AsyncSession):
        self.redis = redis
        self.db = db
        self.local_cache = {}  # L1 cache
        self.cache_ttl = 60  # 1 minute

    async def is_enabled(
        self,
        flag_name: str,
        user_id: Optional[str] = None,
        attributes: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if feature is enabled for user

        Evaluation order:
        1. Check kill switch (emergency disable)
        2. Check user whitelist
        3. Check percentage rollout
        4. Check attribute targeting
        5. Default to disabled
        """

        # Get flag config (cached)
        config = await self._get_flag_config(flag_name)

        if not config or not config.enabled:
            return False

        # Strategy: ALL
        if config.strategy == RolloutStrategy.ALL:
            return True

        # Strategy: USER_LIST
        if config.strategy == RolloutStrategy.USER_LIST:
            if not user_id or not config.user_ids:
                return False
            return user_id in config.user_ids

        # Strategy: PERCENTAGE
        if config.strategy == RolloutStrategy.PERCENTAGE:
            if not user_id:
                return False
            return self._is_in_percentage_rollout(
                flag_name,
                user_id,
                config.percentage
            )

        # Strategy: USER_ATTRIBUTE
        if config.strategy == RolloutStrategy.USER_ATTRIBUTE:
            if not attributes or not config.attributes:
                return False
            return self._matches_attributes(attributes, config.attributes)

        # Strategy: GRADUAL
        if config.strategy == RolloutStrategy.GRADUAL:
            if not user_id:
                return False
            current_percentage = self._calculate_gradual_percentage(config)
            return self._is_in_percentage_rollout(
                flag_name,
                user_id,
                current_percentage
            )

        return False

    def _is_in_percentage_rollout(
        self,
        flag_name: str,
        user_id: str,
        percentage: int
    ) -> bool:
        """
        Consistent hashing for percentage rollout

        Ensures same user always gets same result (consistency)
        Distribution is uniform (fairness)
        """
        # Hash user_id + flag_name for consistency
        hash_input = f"{flag_name}:{user_id}".encode()
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)

        # Map to 0-100
        bucket = hash_value % 100

        return bucket < percentage

    def _matches_attributes(
        self,
        user_attrs: Dict[str, Any],
        required_attrs: Dict[str, Any]
    ) -> bool:
        """Check if user attributes match requirements"""
        for key, value in required_attrs.items():
            if key not in user_attrs:
                return False

            # Support operators: eq, in, gt, lt
            if isinstance(value, dict):
                operator = value.get("op")
                operand = value.get("value")

                if operator == "eq":
                    if user_attrs[key] != operand:
                        return False
                elif operator == "in":
                    if user_attrs[key] not in operand:
                        return False
                elif operator == "gt":
                    if user_attrs[key] <= operand:
                        return False
                elif operator == "lt":
                    if user_attrs[key] >= operand:
                        return False
            else:
                # Simple equality
                if user_attrs[key] != value:
                    return False

        return True

    def _calculate_gradual_percentage(self, config: FeatureFlagConfig) -> int:
        """
        Calculate current percentage for gradual rollout

        Example: 0% to 100% over 7 days
        Day 1: 0%
        Day 2: ~14%
        Day 3: ~28%
        ...
        Day 7: 100%
        """
        now = datetime.utcnow()

        if now < config.start_time:
            return config.start_percentage

        if now >= config.end_time:
            return config.end_percentage

        # Linear interpolation
        total_duration = (config.end_time - config.start_time).total_seconds()
        elapsed = (now - config.start_time).total_seconds()
        progress = elapsed / total_duration

        percentage_range = config.end_percentage - config.start_percentage
        current = config.start_percentage + (percentage_range * progress)

        return int(current)

    async def _get_flag_config(self, flag_name: str) -> Optional[FeatureFlagConfig]:
        """Get flag config with L1 + L2 caching"""

        # L1: Local cache
        if flag_name in self.local_cache:
            cached_data, cached_at = self.local_cache[flag_name]
            if (datetime.utcnow() - cached_at).seconds < self.cache_ttl:
                return cached_data

        # L2: Redis cache
        cache_key = f"feature_flag:{flag_name}"
        cached_json = await self.redis.get(cache_key)

        if cached_json:
            config_dict = json.loads(cached_json)
            config = FeatureFlagConfig(**config_dict)

            # Populate L1
            self.local_cache[flag_name] = (config, datetime.utcnow())
            return config

        # Cache miss: Load from DB
        stmt = select(FeatureFlag).where(FeatureFlag.name == flag_name)
        result = await self.db.execute(stmt)
        flag = result.scalar_one_or_none()

        if not flag:
            return None

        config = FeatureFlagConfig(
            name=flag.name,
            enabled=flag.enabled,
            strategy=RolloutStrategy(flag.strategy),
            percentage=flag.percentage,
            user_ids=flag.user_ids,
            attributes=flag.attributes,
            start_percentage=flag.start_percentage,
            end_percentage=flag.end_percentage,
            start_time=flag.start_time,
            end_time=flag.end_time
        )

        # Cache in Redis
        await self.redis.setex(
            cache_key,
            self.cache_ttl,
            json.dumps(config.__dict__, default=str)
        )

        # Cache locally
        self.local_cache[flag_name] = (config, datetime.utcnow())

        return config

    async def update_flag(self, flag_name: str, updates: Dict[str, Any]):
        """
        Update feature flag

        Invalidates cache immediately
        """
        stmt = (
            update(FeatureFlag)
            .where(FeatureFlag.name == flag_name)
            .values(**updates)
        )
        await self.db.execute(stmt)
        await self.db.commit()

        # Invalidate caches
        await self.redis.delete(f"feature_flag:{flag_name}")
        if flag_name in self.local_cache:
            del self.local_cache[flag_name]


# Usage in Application Code
feature_flags = FeatureFlagService(redis, db)

@app.get("/products/{product_id}")
async def get_product(
    product_id: int,
    user: User = Depends(get_current_user)
):
    """
    Feature flag usage example
    """

    # Check feature flag
    new_recommendation_engine_enabled = await feature_flags.is_enabled(
        "new_recommendation_engine",
        user_id=str(user.id),
        attributes={
            "country": user.country,
            "subscription_tier": user.subscription_tier,
            "account_age_days": (datetime.utcnow() - user.created_at).days
        }
    )

    product = await get_product_from_db(product_id)

    if new_recommendation_engine_enabled:
        # New ML-based recommendations
        product.recommendations = await ml_recommendation_service.get_recommendations(
            user_id=user.id,
            product_id=product_id
        )
    else:
        # Old rule-based recommendations
        product.recommendations = await legacy_recommendation_service.get_recommendations(
            product_id
        )

    return product


# Admin API: Manage Feature Flags
@app.post("/admin/feature-flags/{flag_name}/rollout")
async def start_gradual_rollout(
    flag_name: str,
    rollout_config: GradualRolloutConfig
):
    """
    Start gradual rollout

    Example: 0% to 100% over 7 days
    POST /admin/feature-flags/new_checkout/rollout
    {
      "start_percentage": 0,
      "end_percentage": 100,
      "duration_hours": 168  // 7 days
    }
    """
    now = datetime.utcnow()
    end_time = now + timedelta(hours=rollout_config.duration_hours)

    await feature_flags.update_flag(flag_name, {
        "enabled": True,
        "strategy": "gradual",
        "start_percentage": rollout_config.start_percentage,
        "end_percentage": rollout_config.end_percentage,
        "start_time": now,
        "end_time": end_time
    })

    return {
        "status": "rollout_started",
        "current_percentage": rollout_config.start_percentage,
        "end_time": end_time
    }

@app.post("/admin/feature-flags/{flag_name}/kill-switch")
async def emergency_disable(flag_name: str):
    """
    Emergency kill switch

    Immediately disable feature for all users
    """
    await feature_flags.update_flag(flag_name, {
        "enabled": False
    })

    return {"status": "feature_disabled"}
```

**Feature Flag Best Practices**

```python
"""
┌──────────────────────────────────────────────────┐
│         FEATURE FLAG BEST PRACTICES              │
├──────────────────────────────────────────────────┤
│                                                  │
│ 1. NAMING CONVENTIONS                            │
│    ✅ use_new_checkout_flow                      │
│    ✅ enable_ml_recommendations                  │
│    ❌ flag_1, temp_flag                          │
│                                                  │
│ 2. CLEANUP                                       │
│    - Remove flags after full rollout             │
│    - Max lifetime: 3-6 months                    │
│    - Track flag age in monitoring                │
│                                                  │
│ 3. TESTING                                       │
│    - Test both ON and OFF states                │
│    - Integration tests with flags                │
│    - Don't use flags in unit tests               │
│                                                  │
│ 4. TYPES OF FLAGS                                │
│    - Release flags (temporary)                   │
│    - Ops flags (permanent, circuit breaker)      │
│    - Experiment flags (A/B testing)              │
│    - Permission flags (entitlements)             │
│                                                  │
│ 5. ANTI-PATTERNS                                 │
│    ❌ Nested flags (if flag1 and flag2)          │
│    ❌ Business logic in flag service             │
│    ❌ Flags that never get removed               │
│                                                  │
└──────────────────────────────────────────────────┘
"""
```

---

## CATEGORÍA 2: Zero-Downtime Database Migrations

### 2.1 Expand-Contract Pattern
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Cambiar schema sin downtime requiere múltiples deploys. Expand-Contract permite migrations sin interrumpir servicio.

**Pattern: Renombrar Columna Sin Downtime**

```python
# PROBLEMA: Renombrar users.name -> users.full_name SIN DOWNTIME
"""
❌ NAIVE APPROACH (CAUSA DOWNTIME):

1. ALTER TABLE users RENAME COLUMN name TO full_name
2. Deploy código nuevo

= Durante deploy: ERROR (código nuevo busca full_name, pero no existe todavía)
"""

# ✅ EXPAND-CONTRACT PATTERN (ZERO DOWNTIME):

# PHASE 1: EXPAND - Add new column (deploy 1)
"""
Migration:
  ALTER TABLE users ADD COLUMN full_name VARCHAR(255);
  UPDATE users SET full_name = name WHERE full_name IS NULL;
  CREATE INDEX idx_users_full_name ON users(full_name);

Code (backward compatible):
  - Writes go to BOTH columns
  - Reads from OLD column (name)
"""

class UserService:
    async def create_user(self, username: str, name: str):
        """Phase 1: Write to both columns"""
        user = User(
            username=username,
            name=name,           # Old column
            full_name=name       # New column (duplicated)
        )
        self.db.add(user)
        await self.db.commit()

    async def update_user(self, user_id: int, name: str):
        """Phase 1: Update both columns"""
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(
                name=name,       # Old column
                full_name=name   # New column
            )
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_user(self, user_id: int) -> User:
        """Phase 1: Read from OLD column"""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one()

        # Populate new column if empty (backfill during read)
        if not user.full_name and user.name:
            user.full_name = user.name
            await self.db.commit()

        return user


# PHASE 2: MIGRATE - Backfill data
"""
Background job (no deploy required):
  UPDATE users SET full_name = name WHERE full_name IS NULL;

Verify:
  SELECT COUNT(*) FROM users WHERE full_name IS NULL;  -- Should be 0
"""

async def backfill_full_name():
    """
    Background job: Backfill data in batches

    Run without blocking application
    """
    batch_size = 1000
    offset = 0

    while True:
        stmt = (
            update(User)
            .where(User.full_name.is_(None))
            .where(User.name.isnot(None))
            .values(full_name=User.name)
            .limit(batch_size)
        )

        result = await db.execute(stmt)
        await db.commit()

        rows_updated = result.rowcount

        logger.info(
            "backfill_progress",
            rows_updated=rows_updated,
            offset=offset
        )

        if rows_updated == 0:
            break

        offset += batch_size
        await asyncio.sleep(1)  # Rate limit


# PHASE 3: CONTRACT - Switch reads (deploy 2)
"""
Code:
  - Writes still go to BOTH columns
  - Reads from NEW column (full_name)
"""

class UserService:
    async def get_user(self, user_id: int) -> User:
        """Phase 3: Read from NEW column"""
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one()

        # Still backfill if needed (defensive)
        if not user.full_name and user.name:
            user.full_name = user.name
            await self.db.commit()

        return user


# PHASE 4: CLEANUP - Remove old column (deploy 3)
"""
Migration:
  ALTER TABLE users DROP COLUMN name;

Code:
  - Remove all references to old column
"""

class UserService:
    async def create_user(self, username: str, full_name: str):
        """Phase 4: Only write to new column"""
        user = User(
            username=username,
            full_name=full_name  # Only new column
        )
        self.db.add(user)
        await self.db.commit()


# Timeline:
"""
Day 1: Deploy 1 (EXPAND)
  - Add full_name column
  - Write to both columns
  - Read from old column
  ✅ Zero downtime

Day 2-3: Backfill
  - Background job fills full_name
  - Verify 100% backfilled
  ✅ Zero downtime

Day 4: Deploy 2 (CONTRACT - Switch reads)
  - Read from new column
  - Still write to both (safety)
  ✅ Zero downtime

Day 7: Deploy 3 (CLEANUP)
  - Drop old column
  - Remove dual writes
  ✅ Zero downtime

Total: 3 deploys over 7 days, ZERO DOWNTIME
"""
```

**Pattern: Add NOT NULL Constraint**

```python
# PROBLEMA: Add NOT NULL constraint to users.email
"""
❌ NAIVE APPROACH:
  ALTER TABLE users ALTER COLUMN email SET NOT NULL;

= BLOCKS table for duration of table scan (seconds to minutes)
"""

# ✅ SAFE APPROACH:

# PHASE 1: Add CHECK constraint (NOT VALIDATED)
"""
-- PostgreSQL 12+
ALTER TABLE users ADD CONSTRAINT email_not_null
  CHECK (email IS NOT NULL) NOT VALID;

-- This is FAST (no table scan)
-- New rows are validated
-- Old rows are NOT validated yet
"""

# PHASE 2: Backfill NULLs
"""
UPDATE users SET email = 'unknown@example.com'
WHERE email IS NULL;
"""

# PHASE 3: Validate constraint
"""
-- This scans table but does NOT block writes (PostgreSQL 12+)
ALTER TABLE users VALIDATE CONSTRAINT email_not_null;
"""

# PHASE 4: Add NOT NULL (now safe, instant)
"""
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
ALTER TABLE users DROP CONSTRAINT email_not_null;
"""

# Python helper
async def safe_add_not_null_constraint(
    table_name: str,
    column_name: str,
    default_value: Any
):
    """
    Add NOT NULL constraint without blocking

    Steps:
    1. Add CHECK NOT VALID
    2. Backfill NULLs
    3. Validate CHECK
    4. Add NOT NULL
    """
    constraint_name = f"{column_name}_not_null"

    # Step 1: Add CHECK NOT VALID
    await db.execute(text(f"""
        ALTER TABLE {table_name}
        ADD CONSTRAINT {constraint_name}
        CHECK ({column_name} IS NOT NULL) NOT VALID
    """))
    await db.commit()

    logger.info(f"Added CHECK constraint (not validated)")

    # Step 2: Backfill
    batch_size = 1000
    while True:
        result = await db.execute(text(f"""
            UPDATE {table_name}
            SET {column_name} = :default_value
            WHERE {column_name} IS NULL
            LIMIT {batch_size}
        """), {"default_value": default_value})

        await db.commit()

        if result.rowcount == 0:
            break

        logger.info(f"Backfilled {result.rowcount} rows")
        await asyncio.sleep(0.5)

    # Step 3: Validate
    await db.execute(text(f"""
        ALTER TABLE {table_name}
        VALIDATE CONSTRAINT {constraint_name}
    """))
    await db.commit()

    logger.info(f"Validated CHECK constraint")

    # Step 4: Add NOT NULL
    await db.execute(text(f"""
        ALTER TABLE {table_name}
        ALTER COLUMN {column_name} SET NOT NULL
    """))
    await db.execute(text(f"""
        ALTER TABLE {table_name}
        DROP CONSTRAINT {constraint_name}
    """))
    await db.commit()

    logger.info(f"Added NOT NULL constraint")
```

**Pattern: Add Index Without Blocking**

```python
# PROBLEMA: Add index blocks writes
"""
❌ BLOCKING:
  CREATE INDEX idx_users_email ON users(email);

= Acquires SHARE lock, blocks INSERTs/UPDATEs
"""

# ✅ NON-BLOCKING (PostgreSQL):
"""
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

- Does NOT block writes
- Takes longer than regular CREATE INDEX
- Can fail if there are errors (retry needed)
"""

# Python helper
async def create_index_safely(
    table_name: str,
    column_name: str,
    index_name: Optional[str] = None
):
    """
    Create index without blocking writes

    PostgreSQL: CREATE INDEX CONCURRENTLY
    """
    if not index_name:
        index_name = f"idx_{table_name}_{column_name}"

    try:
        # Use raw connection (SQLAlchemy doesn't support CONCURRENTLY in ORM)
        async with db.begin() as conn:
            await conn.execute(text(f"""
                CREATE INDEX CONCURRENTLY {index_name}
                ON {table_name}({column_name})
            """))

        logger.info(
            "index_created",
            table=table_name,
            column=column_name,
            index=index_name
        )

    except Exception as e:
        logger.error(
            "index_creation_failed",
            error=str(e),
            table=table_name,
            column=column_name
        )

        # Cleanup invalid index
        await db.execute(text(f"""
            DROP INDEX CONCURRENTLY IF EXISTS {index_name}
        """))

        raise


# Monitor index creation progress (PostgreSQL)
async def monitor_index_progress(index_name: str):
    """
    Monitor CREATE INDEX CONCURRENTLY progress

    Query: pg_stat_progress_create_index
    """
    while True:
        result = await db.execute(text("""
            SELECT
                phase,
                blocks_done,
                blocks_total,
                tuples_done,
                tuples_total,
                ROUND(100.0 * blocks_done / NULLIF(blocks_total, 0), 2) as percent_complete
            FROM pg_stat_progress_create_index
            WHERE index_relid = :index_name::regclass
        """), {"index_name": index_name})

        row = result.first()

        if not row:
            # Index creation completed
            break

        logger.info(
            "index_creation_progress",
            phase=row.phase,
            percent_complete=row.percent_complete,
            blocks_done=row.blocks_done,
            blocks_total=row.blocks_total
        )

        await asyncio.sleep(5)
```

---

## CATEGORÍA 3: Secrets Management

### 3.1 HashiCorp Vault Integration
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Nunca almacenes secrets en código, env vars, o configs. Vault provee dynamic secrets, encryption as a service, y secret rotation.

**Implementación: Vault Client con Caching**

```python
# HashiCorp Vault Client
import hvac
from dataclasses import dataclass
from typing import Optional
import asyncio
from datetime import datetime, timedelta

@dataclass
class Secret:
    """Cached secret with TTL"""
    value: str
    lease_duration: int
    lease_id: Optional[str]
    fetched_at: datetime

class VaultClient:
    """
    Production Vault client

    Features:
    - Dynamic secrets (DB credentials rotate automatically)
    - Transit encryption (encrypt/decrypt data)
    - Secret caching with TTL
    - Automatic renewal
    - Fallback to local cache if Vault down
    """

    def __init__(
        self,
        vault_addr: str,
        role_id: str,
        secret_id: str
    ):
        self.client = hvac.Client(url=vault_addr)
        self.role_id = role_id
        self.secret_id = secret_id
        self.cache: Dict[str, Secret] = {}
        self.is_authenticated = False

    async def authenticate(self):
        """
        AppRole authentication

        Vault returns token with TTL
        """
        try:
            response = self.client.auth.approle.login(
                role_id=self.role_id,
                secret_id=self.secret_id
            )

            self.client.token = response['auth']['client_token']
            self.is_authenticated = True

            logger.info(
                "vault_authenticated",
                lease_duration=response['auth']['lease_duration']
            )

            # Start token renewal background task
            asyncio.create_task(self._renew_token_periodically())

        except Exception as e:
            logger.error("vault_auth_failed", error=str(e))
            raise

    async def get_secret(
        self,
        path: str,
        key: Optional[str] = None
    ) -> str:
        """
        Get secret from Vault (with caching)

        Examples:
        - Database credentials: secret/data/database/postgres
        - API keys: secret/data/api-keys/stripe
        """

        cache_key = f"{path}:{key}" if key else path

        # Check cache
        if cache_key in self.cache:
            secret = self.cache[cache_key]

            # Check if still valid (80% of lease duration)
            age = (datetime.utcnow() - secret.fetched_at).seconds
            if age < (secret.lease_duration * 0.8):
                return secret.value

        # Cache miss or expired: fetch from Vault
        try:
            response = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point='secret'
            )

            data = response['data']['data']
            value = data.get(key) if key else data

            # Cache secret
            self.cache[cache_key] = Secret(
                value=value,
                lease_duration=response['lease_duration'],
                lease_id=response.get('lease_id'),
                fetched_at=datetime.utcnow()
            )

            return value

        except Exception as e:
            logger.error(
                "vault_fetch_failed",
                path=path,
                key=key,
                error=str(e)
            )

            # Fallback to stale cache if Vault down
            if cache_key in self.cache:
                logger.warning("using_stale_cache", path=path)
                return self.cache[cache_key].value

            raise

    async def get_database_credentials(self, db_name: str) -> Dict[str, str]:
        """
        Get dynamic database credentials

        Vault generates credentials on-demand with TTL
        Credentials auto-rotate
        """
        try:
            response = self.client.secrets.database.generate_credentials(
                name=db_name,
                mount_point='database'
            )

            credentials = {
                'username': response['data']['username'],
                'password': response['data']['password'],
                'lease_id': response['lease_id'],
                'lease_duration': response['lease_duration']
            }

            # Schedule credential renewal
            asyncio.create_task(
                self._renew_lease_periodically(
                    credentials['lease_id'],
                    credentials['lease_duration']
                )
            )

            logger.info(
                "dynamic_credentials_generated",
                database=db_name,
                lease_duration=credentials['lease_duration']
            )

            return credentials

        except Exception as e:
            logger.error(
                "dynamic_credentials_failed",
                database=db_name,
                error=str(e)
            )
            raise

    async def encrypt(self, plaintext: str, context: Optional[str] = None) -> str:
        """
        Transit encryption: Encrypt data

        Vault encrypts, never returns encryption key
        Supports key rotation
        """
        try:
            response = self.client.secrets.transit.encrypt_data(
                name='my-app',
                plaintext=plaintext,
                context=context
            )

            return response['data']['ciphertext']

        except Exception as e:
            logger.error("vault_encrypt_failed", error=str(e))
            raise

    async def decrypt(self, ciphertext: str, context: Optional[str] = None) -> str:
        """Transit encryption: Decrypt data"""
        try:
            response = self.client.secrets.transit.decrypt_data(
                name='my-app',
                ciphertext=ciphertext,
                context=context
            )

            return response['data']['plaintext']

        except Exception as e:
            logger.error("vault_decrypt_failed", error=str(e))
            raise

    async def _renew_token_periodically(self):
        """
        Background task: Renew Vault token

        Renew at 50% of TTL
        """
        while True:
            try:
                await asyncio.sleep(1800)  # 30 minutes

                response = self.client.auth.token.renew_self()

                logger.info(
                    "vault_token_renewed",
                    new_ttl=response['auth']['lease_duration']
                )

            except Exception as e:
                logger.error("vault_token_renewal_failed", error=str(e))
                # Re-authenticate
                await self.authenticate()

    async def _renew_lease_periodically(self, lease_id: str, lease_duration: int):
        """
        Background task: Renew lease (for dynamic secrets)

        Renew at 80% of TTL
        """
        while True:
            try:
                sleep_duration = lease_duration * 0.8
                await asyncio.sleep(sleep_duration)

                response = self.client.sys.renew_lease(lease_id=lease_id)

                lease_duration = response['lease_duration']

                logger.info(
                    "vault_lease_renewed",
                    lease_id=lease_id,
                    new_ttl=lease_duration
                )

            except Exception as e:
                logger.error(
                    "vault_lease_renewal_failed",
                    lease_id=lease_id,
                    error=str(e)
                )
                break


# Usage: Database with Dynamic Credentials
vault = VaultClient(
    vault_addr="https://vault.example.com",
    role_id=os.getenv("VAULT_ROLE_ID"),
    secret_id=os.getenv("VAULT_SECRET_ID")
)

async def get_database_engine():
    """
    Create database engine with dynamic credentials from Vault

    Credentials rotate automatically
    """
    await vault.authenticate()

    # Get dynamic credentials (TTL: 1 hour)
    creds = await vault.get_database_credentials("postgres-prod")

    database_url = (
        f"postgresql+asyncpg://{creds['username']}:{creds['password']}"
        f"@db.example.com:5432/myapp"
    )

    engine = create_async_engine(database_url)

    return engine


# Usage: Encrypt sensitive data
async def store_credit_card(user_id: int, card_number: str):
    """
    Encrypt credit card before storing

    Vault Transit: encryption-as-a-service
    """
    # Encrypt with Vault
    encrypted_card = await vault.encrypt(
        plaintext=card_number,
        context=str(user_id)  # User-specific context
    )

    # Store encrypted value
    await db.execute(
        insert(UserPaymentMethod).values(
            user_id=user_id,
            encrypted_card_number=encrypted_card
        )
    )
    await db.commit()

async def get_credit_card(user_id: int) -> str:
    """Decrypt credit card"""
    result = await db.execute(
        select(UserPaymentMethod.encrypted_card_number)
        .where(UserPaymentMethod.user_id == user_id)
    )
    encrypted_card = result.scalar_one()

    # Decrypt with Vault
    card_number = await vault.decrypt(
        ciphertext=encrypted_card,
        context=str(user_id)
    )

    return card_number
```

**Secrets Rotation Strategy**

```python
# Automatic Secret Rotation with Vault + Application

class DatabaseConnectionManager:
    """
    Connection manager with automatic credential rotation

    Challenge: Rotate DB credentials without dropping connections
    """

    def __init__(self, vault: VaultClient):
        self.vault = vault
        self.current_engine = None
        self.next_engine = None
        self.rotation_in_progress = False

    async def get_engine(self) -> AsyncEngine:
        """Get current database engine"""
        if not self.current_engine:
            self.current_engine = await self._create_engine()

            # Start rotation background task
            asyncio.create_task(self._rotate_credentials_periodically())

        return self.current_engine

    async def _create_engine(self) -> AsyncEngine:
        """Create engine with dynamic credentials"""
        creds = await self.vault.get_database_credentials("postgres-prod")

        database_url = (
            f"postgresql+asyncpg://{creds['username']}:{creds['password']}"
            f"@db.example.com:5432/myapp"
        )

        return create_async_engine(
            database_url,
            pool_size=20,
            max_overflow=10
        )

    async def _rotate_credentials_periodically(self):
        """
        Background task: Rotate credentials before they expire

        Strategy:
        1. Get new credentials
        2. Create new engine
        3. Gracefully drain old engine
        4. Switch to new engine
        """
        while True:
            try:
                # Rotate at 80% of lease duration
                await asyncio.sleep(2880)  # 48 minutes (if lease is 1 hour)

                logger.info("credential_rotation_starting")

                self.rotation_in_progress = True

                # Step 1: Create new engine with new credentials
                self.next_engine = await self._create_engine()

                # Step 2: Wait for old connections to drain (grace period)
                await asyncio.sleep(30)

                # Step 3: Dispose old engine
                old_engine = self.current_engine
                self.current_engine = self.next_engine
                self.next_engine = None

                await old_engine.dispose()

                self.rotation_in_progress = False

                logger.info("credential_rotation_completed")

            except Exception as e:
                logger.error("credential_rotation_failed", error=str(e))
                self.rotation_in_progress = False


# FastAPI Dependency
db_manager = DatabaseConnectionManager(vault)

async def get_db() -> AsyncSession:
    """Get database session with auto-rotating credentials"""
    engine = await db_manager.get_engine()

    async with AsyncSession(engine) as session:
        yield session
```

---

## CATEGORÍA 4: Shadow Traffic Testing

### 4.1 Shadow Traffic Pattern
**Dificultad:** ⭐⭐⭐⭐ **ALTA**

**Contexto:**
Test new code with production traffic without affecting users. Shadow requests are sent to both old and new systems, but only old system's response is returned.

**Implementación: Shadow Traffic Proxy**

```python
# Shadow Traffic Middleware
from typing import Callable
import httpx
import asyncio

class ShadowTrafficMiddleware:
    """
    Send duplicate traffic to shadow service

    Use cases:
    - Test new service version with real traffic
    - Compare ML model performance (A vs B)
    - Validate refactored code
    """

    def __init__(
        self,
        shadow_url: str,
        sample_rate: float = 1.0,  # % of traffic to shadow
        async_mode: bool = True
    ):
        self.shadow_url = shadow_url
        self.sample_rate = sample_rate
        self.async_mode = async_mode
        self.http_client = httpx.AsyncClient(timeout=5.0)

    async def __call__(self, request: Request, call_next: Callable):
        """
        Middleware: Send request to both primary and shadow

        Primary response is returned to client
        Shadow response is logged/compared
        """
        # Decide if this request should be shadowed
        if random.random() > self.sample_rate:
            return await call_next(request)

        # Get request body (for POST/PUT)
        body = await request.body()

        # Primary request (blocking)
        primary_response = await call_next(request)

        # Shadow request (non-blocking if async_mode)
        if self.async_mode:
            asyncio.create_task(
                self._send_shadow_request(request, body)
            )
        else:
            await self._send_shadow_request(request, body)

        # Return primary response (shadow doesn't affect client)
        return primary_response

    async def _send_shadow_request(self, request: Request, body: bytes):
        """Send request to shadow service"""
        shadow_url = f"{self.shadow_url}{request.url.path}"

        try:
            start_time = time.time()

            shadow_response = await self.http_client.request(
                method=request.method,
                url=shadow_url,
                headers=dict(request.headers),
                content=body,
                params=dict(request.query_params)
            )

            duration_ms = (time.time() - start_time) * 1000

            # Log shadow response for comparison
            logger.info(
                "shadow_request_completed",
                path=request.url.path,
                method=request.method,
                shadow_status=shadow_response.status_code,
                shadow_duration_ms=duration_ms
            )

            # Compare responses (if needed)
            await self._compare_responses(request, shadow_response)

        except Exception as e:
            logger.error(
                "shadow_request_failed",
                path=request.url.path,
                error=str(e)
            )

    async def _compare_responses(self, request: Request, shadow_response):
        """
        Compare primary vs shadow responses

        Metrics:
        - Response time difference
        - Status code match
        - Response body match (if deterministic)
        """
        # This would compare against stored primary response
        # Implementation depends on use case
        pass


# Usage in FastAPI
app = FastAPI()

# Add shadow traffic middleware
app.add_middleware(
    ShadowTrafficMiddleware,
    shadow_url="http://new-service.internal:8000",
    sample_rate=0.1,  # Shadow 10% of traffic
    async_mode=True
)


# Advanced: Compare ML Model Predictions
class ModelShadowTester:
    """
    Shadow testing for ML models

    Compare old model vs new model on production traffic
    """

    def __init__(
        self,
        old_model: MLModel,
        new_model: MLModel,
        metrics_client: MetricsClient
    ):
        self.old_model = old_model
        self.new_model = new_model
        self.metrics = metrics_client

    async def predict_with_shadow(self, features: Dict[str, Any]) -> Dict:
        """
        Run both models, return old model prediction

        Log comparison metrics
        """
        # Primary prediction (blocking)
        start = time.time()
        old_prediction = await self.old_model.predict(features)
        old_latency = time.time() - start

        # Shadow prediction (async)
        asyncio.create_task(
            self._shadow_predict(features, old_prediction, old_latency)
        )

        # Return old model result (no impact to user)
        return old_prediction

    async def _shadow_predict(
        self,
        features: Dict,
        old_prediction: Dict,
        old_latency: float
    ):
        """Shadow prediction and comparison"""
        try:
            start = time.time()
            new_prediction = await self.new_model.predict(features)
            new_latency = time.time() - start

            # Compare predictions
            prediction_match = (
                old_prediction['class'] == new_prediction['class']
            )

            confidence_diff = abs(
                old_prediction['confidence'] - new_prediction['confidence']
            )

            # Log metrics
            self.metrics.increment(
                'shadow_predictions_total',
                tags={
                    'match': str(prediction_match),
                    'model_version': 'v2'
                }
            )

            self.metrics.histogram(
                'shadow_latency_diff_ms',
                (new_latency - old_latency) * 1000
            )

            self.metrics.histogram(
                'shadow_confidence_diff',
                confidence_diff
            )

            logger.info(
                "shadow_prediction_compared",
                old_class=old_prediction['class'],
                new_class=new_prediction['class'],
                match=prediction_match,
                confidence_diff=confidence_diff,
                latency_diff_ms=(new_latency - old_latency) * 1000
            )

        except Exception as e:
            logger.error("shadow_prediction_failed", error=str(e))


# Usage
model_tester = ModelShadowTester(old_model, new_model, metrics)

@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Endpoint with shadow testing

    Users always get old model prediction
    New model tested in background
    """
    prediction = await model_tester.predict_with_shadow(request.features)

    return prediction
```

---

## Decisiones Consolidadas 2026

```
┌──────────────────────────────────────────────────────────────┐
│    DEPLOYMENT & OPERATIONS - CHECKLIST 2026                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. FEATURE FLAGS                                             │
│    ├─ [ ] Implement feature flag service (Redis-backed)     │
│    ├─ [ ] Percentage rollout capability                     │
│    ├─ [ ] Gradual rollout automation                        │
│    ├─ [ ] Kill switches for critical features               │
│    └─ [ ] Flag cleanup process (remove after 6 months)      │
│                                                              │
│ 2. DATABASE MIGRATIONS                                       │
│    ├─ [ ] Expand-Contract pattern for schema changes        │
│    ├─ [ ] CREATE INDEX CONCURRENTLY                         │
│    ├─ [ ] NOT NULL constraints without blocking             │
│    ├─ [ ] Automated backfill scripts                        │
│    └─ [ ] Migration verification in staging                 │
│                                                              │
│ 3. SECRETS MANAGEMENT                                        │
│    ├─ [ ] HashiCorp Vault integration                       │
│    ├─ [ ] Dynamic database credentials                      │
│    ├─ [ ] Automatic credential rotation                     │
│    ├─ [ ] Transit encryption for PII                        │
│    └─ [ ] Secret caching with TTL                           │
│                                                              │
│ 4. TESTING IN PRODUCTION                                     │
│    ├─ [ ] Shadow traffic for new services                   │
│    ├─ [ ] ML model A/B comparison                           │
│    ├─ [ ] Canary analysis automation                        │
│    └─ [ ] Automatic rollback on errors                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Conclusión:**

Este archivo cubre patrones críticos de deployment y operations:

1. **Feature Flags**: Sistema completo con percentage rollout, gradual rollout, y user targeting
2. **Zero-Downtime Migrations**: Expand-Contract pattern, índices concurrentes, constraints seguros
3. **Secrets Management**: Vault integration con dynamic credentials y auto-rotation
4. **Shadow Traffic**: Testing en producción sin impacto a usuarios

Cada patrón incluye código de producción completo en Python con trade-offs y best practices.
