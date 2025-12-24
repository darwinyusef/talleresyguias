# Taller Completo: FastMCP para Integración de Múltiples Proyectos con n8n

## 📋 Tabla de Contenidos

1. [Introducción a FastMCP](#introducción-a-fastmcp)
2. [Arquitectura y Conceptos](#arquitectura-y-conceptos)
3. [Instalación y Setup](#instalación-y-setup)
4. [Fundamentos de FastMCP](#fundamentos-de-fastmcp)
5. [Servidores MCP para Diferentes Casos de Uso](#servidores-mcp-para-diferentes-casos-de-uso)
6. [Integración FastMCP con n8n](#integración-fastmcp-con-n8n)
7. [Proyectos Multi-Servicio Completos](#proyectos-multi-servicio-completos)
8. [Patrones y Mejores Prácticas](#patrones-y-mejores-prácticas)
9. [Deployment y Producción](#deployment-y-producción)

---

## 1. Introducción a FastMCP

### ¿Qué es FastMCP?

FastMCP es una implementación rápida y moderna del **Model Context Protocol (MCP)** de Anthropic. Permite crear servidores que exponen herramientas, recursos y prompts que pueden ser consumidos por LLMs y otras aplicaciones.

### ¿Por qué FastMCP?

- **Simplicidad**: Sintaxis similar a FastAPI
- **Type Safety**: Validación automática con Pydantic
- **Async First**: Soporte nativo para operaciones asíncronas
- **Integración fácil**: Compatible con n8n, Claude Desktop, y otras herramientas

### Casos de Uso

1. **Orquestación de microservicios**
2. **Integración de bases de datos**
3. **Automatización de workflows**
4. **APIs unificadas para IA**
5. **Gestión de recursos empresariales**

---

## 2. Arquitectura y Conceptos

### Componentes de MCP

```
┌─────────────────┐
│   MCP Client    │
│  (n8n, Claude)  │
└────────┬────────┘
         │
         │ MCP Protocol
         │ (stdio/HTTP)
         │
┌────────▼────────┐
│   MCP Server    │
│   (FastMCP)     │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
┌───▼───┐ ┌──▼──┐ ┌───▼───┐ ┌──▼──┐
│ Tools │ │Rsrcs│ │Prompts│ │ DBs │
└───────┘ └─────┘ └───────┘ └─────┘
```

### Conceptos Clave

#### 1. Tools (Herramientas)
Funciones que el servidor expone para ser llamadas por clientes.

```python
@mcp.tool()
async def process_data(data: str) -> dict:
    """Procesa datos y retorna resultado"""
    return {"result": data.upper()}
```

#### 2. Resources (Recursos)
Datos o información que el servidor puede proporcionar.

```python
@mcp.resource("config://settings")
async def get_settings() -> str:
    """Retorna configuración del sistema"""
    return json.dumps({"env": "production"})
```

#### 3. Prompts (Plantillas)
Prompts predefinidos que pueden ser utilizados por LLMs.

```python
@mcp.prompt()
async def code_review_prompt(code: str) -> str:
    """Prompt para revisión de código"""
    return f"Review this code:\n{code}"
```

---

## 3. Instalación y Setup

### Instalación de FastMCP

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar FastMCP
pip install fastmcp

# Instalar dependencias adicionales
pip install httpx databases sqlalchemy redis aioredis
pip install anthropic openai  # Para integraciones con IA
```

### Estructura de Proyecto

```
fastmcp-project/
├── servers/
│   ├── __init__.py
│   ├── database_server.py
│   ├── api_server.py
│   ├── ai_server.py
│   └── notification_server.py
├── clients/
│   ├── __init__.py
│   └── mcp_client.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── tests/
│   └── test_servers.py
├── requirements.txt
└── README.md
```

### requirements.txt

```txt
fastmcp>=0.2.0
httpx>=0.24.0
databases>=0.7.0
sqlalchemy>=2.0.0
aioredis>=2.0.0
redis>=4.5.0
anthropic>=0.18.0
openai>=1.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
asyncpg>=0.28.0
pymongo>=4.3.0
motor>=3.1.0
```

---

## 4. Fundamentos de FastMCP

### Servidor Básico

```python
# servers/basic_server.py
from fastmcp import FastMCP
from typing import Dict, Any
import asyncio

# Crear instancia de FastMCP
mcp = FastMCP("Basic Server")

@mcp.tool()
async def greet(name: str) -> str:
    """Saluda a una persona por nombre"""
    return f"Hello, {name}!"

@mcp.tool()
async def calculate(operation: str, a: float, b: float) -> float:
    """Realiza operaciones matemáticas básicas"""
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else 0
    }
    return operations.get(operation, 0)

@mcp.resource("server://info")
async def server_info() -> str:
    """Información del servidor"""
    return """
    Server: Basic MCP Server
    Version: 1.0.0
    Tools: greet, calculate
    """

if __name__ == "__main__":
    mcp.run()
```

### Cliente Básico

```python
# clients/basic_client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Configurar parámetros del servidor
    server_params = StdioServerParameters(
        command="python",
        args=["servers/basic_server.py"],
    )

    # Conectar al servidor
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Inicializar sesión
            await session.initialize()

            # Listar herramientas disponibles
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])

            # Llamar herramienta
            result = await session.call_tool(
                "greet",
                arguments={"name": "FastMCP"}
            )
            print("Result:", result.content[0].text)

            # Llamar otra herramienta
            calc_result = await session.call_tool(
                "calculate",
                arguments={
                    "operation": "add",
                    "a": 10,
                    "b": 5
                }
            )
            print("Calculation:", calc_result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. Servidores MCP para Diferentes Casos de Uso

### 5.1 Servidor de Base de Datos

```python
# servers/database_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import asyncpg
import json
from datetime import datetime

mcp = FastMCP("Database Management Server")

# Pool de conexiones
db_pool = None

async def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            host="localhost",
            port=5432,
            database="mydb",
            user="postgres",
            password="password",
            min_size=5,
            max_size=20
        )
    return db_pool

@mcp.tool()
async def query_users(
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Consulta usuarios con filtros opcionales

    Args:
        filters: Diccionario de filtros (ej: {"status": "active"})
        limit: Número máximo de resultados
    """
    pool = await get_db_pool()

    query = "SELECT id, name, email, status, created_at FROM users WHERE 1=1"
    params = []

    if filters:
        for i, (key, value) in enumerate(filters.items(), start=1):
            query += f" AND {key} = ${i}"
            params.append(value)

    query += f" LIMIT ${len(params) + 1}"
    params.append(limit)

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "status": row["status"],
            "created_at": row["created_at"].isoformat()
        }
        for row in rows
    ]

@mcp.tool()
async def create_user(
    name: str,
    email: str,
    role: str = "user"
) -> Dict[str, Any]:
    """
    Crea un nuevo usuario en la base de datos

    Args:
        name: Nombre del usuario
        email: Email del usuario
        role: Rol del usuario (default: "user")
    """
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO users (name, email, role, status, created_at)
            VALUES ($1, $2, $3, 'active', NOW())
            RETURNING id, name, email, role, status, created_at
            """,
            name, email, role
        )

    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "role": row["role"],
        "status": row["status"],
        "created_at": row["created_at"].isoformat()
    }

@mcp.tool()
async def update_user(
    user_id: int,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Actualiza un usuario existente

    Args:
        user_id: ID del usuario a actualizar
        updates: Diccionario con los campos a actualizar
    """
    pool = await get_db_pool()

    # Construir query dinámicamente
    set_clauses = []
    params = []
    for i, (key, value) in enumerate(updates.items(), start=1):
        set_clauses.append(f"{key} = ${i}")
        params.append(value)

    params.append(user_id)
    query = f"""
        UPDATE users
        SET {", ".join(set_clauses)}, updated_at = NOW()
        WHERE id = ${len(params)}
        RETURNING id, name, email, role, status, updated_at
    """

    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, *params)

    if not row:
        return {"error": "User not found"}

    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "role": row["role"],
        "status": row["status"],
        "updated_at": row["updated_at"].isoformat()
    }

@mcp.tool()
async def delete_user(user_id: int) -> Dict[str, Any]:
    """
    Elimina (soft delete) un usuario

    Args:
        user_id: ID del usuario a eliminar
    """
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE users
            SET status = 'deleted', deleted_at = NOW()
            WHERE id = $1
            RETURNING id, name, email
            """,
            user_id
        )

    if not row:
        return {"error": "User not found"}

    return {
        "success": True,
        "user_id": row["id"],
        "message": f"User {row['name']} deleted successfully"
    }

@mcp.tool()
async def execute_query(
    query: str,
    params: Optional[List[Any]] = None
) -> List[Dict[str, Any]]:
    """
    Ejecuta una query SQL personalizada (solo SELECT)

    Args:
        query: Query SQL a ejecutar
        params: Parámetros para la query
    """
    # Validar que solo sea SELECT
    if not query.strip().upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed"}

    pool = await get_db_pool()
    params = params or []

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    return [dict(row) for row in rows]

@mcp.resource("database://stats")
async def database_stats() -> str:
    """Estadísticas de la base de datos"""
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        total_users = await conn.fetchval("SELECT COUNT(*) FROM users")
        active_users = await conn.fetchval(
            "SELECT COUNT(*) FROM users WHERE status = 'active'"
        )

    stats = {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "timestamp": datetime.now().isoformat()
    }

    return json.dumps(stats, indent=2)

if __name__ == "__main__":
    mcp.run()
```

### 5.2 Servidor de API Gateway

```python
# servers/api_gateway_server.py
from fastmcp import FastMCP
from typing import Dict, Any, Optional, List
import httpx
import json
from datetime import datetime

mcp = FastMCP("API Gateway Server")

# Cliente HTTP compartido
http_client: Optional[httpx.AsyncClient] = None

async def get_http_client() -> httpx.AsyncClient:
    global http_client
    if http_client is None:
        http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_connections=100)
        )
    return http_client

@mcp.tool()
async def call_external_api(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Llama a una API externa

    Args:
        url: URL del endpoint
        method: Método HTTP (GET, POST, PUT, DELETE)
        headers: Headers HTTP opcionales
        body: Cuerpo de la petición (para POST/PUT)
        params: Query parameters
    """
    client = await get_http_client()

    try:
        response = await client.request(
            method=method.upper(),
            url=url,
            headers=headers or {},
            json=body,
            params=params
        )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
            "success": 200 <= response.status_code < 300
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

@mcp.tool()
async def aggregate_apis(
    endpoints: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Agrega respuestas de múltiples APIs en paralelo

    Args:
        endpoints: Lista de configuraciones de endpoints
                  Ejemplo: [{"name": "users", "url": "https://api.com/users"}]
    """
    client = await get_http_client()
    results = {}

    async def fetch_endpoint(config: Dict[str, Any]):
        name = config.get("name", "unnamed")
        url = config.get("url")
        method = config.get("method", "GET")

        try:
            response = await client.request(method, url)
            results[name] = {
                "data": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                "status": response.status_code,
                "success": True
            }
        except Exception as e:
            results[name] = {
                "error": str(e),
                "success": False
            }

    # Ejecutar todas las peticiones en paralelo
    import asyncio
    await asyncio.gather(*[fetch_endpoint(ep) for ep in endpoints])

    return results

@mcp.tool()
async def proxy_request(
    service_name: str,
    path: str,
    method: str = "GET",
    body: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Proxy para servicios internos

    Args:
        service_name: Nombre del servicio (ej: "users-api", "orders-api")
        path: Path del endpoint
        method: Método HTTP
        body: Cuerpo de la petición
    """
    # Mapa de servicios (en producción vendría de un service discovery)
    services = {
        "users-api": "http://localhost:3001",
        "orders-api": "http://localhost:3002",
        "products-api": "http://localhost:3003",
        "payments-api": "http://localhost:3004"
    }

    base_url = services.get(service_name)
    if not base_url:
        return {"error": f"Service {service_name} not found"}

    url = f"{base_url}{path}"

    return await call_external_api(
        url=url,
        method=method,
        body=body
    )

@mcp.tool()
async def batch_requests(
    requests: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Ejecuta múltiples requests en batch

    Args:
        requests: Lista de configuraciones de request
    """
    client = await get_http_client()
    results = []

    async def execute_request(req: Dict[str, Any], index: int):
        try:
            response = await client.request(
                method=req.get("method", "GET"),
                url=req["url"],
                json=req.get("body"),
                headers=req.get("headers"),
                params=req.get("params")
            )

            results.append({
                "index": index,
                "status": response.status_code,
                "data": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                "success": True
            })
        except Exception as e:
            results.append({
                "index": index,
                "error": str(e),
                "success": False
            })

    import asyncio
    await asyncio.gather(*[
        execute_request(req, i)
        for i, req in enumerate(requests)
    ])

    # Ordenar por índice
    results.sort(key=lambda x: x["index"])
    return results

@mcp.resource("gateway://services")
async def list_services() -> str:
    """Lista de servicios disponibles"""
    services = {
        "users-api": {
            "url": "http://localhost:3001",
            "status": "active",
            "version": "1.0.0"
        },
        "orders-api": {
            "url": "http://localhost:3002",
            "status": "active",
            "version": "1.2.0"
        },
        "products-api": {
            "url": "http://localhost:3003",
            "status": "active",
            "version": "2.0.0"
        }
    }

    return json.dumps(services, indent=2)

if __name__ == "__main__":
    mcp.run()
```

### 5.3 Servidor de IA y Procesamiento

```python
# servers/ai_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from anthropic import Anthropic
import json

mcp = FastMCP("AI Processing Server")

# Cliente de Anthropic
anthropic_client = Anthropic()

@mcp.tool()
async def analyze_sentiment(
    text: str,
    language: str = "en"
) -> Dict[str, Any]:
    """
    Analiza el sentimiento de un texto usando Claude

    Args:
        text: Texto a analizar
        language: Idioma del texto
    """
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Analyze the sentiment of the following text and respond in JSON format:

            Text: {text}

            Respond with:
            {{
                "sentiment": "positive|negative|neutral",
                "confidence": 0.0-1.0,
                "emotions": ["emotion1", "emotion2"],
                "summary": "brief summary"
            }}"""
        }]
    )

    response_text = message.content[0].text

    try:
        # Intentar parsear JSON de la respuesta
        result = json.loads(response_text)
    except:
        # Si no es JSON válido, retornar como texto
        result = {"raw_response": response_text}

    result["tokens_used"] = message.usage.input_tokens + message.usage.output_tokens
    result["model"] = message.model

    return result

@mcp.tool()
async def summarize_text(
    text: str,
    max_length: int = 200,
    style: str = "concise"
) -> Dict[str, Any]:
    """
    Resume un texto usando Claude

    Args:
        text: Texto a resumir
        max_length: Longitud máxima del resumen en palabras
        style: Estilo del resumen (concise, detailed, bullet-points)
    """
    style_prompts = {
        "concise": "Create a very concise summary",
        "detailed": "Create a detailed summary maintaining key points",
        "bullet-points": "Create a bullet-point summary with key points"
    }

    prompt = style_prompts.get(style, style_prompts["concise"])

    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""{prompt} in approximately {max_length} words:

            {text}

            Return only the summary without any preamble."""
        }]
    )

    return {
        "summary": message.content[0].text,
        "original_length": len(text.split()),
        "summary_length": len(message.content[0].text.split()),
        "tokens_used": message.usage.input_tokens + message.usage.output_tokens
    }

@mcp.tool()
async def extract_entities(
    text: str,
    entity_types: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Extrae entidades nombradas del texto

    Args:
        text: Texto del que extraer entidades
        entity_types: Tipos de entidades a extraer (person, organization, location, date, etc.)
    """
    entity_types = entity_types or ["person", "organization", "location", "date", "money", "product"]

    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""Extract named entities from the following text. Focus on: {", ".join(entity_types)}

            Text: {text}

            Respond in JSON format:
            {{
                "entities": [
                    {{"type": "entity_type", "value": "entity_value", "context": "surrounding context"}}
                ]
            }}"""
        }]
    )

    try:
        result = json.loads(message.content[0].text)
    except:
        result = {"raw_response": message.content[0].text}

    return result

@mcp.tool()
async def classify_text(
    text: str,
    categories: List[str]
) -> Dict[str, Any]:
    """
    Clasifica texto en categorías predefinidas

    Args:
        text: Texto a clasificar
        categories: Lista de categorías posibles
    """
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Classify the following text into one or more of these categories: {", ".join(categories)}

            Text: {text}

            Respond in JSON format:
            {{
                "primary_category": "category_name",
                "confidence": 0.0-1.0,
                "all_categories": [
                    {{"category": "name", "confidence": 0.0-1.0}}
                ],
                "reasoning": "brief explanation"
            }}"""
        }]
    )

    try:
        result = json.loads(message.content[0].text)
    except:
        result = {"raw_response": message.content[0].text}

    return result

@mcp.tool()
async def generate_content(
    prompt: str,
    content_type: str = "article",
    tone: str = "professional",
    max_tokens: int = 2000
) -> Dict[str, Any]:
    """
    Genera contenido usando Claude

    Args:
        prompt: Descripción del contenido a generar
        content_type: Tipo de contenido (article, email, social-post, etc.)
        tone: Tono del contenido (professional, casual, formal, friendly)
        max_tokens: Tokens máximos para la respuesta
    """
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,
        messages=[{
            "role": "user",
            "content": f"""Generate a {content_type} with a {tone} tone based on:

            {prompt}

            Make it engaging and well-structured."""
        }]
    )

    return {
        "content": message.content[0].text,
        "content_type": content_type,
        "tone": tone,
        "word_count": len(message.content[0].text.split()),
        "tokens_used": message.usage.input_tokens + message.usage.output_tokens
    }

@mcp.tool()
async def translate_text(
    text: str,
    source_language: str,
    target_language: str
) -> Dict[str, Any]:
    """
    Traduce texto entre idiomas

    Args:
        text: Texto a traducir
        source_language: Idioma origen
        target_language: Idioma destino
    """
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""Translate the following text from {source_language} to {target_language}:

            {text}

            Provide only the translation without any explanations."""
        }]
    )

    return {
        "original": text,
        "translation": message.content[0].text,
        "source_language": source_language,
        "target_language": target_language,
        "tokens_used": message.usage.input_tokens + message.usage.output_tokens
    }

@mcp.resource("ai://capabilities")
async def ai_capabilities() -> str:
    """Capacidades disponibles del servidor de IA"""
    capabilities = {
        "sentiment_analysis": "Analyze sentiment and emotions in text",
        "text_summarization": "Generate summaries in multiple styles",
        "entity_extraction": "Extract named entities from text",
        "text_classification": "Classify text into categories",
        "content_generation": "Generate various types of content",
        "translation": "Translate text between languages",
        "model": "claude-3-5-sonnet-20241022"
    }

    return json.dumps(capabilities, indent=2)

if __name__ == "__main__":
    mcp.run()
```

### 5.4 Servidor de Notificaciones

```python
# servers/notification_server.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import httpx
import json
from datetime import datetime

mcp = FastMCP("Notification Server")

@mcp.tool()
async def send_slack_notification(
    webhook_url: str,
    message: str,
    channel: Optional[str] = None,
    username: str = "Notification Bot",
    emoji: str = ":bell:"
) -> Dict[str, Any]:
    """
    Envía notificación a Slack

    Args:
        webhook_url: URL del webhook de Slack
        message: Mensaje a enviar
        channel: Canal (opcional, usa el del webhook por defecto)
        username: Nombre del bot
        emoji: Emoji del bot
    """
    payload = {
        "text": message,
        "username": username,
        "icon_emoji": emoji
    }

    if channel:
        payload["channel"] = channel

    async with httpx.AsyncClient() as client:
        response = await client.post(webhook_url, json=payload)

    return {
        "success": response.status_code == 200,
        "status_code": response.status_code,
        "message": "Notification sent successfully" if response.status_code == 200 else "Failed to send notification"
    }

@mcp.tool()
async def send_discord_notification(
    webhook_url: str,
    title: str,
    description: str,
    color: int = 5814783,
    fields: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Envía notificación a Discord con embed

    Args:
        webhook_url: URL del webhook de Discord
        title: Título del embed
        description: Descripción
        color: Color del embed (decimal)
        fields: Campos adicionales
    """
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": datetime.utcnow().isoformat(),
        "fields": fields or []
    }

    payload = {
        "embeds": [embed]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(webhook_url, json=payload)

    return {
        "success": response.status_code == 204,
        "status_code": response.status_code
    }

@mcp.tool()
async def send_email(
    to: str,
    subject: str,
    body: str,
    from_email: str = "noreply@example.com",
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Envía email (requiere configuración de SMTP)

    Args:
        to: Destinatario
        subject: Asunto
        body: Cuerpo del email
        from_email: Email remitente
        cc: Lista de CC
        bcc: Lista de BCC
    """
    # En producción, usar un servicio real como SendGrid
    email_data = {
        "to": to,
        "from": from_email,
        "subject": subject,
        "body": body,
        "cc": cc or [],
        "bcc": bcc or [],
        "sent_at": datetime.now().isoformat()
    }

    # Simular envío
    return {
        "success": True,
        "email_id": f"email-{datetime.now().timestamp()}",
        "message": "Email queued for sending"
    }

@mcp.tool()
async def send_telegram_message(
    bot_token: str,
    chat_id: str,
    message: str,
    parse_mode: str = "Markdown"
) -> Dict[str, Any]:
    """
    Envía mensaje a Telegram

    Args:
        bot_token: Token del bot de Telegram
        chat_id: ID del chat
        message: Mensaje a enviar
        parse_mode: Modo de parseo (Markdown, HTML)
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    return {
        "success": response.status_code == 200,
        "response": response.json() if response.status_code == 200 else None
    }

@mcp.tool()
async def broadcast_notification(
    message: str,
    channels: List[str],
    configs: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Envía notificación a múltiples canales

    Args:
        message: Mensaje a enviar
        channels: Lista de canales (slack, discord, telegram, email)
        configs: Configuraciones por canal
    """
    results = {}

    for channel in channels:
        config = configs.get(channel, {})

        try:
            if channel == "slack" and "webhook_url" in config:
                result = await send_slack_notification(
                    webhook_url=config["webhook_url"],
                    message=message
                )
                results[channel] = result

            elif channel == "discord" and "webhook_url" in config:
                result = await send_discord_notification(
                    webhook_url=config["webhook_url"],
                    title=config.get("title", "Notification"),
                    description=message
                )
                results[channel] = result

            elif channel == "telegram" and "bot_token" in config and "chat_id" in config:
                result = await send_telegram_message(
                    bot_token=config["bot_token"],
                    chat_id=config["chat_id"],
                    message=message
                )
                results[channel] = result

            else:
                results[channel] = {"success": False, "error": "Missing configuration"}

        except Exception as e:
            results[channel] = {"success": False, "error": str(e)}

    return {
        "message": message,
        "channels": channels,
        "results": results,
        "successful": sum(1 for r in results.values() if r.get("success", False)),
        "failed": sum(1 for r in results.values() if not r.get("success", False))
    }

@mcp.resource("notifications://templates")
async def notification_templates() -> str:
    """Plantillas de notificaciones predefinidas"""
    templates = {
        "error_alert": {
            "title": "🚨 Error Alert",
            "template": "Error in {service}: {error_message}\nTimestamp: {timestamp}"
        },
        "success_notification": {
            "title": "✅ Success",
            "template": "Operation completed successfully: {operation}\nDetails: {details}"
        },
        "warning": {
            "title": "⚠️ Warning",
            "template": "Warning detected in {component}: {message}"
        },
        "info": {
            "title": "ℹ️ Information",
            "template": "Info: {message}"
        }
    }

    return json.dumps(templates, indent=2)

if __name__ == "__main__":
    mcp.run()
```

---

## 6. Integración FastMCP con n8n

### 6.1 Wrapper HTTP para FastMCP

Para integrar FastMCP con n8n, necesitamos un wrapper HTTP:

```python
# servers/http_wrapper.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

app = FastAPI(title="FastMCP HTTP Wrapper")

# Caché de sesiones MCP
mcp_sessions = {}

class MCPToolCall(BaseModel):
    server: str
    tool: str
    arguments: Dict[str, Any]

class MCPResourceRequest(BaseModel):
    server: str
    resource_uri: str

# Configuración de servidores MCP
MCP_SERVERS = {
    "database": {
        "command": "python",
        "args": ["servers/database_server.py"]
    },
    "api_gateway": {
        "command": "python",
        "args": ["servers/api_gateway_server.py"]
    },
    "ai": {
        "command": "python",
        "args": ["servers/ai_server.py"]
    },
    "notifications": {
        "command": "python",
        "args": ["servers/notification_server.py"]
    }
}

async def get_mcp_session(server_name: str):
    """Obtiene o crea una sesión MCP"""
    if server_name not in MCP_SERVERS:
        raise HTTPException(status_code=404, detail=f"Server {server_name} not found")

    if server_name not in mcp_sessions:
        config = MCP_SERVERS[server_name]
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"]
        )

        # Crear nueva sesión
        read, write = await stdio_client(server_params).__aenter__()
        session = await ClientSession(read, write).__aenter__()
        await session.initialize()

        mcp_sessions[server_name] = session

    return mcp_sessions[server_name]

@app.post("/mcp/tool")
async def call_mcp_tool(request: MCPToolCall):
    """
    Llama a una herramienta MCP
    """
    try:
        session = await get_mcp_session(request.server)

        result = await session.call_tool(
            request.tool,
            arguments=request.arguments
        )

        # Extraer texto de la respuesta
        if result.content:
            response_data = result.content[0].text

            # Intentar parsear como JSON
            try:
                import json
                response_data = json.loads(response_data)
            except:
                pass

            return {
                "success": True,
                "server": request.server,
                "tool": request.tool,
                "result": response_data
            }

        return {
            "success": False,
            "error": "No content in response"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/resource")
async def get_mcp_resource(request: MCPResourceRequest):
    """
    Obtiene un recurso MCP
    """
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
    return {
        "servers": list(MCP_SERVERS.keys()),
        "total": len(MCP_SERVERS)
    }

@app.get("/mcp/tools/{server_name}")
async def list_tools(server_name: str):
    """Lista herramientas disponibles en un servidor"""
    try:
        session = await get_mcp_session(server_name)
        tools = await session.list_tools()

        return {
            "server": server_name,
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
        "servers": list(MCP_SERVERS.keys()),
        "active_sessions": list(mcp_sessions.keys())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 6.2 Workflows n8n para FastMCP

#### Workflow 1: Gestión de Usuarios con Database Server

```json
{
  "name": "User Management via FastMCP",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "users/manage",
        "responseMode": "responseNode"
      },
      "id": "webhook-user",
      "name": "User Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 400]
    },
    {
      "parameters": {
        "functionCode": "const action = $input.item.json.body.action;\nconst userData = $input.item.json.body.data;\n\nlet mcpRequest = {\n  server: 'database',\n  arguments: {}\n};\n\nswitch(action) {\n  case 'create':\n    mcpRequest.tool = 'create_user';\n    mcpRequest.arguments = {\n      name: userData.name,\n      email: userData.email,\n      role: userData.role || 'user'\n    };\n    break;\n    \n  case 'update':\n    mcpRequest.tool = 'update_user';\n    mcpRequest.arguments = {\n      user_id: userData.user_id,\n      updates: userData.updates\n    };\n    break;\n    \n  case 'delete':\n    mcpRequest.tool = 'delete_user';\n    mcpRequest.arguments = {\n      user_id: userData.user_id\n    };\n    break;\n    \n  case 'query':\n    mcpRequest.tool = 'query_users';\n    mcpRequest.arguments = {\n      filters: userData.filters || {},\n      limit: userData.limit || 10\n    };\n    break;\n    \n  default:\n    throw new Error('Invalid action');\n}\n\nreturn { json: mcpRequest };"
      },
      "id": "code-prepare-mcp",
      "name": "Prepare MCP Request",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 400]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify($json) }}",
        "options": {}
      },
      "id": "http-call-mcp",
      "name": "Call FastMCP",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [650, 400]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}",
        "options": {}
      },
      "id": "respond-result",
      "name": "Respond Result",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [850, 400]
    }
  ],
  "connections": {
    "User Webhook": {
      "main": [[{"node": "Prepare MCP Request", "type": "main", "index": 0}]]
    },
    "Prepare MCP Request": {
      "main": [[{"node": "Call FastMCP", "type": "main", "index": 0}]]
    },
    "Call FastMCP": {
      "main": [[{"node": "Respond Result", "type": "main", "index": 0}]]
    }
  },
  "active": true
}
```

#### Workflow 2: Análisis de Contenido con IA

```json
{
  "name": "AI Content Analysis Pipeline",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "content/analyze",
        "responseMode": "responseNode"
      },
      "id": "webhook-content",
      "name": "Content Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 500]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'ai',\n  tool: 'analyze_sentiment',\n  arguments: {\n    text: $json.body.text,\n    language: $json.body.language || 'en'\n  }\n}) }}",
        "options": {}
      },
      "id": "http-sentiment",
      "name": "Analyze Sentiment",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 400]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'ai',\n  tool: 'extract_entities',\n  arguments: {\n    text: $('Content Webhook').item.json.body.text\n  }\n}) }}",
        "options": {}
      },
      "id": "http-entities",
      "name": "Extract Entities",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 600]
    },
    {
      "parameters": {
        "functionCode": "const sentiment = $('Analyze Sentiment').item.json.result;\nconst entities = $('Extract Entities').item.json.result;\nconst originalText = $('Content Webhook').item.json.body.text;\n\nreturn {\n  json: {\n    original_text: originalText,\n    analysis: {\n      sentiment: sentiment,\n      entities: entities\n    },\n    analyzed_at: new Date().toISOString()\n  }\n};"
      },
      "id": "code-combine",
      "name": "Combine Results",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [650, 500]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "content_analysis",
        "fields": "original_text, analysis, analyzed_at"
      },
      "id": "mongodb-save",
      "name": "Save to MongoDB",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [850, 500]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $('Combine Results').item.json }}",
        "options": {}
      },
      "id": "respond-analysis",
      "name": "Respond Analysis",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1050, 500]
    }
  ],
  "connections": {
    "Content Webhook": {
      "main": [
        [
          {"node": "Analyze Sentiment", "type": "main", "index": 0},
          {"node": "Extract Entities", "type": "main", "index": 0}
        ]
      ]
    },
    "Analyze Sentiment": {
      "main": [[{"node": "Combine Results", "type": "main", "index": 0}]]
    },
    "Extract Entities": {
      "main": [[{"node": "Combine Results", "type": "main", "index": 0}]]
    },
    "Combine Results": {
      "main": [[{"node": "Save to MongoDB", "type": "main", "index": 0}]]
    },
    "Save to MongoDB": {
      "main": [[{"node": "Respond Analysis", "type": "main", "index": 0}]]
    }
  },
  "active": true
}
```

---

## 7. Proyectos Multi-Servicio Completos

### 7.1 Sistema de E-Commerce Completo

Este es un proyecto que integra todos los servidores MCP:

```python
# servers/ecommerce_orchestrator.py
from fastmcp import FastMCP
from typing import Dict, Any, List
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

