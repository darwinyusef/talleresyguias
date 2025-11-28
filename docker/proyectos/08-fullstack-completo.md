# Proyecto 8: Full Stack Completo

## Objetivo
Crear y desplegar una aplicación completa con React (Frontend), Node.js/FastAPI (Backend), PostgreSQL (Database), Redis (Cache) y Nginx (Reverse Proxy).

## Arquitectura

```
Cliente (Navegador)
      ↓
   Nginx (Puerto 80)
      ↓
   ┌─────────────┬──────────────┐
   ↓             ↓              ↓
Frontend      Backend        Backend
(React)    (Node/FastAPI)   API Alt
   ↓             ↓
   └─────────────┴──────────────┐
                                ↓
                          PostgreSQL
                                ↓
                             Redis
```

---

## Paso 1: Estructura del Proyecto

```bash
mkdir -p ~/curso-docker/proyectos/08-fullstack-completo
cd ~/curso-docker/proyectos/08-fullstack-completo
```

**Estructura:**
```
08-fullstack-completo/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── backend/
│   ├── src/
│   ├── package.json
│   ├── tsconfig.json
│   └── Dockerfile
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

---

## Paso 2: Frontend (React + Vite)

```bash
cd frontend
npm create vite@latest . -- --template react
npm install axios react-router-dom
```

**frontend/src/config.js:**
```javascript
export const API_URL = import.meta.env.VITE_API_URL || '/api'
```

**frontend/src/services/api.js:**
```javascript
import axios from 'axios'
import { API_URL } from '../config'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getUsers = () => api.get('/users')
export const getUser = (id) => api.get(`/users/${id}`)
export const createUser = (data) => api.post('/users', data)
export const updateUser = (id, data) => api.put(`/users/${id}`, data)
export const deleteUser = (id) => api.delete(`/users/${id}`)

export default api
```

**frontend/src/App.jsx:**
```javascript
import { useState, useEffect } from 'react'
import { getUsers, createUser, deleteUser } from './services/api'
import './App.css'

