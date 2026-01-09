# Backend: Deployment, Reliability y Load Testing

## Objetivo
Estrategias avanzadas de deployment, disaster recovery, load testing, y feature management para sistemas de alta disponibilidad.

---

## CATEGORÍA 1: Load Testing y Performance Testing

### 1.1 Locust - Distributed Load Testing
**Dificultad:** ⭐⭐⭐⭐⭐

**Python - Locust Test Suite**

```python
from locust import HttpUser, task, between, events
from locust.contrib.fasthttp import FastHttpUser
import random
import json

class UserBehavior(FastHttpUser):
    """
    Simulate realistic user behavior
    FastHttpUser is faster than HttpUser for high loads
    """

    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    host = "https://api.example.com"

    def on_start(self):
        """
        Called when user starts
        Authenticate and get token
        """
        response = self.client.post("/auth/login", json={
            "email": f"user_{self.environment.runner.user_count}@example.com",
            "password": "password123"
        })

        if response.status_code == 200:
            self.token = response.json()['access_token']
        else:
            self.token = None

    @task(3)  # Weight: 3x more likely than other tasks
    def view_products(self):
        """
        View products (most common action)
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        with self.client.get(
            "/api/products",
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()

                if len(data['products']) > 0:
                    response.success()
                else:
                    response.failure("No products returned")
            else:
                response.failure(f"Got status code {response.status_code}")

    @task(2)
    def search_products(self):
        """
        Search products
        """
        search_terms = ['laptop', 'phone', 'tablet', 'monitor', 'keyboard']
        term = random.choice(search_terms)

        headers = {"Authorization": f"Bearer {self.token}"}

        self.client.get(
            f"/api/products/search?q={term}",
            headers=headers,
            name="/api/products/search"  # Group all searches under same name
        )

    @task(1)
    def create_order(self):
        """
        Create order (less frequent but important)
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        order_data = {
            "items": [
                {"product_id": random.randint(1, 100), "quantity": random.randint(1, 5)}
                for _ in range(random.randint(1, 3))
            ],
            "payment_method": random.choice(["credit_card", "paypal"])
        }

        with self.client.post(
            "/api/orders",
            json=order_data,
            headers=headers,
            catch_response=True
        ) as response:
            if response.status_code == 201:
                response.success()

                # Track custom metric
                self.environment.events.request.fire(
                    request_type="ORDER",
                    name="order_created",
                    response_time=response.elapsed.total_seconds() * 1000,
                    response_length=len(response.content),
                    exception=None,
                    context={}
                )
            elif response.status_code == 400:
                response.failure("Bad request")
            else:
                response.failure(f"Unexpected status: {response.status_code}")

    @task(1)
    def view_order_history(self):
        """
        View past orders
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        self.client.get(
            "/api/orders/history",
            headers=headers
        )

# Advanced load testing scenarios
class SpikeTestUser(FastHttpUser):
    """
    Simulate traffic spike
    Gradually increase load
    """

    wait_time = between(0.5, 2)
    host = "https://api.example.com"

    @task
    def spike_endpoint(self):
        """
        Test endpoint under spike
        """
        self.client.get("/api/products")

class StressTestUser(FastHttpUser):
    """
    Stress test to find breaking point
    No wait time between requests
    """

    wait_time = between(0, 0.1)
    host = "https://api.example.com"

    @task
    def stress_endpoint(self):
        self.client.get("/api/heavy-query")

# Custom metrics and reporting
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    Called when test starts
    """
    print("Load test starting...")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Called when test stops
    Generate custom report
    """
    print("Load test completed!")

    stats = environment.stats

    # Calculate custom metrics
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    error_rate = (total_failures / total_requests * 100) if total_requests > 0 else 0

    print(f"\n=== Load Test Results ===")
    print(f"Total Requests: {total_requests}")
    print(f"Total Failures: {total_failures}")
    print(f"Error Rate: {error_rate:.2f}%")
    print(f"Average Response Time: {stats.total.avg_response_time:.2f}ms")
    print(f"95th Percentile: {stats.total.get_response_time_percentile(0.95):.2f}ms")
    print(f"99th Percentile: {stats.total.get_response_time_percentile(0.99):.2f}ms")
    print(f"Max Response Time: {stats.total.max_response_time:.2f}ms")
    print(f"Requests/sec: {stats.total.total_rps:.2f}")

# Custom event handlers
class CustomEventHandler:
    """
    Custom event handling and metrics
    """

    def __init__(self):
        self.order_response_times = []
        self.payment_errors = 0

        # Register listeners
        events.request.add_listener(self.on_request)

    def on_request(
        self,
        request_type,
        name,
        response_time,
        response_length,
        exception,
        context,
        **kwargs
    ):
        """
        Track custom metrics per request
        """

        # Track order creation times separately
        if request_type == "ORDER":
            self.order_response_times.append(response_time)

        # Track payment errors
        if "payment" in name and exception:
            self.payment_errors += 1

    def get_stats(self):
        """
        Get custom statistics
        """
        if self.order_response_times:
            avg_order_time = sum(self.order_response_times) / len(self.order_response_times)
        else:
            avg_order_time = 0

        return {
            "total_orders": len(self.order_response_times),
            "avg_order_time_ms": avg_order_time,
            "payment_errors": self.payment_errors
        }

# Configuration for different test scenarios
"""
# Run with Locust CLI:

# Basic test: 100 users, spawn 10 per second
locust -f locustfile.py --users 100 --spawn-rate 10 --run-time 10m

# Distributed load test (master)
locust -f locustfile.py --master --expect-workers 4

# Distributed load test (worker)
locust -f locustfile.py --worker --master-host=<master-ip>

# Headless mode with custom host
locust -f locustfile.py --headless --users 1000 --spawn-rate 50 \
       --run-time 30m --host https://api.example.com

# With HTML report
locust -f locustfile.py --headless --users 500 --spawn-rate 25 \
       --run-time 10m --html report.html
"""
```