mcp = FastMCP("E-Commerce Orchestrator")

# Clientes MCP internos
mcp_clients = {}

async def get_mcp_client(server_name: str):
    """Obtiene cliente MCP para un servidor"""
    if server_name not in mcp_clients:
        servers = {
            "database": ["python", "servers/database_server.py"],
            "ai": ["python", "servers/ai_server.py"],
            "notifications": ["python", "servers/notification_server.py"],
            "api_gateway": ["python", "servers/api_gateway_server.py"]
        }

        if server_name in servers:
            params = StdioServerParameters(
                command=servers[server_name][0],
                args=servers[server_name][1:]
            )

            read, write = await stdio_client(params).__aenter__()
            session = await ClientSession(read, write).__aenter__()
            await session.initialize()

            mcp_clients[server_name] = session

    return mcp_clients[server_name]

@mcp.tool()
async def process_order(
    customer_email: str,
    items: List[Dict[str, Any]],
    payment_method: str
) -> Dict[str, Any]:
    """
    Procesa una orden completa de e-commerce

    Args:
        customer_email: Email del cliente
        items: Lista de items [{product_id, quantity, price}]
        payment_method: Método de pago
    """
    results = {
        "order_id": f"ORD-{int(asyncio.get_event_loop().time() * 1000)}",
        "steps": {}
    }

    try:
        # 1. Buscar o crear usuario
        db_client = await get_mcp_client("database")
        user_result = await db_client.call_tool(
            "query_users",
            arguments={"filters": {"email": customer_email}, "limit": 1}
        )

        user_data = user_result.content[0].text
        results["steps"]["user_lookup"] = {"success": True, "data": user_data}

        # 2. Validar inventario (simulated)
        results["steps"]["inventory_check"] = {"success": True, "items_available": True}

        # 3. Calcular total
        total = sum(item["price"] * item["quantity"] for item in items)
        results["total"] = total
        results["currency"] = "USD"

        # 4. Crear registro de orden en DB
        # (En producción, aquí se haría la creación real)
        results["steps"]["order_created"] = {"success": True, "order_id": results["order_id"]}

        # 5. Analizar sentimiento del mensaje del cliente (si existe)
        ai_client = await get_mcp_client("ai")

        # 6. Enviar notificaciones
        notification_client = await get_mcp_client("notifications")

        # Notificar al cliente
        notif_result = await notification_client.call_tool(
            "send_email",
            arguments={
                "to": customer_email,
                "subject": f"Order Confirmation - {results['order_id']}",
                "body": f"Thank you for your order! Total: ${total}",
                "from_email": "orders@ecommerce.com"
            }
        )

        results["steps"]["notification_sent"] = {"success": True}

        results["success"] = True
        results["message"] = "Order processed successfully"

    except Exception as e:
        results["success"] = False
        results["error"] = str(e)

    return results

