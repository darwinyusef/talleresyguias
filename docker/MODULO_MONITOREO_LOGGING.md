# Módulo: Monitoreo y Logging

## Objetivo
Implementar observabilidad completa en aplicaciones Docker usando Prometheus, Grafana, ELK Stack y otras herramientas.

---

## Índice
1. [Prometheus + Grafana](#prometheus-grafana)
2. [ELK Stack (Elasticsearch, Logstash, Kibana)](#elk-stack)
3. [Loki + Grafana](#loki)
4. [Jaeger (Distributed Tracing)](#jaeger)
5. [cAdvisor](#cadvisor)

---

## Prometheus + Grafana

### Stack Completo

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Prometheus - Métricas
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - monitoring

  # Grafana - Visualización
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    networks:
      - monitoring

  # Node Exporter - Métricas del sistema
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    networks:
      - monitoring

  # cAdvisor - Métricas de contenedores
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    networks:
      - monitoring

  # Aplicación de ejemplo
  app:
    build: ./app
    ports:
      - "8000:8000"
    networks:
      - monitoring

volumes:
  prometheus_data:
  grafana_data:

networks:
  monitoring:
    driver: bridge
```

**prometheus.yml:**
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Prometheus self
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  # cAdvisor
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  # Aplicación
  - job_name: 'app'
    static_configs:
      - targets: ['app:8000']
```

### Instrumentar Aplicación (Python/FastAPI)

**app.py:**
```python
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time

app = FastAPI()

# Métricas
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total de requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'app_request_duration_seconds',
    'Duración de requests',
    ['method', 'endpoint']
)

@app.middleware("http")
async def prometheus_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/metrics")
async def metrics():
    return generate_latest(REGISTRY)
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
prometheus-client==0.19.0
```

### Instrumentar Aplicación (Node.js/Express)

**app.js:**
```javascript
const express = require('express')
const promClient = require('prom-client')

const app = express()

// Métricas default (CPU, memoria, etc.)
promClient.collectDefaultMetrics()

// Métricas custom
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duración de requests HTTP',
  labelNames: ['method', 'route', 'status_code']
})

const httpRequestCounter = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total de requests HTTP',
  labelNames: ['method', 'route', 'status_code']
})

// Middleware
app.use((req, res, next) => {
  const start = Date.now()

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000

    httpRequestDuration.labels(
      req.method,
      req.route?.path || req.path,
      res.statusCode
    ).observe(duration)

    httpRequestCounter.labels(
      req.method,
      req.route?.path || req.path,
      res.statusCode
    ).inc()
  })

  next()
})

// Endpoints
app.get('/', (req, res) => {
  res.json({ message: 'Hello World' })
})

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', promClient.register.contentType)
  res.end(await promClient.register.metrics())
})

app.listen(3000, () => {
  console.log('Server running on port 3000')
})
```

### Grafana Dashboards

**grafana/datasources/prometheus.yml:**
```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

**Dashboards populares:**
- Node Exporter Full: ID 1860
- Docker Container & Host: ID 179
- Cadvisor: ID 14282

**Importar dashboard:**
1. Ir a http://localhost:3000
2. Login (admin/admin)
3. Create → Import
4. Ingresar ID del dashboard

---

## ELK Stack

### Stack Completo

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Elasticsearch - Almacenamiento
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - elk

  # Logstash - Procesamiento
  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
    ports:
      - "5000:5000/tcp"
      - "5000:5000/udp"
      - "9600:9600"
    environment:
      LS_JAVA_OPTS: "-Xmx256m -Xms256m"
    depends_on:
      - elasticsearch
    networks:
      - elk

  # Kibana - Visualización
  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    container_name: kibana
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_URL: http://elasticsearch:9200
      ELASTICSEARCH_HOSTS: '["http://elasticsearch:9200"]'
    depends_on:
      - elasticsearch
    networks:
      - elk

  # Filebeat - Recolector de logs
  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    container_name: filebeat
    user: root
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command: filebeat -e -strict.perms=false
    depends_on:
      - elasticsearch
      - logstash
    networks:
      - elk

volumes:
  elasticsearch_data:

networks:
  elk:
    driver: bridge
```

**logstash/pipeline/logstash.conf:**
```conf
input {
  beats {
    port => 5000
  }

  tcp {
    port => 5000
    codec => json
  }
}

filter {
  # Parsear JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
    }
  }

  # Agregar timestamp
  date {
    match => ["timestamp", "ISO8601"]
  }

  # Parsear logs de aplicación
  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }

  # Debug
  stdout {
    codec => rubydebug
  }
}
```

**filebeat.yml:**
```yaml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    processors:
      - add_docker_metadata:
          host: "unix:///var/run/docker.sock"

output.logstash:
  hosts: ["logstash:5000"]
```

### Logging desde Aplicación

**Python:**
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName
        }
        return json.dumps(log_data)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Uso
logger.info("User login", extra={'user_id': 123})
logger.error("Database error", extra={'error': str(e)})
```

**Node.js (Winston):**
```javascript
const winston = require('winston')

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log' })
  ]
})

// Uso
logger.info('User login', { userId: 123 })
logger.error('Database error', { error: err.message })
```

---

## Loki + Grafana

Alternativa más ligera que ELK.

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  loki:
    image: grafana/loki:latest
    container_name: loki
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    networks:
      - monitoring

  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    volumes:
      - /var/log:/var/log
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - monitoring

networks:
  monitoring:
```

**promtail-config.yml:**
```yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: containers
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
```

---

## Jaeger (Distributed Tracing)

```yaml
version: '3.8'

services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"  # UI
      - "14268:14268"
      - "9411:9411"
    environment:
      - COLLECTOR_ZIPKIN_HTTP_PORT=9411
```

**Instrumentar con OpenTelemetry (Python):**
```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup
resource = Resource(attributes={SERVICE_NAME: "my-service"})
provider = TracerProvider(resource=resource)
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Uso
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    with tracer.start_as_current_span("get_user"):
        # Tu código aquí
        user = await db.get_user(user_id)
        return user
```

---

## Stack Completo de Observabilidad

**docker-compose.full.yml:**
```yaml
version: '3.8'

services:
  # Métricas
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  # Logs
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./promtail-config.yml:/etc/promtail/config.yml

  # Traces
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"

  # Visualización
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning

  # Aplicación
  app:
    build: ./app
    ports:
      - "8000:8000"
    environment:
      - JAEGER_AGENT_HOST=jaeger
      - JAEGER_AGENT_PORT=6831
```

---

## Mejores Prácticas

1. **Logging estructurado** - Usar JSON
2. **Niveles de log apropiados** - DEBUG, INFO, WARNING, ERROR
3. **Contexto en logs** - request_id, user_id, etc.
4. **Métricas relevantes** - Latencia, errores, throughput
5. **Dashboards por servicio** - No sobrecargar un dashboard
6. **Alertas inteligentes** - Evitar falsos positivos
7. **Retención de datos** - Balance entre costo y necesidad
8. **Sampling de traces** - No todos los requests

---

## Checklist

- [ ] Prometheus + Grafana configurado
- [ ] Métricas expuestas en /metrics
- [ ] Logs centralizados (ELK o Loki)
- [ ] Dashboards creados
- [ ] Alertas configuradas
- [ ] Distributed tracing (opcional)
- [ ] Rotación de logs configurada
- [ ] Backup de configuraciones

---

¡La observabilidad es clave para mantener sistemas en producción!
