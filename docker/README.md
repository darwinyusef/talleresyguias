# Curso Completo: De Linux a Docker

Curso paso a paso para aprender Linux y Docker, desde fundamentos hasta arquitecturas avanzadas.

**📋 [Ver Índice Completo del Curso](./INDICE_COMPLETO.md)** - Navegación rápida por todo el contenido

---

## 📖 Índice del Curso

### Fundamentos

#### [Módulo Principal: Linux y Docker](./CURSO_LINUX_DOCKER.md)
1. **Módulo 1: Fundamentos de Linux**
   - Sistema de archivos
   - Comandos básicos
   - Permisos
   - Gestión de procesos
   - Networking básico

2. **Módulo 2: Linux Intermedio**
   - Variables de entorno
   - Gestión de paquetes
   - Shell scripting
   - Servicios y systemd

3. **Módulo 3: Introducción a Docker**
   - ¿Qué es Docker?
   - Instalación
   - Comandos básicos
   - Docker Hub

4. **Módulo 4: Dockerfile**
   - Anatomía de un Dockerfile
   - Construcción de imágenes
   - Mejores prácticas
   - Multi-stage builds

5. **Módulo 5: Docker Compose**
   - ¿Qué es Docker Compose?
   - Sintaxis YAML
   - Redes y volúmenes
   - Comandos esenciales

---

### Proyectos Prácticos

#### [Proyecto 1: Web Estática HTML](./proyectos/01-html-estatico.md)
Despliegue de sitio HTML con Nginx.

#### [Proyecto 2: Web con JavaScript](./proyectos/02-html-javascript.md)
Aplicación interactiva con HTML, CSS y JavaScript vanilla.

#### [Proyecto 3: API con FastAPI](./proyectos/03-fastapi.md)
API REST con Python y FastAPI.

#### [Proyecto 4: Frontend con React](./proyectos/04-react-frontend.md)
Aplicación React con Vite, optimización y builds.

#### [Proyecto 5: Backend con Node.js + TypeScript](./proyectos/05-node-typescript.md)
API REST con Express, TypeScript y PostgreSQL.

#### [Proyecto 6: Backend con Astro JS](./proyectos/06-astro-backend.md)
Backend/Fullstack con Astro y API endpoints.

#### [Proyecto 6B: Astro Full Stack Avanzado](./proyectos/06-astro-fullstack-avanzado.md)
Aplicación completa con Astro + Nginx + PostgreSQL + Prisma en Docker.

#### [Proyecto 7: Backend con Java Spring Boot](./proyectos/07-java-spring.md)
API REST empresarial con Spring Boot y Maven.

#### [Proyecto 8: Full Stack Completo](./proyectos/08-fullstack-completo.md)
Aplicación completa: React + Node + PostgreSQL + Redis + Nginx.

---

### Módulos Avanzados

#### [Módulo 6: CI/CD con GitHub Actions](./MODULO_CI_CD.md)
- ¿Qué es CI/CD?
- GitHub Actions
- Workflows
- Build y deploy automático
- Secretos y variables
- Despliegue a producción

#### [Módulo 7: Kubernetes](./MODULO_KUBERNETES.md)
- Arquitectura de Kubernetes
- Instalación (Minikube, Kind, K3s)
- Pods, Deployments, Services
- Networking e Ingress
- ConfigMaps y Secrets
- Auto-scaling
- Helm

#### [Módulo 8: Message Brokers](./MODULO_MESSAGE_BROKERS.md)
- **Redis**: Cache y Pub/Sub
- **RabbitMQ**: Message Queue
- **Apache Kafka**: Event Streaming
- Comparación y casos de uso
- Patrones de arquitectura

#### [Módulo 9: Seguridad en Docker](./MODULO_SEGURIDAD.md)
- Principios de seguridad
- Imágenes seguras
- Contenedores seguros
- Docker Secrets
- Scanning de vulnerabilidades
- Docker Bench Security
- Hardening del daemon

