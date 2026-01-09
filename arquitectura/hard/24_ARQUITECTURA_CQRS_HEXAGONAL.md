# Arquitectura: CQRS, Hexagonal Architecture y Clean Architecture 2026

## Objetivo
Patrones arquitectónicos avanzados: CQRS completo, Hexagonal Architecture (Ports & Adapters), Clean Architecture, y patrones de integración entre bounded contexts.

---

## CATEGORÍA 1: CQRS (Command Query Responsibility Segregation)

### 1.1 CQRS con Read Models Optimizados
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
CQRS separa escrituras (Commands) de lecturas (Queries). Permite optimizar cada lado independientemente.

**Problema: Modelo Único para Escritura y Lectura**

```python
# ❌ BAD: Mismo modelo para writes y reads
class Order:
    """
    ORM model usado para:
    - Writes (place order, update status)
    - Reads (list orders, order details, analytics)

    Problemas:
    - Joins complejos para queries
    - Performance degradada
    - Dificil escalar reads vs writes
    """
    id: int
    customer_id: int
    status: str
    total: Decimal
    items: List[OrderItem]  # Relationship (requires JOIN)

    # Read endpoint
    @staticmethod
    async def get_order_with_customer_and_items(order_id: int):
        """
        Complex query with multiple JOINs

        SELECT orders.*, customers.*, order_items.*, products.*
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        JOIN order_items ON orders.id = order_items.order_id
        JOIN products ON order_items.product_id = products.id
        WHERE orders.id = ?

        Slow for high volume reads!
        """
        pass
```

**✅ GOOD: CQRS Pattern**

