# Arquitectura: Modular Monolith y Evolutionary Architecture 2026

## Objetivo
Patrones de Modular Monolith, Evolutionary Architecture, Fitness Functions, ADRs, y migration paths de monolito a microservices.

---

## CATEGORÍA 1: Modular Monolith Architecture

### 1.1 Package by Feature vs Package by Layer
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
La estructura del código determina la mantenibilidad. Package by Feature facilita modularización futura.

**Anti-Pattern: Package by Layer**

```
❌ BAD: Package by Layer (Traditional layered architecture)

src/
├── controllers/
│   ├── UserController.py
│   ├── OrderController.py
│   ├── ProductController.py
│   └── PaymentController.py
├── services/
│   ├── UserService.py
│   ├── OrderService.py
│   ├── ProductService.py
│   └── PaymentService.py
├── repositories/
│   ├── UserRepository.py
│   ├── OrderRepository.py
│   ├── ProductRepository.py
│   └── PaymentRepository.py
└── models/
    ├── User.py
    ├── Order.py
    ├── Product.py
    └── Payment.py

PROBLEMAS:
❌ Cambios pequeños afectan múltiples capas
❌ Difícil identificar bounded contexts
❌ Alto acoplamiento entre capas
❌ Imposible extraer a microservice
❌ No refleja el dominio del negocio
```

**✅ GOOD: Package by Feature (Modular Monolith)**

```
✅ GOOD: Package by Feature (Domain-driven structure)

src/
├── users/                    # Módulo Users
│   ├── __init__.py
│   ├── domain/
│   │   ├── user.py          # Aggregate
│   │   ├── user_repository.py  # Port
│   │   └── events.py
│   ├── application/
│   │   ├── register_user.py    # Use case
│   │   └── update_profile.py
│   ├── infrastructure/
│   │   ├── user_repository_postgres.py
│   │   └── user_controller.py
│   └── api.py               # Public API del módulo
│
├── orders/                   # Módulo Orders
│   ├── __init__.py
│   ├── domain/
│   │   ├── order.py
│   │   ├── order_repository.py
│   │   └── events.py
│   ├── application/
│   │   ├── place_order.py
│   │   └── cancel_order.py
│   ├── infrastructure/
│   │   ├── order_repository_postgres.py
│   │   └── order_controller.py
│   └── api.py
│
├── products/                 # Módulo Products
│   ├── __init__.py
│   ├── domain/
│   │   ├── product.py
│   │   └── product_repository.py
│   ├── application/
│   │   ├── create_product.py
│   │   └── update_inventory.py
│   ├── infrastructure/
│   │   ├── product_repository_postgres.py
│   │   └── product_controller.py
│   └── api.py
│
├── payments/                 # Módulo Payments
│   ├── __init__.py
│   ├── domain/
│   │   ├── payment.py
│   │   └── payment_gateway.py
│   ├── application/
│   │   └── process_payment.py
│   ├── infrastructure/
│   │   ├── stripe_gateway.py
│   │   └── payment_controller.py
│   └── api.py
│
└── shared/                   # Shared Kernel (minimal)
    ├── domain/
    │   ├── money.py         # Value Objects
    │   └── email.py
    ├── infrastructure/
    │   ├── event_bus.py
    │   └── database.py
    └── exceptions.py

VENTAJAS:
✅ Bounded contexts claros
✅ Bajo acoplamiento entre módulos
✅ Alta cohesión dentro de módulo
✅ Fácil extraer a microservice
✅ Refleja el dominio del negocio
✅ Equipos pueden trabajar en módulos independientes
```

**Implementación: Module API y Dependency Rules**

