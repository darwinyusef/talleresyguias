# Conocimientos Técnicos Difíciles: Database Engineering

## Objetivo
Temas complejos del día a día de ingeniería de bases de datos que un arquitecto debe dominar para apoyar efectivamente a los DB engineers.

---

## CATEGORÍA 1: Query Optimization

### 1.1 EXPLAIN ANALYZE y Query Planning
**Dificultad:** ⭐⭐⭐⭐⭐

**PostgreSQL:**

```sql
-- 1. Análisis básico de query
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC
LIMIT 100;

/*
Salida a analizar:
- Seq Scan vs Index Scan
- Nested Loop vs Hash Join vs Merge Join
- Actual time vs Planning time
- Rows estimadas vs Rows actuales
*/

-- 2. Identificar problemas comunes

-- ❌ Problema: Seq Scan en tabla grande
EXPLAIN ANALYZE
SELECT * FROM orders WHERE customer_id = 12345;
/*
Seq Scan on orders (cost=0.00..10000.00 rows=1 width=100)
Filter: (customer_id = 12345)
Rows Removed by Filter: 999999
*/

-- ✅ Solución: Crear índice
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 3. N+1 Query Problem
-- ❌ Malo: N+1 queries
SELECT * FROM users;
-- Luego por cada user:
SELECT * FROM orders WHERE user_id = ?;

-- ✅ Bueno: Single query con JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- 4. Subquery vs JOIN performance
-- ❌ Subquery puede ser lenta
SELECT *
FROM orders
WHERE customer_id IN (
    SELECT id FROM customers WHERE country = 'US'
);

-- ✅ JOIN es generalmente más rápido
SELECT o.*
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE c.country = 'US';

-- 5. Optimización de GROUP BY
-- ❌ Lento: GROUP BY múltiples columnas
SELECT customer_name, SUM(amount)
FROM orders
GROUP BY customer_name;

-- ✅ Rápido: GROUP BY con ID (única)
SELECT c.name, SUM(o.amount)
FROM orders o
JOIN customers c ON o.customer_id = c.id
GROUP BY c.id, c.name;

-- 6. Window functions vs subqueries
-- ❌ Múltiples scans
SELECT
    o.*,
    (SELECT AVG(amount) FROM orders o2 WHERE o2.customer_id = o.customer_id) as avg_amount
FROM orders o;

-- ✅ Single scan con window function
SELECT
    o.*,
    AVG(amount) OVER (PARTITION BY customer_id) as avg_amount
FROM orders o;
```

---

### 1.2 Index Strategies
**Dificultad:** ⭐⭐⭐⭐⭐

```sql
-- 1. B-Tree Index (default, para la mayoría de casos)
CREATE INDEX idx_users_email ON users(email);

-- 2. Partial Index (solo indexar subset de datos)
CREATE INDEX idx_active_users_email
ON users(email)
WHERE active = true AND deleted_at IS NULL;
-- Más pequeño, más rápido para queries con este filtro

-- 3. Composite Index (orden importa!)
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

-- ✅ Usa el índice
SELECT * FROM orders WHERE customer_id = 123;
SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';

-- ❌ NO usa el índice (status no es la primera columna)
SELECT * FROM orders WHERE status = 'pending';

-- 4. Covering Index (incluir columnas frecuentemente consultadas)
CREATE INDEX idx_orders_covering
ON orders(customer_id, status)
INCLUDE (total_amount, created_at);

-- Query completo desde índice, sin acceder a tabla
SELECT total_amount, created_at
FROM orders
WHERE customer_id = 123 AND status = 'pending';

-- 5. GIN Index (para arrays, JSONB, full-text search)
CREATE INDEX idx_products_tags ON products USING GIN(tags);

SELECT * FROM products WHERE tags @> ARRAY['electronics', 'sale'];

-- JSONB index
CREATE INDEX idx_users_metadata ON users USING GIN(metadata jsonb_path_ops);

SELECT * FROM users WHERE metadata @> '{"premium": true}';

-- 6. GiST Index (para geometría, range types)
CREATE INDEX idx_events_time_range ON events USING GIST(time_range);

SELECT * FROM events WHERE time_range && '[2024-01-01, 2024-12-31]';

-- 7. Index para LIKE queries
-- ❌ NO usa B-tree index
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- ✅ Solución: Trigram index
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_users_email_trgm ON users USING GIN(email gin_trgm_ops);

SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- 8. Detectar índices no usados
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- 9. Detectar queries lentas que necesitan índices
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- más de 100ms
ORDER BY mean_exec_time DESC
LIMIT 20;
```