```python
# CQRS: Separate Write and Read Models

# ============================================
# WRITE SIDE: Commands
# ============================================

from dataclasses import dataclass
from typing import List
from decimal import Decimal

@dataclass
class PlaceOrderCommand:
    """
    Command: Intent to change state

    Immutable, represents business operation
    """
    customer_id: str
    items: List[dict]
    shipping_address: dict

    def __post_init__(self):
        """Validate command"""
        if not self.items:
            raise ValueError("Order must have items")


@dataclass
class ConfirmOrderCommand:
    """Command: Confirm order after payment"""
    order_id: str
    payment_id: str


# Command Handler
class PlaceOrderCommandHandler:
    """
    Write side: Handle commands

    Responsibilities:
    - Validate business rules
    - Modify write model (aggregate)
    - Persist to write database
    - Emit domain events
    """

    def __init__(
        self,
        order_repository: OrderRepository,
        event_bus: EventBus,
        inventory_service: InventoryService
    ):
        self.order_repository = order_repository
        self.event_bus = event_bus
        self.inventory_service = inventory_service

    async def handle(self, command: PlaceOrderCommand) -> str:
        """
        Handle PlaceOrderCommand

        Write model optimized for consistency
        """

        # 1. Validate inventory
        for item in command.items:
            available = await self.inventory_service.check_stock(
                item['product_id'],
                item['quantity']
            )
            if not available:
                raise InsufficientStockError(item['product_id'])

        # 2. Create aggregate (write model)
        order = Order.create(
            customer_id=command.customer_id,
            items=command.items,
            shipping_address=command.shipping_address
        )

        # 3. Persist to write DB
        await self.order_repository.save(order)

        # 4. Emit event (read model will update)
        await self.event_bus.publish(
            OrderPlacedEvent(
                order_id=order.id,
                customer_id=command.customer_id,
                items=command.items,
                total=order.total
            )
        )

        return order.id


# ============================================
# READ SIDE: Queries
# ============================================

@dataclass
class OrderSummaryReadModel:
    """
    Read Model: Optimized for queries

    Denormalized, no JOINs needed
    Updated by domain events
    """
    order_id: str
    customer_id: str
    customer_name: str  # Denormalized
    customer_email: str  # Denormalized
    status: str
    total: Decimal
    item_count: int
    created_at: datetime

    # Denormalized items (JSON)
    items_summary: dict  # {"product_name": "...", "quantity": 2}

    # Pre-calculated analytics
    is_high_value: bool  # total > $1000
    customer_lifetime_orders: int  # Denormalized


@dataclass
class GetOrderDetailsQuery:
    """Query: Read operation"""
    order_id: str


# Query Handler
class GetOrderDetailsQueryHandler:
    """
    Read side: Handle queries

    Responsibilities:
    - Read from optimized read model
    - No business logic
    - Fast reads
    """

    def __init__(self, read_db: AsyncSession):
        self.read_db = read_db

    async def handle(self, query: GetOrderDetailsQuery) -> OrderSummaryReadModel:
        """
        Handle GetOrderDetailsQuery

        Simple SELECT, no JOINs
        """
        stmt = (
            select(OrderSummaryReadModel)
            .where(OrderSummaryReadModel.order_id == query.order_id)
        )

        result = await self.read_db.execute(stmt)
        order = result.scalar_one_or_none()

        if not order:
            raise OrderNotFoundError(query.order_id)

        return order


# ============================================
# READ MODEL UPDATER: Event Handlers
# ============================================

class OrderReadModelUpdater:
    """
    Update read models based on domain events

    Eventual consistency:
    - Write happens first
    - Read model updates async
    - Brief lag acceptable
    """

    def __init__(self, read_db: AsyncSession, customer_service):
        self.read_db = read_db
        self.customer_service = customer_service

    async def on_order_placed(self, event: OrderPlacedEvent):
        """
        Update read model when order is placed

        Denormalize data for fast reads
        """

        # Fetch customer data (could cache)
        customer = await self.customer_service.get_customer(event.customer_id)

        # Create denormalized read model
        read_model = OrderSummaryReadModel(
            order_id=event.order_id,
            customer_id=event.customer_id,
            customer_name=customer.name,  # Denormalized
            customer_email=customer.email,  # Denormalized
            status='pending',
            total=event.total,
            item_count=len(event.items),
            created_at=event.occurred_at,
            items_summary={
                'products': [
                    {
                        'name': item['product_name'],
                        'quantity': item['quantity'],
                        'price': item['price']
                    }
                    for item in event.items
                ]
            },
            is_high_value=event.total > 1000,
            customer_lifetime_orders=customer.total_orders  # Denormalized
        )

        # Insert into read database
        self.read_db.add(read_model)
        await self.read_db.commit()

        logger.info(
            "read_model_updated",
            order_id=event.order_id,
            event_type="OrderPlaced"
        )

    async def on_order_confirmed(self, event: OrderConfirmedEvent):
        """Update read model status"""
        stmt = (
            update(OrderSummaryReadModel)
            .where(OrderSummaryReadModel.order_id == event.order_id)
            .values(status='confirmed')
        )
        await self.read_db.execute(stmt)
        await self.read_db.commit()


# ============================================
# Application Layer: Command/Query Bus
# ============================================

class CommandBus:
    """
    Command Bus: Route commands to handlers

    Centralized command handling
    """

    def __init__(self):
        self._handlers = {}

    def register(self, command_type: type, handler):
        """Register command handler"""
        self._handlers[command_type] = handler

    async def execute(self, command):
        """Execute command"""
        command_type = type(command)

        if command_type not in self._handlers:
            raise CommandHandlerNotFoundError(command_type)

        handler = self._handlers[command_type]

        logger.info(
            "command_executing",
            command_type=command_type.__name__,
            command_data=command.__dict__
        )

        result = await handler.handle(command)

        logger.info(
            "command_executed",
            command_type=command_type.__name__,
            result=result
        )

        return result


class QueryBus:
    """
    Query Bus: Route queries to handlers

    Read-only operations
    """

    def __init__(self):
        self._handlers = {}

    def register(self, query_type: type, handler):
        """Register query handler"""
        self._handlers[query_type] = handler

    async def execute(self, query):
        """Execute query"""
        query_type = type(query)

        if query_type not in self._handlers:
            raise QueryHandlerNotFoundError(query_type)

        handler = self._handlers[query_type]
        return await handler.handle(query)


# ============================================
# FastAPI Endpoints
# ============================================

app = FastAPI()

# Setup buses
command_bus = CommandBus()
query_bus = QueryBus()

# Register handlers
command_bus.register(PlaceOrderCommand, place_order_handler)
query_bus.register(GetOrderDetailsQuery, get_order_details_handler)


@app.post("/orders")
async def place_order(request: PlaceOrderRequest):
    """
    Write endpoint: Command

    Returns immediately after write
    Read model updates async
    """
    command = PlaceOrderCommand(
        customer_id=request.customer_id,
        items=request.items,
        shipping_address=request.shipping_address
    )

    order_id = await command_bus.execute(command)

    return {
        "order_id": order_id,
        "status": "pending"
    }


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    """
    Read endpoint: Query

    Reads from optimized read model
    Fast, no JOINs
    """
    query = GetOrderDetailsQuery(order_id=order_id)

    order = await query_bus.execute(query)

    return order


# ============================================
# Database Architecture
# ============================================

"""
CQRS Database Options:

OPTION 1: Same DB, Different Tables
┌─────────────────────────────────────┐
│         PostgreSQL                  │
│                                     │
│  Write Side:                        │
│  - orders (normalized)              │
│  - order_items (normalized)         │
│  - customers (normalized)           │
│                                     │
│  Read Side:                         │
│  - order_summaries (denormalized)   │
│  - customer_order_history (denorm)  │
│                                     │
└─────────────────────────────────────┘

OPTION 2: Separate Databases
┌──────────────────┐      ┌──────────────────┐
│  PostgreSQL      │      │  MongoDB         │
│  (Write)         │─────▶│  (Read)          │
│                  │ Events│                  │
│  - orders        │      │  - order_summary │
│  - order_items   │      │  (denormalized)  │
└──────────────────┘      └──────────────────┘

Pros: Optimize each independently
Cons: Eventual consistency complexity

OPTION 3: Materialized Views
┌─────────────────────────────────────┐
│         PostgreSQL                  │
│                                     │
│  Write Tables:                      │
│  - orders                           │
│  - order_items                      │
│                                     │
│  Materialized Views (Read):         │
│  - mv_order_summaries               │
│    REFRESH CONCURRENTLY             │
│                                     │
└─────────────────────────────────────┘

Pros: Simpler (SQL only)
Cons: Less flexible, refresh overhead
"""
```

**CQRS con ElasticSearch para Queries Avanzadas**