```python
# ============================================
# USERS MODULE - Public API
# ============================================

# src/users/api.py
"""
Public API del módulo Users

SOLO este archivo es importado por otros módulos
Todo lo demás es PRIVADO al módulo
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class UserDTO:
    """Data Transfer Object - Public interface"""
    id: str
    name: str
    email: str
    is_active: bool

class UsersModuleAPI:
    """
    Public API del módulo Users

    Otros módulos SOLO pueden usar esta API
    No pueden importar directamente desde domain/ o infrastructure/
    """

    def __init__(self, user_service):
        self._user_service = user_service

    async def get_user(self, user_id: str) -> Optional[UserDTO]:
        """Get user by ID"""
        user = await self._user_service.get_user(user_id)

        if not user:
            return None

        # Map domain model to DTO
        return UserDTO(
            id=user.id.value,
            name=user.name.full_name,
            email=user.email.value,
            is_active=user.is_active
        )

    async def register_user(
        self,
        name: str,
        email: str,
        password: str
    ) -> str:
        """Register new user - Returns user_id"""
        return await self._user_service.register_user(name, email, password)

    async def is_user_active(self, user_id: str) -> bool:
        """Check if user is active"""
        user = await self._user_service.get_user(user_id)
        return user.is_active if user else False


# ============================================
# ORDERS MODULE - Uses Users API
# ============================================

# src/orders/application/place_order.py
"""
Orders module uses Users module via public API

NO imports from users.domain or users.infrastructure
ONLY from users.api
"""

from users.api import UsersModuleAPI  # ✅ GOOD: Public API
# from users.domain.user import User   # ❌ BAD: Direct domain access

class PlaceOrderUseCase:
    """
    Place order use case

    Depends on Users module via API
    """

    def __init__(
        self,
        order_repository,
        users_api: UsersModuleAPI  # Dependency on API, not implementation
    ):
        self.order_repository = order_repository
        self.users_api = users_api

    async def execute(
        self,
        user_id: str,
        items: list
    ) -> str:
        """
        Place order

        Validates user via Users API
        """

        # Use Users API (not direct domain access)
        user = await self.users_api.get_user(user_id)

        if not user:
            raise UserNotFoundError(user_id)

        if not user.is_active:
            raise InactiveUserError(user_id)

        # Create order (Orders domain)
        order = Order.create(
            user_id=user_id,
            items=items
        )

        await self.order_repository.save(order)

        return order.id


# ============================================
# DEPENDENCY ENFORCEMENT with ArchUnit
# ============================================

# tests/architecture/test_module_dependencies.py
"""
Architectural tests - Enforce module boundaries

Using ArchUnit-like patterns
"""

import ast
import os
from pathlib import Path

class ArchitectureTest:
    """
    Test architecture rules

    Fails if module boundaries are violated
    """

    def test_modules_only_use_public_apis(self):
        """
        Rule: Modules can only import from other modules' api.py

        ALLOWED:
        - from users.api import UsersModuleAPI ✅
        - from products.api import ProductsModuleAPI ✅

        FORBIDDEN:
        - from users.domain.user import User ❌
        - from users.infrastructure.repository import UserRepo ❌
        """

        violations = []

        # Scan all Python files
        for py_file in Path('src').rglob('*.py'):
            if 'shared' in str(py_file):
                continue  # Shared is allowed

            module_name = py_file.parts[1]  # e.g., 'orders'

            # Parse imports
            with open(py_file) as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    imported_module = node.module

                    if not imported_module:
                        continue

                    # Check cross-module imports
                    if '.' in imported_module:
                        parts = imported_module.split('.')
                        target_module = parts[0]

                        # Cross-module import?
                        if target_module != module_name and target_module != 'shared':
                            # Must be from api.py
                            if len(parts) < 2 or parts[1] != 'api':
                                violations.append({
                                    'file': str(py_file),
                                    'import': imported_module,
                                    'rule': f'Cross-module import must be from {target_module}.api'
                                })

        # Assert no violations
        if violations:
            error_msg = "\n".join([
                f"{v['file']}: {v['import']} - {v['rule']}"
                for v in violations
            ])
            raise AssertionError(f"Architecture violations:\n{error_msg}")

    def test_shared_kernel_is_minimal(self):
        """
        Rule: Shared kernel should be minimal

        MAX 10 files in shared/
        """
        shared_files = list(Path('src/shared').rglob('*.py'))

        assert len(shared_files) <= 10, \
            f"Shared kernel too large: {len(shared_files)} files. Keep it minimal!"


# Run with pytest
# pytest tests/architecture/test_module_dependencies.py
```

---

## CATEGORÍA 2: Module Communication Patterns

