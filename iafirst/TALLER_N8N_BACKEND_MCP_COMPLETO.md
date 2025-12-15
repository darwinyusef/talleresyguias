# Taller Completo: n8n para Integración Backend y MCP con FastMCP

## 📋 Tabla de Contenidos

1. [Introducción a n8n](#introducción-a-n8n)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Fundamentos de Workflows](#fundamentos-de-workflows)
4. [Integración con Backend](#integración-con-backend)
5. [MCP (Model Context Protocol) con FastMCP](#mcp-con-fastmcp)
6. [Ejemplos Prácticos Completos](#ejemplos-prácticos-completos)
7. [Casos de Uso Reales](#casos-de-uso-reales)
8. [Mejores Prácticas](#mejores-prácticas)

---

## 1. Introducción a n8n

n8n es una herramienta de automatización de flujos de trabajo (workflow automation) de código abierto que permite conectar diferentes aplicaciones y servicios sin necesidad de escribir código complejo.

### Características principales:
- **Open Source**: Código abierto y auto-hospedable
- **Visual Workflow Builder**: Constructor visual de flujos
- **400+ integraciones**: APIs, bases de datos, servicios cloud
- **Ejecutable localmente**: Control total de tus datos
- **Extensible**: Puedes crear nodos personalizados

---

## 2. Instalación y Configuración

### Opción 1: Docker (Recomendado)

```bash
# Docker Compose básico
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Opción 2: npm

```bash
npm install n8n -g
n8n start
```

### Opción 3: Docker Compose con PostgreSQL

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: n8n_password
      POSTGRES_DB: n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n_password
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin123
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

volumes:
  postgres_data:
  n8n_data:
```

---

## 3. Fundamentos de Workflows

### Conceptos Básicos

- **Nodo (Node)**: Cada paso en el workflow
- **Conexión (Connection)**: Flujo de datos entre nodos
- **Trigger**: Nodo que inicia el workflow
- **Expresiones**: Código JavaScript para transformar datos

### Ejemplo Básico: Workflow Simple

```json
{
  "name": "Workflow Básico - HTTP Request",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "GET",
        "path": "webhook-test",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "webhook-1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300],
      "webhookId": "test-webhook"
    },
    {
      "parameters": {
        "url": "https://jsonplaceholder.typicode.com/posts/1",
        "options": {}
      },
      "id": "http-request-1",
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}",
        "options": {}
      },
      "id": "respond-webhook-1",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "HTTP Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "HTTP Request": {
      "main": [
        [
          {
            "node": "Respond to Webhook",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {},
  "versionId": "1"
}
```

---

## 4. Integración con Backend

### 4.1 API REST - CRUD Completo

Este workflow demuestra operaciones CRUD con una API REST:

```json
{
  "name": "Backend API - CRUD Operations",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "api/users",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "webhook-api",
      "name": "API Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.body.action }}",
              "operation": "equals",
              "value2": "create"
            }
          ]
        }
      },
      "id": "switch-action",
      "name": "Switch Action",
      "type": "n8n-nodes-base.switch",
      "typeVersion": 1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO users (name, email, role) VALUES ($1, $2, $3) RETURNING *",
        "options": {
          "queryParameters": "={{ JSON.stringify([$json.body.name, $json.body.email, $json.body.role || 'user']) }}"
        }
      },
      "id": "postgres-create",
      "name": "PostgreSQL - Create",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [650, 200],
      "credentials": {
        "postgres": {
          "id": "1",
          "name": "PostgreSQL account"
        }
      }
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM users WHERE id = $1",
        "options": {
          "queryParameters": "={{ JSON.stringify([$json.body.id]) }}"
        }
      },
      "id": "postgres-read",
      "name": "PostgreSQL - Read",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [650, 300],
      "credentials": {
        "postgres": {
          "id": "1",
          "name": "PostgreSQL account"
        }
      }
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "UPDATE users SET name = $1, email = $2 WHERE id = $3 RETURNING *",
        "options": {
          "queryParameters": "={{ JSON.stringify([$json.body.name, $json.body.email, $json.body.id]) }}"
        }
      },
      "id": "postgres-update",
      "name": "PostgreSQL - Update",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [650, 400],
      "credentials": {
        "postgres": {
          "id": "1",
          "name": "PostgreSQL account"
        }
      }
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "DELETE FROM users WHERE id = $1 RETURNING *",
        "options": {
          "queryParameters": "={{ JSON.stringify([$json.body.id]) }}"
        }
      },
      "id": "postgres-delete",
      "name": "PostgreSQL - Delete",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [650, 500],
      "credentials": {
        "postgres": {
          "id": "1",
          "name": "PostgreSQL account"
        }
      }
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { success: true, data: $json, action: $('API Webhook').item.json.body.action } }}",
        "options": {
          "responseHeaders": {
            "entries": [
              {
                "name": "Content-Type",
                "value": "application/json"
              }
            ]
          }
        }
      },
      "id": "respond-success",
      "name": "Respond Success",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [850, 300]
    }
  ],
  "connections": {
    "API Webhook": {
      "main": [
        [
          {
            "node": "Switch Action",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Switch Action": {
      "main": [
        [
          {
            "node": "PostgreSQL - Create",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "PostgreSQL - Read",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "PostgreSQL - Update",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "PostgreSQL - Delete",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "PostgreSQL - Create": {
      "main": [
        [
          {
            "node": "Respond Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "PostgreSQL - Read": {
      "main": [
        [
          {
            "node": "Respond Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "PostgreSQL - Update": {
      "main": [
        [
          {
            "node": "Respond Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "PostgreSQL - Delete": {
      "main": [
        [
          {
            "node": "Respond Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {},
  "versionId": "2"
}
```

### 4.2 Integración con MongoDB

```json
{
  "name": "MongoDB Backend Integration",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "api/products",
        "responseMode": "responseNode"
      },
      "id": "webhook-products",
      "name": "Products Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "products",
        "fields": "name, price, category, stock, description",
        "options": {}
      },
      "id": "mongodb-insert",
      "name": "MongoDB Insert",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [450, 300],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "url": "http://localhost:3000/api/cache/invalidate",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "collection",
              "value": "products"
            },
            {
              "name": "id",
              "value": "={{ $json._id }}"
            }
          ]
        },
        "options": {}
      },
      "id": "http-cache-invalidate",
      "name": "Invalidate Cache",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [650, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { success: true, product: $('MongoDB Insert').item.json, cached: false } }}",
        "options": {}
      },
      "id": "respond-product",
      "name": "Respond Product",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [850, 300]
    }
  ],
  "connections": {
    "Products Webhook": {
      "main": [
        [
          {
            "node": "MongoDB Insert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "MongoDB Insert": {
      "main": [
        [
          {
            "node": "Invalidate Cache",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Invalidate Cache": {
      "main": [
        [
          {
            "node": "Respond Product",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true
}
```

---

## 5. MCP (Model Context Protocol) con FastMCP

### 5.1 ¿Qué es MCP?

MCP (Model Context Protocol) es un protocolo abierto que permite a las aplicaciones proporcionar contexto a los LLMs de manera estandarizada. FastMCP es una implementación rápida de este protocolo.

### 5.2 Instalación de FastMCP

```bash
# Instalar FastMCP
pip install fastmcp

# O con Poetry
poetry add fastmcp
```

### 5.3 Servidor FastMCP Básico

```python
# mcp_server.py
from fastmcp import FastMCP
from typing import Dict, Any
import asyncio

# Crear instancia FastMCP
mcp = FastMCP("Product Management Server")

@mcp.tool()
async def get_product(product_id: str) -> Dict[str, Any]:
    """Obtiene información de un producto por ID"""
    # Simular consulta a base de datos
    return {
        "id": product_id,
        "name": "Laptop Pro",
        "price": 1299.99,
        "stock": 45
    }

@mcp.tool()
async def create_order(
    product_id: str,
    quantity: int,
    customer_email: str
) -> Dict[str, Any]:
    """Crea una nueva orden"""
    return {
        "order_id": "ORD-12345",
        "product_id": product_id,
        "quantity": quantity,
        "customer_email": customer_email,
        "status": "pending",
        "total": 1299.99 * quantity
    }

@mcp.resource("products://inventory")
async def get_inventory() -> str:
    """Obtiene el inventario completo"""
    return """
    Inventario actual:
    - Laptop Pro: 45 unidades
    - Mouse Wireless: 120 unidades
    - Teclado Mecánico: 67 unidades
    """

if __name__ == "__main__":
    mcp.run()
```

### 5.4 Cliente FastMCP

```python
# mcp_client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Listar herramientas disponibles
            tools = await session.list_tools()
            print("Herramientas disponibles:", tools)

            # Llamar a una herramienta
            result = await session.call_tool(
                "get_product",
                arguments={"product_id": "PROD-001"}
            )
            print("Resultado:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 5.5 Integración n8n + FastMCP

```json
{
  "name": "n8n to FastMCP Integration",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "mcp/tool",
        "responseMode": "responseNode"
      },
      "id": "webhook-mcp",
      "name": "MCP Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "functionCode": "const toolName = $input.item.json.body.tool;\nconst args = $input.item.json.body.arguments;\n\nreturn {\n  json: {\n    tool: toolName,\n    arguments: args,\n    timestamp: new Date().toISOString()\n  }\n};"
      },
      "id": "code-prepare",
      "name": "Prepare MCP Call",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/execute",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "tool",
              "value": "={{ $json.tool }}"
            },
            {
              "name": "arguments",
              "value": "={{ $json.arguments }}"
            }
          ]
        },
        "options": {
          "timeout": 30000
        }
      },
      "id": "http-mcp-call",
      "name": "Call FastMCP",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [650, 300]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO mcp_logs (tool, arguments, result, timestamp) VALUES ($1, $2, $3, $4)",
        "options": {
          "queryParameters": "={{ JSON.stringify([$('Prepare MCP Call').item.json.tool, JSON.stringify($('Prepare MCP Call').item.json.arguments), JSON.stringify($json), new Date().toISOString()]) }}"
        }
      },
      "id": "postgres-log",
      "name": "Log to Database",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [850, 300],
      "credentials": {
        "postgres": {
          "id": "1",
          "name": "PostgreSQL account"
        }
      }
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $('Call FastMCP').item.json }}",
        "options": {}
      },
      "id": "respond-mcp",
      "name": "Respond MCP Result",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1050, 300]
    }
  ],
  "connections": {
    "MCP Webhook": {
      "main": [
        [
          {
            "node": "Prepare MCP Call",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Prepare MCP Call": {
      "main": [
        [
          {
            "node": "Call FastMCP",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Call FastMCP": {
      "main": [
        [
          {
            "node": "Log to Database",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Log to Database": {
      "main": [
        [
          {
            "node": "Respond MCP Result",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true
}
```

---

## 6. Ejemplos Prácticos Completos

### 6.1 Sistema de Procesamiento de Pedidos Completo

```json
{
  "name": "Order Processing System - Complete",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "orders/create",
        "responseMode": "responseNode"
      },
      "id": "webhook-order",
      "name": "New Order Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 400]
    },
    {
      "parameters": {
        "functionCode": "const order = $input.item.json.body;\n\n// Validar orden\nif (!order.customer_email || !order.items || order.items.length === 0) {\n  throw new Error('Invalid order data');\n}\n\n// Calcular total\nconst total = order.items.reduce((sum, item) => {\n  return sum + (item.price * item.quantity);\n}, 0);\n\n// Generar ID único\nconst orderId = `ORD-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;\n\nreturn {\n  json: {\n    order_id: orderId,\n    customer_email: order.customer_email,\n    customer_name: order.customer_name,\n    items: order.items,\n    total: total,\n    tax: total * 0.16,\n    grand_total: total * 1.16,\n    status: 'pending',\n    created_at: new Date().toISOString()\n  }\n};"
      },
      "id": "code-process-order",
      "name": "Process Order Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 400]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "orders",
        "fields": "order_id, customer_email, customer_name, items, total, tax, grand_total, status, created_at",
        "options": {}
      },
      "id": "mongodb-save-order",
      "name": "Save to MongoDB",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [650, 400],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "functionCode": "const order = $input.item.json;\n\n// Verificar stock para cada item\nconst stockChecks = order.items.map(item => ({\n  product_id: item.product_id,\n  required_quantity: item.quantity\n}));\n\nreturn stockChecks.map(check => ({ json: check }));"
      },
      "id": "code-check-stock",
      "name": "Prepare Stock Check",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [850, 400]
    },
    {
      "parameters": {
        "operation": "find",
        "collection": "products",
        "query": "={ \"product_id\": \"{{ $json.product_id }}\" }",
        "options": {}
      },
      "id": "mongodb-get-product",
      "name": "Get Product Stock",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [1050, 400],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{ $json.stock }}",
              "operation": "largerEqual",
              "value2": "={{ $('Prepare Stock Check').item.json.required_quantity }}"
            }
          ]
        }
      },
      "id": "if-stock-available",
      "name": "Stock Available?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [1250, 400]
    },
    {
      "parameters": {
        "operation": "update",
        "collection": "products",
        "updateKey": "product_id",
        "fields": "stock",
        "options": {}
      },
      "id": "mongodb-update-stock",
      "name": "Update Stock",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [1450, 300],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "operation": "update",
        "collection": "orders",
        "updateKey": "order_id",
        "fieldsUi": {
          "fieldValues": [
            {
              "fieldName": "status",
              "fieldValue": "confirmed"
            }
          ]
        }
      },
      "id": "mongodb-confirm-order",
      "name": "Confirm Order",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [1650, 300],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "fromEmail": "orders@company.com",
        "toEmail": "={{ $('Process Order Data').item.json.customer_email }}",
        "subject": "Order Confirmation - {{ $('Process Order Data').item.json.order_id }}",
        "emailType": "html",
        "message": "=<h2>Thank you for your order!</h2>\n<p>Order ID: {{ $('Process Order Data').item.json.order_id }}</p>\n<p>Total: ${{ $('Process Order Data').item.json.grand_total }}</p>\n<p>Status: Confirmed</p>",
        "options": {}
      },
      "id": "email-confirmation",
      "name": "Send Confirmation Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [1850, 300],
      "credentials": {
        "smtp": {
          "id": "3",
          "name": "SMTP account"
        }
      }
    },
    {
      "parameters": {
        "operation": "update",
        "collection": "orders",
        "updateKey": "order_id",
        "fieldsUi": {
          "fieldValues": [
            {
              "fieldName": "status",
              "fieldValue": "out_of_stock"
            }
          ]
        }
      },
      "id": "mongodb-mark-out-of-stock",
      "name": "Mark Out of Stock",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [1450, 500],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "url": "http://localhost:3000/api/notifications/slack",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "channel",
              "value": "#inventory-alerts"
            },
            {
              "name": "message",
              "value": "=⚠️ Out of Stock Alert for Order {{ $('Process Order Data').item.json.order_id }}"
            }
          ]
        }
      },
      "id": "http-slack-alert",
      "name": "Slack Alert",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [1650, 500]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ {\n  success: $('Stock Available?').item.json ? true : false,\n  order: $('Process Order Data').item.json,\n  status: $('Stock Available?').item.json ? 'confirmed' : 'out_of_stock'\n} }}",
        "options": {}
      },
      "id": "respond-order-result",
      "name": "Respond Order Result",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [2050, 400]
    }
  ],
  "connections": {
    "New Order Webhook": {
      "main": [
        [
          {
            "node": "Process Order Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Process Order Data": {
      "main": [
        [
          {
            "node": "Save to MongoDB",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Save to MongoDB": {
      "main": [
        [
          {
            "node": "Prepare Stock Check",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Prepare Stock Check": {
      "main": [
        [
          {
            "node": "Get Product Stock",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Product Stock": {
      "main": [
        [
          {
            "node": "Stock Available?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Stock Available?": {
      "main": [
        [
          {
            "node": "Update Stock",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Mark Out of Stock",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Update Stock": {
      "main": [
        [
          {
            "node": "Confirm Order",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Confirm Order": {
      "main": [
        [
          {
            "node": "Send Confirmation Email",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send Confirmation Email": {
      "main": [
        [
          {
            "node": "Respond Order Result",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Mark Out of Stock": {
      "main": [
        [
          {
            "node": "Slack Alert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Slack Alert": {
      "main": [
        [
          {
            "node": "Respond Order Result",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {
    "executionOrder": "v1"
  }
}
```

### 6.2 Sistema de Análisis y Alertas con IA

```json
{
  "name": "AI Analysis and Alerts System",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "minutes",
              "minutesInterval": 15
            }
          ]
        }
      },
      "id": "cron-trigger",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [250, 400]
    },
    {
      "parameters": {
        "operation": "aggregate",
        "collection": "logs",
        "query": "=[\n  {\n    \"$match\": {\n      \"timestamp\": {\n        \"$gte\": { \"$date\": \"{{ $now.minus({minutes: 15}).toISO() }}\" }\n      },\n      \"level\": \"error\"\n    }\n  },\n  {\n    \"$group\": {\n      \"_id\": \"$error_type\",\n      \"count\": { \"$sum\": 1 },\n      \"messages\": { \"$push\": \"$message\" }\n    }\n  },\n  {\n    \"$sort\": { \"count\": -1 }\n  }\n]"
      },
      "id": "mongodb-get-errors",
      "name": "Get Recent Errors",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [450, 400],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{ $json.count }}",
              "operation": "larger",
              "value2": 5
            }
          ]
        }
      },
      "id": "if-threshold-exceeded",
      "name": "Threshold Exceeded?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [650, 400]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/api/ai/analyze",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "error_type",
              "value": "={{ $json._id }}"
            },
            {
              "name": "messages",
              "value": "={{ JSON.stringify($json.messages) }}"
            },
            {
              "name": "count",
              "value": "={{ $json.count }}"
            }
          ]
        },
        "options": {}
      },
      "id": "http-ai-analysis",
      "name": "AI Error Analysis",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [850, 300]
    },
    {
      "parameters": {
        "functionCode": "const analysis = $input.item.json;\nconst error = $('Get Recent Errors').item.json;\n\nreturn {\n  json: {\n    alert: {\n      severity: error.count > 20 ? 'critical' : 'warning',\n      error_type: error._id,\n      count: error.count,\n      ai_summary: analysis.summary,\n      ai_recommendations: analysis.recommendations,\n      timestamp: new Date().toISOString()\n    }\n  }\n};"
      },
      "id": "code-format-alert",
      "name": "Format Alert",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1050, 300]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "alerts",
        "fields": "severity, error_type, count, ai_summary, ai_recommendations, timestamp",
        "options": {}
      },
      "id": "mongodb-save-alert",
      "name": "Save Alert",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [1250, 300],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"blocks\": [\n    {\n      \"type\": \"header\",\n      \"text\": {\n        \"type\": \"plain_text\",\n        \"text\": \"🚨 {{ $json.alert.severity === 'critical' ? 'CRITICAL' : 'WARNING' }} Alert\"\n      }\n    },\n    {\n      \"type\": \"section\",\n      \"fields\": [\n        {\n          \"type\": \"mrkdwn\",\n          \"text\": \"*Error Type:*\\n{{ $json.alert.error_type }}\"\n        },\n        {\n          \"type\": \"mrkdwn\",\n          \"text\": \"*Count:*\\n{{ $json.alert.count }}\"\n        }\n      ]\n    },\n    {\n      \"type\": \"section\",\n      \"text\": {\n        \"type\": \"mrkdwn\",\n        \"text\": \"*AI Summary:*\\n{{ $json.alert.ai_summary }}\"\n      }\n    },\n    {\n      \"type\": \"section\",\n      \"text\": {\n        \"type\": \"mrkdwn\",\n        \"text\": \"*Recommendations:*\\n{{ $json.alert.ai_recommendations }}\"\n      }\n    }\n  ]\n}",
        "options": {}
      },
      "id": "http-slack-webhook",
      "name": "Send Slack Alert",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [1450, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:8000/mcp/execute",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "tool",
              "value": "create_incident"
            },
            {
              "name": "arguments",
              "value": "={{ JSON.stringify({\n  title: `${$json.alert.error_type} - ${$json.alert.count} occurrences`,\n  severity: $json.alert.severity,\n  description: $json.alert.ai_summary,\n  recommendations: $json.alert.ai_recommendations\n}) }}"
            }
          ]
        }
      },
      "id": "http-mcp-incident",
      "name": "Create Incident via MCP",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [1650, 300]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [
        [
          {
            "node": "Get Recent Errors",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Recent Errors": {
      "main": [
        [
          {
            "node": "Threshold Exceeded?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Threshold Exceeded?": {
      "main": [
        [
          {
            "node": "AI Error Analysis",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "AI Error Analysis": {
      "main": [
        [
          {
            "node": "Format Alert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Format Alert": {
      "main": [
        [
          {
            "node": "Save Alert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Save Alert": {
      "main": [
        [
          {
            "node": "Send Slack Alert",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send Slack Alert": {
      "main": [
        [
          {
            "node": "Create Incident via MCP",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true
}
```

---

## 7. Casos de Uso Reales

### 7.1 Sistema de Sincronización Multi-Base de Datos

```json
{
  "name": "Multi-Database Sync System",
  "nodes": [
    {
      "parameters": {
        "triggerOn": "specificFolder",
        "folderToWatch": "/data/imports",
        "event": "file.created"
      },
      "id": "file-trigger",
      "name": "File Created Trigger",
      "type": "n8n-nodes-base.localFileTrigger",
      "typeVersion": 1,
      "position": [250, 400]
    },
    {
      "parameters": {
        "filePath": "={{ $json.path }}",
        "options": {}
      },
      "id": "read-csv",
      "name": "Read CSV File",
      "type": "n8n-nodes-base.readBinaryFile",
      "typeVersion": 1,
      "position": [450, 400]
    },
    {
      "parameters": {
        "mode": "jsonToCsv",
        "options": {
          "delimiter": ","
        }
      },
      "id": "csv-parser",
      "name": "Parse CSV",
      "type": "n8n-nodes-base.convertToFile",
      "typeVersion": 1,
      "position": [650, 400]
    },
    {
      "parameters": {
        "functionCode": "const items = $input.all();\nconst records = [];\n\nfor (const item of items) {\n  const data = item.json;\n  \n  // Transformar y validar datos\n  const record = {\n    external_id: data.id,\n    name: data.name,\n    email: data.email.toLowerCase().trim(),\n    phone: data.phone || null,\n    status: data.status || 'active',\n    metadata: {\n      source: 'csv_import',\n      imported_at: new Date().toISOString(),\n      original_data: data\n    }\n  };\n  \n  // Validar email\n  const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;\n  if (!emailRegex.test(record.email)) {\n    record.status = 'invalid';\n    record.metadata.validation_error = 'Invalid email format';\n  }\n  \n  records.push({ json: record });\n}\n\nreturn records;"
      },
      "id": "code-transform",
      "name": "Transform Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [850, 400]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "users",
        "fields": "external_id, name, email, phone, status, metadata",
        "options": {
          "skipOnConflict": true
        }
      },
      "id": "mongodb-insert",
      "name": "Insert to MongoDB",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [1050, 300],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO users (external_id, name, email, phone, status, metadata, created_at)\nVALUES ($1, $2, $3, $4, $5, $6, NOW())\nON CONFLICT (external_id) DO UPDATE SET\n  name = EXCLUDED.name,\n  email = EXCLUDED.email,\n  phone = EXCLUDED.phone,\n  status = EXCLUDED.status,\n  metadata = EXCLUDED.metadata,\n  updated_at = NOW()\nRETURNING *",
        "options": {
          "queryParameters": "={{ JSON.stringify([\n    $json.external_id,\n    $json.name,\n    $json.email,\n    $json.phone,\n    $json.status,\n    JSON.stringify($json.metadata)\n  ]) }}"
        }
      },
      "id": "postgres-upsert",
      "name": "Upsert to PostgreSQL",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [1050, 500],
      "credentials": {
        "postgres": {
          "id": "1",
          "name": "PostgreSQL account"
        }
      }
    },
    {
      "parameters": {
        "url": "http://localhost:6379",
        "command": "SET",
        "key": "=user:{{ $json.external_id }}",
        "value": "={{ JSON.stringify($json) }}",
        "options": {
          "expire": 3600
        }
      },
      "id": "redis-cache",
      "name": "Cache in Redis",
      "type": "n8n-nodes-base.redis",
      "typeVersion": 1,
      "position": [1250, 400],
      "credentials": {
        "redis": {
          "id": "4",
          "name": "Redis account"
        }
      }
    },
    {
      "parameters": {
        "functionCode": "const allItems = $('Transform Data').all();\n\nconst summary = {\n  total_records: allItems.length,\n  valid_records: allItems.filter(i => i.json.status !== 'invalid').length,\n  invalid_records: allItems.filter(i => i.json.status === 'invalid').length,\n  mongodb_synced: $('Insert to MongoDB').all().length,\n  postgres_synced: $('Upsert to PostgreSQL').all().length,\n  redis_cached: $('Cache in Redis').all().length,\n  timestamp: new Date().toISOString()\n};\n\nreturn { json: summary };"
      },
      "id": "code-summary",
      "name": "Generate Summary",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1450, 400]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "sync_logs",
        "fields": "total_records, valid_records, invalid_records, mongodb_synced, postgres_synced, redis_cached, timestamp",
        "options": {}
      },
      "id": "mongodb-log",
      "name": "Log Sync Results",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [1650, 400],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    }
  ],
  "connections": {
    "File Created Trigger": {
      "main": [
        [
          {
            "node": "Read CSV File",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Read CSV File": {
      "main": [
        [
          {
            "node": "Parse CSV",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse CSV": {
      "main": [
        [
          {
            "node": "Transform Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Transform Data": {
      "main": [
        [
          {
            "node": "Insert to MongoDB",
            "type": "main",
            "index": 0
          },
          {
            "node": "Upsert to PostgreSQL",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Insert to MongoDB": {
      "main": [
        [
          {
            "node": "Cache in Redis",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Upsert to PostgreSQL": {
      "main": [
        [
          {
            "node": "Cache in Redis",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Cache in Redis": {
      "main": [
        [
          {
            "node": "Generate Summary",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Summary": {
      "main": [
        [
          {
            "node": "Log Sync Results",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true
}
```

### 7.2 API Gateway con Rate Limiting y Autenticación

```json
{
  "name": "API Gateway with Auth and Rate Limiting",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "={{ $json.query.method || 'GET' }}",
        "path": "api/gateway",
        "responseMode": "responseNode"
      },
      "id": "webhook-gateway",
      "name": "API Gateway Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 400]
    },
    {
      "parameters": {
        "functionCode": "const headers = $input.item.json.headers;\nconst authHeader = headers['authorization'] || headers['Authorization'];\n\nif (!authHeader || !authHeader.startsWith('Bearer ')) {\n  throw new Error('Missing or invalid authorization header');\n}\n\nconst token = authHeader.replace('Bearer ', '');\n\nreturn {\n  json: {\n    token: token,\n    request_id: `req-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,\n    timestamp: new Date().toISOString(),\n    original_request: $input.item.json\n  }\n};"
      },
      "id": "code-extract-token",
      "name": "Extract Token",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 400]
    },
    {
      "parameters": {
        "url": "http://localhost:6379",
        "command": "GET",
        "key": "=token:{{ $json.token }}"
      },
      "id": "redis-check-token",
      "name": "Verify Token",
      "type": "n8n-nodes-base.redis",
      "typeVersion": 1,
      "position": [650, 400],
      "credentials": {
        "redis": {
          "id": "4",
          "name": "Redis account"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json }}",
              "operation": "isNotEmpty"
            }
          ]
        }
      },
      "id": "if-valid-token",
      "name": "Valid Token?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [850, 400]
    },
    {
      "parameters": {
        "functionCode": "const tokenData = JSON.parse($input.item.json);\nconst userId = tokenData.user_id;\nconst requestId = $('Extract Token').item.json.request_id;\n\nreturn {\n  json: {\n    user_id: userId,\n    request_id: requestId,\n    rate_limit_key: `rate_limit:${userId}`,\n    timestamp: new Date().toISOString()\n  }\n};"
      },
      "id": "code-parse-token",
      "name": "Parse Token Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1050, 300]
    },
    {
      "parameters": {
        "url": "http://localhost:6379",
        "command": "INCR",
        "key": "={{ $json.rate_limit_key }}"
      },
      "id": "redis-increment",
      "name": "Increment Rate Limit",
      "type": "n8n-nodes-base.redis",
      "typeVersion": 1,
      "position": [1250, 300],
      "credentials": {
        "redis": {
          "id": "4",
          "name": "Redis account"
        }
      }
    },
    {
      "parameters": {
        "url": "http://localhost:6379",
        "command": "EXPIRE",
        "key": "={{ $('Parse Token Data').item.json.rate_limit_key }}",
        "value": "60"
      },
      "id": "redis-expire",
      "name": "Set Expiration",
      "type": "n8n-nodes-base.redis",
      "typeVersion": 1,
      "position": [1450, 300],
      "credentials": {
        "redis": {
          "id": "4",
          "name": "Redis account"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{ $('Increment Rate Limit').item.json }}",
              "operation": "smallerEqual",
              "value2": 100
            }
          ]
        }
      },
      "id": "if-within-limit",
      "name": "Within Rate Limit?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [1650, 300]
    },
    {
      "parameters": {
        "url": "={{ $('Extract Token').item.json.original_request.query.target_url }}",
        "method": "={{ $('Extract Token').item.json.original_request.query.method || 'GET' }}",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "X-User-ID",
              "value": "={{ $('Parse Token Data').item.json.user_id }}"
            },
            {
              "name": "X-Request-ID",
              "value": "={{ $('Parse Token Data').item.json.request_id }}"
            }
          ]
        },
        "options": {
          "timeout": 30000
        }
      },
      "id": "http-forward",
      "name": "Forward Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [1850, 200]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO api_logs (request_id, user_id, endpoint, method, status, response_time, timestamp)\nVALUES ($1, $2, $3, $4, $5, $6, NOW())",
        "options": {
          "queryParameters": "={{ JSON.stringify([\n    $('Parse Token Data').item.json.request_id,\n    $('Parse Token Data').item.json.user_id,\n    $('Extract Token').item.json.original_request.query.target_url,\n    $('Extract Token').item.json.original_request.query.method || 'GET',\n    200,\n    Date.now() - new Date($('Parse Token Data').item.json.timestamp).getTime()\n  ]) }}"
        }
      },
      "id": "postgres-log-request",
      "name": "Log Request",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [2050, 200],
      "credentials": {
        "postgres": {
          "id": "1",
          "name": "PostgreSQL account"
        }
      }
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $('Forward Request').item.json }}",
        "options": {
          "responseHeaders": {
            "entries": [
              {
                "name": "X-Request-ID",
                "value": "={{ $('Parse Token Data').item.json.request_id }}"
              },
              {
                "name": "X-Rate-Limit-Remaining",
                "value": "={{ 100 - $('Increment Rate Limit').item.json }}"
              }
            ]
          }
        }
      },
      "id": "respond-success",
      "name": "Respond Success",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [2250, 200]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseCode": 429,
        "responseBody": "={{ {\n  error: 'Rate limit exceeded',\n  message: 'Too many requests. Please try again later.',\n  retry_after: 60\n} }}",
        "options": {}
      },
      "id": "respond-rate-limit",
      "name": "Respond Rate Limit Error",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1850, 400]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseCode": 401,
        "responseBody": "={{ {\n  error: 'Unauthorized',\n  message: 'Invalid or expired token'\n} }}",
        "options": {}
      },
      "id": "respond-unauthorized",
      "name": "Respond Unauthorized",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1050, 500]
    }
  ],
  "connections": {
    "API Gateway Webhook": {
      "main": [
        [
          {
            "node": "Extract Token",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract Token": {
      "main": [
        [
          {
            "node": "Verify Token",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Verify Token": {
      "main": [
        [
          {
            "node": "Valid Token?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Valid Token?": {
      "main": [
        [
          {
            "node": "Parse Token Data",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Respond Unauthorized",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Parse Token Data": {
      "main": [
        [
          {
            "node": "Increment Rate Limit",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Increment Rate Limit": {
      "main": [
        [
          {
            "node": "Set Expiration",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Set Expiration": {
      "main": [
        [
          {
            "node": "Within Rate Limit?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Within Rate Limit?": {
      "main": [
        [
          {
            "node": "Forward Request",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Respond Rate Limit Error",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Forward Request": {
      "main": [
        [
          {
            "node": "Log Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Log Request": {
      "main": [
        [
          {
            "node": "Respond Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true
}
```

---

## 8. Mejores Prácticas

### 8.1 Manejo de Errores

```json
{
  "name": "Error Handling Best Practices",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "api/safe-operation",
        "responseMode": "responseNode"
      },
      "id": "webhook-safe",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 400]
    },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "maxTries": 3,
        "waitBetweenTries": 1000,
        "continueOnFail": true
      },
      "id": "error-trigger",
      "name": "Error Trigger",
      "type": "n8n-nodes-base.errorTrigger",
      "typeVersion": 1,
      "position": [250, 600]
    },
    {
      "parameters": {
        "url": "https://api.external-service.com/endpoint",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "data",
              "value": "={{ $json.body }}"
            }
          ]
        },
        "options": {
          "retry": {
            "maxRetries": 3,
            "retryInterval": 2000
          },
          "timeout": 10000
        }
      },
      "id": "http-risky-operation",
      "name": "Risky HTTP Operation",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 400],
      "continueOnFail": true
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $json.error }}",
              "operation": "exists"
            }
          ]
        }
      },
      "id": "if-error",
      "name": "Has Error?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [650, 400]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "error_logs",
        "fields": "error_message, error_stack, request_data, timestamp",
        "fieldsUi": {
          "fieldValues": [
            {
              "fieldName": "error_message",
              "fieldValue": "={{ $json.error.message }}"
            },
            {
              "fieldName": "error_stack",
              "fieldValue": "={{ $json.error.stack }}"
            },
            {
              "fieldName": "request_data",
              "fieldValue": "={{ JSON.stringify($('Webhook').item.json) }}"
            },
            {
              "fieldName": "timestamp",
              "fieldValue": "={{ new Date().toISOString() }}"
            }
          ]
        }
      },
      "id": "mongodb-log-error",
      "name": "Log Error",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [850, 500],
      "credentials": {
        "mongoDb": {
          "id": "2",
          "name": "MongoDB account"
        }
      }
    },
    {
      "parameters": {
        "url": "https://hooks.slack.com/services/YOUR/ERROR/WEBHOOK",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"text\": \"⚠️ Error in workflow\",\n  \"blocks\": [\n    {\n      \"type\": \"section\",\n      \"text\": {\n        \"type\": \"mrkdwn\",\n        \"text\": \"*Error:* {{ $json.error.message }}\"\n      }\n    }\n  ]\n}"
      },
      "id": "http-notify-error",
      "name": "Notify Error",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [1050, 500]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseCode": 500,
        "responseBody": "={{ {\n  success: false,\n  error: 'Internal server error',\n  request_id: $('Webhook').item.json.headers['x-request-id'] || 'unknown'\n} }}"
      },
      "id": "respond-error",
      "name": "Respond Error",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1250, 500]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $('Risky HTTP Operation').item.json }}"
      },
      "id": "respond-success-2",
      "name": "Respond Success",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [850, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [
        [
          {
            "node": "Risky HTTP Operation",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Risky HTTP Operation": {
      "main": [
        [
          {
            "node": "Has Error?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Has Error?": {
      "main": [
        [
          {
            "node": "Log Error",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Respond Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Log Error": {
      "main": [
        [
          {
            "node": "Notify Error",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Notify Error": {
      "main": [
        [
          {
            "node": "Respond Error",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "errorWorkflow": "error-handling-workflow",
    "saveDataErrorExecution": "all",
    "saveDataSuccessExecution": "all",
    "saveManualExecutions": true
  }
}
```

### 8.2 Variables de Entorno y Credenciales

```bash
# .env para n8n
N8N_ENCRYPTION_KEY=your-secure-encryption-key
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# Database
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=localhost
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=n8n_password

# Webhooks
WEBHOOK_URL=https://your-domain.com/
N8N_PROTOCOL=https
N8N_HOST=your-domain.com

# Executions
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true

# Security
N8N_SECURE_COOKIE=true
N8N_JWT_AUTH_ACTIVE=true
```

### 8.3 Optimización de Performance

1. **Usar paginación en consultas grandes**
2. **Implementar caché con Redis**
3. **Procesar en lotes (batch processing)**
4. **Usar webhooks en lugar de polling cuando sea posible**
5. **Limitar el número de reintentos**

### 8.4 Seguridad

1. **Nunca exponer credenciales en workflows**
2. **Usar autenticación JWT/OAuth**
3. **Implementar rate limiting**
4. **Validar y sanitizar inputs**
5. **Usar HTTPS para webhooks**
6. **Implementar CORS apropiadamente**

---

## 9. Recursos Adicionales

### Documentación Oficial
- n8n Docs: https://docs.n8n.io
- FastMCP: https://github.com/jlowin/fastmcp
- MCP Protocol: https://modelcontextprotocol.io

### Ejemplos de Código Backend

#### FastAPI Backend con n8n Webhook

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

class WebhookPayload(BaseModel):
    event: str
    data: dict

@app.post("/trigger-workflow")
async def trigger_n8n_workflow(payload: WebhookPayload):
    """Trigger n8n workflow from backend"""
    n8n_webhook_url = "http://localhost:5678/webhook/your-webhook-path"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            n8n_webhook_url,
            json=payload.dict()
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail="Failed to trigger workflow"
            )

        return response.json()
```

#### Express.js Backend Integration

```javascript
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

app.post('/api/process-order', async (req, res) => {
  try {
    const n8nWebhook = 'http://localhost:5678/webhook/process-order';

    const response = await axios.post(n8nWebhook, {
      action: 'create',
      order: req.body
    });

    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

## 10. Ejercicios Prácticos

### Ejercicio 1: Crear un sistema de notificaciones
Objetivo: Construir un workflow que escuche cambios en una base de datos y envíe notificaciones por múltiples canales.

### Ejercicio 2: API de agregación
Objetivo: Crear un workflow que combine datos de múltiples APIs externas y los exponga en un endpoint unificado.

### Ejercicio 3: Pipeline de procesamiento de datos
Objetivo: Implementar un pipeline completo de ETL (Extract, Transform, Load) usando n8n.

### Ejercicio 4: Sistema de autenticación con MCP
Objetivo: Crear un servidor FastMCP que maneje autenticación e integrarlo con n8n.

---

---

## 11. Integraciones Útiles con n8n

### 11.1 Servicios de Comunicación

#### Slack Integration
```json
{
  "name": "Slack Complete Integration",
  "nodes": [
    {
      "parameters": {
        "authentication": "oAuth2",
        "resource": "message",
        "operation": "post",
        "channel": "#general",
        "text": "={{ $json.message }}",
        "otherOptions": {
          "blocks": [
            {
              "type": "section",
              "text": {
                "type": "mrkdwn",
                "text": "{{ $json.message }}"
              }
            },
            {
              "type": "actions",
              "elements": [
                {
                  "type": "button",
                  "text": {
                    "type": "plain_text",
                    "text": "Approve"
                  },
                  "value": "approve",
                  "action_id": "approve_action"
                }
              ]
            }
          ]
        }
      },
      "id": "slack-message",
      "name": "Send Slack Message",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [450, 300]
    }
  ]
}
```

#### Discord Webhooks
```json
{
  "name": "Discord Notification System",
  "nodes": [
    {
      "parameters": {
        "url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"username\": \"n8n Bot\",\n  \"avatar_url\": \"https://n8n.io/favicon.ico\",\n  \"embeds\": [{\n    \"title\": \"{{ $json.title }}\",\n    \"description\": \"{{ $json.description }}\",\n    \"color\": 5814783,\n    \"fields\": [\n      {\n        \"name\": \"Status\",\n        \"value\": \"{{ $json.status }}\",\n        \"inline\": true\n      },\n      {\n        \"name\": \"Priority\",\n        \"value\": \"{{ $json.priority }}\",\n        \"inline\": true\n      }\n    ],\n    \"timestamp\": \"{{ $json.timestamp }}\"\n  }]\n}"
      },
      "id": "discord-webhook",
      "name": "Discord Webhook",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    }
  ]
}
```

#### Telegram Bot
```json
{
  "name": "Telegram Alert Bot",
  "nodes": [
    {
      "parameters": {
        "authentication": "accessToken",
        "chatId": "={{ $json.chat_id }}",
        "text": "={{ $json.message }}",
        "additionalFields": {
          "parse_mode": "Markdown",
          "reply_markup": {
            "inline_keyboard": [
              [
                {
                  "text": "View Details",
                  "url": "{{ $json.details_url }}"
                }
              ]
            ]
          }
        }
      },
      "id": "telegram-send",
      "name": "Send Telegram Message",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

### 11.2 Servicios de Storage y Cloud

#### AWS S3 Integration
```json
{
  "name": "AWS S3 File Management",
  "nodes": [
    {
      "parameters": {
        "operation": "upload",
        "bucketName": "my-bucket",
        "fileName": "={{ $json.filename }}",
        "binaryData": true,
        "additionalFields": {
          "acl": "public-read",
          "contentType": "{{ $json.content_type }}",
          "metadata": {
            "metadataProperties": [
              {
                "name": "uploaded_by",
                "value": "n8n-workflow"
              },
              {
                "name": "timestamp",
                "value": "{{ $now.toISO() }}"
              }
            ]
          }
        }
      },
      "id": "s3-upload",
      "name": "Upload to S3",
      "type": "n8n-nodes-base.awsS3",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

#### Google Drive Integration
```json
{
  "name": "Google Drive File Sync",
  "nodes": [
    {
      "parameters": {
        "operation": "upload",
        "name": "={{ $json.filename }}",
        "driveId": {
          "__rl": true,
          "value": "My Drive",
          "mode": "list"
        },
        "folderId": {
          "__rl": true,
          "value": "root",
          "mode": "list"
        },
        "options": {
          "googleFileConversion": {
            "conversion": {
              "doConversion": false
            }
          }
        }
      },
      "id": "gdrive-upload",
      "name": "Upload to Google Drive",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 3,
      "position": [450, 300]
    }
  ]
}
```

#### Dropbox Integration
```json
{
  "name": "Dropbox Backup System",
  "nodes": [
    {
      "parameters": {
        "operation": "upload",
        "path": "/backups/{{ $json.filename }}",
        "binaryData": true,
        "options": {
          "mode": "overwrite"
        }
      },
      "id": "dropbox-upload",
      "name": "Upload to Dropbox",
      "type": "n8n-nodes-base.dropbox",
      "typeVersion": 2,
      "position": [450, 300]
    }
  ]
}
```

### 11.3 Servicios de Email

#### SendGrid Integration
```json
{
  "name": "SendGrid Email Campaign",
  "nodes": [
    {
      "parameters": {
        "fromEmail": "noreply@company.com",
        "fromName": "Company Name",
        "toEmail": "={{ $json.recipient_email }}",
        "subject": "={{ $json.subject }}",
        "emailType": "html",
        "message": "={{ $json.html_content }}",
        "options": {
          "categories": ["newsletter", "automated"],
          "customArgs": {
            "customArgsProperties": [
              {
                "key": "campaign_id",
                "value": "{{ $json.campaign_id }}"
              }
            ]
          }
        }
      },
      "id": "sendgrid-email",
      "name": "Send Email via SendGrid",
      "type": "n8n-nodes-base.sendGrid",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

#### Mailchimp Integration
```json
{
  "name": "Mailchimp Subscriber Management",
  "nodes": [
    {
      "parameters": {
        "operation": "upsert",
        "listId": "your-list-id",
        "email": "={{ $json.email }}",
        "updateFields": {
          "mergeFields": {
            "mergeFieldsValues": [
              {
                "name": "FNAME",
                "value": "{{ $json.first_name }}"
              },
              {
                "name": "LNAME",
                "value": "{{ $json.last_name }}"
              }
            ]
          },
          "tags": ["automated", "n8n-import"]
        }
      },
      "id": "mailchimp-upsert",
      "name": "Add/Update Mailchimp Subscriber",
      "type": "n8n-nodes-base.mailchimp",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

### 11.4 Servicios de Pago

#### Stripe Integration
```json
{
  "name": "Stripe Payment Processing",
  "nodes": [
    {
      "parameters": {
        "resource": "charge",
        "operation": "create",
        "amount": "={{ $json.amount }}",
        "currency": "usd",
        "additionalFields": {
          "description": "{{ $json.description }}",
          "metadata": {
            "metadataProperties": [
              {
                "key": "order_id",
                "value": "{{ $json.order_id }}"
              },
              {
                "key": "customer_id",
                "value": "{{ $json.customer_id }}"
              }
            ]
          },
          "receiptEmail": "{{ $json.customer_email }}"
        }
      },
      "id": "stripe-charge",
      "name": "Create Stripe Charge",
      "type": "n8n-nodes-base.stripe",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

#### PayPal Integration
```json
{
  "name": "PayPal Payment Verification",
  "nodes": [
    {
      "parameters": {
        "url": "https://api.paypal.com/v1/oauth2/token",
        "method": "POST",
        "authentication": "genericCredentialType",
        "sendBody": true,
        "specifyBody": "form",
        "bodyParameters": {
          "parameters": [
            {
              "name": "grant_type",
              "value": "client_credentials"
            }
          ]
        }
      },
      "id": "paypal-auth",
      "name": "PayPal Authentication",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    }
  ]
}
```

### 11.5 Servicios de IA y Machine Learning

#### OpenAI Integration
```json
{
  "name": "OpenAI Content Generation",
  "nodes": [
    {
      "parameters": {
        "model": "gpt-4",
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "You are a helpful assistant."
            },
            {
              "role": "user",
              "content": "={{ $json.prompt }}"
            }
          ]
        },
        "options": {
          "temperature": 0.7,
          "maxTokens": 1000
        }
      },
      "id": "openai-chat",
      "name": "OpenAI Chat Completion",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

#### Anthropic Claude via MCP
```python
# claude_mcp_server.py
from fastmcp import FastMCP
from anthropic import Anthropic

mcp = FastMCP("Claude AI Server")
client = Anthropic()

@mcp.tool()
async def analyze_text(text: str, task: str) -> dict:
    """Analiza texto usando Claude"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"{task}\n\nText: {text}"
            }
        ]
    )

    return {
        "analysis": message.content[0].text,
        "model": message.model,
        "tokens_used": message.usage.input_tokens + message.usage.output_tokens
    }

@mcp.tool()
async def generate_code(description: str, language: str) -> dict:
    """Genera código usando Claude"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"Generate {language} code for: {description}"
            }
        ]
    )

    return {
        "code": message.content[0].text,
        "language": language
    }

if __name__ == "__main__":
    mcp.run()
```

### 11.6 Servicios de Monitoreo y Analytics

#### Grafana Webhook
```json
{
  "name": "Grafana Alert Handler",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "grafana/alert",
        "responseMode": "responseNode"
      },
      "id": "webhook-grafana",
      "name": "Grafana Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "functionCode": "const alert = $input.item.json;\n\nreturn {\n  json: {\n    alert_name: alert.title,\n    status: alert.state,\n    message: alert.message,\n    severity: alert.state === 'alerting' ? 'high' : 'medium',\n    metric_value: alert.evalMatches?.[0]?.value || 0,\n    timestamp: new Date().toISOString(),\n    dashboard_url: alert.ruleUrl\n  }\n};"
      },
      "id": "code-process-grafana",
      "name": "Process Grafana Alert",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 300]
    }
  ]
}
```

#### Google Analytics Integration
```json
{
  "name": "Google Analytics Reporting",
  "nodes": [
    {
      "parameters": {
        "operation": "report",
        "viewId": "your-view-id",
        "startDate": "7daysAgo",
        "endDate": "today",
        "metrics": [
          {
            "expression": "ga:sessions"
          },
          {
            "expression": "ga:users"
          },
          {
            "expression": "ga:pageviews"
          }
        ],
        "dimensions": [
          {
            "name": "ga:date"
          }
        ]
      },
      "id": "ga-report",
      "name": "Get GA Report",
      "type": "n8n-nodes-base.googleAnalytics",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

### 11.7 Servicios de CRM y Sales

#### HubSpot Integration
```json
{
  "name": "HubSpot Contact Sync",
  "nodes": [
    {
      "parameters": {
        "operation": "upsert",
        "email": "={{ $json.email }}",
        "additionalFields": {
          "firstName": "{{ $json.first_name }}",
          "lastName": "{{ $json.last_name }}",
          "phone": "{{ $json.phone }}",
          "company": "{{ $json.company }}",
          "customProperties": {
            "customPropertiesValues": [
              {
                "property": "lead_source",
                "value": "n8n_automation"
              }
            ]
          }
        }
      },
      "id": "hubspot-contact",
      "name": "Create/Update HubSpot Contact",
      "type": "n8n-nodes-base.hubspot",
      "typeVersion": 2,
      "position": [450, 300]
    }
  ]
}
```

#### Salesforce Integration
```json
{
  "name": "Salesforce Lead Creation",
  "nodes": [
    {
      "parameters": {
        "operation": "create",
        "resource": "lead",
        "lastName": "={{ $json.last_name }}",
        "company": "={{ $json.company }}",
        "additionalFields": {
          "firstName": "{{ $json.first_name }}",
          "email": "{{ $json.email }}",
          "phone": "{{ $json.phone }}",
          "leadSource": "Website"
        }
      },
      "id": "salesforce-lead",
      "name": "Create Salesforce Lead",
      "type": "n8n-nodes-base.salesforce",
      "typeVersion": 2,
      "position": [450, 300]
    }
  ]
}
```

### 11.8 Servicios de CI/CD y DevOps

#### GitHub Integration
```json
{
  "name": "GitHub Repository Automation",
  "nodes": [
    {
      "parameters": {
        "operation": "create",
        "resource": "issue",
        "owner": "={{ $json.repo_owner }}",
        "repository": "={{ $json.repo_name }}",
        "title": "={{ $json.issue_title }}",
        "body": "={{ $json.issue_description }}",
        "additionalParameters": {
          "labels": ["bug", "automated"],
          "assignees": ["{{ $json.assignee }}"]
        }
      },
      "id": "github-issue",
      "name": "Create GitHub Issue",
      "type": "n8n-nodes-base.github",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

#### GitLab CI/CD Trigger
```json
{
  "name": "GitLab Pipeline Trigger",
  "nodes": [
    {
      "parameters": {
        "url": "https://gitlab.com/api/v4/projects/{{ $json.project_id }}/trigger/pipeline",
        "method": "POST",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "PRIVATE-TOKEN",
              "value": "={{ $credentials.gitlabApi.token }}"
            }
          ]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "token",
              "value": "{{ $json.trigger_token }}"
            },
            {
              "name": "ref",
              "value": "main"
            },
            {
              "name": "variables[DEPLOY_ENV]",
              "value": "production"
            }
          ]
        }
      },
      "id": "gitlab-trigger",
      "name": "Trigger GitLab Pipeline",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    }
  ]
}
```

#### Docker Integration
```json
{
  "name": "Docker Container Management",
  "nodes": [
    {
      "parameters": {
        "operation": "list",
        "options": {
          "all": true
        }
      },
      "id": "docker-list",
      "name": "List Docker Containers",
      "type": "n8n-nodes-base.docker",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

### 11.9 Servicios de Base de Datos y Caché

#### Redis Pub/Sub
```json
{
  "name": "Redis Pub/Sub Pattern",
  "nodes": [
    {
      "parameters": {
        "url": "redis://localhost:6379",
        "command": "PUBLISH",
        "key": "{{ $json.channel }}",
        "value": "={{ JSON.stringify($json.message) }}"
      },
      "id": "redis-publish",
      "name": "Publish to Redis",
      "type": "n8n-nodes-base.redis",
      "typeVersion": 1,
      "position": [450, 300]
    }
  ]
}
```

#### Elasticsearch Integration
```json
{
  "name": "Elasticsearch Indexing",
  "nodes": [
    {
      "parameters": {
        "url": "http://localhost:9200/my-index/_doc",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify($json) }}",
        "options": {
          "timeout": 10000
        }
      },
      "id": "elasticsearch-index",
      "name": "Index to Elasticsearch",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    }
  ]
}
```

### 11.10 Workflow Completo: Sistema de Integración Multi-Servicio

```json
{
  "name": "Multi-Service Integration Hub",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "integration/event",
        "responseMode": "responseNode"
      },
      "id": "webhook-entry",
      "name": "Integration Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 500]
    },
    {
      "parameters": {
        "functionCode": "const event = $input.item.json;\n\nconst integrations = {\n  slack: event.notify_slack,\n  email: event.notify_email,\n  sms: event.notify_sms,\n  database: event.save_to_db,\n  storage: event.save_to_storage,\n  analytics: event.track_analytics\n};\n\nreturn {\n  json: {\n    event_id: `evt-${Date.now()}`,\n    event_type: event.type,\n    event_data: event.data,\n    integrations: integrations,\n    timestamp: new Date().toISOString()\n  }\n};"
      },
      "id": "code-orchestrate",
      "name": "Orchestrate Integrations",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [450, 500]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $json.integrations.slack }}",
              "value2": true
            }
          ]
        }
      },
      "id": "if-slack",
      "name": "Should Notify Slack?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [650, 400]
    },
    {
      "parameters": {
        "authentication": "oAuth2",
        "channel": "#notifications",
        "text": "={{ $('Orchestrate Integrations').item.json.event_data.message }}"
      },
      "id": "slack-notify",
      "name": "Notify Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [850, 300]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $('Orchestrate Integrations').item.json.integrations.database }}",
              "value2": true
            }
          ]
        }
      },
      "id": "if-database",
      "name": "Should Save to DB?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [650, 600]
    },
    {
      "parameters": {
        "operation": "insert",
        "collection": "events",
        "fields": "event_id, event_type, event_data, timestamp"
      },
      "id": "mongodb-save",
      "name": "Save to MongoDB",
      "type": "n8n-nodes-base.mongoDb",
      "typeVersion": 1,
      "position": [850, 600]
    },
    {
      "parameters": {
        "operation": "upload",
        "bucketName": "events-bucket",
        "fileName": "={{ $('Orchestrate Integrations').item.json.event_id }}.json",
        "binaryData": false,
        "fileContent": "={{ JSON.stringify($('Orchestrate Integrations').item.json) }}"
      },
      "id": "s3-backup",
      "name": "Backup to S3",
      "type": "n8n-nodes-base.awsS3",
      "typeVersion": 1,
      "position": [1050, 500]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ {\n  success: true,\n  event_id: $('Orchestrate Integrations').item.json.event_id,\n  integrations_executed: Object.keys($('Orchestrate Integrations').item.json.integrations).filter(k => $('Orchestrate Integrations').item.json.integrations[k])\n} }}"
      },
      "id": "respond-result",
      "name": "Respond Result",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [1250, 500]
    }
  ],
  "connections": {
    "Integration Webhook": {
      "main": [[{"node": "Orchestrate Integrations", "type": "main", "index": 0}]]
    },
    "Orchestrate Integrations": {
      "main": [
        [
          {"node": "Should Notify Slack?", "type": "main", "index": 0},
          {"node": "Should Save to DB?", "type": "main", "index": 0}
        ]
      ]
    },
    "Should Notify Slack?": {
      "main": [[{"node": "Notify Slack", "type": "main", "index": 0}]]
    },
    "Should Save to DB?": {
      "main": [[{"node": "Save to MongoDB", "type": "main", "index": 0}]]
    },
    "Notify Slack": {
      "main": [[{"node": "Backup to S3", "type": "main", "index": 0}]]
    },
    "Save to MongoDB": {
      "main": [[{"node": "Backup to S3", "type": "main", "index": 0}]]
    },
    "Backup to S3": {
      "main": [[{"node": "Respond Result", "type": "main", "index": 0}]]
    }
  },
  "active": true
}
```

### 11.11 Herramientas de Testing y Debugging

#### Webhook.site Integration
- URL: https://webhook.site
- Útil para: Debuggear webhooks y ver payloads en tiempo real

#### RequestBin Alternative
```json
{
  "name": "Debug Webhook Payload",
  "nodes": [
    {
      "parameters": {
        "url": "https://webhook.site/your-unique-url",
        "method": "POST",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ JSON.stringify($json, null, 2) }}"
      },
      "id": "debug-webhook",
      "name": "Send to Debug Endpoint",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [450, 300]
    }
  ]
}
```

### 11.12 Recursos y Comunidad

**Nodos Comunitarios:**
- n8n-nodes-browserless: Automatización de navegadores
- n8n-nodes-puppeteer: Web scraping avanzado
- n8n-nodes-undetected-chromedriver: Scraping anti-detección
- n8n-nodes-browserstack: Testing automatizado

**Enlaces Útiles:**
- n8n Community: https://community.n8n.io
- n8n Templates: https://n8n.io/workflows
- n8n GitHub: https://github.com/n8n-io/n8n
- n8n Discord: https://discord.gg/n8n

---

## Conclusión

Este taller cubre:
✅ Instalación y configuración de n8n
✅ Fundamentos de workflows
✅ Integración con backends (PostgreSQL, MongoDB, Redis)
✅ Implementación de MCP con FastMCP
✅ Ejemplos reales y casos de uso
✅ Mejores prácticas de seguridad y performance
✅ **50+ integraciones útiles con servicios populares**
✅ **Ejemplos de comunicación (Slack, Discord, Telegram)**
✅ **Servicios de storage (S3, Google Drive, Dropbox)**
✅ **Plataformas de email (SendGrid, Mailchimp)**
✅ **Pasarelas de pago (Stripe, PayPal)**
✅ **IA y ML (OpenAI, Claude via MCP)**
✅ **CRM (HubSpot, Salesforce)**
✅ **DevOps (GitHub, GitLab, Docker)**

**Próximos pasos:**
1. Experimentar con los workflows JSON proporcionados
2. Implementar tu propio servidor FastMCP
3. Crear integraciones personalizadas
4. Explorar nodos avanzados de n8n
5. Conectar n8n con tus servicios favoritos
6. Construir workflows multi-servicio complejos
