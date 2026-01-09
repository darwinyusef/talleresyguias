# Roadmap Incremental de Diagramas Arquitectónicos

## Versión 1.0 - Enfoque Pequeño y Comprensible

---

## Filosofía: Menos es Más

**Principios:**
- ✅ Diagramas pequeños (3-7 elementos)
- ✅ Un concepto por diagrama
- ✅ Fácil de entender en 30 segundos
- ✅ Enfoque incremental: crear lo más usado primero
- ✅ Estilo hand-drawn (Excalidraw) para mejor comprensión

---

## Top 20 Arquitecturas Más Reconocidas (Orden de Creación)

### Fase 1: Arquitecturas Fundamentales (Semana 1)

**1. Hexagonal Architecture (Ports & Adapters)** ⭐⭐⭐⭐⭐
- Diagrama: Hexágono central + Adapters
- Archivo: `01-hexagonal-architecture.excalidraw.md`
- Conceptos: Domain, Ports, Adapters
- Complejidad: Simple (5 elementos)

**2. Clean Architecture (Onion/Layered)** ⭐⭐⭐⭐⭐
- Diagrama: Círculos concéntricos (4 layers)
- Archivo: `02-clean-architecture.excalidraw.md`
- Conceptos: Entities, Use Cases, Interface Adapters, Frameworks
- Complejidad: Simple (4 layers)

**3. CQRS (Command Query Responsibility Segregation)** ⭐⭐⭐⭐⭐
- Diagrama: Split entre Commands y Queries
- Archivo: `03-cqrs-pattern.excalidraw.md`
- Conceptos: Write Model, Read Model, Commands, Queries
- Complejidad: Simple (6 elementos)

**4. Event Sourcing** ⭐⭐⭐⭐⭐
- Diagrama: Event Store + Projections
- Archivo: `04-event-sourcing.excalidraw.md`
- Conceptos: Events, Event Store, Snapshots, Projections
- Complejidad: Media (7 elementos)

**5. Microservices Architecture** ⭐⭐⭐⭐⭐
- Diagrama: Services + API Gateway + Message Bus
- Archivo: `05-microservices-basic.excalidraw.md`
- Conceptos: Services, API Gateway, Database per Service, Async Communication
- Complejidad: Media (7 elementos)

---

### Fase 2: Patrones Modernos (Semana 2)

**6. Serverless Architecture** ⭐⭐⭐⭐⭐
- Diagrama: Lambda + API Gateway + DynamoDB
- Archivo: `06-serverless-pattern.excalidraw.md`
- Conceptos: Functions, Events, Managed Services
- Complejidad: Simple (5 elementos)

**7. Event-Driven Architecture** ⭐⭐⭐⭐⭐
- Diagrama: Producers → Event Bus → Consumers
- Archivo: `07-event-driven.excalidraw.md`
- Conceptos: Events, Event Bus, Publishers, Subscribers
- Complejidad: Simple (5 elementos)

**8. API Gateway Pattern** ⭐⭐⭐⭐⭐
- Diagrama: Clients → Gateway → Microservices
- Archivo: `08-api-gateway.excalidraw.md`
- Conceptos: Gateway, Routing, Rate Limiting, Auth
- Complejidad: Simple (6 elementos)

**9. Backend for Frontend (BFF)** ⭐⭐⭐⭐
- Diagrama: Web BFF + Mobile BFF → Services
- Archivo: `09-bff-pattern.excalidraw.md`
- Conceptos: Multiple Frontends, Dedicated BFFs, Shared Services
- Complejidad: Simple (5 elementos)

**10. Saga Pattern** ⭐⭐⭐⭐⭐
- Diagrama: Orchestration vs Choreography
- Archivo: `10-saga-pattern.excalidraw.md`
- Conceptos: Distributed Transactions, Compensations
- Complejidad: Media (6 elementos)

---

### Fase 3: Escalabilidad & Resiliencia (Semana 3)

**11. Circuit Breaker Pattern** ⭐⭐⭐⭐⭐
- Diagrama: Closed → Open → Half-Open states
- Archivo: `11-circuit-breaker.excalidraw.md`
- Conceptos: States, Thresholds, Fallbacks
- Complejidad: Simple (4 elementos)

**12. CQRS + Event Sourcing (Combined)** ⭐⭐⭐⭐⭐
- Diagrama: Commands → Events → Read Models
- Archivo: `12-cqrs-event-sourcing.excalidraw.md`
- Conceptos: Full pattern integration
- Complejidad: Media (7 elementos)

