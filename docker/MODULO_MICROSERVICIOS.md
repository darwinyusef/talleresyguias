# Módulo: Arquitectura de Microservicios con Docker

## Objetivo
Diseñar, implementar y desplegar arquitecturas de microservicios usando Docker, orquestación y mejores prácticas.

---

## Índice
1. [Introducción a Microservicios](#introducción)
2. [Diseño de Arquitectura](#diseño)
3. [Comunicación entre Servicios](#comunicación)
4. [Service Discovery](#service-discovery)
5. [API Gateway](#api-gateway)
6. [Ejemplo Completo: E-Commerce](#ejemplo-completo)

---

## Introducción a Microservicios

### Monolito vs Microservicios

**Monolito:**
```
┌──────────────────────────┐
│      Aplicación          │
│  ┌────────────────────┐  │
│  │ UI                 │  │
│  ├────────────────────┤  │
│  │ Business Logic     │  │
│  ├────────────────────┤  │
│  │ Data Access        │  │
│  └────────────────────┘  │
│                          │
│  ┌────────────────────┐  │
│  │    Database        │  │
│  └────────────────────┘  │
└──────────────────────────┘
```

**Microservicios:**
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   User      │  │   Product   │  │   Order     │
│   Service   │  │   Service   │  │   Service   │
├─────────────┤  ├─────────────┤  ├─────────────┤
│   User DB   │  │  Product DB │  │   Order DB  │
└─────────────┘  └─────────────┘  └─────────────┘
       │                │                │
       └────────────────┴────────────────┘
                       │
                ┌──────▼──────┐
                │ API Gateway │
                └─────────────┘
```

### Ventajas de Microservicios

✅ Escalado independiente
✅ Deployment independiente
✅ Tecnologías específicas por servicio
✅ Equipos autónomos
✅ Resiliencia (fallas aisladas)

### Desventajas

❌ Complejidad operacional
❌ Testing más complejo
❌ Comunicación entre servicios
❌ Data consistency
❌ Overhead de red

---

## Diseño de Arquitectura

### Principios Fundamentales

1. **Single Responsibility** - Un servicio, una función
2. **Loose Coupling** - Dependencias mínimas
3. **High Cohesion** - Funcionalidad relacionada junta
4. **Database per Service** - Cada servicio su BD
5. **API First** - Contratos claros

### Bounded Contexts (DDD)

```
E-Commerce System
├── User Management Context
│   ├── Authentication
│   ├── Profiles
│   └── Permissions
├── Product Catalog Context
│   ├── Products
│   ├── Categories
│   └── Inventory
├── Order Management Context
│   ├── Cart
│   ├── Orders
│   └── Payments
└── Shipping Context
    ├── Logistics
    └── Tracking
```

### Patrones de Diseño

**1. API Gateway Pattern**
```
Client → API Gateway → Services
```

**2. Backend for Frontend (BFF)**
```
Mobile App → Mobile BFF → Services
Web App → Web BFF → Services
```

**3. Saga Pattern (Transacciones distribuidas)**
```
Order Service → Payment Service → Inventory Service → Shipping Service
     ↓                ↓                  ↓                    ↓
   Success?        Success?          Success?            Success?
     │                │                  │                    │
     └────────────────┴──────────────────┴────────────────────┘
                          Compensate if any fails
```

**4. CQRS (Command Query Responsibility Segregation)**
```
Write Model (Commands) → Write DB
Read Model (Queries) → Read DB (optimized for reads)
```

---

## Comunicación entre Servicios

### 1. REST (Síncrono)

**User Service (FastAPI):**
```python
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/users/{user_id}/orders")
async def get_user_orders(user_id: int):
    # Llamar a Order Service
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://order-service:8000/orders?user_id={user_id}")
        orders = response.json()

    return {"user_id": user_id, "orders": orders}
```

**Order Service (Node.js):**
```javascript
const express = require('express')
const axios = require('axios')

const app = express()

app.get('/orders/:id', async (req, res) => {
  const orderId = req.params.id

  // Llamar a Product Service
  const product = await axios.get(`http://product-service:3000/products/${productId}`)

  res.json({ order, product: product.data })
})
```

### 2. gRPC (Síncrono, más eficiente)

**product.proto:**
```protobuf
syntax = "proto3";

service ProductService {
  rpc GetProduct (ProductRequest) returns (Product);
  rpc ListProducts (Empty) returns (ProductList);
}

message ProductRequest {
  int32 id = 1;
}

message Product {
  int32 id = 1;
  string name = 2;
  double price = 3;
}

message ProductList {
  repeated Product products = 1;
}
```

### 3. Message Queue (Asíncrono)

**Con RabbitMQ:**
```python
# Order Service - Publisher
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='orders', exchange_type='topic')

# Publicar evento
order_created = {
    'order_id': 123,
    'user_id': 456,
    'total': 99.99
}

channel.basic_publish(
    exchange='orders',
    routing_key='order.created',
    body=json.dumps(order_created)
)
```

```python
# Inventory Service - Consumer
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='orders', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='orders', queue=queue_name, routing_key='order.created')

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"Processing order {order['order_id']}")
    # Reducir inventory...

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

### 4. Event Streaming (Kafka)

```javascript
// Order Service - Producer
const { Kafka } = require('kafkajs')

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: ['kafka:9092']
})

const producer = kafka.producer()

await producer.connect()
await producer.send({
  topic: 'order-events',
  messages: [
    {
      key: `order-${orderId}`,
      value: JSON.stringify({
        type: 'ORDER_CREATED',
        orderId,
        userId,
        timestamp: Date.now()
      })
    }
  ]
})
```

---

## Service Discovery

### Con Docker Compose (DNS interno)

```yaml
version: '3.8'

services:
  user-service:
    build: ./user-service
    # Accesible como http://user-service:8000

  order-service:
    build: ./order-service
    # Puede llamar a http://user-service:8000
```

### Con Consul

```yaml
version: '3.8'

services:
  consul:
    image: consul:latest
    ports:
      - "8500:8500"
    command: agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

  user-service:
    build: ./user-service
    environment:
      - CONSUL_HOST=consul:8500
    depends_on:
      - consul
```

**Registrar servicio en Consul:**
```python
import consul

c = consul.Consul(host='consul', port=8500)

c.agent.service.register(
    name='user-service',
    service_id='user-service-1',
    address='user-service',
    port=8000,
    check={
        'http': 'http://user-service:8000/health',
        'interval': '10s'
    }
)
```

---

## API Gateway

### Con Nginx

**nginx.conf:**
```nginx
upstream user_service {
    server user-service:8000;
}

upstream order_service {
    server order-service:3000;
}

upstream product_service {
    server product-service:8080;
}

server {
    listen 80;

    # User Service
    location /api/users {
        proxy_pass http://user_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Order Service
    location /api/orders {
        proxy_pass http://order_service;
    }

    # Product Service
    location /api/products {
        proxy_pass http://product_service;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location /api/ {
        limit_req zone=api burst=20;
    }
}
```

### Con Kong

```yaml
version: '3.8'

services:
  kong-database:
    image: postgres:15
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: kong

  kong-migration:
    image: kong:latest
    command: kong migrations bootstrap
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
    depends_on:
      - kong-database

  kong:
    image: kong:latest
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8000:8000"  # Proxy
      - "8001:8001"  # Admin API
    depends_on:
      - kong-migration
```

---

## Ejemplo Completo: E-Commerce

### Arquitectura

```
                    ┌─────────────┐
                    │ API Gateway │
                    │   (Nginx)   │
                    └──────┬──────┘
                           │
       ┌──────────────┬────┴────┬──────────────┐
       │              │         │              │
┌──────▼──────┐ ┌────▼────┐ ┌──▼──────┐ ┌─────▼─────┐
│   User      │ │ Product │ │  Order  │ │  Payment  │
│   Service   │ │ Service │ │ Service │ │  Service  │
│ (FastAPI)   │ │(Node.js)│ │(Node.js)│ │(FastAPI)  │
└─────┬───────┘ └────┬────┘ └────┬────┘ └─────┬─────┘
      │              │           │            │
┌─────▼───────┐ ┌────▼────┐ ┌───▼─────┐ ┌────▼─────┐
│ PostgreSQL  │ │MongoDB  │ │PostgreSQL│ │PostgreSQL│
└─────────────┘ └─────────┘ └──────────┘ └──────────┘
                           │
                    ┌──────▼──────┐
                    │  RabbitMQ   │
                    │(Event Bus)  │
                    └─────────────┘
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  # API Gateway
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - user-service
      - product-service
      - order-service
      - payment-service

  # User Service
  user-service:
    build: ./services/user
    environment:
      - DATABASE_URL=postgresql://user:pass@user-db:5432/users
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - user-db
      - rabbitmq

  user-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: users
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - user_data:/var/lib/postgresql/data

  # Product Service
  product-service:
    build: ./services/product
    environment:
      - MONGODB_URI=mongodb://product-db:27017/products
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - product-db
      - rabbitmq

  product-db:
    image: mongo:7
    volumes:
      - product_data:/data/db

  # Order Service
  order-service:
    build: ./services/order
    environment:
      - DATABASE_URL=postgresql://user:pass@order-db:5432/orders
      - RABBITMQ_URL=amqp://rabbitmq:5672
      - USER_SERVICE_URL=http://user-service:8000
      - PRODUCT_SERVICE_URL=http://product-service:3000
    depends_on:
      - order-db
      - rabbitmq

  order-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: orders
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - order_data:/var/lib/postgresql/data

  # Payment Service
  payment-service:
    build: ./services/payment
    environment:
      - DATABASE_URL=postgresql://user:pass@payment-db:5432/payments
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - payment-db
      - rabbitmq

  payment-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: payments
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - payment_data:/var/lib/postgresql/data

  # Message Broker
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin

  # Monitoring
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"

volumes:
  user_data:
  product_data:
  order_data:
  payment_data:
```

### Ejemplo de Saga Pattern (Order Flow)

**Order Service:**
```javascript
const express = require('express')
const amqp = require('amqplib')

app.post('/orders', async (req, res) => {
  const { userId, items, total } = req.body

  // 1. Crear order (pending)
  const order = await db.orders.create({
    userId,
    items,
    total,
    status: 'PENDING'
  })

  // 2. Publicar evento
  await publishEvent('order.created', {
    orderId: order.id,
    userId,
    total
  })

  res.json({ orderId: order.id, status: 'PENDING' })
})

// Escuchar eventos
channel.consume('payment.completed', async (msg) => {
  const { orderId, success } = JSON.parse(msg.content)

  if (success) {
    await db.orders.update(orderId, { status: 'PAID' })
    await publishEvent('order.paid', { orderId })
  } else {
    await db.orders.update(orderId, { status: 'PAYMENT_FAILED' })
    // Compensate...
  }
})
```

**Payment Service:**
```javascript
channel.consume('order.created', async (msg) => {
  const { orderId, userId, total } = JSON.parse(msg.content)

  try {
    // Procesar pago
    const payment = await processPayment(userId, total)

    await publishEvent('payment.completed', {
      orderId,
      success: true,
      paymentId: payment.id
    })
  } catch (error) {
    await publishEvent('payment.completed', {
      orderId,
      success: false,
      error: error.message
    })
  }
})
```

---

## Patrones Avanzados

### Circuit Breaker

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
async def call_product_service(product_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://product-service:3000/products/{product_id}")
        return response.json()

# Si falla 5 veces, el circuit se abre por 30 segundos
```

### Retry with Exponential Backoff

```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(5)
)
async def call_external_service():
    # Intenta 5 veces con delays crecientes
    pass
```

### Health Checks

```python
@app.get("/health")
async def health():
    # Check database
    db_healthy = await check_database()

    # Check dependencies
    deps_healthy = await check_dependencies()

    if db_healthy and deps_healthy:
        return {"status": "healthy"}
    else:
        raise HTTPException(status_code=503, detail="unhealthy")
```

---

## Mejores Prácticas

1. **Database per Service** - Nunca compartir BD
2. **API Versioning** - /api/v1/, /api/v2/
3. **Idempotency** - Requests repetidos = mismo resultado
4. **Timeouts** - Siempre configurar timeouts
5. **Retry Logic** - Con exponential backoff
6. **Circuit Breakers** - Prevenir cascading failures
7. **Distributed Tracing** - Jaeger, Zipkin
8. **Centralized Logging** - ELK, Loki
9. **Service Mesh** (avanzado) - Istio, Linkerd
10. **Chaos Engineering** - Testar fallas

---

## Deployment Strategies

### Blue-Green Deployment

```yaml
services:
  app-blue:
    image: myapp:v1
    deploy:
      replicas: 3

  app-green:
    image: myapp:v2
    deploy:
      replicas: 0  # Inicialmente apagado

  nginx:
    # Switch traffic from blue to green
```

### Canary Deployment

```yaml
services:
  app-stable:
    image: myapp:v1
    deploy:
      replicas: 9  # 90% traffic

  app-canary:
    image: myapp:v2
    deploy:
      replicas: 1  # 10% traffic
```

---

## Checklist de Microservicios

- [ ] Servicios bien definidos (bounded contexts)
- [ ] Database per service
- [ ] API Gateway configurado
- [ ] Service discovery implementado
- [ ] Comunicación async para operaciones largas
- [ ] Circuit breakers y retries
- [ ] Health checks en todos los servicios
- [ ] Distributed tracing configurado
- [ ] Logging centralizado
- [ ] Monitoring y alertas
- [ ] CI/CD pipeline
- [ ] Documentation (API docs)

---

¡Los microservicios son poderosos pero complejos - úsalos cuando realmente los necesites!
