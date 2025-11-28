# Taller: WebSockets y gRPC en Docker

## Objetivo
Implementar comunicación en tiempo real con WebSockets y gRPC en arquitecturas distribuidas con Docker.

---

## Parte 1: WebSockets en Múltiples Contenedores

### Problema
Cuando tienes múltiples instancias de un servicio WebSocket, los clientes pueden conectarse a diferentes servidores. ¿Cómo sincronizar mensajes entre todos?

### Solución: Redis Pub/Sub + WebSockets

### Arquitectura

```
Cliente 1 →  WS Server 1  ┐
                          ├─→ Redis Pub/Sub ←─┐
Cliente 2 →  WS Server 2  ┘                   ├─→ Todos reciben
                          ┌───────────────────┘
Cliente 3 →  WS Server 3  ┘
```

### Estructura del Proyecto

```
websocket-chat/
├── backend/
│   ├── server.js
│   ├── package.json
│   └── Dockerfile
├── nginx/
│   └── nginx.conf
└── docker-compose.yml
```

### backend/server.js (Node.js + Socket.IO)

```javascript
const express = require('express')
const http = require('http')
const socketIo = require('socket.io')
const redis = require('redis')
const { createAdapter } = require('@socket.io/redis-adapter')

const app = express()
const server = http.createServer(app)
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
})

// Redis clients
const pubClient = redis.createClient({ url: 'redis://redis:6379' })
const subClient = pubClient.duplicate()

Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  // Configure Socket.IO to use Redis adapter
  io.adapter(createAdapter(pubClient, subClient))

  io.on('connection', (socket) => {
    const serverId = process.env.SERVER_ID || 'unknown'
    console.log(`Client connected to server ${serverId}`)

    socket.on('join_room', (room) => {
      socket.join(room)
      console.log(`Client joined room: ${room}`)
    })

    socket.on('message', (data) => {
      console.log(`Message from ${socket.id}:`, data)

      // Broadcast to room (sincroniza vía Redis)
      io.to(data.room).emit('message', {
        user: socket.id,
        message: data.message,
        server: serverId,
        timestamp: new Date().toISOString()
      })
    })

    socket.on('disconnect', () => {
      console.log('Client disconnected')
    })
  })

  server.listen(3000, () => {
    console.log(`WebSocket server ${serverId} running on port 3000`)
  })
})
```

### backend/package.json

```json
{
  "name": "websocket-server",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.2",
    "socket.io": "^4.6.0",
    "@socket.io/redis-adapter": "^8.2.1",
    "redis": "^4.6.5"
  }
}
```

### backend/Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

### nginx/nginx.conf

```nginx
upstream websocket {
    # Sticky sessions basado en IP
    ip_hash;

    server ws-server-1:3000;
    server ws-server-2:3000;
    server ws-server-3:3000;
}

server {
    listen 80;

    location /socket.io/ {
        proxy_pass http://websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # Timeouts
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine
    container_name: redis
    ports:
      - "6379:6379"

  ws-server-1:
    build: ./backend
    environment:
      - SERVER_ID=server-1
    depends_on:
      - redis

  ws-server-2:
    build: ./backend
    environment:
      - SERVER_ID=server-2
    depends_on:
      - redis

  ws-server-3:
    build: ./backend
    environment:
      - SERVER_ID=server-3
    depends_on:
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - ws-server-1
      - ws-server-2
      - ws-server-3
```

### Cliente HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
    <script src="https://cdn.socket.io/4.6.0/socket.io.min.js"></script>
</head>
<body>
    <div id="messages"></div>
    <input id="message-input" placeholder="Type message..." />
    <button onclick="sendMessage()">Send</button>

    <script>
        const socket = io('http://localhost');

        // Join room
        socket.emit('join_room', 'general');

        // Receive messages
        socket.on('message', (data) => {
            const div = document.createElement('div');
            div.textContent = `[${data.server}] ${data.user}: ${data.message}`;
            document.getElementById('messages').appendChild(div);
        });

        function sendMessage() {
            const input = document.getElementById('message-input');
            socket.emit('message', {
                room: 'general',
                message: input.value
            });
            input.value = '';
        }
    </script>
