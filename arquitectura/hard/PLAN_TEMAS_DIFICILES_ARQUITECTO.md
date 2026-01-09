# Plan para Identificar Temas Críticos y Difíciles del Arquitecto de Software

## Objetivo
Determinar los temas más complejos que debe dominar un arquitecto de software, con énfasis en qué conocimientos técnicos del código necesita para dar soluciones efectivas.

---

## Metodología del Plan

### Fase 1: Categorización por Dominio Técnico
Identificar temas difíciles agrupados en 5 dominios principales:

1. **Dominio de Sistemas Distribuidos**
2. **Dominio de Performance y Escalabilidad**
3. **Dominio de Seguridad y Resiliencia**
4. **Dominio de Datos y Consistencia**
5. **Dominio de Integración y Modernización**

### Fase 2: Criterios de Dificultad
Cada tema se evaluará según:
- **Complejidad Técnica** (1-5): Profundidad del conocimiento requerido
- **Impacto en el Negocio** (1-5): Criticidad de las decisiones
- **Conocimiento de Código Requerido** (1-5): Nivel de implementación necesario
- **Dificultad de Debugging** (1-5): Complejidad para resolver problemas

---

## Temas Críticos Identificados

### DOMINIO 1: Sistemas Distribuidos

#### 1.1 Consistencia Eventual y CAP Theorem
**Nivel de Dificultad:** ⭐⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Implementación de Sagas Patterns**
  ```
  Tecnologías: Choreography vs Orchestration
  Lenguajes: Java/Spring, Node.js, Go
  Frameworks: Temporal.io, Apache Camel, MassTransit
  ```
- **Manejo de Event Sourcing**
  ```
  - Escribir event handlers
  - Implementar snapshots
  - Manejar replays de eventos
  - Frameworks: Axon, EventStore, Kafka Streams
  ```
- **Compensating Transactions**
  ```
  - Diseñar rollbacks distribuidos
  - Implementar idempotencia
  - Manejar timeouts y reintentos
  ```

**Patrones de Código a Dominar:**
- Outbox Pattern
- Two-Phase Commit alternatives
- CQRS (Command Query Responsibility Segregation)
- Idempotent consumers

**Escenarios Críticos:**
- Sistema de pagos con múltiples proveedores
- Inventario distribuido en e-commerce
- Reservas con overbooking controlado

---

#### 1.2 Comunicación Asíncrona y Message Brokers
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Implementación de Producers/Consumers**
  ```
  Kafka: Partitions, Consumer Groups, Offsets
  RabbitMQ: Exchanges, Queues, Routing Keys
  Redis Streams: Consumer Groups, XREAD
  ```
- **Manejo de Backpressure**
  ```java
  // Ejemplo: Rate limiting en consumer
  @RateLimiter(permitsPerSecond = 100)
  public void processMessage(Message msg) {
      // Processing logic
  }
  ```
- **Dead Letter Queues (DLQ)**
  ```
  - Implementar retry policies
  - Logging y alerting de mensajes fallidos
  - Estrategias de reprocessing
  ```

**Patrones de Código a Dominar:**
- Publisher-Subscriber
- Request-Reply asíncrono
- Message Filtering
- Batch processing vs Stream processing

**Debugging Crítico:**
- Detectar message loss
- Resolver duplicados
- Analizar latencias end-to-end
- Ordenamiento de mensajes

---

#### 1.3 Service Mesh y Observabilidad Distribuida
**Nivel de Dificultad:** ⭐⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Distributed Tracing**
  ```
  OpenTelemetry: Spans, Traces, Context Propagation
  Lenguajes: Instrumentación en Java, Python, Go, Node.js
  ```
  ```python
  # Ejemplo: Propagación de contexto
  from opentelemetry import trace
  from opentelemetry.propagate import inject

  tracer = trace.get_tracer(__name__)
  with tracer.start_as_current_span("operation"):
      headers = {}
      inject(headers)  # Inyecta trace context
      requests.post(url, headers=headers)
  ```
- **Circuit Breakers**
  ```java
  @CircuitBreaker(name = "paymentService",
                  fallbackMethod = "paymentFallback")
  public PaymentResult processPayment(Order order) {
      return paymentClient.charge(order);
  }
  ```
- **Rate Limiting y Throttling**
  ```
  Implementación: Token Bucket, Leaky Bucket
  Tecnologías: Redis, Envoy, Kong
  ```

**Configuraciones Críticas:**
- Istio/Linkerd: Traffic splitting, Fault injection
- Envoy Proxy: Filtros, rate limits, timeouts
- Jaeger/Zipkin: Sampling strategies

---

### DOMINIO 2: Performance y Escalabilidad

