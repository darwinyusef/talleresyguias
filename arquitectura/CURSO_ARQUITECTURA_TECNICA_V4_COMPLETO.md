# Curso Completo: Arquitectura de Software - El Arquitecto Aumentado v4.0
## Integración Total: IA, Fundamentos Clásicos y Roadmap Profesional

Bienvenido a la **Versión 4.0 Completa** del curso. Esta edición integra la **visión moderna del arquitecto aumentado por IA** con el **roadmap profesional completo** del Software Architect, combinando habilidades emergentes con fundamentos probados.

Esta guía definitiva combina:
- **Los 7 Pilares Fundamentales** de la arquitectura moderna
- **Las 7 Habilidades Críticas** para el profesional de élite en 2025
- **El Roadmap Completo** del Software Architect profesional
- **Niveles de Arquitectura** y progresión de carrera
- **Frameworks, Certificaciones y Gestión** empresarial

---

## Tabla de Contenidos

### PARTE 0: Fundamentos del Arquitecto de Software
1. [¿Qué es la Arquitectura de Software?](#qué-es-la-arquitectura-de-software)
2. [¿Qué es un Arquitecto de Software?](#qué-es-un-arquitecto-de-software)
3. [Niveles de Arquitectura](#niveles-de-arquitectura)
4. [Responsabilidades del Arquitecto](#responsabilidades-del-arquitecto)
5. [Habilidades Esenciales del Arquitecto](#habilidades-esenciales-del-arquitecto)

### PARTE I: Los 7 Pilares Fundamentales
6. [Pilar 1: Ingeniería de Prompt y Verificación de Código](#pilar-1-ingeniería-de-prompt-y-verificación-de-código)
7. [Pilar 2: Fundamentos Inmutables](#pilar-2-fundamentos-inmutables)
8. [Pilar 3: Protocolos Distribuidos y APIs](#pilar-3-protocolos-distribuidos-y-apis)
9. [Pilar 4: Control de Versiones Avanzado (Git)](#pilar-4-control-de-versiones-avanzado-git)
10. [Pilar 5: Cloud Computing y Arquitectura Nativa](#pilar-5-cloud-computing-y-arquitectura-nativa)
11. [Pilar 6: Automatización y DevOps (CI/CD)](#pilar-6-automatización-y-devops-cicd)
12. [Pilar 7: Ciberseguridad (DevSecOps)](#pilar-7-ciberseguridad-devsecops)

### PARTE II: Las 7 Habilidades Críticas (Skills)
13. [Skill 1: Manejar Claude y LLMs Avanzados](#skill-1-manejar-claude-y-llms-avanzados)
14. [Skill 2: Bases de Datos - Manejo Profundo](#skill-2-bases-de-datos---manejo-profundo)
15. [Skill 3: Agentes (n8n, LangGraph)](#skill-3-agentes-n8n-langgraph)
16. [Skill 4: Orquestar Deep Learning](#skill-4-orquestar-deep-learning)
17. [Skill 5: Docker y CI/CD (La Norma)](#skill-5-docker-y-cicd-la-norma)
18. [Skill 6: Debugear Código (El Contra-Argumento a la IA)](#skill-6-debugear-código-el-contra-argumento-a-la-ia)
19. [Skill 7: Generar Plans y Prompt Engineering](#skill-7-generar-plans-y-prompt-engineering)

### PARTE III: Dominio Técnico Completo
20. [Lenguajes de Programación](#lenguajes-de-programación)
21. [Patrones y Principios de Diseño](#patrones-y-principios-de-diseño)
22. [Patrones de Arquitectura](#patrones-de-arquitectura)
23. [Seguridad en Profundidad](#seguridad-en-profundidad)
24. [APIs e Integraciones](#apis-e-integraciones)
25. [Desarrollo Web y Mobile](#desarrollo-web-y-mobile)
26. [Redes y Comunicaciones](#redes-y-comunicaciones)
27. [Conocimientos de Operaciones](#conocimientos-de-operaciones)
28. [Software Empresarial](#software-empresarial)

### PARTE IV: Frameworks y Gestión
29. [Frameworks de Arquitectura](#frameworks-de-arquitectura)
30. [Metodologías de Gestión](#metodologías-de-gestión)
31. [Modelo Ágil](#modelo-ágil)
32. [Certificaciones](#certificaciones)

### PARTE V: Integración y Casos de Estudio
33. [Caso de Estudio Final: "The Autonomous AI Bank"](#caso-de-estudio-final-the-autonomous-ai-bank)
34. [Ruta de Carrera del Arquitecto](#ruta-de-carrera-del-arquitecto)

---

# PARTE 0: Fundamentos del Arquitecto de Software

## ¿Qué es la Arquitectura de Software?

La **Arquitectura de Software** describe cómo se construye una aplicación, incluyendo:
- Sus **componentes** y módulos
- Cómo **interactúan** entre sí
- El **entorno** en el que operan
- **Decisiones estructurales** de alto nivel que afectan todo el sistema

**Ejemplos:**
- Una arquitectura de microservicios con API Gateway
- Una arquitectura serverless con funciones Lambda
- Una arquitectura monolítica en capas

---

## ¿Qué es un Arquitecto de Software?

Un **experto en software** que:
- Toma **decisiones de diseño de alto nivel**
- Define **estándares técnicos** y herramientas
- Establece **principios de diseño**
- Selecciona **plataformas** y tecnologías
- **Guía a los equipos** en la implementación

**No es solo un programador senior**, es un estratega técnico que balancea:
- Requisitos de negocio
- Limitaciones técnicas
- Costos y tiempos
- Escalabilidad futura

---

## Niveles de Arquitectura

### 1. Application Architecture (Arquitectura de Aplicación)
**Alcance:** Una aplicación individual

**Responsabilidades:**
- Diseñar la estructura interna de la app
- Definir capas (presentación, lógica, datos)
- Seleccionar frameworks y librerías
- Establecer patrones de código

**Ejemplo:** Diseñar la arquitectura de una app móvil de e-commerce
```
Frontend (React Native)
   ↓
API Layer (GraphQL)
   ↓
Business Logic (Node.js)
   ↓
Data Layer (PostgreSQL + Redis)
```

---

### 2. Solution Architecture (Arquitectura de Solución)
**Alcance:** Múltiples aplicaciones trabajando juntas para resolver un problema de negocio

**Responsabilidades:**
- Integrar múltiples sistemas
- Diseñar flujos de datos entre aplicaciones
- Garantizar interoperabilidad
- Gestionar dependencias entre sistemas

**Ejemplo:** Solución de omnichannel para retail
```
Web App ─┐
Mobile App├─→ API Gateway ─→ Order Service ─→ SAP ERP
POS System─┘                      ↓
                            Notification Service
                                  ↓
                            (Email, SMS, Push)
```

---

### 3. Enterprise Architecture (Arquitectura Empresarial)
**Alcance:** Toda la organización

**Responsabilidades:**
- Alinear tecnología con estrategia de negocio
- Estandarizar tecnologías en toda la empresa
- Gestionar roadmap tecnológico a largo plazo
- Optimizar costos y eficiencias a escala

**Ejemplo:** Transformación digital de un banco
- Migración a cloud (AWS)
- Modernización de core bancario (monolito → microservicios)
- Implementación de data lake para analytics
- Adopción de IA para detección de fraude

**Frameworks:** TOGAF, Zachman Framework

---

## Responsabilidades del Arquitecto

### 1. Tech Decisions (Decisiones Tecnológicas)
- Seleccionar el stack tecnológico
- Decidir entre SQL vs. NoSQL
- Elegir entre monolito vs. microservicios
- Evaluar build vs. buy

**Ejemplo de decisión:**
```
¿PostgreSQL o MongoDB?
- Si necesitas transacciones ACID y relaciones complejas → PostgreSQL
- Si necesitas esquemas flexibles y alta escritura → MongoDB
```

### 2. Design & Architecture Decisions
- Definir patrones arquitectónicos
- Establecer principios de diseño
- Documentar decisiones (ADRs - Architecture Decision Records)

**Ejemplo de ADR:**
```markdown
# ADR-001: Adoptar arquitectura de microservicios

## Contexto
El monolito actual no escala y los deploys son riesgosos.

## Decisión
Migrar a microservicios con API Gateway.

## Consecuencias
+ Escalabilidad independiente por servicio
+ Deploys independientes
- Mayor complejidad operacional
- Necesidad de Service Mesh
```

### 3. Requirements Elicitation (Extracción de Requisitos)
- Traducir requisitos de negocio a requisitos técnicos
- Identificar requisitos no funcionales (performance, seguridad, disponibilidad)

**Ejemplo:**
- Negocio dice: "Queremos procesar pagos rápidamente"
- Arquitecto traduce: "Latencia < 200ms en el 99 percentil, disponibilidad 99.95%"

### 4. Documentation (Documentación)
- Diagramas de arquitectura (C4 Model)
- Diagramas de secuencia
- Documentación de APIs
- Runbooks operacionales

### 5. Enforcing Standards (Aplicar Estándares)
- Code reviews enfocados en arquitectura
- Definir guías de estilo
- Establecer pipelines de calidad (linters, tests de arquitectura)

### 6. Collaborate with Others (Colaborar)
- Con Product Managers (requisitos)
- Con DevOps (despliegues)
- Con Security (amenazas)
- Con otros arquitectos (alineación)

### 7. Consult & Coach Developers (Consultar y Entrenar)
- Sesiones de pair programming
- Code reviews educativos
- Tech talks internos
- Mentorías 1-1

---

## Habilidades Esenciales del Arquitecto

### 1. Design & Architecture
Capacidad de diseñar sistemas complejos, escalables y mantenibles.

### 2. Decision Making (Toma de Decisiones)
**El arte del trade-off:**
- Velocidad vs. Calidad
- Costo vs. Performance
- Complejidad vs. Flexibilidad

**Técnica:** [ADR (Architecture Decision Records)](https://adr.github.io/)

### 3. Simplifying Things (Simplificar)
> "La perfección se alcanza no cuando no hay nada más que agregar, sino cuando no hay nada más que quitar." - Antoine de Saint-Exupéry

**Principio KISS:** Keep It Simple, Stupid

### 4. How to Code (Saber Programar)
Un arquitecto que no programa es como un chef que no cocina.
- Hacer POCs (Proof of Concepts)
- Validar decisiones técnicas con código
- Mantener credibilidad técnica

### 5. Documentation (Documentación)
Código sin documentación = conocimiento perdido.
- README.md efectivos
- Diagramas que expliquen, no decoren
- ADRs para decisiones críticas

### 6. Communication (Comunicación)
- Explicar arquitectura a no técnicos
- Defender decisiones con datos
- Escuchar feedback del equipo

### 7. Estimate and Evaluate (Estimar y Evaluar)
- Estimar esfuerzos de desarrollo
- Evaluar tecnologías (POCs)
- Calcular costos de cloud

### 8. Balance (Balancear)
- Perfección técnica vs. Time-to-Market
- Innovación vs. Estabilidad
- Deuda técnica controlada

### 9. Consult & Coach (Consultar y Entrenar)
- Ser un líder técnico sin autoridad formal
- Influenciar sin imponer

### 10. Marketing Skills (Habilidades de Marketing)
- "Vender" tus decisiones arquitectónicas
- Crear buy-in del equipo
- Comunicar valor al negocio

---

# PARTE I: Los 7 Pilares Fundamentales

## Pilar 1: Ingeniería de Prompt y Verificación de Código
**(Crítico para 2025)**

El programador moderno es un **editor y auditor** de código generado por IA.

### Prompt Engineering para Arquitectos

**Prompts débiles vs. Prompts fuertes:**

❌ **Débil:** "Crea una función de login"

✅ **Fuerte:**
```
Diseña un módulo de autenticación con estas características:
- OAuth2 + JWT con refresh tokens
- Stateless (sin sesiones en servidor)
- Rate limiting (5 intentos por minuto)
- Multi-factor authentication (TOTP)
- Principios SOLID
- Manejo de errores: token expirado, usuario bloqueado, MFA fallido
- Lenguaje: TypeScript
- Tests unitarios con Jest
```

### Verificación y Auditoría

La IA **alucina**. Tú detectas:
- **Vulnerabilidades:** SQL Injection, XSS
- **Ineficiencias:** O(n²) en lugar de O(n log n)
- **Deuda técnica:** Código no mantenible
- **Errores lógicos:** Edge cases no manejados

**Regla de Oro:** Nunca hagas commit de código generado por IA que no entiendas al 100%.

### Herramientas de Verificación
- **SonarQube:** Análisis de calidad
- **Snyk:** Vulnerabilidades de seguridad
- **ESLint/Pylint:** Linters
- **CodeQL:** Análisis de seguridad semántico

---

## Pilar 2: Fundamentos Inmutables
**(Indispensable)**

La sintaxis cambia cada año. Los fundamentos permanecen décadas.

### Algoritmos y Estructuras de Datos

**Estructuras:**
- **HashMap:** O(1) búsqueda - usar para cachés
- **Tree (B-Tree):** O(log n) - usar para índices de DB
- **Graph:** Relaciones complejas - redes sociales

**Algoritmos:**
- **QuickSort vs. MergeSort:** QuickSort es más rápido en promedio, MergeSort es estable
- **Dijkstra:** Camino más corto en grafos - rutas de envío
- **Dynamic Programming:** Optimización - pricing algorithms

### Patrones de Diseño

**Creacionales:**
- **Singleton:** Una sola instancia (e.g., conexión a DB)
- **Factory:** Crear objetos sin especificar clase exacta

**Estructurales:**
- **Adapter:** Hacer que interfaces incompatibles trabajen juntas
- **Proxy:** Control de acceso a un objeto

**Comportamiento:**
- **Strategy:** Algoritmos intercambiables
- **Observer:** Notificaciones de cambios (Event-Driven)

**Por qué importan:**
La IA escribe código procedimental. Tú impones **arquitectura**.

### Lógica de Negocio

La IA no entiende tu dominio de negocio. Tú sí.

**Ejemplo:**
```
Regla de negocio: "Un cliente VIP tiene 30 días para devolver un producto"
La IA puede escribir: return days <= 30
Tú escribes: return customer.isVIP() && days <= customer.getReturnWindow()
```

---

## Pilar 3: Protocolos Distribuidos y APIs
**(Indispensable)**

### REST vs. GraphQL vs. gRPC

| Característica | REST | GraphQL | gRPC |
|---|---|---|---|
| **Formato** | JSON | JSON | Protobuf (binario) |
| **Performance** | Media | Media | Alta |
| **Cacheable** | Sí (HTTP) | Difícil | No |
| **Flexibilidad** | Baja | Alta | Baja |
| **Uso ideal** | CRUD, Public APIs | Frontend flexible | Microservicios internos |

### Formatos de Datos

**JSON:**
```json
{"name": "John", "age": 30}
```
- Legible, amplio soporte
- Más pesado que binario

**Protobuf:**
```protobuf
message User {
  string name = 1;
  int32 age = 2;
}
```
- Compacto, rápido
- Requiere definición de schema

### HTTP/HTTPS en Profundidad

**Códigos de Estado:**
- `200 OK` - Éxito
- `201 Created` - Recurso creado
- `400 Bad Request` - Error del cliente
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - Autenticado pero sin permisos
- `429 Too Many Requests` - Rate limit excedido
- `500 Internal Server Error` - Error del servidor
- `503 Service Unavailable` - Servidor sobrecargado

**Headers Críticos:**
- `Authorization: Bearer <token>` - Autenticación
- `Content-Type: application/json` - Tipo de contenido
- `Cache-Control: max-age=3600` - Cacheo
- `X-Request-ID` - Tracing

**TLS Handshake:**
1. Cliente solicita conexión segura
2. Servidor envía certificado
3. Cliente verifica certificado con CA
4. Intercambio de claves (Diffie-Hellman)
5. Comunicación encriptada

---

## Pilar 4: Control de Versiones Avanzado (Git)
**(Indispensable)**

### Flujos de Trabajo

**Trunk-Based Development:**
```
main ─────●─────●─────●────
           ↑     ↑     ↑
         commit commit commit
```
- Commits directos a `main`
- Feature flags para funcionalidades incompletas
- CI/CD robusto

**Git Flow:**
```
main     ─────●─────────●───
               ↑         ↑
develop  ──●───●───●─────●───
            ↑   ↑   ↑
feature    ─●───●   │
hotfix          ─────●
```
- Branches de larga duración
- Releases planificados

### Técnicas Avanzadas

**Git Rebase (vs. Merge):**
```bash
# Merge: Crea commit de merge
git merge feature-branch

# Rebase: Historia lineal
git rebase main
```

**Git Bisect (Encontrar el commit que rompió el build):**
```bash
git bisect start
git bisect bad           # Current commit is broken
git bisect good v1.0     # v1.0 was working
# Git checkout commits intermedios, tú pruebas
git bisect bad/good      # Repites hasta encontrar el commit culpable
```

**Git Reflog (Recuperar commits perdidos):**
```bash
git reflog
git checkout <commit-hash>
```

---

## Pilar 5: Cloud Computing y Arquitectura Nativa
**(Esencial)**

### Modelos de Cloud

**IaaS (Infrastructure as a Service):**
- Control total sobre VMs
- Ejemplo: AWS EC2, Azure VMs
- Uso: Cuando necesitas control del SO

**PaaS (Platform as a Service):**
- Despliegas código, cloud gestiona infraestructura
- Ejemplo: AWS Elastic Beanstalk, Heroku
- Uso: Apps web tradicionales

**FaaS (Functions as a Service - Serverless):**
- Pagas por ejecución, no por tiempo de servidor activo
- Ejemplo: AWS Lambda, Azure Functions
- Uso: Event-driven, cargas variables

### Contenedores y Orquestación

**Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

**Kubernetes:**
- Orquestación de contenedores
- Auto-scaling
- Self-healing
- Service discovery

### Infrastructure as Code (IaC)

**Terraform:**
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
  }
}
```

**Beneficios:**
- Infraestructura versionada en Git
- Reproducible
- Auditable

---

## Pilar 6: Automatización y DevOps (CI/CD)
**(Esencial)**

### Continuous Integration (CI)

**Pipeline típico:**
```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Dependencies
        run: npm install
      - name: Run Linter
        run: npm run lint
      - name: Run Tests
        run: npm test
      - name: Build
        run: npm run build
```

### Continuous Deployment (CD)

**De commit a producción sin intervención humana:**

```
Developer Push → CI Tests → Build Docker Image →
Push to Registry → Deploy to Staging →
Automated Tests → Deploy to Production
```

**Estrategias de Deploy:**

**Blue-Green:**
```
[Blue: v1.0 (100% traffic)] [Green: v1.1 (0% traffic)]
                ↓
[Blue: v1.0 (0% traffic)]  [Green: v1.1 (100% traffic)]
```

**Canary:**
```
v1.0 (95% traffic)  v1.1 (5% traffic)
        ↓
v1.0 (50% traffic)  v1.1 (50% traffic)
        ↓
v1.0 (0% traffic)   v1.1 (100% traffic)
```

---

## Pilar 7: Ciberseguridad (DevSecOps)
**(Esencial)**

### Shift Left Security

Seguridad desde el **diseño**, no como añadido final.

### OWASP Top 10 (2023)

1. **Broken Access Control:** Usuario A accede a datos de Usuario B
2. **Cryptographic Failures:** Contraseñas en texto plano
3. **Injection:** SQL Injection, Command Injection
4. **Insecure Design:** No considerar amenazas en diseño
5. **Security Misconfiguration:** S3 buckets públicos
6. **Vulnerable Components:** Librerías con CVEs
7. **Authentication Failures:** Brute force sin rate limiting
8. **Software and Data Integrity:** Supply chain attacks
9. **Security Logging Failures:** No loggear eventos de seguridad
10. **Server-Side Request Forgery (SSRF):** Servidor hace requests a URLs maliciosas

### Gestión de Secretos

❌ **MAL:**
```javascript
const API_KEY = "sk-1234567890abcdef"; // Hardcoded
```

✅ **BIEN:**
```javascript
const API_KEY = process.env.API_KEY; // Variable de entorno
```

**Herramientas:**
- **HashiCorp Vault:** Gestión centralizada de secretos
- **AWS Secrets Manager:** Rotación automática
- **Doppler:** Secretos para equipos

### Escaneo de Seguridad en CI/CD

```yaml
- name: Security Scan
  run: |
    docker scan myapp:latest
    npm audit
    snyk test
```

---

# PARTE II: Las 7 Habilidades Críticas (Skills)

## Skill 1: Manejar Claude y LLMs Avanzados
**(CRÍTICO)**

Claude, GPT-4, Gemini no son solo chatbots. Son **aceleradores de productividad 10x**.

### Uso Avanzado

**Generar Prototipos Completos:**
```
Prompt: "Genera un CRUD completo de productos con:
- Backend: FastAPI (Python)
- DB: PostgreSQL con SQLAlchemy
- Validación: Pydantic
- Tests: pytest con cobertura >80%
- Docker compose para desarrollo local
- README con instrucciones"
```

**Refactorizar Legacy:**
```
Prompt: "Refactoriza este código PHP legacy a TypeScript moderno usando:
- Clean Architecture
- Dependency Injection
- Principios SOLID
- Tests unitarios
Mantén la misma lógica de negocio"
```

**Traducir entre Lenguajes:**
```
Prompt: "Traduce este script Python de data processing a Rust,
optimizando para performance. Usa Polars en lugar de Pandas"
```

### Técnicas Avanzadas

**Chain-of-Thought Prompting:**
```
"Antes de generar el código, piensa paso a paso:
1. ¿Qué patrones de diseño aplican aquí?
2. ¿Qué edge cases debo manejar?
3. ¿Qué estructura de datos es más eficiente?
Luego genera el código"
```

**Few-Shot Learning:**
```
"Aquí hay ejemplos de nuestro estilo de código:

Ejemplo 1: [tu código]
Ejemplo 2: [tu código]

Ahora genera una nueva función siguiendo ese estilo"
```

**Retrieval-Augmented Generation (RAG):**
```
"Usando esta documentación interna [adjuntar docs],
genera un módulo que integre con nuestro sistema de pagos"
```

---

## Skill 2: Bases de Datos - Manejo Profundo
**(INDISPENSABLE)**

El código cambia, **los datos persisten** por décadas.

### Modelado de Datos

**Normalización (3NF):**
```sql
-- Evitar redundancia
Users: id, name, email
Orders: id, user_id, total
OrderItems: id, order_id, product_id, quantity
```

**Desnormalización (para performance):**
```sql
-- Duplicar datos para evitar JOINs
Orders: id, user_id, user_name, user_email, total
```

### Optimización de Consultas

**Índices:**
```sql
-- B-Tree: Búsquedas por rango
CREATE INDEX idx_created_at ON orders(created_at);

-- Hash: Búsquedas exactas
CREATE INDEX idx_email ON users USING HASH(email);

-- Full-Text: Búsquedas de texto
CREATE INDEX idx_description ON products USING GIN(to_tsvector('english', description));
```

**Análisis de Planes de Ejecución:**
```sql
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;

-- Busca:
-- - Seq Scan (malo) vs Index Scan (bueno)
-- - Execution Time
```

### Elección de Base de Datos

**SQL (PostgreSQL):**
- Transacciones ACID
- Relaciones complejas (JOINs)
- Consultas ad-hoc
- **Uso:** E-commerce, Fintech

**NoSQL Document (MongoDB):**
- Esquemas flexibles
- Alta escritura
- **Uso:** Catálogos de productos, Logs

**NoSQL Wide Column (Cassandra):**
- Escritura masiva
- Latencia baja
- **Uso:** IoT, Time series

**Vector DB (Pinecone, Weaviate):**
- Embeddings de IA
- Búsqueda semántica
- **Uso:** Chatbots con memoria, Recommendation engines

**Graph DB (Neo4j):**
- Relaciones complejas
- **Uso:** Redes sociales, Detección de fraude

---

## Skill 3: Agentes (n8n, LangGraph)
**(PIONERO Y ESENCIAL)**

El futuro no es usar IA, es **diseñar sistemas de agentes inteligentes**.

### n8n (Workflow Automation)

**Ejemplo de flujo:**
```
Trigger: Email recibido
  ↓
OpenAI: Extraer datos estructurados
  ↓
Airtable: Guardar lead
  ↓
Slack: Notificar a ventas
  ↓
Salesforce: Crear oportunidad
```

**Sin código**, pero con lógica de programación:
- Condicionales
- Loops
- Transformaciones de datos

### LangGraph (Agentic AI)

**Agente de Soporte:**
```python
from langgraph import Agent, Tool

tools = [
    Tool("search_knowledge_base", search_kb),
    Tool("check_order_status", check_order),
    Tool("escalate_to_human", escalate)
]

agent = Agent(
    model="gpt-4",
    tools=tools,
    system_prompt="Eres un agente de soporte. Resuelve issues o escala a humano si no puedes."
)

response = agent.run("¿Dónde está mi orden #12345?")
```

**Toma de decisiones complejas:**
- Analizar sentimiento del cliente
- Decidir si escalar basándose en urgencia y complejidad
- Aprender de interacciones pasadas

### Arquitectura Multi-Agente

```
Usuario
  ↓
Agente Clasificador (decide qué agente usar)
  ↓
  ├─→ Agente FAQ (respuestas predefinidas)
  ├─→ Agente Técnico (troubleshooting)
  ├─→ Agente Ventas (ofertas)
  └─→ Humano (casos complejos)
        ↓
    Vector DB (Base de Conocimiento)
```

---

## Skill 4: Orquestar Deep Learning
**(ESENCIAL - Infraestructura)**

No necesitas **entrenar** modelos desde cero, pero debes **integrarlos** y **desplegarlos**.

### Modelos Pre-entrenados

**Hugging Face:**
```python
from transformers import pipeline

# Análisis de sentimiento
classifier = pipeline("sentiment-analysis")
result = classifier("Este producto es excelente!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Generación de texto
generator = pipeline("text-generation", model="gpt2")
result = generator("El futuro de la IA es")
```

**OpenAI API:**
```python
import openai

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Analiza este contrato"}]
)
```

### Gestión de Recursos

**GPUs en la Nube:**
- **AWS SageMaker:** Entrenamiento y hosting
- **Google Vertex AI:** AutoML
- **Azure ML:** Pipelines de ML

**Optimización de Modelos:**
```python
# Cuantización (reduce tamaño sin perder mucha precisión)
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    load_in_8bit=True  # De 32-bit a 8-bit
)
```

### MLOps

**Versionado de Modelos (MLflow):**
```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

**Monitoreo de Drift:**
```python
# Detectar cuando el modelo pierde precisión
from evidently import Dashboard
from evidently.tabs import DataDriftTab

dashboard = Dashboard(tabs=[DataDriftTab()])
dashboard.calculate(reference_data, current_data)
```

---

## Skill 5: Docker y CI/CD (La Norma)
**(INDISPENSABLE)**

Estos no son opcionales. Son la **forma estándar** de trabajar en 2025.

### Docker Avanzado

**Multi-Stage Builds (reducir tamaño):**
```dockerfile
# Etapa 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Etapa 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm install --production
CMD ["node", "dist/index.js"]
```

**Docker Compose (desarrollo local):**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### CI/CD Pipeline Completo

**GitHub Actions:**
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Dependencies
        run: npm ci

      - name: Run Linter
        run: npm run lint

      - name: Run Tests
        run: npm test -- --coverage

      - name: Upload Coverage
        uses: codecov/codecov-action@v3

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Snyk Security Scan
        run: npx snyk test

      - name: Run npm audit
        run: npm audit --audit-level=high

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker Image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Push to Registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to AWS ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service myapp \
            --force-new-deployment
```

---

## Skill 6: Debugear Código (El Contra-Argumento a la IA)
**(CRÍTICO)**

La IA escribe código rápido, pero a menudo con **errores sutiles** que solo un humano experto detecta.

### Técnicas de Debugging

**Logs Estructurados:**
❌ **MAL:**
```javascript
console.log("Error!");
console.log(error);
```

✅ **BIEN:**
```javascript
logger.error({
  userId: user.id,
  action: 'processPayment',
  error: error.message,
  stack: error.stack,
  timestamp: new Date().toISOString()
});
```

**Debuggers de IDE:**
- **Breakpoints:** Pausar ejecución en línea específica
- **Watch Variables:** Monitorear valores en tiempo real
- **Call Stack:** Ver cadena de llamadas

**Debugging de Performance:**
```javascript
// Node.js profiling
node --inspect app.js

// Chrome DevTools: chrome://inspect
```

### Tracing Distribuido

**Jaeger / OpenTelemetry:**
```javascript
const { trace } = require('@opentelemetry/api');

const span = trace.getTracer('myapp').startSpan('processOrder');
span.setAttribute('orderId', orderId);

try {
  // Tu código
} finally {
  span.end();
}
```

**Seguir una petición a través de 10 microservicios:**
```
API Gateway (100ms)
  → Auth Service (50ms)
    → Order Service (200ms)
      → Payment Service (300ms) ← LENTO!
        → Email Service (100ms)
```

### Debugging de IA

**Escenario:** La IA genera un algoritmo O(n²), tú lo detectas con profiling.

```python
# Código generado por IA
def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):  # O(n²)
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates

# Tu versión optimizada
def find_duplicates(arr):
    return list(set([x for x in arr if arr.count(x) > 1]))  # O(n)
```

---

## Skill 7: Generar Plans y Prompt Engineering
**(LA NUEVA ARQUITECTURA)**

El prompt es la **especificación de software** de la era de la IA.

### Generar Plans

**Antes de pedir código, pide un plan:**

```
Prompt: "Genera un plan de arquitectura detallado para un sistema de reservas de hotel con:
- 10,000 usuarios concurrentes
- Búsqueda en tiempo real de disponibilidad
- Procesamiento de pagos
- Notificaciones multi-canal
- Presupuesto: $2000/mes en AWS

Incluye:
1. Diagrama de componentes
2. Elección de base de datos y justificación
3. Estrategia de caché
4. Estimación de costos
5. Puntos de falla y mitigación"
```

**Output de la IA:**
```
PLAN DE ARQUITECTURA

1. COMPONENTES
   - API Gateway (AWS API Gateway)
   - App Server (ECS Fargate)
   - Search Engine (Elasticsearch)
   - Database (RDS PostgreSQL)
   - Cache (ElastiCache Redis)
   - Queue (SQS)
   - Notifications (SNS + Lambda)

2. BASE DE DATOS
   PostgreSQL para:
   - Transacciones ACID (reservas)
   - Relaciones complejas (hoteles, habitaciones, reservas)

   Redis para:
   - Caché de disponibilidad (TTL 1 min)
   - Session store

   Elasticsearch para:
   - Búsqueda rápida de hoteles por ubicación, precio, amenities

3. ESTRATEGIA DE CACHÉ
   - Cache-Aside pattern
   - Invalidación en escritura
   - TTL variable según volatilidad de datos

4. ESTIMACIÓN COSTOS
   - API Gateway: $200/mes
   - ECS Fargate: $500/mes
   - RDS: $300/mes
   - ElastiCache: $150/mes
   - Elasticsearch: $600/mes
   - Otros: $250/mes
   TOTAL: $2000/mes ✓

5. PUNTOS DE FALLA
   - DB down → usar réplicas de lectura
   - Cache down → fallback a DB (degradación)
   - Search down → búsqueda simple en DB
```

### Prompt Engineering Avanzado

**Role Prompting:**
```
"Actúa como un arquitecto senior de AWS con 10 años de experiencia
en sistemas de alta concurrencia. Diseña..."
```

**Constraint Prompting:**
```
"El presupuesto es $500/mes. La latencia debe ser <100ms p99.
El sistema debe soportar picos de 10x tráfico en Black Friday.
Diseña..."
```

**Iterative Refinement:**
```
Tú: "Diseña una arquitectura de microservicios"
IA: [genera plan]
Tú: "Ahora añade observabilidad con métricas, logs y traces"
IA: [refina plan]
Tú: "Ahora añade estrategia de disaster recovery con RPO <1 hora"
IA: [refina más]
```

---

# PARTE III: Dominio Técnico Completo

## Lenguajes de Programación

### ¿Qué lenguajes debe saber un arquitecto?

**No todos, pero sí patrones de cada paradigma:**

### 1. Java / Kotlin / Scala
**Ecosistema JVM**

**Java:**
- Enterprise (Spring Boot)
- Android
- Sistemas legacy

**Kotlin:**
- Java moderno (null safety, coroutines)
- Android oficial

**Scala:**
- Funcional + OOP
- Big Data (Apache Spark)

### 2. Python
- Data Science / ML
- Scripting
- Backends rápidos (FastAPI, Django)

### 3. JavaScript / TypeScript
- Frontend (React, Vue, Angular)
- Backend (Node.js)
- TypeScript = JavaScript con tipos

### 4. Go
- Microservicios (performance)
- DevOps tools (Docker, Kubernetes)
- Concurrencia nativa

### 5. .NET Framework Based (C#, F#)
- Enterprise Microsoft
- Azure native
- Unity (gamedev)

### 6. Ruby
- Ruby on Rails (startups)
- Menos común hoy, pero legacy existe

**Estrategia del Arquitecto:**
- **Dominar 2-3 lenguajes** profundamente
- **Leer** otros 5-7 lenguajes (entender código)
- **Entender paradigmas:** OOP, Funcional, Procedural

---

## Patrones y Principios de Diseño

### Principios SOLID

**S - Single Responsibility Principle:**
```typescript
// ❌ MAL: Clase con múltiples responsabilidades
class User {
  saveToDatabase() { }
  sendEmail() { }
  generateReport() { }
}

// ✅ BIEN: Cada clase una responsabilidad
class User { }
class UserRepository { saveToDatabase() }
class EmailService { sendEmail() }
class ReportGenerator { generateReport() }
```

**O - Open/Closed Principle:**
```typescript
// Abierto para extensión, cerrado para modificación
interface PaymentMethod {
  pay(amount: number): void;
}

class CreditCard implements PaymentMethod {
  pay(amount: number) { /* ... */ }
}

class PayPal implements PaymentMethod {
  pay(amount: number) { /* ... */ }
}
```

**L - Liskov Substitution Principle:**
```typescript
// Los subtipos deben ser sustituibles por sus tipos base
class Bird {
  fly() { }
}

// ❌ MAL: Pingüino no puede volar
class Penguin extends Bird {
  fly() { throw new Error("Can't fly"); }
}

// ✅ BIEN: Jerarquía correcta
interface Bird { }
interface FlyingBird extends Bird {
  fly(): void;
}
```

**I - Interface Segregation Principle:**
```typescript
// Muchas interfaces específicas > 1 interfaz general
interface Printer {
  print(): void;
}

interface Scanner {
  scan(): void;
}

interface Fax {
  fax(): void;
}

// Implementa solo lo que necesitas
class SimplePrinter implements Printer {
  print() { }
}

class MultiFunctionDevice implements Printer, Scanner, Fax {
  print() { }
  scan() { }
  fax() { }
}
```

**D - Dependency Inversion Principle:**
```typescript
// Depende de abstracciones, no de concreciones
interface Database {
  save(data: any): void;
}

class PostgreSQL implements Database {
  save(data: any) { /* ... */ }
}

class MongoDB implements Database {
  save(data: any) { /* ... */ }
}

class UserService {
  constructor(private db: Database) { } // No depende de implementación específica

  createUser(user: User) {
    this.db.save(user);
  }
}
```

### Patrones de Diseño Clásicos (Gang of Four)

Los 23 patrones fundamentales que todo arquitecto debe dominar.

#### Patrones Creacionales (Cómo CREAR objetos)

**1. Singleton - Una Sola Instancia**

Problema: Necesitas exactamente UNA instancia en todo el sistema.

```typescript
class Database {
  private static instance: Database;
  private constructor() {
    this.connection = this.createConnection();
  }

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}

// Uso
const db1 = Database.getInstance();
const db2 = Database.getInstance();
console.log(db1 === db2); // true - misma instancia
```

**Cuándo usar:** DB connections, Logger, Config
**Cuándo NO:** Testing (dificulta mocking), estado global mutable

**2. Factory Method - Creación Flexible**

Problema: Crear objetos sin especificar clase exacta.

```typescript
interface PaymentProcessor {
  processPayment(amount: number): Promise<boolean>;
}

class StripePayment implements PaymentProcessor {
  async processPayment(amount: number): Promise<boolean> {
    // Lógica de Stripe
    return true;
  }
}

class PayPalPayment implements PaymentProcessor {
  async processPayment(amount: number): Promise<boolean> {
    // Lógica de PayPal
    return true;
  }
}

class PaymentFactory {
  static create(type: 'stripe' | 'paypal'): PaymentProcessor {
    switch (type) {
      case 'stripe': return new StripePayment();
      case 'paypal': return new PayPalPayment();
    }
  }
}
```

**3. Builder - Construcción Paso a Paso**

Problema: Objetos complejos con muchos parámetros opcionales.

```typescript
class HttpRequest {
  method: string = 'GET';
  url: string = '';
  headers: Map<string, string> = new Map();
  body?: any;
}

class HttpRequestBuilder {
  private request = new HttpRequest();

  method(m: 'GET' | 'POST'): this {
    this.request.method = m;
    return this;
  }

  url(u: string): this {
    this.request.url = u;
    return this;
  }

  header(key: string, value: string): this {
    this.request.headers.set(key, value);
    return this;
  }

  build(): HttpRequest {
    return this.request;
  }
}

// Uso fluent
const request = new HttpRequestBuilder()
  .method('POST')
  .url('https://api.com')
  .header('Content-Type', 'application/json')
  .build();
```

#### Patrones Estructurales (Cómo ORGANIZAR código)

**4. Adapter - Interfaces Incompatibles**

Problema: Hacer que interfaces incompatibles trabajen juntas.

```typescript
// Sistema legacy
class LegacyPayment {
  makePayment(account: string, amount: number): string {
    return `TX_${Date.now()}`;
  }
}

// Tu interfaz moderna
interface ModernPayment {
  processPayment(userId: string, amount: number): Promise<{
    transactionId: string;
    status: 'success' | 'failed';
  }>;
}

// Adapter
class LegacyPaymentAdapter implements ModernPayment {
  private legacy = new LegacyPayment();

  async processPayment(userId: string, amount: number) {
    const account = this.getUserAccount(userId);
    const txId = this.legacy.makePayment(account, amount);

    return {
      transactionId: txId,
      status: 'success' as const
    };
  }

  private getUserAccount(userId: string): string {
    return `ACC_${userId}`;
  }
}
```

**5. Decorator - Añadir Funcionalidad Dinámicamente**

Problema: Añadir responsabilidades sin modificar código.

```typescript
interface DataSource {
  writeData(data: string): void;
  readData(): string;
}

class FileDataSource implements DataSource {
  writeData(data: string) {
    console.log(`Writing: ${data}`);
  }
  readData(): string {
    return 'data from file';
  }
}

class EncryptionDecorator implements DataSource {
  constructor(private wrappee: DataSource) {}

  writeData(data: string) {
    const encrypted = Buffer.from(data).toString('base64');
    this.wrappee.writeData(encrypted);
  }

  readData(): string {
    const encrypted = this.wrappee.readData();
    return Buffer.from(encrypted, 'base64').toString();
  }
}

// Uso - composición de decorators
let source: DataSource = new FileDataSource();
source = new EncryptionDecorator(source);
source.writeData('secret'); // Escribe encriptado
```

**6. Proxy - Control de Acceso**

Problema: Controlar acceso a un objeto (lazy loading, caching, logging).

```typescript
class RealImage {
  constructor(private filename: string) {
    console.log(`Loading ${filename}...`);
  }
  display() {
    console.log(`Displaying ${this.filename}`);
  }
}

class ImageProxy {
  private realImage?: RealImage;

  constructor(private filename: string) {}

  display() {
    if (!this.realImage) {
      this.realImage = new RealImage(this.filename); // Lazy loading
    }
    this.realImage.display();
  }
}

// Uso
const image = new ImageProxy('photo.jpg'); // NO carga aún
console.log('Proxy created');
image.display(); // Carga AHORA
```

#### Patrones de Comportamiento (Cómo objetos COLABORAN)

**7. Strategy - Algoritmos Intercambiables**

Problema: Múltiples formas de hacer algo, evitar if/else complejos.

```typescript
interface SortStrategy {
  sort(data: number[]): number[];
}

class QuickSort implements SortStrategy {
  sort(data: number[]): number[] {
    console.log('Using QuickSort');
    // Implementación
    return data.sort((a, b) => a - b);
  }
}

class MergeSort implements SortStrategy {
  sort(data: number[]): number[] {
    console.log('Using MergeSort');
    // Implementación
    return data.sort((a, b) => a - b);
  }
}

class Sorter {
  constructor(private strategy: SortStrategy) {}

  setStrategy(strategy: SortStrategy) {
    this.strategy = strategy;
  }

  sort(data: number[]): number[] {
    return this.strategy.sort(data);
  }
}

// Uso - cambiar estrategia en runtime
const sorter = new Sorter(new QuickSort());
sorter.sort([5, 2, 8]);

sorter.setStrategy(new MergeSort());
sorter.sort([5, 2, 8]);
```

**8. Observer - Notificaciones de Cambios**

Problema: Notificar múltiples objetos cuando cambia el estado de otro.

```typescript
interface Observer {
  update(subject: Subject): void;
}

interface Subject {
  attach(observer: Observer): void;
  detach(observer: Observer): void;
  notify(): void;
}

class StockMarket implements Subject {
  private observers: Observer[] = [];
  private stockPrices = new Map<string, number>();

  attach(observer: Observer) {
    this.observers.push(observer);
  }

  detach(observer: Observer) {
    const index = this.observers.indexOf(observer);
    if (index > -1) this.observers.splice(index, 1);
  }

  notify() {
    for (const observer of this.observers) {
      observer.update(this);
    }
  }

  setPrice(stock: string, price: number) {
    this.stockPrices.set(stock, price);
    this.notify();
  }

  getPrice(stock: string): number {
    return this.stockPrices.get(stock) || 0;
  }
}

class Investor implements Observer {
  constructor(private name: string) {}

  update(subject: Subject) {
    if (subject instanceof StockMarket) {
      const price = subject.getPrice('AAPL');
      console.log(`${this.name}: Apple price is ${price}`);
    }
  }
}

// Uso
const market = new StockMarket();
market.attach(new Investor('Alice'));
market.attach(new Investor('Bob'));
market.setPrice('AAPL', 150); // Notifica a todos
```

**9. Command - Encapsular Peticiones**

Problema: Encapsular petición como objeto (útil para undo/redo, queues).

```typescript
interface Command {
  execute(): void;
  undo(): void;
}

class CreateFileCommand implements Command {
  constructor(private filename: string) {}

  execute() {
    console.log(`Creating file: ${this.filename}`);
  }

  undo() {
    console.log(`Deleting file: ${this.filename}`);
  }
}

class CommandHistory {
  private history: Command[] = [];

  executeCommand(command: Command) {
    command.execute();
    this.history.push(command);
  }

  undo() {
    const command = this.history.pop();
    if (command) command.undo();
  }
}

// Uso
const history = new CommandHistory();
history.executeCommand(new CreateFileCommand('file.txt'));
history.undo(); // Revierte
```

---

## Arquitecturas Fundamentales y Modernas

### Arquitecturas Tradicionales

**1. Arquitectura Monolítica**

Descripción: Todo el código base y componentes están interconectados en una única unidad de despliegue.

```
┌────────────────────────────────┐
│      APLICACIÓN MONOLITO       │
│  ┌──────────────────────────┐  │
│  │    Presentación (UI)     │  │
│  ├──────────────────────────┤  │
│  │   Lógica de Negocio      │  │
│  ├──────────────────────────┤  │
│  │   Acceso a Datos (DAL)   │  │
│  └──────────────────────────┘  │
│              ↓                 │
│      ┌──────────────┐          │
│      │   Database   │          │
│      └──────────────┘          │
└────────────────────────────────┘
```

**Ventajas:**
- ✅ Simplicidad de desarrollo inicial
- ✅ Fácil de debuggear (todo en un lugar)
- ✅ Deployment sencillo (un solo artefacto)
- ✅ Performance (no hay latencia de red interna)

**Desventajas:**
- ❌ Escalabilidad limitada (escalar todo o nada)
- ❌ Despliegues riesgosos (todo o nada)
- ❌ Tecnología única (difícil cambiar stack)
- ❌ Código acoplado crece exponencialmente

**Cuándo usar:**
- Startups en MVP
- Equipos pequeños (<10 developers)
- Aplicaciones simples con dominio limitado

**Ejemplo real:**
```typescript
// app.ts - Monolito típico
import express from 'express';
import { userRoutes } from './routes/users';
import { productRoutes } from './routes/products';
import { orderRoutes } from './routes/orders';

const app = express();

// Todo en una app
app.use('/users', userRoutes);
app.use('/products', productRoutes);
app.use('/orders', orderRoutes);

// Una sola base de datos
const db = connectToDatabase();

app.listen(3000);
```

---

**2. Arquitectura Monolítica Modular**

Descripción: Estructura interna del monolito dividida en módulos bien definidos con acoplamiento limitado.

```
┌────────────────────────────────────────┐
│         MONOLITO MODULAR               │
│  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │  Módulo  │  │  Módulo  │  │Módulo│ │
│  │  Users   │  │ Products │  │Orders│ │
│  │          │  │          │  │      │ │
│  │ ┌──────┐ │  │ ┌──────┐ │  │┌────┐│ │
│  │ │Logic │ │  │ │Logic │ │  ││Lgc ││ │
│  │ ├──────┤ │  │ ├──────┤ │  │├────┤│ │
│  │ │ DAL  │ │  │ │ DAL  │ │  ││DAL ││ │
│  │ └──────┘ │  │ └──────┘ │  │└────┘│ │
│  └────┬─────┘  └────┬─────┘  └──┬───┘ │
│       └─────────────┼───────────┘     │
│                     ↓                  │
│            ┌─────────────────┐         │
│            │  Shared Database│         │
│            └─────────────────┘         │
└────────────────────────────────────────┘
```

**Ventajas:**
- ✅ Organización clara (separación de concerns)
- ✅ Equipos pueden trabajar en módulos separados
- ✅ Más fácil de mantener que monolito desorganizado
- ✅ Path hacia microservicios (módulos → servicios)

**Desventajas:**
- ❌ Aún deployado como uno solo
- ❌ Acoplamiento en DB
- ❌ Difícil reforzar boundaries (tentación de acoplar)

**Implementación:**
```typescript
// src/modules/users/users.module.ts
export class UsersModule {
  private repository: UserRepository;

  // Interfaz pública del módulo
  public createUser(data): Promise<User> {
    return this.repository.save(data);
  }

  public findUser(id): Promise<User> {
    return this.repository.findById(id);
  }

  // Métodos privados no expuestos
  private validateUser(user): boolean {
    // Lógica interna
  }
}

// src/modules/orders/orders.module.ts
export class OrdersModule {
  constructor(
    private usersModule: UsersModule  // Dependencia entre módulos
  ) {}

  public async createOrder(userId, products) {
    // Usa interfaz pública de UsersModule
    const user = await this.usersModule.findUser(userId);
    // Crear orden...
  }
}
```

**Patrón de Comunicación entre Módulos:**
```typescript
// Usar interfaces para desacoplar
interface IUserService {
  findUser(id: string): Promise<User>;
}

class OrdersModule {
  constructor(private userService: IUserService) {}
  // OrdersModule NO depende de implementación concreta
}
```

---

**3. Service-Oriented Architecture (SOA)**

Descripción: Colección de servicios grandes y autónomos que se comunican a través de un Enterprise Service Bus (ESB).

```
┌─────────────────────────────────────────┐
│        Enterprise Service Bus (ESB)     │
│    (Orquestación, Transformación)       │
└────┬─────────┬──────────┬──────────┬────┘
     │         │          │          │
     ↓         ↓          ↓          ↓
┌─────────┐ ┌─────────┐ ┌──────┐ ┌────────┐
│Customer │ │Inventory│ │Order │ │Payment │
│Service  │ │Service  │ │Svc   │ │Service │
└────┬────┘ └────┬────┘ └──┬───┘ └───┬────┘
     ↓           ↓          ↓         ↓
  ┌──────┐   ┌──────┐  ┌──────┐ ┌──────┐
  │  DB  │   │  DB  │  │  DB  │ │  DB  │
  └──────┘   └──────┘  └──────┘ └──────┘
```

**Características:**
- Servicios grandes (no micro)
- ESB maneja: routing, transformación, orquestación
- Protocolo pesado: SOAP, XML
- Gobernanza centralizada

**Ventajas:**
- ✅ Reutilización de servicios
- ✅ Interoperabilidad (diferentes tecnologías)
- ✅ Gobernanza centralizada

**Desventajas:**
- ❌ ESB = punto único de falla
- ❌ Complejidad del ESB
- ❌ Acoplamiento a través del ESB
- ❌ Performance (overhead de ESB)

**Diferencia SOA vs Microservicios:**

| Aspecto | SOA | Microservicios |
|---------|-----|----------------|
| **Tamaño servicio** | Grande (múltiples funcionalidades) | Pequeño (una funcionalidad) |
| **Comunicación** | ESB centralizado | Point-to-point (REST, gRPC) |
| **Gobernanza** | Centralizada | Descentralizada |
| **DB** | Puede compartir | Database per service |
| **Deployment** | Coordinado | Independiente |

**Cuándo usar SOA:**
- Grandes empresas con sistemas legacy
- Necesidad de interoperabilidad entre sistemas antiguos
- Gobernanza estricta requerida

---

**4. Cliente-Servidor**

Descripción: Aplicación dividida entre Cliente (solicita servicios) y Servidor (los provee).

```
┌──────────────┐               ┌──────────────┐
│   CLIENTE    │               │   SERVIDOR   │
│              │               │              │
│  - UI/UX     │───Request────▶│  - Lógica    │
│  - Validación│               │  - DB Access │
│  - Cache     │◀──Response────│  - Procesar  │
│              │               │              │
└──────────────┘               └──────────────┘

Ejemplos:
- Navegador (cliente) ↔ API (servidor)
- App móvil (cliente) ↔ Backend (servidor)
- Desktop app (cliente) ↔ Database server
```

**Variantes:**

**Thin Client (Cliente Ligero):**
```
Cliente simple (HTML/CSS)
Todo el procesamiento en servidor
Ejemplo: Apps web tradicionales (server-side rendering)
```

**Thick Client (Cliente Pesado):**
```
Cliente con lógica (React, Angular)
Servidor solo provee datos (API REST)
Ejemplo: SPAs, Apps móviles
```

**Implementación típica:**
```typescript
// SERVIDOR (Node.js + Express)
app.get('/api/users', async (req, res) => {
  const users = await db.query('SELECT * FROM users');
  res.json(users);
});

// CLIENTE (React)
function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  return <ul>{users.map(u => <li>{u.name}</li>)}</ul>;
}
```

---

**5. Maestro-Esclavo (Master-Slave)**

Descripción: Nodo principal (Maestro) distribuye tareas a nodos secundarios (Esclavos) que procesan y devuelven resultado.

```
                  ┌─────────────┐
                  │   MAESTRO   │
                  │  (Coordina) │
                  └──────┬──────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ↓                ↓                ↓
  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ ESCLAVO 1│    │ ESCLAVO 2│    │ ESCLAVO 3│
  │(Procesa) │    │(Procesa) │    │(Procesa) │
  └────┬─────┘    └────┬─────┘    └────┬─────┘
       │               │               │
       └───────────────┴───────────────┘
                       │
                  (Resultados)
```

**Casos de uso:**

**1. Bases de Datos Replicadas:**
```
Master DB (Escrituras)
  ↓ (replica)
Slave DB 1, 2, 3 (Solo lecturas)

Ventaja: Escalabilidad de lecturas
```

**2. Procesamiento Distribuido:**
```python
# Maestro distribuye trabajo
class Master:
    def process_large_dataset(self, data):
        chunks = self.split(data, num_slaves=3)

        results = []
        for i, chunk in enumerate(chunks):
            result = self.send_to_slave(i, chunk)
            results.append(result)

        return self.merge(results)

# Esclavo procesa su chunk
class Slave:
    def process(self, chunk):
        return [transform(item) for item in chunk]
```

**3. MapReduce (Hadoop):**
```
Master (JobTracker)
  ↓ (asigna tareas)
Slaves (TaskTrackers) ejecutan Map y Reduce
```

**Ventajas:**
- ✅ Escalabilidad (añadir más esclavos)
- ✅ Tolerancia a fallos (esclavo cae, maestro reasigna)
- ✅ Separación de lecturas/escrituras (en DBs)

**Desventajas:**
- ❌ Maestro = punto único de falla
- ❌ Complejidad de coordinación
- ❌ Latencia de comunicación

---

### Arquitecturas Cloud Native y Modernas

**6. Arquitectura Cloud Native**

Descripción: Diseño de sistemas para operar nativamente en entornos de nube, usando contenedores, orquestación y serverless.

```
┌─────────────────────────────────────────────────┐
│           CLOUD NATIVE STACK                    │
│                                                 │
│  ┌────────────────────────────────────────┐    │
│  │  Kubernetes (Orquestación)             │    │
│  │  ┌──────┐  ┌──────┐  ┌──────┐         │    │
│  │  │ Pod  │  │ Pod  │  │ Pod  │         │    │
│  │  │┌────┐│  │┌────┐│  │┌────┐│         │    │
│  │  ││Cont││  ││Cont││  ││Cont││         │    │
│  │  │└────┘│  │└────┘│  │└────┘│         │    │
│  │  └──────┘  └──────┘  └──────┘         │    │
│  └────────────────────────────────────────┘    │
│                                                 │
│  ┌────────────────────────────────────────┐    │
│  │  Serverless (FaaS)                     │    │
│  │  Lambda │ Cloud Functions │ Azure Fnc  │    │
│  └────────────────────────────────────────┘    │
│                                                 │
│  ┌────────────────────────────────────────┐    │
│  │  Service Mesh (Istio/Linkerd)          │    │
│  │  - mTLS  - Load Balancing  - Tracing   │    │
│  └────────────────────────────────────────┘    │
│                                                 │
│  ┌────────────────────────────────────────┐    │
│  │  Managed Services                      │    │
│  │  RDS │ S3 │ CloudWatch │ Secrets Mgr   │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

**Principios Cloud Native:**

1. **Contenedores** (Portabilidad)
2. **Orquestación** (Kubernetes)
3. **Microservicios** (Escalabilidad independiente)
4. **Immutable Infrastructure** (IaC - Terraform)
5. **Declarative APIs** (Kubernetes manifests)
6. **Observability** (Logs, Metrics, Traces)

**Ejemplo completo:**
```yaml
# deployment.yaml (Kubernetes)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment
  template:
    metadata:
      labels:
        app: payment
    spec:
      containers:
      - name: payment
        image: myapp/payment:v1.2.3
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080

---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: payment-service
spec:
  selector:
    app: payment
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer

---
# hpa.yaml (Auto-scaling)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Cuándo usar Cloud Native:**
- Escalabilidad variable (traffic spikes)
- Multi-región/Alta disponibilidad
- Deployment frecuente
- Equipos DevOps maduros

---

**7. Event-Driven Architecture (Dirigida por Eventos)**

Descripción: Componentes se comunican asíncronamente reaccionando a eventos usando message brokers.

```
┌──────────────┐      Evento        ┌──────────────┐
│  PRODUCTOR   │──────────────────▶│ MESSAGE      │
│  (Publisher) │  "OrderCreated"    │ BROKER       │
└──────────────┘                    │ (Kafka/      │
                                    │ RabbitMQ)    │
                                    └──────┬───────┘
                                           │
                    ┌──────────────────────┼──────────────────┐
                    │                      │                  │
                    ↓                      ↓                  ↓
            ┌───────────────┐     ┌───────────────┐  ┌──────────────┐
            │  CONSUMIDOR 1 │     │ CONSUMIDOR 2  │  │ CONSUMIDOR 3 │
            │  (Inventory)  │     │ (Notification)│  │ (Analytics)  │
            └───────────────┘     └───────────────┘  └──────────────┘
```

**Patrones Event-Driven:**

**1. Pub/Sub (Publish/Subscribe):**
```typescript
// Publicar evento
await eventBus.publish('order.created', {
  orderId: '123',
  userId: 'user-456',
  total: 99.99,
  timestamp: new Date()
});

// Múltiples suscriptores
eventBus.subscribe('order.created', async (event) => {
  // Servicio 1: Actualizar inventario
  await inventory.reserve(event.orderId);
});

eventBus.subscribe('order.created', async (event) => {
  // Servicio 2: Enviar email
  await email.send(event.userId, 'Order Confirmation');
});

eventBus.subscribe('order.created', async (event) => {
  // Servicio 3: Analytics
  await analytics.track('order_created', event);
});
```

**2. Event Sourcing (ya visto anteriormente)**

**3. CQRS + Events:**
```
Command → Write Model → Event → Read Model(s)
```

**Implementación con Kafka:**
```typescript
// Producer
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: ['kafka1:9092', 'kafka2:9092']
});

const producer = kafka.producer();

async function createOrder(order) {
  // Guardar en DB
  const saved = await db.orders.insert(order);

  // Publicar evento
  await producer.send({
    topic: 'orders',
    messages: [{
      key: saved.id,
      value: JSON.stringify({
        type: 'OrderCreated',
        data: saved,
        timestamp: Date.now()
      })
    }]
  });
}

// Consumer
const consumer = kafka.consumer({ groupId: 'inventory-service' });

await consumer.subscribe({ topic: 'orders' });

await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    const event = JSON.parse(message.value.toString());

    if (event.type === 'OrderCreated') {
      await handleOrderCreated(event.data);
    }
  }
});
```

**Ventajas:**
- ✅ Desacoplamiento total
- ✅ Escalabilidad (consumidores independientes)
- ✅ Resiliencia (broker persiste eventos)
- ✅ Auditoría (todos los eventos registrados)

**Desventajas:**
- ❌ Complejidad (debugging distribuido)
- ❌ Consistencia eventual (no inmediata)
- ❌ Ordenamiento complicado

---

**8. Microkernel (Plugin Architecture)**

Descripción: Núcleo mínimo con funcionalidades añadidas como plugins/extensiones.

```
┌────────────────────────────────────────┐
│                                        │
│  ┌────────────────────────────────┐   │
│  │      MICROKERNEL CORE          │   │
│  │  - Plugin registry             │   │
│  │  - Plugin lifecycle manager    │   │
│  │  - Core functionality          │   │
│  └────────────┬───────────────────┘   │
│               │                        │
│    ┌──────────┼──────────┐            │
│    │          │          │            │
│    ↓          ↓          ↓            │
│ ┌───────┐ ┌───────┐ ┌────────┐       │
│ │Plugin │ │Plugin │ │ Plugin │       │
│ │   A   │ │   B   │ │   C    │       │
│ └───────┘ └───────┘ └────────┘       │
│                                        │
└────────────────────────────────────────┘
```

**Ejemplos reales:**
- **VS Code**: Core + extensiones
- **WordPress**: Core + plugins
- **Browsers**: Core + extensions
- **Eclipse IDE**: Core + plugins

**Implementación:**
```typescript
// Core
interface Plugin {
  name: string;
  version: string;
  activate(context: PluginContext): void;
  deactivate(): void;
}

class PluginRegistry {
  private plugins: Map<string, Plugin> = new Map();

  register(plugin: Plugin) {
    this.plugins.set(plugin.name, plugin);
    plugin.activate(this.getContext());
  }

  unregister(name: string) {
    const plugin = this.plugins.get(name);
    if (plugin) {
      plugin.deactivate();
      this.plugins.delete(name);
    }
  }

  getContext(): PluginContext {
    return {
      registerCommand: this.registerCommand.bind(this),
      registerView: this.registerView.bind(this),
      // API del core disponible para plugins
    };
  }
}

// Plugin Example
class ThemePlugin implements Plugin {
  name = 'dark-theme';
  version = '1.0.0';

  activate(context: PluginContext) {
    context.registerCommand('theme.toggle', () => {
      document.body.classList.toggle('dark-mode');
    });
  }

  deactivate() {
    // Cleanup
  }
}

// Uso
const registry = new PluginRegistry();
registry.register(new ThemePlugin());
```

**Ventajas:**
- ✅ Extensibilidad ilimitada
- ✅ Core mínimo y estable
- ✅ Plugins independientes
- ✅ Actualización sin afectar core

**Desventajas:**
- ❌ Performance overhead (plugins loading)
- ❌ Seguridad (plugins maliciosos)
- ❌ Versioning (compatibilidad plugins)

---

**9. Backend for Frontend (BFF)**

Descripción: Capa de servicio específica construida para cada tipo de cliente, optimizando payload y llamadas.

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Web App   │         │ Mobile App  │         │   IoT App   │
│  (Desktop)  │         │  (Phone)    │         │  (Device)   │
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       │                       │                       │
       ↓                       ↓                       ↓
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   BFF-Web   │         │ BFF-Mobile  │         │  BFF-IoT    │
│- Aggregation│         │- Optimized  │         │- Minimal    │
│- Transform  │         │  payload    │         │  data       │
│- Cache      │         │- Batching   │         │- Binary     │
└──────┬──────┘         └──────┬──────┘         └──────┬──────┘
       └────────────────────────┼────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ↓                       ↓
              ┌──────────┐           ┌──────────┐
              │ Users    │           │ Products │
              │ Service  │           │ Service  │
              └──────────┘           └──────────┘
```

**Problema que resuelve:**

Sin BFF:
```
Mobile App hace 5 llamadas para una pantalla:
1. GET /users/me
2. GET /products?category=X
3. GET /cart
4. GET /recommendations
5. GET /promotions

= 5 round-trips, mucho payload, slow
```

Con BFF:
```
Mobile App hace 1 llamada:
GET /bff-mobile/home

BFF internamente:
- Llama a 5 servicios en paralelo
- Agrega datos
- Filtra campos innecesarios
- Retorna payload optimizado

= 1 round-trip, menos datos, fast
```

**Implementación:**
```typescript
// BFF para Web (payload completo, features ricas)
app.get('/bff-web/product/:id', async (req, res) => {
  const [product, reviews, recommendations, inventory] = await Promise.all([
    productService.get(req.params.id),
    reviewService.getReviews(req.params.id),
    recommendationService.getSimilar(req.params.id),
    inventoryService.getStock(req.params.id)
  ]);

  res.json({
    product: product,  // Objeto completo
    reviews: reviews.map(r => ({
      ...r,
      userProfile: r.user  // Nested data OK
    })),
    recommendations: recommendations,
    inventory: inventory
  });
});

// BFF para Mobile (payload mínimo, optimizado)
app.get('/bff-mobile/product/:id', async (req, res) => {
  const [product, reviews, stock] = await Promise.all([
    productService.get(req.params.id),
    reviewService.getReviews(req.params.id, { limit: 3 }),  // Solo 3
    inventoryService.getStock(req.params.id)
  ]);

  res.json({
    // Solo campos esenciales
    id: product.id,
    name: product.name,
    price: product.price,
    image: product.thumbnailUrl,  // Thumbnail, no full image
    rating: reviews.avgRating,  // Agregado, no lista
    inStock: stock > 0
    // NO incluye: descripción larga, reviews individuales, etc.
  });
});

// BFF para IoT (payload ultra mínimo, binario)
app.get('/bff-iot/product/:id', async (req, res) => {
  const stock = await inventoryService.getStock(req.params.id);

  // Respuesta binaria ultra compacta
  res.send(Buffer.from([stock > 0 ? 1 : 0]));
});
```

**Cuándo usar BFF:**
- Múltiples tipos de clientes (Web, Mobile, IoT)
- Necesidades diferentes de datos
- Performance crítica en mobile
- Equipos frontend autónomos

**Alternativa sin BFF:**
GraphQL (cliente decide qué campos necesita)

---

## Patrones Arquitectónicos Modernos

### Patrones de Microservicios

**10. Strangler Fig - Migración Gradual de Monolito**

Problema: Migrar monolito a microservicios sin big bang rewrite.

```
FASE 1:
Usuario → Proxy → Monolito

FASE 2:
Usuario → Proxy → ┌→ Payments Service (nuevo)
                   └→ Monolito (resto)

FASE N:
Usuario → API Gateway → ┌→ Payments
                         ├→ Users
                         ├→ Orders
                         └→ Inventory
```

**Implementación:**
```typescript
// Proxy con routing
app.use('/api/payments', proxy({
  target: 'http://payments-service:3001'
}));

// Todo lo demás al monolito
app.use('/*', proxy({
  target: 'http://legacy-monolith:8080'
}));
```

**11. Saga - Transacciones Distribuidas**

Problema: No hay transacciones ACID en microservicios distribuidos.

Solución: Secuencia de transacciones locales con compensación.

```
SAGA EXITOSO:
1. Order Service: createOrder() ✅
2. Payment Service: processPayment() ✅
3. Inventory Service: reserveItem() ✅
✅ Completo

SAGA FALLIDO:
1. Order Service: createOrder() ✅
2. Payment Service: processPayment() ✅
3. Inventory Service: reserveItem() ❌ FALLA

COMPENSACIÓN (reversa):
3. (nada que compensar)
2. Payment Service: refundPayment() ✅
1. Order Service: cancelOrder() ✅
```

**Implementación Orchestration:**
```typescript
class CheckoutSaga {
  async execute(order) {
    const steps = [];

    try {
      const orderResult = await orderService.create(order);
      steps.push({ step: 'createOrder', data: orderResult });

      const paymentResult = await paymentService.process(order);
      steps.push({ step: 'processPayment', data: paymentResult });

      const inventoryResult = await inventoryService.reserve(order);
      steps.push({ step: 'reserveInventory', data: inventoryResult });

      return { success: true };

    } catch (error) {
      await this.compensate(steps);
      return { success: false };
    }
  }

  async compensate(steps) {
    for (const step of steps.reverse()) {
      switch (step.step) {
        case 'reserveInventory':
          await inventoryService.release(step.data);
          break;
        case 'processPayment':
          await paymentService.refund(step.data);
          break;
        case 'createOrder':
          await orderService.cancel(step.data);
          break;
      }
    }
  }
}
```

**12. Circuit Breaker - Evitar Cascadas de Fallos**

Problema: Servicio caído causa cascada de fallos.

Solución: "Abrir circuito" después de N fallos consecutivos.

```typescript
class CircuitBreaker {
  private failures = 0;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private threshold = 5;
  private timeout = 60000; // 1 minuto

  async call(fn: () => Promise<any>) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit breaker is OPEN');
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  private onFailure() {
    this.failures++;
    if (this.failures >= this.threshold) {
      this.state = 'OPEN';
      setTimeout(() => {
        this.state = 'HALF_OPEN';
      }, this.timeout);
    }
  }
}

// Uso
const breaker = new CircuitBreaker();
await breaker.call(() => externalService.call());
```

**13. CQRS - Separar Lecturas y Escrituras**

Problema: Lecturas y escrituras tienen necesidades diferentes.

```
Commands (Write) → Write DB (normalizado)
                      ↓ (eventos)
Queries (Read) ← Read DB (denormalizado, optimizado)
```

**Cuándo usar:**
- Alta carga de lecturas vs escrituras
- Event sourcing
- Necesidad de vistas optimizadas diferentes

**14. Event Sourcing - Guardar Eventos, No Estado**

Problema: Necesidad de auditoría completa, debugging temporal.

```
Estado tradicional:
user = { name: 'John', balance: 100 }

Event Sourcing:
eventos = [
  { type: 'UserCreated', name: 'John', balance: 0 },
  { type: 'DepositMade', amount: 150 },
  { type: 'WithdrawalMade', amount: 50 }
]

Estado actual = replay(eventos)
user.balance = 0 + 150 - 50 = 100
```

**Ventajas:**
- Auditoría completa
- Time travel (estado en cualquier momento)
- Event replay para debugging

**Desventajas:**
- Complejidad
- Storage crece ilimitadamente

---

## Patrones de IA y Machine Learning

### 15. RAG (Retrieval Augmented Generation)

Problema: LLM no conoce tu información específica.

Solución: Buscar documentos relevantes y pasarlos al LLM.

```python
def rag_query(question):
  # 1. Retrieve - Buscar docs relevantes
  question_embedding = get_embedding(question)
  docs = vector_db.query(question_embedding, top_k=3)

  # 2. Augment - Crear prompt con contexto
  context = '\n\n'.join(docs)
  prompt = f'''Context: {context}

Question: {question}

Answer based ONLY on the context.'''

  # 3. Generate - LLM responde
  response = llm.generate(prompt)
  return response
```

**Arquitectura:**
```
User Question
  ↓
Embedding Model
  ↓
Vector DB Search → Top 3 docs relevantes
  ↓
Prompt Augmentation
  ↓
LLM (GPT-4)
  ↓
Response
```

**16. Prompt Chaining - Tareas Multi-Paso**

Problema: Tarea compleja para un solo prompt.

Solución: Secuencia de prompts, cada uno procesa output del anterior.

```python
# Step 1: Extract entities
entities = llm.generate(f"Extract people and places from: {text}")

# Step 2: Classify sentiment
sentiment = llm.generate(f"Sentiment of: {text}")

# Step 3: Generate summary using previous results
summary = llm.generate(f"""
Entities: {entities}
Sentiment: {sentiment}
Text: {text}

Write a 2-sentence summary.
""")
```

**17. Agent with Tools - LLM con Acceso a APIs**

Problema: LLM necesita acceder a datos externos, ejecutar acciones.

```python
from langgraph import Agent, Tool

tools = [
  Tool('search_db', search_database),
  Tool('send_email', send_email),
  Tool('create_ticket', create_ticket)
]

agent = Agent(
  model='gpt-4',
  tools=tools,
  system_prompt='You are a support agent. Use tools to help users.'
)

# Agente decide qué tool usar
response = agent.run("Create a ticket for order #123")
# Agente ejecuta: create_ticket(order_id='123')
```

**18. Multi-Agent System - Agentes Especializados**

Problema: Tarea requiere múltiples especialidades.

```
User Query
  ↓
Router Agent (decide qué agente usar)
  ↓
  ├→ Research Agent (busca información)
  ├→ Coding Agent (escribe código)
  ├→ Review Agent (revisa output)
  └→ Summary Agent (consolida resultados)
```

**19. Model as Service - Inferencia como API**

Problema: Modelo ML necesita servir predicciones.

```python
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load('fraud_model.pkl')

@app.post('/predict')
async def predict(transaction: dict):
  features = extract_features(transaction)
  prediction = model.predict([features])[0]

  return {
    'is_fraud': bool(prediction),
    'confidence': float(model.predict_proba([features])[0][1])
  }
```

**20. A/B Testing for Models - Validar Mejoras**

Problema: ¿Nuevo modelo es realmente mejor?

```python
import random

def get_model(user_id):
  # 90% modelo actual, 10% modelo nuevo
  if hash(user_id) % 100 < 10:
    return new_model
  return current_model

@app.post('/predict')
async def predict(user_id, data):
  model = get_model(user_id)
  prediction = model.predict(data)

  # Log para análisis
  log_prediction(user_id, model.version, prediction)

  return prediction
```

---

### Arquitecturas de Datos e IA Avanzadas

**21. MLOps Pipeline - CI/CD para Machine Learning**

Problema: Los modelos ML necesitan versionado, testing, deployment y monitoreo continuo.

Solución: Pipeline completo desde entrenamiento hasta producción con rollback automático.

```
┌─────────────────────────────────────────────────────────┐
│                   MLOps Pipeline                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Data → Feature → Training → Validation → Registry →   │
│         Store                                  Deploy   │
│           ↓         ↓           ↓         ↓      ↓     │
│         DVC      MLflow      pytest    Model   k8s     │
│                                        Version          │
│                                                         │
│  Production → Monitoring → Drift Detection → Retrain   │
│                  ↓             ↓              ↓         │
│              Prometheus    Evidently      Trigger      │
└─────────────────────────────────────────────────────────┘
```

**Implementación con MLflow y GitHub Actions:**

```python
# train.py
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd

def train_model(data_version: str):
    # Setup MLflow
    mlflow.set_experiment("fraud-detection")

    with mlflow.start_run():
        # Log parámetros
        mlflow.log_param("data_version", data_version)
        mlflow.log_param("model_type", "RandomForest")

        # Cargar datos (versionados con DVC)
        X_train, y_train = load_data(data_version)

        # Entrenar
        model = RandomForestClassifier(n_estimators=100, max_depth=10)
        model.fit(X_train, y_train)

        # Evaluar
        X_test, y_test = load_test_data()
        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        f1 = f1_score(y_test, predictions)

        # Log métricas
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)

        # Guardar modelo
        mlflow.sklearn.log_model(model, "model")

        # Auto-promote si supera threshold
        if accuracy > 0.95 and f1 > 0.90:
            client = mlflow.tracking.MlflowClient()
            model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
            client.create_model_version(
                name="fraud-detector",
                source=model_uri,
                run_id=mlflow.active_run().info.run_id
            )
            # Promover a producción
            client.transition_model_version_stage(
                name="fraud-detector",
                version=get_latest_version(),
                stage="Production"
            )

# GitHub Actions Pipeline (.github/workflows/mlops.yml)
```

```yaml
name: MLOps Pipeline

on:
  push:
    paths:
      - 'data/**'
      - 'models/**'
  schedule:
    - cron: '0 2 * * 0'  # Retrain semanalmente

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install mlflow scikit-learn dvc pandas

      - name: Pull data from DVC
        run: dvc pull

      - name: Train model
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
        run: python train.py

      - name: Run model tests
        run: |
          pytest tests/model_tests.py
          pytest tests/data_validation.py

  deploy:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to SageMaker
        run: |
          # Get production model from MLflow
          model_uri = mlflow.get_production_model("fraud-detector")

          # Deploy
          aws sagemaker create-model --model-name fraud-detector-v${VERSION}
          aws sagemaker create-endpoint-config --endpoint-config-name fraud-config
          aws sagemaker update-endpoint --endpoint-name fraud-api

  monitor:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - name: Setup monitoring
        run: |
          # Evidently AI para drift detection
          python setup_monitoring.py
```

**Monitoreo de Drift:**

```python
# monitoring.py
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd

def check_drift(reference_data, current_data):
    """
    Detecta si los datos en producción han cambiado (drift)
    """
    report = Report(metrics=[DataDriftPreset()])

    report.run(
        reference_data=reference_data,
        current_data=current_data
    )

    drift_detected = report.as_dict()['metrics'][0]['result']['dataset_drift']

    if drift_detected:
        # Trigger retrain
        trigger_retraining_pipeline()
        send_alert("Model drift detected! Retraining initiated.")

    return drift_detected
```

**Cuándo usar MLOps:**
- Modelos en producción que requieren actualizaciones frecuentes
- Equipos que necesitan experimentar rápidamente
- Necesidad de auditoría y reproducibilidad
- Detección de degradación del modelo

**Componentes clave:**
- **Feature Store:** Centralizar features (Feast, Tecton)
- **Model Registry:** Versionar modelos (MLflow, SageMaker)
- **Monitoring:** Drift, performance, data quality
- **A/B Testing:** Comparar versiones de modelos

---

**22. API Gateway - Punto de Entrada Único**

Problema: Clientes no deben conocer todos los microservicios. Necesitas autenticación, rate limiting, routing centralizado.

Solución: API Gateway como proxy inteligente.

```
┌──────────────────────────────────────────────────────┐
│                  API Gateway                         │
│  (Kong / AWS API Gateway / Envoy / Azure APIM)      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Auth        │  │ Rate Limit   │  │  Routing   │ │
│  │ (JWT check) │  │ (100 req/min)│  │  (path→svc)│ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Caching    │  │  Transform   │  │   Logs     │ │
│  │  (Redis)    │  │  (Response)  │  │ (Analytics)│ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└──────────────────────────────────────────────────────┘
          │                │              │
          ↓                ↓              ↓
    ┌─────────┐      ┌─────────┐    ┌─────────┐
    │ Users   │      │ Orders  │    │Payments │
    │ Service │      │ Service │    │ Service │
    └─────────┘      └─────────┘    └─────────┘
```

**Implementación con Kong (config declarativa):**

```yaml
# kong.yml
_format_version: "2.1"

services:
  - name: users-service
    url: http://users-service:3001
    routes:
      - name: users-route
        paths:
          - /api/users
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: cors

  - name: orders-service
    url: http://orders-service:3002
    routes:
      - name: orders-route
        paths:
          - /api/orders
    plugins:
      - name: jwt
      - name: request-transformer
        config:
          add:
            headers:
              - X-Service:orders
      - name: response-transformer
        config:
          remove:
            headers:
              - X-Internal-Token

  - name: payments-service
    url: http://payments-service:3003
    routes:
      - name: payments-route
        paths:
          - /api/payments
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 50  # Más restrictivo
      - name: proxy-cache
        config:
          strategy: memory
          content_type:
            - application/json

# Plugin de autenticación JWT
plugins:
  - name: jwt
    config:
      secret_is_base64: false
      key_claim_name: iss
```

**Implementación custom con Node.js (Express Gateway):**

```typescript
// gateway.ts
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import rateLimit from 'express-rate-limit';
import jwt from 'jsonwebtoken';
import Redis from 'ioredis';

const app = express();
const redis = new Redis();

// Middleware de autenticación
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

// Rate limiting
const limiter = rateLimit({
  store: new RedisStore({ client: redis }),
  windowMs: 60 * 1000, // 1 minuto
  max: 100,
  message: 'Too many requests'
});

// Cache middleware
const cacheMiddleware = (duration: number) => {
  return async (req, res, next) => {
    const key = `cache:${req.originalUrl}`;
    const cached = await redis.get(key);

    if (cached) {
      return res.json(JSON.parse(cached));
    }

    // Override res.json para cachear
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      redis.setex(key, duration, JSON.stringify(data));
      return originalJson(data);
    };

    next();
  };
};

// Rutas con proxy
app.use('/api/users',
  authMiddleware,
  limiter,
  createProxyMiddleware({
    target: 'http://users-service:3001',
    changeOrigin: true,
    pathRewrite: { '^/api/users': '/users' }
  })
);

app.use('/api/orders',
  authMiddleware,
  limiter,
  createProxyMiddleware({
    target: 'http://orders-service:3002',
    changeOrigin: true
  })
);

app.use('/api/products',
  limiter,
  cacheMiddleware(300), // Cache 5 minutos
  createProxyMiddleware({
    target: 'http://products-service:3003',
    changeOrigin: true
  })
);

// Health check agregado
app.get('/health', async (req, res) => {
  const services = ['users', 'orders', 'products'];
  const health = await Promise.all(
    services.map(async (svc) => {
      try {
        await fetch(`http://${svc}-service/health`);
        return { service: svc, status: 'healthy' };
      } catch {
        return { service: svc, status: 'unhealthy' };
      }
    })
  );

  res.json({ services: health });
});

app.listen(8000);
```

**Cuándo usar API Gateway:**
- Arquitectura de microservicios
- Necesidad de autenticación centralizada
- Rate limiting por cliente
- Transformación de requests/responses
- Analytics y logging centralizado

**Alternativas:**
- **Service Mesh (Istio):** Para comunicación service-to-service
- **BFF (Backend for Frontend):** Si cada cliente necesita lógica específica

---

**23. Patrón Pipeline - Procesamiento en Etapas**

Problema: Necesitas procesar datos en múltiples pasos transformacionales.

Solución: Cadena de procesadores donde output de uno es input del siguiente.

```
Input → [Filter] → [Transform] → [Validate] → [Enrich] → [Store] → Output
```

**Ejemplo: Pipeline de procesamiento de imágenes**

```python
# pipeline.py
from abc import ABC, abstractmethod
from typing import Any
from PIL import Image
import numpy as np

class PipelineStage(ABC):
    """Etapa base del pipeline"""

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

    def __or__(self, other: 'PipelineStage'):
        """Permite sintaxis: stage1 | stage2 | stage3"""
        return Pipeline([self, other])

class Pipeline:
    def __init__(self, stages: list[PipelineStage]):
        self.stages = stages

    def process(self, data: Any) -> Any:
        result = data
        for stage in self.stages:
            result = stage.process(result)
        return result

    def __or__(self, other: PipelineStage):
        return Pipeline(self.stages + [other])

# Implementación de stages
class ResizeImage(PipelineStage):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def process(self, image: Image) -> Image:
        return image.resize((self.width, self.height))

class ConvertToGrayscale(PipelineStage):
    def process(self, image: Image) -> Image:
        return image.convert('L')

class NormalizePixels(PipelineStage):
    def process(self, image: Image) -> np.ndarray:
        arr = np.array(image)
        return arr / 255.0  # Normalizar a [0, 1]

class DetectEdges(PipelineStage):
    def process(self, image_array: np.ndarray) -> np.ndarray:
        # Sobel filter
        from scipy import ndimage
        edges = ndimage.sobel(image_array)
        return edges

class SaveResult(PipelineStage):
    def __init__(self, path: str):
        self.path = path

    def process(self, data: np.ndarray) -> np.ndarray:
        Image.fromarray((data * 255).astype(np.uint8)).save(self.path)
        return data

# Uso del pipeline
image_pipeline = (
    ResizeImage(512, 512) |
    ConvertToGrayscale() |
    NormalizePixels() |
    DetectEdges() |
    SaveResult('output.png')
)

# Procesar imagen
input_image = Image.open('input.jpg')
result = image_pipeline.process(input_image)
```

**Pipeline de datos (ETL):**

```python
# etl_pipeline.py
class ExtractCSV(PipelineStage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def process(self, _) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

class FilterInvalidRows(PipelineStage):
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        # Eliminar rows con valores nulos en columnas críticas
        return df.dropna(subset=['user_id', 'timestamp', 'amount'])

class TransformDates(PipelineStage):
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        return df

class EnrichWithUserData(PipelineStage):
    def __init__(self, user_db):
        self.user_db = user_db

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        # Join con datos de usuarios
        users = self.user_db.get_all_users()
        return df.merge(users, on='user_id', how='left')

class AggregateMetrics(PipelineStage):
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(['date', 'user_id']).agg({
            'amount': ['sum', 'mean', 'count'],
            'transaction_id': 'count'
        }).reset_index()

class LoadToWarehouse(PipelineStage):
    def __init__(self, warehouse):
        self.warehouse = warehouse

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        self.warehouse.bulk_insert('daily_metrics', df)
        return df

# Pipeline completo
etl_pipeline = (
    ExtractCSV('transactions.csv') |
    FilterInvalidRows() |
    TransformDates() |
    EnrichWithUserData(user_database) |
    AggregateMetrics() |
    LoadToWarehouse(data_warehouse)
)

# Ejecutar
result = etl_pipeline.process(None)
```

**Pipeline asíncrono (para ML inference):**

```python
import asyncio
from typing import TypeVar

T = TypeVar('T')

class AsyncPipelineStage(ABC):
    @abstractmethod
    async def process(self, data: T) -> T:
        pass

class AsyncPipeline:
    def __init__(self, stages: list[AsyncPipelineStage]):
        self.stages = stages

    async def process(self, data: Any) -> Any:
        result = data
        for stage in self.stages:
            result = await stage.process(result)
        return result

# Stages asíncronos
class LoadImage(AsyncPipelineStage):
    async def process(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

class RunModelInference(AsyncPipelineStage):
    async def process(self, image_bytes: bytes) -> dict:
        # Llamada asíncrona a modelo
        result = await model_api.predict(image_bytes)
        return result

class StoreResult(AsyncPipelineStage):
    async def process(self, prediction: dict) -> dict:
        await database.insert('predictions', prediction)
        return prediction

# Uso
inference_pipeline = AsyncPipeline([
    LoadImage(),
    RunModelInference(),
    StoreResult()
])

result = await inference_pipeline.process('https://example.com/image.jpg')
```

**Cuándo usar Pipeline:**
- Procesamiento de datos en múltiples etapas
- ETL (Extract, Transform, Load)
- Procesamiento de imágenes/video
- Compiladores (lexer → parser → optimizer → codegen)
- Pipelines de ML (preprocessing → training → evaluation)

**Ventajas:**
- Separación de responsabilidades (cada stage hace una cosa)
- Fácil testing (testear cada stage por separado)
- Reusabilidad (combinar stages diferentes)
- Paralelización (stages independientes pueden ejecutarse en paralelo)

---

**24. Arquitectura de Streaming - Procesamiento en Tiempo Real**

Problema: Necesitas procesar millones de eventos por segundo en tiempo real.

Solución: Stream processing con Kafka, Flink o Kinesis.

```
┌─────────────────────────────────────────────────────────┐
│            Arquitectura de Streaming                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Producers → Kafka Topics → Stream Processors → Sinks  │
│                                                         │
│  ┌─────────┐     ┌──────────┐     ┌──────────┐        │
│  │IoT      │     │ Topic:   │     │ Flink    │        │
│  │Devices  │────→│ sensor-  │────→│ Job      │───┐    │
│  │(1M/sec) │     │ events   │     │          │   │    │
│  └─────────┘     └──────────┘     └──────────┘   │    │
│                                         │          │    │
│  ┌─────────┐     ┌──────────┐          ↓          ↓    │
│  │Web      │     │ Topic:   │     ┌──────────┐ ┌─────┐│
│  │Clicks   │────→│ clicks   │     │ Aggreg.  │ │ DB  ││
│  └─────────┘     └──────────┘     │ Window   │ └─────┘│
│                                    └──────────┘        │
│                                         │              │
│                                         ↓              │
│                                    ┌──────────┐        │
│                                    │ Alerts   │        │
│                                    │ (>threshold)│     │
│                                    └──────────┘        │
└─────────────────────────────────────────────────────────┘
```

**Implementación con Kafka + Kafka Streams:**

```java
// StreamingApp.java
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.*;
import java.time.Duration;

public class RealTimeAnalytics {

    public static void main(String[] args) {
        StreamsBuilder builder = new StreamsBuilder();

        // Input stream: clicks de usuarios
        KStream<String, ClickEvent> clicks = builder.stream("user-clicks");

        // Transformación 1: Filtrar clicks válidos
        KStream<String, ClickEvent> validClicks = clicks
            .filter((key, event) -> event.getUserId() != null)
            .filter((key, event) -> event.getTimestamp() > 0);

        // Transformación 2: Contar clicks por usuario en ventanas de 5 minutos
        KTable<Windowed<String>, Long> clicksPerUser = validClicks
            .groupByKey()
            .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
            .count();

        // Transformación 3: Detectar usuarios anómalos (>100 clicks en 5 min)
        clicksPerUser
            .toStream()
            .filter((windowedKey, count) -> count > 100)
            .map((windowedKey, count) -> {
                String alert = String.format(
                    "ALERT: User %s made %d clicks in 5 minutes",
                    windowedKey.key(),
                    count
                );
                return KeyValue.pair(windowedKey.key(), alert);
            })
            .to("fraud-alerts");

        // Transformación 4: Calcular métricas agregadas
        KTable<String, PageStats> pageStats = validClicks
            .groupBy((key, event) -> event.getPageUrl())
            .aggregate(
                PageStats::new,
                (url, event, stats) -> {
                    stats.incrementCount();
                    stats.addDuration(event.getDuration());
                    return stats;
                },
                Materialized.as("page-stats-store")
            );

        // Output
        pageStats.toStream().to("page-analytics");

        // Iniciar streaming app
        KafkaStreams streams = new KafkaStreams(builder.build(), getConfig());
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
```

**Implementación con Apache Flink (más potente para stateful processing):**

```java
// FlinkStreamingJob.java
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;

public class FlinkRealTimeAnalytics {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // Habilitar checkpointing (fault tolerance)
        env.enableCheckpointing(10000); // Cada 10 segundos

        // Source: Kafka
        DataStream<Transaction> transactions = env
            .addSource(new FlinkKafkaConsumer<>(
                "transactions",
                new TransactionDeserializer(),
                kafkaProps
            ))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy
                    .<Transaction>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                    .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
            );

        // Processing: Detectar fraude en tiempo real
        DataStream<FraudAlert> fraudAlerts = transactions
            .keyBy(Transaction::getUserId)
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .process(new FraudDetectionFunction())
            .filter(alert -> alert.getRiskScore() > 0.8);

        // Join con datos de usuario (stream enrichment)
        DataStream<User> users = env
            .addSource(new FlinkKafkaConsumer<>("users", ...));

        DataStream<EnrichedAlert> enrichedAlerts = fraudAlerts
            .join(users)
            .where(FraudAlert::getUserId)
            .equalTo(User::getId)
            .window(TumblingEventTimeWindows.of(Time.seconds(10)))
            .apply((alert, user) -> new EnrichedAlert(alert, user));

        // Side output: Métricas para dashboard
        OutputTag<Metric> metricsTag = new OutputTag<Metric>("metrics"){};

        SingleOutputStreamOperator<EnrichedAlert> alertsWithMetrics = enrichedAlerts
            .process(new ProcessFunction<EnrichedAlert, EnrichedAlert>() {
                @Override
                public void processElement(EnrichedAlert alert, Context ctx, Collector<EnrichedAlert> out) {
                    // Output principal
                    out.collect(alert);

                    // Side output de métrica
                    ctx.output(metricsTag, new Metric("fraud_detected", 1.0, System.currentTimeMillis()));
                }
            });

        // Sinks
        enrichedAlerts.addSink(new FlinkKafkaProducer<>("fraud-alerts", ...));
        enrichedAlerts.getSideOutput(metricsTag).addSink(new InfluxDBSink());

        env.execute("Real-Time Fraud Detection");
    }
}

// Función stateful de detección
class FraudDetectionFunction extends ProcessWindowFunction<Transaction, FraudAlert, String, TimeWindow> {

    @Override
    public void process(String userId, Context context, Iterable<Transaction> transactions, Collector<FraudAlert> out) {
        List<Transaction> txList = StreamSupport
            .stream(transactions.spliterator(), false)
            .collect(Collectors.toList());

        // Patrón sospechoso: múltiples transacciones pequeñas seguidas de una grande
        long smallTxCount = txList.stream()
            .filter(tx -> tx.getAmount() < 10)
            .count();

        Optional<Transaction> largeTx = txList.stream()
            .filter(tx -> tx.getAmount() > 1000)
            .findFirst();

        if (smallTxCount > 5 && largeTx.isPresent()) {
            out.collect(new FraudAlert(
                userId,
                largeTx.get(),
                0.95,  // risk score
                "Pattern: Multiple small tx followed by large tx"
            ));
        }
    }
}
```

**Arquitectura Lambda (Batch + Streaming):**

```
┌─────────────────────────────────────────────────────┐
│              Lambda Architecture                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Raw Data → ┌─────────────────┐                    │
│             │ Batch Layer     │ (Spark/Hadoop)     │
│             │ (Completo)      │                    │
│             └────────┬────────┘                    │
│                      ↓                             │
│              Batch Views (S3/HDFS)                 │
│                      ↓                             │
│             ┌────────────────┐                     │
│             │ Serving Layer  │ (Query merged view)│
│             └────────────────┘                     │
│                      ↑                             │
│              Speed Views (Redis/Cassandra)         │
│                      ↑                             │
│             ┌────────┴────────┐                    │
│             │ Speed Layer     │ (Flink/Storm)      │
│             │ (Incremental)   │                    │
│             └─────────────────┘                    │
│                      ↑                             │
│                 Raw Data                           │
└─────────────────────────────────────────────────────┘
```

**Cuándo usar Streaming:**
- IoT con millones de sensores
- Fraud detection en tiempo real
- Monitoreo de sistemas (logs, métricas)
- Recomendaciones en tiempo real
- Trading algorítmico

**Tecnologías:**
- **Kafka:** Message broker (producer/consumer)
- **Kafka Streams:** Librería de procesamiento simple
- **Apache Flink:** Stateful stream processing complejo
- **AWS Kinesis:** Streaming managed en AWS
- **Apache Storm:** Procesamiento distribuido (legacy)

---

**25. Data Lakehouse - Lo Mejor de Data Lake y Data Warehouse**

Problema: Data Lakes son baratos pero caóticos (schema-on-read). Data Warehouses son estructurados pero caros y rígidos.

Solución: Lakehouse combina almacenamiento barato de lake con ACID transactions y schema enforcement de warehouse.

```
┌──────────────────────────────────────────────────────┐
│                  Data Lakehouse                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Raw Data (S3/ADLS)                                 │
│  ├── parquet/delta files (columnar, comprimido)     │
│  ├── Schema enforcement (Delta Lake/Iceberg)        │
│  └── ACID transactions                              │
│           ↓                                          │
│  ┌────────────────────────────────────────────┐     │
│  │         Metadata Layer                     │     │
│  │  (Delta Lake / Apache Iceberg / Hudi)     │     │
│  │  - Versioning                              │     │
│  │  - Time travel                             │     │
│  │  - Schema evolution                        │     │
│  └────────────────────────────────────────────┘     │
│           ↓                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │
│  │   BI Tools   │  │  ML Training │  │  Spark   │  │
│  │  (Tableau)   │  │  (PyTorch)   │  │  SQL     │  │
│  └──────────────┘  └──────────────┘  └──────────┘  │
└──────────────────────────────────────────────────────┘
```

**Implementación con Delta Lake (sobre Spark):**

```python
# lakehouse_setup.py
from pyspark.sql import SparkSession
from delta import *

# Setup Spark con Delta Lake
builder = SparkSession.builder.appName("Lakehouse") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# 1. WRITE: Ingerir datos con ACID
def ingest_transactions(df, table_path):
    """
    Escritura ACID con Delta Lake
    """
    df.write \
        .format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .save(table_path)

# 2. UPSERT: Actualizar datos existentes (merge)
def upsert_user_profiles(updates_df, table_path):
    """
    Upsert (Update + Insert) atómico
    """
    from delta.tables import DeltaTable

    delta_table = DeltaTable.forPath(spark, table_path)

    delta_table.alias("target").merge(
        updates_df.alias("updates"),
        "target.user_id = updates.user_id"
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()

# 3. TIME TRAVEL: Leer datos históricos
def get_data_at_version(table_path, version):
    """
    Time travel: ver datos en cualquier versión
    """
    return spark.read \
        .format("delta") \
        .option("versionAsOf", version) \
        .load(table_path)

def get_data_at_timestamp(table_path, timestamp):
    """
    Time travel: ver datos en momento específico
    """
    return spark.read \
        .format("delta") \
        .option("timestampAsOf", timestamp) \
        .load(table_path)

# 4. SCHEMA EVOLUTION: Cambiar esquema sin romper
def add_new_column(table_path):
    """
    Agregar columna sin reescribir tabla
    """
    df = spark.read.format("delta").load(table_path)

    # Agregar columna nueva
    df_with_new_col = df.withColumn("risk_score", calculate_risk_udf(df.amount))

    # Merge schema automático
    df_with_new_col.write \
        .format("delta") \
        .mode("overwrite") \
        .option("mergeSchema", "true") \
        .save(table_path)

# 5. VACUUM: Limpiar archivos viejos
def cleanup_old_versions(table_path, retention_hours=168):
    """
    Eliminar versiones antiguas (por defecto 7 días)
    """
    from delta.tables import DeltaTable

    delta_table = DeltaTable.forPath(spark, table_path)
    delta_table.vacuum(retention_hours)

# 6. OPTIMIZE: Compactar archivos pequeños
def optimize_table(table_path):
    """
    Compactar archivos para mejor performance
    """
    spark.sql(f"OPTIMIZE delta.`{table_path}`")

    # Z-ordering para queries específicas
    spark.sql(f"""
        OPTIMIZE delta.`{table_path}`
        ZORDER BY (user_id, date)
    """)

# 7. STREAMING: Ingestión en tiempo real
def stream_to_lakehouse(kafka_bootstrap_servers, topic, table_path):
    """
    Streaming desde Kafka a Lakehouse
    """
    stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", topic) \
        .load()

    # Parse JSON y escribir a Delta
    parsed = stream.selectExpr("CAST(value AS STRING) as json") \
        .select(from_json("json", transaction_schema).alias("data")) \
        .select("data.*")

    query = parsed.writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("checkpointLocation", "/tmp/checkpoint") \
        .start(table_path)

    return query

# Ejemplo de uso completo
if __name__ == "__main__":
    # Ingestar datos iniciales
    transactions_df = spark.read.parquet("s3://raw-data/transactions/")
    ingest_transactions(transactions_df, "s3://lakehouse/transactions")

    # Query SQL directo (como warehouse tradicional)
    spark.sql("""
        CREATE TABLE IF NOT EXISTS transactions
        USING DELTA
        LOCATION 's3://lakehouse/transactions'
    """)

    # Analytics con SQL
    result = spark.sql("""
        SELECT
            user_id,
            DATE(timestamp) as date,
            SUM(amount) as total_spent,
            COUNT(*) as tx_count
        FROM transactions
        WHERE timestamp >= '2024-01-01'
        GROUP BY user_id, DATE(timestamp)
    """)

    # ML training directo desde lakehouse
    from pyspark.ml.feature import VectorAssembler
    from pyspark.ml.classification import RandomForestClassifier

    features_df = spark.sql("""
        SELECT
            amount,
            merchant_category,
            hour(timestamp) as hour,
            is_fraud as label
        FROM transactions
    """)

    assembler = VectorAssembler(
        inputCols=["amount", "merchant_category", "hour"],
        outputCol="features"
    )

    model = RandomForestClassifier(labelCol="label", featuresCol="features")
    pipeline = Pipeline(stages=[assembler, model])
    model_trained = pipeline.fit(features_df)
```

**Arquitectura con Apache Iceberg (alternativa a Delta Lake):**

```sql
-- Crear tabla Iceberg
CREATE TABLE lakehouse.transactions (
    transaction_id BIGINT,
    user_id BIGINT,
    amount DECIMAL(10,2),
    timestamp TIMESTAMP,
    merchant STRING,
    is_fraud BOOLEAN
)
USING iceberg
PARTITIONED BY (days(timestamp))
LOCATION 's3://lakehouse/transactions';

-- Time travel con Iceberg
SELECT * FROM lakehouse.transactions
FOR SYSTEM_TIME AS OF '2024-01-01 00:00:00';

-- Rollback a versión anterior
CALL lakehouse.system.rollback_to_snapshot('transactions', 123456789);

-- Schema evolution
ALTER TABLE lakehouse.transactions
ADD COLUMN risk_score DOUBLE;

-- Metadata queries
SELECT * FROM lakehouse.transactions.snapshots;
SELECT * FROM lakehouse.transactions.history;
```

**Comparación: Data Lake vs Warehouse vs Lakehouse**

```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│   Feature       │  Data Lake   │ Warehouse    │  Lakehouse   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Storage Cost    │  Muy bajo    │  Alto        │  Muy bajo    │
│ ACID            │  No          │  Sí          │  Sí          │
│ Schema          │  On-read     │  On-write    │  Híbrido     │
│ ML/AI           │  Excelente   │  Limitado    │  Excelente   │
│ BI/Analytics    │  Lento       │  Rápido      │  Rápido      │
│ Real-time       │  Sí          │  No          │  Sí          │
│ Versioning      │  No          │  No          │  Sí          │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

**Cuándo usar Lakehouse:**
- Necesitas BI analytics Y ML/AI sobre los mismos datos
- Volúmenes masivos (petabytes)
- Necesitas time travel y auditoría
- Streaming + batch en la misma plataforma
- Reducir costos vs warehouse tradicional

**Tecnologías:**
- **Delta Lake** (Databricks)
- **Apache Iceberg** (Netflix, open-source)
- **Apache Hudi** (Uber, para upserts frecuentes)

---

**26. Data Mesh - Datos como Producto Descentralizado**

Problema: Data lakes/warehouses centralizados crean cuellos de botella. Equipos de datos no escalan.

Solución: Descentralizar ownership de datos. Cada dominio es dueño de sus datos como "producto".

```
┌────────────────────────────────────────────────────────┐
│                    Data Mesh                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Domain 1: Orders          Domain 2: Users            │
│  ┌──────────────────┐      ┌──────────────────┐       │
│  │ Orders Team      │      │ Users Team       │       │
│  │ (owns data)      │      │ (owns data)      │       │
│  ├──────────────────┤      ├──────────────────┤       │
│  │ Data Product:    │      │ Data Product:    │       │
│  │ - orders_events  │      │ - user_profiles  │       │
│  │ - order_metrics  │      │ - user_events    │       │
│  │                  │      │                  │       │
│  │ SLA: 99.9%       │      │ SLA: 99.9%       │       │
│  │ Owner: @team-a   │      │ Owner: @team-b   │       │
│  └──────────────────┘      └──────────────────┘       │
│           ↓                         ↓                  │
│  ┌─────────────────────────────────────────────┐      │
│  │      Federated Governance                   │      │
│  │  - Schema registry global                   │      │
│  │  - Security policies                        │      │
│  │  - Discovery (data catalog)                 │      │
│  └─────────────────────────────────────────────┘      │
│           ↓                         ↓                  │
│  Analytics Team consume ambos data products           │
└────────────────────────────────────────────────────────┘
```

**Principios de Data Mesh:**

1. **Domain-Oriented Ownership:** Cada equipo es dueño de sus datos
2. **Data as a Product:** Datos tienen SLA, documentación, calidad
3. **Self-Serve Platform:** Infraestructura facilita crear data products
4. **Federated Governance:** Políticas globales, ejecución local

**Implementación de Data Product (ejemplo con Python + DBT):**

```python
# data_product/orders_analytics.py
"""
Data Product: Orders Analytics
Owner: orders-team@company.com
SLA: 99.9% uptime, <5min latency
"""

from dataclasses import dataclass
from typing import List
import great_expectations as ge

@dataclass
class DataProductMetadata:
    name: str
    version: str
    owner: str
    sla_uptime: float
    sla_latency_seconds: int
    schema_version: str

    def to_catalog_entry(self):
        """Publicar en data catalog"""
        return {
            "name": self.name,
            "version": self.version,
            "owner": self.owner,
            "sla": {
                "uptime": self.sla_uptime,
                "latency_seconds": self.sla_latency_seconds
            },
            "schema_url": f"schema-registry.company.com/{self.name}/v{self.schema_version}"
        }

class OrdersAnalyticsProduct:
    """
    Data Product que expone métricas de orders
    """

    metadata = DataProductMetadata(
        name="orders_analytics",
        version="2.1.0",
        owner="orders-team@company.com",
        sla_uptime=0.999,
        sla_latency_seconds=300,
        schema_version="2.0"
    )

    def __init__(self, spark):
        self.spark = spark
        self.output_path = "s3://data-mesh/orders_analytics"

    def validate_input_quality(self, df):
        """
        Data quality checks con Great Expectations
        """
        ge_df = ge.from_pandas(df.toPandas())

        # Expectations
        ge_df.expect_column_values_to_not_be_null("order_id")
        ge_df.expect_column_values_to_be_between("amount", min_value=0, max_value=1000000)
        ge_df.expect_column_values_to_match_regex("status", "^(pending|completed|cancelled)$")

        results = ge_df.validate()

        if not results.success:
            raise DataQualityException("Input validation failed", results)

        return df

    def transform(self):
        """
        Transformación de datos (puede usar DBT internamente)
        """
        orders = self.spark.sql("""
            SELECT
                order_id,
                user_id,
                amount,
                status,
                created_at
            FROM raw.orders
            WHERE created_at >= current_date - interval 30 days
        """)

        # Validar calidad
        orders_validated = self.validate_input_quality(orders)

        # Agregar métricas
        metrics = self.spark.sql("""
            SELECT
                user_id,
                DATE(created_at) as date,
                COUNT(*) as order_count,
                SUM(amount) as total_spent,
                AVG(amount) as avg_order_value,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
                MAX(created_at) as last_order_date
            FROM orders_validated
            GROUP BY user_id, DATE(created_at)
        """)

        return metrics

    def publish(self):
        """
        Publicar data product con SLA monitoring
        """
        import time
        start = time.time()

        try:
            # Transform
            result = self.transform()

            # Write con Delta Lake (ACID)
            result.write \
                .format("delta") \
                .mode("overwrite") \
                .option("overwriteSchema", "true") \
                .save(self.output_path)

            # Check SLA latency
            duration = time.time() - start
            if duration > self.metadata.sla_latency_seconds:
                alert_sla_violation("latency", duration)

            # Registrar en catalog
            register_in_catalog(self.metadata.to_catalog_entry())

            # Publicar métricas
            publish_metrics({
                "data_product": self.metadata.name,
                "rows_published": result.count(),
                "latency_seconds": duration,
                "timestamp": time.time()
            })

        except Exception as e:
            alert_sla_violation("uptime", str(e))
            raise

# DBT model para transformaciones declarativas
# models/orders_analytics.sql
```

```sql
-- models/orders_analytics.sql
{{
  config(
    materialized='incremental',
    unique_key='user_id',
    on_schema_change='sync_all_columns',
    tags=['data-product', 'orders-domain']
  )
}}

WITH orders_base AS (
  SELECT *
  FROM {{ source('raw', 'orders') }}
  {% if is_incremental() %}
    WHERE created_at > (SELECT MAX(last_order_date) FROM {{ this }})
  {% endif %}
),

metrics AS (
  SELECT
    user_id,
    DATE(created_at) as date,
    COUNT(*) as order_count,
    SUM(amount) as total_spent,
    AVG(amount) as avg_order_value,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
    MAX(created_at) as last_order_date
  FROM orders_base
  GROUP BY user_id, DATE(created_at)
)

SELECT * FROM metrics
```

**Data Catalog (discovery de data products):**

```python
# data_catalog/catalog.py
from fastapi import FastAPI
from typing import List

app = FastAPI()

class DataProductCatalog:
    """
    Catalog centralizado para descubrir data products
    """

    @app.get("/products")
    def list_products(domain: str = None):
        """Listar todos los data products"""
        products = db.query("""
            SELECT
                name,
                version,
                owner,
                domain,
                description,
                schema_url,
                sla_uptime,
                last_updated
            FROM data_products
            WHERE domain = :domain OR :domain IS NULL
        """, domain=domain)

        return products

    @app.get("/products/{name}/schema")
    def get_schema(name: str, version: str = "latest"):
        """Obtener schema de data product"""
        return schema_registry.get(name, version)

    @app.get("/products/{name}/lineage")
    def get_lineage(name: str):
        """Ver dependencias upstream/downstream"""
        return {
            "upstream": ["raw.orders", "raw.users"],
            "downstream": ["ml_features.fraud_detection", "bi.sales_dashboard"]
        }

    @app.get("/products/{name}/health")
    def get_health(name: str):
        """Health check y SLA compliance"""
        return {
            "status": "healthy",
            "uptime_30d": 0.9995,
            "sla_uptime": 0.999,
            "sla_met": True,
            "avg_latency_seconds": 120,
            "last_refresh": "2024-12-02T10:30:00Z"
        }
```

**Self-Serve Platform (infraestructura):**

```yaml
# platform/data_product_template.yml
# Template para crear nuevo data product en minutos
apiVersion: v1
kind: DataProduct
metadata:
  name: ${PRODUCT_NAME}
  domain: ${DOMAIN}
  owner: ${TEAM_EMAIL}
spec:
  source:
    type: kafka | database | s3
    connection: ${CONNECTION_STRING}

  transformations:
    - type: dbt | spark | python
      code: ${TRANSFORMATION_CODE}

  quality:
    - type: great_expectations
      suite: ${EXPECTATIONS_FILE}

  output:
    format: delta | parquet | iceberg
    location: s3://data-mesh/${DOMAIN}/${PRODUCT_NAME}
    partitionBy: [date]

  sla:
    uptime: 0.999
    latency_seconds: 300
    freshness_minutes: 60

  access:
    - team: analytics
      permission: read
    - team: ml-team
      permission: read
```

**Cuándo usar Data Mesh:**
- Organización grande con múltiples dominios/equipos
- Data team centralizado es cuello de botella
- Diferentes dominios necesitan control sobre sus datos
- Cultura de ownership y productos

**Diferencias con Data Lake/Warehouse:**
- **Lake/Warehouse:** Centralizado, un equipo de datos
- **Mesh:** Descentralizado, cada dominio es dueño de sus datos

---

**27. Inferencia Distribuida - Escalar Modelos ML**

Problema: Modelo ML necesita servir millones de predicciones/segundo con baja latencia.

Solución: Distribuir inferencia en múltiples nodos con balanceo de carga.

```
┌────────────────────────────────────────────────────┐
│           Distributed Inference                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  Load Balancer (Nginx/Envoy)                      │
│         │                                          │
│    ┌────┴────┬────────┬────────┐                  │
│    ↓         ↓        ↓        ↓                  │
│  ┌───┐    ┌───┐    ┌───┐    ┌───┐                │
│  │GPU│    │GPU│    │GPU│    │GPU│                │
│  │ 1 │    │ 2 │    │ 3 │    │ 4 │                │
│  └───┘    └───┘    └───┘    └───┘                │
│  Model   Model   Model   Model                    │
│  v1.2    v1.2    v1.2    v1.2                     │
│                                                    │
│  Horizontal Pod Autoscaler (Kubernetes)           │
│  - Scale 1-10 replicas based on CPU/GPU           │
│  - Health checks                                  │
│  - Rolling updates                                │
└────────────────────────────────────────────────────┘
```

**Implementación con TorchServe (PyTorch):**

```python
# model_handler.py
from ts.torch_handler.base_handler import BaseHandler
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

class ImageClassifierHandler(BaseHandler):
    """
    Custom handler para inferencia distribuida
    """

    def __init__(self):
        super().__init__()
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def preprocess(self, requests):
        """
        Preprocesamiento con batching automático
        """
        images = []
        for request in requests:
            image_bytes = request.get("data") or request.get("body")
            image = Image.open(io.BytesIO(image_bytes))
            image_tensor = self.transform(image)
            images.append(image_tensor)

        # Batch inference
        return torch.stack(images)

    def inference(self, batch):
        """
        Inferencia en GPU con batching
        """
        with torch.no_grad():
            predictions = self.model(batch)
        return predictions

    def postprocess(self, inference_output):
        """
        Formatear respuesta
        """
        probabilities = torch.nn.functional.softmax(inference_output, dim=1)
        top_probs, top_indices = torch.topk(probabilities, k=5)

        results = []
        for probs, indices in zip(top_probs, top_indices):
            results.append({
                "predictions": [
                    {
                        "class": self.mapping[str(idx.item())],
                        "probability": prob.item()
                    }
                    for prob, idx in zip(probs, indices)
                ]
            })

        return results
```

**Deployment en Kubernetes:**

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-inference
spec:
  replicas: 4  # 4 pods iniciales
  selector:
    matchLabels:
      app: model-inference
  template:
    metadata:
      labels:
        app: model-inference
        version: v1.2.0
    spec:
      containers:
      - name: torchserve
        image: pytorch/torchserve:latest-gpu
        ports:
        - containerPort: 8080  # Inference
        - containerPort: 8081  # Management
        - containerPort: 8082  # Metrics

        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
            nvidia.com/gpu: 1
          limits:
            memory: "8Gi"
            cpu: "4"
            nvidia.com/gpu: 1

        env:
        - name: MODEL_STORE
          value: "/models"
        - name: TS_BATCH_SIZE
          value: "16"  # Batch inference
        - name: TS_MAX_BATCH_DELAY
          value: "100"  # 100ms max wait

        livenessProbe:
          httpGet:
            path: /ping
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ping
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

        volumeMounts:
        - name: model-store
          mountPath: /models

      volumes:
      - name: model-store
        persistentVolumeClaim:
          claimName: model-pvc

---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-inference-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-inference
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: nvidia.com/gpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: inference_latency_ms
      target:
        type: AverageValue
        averageValue: "100"  # Escalar si latencia > 100ms

---
# Service con Load Balancer
apiVersion: v1
kind: Service
metadata:
  name: model-inference-service
spec:
  type: LoadBalancer
  selector:
    app: model-inference
  ports:
  - name: inference
    port: 80
    targetPort: 8080
  - name: metrics
    port: 8082
    targetPort: 8082
```
