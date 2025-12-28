# 🎨 MCP Diagram Generator Setup

Configuración del servidor MCP para generar diagramas con PlantUML, Mermaid y otros formatos.

## 📋 Configuración Instalada

### Archivo: `.mcp.json`

```json
{
  "mcpServers": {
    "diagram-generator": {
      "command": "npx",
      "args": ["-y", "@domdomegg/diagrammcp"]
    }
  }
}
```

## 🚀 Cómo Usar

### 1. Configurar en Claude Desktop

El archivo `.mcp.json` debe copiarse a la configuración de Claude Desktop:

**macOS:**
```bash
cp .mcp.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

O editar manualmente:
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
Copy-Item .mcp.json "$env:APPDATA\Claude\claude_desktop_config.json"
```

**Linux:**
```bash
cp .mcp.json ~/.config/Claude/claude_desktop_config.json
```

### 2. Reiniciar Claude Desktop

Después de actualizar la configuración, reinicia Claude Desktop para que cargue el servidor MCP.

## 🎯 Formatos Soportados

El servidor `@domdomegg/diagrammcp` soporta:

- **Mermaid** - Diagramas de flujo, secuencia, clases, etc.
- **PlantUML** - UML completo (clases, secuencia, componentes, etc.)
- **GraphViz/DOT** - Grafos dirigidos
- **Otros** según capacidades del servidor

## 📚 Ejemplos de Uso

### Ejemplo 1: Mermaid - Diagrama de Flujo

```
Crea un diagrama de flujo en Mermaid que muestre el proceso de login:
1. Usuario ingresa credenciales
2. Sistema valida
3. Si válido → Dashboard
4. Si inválido → Error
```

### Ejemplo 2: PlantUML - Diagrama de Clases

```
Genera un diagrama de clases PlantUML para:
- Clase User (id, email, password)
- Clase Order (id, total, status)
- Relación: User tiene muchos Orders
```

### Ejemplo 3: Arquitectura Hexagonal

```
Crea un diagrama en Mermaid mostrando arquitectura hexagonal:
- Core Domain en el centro
- Ports (interfaces)
- Adapters (REST, DB, Kafka)
```

## 🔧 Otros Servidores MCP Recomendados

Si necesitas más funcionalidad, puedes agregar estos servidores:

### UML-MCP (Más completo)

```json
{
  "mcpServers": {
    "diagram-generator": {
      "command": "npx",
      "args": ["-y", "@domdomegg/diagrammcp"]
    },
    "uml-mcp": {
      "command": "npx",
      "args": ["-y", "uml-mcp"]
    }
  }
}
```

### mcp-mermaid (Especializado en Mermaid)

```json
{
  "mcpServers": {
    "diagram-generator": {
      "command": "npx",
      "args": ["-y", "@domdomegg/diagrammcp"]
    },
    "mermaid": {
      "command": "npx",
      "args": ["-y", "mcp-mermaid"]
    }
  }
}
```

### Kroki (Múltiples formatos)

```json
{
  "mcpServers": {
    "diagram-generator": {
      "command": "npx",
      "args": ["-y", "@domdomegg/diagrammcp"]
    },
    "kroki": {
      "command": "npx",
      "args": ["-y", "@tkoba1974/mcp-kroki"]
    }
  }
}
```

## 🎨 Integración con Proyecto Actual

### Generar Diagramas para Arquitecturas

Ahora puedes pedir:

```
Genera un diagrama Mermaid para el patrón CQRS que creamos
```

```
Convierte el diagrama de Hexagonal Architecture a PlantUML
```

```
Crea un diagrama de secuencia para el Saga Pattern
```

### Exportar Formatos

Los diagramas se pueden exportar a:
- ✅ **SVG** - Vectorial, escalable
- ✅ **PNG** - Imagen rasterizada
- ✅ **PDF** - Documentación
- ✅ **Código fuente** (Mermaid/PlantUML)

## 🐛 Troubleshooting

### Error: "MCP server not found"

1. Verifica que Node.js está instalado:
   ```bash
   node --version
   npm --version
   ```

2. Prueba instalar el paquete manualmente:
   ```bash
   npm install -g @domdomegg/diagrammcp
   ```

### Error: "Permission denied"

En macOS/Linux:
```bash
chmod +x ~/.config/Claude/claude_desktop_config.json
```

### El servidor no aparece en Claude

1. Verifica el formato JSON (sin errores de sintaxis)
2. Reinicia completamente Claude Desktop
3. Revisa los logs de Claude:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

## 📊 Casos de Uso para Este Proyecto

### 1. Convertir Canvas a Mermaid/PlantUML

Los 10 diagramas Canvas que creamos pueden convertirse a formatos exportables:

```
Convierte el diagrama 01-hexagonal-architecture.canvas a Mermaid
```

### 2. Generar Diagramas de los 10 Restantes

Para las Semanas 3 y 4, generar directamente en Mermaid/PlantUML:

```
Crea diagrama Circuit Breaker en Mermaid con estados: Closed, Open, Half-Open
```

### 3. Diagramas C4 Model

Generar los 74 diagramas C4 planeados:

```
Genera diagrama C4 Context para el sistema de e-commerce
```

### 4. Diagramas UML

Generar los 56 diagramas UML planeados:

```
Crea diagrama de clases UML para Domain-Driven Design con Aggregates
```

## 🎯 Próximos Pasos

1. ✅ Configurar MCP server (HECHO)
2. → Reiniciar Claude Desktop
3. → Probar generación de diagrama Mermaid
4. → Exportar a SVG/PNG
5. → Integrar en workflow de diagramación
6. → Generar diagramas Semana 3 y 4

## 📚 Recursos

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Mermaid Documentation](https://mermaid.js.org/)
- [PlantUML Documentation](https://plantuml.com/)
- [@domdomegg/diagrammcp GitHub](https://github.com/domdomegg/diagrammcp)

---

**Nota:** Este servidor MCP te permitirá generar diagramas profesionales directamente desde Claude sin salir del editor.
