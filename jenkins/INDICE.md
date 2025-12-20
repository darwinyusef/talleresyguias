# 📑 Índice Completo - Taller Jenkins con Docker

Navegación rápida por todo el contenido del taller.

## 📚 Documentación Principal

- **[README.md](README.md)** - Guía completa del taller
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guía de inicio rápido
- **[.gitignore](.gitignore)** - Archivos ignorados por Git

---

## 🐳 Configuración Docker

### Archivos de Configuración
- **[docker/docker-compose.yml](docker/docker-compose.yml)** - Compose completo con Jenkins, SonarQube y Nexus
- **[docker/Dockerfile.jenkins](docker/Dockerfile.jenkins)** - Imagen personalizada de Jenkins
- **[docker/Dockerfile.agent](docker/Dockerfile.agent)** - Agente Jenkins personalizado

### Características
- ✅ Jenkins LTS con Docker CLI
- ✅ Docker-outside-of-Docker (DooD)
- ✅ Plugins preinstalados
- ✅ Node.js, Python, kubectl incluidos
- ✅ SonarQube para análisis de código
- ✅ Nexus para gestión de artifacts

---

## 📝 Pipelines de Ejemplo

### 1. Pipeline Básico
**Archivo**: [pipelines/01-basic-pipeline.jenkinsfile](pipelines/01-basic-pipeline.jenkinsfile)

**Contenido**:
- Stages simples
- Verificación de herramientas
- Post actions

**Nivel**: Principiante

---

### 2. Docker Build Pipeline
**Archivo**: [pipelines/02-docker-build.jenkinsfile](pipelines/02-docker-build.jenkinsfile)

**Contenido**:
- Construcción de imágenes Docker
- Escaneo de vulnerabilidades con Trivy
- Push a Docker Hub
- Deployment automático

**Nivel**: Intermedio

---

### 3. Node.js Application Pipeline
**Archivo**: [pipelines/03-nodejs-app.jenkinsfile](pipelines/03-nodejs-app.jenkinsfile)

**Contenido**:
- Build con agentes Docker
- Linting con ESLint
- Tests con Jest
- Security audit
- Docker multi-stage build
- Deployment parametrizado

**Nivel**: Intermedio-Avanzado

---

### 4. Parallel Stages Pipeline
**Archivo**: [pipelines/04-parallel-stages.jenkinsfile](pipelines/04-parallel-stages.jenkinsfile)

**Contenido**:
- Ejecución paralela de builds
- Tests paralelos (Unit, Integration, E2E)
- Múltiples Docker builds simultáneos
- Deployments paralelos

**Nivel**: Avanzado

---

### 5. Kubernetes Deployment Pipeline
**Archivo**: [pipelines/05-kubernetes-deploy.jenkinsfile](pipelines/05-kubernetes-deploy.jenkinsfile)

**Contenido**:
- Deployment a Kubernetes
- Manifiestos K8s (Deployment, Service, HPA, Ingress)
- Rolling updates
- Health checks
- Smoke tests

**Nivel**: Avanzado

---

## 🎯 Aplicaciones de Ejemplo

### Node.js REST API
**Directorio**: [ejemplos/nodejs-app/](ejemplos/nodejs-app/)

**Archivos**:
- `README.md` - Documentación
- `package.json` - Dependencias y scripts
- `src/index.js` - Aplicación Express
- `src/utils/logger.js` - Logger con Winston
- `tests/api.test.js` - Tests con Jest y Supertest
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Compose para desarrollo
- `Jenkinsfile` - Pipeline CI/CD completo
- `.eslintrc.json` - Configuración ESLint

**Características**:
- ✅ API REST completa (CRUD)
- ✅ Tests unitarios y de integración
- ✅ Linting y code quality
- ✅ Docker optimizado
- ✅ Health checks
- ✅ Logging estructurado
- ✅ Pipeline CI/CD completo

**Endpoints**:
- `GET /` - Info de la API
- `GET /health` - Health check
- `GET /api/users` - Lista usuarios
- `POST /api/users` - Crear usuario
- `GET /api/users/:id` - Obtener usuario
- `PUT /api/users/:id` - Actualizar usuario
- `DELETE /api/users/:id` - Eliminar usuario

---

## 🛠️ Scripts Útiles

### 1. Backup Jenkins
**Archivo**: [scripts/backup-jenkins.sh](scripts/backup-jenkins.sh)

**Uso**:
```bash
./scripts/backup-jenkins.sh [nombre-backup]
```

**Funcionalidad**:
- Crea backup del volumen jenkins_home
- Genera archivo de metadata
- Lista backups existentes

---

### 2. Restore Jenkins
**Archivo**: [scripts/restore-jenkins.sh](scripts/restore-jenkins.sh)

**Uso**:
```bash
./scripts/restore-jenkins.sh backups/jenkins-backup-YYYYMMDD.tar.gz
```