#### 2.1 Caching Distribuido
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Estrategias de Cache**
  ```
  Cache-Aside, Read-Through, Write-Through, Write-Behind
  ```
  ```python
  # Cache-Aside pattern
  def get_user(user_id):
      # 1. Check cache
      user = cache.get(f"user:{user_id}")
      if user:
          return user

      # 2. Cache miss: fetch from DB
      user = db.query(f"SELECT * FROM users WHERE id={user_id}")

      # 3. Update cache
      cache.set(f"user:{user_id}", user, ttl=3600)
      return user
  ```
- **Invalidación de Cache**
  ```
  - Time-based expiration (TTL)
  - Event-based invalidation
  - Cache stampede prevention
  ```
  ```javascript
  // Prevenir cache stampede con locks
  async function getWithLock(key) {
      const lock = await acquireLock(`lock:${key}`);
      try {
          let value = await cache.get(key);
          if (!value) {
              value = await fetchFromDB(key);
              await cache.set(key, value, 3600);
          }
          return value;
      } finally {
          await releaseLock(lock);
      }
  }
  ```
- **Cache Coherence**
  ```
  - Pub/Sub para invalidación distribuida
  - Versioning de cache entries
  - Consistent hashing
  ```

**Tecnologías a Dominar:**
- Redis: Structures, Lua scripts, Cluster mode
- Memcached: Consistent hashing
- CDN caching: Cloudflare, CloudFront

---

#### 2.2 Database Sharding y Partitioning
**Nivel de Dificultad:** ⭐⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Sharding Strategies**
  ```sql
  -- Range-based sharding
  Shard 1: user_id 1-1000000
  Shard 2: user_id 1000001-2000000

  -- Hash-based sharding
  shard_id = hash(user_id) % num_shards

  -- Geographic sharding
  US users → US shard
  EU users → EU shard
  ```
- **Shard Routing Logic**
  ```java
  public class ShardRouter {
      public DataSource getShardForUser(long userId) {
          int shardId = (int)(userId % NUM_SHARDS);
          return dataSources.get(shardId);
      }

      // Cross-shard query
      public List<Order> getOrdersForMultipleUsers(List<Long> userIds) {
          Map<Integer, List<Long>> shardGroups = groupByShards(userIds);
          return shardGroups.entrySet().parallelStream()
              .flatMap(entry -> queryShared(entry.getKey(), entry.getValue()))
              .collect(Collectors.toList());
      }
  }
  ```
- **Rebalancing de Shards**
  ```
  - Mover datos entre shards sin downtime
  - Consistent hashing para minimizar movimientos
  - Virtual shards para flexibility
  ```

**Problemas Complejos:**
- Queries cross-shard (JOINs distribuidos)
- Transactions distribuidas entre shards
- Migraciones de sharding strategy
- Hotspot shards (distribución desbalanceada)

---

#### 2.3 Connection Pooling y Resource Management
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Configuración de Pools**
  ```java
  // HikariCP - Pool de conexiones DB
  HikariConfig config = new HikariConfig();
  config.setMaximumPoolSize(20);           // Max connections
  config.setMinimumIdle(5);                // Min idle connections
  config.setConnectionTimeout(30000);      // 30s timeout
  config.setIdleTimeout(600000);           // 10min idle
  config.setMaxLifetime(1800000);          // 30min max lifetime
  config.setLeakDetectionThreshold(60000); // Detect leaks
  ```
- **Manejo de Connection Leaks**
  ```python
  # Context manager para garantizar cierre
  class DatabaseConnection:
      def __enter__(self):
          self.conn = pool.get_connection()
          return self.conn

      def __exit__(self, exc_type, exc_val, exc_tb):
          self.conn.close()  # Siempre devuelve al pool

  with DatabaseConnection() as conn:
      conn.execute("SELECT * FROM users")
  ```
- **Backpressure y Rate Limiting**
  ```
  - Semaphores para limitar concurrencia
  - Circuit breakers cuando pool está exhausto
  - Retry con exponential backoff
  ```

**Debugging Crítico:**
- Detectar connection starvation
- Analizar pool exhaustion logs
- Profiling de queries lentas
- Monitorear wait times

---

### DOMINIO 3: Seguridad y Resiliencia

#### 3.1 OAuth2, OpenID Connect y JWT
**Nivel de Dificultad:** ⭐⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Implementación de Flows**
  ```
  Authorization Code Flow (web apps)
  Client Credentials Flow (service-to-service)
  PKCE (mobile/SPA)
  Device Flow (IoT)
  ```
  ```javascript
  // Authorization Code Flow con PKCE
  // 1. Generate code verifier & challenge
  const codeVerifier = generateRandomString(128);
  const codeChallenge = base64UrlEncode(sha256(codeVerifier));

  // 2. Redirect to authorization endpoint
  const authUrl = `${AUTH_SERVER}/authorize?` +
      `client_id=${CLIENT_ID}&` +
      `redirect_uri=${REDIRECT_URI}&` +
      `response_type=code&` +
      `code_challenge=${codeChallenge}&` +
      `code_challenge_method=S256`;

  // 3. Exchange code for token
  const tokenResponse = await fetch(`${AUTH_SERVER}/token`, {
      method: 'POST',
      body: {
          grant_type: 'authorization_code',
          code: authorizationCode,
          redirect_uri: REDIRECT_URI,
          code_verifier: codeVerifier
      }
  });
  ```
