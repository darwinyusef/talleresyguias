# Taller Intermedio: FastMCP + Claude Desktop + n8n - Automatización Inteligente

## 📋 Índice

1. [Introducción al Nivel Intermedio](#introducción-al-nivel-intermedio)
2. [Configuración Avanzada de Claude Desktop con MCP](#configuración-avanzada-de-claude-desktop-con-mcp)
3. [Integración Completa: FastMCP + Claude + n8n](#integración-completa-fastmcp--claude--n8n)
4. [Patrones Avanzados de MCP](#patrones-avanzados-de-mcp)
5. [Proyecto Real: Sistema de Análisis de Contenido con IA](#proyecto-real-sistema-de-análisis-de-contenido-con-ia)
6. [Debugging y Optimización](#debugging-y-optimización)
7. [Casos de Uso Empresariales](#casos-de-uso-empresariales)

---

## 1. Introducción al Nivel Intermedio

### Objetivos del Taller

Este taller asume que ya tienes conocimientos básicos de FastMCP y te llevará al siguiente nivel:

- **Nivel Básico** → **Nivel Intermedio** → Nivel Avanzado

**Lo que aprenderás:**
- Configuración avanzada de Claude Desktop con múltiples servidores MCP
- Integración bidireccional entre Claude, MCP y n8n
- Patrones de diseño para sistemas de IA distribuidos
- Debugging y monitoreo de servidores MCP
- Casos de uso empresariales reales

### Arquitectura del Sistema Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   n8n UI     │  │Claude Desktop│  │   Web Client     │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
└─────────┼──────────────────┼───────────────────┼────────────┘
          │                  │                   │
┌─────────▼──────────────────▼───────────────────▼────────────┐
│                  CAPA DE ORQUESTACIÓN                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         n8n Workflow Engine + HTTP Endpoints         │   │
│  └────────────────────┬─────────────────────────────────┘   │
└───────────────────────┼──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│                 CAPA MCP (Protocolo)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ FastMCP HTTP │  │ Claude MCP   │  │ MCP Client Pool  │  │
│  │   Wrapper    │  │  Protocol    │  │                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
└─────────┼──────────────────┼───────────────────┼────────────┘
          │                  │                   │
┌─────────▼──────────────────▼───────────────────▼────────────┐
│             CAPA DE SERVIDORES MCP (FastMCP)                 │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────────┐  │
│  │  Database   │ │  AI/Claude   │ │   File System       │  │
│  │   Server    │ │   Server     │ │     Server          │  │
│  └─────────────┘ └──────────────┘ └─────────────────────┘  │
│  ┌─────────────┐ ┌──────────────┐ ┌─────────────────────┐  │
│  │   Email     │ │   Analytics  │ │    Custom APIs      │  │
│  │   Server    │ │    Server    │ │      Server         │  │
│  └─────────────┘ └──────────────┘ └─────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
          │                  │                   │
┌─────────▼──────────────────▼───────────────────▼────────────┐
│                   CAPA DE SERVICIOS                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │PostgreSQL│  │  Redis   │  │  Claude  │  │   APIs   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Configuración Avanzada de Claude Desktop con MCP

### 2.1 Configuración de Múltiples Servidores MCP

El archivo de configuración de Claude Desktop (`claude_desktop_config.json`) permite configurar múltiples servidores MCP simultáneamente.

**Ubicación del archivo:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "database-manager": {
      "command": "python",
      "args": [
        "/Users/tu-usuario/mcp-servers/database_server.py"
      ],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb",
        "REDIS_URL": "redis://localhost:6379"
      }
    },
    "ai-assistant": {
      "command": "python",
      "args": [
        "/Users/tu-usuario/mcp-servers/ai_server.py"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "OPENAI_API_KEY": "sk-..."
      }
    },
    "file-operations": {
      "command": "python",
      "args": [
        "/Users/tu-usuario/mcp-servers/file_server.py"
      ],
      "env": {
        "WORKSPACE_PATH": "/Users/tu-usuario/workspace",
        "MAX_FILE_SIZE_MB": "10"
      }
    },
    "analytics-engine": {
      "command": "python",
      "args": [
        "/Users/tu-usuario/mcp-servers/analytics_server.py"
      ],
      "env": {
        "DATA_WAREHOUSE_URL": "postgresql://localhost:5432/analytics"
      }
    },
    "notification-hub": {
      "command": "python",
      "args": [
        "/Users/tu-usuario/mcp-servers/notification_server.py"
      ],
      "env": {
        "SLACK_WEBHOOK": "https://hooks.slack.com/services/...",
        "DISCORD_WEBHOOK": "https://discord.com/api/webhooks/...",
        "EMAIL_SERVER": "smtp.gmail.com"
      }
    }
  },
  "globalShortcut": "Cmd+Shift+Space"
}
```

### 2.2 Servidor MCP para Operaciones de Archivo

```python
# file_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from pathlib import Path
import os
import json
from datetime import datetime

mcp = FastMCP("File Operations Server")

# Configuración
WORKSPACE_PATH = Path(os.getenv("WORKSPACE_PATH", "./workspace"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))

@mcp.tool()
async def list_files(
    directory: str = ".",
    pattern: str = "*",
    recursive: bool = False
) -> Dict[str, Any]:
    """
    Lista archivos en un directorio

    Args:
        directory: Directorio a listar (relativo al workspace)
        pattern: Patrón de búsqueda (glob)
        recursive: Buscar recursivamente
    """
    target_dir = WORKSPACE_PATH / directory

    if not target_dir.exists():
        return {"error": f"Directory {directory} not found"}

    if recursive:
        files = list(target_dir.rglob(pattern))
    else:
        files = list(target_dir.glob(pattern))

    return {
        "directory": str(directory),
        "count": len(files),
        "files": [
            {
                "name": f.name,
                "path": str(f.relative_to(WORKSPACE_PATH)),
                "size": f.stat().st_size if f.is_file() else 0,
                "is_directory": f.is_dir(),
                "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
            }
            for f in files
        ]
    }

@mcp.tool()
async def read_file(file_path: str) -> Dict[str, Any]:
    """
    Lee el contenido de un archivo

    Args:
        file_path: Ruta del archivo (relativa al workspace)
    """
    target_file = WORKSPACE_PATH / file_path

    if not target_file.exists():
        return {"error": f"File {file_path} not found"}

    if not target_file.is_file():
        return {"error": f"{file_path} is not a file"}

    # Verificar tamaño
    size_mb = target_file.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return {
            "error": f"File too large: {size_mb:.2f}MB (max: {MAX_FILE_SIZE_MB}MB)"
        }

    try:
        # Intentar leer como texto
        content = target_file.read_text(encoding='utf-8')
        return {
            "path": file_path,
            "content": content,
            "size": target_file.stat().st_size,
            "lines": len(content.splitlines()),
            "encoding": "utf-8"
        }
    except UnicodeDecodeError:
        # Si falla, es binario
        return {
            "path": file_path,
            "error": "Binary file - cannot display as text",
            "size": target_file.stat().st_size,
            "encoding": "binary"
        }

@mcp.tool()
async def write_file(
    file_path: str,
    content: str,
    create_dirs: bool = True
) -> Dict[str, Any]:
    """
    Escribe contenido a un archivo

    Args:
        file_path: Ruta del archivo
        content: Contenido a escribir
        create_dirs: Crear directorios si no existen
    """
    target_file = WORKSPACE_PATH / file_path

    # Crear directorios si es necesario
    if create_dirs:
        target_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        target_file.write_text(content, encoding='utf-8')
        return {
            "success": True,
            "path": file_path,
            "size": target_file.stat().st_size,
            "message": f"File written successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def search_in_files(
    search_term: str,
    directory: str = ".",
    file_pattern: str = "*.py",
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """
    Busca un término en archivos

    Args:
        search_term: Término a buscar
        directory: Directorio donde buscar
        file_pattern: Patrón de archivos
        case_sensitive: Búsqueda sensible a mayúsculas
    """
    target_dir = WORKSPACE_PATH / directory

    if not target_dir.exists():
        return {"error": f"Directory {directory} not found"}

    results = []
    files = list(target_dir.rglob(file_pattern))

    for file in files:
        if not file.is_file():
            continue

        try:
            content = file.read_text(encoding='utf-8')
            lines = content.splitlines()

            for line_num, line in enumerate(lines, 1):
                check_line = line if case_sensitive else line.lower()
                check_term = search_term if case_sensitive else search_term.lower()

                if check_term in check_line:
                    results.append({
                        "file": str(file.relative_to(WORKSPACE_PATH)),
                        "line_number": line_num,
                        "line_content": line.strip(),
                        "match_position": check_line.index(check_term)
                    })
        except:
            continue

    return {
        "search_term": search_term,
        "directory": directory,
        "files_searched": len(files),
        "matches_found": len(results),
        "results": results[:100]  # Limitar a 100 resultados
    }

@mcp.tool()
async def create_directory(
    directory_path: str,
    parents: bool = True
) -> Dict[str, Any]:
    """
    Crea un directorio

    Args:
        directory_path: Ruta del directorio
        parents: Crear directorios padre si no existen
    """
    target_dir = WORKSPACE_PATH / directory_path

    try:
        target_dir.mkdir(parents=parents, exist_ok=False)
        return {
            "success": True,
            "path": directory_path,
            "message": "Directory created successfully"
        }
    except FileExistsError:
        return {
            "success": False,
            "error": "Directory already exists"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def analyze_directory(
    directory: str = "."
) -> Dict[str, Any]:
    """
    Analiza un directorio y retorna estadísticas

    Args:
        directory: Directorio a analizar
    """
    target_dir = WORKSPACE_PATH / directory

    if not target_dir.exists():
        return {"error": f"Directory {directory} not found"}

    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "file_types": {},
        "largest_files": []
    }

    files_with_size = []

    for item in target_dir.rglob("*"):
        if item.is_file():
            stats["total_files"] += 1
            size = item.stat().st_size
            stats["total_size"] += size

            # Contar por extensión
            ext = item.suffix or "no_extension"
            stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1

            # Guardar para encontrar los más grandes
            files_with_size.append({
                "path": str(item.relative_to(WORKSPACE_PATH)),
                "size": size,
                "size_mb": size / (1024 * 1024)
            })
        elif item.is_dir():
            stats["total_dirs"] += 1

    # Top 10 archivos más grandes
    files_with_size.sort(key=lambda x: x["size"], reverse=True)
    stats["largest_files"] = files_with_size[:10]

    return {
        "directory": directory,
        "statistics": {
            **stats,
            "total_size_mb": stats["total_size"] / (1024 * 1024),
            "average_file_size": stats["total_size"] / stats["total_files"] if stats["total_files"] > 0 else 0
        }
    }

@mcp.resource("files://workspace-info")
async def workspace_info() -> str:
    """Información del workspace"""
    return json.dumps({
        "workspace_path": str(WORKSPACE_PATH),
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "exists": WORKSPACE_PATH.exists(),
        "is_directory": WORKSPACE_PATH.is_dir() if WORKSPACE_PATH.exists() else False
    }, indent=2)

if __name__ == "__main__":
    # Asegurar que el workspace existe
    WORKSPACE_PATH.mkdir(parents=True, exist_ok=True)
    mcp.run()
```

### 2.3 Servidor MCP de Analytics

```python
# analytics_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import asyncpg
import json
from datetime import datetime, timedelta

mcp = FastMCP("Analytics Engine Server")

# Pool de conexiones
db_pool = None

async def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            os.getenv("DATA_WAREHOUSE_URL"),
            min_size=5,
            max_size=20
        )
    return db_pool

@mcp.tool()
async def get_user_metrics(
    user_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Obtiene métricas de usuario

    Args:
        user_id: ID del usuario (None para todos)
        start_date: Fecha inicio (ISO format)
        end_date: Fecha fin (ISO format)
    """
    pool = await get_db_pool()

    # Parsear fechas
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
    if not end_date:
        end_date = datetime.now().isoformat()

    query = """
        SELECT
            COUNT(*) as total_actions,
            COUNT(DISTINCT user_id) as unique_users,
            AVG(session_duration) as avg_session_duration,
            COUNT(DISTINCT DATE(created_at)) as active_days
        FROM user_events
        WHERE created_at BETWEEN $1 AND $2
    """

    params = [start_date, end_date]

    if user_id:
        query += " AND user_id = $3"
        params.append(user_id)

    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, *params)

    return {
        "period": {
            "start": start_date,
            "end": end_date
        },
        "metrics": dict(row) if row else {}
    }

@mcp.tool()
async def get_conversion_funnel(
    funnel_steps: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analiza un funnel de conversión

    Args:
        funnel_steps: Lista de eventos que conforman el funnel
        start_date: Fecha inicio
        end_date: Fecha fin
    """
    pool = await get_db_pool()

    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).isoformat()
    if not end_date:
        end_date = datetime.now().isoformat()

    results = []
    previous_users = None

    for step in funnel_steps:
        query = """
            SELECT COUNT(DISTINCT user_id) as users
            FROM user_events
            WHERE event_name = $1
            AND created_at BETWEEN $2 AND $3
        """

        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, step, start_date, end_date)

        users = row['users']

        step_data = {
            "step": step,
            "users": users,
            "conversion_rate": None,
            "dropoff_rate": None
        }

        if previous_users is not None:
            step_data["conversion_rate"] = (users / previous_users * 100) if previous_users > 0 else 0
            step_data["dropoff_rate"] = 100 - step_data["conversion_rate"]

        results.append(step_data)
        previous_users = users

    return {
        "funnel": funnel_steps,
        "period": {"start": start_date, "end": end_date},
        "steps": results,
        "overall_conversion": (results[-1]["users"] / results[0]["users"] * 100) if results[0]["users"] > 0 else 0
    }

@mcp.tool()
async def get_cohort_analysis(
    cohort_date: str,
    metric: str = "retention",
    periods: int = 12
) -> Dict[str, Any]:
    """
    Análisis de cohortes

    Args:
        cohort_date: Fecha de la cohorte (YYYY-MM)
        metric: Métrica a analizar (retention, revenue, engagement)
        periods: Número de períodos a analizar
    """
    pool = await get_db_pool()

    # Query base para obtener usuarios de la cohorte
    query = """
        SELECT user_id
        FROM users
        WHERE DATE_TRUNC('month', created_at) = $1
    """

    async with pool.acquire() as conn:
        cohort_users = await conn.fetch(query, cohort_date)

    user_ids = [row['user_id'] for row in cohort_users]
    cohort_size = len(user_ids)

    if cohort_size == 0:
        return {"error": "No users found for this cohort"}

    # Analizar retención por período
    retention_data = []

    for period in range(periods):
        period_start = datetime.fromisoformat(cohort_date) + timedelta(days=30 * period)
        period_end = period_start + timedelta(days=30)

        query = """
            SELECT COUNT(DISTINCT user_id) as active_users
            FROM user_events
            WHERE user_id = ANY($1)
            AND created_at BETWEEN $2 AND $3
        """

        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, user_ids, period_start, period_end)

        active_users = row['active_users']
        retention_rate = (active_users / cohort_size * 100) if cohort_size > 0 else 0

        retention_data.append({
            "period": period,
            "month": period_start.strftime("%Y-%m"),
            "active_users": active_users,
            "retention_rate": round(retention_rate, 2)
        })

    return {
        "cohort_date": cohort_date,
        "cohort_size": cohort_size,
        "metric": metric,
        "periods_analyzed": periods,
        "data": retention_data
    }

@mcp.tool()
async def generate_dashboard_data(
    dashboard_type: str = "overview",
    date_range: str = "last_30_days"
) -> Dict[str, Any]:
    """
    Genera datos para dashboards

    Args:
        dashboard_type: Tipo de dashboard (overview, sales, users, engagement)
        date_range: Rango de fechas (last_7_days, last_30_days, last_90_days)
    """
    # Calcular fechas
    days_map = {
        "last_7_days": 7,
        "last_30_days": 30,
        "last_90_days": 90
    }

    days = days_map.get(date_range, 30)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    pool = await get_db_pool()

    async with pool.acquire() as conn:
        # Métricas generales
        total_users = await conn.fetchval(
            "SELECT COUNT(*) FROM users WHERE created_at >= $1",
            start_date
        )

        total_events = await conn.fetchval(
            "SELECT COUNT(*) FROM user_events WHERE created_at >= $1",
            start_date
        )

        # Eventos por día
        daily_events = await conn.fetch("""
            SELECT
                DATE(created_at) as date,
                COUNT(*) as events
            FROM user_events
            WHERE created_at >= $1
            GROUP BY DATE(created_at)
            ORDER BY date
        """, start_date)

    return {
        "dashboard_type": dashboard_type,
        "date_range": date_range,
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        "summary": {
            "total_users": total_users,
            "total_events": total_events,
            "avg_events_per_day": total_events / days if days > 0 else 0
        },
        "daily_breakdown": [
            {
                "date": row['date'].isoformat(),
                "events": row['events']
            }
            for row in daily_events
        ]
    }

@mcp.resource("analytics://available-metrics")
async def available_metrics() -> str:
    """Lista de métricas disponibles"""
    metrics = {
        "user_metrics": ["total_actions", "unique_users", "avg_session_duration", "active_days"],
        "conversion_metrics": ["conversion_rate", "dropoff_rate", "funnel_completion"],
        "cohort_metrics": ["retention_rate", "revenue_per_user", "engagement_score"],
        "dashboard_types": ["overview", "sales", "users", "engagement"]
    }

    return json.dumps(metrics, indent=2)

if __name__ == "__main__":
    mcp.run()
```

### 2.4 Probar la Configuración en Claude Desktop

Una vez configurados los servidores, reinicia Claude Desktop y verifica que aparezcan los tools:

```
Usuario: "¿Qué herramientas tienes disponibles?"

Claude: "Tengo acceso a las siguientes herramientas MCP:

**Database Manager:**
- query_users
- create_user
- update_user
- delete_user

**AI Assistant:**
- analyze_sentiment
- summarize_text
- extract_entities
- classify_text

**File Operations:**
- list_files
- read_file
- write_file
- search_in_files
- analyze_directory

**Analytics Engine:**
- get_user_metrics
- get_conversion_funnel
- get_cohort_analysis
- generate_dashboard_data

**Notification Hub:**
- send_slack_notification
- send_discord_notification
- send_email
- broadcast_notification

¿Qué te gustaría hacer?"
```

---

## 3. Integración Completa: FastMCP + Claude + n8n

### 3.1 Arquitectura de la Integración

```
┌──────────────────────────────────────────────────────────┐
│                      FLUJO DE DATOS                       │
└──────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   n8n        │────▶│   FastMCP    │────▶│   Claude     │
│   Workflow   │◀────│   HTTP       │◀────│   Desktop    │
└──────────────┘     │   Wrapper    │     └──────────────┘
                     └──────────────┘
                            │
                     ┌──────▼──────┐
                     │  MCP Server │
                     │   Database  │
                     │   AI Tools  │
                     │   Files     │
                     └─────────────┘
```

### 3.2 MCP HTTP Wrapper Mejorado

```python
# mcp_http_wrapper_advanced.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastMCP HTTP Wrapper Advanced",
    description="HTTP wrapper para servidores MCP con features avanzadas",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class MCPToolCall(BaseModel):
    server: str = Field(..., description="Nombre del servidor MCP")
    tool: str = Field(..., description="Nombre de la herramienta")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Argumentos")

class MCPBatchCall(BaseModel):
    calls: List[MCPToolCall] = Field(..., description="Lista de llamadas a ejecutar")
    parallel: bool = Field(default=True, description="Ejecutar en paralelo")

class MCPResourceRequest(BaseModel):
    server: str
    resource_uri: str

# Configuración de servidores
MCP_SERVERS = {
    "database": {
        "command": "python",
        "args": ["/path/to/database_server.py"],
        "env": {}
    },
    "ai": {
        "command": "python",
        "args": ["/path/to/ai_server.py"],
        "env": {}
    },
    "files": {
        "command": "python",
        "args": ["/path/to/file_server.py"],
        "env": {}
    },
    "analytics": {
        "command": "python",
        "args": ["/path/to/analytics_server.py"],
        "env": {}
    },
    "notifications": {
        "command": "python",
        "args": ["/path/to/notification_server.py"],
        "env": {}
    }
}

# Cache de sesiones
mcp_sessions = {}
session_stats = {}

async def get_mcp_session(server_name: str):
    """Obtiene o crea una sesión MCP con stats"""
    if server_name not in MCP_SERVERS:
        raise HTTPException(
            status_code=404,
            detail=f"Server '{server_name}' not found. Available: {list(MCP_SERVERS.keys())}"
        )

    if server_name not in mcp_sessions:
        logger.info(f"Creating new MCP session for '{server_name}'")
        config = MCP_SERVERS[server_name]
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=config.get("env", {})
        )

        try:
            read, write = await stdio_client(server_params).__aenter__()
            session = await ClientSession(read, write).__aenter__()
            await session.initialize()

            mcp_sessions[server_name] = session
            session_stats[server_name] = {
                "created_at": datetime.now().isoformat(),
                "total_calls": 0,
                "total_errors": 0,
                "last_call": None
            }

            logger.info(f"Session created successfully for '{server_name}'")
        except Exception as e:
            logger.error(f"Failed to create session for '{server_name}': {e}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize server: {str(e)}")

    return mcp_sessions[server_name]

@app.post("/mcp/tool")
async def call_mcp_tool(request: MCPToolCall):
    """
    Llama a una herramienta MCP

    Example:
    ```json
    {
      "server": "database",
      "tool": "query_users",
      "arguments": {"limit": 10}
    }
    ```
    """
    start_time = datetime.now()

    try:
        session = await get_mcp_session(request.server)

        logger.info(f"Calling {request.server}.{request.tool} with args: {request.arguments}")

        result = await session.call_tool(
            request.tool,
            arguments=request.arguments
        )

        # Actualizar stats
        session_stats[request.server]["total_calls"] += 1
        session_stats[request.server]["last_call"] = datetime.now().isoformat()

        # Procesar resultado
        if result.content:
            response_data = result.content[0].text

            try:
                response_data = json.loads(response_data)
            except:
                pass

            duration = (datetime.now() - start_time).total_seconds()

            return {
                "success": True,
                "server": request.server,
                "tool": request.tool,
                "result": response_data,
                "metadata": {
                    "duration_seconds": duration,
                    "timestamp": datetime.now().isoformat()
                }
            }

        return {
            "success": False,
            "error": "No content in response"
        }

    except Exception as e:
        logger.error(f"Error calling {request.server}.{request.tool}: {e}")

        if request.server in session_stats:
            session_stats[request.server]["total_errors"] += 1

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "server": request.server,
                "tool": request.tool
            }
        )