#### [Módulo 10: Paralelismo y Concurrencia](./MODULO_PARALELISMO_CONCURRENCIA.md)
- Conceptos: Concurrencia vs Paralelismo
- **Python**: Asyncio, Threading, Multiprocessing
- **Node.js**: Worker Threads, Cluster Module
- **Java**: Threads, ExecutorService, Parallel Streams
- **Go**: Goroutines y Channels
- Optimización de contenedores para paralelismo
- Patrones: Worker Pool, Fan-Out/Fan-In, Pipeline
- Benchmarking y profiling

#### [Módulo 11: Optimización de Imágenes](./MODULO_OPTIMIZACION.md)
- Análisis de imágenes con dive
- Técnicas de optimización
- Multi-stage builds avanzado
- Imágenes base ligeras (Alpine, Distroless, Scratch)
- BuildKit y cache optimization
- Optimización por lenguaje

#### [Módulo 12: Monitoreo y Logging](./MODULO_MONITOREO_LOGGING.md)
- **Prometheus + Grafana** - Métricas y visualización
- **ELK Stack** - Elasticsearch, Logstash, Kibana
- **Loki + Grafana** - Alternativa ligera
- **Jaeger** - Distributed tracing
- **cAdvisor** - Métricas de contenedores
- Instrumentación de aplicaciones

#### [Módulo 13: Arquitectura de Microservicios](./MODULO_MICROSERVICIOS.md)
- Diseño de microservicios
- Comunicación: REST, gRPC, Message Queue
- Service Discovery
- API Gateway (Nginx, Kong)
- Saga Pattern
- Circuit Breaker y Resilience
- Health Checks y Monitoring

#### [Módulo 14: Despliegue en Producción y Cloud](./MODULO_PRODUCCION_CLOUD.md)
- **SSL/HTTPS** con Let's Encrypt y Certbot
- Nginx y Traefik con certificados automáticos
- **AWS EC2** - Despliegue de aplicaciones Docker
- **Azure VMs** - Virtual Machines y Container Instances
- **Kubernetes en Cloud**: EKS (AWS), AKS (Azure), GKE (Google)
- Servicios externos: RDS, S3, Azure Blob Storage
- Configuración de dominios y DNS
- Secretos y variables de entorno en producción
- Health checks, logging y backups
- Monitoreo en producción

#### [Módulo 15: Terraform - Infrastructure as Code](./MODULO_TERRAFORM_IAC.md)
- ¿Qué es IaC?
- Instalación y configuración de Terraform
- **Providers**: AWS, Azure, Google Cloud
- Recursos, Variables y Outputs
- Terraform State y Remote Backend (S3)
- **Módulos** reutilizables
- Terraform con AWS (EC2, VPC, RDS)
- Terraform con Azure (Container Instances, ACR)
- Terraform con Kubernetes (EKS, AKS)
- Mejores prácticas y workflows

#### [Módulo 16: Ansible - Automatización de Configuración](./MODULO_ANSIBLE.md)
- ¿Qué es Ansible?
- Inventarios (estáticos y dinámicos)
- **Playbooks** y sintaxis YAML
- **Roles** reutilizables
- Instalación y configuración de Docker con Ansible
- Despliegue de aplicaciones Docker
- Docker Compose con Ansible
- **Ansible Vault** para secretos
- Handlers, loops y condiciones
- Integración con CI/CD (GitLab, GitHub Actions)

#### [Módulo 17: Arquitecturas Avanzadas](./MODULO_ARQUITECTURAS_AVANZADAS.md)
- **Service Mesh**: Istio y Linkerd
- Traffic management y Circuit Breakers
- Mutual TLS (mTLS) entre servicios
- Observability con Kiali, Grafana y Jaeger
- **Serverless**: AWS Lambda y Azure Functions
- Contenedores en Lambda (Docker)
- **CDN**: CloudFront (AWS), Azure Front Door
- **Multi-Region Deployment**
- Route 53 Failover y Latency-based routing
- Replicación de bases de datos cross-region

---

