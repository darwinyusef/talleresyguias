# Taller: Event-Driven Architecture, Event Sourcing y WebRTC

## Objetivo
Implementar arquitecturas basadas en eventos, event sourcing y comunicación WebRTC en contenedores Docker.

---

## Índice
1. [Event-Driven Architecture (EDA)](#event-driven-architecture)
2. [Pub/Sub Pattern](#pubsub-pattern)
3. [Event Sourcing](#event-sourcing)
4. [CQRS](#cqrs)
5. [WebRTC con Docker](#webrtc)

---

## Event-Driven Architecture

### Arquitectura

```
Producer → Event Bus → Consumer 1
                    → Consumer 2
                    → Consumer 3
```

### Proyecto: Sistema de Pedidos E-Commerce

```
order-system/
├── services/
│   ├── order-service/
│   ├── payment-service/
│   ├── inventory-service/
│   ├── notification-service/
│   └── shipping-service/
├── shared/
│   └── events.py
└── docker-compose.yml
```

### shared/events.py

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any
import json

@dataclass
class Event:
    event_type: str
    aggregate_id: str
    data: Dict[str, Any]
    timestamp: str = None
    version: int = 1

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_json(self):
        return json.dumps({
            'event_type': self.event_type,
            'aggregate_id': self.aggregate_id,
            'data': self.data,
            'timestamp': self.timestamp,
            'version': self.version
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

# Domain Events
class OrderCreated(Event):
    def __init__(self, order_id, user_id, items, total):
        super().__init__(
            event_type='OrderCreated',
            aggregate_id=order_id,
            data={
                'user_id': user_id,
                'items': items,
                'total': total,
                'status': 'pending'
            }
        )

class PaymentProcessed(Event):
    def __init__(self, order_id, payment_id, amount, status):
        super().__init__(
            event_type='PaymentProcessed',
            aggregate_id=order_id,
            data={
                'payment_id': payment_id,
                'amount': amount,
                'status': status
            }
        )

class InventoryReserved(Event):
    def __init__(self, order_id, items):
        super().__init__(
            event_type='InventoryReserved',
            aggregate_id=order_id,
            data={'items': items}
        )

class OrderShipped(Event):
    def __init__(self, order_id, tracking_number):
        super().__init__(
            event_type='OrderShipped',
            aggregate_id=order_id,
            data={'tracking_number': tracking_number}
        )
```

### order-service/app.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import aio_pika
import json
from shared.events import OrderCreated

app = FastAPI()

class CreateOrderRequest(BaseModel):
    user_id: str
    items: list
    total: float

async def publish_event(event):
    """Publish event to RabbitMQ"""
    connection = await aio_pika.connect_robust("amqp://rabbitmq:5672/")
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            'events',
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        message = aio_pika.Message(
            body=event.to_json().encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await exchange.publish(
            message,
            routing_key=f"order.{event.event_type.lower()}"
        )

@app.post("/orders")
async def create_order(request: CreateOrderRequest):
    # Generate order ID
    order_id = f"ORD-{int(time.time())}"

    # Create event
    event = OrderCreated(
        order_id=order_id,
        user_id=request.user_id,
        items=request.items,
        total=request.total
    )

    # Publish event
    await publish_event(event)

    return {
        "order_id": order_id,
        "status": "pending",
        "message": "Order created and being processed"
    }
```

### payment-service/consumer.py

```python
import aio_pika
import asyncio
import json
from shared.events import Event, PaymentProcessed

async def process_payment(order_data):
    """Simulate payment processing"""
    await asyncio.sleep(2)  # Simulate delay
    return {
        'payment_id': f"PAY-{order_data['aggregate_id']}",
        'status': 'success'
    }

async def consume_events():
    connection = await aio_pika.connect_robust("amqp://rabbitmq:5672/")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        exchange = await channel.declare_exchange(
            'events',
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        queue = await channel.declare_queue('payment_service', durable=True)
        await queue.bind(exchange, routing_key='order.ordercreated')

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    event_data = json.loads(message.body.decode())
                    event = Event.from_json(message.body.decode())

                    print(f"Processing payment for order {event.aggregate_id}")

                    # Process payment
                    payment_result = await process_payment(event_data)

                    # Publish PaymentProcessed event
                    payment_event = PaymentProcessed(
                        order_id=event.aggregate_id,
                        payment_id=payment_result['payment_id'],
                        amount=event.data['total'],
                        status=payment_result['status']
                    )

                    # Publish to exchange
                    message = aio_pika.Message(
                        body=payment_event.to_json().encode(),
                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                    )
                    await exchange.publish(
                        message,
                        routing_key='payment.processed'
                    )

if __name__ == '__main__':
    asyncio.run(consume_events())
```

---

## Pub/Sub Pattern con Redis

### publisher.py

```python
import redis
import json
import time

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def publish_event(channel, event):
    r.publish(channel, json.dumps(event))

# Publish events
while True:
    event = {
        'type': 'user_action',
        'user_id': 123,
        'action': 'click',
        'timestamp': time.time()
    }
    publish_event('user_events', event)
    time.sleep(5)
```

### subscriber.py

```python
import redis
import json

r = redis.Redis(host='redis', port=6379, decode_responses=True)
pubsub = r.pubsub()

# Subscribe to channels
pubsub.subscribe('user_events', 'system_events')

print('Listening for messages...')

for message in pubsub.listen():
    if message['type'] == 'message':
        event = json.loads(message['data'])
        print(f"Received event: {event}")

        # Process event
        if event['type'] == 'user_action':
            print(f"User {event['user_id']} performed {event['action']}")
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  publisher:
    build: .
    command: python publisher.py
    depends_on:
      - redis

  subscriber-1:
    build: .
    command: python subscriber.py
    depends_on:
      - redis

  subscriber-2:
    build: .
    command: python subscriber.py
    depends_on:
      - redis
```

---

## Event Sourcing

### Concepto
En lugar de guardar el estado actual, guardar todos los eventos que llevaron a ese estado.

```
Traditional:
users table:
  id | name  | email           | status
  1  | Alice | alice@ex.com    | active

Event Sourcing:
events table:
  id | aggregate_id | event_type     | data                  | timestamp
  1  | user-1       | UserCreated    | {name: "Alice",...}   | 2024-01-01
  2  | user-1       | EmailUpdated   | {email: "new@..."}    | 2024-01-02
  3  | user-1       | UserActivated  | {}                    | 2024-01-03
```

### Implementation

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime
import json

@dataclass
class Event:
    aggregate_id: str
    event_type: str
    data: dict
    timestamp: str
    version: int

class EventStore:
    def __init__(self):
        self.events = []

    def append(self, event: Event):
        """Append event to store"""
        self.events.append(event)

    def get_events(self, aggregate_id: str) -> List[Event]:
        """Get all events for an aggregate"""
        return [e for e in self.events if e.aggregate_id == aggregate_id]

    def get_snapshot(self, aggregate_id: str, version: int = None):
        """Rebuild state from events"""
        events = self.get_events(aggregate_id)
        if version:
            events = [e for e in events if e.version <= version]

        # Rebuild state
        state = {}
        for event in events:
            state = self.apply_event(state, event)

        return state

    def apply_event(self, state: dict, event: Event) -> dict:
        """Apply event to state"""
        handlers = {
            'UserCreated': self._apply_user_created,
            'EmailUpdated': self._apply_email_updated,
            'UserActivated': self._apply_user_activated,
        }

        handler = handlers.get(event.event_type)
        if handler:
            return handler(state, event)
        return state

    def _apply_user_created(self, state, event):
        return {
            'id': event.aggregate_id,
            'name': event.data['name'],
            'email': event.data['email'],
            'status': 'inactive'
        }

    def _apply_email_updated(self, state, event):
        state['email'] = event.data['email']
        return state

    def _apply_user_activated(self, state, event):
        state['status'] = 'active'
        return state

# Usage
store = EventStore()

# Create user
store.append(Event(
    aggregate_id='user-1',
    event_type='UserCreated',
    data={'name': 'Alice', 'email': 'alice@example.com'},
    timestamp=datetime.utcnow().isoformat(),
    version=1
))

# Update email
store.append(Event(
    aggregate_id='user-1',
    event_type='EmailUpdated',
    data={'email': 'newemail@example.com'},
    timestamp=datetime.utcnow().isoformat(),
    version=2
))

# Activate user
store.append(Event(
    aggregate_id='user-1',
    event_type='UserActivated',
    data={},
    timestamp=datetime.utcnow().isoformat(),
    version=3
))

# Rebuild state
current_state = store.get_snapshot('user-1')
print(current_state)
# {'id': 'user-1', 'name': 'Alice', 'email': 'newemail@example.com', 'status': 'active'}

# Get state at version 2
state_v2 = store.get_snapshot('user-1', version=2)
print(state_v2)
# {'id': 'user-1', 'name': 'Alice', 'email': 'newemail@example.com', 'status': 'inactive'}
```

### Event Store con PostgreSQL

```python
import psycopg2
import json
from datetime import datetime

class PostgreSQLEventStore:
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    aggregate_id VARCHAR(255) NOT NULL,
                    event_type VARCHAR(255) NOT NULL,
                    data JSONB NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    version INTEGER NOT NULL,
                    UNIQUE(aggregate_id, version)
                )
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_aggregate_id
                ON events(aggregate_id)
            """)
            self.conn.commit()

    def append(self, aggregate_id, event_type, data):
        with self.conn.cursor() as cur:
            # Get next version
            cur.execute("""
                SELECT COALESCE(MAX(version), 0) + 1
                FROM events
                WHERE aggregate_id = %s
            """, (aggregate_id,))
            version = cur.fetchone()[0]

            # Insert event
            cur.execute("""
                INSERT INTO events (aggregate_id, event_type, data, timestamp, version)
                VALUES (%s, %s, %s, %s, %s)
            """, (aggregate_id, event_type, json.dumps(data), datetime.utcnow(), version))

            self.conn.commit()
            return version

    def get_events(self, aggregate_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT aggregate_id, event_type, data, timestamp, version
                FROM events
                WHERE aggregate_id = %s
                ORDER BY version
            """, (aggregate_id,))

            return [
                {
                    'aggregate_id': row[0],
                    'event_type': row[1],
                    'data': row[2],
                    'timestamp': row[3].isoformat(),
                    'version': row[4]
                }
                for row in cur.fetchall()
            ]
```

---

## CQRS (Command Query Responsibility Segregation)

### Arquitectura

```
Commands → Write Model (Event Store)
              ↓ Events
           Event Bus
              ↓
         Read Model (Projections)
              ↑
          Queries
```

### Implementation

```python
# Command Handler
class CreateUserCommand:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

class CommandHandler:
    def __init__(self, event_store, event_bus):
        self.event_store = event_store
        self.event_bus = event_bus

    def handle_create_user(self, command):
        # Validate
        # ...

        # Create event
        event = {
            'aggregate_id': command.user_id,
            'event_type': 'UserCreated',
            'data': {
                'name': command.name,
                'email': command.email
            }
        }

        # Store event
        self.event_store.append(**event)

        # Publish to event bus
        self.event_bus.publish('UserCreated', event)

# Query Handler (Read Model)
class UserReadModel:
    def __init__(self):
        self.users = {}  # En producción: base de datos read-optimized

    def handle_user_created(self, event):
        """Project event to read model"""
        self.users[event['aggregate_id']] = {
            'id': event['aggregate_id'],
            'name': event['data']['name'],
            'email': event['data']['email'],
            'status': 'inactive'
        }

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_all_users(self):
        return list(self.users.values())

# Event Bus
class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, handler):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def publish(self, event_type, event):
        handlers = self.subscribers.get(event_type, [])
        for handler in handlers:
            handler(event)
```

### docker-compose.yml (CQRS)

```yaml
version: '3.8'

services:
  # Write side (Commands)
  write-api:
    build: ./write-api
    ports:
      - "8000:8000"
    environment:
      - EVENT_STORE_DB=postgresql://user:pass@postgres:5432/eventstore
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - postgres
      - rabbitmq

  # Read side (Queries)
  read-api:
    build: ./read-api
    ports:
      - "8001:8001"
    environment:
      - READ_DB=mongodb://mongo:27017/readmodel
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - mongo
      - rabbitmq

  # Event Store
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: eventstore
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass

  # Read Model
  mongo:
    image: mongo:7
    volumes:
      - mongo_data:/data/db

  # Event Bus
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "15672:15672"

volumes:
  mongo_data:
```

---

## WebRTC con Docker

### Arquitectura

```
Client A ←→ Signaling Server ←→ Client B
    ↓                               ↓
    └──────── P2P Connection ───────┘
              (STUN/TURN)
```

### signaling-server/server.js

```javascript
const express = require('express')
const http = require('http')
const socketIo = require('socket.io')

const app = express()
const server = http.createServer(app)
const io = socketIo(server, {
  cors: { origin: "*" }
})

const rooms = {}

io.on('connection', (socket) => {
  console.log('Client connected:', socket.id)

  socket.on('join_room', (roomId) => {
    socket.join(roomId)

    if (!rooms[roomId]) {
      rooms[roomId] = []
    }
    rooms[roomId].push(socket.id)

    // Notify others in room
    socket.to(roomId).emit('user_joined', socket.id)

    // Send list of users
    socket.emit('room_users', rooms[roomId])
  })

  socket.on('offer', (data) => {
    socket.to(data.target).emit('offer', {
      offer: data.offer,
      sender: socket.id
    })
  })

  socket.on('answer', (data) => {
    socket.to(data.target).emit('answer', {
      answer: data.answer,
      sender: socket.id
    })
  })

  socket.on('ice_candidate', (data) => {
    socket.to(data.target).emit('ice_candidate', {
      candidate: data.candidate,
      sender: socket.id
    })
  })

  socket.on('disconnect', () => {
    // Remove from all rooms
    for (const room in rooms) {
      rooms[room] = rooms[room].filter(id => id !== socket.id)
      socket.to(room).emit('user_left', socket.id)
    }
  })
})

server.listen(3000, () => {
  console.log('Signaling server running on port 3000')
})
```

### client/index.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebRTC Video Call</title>
    <script src="https://cdn.socket.io/4.6.0/socket.io.min.js"></script>
</head>
<body>
    <video id="localVideo" autoplay muted></video>
    <video id="remoteVideo" autoplay></video>
    <button onclick="startCall()">Start Call</button>

    <script>
        const socket = io('http://localhost:3000')
        const roomId = 'room1'

        let localStream
        let peerConnection
        const config = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' }
            ]
        }

        // Get local media
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(stream => {
                localStream = stream
                document.getElementById('localVideo').srcObject = stream
            })

        socket.emit('join_room', roomId)

        socket.on('user_joined', (userId) => {
            console.log('User joined:', userId)
            createPeerConnection(userId)
        })

        socket.on('offer', async (data) => {
            console.log('Received offer from:', data.sender)
            createPeerConnection(data.sender)
            await peerConnection.setRemoteDescription(data.offer)
            const answer = await peerConnection.createAnswer()
            await peerConnection.setLocalDescription(answer)
            socket.emit('answer', {
                target: data.sender,
                answer: answer
            })
        })

        socket.on('answer', async (data) => {
            console.log('Received answer from:', data.sender)
            await peerConnection.setRemoteDescription(data.answer)
        })

        socket.on('ice_candidate', async (data) => {
            if (data.candidate) {
                await peerConnection.addIceCandidate(data.candidate)
            }
        })

        function createPeerConnection(remoteId) {
            peerConnection = new RTCPeerConnection(config)

            // Add local stream
            localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, localStream)
            })

            // Handle remote stream
            peerConnection.ontrack = (event) => {
                document.getElementById('remoteVideo').srcObject = event.streams[0]
            }

            // Handle ICE candidates
            peerConnection.onicecandidate = (event) => {
                if (event.candidate) {
                    socket.emit('ice_candidate', {
                        target: remoteId,
                        candidate: event.candidate
                    })
                }
            }
        }

        async function startCall() {
            const offer = await peerConnection.createOffer()
            await peerConnection.setLocalDescription(offer)

            socket.emit('offer', {
                target: 'targetUserId',  // Get from room_users event
                offer: offer
            })
        }
    </script>
</body>
</html>
```

### docker-compose.yml (WebRTC)

```yaml
version: '3.8'

services:
  signaling-server:
    build: ./signaling-server
    ports:
      - "3000:3000"

  coturn:  # TURN server (for NAT traversal)
    image: coturn/coturn:latest
    network_mode: host
    volumes:
      - ./coturn/turnserver.conf:/etc/coturn/turnserver.conf
    command: -c /etc/coturn/turnserver.conf

  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./client:/usr/share/nginx/html
```

### coturn/turnserver.conf

```
listening-port=3478
fingerprint
lt-cred-mech
user=username:password
realm=example.com
```

---

## Mejores Prácticas

### Event-Driven
1. Idempotent event handlers
2. Event versioning
3. Dead letter queues
4. Retry policies
5. Event schemas

### Event Sourcing
1. Snapshots para performance
2. Soft deletes (nunca borrar events)
3. Encryption para datos sensibles
4. Replay capability
5. Event upcasting (migrations)

### CQRS
1. Eventual consistency aceptada
2. Optimizar read models
3. Multiple read models
4. Cache agresivo en queries

### WebRTC
1. STUN/TURN servers
2. Signaling security
3. Bandwidth adaptation
4. Error handling
5. Reconnection logic

---

¡Estas arquitecturas permiten sistemas altamente escalables y resilientes!
