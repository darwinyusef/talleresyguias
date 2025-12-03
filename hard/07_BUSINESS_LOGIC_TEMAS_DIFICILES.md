# Conocimientos Técnicos Difíciles: Business Logic & Domain Modeling

## Objetivo
Temas complejos de lógica de negocio, modelado de dominio y reglas empresariales que un arquitecto debe dominar para apoyar efectivamente a developers en la implementación de requisitos de negocio complejos.

---

## CATEGORÍA 1: Domain-Driven Design (DDD)

### 1.1 Aggregate Design y Consistency Boundaries
**Dificultad:** ⭐⭐⭐⭐⭐

**Concepto:** Un aggregate es un cluster de objetos de dominio que se tratan como una unidad para cambios de datos.

```python
# ❌ Malo: Aggregate demasiado grande, problemas de concurrencia
class Order:
    def __init__(self):
        self.id = None
        self.customer = Customer()  # Aggregate completo dentro
        self.items = []
        self.payment = Payment()
        self.shipment = Shipment()
        self.invoice = Invoice()

    def add_item(self, product, quantity):
        # Bloquea TODO el aggregate para agregar un item
        self.items.append(OrderItem(product, quantity))
        self.recalculate_total()

# ✅ Bueno: Aggregates pequeños con boundaries claros
class Order:
    """Aggregate Root: Solo Order se puede acceder desde afuera"""
    def __init__(self, customer_id: CustomerId):
        self.id = OrderId.generate()
        self.customer_id = customer_id  # Solo referencia por ID
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._version = 0  # Para optimistic locking

    def add_item(self, product_id: ProductId, quantity: int, unit_price: Money):
        # Validar invariantes del aggregate
        if self.status != OrderStatus.PENDING:
            raise InvalidOperationError("Cannot add items to non-pending order")

        if quantity <= 0:
            raise ValidationError("Quantity must be positive")

        # Verificar límite de items
        if len(self.items) >= 100:
            raise BusinessRuleViolation("Order cannot have more than 100 items")

        item = OrderItem(product_id, quantity, unit_price)
        self.items.append(item)

        # Emitir evento de dominio
        self.add_domain_event(OrderItemAdded(self.id, product_id, quantity))

    def submit(self):
        # Validar invariantes
        if not self.items:
            raise BusinessRuleViolation("Cannot submit empty order")

        self.status = OrderStatus.SUBMITTED
        self.add_domain_event(OrderSubmitted(self.id, self.total()))

    def total(self) -> Money:
        return sum(item.subtotal() for item in self.items)

class OrderItem:
    """Entity dentro del aggregate (no aggregate root)"""
    def __init__(self, product_id: ProductId, quantity: int, unit_price: Money):
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

    def subtotal(self) -> Money:
        return self.unit_price * self.quantity

# Aggregate separado: Payment
class Payment:
    """Aggregate Root separado - consistencia eventual con Order"""
    def __init__(self, order_id: OrderId, amount: Money):
        self.id = PaymentId.generate()
        self.order_id = order_id
        self.amount = amount
        self.status = PaymentStatus.PENDING

    def process(self, payment_method: PaymentMethod):
        if self.status != PaymentStatus.PENDING:
            raise InvalidOperationError("Payment already processed")

        # Procesar pago...
        self.status = PaymentStatus.COMPLETED
        self.add_domain_event(PaymentCompleted(self.id, self.order_id))

# Repository por aggregate
class OrderRepository:
    def get(self, order_id: OrderId) -> Order:
        # Load aggregate completo
        pass

    def save(self, order: Order):
        # Save aggregate completo atomically
        # + Publicar domain events
        pass
```

**Reglas para Aggregate Boundaries:**

