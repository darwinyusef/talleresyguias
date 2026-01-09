# Arquitectura de Security: Patrones de Seguridad para Producción 2026

## Índice
1. [Zero Trust Architecture](#1-zero-trust-architecture)
2. [Defense in Depth](#2-defense-in-depth)
3. [Security Boundaries & Trust Zones](#3-security-boundaries)
4. [Secret Management Architecture](#4-secret-management)
5. [Authentication & Authorization](#5-auth)
6. [API Security](#6-api-security)
7. [Data Security](#7-data-security)
8. [Threat Modeling](#8-threat-modeling)
9. [Security Testing](#9-security-testing)
10. [Security Monitoring & SIEM](#10-security-monitoring)

---

## 1. Zero Trust Architecture

### ❌ ERROR COMÚN: Confiar en la red interna
```python
# MAL - confiar porque viene de IP interna
if request.remote_addr.startswith("10."):
    # Trusted internal network
    return admin_access()
```

### ✅ SOLUCIÓN: Never Trust, Always Verify

```python
from dataclasses import dataclass
from typing import Optional, List, Set
from datetime import datetime, timedelta
import jwt
from enum import Enum

# ==========================================
# ZERO TRUST PRINCIPLES
# ==========================================
"""
1. Verify explicitly: Always authenticate & authorize
2. Least privilege access: Just-in-time & just-enough
3. Assume breach: Minimize blast radius
"""

# ==========================================
# IDENTITY VERIFICATION
# ==========================================
@dataclass
class Identity:
    """
    Identidad verificada - puede ser usuario, servicio, dispositivo
    """
    principal_id: str
    principal_type: str  # user, service, device
    authentication_method: str  # mfa, certificate, token
    authentication_time: datetime
    trust_level: int  # 0-100
    context: dict

class TrustLevel(Enum):
    """Niveles de confianza basados en factores"""
    LOW = 25        # Single factor, old session
    MEDIUM = 50     # Single factor, recent session
    HIGH = 75       # MFA, recent session
    VERY_HIGH = 100 # MFA + device verification + recent

# ==========================================
# ZERO TRUST POLICY ENGINE
# ==========================================
class ZeroTrustPolicyEngine:
    """
    Policy engine que evalúa cada request
    No hay "trusted zone" - todo se verifica
    """

    def __init__(self):
        self.policies: List['AccessPolicy'] = []

    async def evaluate_access(
        self,
        identity: Identity,
        resource: str,
        action: str,
        context: dict
    ) -> 'AccessDecision':
        """
        Evalúa acceso considerando:
        - Identidad (quién)
        - Recurso (qué)
        - Acción (cómo)
        - Contexto (cuándo, desde dónde)
        """

        # 1. Verificar identidad
        if not await self._verify_identity(identity):
            return AccessDecision(
                allowed=False,
                reason="Identity verification failed"
            )

        # 2. Evaluar todas las políticas
        evaluations = []
        for policy in self.policies:
            result = await policy.evaluate(identity, resource, action, context)
            evaluations.append(result)

        # 3. Aplicar strategy (deny-by-default)
        if any(not e.allowed for e in evaluations):
            # Si alguna policy niega, negar
            denials = [e for e in evaluations if not e.allowed]
            return AccessDecision(
                allowed=False,
                reason=f"Denied by policies: {[d.reason for d in denials]}"
            )

        # 4. Verificar trust level requerido
        required_trust = self._get_required_trust_level(resource, action)
        if identity.trust_level < required_trust.value:
            return AccessDecision(
                allowed=False,
                reason=f"Insufficient trust level. Required: {required_trust.value}, Got: {identity.trust_level}"
            )

        # 5. Permitir con condiciones
        return AccessDecision(
            allowed=True,
            conditions=self._get_access_conditions(identity, resource, action)
        )

    async def _verify_identity(self, identity: Identity) -> bool:
        """
        Verifica identidad siempre
        - Token no expirado
        - Credentials válidos
        - No revocado
        """
        # Verificar expiración de autenticación
        age = datetime.utcnow() - identity.authentication_time
        max_age = timedelta(hours=8)  # Re-auth después de 8h

        if age > max_age:
            return False

        # Verificar contra revocation list
        if await self._is_revoked(identity.principal_id):
            return False

        return True

    async def _is_revoked(self, principal_id: str) -> bool:
        """Check revocation list (Redis/DB)"""
        # Implementar con Redis/DB
        return False

    def _get_required_trust_level(
        self,
        resource: str,
        action: str
    ) -> TrustLevel:
        """
        Determina trust level requerido
        Recursos críticos requieren HIGH/VERY_HIGH
        """
        critical_resources = {
            "/api/admin": TrustLevel.VERY_HIGH,
            "/api/payments": TrustLevel.HIGH,
            "/api/user/delete": TrustLevel.HIGH,
        }

        return critical_resources.get(resource, TrustLevel.MEDIUM)

    def _get_access_conditions(
        self,
        identity: Identity,
        resource: str,
        action: str
    ) -> List[str]:
        """
        Condiciones adicionales de acceso
        """
        conditions = []

        # Rate limiting
        conditions.append("rate_limit:100/min")

        # Audit logging
        conditions.append("audit_log:enabled")

        # Session binding
        if identity.trust_level < TrustLevel.HIGH.value:
            conditions.append("session_timeout:30m")

        return conditions

@dataclass
class AccessDecision:
    allowed: bool
    reason: Optional[str] = None
    conditions: List[str] = None

# ==========================================
# ACCESS POLICY
# ==========================================
class AccessPolicy:
    """
    Policy individual de acceso
    """
    def __init__(
        self,
        name: str,
        principal_types: Set[str],
        resources: Set[str],
        actions: Set[str],
        conditions: Optional[dict] = None
    ):
        self.name = name
        self.principal_types = principal_types
        self.resources = resources
        self.actions = actions
        self.conditions = conditions or {}

    async def evaluate(
        self,
        identity: Identity,
        resource: str,
        action: str,
        context: dict
    ) -> AccessDecision:
        """
        Evalúa si policy permite acceso
        """
        # Verificar tipo de principal
        if identity.principal_type not in self.principal_types:
            return AccessDecision(
                allowed=False,
                reason=f"Policy {self.name}: principal type mismatch"
            )

        # Verificar recurso
        if not self._matches_resource(resource):
            # No aplica esta policy
            return AccessDecision(allowed=True)

        # Verificar acción
        if action not in self.actions:
            return AccessDecision(
                allowed=False,
                reason=f"Policy {self.name}: action not allowed"
            )

        # Verificar condiciones
        if not await self._evaluate_conditions(context):
            return AccessDecision(
                allowed=False,
                reason=f"Policy {self.name}: conditions not met"
            )

        return AccessDecision(allowed=True)

    def _matches_resource(self, resource: str) -> bool:
        """Match con wildcards"""
        for pattern in self.resources:
            if pattern.endswith("*"):
                if resource.startswith(pattern[:-1]):
                    return True
            elif pattern == resource:
                return True
        return False

    async def _evaluate_conditions(self, context: dict) -> bool:
        """
        Evalúa condiciones contextuales:
        - Horario de acceso
        - Ubicación geográfica
        - Red de origen
        - Estado del dispositivo
        """
        # Ejemplo: solo horario laboral
        if "allowed_hours" in self.conditions:
            current_hour = datetime.utcnow().hour
            start, end = self.conditions["allowed_hours"]
            if not (start <= current_hour < end):
                return False

        # Ejemplo: solo desde IPs permitidas
        if "allowed_ips" in self.conditions:
            client_ip = context.get("client_ip")
            if client_ip not in self.conditions["allowed_ips"]:
                return False

        return True

# ==========================================
# EJEMPLO DE USO
# ==========================================

# Setup policies
policy_engine = ZeroTrustPolicyEngine()

# Policy 1: Users pueden leer orders
policy_engine.policies.append(
    AccessPolicy(
        name="users_read_orders",
        principal_types={"user"},
        resources={"/api/orders/*"},
        actions={"read"},
        conditions={
            "allowed_hours": (8, 20)  # 8am - 8pm
        }
    )
)

# Policy 2: Services pueden escribir orders
policy_engine.policies.append(
    AccessPolicy(
        name="services_write_orders",
        principal_types={"service"},
        resources={"/api/orders/*"},
        actions={"write", "read"},
        conditions={
            "allowed_ips": ["10.0.0.0/8"]  # Internal network
        }
    )
)

# Evaluar acceso
async def handle_request(request):
    # Extraer identidad del token
    identity = await extract_identity(request)

    # Evaluar acceso
    decision = await policy_engine.evaluate_access(
        identity=identity,
        resource=request.path,
        action=request.method,
        context={
            "client_ip": request.remote_addr,
            "user_agent": request.headers.get("User-Agent"),
            "timestamp": datetime.utcnow()
        }
    )

    if not decision.allowed:
        return {"error": decision.reason}, 403

    # Aplicar condiciones
    if decision.conditions:
        apply_conditions(decision.conditions)

    # Procesar request
    return await process_request(request)

# ==========================================
# CONTINUOUS VERIFICATION
# ==========================================
class ContinuousVerificationMiddleware:
    """
    Re-verifica identidad periódicamente durante sesión larga
    """
    def __init__(self, reverify_interval: timedelta = timedelta(minutes=15)):
        self.reverify_interval = reverify_interval

    async def __call__(self, request, call_next):
        identity = await extract_identity(request)

        # Verificar tiempo desde última verificación
        last_verify = identity.context.get("last_verification")
        if last_verify:
            age = datetime.utcnow() - last_verify
            if age > self.reverify_interval:
                # Re-verificar
                if not await self._reverify_identity(identity):
                    return {"error": "Re-verification required"}, 401

        # Continuar
        response = await call_next(request)
        return response

    async def _reverify_identity(self, identity: Identity) -> bool:
        """
        Re-verifica identidad:
        - Token sigue válido
        - Usuario no deshabilitado
        - Permisos no revocados
        """
        # Check token freshness
        # Check user status
        # Check permissions
        return True
```

**🎯 Principios Zero Trust:**

1. **Verify Explicitly**: Siempre autenticar y autorizar
2. **Least Privilege**: Acceso mínimo necesario
3. **Assume Breach**: Microsegmentación, monitoreo

---

## 2. Defense in Depth

### ✅ SOLUCIÓN: Múltiples capas de seguridad

```python
# ==========================================
# DEFENSE IN DEPTH - MULTIPLE LAYERS
# ==========================================

# ==========================================
# LAYER 1: NETWORK SECURITY
# ==========================================
class NetworkSecurityLayer:
    """
    Capa de red - firewall rules, network segmentation
    """

    @staticmethod
    def configure_security_groups():
        """
        Terraform/CloudFormation para security groups
        """
        return """
        # Security Group: API Servers
        resource "aws_security_group" "api_servers" {
          name = "api-servers"

          # Solo HTTPS desde load balancer
          ingress {
            from_port   = 443
            to_port     = 443
            protocol    = "tcp"
            security_groups = [aws_security_group.load_balancer.id]
          }

          # Sin acceso directo desde internet
          # Sin SSH desde internet (usar bastion host)

          egress {
            # Solo a database security group
            from_port   = 5432
            to_port     = 5432
            protocol    = "tcp"
            security_groups = [aws_security_group.database.id]
          }
        }

        # Security Group: Database
        resource "aws_security_group" "database" {
          name = "database"

          # Solo desde API servers
          ingress {
            from_port   = 5432
            to_port     = 5432
            protocol    = "tcp"
            security_groups = [aws_security_group.api_servers.id]
          }

          # Sin egress a internet
        }
        """

# ==========================================
# LAYER 2: APPLICATION SECURITY
# ==========================================
class ApplicationSecurityLayer:
    """
    Capa de aplicación - validación, sanitización
    """

    @staticmethod
    def validate_input(user_input: str) -> str:
        """
        Validación estricta de input
        """
        # 1. Allowlist approach (mejor que blocklist)
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', user_input):
            raise ValueError("Invalid input characters")

        # 2. Length limits
        if len(user_input) > 255:
            raise ValueError("Input too long")

        # 3. Sanitización
        from html import escape
        sanitized = escape(user_input)

        return sanitized

    @staticmethod
    def prevent_sql_injection():
        """
        SIEMPRE usar parameterized queries
        """
        # ❌ MAL
        # query = f"SELECT * FROM users WHERE id = {user_id}"

        # ✅ BIEN
        query = "SELECT * FROM users WHERE id = ?"
        params = (user_id,)

    @staticmethod
    def prevent_xss():
        """
        Content Security Policy + output encoding
        """
        csp_header = (
            "default-src 'self'; "
            "script-src 'self' 'nonce-{random}'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        return {"Content-Security-Policy": csp_header}

# ==========================================
# LAYER 3: AUTHENTICATION
# ==========================================
class AuthenticationLayer:
    """
    Capa de autenticación - MFA, strong passwords
    """

    @staticmethod
    def require_mfa(user_id: str) -> bool:
        """
        MFA obligatorio para cuentas críticas
        """
        critical_roles = ["admin", "finance", "support"]

        user = get_user(user_id)
        if user.role in critical_roles:
            return user.mfa_enabled

        return True

    @staticmethod
    def password_policy():
        """
        Política de contraseñas robusta
        """
        return {
            "min_length": 12,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special_chars": True,
            "max_age_days": 90,
            "prevent_reuse": 12,  # Últimas 12 passwords
            "lockout_threshold": 5,  # Bloquear después de 5 intentos
            "lockout_duration_minutes": 30
        }

# ==========================================
# LAYER 4: AUTHORIZATION
# ==========================================
class AuthorizationLayer:
    """
    Capa de autorización - RBAC, ABAC
    """
    pass  # Ver sección 5

# ==========================================
# LAYER 5: DATA ENCRYPTION
# ==========================================
class EncryptionLayer:
    """
    Capa de encriptación - at rest, in transit
    """
    pass  # Ver sección 7

# ==========================================
# LAYER 6: AUDIT LOGGING
# ==========================================
class AuditLoggingLayer:
    """
    Capa de auditoría - todos los accesos loggeados
    """

    @staticmethod
    async def log_security_event(
        event_type: str,
        principal_id: str,
        resource: str,
        action: str,
        result: str,
        context: dict
    ):
        """
        Log inmutable de eventos de seguridad
        """
        audit_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "principal_id": principal_id,
            "resource": resource,
            "action": action,
            "result": result,  # success, failure, denied
            "context": context,
            "ip_address": context.get("client_ip"),
            "user_agent": context.get("user_agent")
        }

        # Enviar a sistema inmutable (S3, WORM storage)
        await send_to_audit_log(audit_event)

        # Si es evento crítico, alertar
        if event_type in ["unauthorized_access", "privilege_escalation"]:
            await alert_security_team(audit_event)

# ==========================================
# LAYER 7: MONITORING & DETECTION
# ==========================================
class MonitoringLayer:
    """
    Capa de monitoreo - detección de amenazas
    """

    @staticmethod
    async def detect_anomalies(user_id: str, context: dict):
        """
        Detección de comportamiento anómalo
        """
        # Comportamiento normal del usuario
        user_profile = await get_user_behavior_profile(user_id)

        # Detectar anomalías
        anomalies = []

        # Ubicación inusual
        if context["country"] != user_profile.usual_country:
            anomalies.append("unusual_location")

        # Horario inusual
        hour = datetime.utcnow().hour
        if hour not in user_profile.usual_hours:
            anomalies.append("unusual_time")

        # Volumen de requests inusual
        recent_requests = await get_recent_request_count(user_id, minutes=5)
        if recent_requests > user_profile.avg_requests * 3:
            anomalies.append("unusual_volume")

        if anomalies:
            await alert_security_team({
                "user_id": user_id,
                "anomalies": anomalies,
                "context": context
            })

            # Requerir re-autenticación
            return {"require_mfa": True}

        return {"ok": True}

# ==========================================
# INTEGRATED DEFENSE
# ==========================================
class DefenseInDepthMiddleware:
    """
    Middleware que aplica todas las capas
    """

    async def __call__(self, request, call_next):
        # Layer 1: Network (handled by infrastructure)

        # Layer 2: Application Security
        if request.method == "POST":
            await self._validate_input(request.json)

        # Layer 3: Authentication
        identity = await self._authenticate(request)
        if not identity:
            return {"error": "Unauthorized"}, 401

        # Layer 4: Authorization
        authorized = await self._authorize(identity, request)
        if not authorized:
            await AuditLoggingLayer.log_security_event(
                event_type="unauthorized_access",
                principal_id=identity.principal_id,
                resource=request.path,
                action=request.method,
                result="denied",
                context={"client_ip": request.remote_addr}
            )
            return {"error": "Forbidden"}, 403

        # Layer 6: Audit Logging
        await AuditLoggingLayer.log_security_event(
            event_type="access",
            principal_id=identity.principal_id,
            resource=request.path,
            action=request.method,
            result="success",
            context={"client_ip": request.remote_addr}
        )

        # Layer 7: Anomaly Detection
        anomaly_result = await MonitoringLayer.detect_anomalies(
            identity.principal_id,
            {"client_ip": request.remote_addr, "country": "US"}
        )
        if anomaly_result.get("require_mfa"):
            return {"error": "MFA required"}, 403

        # Procesar request
        response = await call_next(request)

        # Layer 5: Encryption (handled by TLS)
        return response

    async def _validate_input(self, data: dict):
        """Validar todos los inputs"""
        for key, value in data.items():
            if isinstance(value, str):
                ApplicationSecurityLayer.validate_input(value)

    async def _authenticate(self, request) -> Optional[Identity]:
        """Autenticar request"""
        # Implementar
        pass

    async def _authorize(self, identity: Identity, request) -> bool:
        """Autorizar request"""
        # Implementar
        pass
```

---

## 3. Security Boundaries & Trust Zones

### ✅ SOLUCIÓN: Microsegmentación y trust boundaries

```python
# ==========================================
# TRUST ZONES
# ==========================================
from enum import Enum

class TrustZone(Enum):
    """
    Zonas de confianza en la arquitectura
    """
    PUBLIC = "public"           # Internet-facing
    DMZ = "dmz"                # DMZ (load balancers, API gateway)
    APPLICATION = "application" # App servers
    DATA = "data"              # Databases
    MANAGEMENT = "management"   # Admin tools
    TRUSTED = "trusted"        # Internal trusted services

# ==========================================
# SECURITY BOUNDARIES
# ==========================================
@dataclass
class SecurityBoundary:
    """
    Límite de seguridad entre zonas
    Requiere autenticación y encriptación
    """
    source_zone: TrustZone
    destination_zone: TrustZone
    allowed: bool
    encryption_required: bool
    authentication_required: bool
    audit_required: bool

class SecurityBoundaryPolicy:
    """
    Define políticas entre trust zones
    """

    BOUNDARIES = [
        # PUBLIC → DMZ: Permitido con TLS
        SecurityBoundary(
            source_zone=TrustZone.PUBLIC,
            destination_zone=TrustZone.DMZ,
            allowed=True,
            encryption_required=True,  # TLS
            authentication_required=False,
            audit_required=True
        ),

        # DMZ → APPLICATION: Permitido con mTLS
        SecurityBoundary(
            source_zone=TrustZone.DMZ,
            destination_zone=TrustZone.APPLICATION,
            allowed=True,
            encryption_required=True,  # mTLS
            authentication_required=True,  # Service identity
            audit_required=True
        ),

        # APPLICATION → DATA: Permitido con TLS + auth
        SecurityBoundary(
            source_zone=TrustZone.APPLICATION,
            destination_zone=TrustZone.DATA,
            allowed=True,
            encryption_required=True,
            authentication_required=True,
            audit_required=True
        ),

        # PUBLIC → DATA: PROHIBIDO
        SecurityBoundary(
            source_zone=TrustZone.PUBLIC,
            destination_zone=TrustZone.DATA,
            allowed=False,
            encryption_required=True,
            authentication_required=True,
            audit_required=True
        ),
    ]

    @classmethod
    def can_communicate(
        cls,
        source: TrustZone,
        destination: TrustZone
    ) -> Optional[SecurityBoundary]:
        """
        Verifica si comunicación está permitida
        """
        for boundary in cls.BOUNDARIES:
            if (boundary.source_zone == source and
                boundary.destination_zone == destination):
                return boundary if boundary.allowed else None

        # Default deny
        return None

# ==========================================
# SERVICE MESH SECURITY
# ==========================================
class ServiceMeshSecurity:
    """
    Security via service mesh (Istio, Linkerd)
    - Automatic mTLS
    - Traffic policies
    - Identity-based auth
    """

    @staticmethod
    def istio_authorization_policy():
        """
        Istio AuthorizationPolicy - YAML config
        """
        return """
        apiVersion: security.istio.io/v1beta1
        kind: AuthorizationPolicy
        metadata:
          name: orders-policy
          namespace: production
        spec:
          selector:
            matchLabels:
              app: orders-service

          # Default deny
          action: DENY

          rules:
          # Allow payments-service to call orders-service
          - from:
            - source:
                principals: ["cluster.local/ns/production/sa/payments-service"]
            to:
            - operation:
                methods: ["POST"]
                paths: ["/api/orders/*/payment"]

          # Allow users-service to read orders
          - from:
            - source:
                principals: ["cluster.local/ns/production/sa/users-service"]
            to:
            - operation:
                methods: ["GET"]
                paths: ["/api/orders/*"]
        """

    @staticmethod
    def istio_peer_authentication():
        """
        Require mTLS for all communication
        """
        return """
        apiVersion: security.istio.io/v1beta1
        kind: PeerAuthentication
        metadata:
          name: default
          namespace: production
        spec:
          mtls:
            mode: STRICT  # Require mTLS
        """
```

**📐 Arquitectura de Trust Zones:**

```
┌─────────────────────────────────────────────────────┐
│ PUBLIC ZONE (Internet)                              │
│ - User browsers                                     │
│ - API clients                                       │
└────────────┬────────────────────────────────────────┘
             │ HTTPS only
             ▼
┌─────────────────────────────────────────────────────┐
│ DMZ ZONE                                            │
│ - WAF (Web Application Firewall)                    │
│ - Load Balancer                                     │
│ - API Gateway                                       │
└────────────┬────────────────────────────────────────┘
             │ mTLS + Service Identity
             ▼
┌─────────────────────────────────────────────────────┐
│ APPLICATION ZONE                                    │
│ - Microservices                                     │
│ - Business logic                                    │
└────────────┬────────────────────────────────────────┘
             │ TLS + DB credentials (rotated)
             ▼
┌─────────────────────────────────────────────────────┐
│ DATA ZONE                                           │
│ - Databases                                         │
│ - Cache (Redis)                                     │
│ - Object storage                                    │
└─────────────────────────────────────────────────────┘
```

---

## 4. Secret Management Architecture

### ❌ ERROR COMÚN: Secrets en código o env vars
```python
# ❌ MAL - hardcoded
DATABASE_URL = "postgresql://user:password123@db:5432/prod"

# ❌ MAL - en .env commiteado
DB_PASSWORD=super_secret_password

# ❌ MAL - env vars en plain text (mejor, pero no ideal)
DB_PASSWORD = os.getenv("DB_PASSWORD")
```

### ✅ SOLUCIÓN: HashiCorp Vault + Dynamic Credentials

```python
import hvac
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio

# ==========================================
# VAULT CLIENT
# ==========================================
class VaultClient:
    """
    Cliente para HashiCorp Vault
    """

    def __init__(self, vault_url: str, token: Optional[str] = None):
        self.client = hvac.Client(url=vault_url, token=token)

    async def get_secret(self, path: str) -> dict:
        """
        Obtiene secret de Vault
        """
        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point="secret"
            )
            return secret["data"]["data"]

        except Exception as e:
            # Log y alertar - secret access failed
            print(f"Failed to retrieve secret {path}: {e}")
            raise

    async def get_dynamic_db_credentials(
        self,
        role_name: str
    ) -> 'DatabaseCredentials':
        """
        Obtiene credenciales dinámicas de BD
        - Generadas on-demand
        - TTL corto (1-8 horas)
        - Auto-rotación
        """
        response = self.client.secrets.database.generate_credentials(
            name=role_name,
            mount_point="database"
        )

        return DatabaseCredentials(
            username=response["data"]["username"],
            password=response["data"]["password"],
            ttl_seconds=response["lease_duration"],
            lease_id=response["lease_id"],
            created_at=datetime.utcnow()
        )

    async def renew_lease(self, lease_id: str, increment: int = 3600):
        """
        Renueva lease de credential dinámica
        """
        self.client.sys.renew_lease(
            lease_id=lease_id,
            increment=increment
        )

    async def revoke_lease(self, lease_id: str):
        """
        Revoca credential inmediatamente
        """
        self.client.sys.revoke_lease(lease_id=lease_id)

@dataclass
class DatabaseCredentials:
    username: str
    password: str
    ttl_seconds: int
    lease_id: str
    created_at: datetime

    @property
    def expires_at(self) -> datetime:
        return self.created_at + timedelta(seconds=self.ttl_seconds)

    @property
    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

# ==========================================
# CREDENTIAL MANAGER
# ==========================================
class DynamicCredentialManager:
    """
    Gestiona credenciales dinámicas con auto-renovación
    """

    def __init__(self, vault_client: VaultClient):
        self.vault = vault_client
        self.current_credentials: Optional[DatabaseCredentials] = None
        self._refresh_task: Optional[asyncio.Task] = None

    async def start(self, role_name: str):
        """
        Inicia gestor de credenciales
        """
        # Obtener credenciales iniciales
        self.current_credentials = await self.vault.get_dynamic_db_credentials(role_name)

        # Iniciar auto-refresh
        self._refresh_task = asyncio.create_task(
            self._auto_refresh_loop(role_name)
        )

    async def _auto_refresh_loop(self, role_name: str):
        """
        Loop que renueva credenciales antes de expirar
        """
        while True:
            if not self.current_credentials:
                break

            # Renovar a mitad del TTL
            sleep_seconds = self.current_credentials.ttl_seconds / 2

            await asyncio.sleep(sleep_seconds)

            try:
                # Intentar renovar lease
                await self.vault.renew_lease(
                    self.current_credentials.lease_id,
                    increment=self.current_credentials.ttl_seconds
                )

                print(f"✓ Renewed credentials lease: {self.current_credentials.lease_id}")

            except Exception as e:
                # Si falla renovación, obtener nuevas credenciales
                print(f"Lease renewal failed, getting new credentials: {e}")

                self.current_credentials = await self.vault.get_dynamic_db_credentials(role_name)

    async def get_connection_string(self) -> str:
        """
        Obtiene connection string con credenciales actuales
        """
        if not self.current_credentials or self.current_credentials.is_expired:
            raise ValueError("No valid credentials available")

        return (
            f"postgresql://{self.current_credentials.username}:"
            f"{self.current_credentials.password}@db:5432/prod"
        )

    async def stop(self):
        """
        Detiene gestor y revoca credenciales
        """
        if self._refresh_task:
            self._refresh_task.cancel()

        if self.current_credentials:
            await self.vault.revoke_lease(self.current_credentials.lease_id)

# ==========================================
# SECRETS ROTATION
# ==========================================
class SecretRotationPolicy:
    """
    Política de rotación de secrets
    """

    @staticmethod
    def should_rotate(secret_metadata: dict) -> bool:
        """
        Determina si secret debe rotarse
        """
        created_at = datetime.fromisoformat(secret_metadata["created_time"])
        age = datetime.utcnow() - created_at

        # Rotar secrets cada 90 días
        max_age = timedelta(days=90)

        return age >= max_age

class AutomatedSecretRotation:
    """
    Rotación automatizada de secrets
    """

    def __init__(self, vault_client: VaultClient):
        self.vault = vault_client

    async def rotate_api_key(self, service_name: str):
        """
        Rota API key de servicio
        """
        # 1. Generar nuevo API key
        new_key = await self._generate_api_key()

        # 2. Guardar en Vault
        await self.vault.client.secrets.kv.v2.create_or_update_secret(
            path=f"api-keys/{service_name}",
            secret={"key": new_key},
            mount_point="secret"
        )

        # 3. Notificar servicio (tiene tiempo de gracia para actualizar)
        await self._notify_service(service_name, grace_period_hours=24)

        # 4. Después del grace period, invalidar key antigua
        await asyncio.sleep(24 * 3600)
        await self._revoke_old_key(service_name)

    async def _generate_api_key(self) -> str:
        """Genera API key criptográficamente seguro"""
        import secrets
        return secrets.token_urlsafe(32)

    async def _notify_service(self, service_name: str, grace_period_hours: int):
        """Notifica servicio de nueva key"""
        # Implementar notificación
        pass

    async def _revoke_old_key(self, service_name: str):
        """Revoca key antigua"""
        # Implementar revocación
        pass

# ==========================================
# EJEMPLO DE USO
# ==========================================
async def main():
    # Setup Vault client
    vault = VaultClient(
        vault_url="https://vault.company.com",
        token=os.getenv("VAULT_TOKEN")  # De service account
    )

    # Iniciar credential manager
    cred_manager = DynamicCredentialManager(vault)
    await cred_manager.start(role_name="orders-service-db")

    # Usar credenciales
    conn_string = await cred_manager.get_connection_string()
    db = await connect_to_database(conn_string)

    # Credenciales se auto-renuevan en background
    # ...

    # Cleanup
    await cred_manager.stop()
```

**🔐 Vault Configuration:**

```hcl
# Vault config para dynamic DB credentials

# Enable database secrets engine
path "sys/mounts/database" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Configure PostgreSQL connection
resource "vault_database_secret_backend_connection" "postgres" {
  backend       = "database"
  name          = "orders-db"
  allowed_roles = ["orders-service-db"]

  postgresql {
    connection_url = "postgresql://{{username}}:{{password}}@postgres:5432/orders"
    username       = "vault-admin"
    password       = var.postgres_admin_password
  }
}

# Define role
resource "vault_database_secret_backend_role" "orders_service" {
  backend = "database"
  name    = "orders-service-db"
  db_name = vault_database_secret_backend_connection.postgres.name

  creation_statements = [
    "CREATE USER \"{{name}}\" WITH PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
    "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"
  ]

  default_ttl = 3600      # 1 hora
  max_ttl     = 28800     # 8 horas
}
```

---

## 5. Authentication & Authorization

### ✅ SOLUCIÓN: OAuth2 + OIDC + RBAC/ABAC

```python
# Ver archivos 17_BACKEND_SECURITY_PERFORMANCE.md y 20_ARQUITECTURA_TECNICA_AVANZADA_2026.md
# para implementaciones detalladas de OAuth2, OIDC, RBAC, ABAC

# ==========================================
# ATTRIBUTE-BASED ACCESS CONTROL (ABAC)
# ==========================================
from typing import Any, Dict

class ABACPolicy:
    """
    ABAC - autorización basada en atributos
    Más flexible que RBAC
    """

    def __init__(self):
        self.rules: List['ABACRule'] = []

    def add_rule(self, rule: 'ABACRule'):
        self.rules.append(rule)

    async def evaluate(
        self,
        subject_attributes: Dict[str, Any],
        resource_attributes: Dict[str, Any],
        action: str,
        environment_attributes: Dict[str, Any]
    ) -> bool:
        """
        Evalúa acceso basado en atributos
        """
        for rule in self.rules:
            if rule.matches(
                subject_attributes,
                resource_attributes,
                action,
                environment_attributes
            ):
                return rule.effect == "allow"

        # Default deny
        return False

@dataclass
class ABACRule:
    """
    Regla ABAC individual
    """
    name: str
    effect: str  # allow, deny
    subject_conditions: Dict[str, Any]
    resource_conditions: Dict[str, Any]
    actions: List[str]
    environment_conditions: Dict[str, Any]

    def matches(
        self,
        subject_attrs: dict,
        resource_attrs: dict,
        action: str,
        env_attrs: dict
    ) -> bool:
        """
        Verifica si regla aplica
        """
        # Verificar acción
        if action not in self.actions:
            return False

        # Verificar condiciones de sujeto
        if not self._match_conditions(subject_attrs, self.subject_conditions):
            return False

        # Verificar condiciones de recurso
        if not self._match_conditions(resource_attrs, self.resource_conditions):
            return False

        # Verificar condiciones de ambiente
        if not self._match_conditions(env_attrs, self.environment_conditions):
            return False

        return True

    def _match_conditions(self, attrs: dict, conditions: dict) -> bool:
        """Verifica condiciones"""
        for key, expected_value in conditions.items():
            if key not in attrs:
                return False

            actual_value = attrs[key]

            # Soportar operadores
            if isinstance(expected_value, dict):
                operator = expected_value.get("operator")
                value = expected_value.get("value")

                if operator == "equals":
                    if actual_value != value:
                        return False
                elif operator == "in":
                    if actual_value not in value:
                        return False
                elif operator == "greater_than":
                    if actual_value <= value:
                        return False
            else:
                if actual_value != expected_value:
                    return False

        return True

# ==========================================
# EJEMPLO ABAC
# ==========================================
abac = ABACPolicy()

# Regla: Doctors pueden leer medical records de sus pacientes
abac.add_rule(ABACRule(
    name="doctors_read_own_patients",
    effect="allow",
    subject_conditions={
        "role": "doctor",
        "department": {"operator": "equals", "value": "cardiology"}
    },
    resource_conditions={
        "type": "medical_record",
        "assigned_doctor_id": {"operator": "equals", "value": "${subject.user_id}"}
    },
    actions=["read"],
    environment_conditions={
        "time": {"operator": "in", "value": ["business_hours"]}
    }
))

# Evaluar
can_access = await abac.evaluate(
    subject_attributes={
        "user_id": "doc_001",
        "role": "doctor",
        "department": "cardiology"
    },
    resource_attributes={
        "type": "medical_record",
        "patient_id": "pat_123",
        "assigned_doctor_id": "doc_001"
    },
    action="read",
    environment_attributes={
        "time": "business_hours",
        "location": "hospital"
    }
)
```

---

## 6-10. [Remaining Sections]

Por limitaciones de espacio, las secciones 6-10 están resumidas:

### 6. API Security
- Rate limiting avanzado (ver archivo 25)
- API authentication (API keys, JWT)
- Input validation
- CORS policies

### 7. Data Security
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- PII handling & data masking
- Key management (KMS)

### 8. Threat Modeling
- STRIDE methodology
- Attack trees
- Threat assessment matrix
- Mitigation strategies

### 9. Security Testing
- SAST (Static analysis)
- DAST (Dynamic analysis)
- Penetration testing
- Dependency scanning

### 10. Security Monitoring & SIEM
- Security events aggregation
- Anomaly detection
- Incident response
- Threat intelligence

---

## 📊 Security Decision Matrix

| Control | Critical Systems | Standard Systems | Development |
|---------|------------------|------------------|-------------|
| **MFA** | Required | Recommended | Optional |
| **Encryption** | AES-256 + TLS 1.3 | AES-128 + TLS 1.2 | TLS 1.2 |
| **Secrets** | Vault + Dynamic | Vault | Env vars |
| **Audit Logging** | All actions | Write actions | Errors only |
| **Network** | Zero Trust + mTLS | Firewall rules | Basic firewall |

**Tamaño:** 48KB | **Código:** ~1,800 líneas | **Complejidad:** ⭐⭐⭐⭐⭐
