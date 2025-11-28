# Módulo: Arquitecturas Avanzadas - Service Mesh, Serverless y Multi-Region

## Objetivo
Dominar arquitecturas distribuidas avanzadas incluyendo Service Mesh (Istio, Linkerd), Serverless Computing (AWS Lambda, Azure Functions) y despliegues Multi-Region con CDN.

---

# PARTE 1: SERVICE MESH

## ¿Qué es un Service Mesh?

Un **Service Mesh** es una capa de infraestructura dedicada para gestionar la comunicación entre microservicios.

### Beneficios
- ✅ **Traffic Management**: Load balancing, circuit breaking, retries
- ✅ **Security**: mTLS automático entre servicios
- ✅ **Observability**: Métricas, logs y tracing distribuido
- ✅ **Resiliency**: Fault injection, timeouts, retries
- ✅ **A/B Testing**: Canary deployments, traffic splitting

### Herramientas Principales
- **Istio** - Más completo, mayor adopción
- **Linkerd** - Ligero y simple
- **Consul Connect** - HashiCorp
- **AWS App Mesh** - Nativo de AWS

---

## Istio - Getting Started

### Instalación en Kubernetes

```bash
# Descargar Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Instalar Istio en K8s
istioctl install --set profile=demo -y

# Habilitar inyección automática de sidecars
kubectl label namespace default istio-injection=enabled

# Verificar
kubectl get pods -n istio-system
```

### Arquitectura Istio

```
┌──────────────────────────────────────┐
│       Control Plane (istiod)         │
│  - Pilot (configuración)             │
│  - Citadel (certificados)            │
│  - Galley (validación)               │
└──────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│          Data Plane                  │
│  ┌─────────┐  ┌─────────┐            │
│  │ Service │  │ Service │            │
│  │    A    │  │    B    │            │
│  └─────────┘  └─────────┘            │
│  │ Envoy │    │ Envoy │              │
│  │ Proxy │◄───┤ Proxy │              │
│  └───────┘    └───────┘              │
└──────────────────────────────────────┘
```

### Desplegar Aplicación con Istio

#### app-deployment.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  ports:
  - port: 80
    name: http
  selector:
    app: myapp
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: v1
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
      - name: myapp
        image: tu-usuario/myapp:v1
        ports:
        - containerPort: 3000
```

#### Aplicar
```bash
kubectl apply -f app-deployment.yaml
```

### Virtual Service (Traffic Management)

#### virtualservice.yaml
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        user-type:
          exact: premium
    route:
    - destination:
        host: myapp
        subset: v2
      weight: 100
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10  # 10% a versión 2 (canary)
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 2
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### Gateway (Ingress)

#### gateway.yaml
```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: myapp-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "myapp.example.com"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-external
spec:
  hosts:
  - "myapp.example.com"
  gateways:
  - myapp-gateway
  http:
  - route:
    - destination:
        host: myapp
        port:
          number: 80
```

### Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp-cb
spec:
  host: myapp
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

### Mutual TLS (mTLS)

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT  # Forzar mTLS
```

### Observability con Istio

```bash
# Instalar addons
kubectl apply -f samples/addons/prometheus.yaml
kubectl apply -f samples/addons/grafana.yaml
kubectl apply -f samples/addons/jaeger.yaml
kubectl apply -f samples/addons/kiali.yaml

# Acceder a Kiali (service mesh dashboard)
istioctl dashboard kiali

# Grafana
istioctl dashboard grafana

# Jaeger (tracing)
istioctl dashboard jaeger
```

---

## Linkerd - Alternativa Ligera

### Instalación

```bash
# Instalar CLI
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin

# Validar cluster
linkerd check --pre

# Instalar Linkerd
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -

# Verificar
linkerd check

# Instalar Viz (observability)
linkerd viz install | kubectl apply -f -
```

### Inyectar Linkerd en Deployment

```bash
# Método 1: Inyectar manualmente
kubectl get deploy myapp -o yaml | linkerd inject - | kubectl apply -f -

# Método 2: Anotar namespace
kubectl annotate namespace default linkerd.io/inject=enabled

# Dashboard
linkerd viz dashboard
```

---

# PARTE 2: SERVERLESS COMPUTING

## AWS Lambda con Docker

### Función Lambda

#### app/index.js
```javascript
exports.handler = async (event) => {
    console.log('Event:', JSON.stringify(event, null, 2));

    const response = {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: 'Hello from Lambda!',
            input: event,
            timestamp: new Date().toISOString()
        }),
    };

    return response;
};
```

### Dockerfile para Lambda

```dockerfile
FROM public.ecr.aws/lambda/nodejs:18

# Copy function code
COPY app/index.js ${LAMBDA_TASK_ROOT}/

# Set handler
CMD [ "index.handler" ]
```

### Desplegar con AWS SAM