### Talleres Avanzados

#### [Taller: Agentes AI (LangChain)](./TALLER_AI_AGENTS.md)
- Agent simple con LangChain
- Multi-agent systems
- RAG con vector databases (ChromaDB)
- LangGraph state machines
- AutoGen multi-agent
- Memoria persistente con Redis

#### [Taller: WebSockets y gRPC](./TALLER_WEBSOCKETS_GRPC.md)
- **WebSockets** en múltiples contenedores
- Sincronización con Redis Pub/Sub
- Socket.IO adapter
- **gRPC** con Protocol Buffers
- Server streaming, client streaming, bidirectional
- Load balancing con Envoy
- Comparación REST vs gRPC vs WebSockets

#### [Taller: Event-Driven Architecture](./TALLER_EVENT_DRIVEN_WEBRTC.md)
- Event-Driven Architecture (EDA)
- Pub/Sub patterns con Redis y RabbitMQ
- **Event Sourcing** - Store events, not state
- **CQRS** - Command Query Responsibility Segregation
- **WebRTC** con Docker - Video/audio en tiempo real
- Signaling servers
- STUN/TURN configuration

#### [Taller: Aplicaciones CLI con Docker](./TALLER_CLI_APPS.md)
- **Python CLI**: Argparse, Click, Typer
- CLI con argumentos y subcomandos
- Rich terminal output con colores y tablas
- **Go CLI**: Cobra, Viper
- Gestión de configuración
- Containerización de CLIs
- Distribución con Docker

---

## 🎯 Cómo Usar Este Curso

### Para Principiantes
1. Empieza con el [Módulo Principal](./CURSO_LINUX_DOCKER.md) (Módulos 1-5)
2. Practica con [Proyecto 1](./proyectos/01-html-estatico.md) y [Proyecto 2](./proyectos/02-html-javascript.md)
3. Continúa con los proyectos según tu stack preferido

### Para Desarrolladores con Experiencia
1. Revisa conceptos en el [Módulo Principal](./CURSO_LINUX_DOCKER.md)
2. Ve directo a los proyectos de tu interés
3. Explora módulos avanzados (Kubernetes, CI/CD, Seguridad)

### Para DevOps/SRE
1. Repasa fundamentos si es necesario
2. Enfócate en [Kubernetes](./MODULO_KUBERNETES.md)
3. Estudia [CI/CD](./MODULO_CI_CD.md) y [Seguridad](./MODULO_SEGURIDAD.md)
4. Implementa [Message Brokers](./MODULO_MESSAGE_BROKERS.md)

---

## 🛠️ Tecnologías Cubiertas

### Lenguajes y Frameworks
- HTML/CSS/JavaScript
- Python (FastAPI, LangChain, AutoGen)
- Node.js + TypeScript (Express, Socket.IO)
- React (Vite)
- Astro JS
- Java (Spring Boot)
- Go (Goroutines)

### Bases de Datos
- PostgreSQL
- MongoDB
- Redis
- ChromaDB (Vector Database)
- Elasticsearch

### Message Brokers & Event Streaming
- RabbitMQ
- Apache Kafka
- Redis Pub/Sub

### Comunicación
- REST APIs
- WebSockets (Socket.IO)
- gRPC (Protocol Buffers)
- WebRTC (P2P)

### AI & Machine Learning
- LangChain
- LangGraph
- OpenAI API
- Vector Databases
- RAG (Retrieval Augmented Generation)

### Monitoring & Observability
- Prometheus
- Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Loki + Promtail
- Jaeger (Distributed Tracing)
- cAdvisor

### Orquestación & CI/CD
- Docker & Docker Compose
- Kubernetes (K8s)
- Helm
- GitHub Actions
- Nginx (Load Balancer, Reverse Proxy)
- Envoy Proxy

### Herramientas Adicionales
- Kong (API Gateway)
- Consul (Service Discovery)
- Coturn (TURN server)

