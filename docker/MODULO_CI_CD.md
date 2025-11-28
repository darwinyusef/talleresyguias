# Módulo 6: CI/CD con GitHub Actions

## Objetivo
Aprender a automatizar el proceso de construcción, testing y despliegue de aplicaciones Docker usando GitHub Actions.

---

## Índice

1. [¿Qué es CI/CD?](#qué-es-cicd)
2. [Introducción a GitHub Actions](#introducción-a-github-actions)
3. [Conceptos Básicos](#conceptos-básicos)
4. [Sintaxis de Workflows](#sintaxis-de-workflows)
5. [CI/CD para Proyectos Docker](#cicd-para-proyectos-docker)
6. [Ejemplos Prácticos](#ejemplos-prácticos)
7. [Secretos y Variables](#secretos-y-variables)
8. [Despliegue a Producción](#despliegue-a-producción)

---

## ¿Qué es CI/CD?

### Continuous Integration (CI)
Integración continua: automatizar el proceso de integrar cambios de código frecuentemente.

**Beneficios:**
- Detectar errores temprano
- Reducir conflictos de merge
- Asegurar calidad del código
- Builds automáticos

### Continuous Deployment/Delivery (CD)
Despliegue continuo: automatizar el proceso de liberar código a producción.

**Continuous Delivery:** Manual approval antes de producción
**Continuous Deployment:** Automático a producción

**Beneficios:**
- Entregas más rápidas
- Reducir errores humanos
- Rollbacks más fáciles
- Feedback más rápido

---

## Introducción a GitHub Actions

GitHub Actions es el sistema de CI/CD nativo de GitHub.

### Características
- Integrado con GitHub
- Marketplace de actions reutilizables
- Ejecutores (runners) en la nube
- Soporte para múltiples lenguajes
- Free tier generoso

### Límites Free Tier
- 2000 minutos/mes para repos privados
- Ilimitado para repos públicos
- 500 MB de storage

---

## Conceptos Básicos

### Workflow
Proceso automatizado configurable que ejecuta uno o más jobs.

### Event
Actividad que trigger un workflow:
- `push` - Al hacer push
- `pull_request` - Al crear/actualizar PR
- `schedule` - Cron jobs
- `workflow_dispatch` - Manual
- `release` - Al crear release

### Job
Set de steps que se ejecutan en el mismo runner.

### Step
Tarea individual (comando o action).

### Action
Aplicación reutilizable para realizar tareas.

### Runner
Servidor que ejecuta los workflows.

---

## Sintaxis de Workflows

Los workflows se definen en archivos YAML en `.github/workflows/`

### Estructura Básica

```yaml
name: Nombre del Workflow

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  job-name:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run a command
        run: echo "Hello World"
```

### Triggers Comunes

```yaml
# Push a branch específico
on:
  push:
    branches:
      - main
      - develop

# Pull request
on:
  pull_request:
    branches: [ main ]

# Múltiples eventos
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

# Schedule (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Diario a medianoche

# Manual
on:
  workflow_dispatch:

# On tag push
on:
  push:
    tags:
      - 'v*'
```

### Runners

```yaml
jobs:
  build:
    runs-on: ubuntu-latest    # Ubuntu Linux
    # runs-on: macos-latest   # macOS
    # runs-on: windows-latest # Windows
```

### Steps

```yaml
steps:
  # Usar action del marketplace
  - uses: actions/checkout@v4

  # Ejecutar comando
  - run: npm install

  # Múltiples comandos
  - run: |
      npm install
      npm run build
      npm test

  # Con nombre
  - name: Install dependencies
    run: npm install

  # Con working directory
  - name: Build
    working-directory: ./frontend
    run: npm run build
```

---

## CI/CD para Proyectos Docker

### 1. Workflow Básico - Build y Test

**.github/workflows/ci.yml:**
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: myapp:test
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run tests
        run: |
          docker run --rm myapp:test npm test
```

### 2. Build Multi-Platform

```yaml
name: Build Multi-Platform

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build multi-platform
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: false
          tags: myapp:latest
```

### 3. Push a Docker Hub

```yaml
name: Build and Push to Docker Hub

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: username/myapp
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 4. GitHub Container Registry (GHCR)

```yaml
name: Build and Push to GHCR

on:
  push:
    branches: [ main ]

jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

---

## Ejemplos Prácticos

### Ejemplo 1: Frontend React

**.github/workflows/frontend.yml:**
```yaml
name: Frontend CI/CD

on:
  push:
    branches: [ main ]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        working-directory: frontend
        run: npm ci

      - name: Run linter
        working-directory: frontend
        run: npm run lint

      - name: Run tests
        working-directory: frontend
        run: npm test

      - name: Build
        working-directory: frontend
        run: npm run build

  docker:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          push: true
          tags: username/frontend:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Ejemplo 2: Backend Node.js

**.github/workflows/backend.yml:**
```yaml
name: Backend CI/CD

on:
  push:
    branches: [ main ]
    paths:
      - 'backend/**'
  pull_request:
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: backend/package-lock.json

      - name: Install dependencies
        working-directory: backend
        run: npm ci

      - name: Run tests
        working-directory: backend
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
        run: npm test

  docker:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ghcr.io/${{ github.repository }}/backend:latest
```

### Ejemplo 3: Full Stack con Docker Compose

**.github/workflows/fullstack.yml:**
```yaml
name: Full Stack CI/CD

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Create .env file
        run: |
          echo "DB_USER=test" >> .env
          echo "DB_PASSWORD=test" >> .env
          echo "DB_NAME=testdb" >> .env

      - name: Start services
        run: docker compose up -d

      - name: Wait for services
        run: |
          timeout 60 bash -c 'until docker compose exec -T backend curl -f http://localhost:3000/health; do sleep 2; done'

      - name: Run integration tests
        run: docker compose exec -T backend npm test

      - name: Stop services
        run: docker compose down

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          echo "Deploy to your server"
          # Aquí van los comandos de deploy
```

### Ejemplo 4: Spring Boot (Java)

**.github/workflows/spring-boot.yml:**
```yaml
name: Spring Boot CI/CD

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: 'maven'

      - name: Build with Maven
        run: mvn clean package -DskipTests

      - name: Run tests
        run: mvn test

      - name: Build Docker image
        run: docker build -t myapp:latest .

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Push to Docker Hub
        run: |
          docker tag myapp:latest username/myapp:latest
          docker push username/myapp:latest
```

---

## Secretos y Variables

### Crear Secretos en GitHub

1. Ir a repositorio → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Agregar nombre y valor

### Usar Secretos

```yaml
steps:
  - name: Login to Docker Hub
    uses: docker/login-action@v3
    with:
      username: ${{ secrets.DOCKERHUB_USERNAME }}
      password: ${{ secrets.DOCKERHUB_TOKEN }}

  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    run: ./deploy.sh
```

### Variables de Entorno

```yaml
env:
  NODE_ENV: production
  API_URL: https://api.example.com

jobs:
  build:
    env:
      BUILD_ENV: staging

    steps:
      - name: Build
        env:
          SPECIFIC_VAR: value
        run: npm run build
```

### Secrets Comunes

```
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
GITHUB_TOKEN (automático)
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
SSH_PRIVATE_KEY
API_KEY
DATABASE_URL
```

---

## Despliegue a Producción

### 1. Despliegue por SSH

**.github/workflows/deploy-ssh.yml:**
```yaml
name: Deploy via SSH

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app
            git pull origin main
            docker compose down
            docker compose up -d --build
```

### 2. Despliegue a AWS ECR

```yaml
name: Deploy to AWS ECR

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: my-app
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

### 3. Despliegue a Google Cloud Run

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}

      - name: Configure Docker
        run: gcloud auth configure-docker

      - name: Build and push
        run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/myapp:latest .
          docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/myapp:latest

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy myapp \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/myapp:latest \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated
```

### 4. Despliegue a DigitalOcean

```yaml
name: Deploy to DigitalOcean

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_TOKEN }}

      - name: Build image
        run: docker build -t myapp .

      - name: Push to registry
        run: |
          doctl registry login
          docker tag myapp registry.digitalocean.com/my-registry/myapp:latest
          docker push registry.digitalocean.com/my-registry/myapp:latest

      - name: Deploy to droplet
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.DROPLET_IP }}
          username: root
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            doctl registry login
            docker pull registry.digitalocean.com/my-registry/myapp:latest
            docker stop myapp || true
            docker rm myapp || true
            docker run -d --name myapp -p 80:80 \
              registry.digitalocean.com/my-registry/myapp:latest
```

---

## Workflows Avanzados

### Matrix Strategy

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: [16, 18, 20]
        os: [ubuntu-latest, macos-latest]

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}

      - run: npm test
```

### Reusable Workflows

**.github/workflows/reusable-docker-build.yml:**
```yaml
name: Reusable Docker Build

on:
  workflow_call:
    inputs:
      image_name:
        required: true
        type: string
      context:
        required: false
        type: string
        default: .

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: ${{ inputs.context }}
          tags: ${{ inputs.image_name }}:latest
```

**Usar workflow reutilizable:**
```yaml
jobs:
  build-frontend:
    uses: ./.github/workflows/reusable-docker-build.yml
    with:
      image_name: myapp-frontend
      context: ./frontend
```

### Cache de Dependencias

```yaml
steps:
  - uses: actions/checkout@v4

  # Node.js
  - uses: actions/setup-node@v4
    with:
      node-version: '18'
      cache: 'npm'

  # Python
  - uses: actions/setup-python@v5
    with:
      python-version: '3.11'
      cache: 'pip'

  # Maven
  - uses: actions/setup-java@v4
    with:
      java-version: '17'
      distribution: 'temurin'
      cache: 'maven'

  # Docker layers
  - uses: docker/build-push-action@v5
    with:
      cache-from: type=gha
      cache-to: type=gha,mode=max
```

---

## Badges de Estado

Agregar badge al README.md:

```markdown
![CI](https://github.com/username/repo/workflows/CI/badge.svg)
![Docker](https://github.com/username/repo/workflows/Docker/badge.svg)
```

---

## Troubleshooting

### Debug Mode

Agregar secreto `ACTIONS_STEP_DEBUG` con valor `true`

### Ver logs detallados

```yaml
- name: Debug
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    env
```

### Workflow no se ejecuta

- Verificar sintaxis YAML
- Verificar path del archivo (`.github/workflows/`)
- Verificar triggers (on)
- Verificar permisos

---

## Mejores Prácticas

1. **Usar versiones específicas de actions**
```yaml
# Bien
- uses: actions/checkout@v4

# Evitar
- uses: actions/checkout@main
```

2. **Cachear dependencias**
```yaml
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
```

3. **Minimizar uso de minutos**
- Usar cache
- Ejecutar solo en paths relevantes
- Cancelar workflows anteriores

4. **Seguridad**
- Usar secrets para información sensible
- No hacer echo de secrets
- Usar GITHUB_TOKEN cuando sea posible

5. **Organizar workflows**
- Un workflow por propósito
- Nombres descriptivos
- Documentar con comentarios

---

## Recursos

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Marketplace](https://github.com/marketplace?type=actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)

---

## Ejercicios Prácticos

### Ejercicio 1: CI Básico
Crea un workflow que:
- Se ejecute en push y PR
- Haga build de tu proyecto
- Ejecute tests
- Reporte código coverage

### Ejercicio 2: Docker Build y Push
Crea workflow que:
- Build imagen Docker
- Push a Docker Hub
- Solo en push a main
- Con tags de versión

### Ejercicio 3: Deploy Automático
Crea workflow que:
- Build y test
- Deploy a servidor via SSH
- Solo si tests pasan
- Notificar en Slack/Discord

### Ejercicio 4: Multi-Environment
Crea workflow con:
- Deploy a staging automático
- Deploy a producción manual
- Diferentes variables por ambiente

---

¡Felicidades! Has completado el módulo de CI/CD con GitHub Actions.