- **Validación y Verificación de JWT**
  ```python
  import jwt
  from cryptography.hazmat.primitives import serialization

  def verify_jwt(token, public_key_pem):
      try:
          # Decode y verificar firma
          payload = jwt.decode(
              token,
              public_key_pem,
              algorithms=['RS256'],
              audience='your-api',
              issuer='https://auth.example.com'
          )

          # Validaciones adicionales
          if payload['exp'] < time.time():
              raise jwt.ExpiredSignatureError

          if 'required_scope' not in payload.get('scope', []):
              raise PermissionError

          return payload
      except jwt.InvalidTokenError as e:
          # Log y manejar
          pass
  ```
- **Token Refresh y Rotation**
  ```
  - Implementar refresh token rotation
  - Manejar token revocation
  - Blacklisting de tokens comprometidos
  ```

**Vulnerabilidades Críticas:**
- JWT algorithm confusion (none attack)
- Token replay attacks
- CSRF en OAuth flows
- Open redirects
- Insufficient scope validation

---

#### 3.2 Secrets Management
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Integración con Vaults**
  ```python
  # HashiCorp Vault
  import hvac

  client = hvac.Client(url='https://vault.example.com')
  client.auth.kubernetes.login(role='my-app', jwt=service_account_jwt)

  # Leer secret con auto-rotation
  def get_db_credentials():
      secret = client.secrets.database.generate_credentials(
          name='my-database',
          mount_point='database'
      )
      return secret['data']['username'], secret['data']['password']

  # Renovar lease automáticamente
  client.renew_secret(lease_id)
  ```
- **Encriptación en Código**
  ```go
  // Envelope encryption
  func encryptData(plaintext []byte, kmsClient *kms.Client) ([]byte, error) {
      // 1. Generate data key from KMS
      dataKeyResp, _ := kmsClient.GenerateDataKey(&kms.GenerateDataKeyInput{
          KeyId:   aws.String("alias/my-key"),
          KeySpec: aws.String("AES_256"),
      })

      // 2. Encrypt data with data key
      encryptedData := aesEncrypt(plaintext, dataKeyResp.Plaintext)

      // 3. Store encrypted data + encrypted data key
      return append(dataKeyResp.CiphertextBlob, encryptedData...), nil
  }
  ```
- **Rotation de Secrets**
  ```
  - Zero-downtime secret rotation
  - Dual-write durante transición
  - Rollback automático en fallas
  ```

**Patrones Seguros:**
- Never log secrets
- Use environment variables properly
- Implement least privilege access
- Audit secret access

---

#### 3.3 Rate Limiting y DDoS Protection
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Algoritmos de Rate Limiting**
  ```python
  # Token Bucket Algorithm
  class TokenBucket:
      def __init__(self, capacity, refill_rate):
          self.capacity = capacity
          self.tokens = capacity
          self.refill_rate = refill_rate  # tokens per second
          self.last_refill = time.time()

      def consume(self, tokens=1):
          self._refill()
          if self.tokens >= tokens:
              self.tokens -= tokens
              return True
          return False

      def _refill(self):
          now = time.time()
          elapsed = now - self.last_refill
          refill = elapsed * self.refill_rate
          self.tokens = min(self.capacity, self.tokens + refill)
          self.last_refill = now

  # Sliding Window Log
  class SlidingWindowLog:
      def __init__(self, max_requests, window_seconds):
          self.max_requests = max_requests
          self.window = window_seconds
          self.requests = []  # timestamps

      def allow_request(self):
          now = time.time()
          # Remove old requests
          self.requests = [r for r in self.requests if now - r < self.window]

          if len(self.requests) < self.max_requests:
              self.requests.append(now)
              return True
          return False
  ```
- **Rate Limiting Distribuido**
  ```lua
  -- Redis Lua script para rate limiting atómico
  local key = KEYS[1]
  local limit = tonumber(ARGV[1])
  local window = tonumber(ARGV[2])
  local current = redis.call('INCR', key)

  if current == 1 then
      redis.call('EXPIRE', key, window)
  end

  if current > limit then
      return 0
  end

  return 1
  ```
- **Adaptive Rate Limiting**
  ```
  - Ajustar límites basado en carga del sistema
  - Priorizar usuarios premium
  - Implementar backoff exponencial
  ```

**Técnicas Avanzadas:**
- Fingerprinting de bots
- Geo-blocking dinámico
- Challenge-response (CAPTCHA)
- Behavioral analysis