@app.post("/mcp/batch")
async def call_mcp_batch(request: MCPBatchCall):
    """
    Ejecuta múltiples llamadas MCP en batch

    Example:
    ```json
    {
      "parallel": true,
      "calls": [
        {"server": "database", "tool": "query_users", "arguments": {}},
        {"server": "analytics", "tool": "get_user_metrics", "arguments": {}}
      ]
    }
    ```
    """
    results = []

    async def execute_call(call: MCPToolCall, index: int):
        try:
            response = await call_mcp_tool(call)
            return {
                "index": index,
                "success": True,
                "call": {
                    "server": call.server,
                    "tool": call.tool
                },
                "result": response
            }
        except Exception as e:
            return {
                "index": index,
                "success": False,
                "call": {
                    "server": call.server,
                    "tool": call.tool
                },
                "error": str(e)
            }

    if request.parallel:
        # Ejecutar en paralelo
        tasks = [execute_call(call, i) for i, call in enumerate(request.calls)]
        results = await asyncio.gather(*tasks)
    else:
        # Ejecutar secuencialmente
        for i, call in enumerate(request.calls):
            result = await execute_call(call, i)
            results.append(result)

    # Ordenar por índice
    results.sort(key=lambda x: x["index"])

    return {
        "total_calls": len(request.calls),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "execution_mode": "parallel" if request.parallel else "sequential",
        "results": results
    }