```python
# CQRS: Write to PostgreSQL, Read from ElasticSearch

class OrderSearchReadModel:
    """
    Read model in ElasticSearch

    Optimized for:
    - Full-text search
    - Faceted search
    - Analytics aggregations
    """

    async def on_order_placed(self, event: OrderPlacedEvent):
        """Index order in ElasticSearch"""

        document = {
            'order_id': event.order_id,
            'customer_id': event.customer_id,
            'customer_name': event.customer_name,
            'status': 'pending',
            'total': float(event.total),
            'created_at': event.occurred_at.isoformat(),
            'items': [
                {
                    'product_id': item['product_id'],
                    'product_name': item['product_name'],
                    'category': item['category'],
                    'quantity': item['quantity'],
                    'price': float(item['price'])
                }
                for item in event.items
            ],
            # For faceted search
            'tags': self._extract_tags(event.items),
            'price_range': self._get_price_range(event.total)
        }

        await self.es.index(
            index='orders',
            id=event.order_id,
            document=document
        )


# Advanced Query: Search Orders
@dataclass
class SearchOrdersQuery:
    """
    Query with complex filtering

    ElasticSearch handles efficiently
    """
    customer_id: Optional[str] = None
    search_text: Optional[str] = None  # Full-text search
    min_total: Optional[Decimal] = None
    max_total: Optional[Decimal] = None
    status: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    page: int = 1
    page_size: int = 20


class SearchOrdersQueryHandler:
    """Handle complex search queries"""

    def __init__(self, es_client):
        self.es = es_client

    async def handle(self, query: SearchOrdersQuery) -> dict:
        """
        Search orders in ElasticSearch

        Much faster than SQL with multiple WHERE clauses
        """

        # Build ElasticSearch query
        must_clauses = []

        if query.customer_id:
            must_clauses.append({
                'term': {'customer_id': query.customer_id}
            })

        if query.search_text:
            must_clauses.append({
                'multi_match': {
                    'query': query.search_text,
                    'fields': ['customer_name', 'items.product_name']
                }
            })

        if query.min_total or query.max_total:
            range_query = {}
            if query.min_total:
                range_query['gte'] = float(query.min_total)
            if query.max_total:
                range_query['lte'] = float(query.max_total)

            must_clauses.append({
                'range': {'total': range_query}
            })

        if query.status:
            must_clauses.append({
                'term': {'status': query.status}
            })

        # Execute search
        response = await self.es.search(
            index='orders',
            body={
                'query': {
                    'bool': {
                        'must': must_clauses
                    }
                },
                'from': (query.page - 1) * query.page_size,
                'size': query.page_size,
                'sort': [
                    {'created_at': 'desc'}
                ],
                # Aggregations for facets
                'aggs': {
                    'status_counts': {
                        'terms': {'field': 'status'}
                    },
                    'price_ranges': {
                        'range': {
                            'field': 'total',
                            'ranges': [
                                {'to': 50},
                                {'from': 50, 'to': 200},
                                {'from': 200, 'to': 1000},
                                {'from': 1000}
                            ]
                        }
                    }
                }
            }
        )

        return {
            'total': response['hits']['total']['value'],
            'orders': [hit['_source'] for hit in response['hits']['hits']],
            'facets': {
                'status': response['aggregations']['status_counts']['buckets'],
                'price_ranges': response['aggregations']['price_ranges']['buckets']
            }
        }
```

---

## CATEGORÍA 2: Hexagonal Architecture (Ports & Adapters)

### 2.1 Hexagonal Architecture Pattern
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Hexagonal Architecture aísla lógica de negocio de detalles de infraestructura. Permite cambiar DB, frameworks, APIs sin tocar el core.

**Estructura de Capas**

```
┌────────────────────────────────────────────────────┐
│                                                    │
│              INFRASTRUCTURE LAYER                  │
│  (Adapters: FastAPI, PostgreSQL, Redis, etc.)     │
│                                                    │
│  ┌──────────────────────────────────────────┐     │
│  │                                          │     │
│  │         APPLICATION LAYER                │     │
│  │  (Use Cases, Application Services)       │     │
│  │                                          │     │
│  │  ┌────────────────────────────────┐      │     │
│  │  │                                │      │     │
│  │  │       DOMAIN LAYER             │      │     │
│  │  │  (Entities, Value Objects,     │      │     │
│  │  │   Domain Services, Policies)   │      │     │
│  │  │                                │      │     │
│  │  │   ┌──────────────────────┐     │      │     │
│  │  │   │   Business Rules     │     │      │     │
│  │  │   └──────────────────────┘     │      │     │
│  │  │                                │      │     │
│  │  └────────────────────────────────┘      │     │
│  │                                          │     │
│  └──────────────────────────────────────────┘     │
│                                                    │
└────────────────────────────────────────────────────┘

Dependencies flow INWARD:
Infrastructure → Application → Domain
NEVER: Domain → Application
NEVER: Domain → Infrastructure
```

**Implementación: Hexagonal Architecture**