@mcp.tool()
async def analyze_customer_feedback(
    feedback_text: str,
    customer_email: str
) -> Dict[str, Any]:
    """
    Analiza feedback del cliente y toma acciones

    Args:
        feedback_text: Texto del feedback
        customer_email: Email del cliente
    """
    results = {}

    # 1. Analizar sentimiento
    ai_client = await get_mcp_client("ai")
    sentiment_result = await ai_client.call_tool(
        "analyze_sentiment",
        arguments={"text": feedback_text}
    )

    import json
    sentiment = json.loads(sentiment_result.content[0].text)
    results["sentiment"] = sentiment

    # 2. Si es negativo, notificar al equipo
    if sentiment.get("sentiment") == "negative":
        notification_client = await get_mcp_client("notifications")

        await notification_client.call_tool(
            "send_slack_notification",
            arguments={
                "webhook_url": "https://hooks.slack.com/...",
                "message": f"Negative feedback from {customer_email}: {feedback_text}",
                "emoji": ":warning:"
            }
        )

        results["action_taken"] = "Support team notified"

    # 3. Guardar en base de datos
    db_client = await get_mcp_client("database")
    # ... guardar feedback

    return results

@mcp.tool()
async def generate_product_description(
    product_name: str,
    features: List[str],
    target_audience: str
) -> Dict[str, Any]:
    """
    Genera descripción de producto con IA

    Args:
        product_name: Nombre del producto
        features: Lista de características
        target_audience: Audiencia objetivo
    """
    ai_client = await get_mcp_client("ai")

    prompt = f"""Create a compelling product description for:
    Product: {product_name}
    Features: {', '.join(features)}
    Target Audience: {target_audience}
    """

    result = await ai_client.call_tool(
        "generate_content",
        arguments={
            "prompt": prompt,
            "content_type": "product_description",
            "tone": "engaging"
        }
    )

    import json
    description_data = json.loads(result.content[0].text)

    return {
        "product_name": product_name,
        "description": description_data["content"],
        "word_count": description_data["word_count"]
    }

