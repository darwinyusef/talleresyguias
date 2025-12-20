# Taller Completo: Jenkins con Docker

Guía completa para dominar Jenkins usando Docker, desde fundamentos hasta pipelines avanzados de CI/CD.

**📋 [Ver Índice Completo del Taller](#-índice-del-taller)** - Navegación rápida por todo el contenido

---

## 📖 Índice del Taller

### Fundamentos

#### [Módulo 1: Introducción a Jenkins](#módulo-1-introducción-a-jenkins)
- ¿Qué es Jenkins?
- Arquitectura de Jenkins
- Instalación con Docker
- Configuración inicial
- Interfaz web y conceptos básicos

#### [Módulo 2: Primeros Pasos con Jenkins](#módulo-2-primeros-pasos-con-jenkins)
- Crear tu primer Job
- Tipos de Jobs (Freestyle, Pipeline)
- Configuración de Jobs
- Ejecutar builds manualmente
- Ver logs y resultados

#### [Módulo 3: Jenkins con Docker](#módulo-3-jenkins-con-docker)
- Docker-in-Docker (DinD)
- Docker-outside-of-Docker (DooD)
- Agentes Docker
- Construcción de imágenes en Jenkins
- Docker Compose con Jenkins

### Pipelines

#### [Módulo 4: Introducción a Pipelines](#módulo-4-introducción-a-pipelines)
- Declarative vs Scripted Pipeline
- Sintaxis básica de Jenkinsfile
- Stages y Steps
- Variables de entorno
- Parámetros de build

#### [Módulo 5: Pipelines Avanzados](#módulo-5-pipelines-avanzados)
- Parallel execution
- Conditional stages
- Post actions
- Shared libraries
- Pipeline templates

### Integración Continua

#### [Módulo 6: CI/CD con Jenkins](#módulo-6-cicd-con-jenkins)
- Integración con Git/GitHub
- Webhooks y triggers automáticos
- Build de aplicaciones (Node.js, Python, Java)
- Testing automatizado
- Code quality (SonarQube)

#### [Módulo 7: Deployment Automatizado](#módulo-7-deployment-automatizado)
- Deploy a Docker Hub
- Deploy a servidores remotos
- Deploy a Kubernetes
- Blue-Green deployment
- Canary deployment

### Seguridad y Mejores Prácticas

#### [Módulo 8: Seguridad en Jenkins](#módulo-8-seguridad-en-jenkins)
- Gestión de credenciales
- Secrets management
- Roles y permisos
- Plugins de seguridad
- Auditoría y logs

#### [Módulo 9: Monitoreo y Optimización](#módulo-9-monitoreo-y-optimización)
- Métricas de Jenkins
- Monitoreo con Prometheus
- Optimización de builds
- Cache y artifacts
- Limpieza automática

### Proyectos Prácticos

#### [Proyecto 1: Pipeline para Aplicación Node.js](#proyecto-1-pipeline-para-aplicación-nodejs)
- Build, test y deploy de app Node.js
- Docker multi-stage build
- Deploy a Docker Hub

#### [Proyecto 2: Pipeline Full Stack](#proyecto-2-pipeline-full-stack)
- Frontend React + Backend Node.js
- Testing E2E
- Deploy a producción

#### [Proyecto 3: Microservicios con Jenkins](#proyecto-3-microservicios-con-jenkins)
- Pipeline para múltiples servicios
- Orquestación con Docker Compose
- Deploy a Kubernetes

---

## 🎯 Objetivos de Aprendizaje

Al completar este taller, serás capaz de:

### Fundamentos
✅ Instalar y configurar Jenkins con Docker
✅ Crear y gestionar Jobs
✅ Entender la arquitectura de Jenkins
✅ Usar Docker dentro de Jenkins (DinD/DooD)

### Pipelines
✅ Escribir Jenkinsfiles declarativos y scriptados
✅ Implementar pipelines multi-stage
✅ Usar parallel execution
✅ Crear shared libraries reutilizables

### CI/CD
✅ Integrar Jenkins con Git/GitHub
✅ Automatizar builds y tests
✅ Implementar deployment continuo
✅ Usar estrategias de deployment avanzadas

### Seguridad
✅ Gestionar credenciales de forma segura
✅ Configurar roles y permisos
✅ Implementar mejores prácticas de seguridad

---

## 🚀 Inicio Rápido

```bash
# 1. Crear directorio para Jenkins
mkdir -p ~/jenkins-docker
cd ~/jenkins-docker

# 2. Crear docker-compose.yml (ver Módulo 1)
# 3. Iniciar Jenkins
docker compose up -d

# 4. Obtener password inicial
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# 5. Abrir navegador
open http://localhost:8080
```

---

## 📁 Estructura del Repositorio

```
jenkins/
├── README.md                          # Este archivo (índice principal)
├── docker/                            # Configuraciones Docker
│   ├── docker-compose.yml             # Compose para Jenkins
│   ├── Dockerfile.jenkins             # Imagen personalizada de Jenkins
│   └── Dockerfile.agent               # Agente Jenkins personalizado
├── pipelines/                         # Ejemplos de Jenkinsfiles
│   ├── 01-basic-pipeline.jenkinsfile
│   ├── 02-docker-build.jenkinsfile
│   ├── 03-nodejs-app.jenkinsfile
│   ├── 04-parallel-stages.jenkinsfile
│   └── 05-kubernetes-deploy.jenkinsfile
├── ejemplos/                          # Aplicaciones de ejemplo
│   ├── nodejs-app/
│   ├── python-api/
│   └── java-spring/
└── scripts/                           # Scripts útiles
    ├── backup-jenkins.sh
    ├── restore-jenkins.sh
    └── cleanup-old-builds.sh
```

---

## 💡 Consejos para el Aprendizaje

1. **Practica con cada ejemplo** - Ejecuta todos los pipelines
2. **Modifica los Jenkinsfiles** - Experimenta con diferentes configuraciones
3. **Revisa los logs** - Aprende a debuggear pipelines
4. **Usa versión control** - Guarda tus Jenkinsfiles en Git
5. **Automatiza todo** - Si lo haces más de una vez, automatízalo

---

## 🛠️ Tecnologías Cubiertas

### Core
- Jenkins LTS
- Docker & Docker Compose
- Groovy (para Jenkinsfiles)

### Lenguajes y Frameworks
- Node.js + Express
- Python + FastAPI
- Java + Spring Boot
- React + Vite

### Herramientas de CI/CD
- Git/GitHub
- Docker Hub
- SonarQube
- Nexus/Artifactory

### Testing
- Jest (JavaScript)
- Pytest (Python)
- JUnit (Java)
- Selenium/Cypress (E2E)

### Deployment
- Docker Swarm
- Kubernetes
- AWS EC2
- Azure VMs

### Monitoreo
- Prometheus
- Grafana
- ELK Stack

---

## 📋 Prerrequisitos

### Software Necesario
- Docker Desktop o Docker Engine
- Docker Compose
- Git
- Editor de código (VS Code recomendado)

### Conocimientos
- Básicos de Docker
- Conceptos de CI/CD
- Línea de comandos
- Git básico

---

## 🔗 Recursos Adicionales

### Documentación Oficial
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Plugin Index](https://plugins.jenkins.io/)

### Herramientas Útiles
- [Jenkins Pipeline Linter](https://www.jenkins.io/doc/book/pipeline/development/#linter)
- [Blue Ocean Plugin](https://www.jenkins.io/projects/blueocean/)
- [Pipeline Snippet Generator](https://www.jenkins.io/doc/book/pipeline/getting-started/#snippet-generator)

### Comunidades
- [Jenkins Community](https://www.jenkins.io/participate/)
- [r/jenkinsci](https://reddit.com/r/jenkinsci)
- [Stack Overflow - Jenkins](https://stackoverflow.com/questions/tagged/jenkins)

---

## 🎉 ¡Comienza tu viaje!

Empieza con el [Módulo 1](#módulo-1-introducción-a-jenkins) y avanza a tu propio ritmo.

**¡Buena suerte y feliz aprendizaje!** 🚀

---

<div align="center">

**Jenkins con Docker - Taller Completo**

[Fundamentos](#fundamentos) • [Pipelines](#pipelines) • [CI/CD](#integración-continua) • [Proyectos](#proyectos-prácticos)

</div>

---

# Módulo 1: Introducción a Jenkins

## ¿Qué es Jenkins?

Jenkins es un servidor de automatización open-source que permite implementar CI/CD (Integración Continua y Despliegue Continuo). Es la herramienta más popular para automatizar:

- **Build**: Compilación de código
- **Test**: Ejecución de pruebas automatizadas
- **Deploy**: Despliegue a diferentes entornos
- **Monitoreo**: Seguimiento de builds y deployments

### Características Principales

- **Open Source**: Gratuito y con gran comunidad
- **Extensible**: Más de 1800 plugins disponibles
- **Multiplataforma**: Funciona en Windows, Linux, macOS
- **Distribuido**: Soporta builds distribuidos con agentes
- **Pipeline as Code**: Define pipelines en código (Jenkinsfile)

## Arquitectura de Jenkins

```
┌─────────────────────────────────────────┐
│         Jenkins Master (Controller)      │
│  - Gestiona builds                       │
│  - Programa trabajos                     │
│  - Monitorea agentes                     │
│  - Interfaz web                          │
└─────────────┬───────────────────────────┘
              │
    ┌─────────┴─────────┬─────────────┐
    │                   │             │
┌───▼────┐      ┌──────▼───┐   ┌────▼─────┐
│ Agent 1│      │ Agent 2  │   │ Agent 3  │
│ (Docker)│     │ (Linux)  │   │ (Windows)│
└────────┘      └──────────┘   └──────────┘
```

### Componentes

1. **Master/Controller**: Servidor principal que coordina todo
2. **Agents/Nodes**: Máquinas que ejecutan los builds
3. **Jobs/Projects**: Tareas configuradas para ejecutar
4. **Builds**: Ejecuciones individuales de un job
5. **Plugins**: Extensiones que añaden funcionalidad

## Instalación con Docker

### Opción 1: Docker Run Simple

```bash
# Crear volumen para persistencia
docker volume create jenkins_home

# Ejecutar Jenkins
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

### Opción 2: Docker Compose (Recomendado)

Crea el archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  jenkins:
    image: jenkins/jenkins:lts
    container_name: jenkins
    privileged: true
    user: root
    ports:
      - "8080:8080"      # Puerto web
      - "50000:50000"    # Puerto para agentes
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock  # Docker-outside-of-Docker
    environment:
      - JENKINS_OPTS=--prefix=/jenkins
    restart: unless-stopped

volumes:
  jenkins_home:
    driver: local
```

**Iniciar Jenkins:**

```bash
# Crear directorio del proyecto
mkdir jenkins-docker && cd jenkins-docker

# Crear docker-compose.yml (copiar contenido de arriba)

# Iniciar Jenkins
docker compose up -d

# Ver logs
docker compose logs -f jenkins

# Obtener password inicial
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Opción 3: Jenkins con Docker Instalado (DooD)

Para poder usar Docker dentro de Jenkins, necesitamos instalar Docker CLI en el contenedor:

Crea `Dockerfile.jenkins`:

```dockerfile
FROM jenkins/jenkins:lts

USER root

# Instalar Docker CLI
RUN apt-get update && \
    apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

USER jenkins

# Instalar plugins comunes (opcional)
RUN jenkins-plugin-cli --plugins \
    git \
    docker-workflow \
    pipeline-stage-view \
    blueocean
```

Actualiza `docker-compose.yml`:

```yaml
version: '3.8'

services:
  jenkins:
    build:
      context: .
      dockerfile: Dockerfile.jenkins
    container_name: jenkins
    privileged: true
    user: root
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DOCKER_HOST=unix:///var/run/docker.sock
    restart: unless-stopped

volumes:
  jenkins_home:
```

**Construir e iniciar:**

```bash
docker compose build
docker compose up -d
```

## Configuración Inicial

### 1. Acceder a Jenkins

Abre tu navegador en: `http://localhost:8080`

### 2. Desbloquear Jenkins

Obtén el password inicial:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Copia el password y pégalo en la interfaz web.

### 3. Instalar Plugins

Selecciona **"Install suggested plugins"** para instalar los plugins más comunes:

- Git
- Pipeline
- Docker
- Credentials
- SSH
- Email Extension

### 4. Crear Usuario Administrador

Completa el formulario:
- Username: `admin`
- Password: `tu_password_seguro`
- Full name: `Tu Nombre`
- Email: `tu@email.com`

### 5. Configurar URL de Jenkins

Por defecto: `http://localhost:8080/`

Para producción, usa tu dominio: `https://jenkins.tudominio.com/`

## Interfaz Web y Conceptos Básicos

### Dashboard Principal

```
┌─────────────────────────────────────────┐
│  Jenkins                    [Admin ▼]   │
├─────────────────────────────────────────┤
│  [New Item] [People] [Build History]    │
├─────────────────────────────────────────┤
│  📊 All Jobs                             │
│  ┌──────────────────────────────────┐  │
│  │ ✓ my-first-job      #5 Success  │  │
│  │ ⚠ backend-build     #12 Unstable│  │
│  │ ✗ frontend-deploy   #3 Failed   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Elementos de la Interfaz

1. **New Item**: Crear nuevo job/pipeline
2. **People**: Usuarios y permisos
3. **Build History**: Historial de builds
4. **Manage Jenkins**: Configuración global
5. **My Views**: Vistas personalizadas

### Tipos de Jobs

1. **Freestyle Project**: Job tradicional con GUI
2. **Pipeline**: Pipeline as code (Jenkinsfile)
3. **Multibranch Pipeline**: Pipeline para múltiples ramas
4. **Folder**: Organizar jobs en carpetas
5. **Multibranch Pipeline**: Pipeline automático por rama

## Verificar Instalación

### 1. Verificar Docker en Jenkins

Crea un job de prueba:

1. Click en **"New Item"**
2. Nombre: `test-docker`
3. Tipo: **Pipeline**
4. En "Pipeline script", escribe:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test Docker') {
            steps {
                sh 'docker --version'
                sh 'docker ps'
            }
        }
    }
}
```

5. Click **"Save"** y luego **"Build Now"**

### 2. Verificar Plugins Instalados

1. Ve a **"Manage Jenkins"** → **"Manage Plugins"**
2. Pestaña **"Installed"**
3. Verifica que estén instalados:
   - Git plugin
   - Docker plugin
   - Pipeline plugin

## Comandos Útiles

```bash
# Ver logs de Jenkins
docker compose logs -f jenkins

# Reiniciar Jenkins
docker compose restart jenkins

# Detener Jenkins
docker compose stop jenkins

# Iniciar Jenkins
docker compose start jenkins

# Eliminar Jenkins (¡cuidado! perderás datos si no usas volumen)
docker compose down

# Backup de Jenkins
docker run --rm \
  -v jenkins_home:/var/jenkins_home \
  -v $(pwd):/backup \
  alpine tar czf /backup/jenkins-backup-$(date +%Y%m%d).tar.gz /var/jenkins_home

# Restore de Jenkins
docker run --rm \
  -v jenkins_home:/var/jenkins_home \
  -v $(pwd):/backup \
  alpine tar xzf /backup/jenkins-backup-YYYYMMDD.tar.gz -C /
```

## Troubleshooting

### Problema: No puedo acceder a Jenkins

```bash
# Verificar que el contenedor está corriendo
docker ps | grep jenkins

# Verificar logs
docker logs jenkins

# Verificar puerto
lsof -i :8080
```

### Problema: Permission denied con Docker

```bash
# Dar permisos al usuario jenkins
docker exec -u root jenkins chmod 666 /var/run/docker.sock

# O añadir jenkins al grupo docker (dentro del contenedor)
docker exec -u root jenkins usermod -aG docker jenkins
docker restart jenkins
```

### Problema: Jenkins muy lento

```bash
# Aumentar memoria en docker-compose.yml
environment:
  - JAVA_OPTS=-Xmx2048m -Xms512m
```

---

# Módulo 2: Primeros Pasos con Jenkins

## Crear tu Primer Job

### Job Freestyle (Tradicional)

1. **Crear Job**
   - Click en **"New Item"**
   - Nombre: `mi-primer-job`
   - Tipo: **Freestyle project**
   - Click **"OK"**

2. **Configurar Job**
   
   **General:**
   - Description: `Mi primer job en Jenkins`
   - ✓ Discard old builds (mantener últimos 10)

   **Build Steps:**
   - Click **"Add build step"** → **"Execute shell"**
   - Comando:
   ```bash
   echo "¡Hola desde Jenkins!"
   echo "Fecha: $(date)"
   echo "Usuario: $(whoami)"
   echo "Directorio: $(pwd)"
   ```

3. **Guardar y Ejecutar**
   - Click **"Save"**
   - Click **"Build Now"**
   - Ver resultado en **"Console Output"**

### Job Pipeline (Moderno)

1. **Crear Pipeline**
   - Click en **"New Item"**
   - Nombre: `mi-primer-pipeline`
   - Tipo: **Pipeline**
   - Click **"OK"**

2. **Escribir Pipeline**

```groovy
pipeline {
    agent any
    
    stages {
        stage('Preparación') {
            steps {
                echo '🚀 Iniciando pipeline...'
            }
        }
        
        stage('Build') {
            steps {
                echo '🔨 Construyendo aplicación...'
                sh 'echo "Simulando build..."'
                sh 'sleep 2'
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Ejecutando tests...'
                sh 'echo "Simulando tests..."'
                sh 'sleep 2'
            }
        }
        
        stage('Deploy') {
            steps {
                echo '🚢 Desplegando aplicación...'
                sh 'echo "Simulando deploy..."'
                sh 'sleep 2'
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completado exitosamente!'
        }
        failure {
            echo '❌ Pipeline falló!'
        }
    }
}
```

3. **Ejecutar**
   - Click **"Save"**
   - Click **"Build Now"**
   - Ver progreso en **"Stage View"**

## Tipos de Jobs

### 1. Freestyle Project

**Ventajas:**
- Fácil de configurar con GUI
- Ideal para principiantes
- No requiere código

**Desventajas:**
- No versionable
- Difícil de mantener
- Limitado en funcionalidad

**Cuándo usar:**
- Jobs simples
- Tareas administrativas
- Migraciones legacy

### 2. Pipeline

**Ventajas:**
- Pipeline as Code (Jenkinsfile)
- Versionable en Git
- Reutilizable
- Poderoso y flexible

**Desventajas:**
- Curva de aprendizaje
- Requiere conocer Groovy

**Cuándo usar:**
- CI/CD moderno
- Proyectos complejos
- Equipos colaborativos

### 3. Multibranch Pipeline

**Ventajas:**
- Detecta ramas automáticamente
- Jenkinsfile por rama
- Ideal para Git Flow

**Desventajas:**
- Más complejo de configurar
- Requiere Jenkinsfile en repo

**Cuándo usar:**
- Proyectos con múltiples ramas
- Feature branches
- Pull requests

### 4. Organization Folder

**Ventajas:**
- Escanea toda la organización
- Detecta repos automáticamente
- Ideal para microservicios

**Cuándo usar:**
- Múltiples repositorios
- Organización GitHub/GitLab
- Arquitectura de microservicios

## Configuración de Jobs

### Parámetros de Build

Permite ejecutar builds con diferentes valores:

```groovy
pipeline {
    agent any
    
    parameters {
        string(name: 'ENVIRONMENT', defaultValue: 'dev', description: 'Entorno de deploy')
        choice(name: 'VERSION', choices: ['1.0', '1.1', '2.0'], description: 'Versión a desplegar')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: '¿Ejecutar tests?')
    }
    
    stages {
        stage('Info') {
            steps {
                echo "Desplegando versión ${params.VERSION} en ${params.ENVIRONMENT}"
                echo "Ejecutar tests: ${params.RUN_TESTS}"
            }
        }
        
        stage('Test') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                echo '🧪 Ejecutando tests...'
            }
        }
    }
}
```

### Triggers Automáticos

#### 1. Poll SCM (Verificar cambios periódicamente)

```groovy
pipeline {
    agent any
    
    triggers {
        // Verificar cada 5 minutos
        pollSCM('H/5 * * * *')
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
    }
}
```

#### 2. Cron (Ejecutar en horarios específicos)

```groovy
pipeline {
    agent any
    
    triggers {
        // Ejecutar todos los días a las 2 AM
        cron('0 2 * * *')
    }
    
    stages {
        stage('Backup') {
            steps {
                echo 'Ejecutando backup nocturno...'
            }
        }
    }
}
```

#### 3. Webhook (GitHub/GitLab)

Configuración en GitHub:
1. Settings → Webhooks → Add webhook
2. Payload URL: `http://jenkins.tudominio.com/github-webhook/`
3. Content type: `application/json`
4. Events: `Push events`, `Pull requests`

En Jenkins:

```groovy
pipeline {
    agent any
    
    triggers {
        githubPush()
    }
    
    stages {
        stage('Build on Push') {
            steps {
                echo 'Build triggered by GitHub push'
            }
        }
    }
}
```

### Variables de Entorno

```groovy
pipeline {
    agent any
    
    environment {
        // Variables globales
        APP_NAME = 'mi-aplicacion'
        VERSION = '1.0.0'
        DOCKER_REGISTRY = 'docker.io'
    }
    
    stages {
        stage('Build') {
            environment {
                // Variables específicas del stage
                BUILD_ENV = 'production'
            }
            
            steps {
                echo "Building ${APP_NAME} v${VERSION}"
                echo "Registry: ${DOCKER_REGISTRY}"
                echo "Environment: ${BUILD_ENV}"
                
                // Variables predefinidas de Jenkins
                echo "Build Number: ${BUILD_NUMBER}"
                echo "Job Name: ${JOB_NAME}"
                echo "Workspace: ${WORKSPACE}"
            }
        }
    }
}
```

### Variables Predefinidas Útiles

```groovy
pipeline {
    agent any
    
    stages {
        stage('Environment Info') {
            steps {
                sh '''
                    echo "BUILD_NUMBER: ${BUILD_NUMBER}"
                    echo "BUILD_ID: ${BUILD_ID}"
                    echo "JOB_NAME: ${JOB_NAME}"
                    echo "BUILD_TAG: ${BUILD_TAG}"
                    echo "WORKSPACE: ${WORKSPACE}"
                    echo "JENKINS_HOME: ${JENKINS_HOME}"
                    echo "JENKINS_URL: ${JENKINS_URL}"
                    echo "NODE_NAME: ${NODE_NAME}"
                '''
            }
        }
    }
}
```

## Ejecutar Builds

### Manualmente

1. **Desde la interfaz:**
   - Ir al job
   - Click **"Build Now"**
   - (Si hay parámetros) Click **"Build with Parameters"**

2. **Desde CLI:**

```bash
# Instalar Jenkins CLI
wget http://localhost:8080/jnlpJars/jenkins-cli.jar

# Ejecutar build
java -jar jenkins-cli.jar -s http://localhost:8080/ \
  -auth admin:password \
  build mi-primer-job

# Con parámetros
java -jar jenkins-cli.jar -s http://localhost:8080/ \
  -auth admin:password \
  build mi-primer-job \
  -p ENVIRONMENT=production \
  -p VERSION=2.0
```

3. **Desde API REST:**

```bash
# Sin parámetros
curl -X POST http://admin:password@localhost:8080/job/mi-primer-job/build

# Con parámetros
curl -X POST http://admin:password@localhost:8080/job/mi-primer-job/buildWithParameters \
  --data ENVIRONMENT=production \
  --data VERSION=2.0
```

### Automáticamente

Ver sección de [Triggers Automáticos](#triggers-automáticos).

## Ver Logs y Resultados

### Console Output

1. Ir al job
2. Click en el número de build (ej: `#5`)
3. Click **"Console Output"**

### Pipeline Stage View

Para pipelines, Jenkins muestra una vista visual de stages:

```
[Preparación] → [Build] → [Test] → [Deploy]
   ✓ 2s         ✓ 5s      ✓ 10s     ✓ 3s
```

### Blue Ocean (Interfaz Moderna)

1. Instalar plugin **Blue Ocean**
2. Click en **"Open Blue Ocean"**
3. Vista moderna y visual de pipelines

### Logs en Tiempo Real

```bash
# Ver logs en tiempo real
docker exec jenkins tail -f /var/jenkins_home/jobs/mi-primer-job/builds/lastBuild/log
```

### Artifacts

Guardar archivos generados:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'echo "Build output" > output.txt'
                sh 'tar czf app.tar.gz output.txt'
            }
        }
        
        stage('Archive') {
            steps {
                // Guardar artifacts
                archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
            }
        }
    }
}
```

Los artifacts se pueden descargar desde la interfaz web.

## Ejemplo Práctico Completo

```groovy
pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Target environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests?')
    }
    
    environment {
        APP_NAME = 'my-app'
        VERSION = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "📥 Checking out code..."
                // En un proyecto real, aquí iría:
                // git 'https://github.com/user/repo.git'
            }
        }
        
        stage('Build') {
            steps {
                echo "🔨 Building ${APP_NAME} v${VERSION}..."
                sh '''
                    echo "Compiling..."
                    sleep 2
                    echo "Build complete!"
                '''
            }
        }
        
        stage('Test') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                echo "🧪 Running tests..."
                sh '''
                    echo "Running unit tests..."
                    sleep 2
                    echo "All tests passed!"
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                echo "🚀 Deploying to ${params.ENVIRONMENT}..."
                sh """
                    echo "Deploying ${APP_NAME} v${VERSION} to ${params.ENVIRONMENT}"
                    sleep 2
                    echo "Deployment complete!"
                """
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
            // emailext (
            //     subject: "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
            //     body: "Build succeeded!",
            //     to: "team@example.com"
            // )
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            echo '🧹 Cleaning up...'
            cleanWs()
        }
    }
}
```

---

# Módulo 3: Jenkins con Docker

## Docker-in-Docker (DinD) vs Docker-outside-of-Docker (DooD)

### Docker-in-Docker (DinD)

Jenkins corre Docker daemon dentro del contenedor.

**Ventajas:**
- Aislamiento completo
- Múltiples daemons independientes

**Desventajas:**
- Más complejo
- Problemas de seguridad
- Mayor uso de recursos

**Configuración:**

```yaml
version: '3.8'

services:
  jenkins:
    image: jenkins/jenkins:lts
    privileged: true
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
    environment:
      - DOCKER_TLS_CERTDIR=/certs
    
  dind:
    image: docker:dind
    privileged: true
    environment:
      - DOCKER_TLS_CERTDIR=/certs
    volumes:
      - jenkins-docker-certs:/certs/client
      - jenkins_home:/var/jenkins_home

volumes:
  jenkins_home:
  jenkins-docker-certs:
```

### Docker-outside-of-Docker (DooD) - Recomendado

Jenkins usa el Docker daemon del host.

**Ventajas:**
- Más simple
- Mejor rendimiento
- Comparte imágenes con host

**Desventajas:**
- Menos aislamiento
- Acceso al Docker del host

**Configuración:**

Ya la vimos en el Módulo 1. Es la opción recomendada.

## Agentes Docker

Los agentes Docker permiten ejecutar builds en contenedores efímeros.

### Agente Docker Simple

```groovy
pipeline {
    agent {
        docker {
            image 'node:18-alpine'
        }
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'node --version'
                sh 'npm --version'
            }
        }
    }
}
```

### Agente Docker con Argumentos

```groovy
pipeline {
    agent {
        docker {
            image 'node:18-alpine'
            args '-v /tmp:/tmp -u root'
        }
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm test'
            }
        }
    }
}
```

### Múltiples Agentes Docker

```groovy
pipeline {
    agent none
    
    stages {
        stage('Backend Build') {
            agent {
                docker {
                    image 'node:18-alpine'
                }
            }
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Frontend Build') {
            agent {
                docker {
                    image 'node:18-alpine'
                }
            }
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Python Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                }
            }
            steps {
                sh 'pip install pytest'
                sh 'pytest'
            }
        }
    }
}
```

### Agente Docker Personalizado

Crear `Dockerfile.build`:

```dockerfile
FROM node:18-alpine

RUN apk add --no-cache \
    git \
    python3 \
    make \
    g++

WORKDIR /app

USER node
```

Usar en pipeline:

```groovy
pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.build'
            args '-v $HOME/.npm:/home/node/.npm'
        }
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
    }
}
```

## Construcción de Imágenes en Jenkins

### Build Simple

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("mi-app:${BUILD_NUMBER}")
                }
            }
        }
    }
}
```

### Build con Dockerfile Personalizado

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    def app = docker.build(
                        "mi-app:${BUILD_NUMBER}",
                        "-f Dockerfile.prod ."
                    )
                }
            }
        }
    }
}
```

### Build y Push a Docker Hub

```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'usuario/mi-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Build Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true"
        }
    }
}
```

### Multi-Stage Build

`Dockerfile`:

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

`Jenkinsfile`:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build Multi-Stage Image') {
            steps {
                script {
                    docker.build(
                        "mi-app:${BUILD_NUMBER}",
                        "--target production ."
                    )
                }
            }
        }
    }
}
```

## Docker Compose con Jenkins

### Ejemplo: Aplicación Full Stack

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://backend:4000

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "4000:4000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

`Jenkinsfile`:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build Services') {
            steps {
                sh 'docker compose build'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    docker compose up -d db
                    sleep 5
                    docker compose run --rm backend npm test
                    docker compose run --rm frontend npm test
                '''
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh '''
                    docker compose up -d
                    sleep 10
                    # Ejecutar tests E2E
                    docker compose run --rm frontend npm run test:e2e
                '''
            }
        }
    }
    
    post {
        always {
            sh 'docker compose down -v'
        }
    }
}
```

### Testing con Docker Compose

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup Test Environment') {
            steps {
                sh '''
                    # Crear network para tests
                    docker network create test-network || true
                    
                    # Iniciar base de datos de prueba
                    docker run -d \
                        --name test-db \
                        --network test-network \
                        -e POSTGRES_PASSWORD=test \
                        postgres:15-alpine
                    
                    # Esperar a que esté lista
                    sleep 5
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm \
                        --network test-network \
                        -e DATABASE_URL=postgresql://postgres:test@test-db:5432/postgres \
                        mi-app:test \
                        npm test
                '''
            }
        }
    }
    
    post {
        always {
            sh '''
                docker stop test-db || true
                docker rm test-db || true
                docker network rm test-network || true
            '''
        }
    }
}
```

## Ejemplo Práctico: Pipeline Completo con Docker

```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'usuario/mi-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/usuario/mi-app.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }
        
        stage('Test in Container') {
            steps {
                sh """
                    docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} npm test
                """
            }
        }
        
        stage('Security Scan') {
            steps {
                sh """
                    # Escanear vulnerabilidades con Trivy
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image ${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials') {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    # Deploy usando docker-compose
                    docker compose -f docker-compose.prod.yml pull
                    docker compose -f docker-compose.prod.yml up -d
                """
            }
        }
    }
    
    post {
        always {
            sh """
                # Limpiar imágenes antiguas
                docker image prune -f
            """
        }
        success {
            echo "✅ Build y deploy exitoso!"
        }
        failure {
            echo "❌ Build falló!"
        }
    }
}
```

---

*Continúa en la siguiente sección...*