</body>
</html>
```

### Ejecutar

```bash
docker compose up -d --scale ws-server-1=3
```

---

## Parte 2: gRPC con Docker

### ¿Qué es gRPC?

gRPC es un framework RPC de alto rendimiento que usa HTTP/2 y Protocol Buffers.

### Estructura

```
grpc-demo/
├── proto/
│   └── service.proto
├── server/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── client/
│   ├── client.py
│   ├── requirements.txt
│   └── Dockerfile
└── docker-compose.yml
```

### proto/service.proto

```protobuf
syntax = "proto3";

package userservice;

service UserService {
  rpc GetUser (UserRequest) returns (UserResponse);
  rpc ListUsers (Empty) returns (stream UserResponse);
  rpc CreateUser (CreateUserRequest) returns (UserResponse);
  rpc SubscribeToUpdates (Empty) returns (stream UserUpdate);
}

message Empty {}

message UserRequest {
  int32 id = 1;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message UserResponse {
  int32 id = 1;
  string name = 2;
  string email = 3;
  string created_at = 4;
}

message UserUpdate {
  string action = 1;
  UserResponse user = 2;
}
```

### server/server.py

```python
import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc

class UserService(service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {
            1: {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            2: {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        }
        self.next_id = 3

    def GetUser(self, request, context):
        user = self.users.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return service_pb2.UserResponse()

        return service_pb2.UserResponse(
            id=user['id'],
            name=user['name'],
            email=user['email'],
            created_at=time.ctime()
        )

    def ListUsers(self, request, context):
        """Server streaming RPC"""
        for user in self.users.values():
            yield service_pb2.UserResponse(
                id=user['id'],
                name=user['name'],
                email=user['email'],
                created_at=time.ctime()
            )
            time.sleep(0.5)  # Simulate delay

    def CreateUser(self, request, context):
        user = {
            'id': self.next_id,
            'name': request.name,
            'email': request.email
        }
        self.users[self.next_id] = user
        self.next_id += 1

        return service_pb2.UserResponse(
            id=user['id'],
            name=user['name'],
            email=user['email'],
            created_at=time.ctime()
        )

    def SubscribeToUpdates(self, request, context):
        """Bidirectional streaming"""
        while True:
            # Simulate user updates
            time.sleep(2)
            for user in self.users.values():
                yield service_pb2.UserUpdate(
                    action='update',
                    user=service_pb2.UserResponse(
                        id=user['id'],
                        name=user['name'],
                        email=user['email']
                    )
                )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(), server
    )
    server.add_insecure_port('[::]:50051')
    print('gRPC Server running on port 50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

### client/client.py

```python
import grpc
import service_pb2
import service_pb2_grpc

def run():
    channel = grpc.insecure_channel('server:50051')
    stub = service_pb2_grpc.UserServiceStub(channel)

    # Unary RPC
    print("=== Get User ===")
    response = stub.GetUser(service_pb2.UserRequest(id=1))
    print(f"User: {response.name} ({response.email})")

    # Server Streaming
    print("\n=== List Users (Streaming) ===")
    for user in stub.ListUsers(service_pb2.Empty()):
        print(f"- {user.name} ({user.email})")

    # Create User
    print("\n=== Create User ===")
    new_user = stub.CreateUser(
        service_pb2.CreateUserRequest(
            name="Charlie",
            email="charlie@example.com"
        )
    )
    print(f"Created: {new_user.name} with ID {new_user.id}")

    # Subscribe to updates (Streaming)
    print("\n=== Subscribe to Updates ===")
    try:
        for update in stub.SubscribeToUpdates(service_pb2.Empty()):
            print(f"{update.action}: {update.user.name}")
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run()
```

### server/requirements.txt

```
grpcio==1.60.0
grpcio-tools==1.60.0
```

### Generar código Python desde .proto

```bash
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./server \
  --grpc_python_out=./server \
  ./proto/service.proto
```

### server/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto file and generate code
COPY proto/ ./proto/
RUN python -m grpc_tools.protoc \
    -I./proto \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/service.proto

# Copy server code
COPY server.py .

EXPOSE 50051

CMD ["python", "server.py"]
```

### client/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY proto/ ./proto/
RUN python -m grpc_tools.protoc \
    -I./proto \
    --python_out=. \
    --grpc_python_out=. \
    ./proto/service.proto

COPY client.py .

CMD ["python", "client.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  server:
    build:
      context: .
      dockerfile: server/Dockerfile
    ports:
      - "50051:50051"
    container_name: grpc-server

  client:
    build:
      context: .
      dockerfile: client/Dockerfile
    depends_on:
      - server
    container_name: grpc-client
```

---

## gRPC Load Balancing

### Envoy Proxy para Load Balancing

**envoy.yaml:**
```yaml
static_resources:
  listeners:
  - name: listener_0
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 9000
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          codec_type: AUTO
          route_config:
            name: local_route
            virtual_hosts:
            - name: backend
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                  grpc: {}
                route:
                  cluster: grpc_cluster
          http_filters:
          - name: envoy.filters.http.router

  clusters:
  - name: grpc_cluster
    connect_timeout: 0.25s
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    http2_protocol_options: {}
    load_assignment:
      cluster_name: grpc_cluster
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: grpc-server-1
                port_value: 50051
        - endpoint:
            address:
              socket_address:
                address: grpc-server-2
                port_value: 50051
```

**docker-compose con Envoy:**
```yaml
version: '3.8'

services:
  envoy:
    image: envoyproxy/envoy:v1.28-latest
    ports:
      - "9000:9000"
      - "9901:9901"
    volumes:
      - ./envoy.yaml:/etc/envoy/envoy.yaml
    command: /usr/local/bin/envoy -c /etc/envoy/envoy.yaml

  grpc-server-1:
    build: ./server
    container_name: grpc-server-1

  grpc-server-2:
    build: ./server
    container_name: grpc-server-2
```

---

## gRPC con Node.js

### server.js

```javascript
const grpc = require('@grpc/grpc-js')
const protoLoader = require('@grpc/proto-loader')

const PROTO_PATH = './proto/service.proto'

const packageDefinition = protoLoader.loadSync(PROTO_PATH)
const proto = grpc.loadPackageDefinition(packageDefinition).userservice

const users = {
  1: { id: 1, name: 'Alice', email: 'alice@example.com' },
  2: { id: 2, name: 'Bob', email: 'bob@example.com' }
}

function getUser(call, callback) {
  const user = users[call.request.id]
  if (user) {
    callback(null, user)
  } else {
    callback({
      code: grpc.status.NOT_FOUND,
      details: 'User not found'
    })
  }
}

function listUsers(call) {
  Object.values(users).forEach(user => {
    call.write(user)
  })
  call.end()
}

function main() {
  const server = new grpc.Server()

  server.addService(proto.UserService.service, {
    getUser: getUser,
    listUsers: listUsers
  })

  server.bindAsync(
    '0.0.0.0:50051',
    grpc.ServerCredentials.createInsecure(),
    () => {
      console.log('gRPC Server running on port 50051')
      server.start()
    }
  )
}

main()
```

---

## Comparación: REST vs gRPC vs WebSockets

| Feature | REST | gRPC | WebSockets |
|---------|------|------|------------|
| Protocol | HTTP/1.1 | HTTP/2 | TCP |
| Data Format | JSON/XML | Protobuf | Any |
| Streaming | No | Yes | Yes |
| Bidirectional | No | Yes | Yes |
| Browser Support | ✅ | ❌ (via proxy) | ✅ |
| Performance | Medium | High | High |
| Use Case | CRUD APIs | Microservices | Real-time |

---

## Mejores Prácticas

### WebSockets
1. Usar adaptadores (Redis) para múltiples servidores
2. Implementar heartbeat/ping-pong
3. Reconexión automática en cliente
4. Rate limiting
5. Autenticación robusta

### gRPC
1. Definir .proto versionados
2. Usar interceptors para logging/auth
3. Implementar health checks
4. Manejar errores apropiadamente
5. Usar load balancing

---

¡WebSockets y gRPC son esenciales para comunicación moderna en microservicios!
