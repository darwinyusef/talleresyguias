# Claude Code - Quickstart

## Instalación en 3 Pasos

### 1. Instalar Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```

### 2. Login
```bash
claude-code login
```

### 3. Primer Comando
```bash
cd tu-proyecto
claude-code
```

## Comandos Básicos

### Conversación Interactiva
```bash
claude-code
> "Analiza este proyecto y dame un resumen"
```

### Tarea Específica
```bash
claude-code exec "Crea un componente React para login"
```

### Usar un Skill
```bash
claude-code /skill code-review
```

## Configuración Inicial

### Crear Configuración
```bash
mkdir .claude
cat > .claude/config.json << 'INNER_EOF'
{
  "model": "claude-sonnet-4",
  "maxContextFiles": 20,
  "outputStyle": "markdown"
}
INNER_EOF
```

### Ignorar Archivos
```bash
cat > .claudeignore << 'INNER_EOF'
node_modules/
dist/
.git/
*.log
INNER_EOF
```

## Instalar Primer Plugin

```bash
# Plugin de database
claude-code plugin install @claude/database-tools

# Usar plugin
claude-code
> "Lista las tablas de la base de datos"
```

## Crear Primer Hook

```bash
mkdir -p .claude/hooks

cat > .claude/hooks/pre-commit.sh << 'INNER_EOF'
#!/bin/bash
npm test
INNER_EOF

chmod +x .claude/hooks/pre-commit.sh
```

Configurar:
```json
{
  "hooks": {
    "user-prompt-submit": "bash .claude/hooks/pre-commit.sh"
  }
}
```

## Ejemplos Útiles

### Refactoring
```bash
claude-code exec "Refactoriza src/utils.js para usar async/await"
```

### Documentación
```bash
claude-code exec "Genera README.md basado en el código"
```

### Testing
```bash
claude-code exec "Crea tests para src/auth/login.js"
```

### Code Review
```bash
claude-code /skill code-review
```

## Atajos Útiles

- `/help` - Ver ayuda
- `/clear` - Limpiar conversación
- `/exit` - Salir
- `/files` - Ver archivos en contexto
- `/skill <name>` - Ejecutar skill

## Próximos Pasos

1. Lee [README.md](README.md) para guía completa
2. Explora [guides/](guides/) para temas específicos
3. Ve [examples/](examples/) para código de ejemplo
4. Únete al [Discord](https://discord.gg/anthropic)

## Troubleshooting Rápido

### No responde
```bash
claude-code cache clear
claude-code logout && claude-code login
```

### Error de permisos
```bash
sudo chown -R $USER:$USER .claude/
```

### Muy lento
```json
{
  "model": "claude-haiku-4",
  "maxContextFiles": 10
}
```

¡Listo para empezar! 🚀
