# Backend: Security, Chaos Engineering y Performance

## Objetivo
Patrones avanzados de seguridad, pruebas de resiliencia, y optimización de performance para sistemas en producción.

---

## CATEGORÍA 1: Security Avanzada

### 1.1 OAuth2 y OpenID Connect
**Dificultad:** ⭐⭐⭐⭐⭐

**Python - OAuth2 Server Implementation**

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import secrets
import hashlib

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class OAuth2Server:
    """
    OAuth2 Authorization Server
    Implements:
    - Authorization Code Flow
    - Client Credentials Flow
    - Refresh Token Flow
    - PKCE (Proof Key for Code Exchange)
    """

    def __init__(self, db):
        self.db = db
        self.authorization_codes = {}  # In production: use Redis
        self.refresh_tokens = {}       # In production: use Redis

    async def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "token_type": "access"
        })

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def create_refresh_token(self, user_id: int) -> str:
        """Create refresh token"""

        token = secrets.token_urlsafe(32)

        # Store refresh token
        self.refresh_tokens[token] = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        }

        return token

    async def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token"""

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception

            # Check if token is revoked
            if await self.is_token_revoked(token):
                raise credentials_exception

            return payload

        except JWTError:
            raise credentials_exception

    async def is_token_revoked(self, token: str) -> bool:
        """Check if token is in revocation list"""
        # In production: check Redis set
        revoked_key = f"revoked_token:{hashlib.sha256(token.encode()).hexdigest()}"
        return await self.db.exists(revoked_key)

    async def revoke_token(self, token: str):
        """Revoke token"""
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get('exp')

        if exp:
            ttl = exp - int(datetime.utcnow().timestamp())
            if ttl > 0:
                revoked_key = f"revoked_token:{hashlib.sha256(token.encode()).hexdigest()}"
                await self.db.setex(revoked_key, ttl, "1")

    # Authorization Code Flow (for web apps)
    async def create_authorization_code(
        self,
        client_id: str,
        user_id: int,
        redirect_uri: str,
        scope: str,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None
    ) -> str:
        """Create authorization code (step 1 of OAuth2 flow)"""

        code = secrets.token_urlsafe(32)

        self.authorization_codes[code] = {
            'client_id': client_id,
            'user_id': user_id,
            'redirect_uri': redirect_uri,
            'scope': scope,
            'code_challenge': code_challenge,
            'code_challenge_method': code_challenge_method,
            'created_at': datetime.utcnow(),
            'used': False
        }

        return code

    async def exchange_code_for_token(
        self,
        code: str,
        client_id: str,
        redirect_uri: str,
        code_verifier: Optional[str] = None
    ) -> dict:
        """Exchange authorization code for tokens (step 2)"""

        if code not in self.authorization_codes:
            raise HTTPException(status_code=400, detail="Invalid authorization code")

        code_data = self.authorization_codes[code]

        # Validate code
        if code_data['used']:
            raise HTTPException(status_code=400, detail="Code already used")

        if code_data['client_id'] != client_id:
            raise HTTPException(status_code=400, detail="Invalid client")

        if code_data['redirect_uri'] != redirect_uri:
            raise HTTPException(status_code=400, detail="Invalid redirect URI")

        # Check code expiration (10 minutes)
        if (datetime.utcnow() - code_data['created_at']).seconds > 600:
            raise HTTPException(status_code=400, detail="Code expired")

        # Verify PKCE
        if code_data['code_challenge']:
            if not code_verifier:
                raise HTTPException(status_code=400, detail="Code verifier required")

            if not self._verify_pkce(
                code_verifier,
                code_data['code_challenge'],
                code_data['code_challenge_method']
            ):
                raise HTTPException(status_code=400, detail="Invalid code verifier")

        # Mark code as used
        code_data['used'] = True

        # Generate tokens
        user_id = code_data['user_id']

        access_token = await self.create_access_token(
            data={
                "sub": str(user_id),
                "scope": code_data['scope']
            }
        )

        refresh_token = await self.create_refresh_token(user_id)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "refresh_token": refresh_token,
            "scope": code_data['scope']
        }

    def _verify_pkce(
        self,
        code_verifier: str,
        code_challenge: str,
        method: str
    ) -> bool:
        """Verify PKCE challenge"""

        if method == "S256":
            # SHA256 hash
            computed_challenge = hashlib.sha256(code_verifier.encode()).hexdigest()
        elif method == "plain":
            computed_challenge = code_verifier
        else:
            return False

        return computed_challenge == code_challenge

    # Refresh Token Flow
    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Get new access token using refresh token"""

        if refresh_token not in self.refresh_tokens:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        token_data = self.refresh_tokens[refresh_token]

        # Check expiration
        if datetime.utcnow() > token_data['expires_at']:
            del self.refresh_tokens[refresh_token]
            raise HTTPException(status_code=400, detail="Refresh token expired")

        # Generate new access token
        user_id = token_data['user_id']

        access_token = await self.create_access_token(
            data={"sub": str(user_id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

    # Client Credentials Flow (for service-to-service)
    async def client_credentials_token(
        self,
        client_id: str,
        client_secret: str,
        scope: str
    ) -> dict:
        """Get token using client credentials"""

        # Verify client
        client = await self.db.get_client(client_id)

        if not client or not self._verify_client_secret(client_secret, client['secret_hash']):
            raise HTTPException(status_code=401, detail="Invalid client credentials")

        # Generate token
        access_token = await self.create_access_token(
            data={
                "sub": client_id,
                "scope": scope,
                "client_id": client_id
            },
            expires_delta=timedelta(hours=1)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "scope": scope
        }

    def _verify_client_secret(self, secret: str, secret_hash: str) -> bool:
        """Verify client secret"""
        return pwd_context.verify(secret, secret_hash)

# Endpoints
oauth2_server = OAuth2Server(db)

@app.post("/oauth/authorize")
async def authorize(
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = "S256",
    current_user = Depends(get_current_user)
):
    """Authorization endpoint (step 1)"""

    # Validate client and redirect URI
    client = await db.get_client(client_id)
    if not client or redirect_uri not in client['redirect_uris']:
        raise HTTPException(status_code=400, detail="Invalid client or redirect URI")

    # Create authorization code
    code = await oauth2_server.create_authorization_code(
        client_id=client_id,
        user_id=current_user.id,
        redirect_uri=redirect_uri,
        scope=scope,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method
    )

    # Redirect user back to client
    return RedirectResponse(
        url=f"{redirect_uri}?code={code}&state={state}"
    )

@app.post("/oauth/token")
async def token(
    grant_type: str,
    code: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    refresh_token: Optional[str] = None,
    code_verifier: Optional[str] = None,
    scope: Optional[str] = None
):
    """Token endpoint"""

    if grant_type == "authorization_code":
        # Exchange code for token
        return await oauth2_server.exchange_code_for_token(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier
        )

    elif grant_type == "refresh_token":
        # Refresh access token
        return await oauth2_server.refresh_access_token(refresh_token)

    elif grant_type == "client_credentials":
        # Client credentials flow
        return await oauth2_server.client_credentials_token(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope
        )

    else:
        raise HTTPException(status_code=400, detail="Unsupported grant type")

@app.post("/oauth/revoke")
async def revoke_token(
    token: str,
    token_type_hint: Optional[str] = None
):
    """Revoke token"""
    await oauth2_server.revoke_token(token)
    return {"status": "revoked"}

# Protected endpoint
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from token"""
    payload = await oauth2_server.verify_token(token)
    user_id = int(payload.get("sub"))
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/protected")
async def protected_endpoint(current_user = Depends(get_current_user)):
    return {"message": f"Hello {current_user.name}"}
```

---

### 1.2 mTLS (Mutual TLS) Authentication
**Dificultad:** ⭐⭐⭐⭐⭐

```python
import ssl
from fastapi import FastAPI, Request, HTTPException
from typing import Optional
import cryptography
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

class mTLSAuthenticator:
    """
    Mutual TLS authentication
    Both client and server verify each other's certificates
    """

    def __init__(self, ca_cert_path: str, allowed_clients: dict):
        self.ca_cert = self._load_ca_cert(ca_cert_path)
        self.allowed_clients = allowed_clients  # client_id -> certificate CN

    def _load_ca_cert(self, path: str):
        """Load CA certificate"""
        with open(path, 'rb') as f:
            return x509.load_pem_x509_certificate(f.read())

    async def authenticate_client(self, request: Request) -> dict:
        """Authenticate client from certificate"""

        # Get client certificate from request
        client_cert_pem = request.headers.get('X-SSL-Client-Cert')

        if not client_cert_pem:
            raise HTTPException(
                status_code=401,
                detail="Client certificate required"
            )

        try:
            # Parse certificate
            client_cert = x509.load_pem_x509_certificate(
                client_cert_pem.encode()
            )

            # Verify certificate
            await self._verify_certificate(client_cert)

            # Extract client info
            client_id = self._extract_client_id(client_cert)

            return {
                'client_id': client_id,
                'common_name': self._get_common_name(client_cert),
                'organization': self._get_organization(client_cert)
            }

        except Exception as e:
            logger.error(f"Certificate verification failed: {e}")
            raise HTTPException(status_code=401, detail="Invalid certificate")

    async def _verify_certificate(self, cert: x509.Certificate):
        """Verify certificate validity and chain of trust"""

        # Check if certificate is expired
        now = datetime.utcnow()
        if cert.not_valid_before > now or cert.not_valid_after < now:
            raise ValueError("Certificate expired or not yet valid")

        # Verify certificate was signed by our CA
        try:
            self.ca_cert.public_key().verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                cert.signature_algorithm_parameters
            )
        except Exception:
            raise ValueError("Certificate not signed by trusted CA")

        # Check certificate revocation (in production: check CRL/OCSP)
        if await self._is_certificate_revoked(cert):
            raise ValueError("Certificate has been revoked")

    async def _is_certificate_revoked(self, cert: x509.Certificate) -> bool:
        """Check if certificate is revoked"""
        # In production: check Certificate Revocation List (CRL)
        # or Online Certificate Status Protocol (OCSP)
        serial_number = cert.serial_number
        # Check against revocation list in database/Redis
        return False

    def _extract_client_id(self, cert: x509.Certificate) -> str:
        """Extract client ID from certificate"""
        # Get from Subject Alternative Name extension
        try:
            san = cert.extensions.get_extension_for_oid(
                x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
            )
            return san.value.get_values_for_type(x509.DNSName)[0]
        except:
            return self._get_common_name(cert)

    def _get_common_name(self, cert: x509.Certificate) -> str:
        """Get Common Name from certificate"""
        return cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    def _get_organization(self, cert: x509.Certificate) -> str:
        """Get Organization from certificate"""
        try:
            return cert.subject.get_attributes_for_oid(
                NameOID.ORGANIZATION_NAME
            )[0].value
        except:
            return ""

# Middleware
mtls_auth = mTLSAuthenticator(
    ca_cert_path="/etc/certs/ca.crt",
    allowed_clients={}
)

@app.middleware("http")
async def mtls_middleware(request: Request, call_next):
    """Enforce mTLS authentication"""

    # Only for specific paths
    if request.url.path.startswith("/api/internal"):
        client = await mtls_auth.authenticate_client(request)
        request.state.client = client

    return await call_next(request)

# Server configuration with SSL
def create_ssl_context() -> ssl.SSLContext:
    """Create SSL context for mTLS"""

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Load server certificate and key
    context.load_cert_chain(
        certfile="/etc/certs/server.crt",
        keyfile="/etc/certs/server.key"
    )

    # Load CA certificate for client verification
    context.load_verify_locations(cafile="/etc/certs/ca.crt")

    # Require client certificate
    context.verify_mode = ssl.CERT_REQUIRED

    # Use strong cipher suites
    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')

    # Set minimum TLS version
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    return context

# Run with mTLS
if __name__ == "__main__":
    import uvicorn
    ssl_context = create_ssl_context()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="/etc/certs/server.key",
        ssl_certfile="/etc/certs/server.crt",
        ssl_ca_certs="/etc/certs/ca.crt",
        ssl_cert_reqs=ssl.CERT_REQUIRED
    )
```

---

### 1.3 API Key Rotation y Management
**Dificultad:** ⭐⭐⭐⭐

```python
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional

class APIKeyManager:
    """
    API Key management with:
    - Automatic rotation
    - Multiple active keys per client
    - Key expiration
    - Rate limiting per key
    - Usage tracking
    """

    def __init__(self, db, redis):
        self.db = db
        self.redis = redis

    async def create_api_key(
        self,
        client_id: str,
        name: str,
        scopes: list,
        expires_in_days: int = 90
    ) -> dict:
        """Create new API key"""

        # Generate secure random key
        api_key = self._generate_key()
        key_hash = self._hash_key(api_key)

        # Store in database
        key_id = await self.db.execute(
            """
            INSERT INTO api_keys (
                client_id, key_hash, name, scopes,
                created_at, expires_at, active
            )
            VALUES ($1, $2, $3, $4, NOW(), NOW() + INTERVAL '%s days', true)
            RETURNING id
            """,
            client_id, key_hash, name, scopes, expires_in_days
        )

        # Log key creation
        logger.info(
            f"API key created",
            client_id=client_id,
            key_id=key_id[0]['id'],
            name=name
        )

        # Return key (only time it's shown in plain text)
        return {
            'api_key': api_key,
            'key_id': key_id[0]['id'],
            'expires_at': (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat()
        }

    async def validate_api_key(self, api_key: str) -> Optional[dict]:
        """Validate API key and return client info"""

        key_hash = self._hash_key(api_key)

        # Check cache first
        cached = await self.redis.get(f"api_key:{key_hash}")
        if cached:
            return json.loads(cached)

        # Query database
        result = await self.db.execute(
            """
            SELECT id, client_id, scopes, expires_at, active, rate_limit
            FROM api_keys
            WHERE key_hash = $1
            """,
            key_hash
        )

        if not result:
            return None

        key_data = result[0]

        # Validate
        if not key_data['active']:
            logger.warning(f"Inactive API key used: {key_data['id']}")
            return None

        if key_data['expires_at'] < datetime.utcnow():
            logger.warning(f"Expired API key used: {key_data['id']}")
            await self._deactivate_key(key_data['id'])
            return None

        # Cache for 5 minutes
        await self.redis.setex(
            f"api_key:{key_hash}",
            300,
            json.dumps(key_data, default=str)
        )

        # Track usage
        await self._track_usage(key_data['id'])

        return key_data

    async def rotate_key(self, old_key_id: int) -> dict:
        """
        Rotate API key
        Creates new key and schedules old key for deactivation
        """

        # Get old key info
        old_key = await self.db.execute(
            "SELECT client_id, name, scopes FROM api_keys WHERE id = $1",
            old_key_id
        )

        if not old_key:
            raise ValueError("Key not found")

        # Create new key
        new_key = await self.create_api_key(
            client_id=old_key[0]['client_id'],
            name=f"{old_key[0]['name']} (rotated)",
            scopes=old_key[0]['scopes']
        )

        # Schedule old key deactivation (grace period)
        grace_period_hours = 24

        await self.db.execute(
            """
            UPDATE api_keys
            SET rotation_scheduled_at = NOW() + INTERVAL '%s hours'
            WHERE id = $1
            """,
            grace_period_hours,
            old_key_id
        )

        logger.info(
            f"API key rotated",
            old_key_id=old_key_id,
            new_key_id=new_key['key_id'],
            grace_period_hours=grace_period_hours
        )

        return new_key

    async def revoke_key(self, key_id: int):
        """Immediately revoke API key"""

        await self._deactivate_key(key_id)

        # Clear cache
        key_hash = await self.db.execute(
            "SELECT key_hash FROM api_keys WHERE id = $1",
            key_id
        )

        if key_hash:
            await self.redis.delete(f"api_key:{key_hash[0]['key_hash']}")

        logger.info(f"API key revoked", key_id=key_id)

    async def check_rate_limit(self, key_id: int, limit: int) -> bool:
        """Check rate limit for API key"""

        key = f"api_key_rate:{key_id}"
        current_minute = int(time.time() / 60)
        rate_key = f"{key}:{current_minute}"

        current_count = await self.redis.get(rate_key)
        current_count = int(current_count) if current_count else 0

        if current_count >= limit:
            return False

        # Increment
        pipe = self.redis.pipeline()
        pipe.incr(rate_key)
        pipe.expire(rate_key, 60)
        await pipe.execute()

        return True

    async def get_usage_stats(self, key_id: int, days: int = 30) -> dict:
        """Get usage statistics for API key"""

        stats = await self.db.execute(
            """
            SELECT
                DATE(used_at) as date,
                COUNT(*) as request_count,
                COUNT(DISTINCT endpoint) as unique_endpoints
            FROM api_key_usage
            WHERE key_id = $1
              AND used_at > NOW() - INTERVAL '%s days'
            GROUP BY DATE(used_at)
            ORDER BY date DESC
            """,
            key_id, days
        )

        return {
            'key_id': key_id,
            'daily_stats': stats,
            'total_requests': sum(s['request_count'] for s in stats)
        }

    def _generate_key(self) -> str:
        """Generate secure API key"""
        # Format: prefix_randompart
        prefix = "sk"  # secret key
        random_part = secrets.token_urlsafe(32)
        return f"{prefix}_{random_part}"

    def _hash_key(self, api_key: str) -> str:
        """Hash API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()

    async def _deactivate_key(self, key_id: int):
        """Deactivate API key"""
        await self.db.execute(
            "UPDATE api_keys SET active = false WHERE id = $1",
            key_id
        )

    async def _track_usage(self, key_id: int):
        """Track API key usage"""
        # Async insert to avoid blocking
        asyncio.create_task(
            self.db.execute(
                """
                INSERT INTO api_key_usage (key_id, used_at, endpoint)
                VALUES ($1, NOW(), $2)
                """,
                key_id,
                "endpoint"  # Get from request context
            )
        )

# Middleware
api_key_manager = APIKeyManager(db, redis_client)

@app.middleware("http")
async def api_key_auth_middleware(request: Request, call_next):
    """API Key authentication middleware"""

    # Skip for public endpoints
    if request.url.path.startswith("/public"):
        return await call_next(request)

    # Get API key from header
    api_key = request.headers.get("X-API-Key")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"}
        )

    # Validate key
    key_data = await api_key_manager.validate_api_key(api_key)

    if not key_data:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Check rate limit
    rate_limit = key_data.get('rate_limit', 1000)
    allowed = await api_key_manager.check_rate_limit(
        key_data['id'],
        rate_limit
    )

    if not allowed:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Store in request state
    request.state.api_key_data = key_data
    request.state.client_id = key_data['client_id']

    response = await call_next(request)
    return response

# Background task: Auto-rotation
async def auto_rotate_expiring_keys():
    """Automatically rotate keys expiring soon"""

    while True:
        try:
            # Find keys expiring in next 7 days
            expiring_keys = await db.execute(
                """
                SELECT id, client_id
                FROM api_keys
                WHERE active = true
                  AND expires_at < NOW() + INTERVAL '7 days'
                  AND rotation_scheduled_at IS NULL
                """
            )

            for key in expiring_keys:
                await api_key_manager.rotate_key(key['id'])

                # Notify client
                await notify_client(
                    key['client_id'],
                    "API key expiring soon - new key generated"
                )

            await asyncio.sleep(3600)  # Check every hour

        except Exception as e:
            logger.error(f"Auto-rotation error: {e}")
            await asyncio.sleep(3600)
```

---

## CATEGORÍA 2: Chaos Engineering

### 2.1 Chaos Testing Framework
**Dificultad:** ⭐⭐⭐⭐⭐

```python
import random
import asyncio
from typing import Callable, Optional
from enum import Enum
from dataclasses import dataclass

class ChaosType(Enum):
    LATENCY = "latency"
    ERROR = "error"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    NETWORK_PARTITION = "network_partition"
    DEPENDENCY_FAILURE = "dependency_failure"

@dataclass
class ChaosExperiment:
    """Definition of chaos experiment"""
    name: str
    chaos_type: ChaosType
    probability: float  # 0.0 to 1.0
    enabled: bool = True

    # Latency chaos
    latency_ms_min: int = 0
    latency_ms_max: int = 0

    # Error chaos
    error_rate: float = 0.0
    error_codes: list = None

    # Resource chaos
    cpu_percentage: int = 0
    memory_mb: int = 0

class ChaosMonkey:
    """
    Chaos Engineering framework
    Inject failures to test system resilience
    """

    def __init__(self):
        self.experiments = {}
        self.enabled = False

    def register_experiment(self, experiment: ChaosExperiment):
        """Register chaos experiment"""
        self.experiments[experiment.name] = experiment
        logger.info(f"Chaos experiment registered: {experiment.name}")

    def enable(self):
        """Enable chaos testing"""
        self.enabled = True
        logger.warning("Chaos Monkey ENABLED - failures will be injected")

    def disable(self):
        """Disable chaos testing"""
        self.enabled = False
        logger.info("Chaos Monkey disabled")

    async def inject_chaos(
        self,
        experiment_name: str,
        operation: Callable
    ):
        """
        Inject chaos before operation
        Either executes normally or injects failure
        """

        if not self.enabled:
            return await operation()

        if experiment_name not in self.experiments:
            return await operation()

        experiment = self.experiments[experiment_name]

        if not experiment.enabled:
            return await operation()

        # Roll dice to see if chaos should be injected
        if random.random() > experiment.probability:
            return await operation()

        # Inject chaos based on type
        if experiment.chaos_type == ChaosType.LATENCY:
            return await self._inject_latency(experiment, operation)

        elif experiment.chaos_type == ChaosType.ERROR:
            return await self._inject_error(experiment, operation)

        elif experiment.chaos_type == ChaosType.RESOURCE_EXHAUSTION:
            return await self._inject_resource_exhaustion(experiment, operation)

        elif experiment.chaos_type == ChaosType.DEPENDENCY_FAILURE:
            return await self._inject_dependency_failure(experiment, operation)

        else:
            return await operation()

    async def _inject_latency(
        self,
        experiment: ChaosExperiment,
        operation: Callable
    ):
        """Inject random latency"""

        latency_ms = random.randint(
            experiment.latency_ms_min,
            experiment.latency_ms_max
        )

        logger.warning(
            f"Chaos: Injecting {latency_ms}ms latency",
            experiment=experiment.name
        )

        await asyncio.sleep(latency_ms / 1000)

        return await operation()

    async def _inject_error(
        self,
        experiment: ChaosExperiment,
        operation: Callable
    ):
        """Inject random error"""

        if random.random() < experiment.error_rate:
            error_code = random.choice(experiment.error_codes or [500])

            logger.warning(
                f"Chaos: Injecting error {error_code}",
                experiment=experiment.name
            )

            raise HTTPException(
                status_code=error_code,
                detail=f"Chaos experiment: {experiment.name}"
            )

        return await operation()

    async def _inject_resource_exhaustion(
        self,
        experiment: ChaosExperiment,
        operation: Callable
    ):
        """Simulate resource exhaustion"""

        logger.warning(
            f"Chaos: Simulating resource exhaustion",
            experiment=experiment.name
        )

        # Simulate CPU usage
        if experiment.cpu_percentage > 0:
            # Busy loop for short duration
            end_time = time.time() + 0.1  # 100ms
            while time.time() < end_time:
                _ = sum(range(1000))

        # Simulate memory usage
        if experiment.memory_mb > 0:
            # Allocate memory
            waste = bytearray(experiment.memory_mb * 1024 * 1024)
            await asyncio.sleep(0.1)
            del waste

        return await operation()

    async def _inject_dependency_failure(
        self,
        experiment: ChaosExperiment,
        operation: Callable
    ):
        """Simulate dependency failure"""

        logger.warning(
            f"Chaos: Simulating dependency failure",
            experiment=experiment.name
        )

        raise Exception(f"Dependency unavailable: {experiment.name}")

# Chaos middleware
chaos_monkey = ChaosMonkey()

# Register experiments
chaos_monkey.register_experiment(ChaosExperiment(
    name="database_latency",
    chaos_type=ChaosType.LATENCY,
    probability=0.1,  # 10% of requests
    latency_ms_min=100,
    latency_ms_max=2000
))

chaos_monkey.register_experiment(ChaosExperiment(
    name="api_errors",
    chaos_type=ChaosType.ERROR,
    probability=0.05,  # 5% of requests
    error_rate=1.0,
    error_codes=[500, 502, 503]
))

chaos_monkey.register_experiment(ChaosExperiment(
    name="payment_service_failure",
    chaos_type=ChaosType.DEPENDENCY_FAILURE,
    probability=0.02  # 2% of requests
))

# Enable in testing/staging only
if os.getenv('ENV') in ['testing', 'staging']:
    chaos_monkey.enable()

# Usage in code
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async def fetch_user():
        return await db.query(User).filter(User.id == user_id).first()

    # Inject chaos
    return await chaos_monkey.inject_chaos("database_latency", fetch_user)

# Decorator for chaos injection
def with_chaos(experiment_name: str):
    """Decorator to inject chaos into function"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            async def operation():
                return await func(*args, **kwargs)

            return await chaos_monkey.inject_chaos(experiment_name, operation)

        return wrapper
    return decorator

# Usage
@with_chaos("api_errors")
async def call_external_api(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Chaos experiment runner
class ChaosExperimentRunner:
    """
    Run structured chaos experiments
    Measure system behavior under failure conditions
    """

    def __init__(self, chaos_monkey: ChaosMonkey, metrics_collector):
        self.chaos = chaos_monkey
        self.metrics = metrics_collector

    async def run_experiment(
        self,
        experiment_name: str,
        duration_seconds: int,
        target_endpoint: str,
        requests_per_second: int
    ):
        """
        Run chaos experiment and collect metrics
        """

        logger.info(
            f"Starting chaos experiment: {experiment_name}",
            duration=duration_seconds
        )

        # Baseline metrics (before chaos)
        baseline = await self._collect_baseline(
            target_endpoint,
            requests_per_second,
            duration=30
        )

        # Enable experiment
        experiment = self.chaos.experiments[experiment_name]
        experiment.enabled = True

        # Run with chaos
        chaos_metrics = await self._run_with_chaos(
            target_endpoint,
            requests_per_second,
            duration_seconds
        )

        # Disable experiment
        experiment.enabled = False

        # Compare results
        results = self._analyze_results(baseline, chaos_metrics)

        logger.info(
            f"Chaos experiment completed: {experiment_name}",
            results=results
        )

        return results

    async def _collect_baseline(
        self,
        endpoint: str,
        rps: int,
        duration: int
    ) -> dict:
        """Collect baseline metrics without chaos"""

        metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'latencies': [],
            'error_codes': {}
        }

        end_time = time.time() + duration
        request_interval = 1.0 / rps

        while time.time() < end_time:
            start = time.time()

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"http://localhost:8000{endpoint}")

                    latency = (time.time() - start) * 1000
                    metrics['latencies'].append(latency)
                    metrics['total_requests'] += 1

                    if response.status_code < 400:
                        metrics['successful_requests'] += 1
                    else:
                        metrics['failed_requests'] += 1
                        metrics['error_codes'][response.status_code] = \
                            metrics['error_codes'].get(response.status_code, 0) + 1

            except Exception:
                metrics['failed_requests'] += 1

            await asyncio.sleep(request_interval)

        return metrics

    async def _run_with_chaos(
        self,
        endpoint: str,
        rps: int,
        duration: int
    ) -> dict:
        """Run load test with chaos enabled"""
        return await self._collect_baseline(endpoint, rps, duration)

    def _analyze_results(self, baseline: dict, chaos: dict) -> dict:
        """Analyze experiment results"""

        return {
            'baseline': {
                'success_rate': baseline['successful_requests'] / baseline['total_requests'],
                'avg_latency': sum(baseline['latencies']) / len(baseline['latencies']),
                'p99_latency': sorted(baseline['latencies'])[int(len(baseline['latencies']) * 0.99)]
            },
            'with_chaos': {
                'success_rate': chaos['successful_requests'] / chaos['total_requests'],
                'avg_latency': sum(chaos['latencies']) / len(chaos['latencies']),
                'p99_latency': sorted(chaos['latencies'])[int(len(chaos['latencies']) * 0.99)]
            },
            'degradation': {
                'success_rate_drop': (baseline['successful_requests'] / baseline['total_requests']) -
                                      (chaos['successful_requests'] / chaos['total_requests']),
                'latency_increase': (sum(chaos['latencies']) / len(chaos['latencies'])) -
                                     (sum(baseline['latencies']) / len(baseline['latencies']))
            }
        }
```

---

Continúa en siguiente sección...

---

## Resumen Security y Performance

| Tema | Dificultad | Complejidad | Impacto | Prioridad |
|------|------------|-------------|---------|-----------|
| OAuth2 / OIDC | 5 | 5 | 5 | **CRÍTICA** |
| mTLS | 5 | 5 | 4 | **ALTA** |
| API Key Management | 4 | 4 | 5 | **CRÍTICA** |
| Chaos Engineering | 5 | 5 | 4 | **ALTA** |
| JWT Rotation | 4 | 4 | 5 | **CRÍTICA** |
| Certificate Management | 5 | 5 | 4 | **ALTA** |

**El siguiente archivo continuará con:**
- Performance optimization (database indexing, query optimization)
- Monitoring y Alerting (Prometheus, Grafana)
- Database optimization (connection pooling, prepared statements)
- Profiling y debugging en producción
- Backup y Disaster Recovery
