# Proyecto 5: Backend con Node.js + TypeScript

## Objetivo
Crear una API REST con Node.js, Express y TypeScript usando Docker.

## Prerrequisitos
- Proyectos anteriores completados
- Conocimientos de Node.js y Express
- Conocimientos básicos de TypeScript

---

## Paso 1: Estructura del Proyecto

```bash
mkdir -p ~/curso-docker/proyectos/05-node-typescript
cd ~/curso-docker/proyectos/05-node-typescript
```

**Inicializar proyecto:**
```bash
npm init -y
```

**Estructura esperada:**
```
05-node-typescript/
├── src/
│   ├── index.ts
│   ├── routes/
│   │   └── index.ts
│   ├── controllers/
│   │   └── userController.ts
│   ├── models/
│   │   └── User.ts
│   ├── middleware/
│   │   └── errorHandler.ts
│   └── config/
│       └── database.ts
├── dist/              (generado después del build)
├── package.json
├── tsconfig.json
├── .env
├── .dockerignore
├── Dockerfile
├── Dockerfile.dev
└── docker-compose.yml
```

## Paso 2: Instalar Dependencias

```bash
# Dependencias de producción
npm install express cors dotenv

# Dependencias de desarrollo
npm install -D typescript @types/node @types/express @types/cors ts-node nodemon
```

**package.json scripts:**
```json
{
  "name": "node-typescript-api",
  "version": "1.0.0",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "nodemon --exec ts-node src/index.ts",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/node": "^20.10.5",
    "@types/express": "^4.17.21",
    "@types/cors": "^2.8.17",
    "ts-node": "^10.9.2",
    "nodemon": "^3.0.2"
  }
}
```

## Paso 3: Configurar TypeScript

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "sourceMap": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Paso 4: Crear Aplicación Express

**src/index.ts:**
```typescript
import express, { Application, Request, Response } from 'express'
import cors from 'cors'
import dotenv from 'dotenv'

// Cargar variables de entorno
dotenv.config()

const app: Application = express()
const PORT = process.env.PORT || 3000

// Middleware
app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Rutas
app.get('/', (req: Request, res: Response) => {
  res.json({
    message: 'API con Node.js + TypeScript',
    status: 'running',
    version: '1.0.0'
  })
})

app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'healthy' })
})

// Importar rutas adicionales
// import routes from './routes'
// app.use('/api', routes)

// Manejo de errores
app.use((err: Error, req: Request, res: Response, next: any) => {
  console.error(err.stack)
  res.status(500).json({ error: 'Something went wrong!' })
})

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`)
})
```

**src/routes/index.ts (ejemplo):**
```typescript
import { Router } from 'express'

const router = Router()

router.get('/users', (req, res) => {
  res.json({ users: [] })
})

router.post('/users', (req, res) => {
  const { name, email } = req.body
  res.status(201).json({ id: 1, name, email })
})

export default router
```

## Paso 5: Crear .env

```env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
JWT_SECRET=your-secret-key
```

## Paso 6: Dockerfile Multi-Stage (Producción)

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente
COPY . .

# Compilar TypeScript
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar solo dependencias de producción
RUN npm ci --only=production && npm cache clean --force

# Copiar código compilado
COPY --from=builder /app/dist ./dist

# Exponer puerto
EXPOSE 3000

# Usuario no-root
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {r.statusCode === 200 ? process.exit(0) : process.exit(1)})"

# Comando de inicio
CMD ["node", "dist/index.js"]
```

## Paso 7: Dockerfile.dev (Desarrollo)

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Instalar dependencias
COPY package*.json ./
RUN npm install

# El código se monta como volumen

EXPOSE 3000

# Modo desarrollo con nodemon
CMD ["npm", "run", "dev"]
```

## Paso 8: Crear .dockerignore

```
node_modules
npm-debug.log
dist
.git
.gitignore
README.md
.env
.env.local
.env.development
.env.production
.DS_Store
coverage
.vscode
.idea
*.log
```

## Paso 9: Docker Compose

```yaml
version: '3.8'