---

## CATEGORÍA 2: Transactions y Locking

### 2.1 Isolation Levels
**Dificultad:** ⭐⭐⭐⭐⭐

```sql
-- 1. READ UNCOMMITTED (no soportado en PostgreSQL)
-- Lee datos no commiteados (dirty reads)

-- 2. READ COMMITTED (default en PostgreSQL)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Lee solo datos commiteados
-- Pero puede leer diferentes valores en la misma transacción (non-repeatable reads)

SELECT balance FROM accounts WHERE id = 1;  -- balance = 100

-- Otra transacción hace UPDATE y COMMIT

SELECT balance FROM accounts WHERE id = 1;  -- balance = 150 (diferente!)

COMMIT;

-- 3. REPEATABLE READ
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

SELECT balance FROM accounts WHERE id = 1;  -- balance = 100

-- Otra transacción hace UPDATE y COMMIT

SELECT balance FROM accounts WHERE id = 1;  -- balance = 100 (mismo!)

COMMIT;

-- ⚠️ Pero puede tener phantom reads en queries de rango

-- 4. SERIALIZABLE (más estricto)
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SELECT SUM(balance) FROM accounts WHERE user_id = 1;

-- Otra transacción inserta nueva cuenta y hace COMMIT

SELECT SUM(balance) FROM accounts WHERE user_id = 1;
-- Si hay conflict, ERROR: could not serialize access

COMMIT;

-- 5. Ejemplo práctico: Transfer de dinero
-- ❌ Sin transaction (race condition)
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- Si segunda query falla, quedamos inconsistentes

-- ✅ Con transaction
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Verificar
SELECT balance FROM accounts WHERE id IN (1, 2);

COMMIT;
-- O ROLLBACK si algo falla
```

---

### 2.2 Locking Strategies
**Dificultad:** ⭐⭐⭐⭐⭐

```sql
-- 1. Row-level locks

-- FOR UPDATE (exclusive lock)
BEGIN;
SELECT * FROM inventory WHERE product_id = 123 FOR UPDATE;
-- Otras transacciones esperan si intentan FOR UPDATE en mismas filas

UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 123;
COMMIT;

-- FOR SHARE (shared lock)
BEGIN;
SELECT * FROM products WHERE id = 123 FOR SHARE;
-- Otras transacciones pueden leer (FOR SHARE)
-- Pero no pueden escribir (FOR UPDATE bloquea)
COMMIT;

-- 2. SKIP LOCKED (evitar esperar)
-- Útil para job queues
BEGIN;
SELECT * FROM jobs
WHERE status = 'pending'
ORDER BY created_at
FOR UPDATE SKIP LOCKED
LIMIT 1;

UPDATE jobs SET status = 'processing' WHERE id = ...;
COMMIT;

-- 3. NOWAIT (fallar si locked)
BEGIN;
SELECT * FROM accounts WHERE id = 123 FOR UPDATE NOWAIT;
-- ERROR: could not obtain lock on row
COMMIT;

-- 4. Detectar deadlocks
-- PostgreSQL automáticamente los detecta y cancela una transacción

-- Transaction 1:
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- espera...
COMMIT;

-- Transaction 2:
BEGIN;
UPDATE accounts SET balance = balance - 50 WHERE id = 2;
UPDATE accounts SET balance = balance + 50 WHERE id = 1;  -- DEADLOCK!
-- ERROR: deadlock detected
ROLLBACK;

-- 5. Advisory Locks (application-level)
-- Útil para sincronizar procesos externos

-- Obtener lock
SELECT pg_advisory_lock(12345);

-- Hacer operación crítica...

-- Liberar lock
SELECT pg_advisory_unlock(12345);

-- Try lock (no bloquea)
SELECT pg_try_advisory_lock(12345);
-- true si obtuvo lock, false si ya está locked

-- 6. Monitorear locks activos
SELECT
    l.pid,
    l.mode,
    l.granted,
    a.query,
    a.state
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted;

-- 7. Matar transacción bloqueada
SELECT pg_terminate_backend(pid);
```

