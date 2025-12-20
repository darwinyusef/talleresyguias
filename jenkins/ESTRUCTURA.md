# 📁 Estructura del Proyecto - Jenkins con Docker

```
jenkins/
│
├── �� DOCUMENTACIÓN
│   ├── README.md                    # Guía completa del taller (540+ líneas)
│   ├── INICIO_RAPIDO.md             # Quick start guide
│   ├── INDICE.md                    # Índice navegable completo
│   ├── EJERCICIOS.md                # Ejercicios prácticos por niveles
│   ├── RESUMEN.md                   # Resumen ejecutivo
│   ├── ESTRUCTURA.md                # Este archivo
│   └── .gitignore                   # Archivos ignorados por Git
│
├── 🐳 DOCKER/
│   ├── docker-compose.yml           # Compose con Jenkins + SonarQube + Nexus
│   ├── Dockerfile.jenkins           # Jenkins personalizado con Docker CLI
│   └── Dockerfile.agent             # Agente Jenkins con herramientas
│
├── 📝 PIPELINES/
│   ├── 01-basic-pipeline.jenkinsfile        # Pipeline básico (Nivel: Principiante)
│   ├── 02-docker-build.jenkinsfile          # Build Docker (Nivel: Intermedio)
│   ├── 03-nodejs-app.jenkinsfile            # App Node.js completa (Nivel: Intermedio)
│   ├── 04-parallel-stages.jenkinsfile       # Ejecución paralela (Nivel: Avanzado)
│   └── 05-kubernetes-deploy.jenkinsfile     # Deploy K8s (Nivel: Avanzado)
│
├── 🎯 EJEMPLOS/
│   └── nodejs-app/                  # Aplicación Node.js completa
│       ├── src/
│       │   ├── index.js             # API REST con Express
│       │   └── utils/
│       │       └── logger.js        # Winston logger
│       ├── tests/
│       │   └── api.test.js          # Tests con Jest + Supertest
│       ├── Dockerfile               # Multi-stage build optimizado
│       ├── docker-compose.yml       # Compose para desarrollo
│       ├── Jenkinsfile              # Pipeline CI/CD completo
│       ├── package.json             # Dependencias y scripts
│       ├── .eslintrc.json           # Configuración ESLint
│       ├── dockerignore.txt         # Archivos ignorados en Docker
│       └── README.md                # Documentación de la app
│
└── 🛠️ SCRIPTS/
    ├── backup-jenkins.sh            # Backup automatizado de Jenkins
    ├── restore-jenkins.sh           # Restore con backup de seguridad
    └── cleanup-old-builds.sh        # Limpieza de builds antiguos
```

---

## 📊 Desglose por Categoría

### 📚 Documentación (6 archivos)
- Guías completas
- Inicio rápido
- Índice navegable
- Ejercicios prácticos
- Resumen ejecutivo

### 🐳 Docker (3 archivos)
- Compose completo
- Jenkins personalizado
- Agente personalizado

### 📝 Pipelines (5 archivos)
- Básico a avanzado
- Docker builds
- Kubernetes deploy
- Ejecución paralela

### 🎯 Ejemplos (8 archivos)
- API REST completa
- Tests incluidos
- Docker optimizado
- Pipeline CI/CD

### 🛠️ Scripts (3 archivos)
- Backup/Restore
- Limpieza automática
- Permisos configurados

---

## 🎯 Archivos por Nivel

### Nivel Principiante
```
INICIO_RAPIDO.md
pipelines/01-basic-pipeline.jenkinsfile
docker/docker-compose.yml
```

### Nivel Intermedio
```
README.md (Módulos 1-5)
pipelines/02-docker-build.jenkinsfile
pipelines/03-nodejs-app.jenkinsfile
ejemplos/nodejs-app/
```

### Nivel Avanzado
```
README.md (Módulos 6-9)
pipelines/04-parallel-stages.jenkinsfile
pipelines/05-kubernetes-deploy.jenkinsfile
EJERCICIOS.md (Nivel 4-5)
```