**13. Data Mesh Architecture** ⭐⭐⭐⭐⭐
- Diagrama: Domain-oriented data ownership
- Archivo: `13-data-mesh.excalidraw.md`
- Conceptos: Data Products, Domain Teams, Self-serve Platform
- Complejidad: Media (6 elementos)

**14. Strangler Fig Pattern** ⭐⭐⭐⭐⭐
- Diagrama: Legacy → Proxy → New System (migration)
- Archivo: `14-strangler-fig.excalidraw.md`
- Conceptos: Legacy, Facade, Incremental Migration
- Complejidad: Simple (5 elementos)

**15. Modular Monolith** ⭐⭐⭐⭐⭐
- Diagrama: Modules with clear boundaries
- Archivo: `15-modular-monolith.excalidraw.md`
- Conceptos: Modules, Internal APIs, Boundaries
- Complejidad: Simple (5 elementos)

---

### Fase 4: AI & Data (Semana 4)

**16. RAG Architecture (Retrieval-Augmented Generation)** ⭐⭐⭐⭐⭐
- Diagrama: Query → Vector DB → LLM → Response
- Archivo: `16-rag-architecture.excalidraw.md`
- Conceptos: Embeddings, Vector Store, LLM, Context
- Complejidad: Media (6 elementos)

**17. Lambda Architecture (Big Data)** ⭐⭐⭐⭐
- Diagrama: Batch Layer + Speed Layer + Serving Layer
- Archivo: `17-lambda-architecture.excalidraw.md`
- Conceptos: Batch Processing, Real-time, Views
- Complejidad: Media (6 elementos)

**18. Kappa Architecture** ⭐⭐⭐⭐
- Diagrama: Stream Processing only (no batch)
- Archivo: `18-kappa-architecture.excalidraw.md`
- Conceptos: Streaming, Replay, Single Pipeline
- Complejidad: Simple (4 elementos)

**19. Space-Based Architecture** ⭐⭐⭐⭐
- Diagrama: Processing Units + In-Memory Grid
- Archivo: `19-space-based.excalidraw.md`
- Conceptos: PU, Data Grid, Messaging, Deployment Manager
- Complejidad: Media (6 elementos)

**20. Zero Trust Architecture** ⭐⭐⭐⭐⭐
- Diagrama: Never Trust, Always Verify
- Archivo: `20-zero-trust.excalidraw.md`
- Conceptos: Identity, Verify, Least Privilege, Micro-segmentation
- Complejidad: Simple (5 elementos)

---

## Estructura de Cada Diagrama

### Template Excalidraw (Minimalista)

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw, architecture, {pattern-name}]
---

# {Architecture Name}

## Descripción (1 línea)
{Qué problema resuelve esta arquitectura}

## Elementos Clave (3-5 items)
1. {Elemento 1}
2. {Elemento 2}
3. {Elemento 3}

## Cuándo Usar
✅ {Escenario 1}
✅ {Escenario 2}
❌ {Cuándo NO usar}

## Archivo Relacionado
[[{numero}_ARCHIVO_RELACIONADO]]

---

