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

### Teoremas Fundamentales

**ACID (Transacciones):**
- **Atomicity:** Todo o nada
- **Consistency:** Estado válido siempre
- **Isolation:** Transacciones no interfieren
- **Durability:** Cambios persisten

**CAP Theorem:**
```
En sistema distribuido, solo 2 de 3:
- Consistency (todos leen lo mismo)
- Availability (siempre responde)
- Partition Tolerance (funciona con fallas de red)
```
- **CP:** PostgreSQL, HBase
- **AP:** Cassandra, DynamoDB

**TDD (Test-Driven Development):**
1. Escribe test (falla)
2. Escribe código mínimo (pasa)
3. Refactoriza

**DDD (Domain-Driven Design):**
- Ubiquitous Language
- Bounded Contexts
- Aggregates

---

## Seguridad en Profundidad

### Hashing Algorithms

**MD5 / SHA-1:** ❌ DEPRECADOS (colisiones conocidas)

**SHA-256:**
```python
import hashlib
hash = hashlib.sha256(b"password").hexdigest()
```

**bcrypt (para contraseñas):**
```python
import bcrypt
hashed = bcrypt.hashpw(b"password", bcrypt.gensalt())
```
- Computacionalmente costoso (dificulta brute force)

### PKI (Public Key Infrastructure)

**Asimétrico (RSA, ECDSA):**
```
Clave Pública (cifra) + Clave Privada (descifra)
```

**Certificados SSL/TLS:**
```
CA (Certificate Authority) firma certificado
   ↓
Navegador verifica firma
   ↓
Conexión HTTPS segura
```

### OWASP (Detallado)

**1. Broken Access Control:**
```python
# ❌ MAL
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return db.get_user(user_id)  # Cualquiera puede acceder

# ✅ BIEN
@app.get("/users/{user_id}")
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403)
    return db.get_user(user_id)
```

**2. SQL Injection:**
```python
# ❌ MAL
query = f"SELECT * FROM users WHERE email = '{email}'"
# email = "'; DROP TABLE users; --"

# ✅ BIEN
query = "SELECT * FROM users WHERE email = ?"
cursor.execute(query, (email,))  # Parametrizado
```

**3. XSS (Cross-Site Scripting):**
```javascript
// ❌ MAL
div.innerHTML = userInput;  // userInput = "<script>alert('XSS')</script>"

// ✅ BIEN
div.textContent = userInput;  // Escapa HTML automáticamente
```

### Estrategias de Autenticación

**1. Session-Based:**
```
Login → Server crea sesión → Cookie con SessionID
```
**Pros:** Fácil revocar
**Contras:** No stateless

**2. Token-Based (JWT):**
```
Login → Server firma JWT → Cliente guarda JWT
```
**Pros:** Stateless
**Contras:** Difícil revocar

**3. OAuth2:**
```
Usuario → Autoriza app → Auth Server da token → App usa token
```
**Uso:** "Login with Google"

**4. SAML:**
```
Empresa → Identity Provider (IdP) → Service Provider (SP)
```
**Uso:** Enterprise SSO

---

## APIs e Integraciones

### REST
```http
GET /users          # Lista
GET /users/123      # Detalle
POST /users         # Crear
PUT /users/123      # Actualizar completo
PATCH /users/123    # Actualizar parcial
DELETE /users/123   # Eliminar
```

**Idempotencia:**
- GET, PUT, DELETE: Idempotentes (mismo resultado si repites)
- POST: No idempotente

### GraphQL
```graphql
query {
  user(id: 123) {
    name
    email
    posts {
      title
    }
  }
}
```
**Pros:** Cliente pide exactamente lo que necesita
**Contras:** Complejidad en backend

### gRPC
```protobuf
service UserService {
  rpc GetUser (UserRequest) returns (UserResponse);
}
```
**Pros:** Binario (rápido), HTTP/2, streaming
**Contras:** No legible sin herramientas

### ESB (Enterprise Service Bus)
Middleware que conecta aplicaciones:
```
App A → ESB → App B
        ↓
       App C
```

### SOAP
XML over HTTP. Legacy, pero aún en uso enterprise.

### BPM (Business Process Management) / BPEL
Orquestación de procesos de negocio.

### Messaging Queues

**RabbitMQ:**
```
Producer → Exchange → Queue → Consumer
```

**Apache Kafka:**
```
Producer → Topic (particionado) → Consumer Group
```
**Diferencia:** Kafka para streaming, RabbitMQ para colas tradicionales

---

## Desarrollo Web y Mobile

### Programación Funcional
```javascript
// Imperativo
const doubled = [];
for (let i = 0; i < nums.length; i++) {
  doubled.push(nums[i] * 2);
}

// Funcional
const doubled = nums.map(x => x * 2);
```

**Principios:**
- Funciones puras (sin efectos secundarios)
- Inmutabilidad
- Composición

### Frameworks Frontend

**React:**
```jsx
function UserProfile({ user }) {
  return <div>{user.name}</div>;
}
```
- Componentes
- Virtual DOM
- Ecosistema masivo

**Vue:**
```vue
<template>
  <div>{{ user.name }}</div>
</template>
```
- Plantillas
- Reactivo
- Fácil de aprender

**Angular:**
```typescript
@Component({
  selector: 'user-profile',
  template: '<div>{{user.name}}</div>'
})
export class UserProfileComponent { }
```
- Framework completo
- TypeScript nativo
- Enterprise

### Paradigmas de Rendering

**SPA (Single Page Application):**
```
Client-side rendering
User → HTML vacío + JS → JS renderiza todo
```
**Pros:** UX fluido
**Contras:** SEO difícil, carga inicial lenta

**SSR (Server-Side Rendering):**
```
User → Server renderiza HTML → HTML completo
```
**Pros:** SEO, carga inicial rápida
**Contras:** Más carga en servidor

**SSG (Static Site Generation):**
```
Build time → Genera HTML estático
```
**Pros:** Performance máxima
**Contras:** No dinámico

### Microfrontends
```
Shell App
  ├─ Header (React)
  ├─ Products (Vue)
  └─ Checkout (Angular)
```
**Pros:** Equipos independientes
**Contras:** Complejidad

### Programación Reactiva (RxJS)
```javascript
import { fromEvent } from 'rxjs';
import { debounceTime, map } from 'rxjs/operators';

fromEvent(input, 'input')
  .pipe(
    debounceTime(300),
    map(e => e.target.value)
  )
  .subscribe(value => search(value));
```

### Estándares W3C y WHATWG
- HTML5, CSS3
- Web APIs (Fetch, WebSockets, WebRTC)
- Accessibility (ARIA)

---

## Redes y Comunicaciones

### Modelo OSI (7 capas)
```
7. Application (HTTP, FTP)
6. Presentation (SSL/TLS)
5. Session
4. Transport (TCP, UDP)
3. Network (IP)
2. Data Link (Ethernet)
1. Physical (Cables)
```

### Modelo TCP/IP (4 capas)
```
4. Application (HTTP)
3. Transport (TCP)
2. Internet (IP)
1. Network Access (Ethernet)
```

### HTTP / HTTPS en Detalle

**HTTP/1.1:**
- Una petición por conexión
- Head-of-line blocking

**HTTP/2:**
- Multiplexing (múltiples peticiones por conexión)
- Server push
- Compresión de headers

**HTTP/3 (QUIC):**
- UDP en lugar de TCP
- Menos latencia

### Proxies

**Forward Proxy:**
```
Cliente → Proxy → Internet
```
**Uso:** Filtrar contenido, caché

**Reverse Proxy:**
```
Internet → Proxy → Servidores internos
```
**Uso:** Load balancing, SSL termination
**Herramientas:** Nginx, HAProxy

### Firewalls

**Tipos:**
- **Packet Filtering:** Bloquea por IP/puerto
- **Stateful:** Rastrea conexiones
- **Application-Level:** Inspecciona contenido (WAF)

