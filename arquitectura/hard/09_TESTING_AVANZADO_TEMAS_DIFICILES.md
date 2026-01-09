# Conocimientos Técnicos Difíciles: Testing Avanzado

## Objetivo
Temas complejos de testing más allá de unit tests básicos que un arquitecto debe dominar para garantizar calidad y confiabilidad en sistemas complejos.

---

## CATEGORÍA 1: Testing Strategies

### 1.1 Contract Testing
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# Pact - Consumer-Driven Contract Testing
from pact import Consumer, Provider, Like, EachLike
import unittest

# Consumer side
class UserServiceConsumerTest(unittest.TestCase):
    def setUp(self):
        self.pact = Consumer('UserService').has_pact_with(
            Provider('OrderService'),
            pact_dir='./pacts'
        )

    def test_get_user_orders(self):
        # Define expected interaction
        expected = {
            'user_id': '123',
            'orders': EachLike({
                'id': Like('order-1'),
                'total': Like(99.99),
                'status': Like('completed')
            })
        }

        (self.pact
         .given('user 123 has orders')
         .upon_receiving('a request for user orders')
         .with_request('GET', '/users/123/orders')
         .will_respond_with(200, body=expected))

        with self.pact:
            # Make actual call
            result = OrderServiceClient().get_user_orders('123')
            assert len(result['orders']) > 0

# Provider side verification
from pact import Verifier

verifier = Verifier(
    provider='OrderService',
    provider_base_url='http://localhost:8080'
)

# Verify against consumer pacts
output, _ = verifier.verify_pacts('./pacts/userservice-orderservice.json')
```

**Spring Cloud Contract (Java):**

```groovy
// contracts/shouldReturnUser.groovy
Contract.make {
    request {
        method 'GET'
        url '/api/users/1'
        headers {
            contentType(applicationJson())
        }
    }
    response {
        status OK()
        body([
            id: 1,
            name: 'John Doe',
            email: 'john@example.com'
        ])
        headers {
            contentType(applicationJson())
        }
    }
}
```

---

### 1.2 Property-Based Testing
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# Hypothesis - Property-based testing
from hypothesis import given, strategies as st
import hypothesis.stateful as stateful

# 1. Basic property testing
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Addition should be commutative"""
    assert a + b == b + a

@given(st.lists(st.integers()))
def test_reverse_twice_is_identity(lst):
    """Reversing twice should give original list"""
    assert list(reversed(list(reversed(lst)))) == lst

# 2. Testing data structures
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

# Stateful testing
class StackStateMachine(stateful.RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.stack = Stack()
        self.model = []

    @stateful.rule(value=st.integers())
    def push(self, value):
        self.stack.push(value)
        self.model.append(value)

    @stateful.rule()
    def pop(self):
        if self.model:
            assert self.stack.pop() == self.model.pop()
        else:
            with pytest.raises(IndexError):
                self.stack.pop()

    @stateful.invariant()
    def sizes_match(self):
        assert self.stack.is_empty() == (len(self.model) == 0)

TestStack = StackStateMachine.TestCase

# 3. Complex domain testing
@given(
    st.builds(
        Order,
        id=st.uuids(),
        items=st.lists(
            st.builds(
                OrderItem,
                product_id=st.uuids(),
                quantity=st.integers(min_value=1, max_value=100),
                unit_price=st.decimals(min_value=0.01, max_value=10000, places=2)
            ),
            min_size=1
        )
    )
)
def test_order_total_is_sum_of_items(order):
    """Order total should equal sum of all item subtotals"""
    expected_total = sum(
        item.quantity * item.unit_price
        for item in order.items
    )
    assert order.total() == expected_total
```

---

### 1.3 Chaos Engineering
**Dificultad:** ⭐⭐⭐⭐⭐

```python
# Chaos Toolkit
from chaoslib.types import Configuration, Secrets
from chaostoolkit.experiment import run_experiment

# chaos-experiment.json
experiment = {
    "version": "1.0.0",
    "title": "System survives pod failures",
    "description": "Kill pods and verify system recovery",

    "steady-state-hypothesis": {
        "title": "Application is healthy",
        "probes": [
            {
                "type": "probe",
                "name": "app-responds-to-requests",
                "tolerance": 200,
                "provider": {
                    "type": "http",
                    "url": "http://myapp/health",
                    "timeout": 3
                }
            }
        ]
    },

    "method": [
        {
            "type": "action",
            "name": "terminate-random-pod",
            "provider": {
                "type": "python",
                "module": "chaosk8s.pod.actions",
                "func": "terminate_pods",
                "arguments": {
                    "label_selector": "app=myapp",
                    "qty": 1,
                    "rand": True
                }
            },
            "pauses": {
                "after": 10
            }
        }
    ],

    "rollbacks": []
}

# Run experiment
run_experiment(experiment)
```

**Toxiproxy (Network chaos):**