**K6 Load Testing (JavaScript)**

```javascript
// k6_load_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const orderDuration = new Trend('order_duration');
const orderSuccess = new Counter('orders_successful');

// Test configuration
export const options = {
    stages: [
        // Ramp-up: 0 to 100 users in 2 minutes
        { duration: '2m', target: 100 },
        // Stay at 100 users for 5 minutes
        { duration: '5m', target: 100 },
        // Spike: 100 to 500 users in 1 minute
        { duration: '1m', target: 500 },
        // Stay at 500 users for 2 minutes
        { duration: '2m', target: 500 },
        // Ramp-down: 500 to 0 users in 2 minutes
        { duration: '2m', target: 0 },
    ],
    thresholds: {
        // 99% of requests must complete below 2s
        'http_req_duration': ['p(99)<2000'],
        // Error rate must be below 1%
        'errors': ['rate<0.01'],
        // 95% of order creations must complete below 3s
        'order_duration': ['p(95)<3000'],
    },
};

// Test data
const BASE_URL = 'https://api.example.com';
let authToken;

export function setup() {
    // Run once before test
    // Authenticate and get token
    const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
        email: 'test@example.com',
        password: 'password123'
    }), {
        headers: { 'Content-Type': 'application/json' },
    });

    return { token: loginRes.json('access_token') };
}

export default function(data) {
    const params = {
        headers: {
            'Authorization': `Bearer ${data.token}`,
            'Content-Type': 'application/json',
        },
    };

    // Scenario 1: Browse products (60% of traffic)
    if (Math.random() < 0.6) {
        const productsRes = http.get(`${BASE_URL}/api/products`, params);

        check(productsRes, {
            'products status is 200': (r) => r.status === 200,
            'products returned': (r) => r.json('products').length > 0,
        }) || errorRate.add(1);
    }

    // Scenario 2: Search (20% of traffic)
    else if (Math.random() < 0.8) {
        const searchTerms = ['laptop', 'phone', 'tablet'];
        const term = searchTerms[Math.floor(Math.random() * searchTerms.length)];

        const searchRes = http.get(
            `${BASE_URL}/api/products/search?q=${term}`,
            params
        );

        check(searchRes, {
            'search status is 200': (r) => r.status === 200,
        }) || errorRate.add(1);
    }

    // Scenario 3: Create order (20% of traffic)
    else {
        const orderData = {
            items: [
                {
                    product_id: Math.floor(Math.random() * 100) + 1,
                    quantity: Math.floor(Math.random() * 3) + 1
                }
            ],
            payment_method: 'credit_card'
        };

        const orderRes = http.post(
            `${BASE_URL}/api/orders`,
            JSON.stringify(orderData),
            params
        );

        const orderSuccessful = check(orderRes, {
            'order status is 201': (r) => r.status === 201,
            'order has id': (r) => r.json('order_id') !== undefined,
        });

        if (orderSuccessful) {
            orderSuccess.add(1);
        } else {
            errorRate.add(1);
        }

        orderDuration.add(orderRes.timings.duration);
    }

    sleep(Math.random() * 3 + 1); // 1-4 seconds
}

export function teardown(data) {
    // Run once after test
    console.log('Test completed');
}

/*
Run with:
k6 run k6_load_test.js

Run with custom options:
k6 run --vus 100 --duration 30s k6_load_test.js

Run with cloud output:
k6 run --out cloud k6_load_test.js

Generate HTML report:
k6 run --out json=results.json k6_load_test.js
*/
```