if __name__ == "__main__":
    mcp.run()
```

### 7.2 Workflow n8n para E-Commerce Completo

```json
{
  "name": "Complete E-Commerce Flow",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "ecommerce/order",
        "responseMode": "responseNode"
      },
      "id": "webhook-order",
      "name": "Order Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 500]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'ecommerce_orchestrator',\n  tool: 'process_order',\n  arguments: {\n    customer_email: $json.body.customer_email,\n    items: $json.body.items,\n    payment_method: $json.body.payment_method\n  }\n}) }}"
      },
      "id": "http-process-order",
      "name": "Process Order via MCP",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 500]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $json.result.success }}",
              "value2": true
            }
          ]
        }
      },
      "id": "if-success",
      "name": "Order Successful?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [650, 500]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'notifications',\n  tool: 'send_slack_notification',\n  arguments: {\n    webhook_url: 'https://hooks.slack.com/services/...',\n    message: `New order: ${$('Process Order via MCP').item.json.result.order_id} - $${$('Process Order via MCP').item.json.result.total}`,\n    emoji: ':shopping_cart:'\n  }\n}) }}"
      },
      "id": "http-notify-success",
      "name": "Notify Team - Success",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [850, 400]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'notifications',\n  tool: 'send_slack_notification',\n  arguments: {\n    webhook_url: 'https://hooks.slack.com/services/...',\n    message: `Order failed: ${$('Process Order via MCP').item.json.result.error}`,\n    emoji: ':x:'\n  }\n}) }}"
      },
      "id": "http-notify-error",
      "name": "Notify Team - Error",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [850, 600]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $('Process Order via MCP').item.json }}",
        "options": {}
      },
      "id": "respond-final",
      "name": "Respond Result",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1050, 500]
    }
  ],
  "connections": {
    "Order Webhook": {
      "main": [[{"node": "Process Order via MCP", "type": "main", "index": 0}]]
    },
    "Process Order via MCP": {
      "main": [[{"node": "Order Successful?", "type": "main", "index": 0}]]
    },
    "Order Successful?": {
      "main": [
        [{"node": "Notify Team - Success", "type": "main", "index": 0}],
        [{"node": "Notify Team - Error", "type": "main", "index": 0}]
      ]
    },
    "Notify Team - Success": {
      "main": [[{"node": "Respond Result", "type": "main", "index": 0}]]
    },
    "Notify Team - Error": {
      "main": [[{"node": "Respond Result", "type": "main", "index": 0}]]
    }
  },
  "active": true
}
```

---

## 8. Patrones y Mejores Prácticas

### 8.1 Patrón: Circuit Breaker

```python
# patterns/circuit_breaker.py
from fastmcp import FastMCP
from typing import Dict, Any, Callable
import asyncio
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open

    async def call(self, func: Callable, *args, **kwargs):
        if self.state == "open":
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.state = "half_open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            if self.state == "half_open":
                self.state = "closed"
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = datetime.now()

            if self.failures >= self.failure_threshold:
                self.state = "open"

            raise e

