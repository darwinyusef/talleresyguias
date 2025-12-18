# 🎯 Índice Rápido de Talleres

## 📁 Estructura de Archivos

```
iafirst/
│
├── 📘 TALLERES PRINCIPALES
│   ├── ⭐ TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md (NUEVO!)
│   ├── 🔌 TALLER_FASTMCP_FASTAPI_COMPLETO.md
│   ├── 🔗 TALLER_FASTMCP_INTEGRACION_PROYECTOS_N8N.md
│   └── ⚙️ TALLER_N8N_BACKEND_MCP_COMPLETO.md
│
├── 📚 CURSOS Y GUÍAS
│   ├── 🗺️ 00_PLAN_INTEGRACION_IA_ARQUITECTURA.md
│   ├── 🤖 01_ML_TECNICAS_DESARROLLADORES_2026.md
│   └── 🔥 02_PYTORCH_CURSO_COMPLETO.md
│
└── 💻 PROYECTO PRÁCTICO
    └── mlops-project/
        ├── README.md
        ├── docker-compose.yml
        ├── Makefile
        ├── scripts/
        └── src/
```

---

## ⚡ Quick Access

### 🆕 NUEVO: MLOps Completo
**Archivo:** `TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md`

```bash
# Ver taller
cat TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md

# Iniciar proyecto
cd mlops-project
make quickstart
```

**Contiene:**
- ✅ Docker para PyTorch & TensorFlow
- ✅ Event-Driven con RabbitMQ
- ✅ RAG con ChromaDB + LangChain
- ✅ MLflow + Prometheus + Grafana
- ✅ Proyecto production-ready

---

### 🔥 Top 3 Talleres Más Completos

#### 1. MLOps Docker Event-Driven (78 KB)
```bash
# Leer
less TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md

# Proyecto
cd mlops-project && make up
```

#### 2. n8n Backend MCP (82 KB)
```bash
less TALLER_N8N_BACKEND_MCP_COMPLETO.md
```

#### 3. FastMCP + FastAPI (74 KB)
```bash
less TALLER_FASTMCP_FASTAPI_COMPLETO.md
```

---

## 🎓 Por Tema

### 🤖 Machine Learning & MLOps
```bash
# PyTorch desde cero
cat 02_PYTORCH_CURSO_COMPLETO.md

# Técnicas ML modernas
cat 01_ML_TECNICAS_DESARROLLADORES_2026.md

# MLOps completo
cat TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md
```

### 🔌 APIs & Backend
```bash
# FastAPI + MCP
cat TALLER_FASTMCP_FASTAPI_COMPLETO.md

# Integración n8n
cat TALLER_FASTMCP_INTEGRACION_PROYECTOS_N8N.md
```

### ⚙️ Automatización
```bash
# n8n workflows
cat TALLER_N8N_BACKEND_MCP_COMPLETO.md
```

### 🏗️ Arquitectura
```bash
# Plan de integración IA
cat 00_PLAN_INTEGRACION_IA_ARQUITECTURA.md
```

---

## 🎯 Por Nivel

### 🟢 Principiante
1. `02_PYTORCH_CURSO_COMPLETO.md` - Fundamentos PyTorch
2. `01_ML_TECNICAS_DESARROLLADORES_2026.md` - ML moderno

### 🟡 Intermedio
1. `TALLER_FASTMCP_FASTAPI_COMPLETO.md` - APIs modernas
2. `TALLER_FASTMCP_INTEGRACION_PROYECTOS_N8N.md` - Integración
3. `TALLER_N8N_BACKEND_MCP_COMPLETO.md` - Automatización

### 🔴 Avanzado
1. `TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md` - MLOps completo
2. `00_PLAN_INTEGRACION_IA_ARQUITECTURA.md` - Arquitectura
3. `mlops-project/` - Proyecto producción

---

## 🚀 Quick Start Commands

```bash
# Ver todos los talleres
ls -lh *.md

# Buscar por palabra clave
grep -r "Docker" *.md

# Abrir en VSCode
code TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md

# Iniciar proyecto MLOps
cd mlops-project
make quickstart

# Ver servicios
make ps

# Logs
make logs
```

