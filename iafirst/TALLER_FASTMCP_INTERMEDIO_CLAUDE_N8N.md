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

**(Continuaré en el siguiente mensaje con más contenido intermedio...)**