mcp = FastMCP("Circuit Breaker Pattern")
circuit_breakers = {}

def get_circuit_breaker(service_name: str) -> CircuitBreaker:
    if service_name not in circuit_breakers:
        circuit_breakers[service_name] = CircuitBreaker()
    return circuit_breakers[service_name]

@mcp.tool()
async def call_with_circuit_breaker(
    service_name: str,
    operation: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """Llama a un servicio con circuit breaker"""
    breaker = get_circuit_breaker(service_name)

    async def call_service():
        # Aquí iría la llamada real al servicio
        return {"result": "success"}

    try:
        result = await breaker.call(call_service)
        return {
            "success": True,
            "circuit_state": breaker.state,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "circuit_state": breaker.state,
            "error": str(e)
        }
```

### 8.2 Patrón: Retry con Backoff

```python
# patterns/retry_backoff.py
from fastmcp import FastMCP
from typing import Dict, Any, Callable
import asyncio

mcp = FastMCP("Retry with Backoff")

async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    *args,
    **kwargs
):
    """Reintenta una función con exponential backoff"""
    for attempt in range(max_retries):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise e

            delay = min(base_delay * (2 ** attempt), max_delay)
            await asyncio.sleep(delay)

@mcp.tool()
async def call_with_retry(
    operation: str,
    arguments: Dict[str, Any],
    max_retries: int = 3
) -> Dict[str, Any]:
    """Ejecuta operación con retry"""
    async def operation_func():
        # Operación a ejecutar
        return {"status": "completed"}

    try:
        result = await retry_with_backoff(
            operation_func,
            max_retries=max_retries
        )
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "retries_exhausted": True
        }
