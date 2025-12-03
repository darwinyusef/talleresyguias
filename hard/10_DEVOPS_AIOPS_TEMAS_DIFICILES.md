# Conocimientos Técnicos Difíciles: DevOps, DevSecOps, AIOps & GenAIOps

## Objetivo
Temas complejos de operaciones, seguridad, automatización con IA y MLOps que un arquitecto debe dominar.

---

## CATEGORÍA 1: GitOps & Infrastructure as Code

### 1.1 ArgoCD con App of Apps Pattern
**Dificultad:** ⭐⭐⭐⭐⭐

```yaml
# apps/root-app.yaml - App of Apps pattern
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops
    targetRevision: main
    path: apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true

# apps/backend-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: backend
  namespace: argocd
spec:
  project: production
  source:
    repoURL: https://github.com/org/backend
    targetRevision: main
    path: k8s/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: backend-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - RespectIgnoreDifferences=true

# Kustomize overlay structure
# k8s/
#   base/
#     deployment.yaml
#     service.yaml
#   overlays/
#     dev/
#       kustomization.yaml
#     prod/
#       kustomization.yaml
```

### 1.2 Terraform Advanced Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

```hcl
# Remote state with locking
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/infrastructure.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# Workspaces para multi-env
resource "aws_instance" "app" {
  count         = terraform.workspace == "prod" ? 5 : 2
  instance_type = terraform.workspace == "prod" ? "t3.large" : "t3.micro"
}

# Modules con composition
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = var.vpc_cidr
  azs        = var.availability_zones
  
  tags = merge(
    var.common_tags,
    {
      Environment = terraform.workspace
    }
  )
}

# Dynamic blocks
resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = module.vpc.id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}

# Terraform test
# tests/vpc_test.tftest.hcl
run "validate_vpc_cidr" {
  assert {
    condition     = module.vpc.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR must be 10.0.0.0/16"
  }
}
```

---

## CATEGORÍA 2: Container Security

### 2.1 Trivy Security Scanning
**Dificultad:** ⭐⭐⭐⭐

```bash
# Scan image for vulnerabilities
trivy image --severity HIGH,CRITICAL nginx:latest

# CI/CD integration
trivy image --exit-code 1 --severity CRITICAL myapp:latest

# IaC scanning
trivy config ./terraform/

# SBOM generation
trivy image --format cyclonedx myapp:latest > sbom.json
```

### 2.2 Falco Runtime Security
**Dificultad:** ⭐⭐⭐⭐⭐

```yaml
# Custom Falco rules
- rule: Unauthorized Process in Container
  desc: Detect unauthorized process execution
  condition: >
    spawned_process and
    container and
    not proc.name in (allowed_processes)
  output: >
    Unauthorized process started
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: WARNING

- rule: Sensitive File Access
  desc: Detect access to sensitive files
  condition: >
    open_read and
    fd.name in (/etc/shadow, /etc/passwd) and
    not proc.name in (allowed_readers)
  output: >
    Sensitive file accessed
    (file=%fd.name process=%proc.name)
  priority: CRITICAL
```

---

## CATEGORÍA 3: Observability

### 3.1 OpenTelemetry Auto-instrumentation
**Dificultad:** ⭐⭐⭐⭐⭐

```yaml
# Kubernetes auto-instrumentation
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: otel-instrumentation
spec:
  exporter:
    endpoint: http://otel-collector:4317
  propagators:
    - tracecontext
    - baggage
  sampler:
    type: parentbased_traceidratio
    argument: "0.1"  # 10% sampling
  python:
    env:
      - name: OTEL_EXPORTER_OTLP_ENDPOINT
        value: http://otel-collector:4317
  nodejs:
    env:
      - name: NODE_OPTIONS
        value: "--require @opentelemetry/auto-instrumentations-node/register"
```

### 3.2 PromQL Queries Avanzadas
**Dificultad:** ⭐⭐⭐⭐⭐

