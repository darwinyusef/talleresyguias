# Curso Completo: Arquitectura de Software - El Camino del Arquitecto Técnico (v2)
## De Cero a Experto: Basado en Roadmaps de Industria

Bienvenido a la versión 2.0 de este curso integral. Hemos actualizado el contenido basándonos en los estándares de la industria (Software Architect & System Design Roadmaps) para ofrecerte una guía estructurada y profunda. Este curso te transformará en un **Arquitecto Técnico** capaz de diseñar sistemas robustos, escalables y mantenibles.

---

## Tabla de Contenidos

1.  [Introducción: El Perfil del Arquitecto Moderno](#1-introducción-el-perfil-del-arquitecto-moderno)
2.  [Fase 1: Fundamentos de Diseño de Sistemas (Nivel Junior)](#2-fase-1-fundamentos-de-diseño-de-sistemas-nivel-junior)
    *   *Caso de Uso 1: La Librería Local (Monolito & Conceptos Base)*
3.  [Fase 2: Componentes y Patrones de Arquitectura (Nivel Intermedio)](#3-fase-2-componentes-y-patrones-de-arquitectura-nivel-intermedio)
    *   *Caso de Uso 2: Startup de Delivery (Escalabilidad & Patrones)*
4.  [Fase 3: Sistemas Distribuidos y Comunicación (Nivel Senior)](#4-fase-3-sistemas-distribuidos-y-comunicación-nivel-senior)
    *   *Caso de Uso 3: Plataforma de Streaming Global (Alto Rendimiento)*
5.  [Fase 4: Cloud Native, Resiliencia y Estrategia (Nivel Experto)](#5-fase-4-cloud-native-resiliencia-y-estrategia-nivel-experto)
    *   *Caso de Uso 4: Transformación Digital Bancaria (Legacy & Cloud Patterns)*
6.  [Habilidades Blandas y Carrera](#6-habilidades-blandas-y-carrera)
7.  [Herramientas y Entregables](#7-herramientas-y-entregables)

---

## 1. Introducción: El Perfil del Arquitecto Moderno

El Arquitecto Técnico no solo dibuja cajas y flechas. Es un líder técnico que equilibra las necesidades del negocio con la realidad tecnológica.

**Responsabilidades Expandidas:**
*   **Diseño de Alto Nivel:** Tomar decisiones críticas que afectan a todo el sistema.
*   **Filtrado de Requisitos:** Distinguir la señal del ruido; identificar qué requerimientos son realmente críticos.
*   **Estimación y Evaluación:** Proveer estimaciones realistas (desde días hasta años) y evaluar tecnologías.
*   **Seguridad:** Diseñar con la seguridad en mente desde el día 0 (OWASP).
*   **Comunicación y Mentoría:** Traducir problemas técnicos a lenguaje de negocio y guiar al equipo.

---

## 2. Fase 1: Fundamentos de Diseño de Sistemas (Nivel Junior)

Antes de diseñar microservicios, debes dominar los conceptos fundamentales que rigen el comportamiento de los sistemas.

### Conceptos Clave (System Design Roadmap)
*   **Performance vs. Escalabilidad:** Entender que un sistema rápido no siempre es escalable, y viceversa.
*   **Latencia vs. Throughput:** Tiempo de respuesta vs. capacidad de procesamiento.
*   **Teorema CAP:** La eterna lucha entre Consistencia, Disponibilidad y Tolerancia a Particiones.
*   **Modelos de Consistencia:** Fuerte, Eventual, Débil.
*   **DNS & Networking Básico:** Cómo viajan las peticiones.

### 🏛️ Caso de Uso 1: La Librería Local
**Contexto:** Una pequeña librería quiere vender online.

**Evolución del Diseño:**
1.  **Arquitectura:** Monolito Modular (Layered Architecture).
2.  **Base de Datos:** SQL (PostgreSQL) para consistencia ACID (Inventario y Pagos).
3.  **Decisión de Diseño:** Priorizar **Simplicidad** sobre Escalabilidad. No usar microservicios para evitar complejidad innecesaria.
4.  **Infraestructura:** Un servidor único (Vertical Scaling) es suficiente al inicio.

**Ejercicio Práctico:**
*   Calcula la latencia estimada de una petición SQL vs. leer de memoria.
*   Diseña el esquema de base de datos normalizado.

---

## 3. Fase 2: Componentes y Patrones de Arquitectura (Nivel Intermedio)

En esta fase, introducimos los bloques de construcción esenciales para sistemas que crecen.

### Componentes Clave
*   **Load Balancers:** L4 vs L7. Algoritmos (Round Robin, Least Connections).
*   **Caching:**
    *   *Estrategias:* Cache-Aside, Write-Through, Write-Behind.
    *   *Tipos:* Client, CDN, Web Server, Database, Application (Redis/Memcached).
*   **Proxies:** Reverse Proxy vs. Forward Proxy.
*   **Bases de Datos:** SQL vs. NoSQL (Document, Key-Value, Wide Column, Graph).

### Patrones de Arquitectura
*   **Microkernel / Plugin:** Para sistemas extensibles.
*   **Event-Driven:** Desacoplamiento mediante eventos.

### 🛵 Caso de Uso 2: Startup de Delivery
**Contexto:** El tráfico ha crecido. La base de datos es el cuello de botella.

**Solución Arquitectónica:**
1.  **Escalado Horizontal:** Múltiples instancias del backend detrás de un Load Balancer (Nginx/ALB).
2.  **Caching:** Implementar **Cache-Aside** con Redis para los menús de restaurantes (lectura intensiva).
3.  **Base de Datos:**
    *   *Sharding:* Particionar la tabla de pedidos por `city_id` si crece demasiado.
    *   *Replicación:* Master-Slave para separar lecturas y escrituras.
4.  **CDN:** Servir imágenes de comida desde un CDN (Cloudflare/AWS CloudFront).

**Ejercicio Práctico:**
*   Configura una estrategia de invalidación de caché para cuando un restaurante cambia un precio.
*   Elige entre una DB SQL o NoSQL para almacenar el historial de ubicaciones de los repartidores (Write-heavy).

---

## 4. Fase 3: Sistemas Distribuidos y Comunicación (Nivel Senior)

Aquí entramos en la complejidad de los sistemas que operan en múltiples nodos y deben hablar entre sí eficientemente.

### Protocolos de Comunicación
*   **Síncronos:** REST, gRPC (Protobuf), GraphQL.
*   **Asíncronos:** Message Queues (RabbitMQ, Kafka), Pub/Sub.
*   **Técnicas:** Short Polling, Long Polling, WebSockets, Server-Sent Events (SSE).

### Conceptos Avanzados
*   **Idempotencia:** Garantizar que reintentar una operación no tenga efectos secundarios.
*   **Hashing Consistente:** Para distribuir carga en cachés distribuidos.

### 🎬 Caso de Uso 3: Plataforma de Streaming Global
**Contexto:** Millones de usuarios concurrentes viendo video en vivo.

**Solución Arquitectónica:**
1.  **Protocolos:**
    *   *Video:* HLS/DASH sobre HTTP (aprovecha CDNs).
    *   *Chat en vivo:* WebSockets para baja latencia bidireccional.
    *   *Backend Interno:* gRPC para comunicación rápida entre microservicios.
2.  **Base de Datos:** Cassandra o DynamoDB (Wide Column) para almacenar millones de mensajes de chat por segundo (Alta disponibilidad y particionamiento).
3.  **Message Queue:** Kafka para ingesta masiva de eventos de analítica (quién ve qué).

**Ejercicio Práctico:**
*   Diseña el flujo de autenticación usando JWT y un API Gateway.
*   Explica cómo manejarías el "Thundering Herd Problem" si el caché se cae.

---

## 5. Fase 4: Cloud Native, Resiliencia y Estrategia (Nivel Experto)

El nivel experto se enfoca en patrones de nube, migración y robustez ante fallos.

### Cloud Design Patterns
*   **Ambassador:** Contenedor helper para proxying.
*   **Sidecar:** Extender funcionalidad (logging, proxy) sin tocar el contenedor principal.
*   **BFF (Backend for Frontend):** Backends específicos para Móvil vs. Web.
*   **Strangler Fig:** Migración gradual de monolito a microservicios.

### Reliability Patterns (Resiliencia)
*   **Circuit Breaker:** Prevenir fallos en cascada.
*   **Bulkhead:** Aislar recursos para que un fallo no tumbe todo el sistema.
*   **Retry & Exponential Backoff:** Reintentos inteligentes.
*   **Saga Pattern:** Transacciones distribuidas (Coreografía vs Orquestación).

### 🏦 Caso de Uso 4: Transformación Digital Bancaria
**Contexto:** Modernizar un Core Bancario Legacy sin detener la operación.

**Solución Arquitectónica:**
1.  **Patrón Strangler Fig:**
    *   Poner un API Gateway delante del Monolito.
    *   Crear nuevos microservicios para nuevas funcionalidades (ej. Pagos QR).
    *   Redirigir tráfico gradualmente del Monolito a los nuevos servicios.
2.  **Anti-Corruption Layer (ACL):** Traducir modelos modernos a modelos legacy del Mainframe.
3.  **Resiliencia:** Implementar Circuit Breakers en las llamadas al Mainframe (que suele ser lento).
4.  **Seguridad:** Implementar OAuth2/OIDC centralizado.

**Ejercicio Práctico:**
*   Diseña una Saga para una transferencia bancaria que falla a mitad de camino (Compensating Transaction).
*   Define la estrategia de Observabilidad (Tracing distribuido con Jaeger/OpenTelemetry).

---

## 6. Habilidades Blandas y Carrera

Ser arquitecto es 50% técnico y 50% humano.

*   **Liderazgo:** Influenciar sin autoridad directa.
*   **Negociación:** Convencer a stakeholders de pagar deuda técnica.
*   **Mentoría:** Crear la próxima generación de líderes técnicos.
*   **Aprendizaje Continuo:** La tecnología cambia, los fundamentos permanecen.

## 7. Herramientas y Entregables

*   **Diagramas:** C4 Model, UML (Secuencia, Componentes).
*   **Documentación:** ADRs (Architecture Decision Records), RFCs (Request for Comments).
*   **Cloud:** AWS/Azure/GCP Well-Architected Frameworks.

---
*Este curso v2 integra los mejores conocimientos de los roadmaps de "Software Architect" y "System Design" para ofrecerte una ruta clara y práctica.*