```

### 8.3 Mejores Prácticas

1. **Validación de Entrada**
```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str
    age: int

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Invalid age')
        return v
```

2. **Logging y Observabilidad**
```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
async def monitored_operation(data: str) -> Dict[str, Any]:
    """Operación con logging completo"""
    start_time = datetime.now()

    try:
        logger.info(f"Starting operation with data: {data}")
        result = {"processed": data.upper()}

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Operation completed in {duration}s")

        return result
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}", exc_info=True)
        raise
```

3. **Connection Pooling**
```python
# Usar pools de conexiones para DB
from databases import Database

database = Database("postgresql://user:pass@localhost/db")

async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()
```

---

## 9. Deployment y Producción

### 9.1 Dockerfile para FastMCP

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto (si se usa HTTP wrapper)
EXPOSE 8000

# Comando por defecto
CMD ["python", "servers/http_wrapper.py"]
```

### 9.2 Docker Compose Multi-Servicio

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: dbuser
      POSTGRES_PASSWORD: dbpass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  mcp-http-wrapper:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://dbuser:dbpass@postgres:5432/ecommerce
      - REDIS_URL=redis://redis:6379
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./servers:/app/servers

  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=dbuser
      - DB_POSTGRESDB_PASSWORD=dbpass
      - WEBHOOK_URL=http://localhost:5678/
    depends_on:
      - postgres
      - mcp-http-wrapper
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  postgres_data:
  redis_data:
  n8n_data:
```

### 9.3 Configuración con Variables de Entorno

```python
# config/settings.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    db_pool_size: int = 10

    # Redis
    redis_url: str

    # API Keys
    anthropic_api_key: str
    openai_api_key: Optional[str] = None

    # MCP Settings
    mcp_timeout: int = 30
    mcp_max_retries: int = 3

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 9.4 Systemd Service

```ini
# /etc/systemd/system/fastmcp-wrapper.service
[Unit]
Description=FastMCP HTTP Wrapper
After=network.target postgresql.service

[Service]
Type=simple
User=fastmcp
WorkingDirectory=/opt/fastmcp
Environment="PATH=/opt/fastmcp/venv/bin"
ExecStart=/opt/fastmcp/venv/bin/python servers/http_wrapper.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 9.5 Nginx como Reverse Proxy

```nginx
# /etc/nginx/sites-available/fastmcp
upstream fastmcp {
    server localhost:8000;
}