```python
# ============================================
# DOMAIN LAYER (Core, no dependencies)
# ============================================

# Domain Model
@dataclass
class Order:
    """
    Domain Entity: Pure business logic

    NO dependencies on:
    - Database (SQLAlchemy)
    - Framework (FastAPI)
    - External services
    """
    id: OrderId
    customer_id: CustomerId
    items: List[OrderLine]
    status: OrderStatus
    total: Money

    def place_order(self):
        """Business rule"""
        if len(self.items) == 0:
            raise EmptyOrderError()

        if self.total.amount <= 0:
            raise InvalidOrderTotalError()

        self.status = OrderStatus.PLACED

    def add_item(self, product: Product, quantity: int):
        """Business rule"""
        if self.status != OrderStatus.DRAFT:
            raise OrderAlreadyPlacedError()

        line = OrderLine(
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price
        )

        self.items.append(line)
        self._recalculate_total()


# Domain Service
class OrderPricingService:
    """
    Domain Service: Business logic crossing aggregates

    Pure domain logic, no infrastructure
    """

    def calculate_total(
        self,
        items: List[OrderLine],
        customer: Customer,
        pricing_policy: PricingPolicy
    ) -> Money:
        """Calculate order total using policy"""
        base_total = sum(
            item.unit_price.multiply(Decimal(item.quantity))
            for item in items
        )

        # Apply pricing policy
        discount = pricing_policy.calculate_discount(customer, base_total)

        return base_total.subtract(discount)


# ============================================
# PORTS (Interfaces - Domain Layer)
# ============================================

from abc import ABC, abstractmethod

class OrderRepository(ABC):
    """
    Port: Interface for persistence

    Domain defines what it needs
    Infrastructure provides implementation
    """

    @abstractmethod
    async def get_by_id(self, order_id: OrderId) -> Optional[Order]:
        """Get order by ID"""
        pass

    @abstractmethod
    async def save(self, order: Order):
        """Save order"""
        pass

    @abstractmethod
    async def get_by_customer(self, customer_id: CustomerId) -> List[Order]:
        """Get customer orders"""
        pass


class PaymentGateway(ABC):
    """
    Port: Interface for payment processing

    Domain doesn't care HOW payment is processed
    """

    @abstractmethod
    async def charge(
        self,
        customer_id: CustomerId,
        amount: Money,
        payment_method_id: str
    ) -> PaymentResult:
        pass

    @abstractmethod
    async def refund(self, payment_id: str, amount: Money) -> PaymentResult:
        pass


class EmailService(ABC):
    """Port: Email sending"""

    @abstractmethod
    async def send_order_confirmation(
        self,
        customer_email: Email,
        order: Order
    ):
        pass


# ============================================
# APPLICATION LAYER (Use Cases)
# ============================================

class PlaceOrderUseCase:
    """
    Application Service: Orchestrates domain

    Dependencies on PORTS (interfaces), not implementations
    """

    def __init__(
        self,
        order_repository: OrderRepository,  # Port
        payment_gateway: PaymentGateway,    # Port
        email_service: EmailService,        # Port
        pricing_service: OrderPricingService
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway
        self.email_service = email_service
        self.pricing_service = pricing_service

    async def execute(
        self,
        customer_id: CustomerId,
        items: List[dict],
        payment_method_id: str
    ) -> OrderId:
        """
        Place order use case

        Pure business workflow
        No knowledge of FastAPI, PostgreSQL, etc.
        """

        # 1. Create order (domain logic)
        order = Order.create(customer_id)

        for item_data in items:
            product = await self._get_product(item_data['product_id'])
            order.add_item(product, item_data['quantity'])

        # 2. Calculate total (domain service)
        customer = await self._get_customer(customer_id)
        order.total = self.pricing_service.calculate_total(
            order.items,
            customer,
            StandardPricingPolicy()
        )

        # 3. Place order (domain logic)
        order.place_order()

        # 4. Save order (port)
        await self.order_repository.save(order)

        # 5. Process payment (port)
        payment_result = await self.payment_gateway.charge(
            customer_id=customer_id,
            amount=order.total,
            payment_method_id=payment_method_id
        )

        if not payment_result.success:
            raise PaymentFailedError(payment_result.error)

        # 6. Send confirmation (port)
        await self.email_service.send_order_confirmation(
            customer_email=customer.email,
            order=order
        )

        return order.id


# ============================================
# ADAPTERS (Infrastructure Layer)
# ============================================

# Adapter: PostgreSQL Repository
class PostgreSQLOrderRepository(OrderRepository):
    """
    Adapter: Implements OrderRepository port

    Infrastructure detail (PostgreSQL)
    Can be swapped for MongoDB, DynamoDB, etc.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: OrderId) -> Optional[Order]:
        """
        Load from PostgreSQL

        Map ORM model to Domain model
        """
        stmt = (
            select(OrderORM)
            .where(OrderORM.id == order_id.value)
            .options(selectinload(OrderORM.items))
        )

        result = await self.session.execute(stmt)
        order_orm = result.scalar_one_or_none()

        if not order_orm:
            return None

        # Map ORM → Domain
        return self._to_domain(order_orm)

    async def save(self, order: Order):
        """
        Save to PostgreSQL

        Map Domain model to ORM model
        """
        # Map Domain → ORM
        order_orm = self._to_orm(order)

        self.session.add(order_orm)
        await self.session.commit()

    def _to_domain(self, order_orm: OrderORM) -> Order:
        """Map ORM to Domain"""
        return Order(
            id=OrderId(order_orm.id),
            customer_id=CustomerId(order_orm.customer_id),
            items=[
                OrderLine(
                    product_id=ProductId(item.product_id),
                    quantity=item.quantity,
                    unit_price=Money(item.unit_price, 'USD')
                )
                for item in order_orm.items
            ],
            status=OrderStatus(order_orm.status),
            total=Money(order_orm.total, 'USD')
        )

    def _to_orm(self, order: Order) -> OrderORM:
        """Map Domain to ORM"""
        return OrderORM(
            id=order.id.value,
            customer_id=order.customer_id.value,
            status=order.status.value,
            total=order.total.amount,
            items=[
                OrderItemORM(
                    product_id=item.product_id.value,
                    quantity=item.quantity,
                    unit_price=item.unit_price.amount
                )
                for item in order.items
            ]
        )


# Adapter: Stripe Payment Gateway
class StripePaymentGateway(PaymentGateway):
    """
    Adapter: Implements PaymentGateway port

    Infrastructure detail (Stripe)
    Can be swapped for PayPal, Braintree, etc.
    """

    def __init__(self, api_key: str):
        self.stripe = stripe
        self.stripe.api_key = api_key

    async def charge(
        self,
        customer_id: CustomerId,
        amount: Money,
        payment_method_id: str
    ) -> PaymentResult:
        """Charge using Stripe"""
        try:
            payment_intent = await self.stripe.PaymentIntent.create(
                amount=int(amount.amount * 100),  # cents
                currency=amount.currency.lower(),
                customer=customer_id.value,
                payment_method=payment_method_id,
                confirm=True
            )

            return PaymentResult(
                success=True,
                payment_id=payment_intent.id,
                transaction_id=payment_intent.id
            )

        except stripe.error.CardError as e:
            return PaymentResult(
                success=False,
                error=str(e)
            )


# Adapter: SendGrid Email Service
class SendGridEmailService(EmailService):
    """
    Adapter: Implements EmailService port

    Infrastructure detail (SendGrid)
    Can be swapped for AWS SES, Mailgun, etc.
    """

    def __init__(self, api_key: str):
        self.sendgrid = sendgrid.SendGridAPIClient(api_key)

    async def send_order_confirmation(
        self,
        customer_email: Email,
        order: Order
    ):
        """Send email using SendGrid"""
        message = Mail(
            from_email='orders@example.com',
            to_emails=customer_email.value,
            subject=f'Order Confirmation #{order.id.value}',
            html_content=self._render_template(order)
        )

        await self.sendgrid.send(message)


# ============================================
# INFRASTRUCTURE: FastAPI Adapter
# ============================================

app = FastAPI()

# Dependency Injection (wire adapters)
def get_order_repository() -> OrderRepository:
    """Factory: Provide repository implementation"""
    session = get_db_session()
    return PostgreSQLOrderRepository(session)

def get_payment_gateway() -> PaymentGateway:
    """Factory: Provide payment gateway"""
    api_key = os.getenv("STRIPE_API_KEY")
    return StripePaymentGateway(api_key)

def get_email_service() -> EmailService:
    """Factory: Provide email service"""
    api_key = os.getenv("SENDGRID_API_KEY")
    return SendGridEmailService(api_key)

def get_place_order_use_case(
    order_repo: OrderRepository = Depends(get_order_repository),
    payment_gateway: PaymentGateway = Depends(get_payment_gateway),
    email_service: EmailService = Depends(get_email_service)
) -> PlaceOrderUseCase:
    """Factory: Provide use case with dependencies"""
    return PlaceOrderUseCase(
        order_repository=order_repo,
        payment_gateway=payment_gateway,
        email_service=email_service,
        pricing_service=OrderPricingService()
    )


@app.post("/orders")
async def place_order(
    request: PlaceOrderRequest,
    use_case: PlaceOrderUseCase = Depends(get_place_order_use_case)
):
    """
    FastAPI endpoint (Infrastructure layer)

    Delegates to use case (Application layer)
    Use case has no knowledge of FastAPI
    """

    order_id = await use_case.execute(
        customer_id=CustomerId(request.customer_id),
        items=request.items,
        payment_method_id=request.payment_method_id
    )

    return {"order_id": order_id.value}


# ============================================
# TESTING: Easy to test with hexagonal
# ============================================

class InMemoryOrderRepository(OrderRepository):
    """
    Test Adapter: In-memory repository

    No database needed for tests!
    """

    def __init__(self):
        self.orders: Dict[OrderId, Order] = {}

    async def get_by_id(self, order_id: OrderId) -> Optional[Order]:
        return self.orders.get(order_id)

    async def save(self, order: Order):
        self.orders[order.id] = order

    async def get_by_customer(self, customer_id: CustomerId) -> List[Order]:
        return [
            order for order in self.orders.values()
            if order.customer_id == customer_id
        ]


class FakePaymentGateway(PaymentGateway):
    """Test Adapter: Fake payment (always succeeds)"""

    async def charge(self, customer_id, amount, payment_method_id):
        return PaymentResult(
            success=True,
            payment_id='fake_payment_123'
        )


class MockEmailService(EmailService):
    """Test Adapter: Mock email (tracks calls)"""

    def __init__(self):
        self.sent_emails = []

    async def send_order_confirmation(self, customer_email, order):
        self.sent_emails.append({
            'email': customer_email,
            'order_id': order.id
        })


# Test
async def test_place_order_use_case():
    """
    Test use case with test adapters

    No database, no Stripe, no SendGrid needed!
    """

    # Arrange: Test adapters
    order_repo = InMemoryOrderRepository()
    payment_gateway = FakePaymentGateway()
    email_service = MockEmailService()

    use_case = PlaceOrderUseCase(
        order_repository=order_repo,
        payment_gateway=payment_gateway,
        email_service=email_service,
        pricing_service=OrderPricingService()
    )

    # Act
    order_id = await use_case.execute(
        customer_id=CustomerId('customer_123'),
        items=[
            {'product_id': 'prod_1', 'quantity': 2}
        ],
        payment_method_id='pm_123'
    )

    # Assert
    saved_order = await order_repo.get_by_id(order_id)
    assert saved_order is not None
    assert saved_order.status == OrderStatus.PLACED
    assert len(email_service.sent_emails) == 1
```