---

### DOMINIO 4: Datos y Consistencia

#### 4.1 Transaction Management en Microservicios
**Nivel de Dificultad:** ⭐⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Saga Orchestration**
  ```java
  // Orquestador de Saga
  public class OrderSaga {
      @Autowired
      private PaymentService paymentService;
      @Autowired
      private InventoryService inventoryService;
      @Autowired
      private ShippingService shippingService;

      public void executeOrderSaga(Order order) {
          SagaExecutionCoordinator coordinator = new SagaExecutionCoordinator();

          try {
              // Step 1: Reserve inventory
              coordinator.addStep(
                  () -> inventoryService.reserve(order.getItems()),
                  () -> inventoryService.cancelReservation(order.getItems())
              );

              // Step 2: Process payment
              coordinator.addStep(
                  () -> paymentService.charge(order.getTotal()),
                  () -> paymentService.refund(order.getPaymentId())
              );

              // Step 3: Create shipment
              coordinator.addStep(
                  () -> shippingService.createShipment(order),
                  () -> shippingService.cancelShipment(order.getShipmentId())
              );

              coordinator.execute();
          } catch (SagaExecutionException e) {
              // Automatic compensation
              coordinator.compensate();
              throw e;
          }
      }
  }
  ```
- **Saga Choreography (Event-Driven)**
  ```javascript
  // Order Service
  async function createOrder(orderData) {
      const order = await db.orders.create(orderData);
      await eventBus.publish('OrderCreated', { orderId: order.id });
      return order;
  }

  // Inventory Service
  eventBus.subscribe('OrderCreated', async (event) => {
      try {
          await reserveInventory(event.orderId);
          await eventBus.publish('InventoryReserved', { orderId: event.orderId });
      } catch (error) {
          await eventBus.publish('InventoryReservationFailed', {
              orderId: event.orderId,
              reason: error.message
          });
      }
  });

  // Payment Service
  eventBus.subscribe('InventoryReserved', async (event) => {
      try {
          await processPayment(event.orderId);
          await eventBus.publish('PaymentProcessed', { orderId: event.orderId });
      } catch (error) {
          await eventBus.publish('PaymentFailed', { orderId: event.orderId });
      }
  });

  // Compensación automática
  eventBus.subscribe('PaymentFailed', async (event) => {
      await inventoryService.cancelReservation(event.orderId);
      await orderService.markOrderFailed(event.orderId);
  });
  ```

**Patrones Críticos:**
- Outbox Pattern para atomicidad
- Idempotency keys
- State machines para tracking
- Timeout handling

---

#### 4.2 Read/Write Patterns y CQRS
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **CQRS Implementation**
  ```csharp
  // Command Model (Write)
  public class CreateOrderCommand : ICommand
  {
      public Guid OrderId { get; set; }
      public List<OrderItem> Items { get; set; }
  }

  public class CreateOrderHandler : ICommandHandler<CreateOrderCommand>
  {
      private readonly IEventStore _eventStore;

      public async Task Handle(CreateOrderCommand command)
      {
          var order = new Order(command.OrderId);
          order.AddItems(command.Items);

          // Persist events
          var events = order.GetUncommittedEvents();
          await _eventStore.SaveEvents(command.OrderId, events);

          // Publish for read model update
          await _eventBus.PublishAll(events);
      }
  }

  // Query Model (Read)
  public class OrderQueryService
  {
      private readonly IReadDatabase _readDb;

      public async Task<OrderDTO> GetOrder(Guid orderId)
      {
          // Read from optimized read model
          return await _readDb.Orders
              .Include(o => o.Items)
              .Include(o => o.Customer)
              .FirstOrDefaultAsync(o => o.Id == orderId);
      }
  }

  // Projection (Event Handler para actualizar read model)
  public class OrderProjection : IEventHandler<OrderCreatedEvent>
  {
      private readonly IReadDatabase _readDb;

      public async Task Handle(OrderCreatedEvent @event)
      {
          var orderDto = new OrderDTO
          {
              Id = @event.OrderId,
              CustomerId = @event.CustomerId,
              Status = "Pending",
              CreatedAt = @event.Timestamp
          };

          await _readDb.Orders.AddAsync(orderDto);
          await _readDb.SaveChangesAsync();
      }
  }
  ```