### 2.1 Internal Event Bus
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Módulos deben comunicarse sin acoplamiento directo. Event bus interno permite eventual consistency.

**Implementación: In-Process Event Bus**

```python
# ============================================
# INTERNAL EVENT BUS (Shared Kernel)
# ============================================

# src/shared/infrastructure/event_bus.py
"""
Internal Event Bus for Modular Monolith

In-process event bus (no Kafka/RabbitMQ needed)
When extracting to microservices, replace with real message broker
"""

from typing import Callable, List, Dict, Type
from dataclasses import dataclass
from datetime import datetime
import asyncio

@dataclass
class DomainEvent:
    """Base domain event"""
    event_id: str
    occurred_at: datetime
    aggregate_id: str

class InternalEventBus:
    """
    In-process event bus

    Benefits:
    - No external dependencies (no Kafka/RabbitMQ)
    - Transactional (same DB transaction)
    - Fast (in-memory)
    - Easy testing

    Limitations:
    - Single process only
    - No persistence (events lost on crash)
    - No replay capability

    Migration path:
    - Easy to replace with Kafka/RabbitMQ later
    """

    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}

    def subscribe(
        self,
        event_type: Type[DomainEvent],
        handler: Callable
    ):
        """Subscribe handler to event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)

    async def publish(self, event: DomainEvent):
        """
        Publish event to all subscribers

        In-process: executes immediately
        """
        event_type = type(event)

        if event_type not in self._handlers:
            return

        # Execute all handlers
        for handler in self._handlers[event_type]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)

            except Exception as e:
                # Log but don't fail (eventual consistency)
                logger.error(
                    "event_handler_failed",
                    event_type=event_type.__name__,
                    handler=handler.__name__,
                    error=str(e)
                )


# ============================================
# ORDERS MODULE - Publishes Events
# ============================================

# src/orders/domain/events.py
from shared.infrastructure.event_bus import DomainEvent

@dataclass
class OrderPlacedEvent(DomainEvent):
    """Order was placed"""
    order_id: str
    user_id: str
    total: float
    items: List[dict]


# src/orders/application/place_order.py
class PlaceOrderUseCase:
    """Place order - publishes event"""

    def __init__(
        self,
        order_repository,
        event_bus: InternalEventBus
    ):
        self.order_repository = order_repository
        self.event_bus = event_bus

    async def execute(self, user_id: str, items: List) -> str:
        """Place order"""

        # Create order
        order = Order.create(user_id, items)

        # Save order
        await self.order_repository.save(order)

        # Publish event (in-process)
        await self.event_bus.publish(
            OrderPlacedEvent(
                event_id=str(uuid.uuid4()),
                occurred_at=datetime.utcnow(),
                aggregate_id=order.id,
                order_id=order.id,
                user_id=user_id,
                total=order.total,
                items=items
            )
        )

        return order.id


# ============================================
# USERS MODULE - Subscribes to Events
# ============================================

# src/users/application/event_handlers.py
"""
Users module reacts to events from other modules

Decoupled via event bus
"""

from orders.domain.events import OrderPlacedEvent

class UserEventHandlers:
    """Event handlers for Users module"""

    def __init__(self, user_service):
        self.user_service = user_service

    async def on_order_placed(self, event: OrderPlacedEvent):
        """
        When order is placed:
        - Update user's order count
        - Update loyalty points
        """

        await self.user_service.increment_order_count(event.user_id)
        await self.user_service.add_loyalty_points(
            event.user_id,
            points=int(event.total * 0.1)  # 10% of total
        )


# ============================================
# APPLICATION STARTUP - Wire handlers
# ============================================

# src/main.py
"""
Application startup

Wire event handlers to event bus
"""

async def setup_event_handlers(event_bus: InternalEventBus):
    """
    Setup event handlers

    Each module registers its handlers
    """

    # Users module handlers
    user_handlers = UserEventHandlers(user_service)
    event_bus.subscribe(OrderPlacedEvent, user_handlers.on_order_placed)

    # Inventory module handlers
    inventory_handlers = InventoryEventHandlers(inventory_service)
    event_bus.subscribe(OrderPlacedEvent, inventory_handlers.on_order_placed)

    # Notifications module handlers
    notification_handlers = NotificationEventHandlers(email_service)
    event_bus.subscribe(OrderPlacedEvent, notification_handlers.on_order_placed)
```