**Funcionalidad**:
- Restaura backup de Jenkins
- Crea backup de seguridad antes de restaurar
- Ajusta permisos automáticamente
- Reinicia Jenkins

---

### 3. Cleanup Old Builds
**Archivo**: [scripts/cleanup-old-builds.sh](scripts/cleanup-old-builds.sh)

**Uso**:
```bash
./scripts/cleanup-old-builds.sh [días]
```

**Funcionalidad**:
- Limpia builds antiguos
- Elimina workspaces no usados
- Limpia logs antiguos
- Limpia imágenes Docker
- Muestra espacio liberado

---

## 📖 Módulos del Taller

### Fundamentos

#### Módulo 1: Introducción a Jenkins
- ¿Qué es Jenkins?
- Arquitectura
- Instalación con Docker
- Configuración inicial

#### Módulo 2: Primeros Pasos
- Crear Jobs
- Tipos de Jobs
- Configuración
- Logs y resultados

#### Módulo 3: Jenkins con Docker
- DinD vs DooD
- Agentes Docker
- Build de imágenes
- Docker Compose

### Pipelines

#### Módulo 4: Introducción a Pipelines
- Declarative vs Scripted
- Sintaxis de Jenkinsfile
- Stages y Steps
- Variables y parámetros

#### Módulo 5: Pipelines Avanzados
- Parallel execution
- Conditional stages
- Post actions
- Shared libraries

### CI/CD

#### Módulo 6: CI/CD con Jenkins
- Integración con Git
- Webhooks
- Build automatizado
- Testing
- Code quality

#### Módulo 7: Deployment
- Deploy a Docker Hub
- Deploy a servidores
- Deploy a Kubernetes
- Blue-Green deployment
- Canary deployment

### Seguridad

#### Módulo 8: Seguridad
- Gestión de credenciales
- Secrets management
- Roles y permisos
- Plugins de seguridad

#### Módulo 9: Monitoreo
- Métricas de Jenkins
- Prometheus
- Optimización
- Cache y artifacts

---

## 🎓 Rutas de Aprendizaje

### Para Principiantes
1. Leer [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
2. Instalar Jenkins con Docker Compose
3. Probar [01-basic-pipeline.jenkinsfile](pipelines/01-basic-pipeline.jenkinsfile)
4. Explorar la interfaz de Jenkins
5. Crear primer Job Freestyle

### Para Desarrolladores
1. Revisar [02-docker-build.jenkinsfile](pipelines/02-docker-build.jenkinsfile)
2. Estudiar [03-nodejs-app.jenkinsfile](pipelines/03-nodejs-app.jenkinsfile)
3. Clonar y ejecutar [ejemplos/nodejs-app](ejemplos/nodejs-app/)
4. Crear pipeline para tu proyecto
5. Configurar webhooks con GitHub

### Para DevOps
1. Estudiar [04-parallel-stages.jenkinsfile](pipelines/04-parallel-stages.jenkinsfile)
2. Implementar [05-kubernetes-deploy.jenkinsfile](pipelines/05-kubernetes-deploy.jenkinsfile)
3. Configurar SonarQube y Nexus
4. Implementar shared libraries
5. Configurar monitoreo con Prometheus

---

## 🔗 Enlaces Rápidos

### Documentación
- [README Principal](README.md)
- [Inicio Rápido](INICIO_RAPIDO.md)

### Docker
- [Docker Compose](docker/docker-compose.yml)
- [Dockerfile Jenkins](docker/Dockerfile.jenkins)
- [Dockerfile Agent](docker/Dockerfile.agent)

### Pipelines
- [Pipeline Básico](pipelines/01-basic-pipeline.jenkinsfile)
- [Docker Build](pipelines/02-docker-build.jenkinsfile)
- [Node.js App](pipelines/03-nodejs-app.jenkinsfile)
- [Parallel Stages](pipelines/04-parallel-stages.jenkinsfile)
- [Kubernetes Deploy](pipelines/05-kubernetes-deploy.jenkinsfile)

### Ejemplos
- [Node.js App](ejemplos/nodejs-app/)

### Scripts
- [Backup](scripts/backup-jenkins.sh)
- [Restore](scripts/restore-jenkins.sh)
- [Cleanup](scripts/cleanup-old-builds.sh)

---

## 📊 Estadísticas del Taller

- **Archivos de configuración**: 3
- **Pipelines de ejemplo**: 5
- **Aplicaciones completas**: 1
- **Scripts útiles**: 3
- **Módulos de aprendizaje**: 9
- **Líneas de código**: ~3000+

---

## 💡 Próximos Pasos

1. ✅ Instalar Jenkins
2. ✅ Probar pipelines de ejemplo
3. ✅ Ejecutar aplicación Node.js
4. ⬜ Crear tu propio pipeline
5. ⬜ Integrar con tu repositorio
6. ⬜ Configurar deployment automático
7. ⬜ Implementar monitoreo

---

**¡Feliz aprendizaje! 🚀**

[Volver al README](README.md)