---

## Conocimientos de Operaciones

### Infrastructure as Code (IaC)

**Terraform:**
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```

**CloudFormation (AWS):**
```yaml
Resources:
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t2.micro
```

### Cloud Providers

**AWS:**
- Más maduro, más servicios
- Curva de aprendizaje alta

**Azure:**
- Integración con Microsoft
- Enterprise

**Google Cloud:**
- ML/AI lider
- Kubernetes (GKE)

### Serverless Concepts

**FaaS:** Lambda, Cloud Functions
**BaaS:** Firebase, Supabase

**Cold Start:**
```
Primera invocación → ~1s (inicializar runtime)
Invocaciones siguientes → ~10ms
```

### Linux / Unix

**Comandos esenciales:**
```bash
# Procesos
ps aux | grep nginx
top
htop

# Logs
tail -f /var/log/app.log
journalctl -u myservice

# Networking
netstat -tulpn
ss -tulpn
curl -I https://example.com

# Disco
df -h
du -sh /var/log

# Permisos
chmod 755 script.sh
chown user:group file.txt
```

### Service Mesh (Istio, Linkerd)

**Resuelve:**
- Service discovery
- Load balancing
- Encryption (mTLS)
- Observabilidad
- Circuit breaking

**Arquitectura:**
```
App Container
   ↓
Sidecar Proxy (Envoy)
   ↓
Network
```

### CI / CD (Detallado en Pilar 6)

### Containers (Detallado en Skill 5)

### Cloud Design Patterns

**1. Retry Pattern:**
```python
@retry(max_attempts=3, backoff=2)
def call_api():
    response = requests.get(url)
    response.raise_for_status()
```

**2. Circuit Breaker:**
```
Cerrado (normal) → Falla → Abierto (no llama) → Half-Open (prueba) → Cerrado
```

**3. Bulkhead:**
Aislar recursos para que fallo en uno no afecte otros.

**4. Throttling:**
Limitar rate de peticiones.

**5. Cache-Aside:**
```python
def get_user(user_id):
    user = cache.get(user_id)
    if user is None:
        user = db.get_user(user_id)
        cache.set(user_id, user)
    return user
```

---

## Software Empresarial

### SAP
- **ERP:** Enterprise Resource Planning (finanzas, HR, supply chain)
- **HANA:** In-memory database
- **Business Objects:** BI/Analytics

### Microsoft Dynamics
- CRM (Customer Relationship Management)
- ERP

### Salesforce
- CRM líder
- Ecosystem masivo (AppExchange)
- Lightning (frontend framework)

### EMC DMS (Document Management System)
Gestión documental enterprise.

### IBM BPM (Business Process Management)
Orquestación de procesos.

**Por qué importa:**
Enterprise contrata arquitectos que entiendan su stack.

---

# PARTE IV: Frameworks y Gestión

## Frameworks de Arquitectura

### TOGAF (The Open Group Architecture Framework)

**Componentes:**
1. **ADM (Architecture Development Method):** Ciclo de desarrollo de arquitectura
2. **Architecture Repository:** Repositorio de artefactos
3. **Reference Models:** Modelos de referencia

**Fases ADM:**
```
Preliminary → Vision → Business → Information Systems → Technology →
Opportunities → Migration → Implementation → Change Management
```

**Uso:** Arquitectura empresarial (Enterprise Architecture)

### BABOK (Business Analysis Body of Knowledge)

**Áreas:**
- Requirements elicitation
- Stakeholder engagement
- Strategy analysis

**Uso:** Arquitectos que trabajan con requisitos de negocio

### IAF (Integrated Architecture Framework)

Similar a TOGAF, menos común.

### UML (Unified Modeling Language)

**Diagramas:**

**Estructurales:**
- Class Diagram
- Component Diagram
- Deployment Diagram

**Comportamiento:**
- Use Case Diagram
- Sequence Diagram
- Activity Diagram

**Ejemplo: Sequence Diagram:**
```
Usuario → Frontend: Login
Frontend → Backend: POST /auth/login
Backend → DB: Verificar credenciales
DB → Backend: Usuario válido
Backend → Frontend: JWT token
Frontend → Usuario: Redirigir a dashboard
```

---

## Metodologías de Gestión

### PMI (Project Management Institute)

**PMBOK (Project Management Body of Knowledge):**
- Scope, Time, Cost, Quality, Risk, etc.

**Certificación:** PMP (Project Management Professional)

### ITIL (Information Technology Infrastructure Library)

**Service Management:**
- Incident Management
- Change Management
- Problem Management

**Uso:** Operaciones IT

### Prince2 (Projects in Controlled Environments)

Metodología de gestión de proyectos UK.

### RUP (Rational Unified Process)

Metodología iterativa de desarrollo software.

---

## Modelo Ágil

### Scrum

**Roles:**
- Product Owner
- Scrum Master
- Development Team

**Eventos:**
- Sprint Planning
- Daily Standup
- Sprint Review
- Sprint Retrospective

**Artefactos:**
- Product Backlog
- Sprint Backlog
- Increment

### Kanban

**Principios:**
- Visualizar flujo
- Limitar WIP (Work In Progress)
- Gestionar flujo

**Board:**
```
To Do | In Progress | Code Review | Done
```

### XP (Extreme Programming)

**Prácticas:**
- Pair Programming
- TDD
- Continuous Integration
- Refactoring

### SAFe (Scaled Agile Framework)

Ágil a escala empresarial.

**Niveles:**
- Team
- Program (Agile Release Train)
- Large Solution
- Portfolio

### LeSS (Large-Scale Scrum)

Scrum escalado de forma más simple que SAFe.

---

## TOGAF + Scrum: El Híbrido Aumentado por IA (2026)

### La Paradoja Resuelta

Durante décadas, TOGAF y Scrum han sido vistos como **opuestos incompatibles:**

| Aspecto | TOGAF (Tradicional) | Scrum (Ágil) |
|---------|---------------------|--------------|
| **Horizonte** | Largo plazo (3-5 años) | Corto plazo (2 semanas) |
| **Enfoque** | Planificación exhaustiva | Iteración rápida |
| **Documentación** | Extensa | Mínima viable |
| **Cambios** | Costosos | Bienvenidos |
| **Estructura** | Waterfall | Iterativo |
| **Ámbito** | Enterprise | Equipo/Producto |

**El problema del mundo real:**
- Las empresas **necesitan visión estratégica** (TOGAF)
- Pero también **velocidad de ejecución** (Scrum)

**La solución 2026:** Un híbrido **aumentado por IA** que toma lo mejor de ambos mundos.

---

### El Framework: TOGAF-Scrum-AI (TSA Framework)

**Principio central:**
> "Piensa estratégicamente como TOGAF, ejecuta ágilmente como Scrum, acelera exponencialmente con IA"

**Componentes:**

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA ESTRATÉGICA (TOGAF)                 │
│              Vision · Principios · Roadmap (12 meses)       │
│                    ↓ (Guía, no dicta)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          CAPA DE EJECUCIÓN (Scrum-AI)                │  │
│  │  Sprint 1 → Sprint 2 → Sprint 3 → ... → Sprint N     │  │
│  │      ↓         ↓         ↓              ↓            │  │
│  │  Agentes IA validan arquitectura en cada sprint      │  │
│  └──────────────────────────────────────────────────────┘  │
│                    ↑ (Feedback continuo)                    │
│            Actualiza visión basada en aprendizajes          │
└─────────────────────────────────────────────────────────────┘
```

---

### Fase 1: Visión Estratégica Acelerada (TOGAF-AI)

**Tradicional TOGAF ADM Fase A (Architecture Vision):**
- Duración: 4-8 semanas
- Equipos: 10-15 personas
- Documentación: 100+ páginas

**TOGAF-AI 2026:**
- Duración: **3-5 días**
- Equipos: 3-5 arquitectos + Agentes IA
- Documentación: **Generada automáticamente**