services:
  # Producción
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    container_name: node-api-prod
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - PORT=3000
    env_file:
      - .env
    profiles:
      - production

  # Desarrollo con hot reload
  api-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - ./tsconfig.json:/app/tsconfig.json
    container_name: node-api-dev
    environment:
      - NODE_ENV=development
      - PORT=3000
    env_file:
      - .env
    profiles:
      - development
```

## Paso 10: Construir y Ejecutar

**Desarrollo local (sin Docker):**
```bash
npm run dev
```

**Producción con Docker:**
```bash
# Build
docker build -t node-api:v1 .

# Run
docker run -d \
  --name node-api \
  -p 3000:3000 \
  -e NODE_ENV=production \
  node-api:v1

# Verificar
curl http://localhost:3000
docker logs node-api
```

**Desarrollo con Docker:**
```bash
docker compose --profile development up -d
docker compose logs -f api-dev
```

---

## Integración con Base de Datos PostgreSQL

**Instalar dependencias:**
```bash
npm install pg
npm install -D @types/pg
```

**src/config/database.ts:**
```typescript
import { Pool } from 'pg'

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

export default pool
```

**docker-compose.yml con PostgreSQL:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U usuario"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  api:
    build: .
    container_name: node-api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://usuario:password@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

**Uso en código:**
```typescript
import pool from './config/database'

// Consulta simple
async function getUsers() {
  const result = await pool.query('SELECT * FROM users')
  return result.rows
}

// Con parámetros
async function getUserById(id: number) {
  const result = await pool.query(
    'SELECT * FROM users WHERE id = $1',
    [id]
  )
  return result.rows[0]
}
```

---

## CRUD Completo

**src/controllers/userController.ts:**
```typescript
import { Request, Response } from 'express'
import pool from '../config/database'

export const getUsers = async (req: Request, res: Response) => {
  try {
    const result = await pool.query('SELECT * FROM users ORDER BY id')
    res.json({ users: result.rows })
  } catch (error) {
    console.error('Error getting users:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
}

export const getUserById = async (req: Request, res: Response) => {
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
}

export const createUser = async (req: Request, res: Response) => {
  try {
    const { name, email } = req.body

    const result = await pool.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
      [name, email]
    )

    res.status(201).json(result.rows[0])
  } catch (error) {
    console.error('Error creating user:', error)
    res.status(500).json({ error: 'Internal server error' })
  }
}

export const updateUser = async (req: Request, res: Response) => {
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
}

export const deleteUser = async (req: Request, res: Response) => {
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
}
```

**src/routes/userRoutes.ts:**
```typescript
import { Router } from 'express'
import * as userController from '../controllers/userController'

const router = Router()

router.get('/users', userController.getUsers)
router.get('/users/:id', userController.getUserById)
router.post('/users', userController.createUser)
router.put('/users/:id', userController.updateUser)
router.delete('/users/:id', userController.deleteUser)

export default router
```

**Registrar en src/index.ts:**
```typescript
import userRoutes from './routes/userRoutes'

app.use('/api', userRoutes)
```

---

## Middleware de Validación

**Instalar:**
```bash
npm install express-validator
npm install -D @types/express-validator
```

**src/middleware/validation.ts:**
```typescript
import { body, validationResult } from 'express-validator'
import { Request, Response, NextFunction } from 'express'

export const validateUser = [
  body('name')
    .trim()
    .isLength({ min: 2, max: 100 })
    .withMessage('Name must be between 2 and 100 characters'),
  body('email')
    .trim()
    .isEmail()
    .withMessage('Must be a valid email')
    .normalizeEmail(),
]

export const handleValidationErrors = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() })
  }
  next()
}
```

**Uso:**
```typescript
import { validateUser, handleValidationErrors } from '../middleware/validation'