### Plataformas Cloud
- **AWS**: EC2, EKS, RDS, S3, Secrets Manager
- **Azure**: VMs, AKS, Container Instances, Blob Storage
- **Google Cloud**: GKE
- Linux (Ubuntu, Debian, Alpine)
- Docker Hub / GHCR
- Minikube, Kind, K3s

### SSL/HTTPS
- Let's Encrypt
- Certbot
- Traefik con ACME
- Nginx con certificados SSL

---

## 📋 Prerrequisitos

### Software Necesario
- Docker Desktop o Docker Engine
- Git
- Editor de código (VS Code recomendado)
- Terminal (Bash, Zsh)

### Conocimientos
- Básicos de línea de comandos
- Conceptos de programación
- Opcional: experiencia con algún lenguaje de programación

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar o descargar este repositorio
cd ~/curso-docker

# 2. Verificar que Docker está instalado
docker --version
docker compose version

# 3. Empezar con el primer proyecto
cd proyectos/01-html-estatico

# 4. Crear tu primer contenedor
docker run hello-world
```

---

## 📁 Estructura del Repositorio

```
linuxdocker/
├── README.md                              # Este archivo (índice principal)
│
├── CURSO_LINUX_DOCKER.md                  # Módulos 1-5 (Fundamentos)
│   ├── Módulo 1: Fundamentos de Linux
│   ├── Módulo 2: Linux Intermedio
│   ├── Módulo 3: Introducción a Docker
│   ├── Módulo 4: Dockerfile
│   └── Módulo 5: Docker Compose
│
├── Módulos Avanzados
│   ├── MODULO_CI_CD.md                    # GitHub Actions
│   ├── MODULO_KUBERNETES.md               # Kubernetes y Helm
│   ├── MODULO_MESSAGE_BROKERS.md          # Kafka, RabbitMQ, Redis
│   ├── MODULO_SEGURIDAD.md                # Seguridad en Docker
│   ├── MODULO_PARALELISMO_CONCURRENCIA.md # Concurrency & Parallelism
│   ├── MODULO_OPTIMIZACION.md             # Optimización de imágenes
│   ├── MODULO_MONITOREO_LOGGING.md        # Prometheus, Grafana, ELK
│   ├── MODULO_MICROSERVICIOS.md           # Arquitectura de Microservicios
│   ├── MODULO_PRODUCCION_CLOUD.md         # Producción, SSL, AWS, Azure
│   ├── MODULO_TERRAFORM_IAC.md            # Infrastructure as Code
│   ├── MODULO_ANSIBLE.md                  # Automatización con Ansible
│   └── MODULO_ARQUITECTURAS_AVANZADAS.md  # Service Mesh, Serverless, CDN
│
├── Talleres Prácticos Avanzados
│   ├── TALLER_AI_AGENTS.md                # LangChain, RAG, Multi-Agent
│   ├── TALLER_WEBSOCKETS_GRPC.md          # WebSockets, gRPC
│   ├── TALLER_EVENT_DRIVEN_WEBRTC.md      # Event Sourcing, CQRS, WebRTC
│   └── TALLER_CLI_APPS.md                 # CLI Apps (Python, Go)
│
└── proyectos/                             # Proyectos paso a paso
    ├── 01-html-estatico.md                # Web estática con Nginx
    ├── 02-html-javascript.md              # Web con JavaScript
    ├── 03-fastapi.md                      # API con FastAPI (Python)
    ├── 04-react-frontend.md               # Frontend con React + Vite
    ├── 05-node-typescript.md              # Backend Node.js + TypeScript
    ├── 06-astro-backend.md                # Backend con Astro JS
    ├── 07-java-spring.md                  # Backend con Java Spring Boot
    └── 08-fullstack-completo.md           # Full Stack (React + Node + DB)