#### Proceso Aumentado

**Día 1: Requirements Elicitation con IA**

```python
# Agente de Requisitos
from langgraph import Agent, Tool

requirements_agent = Agent(
    model="gpt-4",
    tools=[
        Tool("interview_stakeholder", interview_tool),
        Tool("analyze_documents", document_analyzer),
        Tool("extract_constraints", constraint_extractor)
    ],
    system_prompt="""Eres un arquitecto empresarial experto en TOGAF.
    Entrevista a stakeholders, analiza documentos y extrae:
    1. Objetivos de negocio
    2. Requisitos funcionales y no funcionales
    3. Restricciones (presupuesto, tiempo, regulatorias)
    4. Drivers arquitectónicos

    Genera un documento estructurado de requisitos."""
)

# Ejecución
stakeholder_inputs = [
    "Queremos reducir costos de TI un 30%",
    "Necesitamos migrar a cloud en 12 meses",
    "Compliance con GDPR es crítico"
]

requirements_doc = requirements_agent.run(stakeholder_inputs)
```

**Output (generado en 2 horas vs. 2 semanas):**
```markdown
# Architecture Vision Document

## Business Goals
1. Reducir TCO de TI en 30% ($5M/año)
2. Mejorar time-to-market de 6 meses a 2 semanas
3. Escalar a 10M usuarios (actualmente 1M)

## Architecture Drivers
- **Performance:** <100ms latency p99
- **Scalability:** 10x crecimiento en 12 meses
- **Security:** GDPR, SOC2, ISO 27001
- **Cost:** ≤$500K/mes cloud spend

## Constraints
- Presupuesto: $3M
- Timeline: 12 meses
- Team: 20 developers
- Legacy: SAP ERP (no reemplazable)
```

**Día 2-3: Diseño de Arquitectura con IA**

```python
# Agente Arquitecto
architecture_agent = Agent(
    model="claude-3-opus",
    tools=[
        Tool("generate_architecture", architecture_generator),
        Tool("cost_estimation", cost_estimator),
        Tool("validate_constraints", constraint_validator),
        Tool("generate_diagrams", diagram_generator)
    ],
    system_prompt="""Eres un Solution Architect senior.
    Genera arquitecturas que cumplan requirements, optimizando:
    - Costo/beneficio
    - Riesgo técnico
    - Viabilidad de implementación

    Genera 3 opciones (conservadora, balanceada, innovadora)."""
)

architectures = architecture_agent.run(requirements_doc)
```

**Output: 3 Opciones Arquitectónicas**

**Opción A - Conservadora (Lift & Shift):**
```
┌─────────────────────────────────────┐
│ Migración a AWS con cambios mínimos │
│ Monolito → EC2                      │
│ DB → RDS                            │
│ Costo: $400K/mes · Riesgo: Bajo     │
│ Reducción TCO: 15% ⚠️               │
└─────────────────────────────────────┘
```

**Opción B - Balanceada (Modernización Gradual):**
```
┌─────────────────────────────────────┐
│ Strangler Fig Pattern               │
│ Monolito + Microservicios nuevos    │
│ ECS Fargate + Lambda                │
│ Costo: $350K/mes · Riesgo: Medio    │
│ Reducción TCO: 30% ✅               │
└─────────────────────────────────────┘
```

**Opción C - Innovadora (Cloud Native Total):**
```
┌─────────────────────────────────────┐
│ Rewrite completo a Serverless       │
│ Microservicios + Event-Driven       │
│ Lambda + DynamoDB + EventBridge     │
│ Costo: $250K/mes · Riesgo: Alto     │
│ Reducción TCO: 50% 🚀 (pero riesgo) │
└─────────────────────────────────────┘
```

**Día 4: Validación Automatizada**

```python
# Agente Validador
validation_agent = Agent(
    model="gpt-4",
    tools=[
        Tool("check_security", security_checker),
        Tool("check_compliance", compliance_checker),
        Tool("check_performance", performance_estimator),
        Tool("check_cost", cost_validator)
    ]
)

# Validar cada opción
for option in architectures:
    validation_result = validation_agent.validate(option, requirements_doc)

    if validation_result.passes_all_checks():
        option.mark_as_viable()
    else:
        option.flag_issues(validation_result.issues)
```

**Output:**
```
Opción A: ✅ VIABLE (7/10 score)
  ⚠️ No cumple objetivo de reducción de costos

Opción B: ✅ VIABLE (9/10 score) ⭐ RECOMENDADA
  ✅ Cumple todos los requisitos
  ✅ Riesgo balanceado

Opción C: ⚠️ VIABLE CON RIESGO (6/10 score)
  ⚠️ Requiere reescritura completa (12 meses puede no ser suficiente)
  ✅ Mejor costo a largo plazo
```

**Día 5: Presentación y Decision**

El Agente IA genera:
- **Presentación PowerPoint** (auto-generada)
- **Estimación de costos** detallada
- **Roadmap de alto nivel** (12 meses)
- **Matriz de riesgos**

**Stakeholders eligen:** Opción B (Balanceada)

---

### Fase 2: Descomposición en Epics (Transición TOGAF → Scrum)

**TOGAF ADM nos dio la visión.** Ahora Scrum ejecuta.

**Agente de Planificación convierte Arquitectura → Epics:**

```python
epic_agent = Agent(
    model="gpt-4",
    system_prompt="""Descompone la arquitectura target en Epics implementables.
    Cada Epic debe:
    - Tener valor de negocio independiente
    - Ser implementable en 4-8 sprints
    - Tener dependencias claras
    - Incluir criterios de aceptación"""
)

epics = epic_agent.decompose(selected_architecture)
```

**Output: Product Backlog Inicial**

```markdown
# Epic 1: Infraestructura Cloud Base [8 Story Points]
**Valor:** Fundación para todo lo demás
**Criterios:**
- [x] AWS Landing Zone configurado
- [x] VPC, Subnets, Security Groups
- [x] CI/CD pipeline base (GitHub Actions)
- [x] Monitoreo (CloudWatch, Datadog)

**Dependencias:** Ninguna (puede empezar Ya)

---

# Epic 2: Migración de Base de Datos [13 Story Points]
**Valor:** Reduce costos de licenciamiento Oracle
**Criterios:**
- [x] RDS PostgreSQL configurado
- [x] Schema migrado
- [x] DMS (Database Migration Service) configurado
- [x] Validación de integridad de datos
- [x] Rollback plan probado

**Dependencias:** Epic 1

---

# Epic 3: Extracción de Servicio de Pagos [21 Story Points]
**Valor:** Primer microservicio, permite escalar pagos independientemente
**Criterios:**
- [x] Payment Service (TypeScript + NestJS)
- [x] Desacoplado del monolito (Event-Driven)
- [x] Tests >80% cobertura
- [x] Deployed en ECS Fargate
- [x] 0 downtime durante migración

**Dependencias:** Epic 1, Epic 2

---

# Epic 4: Sistema de Autenticación Moderno [13 Story Points]
# Epic 5: API Gateway [8 Story Points]
# Epic 6: Migración de Checkout [21 Story Points]
...
```

---

### Fase 3: Sprints Aumentados por IA

**Scrum tradicional + IA = Hyper-Scrum**

#### Sprint Planning Aumentado

**Antes (sin IA):**
- Duración: 4 horas
- Equipo estima Story Points manualmente
- Riesgo de subestimación

**Ahora (con IA):**
- Duración: 1.5 horas
- IA asiste en estimación y detección de riesgos

```python
sprint_planning_agent = Agent(
    model="gpt-4",
    tools=[
        Tool("estimate_story", story_estimator),
        Tool("detect_risks", risk_detector),
        Tool("suggest_subtasks", task_decomposer)
    ]
)

# Para cada User Story
for story in sprint_backlog:
    # IA sugiere estimación
    estimate = sprint_planning_agent.estimate(story, team_velocity)

    # IA detecta riesgos
    risks = sprint_planning_agent.detect_risks(story)

    # IA sugiere subtareas
    subtasks = sprint_planning_agent.decompose(story)

    # Equipo revisa y ajusta
    team.review(estimate, risks, subtasks)
```