---

## CATEGORÍA 2: Backup y Disaster Recovery

### 2.1 Database Backup Strategies
**Dificultad:** ⭐⭐⭐⭐⭐

```python
import subprocess
import boto3
from datetime import datetime, timedelta
import os
import gzip

class DatabaseBackupManager:
    """
    Automated database backup with:
    - Full backups
    - Incremental backups
    - Point-in-time recovery
    - S3 storage
    - Backup rotation
    """

    def __init__(
        self,
        db_config: dict,
        s3_bucket: str,
        retention_days: int = 30
    ):
        self.db_config = db_config
        self.s3_bucket = s3_bucket
        self.retention_days = retention_days
        self.s3_client = boto3.client('s3')

    async def create_full_backup(self) -> dict:
        """
        Create full database backup
        """

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        backup_file = f"backup_full_{timestamp}.sql"
        compressed_file = f"{backup_file}.gz"

        try:
            logger.info("Starting full database backup")

            # Run pg_dump
            dump_command = [
                'pg_dump',
                '-h', self.db_config['host'],
                '-U', self.db_config['user'],
                '-d', self.db_config['database'],
                '-F', 'c',  # Custom format (compressed)
                '-f', backup_file,
                '--verbose'
            ]

            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_config['password']

            process = subprocess.Popen(
                dump_command,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                raise Exception(f"Backup failed: {stderr.decode()}")

            # Compress backup
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    f_out.writelines(f_in)

            # Upload to S3
            s3_key = f"backups/full/{compressed_file}"
            await self._upload_to_s3(compressed_file, s3_key)

            # Calculate size and checksum
            file_size = os.path.getsize(compressed_file)
            checksum = await self._calculate_checksum(compressed_file)

            # Store backup metadata
            metadata = {
                'backup_type': 'full',
                'timestamp': timestamp,
                'file_name': compressed_file,
                's3_key': s3_key,
                'size_bytes': file_size,
                'checksum': checksum,
                'database': self.db_config['database']
            }

            await self._store_backup_metadata(metadata)

            # Cleanup local files
            os.remove(backup_file)
            os.remove(compressed_file)

            logger.info(
                "Full backup completed",
                size_mb=file_size / 1024 / 1024,
                s3_key=s3_key
            )

            return metadata

        except Exception as e:
            logger.error(f"Backup failed: {e}")
            raise

    async def create_incremental_backup(
        self,
        base_backup_lsn: str
    ) -> dict:
        """
        Create incremental backup (WAL archiving)
        Requires PostgreSQL with WAL archiving enabled
        """

        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

        # Use pg_basebackup with incremental option
        backup_dir = f"backup_incremental_{timestamp}"

        command = [
            'pg_basebackup',
            '-h', self.db_config['host'],
            '-U', self.db_config['user'],
            '-D', backup_dir,
            '-F', 'tar',
            '-z',  # Compress
            '-P',  # Progress
            '--wal-method=fetch'
        ]

        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_config['password']

        subprocess.run(command, env=env, check=True)

        # Upload to S3
        s3_key = f"backups/incremental/{backup_dir}.tar.gz"
        await self._upload_directory_to_s3(backup_dir, s3_key)

        return {
            'backup_type': 'incremental',
            'timestamp': timestamp,
            's3_key': s3_key,
            'base_lsn': base_backup_lsn
        }

    async def restore_backup(
        self,
        backup_metadata: dict,
        target_time: datetime = None
    ):
        """
        Restore database from backup
        Supports point-in-time recovery
        """

        logger.info(
            "Starting database restore",
            backup=backup_metadata['file_name'],
            target_time=target_time
        )

        # Download backup from S3
        local_file = f"/tmp/{backup_metadata['file_name']}"
        await self._download_from_s3(backup_metadata['s3_key'], local_file)

        # Verify checksum
        checksum = await self._calculate_checksum(local_file)
        if checksum != backup_metadata['checksum']:
            raise Exception("Backup file corrupted - checksum mismatch")

        # Decompress
        decompressed_file = local_file.replace('.gz', '')
        with gzip.open(local_file, 'rb') as f_in:
            with open(decompressed_file, 'wb') as f_out:
                f_out.write(f_in.read())

        # Drop existing database
        drop_command = [
            'dropdb',
            '-h', self.db_config['host'],
            '-U', self.db_config['user'],
            '--if-exists',
            self.db_config['database']
        ]

        env = os.environ.copy()
        env['PGPASSWORD'] = self.db_config['password']

        subprocess.run(drop_command, env=env, check=True)

        # Create new database
        create_command = [
            'createdb',
            '-h', self.db_config['host'],
            '-U', self.db_config['user'],
            self.db_config['database']
        ]

        subprocess.run(create_command, env=env, check=True)

        # Restore from backup
        restore_command = [
            'pg_restore',
            '-h', self.db_config['host'],
            '-U', self.db_config['user'],
            '-d', self.db_config['database'],
            '-v',
            decompressed_file
        ]

        subprocess.run(restore_command, env=env, check=True)

        # Point-in-time recovery if specified
        if target_time:
            await self._apply_wal_until(target_time)

        # Cleanup
        os.remove(local_file)
        os.remove(decompressed_file)

        logger.info("Database restore completed")

    async def rotate_old_backups(self):
        """
        Delete backups older than retention period
        """

        cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)

        logger.info(
            f"Rotating backups older than {cutoff_date}"
        )

        # List all backups
        response = self.s3_client.list_objects_v2(
            Bucket=self.s3_bucket,
            Prefix='backups/'
        )

        deleted_count = 0

        for obj in response.get('Contents', []):
            # Parse timestamp from key
            # Format: backups/full/backup_full_20250101_120000.sql.gz
            try:
                timestamp_str = obj['Key'].split('_')[-2] + '_' + obj['Key'].split('_')[-1].split('.')[0]
                backup_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

                if backup_time < cutoff_date:
                    self.s3_client.delete_object(
                        Bucket=self.s3_bucket,
                        Key=obj['Key']
                    )
                    deleted_count += 1

            except Exception as e:
                logger.warning(f"Could not parse backup timestamp: {obj['Key']}")

        logger.info(f"Deleted {deleted_count} old backups")

    async def _upload_to_s3(self, local_file: str, s3_key: str):
        """Upload file to S3"""
        self.s3_client.upload_file(
            local_file,
            self.s3_bucket,
            s3_key,
            ExtraArgs={'ServerSideEncryption': 'AES256'}
        )

    async def _download_from_s3(self, s3_key: str, local_file: str):
        """Download file from S3"""
        self.s3_client.download_file(
            self.s3_bucket,
            s3_key,
            local_file
        )

    async def _calculate_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum"""
        import hashlib

        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    async def _store_backup_metadata(self, metadata: dict):
        """Store backup metadata in database"""
        await db.execute(
            """
            INSERT INTO backup_history (
                backup_type, timestamp, file_name, s3_key,
                size_bytes, checksum, database_name
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            metadata['backup_type'],
            metadata['timestamp'],
            metadata['file_name'],
            metadata['s3_key'],
            metadata['size_bytes'],
            metadata['checksum'],
            metadata['database']
        )

    async def _apply_wal_until(self, target_time: datetime):
        """
        Apply WAL (Write-Ahead Log) until target time
        For point-in-time recovery
        """
        # This requires PostgreSQL recovery configuration
        # Create recovery.conf with recovery_target_time
        pass

# Scheduled backup job
async def scheduled_backup_job():
    """
    Run backups on schedule
    """

    backup_manager = DatabaseBackupManager(
        db_config={
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME')
        },
        s3_bucket='my-backups-bucket',
        retention_days=30
    )

    while True:
        try:
            # Full backup daily at 2 AM
            now = datetime.utcnow()
            if now.hour == 2 and now.minute < 5:
                await backup_manager.create_full_backup()

            # Rotate old backups weekly
            if now.weekday() == 0 and now.hour == 3:  # Monday 3 AM
                await backup_manager.rotate_old_backups()

            await asyncio.sleep(300)  # Check every 5 minutes

        except Exception as e:
            logger.error(f"Backup job error: {e}")
            await asyncio.sleep(300)
```