- **Event Sourcing**
  ```python
  # Aggregate Root
  class BankAccount:
      def __init__(self, account_id):
          self.account_id = account_id
          self.balance = 0
          self.events = []

      def deposit(self, amount):
          event = MoneyDepositedEvent(self.account_id, amount, datetime.now())
          self.apply(event)
          self.events.append(event)

      def withdraw(self, amount):
          if self.balance < amount:
              raise InsufficientFundsError()

          event = MoneyWithdrawnEvent(self.account_id, amount, datetime.now())
          self.apply(event)
          self.events.append(event)

      def apply(self, event):
          if isinstance(event, MoneyDepositedEvent):
              self.balance += event.amount
          elif isinstance(event, MoneyWithdrawnEvent):
              self.balance -= event.amount

      @staticmethod
      def from_events(events):
          account = BankAccount(events[0].account_id)
          for event in events:
              account.apply(event)
          return account

  # Replay events para reconstruir estado
  def get_account(account_id):
      events = event_store.get_events(account_id)
      return BankAccount.from_events(events)
  ```

**Desafíos de Implementación:**
- Eventual consistency entre write y read models
- Snapshotting para performance
- Evolución de schemas de eventos
- Replay de eventos para debugging

---

#### 4.3 Multi-Tenancy y Data Isolation
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Estrategias de Tenancy**
  ```sql
  -- 1. Shared Database, Shared Schema
  CREATE TABLE orders (
      id UUID PRIMARY KEY,
      tenant_id UUID NOT NULL,  -- Discriminator
      customer_name VARCHAR(100),
      total DECIMAL(10,2)
  );
  CREATE INDEX idx_tenant ON orders(tenant_id);

  -- Row-Level Security (PostgreSQL)
  CREATE POLICY tenant_isolation ON orders
      USING (tenant_id = current_setting('app.current_tenant')::UUID);

  -- 2. Shared Database, Separate Schemas
  CREATE SCHEMA tenant_acme;
  CREATE TABLE tenant_acme.orders (...);

  CREATE SCHEMA tenant_globex;
  CREATE TABLE tenant_globex.orders (...);

  -- 3. Separate Databases
  -- tenant_acme_db
  -- tenant_globex_db
  ```
- **Tenant Context Propagation**
  ```java
  // Middleware para identificar tenant
  @Component
  public class TenantFilter implements Filter {
      @Override
      public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) {
          HttpServletRequest httpRequest = (HttpServletRequest) request;
          String tenantId = extractTenantId(httpRequest);

          TenantContext.setCurrentTenant(tenantId);
          try {
              chain.doFilter(request, response);
          } finally {
              TenantContext.clear();
          }
      }
  }

  // Repository con tenant awareness
  @Repository
  public class OrderRepository {
      @PersistenceContext
      private EntityManager entityManager;

      public List<Order> findOrders() {
          String tenantId = TenantContext.getCurrentTenant();
          return entityManager
              .createQuery("SELECT o FROM Order o WHERE o.tenantId = :tenantId")
              .setParameter("tenantId", tenantId)
              .getResultList();
      }
  }

  // Hibernate Interceptor para tenant automático
  public class TenantInterceptor extends EmptyInterceptor {
      @Override
      public boolean onSave(Object entity, Serializable id, Object[] state, String[] propertyNames, Type[] types) {
          if (entity instanceof TenantAware) {
              String tenantId = TenantContext.getCurrentTenant();
              ((TenantAware) entity).setTenantId(tenantId);
          }
          return super.onSave(entity, id, state, propertyNames, types);
      }
  }
  ```

**Consideraciones Críticas:**
- Cross-tenant data leak prevention
- Query performance con millones de tenants
- Tenant-specific customizations
- Backup y restore por tenant

---

### DOMINIO 5: Integración y Modernización

#### 5.1 Strangler Fig Pattern (Migración de Legacy)
**Nivel de Dificultad:** ⭐⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Proxy/Gateway para Routing**
  ```nginx
  # NGINX como proxy de strangler
  upstream legacy_app {
      server legacy.internal.com:8080;
  }

  upstream new_service {
      server new-service.internal.com:8080;
  }

  server {
      listen 80;

      # Rutas migradas al nuevo servicio
      location /api/v2/orders {
          proxy_pass http://new_service;
      }

      location /api/v2/customers {
          proxy_pass http://new_service;
      }

      # Rutas aún en legacy
      location / {
          proxy_pass http://legacy_app;
      }
  }
  ```
  ```javascript
  // API Gateway programático
  const express = require('express');
  const httpProxy = require('http-proxy');

  const app = express();
  const legacyProxy = httpProxy.createProxyServer({ target: 'http://legacy:8080' });
  const newProxy = httpProxy.createProxyServer({ target: 'http://new-service:8080' });

  // Feature flags para gradual rollout
  const featureFlags = {
      'orders-v2': { enabled: true, percentage: 50 },
      'customers-v2': { enabled: true, percentage: 100 }
  };

  app.use('/api/orders', (req, res) => {
      if (shouldUseNewService('orders-v2', req.user)) {
          newProxy.web(req, res);
      } else {
          legacyProxy.web(req, res);
      }
  });

  function shouldUseNewService(feature, user) {
      const flag = featureFlags[feature];
      if (!flag.enabled) return false;

      // Canary release: percentage of users
      return (hash(user.id) % 100) < flag.percentage;
  }
  ```