---

## CATEGORÍA 3: Clean Architecture

### 3.1 Clean Architecture con Dependency Rule
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Clean Architecture similar a Hexagonal, pero con capas más explícitas y Dependency Rule estricta.

**Dependency Rule:**

```
┌──────────────────────────────────────────────┐
│  FRAMEWORKS & DRIVERS (outermost)           │
│  - Web (FastAPI)                            │
│  - DB (SQLAlchemy)                          │
│  - External APIs                            │
│                                             │
│  ┌────────────────────────────────────────┐ │
│  │  INTERFACE ADAPTERS                    │ │
│  │  - Controllers                         │ │
│  │  - Presenters                          │ │
│  │  - Gateways                            │ │
│  │                                        │ │
│  │  ┌──────────────────────────────────┐  │ │
│  │  │  USE CASES (Application Business │  │ │
│  │  │  Rules)                          │  │ │
│  │  │  - Interactors                   │  │ │
│  │  │  - Input/Output Ports            │  │ │
│  │  │                                  │  │ │
│  │  │  ┌────────────────────────────┐  │  │ │
│  │  │  │  ENTITIES                  │  │  │ │
│  │  │  │  (Enterprise Business      │  │  │ │
│  │  │  │   Rules)                   │  │  │ │
│  │  │  │  - Domain models           │  │  │ │
│  │  │  │  - Business logic          │  │  │ │
│  │  │  └────────────────────────────┘  │  │ │
│  │  └──────────────────────────────────┘  │ │
│  └────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘

RULE: Dependencies point INWARD only
Source code dependencies can only point inward
```