**Ejemplo de Output:**

```markdown
## User Story: "Como usuario, quiero pagar con tarjeta de crédito"

### Estimación IA: 8 Story Points
**Justificación:**
- Integración con Stripe API (3 SP)
- Validación de datos sensibles (2 SP)
- Compliance PCI-DSS (2 SP)
- Tests de seguridad (1 SP)

### Riesgos Detectados:
⚠️ **ALTO:** Compliance PCI-DSS requiere certificación
  Mitigación: Usar Stripe Elements (compliance delegado a Stripe)

⚠️ **MEDIO:** Testing de pagos reales es complejo
  Mitigación: Usar Stripe Test Mode + mocks

### Subtareas Sugeridas:
1. [ ] Configurar Stripe SDK
2. [ ] Crear Payment Intent endpoint
3. [ ] Implementar frontend de checkout (Stripe Elements)
4. [ ] Manejar webhooks (payment.succeeded, payment.failed)
5. [ ] Tests unitarios
6. [ ] Tests de integración con Stripe Test Mode
7. [ ] Documentación de flujo de pago
8. [ ] Security review con checklist PCI
```

**Equipo valida:** "8 SP está bien, aceptamos las subtareas sugeridas"

---

#### Daily Standup Aumentado

**Tradicional:** 15 minutos, manual

**Con IA:** 5 minutos + reporte automático

```python
# Agente escucha standup y genera insights
standup_agent = Agent(
    model="gpt-4",
    tools=[
        Tool("analyze_blockers", blocker_analyzer),
        Tool("predict_delays", delay_predictor),
        Tool("suggest_solutions", solution_suggester)
    ]
)

# Durante el standup
dev1: "Ayer terminé login, hoy haré logout, bloqueado por API de sesiones"
dev2: "Ayer avancé en pagos, hoy termino, sin blockers"
dev3: "Ayer intenté integrar Stripe, hay un error 401, bloqueado"

# IA analiza en tiempo real
analysis = standup_agent.analyze([dev1, dev2, dev3])
```

**Output (mostrado al Scrum Master):**

```
⚠️ ALERTA: 2 blockers detectados

BLOCKER 1: Dev1 esperando API de sesiones
  Impacto: Logout (3 SP) en riesgo
  Sugerencia: Usar mock temporal mientras se completa API
  Responsable sugerido: Dev2 (tiene contexto de APIs)

BLOCKER 2: Dev3 con error 401 en Stripe
  Diagnóstico probable: API Key incorrecta o no configurada
  Solución sugerida: Verificar STRIPE_SECRET_KEY en .env
  Documentación: https://stripe.com/docs/keys

📊 Predicción: Sprint en riesgo de completar solo 18/21 SP si blockers no se resuelven hoy
```

Scrum Master actúa inmediatamente basándose en insights.

---

#### AI Code Review Continuo

**Durante el Sprint:**

```python
# Cada Pull Request es analizado por IA
code_review_agent = Agent(
    model="claude-3-opus",
    tools=[
        Tool("check_architecture", architecture_checker),
        Tool("check_security", security_scanner),
        Tool("check_performance", performance_analyzer),
        Tool("check_tests", test_coverage_checker)
    ],
    system_prompt="""Eres un arquitecto senior revisando código.
    Valida que el código:
    1. Sigue la arquitectura target de TOGAF
    2. No introduce deuda técnica
    3. No tiene vulnerabilidades de seguridad
    4. Tiene performance adecuado
    5. Tiene tests suficientes"""
)

# PR abierto
pr = github.get_pull_request(123)
review = code_review_agent.review(pr.diff, architecture_target)
```

**Output (comentario automático en PR):**

```markdown
## 🤖 AI Architecture Review

### ✅ Cumplimiento de Arquitectura: 85% (APROBADO)
- ✅ Usa el patrón Repository correcto
- ✅ Dependency Injection implementado correctamente
- ⚠️ SUGERENCIA: Mover lógica de negocio de Controller a UseCase

### 🔒 Seguridad: APROBADO
- ✅ Input validation presente
- ✅ SQL Injection: No detectado (usa ORM correctamente)
- ✅ XSS: No aplica (backend only)

### ⚡ Performance: ATENCIÓN REQUERIDA
- ⚠️ PROBLEMA: Línea 45 - Query N+1 detectado
  ```typescript
  // Esto hará N queries adicionales
  for (const user of users) {
    user.orders = await orderRepo.findByUser(user.id); // ❌
  }

  // RECOMENDACIÓN: Usar eager loading
  const users = await userRepo.find({ relations: ['orders'] }); // ✅
  ```

### 🧪 Tests: 78% cobertura (⚠️ Bajo del objetivo 80%)
- ❌ Falta test para caso de error de pago rechazado
- ❌ Falta test para timeout de API externa

---

**Decisión:** APROBAR CON CAMBIOS SUGERIDOS
**Prioridad cambios:** Alta (performance issue puede causar problemas en producción)
```

**Developer corrige, IA re-valida automáticamente.**

---

#### Sprint Review con IA Analytics

**Al final del Sprint:**

```python
sprint_review_agent = Agent(
    model="gpt-4",
    tools=[
        Tool("analyze_velocity", velocity_analyzer),
        Tool("compare_vs_plan", plan_comparator),
        Tool("extract_learnings", learning_extractor)
    ]
)

sprint_report = sprint_review_agent.analyze(sprint_data)
```

**Output:**

```markdown
# Sprint 3 - Review Report

## 📊 Métricas
- **Story Points Completados:** 18/21 (85%)
- **Velocidad:** 18 SP (vs. 20 SP histórico) - ⚠️ 10% bajo
- **Bugs Introducidos:** 2 (vs. 1.5 promedio) - ⚠️ Ligeramente alto
- **Code Review Time:** 4 horas (vs. 8 horas sin IA) - ✅ 50% mejora

## 🎯 Objetivos vs. Resultados
- ✅ Payment Service deployed (Epic 3 - 80% completo)
- ⚠️ Checkout integration incompleto (queda 1 story)
- ✅ 0 downtime durante deployment

## 🔍 Análisis de Causa Raíz (Velocity baja)
IA detectó:
1. **Blocker de Stripe** (Día 2-3): Costó 1.5 días resolver
   → Lección: Validar API keys al inicio del sprint
2. **Subestimación:** Story "Webhook handling" era 3 SP, debió ser 5 SP
   → Pattern detectado: Integraciones externas típicamente +50% tiempo
3. **Code Review delays:** 2 PRs esperaron 1 día por review humano
   → Recomendación: Dar más autoridad a AI review para PRs simples

## 📈 Tendencias (últimos 5 sprints)
- Velocity estable: 18-20 SP
- Bug rate bajando (era 3 bugs/sprint hace 3 sprints)
- IA review adoption: 100% PRs (antes 0%)

## 🚀 Recomendaciones para Sprint 4
1. Aumentar Story Points de integraciones externas en +50%
2. Completar story pendiente de checkout (3 SP)
3. Continuar Epic 3, iniciar Epic 4 (Auth)
4. Dedicar 2 SP a refactoring de performance issues detectados por IA
```

---

#### Sprint Retrospective con IA Facilitator

```python
retro_agent = Agent(
    model="gpt-4",
    system_prompt="""Facilita retrospectivas identificando patterns
    que humanos pueden no ver. Analiza datos de:
    - Commits, PRs, code reviews
    - Tiempo en cada tarea
    - Comunicaciones (Slack, comments)
    - Sentiment analysis

    Sugiere mejoras de proceso."""
)

retro_insights = retro_agent.facilitate(sprint_data, team_feedback)
```

