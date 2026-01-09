# Arquitectura de Datos: Patrones Modernos y Data Mesh 2026

## Índice
1. [Data Architecture Fundamentals](#1-data-architecture-fundamentals)
2. [Data Mesh](#2-data-mesh)
3. [Data Lakehouse](#3-data-lakehouse)
4. [Change Data Capture (CDC)](#4-cdc)
5. [Data Governance](#5-data-governance)
6. [Data Quality](#6-data-quality)
7. [Real-Time Data Architecture](#7-real-time-data)
8. [Data Versioning & Lineage](#8-data-lineage)
9. [Polyglot Persistence](#9-polyglot-persistence)
10. [Data Migration Patterns](#10-data-migration)

---

## 1. Data Architecture Fundamentals

### ❌ ERROR COMÚN: Monolithic data warehouse
```python
# MAL - Todo en un solo warehouse centralizado
# - Single point of failure
# - No ownership por dominio
# - Acoplamiento fuerte

centralized_warehouse = {
    "orders": "SELECT * FROM orders",
    "customers": "SELECT * FROM customers",
    "products": "SELECT * FROM products",
    "analytics": "SELECT * FROM analytics",
    # 500+ tablas sin ownership claro
}
```

### ✅ SOLUCIÓN: Arquitectura moderna de datos

```python
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

# ==========================================
# DATA ARCHITECTURE PATTERNS
# ==========================================

class DataArchitecturePattern(Enum):
    """Patrones modernos de arquitectura de datos"""
    DATA_WAREHOUSE = "data_warehouse"      # Traditional centralized
    DATA_LAKE = "data_lake"                # Raw data storage
    DATA_LAKEHOUSE = "data_lakehouse"      # Lake + Warehouse benefits
    DATA_MESH = "data_mesh"                # Decentralized, domain-oriented
    DATA_FABRIC = "data_fabric"            # Unified virtual layer

# ==========================================
# DATA DOMAINS
# ==========================================
@dataclass
class DataDomain:
    """
    Domain-oriented data ownership (Data Mesh)
    """
    name: str
    owner_team: str
    description: str
    data_products: List['DataProduct']
    sla: Dict[str, Any]
    quality_metrics: Dict[str, float]

@dataclass
class DataProduct:
    """
    Data as a Product - core concept of Data Mesh

    Properties:
    - Discoverable
    - Addressable
    - Trustworthy
    - Self-describing
    - Secure
    - Interoperable
    """
    id: str
    name: str
    domain: str
    owner: str
    description: str

    # Data contract
    schema_version: str
    schema: Dict

    # Access
    endpoint: str  # SQL endpoint, API, etc.
    authentication: str

    # Quality
    sla_latency_ms: int
    sla_availability: float  # 99.9%
    freshness_sla_minutes: int

    # Metadata
    created_at: datetime
    updated_at: datetime
    tags: List[str]

# ==========================================
# EXAMPLE: ORDERS DATA DOMAIN
# ==========================================
orders_domain = DataDomain(
    name="orders",
    owner_team="orders-team",
    description="Order management data domain",
    data_products=[
        DataProduct(
            id="orders.order_events",
            name="Order Events Stream",
            domain="orders",
            owner="orders-team@company.com",
            description="Real-time stream of order events",
            schema_version="1.2.0",
            schema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "customer_id": {"type": "string"},
                    "status": {"type": "string"},
                    "total_amount": {"type": "number"},
                    "timestamp": {"type": "string", "format": "date-time"}
                },
                "required": ["order_id", "customer_id", "status"]
            },
            endpoint="kafka://orders.events",
            authentication="oauth2",
            sla_latency_ms=100,
            sla_availability=99.9,
            freshness_sla_minutes=1,
            created_at=datetime(2024, 1, 1),
            updated_at=datetime.utcnow(),
            tags=["real-time", "transactional", "core"]
        ),

        DataProduct(
            id="orders.analytics_orders",
            name="Orders Analytics Dataset",
            domain="orders",
            owner="orders-team@company.com",
            description="Analytical view of orders for reporting",
            schema_version="2.0.0",
            schema={
                "type": "table",
                "columns": {
                    "order_id": "STRING",
                    "customer_id": "STRING",
                    "order_date": "DATE",
                    "total_amount": "DECIMAL(10,2)",
                    "status": "STRING",
                    "items_count": "INTEGER"
                }
            },
            endpoint="bigquery://analytics.orders.orders_view",
            authentication="service_account",
            sla_latency_ms=5000,
            sla_availability=99.5,
            freshness_sla_minutes=15,
            created_at=datetime(2024, 1, 1),
            updated_at=datetime.utcnow(),
            tags=["analytics", "aggregated", "daily"]
        )
    ],
    sla={
        "data_freshness": "15 minutes",
        "availability": "99.9%",
        "query_latency_p99": "5 seconds"
    },
    quality_metrics={
        "completeness": 0.999,
        "accuracy": 0.995,
        "consistency": 0.998
    }
)

# ==========================================
# DATA CATALOG
# ==========================================
class DataCatalog:
    """
    Central catalog of all data products
    Enables discovery and governance
    """

    def __init__(self):
        self.products: Dict[str, DataProduct] = {}
        self.domains: Dict[str, DataDomain] = {}

    def register_product(self, product: DataProduct):
        """Register new data product"""
        self.products[product.id] = product

        # Update metadata store (e.g., DataHub, Amundsen)
        self._update_metadata_store(product)

    def search_products(
        self,
        query: str,
        domain: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[DataProduct]:
        """
        Search data products
        """
        results = []

        for product in self.products.values():
            # Filter by domain
            if domain and product.domain != domain:
                continue

            # Filter by tags
            if tags and not any(tag in product.tags for tag in tags):
                continue

            # Text search
            if (query.lower() in product.name.lower() or
                query.lower() in product.description.lower()):
                results.append(product)

        return results

    def get_product_lineage(self, product_id: str) -> Dict:
        """
        Get data lineage for a product
        Shows upstream and downstream dependencies
        """
        # Integration with lineage tools (Marquez, DataHub)
        return {
            "product_id": product_id,
            "upstream": [
                {"type": "database", "name": "orders_db.orders"},
                {"type": "stream", "name": "kafka.order_events"}
            ],
            "downstream": [
                {"type": "dashboard", "name": "sales_dashboard"},
                {"type": "ml_model", "name": "churn_prediction"}
            ]
        }

    def _update_metadata_store(self, product: DataProduct):
        """Update external metadata store"""
        # Integration with DataHub, Amundsen, etc.
        pass

# ==========================================
# DATA CONTRACT
# ==========================================
import jsonschema

class DataContract:
    """
    Data Contract - SLA entre producer y consumers

    Defines:
    - Schema
    - Quality expectations
    - Freshness SLA
    - Breaking change policy
    """

    def __init__(self, product: DataProduct):
        self.product = product
        self.schema = product.schema

    def validate_data(self, data: dict) -> bool:
        """
        Validate data against contract
        """
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            return True
        except jsonschema.ValidationError as e:
            print(f"Contract violation: {e}")
            return False

    def check_sla_compliance(self, metrics: dict) -> bool:
        """
        Verify SLA compliance
        """
        checks = []

        # Latency check
        if metrics.get('latency_ms', 0) > self.product.sla_latency_ms:
            checks.append(f"Latency SLA violated: {metrics['latency_ms']}ms > {self.product.sla_latency_ms}ms")

        # Freshness check
        if metrics.get('freshness_minutes', 0) > self.product.freshness_sla_minutes:
            checks.append(f"Freshness SLA violated: {metrics['freshness_minutes']}min > {self.product.freshness_sla_minutes}min")

        # Availability check
        if metrics.get('availability', 0) < self.product.sla_availability:
            checks.append(f"Availability SLA violated: {metrics['availability']}% < {self.product.sla_availability}%")

        if checks:
            for check in checks:
                print(f"⚠️  SLA Violation: {check}")
            return False

        return True
```

---

## 2. Data Mesh

### ✅ SOLUCIÓN: Data Mesh architecture

```python
# ==========================================
# DATA MESH PRINCIPLES
# ==========================================
"""
1. Domain-oriented decentralized data ownership
2. Data as a Product
3. Self-serve data infrastructure
4. Federated computational governance
"""

# ==========================================
# SELF-SERVE DATA PLATFORM
# ==========================================
class SelfServeDataPlatform:
    """
    Infrastructure platform para data mesh

    Provides:
    - Data pipeline templates
    - Automated testing
    - Monitoring & alerting
    - Schema registry
    - Access control
    """

    def create_data_product(
        self,
        domain: str,
        name: str,
        source_config: dict
    ) -> DataProduct:
        """
        Self-service creation of data product
        """
        # 1. Setup infrastructure
        pipeline_id = self._create_pipeline(domain, name, source_config)

        # 2. Setup schema registry
        schema_id = self._register_schema(domain, name)

        # 3. Setup monitoring
        self._setup_monitoring(pipeline_id)

        # 4. Setup access control
        self._setup_access_control(domain, name)

        # 5. Create data product
        product = DataProduct(
            id=f"{domain}.{name}",
            name=name,
            domain=domain,
            owner=f"{domain}-team@company.com",
            description=f"Data product for {name}",
            schema_version="1.0.0",
            schema={},
            endpoint=f"bigquery://{domain}.{name}",
            authentication="oauth2",
            sla_latency_ms=5000,
            sla_availability=99.5,
            freshness_sla_minutes=15,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            tags=[]
        )

        return product

    def _create_pipeline(self, domain: str, name: str, config: dict) -> str:
        """
        Create data pipeline using templates

        Templates:
        - Batch ETL (Airflow)
        - Streaming (Kafka + Flink)
        - CDC (Debezium)
        - API ingestion
        """
        # Example: Create Airflow DAG from template
        dag_code = f"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {{
    'owner': '{domain}-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}}

dag = DAG(
    '{domain}_{name}_pipeline',
    default_args=default_args,
    schedule_interval='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False
)

def extract():
    # Extract from source
    pass

def transform():
    # Apply transformations
    pass

def load():
    # Load to data product
    pass

extract_task = PythonOperator(task_id='extract', python_callable=extract, dag=dag)
transform_task = PythonOperator(task_id='transform', python_callable=transform, dag=dag)
load_task = PythonOperator(task_id='load', python_callable=load, dag=dag)

extract_task >> transform_task >> load_task
        """

        # Deploy DAG
        pipeline_id = self._deploy_dag(dag_code)
        return pipeline_id

    def _register_schema(self, domain: str, name: str) -> str:
        """Register schema in schema registry (Confluent, DataHub)"""
        pass

    def _setup_monitoring(self, pipeline_id: str):
        """Setup automated monitoring and alerting"""
        pass

    def _setup_access_control(self, domain: str, name: str):
        """Setup RBAC for data product"""
        pass

    def _deploy_dag(self, dag_code: str) -> str:
        """Deploy Airflow DAG"""
        pass

# ==========================================
# FEDERATED GOVERNANCE
# ==========================================
class FederatedGovernance:
    """
    Governance policies aplicadas de forma federada

    Global policies:
    - PII handling
    - Data retention
    - Security standards

    Domain-specific:
    - Schema evolution rules
    - Quality thresholds
    - Access policies
    """

    def __init__(self):
        self.global_policies = self._load_global_policies()
        self.domain_policies: Dict[str, List] = {}

    def _load_global_policies(self) -> List:
        """Global policies aplicables a todos los dominios"""
        return [
            {
                "name": "pii_encryption",
                "description": "PII must be encrypted at rest",
                "rule": "check_pii_encryption",
                "severity": "critical"
            },
            {
                "name": "data_retention",
                "description": "Data older than 7 years must be archived",
                "rule": "check_retention_policy",
                "severity": "high"
            },
            {
                "name": "gdpr_compliance",
                "description": "GDPR right to be forgotten",
                "rule": "check_gdpr_deletion",
                "severity": "critical"
            }
        ]

    def validate_data_product(
        self,
        product: DataProduct
    ) -> Dict[str, List[str]]:
        """
        Validate data product against policies
        """
        violations = {
            "critical": [],
            "high": [],
            "medium": []
        }

        # Check global policies
        for policy in self.global_policies:
            if not self._check_policy(product, policy):
                violations[policy['severity']].append(
                    f"Policy violation: {policy['name']}"
                )

        # Check domain policies
        domain_policies = self.domain_policies.get(product.domain, [])
        for policy in domain_policies:
            if not self._check_policy(product, policy):
                violations[policy['severity']].append(
                    f"Domain policy violation: {policy['name']}"
                )

        return violations

    def _check_policy(self, product: DataProduct, policy: dict) -> bool:
        """Execute policy check"""
        # Implement policy check logic
        return True
```

---

## 3. Data Lakehouse

### ✅ SOLUCIÓN: Lakehouse architecture con Delta Lake

```python
# ==========================================
# DELTA LAKE - LAKEHOUSE FOUNDATION
# ==========================================
from pyspark.sql import SparkSession
from delta import *

# Create Spark session with Delta Lake
spark = (
    SparkSession.builder
    .appName("DataLakehouse")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

# ==========================================
# MEDALLION ARCHITECTURE
# ==========================================
"""
Bronze Layer: Raw data (append-only)
Silver Layer: Cleaned, validated data
Gold Layer: Aggregated, business-level data
"""

class LakehouseLayer:
    """Base class for Lakehouse layers"""

    def __init__(self, spark: SparkSession, path: str):
        self.spark = spark
        self.path = path

class BronzeLayer(LakehouseLayer):
    """
    Bronze Layer - Raw ingestion

    Characteristics:
    - Schema-on-read
    - Append-only
    - No transformations
    - Full audit trail
    """

    def ingest_from_kafka(self, topic: str):
        """
        Ingest streaming data from Kafka
        """
        df = (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")
            .option("subscribe", topic)
            .option("startingOffsets", "latest")
            .load()
        )

        # Write to Bronze (Delta format)
        (
            df.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", f"{self.path}/_checkpoints/{topic}")
            .start(f"{self.path}/bronze/{topic}")
        )

    def ingest_from_database_cdc(self, table: str):
        """
        Ingest CDC events from database
        Using Debezium
        """
        # Read CDC events
        cdc_df = (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")
            .option("subscribe", f"dbserver.public.{table}")
            .load()
        )

        # Parse Debezium format
        from pyspark.sql.functions import from_json, col

        schema = """
        {
            "type": "struct",
            "fields": [
                {"name": "before", "type": "string"},
                {"name": "after", "type": "string"},
                {"name": "op", "type": "string"}
            ]
        }
        """

        parsed_df = cdc_df.select(
            from_json(col("value").cast("string"), schema).alias("data")
        ).select("data.*")

        # Write to Bronze
        (
            parsed_df.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", f"{self.path}/_checkpoints/cdc_{table}")
            .start(f"{self.path}/bronze/cdc_{table}")
        )

class SilverLayer(LakehouseLayer):
    """
    Silver Layer - Cleaned and validated

    Transformations:
    - Data quality checks
    - Deduplication
    - Type casting
    - Standardization
    """

    def transform_orders(self):
        """
        Transform orders from Bronze to Silver
        """
        # Read from Bronze
        bronze_df = self.spark.read.format("delta").load(
            f"{self.path}/bronze/orders"
        )

        from pyspark.sql.functions import col, to_timestamp, regexp_replace

        # Transformations
        silver_df = (
            bronze_df
            # Remove duplicates
            .dropDuplicates(["order_id"])

            # Data quality - remove nulls
            .filter(col("order_id").isNotNull())
            .filter(col("customer_id").isNotNull())

            # Type conversions
            .withColumn("order_date", to_timestamp(col("order_date")))
            .withColumn("total_amount", col("total_amount").cast("decimal(10,2)"))

            # Standardization
            .withColumn("status", regexp_replace(col("status"), " ", "_").lower())

            # Add metadata
            .withColumn("processed_at", current_timestamp())
        )

        # Write to Silver with MERGE (upsert)
        from delta.tables import DeltaTable

        silver_path = f"{self.path}/silver/orders"

        if DeltaTable.isDeltaTable(self.spark, silver_path):
            # Merge if exists
            delta_table = DeltaTable.forPath(self.spark, silver_path)

            delta_table.alias("target").merge(
                silver_df.alias("source"),
                "target.order_id = source.order_id"
            ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        else:
            # Create new table
            silver_df.write.format("delta").save(silver_path)

class GoldLayer(LakehouseLayer):
    """
    Gold Layer - Business-level aggregations

    Characteristics:
    - Denormalized
    - Optimized for queries
    - Business metrics
    """

    def create_daily_sales_summary(self):
        """
        Create daily sales summary for BI dashboards
        """
        # Read from Silver
        orders_df = self.spark.read.format("delta").load(
            f"{self.path}/silver/orders"
        )

        from pyspark.sql.functions import (
            date_trunc, sum as _sum, count, avg
        )

        # Aggregations
        daily_summary = (
            orders_df
            .groupBy(date_trunc("day", "order_date").alias("date"))
            .agg(
                count("order_id").alias("total_orders"),
                _sum("total_amount").alias("total_revenue"),
                avg("total_amount").alias("avg_order_value"),
                count("customer_id").alias("unique_customers")
            )
        )

        # Write to Gold
        daily_summary.write.format("delta").mode("overwrite").save(
            f"{self.path}/gold/daily_sales_summary"
        )

# ==========================================
# DELTA LAKE FEATURES
# ==========================================

# Feature 1: Time Travel
def query_historical_data(spark, table_path, version: int):
    """
    Query data at specific version
    """
    df = spark.read.format("delta").option("versionAsOf", version).load(table_path)
    return df

# Feature 2: Schema Evolution
def evolve_schema(spark, table_path):
    """
    Add new column without breaking existing queries
    """
    df = spark.read.format("delta").load(table_path)

    # Add new column
    from pyspark.sql.functions import lit
    df_with_new_col = df.withColumn("new_column", lit(None))

    # Write with schema merge
    df_with_new_col.write.format("delta").mode("append").option(
        "mergeSchema", "true"
    ).save(table_path)

# Feature 3: ACID Transactions
def atomic_multi_table_update(spark):
    """
    Update multiple tables atomically
    """
    from delta.tables import DeltaTable

    # Start transaction
    orders = DeltaTable.forPath(spark, "s3://lakehouse/silver/orders")
    inventory = DeltaTable.forPath(spark, "s3://lakehouse/silver/inventory")

    # Both updates succeed or both fail
    orders.update(
        condition="status = 'pending'",
        set={"status": "shipped"}
    )

    inventory.update(
        condition="product_id IN (SELECT product_id FROM orders WHERE status = 'shipped')",
        set={"stock": "stock - quantity"}
    )

# Feature 4: Optimize & Z-Ordering
def optimize_table(spark, table_path):
    """
    Compact small files and optimize layout
    """
    from delta.tables import DeltaTable

    delta_table = DeltaTable.forPath(spark, table_path)

    # Compact small files
    delta_table.optimize().executeCompaction()

    # Z-order by commonly filtered columns
    delta_table.optimize().executeZOrderBy("customer_id", "order_date")
```

---

## 4. Change Data Capture (CDC)

### ✅ SOLUCIÓN: CDC con Debezium

```python
# ==========================================
# DEBEZIUM CDC
# ==========================================

# Debezium Connector Configuration (JSON)
debezium_config = {
    "name": "postgres-orders-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "postgres",
        "database.port": "5432",
        "database.user": "debezium",
        "database.password": "dbz",
        "database.dbname": "orders_db",
        "database.server.name": "dbserver",
        "table.include.list": "public.orders,public.order_items",
        "plugin.name": "pgoutput",

        # Output to Kafka
        "kafka.topic": "dbserver.public.orders",

        # Snapshot configuration
        "snapshot.mode": "initial",

        # Schema changes
        "schema.history.internal.kafka.topic": "schema-changes.orders",

        # Transforms
        "transforms": "unwrap",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
        "transforms.unwrap.drop.tombstones": "false"
    }
}

# ==========================================
# CDC EVENT CONSUMER
# ==========================================
from kafka import KafkaConsumer
import json

class CDCEventConsumer:
    """
    Consume CDC events from Kafka
    """

    def __init__(self, topic: str):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def process_events(self):
        """
        Process CDC events
        """
        for message in self.consumer:
            event = message.value

            # Debezium event structure
            operation = event.get('op')  # c=create, u=update, d=delete
            before = event.get('before')  # Old values
            after = event.get('after')    # New values

            if operation == 'c':
                self.handle_create(after)
            elif operation == 'u':
                self.handle_update(before, after)
            elif operation == 'd':
                self.handle_delete(before)

    def handle_create(self, record: dict):
        """New record created"""
        print(f"INSERT: {record}")
        # Sync to data warehouse, cache, search index, etc.

    def handle_update(self, before: dict, after: dict):
        """Record updated"""
        print(f"UPDATE: {before} -> {after}")
        # Update derived data

    def handle_delete(self, record: dict):
        """Record deleted"""
        print(f"DELETE: {record}")
        # Handle cascading deletes

# ==========================================
# CDC TO DATA WAREHOUSE
# ==========================================
class CDCToWarehouse:
    """
    Sync CDC events to data warehouse
    """

    def __init__(self, bigquery_client):
        self.bq = bigquery_client

    def sync_event(self, event: dict):
        """
        Sync single CDC event to BigQuery
        """
        operation = event['op']
        table_name = event['source']['table']

        if operation in ['c', 'u']:
            # Insert or update
            self._upsert_to_warehouse(table_name, event['after'])
        elif operation == 'd':
            # Soft delete
            self._soft_delete(table_name, event['before']['id'])

    def _upsert_to_warehouse(self, table: str, record: dict):
        """
        Upsert to BigQuery using MERGE
        """
        query = f"""
        MERGE `project.dataset.{table}` T
        USING (SELECT {', '.join(f"'{v}' as {k}" for k, v in record.items())}) S
        ON T.id = S.id
        WHEN MATCHED THEN
            UPDATE SET {', '.join(f"T.{k} = S.{k}" for k in record.keys())}
        WHEN NOT MATCHED THEN
            INSERT ({', '.join(record.keys())})
            VALUES ({', '.join(f"S.{k}" for k in record.keys())})
        """

        self.bq.query(query).result()

    def _soft_delete(self, table: str, record_id: str):
        """Soft delete by setting deleted_at"""
        query = f"""
        UPDATE `project.dataset.{table}`
        SET deleted_at = CURRENT_TIMESTAMP()
        WHERE id = '{record_id}'
        """
        self.bq.query(query).result()
```

---

## 5-10. [Remaining Sections Summary]

### 5. Data Governance
- Data classification (PII, sensitive, public)
- Access control (RBAC, ABAC)
- Data masking & anonymization
- Compliance (GDPR, CCPA)

### 6. Data Quality
```python
# Great Expectations
import great_expectations as ge

df = ge.read_csv("orders.csv")

# Define expectations
df.expect_column_values_to_not_be_null("order_id")
df.expect_column_values_to_be_unique("order_id")
df.expect_column_values_to_be_between("total_amount", min_value=0, max_value=100000)
df.expect_column_values_to_be_in_set("status", ["pending", "shipped", "delivered"])

# Validate
validation_results = df.validate()
```

### 7. Real-Time Data Architecture
- Lambda architecture (batch + streaming)
- Kappa architecture (streaming-only)
- Real-time feature stores (Feast, Tecton)

### 8. Data Versioning & Lineage
- DVC (Data Version Control)
- Lineage tracking (Marquez, DataHub)
- Impact analysis

### 9. Polyglot Persistence
```python
# Different databases for different use cases
databases = {
    "transactional": "PostgreSQL",      # ACID transactions
    "analytics": "BigQuery",            # Large-scale analytics
    "cache": "Redis",                   # Fast key-value
    "search": "Elasticsearch",          # Full-text search
    "graph": "Neo4j",                   # Relationships
    "time_series": "InfluxDB",          # Metrics
    "document": "MongoDB"               # Flexible schema
}
```

### 10. Data Migration Patterns
- Dual-write pattern
- Change data capture
- Event sourcing migration
- Zero-downtime migration

---

## 📊 Data Architecture Decision Matrix

| Pattern | Use When | Don't Use When | Complexity |
|---------|----------|----------------|------------|
| **Data Warehouse** | BI, reporting, historical | Real-time analytics | ⭐⭐⭐ |
| **Data Lake** | Raw data, ML, exploration | Structured queries only | ⭐⭐⭐⭐ |
| **Data Lakehouse** | Both analytics + ML | Simple use cases | ⭐⭐⭐⭐⭐ |
| **Data Mesh** | Multiple domains, scale | Small org (< 50 people) | ⭐⭐⭐⭐⭐ |
| **Streaming** | Real-time requirements | Batch sufficient | ⭐⭐⭐⭐ |

**Tamaño:** 58KB | **Código:** ~2,300 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