```python
from toxiproxy import Toxiproxy

toxiproxy = Toxiproxy()

# Create proxy for database
db_proxy = toxiproxy.create(
    name="database",
    listen="localhost:3307",
    upstream="database:3306"
)

# Add latency toxic
db_proxy.add_toxic(
    name="latency_downstream",
    type="latency",
    attributes={"latency": 1000}  # 1s delay
)

# Test application under latency
def test_app_handles_slow_database():
    response = requests.get("http://app/api/data")
    assert response.status_code == 200
    # Should implement timeout/fallback

# Add bandwidth limitation
db_proxy.add_toxic(
    name="bandwidth_limit",
    type="bandwidth",
    attributes={"rate": 10}  # 10 KB/s
)

# Simulate connection cuts
db_proxy.add_toxic(
    name="connection_cut",
    type="timeout",
    attributes={"timeout": 0}
)
```

---

## CATEGORÍA 2: Load & Performance Testing

### 2.1 k6 Load Testing
**Dificultad:** ⭐⭐⭐⭐

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const checkoutDuration = new Trend('checkout_duration');

// Test configuration
export const options = {
    stages: [
        { duration: '2m', target: 100 },  // Ramp up
        { duration: '5m', target: 100 },  // Stay at 100 users
        { duration: '2m', target: 200 },  // Ramp to 200
        { duration: '5m', target: 200 },  // Stay at 200
        { duration: '2m', target: 0 },    // Ramp down
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% under 500ms
        http_req_failed: ['rate<0.01'],   // <1% errors
        errors: ['rate<0.1'],             // <10% business errors
    },
};

// Test scenario
export default function () {
    // 1. Browse products
    let response = http.get('https://api.example.com/products');

    check(response, {
        'products loaded': (r) => r.status === 200,
        'has products': (r) => JSON.parse(r.body).length > 0,
    });

    sleep(1);

    // 2. Add to cart
    const product = JSON.parse(response.body)[0];

    response = http.post(
        'https://api.example.com/cart',
        JSON.stringify({
            product_id: product.id,
            quantity: 1,
        }),
        {
            headers: { 'Content-Type': 'application/json' },
        }
    );

    check(response, {
        'added to cart': (r) => r.status === 200,
    }) || errorRate.add(1);

    sleep(2);

    // 3. Checkout
    const start = Date.now();

    response = http.post('https://api.example.com/checkout', JSON.stringify({
        payment_method: 'credit_card',
    }), {
        headers: { 'Content-Type': 'application/json' },
    });

    const duration = Date.now() - start;
    checkoutDuration.add(duration);

    check(response, {
        'checkout successful': (r) => r.status === 200,
        'order created': (r) => JSON.parse(r.body).order_id !== undefined,
    }) || errorRate.add(1);

    sleep(1);
}

// Thresholds alerts
export function handleSummary(data) {
    return {
        'summary.json': JSON.stringify(data),
        stdout: textSummary(data, { indent: ' ', enableColors: true }),
    };
}
```

---

### 2.2 JMeter para APIs complejas
**Dificultad:** ⭐⭐⭐⭐

```xml
<!-- JMeter Test Plan (via code) -->
<jmeterTestPlan>
  <hashTree>
    <TestPlan>
      <stringProp name="TestPlan.comments">API Load Test</stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables">
        <collectionProp name="Arguments.arguments">
          <elementProp name="HOST" elementType="Argument">
            <stringProp name="Argument.value">api.example.com</stringProp>
          </elementProp>
          <elementProp name="USERS" elementType="Argument">
            <stringProp name="Argument.value">100</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>

    <ThreadGroup>
      <stringProp name="ThreadGroup.num_threads">${USERS}</stringProp>
      <stringProp name="ThreadGroup.ramp_time">60</stringProp>
      <stringProp name="ThreadGroup.duration">300</stringProp>
    </ThreadGroup>

    <!-- HTTP Sampler -->
    <HTTPSamplerProxy>
      <stringProp name="HTTPSampler.domain">${HOST}</stringProp>
      <stringProp name="HTTPSampler.path">/api/products</stringProp>
      <stringProp name="HTTPSampler.method">GET</stringProp>
    </HTTPSamplerProxy>

    <!-- Assertions -->
    <ResponseAssertion>
      <collectionProp name="Asserion.test_strings">
        <stringProp name="200">200</stringProp>
      </collectionProp>
      <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
    </ResponseAssertion>

    <!-- Listeners -->
    <ResultCollector>
      <stringProp name="filename">results.jtl</stringProp>
    </ResultCollector>
  </hashTree>
