┌─────────────────────────────────────────────────────────────┐
│  IMPORTANTE: Diferencia de Directorios                     │
└─────────────────────────────────────────────────────────────┘

Este proyecto: claude-code-guide/
├── ✅ Directorio PÚBLICO (sin punto al inicio)
├── ✅ Visible en exploradores de archivos
├── ✅ Documentación y guías para aprender
├── ✅ Ejemplos de código reutilizables
└── ✅ Se versiona en Git y se comparte

Tu configuración: .claude/
├── ⚙️ Directorio OCULTO (empieza con punto)
├── ⚙️ Específico de cada proyecto
├── ⚙️ config.json, hooks/, skills/
├── ⚙️ Configuración personalizada
└── ⚙️ Opcional en Git (.gitignore)

┌─────────────────────────────────────────────────────────────┐
│  Ejemplo de Uso                                             │
└─────────────────────────────────────────────────────────────┘

1. Estudiar esta guía:
   cd claude-code-guide
   cat README.md

2. Crear configuración en tu proyecto:
   cd mi-proyecto
   mkdir .claude

3. Copiar ejemplos de esta guía:
   cp ../claude-code-guide/examples/hooks/pre-commit-check.sh .claude/hooks/
   cp ../claude-code-guide/examples/skills/code-review-skill.md .claude/skills/

4. Configurar:
   cat > .claude/config.json << 'INNER_EOF'
   {
     "hooks": {
       "user-prompt-submit": "bash .claude/hooks/pre-commit-check.sh"
     }
   }
   INNER_EOF

5. ¡Usar!
   claude-code

Ver ESTRUCTURA.md para más detalles.
