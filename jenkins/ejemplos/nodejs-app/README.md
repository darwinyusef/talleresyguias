# Aplicación Node.js de Ejemplo para Jenkins

Aplicación Express simple para demostrar CI/CD con Jenkins.

## 🚀 Características

- API REST con Express
- Tests con Jest
- Linting con ESLint
- Docker multi-stage build
- Health checks
- Logging estructurado

## 📋 Requisitos

- Node.js 18+
- Docker
- Jenkins

## 🛠️ Instalación Local

```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev

# Ejecutar tests
npm test

# Ejecutar linter
npm run lint

# Build para producción
npm run build
```

## 🐳 Docker

```bash
# Build
docker build -t nodejs-app:latest .

# Run
docker run -p 3000:3000 nodejs-app:latest

# Con docker-compose
docker compose up
```

## 🔧 Variables de Entorno

```bash
PORT=3000
NODE_ENV=production
LOG_LEVEL=info
```

## 📡 Endpoints

- `GET /` - Información de la API
- `GET /health` - Health check
- `GET /api/users` - Lista de usuarios
- `POST /api/users` - Crear usuario
- `GET /api/users/:id` - Obtener usuario
- `PUT /api/users/:id` - Actualizar usuario
- `DELETE /api/users/:id` - Eliminar usuario

## 🧪 Testing

```bash
# Tests unitarios
npm test

# Tests con coverage
npm run test:coverage

# Tests en watch mode
npm run test:watch
```

## 📦 CI/CD con Jenkins

Ver `Jenkinsfile` en la raíz del proyecto.

### Pipeline Stages:

1. **Checkout** - Clonar repositorio
2. **Install** - Instalar dependencias
3. **Lint** - Verificar código
4. **Test** - Ejecutar tests
5. **Build** - Construir imagen Docker
6. **Push** - Publicar a registry
7. **Deploy** - Desplegar aplicación

## 📄 Licencia

MIT