```python
# 1. Proteger invariantes de negocio
class BankAccount:
    """Aggregate: Garantiza que balance nunca sea negativo"""
    def __init__(self, account_number: str):
        self.account_number = account_number
        self._balance = Money(0)
        self._transactions = []

    def deposit(self, amount: Money):
        if amount <= 0:
            raise ValidationError("Amount must be positive")

        self._balance += amount
        self._transactions.append(
            Transaction(TransactionType.DEPOSIT, amount)
        )

    def withdraw(self, amount: Money):
        if amount <= 0:
            raise ValidationError("Amount must be positive")

        # INVARIANTE: Balance no puede ser negativo
        if self._balance - amount < 0:
            raise InsufficientFundsError()

        self._balance -= amount
        self._transactions.append(
            Transaction(TransactionType.WITHDRAWAL, amount)
        )

# 2. Referencias entre aggregates: solo por ID
class OrderLine:
    def __init__(self, product_id: ProductId, quantity: int):
        # ✅ Referencia por ID
        self.product_id = product_id
        self.quantity = quantity

        # ❌ NO: referencia a aggregate completo
        # self.product = Product()

# 3. Actualizar múltiples aggregates: usar Domain Events
class OrderService:
    def submit_order(self, order_id: OrderId):
        # 1. Cargar y modificar primer aggregate
        order = self.order_repo.get(order_id)
        order.submit()
        self.order_repo.save(order)  # Publica OrderSubmitted event

        # 2. Event handler actualiza otros aggregates (async)
        # No en misma transacción - consistencia eventual

@event_handler
def handle_order_submitted(event: OrderSubmitted):
    # Actualizar inventory aggregate
    inventory = inventory_repo.get(event.product_id)
    inventory.reserve(event.quantity)
    inventory_repo.save(inventory)

    # Crear payment aggregate
    payment = Payment(event.order_id, event.total)
    payment_repo.save(payment)
```

---

### 1.2 Value Objects y Ubiquitous Language
**Dificultad:** ⭐⭐⭐⭐

```python
# ❌ Malo: Primitive Obsession
def transfer_money(from_account: str, to_account: str, amount: float, currency: str):
    if amount <= 0:
        raise ValueError("Invalid amount")
    if currency not in ['USD', 'EUR', 'GBP']:
        raise ValueError("Invalid currency")
    # ...

# ✅ Bueno: Value Objects con validación y comportamiento
@dataclass(frozen=True)  # Immutable
class Money:
    """Value Object: Se compara por valor, no por identidad"""
    amount: Decimal
    currency: Currency

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Cannot add {self.currency} and {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, multiplier: int) -> 'Money':
        return Money(self.amount * multiplier, self.currency)

    def is_greater_than(self, other: 'Money') -> bool:
        self._assert_same_currency(other)
        return self.amount > other.amount

@dataclass(frozen=True)
class AccountNumber:
    """Value Object: Encapsula validación"""
    value: str

    def __post_init__(self):
        if not self.value.isalnum():
            raise ValueError("Account number must be alphanumeric")
        if len(self.value) != 10:
            raise ValueError("Account number must be 10 characters")

@dataclass(frozen=True)
class Email:
    """Value Object: Valida formato"""
    value: str

    def __post_init__(self):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.value):
            raise ValueError("Invalid email format")

    @property
    def domain(self) -> str:
        return self.value.split('@')[1]

# Uso con Value Objects
def transfer_money(
    from_account: AccountNumber,
    to_account: AccountNumber,
    amount: Money
):
    # Validación ya garantizada por Value Objects
    # Código más expresivo
    if amount.is_greater_than(Money(Decimal(10000), Currency.USD)):
        # Requires approval for large transfers
        pass

# Value Objects compuestos
@dataclass(frozen=True)
class Address:
    street: str
    city: str
    state: str
    zip_code: ZipCode
    country: Country

    def is_domestic(self) -> bool:
        return self.country == Country.USA

    def same_city_as(self, other: 'Address') -> bool:
        return self.city == other.city and self.country == other.country

@dataclass(frozen=True)
class DateRange:
    """Value Object: Encapsula lógica de rangos"""
    start: date
    end: date

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start date must be before end date")

    def contains(self, date: date) -> bool:
        return self.start <= date <= self.end

    def overlaps(self, other: 'DateRange') -> bool:
        return (
            self.start <= other.end and
            other.start <= self.end
        )

    def days_count(self) -> int:
        return (self.end - self.start).days + 1

# Uso en entidades
class Reservation:
    def __init__(self, room_id: RoomId, guest: Guest, period: DateRange):
        self.room_id = room_id
        self.guest = guest
        self.period = period

    def conflicts_with(self, other: 'Reservation') -> bool:
        return (
            self.room_id == other.room_id and
            self.period.overlaps(other.period)
        )
```

