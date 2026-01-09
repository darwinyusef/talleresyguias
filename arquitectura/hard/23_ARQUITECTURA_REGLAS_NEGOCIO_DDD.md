# Arquitectura: Reglas de Negocio y DDD Táctico 2026

## Objetivo
Domain-Driven Design enfocado en modelar reglas de negocio complejas, invariantes, políticas, y workflows usando patrones tácticos.

---

## CATEGORÍA 1: Business Rules y Domain Model

### 1.1 Specification Pattern para Reglas de Negocio
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Las reglas de negocio cambian frecuentemente. Specification Pattern permite encapsular reglas complejas, combinarlas, y reutilizarlas.

**Problema: Reglas de Negocio Hardcoded**

```python
# ❌ BAD: Business rules scattered y hardcoded
class OrderService:
    async def can_place_order(self, user: User, order: Order) -> bool:
        """
        Problemas:
        - Reglas mezcladas con lógica de aplicación
        - Difícil testear reglas individualmente
        - Difícil cambiar reglas (require code change)
        - No reutilizable
        """
        # Rule 1: User must be active
        if not user.is_active:
            return False

        # Rule 2: User must have verified email
        if not user.email_verified:
            return False

        # Rule 3: Order total must be > 0
        if order.total <= 0:
            return False

        # Rule 4: User must not exceed credit limit
        pending_orders = await self._get_pending_orders(user.id)
        total_pending = sum(o.total for o in pending_orders)
        if total_pending + order.total > user.credit_limit:
            return False

        # Rule 5: Premium users can order anytime
        # Regular users only during business hours
        if user.tier != "premium":
            current_hour = datetime.utcnow().hour
            if current_hour < 9 or current_hour > 18:
                return False

        return True
```

**✅ GOOD: Specification Pattern**

