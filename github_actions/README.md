# Taller Completo: GitHub Actions con Docker

Guía exhaustiva para dominar la automatización de flujos de trabajo (CI/CD) utilizando GitHub Actions y contenedores Docker.

**📋 [Ver Índice Completo del Taller](./INDICE.md)** - Navegación rápida por todo el contenido

---

## 📖 Índice del Taller

### Fundamentos

#### 1. [Introducción a GitHub Actions](#introducción-a-github-actions)
- ¿Qué es GitHub Actions?
- Conceptos clave: Workflow, Event, Job, Step, Action, Runner.
- Estructura de un archivo YAML.
- Componentes del Marketplace.

#### 2. [GitHub Actions y Docker](#github-actions-y-docker)
- Uso de Docker en Runners.
- Actions oficiales de Docker (`docker/setup-buildx-action`, `docker/login-action`, etc.).
- Construcción de imágenes en el CI.
- Mejores prácticas de seguridad (Secrets).

#### 3. [Configuración de Entorno](#configuración-de-entorno)
- Secrets y Variables de entorno en GitHub.
- Configuración de un Registry (Docker Hub, GHCR).
- Runners: GitHub-hosted vs Self-hosted.

### Pipelines (Workflows)

#### 4. [Construcción de Flujos de Trabajo](#construcción-de-flujos-de-trabajo)
- Sintaxis avanzada: `strategy/matrix`, `conditional (if)`, `env`, `outputs`.
- Reutilización de Workflows (`workflow_call`).
- Cache de dependencias y capas de Docker.

#### 5. [Integración Continua (CI)](#integración-continua-ci)
- Automatización de Tests (Unit, Integration).
- Linting y formateo de código.
- Análisis estático de seguridad (SAST).
- Generación de artefactos.

#### 6. [Despliegue Continuo (CD)](#despliegue-continuo-cd)
- Estrategias de despliegue: SSH, Docker Compose remoto, Kubernetes.
- Ambientes (Environments) y aprobaciones manuales.
- Rollbacks automáticos.

#### 7. [Orquestación con Kubernetes](./kubernetes/)
- Estructura de manifiestos (Deployment, Service, Namespace).
- GitOps con `kubectl` desde GitHub Actions.
- Gestión de Secretos en el clúster.

### Proyectos Prácticos

#### [Proyecto 1: Pipeline para App Node.js](./ejemplos/nodejs-app/)
- Automatización completa de una aplicación Express.
- Docker multi-stage build y push a GHCR.

#### [Proyecto 2: Python FastAPI](./ejemplos/python-fastapi/)
- API moderna con validación Pydantic y tests con Pytest.

#### [Proyecto 3: Machine Learning & Scikit-learn](./ejemplos/ml-sklearn/)
- Entrenamiento automatizado y versionado de modelos.

#### [Proyecto 4: Deep Learning & TensorFlow](./ejemplos/dl-tensorflow/)
- Integración de redes neuronales en contenedores.

#### [Proyecto 5: Go Fiber](./ejemplos/go-fiber/)
- API de alto rendimiento con binarios estáticos optimizados.

#### 8. [Integración con Proyectos Externos](./github/)
- Reutilización de Workflows (`workflow_call`).
- Creación de **Composite Actions** personalizadas.
- Clonación de múltiples repositorios en un mismo Runner.

---

## 🎯 Objetivos de Aprendizaje

Al completar este taller, serás capaz de:

### Fundamentos
✅ Entender la arquitectura de GitHub Actions.
✅ Crear Workflows desde cero.
✅ Gestionar secretos de forma segura.

### Automatización con Docker
✅ Construir y optimizar imágenes Docker en flujos de CI.
✅ Publicar imágenes en GitHub Container Registry (GHCR) y Docker Hub.
✅ Usar servicios de Docker dentro de los flujos de prueba (databases, redis).

### CI/CD Avanzado
✅ Implementar estrategias de despliegue automatizado.
✅ Optimizar tiempos de ejecución mediante cache.
✅ Validar la calidad del código mediante jobs paralelos.

---

## 🚀 Inicio Rápido

1. Crea una carpeta `.github/workflows/` en la raíz de tu proyecto.
2. Crea un archivo `ci.yml`:

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker Image
        run: docker build . -t my-app:latest
```

3. Sube los cambios a GitHub y observa la pestaña **Actions**.

---

## 📁 Estructura del Repositorio

```
github_actions/
├── README.md                          # Este archivo (índice principal)
├── INDICE.md                          # Navegación detallada
├── INICIO_RAPIDO.md                   # Guía rápida
├── EJERCICIOS.md                      # Prácticas por niveles
├── docker/                            # Configuraciones Docker de ejemplo
│   ├── Dockerfile                     # Ejemplo de multi-stage
│   └── docker-compose.yml             # Despliegue con Compose
├── pipeline/                          # Ejemplos de workflows (.yml)
│   ├── basic-ci.yml                   # CI básico
│   ├── docker-publish.yml             # Build & Push
│   ├── deploy-ssh.yml                 # Deploy mediante SSH
│   ├── multi-language-ci.yml          # CI para Monorepos (Python, Go, ML)
│   ├── k8s-deploy.yml                 # Deploy a Kubernetes
│   ├── security-scan.yml              # Escaneo de seguridad (Trivy/Hadolint)
│   ├── scripted-python-ci.yml         # CI usando scripts .sh
│   └── tag-and-release.yml            # Automatización de Releases
├── scripts/                            # Scripts Bash útiles
│   ├── docker-check.sh                # Verificador de entorno
│   ├── docker-cleanup.sh              # Limpieza automática
│   └── setup-python-env.sh            # Setup y tests de Python
├── kubernetes/                        # Manifiestos de K8s para todos los ejemplos
│   ├── base/                          # Namespace y configs globales
│   ├── nodejs-app/                    # K8s config para Node.js
│   ├── python-fastapi/                # K8s config para FastAPI
│   └── ...                            # (Demás servicios)
└── ejemplos/                          # Aplicaciones de demostración
    ├── nodejs-app/                    # App Node.js
    ├── python-fastapi/                # API con FastAPI
    ├── ml-sklearn/                    # ML con Scikit-learn
    ├── dl-tensorflow/                 # DL con TensorFlow
    └── go-fiber/                      # API con Go Fiber
```

---

## 🛠️ Tecnologías Cubiertas

- **GitHub Actions**: Core de automatización.
- **Docker**: Containerización.
- **Node.js / Python / Go**: Ejemplos de ejecución.
- **GHCR / Docker Hub**: Almacenamiento de imágenes.
- **Trivy / Hadolint**: Seguridad y calidad de Docker.

---

## 📋 Prerrequisitos

- Cuenta en GitHub.
- Conocimientos básicos de Docker y Git.
- (Opcional) Cuenta en Docker Hub para pruebas de publicación.

---

## 🔗 Recursos Adicionales

- [Documentación oficial de GitHub Actions](https://docs.github.com/en/actions)
- [Docker GitHub Actions](https://github.com/marketplace?type=actions&query=docker)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

<div align="center">

**Dominando GitHub Actions y Docker**

[Fundamentos](#) • [Escalamiento](#) • [CI/CD](#) • [Proyectos](#)

</div>
