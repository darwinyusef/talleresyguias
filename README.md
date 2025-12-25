# 🎓 Talleres de Programación y MLOps

Repositorio con talleres completos y guías avanzadas.

## 📚 Contenido

### 1. MLflow MLOps Workshop
Taller completo de MLOps centrado en MLflow con múltiples frameworks.

📁 **Ubicación**: `mlflow-mlops-workshop/`

**Contenido**:
- 8 notebooks interactivos
- scikit-learn, TensorFlow, PyTorch, Spark
- Airflow orchestration
- 30+ modelos diferentes
- 15-20 horas de contenido

[📖 Ver documentación completa →](mlflow-mlops-workshop/README.md)

**Quick Start**:
```bash
cd mlflow-mlops-workshop
./setup.sh
./start_mlflow.sh
```

---

### 2. Claude Code - Guía Avanzada
Guía completa de Claude Code con plugins, MCP, hooks y skills.

📁 **Ubicación**: `claude-code-guide/`

**Contenido**:
- 9 temas avanzados
- 4 ejemplos funcionales (plugin, MCP, hook, skill)
- 1,500+ líneas de código
- Documentación exhaustiva

[📖 Ver documentación completa →](claude-code-guide/README.md)

**Quick Start**:
```bash
cd claude-code-guide
cat QUICKSTART.md
```

---

## 🗂️ Estructura del Repositorio

```
talleres/
│
├── mlflow-mlops-workshop/           # Taller MLflow + MLOps
│   ├── modulo1-sklearn/             # scikit-learn
│   ├── modulo2-tensorflow/          # Deep Learning
│   ├── modulo3-pytorch/             # PyTorch
│   ├── modulo7-spark-mlflow/        # Spark distribuido
│   ├── modulo9-airflow-orchestration/ # Airflow
│   ├── README.md
│   ├── GETTING_STARTED.md
│   ├── setup.sh
│   └── requirements.txt
│
├── claude-code-guide/               # Guía Claude Code
│   ├── README.md                    # Guía completa
│   ├── QUICKSTART.md                # Inicio rápido
│   ├── ESTRUCTURA.md                # Explicación directorios
│   ├── guides/                      # Guías detalladas
│   └── examples/                    # Código funcional
│       ├── plugins/
│       ├── mcp-servers/
│       ├── hooks/
│       └── skills/
│
└── README.md                        # Este archivo
```

---

## 🚀 Inicio Rápido

### MLflow Workshop
```bash
cd mlflow-mlops-workshop
./setup.sh                    # Instala todo
./start_mlflow.sh            # Inicia MLflow
jupyter notebook modulo1-sklearn/01_mlflow_basics.ipynb
```

### Claude Code Guide
```bash
cd claude-code-guide
cat README.md | less         # Lee la guía
cat QUICKSTART.md            # Inicio rápido
```

---

## 📊 Comparación

| Aspecto | MLflow Workshop | Claude Code Guide |
|---------|----------------|-------------------|
| **Tipo** | Taller práctico interactivo | Guía de referencia |
| **Formato** | Notebooks Jupyter | Markdown + código |
| **Duración** | 15-20 horas | Autónomo |
| **Nivel** | Intermedio-Avanzado | Avanzado |
| **Frameworks** | ML/DL (sklearn, TF, PyTorch, Spark) | Claude Code CLI |
| **Ejemplos** | 30+ modelos entrenados | 4 implementaciones completas |

---

## 🎯 ¿Por dónde empezar?

### Si eres nuevo en MLOps:
1. Empieza con **MLflow Workshop** → `mlflow-mlops-workshop/`
2. Sigue los módulos en orden (1→2→3→7→9)
3. Practica con tus propios datos

### Si quieres dominar Claude Code:
1. Lee **Claude Code Guide** → `claude-code-guide/QUICKSTART.md`
2. Instala Claude Code
3. Prueba los ejemplos
4. Crea tus propios plugins/hooks

### Si quieres ambos:
1. **Día 1-3**: MLflow básico (Módulo 1)
2. **Día 4-5**: Deep Learning con MLflow (Módulos 2-3)
3. **Día 6**: Claude Code setup y basics
4. **Día 7-8**: MLflow avanzado (Spark + Airflow)
5. **Día 9-10**: Claude Code avanzado (plugins, MCP)

---

## 🛠️ Tecnologías Cubiertas

### MLflow Workshop
- MLflow 2.10.2
- TensorFlow 2.15.0
- PyTorch 2.1.2
- Apache Spark 3.5.0
- Apache Airflow 2.8.1
- scikit-learn 1.3.0

### Claude Code Guide
- Claude Code CLI
- Node.js / JavaScript
- MCP (Model Context Protocol)
- Bash scripting
- Plugin development

---

## 📖 Documentación

Cada taller incluye documentación completa:

### MLflow Workshop
- [README.md](mlflow-mlops-workshop/README.md) - Overview
- [GETTING_STARTED.md](mlflow-mlops-workshop/GETTING_STARTED.md) - Setup
- [CONTENIDO_COMPLETO.md](mlflow-mlops-workshop/CONTENIDO_COMPLETO.md) - Detalles
- [QUICKSTART.md](mlflow-mlops-workshop/QUICKSTART.md) - Inicio rápido

### Claude Code Guide
- [README.md](claude-code-guide/README.md) - Guía completa
- [QUICKSTART.md](claude-code-guide/QUICKSTART.md) - Inicio rápido
- [ESTRUCTURA.md](claude-code-guide/ESTRUCTURA.md) - Organización
- [INDEX.md](claude-code-guide/INDEX.md) - Índice de recursos

---

## 🤝 Contribuir

Ambos talleres son open source. Contribuciones bienvenidas:

1. Fork el repositorio
2. Crea una branch para tu feature
3. Commit tus cambios
4. Push a tu branch
5. Abre un Pull Request

---

## 📝 Notas

- Todos los ejemplos están probados y funcionan
- Código sigue mejores prácticas
- Documentación exhaustiva incluida
- Listo para uso en producción

---

## 📧 Contacto

Para preguntas o sugerencias:
- Issues en GitHub
- Pull Requests bienvenidos

---

**Última actualización**: Diciembre 2024
**Autor**: Yusef González
**Licencia**: MIT