---

### 2.2 Database Replication y Failover
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from typing import List, Optional
import asyncpg

class DatabaseReplicationManager:
    """
    Manage database replication and automatic failover
    Primary-Replica setup with automatic failover
    """

    def __init__(
        self,
        primary_url: str,
        replica_urls: List[str]
    ):
        self.primary_url = primary_url
        self.replica_urls = replica_urls
        self.current_primary = primary_url
        self.replicas = replica_urls.copy()

    async def get_write_connection(self):
        """
        Get connection to primary (for writes)
        """
        try:
            conn = await asyncpg.connect(self.current_primary)
            return conn

        except Exception as e:
            logger.error(f"Failed to connect to primary: {e}")

            # Attempt failover
            await self.failover_to_replica()

            # Retry
            conn = await asyncpg.connect(self.current_primary)
            return conn

    async def get_read_connection(self):
        """
        Get connection to replica (for reads)
        Load balance across replicas
        """

        # Try replicas in order
        for replica_url in self.replicas:
            try:
                conn = await asyncpg.connect(replica_url)

                # Check if replica is healthy and not lagging
                is_healthy = await self._check_replica_health(conn)

                if is_healthy:
                    return conn
                else:
                    await conn.close()

            except Exception as e:
                logger.warning(f"Replica unavailable: {replica_url}")
                continue

        # Fallback to primary if all replicas fail
        logger.warning("All replicas unavailable, falling back to primary")
        return await self.get_write_connection()

    async def failover_to_replica(self):
        """
        Promote replica to primary
        """

        logger.critical("Initiating failover to replica")

        # Find healthiest replica
        best_replica = await self._find_best_replica()

        if not best_replica:
            raise Exception("No healthy replica available for failover")

        logger.info(f"Promoting replica to primary: {best_replica}")

        # Connect to replica
        conn = await asyncpg.connect(best_replica)

        # Promote to primary (PostgreSQL)
        await conn.execute("SELECT pg_promote()")

        # Update current primary
        old_primary = self.current_primary
        self.current_primary = best_replica

        # Remove promoted replica from replica list
        self.replicas.remove(best_replica)

        # Add old primary as replica (if recoverable)
        # In production: verify old primary is in recovery mode first
        # self.replicas.append(old_primary)

        await conn.close()

        logger.info(
            "Failover completed",
            new_primary=best_replica,
            old_primary=old_primary
        )

        # Notify monitoring/alerting
        await self._send_failover_alert(old_primary, best_replica)

    async def _find_best_replica(self) -> Optional[str]:
        """
        Find replica with least lag
        """

        best_replica = None
        min_lag = float('inf')

        for replica_url in self.replicas:
            try:
                conn = await asyncpg.connect(replica_url)

                # Check replication lag
                lag = await self._get_replication_lag(conn)

                if lag < min_lag:
                    min_lag = lag
                    best_replica = replica_url

                await conn.close()

            except Exception as e:
                logger.warning(f"Could not check replica: {replica_url}")

        return best_replica

    async def _check_replica_health(self, conn) -> bool:
        """
        Check if replica is healthy
        """

        # Check if in recovery mode (is replica)
        result = await conn.fetchval("SELECT pg_is_in_recovery()")

        if not result:
            logger.warning("Replica is not in recovery mode")
            return False

        # Check replication lag
        lag = await self._get_replication_lag(conn)

        # Unhealthy if lagging more than 10 seconds
        if lag > 10:
            logger.warning(f"Replica lagging by {lag} seconds")
            return False

        return True

    async def _get_replication_lag(self, conn) -> float:
        """
        Get replication lag in seconds
        """

        result = await conn.fetchval("""
            SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))
        """)

        return result or 0

    async def _send_failover_alert(self, old_primary: str, new_primary: str):
        """
        Send alert about failover
        """

        # Send to monitoring system, PagerDuty, Slack, etc.
        logger.critical(
            "DATABASE FAILOVER",
            old_primary=old_primary,
            new_primary=new_primary
        )