router.post(
  '/users',
  validateUser,
  handleValidationErrors,
  userController.createUser
)
```

---

## Logger con Winston

**Instalar:**
```bash
npm install winston
```

**src/config/logger.ts:**
```typescript
import winston from 'winston'

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
})

export default logger
```

**Uso:**
```typescript
import logger from './config/logger'

logger.info('Server started')
logger.error('Error occurred', { error })
```

---

## Testing con Jest

**Instalar:**
```bash
npm install -D jest ts-jest @types/jest supertest @types/supertest
```

**jest.config.js:**
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
  ],
}
```

**src/__tests__/api.test.ts:**
```typescript
import request from 'supertest'
import express from 'express'

const app = express()

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' })
})

describe('API Tests', () => {
  it('should return health status', async () => {
    const response = await request(app).get('/health')

    expect(response.status).toBe(200)
    expect(response.body).toEqual({ status: 'healthy' })
  })
})
```

**package.json:**
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

**Dockerfile.test:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npm", "test"]
```

**Ejecutar:**
```bash
docker build -f Dockerfile.test -t node-api-test .
docker run --rm node-api-test
```

---

## Ejercicios Prácticos

### Ejercicio 1: CRUD con TypeScript
Implementa CRUD completo para una entidad "Products" con:
- Validación de datos
- Manejo de errores
- Types/Interfaces de TypeScript
- Persistencia en PostgreSQL

### Ejercicio 2: Autenticación JWT
```bash
npm install jsonwebtoken bcryptjs
npm install -D @types/jsonwebtoken @types/bcryptjs
```

Implementa:
- POST /auth/register
- POST /auth/login
- Middleware de autenticación
- Rutas protegidas

### Ejercicio 3: Rate Limiting
```bash
npm install express-rate-limit
```

### Ejercicio 4: Documentación con Swagger
```bash
npm install swagger-jsdoc swagger-ui-express
npm install -D @types/swagger-jsdoc @types/swagger-ui-express
```

---

## Optimización de Dockerfile

**Multi-stage optimizado:**
```dockerfile
FROM node:18-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nodejs

COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./package.json

USER nodejs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

---

## Troubleshooting

### TypeScript no compila
```bash
# Verificar tsconfig.json
npx tsc --noEmit

# Ver errores de tipos
npm run type-check
```

### Cannot find module después de build
```bash
# Verificar que dist/ contiene los archivos
ls -la dist/

# Verificar tsconfig.json outDir y rootDir
```

### Base de datos no conecta
```bash
# Verificar que db está corriendo
docker compose ps

# Probar conexión desde api
docker compose exec api ping db

# Ver logs
docker compose logs db
```

---

## Resumen de Comandos

```bash
# Desarrollo local
npm run dev

# Build TypeScript
npm run build

# Producción local
npm start

# Docker producción
docker build -t node-api:v1 .
docker run -d --name node-api -p 3000:3000 node-api:v1

# Docker desarrollo
docker compose --profile development up -d

# Tests
npm test
docker run --rm node-api-test

# Logs
docker logs -f node-api
docker compose logs -f
```

---

## Checklist del Proyecto

- [ ] Inicializar proyecto npm
- [ ] Configurar TypeScript
- [ ] Instalar dependencias
- [ ] Crear estructura de directorios
- [ ] Desarrollar API Express
- [ ] Crear Dockerfile multi-stage
- [ ] Crear Dockerfile.dev
- [ ] Crear .dockerignore
- [ ] Construir y probar imagen
- [ ] Crear docker-compose.yml
- [ ] Integrar PostgreSQL
- [ ] Implementar CRUD endpoints
- [ ] Agregar validación
- [ ] Configurar logging
- [ ] Escribir tests
- [ ] Documentar API

---

## Siguiente Paso

Continúa con:
**[Proyecto 6: Backend con Astro JS](./06-astro-backend.md)**