```python
# Specification Pattern: Encapsular reglas de negocio
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar('T')

class Specification(ABC, Generic[T]):
    """
    Base Specification

    Permite:
    - Encapsular business rules
    - Combinar reglas (AND, OR, NOT)
    - Testear reglas aisladas
    - Reutilizar reglas
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if candidate satisfies specification"""
        pass

    def and_(self, other: 'Specification[T]') -> 'Specification[T]':
        """Combine specifications with AND"""
        return AndSpecification(self, other)

    def or_(self, other: 'Specification[T]') -> 'Specification[T]':
        """Combine specifications with OR"""
        return OrSpecification(self, other)

    def not_(self) -> 'Specification[T]':
        """Negate specification"""
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return (
            self.left.is_satisfied_by(candidate) and
            self.right.is_satisfied_by(candidate)
        )


class OrSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return (
            self.left.is_satisfied_by(candidate) or
            self.right.is_satisfied_by(candidate)
        )


class NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]):
        self.spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self.spec.is_satisfied_by(candidate)


# Concrete Specifications for User
class UserIsActiveSpecification(Specification[User]):
    """User must be active"""

    def is_satisfied_by(self, user: User) -> bool:
        return user.is_active

    def __str__(self):
        return "User must be active"


class UserEmailVerifiedSpecification(Specification[User]):
    """User email must be verified"""

    def is_satisfied_by(self, user: User) -> bool:
        return user.email_verified

    def __str__(self):
        return "User email must be verified"


class UserHasAvailableCreditSpecification(Specification[User]):
    """
    User must have available credit

    Async specification: requires additional data
    """

    def __init__(self, order_total: Decimal, order_repository):
        self.order_total = order_total
        self.order_repository = order_repository

    async def is_satisfied_by_async(self, user: User) -> bool:
        """Async version for DB queries"""
        pending_orders = await self.order_repository.get_pending_orders(user.id)
        total_pending = sum(o.total for o in pending_orders)
        return total_pending + self.order_total <= user.credit_limit

    def __str__(self):
        return f"User must have available credit for {self.order_total}"


class UserCanOrderAtCurrentTimeSpecification(Specification[User]):
    """
    Premium users: anytime
    Regular users: business hours only
    """

    def is_satisfied_by(self, user: User) -> bool:
        if user.tier == "premium":
            return True

        current_hour = datetime.utcnow().hour
        return 9 <= current_hour <= 18

    def __str__(self):
        return "User can order at current time"


# Concrete Specifications for Order
class OrderHasPositiveTotalSpecification(Specification[Order]):
    """Order total must be > 0"""

    def is_satisfied_by(self, order: Order) -> bool:
        return order.total > 0

    def __str__(self):
        return "Order total must be positive"


class OrderItemsInStockSpecification(Specification[Order]):
    """All order items must be in stock"""

    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    async def is_satisfied_by_async(self, order: Order) -> bool:
        for item in order.items:
            available = await self.inventory_service.check_stock(
                item.product_id,
                item.quantity
            )
            if not available:
                return False
        return True

    def __str__(self):
        return "All order items must be in stock"


# Composite Specifications
class CanPlaceOrderSpecification:
    """
    Composite specification: Combina todas las reglas

    Ventajas:
    - Reglas declarativas
    - Fácil agregar/remover reglas
    - Testeable
    - Reutilizable
    """

    def __init__(self, order_repository, inventory_service):
        self.order_repository = order_repository
        self.inventory_service = inventory_service

    def create_specification(self, order: Order) -> Specification[User]:
        """
        Build composite specification

        Rules:
        1. User is active
        2. User email verified
        3. User can order at current time
        """
        return (
            UserIsActiveSpecification()
            .and_(UserEmailVerifiedSpecification())
            .and_(UserCanOrderAtCurrentTimeSpecification())
        )

    async def is_satisfied_by(self, user: User, order: Order) -> tuple[bool, list[str]]:
        """
        Check all specifications

        Returns: (is_satisfied, reasons)
        """
        violations = []

        # Sync specifications
        user_spec = self.create_specification(order)
        if not user_spec.is_satisfied_by(user):
            violations.append("User requirements not met")

        # Order specification
        order_spec = OrderHasPositiveTotalSpecification()
        if not order_spec.is_satisfied_by(order):
            violations.append(str(order_spec))

        # Async specifications
        credit_spec = UserHasAvailableCreditSpecification(
            order.total,
            self.order_repository
        )
        if not await credit_spec.is_satisfied_by_async(user):
            violations.append(str(credit_spec))

        stock_spec = OrderItemsInStockSpecification(self.inventory_service)
        if not await stock_spec.is_satisfied_by_async(order):
            violations.append(str(stock_spec))

        return (len(violations) == 0, violations)


# Usage in Application Service
class OrderApplicationService:
    def __init__(
        self,
        order_repository,
        inventory_service,
        can_place_order_spec: CanPlaceOrderSpecification
    ):
        self.order_repository = order_repository
        self.inventory_service = inventory_service
        self.can_place_order_spec = can_place_order_spec

    async def place_order(self, user: User, order: Order):
        """
        Application service con specifications

        Business logic está en specifications
        Application service solo orquesta
        """
        # Check specifications
        can_place, violations = await self.can_place_order_spec.is_satisfied_by(
            user,
            order
        )

        if not can_place:
            raise BusinessRuleViolationError(
                "Cannot place order",
                violations=violations
            )

        # Process order
        order.status = OrderStatus.PENDING
        await self.order_repository.save(order)

        return order


# Testing Specifications (isolated)
class TestUserSpecifications:
    """
    Test specifications en aislamiento

    Ventaja: No necesitas mock de services
    """

    def test_user_is_active_specification(self):
        spec = UserIsActiveSpecification()

        active_user = User(is_active=True)
        assert spec.is_satisfied_by(active_user) is True

        inactive_user = User(is_active=False)
        assert spec.is_satisfied_by(inactive_user) is False

    def test_user_can_order_at_current_time(self):
        spec = UserCanOrderAtCurrentTimeSpecification()

        # Premium user can order anytime
        premium_user = User(tier="premium")
        assert spec.is_satisfied_by(premium_user) is True

        # Regular user during business hours
        # (mock time if needed)

    def test_composite_specification(self):
        """Test combined specifications"""
        spec = (
            UserIsActiveSpecification()
            .and_(UserEmailVerifiedSpecification())
        )

        valid_user = User(is_active=True, email_verified=True)
        assert spec.is_satisfied_by(valid_user) is True

        invalid_user = User(is_active=True, email_verified=False)
        assert spec.is_satisfied_by(invalid_user) is False
```

**Specification Pattern con SQL (Query Object)**

```python
# Specification to SQL (para queries)
class SqlSpecification(Specification[T]):
    """
    Specification que se puede convertir a SQL

    Permite filtrar en DB en vez de en memoria
    """

    @abstractmethod
    def to_sql(self) -> Select:
        """Convert specification to SQLAlchemy query"""
        pass


class UserIsActiveSpecificationSql(SqlSpecification[User]):
    def to_sql(self) -> Select:
        return select(User).where(User.is_active == True)

    def is_satisfied_by(self, user: User) -> bool:
        return user.is_active


class UserEmailVerifiedSpecificationSql(SqlSpecification[User]):
    def to_sql(self) -> Select:
        return select(User).where(User.email_verified == True)

    def is_satisfied_by(self, user: User) -> bool:
        return user.email_verified


class AndSpecificationSql(SqlSpecification[T]):
    def __init__(self, left: SqlSpecification[T], right: SqlSpecification[T]):
        self.left = left
        self.right = right

    def to_sql(self) -> Select:
        """Combine SQL queries with AND"""
        left_query = self.left.to_sql()
        right_query = self.right.to_sql()

        # Extract WHERE clauses and combine
        return select(User).where(
            and_(
                left_query.whereclause,
                right_query.whereclause
            )
        )

    def is_satisfied_by(self, candidate: T) -> bool:
        return (
            self.left.is_satisfied_by(candidate) and
            self.right.is_satisfied_by(candidate)
        )


# Usage: Filter in database
class UserRepository:
    async def find_by_specification(
        self,
        spec: SqlSpecification[User]
    ) -> List[User]:
        """
        Find users matching specification

        Ejecuta query en DB (eficiente)
        En vez de cargar todos y filtrar en memoria
        """
        query = spec.to_sql()
        result = await self.session.execute(query)
        return result.scalars().all()


# Example
spec = (
    UserIsActiveSpecificationSql()
    .and_(UserEmailVerifiedSpecificationSql())
)

# This generates SQL:
# SELECT * FROM users WHERE is_active = true AND email_verified = true
eligible_users = await user_repository.find_by_specification(spec)
```