**Implementación: Clean Architecture**

```python
# ============================================
# ENTITIES LAYER (innermost)
# ============================================

class Order:
    """
    Entity: Enterprise business rules

    Pure business logic
    Independent of use cases
    """

    def __init__(self, order_id: str, customer_id: str):
        self.id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.status = OrderStatus.DRAFT

    def add_item(self, product_id: str, quantity: int, price: Decimal):
        """Business rule: Add item"""
        if self.status != OrderStatus.DRAFT:
            raise InvalidOperationError("Cannot modify confirmed order")

        self.items.append(OrderItem(product_id, quantity, price))

    def calculate_total(self) -> Decimal:
        """Business rule: Calculate total"""
        return sum(
            item.price * item.quantity
            for item in self.items
        )

    def confirm(self):
        """Business rule: Confirm order"""
        if not self.items:
            raise InvalidOperationError("Cannot confirm empty order")

        self.status = OrderStatus.CONFIRMED


# ============================================
# USE CASES LAYER
# ============================================

# Input Port (Interface)
@dataclass
class PlaceOrderInputData:
    """Input data for use case"""
    customer_id: str
    items: List[dict]
    payment_method_id: str


# Output Port (Interface)
@dataclass
class PlaceOrderOutputData:
    """Output data from use case"""
    order_id: str
    status: str
    total: Decimal


class PlaceOrderOutputBoundary(ABC):
    """
    Output Boundary: How use case presents results

    Interface defined by use case
    Implemented by presenter (outer layer)
    """

    @abstractmethod
    def present_success(self, output_data: PlaceOrderOutputData):
        """Present successful order placement"""
        pass

    @abstractmethod
    def present_error(self, error: Exception):
        """Present error"""
        pass


# Data Access Interface (defined by use case)
class OrderDataAccess(ABC):
    """
    Data Access Interface

    Use case defines what it needs
    Gateway implements it
    """

    @abstractmethod
    async def save_order(self, order: Order):
        pass

    @abstractmethod
    async def get_product(self, product_id: str) -> Product:
        pass


# Use Case Interactor
class PlaceOrderInteractor:
    """
    Use Case Interactor: Application business rules

    Orchestrates entities
    Depends on interfaces (ports), not implementations
    """

    def __init__(
        self,
        order_data_access: OrderDataAccess,
        payment_gateway: PaymentGateway,
        output_boundary: PlaceOrderOutputBoundary
    ):
        self.order_data_access = order_data_access
        self.payment_gateway = payment_gateway
        self.output_boundary = output_boundary

    async def execute(self, input_data: PlaceOrderInputData):
        """
        Execute use case

        Business workflow
        """
        try:
            # 1. Create entity
            order = Order(
                order_id=str(uuid.uuid4()),
                customer_id=input_data.customer_id
            )

            # 2. Add items (entity business rules)
            for item in input_data.items:
                product = await self.order_data_access.get_product(
                    item['product_id']
                )
                order.add_item(
                    product_id=product.id,
                    quantity=item['quantity'],
                    price=product.price
                )

            # 3. Calculate total (entity business rules)
            total = order.calculate_total()

            # 4. Process payment (gateway)
            payment_result = await self.payment_gateway.charge(
                customer_id=input_data.customer_id,
                amount=total,
                payment_method_id=input_data.payment_method_id
            )

            if not payment_result.success:
                raise PaymentFailedError(payment_result.error)

            # 5. Confirm order (entity business rules)
            order.confirm()

            # 6. Save (data access)
            await self.order_data_access.save_order(order)

            # 7. Present result (output boundary)
            output_data = PlaceOrderOutputData(
                order_id=order.id,
                status=order.status.value,
                total=total
            )

            self.output_boundary.present_success(output_data)

        except Exception as e:
            self.output_boundary.present_error(e)


# ============================================
# INTERFACE ADAPTERS LAYER
# ============================================

# Controller (converts HTTP → Input Data)
class OrderController:
    """
    Controller: Adapter from web to use case

    Converts HTTP request to input data
    """

    def __init__(self, place_order_interactor: PlaceOrderInteractor):
        self.interactor = place_order_interactor

    async def place_order(self, request: PlaceOrderHTTPRequest):
        """
        Handle HTTP request

        Convert to use case input data
        """
        input_data = PlaceOrderInputData(
            customer_id=request.customer_id,
            items=request.items,
            payment_method_id=request.payment_method_id
        )

        await self.interactor.execute(input_data)


# Presenter (converts Output Data → HTTP Response)
class OrderPresenter(PlaceOrderOutputBoundary):
    """
    Presenter: Adapter from use case to web

    Converts output data to HTTP response
    """

    def __init__(self):
        self.response = None

    def present_success(self, output_data: PlaceOrderOutputData):
        """Format success response"""
        self.response = {
            "success": True,
            "data": {
                "order_id": output_data.order_id,
                "status": output_data.status,
                "total": float(output_data.total)
            }
        }

    def present_error(self, error: Exception):
        """Format error response"""
        self.response = {
            "success": False,
            "error": {
                "type": type(error).__name__,
                "message": str(error)
            }
        }

    def get_response(self):
        """Get formatted response"""
        return self.response


# Gateway (implements Data Access)
class OrderDatabaseGateway(OrderDataAccess):
    """
    Gateway: Adapter to database

    Implements interface defined by use case
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_order(self, order: Order):
        """Save to database"""
        order_orm = OrderORM(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status.value,
            total=order.calculate_total()
        )

        self.session.add(order_orm)
        await self.session.commit()

    async def get_product(self, product_id: str) -> Product:
        """Get product from database"""
        stmt = select(ProductORM).where(ProductORM.id == product_id)
        result = await self.session.execute(stmt)
        product_orm = result.scalar_one()

        return Product(
            id=product_orm.id,
            name=product_orm.name,
            price=product_orm.price
        )


# ============================================
# FRAMEWORKS & DRIVERS LAYER (outermost)
# ============================================

app = FastAPI()

@app.post("/orders")
async def place_order_endpoint(
    request: PlaceOrderHTTPRequest,
    session: AsyncSession = Depends(get_db)
):
    """
    FastAPI endpoint

    Wires everything together
    """

    # Create dependencies (outer layers)
    data_access = OrderDatabaseGateway(session)
    payment_gateway = StripePaymentGateway(os.getenv("STRIPE_KEY"))
    presenter = OrderPresenter()

    # Create use case (with dependencies)
    interactor = PlaceOrderInteractor(
        order_data_access=data_access,
        payment_gateway=payment_gateway,
        output_boundary=presenter
    )

    # Create controller
    controller = OrderController(interactor)

    # Execute
    await controller.place_order(request)

    # Return formatted response
    return presenter.get_response()
```