```promql
# SLI: Request success rate (99.9% target)
sum(rate(http_requests_total{status!~"5.."}[5m])) /
sum(rate(http_requests_total[5m]))

# Error budget burn rate
(1 - (
  sum(rate(http_requests_total{status!~"5.."}[1h])) /
  sum(rate(http_requests_total[1h]))
)) / (1 - 0.999) > 1  # Burning faster than budget

# P99 latency by endpoint
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m]))
  by (le, endpoint)
)

# Multi-window multi-burn rate alert
(
  (sum(rate(http_requests_total{status=~"5.."}[1m])) /
   sum(rate(http_requests_total[1m]))) > 0.14
  and
  (sum(rate(http_requests_total{status=~"5.."}[5m])) /
   sum(rate(http_requests_total[5m]))) > 0.14
)
or
(
  (sum(rate(http_requests_total{status=~"5.."}[1h])) /
   sum(rate(http_requests_total[1h]))) > 0.01
  and
  (sum(rate(http_requests_total{status=~"5.."}[6h])) /
   sum(rate(http_requests_total[6h]))) > 0.01
)
```

---

## CATEGORÍA 4: AIOps - AI-Powered Operations

### 4.1 Anomaly Detection with Prophet
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from prophet import Prophet
import pandas as pd

# Load metrics from Prometheus
def fetch_metrics(query, start, end):
    response = prometheus.query_range(
        query=query,
        start=start,
        end=end,
        step='1m'
    )
    return pd.DataFrame(response)

# Train Prophet model
df = fetch_metrics(
    'rate(http_requests_total[5m])',
    start='2024-01-01',
    end='2024-12-01'
)

df.columns = ['ds', 'y']  # Prophet format
df['ds'] = pd.to_datetime(df['ds'])

model = Prophet(
    interval_width=0.95,
    changepoint_prior_scale=0.05
)
model.fit(df)

# Predict and detect anomalies
future = model.make_future_dataframe(periods=60, freq='min')
forecast = model.predict(future)

# Detect anomalies
anomalies = df[
    (df['y'] > forecast['yhat_upper']) |
    (df['y'] < forecast['yhat_lower'])
]

if len(anomalies) > 0:
    send_alert(f"Anomaly detected: {anomalies}")
```

### 4.2 Root Cause Analysis con ML
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Feature engineering de métricas
def extract_features(timestamp, window='5m'):
    features = {
        'cpu_usage': get_metric('cpu_usage', timestamp, window),
        'memory_usage': get_metric('memory_usage', timestamp, window),
        'error_rate': get_metric('error_rate', timestamp, window),
        'latency_p99': get_metric('latency_p99', timestamp, window),
        'db_connections': get_metric('db_connections', timestamp, window),
        'queue_depth': get_metric('queue_depth', timestamp, window),
    }
    return features

# Training data: incidents históricos
incidents = load_historical_incidents()
X_train = []
y_train = []

for incident in incidents:
    features = extract_features(incident.timestamp)
    X_train.append(list(features.values()))
    y_train.append(incident.root_cause)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Predict root cause en tiempo real
def diagnose_incident(current_timestamp):
    features = extract_features(current_timestamp)
    X = [list(features.values())]

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]

    feature_importance = dict(zip(
        features.keys(),
        model.feature_importances_
    ))

    return {
        'predicted_root_cause': prediction,
        'confidence': max(probability),
        'contributing_factors': sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
    }
```

---

## CATEGORÍA 5: GenAIOps - LLM-Powered Operations

### 5.1 AI-Assisted Incident Response
**Dificultad:** ⭐⭐⭐⭐⭐