---

### 1.3 Domain Events y Event Sourcing
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

# 1. Domain Events
@dataclass(frozen=True)
class DomainEvent:
    """Base para todos los domain events"""
    event_id: UUID
    aggregate_id: UUID
    occurred_at: datetime
    version: int

@dataclass(frozen=True)
class AccountOpened(DomainEvent):
    account_number: str
    owner_name: str
    initial_balance: Decimal

@dataclass(frozen=True)
class MoneyDeposited(DomainEvent):
    amount: Decimal

@dataclass(frozen=True)
class MoneyWithdrawn(DomainEvent):
    amount: Decimal

@dataclass(frozen=True)
class AccountClosed(DomainEvent):
    reason: str

# 2. Event-Sourced Aggregate
class BankAccount:
    """Aggregate reconstruido desde eventos"""
    def __init__(self, account_id: UUID):
        self.account_id = account_id
        self.account_number = None
        self.owner_name = None
        self.balance = Decimal(0)
        self.is_closed = False
        self.version = 0

        # Eventos no guardados
        self._uncommitted_events: List[DomainEvent] = []

    # Factory method
    @classmethod
    def open(cls, account_number: str, owner_name: str, initial_balance: Decimal):
        account = cls(uuid4())
        event = AccountOpened(
            event_id=uuid4(),
            aggregate_id=account.account_id,
            occurred_at=datetime.utcnow(),
            version=1,
            account_number=account_number,
            owner_name=owner_name,
            initial_balance=initial_balance
        )
        account._apply_event(event)
        account._uncommitted_events.append(event)
        return account

    # Commands (generate events)
    def deposit(self, amount: Decimal):
        if self.is_closed:
            raise AccountClosedError()

        if amount <= 0:
            raise InvalidAmountError()

        event = MoneyDeposited(
            event_id=uuid4(),
            aggregate_id=self.account_id,
            occurred_at=datetime.utcnow(),
            version=self.version + 1,
            amount=amount
        )
        self._apply_event(event)
        self._uncommitted_events.append(event)

    def withdraw(self, amount: Decimal):
        if self.is_closed:
            raise AccountClosedError()

        if amount <= 0:
            raise InvalidAmountError()

        if self.balance - amount < 0:
            raise InsufficientFundsError()

        event = MoneyWithdrawn(
            event_id=uuid4(),
            aggregate_id=self.account_id,
            occurred_at=datetime.utcnow(),
            version=self.version + 1,
            amount=amount
        )
        self._apply_event(event)
        self._uncommitted_events.append(event)

    # Apply events (change state)
    def _apply_event(self, event: DomainEvent):
        if isinstance(event, AccountOpened):
            self.account_number = event.account_number
            self.owner_name = event.owner_name
            self.balance = event.initial_balance

        elif isinstance(event, MoneyDeposited):
            self.balance += event.amount

        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount

        elif isinstance(event, AccountClosed):
            self.is_closed = True

        self.version = event.version

    # Reconstruction from events
    @classmethod
    def from_events(cls, events: List[DomainEvent]):
        if not events:
            raise ValueError("Cannot reconstruct from empty event list")

        first_event = events[0]
        if not isinstance(first_event, AccountOpened):
            raise ValueError("First event must be AccountOpened")

        account = cls(first_event.aggregate_id)
        for event in events:
            account._apply_event(event)

        return account

    def get_uncommitted_events(self) -> List[DomainEvent]:
        return self._uncommitted_events.copy()

    def mark_events_as_committed(self):
        self._uncommitted_events.clear()

