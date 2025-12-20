# 🎯 Ejercicios Prácticos - Jenkins con Docker

Ejercicios hands-on para dominar Jenkins con Docker.

---

## 📚 Nivel 1: Fundamentos

### Ejercicio 1.1: Instalación y Configuración

**Objetivo**: Instalar Jenkins con Docker y configurarlo correctamente.

**Tareas**:
1. Instalar Jenkins usando Docker Compose
2. Configurar usuario administrador
3. Instalar plugins sugeridos
4. Verificar que Docker funciona dentro de Jenkins

**Verificación**:
```bash
# Jenkins está corriendo
docker ps | grep jenkins

# Docker funciona en Jenkins
docker exec jenkins docker ps

# Acceder a Jenkins
curl http://localhost:8080
```

**Criterios de éxito**:
- ✅ Jenkins accesible en http://localhost:8080
- ✅ Usuario admin creado
- ✅ Docker CLI funcional en Jenkins

---

### Ejercicio 1.2: Primer Pipeline

**Objetivo**: Crear tu primer pipeline declarativo.

**Tareas**:
1. Crear nuevo Pipeline Job
2. Escribir pipeline con 3 stages:
   - Checkout
   - Build
   - Test
3. Usar comandos shell en cada stage
4. Ejecutar el pipeline

**Template**:
```groovy
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                // Tu código aquí
            }
        }
        
        stage('Build') {
            steps {
                // Tu código aquí
            }
        }
        
        stage('Test') {
            steps {
                // Tu código aquí
            }
        }
    }
}
```

**Criterios de éxito**:
- ✅ Pipeline ejecuta sin errores
- ✅ Todos los stages completan
- ✅ Logs visibles en Console Output

---

### Ejercicio 1.3: Variables de Entorno

**Objetivo**: Usar variables de entorno en pipelines.

**Tareas**:
1. Crear pipeline con variables globales
2. Usar variables predefinidas de Jenkins
3. Crear variables específicas por stage
4. Imprimir todas las variables

**Pistas**:
```groovy
environment {
    APP_NAME = 'mi-app'
    VERSION = '1.0.0'
}
```

**Criterios de éxito**:
- ✅ Variables globales funcionan
- ✅ Variables de stage funcionan
- ✅ Variables predefinidas accesibles

---

## 📚 Nivel 2: Docker en Jenkins

### Ejercicio 2.1: Build de Imagen Docker

**Objetivo**: Construir una imagen Docker desde Jenkins.

**Tareas**:
1. Crear Dockerfile para aplicación simple
2. Crear pipeline que:
   - Construye la imagen
   - Tagea la imagen
   - Lista imágenes creadas
3. Verificar que la imagen funciona

**Dockerfile ejemplo**:
```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
```

**Criterios de éxito**:
- ✅ Imagen construida exitosamente
- ✅ Imagen tiene tag correcto
- ✅ Imagen puede ejecutarse

---

### Ejercicio 2.2: Agentes Docker

**Objetivo**: Usar agentes Docker para builds aislados.

**Tareas**:
1. Crear pipeline con agente Docker Node.js
2. Instalar dependencias npm
3. Ejecutar tests
4. Crear otro stage con agente Python
5. Ejecutar script Python

**Template**:
```groovy
pipeline {
    agent none
    
    stages {
        stage('Node Build') {
            agent {
                docker {
                    image 'node:18-alpine'
                }
            }
            steps {
                // Tu código aquí
            }
        }
        
        stage('Python Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                }
            }
            steps {
                // Tu código aquí
            }
        }
    }
}
```

**Criterios de éxito**:
- ✅ Agente Node.js funciona
- ✅ Agente Python funciona
- ✅ Builds aislados correctamente

---

### Ejercicio 2.3: Multi-Stage Build

**Objetivo**: Implementar Docker multi-stage build.

**Tareas**:
1. Crear Dockerfile multi-stage para app Node.js
2. Stage 1: Build (instalar deps, compilar)
3. Stage 2: Production (solo runtime)
4. Comparar tamaños de imagen

**Criterios de éxito**:
- ✅ Imagen final < 100MB
- ✅ Imagen funciona correctamente
- ✅ No contiene archivos de desarrollo