# Excalidraw Data
[Diagrama simple y claro]
```

### Convenciones Visuales

**Formas:**
- 🟦 Rectángulo: Componente/Servicio
- ⬡ Hexágono: Core Domain
- 🔷 Rombo: Decision/Gateway
- 💾 Cilindro: Database
- ☁️ Nube: External Service
- 👤 Persona: User/Actor

**Colores:**
- 🔴 Rojo: External/User-facing
- 🟡 Amarillo: Core/Domain
- 🟢 Verde: Infrastructure
- 🔵 Azul: Data Layer
- 🟠 Naranja: Integration/Messaging

**Flechas:**
- → Solid: Synchronous call
- ⇢ Dashed: Asynchronous/Event
- ⟺ Double: Bidirectional

---

## Checklist por Diagrama

Antes de considerar completo:

- [ ] Max 7 elementos (cognitive load)
- [ ] 1 concepto principal claro
- [ ] Etiquetas en español
- [ ] Colores consistentes
- [ ] Descripción de 1 línea en el markdown
- [ ] "Cuándo usar" incluido
- [ ] Link al archivo relacionado
- [ ] Guardado en directorio correcto
- [ ] Nombre descriptivo del archivo

---

## Roadmap de Creación

### Semana 1: Fundamentos (5 diagramas)
- [ ] 01 Hexagonal Architecture
- [ ] 02 Clean Architecture
- [ ] 03 CQRS
- [ ] 04 Event Sourcing
- [ ] 05 Microservices

### Semana 2: Patrones Modernos (5 diagramas)
- [ ] 06 Serverless
- [ ] 07 Event-Driven
- [ ] 08 API Gateway
- [ ] 09 BFF
- [ ] 10 Saga Pattern

### Semana 3: Escalabilidad (5 diagramas)
- [ ] 11 Circuit Breaker
- [ ] 12 CQRS + Event Sourcing
- [ ] 13 Data Mesh
- [ ] 14 Strangler Fig
- [ ] 15 Modular Monolith

### Semana 4: AI & Data (5 diagramas)
- [ ] 16 RAG Architecture
- [ ] 17 Lambda Architecture
- [ ] 18 Kappa Architecture
- [ ] 19 Space-Based
- [ ] 20 Zero Trust

**Total: 20 diagramas en 4 semanas**
**Velocity: 5 diagramas/semana**

---

## Estrategia Incremental

1. **Crear 1 diagrama bien hecho** > 10 diagramas mediocres
2. **Iterar basado en feedback** de uso real
3. **Expandir gradualmente** a diagramas más complejos
4. **Mantener consistencia** visual en toda la colección
5. **Documentar decisiones** de diseño del diagrama

---

## Herramientas de Validación

**Antes de publicar cada diagrama:**

```bash
# Validar que el archivo existe
ls diagrams/architecture-patterns/{nombre}.excalidraw.md

# Verificar tags
grep "tags:" {archivo}

# Verificar link a archivo relacionado
grep "\[\[" {archivo}

# Contar elementos (max 7)
# Visual inspection en Obsidian
```

---

## Próximos Pasos

1. ✅ Crear estructura de directorios
2. → Crear primeros 5 diagramas (Semana 1)
3. → Validar con usuarios reales
4. → Iterar diseño basado en feedback
5. → Continuar con Semanas 2-4
6. → Expandir a diagramas de flujos y C4

**Enfoque: Calidad > Cantidad**

---

## Índice de Diagramas por Archivo

### Archivo 24: CQRS & Hexagonal
- Diagrama 01: Hexagonal Architecture ✅ (próximo)
- Diagrama 02: Clean Architecture ✅ (próximo)
- Diagrama 03: CQRS Pattern ✅ (próximo)

### Archivo 28: Event-Driven
- Diagrama 04: Event Sourcing ✅ (próximo)
- Diagrama 07: Event-Driven Architecture ✅ (próximo)
- Diagrama 12: CQRS + Event Sourcing ✅ (próximo)

### Archivo 25: Microservices
- Diagrama 05: Microservices Basic ✅ (próximo)
- Diagrama 08: API Gateway ✅ (próximo)
- Diagrama 09: BFF Pattern ✅ (próximo)
- Diagrama 10: Saga Pattern ✅ (próximo)
- Diagrama 14: Strangler Fig ✅ (próximo)

### Archivo 27: Serverless
- Diagrama 06: Serverless Pattern ✅ (próximo)

### Archivo 32: Resilience
- Diagrama 11: Circuit Breaker ✅ (próximo)

### Archivo 33: Data Architecture
- Diagrama 13: Data Mesh ✅ (próximo)
- Diagrama 17: Lambda Architecture
- Diagrama 18: Kappa Architecture

### Archivo 26: Modular Monolith
- Diagrama 15: Modular Monolith ✅ (próximo)

### Archivo 06: Agentic GenAI
- Diagrama 16: RAG Architecture ✅ (próximo)

### Archivo 34: Space-Based
- Diagrama 19: Space-Based ✅ (próximo)

### Archivo 30: Security
- Diagrama 20: Zero Trust ✅ (próximo)

---

## Resumen Ejecutivo

**Plan Actualizado:**
- **20 diagramas** de arquitecturas más reconocidas
- **4 semanas** de ejecución
- **Enfoque:** Pequeño, claro, comprensible
- **Max 7 elementos** por diagrama
- **1 concepto** por diagrama
- **Herramienta:** Excalidraw (hand-drawn style)

**Siguiente acción:** Crear primeros 5 diagramas de Semana 1

