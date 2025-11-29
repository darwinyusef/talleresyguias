# Curso Completo: Arquitectura de Software - El Camino del Arquitecto Técnico (v2.1 Avanzado)
## De Cero a Experto: Edición Mejorada y Práctica

Bienvenido a la versión avanzada (v2.1) de este curso. Esta edición expande los conceptos teóricos con **ejemplos de código**, **diagramas conceptuales** y una profundidad técnica mayor, diseñada para prepararte no solo para el trabajo, sino para entrevistas de System Design de alto nivel (FAANG).

---

## Tabla de Contenidos

1.  [Introducción: El Mindset del Arquitecto](#1-introducción-el-mindset-del-arquitecto)
2.  [Fase 1: Fundamentos y Diseño de Datos (Nivel Junior)](#2-fase-1-fundamentos-y-diseño-de-datos-nivel-junior)
    *   *Deep Dive: Índices de Base de Datos y Normalización*
    *   *Caso de Uso 1: Librería Local (Implementación de Esquema)*
3.  [Fase 2: Escalabilidad Horizontal y Patrones (Nivel Intermedio)](#3-fase-2-escalabilidad-horizontal-y-patrones-nivel-intermedio)
    *   *Deep Dive: Estrategias de Caching y Load Balancing*
    *   *Caso de Uso 2: Startup de Delivery (Configuración de Redis y Nginx)*
4.  [Fase 3: Sistemas Distribuidos y Alta Concurrencia (Nivel Senior)](#4-fase-3-sistemas-distribuidos-y-alta-concurrencia-nivel-senior)
    *   *Deep Dive: Kafka vs. RabbitMQ y Particionamiento*
    *   *Caso de Uso 3: Streaming Global (Diseño de Sharding)*
5.  [Fase 4: Arquitectura Empresarial y Cloud Native (Nivel Experto)](#5-fase-4-arquitectura-empresarial-y-cloud-native-nivel-experto)
    *   *Deep Dive: Kubernetes Patterns y Service Mesh*
    *   *Caso de Uso 4: Transformación Bancaria (Implementación de Circuit Breaker)*
6.  [Taller de Entrevistas de System Design](#6-taller-de-entrevistas-de-system-design)
7.  [Recursos y Herramientas](#7-recursos-y-herramientas)

---

## 1. Introducción: El Mindset del Arquitecto

El arquitecto no busca la solución "perfecta", busca la solución con los **trade-offs (compromisos)** correctos.

**La Regla de Oro:** "Todo en arquitectura es un trade-off. Si alguien te dice que una solución no tiene desventajas, te está mintiendo o no la ha analizado lo suficiente."

**Ejemplo de Trade-off:**
*   *Microservicios:* Ganas agilidad de despliegue y escalabilidad independiente. **Pierdes** simplicidad, consistencia de datos fácil y facilidad de depuración.
*   *SQL:* Ganas consistencia ACID y consultas complejas. **Pierdes** flexibilidad de esquema y escalabilidad horizontal fácil (comparado con NoSQL).

---

## 2. Fase 1: Fundamentos y Diseño de Datos (Nivel Junior)

### Deep Dive: Índices y Rendimiento
No basta con decir "usa una base de datos". Debes saber cómo hacerla rápida.

*   **B-Trees:** Estructura por defecto en SQL. Excelente para búsquedas de rango (`WHERE age > 20`).
*   **Hash Indexes:** O(1) para búsquedas exactas (`WHERE id = 123`). No sirven para rangos.

### 🏛️ Caso de Uso 1: La Librería Local (Implementación)

**Reto:** Diseñar el esquema para soportar búsquedas rápidas de libros por autor y categoría.

**Solución de Esquema (SQL):**

```sql
-- Tabla Libros
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT REFERENCES authors(id),
    category_id INT REFERENCES categories(id),
    price DECIMAL(10, 2),
    published_date DATE
);

-- Índices Críticos (La magia del rendimiento)
-- Acelera búsquedas por autor:
CREATE INDEX idx_books_author ON books(author_id);
-- Acelera filtros por categoría y fecha (índice compuesto):
CREATE INDEX idx_books_cat_date ON books(category_id, published_date DESC);
```

**Lección:** Sin índices, la base de datos hace un "Full Table Scan" (lee todo el disco). Con índices, salta directo al dato.

---

## 3. Fase 2: Escalabilidad Horizontal y Patrones (Nivel Intermedio)

### Deep Dive: Caching Strategies
El caché es la forma más barata de escalar.

1.  **Cache-Aside (Lazy Loading):**
    *   La aplicación pide el dato al caché.
    *   Si no está (Miss), va a la DB, lo lee y lo guarda en caché.
    *   *Pros:* Solo guarda lo que se usa. *Contras:* Latencia en el primer acceso.
2.  **Write-Through:**
    *   La aplicación escribe en caché y DB al mismo tiempo.
    *   *Pros:* Datos siempre frescos. *Contras:* Escritura más lenta.

### 🛵 Caso de Uso 2: Startup de Delivery (Configuración)

**Reto:** Configurar Nginx como Load Balancer y Redis para sesiones.

**Configuración Nginx (Load Balancer):**

```nginx
upstream backend_servers {
    # Algoritmo Least Connections: Envía tráfico al server más libre
    least_conn; 
    server backend1.example.com;
    server backend2.example.com;
    server backend3.example.com;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend_servers;
    }
}
```

**Diseño de Clave Redis:**
*   Mala práctica: `key: "user123"` (Colisiones posibles).
*   Buena práctica: `key: "session:user:123"`, `key: "cart:user:123"`.

---

## 4. Fase 3: Sistemas Distribuidos y Alta Concurrencia (Nivel Senior)

### Deep Dive: Kafka vs. RabbitMQ
*   **RabbitMQ (Smart Broker, Dumb Consumer):**
    *   Ideal para tareas complejas de enrutamiento.
    *   Mensaje se borra tras consumo.
    *   *Uso:* Procesamiento de pedidos, envío de emails.
*   **Kafka (Dumb Broker, Smart Consumer):**
    *   Log distribuido. Persiste mensajes por días/semanas.
    *   Alto throughput (millones/seg).
    *   *Uso:* Analytics, Event Sourcing, Logs de actividad.

### 🎬 Caso de Uso 3: Streaming Global (Sharding)

**Reto:** Almacenar 10 millones de mensajes de chat por minuto. Una sola DB no aguanta la escritura.

**Estrategia de Sharding (Particionamiento):**
Usaremos **Partition Key** basada en `live_stream_id`.

*   Todos los mensajes del stream "Final del Mundial" van al mismo nodo (Shard A).
*   *Problema:* "Hot Partition". Si todo el mundo ve el mundial, el Shard A explota.
*   *Solución Avanzada:* `Partition Key = live_stream_id + random_bucket(1-10)`.
    *   Distribuye la carga del mundial en 10 nodos.
    *   Para leer, tienes que consultar los 10 nodos y mezclar resultados (Scatter-Gather).

---

## 5. Fase 4: Arquitectura Empresarial y Cloud Native (Nivel Experto)

### Deep Dive: Patrones de Resiliencia (Circuit Breaker)
Evita que un fallo en el servicio de "Recomendaciones" tumbe toda la página de "Inicio".

**Implementación Conceptual (Javascript/Pseudo-código):**

```javascript
const circuitBreaker = new CircuitBreaker(recommendationService.get, {
  timeout: 3000, // Si tarda más de 3s, falla
  errorThresholdPercentage: 50, // Si el 50% falla, abre el circuito
  resetTimeout: 10000 // Espera 10s antes de intentar de nuevo
});

circuitBreaker.fallback(() => {
  return ["Recomendación Genérica 1", "Recomendación Genérica 2"];
});

// Uso
const recommendations = await circuitBreaker.fire(userId);
```

### 🏦 Caso de Uso 4: Transformación Bancaria (Strangler Fig)

**Estrategia de Migración Paso a Paso:**
1.  **Día 0:** Todo tráfico -> Monolito Legacy.
2.  **Día 30:** API Gateway intercepta ruta `/api/v1/pagos-qr`.
    *   Redirige al nuevo Microservicio (Go/Node).
    *   El resto (`/api/v1/transferencias`) sigue pasando al Monolito.
3.  **Día 60:** Microservicio necesita datos de Cliente del Monolito.
    *   Usa **CDC (Change Data Capture)** con Debezium para replicar cambios de la DB Legacy a una DB moderna en tiempo real, sin tocar el código COBOL.

---

## 6. Taller de Entrevistas de System Design

Estructura recomendada para responder en una entrevista (45 min):

1.  **Aclarar Requisitos (5 min):**
    *   ¿Funcionales? (Enviar mensaje, ver historial).
    *   ¿No funcionales? (Latencia < 200ms, Consistencia eventual ok).
    *   ¿Escala? (DAU, QPS, Read/Write ratio).
2.  **Diseño de Alto Nivel (10 min):**
    *   Dibuja cajas grandes: Cliente -> LB -> API Gateway -> Service -> DB.
3.  **Diseño Detallado (20 min):**
    *   Profundiza en lo difícil. ¿Cómo escalas la DB? ¿Cómo manejas la concurrencia?
4.  **Cuellos de Botella (10 min):**
    *   Identifica puntos de fallo (SPOF).
    *   Propón soluciones (Replicación, Sharding, Rate Limiting).

---

## 7. Recursos y Herramientas

*   **Libros:** "Designing Data-Intensive Applications" (La Biblia), "Clean Architecture".
*   **Herramientas:**
    *   *Diagramas:* Excalidraw (Estilo sketch), PlantUML (Diagramas como código).
    *   *Pruebas de Carga:* k6, JMeter (Para probar si tu arquitectura aguanta).

---
*Esta versión v2.1 añade profundidad técnica real y ejemplos de implementación para cerrar la brecha entre la teoría y la práctica.*
