# Plan Maestro de Diagramación Arquitectónica

## Versión 1.0 - Estrategia Completa de Visualización para 37 Archivos

---

## Índice
1. [Estrategia de Diagramación](#1-estrategia)
2. [Tipos de Diagramas y Cuándo Usarlos](#2-tipos-diagramas)
3. [Herramientas: Canvas vs Excalidraw](#3-herramientas)
4. [Índice de Diagramas por Archivo (1-37)](#4-indice-diagramas)
5. [Templates Base](#5-templates)
6. [Guía de Implementación](#6-implementacion)
7. [Convenciones y Estándares](#7-convenciones)
8. [Roadmap de Creación](#8-roadmap)

---

## 1. Estrategia de Diagramación

### Objetivo General

Crear una biblioteca visual completa que permita a los arquitectos:
- ✅ **Entender** conceptos arquitectónicos complejos de forma visual
- ✅ **Comparar** diferentes patrones y decisiones
- ✅ **Comunicar** arquitecturas a stakeholders técnicos y no técnicos
- ✅ **Decidir** entre opciones arquitectónicas con fundamento visual
- ✅ **Documentar** decisiones arquitectónicas de forma clara

### Principios de Diagramación

```markdown
1. **Claridad sobre Estética**
   - Diagramas fáciles de entender > Diagramas bonitos
   - Max 7±2 elementos por diagrama (límite cognitivo)
   - Usar colores con propósito, no decoración

2. **Consistencia**
   - Mismos íconos para mismos conceptos
   - Mismas formas para mismos tipos de componentes
   - Misma paleta de colores en toda la colección

3. **Contexto Múltiple**
   - Diagramas de alto nivel (C4 Context)
   - Diagramas de diseño (C4 Container, Component)
   - Diagramas de implementación (UML Deployment)
   - Diagramas de decisión (Decision Trees)

4. **Interactividad en Obsidian**
   - Canvas para relaciones y navegación
   - Excalidraw para diagramas técnicos detallados
   - Links entre diagramas y archivos markdown
```

### Estadísticas del Plan

```markdown
Total de Archivos: 37
Total de Diagramas Planificados: 185+
Diagramas por Archivo: ~5 promedio

Breakdown por Tipo:
- C4 (Context, Container, Component): 74 diagramas
- UML (Class, Sequence, State): 56 diagramas
- ArchiMate (Business, Application, Tech): 22 diagramas
- Flow/Decision Diagrams: 18 diagramas
- Architecture Patterns: 15 diagramas
```

---

## 2. Tipos de Diagramas y Cuándo Usarlos

### 2.1 C4 Model (Recomendado para Arquitectura de Software)

```markdown
# C4 MODEL - 4 Niveles de Abstracción

Level 1: SYSTEM CONTEXT
├─ Propósito: Mostrar el sistema en su contexto (usuarios, sistemas externos)
├─ Cuándo: Comunicar con stakeholders no técnicos, vista de negocio
├─ Elementos: Sistema (1), Usuarios (personas), Sistemas externos
├─ Herramienta: Canvas (alto nivel, relaciones)
└─ Ejemplo: "E-commerce Platform en contexto de clientes, payment gateway, shipping"

Level 2: CONTAINER
├─ Propósito: Mostrar contenedores (apps, databases, microservices)
├─ Cuándo: Comunicar arquitectura técnica a desarrolladores
├─ Elementos: Web App, API, Database, Message Queue
├─ Herramienta: Excalidraw (más detalle técnico)
└─ Ejemplo: "Frontend React, Backend FastAPI, PostgreSQL, Redis, Kafka"

Level 3: COMPONENT
├─ Propósito: Mostrar componentes dentro de un contenedor
├─ Cuándo: Diseñar estructura interna de servicios
├─ Elementos: Controllers, Services, Repositories, Domain Models
├─ Herramienta: Excalidraw (diagramas técnicos)
└─ Ejemplo: "UserController, UserService, UserRepository, User (domain)"

Level 4: CODE
├─ Propósito: Clases, interfaces (UML)
├─ Cuándo: Diseño detallado de implementación
├─ Elementos: Clases, métodos, relaciones
├─ Herramienta: Excalidraw (UML Class Diagram)
└─ Ejemplo: "Class User, IUserRepository, UserRepositoryPostgres"
```

**Cuándo usar C4:**
- ✅ Arquitecturas de microservices
- ✅ Explicar sistemas a nuevos team members
- ✅ Documentación de arquitectura moderna
- ✅ ADRs (Architecture Decision Records)

### 2.2 UML (Unified Modeling Language)

```markdown
# UML - Multiple Diagram Types

1. CLASS DIAGRAM (Estructura)
   ├─ Propósito: Relaciones entre clases (inheritance, composition, association)
   ├─ Cuándo: DDD (Domain-Driven Design), OOP design
   ├─ Herramienta: Excalidraw
   └─ Ejemplo: "Aggregate, Entity, Value Object relationships"

2. SEQUENCE DIAGRAM (Comportamiento)
   ├─ Propósito: Interacciones entre objetos en el tiempo
   ├─ Cuándo: Flujos complejos, sagas, distributed transactions
   ├─ Herramienta: Excalidraw (vertical timeline)
   └─ Ejemplo: "Order creation flow: API → OrderService → PaymentService → Kafka"

3. STATE DIAGRAM (Comportamiento)
   ├─ Propósito: Estados y transiciones de un objeto
   ├─ Cuándo: State machines, workflow engines
   ├─ Herramienta: Excalidraw
   └─ Ejemplo: "Order states: Created → Paid → Shipped → Delivered"

4. ACTIVITY DIAGRAM (Comportamiento)
   ├─ Propósito: Flujo de actividades (como flowchart)
   ├─ Cuándo: Procesos de negocio, algoritmos complejos
   ├─ Herramienta: Excalidraw
   └─ Ejemplo: "Checkout process with decision points"

5. DEPLOYMENT DIAGRAM (Físico)
   ├─ Propósito: Hardware, servidores, contenedores
   ├─ Cuándo: DevOps, infrastructure as code
   ├─ Herramienta: Excalidraw
   └─ Ejemplo: "EKS cluster with nodes, pods, load balancers"

6. COMPONENT DIAGRAM (Estructura)
   ├─ Propósito: Componentes y sus interfaces
   ├─ Cuándo: Arquitectura de componentes, plugins
   ├─ Herramienta: Excalidraw
   └─ Ejemplo: "Plugin architecture with extension points"
```

**Cuándo usar UML:**
- ✅ Domain-Driven Design (Class diagrams para aggregates)
- ✅ Sequence diagrams para sagas, distributed flows
- ✅ State machines para workflows
- ✅ Deployment para infraestructura

### 2.3 ArchiMate (Enterprise Architecture)

```markdown
# ARCHIMATE - Enterprise Architecture Framework

BUSINESS LAYER
├─ Elementos: Actor, Role, Business Process, Business Service
├─ Cuándo: TOGAF, enterprise architecture, business capabilities
├─ Herramienta: Canvas (alto nivel, relaciones de negocio)
└─ Ejemplo: "Customer, Order Management Process, E-commerce Service"

APPLICATION LAYER
├─ Elementos: Application Component, Data Object, Application Service
├─ Cuándo: Application portfolio, application landscapes
├─ Herramienta: Canvas
└─ Ejemplo: "CRM System, ERP System, Integration Hub"

TECHNOLOGY LAYER
├─ Elementos: Node, Device, System Software, Technology Service
├─ Cuándo: Infrastructure, cloud architecture
├─ Herramienta: Excalidraw
└─ Ejemplo: "AWS EKS, RDS, ElastiCache, S3"

MOTIVATION LAYER
├─ Elementos: Goal, Requirement, Principle, Constraint
├─ Cuándo: Architecture vision, ADRs, decision rationale
├─ Herramienta: Canvas (mind-map style)
└─ Ejemplo: "Business Goal → Requirements → Architecture Principles"
```

**Cuándo usar ArchiMate:**
- ✅ TOGAF ADM (Architecture Development Method)
- ✅ Enterprise architecture
- ✅ Relacionar negocio con tecnología
- ✅ Architecture governance

### 2.4 Flowcharts & Decision Trees

```markdown
# FLOWCHARTS - Process Flow

Propósito: Mostrar flujo de procesos con decisiones
Cuándo: Algoritmos, business processes, decision logic
Herramienta: Excalidraw
Elementos:
├─ Start/End (oval)
├─ Process (rectangle)
├─ Decision (diamond)
├─ Data (parallelogram)
└─ Flow (arrows)

Ejemplo: "Should I create an ADR?" decision tree
```

**Cuándo usar Flowcharts:**
- ✅ Decision trees (ej: "When to use microservices vs monolith")
- ✅ Algorithms
- ✅ Business process modeling (BPMN-lite)

### 2.5 Otros Diagramas Especializados

```markdown
1. ENTITY RELATIONSHIP DIAGRAM (ERD)
   ├─ Propósito: Database schema
   ├─ Cuándo: Database design, data modeling
   ├─ Herramienta: Excalidraw
   └─ Ejemplo: "Users, Orders, Products tables with foreign keys"

2. NETWORK DIAGRAM
   ├─ Propósito: Network topology
   ├─ Cuándo: Network architecture, security zones
   ├─ Herramienta: Excalidraw
   └─ Ejemplo: "VPC, subnets, security groups, NAT gateway"

3. EVENT STORMING
   ├─ Propósito: Domain events, commands, aggregates
   ├─ Cuándo: DDD, event-driven architecture
   ├─ Herramienta: Canvas (post-it note style)
   └─ Ejemplo: "OrderPlaced → PaymentProcessed → OrderShipped"

4. VALUE STREAM MAP
   ├─ Propósito: Flow of value through system
   ├─ Cuándo: DevOps, continuous delivery
   ├─ Herramienta: Canvas
   └─ Ejemplo: "Code → Build → Test → Deploy → Monitor"

5. MIND MAP
   ├─ Propósito: Brainstorming, concept relationships
   ├─ Cuándo: Learning, architecture exploration
   ├─ Herramienta: Canvas
   └─ Ejemplo: "Microservices Patterns: Circuit Breaker, Saga, CQRS..."
```

---

## 3. Herramientas: Canvas vs Excalidraw

### 3.1 Obsidian Canvas

**Fortalezas:**
- ✅ Excelente para **relaciones y navegación**
- ✅ Link directo a archivos markdown (double-click to open)
- ✅ Bueno para **alto nivel** y **contexto**
- ✅ Organizar conceptos en **mind maps**
- ✅ Crear **knowledge graphs**

**Usar Canvas para:**
- C4 Level 1 (System Context) - alto nivel
- ArchiMate Business/Application Layer
- Mind maps de patrones arquitectónicos
- Roadmaps y timelines
- Organizar colección de diagramas (meta-diagram)

**Formato Canvas:**
```json
{
  "nodes": [
    {
      "id": "unique-id",
      "type": "text|file|link|group",
      "text": "Content",
      "x": 0, "y": 0,
      "width": 300, "height": 200,
      "color": "1-6"  // Predefined colors
    }
  ],
  "edges": [
    {
      "id": "edge-id",
      "fromNode": "node-id-1",
      "toNode": "node-id-2",
      "label": "Relationship"
    }
  ]
}
```

### 3.2 Excalidraw

**Fortalezas:**
- ✅ **Diagramas técnicos detallados**
- ✅ Hand-drawn aesthetic (más humano, menos formal)
- ✅ Excelente para **UML, C4, flowcharts**
- ✅ Flechas, formas, text, iconos
- ✅ Colaboración (export/import)

**Usar Excalidraw para:**
- C4 Level 2-4 (Container, Component, Code)
- UML diagrams (Class, Sequence, State, Deployment)
- Flowcharts y decision trees
- Architecture patterns con detalle técnico
- ERD, network diagrams

**Formato Excalidraw:**
```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---

# Text Elements
Label 1 ^element-id-1
Label 2 ^element-id-2

%%
## Drawing
```compressed-json
[Compressed JSON data]
```
%%
```

### 3.3 Decisión: Canvas vs Excalidraw

```markdown
Pregunta: ¿Qué herramienta usar?

┌─ ¿Es alto nivel conceptual? (business, context)
│  └─ SÍ → Canvas
│
├─ ¿Necesitas links a archivos markdown?
│  └─ SÍ → Canvas
│
├─ ¿Es diagrama técnico detallado? (UML, C4 L2+)
│  └─ SÍ → Excalidraw
│
├─ ¿Necesitas flechas precisas y formas?
│  └─ SÍ → Excalidraw
│
└─ ¿Organizando conocimiento/roadmap?
   └─ SÍ → Canvas
```

---

## 4. Índice de Diagramas por Archivo (1-37)

### Archivo 01: Frontend Development (37KB)

**Diagramas a crear: 5**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 01-01 | Core Web Vitals Flow | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |
| 01-02 | Bundle Optimization Pipeline | C4 Container | Excalidraw | ⭐⭐⭐⭐⭐ |
| 01-03 | React Concurrent Rendering | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 01-04 | State Management Patterns | Component Diagram | Excalidraw | ⭐⭐⭐⭐ |
| 01-05 | Virtual Scrolling Architecture | Component Diagram | Excalidraw | ⭐⭐⭐⭐ |

**Descripción detallada:**

**01-01: Core Web Vitals Flow**
```
Propósito: Mostrar cómo se miden LCP, CLS, INP
Elementos:
- User action → Browser rendering → Metrics collection → Reporting
- Decision points: "Is LCP < 2.5s?" → Optimizations
Archivo relacionado: 01_FRONTEND_TEMAS_DIFICILES.md - Section 1
```

**01-02: Bundle Optimization Pipeline**
```
Propósito: Visualizar proceso de optimización de bundles
Elementos:
- Source code → Webpack/Vite → Tree shaking → Code splitting → Output
- Containers: Build tool, Bundle analyzer, CDN
Archivo relacionado: 01_FRONTEND_TEMAS_DIFICILES.md - Section 2
```

---

### Archivo 02: Backend Development (33KB)

**Diagramas a crear: 5**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 02-01 | Async/Await Event Loop | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 02-02 | Connection Pooling Architecture | Component Diagram | Excalidraw | ⭐⭐⭐⭐ |
| 02-03 | Rate Limiting Strategies | Flowchart | Excalidraw | ⭐⭐⭐⭐ |
| 02-04 | API Pagination Patterns | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐ |
| 02-05 | Error Handling Flow | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |

---

### Archivo 03: Database Engineering (15KB)

**Diagramas a crear: 6**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 03-01 | Query Execution Plan (EXPLAIN) | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |
| 03-02 | Index Types Comparison | Decision Tree | Excalidraw | ⭐⭐⭐⭐⭐ |
| 03-03 | Transaction Isolation Levels | State Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 03-04 | Replication Topologies | Network Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 03-05 | Zero-Downtime Migration | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 03-06 | Database Schema (ERD) | ERD | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 04: Machine Learning Engineering (22KB)

**Diagramas a crear: 5**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 04-01 | Distributed Training Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐⭐ |
| 04-02 | Model Serving Pipeline | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 04-03 | MLOps Workflow | Flowchart | Canvas | ⭐⭐⭐⭐ |
| 04-04 | Hyperparameter Tuning Flow | Flowchart | Excalidraw | ⭐⭐⭐⭐ |
| 04-05 | Model Monitoring Dashboard | Component Diagram | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 05: Data Analytics (22KB)

**Diagramas a crear: 4**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 05-01 | SQL Window Functions Execution | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 05-02 | Recursive CTE Visualization | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |
| 05-03 | Data Pipeline Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐ |
| 05-04 | A/B Testing Workflow | Flowchart | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 06: Agentic & GenAI Development (31KB)

**Diagramas a crear: 5**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 06-01 | Agent Architecture (ReAct) | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 06-02 | RAG Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐⭐ |
| 06-03 | Function Calling Flow | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 06-04 | Multi-Agent Collaboration | Component Diagram | Excalidraw | ⭐⭐⭐⭐ |
| 06-05 | Prompt Engineering Decision Tree | Decision Tree | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 07: Business Logic & Domain Modeling (35KB)

**Diagramas a crear: 6**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 07-01 | Aggregate Design (DDD) | UML Class Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 07-02 | Domain Events Flow | Event Storming | Canvas | ⭐⭐⭐⭐⭐ |
| 07-03 | Event Sourcing Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐⭐ |
| 07-04 | State Machine (Order) | State Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 07-05 | Specification Pattern | UML Class Diagram | Excalidraw | ⭐⭐⭐⭐ |
| 07-06 | Multi-Tenancy Architecture | Component Diagram | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 08: Mobile Development (34KB)

**Diagramas a crear: 4**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 08-01 | Offline-First Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐⭐ |
| 08-02 | Sync Strategy (Conflict Resolution) | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 08-03 | React Native Bridge | Component Diagram | Excalidraw | ⭐⭐⭐⭐ |
| 08-04 | Mobile Performance Optimization | Flowchart | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 09: Testing Avanzado (16KB)

**Diagramas a crear: 4**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 09-01 | Contract Testing (Pact) | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 09-02 | Chaos Engineering Workflow | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |
| 09-03 | Load Testing Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐ |
| 09-04 | Mutation Testing Process | Flowchart | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 10: DevOps, DevSecOps, AIOps (18KB)

**Diagramas a crear: 5**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 10-01 | GitOps Workflow (ArgoCD) | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 10-02 | IaC Pipeline (Terraform) | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |
| 10-03 | Container Security Scanning | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |
| 10-04 | OpenTelemetry Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐⭐ |
| 10-05 | AIOps Anomaly Detection | Flowchart | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 11: Arquitectura 2026 (17KB)

**Diagramas a crear: 5**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 11-01 | AI-First Architecture | C4 Context | Canvas | ⭐⭐⭐⭐⭐ |
| 11-02 | Platform Engineering Landscape | ArchiMate | Canvas | ⭐⭐⭐⭐⭐ |
| 11-03 | Zero Trust Security Model | Network Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 11-04 | Streaming-First Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐ |
| 11-05 | Edge Computing Topology | Network Diagram | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 12-17: Backend Avanzado (6 archivos)

**Diagramas a crear: 25 (promedio 4-5 por archivo)**

| Archivo | Diagramas Clave | Prioridad |
|---------|-----------------|-----------|
| 12 Backend Avanzado | gRPC Communication, Circuit Breaker, Multi-Level Cache, Message Queue | ⭐⭐⭐⭐⭐ |
| 13 Problemas Avanzados | Distributed Tracing, Idempotency, WebSocket, API Versioning | ⭐⭐⭐⭐⭐ |
| 14 Arq. Distribuida | GraphQL DataLoader, Sharding, Saga Pattern, 2PC | ⭐⭐⭐⭐⭐ |
| 15 Event-Driven | Event Sourcing, CQRS, Saga, Outbox Pattern | ⭐⭐⭐⭐⭐ |
| 16 Infraestructura | Kubernetes Architecture, Service Mesh, Istio | ⭐⭐⭐⭐⭐ |
| 17 Security & Perf | OAuth2 Flow, JWT, Rate Limiting, CDN Architecture | ⭐⭐⭐⭐⭐ |

---

### Archivo 18-22: Performance & Deployment (5 archivos)

**Diagramas a crear: 20**

| Archivo | Diagramas Clave | Prioridad |
|---------|-----------------|-----------|
| 18 Performance | Cache Hierarchy, Database Optimization, CDN Strategy | ⭐⭐⭐⭐⭐ |
| 19 Deployment | Blue-Green, Canary, Rolling Deployment | ⭐⭐⭐⭐⭐ |
| 20 Arq. Técnica 2026 | Modern Architecture Patterns, Cloud-Native | ⭐⭐⭐⭐⭐ |
| 21 Arq. Técnica P2 | Advanced Patterns, Multi-Cloud | ⭐⭐⭐⭐ |
| 22 Arq. Técnica P3 | Future Architecture Trends | ⭐⭐⭐⭐ |

---

### Archivo 23-25: DDD & Architecture Patterns (3 archivos)

**Diagramas a crear: 15**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 23-01 | Bounded Context Map | DDD Context Map | Canvas | ⭐⭐⭐⭐⭐ |
| 23-02 | Aggregate Lifecycle | State Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 24-01 | CQRS Architecture | C4 Container | Excalidraw | ⭐⭐⭐⭐⭐ |
| 24-02 | Hexagonal Architecture | Component Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 24-03 | Clean Architecture Layers | Component Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 25-01 | Strangler Pattern | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 25-02 | BFF Pattern | C4 Container | Excalidraw | ⭐⭐⭐⭐ |
| 25-03 | Temporal Workflows | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐ |

---

### Archivo 26-34: Modern Architecture Patterns (9 archivos)

**Diagramas a crear: 45**

| Archivo | Diagramas Clave | Cantidad | Prioridad |
|---------|-----------------|----------|-----------|
| 26 Modular Monolith | Module Boundaries, Internal Event Bus, Migration Path | 5 | ⭐⭐⭐⭐⭐ |
| 27 Serverless | Lambda Architecture, Event-Driven Serverless, Step Functions | 5 | ⭐⭐⭐⭐⭐ |
| 28 Event-Driven Avanz. | Event Store, Projections, Saga Patterns | 5 | ⭐⭐⭐⭐⭐ |
| 29 Reactive | Reactive Streams, Backpressure, Event Loop | 5 | ⭐⭐⭐⭐⭐ |
| 30 Security | Zero Trust, Defense in Depth, Secret Management | 5 | ⭐⭐⭐⭐⭐ |
| 31 API-First | API Gateway, GraphQL Federation, Versioning | 5 | ⭐⭐⭐⭐⭐ |
| 32 Resilience | Circuit Breaker, Bulkhead, Retry Patterns | 5 | ⭐⭐⭐⭐⭐ |
| 33 Data Architecture | Data Mesh, Data Lakehouse, CDC (Debezium) | 5 | ⭐⭐⭐⭐⭐ |
| 34 Space-Based | Processing Units, In-Memory Grid, Data Pumps | 5 | ⭐⭐⭐⭐⭐ |

---

### Archivo 35-37: ADR + TOGAF + Scrum (3 archivos)

**Diagramas a crear: 15**

| # | Nombre | Tipo | Herramienta | Prioridad |
|---|--------|------|-------------|-----------|
| 35-01 | ADR Lifecycle | State Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 35-02 | ADR Decision Tree | Decision Tree | Excalidraw | ⭐⭐⭐⭐⭐ |
| 36-01 | ADR+TOGAF+Scrum Integration | C4 Context | Canvas | ⭐⭐⭐⭐⭐ |
| 36-02 | Sprint Workflow with ADRs | Sequence Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 36-03 | Governance Framework | Component Diagram | Excalidraw | ⭐⭐⭐⭐⭐ |
| 36-04 | TOGAF ADM Agile Adaptation | ArchiMate | Canvas | ⭐⭐⭐⭐⭐ |
| 37-01 | E-commerce Migration Timeline | Gantt/Timeline | Canvas | ⭐⭐⭐⭐ |
| 37-02 | Architecture Board Review Process | Flowchart | Excalidraw | ⭐⭐⭐⭐⭐ |
| 37-03 | Metrics Dashboard Layout | Wireframe | Excalidraw | ⭐⭐⭐⭐ |
| 37-04 | Anti-patterns Comparison | Comparison Diagram | Canvas | ⭐⭐⭐⭐ |

---

## 5. Templates Base

### 5.1 Template Canvas: C4 System Context

```json
{
  "nodes": [
    {
      "id": "system-1",
      "type": "text",
      "text": "## 📦 System Name\n\n**Type:** Software System\n**Owner:** Team\n**Description:** What it does",
      "x": 0,
      "y": 0,
      "width": 400,
      "height": 300,
      "color": "3"
    },
    {
      "id": "user-1",
      "type": "text",
      "text": "## 👤 User/Actor\n\n**Type:** Person\n**Description:** Who uses it",
      "x": -600,
      "y": 0,
      "width": 300,
      "height": 200,
      "color": "1"
    },
    {
      "id": "external-1",
      "type": "text",
      "text": "## 🔌 External System\n\n**Type:** External System\n**Description:** What it provides",
      "x": 600,
      "y": 0,
      "width": 300,
      "height": 200,
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "fromNode": "user-1",
      "toNode": "system-1",
      "label": "Uses"
    },
    {
      "id": "edge-2",
      "fromNode": "system-1",
      "toNode": "external-1",
      "label": "Calls API"
    }
  ]
}
```

**Colores Canvas:**
- Color 1 (Rojo): Personas/Usuarios
- Color 2 (Naranja): Warnings/Problemas
- Color 3 (Amarillo): Sistema Principal
- Color 4 (Verde): Sistemas Externos
- Color 5 (Morado): Datos/Base de Datos
- Color 6 (Azul): Procesos/Workflows

### 5.2 Template Excalidraw: UML Class Diagram

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw, uml, class-diagram]
---

# Text Elements
ClassName ^class-name-1

+ publicMethod(): void ^method-1
- privateField: string ^field-1

%%
## Drawing
```compressed-json
[Diagram data - rectangles for classes, lines for relationships]
```
%%

# Leyenda UML:
- Rectángulo: Class
- Línea sólida con flecha vacía: Inheritance
- Línea sólida con flecha rellena: Composition
- Línea punteada: Dependency
- Línea sólida: Association
```

### 5.3 Template Excalidraw: Sequence Diagram

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw, uml, sequence-diagram]
---

# Text Elements
User ^actor-1
API Gateway ^system-1
Service ^system-2
Database ^system-3

1. Request ^message-1
2. Validate ^message-2
3. Query ^message-3
4. Return Data ^message-4
5. Response ^message-5

%%
## Drawing
```compressed-json
[Vertical lifelines, horizontal arrows for messages]
```
%%

# Sequence Diagram Elements:
- Lifeline: Vertical dashed line
- Activation: Thin rectangle on lifeline
- Message: Arrow with label
- Return: Dashed arrow
- Note: Rectangle with folded corner
```

### 5.4 Template Canvas: Mind Map

```json
{
  "nodes": [
    {
      "id": "central-concept",
      "type": "text",
      "text": "## 🎯 Central Concept\n\nMain topic",
      "x": 0,
      "y": 0,
      "width": 400,
      "height": 200,
      "color": "3"
    },
    {
      "id": "branch-1",
      "type": "text",
      "text": "### Branch 1\n\nSub-topic",
      "x": -600,
      "y": -300,
      "width": 300,
      "height": 150,
      "color": "1"
    },
    {
      "id": "branch-2",
      "type": "text",
      "text": "### Branch 2\n\nSub-topic",
      "x": -600,
      "y": 300,
      "width": 300,
      "height": 150,
      "color": "2"
    },
    {
      "id": "branch-3",
      "type": "text",
      "text": "### Branch 3\n\nSub-topic",
      "x": 600,
      "y": -300,
      "width": 300,
      "height": 150,
      "color": "4"
    },
    {
      "id": "branch-4",
      "type": "text",
      "text": "### Branch 4\n\nSub-topic",
      "x": 600,
      "y": 300,
      "width": 300,
      "height": 150,
      "color": "5"
    }
  ],
  "edges": [
    {"id": "e1", "fromNode": "central-concept", "toNode": "branch-1"},
    {"id": "e2", "fromNode": "central-concept", "toNode": "branch-2"},
    {"id": "e3", "fromNode": "central-concept", "toNode": "branch-3"},
    {"id": "e4", "fromNode": "central-concept", "toNode": "branch-4"}
  ]
}
```

---

## 6. Guía de Implementación

### Fase 1: Setup (Semana 1)

**Día 1-2: Preparar Estructura**
```bash
# En tu repositorio /hard/

# Crear directorio para diagramas
mkdir -p diagrams/{canvas,excalidraw}
mkdir -p diagrams/by-topic/{frontend,backend,database,ml,architecture}

# Estructura recomendada:
hard/
├── diagrams/
│   ├── canvas/
│   │   ├── 00_MASTER_DIAGRAM_INDEX.canvas
│   │   ├── c4-context/
│   │   ├── archimate/
│   │   └── mindmaps/
│   ├── excalidraw/
│   │   ├── c4-container/
│   │   ├── c4-component/
│   │   ├── uml/
│   │   ├── flowcharts/
│   │   └── patterns/
│   └── by-topic/
│       ├── frontend/
│       ├── backend/
│       ├── database/
│       └── architecture/
```

**Día 3-5: Crear Templates**
- Copiar templates base de esta guía
- Crear ejemplos de cada tipo de diagrama
- Documentar convenciones (colores, íconos, formas)

### Fase 2: Creación Prioritaria (Semanas 2-4)

**Prioridad 1: Arquitectura Core (10 diagramas)**
1. 36-01: ADR+TOGAF+Scrum Integration
2. 24-01: CQRS Architecture
3. 24-02: Hexagonal Architecture
4. 28-01: Event-Driven Architecture
5. 33-01: Data Mesh
6. 11-01: AI-First Architecture
7. 10-04: OpenTelemetry
8. 30-01: Zero Trust Security
9. 32-01: Circuit Breaker Pattern
10. 25-01: Strangler Pattern

**Prioridad 2: Patrones Fundamentales (15 diagramas)**
- C4 Diagrams para archivos 1-10
- UML Class Diagrams para DDD (archivo 7, 23)
- Sequence Diagrams para flows críticos

**Prioridad 3: Resto (160+ diagramas)**
- Completar 5 diagramas por archivo
- Priorizar por uso frecuente

### Fase 3: Organización y Enlaces (Semana 5)

**Crear Diagrama Maestro (Canvas)**
```
00_MASTER_DIAGRAM_INDEX.canvas

Estructura:
- Centro: Índice de 37 archivos
- Cada archivo → Link a sus diagramas
- Agrupado por categoría (Frontend, Backend, Architecture, etc.)
- Color-coded por prioridad
```

**Enlaces en Archivos Markdown**
```markdown
# En cada archivo .md, agregar sección:

## 📊 Diagramas Relacionados

### C4 Context
![C4 Context](diagrams/excalidraw/c4-context/01-frontend-context.excalidraw.md)

### Component Diagram
![Component](diagrams/excalidraw/c4-component/01-frontend-components.excalidraw.md)

### Flowchart
![Flow](diagrams/excalidraw/flowcharts/01-web-vitals-flow.excalidraw.md)
```

### Fase 4: Iteración y Mejora (Continuo)

**Revisar y Actualizar**
- Feedback de uso
- Mejorar claridad de diagramas
- Agregar nuevos diagramas según necesidad
- Mantener consistencia visual

---

## 7. Convenciones y Estándares

### 7.1 Naming Conventions

```markdown
# Archivos Canvas:
{number}-{topic}-{type}.canvas

Ejemplos:
- 01-frontend-context.canvas
- 24-cqrs-architecture.canvas
- 36-adr-togaf-sprint-workflow.canvas

# Archivos Excalidraw:
{number}-{topic}-{diagram-type}.excalidraw.md

Ejemplos:
- 01-frontend-web-vitals-flow.excalidraw.md
- 03-database-query-execution.excalidraw.md
- 07-ddd-aggregate-class-diagram.excalidraw.md
```

### 7.2 Convenciones Visuales

**Colores (Paleta Consistente):**
```markdown
# Canvas Colors:
- Color 1 (Rojo): Personas, Usuarios, Actores
- Color 2 (Naranja): Warnings, Problemas, Riesgos
- Color 3 (Amarillo): Sistema Principal, Core
- Color 4 (Verde): Sistemas Externos, Éxito
- Color 5 (Morado): Datos, Almacenamiento
- Color 6 (Azul): Procesos, Workflows, Lógica

# Excalidraw Colors:
- #FF6B6B: Crítico, Errores
- #4ECDC4: Éxito, Validación
- #45B7D1: Procesos, Flujos
- #FFA07A: Warnings
- #98D8C8: Datos
- #F7DC6F: Core System
```

**Formas (Significado Consistente):**
```markdown
# Rectángulo: Componente, Sistema, Clase
# Rectángulo redondeado: Proceso, Servicio
# Cilindro: Base de datos, Almacenamiento
# Nube: Servicio cloud, External system
# Persona (stickman): Usuario, Actor
# Diamante: Decisión, Gateway
# Óvalo: Inicio/Fin de proceso
# Hexágono: Integration point
```

**Flechas (Tipos de Relaciones):**
```markdown
# Flecha sólida →: Flujo de datos, Llamada
# Flecha punteada ⇢: Dependencia, Referencia
# Flecha doble ↔: Comunicación bidireccional
# Flecha con etiqueta: Tipo de relación específica
```

### 7.3 Metadata en Diagramas

**Canvas:**
```json
{
  "nodes": [
    {
      "id": "metadata",
      "type": "text",
      "text": "## 📋 Metadata\n\n**Archivo:** 01_FRONTEND\n**Versión:** 1.0\n**Fecha:** 2025-12-27\n**Autor:** Architecture Team\n**Relacionado:** [[01_FRONTEND_TEMAS_DIFICILES]]",
      "x": -1000,
      "y": -500,
      "width": 300,
      "height": 200,
      "color": "6"
    }
  ]
}
```

**Excalidraw:**
```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw, frontend, c4, web-vitals]
archivo: 01_FRONTEND_TEMAS_DIFICILES
version: 1.0
date: 2025-12-27
---

# Diagram: Core Web Vitals Flow
# Purpose: Show how LCP, CLS, INP are measured
# Level: Flowchart
# Related: [[01_FRONTEND_TEMAS_DIFICILES#Core Web Vitals]]
```

---

## 8. Roadmap de Creación

### Meta: 185+ Diagramas en 12 Semanas

```markdown
# ROADMAP DE CREACIÓN

## Semana 1: Setup & Templates (0 → 10)
- [ ] Estructura de directorios
- [ ] Templates base (Canvas, Excalidraw)
- [ ] Convenciones documentadas
- [ ] Diagrama maestro inicial
- [ ] 10 diagramas de ejemplo

## Semana 2-3: Arquitectura Core (10 → 30)
- [ ] ADR + TOGAF + Scrum (5 diagramas)
- [ ] CQRS, Hexagonal, Clean (5 diagramas)
- [ ] Event-Driven, Microservices (5 diagramas)
- [ ] Data Architecture (5 diagramas)

## Semana 4-5: Patrones Fundamentales (30 → 60)
- [ ] DDD Patterns (6 diagramas)
- [ ] Reactive, Resilience (6 diagramas)
- [ ] Security, API-First (6 diagramas)
- [ ] GenAI, Agentic (6 diagramas)
- [ ] Frontend, Backend basics (6 diagramas)

## Semana 6-7: Database & Data (60 → 90)
- [ ] Database patterns (6 diagramas)
- [ ] Data pipelines (6 diagramas)
- [ ] ML Engineering (5 diagramas)
- [ ] Data Analytics (5 diagramas)
- [ ] ETL/ELT flows (8 diagramas)

## Semana 8-9: DevOps & Infrastructure (90 → 120)
- [ ] GitOps, IaC (6 diagramas)
- [ ] Container orchestration (6 diagramas)
- [ ] Observability (6 diagramas)
- [ ] Security scanning (6 diagramas)
- [ ] Deployment patterns (6 diagramas)

## Semana 10-11: Advanced Topics (120 → 160)
- [ ] Mobile architecture (5 diagramas)
- [ ] Testing strategies (5 diagramas)
- [ ] Performance optimization (10 diagramas)
- [ ] Advanced backend (10 diagramas)
- [ ] Business logic patterns (10 diagramas)

## Semana 12: Completar & Revisar (160 → 185+)
- [ ] Diagramas faltantes (25+)
- [ ] Revisión de consistencia
- [ ] Enlaces entre diagramas
- [ ] Documentación final
- [ ] Índice maestro completo
```

### Velocity Target

```markdown
Semanas 1-3: 10 diagramas/semana (setup + learning)
Semanas 4-9: 15 diagramas/semana (productive phase)
Semanas 10-12: 13 diagramas/semana (completion)

Total: 185 diagramas en 12 semanas
Promedio: 15.4 diagramas/semana
```

---

## 9. Quick Start Guide

### Crear tu Primer Diagrama (5 minutos)

**Opción A: Canvas (C4 Context)**

1. En Obsidian: `Cmd+P` → "Canvas: Create new canvas"
2. Nombrar: `01-frontend-context.canvas`
3. Drag & drop: Crear 3 nodos (User, System, External)
4. Click derecho en nodo → Change color
5. Conectar con edges (arrastra entre nodos)
6. Guardar en `diagrams/canvas/c4-context/`

**Opción B: Excalidraw (Flowchart)**

1. En Obsidian: `Cmd+P` → "Excalidraw: Create new drawing"
2. Nombrar: `01-frontend-web-vitals-flow.excalidraw.md`
3. Dibujar:
   - Rectángulo para procesos
   - Diamante para decisiones
   - Óvalo para inicio/fin
   - Flechas para flujo
4. Agregar texto con doble-click
5. Guardar en `diagrams/excalidraw/flowcharts/`

### Link Diagrama en Markdown

```markdown
# En 01_FRONTEND_TEMAS_DIFICILES.md

## Core Web Vitals

[Descripción del concepto...]

### 📊 Diagrama
![[01-frontend-web-vitals-flow.excalidraw]]

El diagrama muestra el flujo completo de medición de Core Web Vitals.
```

---

## 10. Checklist por Diagrama

Antes de considerar un diagrama "completo":

```markdown
- [ ] Título claro y descriptivo
- [ ] Metadata (archivo relacionado, versión, fecha)
- [ ] Leyenda si usa símbolos no estándar
- [ ] Colores consistentes con convenciones
- [ ] Max 7±2 elementos principales (claridad cognitiva)
- [ ] Flechas etiquetadas con tipo de relación
- [ ] Linked desde archivo markdown correspondiente
- [ ] Guardado en directorio correcto
- [ ] Tags apropiados (para búsqueda)
- [ ] Revisado por otra persona (peer review)
```

---

## Resumen Ejecutivo

**Plan de Diagramación:**
- **185+ diagramas** para 37 archivos
- **12 semanas** de ejecución
- **2 herramientas**: Canvas (alto nivel), Excalidraw (detalle técnico)
- **7 tipos**: C4, UML, ArchiMate, Flowcharts, ERD, Network, Decision Trees
- **Prioridad**: Arquitectura core primero, luego patrones, luego específicos

**Beneficios:**
- ✅ Aprendizaje visual de conceptos complejos
- ✅ Documentación arquitectónica completa
- ✅ Comunicación efectiva con stakeholders
- ✅ Toma de decisiones fundamentada
- ✅ Onboarding más rápido de nuevos miembros

**Next Steps:**
1. Crear estructura de directorios
2. Copiar templates base
3. Crear primeros 10 diagramas prioritarios
4. Iterar y expandir según roadmap

---

**¿Listo para empezar? →** [[#6-implementacion|Guía de Implementación]]