---

## 📈 Líneas de Código por Archivo

### Documentación
- README.md: ~540 líneas
- INICIO_RAPIDO.md: ~200 líneas
- INDICE.md: ~350 líneas
- EJERCICIOS.md: ~450 líneas
- RESUMEN.md: ~300 líneas

### Docker
- docker-compose.yml: ~60 líneas
- Dockerfile.jenkins: ~80 líneas
- Dockerfile.agent: ~50 líneas

### Pipelines
- 01-basic-pipeline: ~60 líneas
- 02-docker-build: ~150 líneas
- 03-nodejs-app: ~250 líneas
- 04-parallel-stages: ~200 líneas
- 05-kubernetes-deploy: ~350 líneas

### Aplicación Node.js
- src/index.js: ~200 líneas
- tests/api.test.js: ~150 líneas
- Jenkinsfile: ~120 líneas

### Scripts
- backup-jenkins.sh: ~70 líneas
- restore-jenkins.sh: ~90 líneas
- cleanup-old-builds.sh: ~60 líneas

**Total: ~3,500+ líneas de código**

---

## 🔗 Dependencias entre Archivos

### Flujo de Aprendizaje
```
INICIO_RAPIDO.md
    ↓
docker/docker-compose.yml
    ↓
pipelines/01-basic-pipeline.jenkinsfile
    ↓
pipelines/02-docker-build.jenkinsfile
    ↓
ejemplos/nodejs-app/
    ↓
pipelines/03-nodejs-app.jenkinsfile
    ↓
EJERCICIOS.md
```

### Flujo de Deployment
```
ejemplos/nodejs-app/src/
    ↓
ejemplos/nodejs-app/tests/
    ↓
ejemplos/nodejs-app/Dockerfile
    ↓
ejemplos/nodejs-app/Jenkinsfile
    ↓
docker/docker-compose.yml
```

---

## 🎨 Características por Archivo

### README.md
- ✅ 9 módulos de aprendizaje
- ✅ Ejemplos de código
- ✅ Troubleshooting
- ✅ Mejores prácticas

### INICIO_RAPIDO.md
- ✅ Instalación en 5 minutos
- ✅ Primer pipeline en 10 minutos
- ✅ Comandos útiles
- ✅ Troubleshooting común

### EJERCICIOS.md
- ✅ 15+ ejercicios
- ✅ 5 niveles de dificultad
- ✅ Proyecto final
- ✅ Desafíos adicionales

### docker-compose.yml
- ✅ Jenkins LTS
- ✅ SonarQube
- ✅ Nexus
- ✅ Networks configuradas

### Pipelines
- ✅ Ejemplos progresivos
- ✅ Comentarios detallados
- ✅ Mejores prácticas
- ✅ Error handling

### nodejs-app
- ✅ API REST completa
- ✅ CRUD operations
- ✅ Tests 100% coverage
- ✅ Docker optimizado

---

## 💾 Tamaño Estimado

```
Total del proyecto: ~2 MB
├── Documentación: ~500 KB
├── Docker configs: ~50 KB
├── Pipelines: ~100 KB
├── Aplicación Node.js: ~200 KB
└── Scripts: ~50 KB
```

---

## 🚀 Cómo Navegar

### Para Empezar
1. Lee [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
2. Instala con [docker/docker-compose.yml](docker/docker-compose.yml)
3. Prueba [pipelines/01-basic-pipeline.jenkinsfile](pipelines/01-basic-pipeline.jenkinsfile)

### Para Aprender
1. Lee [README.md](README.md) completo
2. Sigue [INDICE.md](INDICE.md) por módulos
3. Practica con [EJERCICIOS.md](EJERCICIOS.md)

### Para Implementar
1. Revisa [ejemplos/nodejs-app/](ejemplos/nodejs-app/)
2. Adapta pipelines a tu proyecto
3. Usa [scripts/](scripts/) para mantenimiento

---

[Volver al README](README.md) | [Ver Índice](INDICE.md)