```

---

## 🎓 Objetivos de Aprendizaje

Al completar este curso, serás capaz de:

### Fundamentos
✅ Dominar comandos de Linux esenciales
✅ Crear y gestionar contenedores Docker
✅ Escribir Dockerfiles optimizados
✅ Usar Docker Compose para multi-contenedores
✅ Gestionar volúmenes y redes

### Desarrollo
✅ Desplegar aplicaciones full-stack (8 tipos de proyectos)
✅ Implementar paralelismo y concurrencia
✅ Optimizar imágenes Docker (reducir hasta 96% del tamaño)
✅ Aplicar mejores prácticas de seguridad

### Orquestación y Escalado
✅ Orquestar con Kubernetes (Pods, Services, Deployments)
✅ Usar Helm para package management
✅ Implementar auto-scaling
✅ Escalar aplicaciones horizontalmente

### CI/CD y Automatización
✅ Implementar CI/CD con GitHub Actions
✅ Automatizar builds y deployments
✅ Integrar testing en pipelines

### Comunicación
✅ Implementar REST APIs
✅ Usar WebSockets para real-time (múltiples contenedores)
✅ Implementar gRPC para microservicios
✅ Configurar WebRTC para P2P video/audio

### Message Brokers y Eventos
✅ Usar Kafka para event streaming
✅ Implementar RabbitMQ para task queues
✅ Usar Redis Pub/Sub
✅ Diseñar arquitecturas Event-Driven
✅ Implementar Event Sourcing y CQRS

### Microservicios
✅ Diseñar arquitecturas de microservicios
✅ Implementar Service Discovery
✅ Usar API Gateway (Nginx, Kong)
✅ Aplicar patrones Saga, Circuit Breaker

### AI y Machine Learning
✅ Containerizar agentes de IA (LangChain)
✅ Implementar multi-agent systems
✅ Usar RAG con vector databases
✅ Desplegar modelos de ML en contenedores

### Observabilidad
✅ Monitorear con Prometheus + Grafana
✅ Centralizar logs con ELK Stack o Loki
✅ Implementar distributed tracing con Jaeger
✅ Instrumentar aplicaciones para métricas

### Producción y Cloud
✅ Configurar SSL/HTTPS con Let's Encrypt
✅ Desplegar en AWS EC2 con Docker
✅ Usar Azure VMs y Container Instances
✅ Gestionar Kubernetes en la nube (EKS, AKS, GKE)
✅ Integrar servicios cloud (RDS, S3, Azure Storage)
✅ Configurar dominios y DNS
✅ Implementar backups y disaster recovery
✅ Gestionar secretos en producción

---

## 💡 Consejos para el Aprendizaje

1. **Practica con cada ejemplo** - No solo leas, ejecuta los comandos
2. **Modifica los ejemplos** - Experimenta y rompe cosas
3. **Construye proyectos propios** - Aplica lo aprendido a tus ideas
4. **Lee la documentación oficial** - Complementa con docs de Docker/K8s
5. **Únete a comunidades** - Discord, Reddit, Stack Overflow

---

## 🔗 Recursos Adicionales

### Documentación Oficial
- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

### Herramientas Útiles
- [Docker Hub](https://hub.docker.com/)
- [Play with Docker](https://labs.play-with-docker.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

### Comunidades
- [Docker Community](https://www.docker.com/community/)
- [r/docker](https://reddit.com/r/docker)
- [r/kubernetes](https://reddit.com/r/kubernetes)

---

## 🤝 Contribuir

Si encuentras errores o quieres sugerir mejoras:
1. Reporta issues
2. Sugiere cambios
3. Comparte tus proyectos

---

## 📜 Licencia

Este curso es de código abierto y está disponible para uso educativo.

---

## 🎉 ¡Comienza tu viaje!

Empieza con el [Módulo Principal](./CURSO_LINUX_DOCKER.md) y avanza a tu propio ritmo.

**¡Buena suerte y feliz aprendizaje!** 🚀

---

<div align="center">

**De Linux a Docker - Curso Completo**

[Fundamentos](./CURSO_LINUX_DOCKER.md) • [Proyectos](./proyectos/) • [Kubernetes](./MODULO_KUBERNETES.md) • [CI/CD](./MODULO_CI_CD.md)

</div>