---

## 📚 Nivel 3: CI/CD Completo

### Ejercicio 3.1: Pipeline con Tests

**Objetivo**: Implementar pipeline con testing automatizado.

**Tareas**:
1. Crear aplicación Node.js simple
2. Escribir tests con Jest
3. Crear pipeline que:
   - Instala dependencias
   - Ejecuta linter
   - Ejecuta tests
   - Genera reporte de coverage
4. Publicar resultados de tests

**Criterios de éxito**:
- ✅ Tests ejecutan automáticamente
- ✅ Pipeline falla si tests fallan
- ✅ Reporte de coverage visible

---

### Ejercicio 3.2: Deployment Condicional

**Objetivo**: Deploy solo en rama main.

**Tareas**:
1. Crear pipeline con stage de deploy
2. Deploy solo ejecuta en rama main
3. Usar parámetros para controlar deploy
4. Implementar rollback en caso de fallo

**Template**:
```groovy
stage('Deploy') {
    when {
        branch 'main'
    }
    steps {
        // Tu código aquí
    }
}
```

**Criterios de éxito**:
- ✅ Deploy solo en main
- ✅ Parámetros funcionan
- ✅ Rollback implementado

---

### Ejercicio 3.3: Pipeline Parametrizado

**Objetivo**: Crear pipeline con múltiples parámetros.

**Tareas**:
1. Añadir parámetros:
   - ENVIRONMENT (choice: dev, staging, prod)
   - VERSION (string)
   - RUN_TESTS (boolean)
   - DEPLOY (boolean)
2. Usar parámetros en pipeline
3. Implementar lógica condicional

**Criterios de éxito**:
- ✅ Todos los parámetros funcionan
- ✅ Lógica condicional correcta
- ✅ Build parametrizado exitoso

---

## 📚 Nivel 4: Avanzado

### Ejercicio 4.1: Ejecución Paralela

**Objetivo**: Ejecutar stages en paralelo.

**Tareas**:
1. Crear pipeline con 3 builds paralelos:
   - Frontend (React)
   - Backend (Node.js)
   - Mobile (React Native)
2. Cada build en su propio agente Docker
3. Tests paralelos después de builds
4. Deploy solo si todos pasan

**Criterios de éxito**:
- ✅ Builds ejecutan en paralelo
- ✅ Tiempo total reducido
- ✅ Fallo en uno detiene deploy

---

### Ejercicio 4.2: Integration con SonarQube

**Objetivo**: Análisis de código con SonarQube.

**Tareas**:
1. Configurar SonarQube en docker-compose
2. Instalar plugin de SonarQube en Jenkins
3. Añadir stage de análisis de código
4. Configurar Quality Gates
5. Fallar build si no pasa Quality Gate

**Criterios de éxito**:
- ✅ SonarQube analiza código
- ✅ Resultados visibles en SonarQube
- ✅ Quality Gates funcionan

---

### Ejercicio 4.3: Deploy a Kubernetes

**Objetivo**: Desplegar aplicación a Kubernetes.

**Tareas**:
1. Crear manifiestos de Kubernetes:
   - Deployment
   - Service
   - Ingress
2. Crear pipeline que:
   - Construye imagen
   - Push a registry
   - Deploy a K8s
   - Verifica deployment
3. Implementar rolling update

**Criterios de éxito**:
- ✅ Deploy exitoso a K8s
- ✅ Rolling update funciona
- ✅ Zero downtime deployment

---

## 📚 Nivel 5: Experto

### Ejercicio 5.1: Shared Library

**Objetivo**: Crear shared library reutilizable.

**Tareas**:
1. Crear repositorio para shared library
2. Implementar funciones comunes:
   - buildDockerImage()
   - runTests()
   - deployToEnvironment()
3. Usar library en múltiples pipelines
4. Versionar library

**Criterios de éxito**:
- ✅ Library funciona en múltiples pipelines
- ✅ Código reutilizable
- ✅ Versionado correcto

---

### Ejercicio 5.2: Blue-Green Deployment

**Objetivo**: Implementar estrategia Blue-Green.

