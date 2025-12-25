# Claude Code - Índice Completo de Recursos

## 📚 Documentación Principal

### Guías Rápidas
- [README.md](README.md) - Guía completa con todos los temas
- [QUICKSTART.md](QUICKSTART.md) - Instalación y primeros pasos en 5 minutos

### Guías Detalladas (guides/)
- [subagents.md](guides/subagents.md) - Uso avanzado de subagents

## 🔧 Ejemplos Prácticos

### Plugins (examples/plugins/)
#### Database Query Tool
Plugin completo para ejecutar queries SQL desde Claude Code
- [index.js](examples/plugins/database-query-tool/index.js) - Implementación
- [package.json](examples/plugins/database-query-tool/package.json) - Configuración

**Instalación**:
```bash
cd .claude_app/examples/plugins/database-query-tool
npm install
npm link
claude-code plugin install .
```

**Uso**:
```
"Query la tabla users y muestra los resultados"
"Lista todas las tablas de la base de datos"
"Describe el schema de la tabla products"
```

**Features**:
- ✅ Read-only por defecto (seguro)
- ✅ Validación de queries peligrosas
- ✅ Soporte para prepared statements
- ✅ Schema introspection
- ✅ Error handling robusto

### MCP Servers (examples/mcp-servers/)
#### GitHub MCP Server
Servidor MCP para integración completa con GitHub

- [server.js](examples/mcp-servers/github-mcp/server.js) - Servidor MCP
- [package.json](examples/mcp-servers/github-mcp/package.json) - Dependencias

**Setup**:
```bash
cd .claude_app/examples/mcp-servers/github-mcp
npm install
export GITHUB_TOKEN=your_token_here
npm start
```

**Configurar en Claude Code**:
```json
{
  "mcpServers": [
    {
      "name": "github",
      "url": "http://localhost:3000",
      "enabled": true
    }
  ]
}
```

**Tools Disponibles**:
1. `list_repos` - Listar repositorios de un usuario
2. `get_repo_info` - Info detallada de un repo
3. `list_pull_requests` - Listar PRs
4. `create_issue` - Crear issues
5. `search_code` - Buscar código en GitHub

**Ejemplos de Uso**:
```
"Lista mis repositorios públicos"
"Dame info del repo anthropics/claude-code"
"Busca código que usa MLflow en repositorios Python"
"Crea un issue en mi repo para agregar tests"
```

### Hooks (examples/hooks/)
#### Pre-Commit Check Hook
Hook completo para validación pre-commit

- [pre-commit-check.sh](examples/hooks/pre-commit-check.sh) - Script ejecutable

**Instalación**:
```bash
cp .claude_app/examples/hooks/pre-commit-check.sh .claude/hooks/
chmod +x .claude/hooks/pre-commit-check.sh
```

**Configurar en .claude/config.json**:
```json
{
  "hooks": {
    "user-prompt-submit": "bash .claude/hooks/pre-commit-check.sh"
  }
}
```

**Validaciones que ejecuta**:
1. ✅ Linter (ESLint)
2. ✅ Type checking (TypeScript)
3. ✅ Tests unitarios
4. ✅ Detección de console.log
5. ✅ Búsqueda de TODOs
6. ✅ Security audit (npm audit)

**Comportamiento**:
- Solo se ejecuta cuando detecta palabras clave: "commit", "push"
- Bloquea commit si hay errores críticos
- Muestra warnings para issues menores
- Output con colores para fácil lectura

### Skills (examples/skills/)
#### Code Review Skill
Skill profesional para revisión de código

- [code-review-skill.md](examples/skills/code-review-skill.md) - Skill completo

**Instalación**:
```bash
cp .claude_app/examples/skills/code-review-skill.md .claude/skills/
```

**Uso**:
```bash
claude-code /skill code-review

claude-code /skill code-review files="src/auth/*.js"

claude-code /skill code-review focus=security
```

**Aspectos que revisa**:
1. 🔍 **Funcionalidad**: Bugs, edge cases
2. 📏 **Calidad**: SOLID, DRY, legibilidad
3. ⚡ **Performance**: Ineficiencias, N+1 queries
4. 🔒 **Seguridad**: SQL injection, XSS, secrets
5. 🧪 **Testing**: Coverage, casos edge

**Output Format**:
- Resumen ejecutivo
- Aspectos positivos
- Problemas por severidad (Crítico/Importante/Menor)
- Sugerencias de código mejorado
- Recomendación final (Aprobar/Cambios/Comentarios)

## 📖 Temas Cubiertos

### ✅ Completos
- **Subagents**: Guía completa con ejemplos
- **Plugins**: Plugin funcional de database queries
- **MCP**: Servidor GitHub MCP completo
- **Hooks**: Pre-commit hook con múltiples validaciones
- **Skills**: Code review skill profesional
- **Quickstart**: Instalación y primeros pasos

### 🚧 Por Desarrollar
(Estos temas están cubiertos en el README principal pero pendientes de guías detalladas)
- Output Styles (guía detallada)
- Programmatic Usage (ejemplos SDK)
- Troubleshooting (casos adicionales)

## 🎯 Flujo de Uso Recomendado

### Día 1: Instalación y Básicos
1. Instalar Claude Code siguiendo [QUICKSTART.md](QUICKSTART.md)
2. Crear configuración básica
3. Probar comandos interactivos
4. Explorar un proyecto existente

### Día 2: Plugins y Tools
1. Instalar Database Query Plugin
2. Configurar GitHub MCP Server
3. Ejecutar queries y operaciones GitHub
4. Crear tu primer plugin personalizado

### Día 3: Automation
1. Configurar pre-commit hook
2. Crear skills personalizados
3. Automatizar code reviews
4. Integrar con CI/CD

### Día 4: Advanced
1. Desarrollar MCP server personalizado
2. Crear pipeline completo con hooks
3. Usar subagents para análisis complejo
4. Programmatic usage con SDK

## 🔗 Enlaces Rápidos

### Documentación
- [README principal](.claude_app/README.md)
- [Quickstart](.claude_app/QUICKSTART.md)
- [Subagents](.claude_app/guides/subagents.md)

### Código Listo para Usar
- [Database Plugin](.claude_app/examples/plugins/database-query-tool/)
- [GitHub MCP](.claude_app/examples/mcp-servers/github-mcp/)
- [Pre-commit Hook](.claude_app/examples/hooks/pre-commit-check.sh)
- [Code Review Skill](.claude_app/examples/skills/code-review-skill.md)

### Recursos Externos
- [Documentación Oficial Claude Code](https://docs.claude.com/claude-code)
- [GitHub Repository](https://github.com/anthropics/claude-code)
- [Discord Community](https://discord.gg/anthropic)

## 💡 Tips Útiles

### Performance
```json
{
  "model": "claude-haiku-4",
  "maxContextFiles": 10
}
```

### Seguridad
```bash
echo "*.env" >> .claudeignore
echo "credentials.json" >> .claudeignore
```

### Debugging
```bash
CLAUDE_DEBUG=1 claude-code
tail -f ~/.claude/logs/claude-code.log
```

## 🤝 Contribuir

Mejora estos recursos:
1. Reporta bugs en ejemplos
2. Sugiere nuevos plugins/skills
3. Comparte tus hooks útiles
4. Documenta casos de uso

## 📝 Notas

- Todos los ejemplos están probados y listos para usar
- Código sigue mejores prácticas de la comunidad
- Documentación incluye teoría y práctica
- Ejemplos cubren casos reales de uso

---

**Última actualización**: Diciembre 2024
**Versión de Claude Code**: 1.0+
**Mantenedor**: Claude Code Community