---

## CATEGORÍA 2: Value Objects con Reglas de Negocio

### 2.1 Value Objects y Validaciones
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Value Objects encapsulan reglas de negocio y garantizan invariantes. Son immutables y se comparan por valor.

**Implementación: Value Objects Avanzados**

```python
# Value Objects with Business Rules
from dataclasses import dataclass
from typing import ClassVar
import re

@dataclass(frozen=True)
class Email:
    """
    Email Value Object

    Invariants:
    - Must be valid email format
    - Must not be from disposable email provider
    - Domain must be lowercase

    Ventajas:
    - Imposible crear Email inválido
    - Validación en un solo lugar
    - Type safety (Email vs str)
    """

    value: str

    # Class-level configuration
    DISPOSABLE_DOMAINS: ClassVar[set[str]] = {
        'tempmail.com', 'guerrillamail.com', '10minutemail.com'
    }

    EMAIL_REGEX: ClassVar[re.Pattern] = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    def __post_init__(self):
        """
        Validate on construction

        Raises ValueError if invalid
        """
        # Normalize
        normalized = self.value.strip().lower()
        object.__setattr__(self, 'value', normalized)

        # Validate format
        if not self.EMAIL_REGEX.match(self.value):
            raise ValueError(f"Invalid email format: {self.value}")

        # Business rule: No disposable emails
        domain = self.value.split('@')[1]
        if domain in self.DISPOSABLE_DOMAINS:
            raise ValueError(f"Disposable email not allowed: {domain}")

    @property
    def domain(self) -> str:
        """Extract domain"""
        return self.value.split('@')[1]

    @property
    def local_part(self) -> str:
        """Extract local part"""
        return self.value.split('@')[0]

    def is_corporate_email(self) -> bool:
        """
        Business rule: Corporate emails

        Not gmail, yahoo, hotmail, etc.
        """
        public_domains = {'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'}
        return self.domain not in public_domains


@dataclass(frozen=True)
class Money:
    """
    Money Value Object

    Invariants:
    - Amount and currency always together
    - Precision: 2 decimals
    - Currency must be valid ISO code

    Business rules:
    - Cannot add different currencies
    - Comparisons only within same currency
    """

    amount: Decimal
    currency: str

    VALID_CURRENCIES: ClassVar[set[str]] = {
        'USD', 'EUR', 'GBP', 'JPY', 'MXN', 'BRL', 'ARS'
    }

    def __post_init__(self):
        # Validate currency
        if self.currency not in self.VALID_CURRENCIES:
            raise ValueError(f"Invalid currency: {self.currency}")

        # Normalize precision
        normalized_amount = self.amount.quantize(Decimal('0.01'))
        object.__setattr__(self, 'amount', normalized_amount)

        # Business rule: No negative money (use separate sign)
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

    def add(self, other: 'Money') -> 'Money':
        """
        Add money

        Business rule: Same currency required
        """
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add different currencies: {self.currency} and {other.currency}"
            )

        return Money(self.amount + other.amount, self.currency)

    def subtract(self, other: 'Money') -> 'Money':
        """Subtract money"""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot subtract different currencies"
            )

        result_amount = self.amount - other.amount
        if result_amount < 0:
            raise ValueError("Result would be negative")

        return Money(result_amount, self.currency)

    def multiply(self, factor: Decimal) -> 'Money':
        """Multiply by factor"""
        return Money(self.amount * factor, self.currency)

    def __eq__(self, other) -> bool:
        """Equality by value"""
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other: 'Money') -> bool:
        """Less than (same currency only)"""
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.amount < other.amount

    def __str__(self) -> str:
        return f"{self.currency} {self.amount}"


@dataclass(frozen=True)
class PhoneNumber:
    """
    Phone Number Value Object

    Business rules:
    - Must be valid format for country
    - Must be mobile (not landline) for SMS
    - International format preferred
    """

    value: str
    country_code: str

    def __post_init__(self):
        """Validate phone number"""
        # Remove formatting
        digits_only = re.sub(r'[^0-9+]', '', self.value)
        object.__setattr__(self, 'value', digits_only)

        # Validate format (simple check)
        if not digits_only.startswith('+'):
            raise ValueError("Phone must start with country code (+)")

        if len(digits_only) < 10:
            raise ValueError("Phone number too short")

    def is_mobile(self) -> bool:
        """
        Business rule: Check if mobile

        Simplified (real impl would use libphonenumber)
        """
        # Mexico mobile starts with +521
        if self.country_code == 'MX':
            return self.value.startswith('+521')

        # US/Canada mobile (all numbers potentially mobile)
        if self.country_code in ['US', 'CA']:
            return True

        return False

    def can_receive_sms(self) -> bool:
        """Business rule: Can receive SMS"""
        return self.is_mobile()


@dataclass(frozen=True)
class DateRange:
    """
    Date Range Value Object

    Invariants:
    - start_date <= end_date
    - No null dates

    Business rules:
    - Max duration limits
    - Overlap detection
    """

    start_date: date
    end_date: date

    def __post_init__(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must be <= end_date")

    @property
    def duration_days(self) -> int:
        """Duration in days"""
        return (self.end_date - self.start_date).days

    def overlaps_with(self, other: 'DateRange') -> bool:
        """Check if overlaps with another range"""
        return (
            self.start_date <= other.end_date and
            self.end_date >= other.start_date
        )

    def contains_date(self, check_date: date) -> bool:
        """Check if date is in range"""
        return self.start_date <= check_date <= self.end_date

    def is_valid_for_booking(self) -> bool:
        """
        Business rule: Booking constraints

        - Min 1 day
        - Max 30 days
        - Must be future dates
        """
        if self.duration_days < 1:
            return False

        if self.duration_days > 30:
            return False

        if self.start_date < date.today():
            return False

        return True


# Usage in Entity
@dataclass
class Customer:
    """
    Entity with Value Objects

    Value Objects enforce invariants
    """
    id: CustomerId
    email: Email  # Value Object (always valid)
    phone: PhoneNumber  # Value Object
    credit_limit: Money  # Value Object

    def update_email(self, new_email: str):
        """
        Update email

        Validation automatic (Email constructor)
        """
        self.email = Email(new_email)  # Raises if invalid

    def can_purchase(self, amount: Money) -> bool:
        """
        Business rule: Can purchase

        Money Value Object ensures same currency comparison
        """
        return amount < self.credit_limit

    def increase_credit_limit(self, increase: Money):
        """Increase credit limit"""
        # Money.add() ensures same currency
        self.credit_limit = self.credit_limit.add(increase)


# Testing Value Objects
class TestMoneyValueObject:
    def test_cannot_create_negative_money(self):
        with pytest.raises(ValueError):
            Money(Decimal("-10.00"), "USD")

    def test_cannot_add_different_currencies(self):
        usd = Money(Decimal("10.00"), "USD")
        eur = Money(Decimal("10.00"), "EUR")

        with pytest.raises(ValueError):
            usd.add(eur)

    def test_money_equality_by_value(self):
        money1 = Money(Decimal("10.00"), "USD")
        money2 = Money(Decimal("10.00"), "USD")

        assert money1 == money2
        assert money1 is not money2  # Different instances

    def test_precision_normalized(self):
        money = Money(Decimal("10.999"), "USD")
        assert money.amount == Decimal("11.00")  # Rounded
```