# Read-Write Split pattern
class ReadWriteSplitDatabase:
    """
    Automatically route reads to replicas, writes to primary
    """

    def __init__(self, replication_manager: DatabaseReplicationManager):
        self.replication = replication_manager

    async def execute_read(self, query: str, *args):
        """
        Execute read query on replica
        """
        conn = await self.replication.get_read_connection()

        try:
            result = await conn.fetch(query, *args)
            return result
        finally:
            await conn.close()

    async def execute_write(self, query: str, *args):
        """
        Execute write query on primary
        """
        conn = await self.replication.get_write_connection()

        try:
            result = await conn.fetch(query, *args)
            return result
        finally:
            await conn.close()

# Usage
replication_manager = DatabaseReplicationManager(
    primary_url="postgresql://user:pass@primary:5432/db",
    replica_urls=[
        "postgresql://user:pass@replica1:5432/db",
        "postgresql://user:pass@replica2:5432/db"
    ]
)

db = ReadWriteSplitDatabase(replication_manager)

# Read from replica
users = await db.execute_read("SELECT * FROM users WHERE active = true")

# Write to primary
await db.execute_write(
    "INSERT INTO users (name, email) VALUES ($1, $2)",
    "John", "john@example.com"
)
```

---

Continúa en siguiente sección...

---

## CATEGORÍA 3: Blue-Green Deployments

### 3.1 Zero-Downtime Deployment
**Dificultad:** ⭐⭐⭐⭐⭐

```python
import boto3
from typing import List
import time