server {
    listen 80;
    server_name mcp.example.com;

    location / {
        proxy_pass http://fastmcp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts para operaciones largas
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

---

## 10. Integración con MCPs Populares del Ecosistema

### 10.1 ¿Qué son los MCPs del Ecosistema?

El ecosistema MCP cuenta con servidores pre-construidos y mantenidos por la comunidad que proveen funcionalidad común. Podemos integrarlos con nuestros servidores FastMCP para crear soluciones más completas.

**MCPs Oficiales de Anthropic:**
- `@modelcontextprotocol/server-filesystem` - Operaciones con archivos
- `@modelcontextprotocol/server-postgres` - Conexión PostgreSQL
- `@modelcontextprotocol/server-sqlite` - Conexión SQLite
- `@modelcontextprotocol/server-brave-search` - Búsquedas web
- `@modelcontextprotocol/server-puppeteer` - Web automation
- `@modelcontextprotocol/server-slack` - Integración Slack
- `@modelcontextprotocol/server-github` - Operaciones GitHub
- `@modelcontextprotocol/server-google-drive` - Google Drive
- `@modelcontextprotocol/server-memory` - Memoria persistente

### 10.2 Servidor Orquestador de MCPs

Creemos un servidor FastMCP que orquesta y consume otros MCPs:

```python
# servers/mcp_orchestrator.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import subprocess
import json

mcp = FastMCP("MCP Orchestrator")

# Cache de sesiones MCP
mcp_clients: Dict[str, ClientSession] = {}

# Configuración de MCPs externos
EXTERNAL_MCPS = {
    "filesystem": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/Users/workspace"
        ]
    },
    "brave_search": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-brave-search"
        ],
        "env": {
            "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY"
        }
    },
    "postgres": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-postgres",
            "postgresql://user:pass@localhost/db"
        ]
    },
    "github": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-github"
        ],
        "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN"
        }
    },
    "memory": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-memory"
        ]
    },
    "puppeteer": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-puppeteer"
        ]
    }
}

async def get_mcp_client(server_name: str) -> ClientSession:
    """Obtiene o crea un cliente MCP externo"""
    if server_name not in mcp_clients:
        if server_name not in EXTERNAL_MCPS:
            raise ValueError(f"Unknown MCP server: {server_name}")

        config = EXTERNAL_MCPS[server_name]
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=config.get("env", {})
        )

        read, write = await stdio_client(server_params).__aenter__()
        session = await ClientSession(read, write).__aenter__()
        await session.initialize()

        mcp_clients[server_name] = session

    return mcp_clients[server_name]

@mcp.tool()
async def search_web(
    query: str,
    max_results: int = 5
) -> Dict[str, Any]:
    """
    Busca en la web usando Brave Search MCP

    Args:
        query: Consulta de búsqueda
        max_results: Número máximo de resultados
    """
    try:
        client = await get_mcp_client("brave_search")

        result = await client.call_tool(
            "brave_web_search",
            arguments={
                "query": query,
                "count": max_results
            }
        )

        return {
            "success": True,
            "query": query,
            "results": json.loads(result.content[0].text) if result.content else []
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def read_workspace_file(
    file_path: str
) -> Dict[str, Any]:
    """
    Lee un archivo del workspace usando Filesystem MCP

    Args:
        file_path: Ruta del archivo relativa al workspace
    """
    try:
        client = await get_mcp_client("filesystem")

        result = await client.call_tool(
            "read_file",
            arguments={"path": file_path}
        )

        return {
            "success": True,
            "path": file_path,
            "content": result.content[0].text if result.content else ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def write_workspace_file(
    file_path: str,
    content: str
) -> Dict[str, Any]:
    """
    Escribe un archivo en el workspace usando Filesystem MCP

    Args:
        file_path: Ruta del archivo
        content: Contenido a escribir
    """
    try:
        client = await get_mcp_client("filesystem")

        result = await client.call_tool(
            "write_file",
            arguments={
                "path": file_path,
                "content": content
            }
        )

        return {
            "success": True,
            "path": file_path,
            "message": "File written successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def query_database(
    sql: str
) -> Dict[str, Any]:
    """
    Ejecuta una query SQL usando Postgres MCP

    Args:
        sql: Query SQL a ejecutar
    """
    try:
        client = await get_mcp_client("postgres")

        result = await client.call_tool(
            "query",
            arguments={"sql": sql}
        )

        data = json.loads(result.content[0].text) if result.content else []

        return {
            "success": True,
            "sql": sql,
            "rows": data,
            "count": len(data) if isinstance(data, list) else 0
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_github_issue(
    repo: str,
    title: str,
    body: str,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Crea un issue en GitHub usando GitHub MCP

    Args:
        repo: Repositorio (formato: owner/repo)
        title: Título del issue
        body: Descripción del issue
        labels: Labels opcionales
    """
    try:
        client = await get_mcp_client("github")

        result = await client.call_tool(
            "create_issue",
            arguments={
                "repo": repo,
                "title": title,
                "body": body,
                "labels": labels or []
            }
        )

        issue_data = json.loads(result.content[0].text) if result.content else {}

        return {
            "success": True,
            "issue_number": issue_data.get("number"),
            "url": issue_data.get("html_url"),
            "title": title
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def scrape_website(
    url: str,
    selector: Optional[str] = None
) -> Dict[str, Any]:
    """
    Extrae contenido de un sitio web usando Puppeteer MCP

    Args:
        url: URL a scrapear
        selector: Selector CSS opcional
    """
    try:
        client = await get_mcp_client("puppeteer")

        # Navegar a la página
        await client.call_tool(
            "puppeteer_navigate",
            arguments={"url": url}
        )

        # Extraer contenido
        if selector:
            result = await client.call_tool(
                "puppeteer_evaluate",
                arguments={
                    "script": f"document.querySelector('{selector}')?.innerText"
                }
            )
        else:
            result = await client.call_tool(
                "puppeteer_screenshot",
                arguments={"fullPage": True}
            )

        return {
            "success": True,
            "url": url,
            "data": result.content[0].text if result.content else ""
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def store_memory(
    key: str,
    value: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Almacena información en memoria usando Memory MCP

    Args:
        key: Clave para la memoria
        value: Valor a almacenar
        metadata: Metadatos opcionales
    """
    try:
        client = await get_mcp_client("memory")

        result = await client.call_tool(
            "store_memory",
            arguments={
                "key": key,
                "value": value,
                "metadata": metadata or {}
            }
        )

        return {
            "success": True,
            "key": key,
            "message": "Memory stored successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def retrieve_memory(
    key: str
) -> Dict[str, Any]:
    """
    Recupera información de memoria usando Memory MCP

    Args:
        key: Clave de la memoria
    """
    try:
        client = await get_mcp_client("memory")

        result = await client.call_tool(
            "retrieve_memory",
            arguments={"key": key}
        )

        memory_data = json.loads(result.content[0].text) if result.content else {}

        return {
            "success": True,
            "key": key,
            "value": memory_data.get("value"),
            "metadata": memory_data.get("metadata", {})
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def orchestrate_research(
    topic: str
) -> Dict[str, Any]:
    """
    Orquesta una investigación completa usando múltiples MCPs

    Args:
        topic: Tema a investigar
    """
    results = {
        "topic": topic,
        "steps": []
    }

    try:
        # 1. Buscar en web
        search_result = await search_web(topic, max_results=3)
        results["steps"].append({
            "step": "web_search",
            "status": "completed",
            "data": search_result
        })

        # 2. Guardar en memoria
        await store_memory(
            f"research_{topic}",
            json.dumps(search_result),
            {"timestamp": "now", "type": "web_search"}
        )
        results["steps"].append({
            "step": "store_memory",
            "status": "completed"
        })

        # 3. Guardar resultados en archivo
        file_content = f"# Research: {topic}\n\n"
        file_content += json.dumps(search_result, indent=2)

        await write_workspace_file(
            f"research/{topic.replace(' ', '_')}.md",
            file_content
        )
        results["steps"].append({
            "step": "save_to_file",
            "status": "completed"
        })

        # 4. Guardar en base de datos
        await query_database(
            f"""
            INSERT INTO research_logs (topic, data, created_at)
            VALUES ('{topic}', '{json.dumps(search_result)}', NOW())
            """
        )
        results["steps"].append({
            "step": "save_to_database",
            "status": "completed"
        })

        results["success"] = True
        results["message"] = f"Research on '{topic}' completed successfully"

    except Exception as e:
        results["success"] = False
        results["error"] = str(e)

    return results

if __name__ == "__main__":
    mcp.run()
```

### 10.3 Configuración de Claude Desktop con MCPs Múltiples

```json
{
  "mcpServers": {
    "custom-orchestrator": {
      "command": "python",
      "args": ["/path/to/servers/mcp_orchestrator.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/workspace"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://user:pass@localhost:5432/mydb"
      ]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

### 10.4 Workflow n8n con MCPs Populares

```json
{
  "name": "Multi-MCP Research Pipeline",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "research/start",
        "responseMode": "responseNode"
      },
      "id": "webhook",
      "name": "Start Research",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 400]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'orchestrator',\n  tool: 'search_web',\n  arguments: {\n    query: $json.body.topic,\n    max_results: 5\n  }\n}) }}"
      },
      "id": "brave-search",
      "name": "Brave Search",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'orchestrator',\n  tool: 'scrape_website',\n  arguments: {\n    url: $('Brave Search').item.json.result.results[0].url,\n    selector: 'article'\n  }\n}) }}"
      },
      "id": "puppeteer-scrape",
      "name": "Scrape Top Result",
      "type": "n8n-nodes-base.httpRequest",
      "position": [650, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'orchestrator',\n  tool: 'write_workspace_file',\n  arguments: {\n    file_path: `research/${$('Start Research').item.json.body.topic}.md`,\n    content: $('Scrape Top Result').item.json.result.data\n  }\n}) }}"
      },
      "id": "save-file",
      "name": "Save to Filesystem",
      "type": "n8n-nodes-base.httpRequest",
      "position": [850, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'orchestrator',\n  tool: 'store_memory',\n  arguments: {\n    key: `research_${$('Start Research').item.json.body.topic}`,\n    value: JSON.stringify($('Scrape Top Result').item.json),\n    metadata: {\n      timestamp: new Date().toISOString(),\n      source: 'n8n-workflow'\n    }\n  }\n}) }}"
      },
      "id": "save-memory",
      "name": "Save to Memory",
      "type": "n8n-nodes-base.httpRequest",
      "position": [850, 450]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'orchestrator',\n  tool: 'query_database',\n  arguments: {\n    sql: `INSERT INTO research (topic, content, created_at) VALUES ('${$('Start Research').item.json.body.topic}', '${JSON.stringify($('Scrape Top Result').item.json)}', NOW())`\n  }\n}) }}"
      },
      "id": "save-db",
      "name": "Save to PostgreSQL",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1050, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/tool",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify({\n  server: 'orchestrator',\n  tool: 'create_github_issue',\n  arguments: {\n    repo: 'myorg/research-tracker',\n    title: `Research completed: ${$('Start Research').item.json.body.topic}`,\n    body: `Research has been completed and saved.\\n\\nTopic: ${$('Start Research').item.json.body.topic}\\n\\nFile: research/${$('Start Research').item.json.body.topic}.md`,\n    labels: ['research', 'automated']\n  }\n}) }}"
      },
      "id": "github-issue",
      "name": "Create GitHub Issue",
      "type": "n8n-nodes-base.httpRequest",
      "position": [1050, 450]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ {\n  success: true,\n  topic: $('Start Research').item.json.body.topic,\n  file: $('Save to Filesystem').item.json.result.path,\n  database_saved: $('Save to PostgreSQL').item.json.success,\n  github_issue: $('Create GitHub Issue').item.json.result.url\n} }}",
        "options": {}
      },
      "id": "respond",
      "name": "Respond",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [1250, 375]
    }
  ],
  "connections": {
    "Start Research": {
      "main": [[{"node": "Brave Search", "type": "main", "index": 0}]]
    },
    "Brave Search": {
      "main": [[{"node": "Scrape Top Result", "type": "main", "index": 0}]]
    },
    "Scrape Top Result": {
      "main": [[
        {"node": "Save to Filesystem", "type": "main", "index": 0},
        {"node": "Save to Memory", "type": "main", "index": 0}
      ]]
    },
    "Save to Filesystem": {
      "main": [[{"node": "Save to PostgreSQL", "type": "main", "index": 0}]]
    },
    "Save to Memory": {
      "main": [[{"node": "Create GitHub Issue", "type": "main", "index": 0}]]
    },
    "Save to PostgreSQL": {
      "main": [[{"node": "Respond", "type": "main", "index": 0}]]
    },
    "Create GitHub Issue": {
      "main": [[{"node": "Respond", "type": "main", "index": 0}]]
    }
  },
  "active": true
}
```

### 10.5 Casos de Uso Avanzados

#### Caso 1: Sistema de Monitoreo con GitHub + Slack

```python
@mcp.tool()
async def monitor_github_and_notify(
    repo: str,
    slack_webhook: str
) -> Dict[str, Any]:
    """
    Monitorea un repo de GitHub y notifica en Slack
    """
    # Obtener issues recientes
    github_client = await get_mcp_client("github")
    issues_result = await github_client.call_tool(
        "list_issues",
        arguments={"repo": repo, "state": "open"}
    )

    issues = json.loads(issues_result.content[0].text)

    # Enviar notificación a Slack
    from app.mcp.servers.notification_server import send_slack_notification

    for issue in issues[:5]:  # Top 5
        await send_slack_notification(
            webhook_url=slack_webhook,
            message=f"🔥 Open Issue: {issue['title']}\n{issue['html_url']}",
            emoji=":warning:"
        )

    return {
        "success": True,
        "issues_notified": len(issues[:5])
    }