# 3. Event Store
class EventStore:
    def __init__(self):
        # En producción: PostgreSQL, EventStoreDB, etc.
        self._events: Dict[UUID, List[DomainEvent]] = {}

    def save_events(self, aggregate_id: UUID, events: List[DomainEvent], expected_version: int):
        # Optimistic concurrency
        current_events = self._events.get(aggregate_id, [])
        current_version = len(current_events)

        if current_version != expected_version:
            raise ConcurrencyError(
                f"Expected version {expected_version}, but current is {current_version}"
            )

        # Append events
        if aggregate_id not in self._events:
            self._events[aggregate_id] = []

        self._events[aggregate_id].extend(events)

        # Publicar eventos para event handlers
        for event in events:
            self._publish_event(event)

    def get_events(self, aggregate_id: UUID) -> List[DomainEvent]:
        return self._events.get(aggregate_id, []).copy()

    def _publish_event(self, event: DomainEvent):
        # Publicar a message bus para event handlers
        event_bus.publish(event)

# 4. Repository con Event Sourcing
class EventSourcedAccountRepository:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def get(self, account_id: UUID) -> BankAccount:
        events = self.event_store.get_events(account_id)
        if not events:
            raise AccountNotFoundError(account_id)

        return BankAccount.from_events(events)

    def save(self, account: BankAccount):
        uncommitted_events = account.get_uncommitted_events()
        if not uncommitted_events:
            return

        expected_version = account.version - len(uncommitted_events)

        self.event_store.save_events(
            account.account_id,
            uncommitted_events,
            expected_version
        )

        account.mark_events_as_committed()

# 5. Snapshots para performance
class Snapshot:
    def __init__(self, aggregate_id: UUID, version: int, state: dict):
        self.aggregate_id = aggregate_id
        self.version = version
        self.state = state
        self.created_at = datetime.utcnow()

class SnapshotStore:
    def save_snapshot(self, aggregate_id: UUID, account: BankAccount):
        snapshot = Snapshot(
            aggregate_id=aggregate_id,
            version=account.version,
            state={
                'account_number': account.account_number,
                'owner_name': account.owner_name,
                'balance': str(account.balance),
                'is_closed': account.is_closed
            }
        )
        # Save to storage...

    def get_snapshot(self, aggregate_id: UUID) -> Optional[Snapshot]:
        # Load from storage...
        pass

class OptimizedAccountRepository:
    def __init__(self, event_store: EventStore, snapshot_store: SnapshotStore):
        self.event_store = event_store
        self.snapshot_store = snapshot_store

    def get(self, account_id: UUID) -> BankAccount:
        # 1. Try to get snapshot
        snapshot = self.snapshot_store.get_snapshot(account_id)

        if snapshot:
            # 2. Load only events after snapshot
            events = self.event_store.get_events_after_version(
                account_id,
                snapshot.version
            )

            # 3. Reconstruct from snapshot + new events
            account = BankAccount(account_id)
            account._restore_from_snapshot(snapshot.state)

            for event in events:
                account._apply_event(event)

            return account
        else:
            # Full reconstruction from all events
            events = self.event_store.get_events(account_id)
            return BankAccount.from_events(events)

    def save(self, account: BankAccount):
        # Save events
        uncommitted_events = account.get_uncommitted_events()
        if uncommitted_events:
            self.event_store.save_events(
                account.account_id,
                uncommitted_events,
                account.version - len(uncommitted_events)
            )
            account.mark_events_as_committed()

        # Create snapshot every 100 events
        if account.version % 100 == 0:
            self.snapshot_store.save_snapshot(account.account_id, account)

# Uso
repo = EventSourcedAccountRepository(event_store)

# Crear cuenta
account = BankAccount.open("ACC123", "John Doe", Decimal(1000))
repo.save(account)

# Modificar cuenta
account = repo.get(account.account_id)
account.deposit(Decimal(500))
account.withdraw(Decimal(200))
repo.save(account)