---

## CATEGORÍA 3: Evolutionary Architecture

### 3.1 Fitness Functions (Architecture Tests)
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Fitness Functions son tests automáticos que validan arquitectura. Previenen degradación arquitectónica.

**Implementación: Architectural Fitness Functions**

```python
# ============================================
# FITNESS FUNCTIONS - Architecture Tests
# ============================================

# tests/architecture/fitness_functions.py
"""
Fitness Functions: Automated Architecture Tests

Validates architectural constraints
Runs in CI/CD pipeline
"""

import ast
import os
from pathlib import Path
import pytest

class ArchitectureFitnessFunctions:
    """
    Fitness Functions for architecture

    Tests that architecture doesn't degrade over time
    """

    def test_module_independence(self):
        """
        FITNESS FUNCTION: Module independence

        Rule: No circular dependencies between modules

        Example violation:
        - orders imports from products
        - products imports from orders
        = CIRCULAR DEPENDENCY ❌
        """

        dependencies = self._analyze_module_dependencies()

        # Check for cycles
        cycles = self._detect_cycles(dependencies)

        assert not cycles, \
            f"Circular dependencies detected: {cycles}"

    def test_shared_kernel_size(self):
        """
        FITNESS FUNCTION: Shared kernel size

        Rule: Shared kernel < 15% of codebase

        Prevents "shared kernel bloat"
        """

        total_lines = self._count_lines(Path('src'))
        shared_lines = self._count_lines(Path('src/shared'))

        shared_percentage = (shared_lines / total_lines) * 100

        assert shared_percentage < 15, \
            f"Shared kernel too large: {shared_percentage:.1f}% (max 15%)"

    def test_api_stability(self):
        """
        FITNESS FUNCTION: API stability

        Rule: Public APIs shouldn't change frequently

        Tracks API changes in git history
        """

        api_files = list(Path('src').rglob('api.py'))

        for api_file in api_files:
            # Count commits to api.py in last 30 days
            commits = self._count_recent_commits(api_file, days=30)

            assert commits < 5, \
                f"{api_file} changed {commits} times in 30 days. APIs should be stable!"

    def test_layered_architecture_violations(self):
        """
        FITNESS FUNCTION: Layered architecture

        Rule: Dependencies flow inward
        - Infrastructure can depend on Application
        - Application can depend on Domain
        - Domain depends on NOTHING

        Violations:
        - Domain imports from Application ❌
        - Domain imports from Infrastructure ❌
        """

        violations = []

        # Check domain/ folders
        for domain_file in Path('src').rglob('domain/*.py'):
            # Parse imports
            with open(domain_file) as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if not node.module:
                        continue

                    # Domain importing from application or infrastructure?
                    if 'application' in node.module or 'infrastructure' in node.module:
                        violations.append({
                            'file': str(domain_file),
                            'import': node.module,
                            'rule': 'Domain cannot depend on Application or Infrastructure'
                        })

        assert not violations, \
            f"Layer violations: {violations}"

    def test_database_access_only_in_repositories(self):
        """
        FITNESS FUNCTION: Database access

        Rule: Database access ONLY in repositories

        Violations:
        - Direct SQL in controllers ❌
        - Direct SQL in use cases ❌
        """

        violations = []

        # Search for SQL in non-repository files
        for py_file in Path('src').rglob('*.py'):
            if 'repository' in str(py_file):
                continue  # OK

            with open(py_file) as f:
                content = f.read()

            # Look for SQL keywords
            if any(keyword in content.lower() for keyword in ['select ', 'insert ', 'update ', 'delete ']):
                violations.append(str(py_file))

        assert not violations, \
            f"Direct SQL found in non-repository files: {violations}"

    def test_no_god_classes(self):
        """
        FITNESS FUNCTION: No god classes

        Rule: Classes < 300 lines

        Prevents god classes
        """

        violations = []

        for py_file in Path('src').rglob('*.py'):
            with open(py_file) as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Count lines in class
                    class_lines = node.end_lineno - node.lineno

                    if class_lines > 300:
                        violations.append({
                            'file': str(py_file),
                            'class': node.name,
                            'lines': class_lines
                        })

        assert not violations, \
            f"God classes detected (>300 lines): {violations}"

    def test_cyclomatic_complexity(self):
        """
        FITNESS FUNCTION: Cyclomatic complexity

        Rule: Function complexity < 10

        High complexity = hard to test
        """

        violations = []

        for py_file in Path('src').rglob('*.py'):
            with open(py_file) as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_complexity(node)

                    if complexity > 10:
                        violations.append({
                            'file': str(py_file),
                            'function': node.name,
                            'complexity': complexity
                        })

        assert not violations, \
            f"High complexity functions: {violations}"

    # Helper methods
    def _count_lines(self, path: Path) -> int:
        """Count lines of code"""
        total = 0
        for py_file in path.rglob('*.py'):
            with open(py_file) as f:
                total += len(f.readlines())
        return total

    def _analyze_module_dependencies(self) -> dict:
        """Analyze dependencies between modules"""
        # Implementation...
        pass

    def _detect_cycles(self, dependencies: dict) -> list:
        """Detect circular dependencies"""
        # Implementation...
        pass


# ============================================
# CI/CD Integration
# ============================================

# .github/workflows/architecture-tests.yml
"""
name: Architecture Tests

on: [push, pull_request]

jobs:
  architecture:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Fitness Functions
        run: |
          pytest tests/architecture/fitness_functions.py -v

      # Fail build if architecture degrades
"""
```