class BlueGreenDeploymentManager:
    """
    Manage blue-green deployments
    Zero-downtime deployment strategy
    """

    def __init__(
        self,
        load_balancer_arn: str,
        target_group_blue_arn: str,
        target_group_green_arn: str
    ):
        self.lb_arn = load_balancer_arn
        self.blue_tg_arn = target_group_blue_arn
        self.green_tg_arn = target_group_green_arn

        self.elbv2_client = boto3.client('elbv2')
        self.ecs_client = boto3.client('ecs')

    async def deploy_new_version(
        self,
        cluster_name: str,
        service_name: str,
        new_task_definition: str
    ):
        """
        Deploy new version using blue-green strategy
        """

        logger.info("Starting blue-green deployment")

        # Step 1: Identify current (blue) environment
        current_listener = await self._get_current_listener()
        current_tg = current_listener['DefaultActions'][0]['TargetGroupArn']

        if current_tg == self.blue_tg_arn:
            active_tg = 'blue'
            inactive_tg_arn = self.green_tg_arn
            inactive_tg = 'green'
        else:
            active_tg = 'green'
            inactive_tg_arn = self.blue_tg_arn
            inactive_tg = 'blue'

        logger.info(f"Active environment: {active_tg}")

        # Step 2: Deploy to inactive (green) environment
        logger.info(f"Deploying to {inactive_tg} environment")

        await self._update_ecs_service(
            cluster_name,
            service_name,
            new_task_definition,
            inactive_tg_arn
        )

        # Step 3: Wait for deployment to be stable
        await self._wait_for_stable_deployment(cluster_name, service_name)

        # Step 4: Run health checks on green environment
        logger.info("Running health checks on new deployment")

        health_check_passed = await self._run_health_checks(inactive_tg_arn)

        if not health_check_passed:
            logger.error("Health checks failed, aborting deployment")
            raise Exception("Health checks failed")

        # Step 5: Run smoke tests
        logger.info("Running smoke tests")

        smoke_tests_passed = await self._run_smoke_tests(inactive_tg_arn)

        if not smoke_tests_passed:
            logger.error("Smoke tests failed, aborting deployment")
            raise Exception("Smoke tests failed")

        # Step 6: Switch traffic to green environment
        logger.info(f"Switching traffic to {inactive_tg} environment")

        await self._switch_traffic(inactive_tg_arn)

        # Step 7: Monitor for issues
        logger.info("Monitoring new deployment for 5 minutes")

        monitoring_passed = await self._monitor_deployment(300)  # 5 minutes

        if not monitoring_passed:
            logger.error("Issues detected, rolling back")
            await self.rollback(current_tg)
            raise Exception("Deployment monitoring failed")

        # Step 8: Deployment successful
        logger.info(f"Deployment successful! {inactive_tg} is now active")

        return {
            'success': True,
            'old_environment': active_tg,
            'new_environment': inactive_tg
        }

    async def rollback(self, target_group_name: str):
        """
        Rollback to previous environment
        """

        logger.warning(f"Rolling back to {target_group_name} environment")

        if target_group_name == 'blue':
            tg_arn = self.blue_tg_arn
        else:
            tg_arn = self.green_tg_arn

        await self._switch_traffic(tg_arn)

        logger.info("Rollback completed")

    async def _get_current_listener(self):
        """Get current load balancer listener"""

        response = self.elbv2_client.describe_listeners(
            LoadBalancerArn=self.lb_arn
        )

        return response['Listeners'][0]

    async def _update_ecs_service(
        self,
        cluster: str,
        service: str,
        task_definition: str,
        target_group_arn: str
    ):
        """Update ECS service with new task definition"""

        self.ecs_client.update_service(
            cluster=cluster,
            service=service,
            taskDefinition=task_definition,
            loadBalancers=[
                {
                    'targetGroupArn': target_group_arn,
                    'containerName': 'app',
                    'containerPort': 8000
                }
            ]
        )

    async def _wait_for_stable_deployment(
        self,
        cluster: str,
        service: str,
        timeout: int = 600
    ):
        """Wait for ECS service to be stable"""

        start_time = time.time()

        while time.time() - start_time < timeout:
            response = self.ecs_client.describe_services(
                cluster=cluster,
                services=[service]
            )

            service_data = response['services'][0]

            # Check if deployment is stable
            if len(service_data['deployments']) == 1:
                deployment = service_data['deployments'][0]

                if deployment['runningCount'] == deployment['desiredCount']:
                    logger.info("Deployment is stable")
                    return

            await asyncio.sleep(10)

        raise Exception("Deployment did not stabilize in time")

    async def _run_health_checks(self, target_group_arn: str) -> bool:
        """Run health checks on target group"""

        # Get target health
        response = self.elbv2_client.describe_target_health(
            TargetGroupArn=target_group_arn
        )

        # Check all targets are healthy
        for target in response['TargetHealthDescriptions']:
            if target['TargetHealth']['State'] != 'healthy':
                logger.error(
                    f"Unhealthy target: {target['Target']['Id']}"
                )
                return False

        return True

    async def _run_smoke_tests(self, target_group_arn: str) -> bool:
        """Run smoke tests against new deployment"""

        # Get target group endpoints
        targets = await self._get_target_endpoints(target_group_arn)

        # Run basic tests
        for target in targets:
            endpoint = f"http://{target['address']}:{target['port']}"

            try:
                # Test health endpoint
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{endpoint}/health")

                    if response.status_code != 200:
                        logger.error(f"Health check failed for {endpoint}")
                        return False

                    # Test critical endpoint
                    response = await client.get(f"{endpoint}/api/critical")

                    if response.status_code != 200:
                        logger.error(f"Critical endpoint failed for {endpoint}")
                        return False

            except Exception as e:
                logger.error(f"Smoke test failed for {endpoint}: {e}")
                return False

        return True

    async def _switch_traffic(self, target_group_arn: str):
        """Switch load balancer traffic to target group"""

        listeners = self.elbv2_client.describe_listeners(
            LoadBalancerArn=self.lb_arn
        )

        for listener in listeners['Listeners']:
            self.elbv2_client.modify_listener(
                ListenerArn=listener['ListenerArn'],
                DefaultActions=[
                    {
                        'Type': 'forward',
                        'TargetGroupArn': target_group_arn
                    }
                ]
            )

        logger.info("Traffic switched successfully")

    async def _monitor_deployment(self, duration: int) -> bool:
        """Monitor deployment for issues"""

        start_time = time.time()

        while time.time() - start_time < duration:
            # Check error rate
            error_rate = await self._get_error_rate()

            if error_rate > 5:  # More than 5% errors
                logger.error(f"High error rate detected: {error_rate}%")
                return False

            # Check latency
            p99_latency = await self._get_p99_latency()

            if p99_latency > 2000:  # More than 2 seconds
                logger.error(f"High latency detected: {p99_latency}ms")
                return False

            await asyncio.sleep(10)

        return True

    async def _get_error_rate(self) -> float:
        """Get current error rate from CloudWatch"""
        # Query CloudWatch metrics
        return 0.5  # Example

    async def _get_p99_latency(self) -> float:
        """Get P99 latency from CloudWatch"""
        # Query CloudWatch metrics
        return 150  # Example
```

---

Continúa con Feature Flags...

---

## Resumen Deployment y Reliability

| Tema | Dificultad | Complejidad | Impacto | Prioridad |
|------|------------|-------------|---------|-----------|
| Load Testing | 4 | 4 | 5 | **CRÍTICA** |
| Database Backup | 5 | 5 | 5 | **CRÍTICA** |
| Replication/Failover | 5 | 5 | 5 | **CRÍTICA** |
| Blue-Green Deployment | 5 | 5 | 4 | **ALTA** |
| Disaster Recovery | 5 | 5 | 5 | **CRÍTICA** |
| PITR (Point-in-Time Recovery) | 5 | 5 | 4 | **ALTA** |

**El siguiente archivo continuará con:**
- Feature Flags y A/B Testing
- Canary Deployments
- Database Migration Strategies
- Multi-Region Deployments
- Cost Optimization Strategies