- **Sincronización Bidireccional de Datos**
  ```python
  # Change Data Capture para sincronización
  class DataSynchronizer:
      def __init__(self, legacy_db, new_db, event_bus):
          self.legacy_db = legacy_db
          self.new_db = new_db
          self.event_bus = event_bus

      def sync_from_legacy_to_new(self):
          # Escuchar cambios en legacy DB
          for change in self.legacy_db.listen_changes():
              if change.table == 'customers':
                  customer = self.transform_legacy_to_new(change.data)
                  self.new_db.upsert_customer(customer)
                  self.event_bus.publish('CustomerSynced', customer)

      def sync_from_new_to_legacy(self):
          # Escuchar eventos del nuevo sistema
          self.event_bus.subscribe('CustomerUpdated', self.update_legacy)

      def update_legacy(self, event):
          legacy_format = self.transform_new_to_legacy(event.customer)
          self.legacy_db.update_customer(legacy_format)
  ```
- **Anti-Corruption Layer**
  ```java
  // Traductor entre modelos legacy y nuevos
  @Component
  public class CustomerAntiCorruptionLayer {

      public NewCustomer translateFromLegacy(LegacyCustomer legacy) {
          return NewCustomer.builder()
              .id(UUID.fromString(legacy.getCustNo()))
              .fullName(legacy.getFname() + " " + legacy.getLname())
              .email(normalizeEmail(legacy.getEmail()))
              .address(parseAddress(legacy.getAddr()))
              .build();
      }

      public LegacyCustomer translateToLegacy(NewCustomer customer) {
          LegacyCustomer legacy = new LegacyCustomer();
          legacy.setCustNo(customer.getId().toString());
          String[] names = customer.getFullName().split(" ", 2);
          legacy.setFname(names[0]);
          legacy.setLname(names.length > 1 ? names[1] : "");
          legacy.setEmail(customer.getEmail());
          legacy.setAddr(formatAddress(customer.getAddress()));
          return legacy;
      }
  }
  ```

**Estrategias de Migración:**
- Database replication para doble escritura
- Event-driven sync
- Gradual feature migration con feature flags
- Rollback strategy

---

#### 5.2 API Versioning y Backward Compatibility
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Estrategias de Versionado**
  ```
  1. URL Versioning: /api/v1/users, /api/v2/users
  2. Header Versioning: Accept: application/vnd.api.v2+json
  3. Query Parameter: /api/users?version=2
  ```
  ```python
  # Versionado por headers con FastAPI
  from fastapi import FastAPI, Header

  app = FastAPI()

  @app.get("/users/{user_id}")
  async def get_user(
      user_id: int,
      api_version: str = Header("1", alias="API-Version")
  ):
      if api_version == "1":
          return get_user_v1(user_id)
      elif api_version == "2":
          return get_user_v2(user_id)
      else:
          raise HTTPException(400, "Unsupported API version")

  def get_user_v1(user_id):
      user = db.get_user(user_id)
      return {
          "id": user.id,
          "name": user.name,
          "email": user.email
      }

  def get_user_v2(user_id):
      user = db.get_user(user_id)
      return {
          "id": user.id,
          "profile": {
              "full_name": user.name,
              "contact": {
                  "email": user.email,
                  "phone": user.phone
              }
          },
          "metadata": {
              "created_at": user.created_at,
              "updated_at": user.updated_at
          }
      }
  ```
- **Deprecation Strategies**
  ```javascript
  // Gradual deprecation con warnings
  app.get('/api/v1/users/:id', (req, res) => {
      res.setHeader('Deprecation', 'true');
      res.setHeader('Sunset', 'Wed, 31 Dec 2025 23:59:59 GMT');
      res.setHeader('Link', '</api/v2/users>; rel="successor-version"');

      // Log usage para analytics
      analytics.track('deprecated_endpoint_usage', {
          endpoint: '/api/v1/users',
          client: req.headers['user-agent'],
          timestamp: new Date()
      });

      // Retornar datos en formato v1
      const user = await getUserV1(req.params.id);
      res.json(user);
  });
  ```
- **Schema Evolution**
  ```protobuf
  // Protobuf - Backward compatible changes
  message UserV1 {
      int64 id = 1;
      string name = 2;
      string email = 3;
  }

  message UserV2 {
      int64 id = 1;
      string name = 2;
      string email = 3;
      string phone = 4;           // Nuevo campo (opcional)
      repeated Address addresses = 5;  // Nuevo campo
      reserved 6;                 // Reservado para futuro
  }
  ```

**Testing de Compatibilidad:**
- Contract testing (Pact, Spring Cloud Contract)
- Regression testing entre versiones
- Canary deployments por versión

---