# Reconstruir historia completa
events = event_store.get_events(account.account_id)
for event in events:
    print(f"{event.occurred_at}: {event.__class__.__name__} - {event}")
```

---

## CATEGORÍA 2: Complex Business Rules

### 2.1 Specification Pattern
**Dificultad:** ⭐⭐⭐⭐

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Specification(ABC, Generic[T]):
    """Base para reglas de negocio complejas"""

    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        pass

    def and_(self, other: 'Specification[T]') -> 'AndSpecification[T]':
        return AndSpecification(self, other)

    def or_(self, other: 'Specification[T]') -> 'OrSpecification[T]':
        return OrSpecification(self, other)

    def not_(self) -> 'NotSpecification[T]':
        return NotSpecification(self)

# Composite specifications
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

# Ejemplo: Reglas de préstamo bancario
@dataclass
class LoanApplication:
    applicant_age: int
    annual_income: Decimal
    credit_score: int
    debt_to_income_ratio: float
    employment_years: int
    loan_amount: Decimal

# Specifications específicas
class MinimumAgeSpecification(Specification[LoanApplication]):
    def __init__(self, minimum_age: int = 18):
        self.minimum_age = minimum_age

    def is_satisfied_by(self, application: LoanApplication) -> bool:
        return application.applicant_age >= self.minimum_age

class MinimumIncomeSpecification(Specification[LoanApplication]):
    def __init__(self, minimum_income: Decimal):
        self.minimum_income = minimum_income

    def is_satisfied_by(self, application: LoanApplication) -> bool:
        return application.annual_income >= self.minimum_income

class MinimumCreditScoreSpecification(Specification[LoanApplication]):
    def __init__(self, minimum_score: int = 650):
        self.minimum_score = minimum_score

    def is_satisfied_by(self, application: LoanApplication) -> bool:
        return application.credit_score >= self.minimum_score

class DebtToIncomeRatioSpecification(Specification[LoanApplication]):
    def __init__(self, maximum_ratio: float = 0.43):
        self.maximum_ratio = maximum_ratio

    def is_satisfied_by(self, application: LoanApplication) -> bool:
        return application.debt_to_income_ratio <= self.maximum_ratio

class StableEmploymentSpecification(Specification[LoanApplication]):
    def __init__(self, minimum_years: int = 2):
        self.minimum_years = minimum_years

    def is_satisfied_by(self, application: LoanApplication) -> bool:
        return application.employment_years >= self.minimum_years

class LoanAmountToIncomeRatioSpecification(Specification[LoanApplication]):
    def __init__(self, maximum_multiplier: int = 5):
        self.maximum_multiplier = maximum_multiplier

    def is_satisfied_by(self, application: LoanApplication) -> bool:
        max_loan = application.annual_income * self.maximum_multiplier
        return application.loan_amount <= max_loan

# Composición de reglas de negocio
class LoanApprovalPolicy:
    """Policy compuesta de múltiples specifications"""

    @staticmethod
    def standard_loan_policy() -> Specification[LoanApplication]:
        """Política estándar para préstamos"""
        return (
            MinimumAgeSpecification(18)
            .and_(MinimumIncomeSpecification(Decimal(30000)))
            .and_(MinimumCreditScoreSpecification(650))
            .and_(DebtToIncomeRatioSpecification(0.43))
            .and_(StableEmploymentSpecification(2))
            .and_(LoanAmountToIncomeRatioSpecification(5))
        )

    @staticmethod
    def premium_loan_policy() -> Specification[LoanApplication]:
        """Política para clientes premium (menos estricta)"""
        return (
            MinimumAgeSpecification(21)
            .and_(MinimumIncomeSpecification(Decimal(100000)))
            .and_(MinimumCreditScoreSpecification(750))
            .and_(DebtToIncomeRatioSpecification(0.50))
        )

    @staticmethod
    def first_time_buyer_policy() -> Specification[LoanApplication]:
        """Política especial para compradores primerizos"""
        return (
            MinimumAgeSpecification(21)
            .and_(MinimumCreditScoreSpecification(680))
            .and_(
                # Ingreso alto O empleo estable
                MinimumIncomeSpecification(Decimal(50000))
                .or_(StableEmploymentSpecification(5))
            )
            .and_(DebtToIncomeRatioSpecification(0.40))
        )

# Uso
application = LoanApplication(
    applicant_age=30,
    annual_income=Decimal(75000),
    credit_score=720,
    debt_to_income_ratio=0.35,
    employment_years=5,
    loan_amount=Decimal(300000)
)

# Evaluar contra diferentes políticas
standard_policy = LoanApprovalPolicy.standard_loan_policy()
if standard_policy.is_satisfied_by(application):
    print("Approved under standard policy")

premium_policy = LoanApprovalPolicy.premium_loan_policy()
if premium_policy.is_satisfied_by(application):
    print("Approved under premium policy")

# Specification pattern con SQL generation
class SqlSpecification(Specification[T], ABC):
    @abstractmethod
    def to_sql(self) -> str:
        """Generate SQL WHERE clause"""
        pass

class MinimumIncomeSqlSpec(SqlSpecification[LoanApplication]):
    def __init__(self, minimum_income: Decimal):
        self.minimum_income = minimum_income

    def is_satisfied_by(self, application: LoanApplication) -> bool:
        return application.annual_income >= self.minimum_income

    def to_sql(self) -> str:
        return f"annual_income >= {self.minimum_income}"

# Uso en queries
spec = (
    MinimumIncomeSqlSpec(Decimal(50000))
    .and_(MinimumCreditScoreSqlSpec(700))
)

sql = f"SELECT * FROM loan_applications WHERE {spec.to_sql()}"
```