**Output:**

```markdown
# Sprint Retrospective - AI Insights

## 🟢 Qué salió bien
- Adoption de AI code review → 50% reducción en tiempo de review
- Comunicación mejorada (Slack activity +30% vs. sprint anterior)
- Pair programming en problema complejo (Stripe) → resuelto más rápido

## 🔴 Qué salió mal
- Blockers no escalados rápidamente
- Subestimación de integraciones externas (recurrente)

## 🔵 Insights de IA (no obvios para humanos)

### Pattern Detectado: "Context Switching Cost"
IA analizó commits y detectó:
- Dev3 cambió entre 4 tareas diferentes en Sprint
- Tiempo promedio para "volver a contexto": 25 minutos
- **Costo total:** ~4 horas perdidas en context switching

**Recomendación:** Asignar a cada dev máximo 2 tareas en paralelo

### Sentiment Analysis (de comments en PRs/Slack)
- 😊 Sentimiento general: Positivo (75%)
- 😐 Dev2: Neutral (50%) - posible frustración con blockers
- **Acción sugerida:** 1-1 con Dev2 para identificar problemas

### Communication Patterns
- Canal #dev-help usado efectivamente
- Pero: Dev1 y Dev3 nunca colaboraron (podrían aprender uno del otro)
- **Recomendación:** Asignar una tarea de pair programming entre ellos

## 🎯 Action Items para Sprint 4
1. [ ] Limitar a 2 tareas paralelas por developer
2. [ ] Scrum Master 1-1 con Dev2
3. [ ] Dev1 y Dev3: Pair programming en 1 tarea compleja
4. [ ] Crear checklist de "API Integration" con buffer +50% tiempo
```

---

### Fase 4: Validación Continua contra Visión TOGAF

**El peligro de Scrum puro:** Derivar de la visión original

**Solución:** IA valida cada Sprint contra Architecture Target

```python
# Cada 2 sprints (mensualmente)
alignment_agent = Agent(
    model="gpt-4",
    system_prompt="""Valida que el progreso de desarrollo sigue
    alineado con la Architecture Vision de TOGAF.

    Detecta:
    - Architecture drift (desviación no intencional)
    - Deuda técnica acumulándose
    - Decisiones que comprometen requisitos no funcionales"""
)

alignment_report = alignment_agent.validate(
    current_architecture=get_deployed_architecture(),
    target_architecture=togaf_target_architecture,
    nfrs=non_functional_requirements
)
```

**Output (cada mes):**

```markdown
# Architecture Alignment Report - Mes 3

## 📐 Alineación con Target: 88% (✅ BUENO)

### ✅ En línea con visión
- Microservicios: 3/15 extraídos (20% progreso - on track para 12 meses)
- Cloud migration: 30% workload en AWS (target: 100% mes 12)
- Performance: Latency p99 = 95ms (target: <100ms) ✅

### ⚠️ Desviaciones detectadas

**1. Database Strategy**
- **Target TOGAF:** PostgreSQL como DB principal
- **Realidad:** Team añadió MongoDB para catálogo de productos
- **Impacto:**
  - ✅ Mejor performance para catálogo
  - ⚠️ Mayor complejidad operacional (2 DBs)
  - ⚠️ Costo adicional $500/mes
- **Recomendación:** Aceptar (beneficio > costo), pero documentar en ADR

**2. Security**
- **Target TOGAF:** Todos los servicios con mTLS
- **Realidad:** Solo Payment Service tiene mTLS
- **Impacto:**
  - 🔴 RIESGO DE SEGURIDAD
  - Servicios internos comunicándose sin encriptación
- **Acción requerida:** ALTA PRIORIDAD
  - Implementar Service Mesh (Istio) en próximos 2 sprints
  - Costo: 8 SP

**3. Observabilidad**
- **Target TOGAF:** Distributed tracing en todos servicios
- **Realidad:** Solo 50% servicios tienen tracing
- **Impacto:**
  - Debugging de issues distribuidos es difícil
- **Acción:** MEDIA PRIORIDAD
  - Añadir OpenTelemetry a servicios faltantes
  - Costo: 5 SP

## 📊 Proyección a 12 meses
Basado en velocity actual (18 SP/sprint):
- ✅ Migración de servicios críticos: 100% (completado mes 11)
- ⚠️ Security hardening: 85% (falta tiempo para 100%)
- ✅ Performance targets: 100%
- ✅ Cost reduction: 32% (supera target de 30%)

**Recomendación:** Aumentar equipo en +2 developers o extender timeline a 14 meses
para completar 100% security requirements.

## 🎯 Actions para próximo Sprint
1. [ ] Crear Epic de "Service Mesh Implementation" (8 SP)
2. [ ] Documentar ADR-005: "Adopción de MongoDB para Catálogo"
3. [ ] Security review de servicios sin mTLS
```

**Product Owner y Architect revisan juntos, ajustan roadmap si es necesario.**

---

### Fase 5: Adaptación del Roadmap (Feedback Loop)

**TOGAF tradicional:** Roadmap fijo

**TSA Framework 2026:** Roadmap adaptativo basado en learnings

```python
roadmap_agent = Agent(
    model="gpt-4",
    system_prompt="""Actualiza el roadmap de 12 meses basándote en:
    - Velocity real vs. estimada
    - Riesgos emergentes
    - Cambios de negocio
    - Learnings técnicos

    Mantén visión estratégica pero ajusta tácticas."""
)

# Cada trimestre
updated_roadmap = roadmap_agent.update(
    original_roadmap=togaf_roadmap,
    actual_progress=sprint_data,
    new_business_requirements=business_changes,
    technical_learnings=learnings
)
```

**Ejemplo de Actualización:**

```markdown
# Roadmap Update - Q2

## Cambios vs. Plan Original

### ❌ Cancelado: Epic 7 "Mobile App"
**Razón:** Negocio decidió priorizar B2B sobre B2C
**Liberado:** 34 SP → reasignados a Security

### 🆕 Nuevo: Epic 8 "B2B API"
**Razón:** Cliente Enterprise (50% revenue) lo requiere
**Prioridad:** ALTA
**Estimación:** 21 SP
**Timeline:** Q3

### 📅 Reprogramado: Epic 6 "Advanced Analytics"
**Razón:** Dependencia de Data Lake aún no lista
**Original:** Q2 → **Nuevo:** Q4

## Roadmap Actualizado (próximos 6 meses)

```
Q2 (Mes 4-6):
  ├─ Epic 4: Auth System ✅ (completado)
  ├─ Epic 5: API Gateway (en progreso)
  ├─ Epic 9: Service Mesh (nuevo, security)
  └─ Epic 8: B2B API (nuevo)

Q3 (Mes 7-9):
  ├─ Epic 10: Advanced Search
  ├─ Epic 11: Notification System
  └─ Epic 12: Performance Optimization

Q4 (Mes 10-12):
  ├─ Epic 6: Advanced Analytics (reprogramado)
  ├─ Epic 13: Disaster Recovery
  └─ Epic 14: Final Security Hardening
```

**Stakeholders aprueban cambios basándose en datos, no opiniones.**

---

### Herramientas del TSA Framework 2026

#### 1. **TOGAF-AI Vision Generator**
```bash
$ tsa vision --stakeholders="CTO, CFO, Head of Product" \
             --constraints="budget:3M,timeline:12mo" \
             --goals="reduce_cost:30%,scale:10x"

✨ Generando Architecture Vision con Claude Opus...
📋 Entrevistando stakeholders (simulado)...
🎨 Diseñando 3 opciones arquitectónicas...
💰 Estimando costos...
📊 Validando contra constraints...

✅ Vision Document generado: architecture-vision-v1.md
✅ Presentación ejecutiva: vision-deck.pptx
✅ Roadmap de alto nivel: roadmap-12mo.md