---

## CATEGORÍA 4: Architectural Decision Records (ADRs)

### 4.1 ADR Template y Process
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
ADRs documentan decisiones arquitectónicas importantes. Crítico para entender "por qué" se tomaron decisiones.

**Implementación: ADR Template**

```markdown
# ADR Template

<!-- docs/architecture/decisions/0001-use-modular-monolith.md -->

# 1. Use Modular Monolith Architecture

Date: 2025-12-26

## Status

Accepted

## Context

We need to decide on the overall architecture for our e-commerce platform.

Current situation:
- Team size: 8 developers
- Expected traffic: 10K users initially, 100K in 2 years
- Complexity: Medium (orders, payments, inventory, users)
- Deployment frequency: Weekly releases

Options considered:
1. Microservices architecture
2. Traditional layered monolith
3. Modular monolith

## Decision

We will use a **Modular Monolith** architecture with the following structure:

```
src/
├── orders/      # Bounded context
├── users/       # Bounded context
├── products/    # Bounded context
├── payments/    # Bounded context
└── shared/      # Minimal shared kernel
```

Key principles:
- Package by feature (not by layer)
- Explicit module APIs (api.py)
- Internal event bus for module communication
- Architectural fitness functions

## Consequences

### Positive
✅ **Simpler deployment**: Single deployable unit
✅ **Easier debugging**: All code in one place, single process
✅ **Lower operational complexity**: No distributed tracing, no service mesh
✅ **Faster development**: No network overhead, easier refactoring
✅ **Cost efficient**: Single database, single server initially
✅ **Migration path**: Can extract to microservices later

### Negative
❌ **Scaling limitations**: Can't scale individual modules independently
❌ **Technology coupling**: All modules use same tech stack
❌ **Database shared**: All modules share same database initially
❌ **Deployment coupling**: Deploy all modules together

### Risks & Mitigations

**Risk 1**: Team might create tight coupling between modules
- **Mitigation**: Architectural fitness functions in CI/CD
- **Mitigation**: Code review focus on module boundaries

**Risk 2**: Shared database might become bottleneck
- **Mitigation**: Use schemas per module (schema-per-module pattern)
- **Mitigation**: Monitor database performance closely

**Risk 3**: Might grow into "big ball of mud"
- **Mitigation**: Strict module boundaries enforced by tests
- **Mitigation**: Regular architectural reviews (quarterly)

## Alternatives Considered

### Alternative 1: Microservices
❌ Rejected because:
- Team too small (8 devs) to manage multiple services
- Operational complexity too high for initial stage
- Over-engineering for current scale (10K users)

### Alternative 2: Traditional Layered Monolith
❌ Rejected because:
- Hard to extract to microservices later
- Tight coupling between layers
- Doesn't reflect domain model

## Implementation Plan

### Phase 1 (Months 1-2):
- [ ] Setup modular structure
- [ ] Define module boundaries
- [ ] Implement internal event bus
- [ ] Setup architectural tests

### Phase 2 (Months 3-6):
- [ ] Migrate existing code to modular structure
- [ ] Document module APIs
- [ ] Setup fitness functions in CI/CD

### Phase 3 (Ongoing):
- [ ] Monitor module dependencies
- [ ] Review architecture quarterly
- [ ] Identify candidates for extraction (if needed)

## Review Date

Review this decision: **June 2026** (6 months)

Triggers for review:
- Team size > 20 developers
- Traffic > 100K users
- Need to scale specific modules independently
- Performance bottlenecks in shared database

## References

- [Modular Monolith: A Primer](https://www.kamilgrzybek.com/design/modular-monolith-primer/)
- [Monolith First by Martin Fowler](https://martinfowler.com/bliki/MonolithFirst.html)
- Our codebase: `docs/architecture/module-structure.md`

## Notes

Decision made in architecture meeting on 2025-12-26
Attendees: CTO, Tech Lead, Senior Architects

---

<!-- Superseded by: None -->
<!-- Supersedes: None -->
```