---

## CATEGORÍA 3: Workflow Orchestration

### 3.1 State Machines para Business Processes
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from enum import Enum, auto
from typing import Dict, Set, Callable, Optional
from dataclasses import dataclass

# 1. Order Processing State Machine
class OrderState(Enum):
    PENDING = auto()
    PAYMENT_PENDING = auto()
    PAID = auto()
    PROCESSING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    REFUNDED = auto()

class OrderEvent(Enum):
    SUBMIT = auto()
    PAY = auto()
    PAYMENT_FAILED = auto()
    START_PROCESSING = auto()
    SHIP = auto()
    DELIVER = auto()
    CANCEL = auto()
    REFUND = auto()

@dataclass
class StateTransition:
    from_state: OrderState
    event: OrderEvent
    to_state: OrderState
    guard: Optional[Callable] = None  # Condición para permitir transición
    action: Optional[Callable] = None  # Acción al hacer transición

class OrderStateMachine:
    def __init__(self):
        # Definir transiciones válidas
        self.transitions: Dict[tuple, StateTransition] = {}
        self._define_transitions()

    def _define_transitions(self):
        transitions = [
            # De PENDING
            StateTransition(
                OrderState.PENDING,
                OrderEvent.SUBMIT,
                OrderState.PAYMENT_PENDING,
                guard=self._has_items,
                action=self._create_payment
            ),
            StateTransition(
                OrderState.PENDING,
                OrderEvent.CANCEL,
                OrderState.CANCELLED
            ),

            # De PAYMENT_PENDING
            StateTransition(
                OrderState.PAYMENT_PENDING,
                OrderEvent.PAY,
                OrderState.PAID,
                action=self._confirm_payment
            ),
            StateTransition(
                OrderState.PAYMENT_PENDING,
                OrderEvent.PAYMENT_FAILED,
                OrderState.PENDING,
                action=self._notify_payment_failure
            ),
            StateTransition(
                OrderState.PAYMENT_PENDING,
                OrderEvent.CANCEL,
                OrderState.CANCELLED
            ),

            # De PAID
            StateTransition(
                OrderState.PAID,
                OrderEvent.START_PROCESSING,
                OrderState.PROCESSING,
                action=self._allocate_inventory
            ),
            StateTransition(
                OrderState.PAID,
                OrderEvent.CANCEL,
                OrderState.REFUNDED,
                action=self._process_refund
            ),

            # De PROCESSING
            StateTransition(
                OrderState.PROCESSING,
                OrderEvent.SHIP,
                OrderState.SHIPPED,
                guard=self._all_items_packed,
                action=self._create_shipment
            ),

            # De SHIPPED
            StateTransition(
                OrderState.SHIPPED,
                OrderEvent.DELIVER,
                OrderState.DELIVERED,
                action=self._mark_delivered
            ),

            # De DELIVERED
            StateTransition(
                OrderState.DELIVERED,
                OrderEvent.REFUND,
                OrderState.REFUNDED,
                guard=self._within_refund_period,
                action=self._process_refund
            ),
        ]

        for transition in transitions:
            key = (transition.from_state, transition.event)
            self.transitions[key] = transition

    def can_transition(self, order, event: OrderEvent) -> bool:
        """Check si transición es válida"""
        key = (order.state, event)
        transition = self.transitions.get(key)

        if not transition:
            return False

        if transition.guard:
            return transition.guard(order)

        return True

    def transition(self, order, event: OrderEvent):
        """Execute state transition"""
        if not self.can_transition(order, event):
            raise InvalidStateTransitionError(
                f"Cannot {event.name} from {order.state.name}"
            )

        key = (order.state, event)
        transition = self.transitions[key]

        # Ejecutar acción
        if transition.action:
            transition.action(order)

        # Cambiar estado
        old_state = order.state
        order.state = transition.to_state

        # Emitir evento
        order.add_domain_event(
            OrderStateChanged(order.id, old_state, order.state)
        )

    # Guards
    def _has_items(self, order) -> bool:
        return len(order.items) > 0

    def _all_items_packed(self, order) -> bool:
        return all(item.is_packed for item in order.items)

    def _within_refund_period(self, order) -> bool:
        days_since_delivery = (datetime.now() - order.delivered_at).days
        return days_since_delivery <= 30

    # Actions
    def _create_payment(self, order):
        # Crear payment intent
        payment = PaymentService.create_payment(order.total())
        order.payment_id = payment.id

    def _confirm_payment(self, order):
        # Confirmar pago
        PaymentService.confirm(order.payment_id)

    def _notify_payment_failure(self, order):
        # Notificar usuario
        NotificationService.send_email(
            order.customer_email,
            "Payment failed",
            f"Payment for order {order.id} failed"
        )

    def _allocate_inventory(self, order):
        # Reservar inventario
        for item in order.items:
            InventoryService.allocate(item.product_id, item.quantity)

    def _create_shipment(self, order):
        # Crear envío
        shipment = ShippingService.create_shipment(order)
        order.shipment_id = shipment.id

    def _mark_delivered(self, order):
        order.delivered_at = datetime.now()

    def _process_refund(self, order):
        # Procesar reembolso
        PaymentService.refund(order.payment_id)

        # Liberar inventario
        for item in order.items:
            InventoryService.release(item.product_id, item.quantity)