function App() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [formData, setFormData] = useState({ name: '', email: '' })

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await getUsers()
      setUsers(response.data.users || response.data)
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await createUser(formData)
      setFormData({ name: '', email: '' })
      fetchUsers()
    } catch (error) {
      console.error('Error creating user:', error)
    }
  }

  const handleDelete = async (id) => {
    try {
      await deleteUser(id)
      fetchUsers()
    } catch (error) {
      console.error('Error deleting user:', error)
    }
  }

  return (
    <div className="App">
      <h1>Full Stack App</h1>

      <div className="container">
        <div className="form-section">
          <h2>Add User</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
            <button type="submit">Add User</button>
          </form>
        </div>

        <div className="users-section">
          <h2>Users List</h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <ul>
              {users.map((user) => (
                <li key={user.id}>
                  <span>{user.name} - {user.email}</span>
                  <button onClick={() => handleDelete(user.id)}>Delete</button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
```

**frontend/Dockerfile:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## Paso 3: Backend (Node.js + TypeScript + Express)

```bash
cd ../backend
npm init -y
npm install express cors dotenv pg
npm install -D typescript @types/node @types/express @types/cors ts-node nodemon
```

**backend/package.json scripts:**
```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "nodemon --exec ts-node src/index.ts"
  }
}
```

**backend/tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
```

**backend/src/index.ts:**
```typescript
import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import { Pool } from 'pg'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 3000

// Database connection
const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  user: process.env.DB_USER || 'usuario',
  password: process.env.DB_PASSWORD || 'password',
  database: process.env.DB_NAME || 'appdb',
})

// Middleware
app.use(cors())
app.use(express.json())

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' })
})

// Get all users
app.get('/api/users', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM users ORDER BY id')
    res.json({ users: result.rows })
  } catch (error) {
    console.error('Error getting users:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
})

// Get user by ID
app.get('/api/users/:id', async (req, res) => {
  try {
    const { id } = req.params
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id])

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' })
    }

    res.json(result.rows[0])
  } catch (error) {
    console.error('Error getting user:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
})

// Create user
app.post('/api/users', async (req, res) => {
  try {
    const { name, email } = req.body

    if (!name || !email) {
      return res.status(400).json({ error: 'Name and email are required' })
    }

    const result = await pool.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
      [name, email]
    )

    res.status(201).json(result.rows[0])
  } catch (error) {
    console.error('Error creating user:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
})

// Update user
app.put('/api/users/:id', async (req, res) => {
  try {
    const { id } = req.params
    const { name, email } = req.body

    const result = await pool.query(
      'UPDATE users SET name = $1, email = $2 WHERE id = $3 RETURNING *',
      [name, email, id]
    )

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' })
    }

    res.json(result.rows[0])
  } catch (error) {
    console.error('Error updating user:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
})

// Delete user
app.delete('/api/users/:id', async (req, res) => {
  try {
    const { id } = req.params

    const result = await pool.query('DELETE FROM users WHERE id = $1 RETURNING *', [id])

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' })
    }

    res.json({ message: 'User deleted successfully' })
  } catch (error) {
    console.error('Error deleting user:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
})

app.listen(PORT, () => {
  console.log(`🚀 Backend running on port ${PORT}`)
})
```

**backend/Dockerfile:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY --from=builder /app/dist ./dist

EXPOSE 3000

USER node

CMD ["node", "dist/index.js"]
```

---

## Paso 4: Nginx (Reverse Proxy)

**nginx/nginx.conf:**
```nginx
upstream backend {
    server backend:3000;
}

server {
    listen 80;
    server_name localhost;

    # Frontend
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API Backend
    location /api/ {
        proxy_pass http://backend/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check
    location /health {
        proxy_pass http://backend/health;
    }

    # Caché para assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Compresión
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

---

## Paso 5: Docker Compose Completo

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U usuario"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: backend-api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=usuario
      - DB_PASSWORD=password
      - DB_NAME=appdb
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network
    restart: unless-stopped

  # Frontend React
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: frontend-app
    depends_on:
      - backend
    networks:
      - app-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - frontend_build:/usr/share/nginx/html
    depends_on:
      - frontend
      - backend
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  frontend_build:

networks:
  app-network:
    driver: bridge
```

---

## Paso 6: Script de Inicialización de Base de Datos

**init.sql:**
```sql
-- Crear tabla users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo
INSERT INTO users (name, email) VALUES
    ('Juan Pérez', 'juan@example.com'),
    ('María García', 'maria@example.com'),
    ('Carlos López', 'carlos@example.com')
ON CONFLICT (email) DO NOTHING;

-- Índices
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

---

## Paso 7: Desarrollo con Docker Compose

**docker-compose.dev.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - app-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./backend/src:/app/src
      - ./backend/tsconfig.json:/app/tsconfig.json
    environment:
      - NODE_ENV=development
      - DB_HOST=db
      - DB_USER=usuario
      - DB_PASSWORD=password
      - DB_NAME=appdb
    depends_on:
      - db
      - redis
    networks:
      - app-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
    environment:
      - VITE_API_URL=http://localhost:3000
    depends_on:
      - backend
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

**backend/Dockerfile.dev:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

**frontend/Dockerfile.dev:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

---

## Paso 8: Scripts de Gestión

**Makefile:**
```makefile
.PHONY: help dev prod stop clean logs

help:
	@echo "Comandos disponibles:"
	@echo "  make dev     - Iniciar en modo desarrollo"
	@echo "  make prod    - Iniciar en modo producción"
	@echo "  make stop    - Detener todos los servicios"
	@echo "  make clean   - Limpiar todos los contenedores y volúmenes"
	@echo "  make logs    - Ver logs de todos los servicios"
	@echo "  make build   - Construir todas las imágenes"

dev:
	docker compose -f docker-compose.dev.yml up -d

prod:
	docker compose up -d --build

stop:
	docker compose down
	docker compose -f docker-compose.dev.yml down

clean:
	docker compose down -v
	docker compose -f docker-compose.dev.yml down -v

logs:
	docker compose logs -f

build:
	docker compose build
```

---

## Paso 9: Ejecutar la Aplicación

**Modo Producción:**
```bash
# Build y start
docker compose up -d --build

# Ver logs
docker compose logs -f

# Verificar servicios
docker compose ps

# Acceder a la app
open http://localhost
```

**Modo Desarrollo:**
```bash
# Start
docker compose -f docker-compose.dev.yml up -d

# Logs
docker compose -f docker-compose.dev.yml logs -f

# Frontend: http://localhost:5173
# Backend: http://localhost:3000
```

**Acceder a servicios:**
```bash
# PostgreSQL
docker compose exec db psql -U usuario -d appdb

# Redis
docker compose exec redis redis-cli

# Backend
docker compose exec backend sh

# Ver logs
docker compose logs backend
docker compose logs frontend
docker compose logs nginx
```

---

## Paso 10: Agregar Redis Cache

**backend/src/index.ts (con Redis):**
```typescript
import { createClient } from 'redis'

// Redis client
const redisClient = createClient({
  url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`
})

redisClient.on('error', (err) => console.error('Redis error:', err))

await redisClient.connect()

// Get users con caché
app.get('/api/users', async (req, res) => {
  try {
    // Intentar obtener del caché
    const cached = await redisClient.get('users')
    if (cached) {
      console.log('Cache hit')
      return res.json(JSON.parse(cached))
    }

    // Si no está en caché, obtener de DB
    const result = await pool.query('SELECT * FROM users ORDER BY id')
    const users = { users: result.rows }

    // Guardar en caché (expira en 60 segundos)
    await redisClient.setEx('users', 60, JSON.stringify(users))

    res.json(users)
  } catch (error) {
    console.error('Error:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
})

// Invalidar caché al crear/actualizar/eliminar
app.post('/api/users', async (req, res) => {
  // ... crear usuario ...
  await redisClient.del('users')  // Invalidar caché
  // ...
})
```

**Instalar Redis en backend:**
```bash
cd backend
npm install redis
```

---

## Ejercicios Avanzados

### Ejercicio 1: Agregar Autenticación
- JWT tokens
- Login/Register
- Middleware de autenticación
- Rutas protegidas

### Ejercicio 2: Agregar Monitoreo
```yaml
# docker-compose.yml
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
```

### Ejercicio 3: Agregar Testing
- Tests unitarios (Jest)
- Tests de integración
- Tests E2E (Playwright)

### Ejercicio 4: CI/CD Pipeline
- GitHub Actions
- Builds automáticos
- Deploy a producción

---

## Optimización y Seguridad

### 1. Variables de Entorno
```bash
# .env
DB_USER=usuario
DB_PASSWORD=password_seguro
JWT_SECRET=tu_secret_key
```

### 2. Docker Secrets
```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  backend:
    secrets:
      - db_password
```

### 3. Health Checks
```yaml
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 4. Limitaciones de Recursos
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M
```

---

## Troubleshooting

### Servicios no se conectan
```bash
# Verificar red
docker network inspect 08-fullstack-completo_app-network

# Verificar DNS
docker compose exec backend ping db
```

### Base de datos no inicializa
```bash
# Ver logs
docker compose logs db

# Reiniciar con volúmenes limpios
docker compose down -v
docker compose up -d
```

### Frontend no encuentra API
```bash
# Verificar configuración de Nginx
docker compose exec nginx cat /etc/nginx/conf.d/default.conf

# Ver logs de Nginx
docker compose logs nginx
```

---

## Resumen de Comandos

```bash
# Producción
docker compose up -d --build
docker compose ps
docker compose logs -f
docker compose down

# Desarrollo
docker compose -f docker-compose.dev.yml up -d

# Acceder a servicios
docker compose exec db psql -U usuario -d appdb
docker compose exec redis redis-cli
docker compose exec backend sh

# Limpiar todo
docker compose down -v
docker system prune -a
```

---

## Checklist del Proyecto

- [ ] Crear estructura de directorios
- [ ] Desarrollar frontend React
- [ ] Desarrollar backend Node/Express
- [ ] Configurar PostgreSQL
- [ ] Configurar Redis
- [ ] Configurar Nginx
- [ ] Crear Dockerfiles para cada servicio
- [ ] Crear docker-compose.yml
- [ ] Crear script de inicialización de DB
- [ ] Probar en modo desarrollo
- [ ] Probar en modo producción
- [ ] Implementar caché con Redis
- [ ] Agregar health checks
- [ ] Documentar API
- [ ] Escribir tests

---

¡Felicidades! Has completado el proyecto Full Stack completo con Docker.

**Siguiente paso:** [Módulo 6: CI/CD con GitHub Actions](../MODULO_CI_CD.md)