---

## CATEGORÍA 3: Replication y High Availability

### 3.1 PostgreSQL Replication
**Dificultad:** ⭐⭐⭐⭐⭐

```sql
-- 1. Configuración de Streaming Replication

-- Primary (postgresql.conf):
wal_level = replica
max_wal_senders = 5
wal_keep_size = '1GB'
hot_standby = on

-- pg_hba.conf:
host replication replicator 192.168.1.10/32 md5

-- Crear usuario de replicación:
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'password';

-- 2. Standby setup (recovery.conf o postgresql.auto.conf):
primary_conninfo = 'host=primary_host port=5432 user=replicator password=xxx'
restore_command = 'cp /archive/%f %p'
recovery_target_timeline = 'latest'

-- 3. Monitorear replication lag
-- En primary:
SELECT
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state,
    pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replay_lag_bytes
FROM pg_stat_replication;

-- En standby:
SELECT
    now() - pg_last_xact_replay_timestamp() AS replication_lag;

-- 4. Read Queries en Standby
-- Standby puede servir queries de solo lectura

-- postgresql.conf en standby:
hot_standby = on
hot_standby_feedback = on

-- Query en standby:
SELECT * FROM users WHERE id = 123;

-- 5. Failover manual
-- Promover standby a primary:
pg_ctl promote

-- O usando trigger file:
touch /tmp/postgresql.trigger.5432

-- 6. Logical Replication (PostgreSQL 10+)
-- Más flexible: replica tablas específicas, permite writes en subscriber

-- Publisher:
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- Subscriber:
CREATE SUBSCRIPTION my_subscription
CONNECTION 'host=publisher_host dbname=mydb user=replicator password=xxx'
PUBLICATION my_publication;

-- Monitorear logical replication:
SELECT * FROM pg_stat_subscription;
SELECT * FROM pg_replication_slots;
```

---

## CATEGORÍA 4: Performance Tuning

### 4.1 PostgreSQL Configuration
**Dificultad:** ⭐⭐⭐⭐

```ini
# postgresql.conf - Tuning para producción

# Memory settings (para servidor con 32GB RAM)
shared_buffers = 8GB           # 25% de RAM
effective_cache_size = 24GB    # 75% de RAM
work_mem = 64MB                # Por operación de sort/hash
maintenance_work_mem = 2GB     # Para VACUUM, CREATE INDEX

# Checkpoints
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100

# Query Planning
random_page_cost = 1.1         # Para SSDs (default 4.0 para HDDs)
effective_io_concurrency = 200 # Para SSDs

# Connections
max_connections = 200
```

```sql
-- 2. VACUUM y AUTOVACUUM
-- VACUUM libera espacio y actualiza estadísticas

-- Manual vacuum
VACUUM ANALYZE users;

-- Vacuum agresivo (bloquea tabla)
VACUUM FULL users;

-- Autovacuum configuration
ALTER TABLE users SET (autovacuum_vacuum_scale_factor = 0.1);
ALTER TABLE users SET (autovacuum_analyze_scale_factor = 0.05);

-- Monitorear autovacuum
SELECT
    schemaname,
    relname,
    last_vacuum,
    last_autovacuum,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- 3. Connection Pooling con PgBouncer
-- pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction        # o session, o statement
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3

-- 4. Identificar queries problemáticas
-- Habilitar pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Top 10 queries lentas
SELECT
    substring(query, 1, 100) AS short_query,
    round(total_exec_time::numeric, 2) AS total_time,
    calls,
    round(mean_exec_time::numeric, 2) AS mean,
    round((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS percentage
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries más frecuentes
SELECT
    substring(query, 1, 100) AS short_query,
    calls,
    round(mean_exec_time::numeric, 2) AS mean_time
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 10;
```