---

## CATEGORÍA 3: Domain Events y Event Sourcing

### 3.1 Domain Events para Business Logic
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Domain Events representan hechos del negocio que ya ocurrieron. Permiten desacoplar bounded contexts y triggers side effects.

**Implementación: Domain Events System**

```python
# Domain Events Infrastructure
from dataclasses import dataclass, field
from typing import List, Callable, Dict, Type
from datetime import datetime
import uuid

@dataclass
class DomainEvent:
    """
    Base Domain Event

    Represents something that happened in the domain
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    aggregate_id: str = ""
    aggregate_type: str = ""

    def to_dict(self) -> dict:
        """Serialize to dict (for event store)"""
        return {
            'event_id': self.event_id,
            'event_type': self.__class__.__name__,
            'occurred_at': self.occurred_at.isoformat(),
            'aggregate_id': self.aggregate_id,
            'aggregate_type': self.aggregate_type,
            'data': self.__dict__
        }


# Concrete Domain Events
@dataclass
class OrderPlacedEvent(DomainEvent):
    """Order was placed"""
    order_id: str = ""
    customer_id: str = ""
    total_amount: Decimal = Decimal("0")
    items: List[dict] = field(default_factory=list)

    def __post_init__(self):
        self.aggregate_id = self.order_id
        self.aggregate_type = "Order"


@dataclass
class OrderConfirmedEvent(DomainEvent):
    """Order was confirmed (payment successful)"""
    order_id: str = ""
    confirmed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class OrderCancelledEvent(DomainEvent):
    """Order was cancelled"""
    order_id: str = ""
    cancellation_reason: str = ""


@dataclass
class PaymentProcessedEvent(DomainEvent):
    """Payment was processed"""
    payment_id: str = ""
    order_id: str = ""
    amount: Decimal = Decimal("0")


@dataclass
class InventoryReservedEvent(DomainEvent):
    """Inventory was reserved"""
    product_id: str = ""
    quantity: int = 0
    order_id: str = ""


# Event Handler Registry
class DomainEventHandler:
    """
    Domain Event Dispatcher

    Decouples event producers from consumers
    """

    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}

    def subscribe(
        self,
        event_type: Type[DomainEvent],
        handler: Callable
    ):
        """
        Subscribe handler to event type

        Multiple handlers can subscribe to same event
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent):
        """
        Publish event to all subscribers

        Handlers execute in order
        """
        event_type = type(event)

        if event_type not in self._handlers:
            return

        for handler in self._handlers[event_type]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)

            except Exception as e:
                logger.error(
                    "domain_event_handler_failed",
                    event_type=event_type.__name__,
                    handler=handler.__name__,
                    error=str(e)
                )


# Event-Driven Aggregate
class Order:
    """
    Aggregate Root with Domain Events

    Events record what happened
    """

    def __init__(self, order_id: str, customer_id: str):
        self.id = order_id
        self.customer_id = customer_id
        self.items: List[OrderLine] = []
        self.status = OrderStatus.DRAFT
        self.total = Money(Decimal("0"), "USD")

        # Pending events (not persisted yet)
        self._pending_events: List[DomainEvent] = []

    def add_item(self, product_id: str, quantity: int, price: Money):
        """
        Add item to order

        Emits domain event
        """
        # Business rule
        if self.status != OrderStatus.DRAFT:
            raise InvalidOperationError("Cannot modify confirmed order")

        # Modify state
        line = OrderLine(product_id, quantity, price)
        self.items.append(line)
        self.total = self.total.add(price.multiply(Decimal(quantity)))

        # Emit event
        event = ItemAddedToOrderEvent(
            order_id=self.id,
            product_id=product_id,
            quantity=quantity,
            price=price.amount
        )
        self._pending_events.append(event)

    def place_order(self):
        """
        Place order

        Transitions status and emits event
        """
        # Business rules
        if self.status != OrderStatus.DRAFT:
            raise InvalidOperationError("Order already placed")

        if len(self.items) == 0:
            raise InvalidOperationError("Cannot place empty order")

        if self.total.amount <= 0:
            raise InvalidOperationError("Order total must be positive")

        # Change state
        self.status = OrderStatus.PENDING

        # Emit domain event
        event = OrderPlacedEvent(
            order_id=self.id,
            customer_id=self.customer_id,
            total_amount=self.total.amount,
            items=[
                {
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'price': item.price.amount
                }
                for item in self.items
            ]
        )
        self._pending_events.append(event)

    def confirm_order(self):
        """Confirm order (payment successful)"""
        if self.status != OrderStatus.PENDING:
            raise InvalidOperationError("Cannot confirm order in current status")

        self.status = OrderStatus.CONFIRMED

        # Emit event
        event = OrderConfirmedEvent(order_id=self.id)
        self._pending_events.append(event)

    def cancel_order(self, reason: str):
        """Cancel order"""
        if self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise InvalidOperationError("Cannot cancel shipped/delivered order")

        self.status = OrderStatus.CANCELLED

        # Emit event
        event = OrderCancelledEvent(
            order_id=self.id,
            cancellation_reason=reason
        )
        self._pending_events.append(event)

    def get_pending_events(self) -> List[DomainEvent]:
        """Get events not yet published"""
        return self._pending_events.copy()

    def clear_pending_events(self):
        """Clear events after publishing"""
        self._pending_events.clear()


# Repository with Event Publishing
class OrderRepository:
    """
    Repository that publishes domain events

    Pattern: After persisting aggregate, publish events
    """

    def __init__(
        self,
        session: AsyncSession,
        event_handler: DomainEventHandler
    ):
        self.session = session
        self.event_handler = event_handler

    async def save(self, order: Order):
        """
        Save aggregate and publish events

        Transaction: DB + Events (or use Outbox pattern)
        """
        # 1. Persist aggregate
        self.session.add(order)
        await self.session.commit()

        # 2. Publish events
        events = order.get_pending_events()
        for event in events:
            await self.event_handler.publish(event)

        # 3. Clear events
        order.clear_pending_events()


# Event Handlers (Side Effects)
class OrderEventHandlers:
    """
    Event handlers for Order domain events

    Each handler is a side effect of domain event
    """

    def __init__(
        self,
        email_service,
        inventory_service,
        analytics_service
    ):
        self.email_service = email_service
        self.inventory_service = inventory_service
        self.analytics_service = analytics_service

    async def on_order_placed(self, event: OrderPlacedEvent):
        """
        When order is placed:
        - Reserve inventory
        - Send confirmation email
        - Track analytics
        """
        logger.info(
            "order_placed_event_received",
            order_id=event.order_id,
            customer_id=event.customer_id
        )

        # Reserve inventory (async)
        for item in event.items:
            await self.inventory_service.reserve(
                product_id=item['product_id'],
                quantity=item['quantity'],
                order_id=event.order_id
            )

        # Send email (async)
        await self.email_service.send_order_confirmation(
            customer_id=event.customer_id,
            order_id=event.order_id
        )

        # Track analytics
        await self.analytics_service.track_event(
            event_name="order_placed",
            user_id=event.customer_id,
            properties={
                'order_id': event.order_id,
                'total_amount': float(event.total_amount),
                'item_count': len(event.items)
            }
        )

    async def on_order_confirmed(self, event: OrderConfirmedEvent):
        """When order is confirmed: Notify warehouse"""
        await self.warehouse_service.notify_new_order(event.order_id)

    async def on_order_cancelled(self, event: OrderCancelledEvent):
        """
        When order is cancelled:
        - Release inventory
        - Refund payment (if applicable)
        - Send cancellation email
        """
        await self.inventory_service.release_reservation(event.order_id)

        # Trigger refund process
        await self.event_handler.publish(
            RefundRequestedEvent(order_id=event.order_id)
        )


# Wire up handlers
event_handler = DomainEventHandler()
order_handlers = OrderEventHandlers(email_service, inventory_service, analytics)

event_handler.subscribe(OrderPlacedEvent, order_handlers.on_order_placed)
event_handler.subscribe(OrderConfirmedEvent, order_handlers.on_order_confirmed)
event_handler.subscribe(OrderCancelledEvent, order_handlers.on_order_cancelled)


# Application Service (uses domain events)
class PlaceOrderUseCase:
    """
    Use case: Place order

    Domain events decouple side effects
    """

    def __init__(
        self,
        order_repository: OrderRepository,
        payment_service,
        event_handler: DomainEventHandler
    ):
        self.order_repository = order_repository
        self.payment_service = payment_service
        self.event_handler = event_handler

    async def execute(self, customer_id: str, items: List[dict]) -> str:
        """
        Place order use case

        Flow:
        1. Create order (emits events)
        2. Save order (publishes events)
        3. Events trigger side effects automatically
        """
        # Create order
        order = Order(
            order_id=str(uuid.uuid4()),
            customer_id=customer_id
        )

        # Add items
        for item in items:
            order.add_item(
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=Money(Decimal(item['price']), 'USD')
            )

        # Place order (emits OrderPlacedEvent)
        order.place_order()

        # Save (publishes events)
        # Events trigger: inventory reservation, email, analytics
        await self.order_repository.save(order)

        # Process payment
        try:
            payment = await self.payment_service.charge(
                customer_id=customer_id,
                amount=order.total
            )

            # Confirm order (emits OrderConfirmedEvent)
            order.confirm_order()
            await self.order_repository.save(order)

        except PaymentError as e:
            # Cancel order (emits OrderCancelledEvent)
            # Event triggers: inventory release, refund
            order.cancel_order(reason="Payment failed")
            await self.order_repository.save(order)
            raise

        return order.id
```