---

## CATEGORÍA 4: Anti-Corruption Layer (ACL)

### 4.1 Anti-Corruption Layer Pattern
**Dificultad:** ⭐⭐⭐⭐ **ALTA**

**Contexto:**
Al integrar con sistemas legacy o external APIs, ACL protege tu domain model de ser "contaminado" por modelos externos.

**Implementación: ACL para Legacy System**

```python
# ============================================
# EXTERNAL SYSTEM (Legacy, can't change)
# ============================================

# Legacy system returns complex XML
legacy_customer_xml = """
<CUSTOMER>
    <CUST_ID>12345</CUST_ID>
    <FNAME>John</FNAME>
    <LNAME>Doe</LNAME>
    <EMAIL_ADDR>john@example.com</EMAIL_ADDR>
    <ACCT_STATUS>A</ACCT_STATUS>
    <CREDIT_LMT>5000.00</CREDIT_LMT>
    <TIER_CD>PRM</TIER_CD>
</CUSTOMER>
"""


# ============================================
# YOUR DOMAIN MODEL (Clean)
# ============================================

@dataclass
class Customer:
    """
    Your clean domain model

    Should NOT be influenced by legacy system
    """
    id: CustomerId
    name: PersonName  # Value object
    email: Email      # Value object
    is_active: bool
    credit_limit: Money
    tier: CustomerTier


# ============================================
# ANTI-CORRUPTION LAYER
# ============================================

class LegacyCustomerAdapter:
    """
    Anti-Corruption Layer: Translate legacy to domain

    Prevents legacy model from polluting domain
    """

    def __init__(self, legacy_client: LegacySystemClient):
        self.legacy_client = legacy_client

    async def get_customer(self, customer_id: CustomerId) -> Customer:
        """
        Fetch from legacy, translate to domain model

        Isolation: Domain never sees legacy XML structure
        """

        # 1. Fetch from legacy (XML)
        legacy_xml = await self.legacy_client.get_customer_xml(
            customer_id.value
        )

        # 2. Parse legacy format
        legacy_data = self._parse_legacy_xml(legacy_xml)

        # 3. Translate to domain model
        return self._translate_to_domain(legacy_data)

    def _parse_legacy_xml(self, xml_string: str) -> dict:
        """Parse legacy XML"""
        import xml.etree.ElementTree as ET

        root = ET.fromstring(xml_string)

        return {
            'cust_id': root.find('CUST_ID').text,
            'fname': root.find('FNAME').text,
            'lname': root.find('LNAME').text,
            'email_addr': root.find('EMAIL_ADDR').text,
            'acct_status': root.find('ACCT_STATUS').text,
            'credit_lmt': root.find('CREDIT_LMT').text,
            'tier_cd': root.find('TIER_CD').text
        }

    def _translate_to_domain(self, legacy_data: dict) -> Customer:
        """
        Translate legacy data to domain model

        Mapping layer: Protects domain from legacy formats
        """

        # Translate ID
        customer_id = CustomerId(legacy_data['cust_id'])

        # Translate name (combine first + last)
        name = PersonName(
            first=legacy_data['fname'],
            last=legacy_data['lname']
        )

        # Translate email
        email = Email(legacy_data['email_addr'])

        # Translate status ('A' → True, else False)
        is_active = legacy_data['acct_status'] == 'A'

        # Translate credit limit
        credit_limit = Money(
            Decimal(legacy_data['credit_lmt']),
            'USD'
        )

        # Translate tier code
        tier_mapping = {
            'STD': CustomerTier.STANDARD,
            'PRM': CustomerTier.PREMIUM,
            'VIP': CustomerTier.VIP
        }
        tier = tier_mapping.get(
            legacy_data['tier_cd'],
            CustomerTier.STANDARD
        )

        return Customer(
            id=customer_id,
            name=name,
            email=email,
            is_active=is_active,
            credit_limit=credit_limit,
            tier=tier
        )

    async def save_customer(self, customer: Customer):
        """
        Save to legacy system

        Translate domain model back to legacy format
        """

        # Translate domain → legacy
        legacy_data = self._translate_from_domain(customer)

        # Convert to XML
        legacy_xml = self._build_legacy_xml(legacy_data)

        # Save to legacy
        await self.legacy_client.update_customer_xml(legacy_xml)

    def _translate_from_domain(self, customer: Customer) -> dict:
        """Translate domain model to legacy format"""
        return {
            'cust_id': customer.id.value,
            'fname': customer.name.first,
            'lname': customer.name.last,
            'email_addr': customer.email.value,
            'acct_status': 'A' if customer.is_active else 'I',
            'credit_lmt': str(customer.credit_limit.amount),
            'tier_cd': {
                CustomerTier.STANDARD: 'STD',
                CustomerTier.PREMIUM: 'PRM',
                CustomerTier.VIP: 'VIP'
            }[customer.tier]
        }


# ============================================
# USAGE IN DOMAIN
# ============================================

class OrderService:
    """
    Domain service

    Works with clean Customer model
    No knowledge of legacy XML
    """

    def __init__(self, customer_adapter: LegacyCustomerAdapter):
        self.customer_adapter = customer_adapter

    async def place_order(self, customer_id: CustomerId, items: List):
        """
        Place order

        Uses ACL to fetch customer data
        """

        # Fetch customer (ACL handles translation)
        customer = await self.customer_adapter.get_customer(customer_id)

        # Use clean domain model
        if not customer.is_active:
            raise InactiveCustomerError()

        # Calculate total
        total = self._calculate_total(items)

        # Check credit limit (clean domain logic)
        if total > customer.credit_limit:
            raise CreditLimitExceededError()

        # ... continue with order placement
```