@app.post("/mcp/resource")
async def get_mcp_resource(request: MCPResourceRequest):
    """Obtiene un recurso MCP"""
    try:
        session = await get_mcp_session(request.server)

        result = await session.read_resource(request.resource_uri)

        if result.contents:
            content = result.contents[0]

            return {
                "success": True,
                "server": request.server,
                "resource_uri": request.resource_uri,
                "content": content.text if hasattr(content, 'text') else str(content)
            }

        return {
            "success": False,
            "error": "No content in resource"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/servers")
async def list_servers():
    """Lista servidores MCP disponibles"""
    server_info = []

    for server_name, config in MCP_SERVERS.items():
        info = {
            "name": server_name,
            "command": config["command"],
            "status": "active" if server_name in mcp_sessions else "inactive",
            "stats": session_stats.get(server_name, {})
        }
        server_info.append(info)

    return {
        "total_servers": len(MCP_SERVERS),
        "active_sessions": len(mcp_sessions),
        "servers": server_info
    }

@app.get("/mcp/tools/{server_name}")
async def list_tools(server_name: str):
    """Lista herramientas disponibles en un servidor"""
    try:
        session = await get_mcp_session(server_name)
        tools = await session.list_tools()

        return {
            "server": server_name,
            "total_tools": len(tools.tools),
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in tools.tools
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mcp/resources/{server_name}")
async def list_resources(server_name: str):
    """Lista recursos disponibles en un servidor"""
    try:
        session = await get_mcp_session(server_name)
        resources = await session.list_resources()

        return {
            "server": server_name,
            "total_resources": len(resources.resources),
            "resources": [
                {
                    "uri": resource.uri,
                    "name": resource.name,
                    "description": resource.description
                }
                for resource in resources.resources
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "servers": {
            "total": len(MCP_SERVERS),
            "active": len(mcp_sessions)
        },
        "stats": session_stats
    }

@app.get("/stats")
async def get_stats():
    """Obtiene estadísticas detalladas"""
    total_calls = sum(stats.get("total_calls", 0) for stats in session_stats.values())
    total_errors = sum(stats.get("total_errors", 0) for stats in session_stats.values())

    return {
        "summary": {
            "total_calls": total_calls,
            "total_errors": total_errors,
            "error_rate": (total_errors / total_calls * 100) if total_calls > 0 else 0,
            "active_servers": len(mcp_sessions)
        },
        "servers": session_stats
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
```

---

### 3.3 Workflows n8n Avanzados

#### Workflow 1: Sistema de Análisis de Contenido Completo

Este workflow combina múltiples servidores MCP para analizar contenido, guardar resultados y notificar.

```json
{
  "name": "Content Analysis Pipeline Advanced",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "content/analyze/complete",
        "responseMode": "responseNode"
      },
      "id": "webhook-start",
      "name": "Webhook - Receive Content",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 450]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/batch",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  parallel: true,\n  calls: [\n    {\n      server: 'ai',\n      tool: 'analyze_sentiment',\n      arguments: {\n        text: $json.body.content,\n        language: $json.body.language || 'en'\n      }\n    },\n    {\n      server: 'ai',\n      tool: 'extract_entities',\n      arguments: {\n        text: $json.body.content\n      }\n    },\n    {\n      server: 'ai',\n      tool: 'summarize_text',\n      arguments: {\n        text: $json.body.content,\n        max_length: 200,\n        style: 'concise'\n      }\n    },\n    {\n      server: 'ai',\n      tool: 'classify_text',\n      arguments: {\n        text: $json.body.content,\n        categories: ['tech', 'business', 'politics', 'entertainment', 'sports']\n      }\n    }\n  ]\n}) }}"
      },
      "id": "batch-analysis",
      "name": "Batch AI Analysis",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 450]
    },
    {
      "parameters": {
        "functionCode": "// Combinar todos los resultados del batch\nconst batchResults = $input.item.json.results;\nconst originalContent = $('Webhook - Receive Content').item.json.body.content;\n\nconst analysis = {\n  content: originalContent,\n  metadata: {\n    analyzed_at: new Date().toISOString(),\n    word_count: originalContent.split(' ').length,\n    char_count: originalContent.length\n  },\n  sentiment: null,\n  entities: null,\n  summary: null,\n  category: null\n};\n\n// Extraer resultados de cada análisis\nfor (const result of batchResults) {\n  if (!result.success) continue;\n  \n  const callInfo = result.call;\n  const data = result.result.result;\n  \n  switch(callInfo.tool) {\n    case 'analyze_sentiment':\n      analysis.sentiment = data;\n      break;\n    case 'extract_entities':\n      analysis.entities = data;\n      break;\n    case 'summarize_text':\n      analysis.summary = data;\n      break;\n    case 'classify_text':\n      analysis.category = data;\n      break;\n  }\n}\n\n// Calcular score de calidad\nlet qualityScore = 100;\nif (analysis.sentiment?.sentiment === 'negative') qualityScore -= 20;\nif (analysis.summary?.summary_length < 50) qualityScore -= 10;\nif (!analysis.entities || analysis.entities.entities?.length === 0) qualityScore -= 15;\n\nanalysis.quality_score = Math.max(0, qualityScore);\n\nreturn { json: analysis };"
      },
      "id": "combine-results",
      "name": "Combine Analysis Results",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [650, 450]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'files',\n  tool: 'write_file',\n  arguments: {\n    file_path: `analysis/content_${new Date().getTime()}.json`,\n    content: JSON.stringify($json, null, 2),\n    create_dirs: true\n  }\n}) }}"
      },
      "id": "save-analysis",
      "name": "Save Analysis to File",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [850, 350]
    },
    {
      "parameters": {
        "operation": "insertOne",
        "collection": "content_analysis",
        "fields": "content,sentiment,entities,summary,category,quality_score,metadata"
      },
      "id": "mongo-save",
      "name": "Save to MongoDB",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [850, 450]
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{ $json.quality_score }}",
              "operation": "smaller",
              "value2": 50
            }
          ]
        }
      },
      "id": "quality-check",
      "name": "Quality Below Threshold?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [850, 550]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'notifications',\n  tool: 'send_slack_notification',\n  arguments: {\n    webhook_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',\n    message: `⚠️ Low Quality Content Detected\\nQuality Score: ${$('Combine Analysis Results').item.json.quality_score}\\nSentiment: ${$('Combine Analysis Results').item.json.sentiment?.sentiment || 'unknown'}\\nCategory: ${$('Combine Analysis Results').item.json.category?.primary_category || 'unknown'}`,\n    emoji: ':warning:'\n  }\n}) }}"
      },
      "id": "alert-low-quality",
      "name": "Alert Team - Low Quality",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [1050, 650]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $('Combine Analysis Results').item.json }}",
        "options": {
          "responseHeaders": {
            "entries": [
              {
                "name": "X-Analysis-Id",
                "value": "={{ $('Save to MongoDB').item.json._id }}"
              }
            ]
          }
        }
      },
      "id": "respond-result",
      "name": "Respond with Results",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1250, 450]
    }
  ],
  "connections": {
    "Webhook - Receive Content": {
      "main": [[{"node": "Batch AI Analysis", "type": "main", "index": 0}]]
    },
    "Batch AI Analysis": {
      "main": [[{"node": "Combine Analysis Results", "type": "main", "index": 0}]]
    },
    "Combine Analysis Results": {
      "main": [[
        {"node": "Save Analysis to File", "type": "main", "index": 0},
        {"node": "Save to MongoDB", "type": "main", "index": 0},
        {"node": "Quality Below Threshold?", "type": "main", "index": 0}
      ]]
    },
    "Quality Below Threshold?": {
      "main": [
        [{"node": "Alert Team - Low Quality", "type": "main", "index": 0}],
        []
      ]
    },
    "Save to MongoDB": {
      "main": [[{"node": "Respond with Results", "type": "main", "index": 0}]]
    }
  },
  "active": true,
  "settings": {
    "executionOrder": "v1"
  }
}
```

Este workflow:
1. Recibe contenido via webhook
2. Ejecuta 4 análisis de IA en paralelo (sentiment, entities, summary, classify)
3. Combina los resultados y calcula un quality score
4. Guarda el análisis en archivo JSON y MongoDB
5. Si la calidad es baja (<50), envía alerta a Slack
6. Responde con los resultados completos

---

## 4. Patrones Avanzados de MCP

### 4.1 Patrón: Rate Limiting y Throttling

```python
# patterns/rate_limiter.py
from fastmcp import FastMCP
from typing import Dict, Any
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
import redis.asyncio as aioredis