**Event Sourcing Pattern**

```python
# Event Sourcing: Rebuild state from events
class EventSourcedAggregate:
    """
    Aggregate rebuilt from event stream

    State is derived from events (not stored directly)
    """

    def __init__(self, aggregate_id: str):
        self.id = aggregate_id
        self._version = 0
        self._pending_events: List[DomainEvent] = []

    def apply_event(self, event: DomainEvent):
        """
        Apply event to aggregate

        Mutates state based on event type
        """
        event_type = type(event).__name__
        handler_name = f"_apply_{event_type}"

        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            handler(event)

        self._version += 1

    def load_from_history(self, events: List[DomainEvent]):
        """Rebuild aggregate from event stream"""
        for event in events:
            self.apply_event(event)


class EventSourcedOrder(EventSourcedAggregate):
    """
    Order aggregate with event sourcing

    State derived from events
    """

    def __init__(self, order_id: str):
        super().__init__(order_id)
        self.customer_id = ""
        self.items: List[dict] = []
        self.status = OrderStatus.DRAFT
        self.total = Decimal("0")

    # Event application methods
    def _apply_OrderPlacedEvent(self, event: OrderPlacedEvent):
        """Apply OrderPlaced event"""
        self.customer_id = event.customer_id
        self.items = event.items
        self.total = event.total_amount
        self.status = OrderStatus.PENDING

    def _apply_OrderConfirmedEvent(self, event: OrderConfirmedEvent):
        """Apply OrderConfirmed event"""
        self.status = OrderStatus.CONFIRMED

    def _apply_OrderCancelledEvent(self, event: OrderCancelledEvent):
        """Apply OrderCancelled event"""
        self.status = OrderStatus.CANCELLED

    # Commands (emit events)
    def place_order(self, customer_id: str, items: List[dict], total: Decimal):
        """Command: Place order"""
        event = OrderPlacedEvent(
            order_id=self.id,
            customer_id=customer_id,
            items=items,
            total_amount=total
        )

        # Apply event (change state)
        self.apply_event(event)

        # Add to pending (for persistence)
        self._pending_events.append(event)


# Event Store
class EventStore:
    """
    Store for domain events

    Events are append-only (immutable)
    """

    async def append_events(
        self,
        aggregate_id: str,
        events: List[DomainEvent],
        expected_version: int
    ):
        """
        Append events to stream

        Optimistic concurrency: expected_version
        """
        for event in events:
            await self.db.execute(
                insert(EventStoreTable).values(
                    aggregate_id=aggregate_id,
                    event_type=type(event).__name__,
                    event_data=event.to_dict(),
                    version=expected_version,
                    occurred_at=event.occurred_at
                )
            )
            expected_version += 1

        await self.db.commit()

    async def get_events(
        self,
        aggregate_id: str,
        from_version: int = 0
    ) -> List[DomainEvent]:
        """Get event stream for aggregate"""
        stmt = (
            select(EventStoreTable)
            .where(EventStoreTable.aggregate_id == aggregate_id)
            .where(EventStoreTable.version >= from_version)
            .order_by(EventStoreTable.version)
        )

        result = await self.db.execute(stmt)
        rows = result.fetchall()

        # Deserialize events
        events = []
        for row in rows:
            event_class = globals()[row.event_type]  # Get event class
            event = event_class(**row.event_data)
            events.append(event)

        return events


# Repository for Event Sourced Aggregate
class EventSourcedOrderRepository:
    """Repository for event sourced orders"""

    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    async def get(self, order_id: str) -> EventSourcedOrder:
        """
        Load order from events

        No SELECT from orders table
        Rebuild from event stream
        """
        events = await self.event_store.get_events(order_id)

        if not events:
            raise OrderNotFoundError(order_id)

        # Rebuild aggregate
        order = EventSourcedOrder(order_id)
        order.load_from_history(events)

        return order

    async def save(self, order: EventSourcedOrder):
        """
        Save order (append events)

        No UPDATE orders table
        Append new events to stream
        """
        pending = order.get_pending_events()

        await self.event_store.append_events(
            aggregate_id=order.id,
            events=pending,
            expected_version=order._version
        )

        order.clear_pending_events()
```

