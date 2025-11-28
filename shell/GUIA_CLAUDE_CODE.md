# 🤖 Guía de Configuración de Claude Code

Esta guía te enseña cómo configurar y personalizar Claude Code para tu proyecto.

## 📋 Tabla de Contenidos

1. [Configuración Básica](#configuración-básica)
2. [Comandos Personalizados](#comandos-personalizados)
3. [Hooks](#hooks)
4. [Mejores Prácticas](#mejores-prácticas)
5. [Ejemplos Avanzados](#ejemplos-avanzados)

---

## 🚀 Configuración Básica

### Estructura de la carpeta `.claude`

```
.claude/
├── config.json          # Configuración del proyecto
├── commands/            # Comandos personalizados (/comando)
│   └── *.md            # Cada archivo es un comando
├── hooks/              # Scripts que se ejecutan en eventos
└── README.md           # Documentación
```

### Archivo config.json

```json
{
  "project": {
    "name": "nombre-proyecto",
    "description": "Descripción del proyecto",
    "version": "1.0.0"
  },
  "preferences": {
    "codeStyle": "clean",
    "testing": true,
    "documentation": "detailed"
  }
}
```

---

## 🎯 Comandos Personalizados

### Crear un Comando Nuevo

**Archivo**: `.claude/commands/micomando.md`

```markdown
# Comando: /micomando

Descripción de lo que hace el comando.

## Argumentos:
- `arg1`: Descripción del argumento
- `arg2` (opcional): Argumento opcional

## Pasos:

1. Primer paso que ejecutará Claude
2. Segundo paso
3. Tercer paso

## Ejemplo:
/micomando valor1 valor2
```

### Comandos ya Creados en este Proyecto

#### `/test` - Ejecutar Tests
```bash
/test
```
Busca y ejecuta todos los tests del proyecto.

#### `/deploy [env]` - Desplegar
```bash
/deploy production
/deploy staging
```
Despliega al entorno especificado.

#### `/review` - Revisar Código
```bash
/review
```
Analiza el código reciente y sugiere mejoras.

#### `/docs [type]` - Documentación
```bash
/docs          # Toda la documentación
/docs api      # Solo API
/docs readme   # Solo README
```

#### `/refactor [target]` - Refactorizar
```bash
/refactor
/refactor src/utils.js
```
Mejora la calidad del código.

#### `/scaffold <type> <name>` - Generar Código
```bash
/scaffold component Button
/scaffold api users
/scaffold model Product
```

---

## 🪝 Hooks (Eventos Automáticos)

Los hooks son scripts que se ejecutan automáticamente en ciertos eventos.

### Tipos de Hooks Disponibles

**Pre-edit Hook**: Antes de editar un archivo
```bash
# .claude/hooks/pre-edit.sh
#!/bin/bash
echo "Verificando antes de editar..."
# Tu lógica aquí
```

**Post-edit Hook**: Después de editar un archivo
```bash
# .claude/hooks/post-edit.sh
#!/bin/bash
echo "Formateando código..."
npx prettier --write "$EDITED_FILE"
```

**Pre-commit Hook**: Antes de hacer commit
```bash
# .claude/hooks/pre-commit.sh
#!/bin/bash
echo "Ejecutando tests antes de commit..."
npm test
```

### Variables Disponibles en Hooks

- `$EDITED_FILE`: Archivo que fue editado
- `$PROJECT_ROOT`: Raíz del proyecto
- `$COMMAND`: Comando que se está ejecutando

---

## 💡 Mejores Prácticas

### 1. Organización de Comandos

```
commands/
├── dev/
│   ├── test.md
│   ├── lint.md
│   └── format.md
├── deploy/
│   ├── staging.md
│   └── production.md
└── utils/
    ├── docs.md
    └── scaffold.md
```

### 2. Comandos Reutilizables

Crea comandos modulares que puedan combinarse:

```bash
# Flujo completo
/lint
/test
/docs
/deploy staging
```

### 3. Documentación Clara

Cada comando debe tener:
- ✅ Descripción clara
- ✅ Lista de argumentos
- ✅ Ejemplos de uso
- ✅ Pasos específicos

### 4. Manejo de Errores

```markdown
## Pasos:

1. Verificar pre-requisitos
2. Si hay errores, mostrar mensaje claro y detener
3. Ejecutar acción principal
4. Validar resultado
5. Reportar éxito o fallo
```

---

## 🔥 Ejemplos Avanzados

### Comando con Validación

```markdown
# Comando: /release

Crea una nueva versión del proyecto.

## Argumentos:
- `version`: Número de versión (major, minor, patch)

## Pasos:

1. Verificar que estamos en la rama main
2. Verificar que no hay cambios sin commit
3. Ejecutar todos los tests
4. Actualizar version en package.json
5. Crear tag de git
6. Push a repositorio
7. Publicar a npm (si aplica)
8. Generar changelog
```

### Comando de Análisis

```markdown
# Comando: /analyze

Analiza la salud del proyecto.

## Pasos:

1. Analizar cobertura de tests
2. Revisar dependencias desactualizadas
3. Buscar vulnerabilidades de seguridad
4. Calcular complejidad del código
5. Generar reporte con métricas
6. Sugerir mejoras prioritarias
```

### Comando de Setup

```markdown
# Comando: /setup

Configura el entorno de desarrollo.

## Pasos:

1. Verificar que Node.js está instalado
2. Instalar dependencias (npm install)
3. Crear archivo .env desde .env.example
4. Configurar base de datos
5. Ejecutar migraciones
6. Poblar datos de prueba
7. Ejecutar tests para verificar
8. Mostrar instrucciones de próximos pasos
```

---

## 🎨 Personalización Avanzada

### Config con Preferencias Detalladas

```json
{
  "project": {
    "name": "mi-proyecto",
    "type": "web-app",
    "framework": "react",
    "language": "typescript"
  },
  "preferences": {
    "codeStyle": {
      "indent": 2,
      "quotes": "single",
      "semicolons": true,
      "trailingComma": "es5"
    },
    "testing": {
      "framework": "jest",
      "coverage": 80,
      "runOnSave": false
    },
    "linting": {
      "enabled": true,
      "autofix": true
    },
    "git": {
      "autoCommit": false,
      "commitMessageFormat": "conventional"
    }
  },
  "paths": {
    "src": "src",
    "tests": "tests",
    "docs": "docs",
    "build": "dist"
  }
}
```

---

## 🛠️ Comandos Útiles para este Proyecto

### Ejecutar Scripts de Bash
```bash
/scaffold bash "nuevo_script"
# Crea un nuevo script de bash educativo
```

### Probar Makefile
```bash
/test makefile
# Prueba todos los targets del Makefile
```

### Desplegar Nginx
```bash
/deploy nginx
# Ejecuta: make -f Makefile.nginx deploy
```

### Iniciar Docker
```bash
/setup docker
# Configura el entorno Docker completo
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [Claude Code Docs](https://docs.claude.com/claude-code)
- [Slash Commands Guide](https://docs.claude.com/claude-code/slash-commands)
- [Configuration Reference](https://docs.claude.com/claude-code/configuration)

### Ejemplos
- Ver los comandos en `.claude/commands/`
- Leer `.claude/README.md` para más detalles

### Comunidad
- [GitHub Discussions](https://github.com/anthropics/claude-code)
- [Discord Community](https://discord.gg/anthropic)

---

## ✅ Checklist de Configuración

- [ ] Crear carpeta `.claude/`
- [ ] Añadir `config.json` con info del proyecto
- [ ] Crear comandos básicos (test, deploy, docs)
- [ ] Configurar hooks si es necesario
- [ ] Documentar comandos personalizados
- [ ] Probar cada comando
- [ ] Crear flujos de trabajo comunes
- [ ] Compartir con el equipo

---

## 🎉 ¡Listo!

Ahora tienes Claude Code completamente configurado para tu proyecto.

**Prueba los comandos**:
```bash
/test
/review
/docs
```

**¿Necesitas ayuda?**
Pregúntame cualquier cosa sobre configuración o creación de comandos personalizados.
