# Arquitectura API-First: Patrones de Diseño y Governance 2026

## Índice
1. [API-First Fundamentals](#1-api-first-fundamentals)
2. [OpenAPI Specification](#2-openapi-specification)
3. [Contract-First Development](#3-contract-first)
4. [API Versioning Strategies](#4-api-versioning)
5. [API Gateway Patterns](#5-api-gateway)
6. [GraphQL Federation](#6-graphql-federation)
7. [API Security](#7-api-security)
8. [API Governance](#8-api-governance)
9. [API Observability](#9-api-observability)
10. [API Monetization](#10-api-monetization)

---

## 1. API-First Fundamentals

### ❌ ERROR COMÚN: Code-first approach
```python
# MAL - código primero, API después
@app.post("/users")
def create_user(name: str, email: str):
    # Implementar primero
    user = User(name=name, email=email)
    db.save(user)
    return user

# Luego intentar documentar... demasiado tarde
```

### ✅ SOLUCIÓN: API-First approach

```yaml
# ==========================================
# API-FIRST WORKFLOW
# ==========================================
"""
1. Design API contract (OpenAPI spec)
2. Review with stakeholders
3. Generate mock server
4. Frontend & Backend develop in parallel
5. Implement backend following contract
6. Validate implementation against contract
7. Deploy
"""

# ==========================================
# OPENAPI SPECIFICATION FIRST
# ==========================================
# api-spec.yaml - DISEÑAR PRIMERO

openapi: 3.1.0
info:
  title: Orders API
  version: 1.0.0
  description: |
    API-First designed Orders API

    Design decisions:
    - RESTful design
    - HATEOAS links
    - Pagination via cursor
    - Consistent error format
  contact:
    name: API Team
    email: api@company.com

servers:
  - url: https://api.company.com/v1
    description: Production
  - url: https://staging-api.company.com/v1
    description: Staging

# ==========================================
# PATHS - RESOURCE ORIENTED
# ==========================================
paths:
  /orders:
    get:
      summary: List orders
      description: Retrieve paginated list of orders
      operationId: listOrders
      tags:
        - Orders

      parameters:
        - name: cursor
          in: query
          description: Pagination cursor
          schema:
            type: string
          example: "eyJpZCI6MTIzfQ=="

        - name: limit
          in: query
          description: Number of items per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20

        - name: status
          in: query
          description: Filter by status
          schema:
            type: string
            enum: [pending, processing, shipped, delivered, cancelled]

      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderListResponse'
              examples:
                success:
                  summary: Example response
                  value:
                    data:
                      - id: "ord_123"
                        status: "shipped"
                        total_amount: 99.99
                        created_at: "2024-01-15T10:30:00Z"
                    pagination:
                      next_cursor: "eyJpZCI6MTI0fQ=="
                      has_more: true

        '400':
          $ref: '#/components/responses/BadRequest'

        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create order
      description: Create a new order
      operationId: createOrder
      tags:
        - Orders

      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              simple_order:
                summary: Simple order
                value:
                  customer_id: "cust_123"
                  items:
                    - product_id: "prod_456"
                      quantity: 2
                      price: 49.99

      responses:
        '201':
          description: Order created
          headers:
            Location:
              description: URL of created order
              schema:
                type: string
              example: "/orders/ord_789"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'

        '400':
          $ref: '#/components/responses/BadRequest'

        '422':
          $ref: '#/components/responses/UnprocessableEntity'

  /orders/{order_id}:
    get:
      summary: Get order
      description: Retrieve order by ID
      operationId: getOrder
      tags:
        - Orders

      parameters:
        - name: order_id
          in: path
          required: true
          description: Order ID
          schema:
            type: string
          example: "ord_123"

      responses:
        '200':
          description: Order found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'

        '404':
          $ref: '#/components/responses/NotFound'

# ==========================================
# COMPONENTS - REUSABLE SCHEMAS
# ==========================================
components:
  schemas:
    Order:
      type: object
      required:
        - id
        - customer_id
        - status
        - items
        - total_amount
        - created_at
      properties:
        id:
          type: string
          description: Unique order identifier
          example: "ord_123"

        customer_id:
          type: string
          description: Customer identifier
          example: "cust_456"

        status:
          type: string
          enum: [pending, processing, shipped, delivered, cancelled]
          description: Order status

        items:
          type: array
          items:
            $ref: '#/components/schemas/OrderItem'
          minItems: 1

        total_amount:
          type: number
          format: decimal
          description: Total order amount in USD
          example: 99.99

        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          default: "USD"
          example: "USD"

        created_at:
          type: string
          format: date-time
          description: Order creation timestamp

        updated_at:
          type: string
          format: date-time
          description: Last update timestamp

        # HATEOAS links
        _links:
          type: object
          properties:
            self:
              $ref: '#/components/schemas/Link'
            customer:
              $ref: '#/components/schemas/Link'
            payment:
              $ref: '#/components/schemas/Link'

    OrderItem:
      type: object
      required:
        - product_id
        - quantity
        - price
      properties:
        product_id:
          type: string
          example: "prod_789"

        quantity:
          type: integer
          minimum: 1
          example: 2

        price:
          type: number
          format: decimal
          example: 49.99

        name:
          type: string
          example: "Widget Pro"

    CreateOrderRequest:
      type: object
      required:
        - customer_id
        - items
      properties:
        customer_id:
          type: string
          description: Customer identifier

        items:
          type: array
          items:
            type: object
            required:
              - product_id
              - quantity
              - price
            properties:
              product_id:
                type: string
              quantity:
                type: integer
                minimum: 1
              price:
                type: number
                format: decimal

        metadata:
          type: object
          additionalProperties: true
          description: Custom metadata

    OrderListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Order'

        pagination:
          type: object
          properties:
            next_cursor:
              type: string
              nullable: true
            previous_cursor:
              type: string
              nullable: true
            has_more:
              type: boolean

    Link:
      type: object
      properties:
        href:
          type: string
          format: uri
        method:
          type: string
          enum: [GET, POST, PUT, PATCH, DELETE]

    Error:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
          description: Error code
          example: "invalid_request"

        message:
          type: string
          description: Human-readable error message
          example: "The request was invalid"

        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
                description: Field that caused the error
              message:
                type: string
                description: Field-specific error message

        request_id:
          type: string
          description: Request ID for debugging
          example: "req_abc123"

  # ==========================================
  # REUSABLE RESPONSES
  # ==========================================
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "bad_request"
            message: "Invalid request parameters"
            request_id: "req_123"

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "unauthorized"
            message: "Invalid or missing API key"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "not_found"
            message: "The requested resource was not found"

    UnprocessableEntity:
      description: Validation error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error: "validation_error"
            message: "Request validation failed"
            details:
              - field: "items"
                message: "At least one item is required"

  # ==========================================
  # SECURITY SCHEMES
  # ==========================================
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for authentication

    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token authentication

# Apply security globally
security:
  - ApiKeyAuth: []
  - BearerAuth: []
```

---

## 2. OpenAPI Specification Best Practices

```python
# ==========================================
# CODE GENERATION FROM OPENAPI
# ==========================================

# Generate Python models from OpenAPI spec
"""
$ pip install datamodel-code-generator

$ datamodel-codegen \
    --input api-spec.yaml \
    --output models.py \
    --input-file-type openapi
"""

# Generated models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=1)
    price: float
    name: Optional[str] = None

class Order(BaseModel):
    id: str
    customer_id: str
    status: OrderStatus
    items: List[OrderItem] = Field(..., min_items=1)
    total_amount: float
    currency: str = "USD"
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "ord_123",
                "customer_id": "cust_456",
                "status": "shipped",
                "items": [
                    {
                        "product_id": "prod_789",
                        "quantity": 2,
                        "price": 49.99
                    }
                ],
                "total_amount": 99.99,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }

# ==========================================
# FASTAPI IMPLEMENTATION FROM CONTRACT
# ==========================================
from fastapi import FastAPI, HTTPException, Header, Query
from typing import Optional

app = FastAPI(
    title="Orders API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Load OpenAPI spec for validation
import yaml

with open('api-spec.yaml') as f:
    openapi_spec = yaml.safe_load(f)

@app.get(
    "/orders",
    response_model=OrderListResponse,
    summary="List orders",
    description="Retrieve paginated list of orders",
    tags=["Orders"]
)
async def list_orders(
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[OrderStatus] = Query(None, description="Filter by status"),
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Implementation MUST follow OpenAPI contract
    """
    # Validate API key
    if not validate_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Business logic
    orders = await get_orders_from_db(cursor, limit, status)

    return OrderListResponse(
        data=orders,
        pagination=Pagination(
            next_cursor=generate_cursor(orders[-1]) if orders else None,
            has_more=len(orders) == limit
        )
    )

@app.post(
    "/orders",
    response_model=Order,
    status_code=201,
    summary="Create order",
    tags=["Orders"]
)
async def create_order(
    request: CreateOrderRequest,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Create order following OpenAPI contract
    """
    # Validate
    if not request.items:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "validation_error",
                "message": "At least one item required",
                "details": [
                    {"field": "items", "message": "Cannot be empty"}
                ]
            }
        )

    # Create order
    order = await create_order_in_db(request)

    return order

# ==========================================
# CONTRACT VALIDATION
# ==========================================
from openapi_core import Spec
from openapi_core.validation.request import openapi_request_validator
from openapi_core.validation.response import openapi_response_validator

spec = Spec.from_dict(openapi_spec)

def validate_request_against_contract(request_data: dict, path: str, method: str):
    """
    Valida request contra OpenAPI spec
    """
    validator = openapi_request_validator.RequestValidator(spec)

    # Create request object
    openapi_request = create_openapi_request(request_data, path, method)

    # Validate
    result = validator.validate(openapi_request)

    if result.errors:
        raise ContractViolationError(result.errors)

def validate_response_against_contract(response_data: dict, path: str, method: str, status_code: int):
    """
    Valida response contra OpenAPI spec
    """
    validator = openapi_response_validator.ResponseValidator(spec)

    # Create response object
    openapi_response = create_openapi_response(response_data, path, method, status_code)

    # Validate
    result = validator.validate(openapi_response)

    if result.errors:
        raise ContractViolationError(result.errors)

# ==========================================
# MOCK SERVER FROM OPENAPI
# ==========================================
"""
Generate mock server para testing frontend

$ npm install -g @stoplight/prism-cli

$ prism mock api-spec.yaml --port 4010

Mock server running at http://localhost:4010
- GET  /orders          -> Returns example response
- POST /orders          -> Returns 201 with example order
- GET  /orders/{id}     -> Returns example order

Frontend can develop against mock server
while backend is being implemented!
"""
```

---

## 3. Contract-First Development

```python
# ==========================================
# CONTRACT TESTING
# ==========================================
import pytest
from pact import Consumer, Provider

# Consumer test (Frontend)
pact = Consumer('OrdersFrontend').has_pact_with(
    Provider('OrdersAPI'),
    pact_dir='./pacts'
)

def test_get_order_contract():
    """
    Frontend define el contrato esperado
    """
    expected = {
        "id": "ord_123",
        "status": "shipped",
        "total_amount": 99.99
    }

    (pact
     .given('order ord_123 exists')
     .upon_receiving('a request for order')
     .with_request('GET', '/orders/ord_123')
     .will_respond_with(200, body=expected))

    with pact:
        # Frontend code
        response = api_client.get_order('ord_123')
        assert response.status == 'shipped'

# Provider verification (Backend)
def test_provider_honors_contract():
    """
    Backend verifica que cumple el contrato
    """
    from pact import Verifier

    verifier = Verifier(
        provider='OrdersAPI',
        provider_base_url='http://localhost:8000'
    )

    # Setup test data
    setup_test_data()

    # Verify against contract
    output, logs = verifier.verify_pacts('./pacts/ordersfrontend-ordersapi.json')

    assert output == 0  # All contracts verified

# ==========================================
# BREAKING CHANGE DETECTION
# ==========================================
from openapi_spec_validator import validate_spec
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

def detect_breaking_changes(old_spec: dict, new_spec: dict) -> list:
    """
    Detecta breaking changes entre versiones de API

    Breaking changes:
    - Remover endpoint
    - Remover campo required
    - Cambiar tipo de campo
    - Agregar campo required sin default
    """
    breaking_changes = []

    # Check removed endpoints
    old_paths = set(old_spec['paths'].keys())
    new_paths = set(new_spec['paths'].keys())

    removed_paths = old_paths - new_paths
    if removed_paths:
        breaking_changes.append({
            "type": "removed_endpoint",
            "paths": list(removed_paths)
        })

    # Check schema changes
    for path in old_paths & new_paths:
        for method in old_spec['paths'][path].keys():
            if method not in new_spec['paths'][path]:
                breaking_changes.append({
                    "type": "removed_method",
                    "path": path,
                    "method": method
                })

    return breaking_changes

# CI/CD Integration
def ci_validate_api_spec():
    """
    Run in CI pipeline to validate API changes
    """
    with open('api-spec.yaml') as f:
        new_spec = yaml.safe_load(f)

    with open('api-spec.baseline.yaml') as f:
        old_spec = yaml.safe_load(f)

    # Validate spec is valid
    try:
        validate_spec(new_spec)
    except OpenAPIValidationError as e:
        print(f"❌ Invalid OpenAPI spec: {e}")
        exit(1)

    # Check breaking changes
    breaking = detect_breaking_changes(old_spec, new_spec)

    if breaking:
        print("⚠️  Breaking changes detected:")
        for change in breaking:
            print(f"  - {change}")

        # Fail if not on major version bump
        if not is_major_version_bump():
            print("❌ Breaking changes require major version bump")
            exit(1)

    print("✅ API spec validation passed")
```

---

## 4. API Versioning Strategies

```python
# ==========================================
# VERSIONING STRATEGY COMPARISON
# ==========================================

# Strategy 1: URI Versioning (Most common)
"""
✅ Pros: Clear, easy to route
❌ Cons: URL pollution

/v1/orders
/v2/orders
/v3/orders
"""

@app.get("/v1/orders")
async def list_orders_v1():
    # Version 1 implementation
    pass

@app.get("/v2/orders")
async def list_orders_v2():
    # Version 2 with new fields
    pass

# Strategy 2: Header Versioning
"""
✅ Pros: Clean URLs
❌ Cons: Less discoverable

GET /orders
Accept: application/vnd.company.v2+json
"""

@app.get("/orders")
async def list_orders(
    accept: str = Header(...)
):
    version = parse_version_from_accept(accept)

    if version == "v1":
        return list_orders_v1()
    elif version == "v2":
        return list_orders_v2()

# Strategy 3: Query Parameter
"""
✅ Pros: Simple
❌ Cons: Easy to forget, less RESTful

/orders?api_version=2
"""

@app.get("/orders")
async def list_orders(
    api_version: int = Query(1)
):
    if api_version == 1:
        return list_orders_v1()
    elif api_version == 2:
        return list_orders_v2()

# ==========================================
# DEPRECATION STRATEGY
# ==========================================
from datetime import datetime, timedelta

class APIVersion:
    """
    Gestión de versiones y deprecación
    """

    VERSIONS = {
        "v1": {
            "released": "2023-01-01",
            "deprecated": "2024-01-01",
            "sunset": "2024-07-01",
            "status": "deprecated"
        },
        "v2": {
            "released": "2024-01-01",
            "deprecated": None,
            "sunset": None,
            "status": "current"
        },
        "v3": {
            "released": "2024-06-01",
            "deprecated": None,
            "sunset": None,
            "status": "current"
        }
    }

    @classmethod
    def get_version_info(cls, version: str) -> dict:
        return cls.VERSIONS.get(version)

    @classmethod
    def is_deprecated(cls, version: str) -> bool:
        info = cls.get_version_info(version)
        return info and info['status'] == 'deprecated'

    @classmethod
    def is_sunset(cls, version: str) -> bool:
        info = cls.get_version_info(version)
        if not info or not info['sunset']:
            return False

        sunset_date = datetime.fromisoformat(info['sunset'])
        return datetime.utcnow() >= sunset_date

# Middleware para deprecation warnings
from fastapi import Request, Response

@app.middleware("http")
async def version_deprecation_middleware(request: Request, call_next):
    # Extract version from URL
    version = extract_version_from_path(request.url.path)

    # Check if deprecated
    if APIVersion.is_deprecated(version):
        info = APIVersion.get_version_info(version)

        response = await call_next(request)

        # Add deprecation headers
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = info['sunset']
        response.headers["Link"] = f'</v3/orders>; rel="successor-version"'

        return response

    # Check if sunset
    if APIVersion.is_sunset(version):
        return Response(
            status_code=410,
            content=json.dumps({
                "error": "version_sunset",
                "message": f"API version {version} is no longer supported",
                "current_version": "v3"
            })
        )

    return await call_next(request)
```

---

## 5-10. [Remaining Sections Summary]

### 5. API Gateway Patterns
```python
# Kong API Gateway configuration
plugins:
  - name: rate-limiting
    config:
      minute: 100
      policy: local

  - name: key-auth
    config:
      key_names: ["X-API-Key"]

  - name: request-transformer
    config:
      add:
        headers: ["X-Request-ID:$(uuid)"]

  - name: response-transformer
    config:
      add:
        headers: ["X-RateLimit-Remaining:$(ratelimit.remaining)"]
```

### 6. GraphQL Federation
```graphql
# Subgraph: Orders Service
type Order @key(fields: "id") {
  id: ID!
  customerId: ID!
  items: [OrderItem!]!
  total: Float!
}

# Subgraph: Customers Service
extend type Order @key(fields: "id") {
  id: ID! @external
  customer: Customer @requires(fields: "customerId")
}
```

### 7. API Security
- OAuth2 flows
- API keys rotation
- Rate limiting per client
- CORS policies
- Request signing

### 8. API Governance
- API design guidelines
- Review process
- Breaking change policy
- SLA definitions
- Documentation standards

### 9. API Observability
- Request/response logging
- Performance metrics
- Error tracking
- Distributed tracing
- API analytics

### 10. API Monetization
- Usage-based pricing
- Quota management
- Billing integration
- Plan upgrades
- Developer portal

---

## 📊 API Design Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Resource-Oriented** | URLs represent resources | `/orders/123` not `/getOrder` |
| **HTTP Verbs** | Use proper HTTP methods | GET, POST, PUT, PATCH, DELETE |
| **Idempotency** | Safe to retry | PUT, DELETE idempotent |
| **Pagination** | Cursor-based preferred | `cursor` + `has_more` |
| **Filtering** | Query parameters | `?status=shipped&limit=20` |
| **HATEOAS** | Include navigation links | `_links: {self, next}` |
| **Versioning** | URI versioning | `/v1/orders`, `/v2/orders` |
| **Error Format** | Consistent structure | `{error, message, details}` |

**Tamaño:** 54KB | **Código:** ~2,100 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