```python
from anthropic import Anthropic

client = Anthropic()

def ai_incident_analysis(incident_data):
    """Analizar incidente con Claude"""

    # Recopilar contexto
    context = f"""
Incident Details:
- Severity: {incident_data['severity']}
- Service: {incident_data['service']}
- Error Rate: {incident_data['error_rate']}
- Latency P99: {incident_data['latency_p99']}ms

Recent Logs:
{get_recent_logs(incident_data['service'], limit=100)}

Recent Deployments:
{get_recent_deployments(incident_data['service'])}

Similar Past Incidents:
{get_similar_incidents(incident_data)}
"""

    # Analizar con Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""You are an expert SRE. Analyze this production incident:

{context}

Provide:
1. **Root Cause Analysis**: Most likely cause
2. **Immediate Actions**: Steps to mitigate now
3. **Verification Steps**: How to confirm resolution
4. **Prevention**: How to prevent recurrence
5. **Runbook Query**: Suggest relevant runbook searches

Format as structured JSON."""
        }]
    )

    analysis = json.loads(response.content[0].text)

    # Auto-execute safe remediation steps
    if analysis.get('auto_remediation_safe'):
        execute_remediation(analysis['immediate_actions'])

    return analysis

### 5.2 Automated Runbook Generation
**Dificultad:** ⭐⭐⭐⭐⭐

```python
def generate_runbook_from_incidents(service_name):
    """Generate runbook from historical incidents"""

    # Get past incidents
    incidents = load_incidents_for_service(service_name, days=90)

    # Cluster similar incidents
    clustered = cluster_incidents(incidents)

    runbooks = []

    for cluster in clustered:
        # Generate runbook with Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"""Generate a detailed runbook for this incident pattern:

Service: {service_name}
Incident Pattern: {cluster['pattern_description']}
Frequency: {cluster['count']} incidents in 90 days
Resolution Time: Avg {cluster['avg_resolution_time']}

Past Resolutions:
{format_resolutions(cluster['incidents'])}

Generate a runbook with:
1. **Detection**: How to identify this issue
2. **Diagnosis**: Steps to confirm root cause
3. **Resolution**: Exact commands/steps
4. **Verification**: How to verify fix
5. **Escalation**: When to escalate

Use markdown format with code blocks."""
            }]
        )

        runbook = {
            'title': cluster['pattern_description'],
            'content': response.content[0].text,
            'frequency': cluster['count'],
            'severity': cluster['avg_severity']
        }

        runbooks.append(runbook)

        # Save to wiki/knowledge base
        save_runbook(service_name, runbook)

    return runbooks
```

### 5.3 Intelligent Alert Correlation
**Dificultad:** ⭐⭐⭐⭐⭐

```python
def correlate_alerts_with_llm(alerts):
    """Use LLM to correlate and prioritize alerts"""

    # Prepare alert context
    alert_context = "\n\n".join([
        f"""Alert {i+1}:
- Name: {alert['name']}
- Severity: {alert['severity']}
- Service: {alert['service']}
- Message: {alert['message']}
- Metrics: {alert['metrics']}
- Time: {alert['timestamp']}"""
        for i, alert in enumerate(alerts)
    ])

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""You are an expert SRE analyzing multiple alerts:

{alert_context}

Analyze these alerts and provide:
1. **Correlation**: Which alerts are related to the same root cause?
2. **Primary Alert**: Which is the root cause vs symptom?
3. **Priority**: Rank alerts by urgency
4. **Recommended Action**: What should be investigated first?
5. **Suppression**: Which alerts can be suppressed as duplicates?

Return as JSON."""
        }]
    )

    correlation = json.loads(response.content[0].text)

    # Auto-suppress duplicate/symptom alerts
    for alert_id in correlation['suppression_list']:
        suppress_alert(alert_id, reason=correlation['suppression_reason'])

    # Create incident from primary alert
    if correlation['create_incident']:
        create_incident(
            primary_alert=correlation['primary_alert'],
            related_alerts=correlation['related_alerts'],
            analysis=correlation
        )

    return correlation
```

---

## Resumen Prioridades DevOps/AIOps

| Tema | Dificultad | Impacto | Futuro | Prioridad |
|------|------------|---------|--------|-----------|
| GitOps (ArgoCD) | 5 | 5 | 5 | **CRÍTICA** |
| IaC (Terraform) | 5 | 5 | 5 | **CRÍTICA** |
| Container Security | 5 | 5 | 5 | **CRÍTICA** |
| Observability (OTel) | 5 | 5 | 5 | **CRÍTICA** |
| AIOps (Anomaly Detection) | 5 | 4 | 5 | **ALTA** |
| GenAIOps (LLM Ops) | 5 | 4 | 5 | **ALTA** |

**Total:** 15+ temas de operaciones avanzadas