Tiempo total: 4 horas (vs. 4 semanas tradicional)
```

#### 2. **Scrum-AI Sprint Assistant**
```bash
$ tsa sprint plan --epic="Payment Service" \
                   --velocity=18 \
                   --duration="2 weeks"

🤖 Analizando Epic...
📝 Generando User Stories...
🎯 Estimando Story Points...
⚠️  Detectando riesgos...
✅ Sprint Backlog generado

User Stories (18 SP total):
1. [5 SP] Integración con Stripe API
   Riesgos: ⚠️ Requiere PCI compliance

2. [3 SP] Webhook handling
   Riesgos: ✅ Ninguno

3. [8 SP] Payment retry logic
   Riesgos: ⚠️ Complejidad alta

4. [2 SP] Payment history UI
   Riesgos: ✅ Ninguno

📋 Archivo generado: sprint-5-backlog.md
```

#### 3. **Architecture Drift Detector**
```bash
$ tsa validate alignment --frequency=weekly

🔍 Escaneando arquitectura actual...
📐 Comparando con TOGAF target...
🔴 3 desviaciones detectadas

CRITICAL:
  - mTLS no implementado en 5/8 servicios

WARNING:
  - MongoDB añadido (no en plan original)
  - Tracing incompleto

📊 Reporte completo: alignment-report-week-12.md
🎯 Actions sugeridas agregadas a Product Backlog
```

#### 4. **AI Retrospective Facilitator**
```bash
$ tsa retro --sprint=5 --analyze-sentiment --detect-patterns

🧠 Analizando sprint data...
💬 Sentiment analysis de comunicaciones...
🔍 Detectando patterns ocultos...

Insights generados:
1. Context switching cost: 4 horas perdidas
2. Dev2 showing signs of frustration
3. Pair programming correlates with 30% faster completion

📋 Retro board generado: retro-sprint-5.md
```

---

### Roles en TSA Framework 2026

| Rol | Responsabilidades | Herramientas IA |
|-----|-------------------|-----------------|
| **Enterprise Architect** | Visión estratégica TOGAF, validación de alineación | Vision Generator, Drift Detector |
| **Product Owner** | Priorización de backlog, balance estrategia/ejecución | Epic Decomposer, Roadmap Updater |
| **Scrum Master** | Facilitar sprints, remover blockers | Sprint Assistant, Retro Facilitator, Standup Analyzer |
| **Developers** | Implementar, validar arquitectura | Code Review Agent, Story Estimator |
| **AI Governance Officer** (nuevo rol) | Supervisar agentes IA, validar outputs, entrenar modelos | Todas las herramientas |

---

### Métricas de Éxito TSA

**Velocidad:**
- ⚡ Vision de TOGAF: 3-5 días (vs. 4-8 semanas)
- ⚡ Sprint Planning: 1.5 horas (vs. 4 horas)
- ⚡ Code Review: 4 horas (vs. 8 horas)

**Calidad:**
- 📈 Alineación con target arquitectónico: >85%
- 📉 Bugs introducidos: -40%
- 📉 Security issues: -60%

**Predicción:**
- 🎯 Accuracy de estimación: +35%
- 🎯 Detección temprana de riesgos: +50%

**ROI de IA:**
- 💰 Costo de herramientas IA: $2K/mes (OpenAI API + Claude)
- 💰 Ahorro en tiempo: ~$50K/mes (architects + developers)
- 💰 ROI: **25x**

---

### Caso de Estudio: Banco Digital (TSA en acción)

**Empresa:** FinTech con 500 employees, migrando de monolito a cloud

**ANTES (TOGAF puro):**
- 📅 Vision phase: 8 semanas
- 📅 Implementación: 24 meses estimados
- 💰 Costo: $15M
- ⚠️ Riesgo: ALTO (plan fijo, sin adaptación)

**DESPUÉS (TSA Framework):**
- 📅 Vision phase: 5 días (con IA)
- 📅 Implementación: 14 meses reales
- 💰 Costo: $9M ($6M ahorrados)
- ✅ Riesgo: MEDIO (adaptación continua)

**Factores de éxito:**
1. **IA generó vision en días:** Arquitectos se enfocaron en validar, no crear desde cero
2. **Sprints validados continuamente:** 0 "sorpresas" al final del proyecto
3. **Detección temprana de riesgos:** Security issue detectado en Sprint 3, no en producción
4. **Adaptación a cambios de negocio:** Pivote de B2C a B2B manejado sin retrasos

---

### Limitaciones y Consideraciones

#### ⚠️ Cuándo NO usar TSA Framework

1. **Proyectos pequeños (<6 meses):** Overhead no justificado, usar Scrum puro
2. **Equipos <5 personas:** TOGAF es excesivo, usar arquitectura ligera
3. **Dominio totalmente nuevo:** IA no tiene contexto suficiente, requiere más humanos

#### 🔒 Governance de IA

**Problema:** IA puede alucinar o sugerir arquitecturas inviables

**Solución:**
```python
# Arquitecto SIEMPRE valida outputs de IA
@require_human_approval
def finalize_architecture(ai_suggestion):
    human_review = architect.review(ai_suggestion)
    if human_review.approved:
        return ai_suggestion
    else:
        return ai_suggestion.revise(human_review.feedback)
```

**Regla de oro:**
> "IA propone, humano dispone. Nunca implementar sugerencia de IA sin validación de experto."

---

### El Futuro: TSA 2.0 (2027+)

**Tendencias emergentes:**

1. **Agentes Autónomos de Arquitectura:**
   - No solo sugieren, implementan (con supervisión)
   - Self-healing architecture

2. **Predictive Roadmapping:**
   - IA predice cambios de mercado
   - Roadmap se adapta automáticamente

3. **Arquitectura Generativa:**
   - Describes problema de negocio
   - IA genera arquitectura + código + tests + docs
   - Humano solo valida

4. **Digital Twin de Arquitectura:**
   - Simulación completa de sistema antes de construir
   - Testing de escalabilidad sin gastar en cloud

**Visión 2030:**
> "El arquitecto del futuro orquesta agentes IA que diseñan e implementan sistemas, mientras el humano se enfoca en alinear tecnología con visión de negocio y tomar decisiones éticas/estratégicas."

---

### Conclusión: Lo Mejor de Tres Mundos

**TOGAF** nos da:
- ✅ Visión estratégica
- ✅ Alineación con negocio
- ✅ Governance

**Scrum** nos da:
- ✅ Velocidad de ejecución
- ✅ Adaptabilidad
- ✅ Entrega continua de valor

**IA** nos da:
- ✅ Aceleración exponencial
- ✅ Detección de patterns invisibles
- ✅ Automatización de tareas repetitivas

**TSA Framework 2026 = TOGAF + Scrum + IA**

No es reemplazar uno con otro. Es **sinergia**.

**Resultado:** Arquitecturas empresariales robustas, entregadas con velocidad de startup, potenciadas por IA.

---

## Certificaciones

### Arquitectura
- **AWS Certified Solutions Architect**
- **Azure Solutions Architect Expert**
- **Google Cloud Professional Cloud Architect**
- **TOGAF Certification**

### DevOps
- **AWS Certified DevOps Engineer**
- **Kubernetes Administrator (CKA)**
- **Certified Kubernetes Application Developer (CKAD)**

### Seguridad
- **CISSP (Certified Information Systems Security Professional)**
- **CEH (Certified Ethical Hacker)**
- **AWS Certified Security Specialty**

### Agile
- **Certified Scrum Master (CSM)**
- **SAFe Agilist**
- **PMI-ACP (Agile Certified Practitioner)**

### Desarrollo
- **Oracle Certified Professional Java**
- **Microsoft Certified: Azure Developer**

**Estrategia:**
1. Empieza con cloud (AWS/Azure/GCP)
2. Luego arquitectura (TOGAF)
3. Finalmente especialización (Seguridad, ML, etc.)

---

# PARTE V: Integración y Casos de Estudio

## Caso de Estudio Final: "The Autonomous AI Bank"

### Escenario

Construir un **neobanco digital** que usa IA para:
- Detectar fraude en tiempo real
- Recomendar productos financieros
- Automatizar soporte al cliente
- Procesar préstamos automáticamente

**Requisitos:**
- 1M usuarios activos
- 10,000 transacciones/segundo
- Disponibilidad 99.99%
- Compliance regulatorio (PCI-DSS, SOC2)

---

### Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        API Gateway                          │
│                     (Kong / AWS API Gateway)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌───────────────┐   ┌──────────────┐   ┌──────────────┐
│  Auth Service │   │ User Service │   │Transaction   │
│   (OAuth2)    │   │  (CRUD)      │   │   Service    │
└───────────────┘   └──────────────┘   └──────────────┘
        ↓                   ↓                   ↓
    ┌────────┐          ┌──────┐        ┌─────────────┐
    │ Cognito│          │ PG   │        │  Fraud ML   │
    └────────┘          │ DB   │        │  (SageMaker)│
                        └──────┘        └─────────────┘
                                               ↓
                                        ┌─────────────┐
                                        │ Kafka Queue │
                                        └─────────────┘
                                               ↓
                        ┌──────────────────────┼────────────────┐
                        ↓                      ↓                ↓
                ┌──────────────┐      ┌──────────────┐  ┌────────────┐
                │ Notification │      │ Support Agent│  │ Analytics  │
                │   Service    │      │  (LangGraph) │  │  Service   │
                └──────────────┘      └──────────────┘  └────────────┘
                        ↓                      ↓                ↓
                  ┌──────────┐         ┌─────────────┐   ┌──────────┐
                  │SNS/Twilio│         │  Vector DB  │   │ Redshift │
                  └──────────┘         │  (Pinecone) │   └──────────┘
                                       └─────────────┘
```

