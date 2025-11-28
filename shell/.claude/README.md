# Configuración de Claude Code

Esta carpeta contiene configuraciones y comandos personalizados para Claude Code.

## 📁 Estructura

```
.claude/
├── config.json          # Configuración general del proyecto
├── commands/            # Comandos personalizados (slash commands)
│   ├── test.md         # /test - Ejecutar tests
│   ├── deploy.md       # /deploy - Desplegar aplicación
│   ├── review.md       # /review - Revisar código
│   ├── docs.md         # /docs - Generar documentación
│   ├── refactor.md     # /refactor - Refactorizar código
│   └── scaffold.md     # /scaffold - Crear componentes
└── hooks/              # Hooks para eventos (opcional)
```

## 🎯 Comandos Disponibles

### `/test`
Ejecuta todos los tests del proyecto y reporta resultados.
```
/test
```

### `/deploy [env]`
Despliega la aplicación al entorno especificado.
```
/deploy production
/deploy staging
```

### `/review`
Revisa el código reciente y sugiere mejoras.
```
/review
```

### `/docs [type]`
Genera o actualiza documentación del proyecto.
```
/docs
/docs api
/docs readme
```

### `/refactor [target]`
Refactoriza código para mejorar calidad.
```
/refactor
/refactor src/utils.js
```

### `/scaffold <type> <name>`
Crea estructura inicial para nuevos componentes.
```
/scaffold component UserProfile
/scaffold api posts
/scaffold model User
```

## ⚙️ Configuración

El archivo `config.json` contiene la configuración del proyecto:

- **project**: Información básica del proyecto
- **preferences**: Preferencias de código y estilo
- **commands**: Lista de comandos disponibles

## 🔧 Crear Comandos Personalizados

Para crear un nuevo comando:

1. Crea un archivo `.md` en `commands/`
2. Define el comando con formato:

```markdown
# Comando: /nombre

Descripción breve del comando.

## Argumentos:
- `arg1`: Descripción
- `arg2` (opcional): Descripción

## Pasos:

1. Paso 1
2. Paso 2
3. Paso 3
```

3. El comando estará disponible como `/nombre`

## 📚 Ejemplos de Uso

### Flujo de desarrollo típico

```bash
# 1. Revisar código antes de commit
/review

# 2. Ejecutar tests
/test

# 3. Generar documentación
/docs

# 4. Desplegar a staging
/deploy staging
```

### Crear nueva funcionalidad

```bash
# 1. Crear estructura del componente
/scaffold component NewFeature

# 2. Revisar y refactorizar
/review
/refactor

# 3. Documentar
/docs

# 4. Probar
/test
```

## 💡 Tips

- Los comandos son contextuales y analizan tu proyecto
- Puedes combinar comandos para workflows complejos
- Los comandos respetan la estructura de tu proyecto
- Claude Code aprende de tus patrones y convenciones

## 🔗 Recursos

- [Documentación de Claude Code](https://docs.claude.com/claude-code)
- [Guía de Comandos](https://docs.claude.com/claude-code/slash-commands)
- [Ejemplos de Configuración](https://github.com/anthropics/claude-code-examples)