---

## CATEGORÍA 4: Policy Pattern para Business Rules

### 4.1 Policy Pattern
**Dificultad:** ⭐⭐⭐⭐ **ALTA**

**Contexto:**
Policies son business rules que dependen de múltiples aggregates o external services. Viven en Domain Services.

**Implementación: Pricing Policy**

```python
# Policy Pattern: Business Rules que requieren múltiples aggregates
from abc import ABC, abstractmethod

class PricingPolicy(ABC):
    """
    Pricing Policy: Calculate price based on rules

    Business rules:
    - Base price
    - Volume discounts
    - Customer tier discounts
    - Seasonal promotions
    - Geographic pricing
    """

    @abstractmethod
    async def calculate_price(
        self,
        product: Product,
        customer: Customer,
        quantity: int,
        context: PricingContext
    ) -> Money:
        pass


@dataclass
class PricingContext:
    """Context for pricing calculation"""
    order_date: datetime
    customer_location: str
    is_promotional_period: bool = False
    promo_code: Optional[str] = None


class StandardPricingPolicy(PricingPolicy):
    """
    Standard pricing policy

    Rules:
    1. Base price from product
    2. Volume discount (>10 items = 10% off, >50 = 20% off)
    3. Customer tier (premium = 5% off, vip = 10% off)
    4. Seasonal promotion (if active)
    """

    def __init__(self, promotion_repository):
        self.promotion_repository = promotion_repository

    async def calculate_price(
        self,
        product: Product,
        customer: Customer,
        quantity: int,
        context: PricingContext
    ) -> Money:
        """Calculate final price"""

        # 1. Base price
        base_price = product.price

        # 2. Volume discount
        volume_discount = self._calculate_volume_discount(quantity)
        price_after_volume = base_price.multiply(
            Decimal(1 - volume_discount)
        )

        # 3. Customer tier discount
        tier_discount = self._calculate_tier_discount(customer)
        price_after_tier = price_after_volume.multiply(
            Decimal(1 - tier_discount)
        )

        # 4. Promotional discount
        promo_discount = await self._calculate_promotional_discount(
            product,
            context
        )
        final_price = price_after_tier.multiply(
            Decimal(1 - promo_discount)
        )

        # 5. Total for quantity
        total = final_price.multiply(Decimal(quantity))

        logger.info(
            "price_calculated",
            product_id=product.id,
            customer_id=customer.id,
            quantity=quantity,
            base_price=base_price.amount,
            volume_discount=volume_discount,
            tier_discount=tier_discount,
            promo_discount=promo_discount,
            final_unit_price=final_price.amount,
            total=total.amount
        )

        return total

    def _calculate_volume_discount(self, quantity: int) -> float:
        """Volume discount policy"""
        if quantity >= 50:
            return 0.20  # 20% off
        elif quantity >= 10:
            return 0.10  # 10% off
        return 0.0

    def _calculate_tier_discount(self, customer: Customer) -> float:
        """Customer tier discount policy"""
        tier_discounts = {
            'vip': 0.10,      # 10% off
            'premium': 0.05,  # 5% off
            'standard': 0.0
        }
        return tier_discounts.get(customer.tier, 0.0)

    async def _calculate_promotional_discount(
        self,
        product: Product,
        context: PricingContext
    ) -> float:
        """Promotional discount policy"""
        if not context.is_promotional_period:
            return 0.0

        # Check active promotions
        promotions = await self.promotion_repository.get_active_promotions(
            product_id=product.id,
            date=context.order_date
        )

        if not promotions:
            return 0.0

        # Return highest discount
        return max(promo.discount_percentage for promo in promotions)


# Geographic Pricing Policy
class GeographicPricingPolicy(PricingPolicy):
    """
    Geographic pricing: Different prices per region

    Business rule: Adjust for local market, taxes, shipping
    """

    REGIONAL_MULTIPLIERS = {
        'US': 1.0,
        'EU': 1.15,  # Higher due to VAT
        'LATAM': 0.85,  # Lower purchasing power
        'ASIA': 0.90
    }

    async def calculate_price(
        self,
        product: Product,
        customer: Customer,
        quantity: int,
        context: PricingContext
    ) -> Money:
        """Calculate price with geographic adjustment"""

        base_price = product.price

        # Get regional multiplier
        region = self._get_region(context.customer_location)
        multiplier = self.REGIONAL_MULTIPLIERS.get(region, 1.0)

        # Apply multiplier
        regional_price = base_price.multiply(Decimal(multiplier))
        total = regional_price.multiply(Decimal(quantity))

        return total

    def _get_region(self, location: str) -> str:
        """Map location to region"""
        # Simplified
        country_to_region = {
            'US': 'US',
            'MX': 'LATAM',
            'BR': 'LATAM',
            'DE': 'EU',
            'FR': 'EU',
            'JP': 'ASIA'
        }
        return country_to_region.get(location, 'US')


# Composite Policy (Chain of Responsibility)
class CompositePricingPolicy(PricingPolicy):
    """
    Combine multiple policies

    Applies policies in order
    """

    def __init__(self, policies: List[PricingPolicy]):
        self.policies = policies

    async def calculate_price(
        self,
        product: Product,
        customer: Customer,
        quantity: int,
        context: PricingContext
    ) -> Money:
        """Apply all policies in sequence"""

        price = product.price.multiply(Decimal(quantity))

        for policy in self.policies:
            price = await policy.calculate_price(
                product,
                customer,
                quantity,
                context
            )

        return price


# Usage in Domain Service
class OrderPricingService:
    """
    Domain Service: Calculate order price

    Uses policies (pluggable business rules)
    """

    def __init__(self, pricing_policy: PricingPolicy):
        self.pricing_policy = pricing_policy

    async def calculate_order_total(
        self,
        customer: Customer,
        items: List[OrderLineData],
        context: PricingContext
    ) -> Money:
        """Calculate total order price"""

        total = Money(Decimal("0"), "USD")

        for item in items:
            product = await self._get_product(item.product_id)

            item_price = await self.pricing_policy.calculate_price(
                product=product,
                customer=customer,
                quantity=item.quantity,
                context=context
            )

            total = total.add(item_price)

        return total


# Configure policies
standard_policy = StandardPricingPolicy(promotion_repository)
geographic_policy = GeographicPricingPolicy()

# Combine policies
pricing_policy = CompositePricingPolicy([
    geographic_policy,  # Apply first
    standard_policy     # Apply second
])

# Inject into service
pricing_service = OrderPricingService(pricing_policy)
```

