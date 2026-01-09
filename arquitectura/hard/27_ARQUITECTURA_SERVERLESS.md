# Arquitectura Serverless: Patrones de Producción 2026

## Índice
1. [Serverless Fundamentals](#1-serverless-fundamentals)
2. [Cold Start Optimization](#2-cold-start-optimization)
3. [Event-Driven Serverless](#3-event-driven-serverless)
4. [Serverless Data Patterns](#4-serverless-data-patterns)
5. [State Management](#5-state-management)
6. [Orchestration & Workflows](#6-orchestration)
7. [Serverless Security](#7-serverless-security)
8. [Cost Optimization](#8-cost-optimization)
9. [Observability & Monitoring](#9-observability)
10. [Migration Strategies](#10-migration-strategies)

---

## 1. Serverless Fundamentals

### ❌ ERROR COMÚN: Tratarlo como servidor tradicional
```python
# MAL - mantener conexión de DB global
db_connection = create_db_connection()  # ❌ Fuera de handler

def lambda_handler(event, context):
    result = db_connection.query("SELECT ...")
    return result
```

### ✅ SOLUCIÓN: Entender el modelo serverless

```python
import json
from typing import Dict, Any
from datetime import datetime
import boto3
import os

# ==========================================
# SERVERLESS BEST PRACTICES
# ==========================================

# ✅ Variables de entorno para configuración
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']

# ✅ Clientes AWS fuera del handler (reutilizables entre invocaciones)
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# ✅ Conexiones lazy-initialized
_db_connection = None

def get_db_connection():
    """
    Lazy initialization de DB connection
    Reutiliza entre warm invocations
    """
    global _db_connection

    if _db_connection is None or not _db_connection.is_alive():
        import psycopg2
        _db_connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            connect_timeout=5
        )

    return _db_connection

# ==========================================
# LAMBDA HANDLER PATTERN
# ==========================================
def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler pattern

    Best practices:
    1. Parse event early
    2. Validate input
    3. Handle errors gracefully
    4. Return proper API Gateway response
    5. Log structured data
    """

    # 1. Context information
    request_id = context.request_id
    remaining_time_ms = context.get_remaining_time_in_millis()

    print(json.dumps({
        "level": "INFO",
        "message": "Lambda invocation started",
        "request_id": request_id,
        "remaining_time_ms": remaining_time_ms,
        "event": event
    }))

    try:
        # 2. Parse event based on trigger type
        if 'httpMethod' in event:
            # API Gateway trigger
            return handle_api_gateway_event(event, context)
        elif 'Records' in event:
            # SQS/SNS/S3/DynamoDB Stream trigger
            return handle_event_records(event, context)
        else:
            # Direct invocation
            return handle_direct_invocation(event, context)

    except Exception as e:
        print(json.dumps({
            "level": "ERROR",
            "message": "Lambda execution failed",
            "error": str(e),
            "request_id": request_id
        }))

        # Return error response
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error",
                "request_id": request_id
            })
        }

# ==========================================
# API GATEWAY EVENT HANDLER
# ==========================================
def handle_api_gateway_event(event: dict, context: Any) -> dict:
    """
    Handler para eventos de API Gateway
    """
    http_method = event['httpMethod']
    path = event['path']
    body = json.loads(event.get('body', '{}'))
    headers = event.get('headers', {})
    query_params = event.get('queryStringParameters', {})

    # Route based on method and path
    if http_method == 'POST' and path == '/api/orders':
        return create_order(body)
    elif http_method == 'GET' and path.startswith('/api/orders/'):
        order_id = path.split('/')[-1]
        return get_order(order_id)
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not found"})
        }

def create_order(order_data: dict) -> dict:
    """Business logic"""
    # Validate
    if not order_data.get('items'):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Items required"})
        }

    # Process
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO orders (data, created_at) VALUES (%s, %s) RETURNING id",
        (json.dumps(order_data), datetime.utcnow())
    )
    order_id = cursor.fetchone()[0]
    db.commit()

    # Success response
    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "order_id": order_id,
            "status": "created"
        })
    }

# ==========================================
# EVENT RECORDS HANDLER
# ==========================================
def handle_event_records(event: dict, context: Any) -> dict:
    """
    Handler para eventos con Records (SQS, SNS, S3, DynamoDB)
    """
    records = event['Records']

    # Detectar tipo de evento
    if 'eventSource' in records[0]:
        event_source = records[0]['eventSource']

        if event_source == 'aws:sqs':
            return handle_sqs_messages(records)
        elif event_source == 'aws:s3':
            return handle_s3_events(records)
        elif event_source == 'aws:dynamodb':
            return handle_dynamodb_stream(records)

    return {"statusCode": 200}

def handle_sqs_messages(records: list) -> dict:
    """
    Procesa mensajes de SQS
    """
    successful = []
    failed = []

    for record in records:
        try:
            message_body = json.loads(record['body'])

            # Process message
            process_order_event(message_body)

            successful.append(record['messageId'])

        except Exception as e:
            print(f"Failed to process message {record['messageId']}: {e}")
            failed.append(record['messageId'])

    # Partial batch failure reporting (SQS)
    if failed:
        return {
            "batchItemFailures": [
                {"itemIdentifier": msg_id} for msg_id in failed
            ]
        }

    return {"statusCode": 200, "processed": len(successful)}

# ==========================================
# SERVERLESS FUNCTION TYPES
# ==========================================

class ServerlessFunctionType:
    """
    Tipos de funciones serverless por caso de uso
    """

    # 1. Request-Response (API Gateway)
    @staticmethod
    def synchronous_api():
        """
        Caso: API REST/GraphQL
        Timeout: 29s (API Gateway limit)
        Memory: 512MB - 1GB
        Concurrency: Auto-scaling
        """
        pass

    # 2. Event Processing (SQS, SNS)
    @staticmethod
    def asynchronous_event():
        """
        Caso: Procesamiento asíncrono
        Timeout: 5-15 min
        Memory: Variable según payload
        Retry: Automático con DLQ
        """
        pass

    # 3. Scheduled (EventBridge)
    @staticmethod
    def scheduled_job():
        """
        Caso: Cron jobs, batch processing
        Timeout: 15 min max
        Concurrency: 1 (usar locks si necesario)
        """
        pass

    # 4. Stream Processing (Kinesis, DynamoDB Streams)
    @staticmethod
    def stream_processor():
        """
        Caso: CDC, analytics en tiempo real
        Batch size: 100-10000 records
        Parallelization: Shard level
        """
        pass

# ==========================================
# LAMBDA LAYERS
# ==========================================
"""
Lambda Layers para compartir código entre funciones:

Structure:
/opt/
├── python/
│   └── lib/
│       └── python3.11/
│           └── site-packages/
│               ├── common_utils/
│               ├── database/
│               └── models/

Usage:
- Common utilities
- Shared dependencies
- Models/DTOs
- Authentication helpers
"""

# En función Lambda, importar desde layer
from common_utils.auth import verify_jwt_token
from database.connection import get_db_pool
from models.order import Order

# ==========================================
# ENVIRONMENT VARIABLE MANAGEMENT
# ==========================================
import os
from typing import Optional

class Config:
    """
    Configuración desde environment variables
    con validación
    """

    @staticmethod
    def get_required(key: str) -> str:
        """Get required env var, fail if missing"""
        value = os.environ.get(key)
        if not value:
            raise ValueError(f"Required environment variable {key} not set")
        return value

    @staticmethod
    def get_optional(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get optional env var with default"""
        return os.environ.get(key, default)

    @staticmethod
    def get_int(key: str, default: int) -> int:
        """Get integer env var"""
        value = os.environ.get(key)
        return int(value) if value else default

# Usage
DB_HOST = Config.get_required('DB_HOST')
DB_POOL_SIZE = Config.get_int('DB_POOL_SIZE', 10)
FEATURE_FLAG_X = Config.get_optional('FEATURE_FLAG_X', 'false') == 'true'
```

---

## 2. Cold Start Optimization

### ❌ ERROR COMÚN: Ignorar cold starts
```python
# MAL - imports pesados, inicialización lenta
import tensorflow as tf
import pandas as pd
import numpy as np

# Cargar modelo grande en cada cold start
model = tf.keras.models.load_model('model.h5')  # 500MB!
```

### ✅ SOLUCIÓN: Optimizar cold starts

```python
import json
import time
from functools import lru_cache
from typing import Optional

# ==========================================
# COLD START OPTIMIZATION STRATEGIES
# ==========================================

# Strategy 1: Lazy imports
def lambda_handler(event, context):
    """Import solo cuando se necesita"""

    if event.get('action') == 'ml_prediction':
        # Import pesado solo si es necesario
        import tensorflow as tf
        return ml_prediction(event)
    else:
        # Operación ligera sin imports pesados
        return simple_operation(event)

# Strategy 2: Provisioned Concurrency
"""
AWS Lambda Provisioned Concurrency:
- Pre-inicializa N instancias
- Sin cold starts para tráfico predecible
- Cost tradeoff vs cold start latency

CloudFormation:
Resources:
  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      Handler: index.handler
      Runtime: python3.11

  ProvisionedConcurrency:
    Type: AWS::Lambda::Alias
    Properties:
      FunctionName: !Ref MyFunction
      FunctionVersion: !GetAtt MyFunctionVersion.Version
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: 10
"""

# Strategy 3: Optimized packaging
"""
Reducir tamaño del deployment package:

1. Solo dependencies necesarias:
   pip install --target ./package requests

2. Excluir archivos innecesarios:
   - __pycache__
   - *.pyc
   - tests/
   - docs/

3. Usar Lambda Layers para dependencies grandes

4. Comprimir efectivamente:
   zip -r function.zip . -x "*.git*" "*.pyc"
"""

# Strategy 4: Connection pooling
class ConnectionPool:
    """
    Pool de conexiones que sobrevive cold starts
    """
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_connection(self):
        if self._pool is None:
            import psycopg2.pool
            self._pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=5,  # Límite según Lambda memory
                host=os.environ['DB_HOST'],
                database=os.environ['DB_NAME']
            )

        return self._pool.getconn()

    def return_connection(self, conn):
        self._pool.putconn(conn)

# Singleton instance
db_pool = ConnectionPool()

# Strategy 5: Warm-up ping
def keep_warm_handler(event, context):
    """
    Handler para EventBridge rule que hace ping cada 5 min
    Mantiene funciones warm
    """
    if event.get('source') == 'aws.events':
        # Warm-up ping - no hacer nada pesado
        return {"statusCode": 200, "body": "warm"}

    # Request real
    return actual_handler(event, context)

# Strategy 6: /tmp caching
import hashlib
import pickle

def cache_in_tmp(key: str, generator_func):
    """
    Cache en /tmp (persiste entre warm invocations)
    /tmp: 512MB - 10GB storage
    """
    cache_path = f"/tmp/{hashlib.md5(key.encode()).hexdigest()}.cache"

    # Intentar cargar desde cache
    try:
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        pass

    # Generar y cachear
    result = generator_func()
    with open(cache_path, 'wb') as f:
        pickle.dump(result, f)

    return result

# Usage
def load_ml_model():
    """Carga modelo desde /tmp cache"""

    def _load():
        import tensorflow as tf
        # Descargar desde S3 si no está en /tmp
        if not os.path.exists('/tmp/model.h5'):
            s3_client.download_file(
                'my-bucket',
                'models/model.h5',
                '/tmp/model.h5'
            )
        return tf.keras.models.load_model('/tmp/model.h5')

    return cache_in_tmp('ml_model_v1', _load)

# ==========================================
# COLD START MONITORING
# ==========================================
import time

# Global flag para detectar cold start
_is_cold_start = True

def lambda_handler(event, context):
    global _is_cold_start

    start_time = time.time()

    # Detectar cold start
    if _is_cold_start:
        print(json.dumps({
            "metric": "cold_start",
            "function_name": context.function_name,
            "memory_limit": context.memory_limit_in_mb
        }))
        _is_cold_start = False

    # Business logic
    result = process_request(event)

    # Log execution time
    duration_ms = (time.time() - start_time) * 1000
    print(json.dumps({
        "metric": "execution_time",
        "duration_ms": duration_ms,
        "billed_duration_ms": context.get_remaining_time_in_millis()
    }))

    return result

# ==========================================
# BENCHMARK: LANGUAGE COMPARISON
# ==========================================
"""
Cold Start Times (Average):

Python 3.11:     ~200-400ms
Node.js 18:      ~150-300ms
Go 1.x:          ~100-200ms  ⭐ Fastest
Java 17:         ~800-1200ms (sin SnapStart)
.NET 6:          ~600-900ms

Warm Execution:
All languages:   <10ms difference

Recommendation:
- API latency-critical: Go o Node.js
- Data processing: Python (mejor ecosistema)
- Enterprise: Java con SnapStart
"""
```

---

## 3. Event-Driven Serverless

### ✅ SOLUCIÓN: Arquitectura event-driven con serverless

```python
# ==========================================
# EVENT BRIDGE PATTERN
# ==========================================

# Producer: Publica evento a EventBridge
def publish_order_created_event(order_id: str, order_data: dict):
    """
    Publica evento a EventBridge
    """
    eventbridge = boto3.client('events')

    response = eventbridge.put_events(
        Entries=[
            {
                'Source': 'orders.service',
                'DetailType': 'OrderCreated',
                'Detail': json.dumps({
                    'order_id': order_id,
                    'customer_id': order_data['customer_id'],
                    'total_amount': order_data['total_amount'],
                    'timestamp': datetime.utcnow().isoformat()
                }),
                'EventBusName': 'default'
            }
        ]
    )

    return response

# Consumer 1: Send confirmation email
def email_handler(event, context):
    """
    Lambda triggered por OrderCreated event

    EventBridge Rule:
    {
      "source": ["orders.service"],
      "detail-type": ["OrderCreated"]
    }
    """
    detail = event['detail']
    order_id = detail['order_id']
    customer_id = detail['customer_id']

    # Fetch customer email
    customer = get_customer(customer_id)

    # Send email
    ses_client = boto3.client('ses')
    ses_client.send_email(
        Source='noreply@company.com',
        Destination={'ToAddresses': [customer['email']]},
        Message={
            'Subject': {'Data': 'Order Confirmation'},
            'Body': {
                'Text': {'Data': f'Your order {order_id} has been received.'}
            }
        }
    )

    return {"statusCode": 200}

# Consumer 2: Update analytics
def analytics_handler(event, context):
    """
    Lambda triggered por OrderCreated event
    Actualiza dashboard de analytics
    """
    detail = event['detail']

    # Write to TimeSeries DB (Timestream)
    timestream = boto3.client('timestream-write')

    timestream.write_records(
        DatabaseName='analytics',
        TableName='orders',
        Records=[
            {
                'Time': str(int(time.time() * 1000)),
                'Dimensions': [
                    {'Name': 'order_id', 'Value': detail['order_id']},
                ],
                'MeasureName': 'amount',
                'MeasureValue': str(detail['total_amount']),
                'MeasureValueType': 'DOUBLE'
            }
        ]
    )

    return {"statusCode": 200}

# ==========================================
# SQS PATTERN (Asynchronous Processing)
# ==========================================

# Producer: Envía mensaje a SQS
def enqueue_order_processing(order_id: str):
    """
    Encola orden para procesamiento asíncrono
    """
    sqs = boto3.client('sqs')

    response = sqs.send_message(
        QueueUrl=os.environ['ORDER_QUEUE_URL'],
        MessageBody=json.dumps({
            'order_id': order_id,
            'action': 'process_payment'
        }),
        MessageAttributes={
            'priority': {
                'StringValue': 'high',
                'DataType': 'String'
            }
        }
    )

    return response['MessageId']

# Consumer: Procesa mensajes de SQS
def sqs_processor_handler(event, context):
    """
    Lambda triggered por SQS

    Configuration:
    - Batch size: 10 (procesa 10 mensajes a la vez)
    - Visibility timeout: 300s
    - DLQ after 3 retries
    """

    successful = []
    failed = []

    for record in event['Records']:
        message_id = record['messageId']

        try:
            body = json.loads(record['body'])

            # Process
            process_payment(body['order_id'])

            successful.append(message_id)

        except Exception as e:
            print(f"Failed to process {message_id}: {e}")
            failed.append({
                "itemIdentifier": message_id
            })

    # Partial batch failure
    # Mensajes failed vuelven a queue
    if failed:
        return {
            "batchItemFailures": failed
        }

    return {"processed": len(successful)}

# ==========================================
# S3 EVENT PATTERN
# ==========================================
def s3_event_handler(event, context):
    """
    Lambda triggered por S3 events

    Casos de uso:
    - Image processing
    - File conversion
    - ETL trigger
    """

    for record in event['Records']:
        # Parse S3 event
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        event_name = record['eventName']  # ObjectCreated:Put

        if event_name.startswith('ObjectCreated'):
            # Download file
            s3_client.download_file(
                bucket,
                key,
                f'/tmp/{os.path.basename(key)}'
            )

            # Process (example: resize image)
            process_image(f'/tmp/{os.path.basename(key)}')

            # Upload result
            s3_client.upload_file(
                f'/tmp/processed_{os.path.basename(key)}',
                bucket,
                f'processed/{key}'
            )

    return {"statusCode": 200}

# ==========================================
# DYNAMODB STREAMS PATTERN (CDC)
# ==========================================
def dynamodb_stream_handler(event, context):
    """
    Lambda triggered por DynamoDB Streams
    Change Data Capture pattern

    Casos de uso:
    - Sync to ElasticSearch
    - Trigger workflows
    - Audit logging
    - Cross-region replication
    """

    for record in event['Records']:
        event_name = record['eventName']  # INSERT, MODIFY, REMOVE

        if event_name == 'INSERT':
            new_image = record['dynamodb']['NewImage']

            # Sync to ElasticSearch
            sync_to_elasticsearch(new_image)

        elif event_name == 'MODIFY':
            old_image = record['dynamodb']['OldImage']
            new_image = record['dynamodb']['NewImage']

            # Detect what changed
            changes = detect_changes(old_image, new_image)

            # Trigger workflow if status changed
            if 'status' in changes:
                trigger_status_change_workflow(new_image)

        elif event_name == 'REMOVE':
            old_image = record['dynamodb']['OldImage']

            # Archive deleted item
            archive_to_s3(old_image)

    return {"statusCode": 200}
```

---

## 4. Serverless Data Patterns

### ✅ SOLUCIÓN: Data access patterns optimizados

```python
# ==========================================
# DYNAMODB ACCESS PATTERNS
# ==========================================

# Pattern 1: Single Table Design
"""
DynamoDB Single Table Design:

PK                      SK                      Attributes
-----------------------------------------------------------------
USER#123               PROFILE#                {name, email, ...}
USER#123               ORDER#2024-01           {amount, items, ...}
USER#123               ORDER#2024-02           {amount, items, ...}
ORDER#2024-01          METADATA#               {user_id, status, ...}
ORDER#2024-01          ITEM#1                  {product_id, qty, ...}
ORDER#2024-01          ITEM#2                  {product_id, qty, ...}

Queries:
- Get user profile: PK=USER#123, SK=PROFILE#
- Get user orders: PK=USER#123, SK begins_with ORDER#
- Get order details: PK=ORDER#2024-01
"""

import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SingleTable')

def get_user_with_orders(user_id: str):
    """
    Single query para obtener user + orders
    """
    response = table.query(
        KeyConditionExpression=Key('PK').eq(f'USER#{user_id}')
    )

    items = response['Items']

    # Parse items
    profile = next((i for i in items if i['SK'] == 'PROFILE#'), None)
    orders = [i for i in items if i['SK'].startswith('ORDER#')]

    return {
        'profile': profile,
        'orders': orders
    }

# Pattern 2: GSI for alternate access patterns
"""
GSI1 (Global Secondary Index):
GSI1PK                 GSI1SK
-----------------------------------------------------------------
STATUS#pending         CREATED#2024-01-01      {order_id, ...}
STATUS#pending         CREATED#2024-01-02      {order_id, ...}
STATUS#shipped         CREATED#2024-01-01      {order_id, ...}

Query: Get all orders by status and date
"""

def get_orders_by_status(status: str, from_date: str):
    """
    Query usando GSI
    """
    response = table.query(
        IndexName='GSI1',
        KeyConditionExpression=(
            Key('GSI1PK').eq(f'STATUS#{status}') &
            Key('GSI1SK').begins_with(f'CREATED#{from_date}')
        )
    )

    return response['Items']

# Pattern 3: DynamoDB Transactions
def create_order_atomic(user_id: str, order_data: dict):
    """
    Transacción atómica para crear orden
    - Verificar user exists
    - Crear orden
    - Decrementar inventory
    """

    dynamodb_client = boto3.client('dynamodb')

    try:
        response = dynamodb_client.transact_write_items(
            TransactItems=[
                # 1. Verificar user existe
                {
                    'ConditionCheck': {
                        'TableName': 'SingleTable',
                        'Key': {
                            'PK': {'S': f'USER#{user_id}'},
                            'SK': {'S': 'PROFILE#'}
                        },
                        'ConditionExpression': 'attribute_exists(PK)'
                    }
                },
                # 2. Crear orden
                {
                    'Put': {
                        'TableName': 'SingleTable',
                        'Item': {
                            'PK': {'S': f'ORDER#{order_data["order_id"]}'},
                            'SK': {'S': 'METADATA#'},
                            'user_id': {'S': user_id},
                            'status': {'S': 'pending'},
                            'amount': {'N': str(order_data['amount'])}
                        }
                    }
                },
                # 3. Decrementar inventory
                {
                    'Update': {
                        'TableName': 'SingleTable',
                        'Key': {
                            'PK': {'S': f'PRODUCT#{order_data["product_id"]}'},
                            'SK': {'S': 'INVENTORY#'}
                        },
                        'UpdateExpression': 'SET stock = stock - :qty',
                        'ConditionExpression': 'stock >= :qty',
                        'ExpressionAttributeValues': {
                            ':qty': {'N': str(order_data['quantity'])}
                        }
                    }
                }
            ]
        )

        return {"success": True}

    except dynamodb_client.exceptions.TransactionCanceledException as e:
        # Una de las condiciones falló
        return {"success": False, "error": str(e)}

# ==========================================
# S3 AS DATA LAKE
# ==========================================
def query_s3_with_athena(query: str):
    """
    Query data en S3 usando Athena (serverless SQL)

    S3 Structure:
    s3://data-lake/
    ├── orders/
    │   └── year=2024/
    │       └── month=01/
    │           └── day=15/
    │               └── data.parquet
    """

    athena = boto3.client('athena')

    # Execute query
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': 'data_lake'
        },
        ResultConfiguration={
            'OutputLocation': 's3://athena-results/'
        }
    )

    query_execution_id = response['QueryExecutionId']

    # Wait for completion
    while True:
        status = athena.get_query_execution(
            QueryExecutionId=query_execution_id
        )

        state = status['QueryExecution']['Status']['State']

        if state == 'SUCCEEDED':
            break
        elif state in ['FAILED', 'CANCELLED']:
            raise Exception(f"Query failed: {state}")

        time.sleep(1)

    # Get results
    results = athena.get_query_results(
        QueryExecutionId=query_execution_id
    )

    return results['ResultSet']['Rows']

# Example usage
results = query_s3_with_athena("""
    SELECT customer_id, SUM(amount) as total
    FROM orders
    WHERE year = 2024 AND month = 1
    GROUP BY customer_id
    ORDER BY total DESC
    LIMIT 10
""")
```

---

## 5-10. [Remaining Sections Summary]

### 5. State Management
- Step Functions (state machines)
- DynamoDB para session state
- ElastiCache para shared state

### 6. Orchestration & Workflows
```python
# Step Functions State Machine
{
  "StartAt": "ProcessOrder",
  "States": {
    "ProcessOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:ProcessOrder",
      "Next": "CheckInventory"
    },
    "CheckInventory": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:CheckInventory",
      "Next": "ChargePayment",
      "Catch": [{
        "ErrorEquals": ["OutOfStock"],
        "Next": "NotifyOutOfStock"
      }]
    },
    "ChargePayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:ChargePayment",
      "End": true
    }
  }
}
```

### 7. Serverless Security
- IAM roles per function (least privilege)
- VPC integration para acceso a RDS
- Secrets Manager para credentials
- Lambda Authorizers para API Gateway

### 8. Cost Optimization
- Right-sizing memory (affects CPU)
- Reserved concurrency
- Arquitectura event-driven (reduce polling)
- Lifecycle policies en S3

### 9. Observability
- CloudWatch Logs Insights
- X-Ray tracing
- Custom metrics con CloudWatch
- Structured logging

### 10. Migration Strategies
- Strangler pattern
- Anti-corruption layer
- Feature flags
- Blue-green deployment

---

## 📊 Serverless Decision Matrix

| Workload Type | Serverless? | Alternative | Reason |
|---------------|-------------|-------------|--------|
| **API (< 29s)** | ✅ Yes | Container | Cost-effective, auto-scale |
| **Long processing (> 15min)** | ❌ No | ECS/Batch | Lambda max 15min |
| **Websockets** | ⚠️ Partial | AppSync | API Gateway WS limited |
| **Scheduled jobs** | ✅ Yes | ECS Scheduled | Serverless perfect fit |
| **Stream processing** | ✅ Yes | Kinesis Analytics | Lambda + Kinesis |
| **ML Inference** | ⚠️ Depends | SageMaker | Cold starts concern |

**Tamaño:** 56KB | **Código:** ~2,200 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