---

## CATEGORÍA 5: Migrations y Schema Changes

### 5.1 Zero-Downtime Migrations
**Dificultad:** ⭐⭐⭐⭐⭐

```sql
-- 1. Agregar columna con default (bloquea tabla en PG < 11)

-- ❌ Malo (bloquea tabla por mucho tiempo):
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active' NOT NULL;

-- ✅ Bueno (PostgreSQL 11+):
-- Paso 1: Agregar columna sin default
ALTER TABLE users ADD COLUMN status VARCHAR(20);

-- Paso 2: Set default para nuevas filas (no reescribe)
ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';

-- Paso 3: Backfill en batches (sin bloquear)
UPDATE users SET status = 'active'
WHERE id >= 1 AND id < 10000 AND status IS NULL;
-- Repetir en batches

-- Paso 4: Agregar NOT NULL constraint
ALTER TABLE users ALTER COLUMN status SET NOT NULL;

-- 2. Crear índice sin bloquear writes
-- ❌ Malo (bloquea writes):
CREATE INDEX idx_users_email ON users(email);

-- ✅ Bueno (permite writes):
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
-- ⚠️ Toma más tiempo, pero no bloquea

-- 3. Renombrar columna sin downtime
-- Paso 1: Agregar nueva columna
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Paso 2: Backfill data
UPDATE users SET full_name = name WHERE full_name IS NULL;

-- Paso 3: Deploy código que escribe en ambas columnas
-- (Dual-write pattern)

-- Paso 4: Verificar data sync
SELECT COUNT(*) FROM users WHERE full_name != name;

-- Paso 5: Deploy código que solo usa nueva columna

-- Paso 6: Drop columna antigua
ALTER TABLE users DROP COLUMN name;

-- 4. Cambiar tipo de columna
-- Paso 1: Crear nueva columna con nuevo tipo
ALTER TABLE orders ADD COLUMN total_cents BIGINT;

-- Paso 2: Backfill
UPDATE orders SET total_cents = (total * 100)::BIGINT
WHERE total_cents IS NULL;

-- Paso 3: Dual-write en aplicación

-- Paso 4: Verificar y switchear

-- Paso 5: Drop columna antigua
ALTER TABLE orders DROP COLUMN total;

-- Paso 6: Renombrar (instantáneo)
ALTER TABLE orders RENAME COLUMN total_cents TO total;

-- 5. Alembic migrations (Python)
"""Add user status column

Revision ID: abc123
"""

def upgrade():
    # Paso 1: Agregar columna nullable
    op.add_column('users',
        sa.Column('status', sa.String(20), nullable=True)
    )

    # Paso 2: Set default
    op.alter_column('users', 'status',
        server_default='active'
    )

    # Paso 3: Backfill (en batches)
    connection = op.get_bind()
    connection.execute(
        "UPDATE users SET status = 'active' WHERE status IS NULL"
    )

    # Paso 4: Make NOT NULL
    op.alter_column('users', 'status',
        nullable=False
    )

def downgrade():
    op.drop_column('users', 'status')
```

---

## Resumen Prioridades Database

| Tema | Dificultad | Criticidad | Frecuencia | Prioridad |
|------|------------|------------|------------|-----------|
| Query Optimization | 5 | 5 | 5 | **CRÍTICA** |
| Index Strategies | 5 | 5 | 5 | **CRÍTICA** |
| Transactions/Locking | 5 | 5 | 4 | **CRÍTICA** |
| Zero-Downtime Migrations | 5 | 5 | 3 | **ALTA** |
| Replication Setup | 5 | 4 | 3 | **ALTA** |
| Performance Tuning | 4 | 4 | 4 | **ALTA** |