</jmeterTestPlan>
```

---

## CATEGORÍA 3: Security Testing

### 3.1 OWASP ZAP Automation
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from zapv2 import ZAPv2
import time

# Initialize ZAP
zap = ZAPv2(apikey='your-api-key', proxies={
    'http': 'http://localhost:8080',
    'https': 'http://localhost:8080'
})

target = 'https://example.com'

# 1. Spider (Crawl application)
print('Spidering target...')
scan_id = zap.spider.scan(target)

while int(zap.spider.status(scan_id)) < 100:
    print(f'Spider progress: {zap.spider.status(scan_id)}%')
    time.sleep(2)

print('Spider completed')

# 2. Ajax Spider (for SPAs)
print('Ajax spidering...')
zap.ajaxSpider.scan(target)

while zap.ajaxSpider.status == 'running':
    print('Ajax spider running...')
    time.sleep(2)

# 3. Active Scan (Vulnerability scanning)
print('Active scanning...')
scan_id = zap.ascan.scan(target)

while int(zap.ascan.status(scan_id)) < 100:
    print(f'Scan progress: {zap.ascan.status(scan_id)}%')
    time.sleep(5)

# 4. Get results
print('Scan completed. Analyzing results...')

alerts = zap.core.alerts(baseurl=target)

# Group by risk level
high_risk = [a for a in alerts if a['risk'] == 'High']
medium_risk = [a for a in alerts if a['risk'] == 'Medium']
low_risk = [a for a in alerts if a['risk'] == 'Low']

print(f'High risk: {len(high_risk)}')
print(f'Medium risk: {len(medium_risk)}')
print(f'Low risk: {len(low_risk)}')

# 5. Generate report
html_report = zap.core.htmlreport()
with open('zap_report.html', 'w') as f:
    f.write(html_report)

# Fail build if high-risk vulnerabilities
if len(high_risk) > 0:
    print('HIGH RISK VULNERABILITIES FOUND!')
    for alert in high_risk:
        print(f"- {alert['alert']}: {alert['url']}")
    exit(1)
```

---

### 3.2 SQL Injection Testing
**Dificultad:** ⭐⭐⭐⭐

```python
# sqlmap automation
import subprocess
import json

def test_sql_injection(target_url, params):
    """
    Automated SQL injection testing
    """
    cmd = [
        'sqlmap',
        '-u', target_url,
        '--data', params,
        '--batch',              # Non-interactive
        '--level=5',            # Thoroughness level
        '--risk=3',             # Risk level
        '--tamper=space2comment', # Evasion technique
        '--technique=BEUSTQ',   # All techniques
        '--threads=10',
        '--output-dir=./sqlmap-results',
        '--flush-session'
    ]

    # Run sqlmap
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse results
    if 'vulnerable' in result.stdout.lower():
        return {
            'vulnerable': True,
            'details': result.stdout
        }

    return {'vulnerable': False}

# Example usage
result = test_sql_injection(
    'https://example.com/api/search',
    'query=test&category=all'
)

if result['vulnerable']:
    print('SQL INJECTION VULNERABILITY FOUND!')
    print(result['details'])
```

---

## CATEGORÍA 4: Mutation Testing

### 4.1 PITest (Java)
**Dificultad:** ⭐⭐⭐⭐⭐

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <configuration>
        <targetClasses>
            <param>com.example.*</param>
        </targetClasses>
        <targetTests>
            <param>com.example.*Test</param>
        </targetTests>
        <mutators>
            <mutator>STRONGER</mutator>
        </mutators>
        <outputFormats>
            <outputFormat>HTML</outputFormat>
            <outputFormat>XML</outputFormat>
        </outputFormats>
        <timeoutConstant>5000</timeoutConstant>
        <threads>4</threads>
    </configuration>
</plugin>
```

```java
// Example: Testing business logic
public class DiscountCalculator {
    public double calculateDiscount(double price, int quantity) {
        if (quantity >= 100) {
            return price * 0.15;  // 15% discount
        } else if (quantity >= 50) {
            return price * 0.10;  // 10% discount
        } else if (quantity >= 10) {
            return price * 0.05;  // 5% discount
        }
        return 0;
    }
}

// Tests (PITest will mutate code and check if tests catch mutations)
class DiscountCalculatorTest {
    @Test
    void shouldGive15PercentFor100Items() {
        DiscountCalculator calc = new DiscountCalculator();
        double discount = calc.calculateDiscount(100, 100);
        assertEquals(15.0, discount, 0.01);
    }

    @Test
    void shouldGive10PercentFor50Items() {
        DiscountCalculator calc = new DiscountCalculator();
        double discount = calc.calculateDiscount(100, 50);
        assertEquals(10.0, discount, 0.01);
    }

    // Edge cases (catch boundary mutations)
    @Test
    void shouldGive15PercentFor100ItemsExactly() {
        DiscountCalculator calc = new DiscountCalculator();
        double discount = calc.calculateDiscount(100, 100);
        assertEquals(15.0, discount, 0.01);
    }

    @Test
    void shouldGive10PercentFor99Items() {
        DiscountCalculator calc = new DiscountCalculator();
        double discount = calc.calculateDiscount(100, 99);
        assertEquals(10.0, discount, 0.01);
    }
}
```

---

## Resumen Prioridades Testing

| Tema | Dificultad | Criticidad | ROI | Prioridad |
|------|------------|------------|-----|-----------|
| Contract Testing | 5 | 5 | 5 | **CRÍTICA** |
| Property-Based Testing | 5 | 4 | 4 | **ALTA** |
| Chaos Engineering | 5 | 5 | 4 | **CRÍTICA** |
| Load Testing (k6) | 4 | 5 | 5 | **CRÍTICA** |
| Security Testing (ZAP) | 5 | 5 | 5 | **CRÍTICA** |
| Mutation Testing | 5 | 3 | 3 | **MEDIA** |

**Total:** 12+ técnicas avanzadas de testing