#### 5.3 GraphQL Federation y Supergraphs
**Nivel de Dificultad:** ⭐⭐⭐⭐

**Conocimientos de Código Requeridos:**
- **Apollo Federation Implementation**
  ```javascript
  // Subgraph 1: Users Service
  const { buildSubgraphSchema } = require('@apollo/subgraph');
  const { gql } = require('apollo-server');

  const typeDefs = gql`
      type User @key(fields: "id") {
          id: ID!
          username: String!
          email: String!
      }
  `;

  const resolvers = {
      User: {
          __resolveReference(user, { dataSources }) {
              return dataSources.usersAPI.getUserById(user.id);
          }
      },
      Query: {
          user: (_, { id }, { dataSources }) => {
              return dataSources.usersAPI.getUserById(id);
          }
      }
  };

  // Subgraph 2: Orders Service
  const typeDefs = gql`
      extend type User @key(fields: "id") {
          id: ID! @external
          orders: [Order!]!
      }

      type Order @key(fields: "id") {
          id: ID!
          product: String!
          total: Float!
          user: User!
      }
  `;

  const resolvers = {
      User: {
          orders(user, _, { dataSources }) {
              return dataSources.ordersAPI.getOrdersByUserId(user.id);
          }
      },
      Order: {
          user(order) {
              return { __typename: 'User', id: order.userId };
          }
      }
  };

  // Gateway (Router)
  const { ApolloGateway } = require('@apollo/gateway');

  const gateway = new ApolloGateway({
      supergraphSdl: composedSchema,  // Schema composition
      buildService({ url }) {
          return new RemoteGraphQLDataSource({ url });
      }
  });
  ```
- **N+1 Problem Solving**
  ```javascript
  // DataLoader para batching
  const DataLoader = require('dataloader');

  const userLoader = new DataLoader(async (userIds) => {
      const users = await db.users.find({ id: { $in: userIds } });
      return userIds.map(id => users.find(u => u.id === id));
  });

  const resolvers = {
      Order: {
          user(order, _, { loaders }) {
              // Batch multiple requests
              return loaders.userLoader.load(order.userId);
          }
      }
  };
  ```

**Desafíos de Federación:**
- Schema composition conflicts
- Cross-service authentication
- Distributed tracing
- Performance optimization

---

## Matriz de Priorización

| Tema | Complejidad | Impacto Negocio | Conocimiento Código | Dificultad Debug | Prioridad |
|------|-------------|-----------------|---------------------|------------------|-----------|
| Consistencia Eventual & CAP | 5 | 5 | 5 | 5 | **CRÍTICA** |
| Transaction Management (Sagas) | 5 | 5 | 5 | 5 | **CRÍTICA** |
| Strangler Fig Pattern | 5 | 5 | 4 | 5 | **CRÍTICA** |
| Service Mesh | 5 | 4 | 4 | 5 | **CRÍTICA** |
| Database Sharding | 5 | 5 | 5 | 4 | **CRÍTICA** |
| OAuth2 & JWT Security | 5 | 5 | 4 | 3 | **ALTA** |
| CQRS & Event Sourcing | 4 | 4 | 5 | 4 | **ALTA** |
| Multi-Tenancy | 4 | 5 | 4 | 4 | **ALTA** |
| Message Brokers Async | 4 | 4 | 4 | 4 | **ALTA** |
| Caching Distribuido | 4 | 4 | 3 | 3 | **ALTA** |
| Rate Limiting & DDoS | 4 | 5 | 3 | 3 | **ALTA** |
| API Versioning | 4 | 4 | 3 | 3 | **MEDIA** |
| GraphQL Federation | 4 | 3 | 4 | 3 | **MEDIA** |
| Connection Pooling | 4 | 3 | 3 | 4 | **MEDIA** |
| Secrets Management | 4 | 5 | 3 | 2 | **MEDIA** |

---

## Plan de Acción para el Curso

### Módulo 1: Fundamentos de Sistemas Distribuidos (Semanas 1-3)
**Objetivo:** Dominar los conceptos core que causan el 80% de los problemas en producción

**Temas:**
1. **CAP Theorem y Consistencia Eventual**
   - Teoría: CAP, BASE, PACELC
   - Práctica: Implementar Saga Pattern (Choreography y Orchestration)
   - Debugging: Resolver inconsistencias en sistemas distribuidos

2. **Comunicación Asíncrona**
   - Kafka: Partitions, Consumer Groups, Exactly-once semantics
   - RabbitMQ: Exchanges, Dead Letter Queues
   - Proyecto: Sistema de pedidos con compensación automática

**Código a Escribir:**
- Saga orchestrator en Java/Spring
- Event-driven choreography con Kafka
- Dead Letter Queue handler
- Idempotency implementation

---

### Módulo 2: Performance y Escalabilidad (Semanas 4-5)
**Objetivo:** Diseñar sistemas que escalen a millones de usuarios

