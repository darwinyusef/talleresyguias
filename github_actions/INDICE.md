# 📑 Índice Completo - Taller GitHub Actions + Docker

Navegación detallada por todos los recursos y módulos del taller.

---

## 📚 Documentación General
- **[README.md](./README.md)**: Guía maestra y conceptos teóricos.
- **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)**: Configuración en menos de 5 minutos.
- **[EJERCICIOS.md](./EJERCICIOS.md)**: Listado de ejercicios prácticos divididos por niveles.
- **[ESTRUCTURA.md](./ESTRUCTURA.md)**: Diagrama de carpetas y archivos.

---

## 🛠️ Módulos Técnicos

### Módulo 1: Fundamentos de GitHub Actions
- Estructura del Runner (Ubuntu, Windows, Mac).
- Sintaxis del Workflow YAML.
- Disparadores (Triggers): `push`, `pull_request`, `workflow_dispatch`, `schedule`.

### Módulo 2: Flujos con Docker
- **Configuración (`docker/`)**:
  - [Dockerfile de ejemplo](./docker/Dockerfile)
  - [Docker Compose de despliegue](./docker/docker-compose.yml)
- **Actions oficiales**:
  - `docker/login-action`: Autenticación.
  - `docker/setup-buildx-action`: Soporte multi-arch y cache.
  - `docker/build-push-action`: El estándar para construir y subir.

### Módulo 3: Optimización y Seguridad
- Gestión de Secretos (`secrets.DOCKER_PASSWORD`).
- Variables de repositorio y ambiente.
- Estrategias de Cache para Docker Layers.
- Escaneo de vulnerabilidades con **Trivy**.

### Módulo 4: Orquestación con Kubernetes
- **Manifiestos (`kubernetes/`)**:
  - Namespace y aislamiento.
  - Deployments y Service Discovery.
  - Gestión de replicas y escalabilidad.
- **GitOps**:
  - Uso de `azure/k8s-set-context` para conexión.
  - Aplicación de cambios automáticos en el clúster.

### Módulo 5: Automatización con Scripts (.sh)
- **Utilidades (`scripts/`)**:
  - `docker-check.sh`: Verificación de salud del entorno.
  - `docker-cleanup.sh`: Mantenimiento y limpieza de recursos.
  - `setup-python-env.sh`: Orquestación de dependencias y tests.
- **Ventajas**: Portabilidad, facilidad de testeo local y limpieza del YAML.

### Módulo 6: Reutilización y Proyectos Externos (`github/`)
- **Workflows Reutilizables**: Plantillas para múltiples proyectos.
- **Composite Actions**: Empaquetado de pasos lógicos complejos.
- **Multi-Repo Management**: Clonación y validación de dependencias externas.

---

## 📝 Ejemplos de Pipelines (`pipeline/`)

1. **[CI Básico](./pipeline/basic-ci.yml)**: Instalación, Test y Build local.
2. **[Build & Push a GHCR](./pipeline/docker-publish.yml)**: Integración nativa con GitHub Container Registry.
3. **[Deploy SSH](./pipeline/deploy-ssh.yml)**: Despliegue automático a servidor remoto vía Docker Compose.
4. **[Multi-Environment](./pipeline/multi-env.yml)**: Manejo de Dev, Staging y Prod con aprobaciones.

---

## 🎯 Proyectos Prácticos (`ejemplos/`)

### 1. [Node.js REST API](./ejemplos/nodejs-app/)
- **Descripción**: Una API Express con tests de integración.
- **Workflow**: CI + Build Docker + Push a GHCR.
- **Docker**: Imagen optimizada multi-stage.

### 2. [Python FastAPI](./ejemplos/python-fastapi/)
- **Descripción**: API REST moderna y rápida.
- **Workflow**: CI con linting y tests unitarios.

### 3. [Machine Learning (Scikit-learn)](./ejemplos/ml-sklearn/)
- **Descripción**: Entrenamiento automático de un modelo Iris.
- **Workflow**: Pipeline que entrena y valida la precisión.

### 4. [Deep Learning (TensorFlow)](./ejemplos/dl-tensorflow/)
- **Descripción**: Red neuronal simple con contenedores optimizados.
- **Workflow**: CI para modelos pesados con cache.

### 5. [Go Fiber](./ejemplos/go-fiber/)
- **Descripción**: Framework web en Go de alto rendimiento.
- **Workflow**: Multi-stage build optimizado para binarios estáticos.

---

## 🚀 Prácticas Recomendadas
- Uso de versiones fijas para las Actions (`v4` vs `v4.1.0`).
- Limitación de permisos de los tokens (`permissions: contents: read`).
- Evitar el uso de `latest` en imágenes de producción.

---

[Ir al README Principal](./README.md) • [Ver Guía Rápida](./INICIO_RAPIDO.md)