mcp = FastMCP("Rate Limited Server")

# Redis para rate limiting distribuido
redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url(
            "redis://localhost:6379",
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client

class RateLimiter:
    """Rate limiter usando Redis"""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def is_allowed(self, key: str) -> tuple[bool, Dict[str, Any]]:
        """
        Verifica si la request está permitida

        Returns:
            tuple[bool, dict]: (permitido, metadata)
        """
        redis = await get_redis()

        # Usar sliding window con sorted sets
        now = datetime.now().timestamp()
        window_start = now - self.window_seconds

        # Limpiar requests antiguas
        await redis.zremrangebyscore(f"ratelimit:{key}", 0, window_start)

        # Contar requests en la ventana
        current_requests = await redis.zcard(f"ratelimit:{key}")

        if current_requests >= self.max_requests:
            # Rate limit excedido
            ttl = await redis.ttl(f"ratelimit:{key}")
            return False, {
                "allowed": False,
                "current_requests": current_requests,
                "max_requests": self.max_requests,
                "retry_after": ttl,
                "window_seconds": self.window_seconds
            }

        # Agregar request actual
        await redis.zadd(f"ratelimit:{key}", {str(now): now})
        await redis.expire(f"ratelimit:{key}", self.window_seconds)

        remaining = self.max_requests - current_requests - 1

        return True, {
            "allowed": True,
            "current_requests": current_requests + 1,
            "max_requests": self.max_requests,
            "remaining": remaining,
            "window_seconds": self.window_seconds
        }

# Rate limiters por tipo de operación
rate_limiters = {
    "api_calls": RateLimiter(max_requests=100, window_seconds=60),
    "ai_requests": RateLimiter(max_requests=20, window_seconds=60),
    "database_queries": RateLimiter(max_requests=1000, window_seconds=60)
}

@mcp.tool()
async def rate_limited_api_call(
    user_id: str,
    endpoint: str,
    method: str = "GET"
) -> Dict[str, Any]:
    """
    Llamada API con rate limiting

    Args:
        user_id: ID del usuario
        endpoint: Endpoint a llamar
        method: Método HTTP
    """
    limiter = rate_limiters["api_calls"]
    allowed, metadata = await limiter.is_allowed(f"user:{user_id}")

    if not allowed:
        return {
            "success": False,
            "error": "Rate limit exceeded",
            "metadata": metadata
        }

    # Ejecutar la llamada API
    try:
        # Simular llamada API
        await asyncio.sleep(0.1)

        return {
            "success": True,
            "endpoint": endpoint,
            "method": method,
            "rate_limit": metadata
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def throttled_ai_request(
    user_id: str,
    prompt: str
) -> Dict[str, Any]:
    """
    Request AI con throttling

    Args:
        user_id: ID del usuario
        prompt: Prompt para el AI
    """
    limiter = rate_limiters["ai_requests"]
    allowed, metadata = await limiter.is_allowed(f"ai:{user_id}")

    if not allowed:
        return {
            "success": False,
            "error": "AI rate limit exceeded",
            "metadata": metadata,
            "message": f"Please wait {metadata['retry_after']} seconds"
        }

    # Ejecutar request AI
    from anthropic import Anthropic

    try:
        client = Anthropic()
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "success": True,
            "response": message.content[0].text,
            "rate_limit": metadata,
            "tokens_used": message.usage.input_tokens + message.usage.output_tokens
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

### 4.2 Patrón: Cache Inteligente con TTL

```python
# patterns/smart_cache.py
from fastmcp import FastMCP
from typing import Dict, Any, Optional
import asyncio
import json
import hashlib
from datetime import datetime, timedelta
import redis.asyncio as aioredis

mcp = FastMCP("Smart Cache Server")

class SmartCache:
    """Cache inteligente con TTL variable y invalidación"""

    def __init__(self):
        self.redis = None

    async def get_redis(self):
        if self.redis is None:
            self.redis = await aioredis.from_url(
                "redis://localhost:6379",
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis

    def _generate_key(self, namespace: str, **kwargs) -> str:
        """Genera cache key único"""
        key_data = json.dumps(kwargs, sort_keys=True)
        hash_key = hashlib.sha256(key_data.encode()).hexdigest()[:16]
        return f"cache:{namespace}:{hash_key}"

    async def get(self, namespace: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Obtiene del cache"""
        redis = await self.get_redis()
        key = self._generate_key(namespace, **kwargs)

        data = await redis.get(key)
        if data:
            cached = json.loads(data)

            # Verificar si no ha expirado
            if "expires_at" in cached:
                expires = datetime.fromisoformat(cached["expires_at"])
                if datetime.now() > expires:
                    await redis.delete(key)
                    return None

            # Actualizar stats
            await redis.hincrby("cache:stats", "hits", 1)

            return cached.get("value")

        # Cache miss
        await redis.hincrby("cache:stats", "misses", 1)
        return None

    async def set(
        self,
        namespace: str,
        value: Any,
        ttl_seconds: int = 300,
        **kwargs
    ) -> bool:
        """Guarda en cache con TTL"""
        redis = await self.get_redis()
        key = self._generate_key(namespace, **kwargs)

        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)

        cached_data = {
            "value": value,
            "cached_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "ttl": ttl_seconds
        }

        await redis.setex(
            key,
            ttl_seconds,
            json.dumps(cached_data)
        )

        return True

    async def invalidate(self, namespace: str, **kwargs) -> bool:
        """Invalida cache específico"""
        redis = await self.get_redis()
        key = self._generate_key(namespace, **kwargs)
        result = await redis.delete(key)
        return result > 0

    async def invalidate_namespace(self, namespace: str) -> int:
        """Invalida todo un namespace"""
        redis = await self.get_redis()
        pattern = f"cache:{namespace}:*"

        keys = []
        async for key in redis.scan_iter(match=pattern):
            keys.append(key)

        if keys:
            return await redis.delete(*keys)
        return 0

    async def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del cache"""
        redis = await self.get_redis()
        stats = await redis.hgetall("cache:stats")

        hits = int(stats.get("hits", 0))
        misses = int(stats.get("misses", 0))
        total = hits + misses

        return {
            "hits": hits,
            "misses": misses,
            "total_requests": total,
            "hit_rate": (hits / total * 100) if total > 0 else 0
        }

cache = SmartCache()

@mcp.tool()
async def cached_search(
    query: str,
    use_cache: bool = True
) -> Dict[str, Any]:
    """
    Búsqueda con cache inteligente

    Args:
        query: Query de búsqueda
        use_cache: Usar cache o forzar búsqueda nueva
    """
    # Intentar obtener del cache
    if use_cache:
        cached_result = await cache.get("search", query=query)
        if cached_result:
            return {
                "success": True,
                "query": query,
                "results": cached_result,
                "from_cache": True
            }

    # Ejecutar búsqueda real
    try:
        # Simular búsqueda costosa
        await asyncio.sleep(1)
        results = [
            {"title": f"Result for {query}", "score": 0.95},
            {"title": f"Another result for {query}", "score": 0.87}
        ]

        # Guardar en cache (TTL dinámico basado en query)
        ttl = 300 if len(query) > 10 else 600  # Queries largas = TTL corto
        await cache.set("search", results, ttl_seconds=ttl, query=query)

        return {
            "success": True,
            "query": query,
            "results": results,
            "from_cache": False,
            "ttl": ttl
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def invalidate_search_cache(query: Optional[str] = None) -> Dict[str, Any]:
    """
    Invalida cache de búsqueda

    Args:
        query: Query específica a invalidar (None = todo el namespace)
    """
    if query:
        success = await cache.invalidate("search", query=query)
        return {
            "success": success,
            "invalidated": "specific query",
            "query": query
        }
    else:
        count = await cache.invalidate_namespace("search")
        return {
            "success": True,
            "invalidated": "entire namespace",
            "keys_deleted": count
        }

@mcp.tool()
async def get_cache_stats() -> Dict[str, Any]:
    """Obtiene estadísticas del cache"""
    return await cache.get_stats()

if __name__ == "__main__":
    mcp.run()
```

### 4.3 Patrón: Observabilidad y Métricas

```python
# patterns/observability.py
from fastmcp import FastMCP
from typing import Dict, Any, Optional
import time
from datetime import datetime
from functools import wraps
import logging
from prometheus_client import Counter, Histogram, Gauge
import json

mcp = FastMCP("Observability Server")

# Configurar logging estructurado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Métricas Prometheus
tool_calls_total = Counter(
    'mcp_tool_calls_total',
    'Total de llamadas a tools MCP',
    ['tool_name', 'status']
)

tool_duration_seconds = Histogram(
    'mcp_tool_duration_seconds',
    'Duración de tools MCP',
    ['tool_name']
)

active_connections = Gauge(
    'mcp_active_connections',
    'Conexiones MCP activas'
)

errors_total = Counter(
    'mcp_errors_total',
    'Total de errores',
    ['tool_name', 'error_type']
)

def observe_tool(func):
    """Decorator para observabilidad de tools"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tool_name = func.__name__
        start_time = time.time()

        # Log inicio
        logger.info(f"Tool called: {tool_name}", extra={
            "tool": tool_name,
            "args": str(args)[:100],
            "kwargs": str(kwargs)[:100]
        })

        try:
            # Ejecutar tool
            result = await func(*args, **kwargs)

            # Registrar métricas de éxito
            duration = time.time() - start_time
            tool_calls_total.labels(tool_name=tool_name, status="success").inc()
            tool_duration_seconds.labels(tool_name=tool_name).observe(duration)

            # Log éxito
            logger.info(f"Tool completed: {tool_name}", extra={
                "tool": tool_name,
                "duration": duration,
                "status": "success"
            })

            return result

        except Exception as e:
            # Registrar métricas de error
            duration = time.time() - start_time
            tool_calls_total.labels(tool_name=tool_name, status="error").inc()
            tool_duration_seconds.labels(tool_name=tool_name).observe(duration)
            errors_total.labels(
                tool_name=tool_name,
                error_type=type(e).__name__
            ).inc()

            # Log error
            logger.error(f"Tool failed: {tool_name}", extra={
                "tool": tool_name,
                "duration": duration,
                "error": str(e),
                "error_type": type(e).__name__
            }, exc_info=True)

            raise

    return wrapper

@mcp.tool()
@observe_tool
async def monitored_operation(
    operation: str,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Operación monitoreada con métricas completas

    Args:
        operation: Tipo de operación
        data: Datos de la operación
    """
    # Simular operación
    import asyncio
    await asyncio.sleep(0.5)

    return {
        "success": True,
        "operation": operation,
        "result": f"Processed {len(data)} items"
    }

@mcp.tool()
async def get_metrics() -> Dict[str, Any]:
    """Obtiene métricas actuales del sistema"""
    from prometheus_client import REGISTRY
    from prometheus_client.openmetrics.exposition import generate_latest

    # Generar métricas en formato Prometheus
    metrics_output = generate_latest(REGISTRY).decode('utf-8')

    return {
        "success": True,
        "format": "prometheus",
        "metrics": metrics_output
    }

@mcp.tool()
async def health_check(
    include_dependencies: bool = True
) -> Dict[str, Any]:
    """
    Health check completo del sistema

    Args:
        include_dependencies: Incluir check de dependencias
    """
    health = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }

    # Check básico
    health["checks"]["server"] = {
        "status": "healthy",
        "message": "Server is running"
    }

    if include_dependencies:
        # Check Redis
        try:
            import redis.asyncio as aioredis
            redis_client = await aioredis.from_url("redis://localhost:6379")
            await redis_client.ping()
            health["checks"]["redis"] = {
                "status": "healthy",
                "message": "Redis connection OK"
            }
        except Exception as e:
            health["checks"]["redis"] = {
                "status": "unhealthy",
                "message": str(e)
            }
            health["status"] = "degraded"

        # Check Database
        try:
            import asyncpg
            conn = await asyncpg.connect(
                host="localhost",
                database="mydb",
                user="user",
                password="pass"
            )
            await conn.fetchval("SELECT 1")
            await conn.close()
            health["checks"]["database"] = {
                "status": "healthy",
                "message": "Database connection OK"
            }
        except Exception as e:
            health["checks"]["database"] = {
                "status": "unhealthy",
                "message": str(e)
            }
            health["status"] = "degraded"

    return health

if __name__ == "__main__":
    mcp.run()
```

---

## 5. Proyecto Real: Sistema de Análisis de Contenido con IA

### 5.1 Arquitectura del Sistema

```
┌────────────────────────────────────────────────────────┐
│              Content Analysis System                    │
└────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   n8n        │─────▶│   FastMCP    │─────▶│   Claude     │
│   Webhook    │      │   HTTP       │      │   Desktop    │
└──────────────┘      │   Wrapper    │      └──────────────┘
                      └──────┬───────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐         ┌────▼────┐        ┌────▼────┐
    │ Files   │         │Analytics│        │ Memory  │
    │  MCP    │         │   MCP   │        │   MCP   │
    └─────────┘         └─────────┘        └─────────┘
         │                   │                   │
    ┌────▼────┐         ┌────▼────┐        ┌────▼────┐
    │FileSystem         │PostgreSQL│        │  Redis  │
    └─────────┘         └─────────┘        └─────────┘
```

### 5.2 Servidor de Analytics Avanzado

```python
# servers/advanced_analytics.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import asyncpg
from datetime import datetime, timedelta
import json

mcp = FastMCP("Advanced Analytics Server")

db_pool = None

async def get_db():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            host="localhost",
            database="analytics",
            user="user",
            password="pass",
            min_size=5,
            max_size=20
        )
    return db_pool

@mcp.tool()
async def track_content_analysis(
    content_id: str,
    analysis_type: str,
    results: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Registra análisis de contenido

    Args:
        content_id: ID del contenido
        analysis_type: Tipo de análisis (sentiment, entities, etc.)
        results: Resultados del análisis
        metadata: Metadatos adicionales
    """
    pool = await get_db()

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO content_analytics
            (content_id, analysis_type, results, metadata, created_at)
            VALUES ($1, $2, $3, $4, NOW())
        """, content_id, analysis_type, json.dumps(results),
            json.dumps(metadata or {}))

    return {
        "success": True,
        "content_id": content_id,
        "analysis_type": analysis_type
    }

@mcp.tool()
async def get_content_insights(
    content_id: str,
    include_history: bool = True
) -> Dict[str, Any]:
    """
    Obtiene insights agregados de contenido

    Args:
        content_id: ID del contenido
        include_history: Incluir histórico de análisis
    """
    pool = await get_db()

    async with pool.acquire() as conn:
        # Obtener análisis más reciente
        latest = await conn.fetchrow("""
            SELECT analysis_type, results, created_at
            FROM content_analytics
            WHERE content_id = $1
            ORDER BY created_at DESC
            LIMIT 1
        """, content_id)

        if not latest:
            return {
                "success": False,
                "error": "Content not found"
            }

        insights = {
            "content_id": content_id,
            "latest_analysis": {
                "type": latest["analysis_type"],
                "results": json.loads(latest["results"]),
                "timestamp": latest["created_at"].isoformat()
            }
        }

        if include_history:
            history = await conn.fetch("""
                SELECT analysis_type, results, created_at
                FROM content_analytics
                WHERE content_id = $1
                ORDER BY created_at DESC
                LIMIT 10
            """, content_id)

            insights["history"] = [
                {
                    "type": h["analysis_type"],
                    "results": json.loads(h["results"]),
                    "timestamp": h["created_at"].isoformat()
                }
                for h in history
            ]

        return {
            "success": True,
            **insights
        }

@mcp.tool()
async def get_trending_topics(
    time_range_hours: int = 24,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Obtiene topics trending basados en análisis

    Args:
        time_range_hours: Rango de tiempo en horas
        limit: Número de topics a retornar
    """
    pool = await get_db()

    since = datetime.now() - timedelta(hours=time_range_hours)

    async with pool.acquire() as conn:
        trends = await conn.fetch("""
            SELECT
                jsonb_array_elements_text(results->'entities') as entity,
                COUNT(*) as frequency
            FROM content_analytics
            WHERE analysis_type = 'extract_entities'
            AND created_at >= $1
            GROUP BY entity
            ORDER BY frequency DESC
            LIMIT $2
        """, since, limit)

        return {
            "success": True,
            "time_range_hours": time_range_hours,
            "trends": [
                {
                    "topic": t["entity"],
                    "frequency": t["frequency"]
                }
                for t in trends
            ]
        }

@mcp.tool()
async def sentiment_distribution(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> Dict[str, Any]:
    """
    Distribución de sentimientos en periodo

    Args:
        date_from: Fecha inicio (ISO format)
        date_to: Fecha fin (ISO format)
    """
    pool = await get_db()

    if not date_from:
        date_from = (datetime.now() - timedelta(days=7)).isoformat()
    if not date_to:
        date_to = datetime.now().isoformat()

    async with pool.acquire() as conn:
        distribution = await conn.fetch("""
            SELECT
                results->>'sentiment' as sentiment,
                COUNT(*) as count,
                AVG((results->>'confidence')::float) as avg_confidence
            FROM content_analytics
            WHERE analysis_type = 'analyze_sentiment'
            AND created_at BETWEEN $1 AND $2
            GROUP BY results->>'sentiment'
        """, date_from, date_to)

        total = sum(d["count"] for d in distribution)

        return {
            "success": True,
            "period": {
                "from": date_from,
                "to": date_to
            },
            "total_analyses": total,
            "distribution": [
                {
                    "sentiment": d["sentiment"],
                    "count": d["count"],
                    "percentage": (d["count"] / total * 100) if total > 0 else 0,
                    "avg_confidence": float(d["avg_confidence"]) if d["avg_confidence"] else 0
                }
                for d in distribution
            ]
        }

if __name__ == "__main__":
    mcp.run()
```

### 5.3 Integración con MCPs Populares

```python
# servers/content_system_orchestrator.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
import asyncio

mcp = FastMCP("Content System Orchestrator")

# Clientes MCP
mcp_clients = {}

EXTERNAL_MCPS = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    },
    "brave_search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env": {"BRAVE_API_KEY": "your-key"}
    },
    "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"}
    }
}

async def get_mcp_client(server_name: str) -> ClientSession:
    """Obtiene cliente MCP"""
    if server_name not in mcp_clients:
        config = EXTERNAL_MCPS[server_name]
        params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=config.get("env", {})
        )

        read, write = await stdio_client(params).__aenter__()
        session = await ClientSession(read, write).__aenter__()
        await session.initialize()

        mcp_clients[server_name] = session

    return mcp_clients[server_name]

@mcp.tool()
async def full_content_pipeline(
    url: str,
    save_to_github: bool = True
) -> Dict[str, Any]:
    """
    Pipeline completo de análisis de contenido

    Args:
        url: URL del contenido a analizar
        save_to_github: Crear issue en GitHub con resultados
    """
    results = {
        "url": url,
        "pipeline_steps": [],
        "final_analysis": {}
    }

    try:
        # 1. Buscar información relacionada
        search_client = await get_mcp_client("brave_search")
        search_result = await search_client.call_tool(
            "brave_web_search",
            arguments={"query": url, "count": 3}
        )
        results["pipeline_steps"].append({
            "step": "web_search",
            "status": "completed"
        })

        # 2. Extraer contenido (simulado)
        content = "Sample content from URL"

        # 3. Analizar con IA
        from anthropic import Anthropic
        ai_client = Anthropic()

        # Análisis de sentimiento
        sentiment = ai_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"Analyze sentiment: {content}"
            }]
        )

        results["final_analysis"]["sentiment"] = sentiment.content[0].text
        results["pipeline_steps"].append({
            "step": "ai_analysis",
            "status": "completed"
        })

        # 4. Guardar en filesystem
        fs_client = await get_mcp_client("filesystem")
        filename = f"analysis_{url.replace('https://', '').replace('/', '_')}.json"

        await fs_client.call_tool(
            "write_file",
            arguments={
                "path": f"content_analysis/{filename}",
                "content": json.dumps(results, indent=2)
            }
        )
        results["pipeline_steps"].append({
            "step": "save_filesystem",
            "status": "completed",
            "file": filename
        })

        # 5. Guardar en memoria
        memory_client = await get_mcp_client("memory")
        await memory_client.call_tool(
            "store_memory",
            arguments={
                "key": f"content_{url}",
                "value": json.dumps(results),
                "metadata": {"type": "content_analysis"}
            }
        )
        results["pipeline_steps"].append({
            "step": "save_memory",
            "status": "completed"
        })

        # 6. Crear issue en GitHub si se solicita
        if save_to_github:
            gh_client = await get_mcp_client("github")
            issue = await gh_client.call_tool(
                "create_issue",
                arguments={
                    "repo": "myorg/content-tracker",
                    "title": f"Content Analysis: {url}",
                    "body": f"Analysis completed\n\nFile: {filename}\n\nSentiment: {results['final_analysis']['sentiment'][:100]}...",
                    "labels": ["content-analysis", "automated"]
                }
            )
            results["pipeline_steps"].append({
                "step": "github_issue",
                "status": "completed",
                "issue_url": json.loads(issue.content[0].text).get("html_url")
            })

        results["success"] = True
        results["message"] = "Pipeline completed successfully"

    except Exception as e:
        results["success"] = False
        results["error"] = str(e)

    return results

if __name__ == "__main__":
    mcp.run()
```

---

## 6. Debugging y Optimización

### 6.1 Herramientas de Debugging

```python
# utils/debug_tools.py
from fastmcp import FastMCP
from typing import Dict, Any
import logging
import traceback
import sys
from datetime import datetime

mcp = FastMCP("Debug Tools Server")

# Logger configurado
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler para archivo
file_handler = logging.FileHandler('mcp_debug.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@mcp.tool()
async def debug_tool_execution(
    tool_name: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Ejecuta un tool con debugging completo

    Args:
        tool_name: Nombre del tool
        arguments: Argumentos del tool
    """
    debug_info = {
        "tool": tool_name,
        "arguments": arguments,
        "start_time": datetime.now().isoformat(),
        "logs": [],
        "errors": []
    }

    try:
        logger.debug(f"Executing tool: {tool_name} with args: {arguments}")
        debug_info["logs"].append(f"Starting execution at {debug_info['start_time']}")

        # Simular ejecución
        import asyncio
        await asyncio.sleep(0.1)

        result = {"success": True, "data": "Tool executed"}

        debug_info["result"] = result
        debug_info["status"] = "success"
        debug_info["end_time"] = datetime.now().isoformat()

    except Exception as e:
        error_info = {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        debug_info["errors"].append(error_info)
        debug_info["status"] = "error"

        logger.error(f"Error in tool {tool_name}: {e}", exc_info=True)

    return debug_info

@mcp.tool()
async def profile_tool_performance(
    tool_name: str,
    iterations: int = 100
) -> Dict[str, Any]:
    """
    Profilea el performance de un tool

    Args:
        tool_name: Nombre del tool
        iterations: Número de iteraciones
    """
    import time

    times = []

    for i in range(iterations):
        start = time.time()
        # Simular ejecución
        import asyncio
        await asyncio.sleep(0.01)
        end = time.time()
        times.append(end - start)

    return {
        "tool": tool_name,
        "iterations": iterations,
        "avg_time": sum(times) / len(times),
        "min_time": min(times),
        "max_time": max(times),
        "total_time": sum(times)
    }

if __name__ == "__main__":
    mcp.run()
```

### 6.2 Optimización de Performance

**Tips de Optimización:**

1. **Use Connection Pooling**
```python
# ✅ Correcto
db_pool = await asyncpg.create_pool(min_size=5, max_size=20)

# ❌ Incorrecto
conn = await asyncpg.connect()  # Nueva conexión cada vez
```

2. **Batch Operations**
```python
# ✅ Correcto - Batch
async with pool.acquire() as conn:
    await conn.executemany(
        "INSERT INTO table VALUES ($1, $2)",
        [(1, 'a'), (2, 'b'), (3, 'c')]
    )

# ❌ Incorrecto - Loop
for item in items:
    await conn.execute("INSERT INTO table VALUES ($1, $2)", item)
```

3. **Cache Agresivo**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_computation(param):
    # Computación costosa
    return result
```

4. **Parallel Processing**
```python
# ✅ Correcto - Paralelo
results = await asyncio.gather(*[
    process_item(item) for item in items
])

# ❌ Incorrecto - Secuencial
results = []
for item in items:
    result = await process_item(item)
    results.append(result)
```

---

## 7. Casos de Uso Empresariales

### 7.1 Sistema de Moderación de Contenido

```python
# enterprise/content_moderation.py
from fastmcp import FastMCP
from typing import Dict, Any, List
from anthropic import Anthropic
import asyncio

mcp = FastMCP("Content Moderation System")

ai_client = Anthropic()

@mcp.tool()
async def moderate_content(
    content: str,
    content_type: str = "text",
    strict_mode: bool = False
) -> Dict[str, Any]:
    """
    Modera contenido usando IA

    Args:
        content: Contenido a moderar
        content_type: Tipo de contenido (text, image, video)
        strict_mode: Modo estricto de moderación
    """
    # Análisis con Claude
    moderation_prompt = f"""
    Analyze this content for moderation:

    Content: {content}

    Check for:
    - Hate speech
    - Violence
    - Sexual content
    - Spam
    - Misinformation

    Respond in JSON with:
    {{
        "safe": true/false,
        "flags": ["flag1", "flag2"],
        "severity": "low|medium|high",
        "explanation": "reason"
    }}
    """

    message = ai_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": moderation_prompt}]
    )

    import json
    try:
        result = json.loads(message.content[0].text)
    except:
        result = {"error": "Failed to parse moderation result"}

    # Aplicar reglas adicionales en strict mode
    if strict_mode and not result.get("safe", True):
        result["action"] = "block"
    else:
        result["action"] = "review" if not result.get("safe", True) else "approve"

    return {
        "success": True,
        "content_type": content_type,
        "moderation": result,
        "strict_mode": strict_mode
    }

if __name__ == "__main__":
    mcp.run()
```

### 7.2 Sistema de Recomendaciones Personalizadas

```python
# enterprise/recommendations.py
from fastmcp import FastMCP
from typing import Dict, Any, List
import asyncpg
from datetime import datetime, timedelta

mcp = FastMCP("Recommendation Engine")

@mcp.tool()
async def get_personalized_recommendations(
    user_id: str,
    category: str = "all",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Genera recomendaciones personalizadas

    Args:
        user_id: ID del usuario
        category: Categoría de recomendaciones
        limit: Número de recomendaciones
    """
    # Obtener historial del usuario
    # Calcular similitud con otros usuarios
    # Generar recomendaciones

    recommendations = [
        {
            "item_id": f"item_{i}",
            "score": 0.95 - (i * 0.05),
            "reason": "Based on your interests"
        }
        for i in range(limit)
    ]

    return {
        "success": True,
        "user_id": user_id,
        "category": category,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    mcp.run()
```

---

## Conclusión

Este taller intermedio cubre:

✅ **Configuración avanzada de Claude Desktop** con múltiples MCPs
✅ **5+ servidores MCP especializados** (File Ops, Analytics, Orchestrator)
✅ **Patrones avanzados** (Rate Limiting, Smart Cache, Observability)
✅ **Integración completa con MCPs populares** (Filesystem, Brave, GitHub, Memory, Puppeteer)
✅ **HTTP Wrapper avanzado** con batch operations y stats
✅ **Workflows n8n complejos** con procesamiento paralelo
✅ **Proyecto real de análisis de contenido** con IA
✅ **Debugging y optimización** de performance
✅ **Casos de uso empresariales** (Moderación, Recomendaciones)
✅ **Testing y monitoring** completo

**Próximos pasos:**
1. Implementar los servidores MCP avanzados
2. Configurar Claude Desktop con múltiples MCPs
3. Instalar MCPs del ecosistema
4. Crear workflows n8n complejos
5. Implementar observabilidad con Prometheus
6. Optimizar performance con caching y pooling
7. Desplegar en ambiente de staging
8. Escalar a producción

**Recursos adicionales:**
- [MCP Official Servers](https://github.com/modelcontextprotocol/servers)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [n8n Community Workflows](https://n8n.io/workflows)
- [Prometheus Metrics](https://prometheus.io/docs/practices/naming/)
