# Curso Completo: Arquitectura de Software - El Arquitecto Aumentado (v3)
## La Nueva Era: IA, Nube y Seguridad

Bienvenido a la **Versión 3** del curso. Esta edición representa un cambio de paradigma. Ya no solo diseñamos sistemas; orquestamos inteligencia artificial, gobernamos la nube y garantizamos la seguridad desde el primer commit.

Esta guía integra los **7 Pilares del Desarrollo de Software Moderno**, transformando el rol del Arquitecto Técnico en un **Editor, Auditor y Estratega**.

---

## Tabla de Contenidos

1.  [Pilar 1: El Nuevo Rol - Ingeniería de Prompt y Verificación](#1-pilar-1-el-nuevo-rol---ingeniería-de-prompt-y-verificación)
2.  [Pilar 2: Fundamentos Inmutables (Lo que la IA no reemplaza)](#2-pilar-2-fundamentos-inmutables-lo-que-la-ia-no-reemplaza)
3.  [Pilar 3: Protocolos Distribuidos y APIs](#3-pilar-3-protocolos-distribuidos-y-apis)
4.  [Pilar 4: Control de Versiones Avanzado (Git)](#4-pilar-4-control-de-versiones-avanzado-git)
5.  [Pilar 5: Cloud Computing y Arquitectura Nativa](#5-pilar-5-cloud-computing-y-arquitectura-nativa)
6.  [Pilar 6: Automatización y DevOps (CI/CD)](#6-pilar-6-automatización-y-devops-cicd)
7.  [Pilar 7: Ciberseguridad (DevSecOps)](#7-pilar-7-ciberseguridad-devsecops)
8.  [Caso de Estudio Integrador: "The AI-Native Bank"](#8-caso-de-estudio-integrador-the-ai-native-bank)

---

## 1. Pilar 1: El Nuevo Rol - Ingeniería de Prompt y Verificación
**(Crítico)**

El programador ya no es un mero "escritor de código". Ahora es un arquitecto que dirige a una IA.

*   **Prompt Engineering para Arquitectos:**
    *   *Contexto:* No pidas "una función de login". Pide "Un módulo de autenticación OAuth2 seguro, stateless, usando JWT, siguiendo principios SOLID y manejando errores de borde".
    *   *Iteración:* El primer resultado de la IA es un borrador. Tu trabajo es refinarlo.
*   **Verificación y Auditoría:**
    *   La IA alucina. Tu responsabilidad es detectar vulnerabilidades, ineficiencias (O(n^2) donde debería ser O(n)) y deuda técnica introducida por el copilot.
    *   **Regla:** Nunca hagas commit de código generado por IA que no entiendas al 100%.

---

## 2. Pilar 2: Fundamentos Inmutables
**(Indispensable)**

La sintaxis cambia, los fundamentos permanecen. Estos son tus lentes para juzgar el código de la IA.

*   **Algoritmos y Estructuras de Datos:** Saber cuándo usar un `HashMap` vs un `Tree` es vital para el rendimiento.
*   **Patrones de Diseño:** Singleton, Factory, Strategy, Observer. La IA tiende a escribir código procedimental; tú debes imponer la estructura arquitectónica.
*   **Lógica de Negocio:** La IA no entiende tu negocio, tú sí. La traducción de reglas de negocio a lógica de software es tu dominio exclusivo.

---

## 3. Pilar 3: Protocolos Distribuidos y APIs
**(Indispensable)**

En un mundo de microservicios, la comunicación lo es todo.

*   **REST vs. GraphQL:**
    *   *REST:* Estándar, cacheable, verbos HTTP.
    *   *GraphQL:* Flexible, evita over-fetching, pero complejo de cachear.
*   **Formatos:** Dominio absoluto de JSON y Protobuf (para gRPC).
*   **HTTP/HTTPS:** Entender códigos de estado (200, 401, 403, 500), headers, y handshake TLS.

---

## 4. Pilar 4: Control de Versiones Avanzado (Git)
**(Indispensable)**

El código es un activo colaborativo.

*   **Flujos de Trabajo:**
    *   *Trunk-Based Development:* Integración frecuente a `main`. Ideal para CI/CD rápido.
    *   *Git Flow:* Ramas de feature, release, hotfix. Más tradicional.
*   **Técnicas Avanzadas:**
    *   `git rebase` vs `git merge`: Mantener un historial limpio.
    *   `git bisect`: Encontrar el commit exacto que rompió el build (útil cuando la IA introduce bugs sutiles).

---

## 5. Pilar 5: Cloud Computing y Arquitectura Nativa
**(Esencial)**

"En mi máquina funciona" ya no es excusa.

*   **Modelos de Servicio:** IaaS (EC2), PaaS (Heroku), FaaS (Lambda/Serverless).
*   **Contenedores:** Docker como unidad estándar de despliegue.
*   **Orquestación:** Kubernetes (K8s) para manejar miles de contenedores.
*   **Infrastructure as Code (IaC):** Terraform o CloudFormation. Tu infraestructura también es código y debe ser versionada.

---

## 6. Pilar 6: Automatización y DevOps (CI/CD)
**(Esencial)**

Si duele, automatízalo.

*   **CI (Integración Continua):** Cada commit dispara tests automáticos. Si falla, no entra.
*   **CD (Despliegue Continuo):** De `git push` a producción sin intervención humana (si pasan los tests).
*   **Pipelines:** GitHub Actions, GitLab CI, Jenkins. Definir los pasos de build, test, lint, security scan y deploy.

---

## 7. Pilar 7: Ciberseguridad (DevSecOps)
**(Esencial)**

La seguridad no es una capa final, es parte del diseño.

*   **Shift Left Security:** Integrar seguridad desde el diseño, no al final.
*   **OWASP Top 10:** Protegerse contra Inyección SQL, XSS, Broken Auth.
*   **Gestión de Secretos:** Nunca subir `.env` o API Keys al repo. Usar Vault o AWS Secrets Manager.
*   **Validación de Entradas:** "Never trust user input". Ni siquiera si el usuario es una IA interna.

---

## 8. Caso de Estudio Integrador: "The AI-Native Bank"

**Escenario:** Construir un neobanco seguro y escalable.

1.  **Diseño (Pilar 1 & 2):** Usas IA para generar el boilerplate de microservicios en Go, pero validas que use Patrones de Diseño seguros (Adapter para legacy).
2.  **API (Pilar 3):** Expones una API GraphQL para el frontend móvil y gRPC para comunicación interna rápida.
3.  **Código (Pilar 4):** El equipo usa Trunk-Based Development. Los PRs generados por IA son revisados por humanos expertos.
4.  **Infraestructura (Pilar 5):** Todo corre en Kubernetes (EKS) sobre AWS. Base de datos Aurora Serverless.
5.  **Pipeline (Pilar 6):** GitHub Actions corre tests unitarios, de integración y análisis estático (SonarQube).
6.  **Seguridad (Pilar 7):** El pipeline incluye un paso de `snyk` para buscar vulnerabilidades en dependencias y escaneo de contenedores antes de desplegar.

---
*Esta versión v3 redefine al arquitecto técnico no como un constructor de muros, sino como el director de una orquesta tecnológica compleja y automatizada.*