# Uso
class Order:
    def __init__(self):
        self.id = OrderId.generate()
        self.state = OrderState.PENDING
        self.items = []
        self.state_machine = OrderStateMachine()

    def submit(self):
        self.state_machine.transition(self, OrderEvent.SUBMIT)

    def pay(self):
        self.state_machine.transition(self, OrderEvent.PAY)

    def ship(self):
        self.state_machine.transition(self, OrderEvent.SHIP)

    def can_cancel(self) -> bool:
        return self.state_machine.can_transition(self, OrderEvent.CANCEL)

# 2. Visualización de State Machine
def generate_state_diagram(state_machine: OrderStateMachine):
    """Generate Mermaid diagram for documentation"""
    print("```mermaid")
    print("stateDiagram-v2")

    for (from_state, event), transition in state_machine.transitions.items():
        print(f"    {from_state.name} --> {transition.to_state.name}: {event.name}")

    print("```")
```

---

## CATEGORÍA 4: Multi-Tenancy Business Logic

### 4.1 Tenant-Aware Business Rules
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# 1. Tenant-specific configurations
class TenantConfiguration:
    def __init__(self, tenant_id: TenantId):
        self.tenant_id = tenant_id
        self._config = self._load_config()

    def _load_config(self) -> dict:
        # Load from database
        return tenant_config_repo.get(self.tenant_id)

    def get_pricing_strategy(self) -> PricingStrategy:
        strategy_name = self._config.get('pricing_strategy', 'standard')

        if strategy_name == 'volume_discount':
            return VolumeDiscountPricing()
        elif strategy_name == 'tiered':
            return TieredPricing()
        else:
            return StandardPricing()

    def get_tax_calculator(self) -> TaxCalculator:
        region = self._config.get('region')

        if region == 'US':
            return USTaxCalculator()
        elif region == 'EU':
            return EUTaxCalculator()
        else:
            return NoTaxCalculator()

    def allows_feature(self, feature: str) -> bool:
        enabled_features = self._config.get('features', [])
        return feature in enabled_features

# 2. Tenant-specific business rules
class PricingService:
    def __init__(self, tenant_config: TenantConfiguration):
        self.tenant_config = tenant_config

    def calculate_price(self, product: Product, quantity: int) -> Money:
        # Get tenant-specific strategy
        strategy = self.tenant_config.get_pricing_strategy()

        # Calculate base price
        base_price = product.unit_price * quantity

        # Apply tenant-specific pricing
        final_price = strategy.calculate(product, quantity, base_price)

        # Apply tax if applicable
        if self.tenant_config.allows_feature('tax_calculation'):
            tax_calculator = self.tenant_config.get_tax_calculator()
            tax = tax_calculator.calculate(final_price)
            final_price += tax

        return final_price

# 3. Pricing strategies (Strategy pattern)
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, product: Product, quantity: int, base_price: Money) -> Money:
        pass

class StandardPricing(PricingStrategy):
    def calculate(self, product: Product, quantity: int, base_price: Money) -> Money:
        return base_price

class VolumeDiscountPricing(PricingStrategy):
    def calculate(self, product: Product, quantity: int, base_price: Money) -> Money:
        if quantity >= 100:
            discount = Decimal('0.15')  # 15% off
        elif quantity >= 50:
            discount = Decimal('0.10')  # 10% off
        elif quantity >= 10:
            discount = Decimal('0.05')  # 5% off
        else:
            discount = Decimal('0')

        return base_price * (1 - discount)

class TieredPricing(PricingStrategy):
    def calculate(self, product: Product, quantity: int, base_price: Money) -> Money:
        unit_price = product.unit_price

        # First 10: full price
        tier1 = min(quantity, 10) * unit_price

        # Next 40: 10% off
        tier2 = max(0, min(quantity - 10, 40)) * unit_price * Decimal('0.90')

        # Remaining: 20% off
        tier3 = max(0, quantity - 50) * unit_price * Decimal('0.80')

        return Money(tier1 + tier2 + tier3, unit_price.currency)

# Uso
tenant_config = TenantConfiguration(tenant_id)
pricing_service = PricingService(tenant_config)

price = pricing_service.calculate_price(product, quantity=100)
```

---

## Resumen Prioridades Business Logic

| Tema | Dificultad | Criticidad | Impacto | Prioridad |
|------|------------|------------|---------|-----------|
| Aggregate Design | 5 | 5 | 5 | **CRÍTICA** |
| Domain Events | 5 | 5 | 4 | **CRÍTICA** |
| Event Sourcing | 5 | 4 | 4 | **ALTA** |
| Specification Pattern | 4 | 4 | 4 | **ALTA** |
| State Machines | 5 | 5 | 5 | **CRÍTICA** |
| Value Objects | 4 | 4 | 5 | **ALTA** |
| Multi-Tenancy Rules | 5 | 5 | 4 | **CRÍTICA** |

**Total de temas:** 15+ subtemas críticos de lógica de negocio