---

### Implementación por Skills y Pilares

#### Skill 1: Manejar Claude y LLMs
**Aplicación:**
```
Prompt a Claude: "Genera el código base de los microservicios para un neobanco
usando Clean Architecture, con:
- Auth Service (OAuth2 + JWT)
- User Service (CRUD + eventos)
- Transaction Service (ACID + detección de fraude)
Lenguaje: TypeScript con NestJS
DB: PostgreSQL con TypeORM
Tests: Jest con >80% cobertura
Docker compose para desarrollo local"
```

Claude genera estructura completa en 5 minutos. Tú auditas y refinas.

#### Skill 2: Bases de Datos

**PostgreSQL (Transacciones):**
```sql
-- Tabla de transacciones con índices optimizados
CREATE TABLE transactions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  amount DECIMAL(10, 2),
  type VARCHAR(20),
  status VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_transactions ON transactions(user_id, created_at DESC);
CREATE INDEX idx_fraud_check ON transactions(status, created_at) WHERE status = 'pending';
```

**Vector DB (Recomendaciones):**
```python
# Embeddings de perfil de usuario para recomendar productos
import pinecone

index = pinecone.Index("user-profiles")

# Buscar usuarios similares
results = index.query(
    vector=user_embedding,
    top_k=10,
    include_metadata=True
)

# Recomendar productos que usuarios similares tienen
recommended_products = get_products_from_similar_users(results)
```

#### Skill 3: Agentes (LangGraph)

**Agente de Soporte:**
```python
from langgraph import Agent, Tool, StateGraph

# Herramientas del agente
tools = [
    Tool("check_account_balance", check_balance),
    Tool("check_transaction_status", check_transaction),
    Tool("search_knowledge_base", search_kb),
    Tool("escalate_to_human", escalate),
    Tool("analyze_sentiment", analyze_sentiment)
]

# Estado del agente
class AgentState:
    messages: list
    sentiment: str
    escalated: bool

# Grafo de decisión
graph = StateGraph(AgentState)

def handle_query(state):
    sentiment = analyze_sentiment(state.messages[-1])

    if sentiment == "angry" or "complex" in state.messages[-1]:
        return escalate(state)

    response = agent.run(state.messages[-1], tools=tools)
    return response

agent = Agent(
    model="gpt-4",
    tools=tools,
    system_prompt="""Eres un agente de soporte bancario.
    Ayuda con: balance, transacciones, productos.
    Escala a humano si: cliente enojado, problema complejo, solicitud de préstamo."""
)
```

**Flujo:**
1. Cliente pregunta: "¿Dónde está mi transferencia de $500?"
2. Agente usa `check_transaction_status`
3. Encuentra transacción pendiente
4. Responde: "Tu transferencia está en proceso, llegará en 2 horas"

#### Skill 4: Orquestar Deep Learning

**Modelo de Detección de Fraude:**
```python
# Entrenamiento (una vez)
import xgboost as xgb

model = xgb.XGBClassifier()
model.fit(X_train, y_train)  # Features: monto, hora, ubicación, historial

# Deploy a SageMaker
from sagemaker import Model

model = Model(
    model_data="s3://models/fraud-detector.tar.gz",
    role=role,
    image_uri=container
)

predictor = model.deploy(
    instance_type="ml.m5.large",
    initial_instance_count=2
)

# Inference en tiempo real
def check_fraud(transaction):
    features = extract_features(transaction)
    prediction = predictor.predict(features)

    if prediction["fraud_probability"] > 0.8:
        block_transaction(transaction)
        notify_user(transaction.user_id)
```

**MLOps:**
```python
# Monitoreo de drift
from evidently import ColumnDriftMetric

report = Report(metrics=[
    ColumnDriftMetric("amount"),
    ColumnDriftMetric("transaction_time")
])

report.run(reference_data=train_data, current_data=production_data)

if report.has_drift:
    trigger_retraining()
```

#### Skill 5: Docker y CI/CD

**Dockerfile (multi-stage):**
```dockerfile
# Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --production
USER node
CMD ["node", "dist/main.js"]
```

**GitHub Actions CI/CD:**
```yaml
name: Transaction Service CI/CD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: |
          npm ci
          npm test -- --coverage

      - name: Security Scan
        run: |
          npm audit
          snyk test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build & Push Docker
        run: |
          docker build -t transaction-service:${{ github.sha }} .
          docker push transaction-service:${{ github.sha }}

      - name: Deploy to EKS
        run: |
          kubectl set image deployment/transaction-service \
            transaction-service=transaction-service:${{ github.sha }}
          kubectl rollout status deployment/transaction-service
```

#### Skill 6: Debugear Código

**Tracing Distribuido:**
```javascript
// Instrumentar con OpenTelemetry
const { trace } = require('@opentelemetry/api');

async function processTransaction(transaction) {
  const span = trace.getTracer('transaction-service').startSpan('processTransaction');

  span.setAttribute('transaction.id', transaction.id);
  span.setAttribute('transaction.amount', transaction.amount);

  try {
    // 1. Verificar balance
    const balanceSpan = trace.getTracer('transaction-service').startSpan('checkBalance');
    const balance = await checkBalance(transaction.userId);
    balanceSpan.end();

    // 2. Detectar fraude
    const fraudSpan = trace.getTracer('transaction-service').startSpan('fraudCheck');
    const isFraud = await checkFraud(transaction);
    fraudSpan.end();

    if (isFraud) {
      span.setAttribute('fraud.detected', true);
      throw new FraudError('Transaction blocked');
    }

    // 3. Procesar pago
    const paymentSpan = trace.getTracer('transaction-service').startSpan('processPayment');
    await processPayment(transaction);
    paymentSpan.end();

    span.setStatus({ code: 1 }); // OK
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: 2, message: error.message }); // ERROR
    throw error;
  } finally {
    span.end();
  }
}
```

**Jaeger UI:**
```
Request: POST /transactions
  └─ processTransaction (500ms)
      ├─ checkBalance (50ms)
      ├─ fraudCheck (300ms) ← LENTO!
      └─ processPayment (150ms)
```