**Temas:**
1. **Caching Strategies**
   - Redis: Structures, Lua scripts, Cluster
   - Cache invalidation patterns
   - Proyecto: Implementar cache multi-nivel

2. **Database Sharding**
   - Sharding strategies (range, hash, geographic)
   - Cross-shard queries
   - Proyecto: Sharding de una aplicación monolítica

**Código a Escribir:**
- Shard router en Go
- Cache-aside pattern
- Consistent hashing implementation
- Read-through cache

---

### Módulo 3: Seguridad Profunda (Semanas 6-7)
**Objetivo:** Implementar seguridad defense-in-depth

**Temas:**
1. **OAuth2 & JWT**
   - Flows: Authorization Code, Client Credentials, PKCE
   - JWT validation y verification
   - Proyecto: Auth service completo

2. **Rate Limiting & DDoS**
   - Token bucket, Sliding window
   - Distributed rate limiting con Redis
   - Proyecto: API Gateway con rate limiting

**Código a Escribir:**
- OAuth2 server (Authorization Code + PKCE)
- JWT middleware con refresh rotation
- Rate limiter distribuido
- WAF básico

---

### Módulo 4: Datos y Consistencia (Semanas 8-9)
**Objetivo:** Manejar datos en arquitecturas complejas

**Temas:**
1. **CQRS & Event Sourcing**
   - Separación de read/write models
   - Event store implementation
   - Proyecto: Sistema bancario con event sourcing

2. **Multi-Tenancy**
   - Estrategias de aislamiento
   - Tenant context propagation
   - Proyecto: SaaS platform con multi-tenancy

**Código a Escribir:**
- CQRS implementation en C#
- Event store con snapshots
- Tenant-aware repository
- Row-level security

---

### Módulo 5: Modernización Legacy (Semanas 10-12)
**Objetivo:** Migrar sistemas legacy sin downtime

**Temas:**
1. **Strangler Fig Pattern**
   - Proxy-based routing
   - Data synchronization
   - Proyecto: Migrar monolito a microservicios

2. **API Evolution**
   - Versioning strategies
   - Backward compatibility
   - Proyecto: API v2 con soporte v1

**Código a Escribir:**
- Strangler proxy en NGINX
- CDC (Change Data Capture) synchronizer
- Anti-corruption layer
- API version router

---

## Evaluación de Dominio

Para cada tema, el arquitecto debe poder:

### 1. **Explicar** (Nivel Teórico)
- Cuándo usar la técnica
- Trade-offs y limitaciones
- Alternativas disponibles

### 2. **Implementar** (Nivel Código)
- Escribir código funcional desde cero
- Configurar herramientas correctamente
- Seguir best practices

### 3. **Debuggear** (Nivel Experto)
- Identificar problemas en producción
- Usar herramientas de observabilidad
- Resolver incidentes críticos

### 4. **Decidir** (Nivel Arquitecto)
- Evaluar múltiples soluciones
- Considerar contexto del negocio
- Documentar decisiones (ADRs)

---

## Recursos de Código por Tema

### Repositorios de Referencia
```
1. Sistemas Distribuidos:
   - github.com/eventuate-examples/eventuate-tram-sagas
   - github.com/temporal-io/samples-java

2. Caching:
   - github.com/redis/redis
   - github.com/twitter/twemproxy

3. Security:
   - github.com/ory/hydra (OAuth2)
   - github.com/auth0/node-jsonwebtoken

4. CQRS:
   - github.com/EventStore/EventStore
   - github.com/axonframework/axon-server

5. Modernización:
   - github.com/Netflix (Strangler examples)
```

### Labs Prácticos
```
1. Implementar Saga pattern para e-commerce checkout
2. Sharding de base de datos con rebalancing automático
3. OAuth2 server con PKCE y refresh rotation
4. Sistema bancario con event sourcing
5. Migración legacy con Strangler Fig
```

---

## Próximos Pasos

1. **Validar con Expertos:** Revisar este plan con arquitectos senior
2. **Priorizar por Industria:** Ajustar según sector (fintech, e-commerce, SaaS)
3. **Crear Ejercicios:** Desarrollar labs prácticos para cada tema
4. **Casos de Estudio:** Documentar incidentes reales de producción
5. **Certificaciones:** Mapear a AWS SAP, GCP PCA, TOGAF

---

## Conclusión

Los temas más difíciles para un arquitecto requieren **profundo conocimiento de código** para:
- Implementar soluciones complejas desde cero
- Debuggear problemas de producción
- Evaluar trade-offs técnicos
- Tomar decisiones informadas

Este plan cubre los **15 temas críticos** que separan a un arquitecto competente de uno excepcional, con énfasis en habilidades prácticas de programación que permiten resolver los problemas más desafiantes en sistemas modernos.