**ADR Management Tool**

```python
# ============================================
# ADR MANAGEMENT CLI
# ============================================

# scripts/adr.py
"""
ADR Management Tool

Usage:
  python scripts/adr.py new "Use PostgreSQL for main database"
  python scripts/adr.py list
  python scripts/adr.py search "database"
"""

import os
from datetime import datetime
from pathlib import Path
import re

ADR_DIR = Path("docs/architecture/decisions")

ADR_TEMPLATE = """# {number}. {title}

Date: {date}

## Status

Proposed

## Context

[Describe the context and problem statement]

## Decision

[Describe the decision]

## Consequences

### Positive
✅ [Benefit 1]
✅ [Benefit 2]

### Negative
❌ [Drawback 1]
❌ [Drawback 2]

### Risks & Mitigations

**Risk 1**: [Description]
- **Mitigation**: [How to mitigate]

## Alternatives Considered

### Alternative 1: [Name]
❌ Rejected because: [Reason]

## Implementation Plan

- [ ] Step 1
- [ ] Step 2

## Review Date

Review this decision: [Date]

## References

- [Link 1]
- [Link 2]

## Notes

[Additional notes]
"""

class ADRManager:
    """Manage ADRs"""

    def create_new_adr(self, title: str):
        """Create new ADR"""

        # Get next number
        existing_adrs = list(ADR_DIR.glob("*.md"))
        if existing_adrs:
            numbers = [
                int(re.match(r'(\d+)', f.name).group(1))
                for f in existing_adrs
            ]
            next_number = max(numbers) + 1
        else:
            next_number = 1

        # Create ADR file
        filename = f"{next_number:04d}-{self._slugify(title)}.md"
        filepath = ADR_DIR / filename

        content = ADR_TEMPLATE.format(
            number=next_number,
            title=title,
            date=datetime.now().strftime("%Y-%m-%d")
        )

        filepath.write_text(content)

        print(f"Created ADR: {filepath}")

    def list_adrs(self):
        """List all ADRs"""

        adrs = sorted(ADR_DIR.glob("*.md"))

        for adr in adrs:
            # Read status
            with open(adr) as f:
                content = f.read()
                status_match = re.search(r'## Status\n\n(\w+)', content)
                status = status_match.group(1) if status_match else "Unknown"

            print(f"{adr.stem} - {status}")

    def _slugify(self, text: str) -> str:
        """Convert to slug"""
        return text.lower().replace(' ', '-')


if __name__ == "__main__":
    import sys

    manager = ADRManager()

    if len(sys.argv) < 2:
        print("Usage: python adr.py [new|list|search] [args]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "new":
        title = sys.argv[2]
        manager.create_new_adr(title)
    elif command == "list":
        manager.list_adrs()
```

---

## CATEGORÍA 5: Migration to Microservices

### 5.1 When and How to Extract Microservices
**Dificultad:** ⭐⭐⭐⭐⭐ **CRÍTICA**

