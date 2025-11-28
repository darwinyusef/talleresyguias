# Módulo 8: Message Brokers con Docker

## Objetivo
Aprender a desplegar y usar sistemas de mensajería (Kafka, RabbitMQ) y cache (Redis) con Docker.

---

## Índice

1. [Redis - Cache y Message Broker](#redis)
2. [RabbitMQ - Message Queue](#rabbitmq)
3. [Apache Kafka - Event Streaming](#apache-kafka)
4. [Comparación de Tecnologías](#comparación)
5. [Patrones de Uso](#patrones-de-uso)

---

## Redis

### ¿Qué es Redis?

Redis es un almacén de datos en memoria key-value extremadamente rápido.

**Casos de uso:**
- Cache de aplicaciones
- Session storage
- Real-time analytics
- Message broker (Pub/Sub)
- Rate limiting
- Leaderboards

### Redis con Docker

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass mi_password
    restart: unless-stopped

  # Redis Commander (GUI)
  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: redis-commander
    environment:
      - REDIS_HOSTS=local:redis:6379:0:mi_password
    ports:
      - "8081:8081"
    depends_on:
      - redis

volumes:
  redis_data:
```

**Comandos:**
```bash
# Iniciar
docker compose up -d

# Acceder a Redis CLI
docker exec -it redis redis-cli -a mi_password

# Comandos básicos de Redis
> SET nombre "Juan"
> GET nombre
> KEYS *
> DEL nombre
> EXPIRE key 60
> TTL key
```

### Uso en Node.js

**Instalar cliente:**
```bash
npm install redis
```

**Código:**
```javascript
import { createClient } from 'redis'

const client = createClient({
  url: 'redis://localhost:6379',
  password: 'mi_password'
})

client.on('error', (err) => console.error('Redis error:', err))

await client.connect()

// Set/Get
await client.set('key', 'value')
const value = await client.get('key')

// Con expiración
await client.setEx('session:123', 3600, 'user_data')

// Hash
await client.hSet('user:1', { name: 'Juan', email: 'juan@example.com' })
await client.hGetAll('user:1')

// Lists
await client.lPush('queue', 'task1')
await client.lPush('queue', 'task2')
await client.rPop('queue')

// Pub/Sub
const subscriber = client.duplicate()
await subscriber.connect()

await subscriber.subscribe('channel', (message) => {
  console.log('Received:', message)
})

await client.publish('channel', 'Hello World!')
```

### Cache Pattern

```javascript
// Cache-aside pattern
async function getUser(id) {
  // 1. Intentar obtener del cache
  const cached = await redis.get(`user:${id}`)
  if (cached) {
    return JSON.parse(cached)
  }

  // 2. Si no está, obtener de DB
  const user = await db.query('SELECT * FROM users WHERE id = $1', [id])

  // 3. Guardar en cache
  await redis.setEx(`user:${id}`, 3600, JSON.stringify(user))

  return user
}
```

### Redis Pub/Sub

```javascript
// Publisher
await redis.publish('notifications', JSON.stringify({
  type: 'new_message',
  userId: 123,
  message: 'Hola!'
}))

// Subscriber
await redis.subscribe('notifications', (message) => {
  const data = JSON.parse(message)
  console.log('Notification:', data)
})
```

---

## RabbitMQ

### ¿Qué es RabbitMQ?

RabbitMQ es un message broker que implementa AMQP (Advanced Message Queuing Protocol).

**Casos de uso:**
- Task queues (procesamiento asíncrono)
- Event-driven architecture
- Microservices communication
- Load balancing
- Reliable message delivery

### Conceptos Clave

- **Producer** - Envía mensajes
- **Consumer** - Recibe mensajes
- **Queue** - Buffer que almacena mensajes
- **Exchange** - Rutea mensajes a queues
- **Binding** - Regla de ruteo

### RabbitMQ con Docker

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq
    ports:
      - "5672:5672"    # AMQP
      - "15672:15672"  # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    restart: unless-stopped

volumes:
  rabbitmq_data:
```

**Acceder a Management UI:**
```
http://localhost:15672
User: admin
Pass: admin123
```

### Uso en Node.js

**Instalar cliente:**
```bash
npm install amqplib
```

**Producer (enviar mensajes):**
```javascript
import amqp from 'amqplib'

async function sendMessage() {
  const connection = await amqp.connect('amqp://admin:admin123@localhost:5672')
  const channel = await connection.createChannel()

  const queue = 'tasks'

  await channel.assertQueue(queue, { durable: true })

  const message = JSON.stringify({
    task: 'send_email',
    to: 'user@example.com',
    subject: 'Hello'
  })

  channel.sendToQueue(queue, Buffer.from(message), {
    persistent: true
  })

  console.log('Sent:', message)

  setTimeout(() => {
    connection.close()
  }, 500)
}

sendMessage()
```

**Consumer (procesar mensajes):**
```javascript
import amqp from 'amqplib'

async function consumeMessages() {
  const connection = await amqp.connect('amqp://admin:admin123@localhost:5672')
  const channel = await connection.createChannel()

  const queue = 'tasks'

  await channel.assertQueue(queue, { durable: true })
  channel.prefetch(1) // Procesar 1 mensaje a la vez

  console.log('Waiting for messages...')

  channel.consume(queue, async (msg) => {
    const content = JSON.parse(msg.content.toString())
    console.log('Processing:', content)

    // Simular procesamiento
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Acknowledge (confirmar procesamiento)
    channel.ack(msg)
  })
}

consumeMessages()
```

### Patrones de Exchange

**1. Direct Exchange (por routing key):**
```javascript
const exchange = 'logs_direct'
const routingKey = 'error'

await channel.assertExchange(exchange, 'direct', { durable: false })

channel.publish(exchange, routingKey, Buffer.from('Error message'))
```

**2. Fanout Exchange (broadcast):**
```javascript
const exchange = 'logs_fanout'

await channel.assertExchange(exchange, 'fanout', { durable: false })

// Todos los consumers conectados recibirán el mensaje
channel.publish(exchange, '', Buffer.from('Broadcast message'))
```

**3. Topic Exchange (pattern matching):**
```javascript
const exchange = 'logs_topic'
const routingKey = 'app.error.database'

await channel.assertExchange(exchange, 'topic', { durable: false })

channel.publish(exchange, routingKey, Buffer.from('DB error'))

// Consumers pueden suscribirse con patterns:
// 'app.*' - todos los logs de app
// '*.error.*' - todos los errores
// 'app.error.#' - errores de app
```

### Task Queue con Workers

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"

  worker:
    build: ./worker
    depends_on:
      - rabbitmq
    deploy:
      replicas: 3  # 3 workers paralelos
    environment:
      - RABBITMQ_URL=amqp://admin:admin123@rabbitmq:5672
```

---

## Apache Kafka

### ¿Qué es Kafka?

Kafka es una plataforma de streaming de eventos distribuida.

**Casos de uso:**
- Event streaming
- Log aggregation
- Real-time analytics
- Event sourcing
- CDC (Change Data Capture)

### Conceptos Clave

- **Producer** - Publica eventos
- **Consumer** - Lee eventos
- **Topic** - Categoría de eventos
- **Partition** - División de un topic
- **Broker** - Servidor Kafka
- **Consumer Group** - Grupo de consumers

### Kafka con Docker

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
```

**Acceder a Kafka UI:**
```
http://localhost:8080
```

### Uso en Node.js

**Instalar cliente:**
```bash
npm install kafkajs
```

**Producer:**
```javascript
import { Kafka } from 'kafkajs'

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
})

const producer = kafka.producer()

await producer.connect()

// Enviar mensaje
await producer.send({
  topic: 'user-events',
  messages: [
    {
      key: 'user-123',
      value: JSON.stringify({
        type: 'user_created',
        userId: 123,
        name: 'Juan',
        timestamp: Date.now()
      })
    }
  ]
})

await producer.disconnect()
```

**Consumer:**
```javascript
import { Kafka } from 'kafkajs'

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
})

const consumer = kafka.consumer({ groupId: 'user-service' })

await consumer.connect()
await consumer.subscribe({ topic: 'user-events', fromBeginning: true })

await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    const event = JSON.parse(message.value.toString())
    console.log('Received event:', event)

    // Procesar evento
    if (event.type === 'user_created') {
      // Hacer algo...
    }
  }
})
```

### Ejemplo Full Stack con Kafka

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - kafka

  event-processor:
    build: ./event-processor
    environment:
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - kafka
    deploy:
      replicas: 3

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: events
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

---

## Comparación

| Característica | Redis | RabbitMQ | Kafka |
|---------------|-------|----------|-------|
| **Tipo** | In-memory DB/Cache | Message Broker | Event Streaming |
| **Velocidad** | Muy rápida | Rápida | Rápida |
| **Persistencia** | Opcional | Sí | Sí |
| **Orden** | No garantizado | Garantizado | Garantizado (por partition) |
| **Retención** | TTL | Hasta consumir | Configurable |
| **Escalabilidad** | Horizontal | Vertical | Horizontal |
| **Complejidad** | Baja | Media | Alta |
| **Ideal para** | Cache, Pub/Sub simple | Task queues | Event streaming, logs |

---

## Patrones de Uso

### 1. Cache (Redis)
```javascript
// API con cache
app.get('/api/users/:id', async (req, res) => {
  const cached = await redis.get(`user:${req.params.id}`)
  if (cached) return res.json(JSON.parse(cached))

  const user = await db.getUser(req.params.id)
  await redis.setEx(`user:${req.params.id}`, 300, JSON.stringify(user))
  res.json(user)
})
```

### 2. Task Queue (RabbitMQ)
```javascript
// API envía tarea
app.post('/api/send-email', async (req, res) => {
  await rabbitmq.sendToQueue('emails', {
    to: req.body.email,
    subject: 'Welcome',
    body: 'Hello!'
  })
  res.json({ status: 'queued' })
})

// Worker procesa
consumer.consume('emails', async (task) => {
  await sendEmail(task)
})
```

### 3. Event Streaming (Kafka)
```javascript
// API publica evento
app.post('/api/orders', async (req, res) => {
  const order = await db.createOrder(req.body)

  await kafka.send({
    topic: 'orders',
    messages: [{
      value: JSON.stringify({
        type: 'order_created',
        order
      })
    }]
  })

  res.json(order)
})

// Múltiples servicios consumen
// - Servicio de inventario
// - Servicio de notificaciones
// - Servicio de analytics
```

---

## Ejercicios Prácticos

### Ejercicio 1: Sistema de Notificaciones
- API publica notificaciones en Redis Pub/Sub
- Frontend escucha en tiempo real (WebSockets)
- Almacenar en PostgreSQL

### Ejercicio 2: Procesamiento de Imágenes
- API recibe uploads
- Publica en RabbitMQ
- Workers procesan (resize, thumbnail)
- Notifica cuando termina

### Ejercicio 3: Analytics en Tiempo Real
- Eventos de usuario a Kafka
- Consumer procesa y agrega
- Dashboard muestra métricas

---

## Troubleshooting

**Redis no conecta:**
```bash
docker logs redis
docker exec -it redis redis-cli ping
```

**RabbitMQ queue llena:**
```bash
# Ver estado de queues en UI
# O via CLI:
docker exec rabbitmq rabbitmqctl list_queues
```

**Kafka consumer lag:**
```bash
# Ver en Kafka UI o:
docker exec kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --describe --group mi-grupo
```

---

Este módulo te ha enseñado a usar sistemas de mensajería para construir aplicaciones escalables y desacopladas.