---

## 📊 Estadísticas

| Taller | Tamaño | Nivel | Duración |
|--------|--------|-------|----------|
| MLOps Docker Event-Driven | 78 KB | 🔴 Avanzado | 8-12h |
| n8n Backend MCP | 82 KB | 🟡 Intermedio | 8-10h |
| FastMCP FastAPI | 74 KB | 🟡 Intermedio | 6-8h |
| FastMCP n8n | 62 KB | 🟡 Intermedio | 4-6h |
| Plan Integración IA | 62 KB | 🔴 Avanzado | 2-4h |
| ML Técnicas 2026 | 44 KB | 🟡 Intermedio | 4-6h |
| PyTorch Curso | 32 KB | 🟢 Principiante | 6-8h |

**Total:** 434 KB de contenido educativo | 38-54 horas de aprendizaje

---

## 🔍 Búsqueda Rápida

### Por Tecnología

```bash
# Docker
grep -l "Docker" *.md
# → TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md

# PyTorch
grep -l "PyTorch" *.md
# → 02_PYTORCH_CURSO_COMPLETO.md
# → TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md

# FastAPI
grep -l "FastAPI" *.md
# → TALLER_FASTMCP_FASTAPI_COMPLETO.md
# → TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md

# RAG
grep -l "RAG" *.md
# → TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md
# → 01_ML_TECNICAS_DESARROLLADORES_2026.md

# n8n
grep -l "n8n" *.md
# → TALLER_N8N_BACKEND_MCP_COMPLETO.md
# → TALLER_FASTMCP_INTEGRACION_PROYECTOS_N8N.md
```

---

## 🎁 Bonus: Proyecto MLOps

```bash
cd mlops-project/

# Ver estructura
ls -la

# Archivos importantes:
# - README.md          → Documentación completa
# - docker-compose.yml → 11 servicios integrados
# - Makefile           → 30+ comandos útiles
# - .env.example       → Configuración
# - scripts/           → Scripts de entrenamiento y testing
```

### Servicios del Proyecto

1. 🐍 PyTorch Service (GPU)
2. 🧠 TensorFlow Service (GPU)
3. 🔍 RAG Service + ChromaDB
4. 📨 RabbitMQ (Event Bus)
5. 🗄️ Redis (Cache)
6. 🐘 PostgreSQL (MLflow)
7. 📊 MLflow (Tracking)
8. 📈 Prometheus (Metrics)
9. 📉 Grafana (Dashboards)

```bash
# Iniciar todo
make up

# UIs disponibles:
# http://localhost:5000  - MLflow
# http://localhost:3000  - Grafana
# http://localhost:9090  - Prometheus
# http://localhost:15672 - RabbitMQ
```

---

## 📱 Navegación Rápida en Terminal

```bash
# Función helper (añadir a ~/.bashrc o ~/.zshrc)
taller() {
  case $1 in
    mlops)     cat TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md | less ;;
    pytorch)   cat 02_PYTORCH_CURSO_COMPLETO.md | less ;;
    fastapi)   cat TALLER_FASTMCP_FASTAPI_COMPLETO.md | less ;;
    n8n)       cat TALLER_N8N_BACKEND_MCP_COMPLETO.md | less ;;
    ml)        cat 01_ML_TECNICAS_DESARROLLADORES_2026.md | less ;;
    list)      ls -lh *.md ;;
    *)         echo "Uso: taller [mlops|pytorch|fastapi|n8n|ml|list]" ;;
  esac
}

# Uso:
# taller mlops
# taller list
```

---

## 🎯 Próximos Pasos

1. **Lee el README principal:** `README.md`
2. **Elige tu ruta:** Ver sección "Rutas de Aprendizaje"
3. **Empieza con un taller:** Según tu nivel
4. **Practica con el proyecto:** `cd mlops-project`

---

**¡Todo listo para aprender! 🚀**