**Contexto:**
Modular monolith permite fácil extracción a microservices cuando sea necesario. Pero hacerlo demasiado pronto es costly.

**Decision Matrix: When to Extract**

```python
# ============================================
# MICROSERVICE EXTRACTION DECISION MATRIX
# ============================================

"""
┌────────────────────────────────────────────────────┐
│      WHEN TO EXTRACT TO MICROSERVICE?              │
├────────────────────────────────────────────────────┤
│                                                    │
│ GOOD REASONS (✅ Extract):                         │
│                                                    │
│ 1. SCALE INDEPENDENTLY                             │
│    - Module needs 10x more instances than others  │
│    - Different scaling patterns (CPU vs memory)   │
│    Example: Image processing module (CPU-heavy)   │
│                                                    │
│ 2. DEPLOY INDEPENDENTLY                            │
│    - Module changes 10x more frequently           │
│    - Different release cycles needed              │
│    Example: Recommendation engine (A/B testing)   │
│                                                    │
│ 3. TEAM AUTONOMY                                   │
│    - Team size > 15 devs                          │
│    - Separate teams per bounded context           │
│    Example: Different teams for orders, users     │
│                                                    │
│ 4. TECHNOLOGY DIVERSITY                            │
│    - Module needs different tech stack            │
│    Example: ML module (Python) vs API (Go)        │
│                                                    │
│ 5. SECURITY ISOLATION                              │
│    - Module handles sensitive data                │
│    - Needs separate network/access controls       │
│    Example: Payments module (PCI compliance)      │
│                                                    │
│ BAD REASONS (❌ Don't Extract):                    │
│                                                    │
│ ❌ "Microservices are trendy"                      │
│ ❌ "We want to learn microservices"                │
│ ❌ "Our competitor uses microservices"             │
│ ❌ "Resume-driven development"                     │
│ ❌ "We have < 10 developers"                       │
│ ❌ "Traffic < 100K users"                          │
│                                                    │
└────────────────────────────────────────────────────┘

RULE OF THUMB:
- Start with Modular Monolith
- Extract to microservice ONLY when pain is real
- Keep modular structure (easy to extract later)
"""
```

**Extraction Process: Payments Module Example**

```python
# ============================================
# STEP 1: Assess Module Independence
# ============================================

"""
Before extracting, validate module is independent:

Checklist:
✅ Has clear bounded context
✅ Minimal dependencies on other modules
✅ Well-defined API (api.py)
✅ No direct database access from other modules
✅ Events used for communication

Payments Module Assessment:
✅ Clear bounded context (payment processing)
✅ API: PaymentsModuleAPI
✅ Dependencies: Only uses Users API
✅ Events: PaymentProcessedEvent, PaymentFailedEvent
✅ Ready for extraction!
"""

# ============================================
# STEP 2: Database Extraction
# ============================================

"""
OPTION 1: Schema per module (easiest)

Current (Modular Monolith):
PostgreSQL Database
├── public schema
│   ├── users table
│   ├── orders table
│   ├── products table
│   └── payments table

Step 1: Move to schemas
PostgreSQL Database
├── users_schema
│   └── users table
├── orders_schema
│   └── orders table
├── products_schema
│   └── products table
└── payments_schema
    └── payments table

Step 2: Create separate database
Payments Database (separate)
└── payments table

Benefits:
✅ Gradual migration
✅ No application changes needed initially
✅ Can test in isolation
"""

# Migration script
async def migrate_payments_to_separate_db():
    """
    Migrate payments to separate database

    Strategy: Dual writes (modular monolith + microservice)
    """

    # 1. Create payments database
    await create_database("payments_db")

    # 2. Migrate schema
    await run_migrations("payments_db", "payments_schema")

    # 3. Backfill data
    await backfill_payments_data(
        source_db="main_db",
        source_schema="payments_schema",
        target_db="payments_db"
    )

    # 4. Verify data integrity
    await verify_payment_counts()


# ============================================
# STEP 3: Extract Service with Strangler Pattern
# ============================================

"""
Use Strangler Pattern for zero-downtime extraction

Phase 1: Deploy microservice (shadow mode)
┌──────────────────────────────────────┐
│         API Gateway                  │
└────────┬─────────────────────────────┘
         │
         v
┌────────────────────┐   ┌─────────────┐
│  Modular Monolith  │   │  Payments   │
│  (All traffic)     │──▶│  Service    │
│                    │   │  (shadow)   │
└────────────────────┘   └─────────────┘

Phase 2: Route 10% traffic to microservice
┌──────────────────────────────────────┐
│         API Gateway                  │
│  10% → Payments Service              │
│  90% → Modular Monolith              │
└──────────────────────────────────────┘

Phase 3: Route 100% traffic
┌──────────────────────────────────────┐
│         API Gateway                  │
│  100% → Payments Service             │
└──────────────────────────────────────┘

Phase 4: Remove from monolith
"""

# API Gateway routing
class APIGateway:
    """
    API Gateway with strangler pattern

    Routes traffic during extraction
    """

    def __init__(self):
        self.payments_service_percentage = 0  # Start with 0%

    async def route_payment_request(self, request):
        """
        Route payment request

        Gradually shift traffic to microservice
        """

        # Random percentage routing
        if random.randint(1, 100) <= self.payments_service_percentage:
            # Route to microservice
            return await self._call_payments_microservice(request)
        else:
            # Route to monolith
            return await self._call_monolith_payments(request)


# ============================================
# STEP 4: Update Module Communication
# ============================================

"""
Replace internal events with external events

Before (Modular Monolith):
Orders Module ──(InternalEventBus)──▶ Payments Module
                    In-process

After (Microservices):
Orders Service ──(Kafka/RabbitMQ)──▶ Payments Service
                    Over network
"""

# Before: Internal event bus
await event_bus.publish(PaymentRequestedEvent(...))

# After: Kafka
await kafka_producer.send(
    topic='payment-requests',
    value=PaymentRequestedEvent(...).to_json()
)
```