```

#### Caso 2: Pipeline de Contenido Automático

```python
@mcp.tool()
async def content_pipeline(
    topic: str,
    output_format: str = "markdown"
) -> Dict[str, Any]:
    """
    Pipeline completo: Buscar -> Scrapear -> Analizar -> Guardar -> Publicar
    """
    # 1. Buscar información
    search_results = await search_web(topic, max_results=3)

    # 2. Scrapear contenido
    scraped_content = []
    for result in search_results.get("results", [])[:2]:
        content = await scrape_website(result["url"])
        scraped_content.append(content)

    # 3. Analizar con IA (usando nuestro AI server)
    from app.mcp.servers.ai_server import summarize_text

    all_content = "\n\n".join([c.get("data", "") for c in scraped_content])
    summary = await summarize_text(
        text=all_content,
        max_length=500,
        style="detailed"
    )

    # 4. Guardar en filesystem
    filename = f"content/{topic.replace(' ', '_')}_{output_format}"
    await write_workspace_file(filename, summary["summary"])

    # 5. Guardar metadata en DB
    await query_database(f"""
        INSERT INTO content_pipeline
        (topic, summary, sources, created_at)
        VALUES (
            '{topic}',
            '{summary["summary"]}',
            '{json.dumps([r["url"] for r in search_results.get("results", [])])}',
            NOW()
        )
    """)

    # 6. Crear issue en GitHub para revisión
    issue = await create_github_issue(
        repo="myorg/content-review",
        title=f"Review: {topic}",
        body=f"New content generated for review:\n\nFile: {filename}\n\nSummary length: {summary['summary_length']} words",
        labels=["content", "needs-review"]
    )

    return {
        "success": True,
        "topic": topic,
        "file": filename,
        "github_issue": issue.get("url"),
        "word_count": summary["summary_length"]
    }
```

### 10.6 Instalación de MCPs del Ecosistema

```bash
# Instalar MCPs oficiales globalmente
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-postgres
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-puppeteer
npm install -g @modelcontextprotocol/server-slack
npm install -g @modelcontextprotocol/server-google-drive
npm install -g @modelcontextprotocol/server-memory

# O usar npx (recomendado para testing)
npx -y @modelcontextprotocol/server-filesystem /workspace
```

### 10.7 Variables de Entorno para MCPs Externos

```bash
# .env
# Brave Search
BRAVE_API_KEY=your_brave_api_key

# GitHub
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token

# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Google Drive
GOOGLE_DRIVE_CREDENTIALS_PATH=/path/to/credentials.json

# Postgres
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
```

### 10.8 Testing de Integraciones MCP

```python
# tests/test_mcp_integrations.py
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def orchestrator_session():
    """Sesión del orquestador MCP"""
    server_params = StdioServerParameters(
        command="python",
        args=["servers/mcp_orchestrator.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

async def test_web_search_integration(orchestrator_session):
    """Test integración con Brave Search"""
    result = await orchestrator_session.call_tool(
        "search_web",
        arguments={
            "query": "FastMCP tutorial",
            "max_results": 3
        }
    )

    assert result.content
    import json
    data = json.loads(result.content[0].text)

    assert data["success"] is True
    assert "results" in data
    assert len(data["results"]) <= 3

async def test_file_operations(orchestrator_session):
    """Test operaciones de archivos"""
    # Escribir
    write_result = await orchestrator_session.call_tool(
        "write_workspace_file",
        arguments={
            "file_path": "test/sample.txt",
            "content": "Hello from test"
        }
    )

    assert write_result.content

    # Leer
    read_result = await orchestrator_session.call_tool(
        "read_workspace_file",
        arguments={"file_path": "test/sample.txt"}
    )

    data = json.loads(read_result.content[0].text)
    assert data["content"] == "Hello from test"

async def test_orchestrate_research(orchestrator_session):
    """Test orquestación completa"""
    result = await orchestrator_session.call_tool(
        "orchestrate_research",
        arguments={"topic": "FastMCP"}
    )

    assert result.content
    data = json.loads(result.content[0].text)

    assert data["success"] is True
    assert len(data["steps"]) >= 3
    assert all(step["status"] == "completed" for step in data["steps"])
```

---

## Conclusión

Este taller cubre:

✅ **Fundamentos de FastMCP**
✅ **4 servidores MCP completos** (Database, API Gateway, IA, Notificaciones)
✅ **Integración completa con n8n** mediante HTTP wrapper
✅ **Proyecto e-commerce multi-servicio real**
✅ **Workflows n8n listos para usar**
✅ **Patrones de diseño** (Circuit Breaker, Retry, etc.)
✅ **Deployment en producción** (Docker, Docker Compose, Systemd, Nginx)
✅ **Mejores prácticas** de código y arquitectura
✅ **Integración con 9+ MCPs populares del ecosistema**
✅ **Servidor orquestador de MCPs externos**
✅ **Workflows multi-MCP avanzados**

**Próximos pasos:**
1. Clonar el repositorio de ejemplo
2. Configurar las variables de entorno
3. Instalar MCPs del ecosistema (`npm install -g @modelcontextprotocol/...`)
4. Levantar los servicios con Docker Compose
5. Importar los workflows de n8n
6. Probar las integraciones con MCPs externos
7. Extender con tus propios servidores MCP
8. Desplegar en producción