Detectas que `fraudCheck` es el cuello de botella. Optimizas cacheando resultados de modelo ML.

#### Skill 7: Generar Plans

**Prompt Inicial:**
```
Genera un plan de arquitectura detallado para un neobanco con:

Funcionalidades:
- Cuentas y transacciones
- Detección de fraude en tiempo real
- Soporte automatizado con IA
- Recomendaciones de productos

Requisitos:
- 1M usuarios activos
- 10,000 transacciones/segundo
- Latencia <100ms p99
- Disponibilidad 99.99%
- Compliance PCI-DSS

Restricciones:
- Presupuesto $10,000/mes en AWS
- Equipo de 5 developers

Incluye:
1. Diagrama de arquitectura de alto nivel
2. Elección de tecnologías con justificación
3. Estrategia de escalabilidad
4. Estrategia de seguridad
5. Estimación de costos
6. Plan de fases de implementación
```

Claude genera plan completo que luego refinas con tu expertise.

---

### Pilares Integrados

#### Pilar 1: Ingeniería de Prompt
- Usaste prompts avanzados para generar código base
- Verificaste todo código generado por IA
- Detectaste y corregiste vulnerabilidades

#### Pilar 2: Fundamentos
- Aplicaste patrones de diseño (Strategy para canales de notificación)
- Optimizaste algoritmos (índices de DB, caché)
- Modelaste lógica de negocio compleja (reglas de fraude)

#### Pilar 3: Protocolos
- API Gateway con REST
- gRPC para comunicación interna entre microservicios
- GraphQL para frontend flexible

#### Pilar 4: Git
- Trunk-Based Development
- Feature flags para despliegue gradual
- Git bisect para encontrar regresiones

#### Pilar 5: Cloud
- AWS EKS (Kubernetes)
- AWS SageMaker (ML)
- AWS RDS (PostgreSQL)
- Serverless (Lambda para notificaciones)

#### Pilar 6: DevOps
- CI/CD completo con GitHub Actions
- Deploy automático a producción
- Canary deployments

#### Pilar 7: Seguridad
- Shift Left Security (Snyk en CI)
- OWASP: Protección contra Injection, Broken Auth
- PCI-DSS compliance (encriptación, auditoría)
- Gestión de secretos con AWS Secrets Manager

---

### Niveles de Arquitectura en el Proyecto

**Application Architecture:**
- Estructura interna de cada microservicio
- Clean Architecture con capas: Controllers → Use Cases → Entities

**Solution Architecture:**
- Integración de microservicios
- Event-driven con Kafka
- API Gateway como punto de entrada

**Enterprise Architecture:**
- Alineación con estrategia de negocio (IA para reducir costos de soporte)
- Roadmap tecnológico (migrar de monolito legacy a microservicios)
- Estandarización (todos los servicios usan TypeScript + NestJS)

---

### Resultados

**Performance:**
- Latencia p99: 80ms ✅
- Throughput: 15,000 transacciones/segundo ✅

**Costo:**
- Total: $8,500/mes ✅ (bajo presupuesto)

**Seguridad:**
- 0 incidentes de seguridad en producción ✅
- Certificación PCI-DSS obtenida ✅

**Negocio:**
- Soporte automatizado: 70% de queries resueltas sin humano
- Detección de fraude: 95% accuracy, $2M ahorrados/año
- Time-to-market: 6 meses (vs 18 meses estimados sin IA)

---

## Ruta de Carrera del Arquitecto

### Nivel 1: Developer (0-3 años)
**Foco:** Dominar programación y fundamentos

**Habilidades:**
- ✅ Algoritmos y estructuras de datos
- ✅ Un lenguaje profundamente (Java, Python, JavaScript)
- ✅ Git básico
- ✅ Bases de datos (SQL)
- ✅ APIs REST

**Certificaciones sugeridas:**
- Ninguna aún, enfócate en construir

### Nivel 2: Senior Developer (3-5 años)
**Foco:** Liderar features completas, mentorear juniors

**Habilidades:**
- ✅ Múltiples lenguajes y paradigmas
- ✅ Patrones de diseño
- ✅ Arquitectura de aplicaciones
- ✅ TDD, CI/CD
- ✅ Cloud básico

**Certificaciones sugeridas:**
- AWS Certified Developer

### Nivel 3: Application Architect (5-7 años)
**Foco:** Diseñar aplicaciones completas

**Habilidades:**
- ✅ Clean Architecture, DDD
- ✅ Performance optimization
- ✅ Security (OWASP)
- ✅ Docker, Kubernetes
- ✅ Múltiples DBs (SQL, NoSQL, Vector)

**Certificaciones sugeridas:**
- AWS Certified Solutions Architect - Associate
- Certified Kubernetes Administrator (CKA)

### Nivel 4: Solution Architect (7-10 años)
**Foco:** Integrar múltiples sistemas, liderar proyectos grandes

**Habilidades:**
- ✅ Arquitecturas distribuidas
- ✅ Event-driven architecture
- ✅ APIs avanzadas (gRPC, GraphQL)
- ✅ Service Mesh
- ✅ **IA/ML integration** ← CRÍTICO en 2025
- ✅ Agentes inteligentes

**Certificaciones sugeridas:**
- AWS Certified Solutions Architect - Professional
- TOGAF 9 Certified

### Nivel 5: Enterprise Architect (10+ años)
**Foco:** Alinear tecnología con estrategia de negocio, transformación digital

**Habilidades:**
- ✅ Todas las anteriores
- ✅ Business acumen
- ✅ Roadmaps tecnológicos multi-año
- ✅ Vendor management
- ✅ Presupuestos ($M)
- ✅ Liderazgo organizacional

**Certificaciones sugeridas:**
- TOGAF 9 Certified (Master)
- Zachman Framework

---

### Ruta Específica 2025: El Arquitecto Aumentado por IA

**Diferenciador clave:** Dominio de IA aplicada a arquitectura

**Año 1-2:**
- Aprende a usar Claude/GPT-4 avanzadamente
- Construye proyectos con LLM APIs

**Año 3-4:**
- Diseña sistemas de agentes
- Integra modelos ML en producción

**Año 5+:**
- Lidera transformación digital con IA
- Arquitecturas autónomas (self-healing, auto-scaling basado en predicciones)

---

## Conclusión

El arquitecto moderno del 2025 es un **orquestador de sistemas complejos** que:

1. **Domina fundamentos inmutables** (algoritmos, patrones, protocolos)
2. **Aprovecha IA** para 10x productividad (Claude, LLMs, Agentes)
3. **Diseña para escala** (cloud, microservicios, distribución)
4. **Prioriza seguridad** (DevSecOps, OWASP, compliance)
5. **Gestiona datos profundamente** (SQL, NoSQL, Vector DBs)
6. **Automatiza todo** (CI/CD, IaC, MLOps)
7. **Comunica efectivamente** (stakeholders técnicos y de negocio)

**No es un especialista en una tecnología.** Es un **generalista profundo** con expertise en múltiples dominios y la capacidad de aprender cualquier nueva tecnología rápidamente.

**La IA no reemplaza al arquitecto.** Lo **aumenta**, liberándolo de tareas repetitivas para enfocarse en decisiones estratégicas de alto impacto.

---

**Esta versión v4.0 Completa es la guía definitiva e integral del arquitecto de software moderno, combinando tradición y vanguardia.**

---

## Próximos Pasos Recomendados

1. **Elige un proyecto** del Caso de Estudio y construyelo
2. **Obtén una certificación** de cloud (AWS/Azure/GCP)
3. **Contribuye a open source** para demostrar expertise
4. **Escribe sobre arquitectura** (blog, LinkedIn)
5. **Mentorea** a developers junior
6. **Nunca dejes de aprender** - la tecnología evoluciona constantemente

**¡Éxito en tu camino como Arquitecto de Software!**