---

## Decisiones Consolidadas 2026

```
┌──────────────────────────────────────────────────────────────┐
│  MODULAR MONOLITH & EVOLUTIONARY ARCHITECTURE - CHECKLIST    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. MODULAR STRUCTURE                                         │
│    ├─ [ ] Package by feature (not by layer)                 │
│    ├─ [ ] Explicit module APIs (api.py)                     │
│    ├─ [ ] Minimal shared kernel (<15% codebase)             │
│    └─ [ ] Module independence tests                         │
│                                                              │
│ 2. MODULE COMMUNICATION                                      │
│    ├─ [ ] Internal event bus (in-process)                   │
│    ├─ [ ] Eventual consistency between modules              │
│    ├─ [ ] No direct domain access across modules            │
│    └─ [ ] Migration path to external message broker         │
│                                                              │
│ 3. EVOLUTIONARY ARCHITECTURE                                 │
│    ├─ [ ] Fitness functions in CI/CD                        │
│    ├─ [ ] Architectural tests (no cycles, layer violations) │
│    ├─ [ ] Complexity metrics (cyclomatic < 10)              │
│    └─ [ ] Quarterly architecture reviews                    │
│                                                              │
│ 4. ADRs (Architectural Decision Records)                     │
│    ├─ [ ] ADR template defined                              │
│    ├─ [ ] ADR for major decisions                           │
│    ├─ [ ] ADR review process                                │
│    └─ [ ] ADR management tool                               │
│                                                              │
│ 5. MIGRATION PATH                                            │
│    ├─ [ ] Decision matrix for extraction                    │
│    ├─ [ ] Schema-per-module strategy                        │
│    ├─ [ ] Strangler pattern for extraction                  │
│    └─ [ ] Gradual traffic shifting (0% → 100%)              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Conclusión:**

Este archivo cubre Modular Monolith y Evolutionary Architecture:

1. **Modular Monolith**: Package by feature, module APIs, dependency enforcement
2. **Module Communication**: Internal event bus, eventual consistency
3. **Fitness Functions**: Automated architecture tests, prevents degradation
4. **ADRs**: Document architectural decisions, template y proceso
5. **Migration to Microservices**: When and how to extract, strangler pattern

Todos los patrones incluyen código de producción en Python, architectural tests, ADR templates, y migration strategies.