**Tareas**:
1. Crear 2 environments: blue y green
2. Deploy a environment inactivo
3. Ejecutar smoke tests
4. Switch de tráfico
5. Rollback automático si falla

**Criterios de éxito**:
- ✅ Zero downtime deployment
- ✅ Rollback automático funciona
- ✅ Switch de tráfico correcto

---

### Ejercicio 5.3: Pipeline Completo de Microservicios

**Objetivo**: CI/CD para arquitectura de microservicios.

**Tareas**:
1. Crear 3 microservicios:
   - API Gateway
   - User Service
   - Order Service
2. Pipeline que:
   - Detecta cambios por servicio
   - Build solo servicios modificados
   - Tests de integración
   - Deploy orquestado
3. Implementar service mesh (Istio)

**Criterios de éxito**:
- ✅ Build selectivo funciona
- ✅ Tests de integración pasan
- ✅ Deploy orquestado exitoso
- ✅ Service mesh configurado

---

## 🎯 Desafíos Adicionales

### Desafío 1: Pipeline Auto-Healing

**Objetivo**: Pipeline que se recupera de fallos.

**Requisitos**:
- Retry automático en fallos transitorios
- Notificaciones de fallos
- Rollback automático
- Logs detallados

---

### Desafío 2: Multi-Cloud Deployment

**Objetivo**: Deploy a múltiples clouds.

**Requisitos**:
- Deploy a AWS ECS
- Deploy a Azure Container Instances
- Deploy a GCP Cloud Run
- Health checks en todos

---

### Desafío 3: GitOps con Jenkins

**Objetivo**: Implementar GitOps workflow.

**Requisitos**:
- Manifiestos en Git
- Sync automático
- Drift detection
- Reconciliation automática

---

## 📊 Proyecto Final

### Aplicación Full Stack con CI/CD Completo

**Descripción**: Crear aplicación completa con pipeline de producción.

**Componentes**:
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL
- Cache: Redis
- Message Queue: RabbitMQ

**Pipeline debe incluir**:
1. ✅ Lint y format check
2. ✅ Unit tests (frontend y backend)
3. ✅ Integration tests
4. ✅ E2E tests con Cypress
5. ✅ Security scan (Trivy, npm audit)
6. ✅ Code quality (SonarQube)
7. ✅ Docker multi-stage builds
8. ✅ Push a registry
9. ✅ Deploy a Kubernetes
10. ✅ Smoke tests post-deploy
11. ✅ Rollback automático
12. ✅ Notificaciones (Slack/Email)
13. ✅ Métricas y monitoreo

**Criterios de éxito**:
- ✅ Pipeline completo funcional
- ✅ Zero downtime deployments
- ✅ Automated rollback
- ✅ < 10 minutos de build a producción
- ✅ 100% tests passing
- ✅ A+ en SonarQube
- ✅ Sin vulnerabilidades críticas

---

## 💡 Tips para los Ejercicios

### Debugging
```groovy
// Ver todas las variables
sh 'printenv'

// Debug de Docker
sh 'docker ps -a'
sh 'docker images'

// Ver workspace
sh 'ls -la'
sh 'pwd'
```

### Testing Pipelines
```groovy
// Dry run
sh 'echo "Would deploy to ${ENVIRONMENT}"'

// Validar antes de ejecutar
sh 'docker-compose config'
sh 'kubectl apply --dry-run=client -f manifests/'
```

### Mejores Prácticas
- Usa `try-catch` para manejo de errores
- Implementa `post` actions
- Limpia workspace con `cleanWs()`
- Usa credenciales de Jenkins, no hardcodees
- Versiona tus Jenkinsfiles en Git

---

## 🎓 Recursos para Aprender Más

### Documentación
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Docs](https://kubernetes.io/docs/)

### Cursos Recomendados
- Jenkins Fundamentals
- Docker Mastery
- Kubernetes for Developers
- CI/CD Best Practices

### Comunidad
- Jenkins Community Forums
- Stack Overflow - Jenkins tag
- Reddit r/jenkinsci
- Discord DevOps servers

---

**¡Buena suerte con los ejercicios! 🚀**

[Volver al README](README.md) | [Ver Índice](INDICE.md)
