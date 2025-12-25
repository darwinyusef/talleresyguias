# Estructura del Proyecto

## 📁 Directorios y Archivos

```
claude-code-guide/                    # ← Directorio PÚBLICO (no oculto)
│
├── 📄 README.md                      # Guía completa (28KB)
├── 📄 QUICKSTART.md                  # Inicio rápido
├── 📄 INDEX.md                       # Índice navegable
├── 📄 SUMMARY.md                     # Resumen ejecutivo
├── 📄 ESTRUCTURA.md                  # Este archivo
├── 📄 .gitignore                     # Git ignore rules
│
├── 📂 guides/                        # Guías detalladas
│   └── subagents.md                  # Guía de subagents
│
└── 📂 examples/                      # Ejemplos funcionales
    │
    ├── 📂 plugins/                   # Plugins de ejemplo
    │   └── database-query-tool/
    │       ├── index.js              # Implementación del plugin
    │       └── package.json          # Configuración npm
    │
    ├── 📂 mcp-servers/              # Servidores MCP
    │   └── github-mcp/
    │       ├── server.js             # Servidor MCP GitHub
    │       └── package.json          # Dependencias
    │
    ├── 📂 hooks/                     # Hooks de ejemplo
    │   └── pre-commit-check.sh       # Hook de validación
    │
    └── 📂 skills/                    # Skills reutilizables
        └── code-review-skill.md      # Skill de code review
```

## 🔍 Diferencia entre Directorios

### `claude-code-guide/` (Este proyecto)
- ✅ **Público y visible**
- ✅ Documentación y guías
- ✅ Ejemplos para aprender
- ✅ Código de referencia
- ✅ Se versiona en Git
- ✅ Compartible entre proyectos

**Ubicación**: `/Users/yusefgonzalez/proyectos/talleres/claude-code-guide/`

### `.claude/` (Configuración del proyecto)
- ⚙️ **Oculto** (empieza con punto)
- ⚙️ Configuración específica del proyecto
- ⚙️ Skills personalizados
- ⚙️ Hooks activos
- ⚙️ Puede estar en .gitignore
- ⚙️ Por proyecto individual

**Ubicación típica**: `tu-proyecto/.claude/`

## 📋 Ejemplo de Uso

### 1. Estructura Típica de un Proyecto con Claude Code

```
mi-proyecto/
├── src/
├── tests/
├── package.json
│
├── .claude/                          # ← Configuración OCULTA del proyecto
│   ├── config.json                   # Configuración local
│   ├── skills/                       # Skills del proyecto
│   │   ├── deploy.md
│   │   └── test-runner.md
│   └── hooks/                        # Hooks activos
│       └── pre-commit.sh
│
└── .claudeignore                     # Archivos a ignorar
```

### 2. Esta Guía (Recurso Compartido)

```
talleres/
├── mlflow-mlops-workshop/
│
└── claude-code-guide/                # ← Guía PÚBLICA (este repo)
    ├── README.md                     # Documentación
    ├── guides/                       # Tutoriales
    └── examples/                     # Código de ejemplo
        ├── plugins/                  # Para copiar a tu proyecto
        ├── hooks/                    # Para copiar a .claude/hooks/
        └── skills/                   # Para copiar a .claude/skills/
```

## 🔄 Flujo de Trabajo Recomendado

### Paso 1: Estudiar la Guía
```bash
cd claude-code-guide
cat README.md
```

### Paso 2: Copiar Ejemplos a tu Proyecto
```bash
# En tu proyecto
mkdir -p .claude/hooks
mkdir -p .claude/skills

# Copiar hook de ejemplo
cp ../claude-code-guide/examples/hooks/pre-commit-check.sh .claude/hooks/

# Copiar skill de ejemplo
cp ../claude-code-guide/examples/skills/code-review-skill.md .claude/skills/
```

### Paso 3: Configurar Claude Code
```bash
# En tu proyecto
cat > .claude/config.json << 'EOF'
{
  "model": "claude-sonnet-4",
  "hooks": {
    "user-prompt-submit": "bash .claude/hooks/pre-commit-check.sh"
  }
}
EOF
```

### Paso 4: Usar
```bash
cd tu-proyecto
claude-code /skill code-review
```

## 📦 Instalación de Plugins

Los plugins de esta guía se instalan globalmente o por proyecto:

### Opción 1: Global
```bash
cd claude-code-guide/examples/plugins/database-query-tool
npm install -g .
```

### Opción 2: Local al proyecto
```bash
cd tu-proyecto
npm install ../claude-code-guide/examples/plugins/database-query-tool
```

## 🚀 MCP Servers

Los MCP servers se ejecutan como servicios separados:

```bash
# Terminal 1: Iniciar MCP server
cd claude-code-guide/examples/mcp-servers/github-mcp
npm install
npm start

# Terminal 2: Configurar en tu proyecto
cd tu-proyecto
cat > .claude/config.json << 'EOF'
{
  "mcpServers": [
    {
      "name": "github",
      "url": "http://localhost:3000",
      "enabled": true
    }
  ]
}
EOF

# Terminal 3: Usar Claude Code
claude-code
```

## 🎯 Resumen

| Directorio | Tipo | Propósito | Compartir |
|------------|------|-----------|-----------|
| `claude-code-guide/` | Público | Documentación y ejemplos | ✅ Sí |
| `.claude/` | Oculto | Configuración del proyecto | ❌ No (opcional) |
| `.claudeignore` | Oculto | Exclusiones | ❌ No (opcional) |

## 💡 Tips

1. **Este repositorio (claude-code-guide/)**: Mantén actualizado y comparte
2. **Tu configuración (.claude/)**: Personaliza para cada proyecto
3. **Ejemplos**: Copia y adapta según necesites
4. **Git**: Puedes versionar `.claude/` o agregarlo a `.gitignore`

## 📚 Lectura Relacionada

- [README.md](README.md) - Guía completa
- [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
- [INDEX.md](INDEX.md) - Índice de recursos

---

**Nota**: La estructura con `.claude/` oculto es una convención de Claude Code para configuración específica del proyecto, similar a `.git/` o `.vscode/`.