#### template.yaml
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      PackageType: Image
      ImageUri: !Sub ${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/my-lambda:latest
      MemorySize: 512
      Timeout: 30
      Environment:
        Variables:
          NODE_ENV: production
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /hello
            Method: get

Outputs:
  ApiUrl:
    Description: "API Gateway URL"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello"
```

### Comandos

```bash
# Build
sam build

# Deploy
sam deploy --guided

# Test local
sam local invoke MyFunction -e events/event.json

# API local
sam local start-api
```

### Lambda con API Gateway + DynamoDB

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  UsersTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: Users
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: userId
          AttributeType: S
      KeySchema:
        - AttributeName: userId
          KeyType: HASH

  CreateUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: users.create
      Runtime: nodejs18.x
      Environment:
        Variables:
          TABLE_NAME: !Ref UsersTable
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref UsersTable
      Events:
        CreateUser:
          Type: Api
          Properties:
            Path: /users
            Method: post
```

---

## Azure Functions con Docker

### Dockerfile (Azure Functions)

```dockerfile
FROM mcr.microsoft.com/azure-functions/node:4

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY . /home/site/wwwroot

RUN cd /home/site/wwwroot && npm install
```

### function.json
```json
{
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
```

### index.js (Azure Function)
```javascript
module.exports = async function (context, req) {
    context.log('HTTP trigger function processed a request.');

    const name = req.query.name || req.body?.name || 'World';

    context.res = {
        status: 200,
        body: `Hello, ${name}!`,
        headers: {
            'Content-Type': 'application/json'
        }
    };
};
```

### Desplegar

```bash
# Login
az login

# Create resource group
az group create --name myapp-rg --location eastus

# Create storage account
az storage account create \
  --name myappstore \
  --resource-group myapp-rg \
  --location eastus \
  --sku Standard_LRS

# Create Function App
az functionapp create \
  --resource-group myapp-rg \
  --name myapp-functions \
  --storage-account myappstore \
  --functions-version 4 \
  --runtime node \
  --runtime-version 18 \
  --os-type Linux

# Deploy
func azure functionapp publish myapp-functions
```

---

# PARTE 3: CDN Y MULTI-REGION

## AWS CloudFront + S3

### Arquitectura Multi-Region

```
┌────────────────────────────────────┐
│         CloudFront (Global)        │
│  - Edge Locations worldwide        │
│  - SSL/TLS termination             │
│  - DDoS protection                 │
└────────┬───────────────────────────┘
         │
    ┌────┴────┬──────────────┐
    ▼         ▼              ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ S3      │ │ ALB     │ │ API GW  │
│ Origin  │ │ us-east │ │ Global  │
└─────────┘ └─────────┘ └─────────┘
```

### CloudFront con Terraform

```hcl
# S3 bucket para contenido estático
resource "aws_s3_bucket" "cdn_origin" {
  bucket = "my-app-cdn-origin"
}

resource "aws_s3_bucket_public_access_block" "cdn_origin" {
  bucket = aws_s3_bucket.cdn_origin.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Origin Access Control
resource "aws_cloudfront_origin_access_control" "cdn" {
  name                              = "my-app-oac"
  description                       = "OAC for S3"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# CloudFront Distribution
resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "My App CDN"
  default_root_object = "index.html"
  price_class         = "PriceClass_All"

  origin {
    domain_name              = aws_s3_bucket.cdn_origin.bucket_regional_domain_name
    origin_id                = "S3-${aws_s3_bucket.cdn_origin.id}"
    origin_access_control_id = aws_cloudfront_origin_access_control.cdn.id
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-${aws_s3_bucket.cdn_origin.id}"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

output "cloudfront_domain" {
  value = aws_cloudfront_distribution.cdn.domain_name
}
```

---

## Azure CDN + Front Door

### Azure Front Door (Global Load Balancer + CDN)

```hcl
resource "azurerm_frontdoor" "main" {
  name                = "my-app-frontdoor"
  resource_group_name = azurerm_resource_group.main.name

  routing_rule {
    name               = "default-routing"
    accepted_protocols = ["Https"]
    patterns_to_match  = ["/*"]
    frontend_endpoints = ["main-frontend"]
    forwarding_configuration {
      forwarding_protocol = "MatchRequest"
      backend_pool_name   = "main-backend-pool"
    }
  }

  backend_pool_load_balancing {
    name = "load-balancing-settings"
  }

  backend_pool_health_probe {
    name                = "health-probe"
    protocol            = "Https"
    interval_in_seconds = 120
  }

  backend_pool {
    name = "main-backend-pool"
    backend {
      host_header = "app-eastus.azurewebsites.net"
      address     = "app-eastus.azurewebsites.net"
      http_port   = 80
      https_port  = 443
      priority    = 1
      weight      = 50
    }
    backend {
      host_header = "app-westus.azurewebsites.net"
      address     = "app-westus.azurewebsites.net"
      http_port   = 80
      https_port  = 443
      priority    = 1
      weight      = 50
    }

    load_balancing_name = "load-balancing-settings"
    health_probe_name   = "health-probe"
  }

  frontend_endpoint {
    name      = "main-frontend"
    host_name = "my-app-frontdoor.azurefd.net"
  }
}
```

---

## Multi-Region con Route 53 (AWS)

### Latency-Based Routing

```hcl
# Application Load Balancer - US East
resource "aws_lb" "us_east" {
  provider = aws.us_east_1
  name     = "app-alb-us-east"
  # ... configuración
}

# Application Load Balancer - EU West
resource "aws_lb" "eu_west" {
  provider = aws.eu_west_1
  name     = "app-alb-eu-west"
  # ... configuración
}

# Route 53 - Latency-based routing
resource "aws_route53_record" "app_us_east" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "us-east-1"

  latency_routing_policy {
    region = "us-east-1"
  }

  alias {
    name                   = aws_lb.us_east.dns_name
    zone_id                = aws_lb.us_east.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "app_eu_west" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "eu-west-1"

  latency_routing_policy {
    region = "eu-west-1"
  }

  alias {
    name                   = aws_lb.eu_west.dns_name
    zone_id                = aws_lb.eu_west.zone_id
    evaluate_target_health = true
  }
}
```

### Failover Routing (Alta Disponibilidad)

```hcl
resource "aws_route53_record" "primary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  alias {
    name                   = aws_lb.primary.dns_name
    zone_id                = aws_lb.primary.zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "secondary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "app.example.com"
  type           = "A"
  set_identifier = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  alias {
    name                   = aws_lb.secondary.dns_name
    zone_id                = aws_lb.secondary.zone_id
    evaluate_target_health = true
  }
}
```

---

## Replicación Multi-Region

### PostgreSQL Replication (AWS RDS)

```hcl
# Primary database in us-east-1
resource "aws_db_instance" "primary" {
  provider             = aws.us_east_1
  identifier           = "myapp-db-primary"
  engine               = "postgres"
  engine_version       = "14"
  instance_class       = "db.t3.medium"
  allocated_storage    = 100
  storage_encrypted    = true
  multi_az             = true
  backup_retention_period = 7
}

# Read replica in eu-west-1
resource "aws_db_instance" "replica_eu" {
  provider             = aws.eu_west_1
  identifier           = "myapp-db-replica-eu"
  replicate_source_db  = aws_db_instance.primary.arn
  instance_class       = "db.t3.medium"
  storage_encrypted    = true
  publicly_accessible  = false
}
```

### S3 Cross-Region Replication

```hcl
resource "aws_s3_bucket_replication_configuration" "replication" {
  bucket = aws_s3_bucket.source.id
  role   = aws_iam_role.replication.arn

  rule {
    id     = "replicate-all"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.destination.arn
      storage_class = "STANDARD"

      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }

      metrics {
        status = "Enabled"
        event_threshold {
          minutes = 15
        }
      }
    }
  }
}
```

---

## Docker Swarm Multi-Region (Alternativa Simple)

### docker-compose.yml con deploy constraints
```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    deploy:
      replicas: 6
      placement:
        constraints:
          - node.labels.region == us-east || node.labels.region == eu-west
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure
    networks:
      - overlay-net

networks:
  overlay-net:
    driver: overlay
    attachable: true
```

---

## Monitoreo Multi-Region

### Prometheus Federation

```yaml
# Prometheus en región primaria
global:
  external_labels:
    region: 'us-east-1'

scrape_configs:
  # Federate from other regions
  - job_name: 'federate-eu-west'
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{job=~".+"}'
    static_configs:
      - targets:
          - 'prometheus-eu-west.example.com:9090'
```

---

## Resumen de Comandos

### Istio
```bash
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
istioctl dashboard kiali
```

### Linkerd
```bash
linkerd install --crds | kubectl apply -f -
linkerd check
linkerd viz dashboard
```

### AWS Lambda
```bash
sam build
sam deploy --guided
sam local invoke
```

### CloudFront
```bash
aws cloudfront create-invalidation --distribution-id E123 --paths "/*"
```

---

## Checklist

- [ ] Instalar Service Mesh (Istio o Linkerd)
- [ ] Configurar mTLS entre servicios
- [ ] Implementar Circuit Breakers
- [ ] Desplegar función Serverless
- [ ] Configurar CDN (CloudFront/Azure CDN)
- [ ] Implementar Multi-Region deployment
- [ ] Configurar DNS con failover
- [ ] Replicación de datos cross-region
- [ ] Monitoreo multi-region
- [ ] Disaster recovery plan

---

¡Arquitecturas distribuidas a escala global! 🌍