---

## Decisiones Consolidadas 2026

```
┌──────────────────────────────────────────────────────────────┐
│    CQRS & HEXAGONAL ARCHITECTURE - CHECKLIST 2026            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. CQRS                                                      │
│    ├─ [ ] Separate write models (aggregates)                │
│    ├─ [ ] Separate read models (denormalized)               │
│    ├─ [ ] Command bus for writes                            │
│    ├─ [ ] Query bus for reads                               │
│    ├─ [ ] Event handlers update read models                 │
│    └─ [ ] ElasticSearch for complex queries                 │
│                                                              │
│ 2. HEXAGONAL ARCHITECTURE                                    │
│    ├─ [ ] Domain layer (no external dependencies)           │
│    ├─ [ ] Ports (interfaces defined by domain)              │
│    ├─ [ ] Adapters (implementations in infrastructure)      │
│    ├─ [ ] Dependency inversion (domain independent)         │
│    └─ [ ] Test adapters for easy testing                    │
│                                                              │
│ 3. CLEAN ARCHITECTURE                                        │
│    ├─ [ ] Entities (enterprise business rules)              │
│    ├─ [ ] Use cases (application business rules)            │
│    ├─ [ ] Interface adapters (controllers, presenters)      │
│    ├─ [ ] Frameworks & drivers (outermost)                  │
│    └─ [ ] Dependency rule (inward only)                     │
│                                                              │
│ 4. ANTI-CORRUPTION LAYER                                     │
│    ├─ [ ] ACL for legacy system integration                 │
│    ├─ [ ] Translate external models to domain               │
│    ├─ [ ] Protect domain from external changes              │
│    └─ [ ] Facade pattern for complex integrations           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Conclusión:**

Este archivo cubre patrones arquitectónicos avanzados para 2026:

1. **CQRS**: Separación de escritura y lectura con read models optimizados, ElasticSearch integration
2. **Hexagonal Architecture**: Ports & Adapters, dependency inversion, easy testing
3. **Clean Architecture**: Capas explícitas, dependency rule, use cases
4. **Anti-Corruption Layer**: Proteger domain de sistemas legacy y external APIs

Todos los patrones incluyen implementaciones completas en Python con ejemplos de testing, mapeo de modelos, y dependency injection.
