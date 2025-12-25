# Guía Avanzada de Subagents

## ¿Qué son los Subagents?

Los subagents son agentes especializados que Claude Code lanza para tareas específicas que requieren autonomía y múltiples pasos.

## Tipos de Subagents

### 1. General Purpose Agent

**Uso**: Tareas complejas multi-paso

**Ejemplo**:
```
"Busca todos los archivos que usan axios, analiza cómo se manejan errors, y crea un resumen de mejores prácticas"
```

Este agent:
- Buscará archivos con Glob/Grep
- Leerá contenido relevante
- Analizará patrones
- Generará reporte

**Cuándo usar**:
- Necesitas múltiples operaciones de búsqueda
- Análisis que requiere leer varios archivos
- Generación de reportes complejos

### 2. Explore Agent

**Uso**: Exploración y entendimiento de código

**Niveles de thoroughness**:

#### Quick (rápido)
```python
"quick: Encuentra dónde se define UserModel"
```
- Búsqueda básica
- Pocos archivos
- Respuesta rápida

#### Medium (moderado)
```python
"medium: ¿Cómo funciona el sistema de autenticación?"
```
- Múltiples búsquedas
- Lee archivos relacionados
- Balance velocidad/profundidad

#### Very Thorough (exhaustivo)
```python
"very thorough: Explica la arquitectura completa del backend"
```
- Exploración exhaustiva
- Lee muchos archivos
- Análisis profundo
- Más lento pero completo

**Ejemplos prácticos**:

```python
# Entender un feature
"Explora cómo se implementa la paginación en las APIs"

# Análisis arquitectónico
"Analiza la estructura de carpetas y explica la arquitectura del proyecto"

# Dependency tracking
"Encuentra todas las dependencias de la función processPayment"

# Code patterns
"Busca patrones de manejo de errores en todo el proyecto"
```

### 3. Plan Agent

**Uso**: Planificación de tareas complejas

**Ejemplo**:
```
"Planifica la migración de Express a Fastify"
```

El agent generará:
1. Análisis de dependencias
2. Pasos de migración
3. Riesgos y consideraciones
4. Plan de testing

## Mejores Prácticas

### ✅ DO: Usar Subagents

```python
# Exploración amplia
"Explora el codebase para encontrar todos los lugares donde se accede a la base de datos"

# Análisis complejo
"Analiza el flujo de autenticación desde login hasta refresh token"

# Multi-archivo
"Busca inconsistencias en el manejo de fechas entre frontend y backend"
```

### ❌ DON'T: Usar Subagents

```python
# Archivo específico conocido
# MAL: "Explora para encontrar src/auth/login.js"
# BIEN: Read src/auth/login.js directamente

# Búsqueda simple
# MAL: "Explora para encontrar la clase UserModel"
# BIEN: Glob **/*User*.js

# Pocos archivos
# MAL: "Explora estos 2 archivos"
# BIEN: Read ambos archivos
```

## Configuración de Subagents

```json
// .claude/config.json
{
  "subagents": {
    "explore": {
      "defaultThoroughness": "medium",
      "maxFiles": 50,
      "timeout": 300000
    },
    "generalPurpose": {
      "maxSteps": 20,
      "timeout": 600000
    }
  }
}
```

## Ejemplos Avanzados

### Refactoring Planning

```
"Usa el Plan agent para crear un plan detallado de refactorización del módulo de pagos para usar async/await en lugar de callbacks"
```

### Code Quality Analysis

```
"Explora exhaustivamente el proyecto y genera un reporte de:
1. Código duplicado
2. Funciones muy largas (>50 líneas)
3. Archivos con muchas dependencias
4. Oportunidades de refactoring"
```

### Migration Planning

```
"Planifica la migración de:
- Redux a Zustand
- Class components a Function components
- PropTypes a TypeScript

Incluye:
- Orden de migración
- Archivos afectados
- Cambios breaking
- Plan de testing"
```

## Debugging Subagents

```bash
# Ver qué hace el subagent
CLAUDE_DEBUG=1 claude-code

# Logs detallados
tail -f ~/.claude/logs/subagents.log

# Limitar timeout
claude-code --subagent-timeout 180000
```

## Performance Tips

1. **Especifica alcance**: "Explora solo el directorio src/api"
2. **Usa thoroughness apropiado**: No uses "very thorough" si "medium" es suficiente
3. **Filtra archivos irrelevantes**: Usa .claudeignore
4. **Divide tareas grandes**: En lugar de una exploración masiva, divide en partes

## Ejemplos por Caso de Uso

### Onboarding a Codebase Nuevo

```
"Explora el proyecto y genera una guía de onboarding que incluya:
1. Estructura del proyecto
2. Tecnologías usadas
3. Puntos de entrada principales
4. Convenciones de código
5. Setup de desarrollo"
```

### Security Audit

```
"Explora exhaustivamente el código buscando:
1. SQL injection risks
2. XSS vulnerabilities
3. Hardcoded secrets
4. Insecure dependencies
5. Authentication weaknesses"
```

### Documentation Generation

```
"Analiza el módulo de API y genera documentación que incluya:
1. Endpoints disponibles
2. Parámetros requeridos
3. Responses esperados
4. Error handling
5. Ejemplos de uso"
```

### Dependency Analysis

```
"Explora y crea un mapa de dependencias que muestre:
1. Qué módulos dependen de qué
2. Dependencias circulares
3. Módulos con muchas dependencias
4. Código no usado"
```