---

## Decisiones Consolidadas 2026

```
┌──────────────────────────────────────────────────────────────┐
│      DDD TÁCTICO Y REGLAS DE NEGOCIO - CHECKLIST 2026        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. SPECIFICATION PATTERN                                     │
│    ├─ [ ] Specifications para business rules complejas      │
│    ├─ [ ] Combinar specs con AND/OR/NOT                     │
│    ├─ [ ] Convert to SQL para filtering en DB               │
│    └─ [ ] Test specifications en aislamiento                │
│                                                              │
│ 2. VALUE OBJECTS                                             │
│    ├─ [ ] Value Objects para conceptos del dominio          │
│    ├─ [ ] Invariants en __post_init__                       │
│    ├─ [ ] Immutability (frozen=True)                        │
│    ├─ [ ] Business rules en Value Objects                   │
│    └─ [ ] Type safety (Email vs str)                        │
│                                                              │
│ 3. DOMAIN EVENTS                                             │
│    ├─ [ ] Events para facts del negocio                     │
│    ├─ [ ] Event handlers para side effects                  │
│    ├─ [ ] Event store para auditing                         │
│    ├─ [ ] Event sourcing para critical aggregates           │
│    └─ [ ] Decouple bounded contexts con events              │
│                                                              │
│ 4. POLICY PATTERN                                            │
│    ├─ [ ] Policies para rules que cruzan aggregates         │
│    ├─ [ ] Pluggable policies (strategy pattern)             │
│    ├─ [ ] Composite policies para combinar rules            │
│    └─ [ ] Domain services con policies                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Conclusión:**

Este archivo cubre DDD táctico enfocado en reglas de negocio:

1. **Specification Pattern**: Encapsular y combinar business rules de manera testeable
2. **Value Objects**: Invariants, validaciones, y business rules en objetos inmutables
3. **Domain Events**: Representar hechos del negocio, desacoplar side effects
4. **Policy Pattern**: Business rules complejas que requieren múltiples aggregates

Todos los patrones incluyen implementaciones completas en Python con ejemplos de uso en agregados, servicios de dominio, y casos de uso.
