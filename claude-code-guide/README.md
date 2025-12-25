# Claude Code - Guía Completa Avanzada

![Claude Code](https://img.shields.io/badge/Claude-Code-7C3AED)

Guía avanzada para dominar Claude Code CLI, la herramienta oficial de Anthropic para desarrollo asistido por IA.

## 📚 Tabla de Contenidos

1. [Introducción a Claude Code](#introducción)
2. [Subagents](#subagents)
3. [Plugins](#plugins)
4. [Agent Skills](#agent-skills)
5. [Output Styles](#output-styles)
6. [Hooks](#hooks)
7. [Programmatic Usage](#programmatic-usage)
8. [Model Context Protocol (MCP)](#mcp)
9. [Troubleshooting](#troubleshooting)

## 🚀 Introducción

Claude Code es un CLI interactivo que permite:
- Desarrollo asistido por IA
- Ejecución de tareas complejas
- Integración con tu flujo de trabajo
- Extensibilidad mediante plugins y hooks

> **📁 Nota Importante sobre Directorios**:
> - **`claude-code-guide/`** (este directorio) → Guía pública con documentación y ejemplos
> - **`.claude/`** (en tu proyecto) → Configuración oculta específica del proyecto
>
> Ver [ESTRUCTURA.md](ESTRUCTURA.md) para más detalles.

### Instalación Rápida

```bash
npm install -g @anthropic-ai/claude-code
claude-code login
```

## 🤖 Subagents

Los **subagents** son agentes especializados que Claude Code puede lanzar para tareas específicas.

### Tipos de Subagents

#### 1. General Purpose Agent
```python
# Usa el Task tool
"Busca todos los archivos que contienen 'MLflow' y crea un resumen"
```

#### 2. Explore Agent
```python
# Especializado en explorar codebases
"¿Cómo funciona el sistema de autenticación?"
"Encuentra todos los endpoints de API"
```

Niveles de thoroughness:
- `quick`: Búsqueda básica
- `medium`: Exploración moderada
- `very thorough`: Análisis exhaustivo

#### 3. Plan Agent
```python
# Planificación de tareas
"Crea un plan para migrar de Python 3.8 a 3.11"
```

### Cuándo Usar Subagents

✅ **Usar subagents cuando**:
- Necesitas explorar un codebase grande
- Búsquedas complejas con múltiples criterios
- Análisis arquitectónico
- Tareas multi-paso que requieren autonomía

❌ **NO usar subagents cuando**:
- Sabes exactamente qué archivo leer
- Búsqueda simple de una clase/función específica
- Edición de 2-3 archivos conocidos

### Ejemplo de Uso

```python
# En lugar de:
# grep -r "class UserModel" .

# Usa Explore agent:
"Explora el codebase para entender cómo se manejan los modelos de usuario"
```

Ver [guides/subagents.md](guides/subagents.md) para más detalles.

---

## 🔌 Plugins

Los plugins extienden las capacidades de Claude Code.

### Tipos de Plugins

1. **Tools**: Agregan nuevas herramientas
2. **Skills**: Workflows especializados
3. **MCP Servers**: Integración con servicios externos

### Crear un Plugin Personalizado

```bash
cd .claude_app/plugins
mkdir my-plugin
cd my-plugin
```

**Estructura básica**:
```
my-plugin/
├── package.json
├── index.js
└── README.md
```

**package.json**:
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "claudeCode": {
    "type": "tool",
    "description": "Mi plugin personalizado"
  },
  "main": "index.js"
}
```

**index.js**:
```javascript
module.exports = {
  name: 'my-custom-tool',
  description: 'Herramienta personalizada',
  parameters: {
    type: 'object',
    properties: {
      input: {
        type: 'string',
        description: 'Entrada para la herramienta'
      }
    },
    required: ['input']
  },
  async execute({ input }) {
    // Tu lógica aquí
    return {
      success: true,
      result: `Procesado: ${input}`
    };
  }
};
```

### Instalar Plugins Prebuilt

```bash
# Desde NPM
claude-code plugin install @claude/database-tools

# Desde directorio local
claude-code plugin install ./my-plugin

# Listar plugins instalados
claude-code plugin list

# Desinstalar
claude-code plugin uninstall my-plugin
```

### Plugins Populares

- `@claude/git-tools`: Operaciones avanzadas de Git
- `@claude/docker-tools`: Gestión de containers
- `@claude/database-tools`: Queries a bases de datos
- `@claude/cloud-tools`: AWS, Azure, GCP

Ver [guides/plugins.md](guides/plugins.md) para ejemplos completos.

---

## 💡 Agent Skills

Skills son workflows reutilizables que encapsulan conocimiento específico.

### Anatomía de un Skill

```markdown
# .claude/skills/review-pr.md

Eres un experto revisor de código. Al revisar un PR:

1. Lee el diff completo
2. Identifica:
   - Bugs potenciales
   - Problemas de rendimiento
   - Violaciones de mejores prácticas
3. Sugiere mejoras
4. Genera reporte en markdown
```

### Invocar Skills

```bash
# Desde CLI
claude-code /skill review-pr

# Desde conversación
"Usa el skill review-pr para revisar el último commit"
```

### Skills Avanzados con Parámetros

```markdown
# .claude/skills/deploy.md

Deploya la aplicación al ambiente {{environment}}.

Pasos:
1. Verificar tests pasen
2. Build de producción
3. Deploy a {{environment}}
4. Smoke tests
5. Notificar en Slack
```

Uso:
```bash
claude-code /skill deploy environment=production
```

### Crear Skills Reutilizables

**Estructura recomendada**:
```
.claude/skills/
├── backend/
│   ├── api-design.md
│   ├── database-migration.md
│   └── testing.md
├── frontend/
│   ├── component-creation.md
│   └── state-management.md
└── devops/
    ├── ci-cd-setup.md
    └── monitoring.md
```

Ver [guides/skills.md](guides/skills.md) para biblioteca de skills.

---

## 🎨 Output Styles

Controla cómo Claude Code presenta información.

### Estilos Disponibles

#### 1. Default (Markdown)
```bash
# Automático, usa CommonMark
```

#### 2. Code Block Focus
```bash
# Resalta bloques de código
```

#### 3. Compact Mode
```bash
# Respuestas más concisas
```

#### 4. Verbose Mode
```bash
# Explicaciones detalladas
```

### Configurar Output Style

**En conversación**:
```
"Por favor responde en modo compacto"
"Dame explicaciones detalladas"
```

**En configuración**:
```json
// .claude/config.json
{
  "outputStyle": "compact",
  "codeBlockHighlight": true,
  "emojiEnabled": false
}
```

### Custom Formatters

```javascript
// .claude/formatters/custom.js
module.exports = {
  format(content, type) {
    if (type === 'code') {
      return `\`\`\`\n${content}\n\`\`\``;
    }
    return content;
  }
};
```

Ver [guides/output-styles.md](guides/output-styles.md).

---

## 🪝 Hooks

Hooks ejecutan código en respuesta a eventos de Claude Code.

### Tipos de Hooks

1. **Pre-prompt**: Antes de enviar prompt
2. **Post-tool**: Después de ejecutar herramienta
3. **User-prompt-submit**: Al enviar mensaje usuario
4. **Session-start**: Al iniciar sesión
5. **Session-end**: Al terminar sesión

### Configurar Hooks

**`.claude/config.json`**:
```json
{
  "hooks": {
    "user-prompt-submit": "bash .claude/hooks/lint-check.sh",
    "post-tool": "node .claude/hooks/log-tool-use.js",
    "session-start": "python .claude/hooks/setup-env.py"
  }
}
```

### Ejemplo: Lint Check Hook

**`.claude/hooks/lint-check.sh`**:
```bash
#!/bin/bash

# Pre-commit lint check
if [[ $CLAUDE_USER_MESSAGE == *"commit"* ]]; then
    echo "🔍 Ejecutando linter..."
    npm run lint

    if [ $? -ne 0 ]; then
        echo "❌ Lint failed. Fix errors before committing."
        exit 1
    fi

    echo "✅ Lint passed"
fi
```

### Ejemplo: Tool Logging Hook

**`.claude/hooks/log-tool-use.js`**:
```javascript
const fs = require('fs');

const toolName = process.env.CLAUDE_TOOL_NAME;
const timestamp = new Date().toISOString();

const log = `${timestamp} - Tool used: ${toolName}\n`;

fs.appendFileSync('.claude/tool-usage.log', log);
```

### Variables de Entorno en Hooks

- `CLAUDE_USER_MESSAGE`: Mensaje del usuario
- `CLAUDE_TOOL_NAME`: Nombre de la herramienta ejecutada
- `CLAUDE_TOOL_ARGS`: Argumentos de la herramienta
- `CLAUDE_SESSION_ID`: ID de sesión actual

### Hooks Avanzados

**Validación de código antes de commits**:
```bash
# .claude/hooks/pre-commit.sh
#!/bin/bash

# Tests
npm test || exit 1

# Type check
tsc --noEmit || exit 1

# Security scan
npm audit || exit 1

echo "✅ All checks passed"
```

Ver [guides/hooks.md](guides/hooks.md) y [examples/hooks/](examples/hooks/).

---

## 💻 Programmatic Usage

Usa Claude Code desde tus propios scripts.

### Node.js SDK

```bash
npm install @anthropic-ai/claude-code-sdk
```

**Ejemplo básico**:
```javascript
const { ClaudeCode } = require('@anthropic-ai/claude-code-sdk');

const client = new ClaudeCode({
  apiKey: process.env.ANTHROPIC_API_KEY
});

async function main() {
  const session = await client.createSession({
    cwd: process.cwd()
  });

  const response = await session.sendMessage(
    'Analiza el archivo package.json y sugiere mejoras'
  );

  console.log(response.content);
}

main();
```

### Ejecutar Tareas Programáticamente

```javascript
const task = await session.executeTask({
  description: 'Refactor authentication module',
  files: ['src/auth/*.js'],
  constraints: {
    preserveTests: true,
    noBreakingChanges: true
  }
});

console.log(task.status); // 'completed'
console.log(task.changes); // Lista de archivos modificados
```

### Integración con CI/CD

**GitHub Actions**:
```yaml
name: Claude Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Node
        uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Review PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude-code exec \
            --task "Review this PR and provide feedback" \
            --output review.md

      - name: Post Review
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### API Completa

```javascript
// Crear sesión
const session = await client.createSession(options);

// Enviar mensaje
await session.sendMessage(prompt);

// Ejecutar herramienta
await session.executeTool(toolName, args);

// Leer archivo
const content = await session.readFile(path);

// Escribir archivo
await session.writeFile(path, content);

// Ejecutar comando
const result = await session.runCommand(command);

// Listar archivos
const files = await session.listFiles(pattern);

// Terminar sesión
await session.end();
```

Ver [guides/programmatic-usage.md](guides/programmatic-usage.md).

---

## 🔗 Model Context Protocol (MCP)

MCP permite a Claude Code comunicarse con servicios externos.

### ¿Qué es MCP?

**Model Context Protocol** es un protocolo estándar para que modelos de IA accedan a:
- Bases de datos
- APIs
- Sistemas de archivos remotos
- Servicios cloud
- Herramientas personalizadas

### Arquitectura MCP

```
┌─────────────────┐
│   Claude Code   │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│   MCP Server    │
│  (Tu servicio)  │
└────────┬────────┘
         │
         ▼
  ┌──────────────┐
  │   Database   │
  │   API        │
  │   Filesystem │
  └──────────────┘
```

### Crear MCP Server

**Estructura**:
```
my-mcp-server/
├── package.json
├── server.js
└── manifest.json
```

**manifest.json**:
```json
{
  "name": "my-database-mcp",
  "version": "1.0.0",
  "protocol": "mcp/1.0",
  "capabilities": {
    "tools": [
      {
        "name": "query_database",
        "description": "Execute SQL query",
        "parameters": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string",
              "description": "SQL query to execute"
            }
          },
          "required": ["query"]
        }
      }
    ]
  }
}
```

**server.js**:
```javascript
const { MCPServer } = require('@anthropic-ai/mcp-sdk');
const Database = require('better-sqlite3');

const db = new Database('mydb.sqlite');

const server = new MCPServer({
  name: 'my-database-mcp',
  version: '1.0.0'
});

server.addTool({
  name: 'query_database',
  async handler({ query }) {
    try {
      const rows = db.prepare(query).all();
      return {
        success: true,
        data: rows,
        rowCount: rows.length
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
});

server.listen(3000);
console.log('MCP Server listening on port 3000');
```

### Configurar MCP Server en Claude Code

**`.claude/config.json`**:
```json
{
  "mcpServers": [
    {
      "name": "database",
      "url": "http://localhost:3000",
      "enabled": true
    },
    {
      "name": "aws-tools",
      "url": "http://localhost:3001",
      "enabled": true,
      "auth": {
        "type": "bearer",
        "token": "${AWS_MCP_TOKEN}"
      }
    }
  ]
}
```

### Usar MCP Tools

Una vez configurado, Claude Code automáticamente detecta y usa las herramientas:

```
"Query la tabla users de la base de datos y muestra los resultados"

# Claude Code usa mcp__query_database automáticamente
```

### MCP Servers Prebuilt

```bash
# Instalar MCP server para GitHub
npm install -g @claude/mcp-github
claude-mcp start github

# Instalar MCP server para AWS
npm install -g @claude/mcp-aws
claude-mcp start aws

# Listar MCP servers activos
claude-mcp list
```

### Ejemplo: MCP Server para Slack

```javascript
const { MCPServer } = require('@anthropic-ai/mcp-sdk');
const { WebClient } = require('@slack/web-api');

const slack = new WebClient(process.env.SLACK_TOKEN);
const server = new MCPServer({ name: 'slack-mcp' });

server.addTool({
  name: 'send_slack_message',
  parameters: {
    channel: 'string',
    message: 'string'
  },
  async handler({ channel, message }) {
    const result = await slack.chat.postMessage({
      channel,
      text: message
    });
    return { success: true, ts: result.ts };
  }
});

server.addTool({
  name: 'search_slack_messages',
  parameters: {
    query: 'string',
    count: 'number'
  },
  async handler({ query, count = 10 }) {
    const result = await slack.search.messages({
      query,
      count
    });
    return {
      success: true,
      messages: result.messages.matches
    };
  }
});

server.listen(3002);
```

Ver [guides/mcp.md](guides/mcp.md) y [examples/mcp-servers/](examples/mcp-servers/).

---

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. Claude Code no responde

**Síntomas**: El comando cuelga sin respuesta

**Soluciones**:
```bash
# Verificar API key
echo $ANTHROPIC_API_KEY

# Revisar conectividad
curl https://api.anthropic.com/v1/messages

# Limpiar cache
claude-code cache clear

# Reiniciar sesión
claude-code logout && claude-code login
```

#### 2. Herramientas no disponibles

**Síntomas**: Error "Tool not found"

**Soluciones**:
```bash
# Verificar plugins instalados
claude-code plugin list

# Reinstalar plugin
claude-code plugin uninstall <plugin>
claude-code plugin install <plugin>

# Verificar permisos
ls -la .claude/plugins/
```

#### 3. Hooks no se ejecutan

**Síntomas**: Hooks configurados pero no ejecutan

**Soluciones**:
```bash
# Verificar permisos de ejecución
chmod +x .claude/hooks/*.sh

# Test hook manualmente
bash .claude/hooks/my-hook.sh

# Verificar configuración
cat .claude/config.json | jq '.hooks'

# Debug mode
CLAUDE_DEBUG=1 claude-code
```

#### 4. MCP Server no conecta

**Síntomas**: Error "MCP server unavailable"

**Soluciones**:
```bash
# Verificar servidor corriendo
curl http://localhost:3000/health

# Revisar logs del servidor
tail -f mcp-server.log

# Verificar puerto no está en uso
lsof -i :3000

# Verificar configuración
cat .claude/config.json | jq '.mcpServers'
```

#### 5. Performance lento

**Síntomas**: Respuestas tardan mucho

**Soluciones**:
```bash
# Reducir contexto
# En .claude/config.json
{
  "maxContextFiles": 10,
  "maxFileSize": "100KB"
}

# Usar modelos más rápidos
{
  "model": "claude-haiku-4"
}

# Limpiar historial
claude-code history clear

# Deshabilitar plugins no usados
claude-code plugin disable <plugin>
```

### Logs y Debugging

```bash
# Ver logs
tail -f ~/.claude/logs/claude-code.log

# Debug mode
CLAUDE_DEBUG=1 claude-code

# Verbose output
claude-code --verbose

# Exportar sesión para análisis
claude-code export session.json
```

### Errores Específicos

#### Error: "Rate limit exceeded"
```bash
# Esperar y reintentar
sleep 60

# Usar modelo diferente
claude-code --model claude-haiku-4
```

#### Error: "Context too large"
```bash
# Reducir archivos en contexto
# Usar .claudeignore
echo "node_modules/" >> .claudeignore
echo "dist/" >> .claudeignore
```

#### Error: "Permission denied"
```bash
# Verificar permisos
ls -la .claude/

# Corregir ownership
sudo chown -R $USER:$USER .claude/
```

### Recursos de Soporte

- **Documentación oficial**: https://docs.claude.com/claude-code
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Discord**: https://discord.gg/anthropic
- **Stack Overflow**: Tag `claude-code`

Ver [guides/troubleshooting.md](guides/troubleshooting.md) para más casos.

---

## 📖 Guías Adicionales

- [Subagents Avanzados](guides/subagents.md)
- [Desarrollo de Plugins](guides/plugins.md)
- [Biblioteca de Skills](guides/skills.md)
- [Output Customization](guides/output-styles.md)
- [Hooks Cookbook](guides/hooks.md)
- [Programmatic API](guides/programmatic-usage.md)
- [MCP Development](guides/mcp.md)
- [Troubleshooting Guide](guides/troubleshooting.md)

## 📦 Ejemplos

- [Plugins de ejemplo](examples/plugins/)
- [Skills reutilizables](examples/skills/)
- [Hooks útiles](examples/hooks/)
- [MCP Servers](examples/mcp-servers/)

## 🤝 Contribuir

Mejora esta guía:
1. Fork el repositorio
2. Crea branch para tu feature
3. Commit tus cambios
4. Push a tu branch
5. Abre Pull Request

---

**Autor**: Claude Code Community
**Última actualización**: Diciembre 2024
**Versión**: 2.0
