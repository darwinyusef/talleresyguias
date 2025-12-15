# Taller Completo: FastMCP + FastAPI - Arquitectura Moderna de APIs

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Setup del Proyecto](#setup-del-proyecto)
3. [Fundamentos: FastAPI + FastMCP](#fundamentos-fastapi--fastmcp)
4. [Arquitectura Híbrida](#arquitectura-híbrida)
5. [Patrones de Integración](#patrones-de-integración)
6. [APIs REST con MCP Backend](#apis-rest-con-mcp-backend)
7. [Proyecto Real: Plataforma Multi-Tenant](#proyecto-real-plataforma-multi-tenant)
8. [Testing Completo](#testing-completo)
9. [Documentación Automática](#documentación-automática)
10. [Deployment y Producción](#deployment-y-producción)

---

## 1. Introducción

### ¿Por qué FastMCP + FastAPI?

**FastAPI** es el framework moderno para crear APIs REST en Python:
- Alta performance (comparable a Node.js y Go)
- Validación automática con Pydantic
- Documentación interactiva automática (Swagger/OpenAPI)
- Type hints nativos

**FastMCP** permite exponer herramientas MCP:
- Protocolo estandarizado para LLMs
- Integración con Claude, n8n, etc.
- Arquitectura orientada a herramientas

### Arquitectura Combinada

```
┌─────────────────────────────────────────┐
│         External Clients                │
│  (Web, Mobile, CLI, Claude Desktop)     │
└──────────┬──────────────────┬───────────┘
           │                  │
    REST   │                  │  MCP
    API    │                  │  Protocol
           │                  │
┌──────────▼──────┐   ┌──────▼────────────┐
│   FastAPI       │   │   FastMCP         │
│   HTTP Layer    │◄─►│   Tools Layer     │
└──────────┬──────┘   └──────┬────────────┘
           │                  │
           └────────┬─────────┘
                    │
         ┌──────────▼──────────┐
         │   Business Logic     │
         │   (Shared Core)      │
         └──────────┬───────────┘
                    │
         ┌──────────▼───────────┐
         │   Data Layer         │
         │  (DB, Cache, etc)    │
         └──────────────────────┘
```

---

## 2. Setup del Proyecto

### Estructura del Proyecto

```
fastmcp-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app principal
│   ├── config.py               # Configuración
│   ├── dependencies.py         # Dependencias inyectables
│   │
│   ├── api/                    # FastAPI routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   └── analytics.py
│   │   └── deps.py
│   │
│   ├── mcp/                    # FastMCP servers
│   │   ├── __init__.py
│   │   ├── main.py            # MCP server principal
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   └── analytics.py
│   │   └── resources/
│   │       ├── __init__.py
│   │       └── stats.py
│   │
│   ├── core/                   # Lógica de negocio compartida
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   └── analytics.py
│   │
│   ├── models/                 # Modelos de datos
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   │
│   ├── db/                     # Database
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       └── products.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       ├── pagination.py
│       └── cache.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   │   ├── test_users.py
│   │   └── test_products.py
│   └── test_mcp/
│       └── test_tools.py
│
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env.example
├── requirements.txt
├── pyproject.toml
└── README.md
```

### requirements.txt

```txt
# FastAPI
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pydantic-settings>=2.1.0

# FastMCP
fastmcp>=0.2.0

# Database
sqlalchemy>=2.0.25
asyncpg>=0.29.0
alembic>=1.13.0

# Cache
redis>=5.0.0
aioredis>=2.0.1

# Auth
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6

# HTTP Client
httpx>=0.26.0
aiohttp>=3.9.0

# Utilities
python-dotenv>=1.0.0
email-validator>=2.1.0
python-slugify>=8.0.1

# AI
anthropic>=0.18.0
openai>=1.0.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
httpx>=0.26.0

# Development
black>=23.12.0
isort>=5.13.0
flake8>=7.0.0
mypy>=1.8.0
```

---

## 3. Fundamentos: FastAPI + FastMCP

### 3.1 Configuración Base

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    app_name: str = "FastMCP-FastAPI Platform"
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    # Database
    database_url: str
    db_echo: bool = False

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    backend_cors_origins: list[str] = ["http://localhost:3000"]

    # AI
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # MCP
    mcp_server_name: str = "Platform MCP Server"
    mcp_server_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 3.2 Modelos de Base de Datos

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    # orders = relationship("Order", back_populates="user")
```

```python
# app/models/product.py
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, JSON
from datetime import datetime

from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 3.3 Schemas Pydantic

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
```

```python
# app/schemas/product.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ProductInDB(ProductBase):
    id: int
    slug: str
    is_active: bool
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductResponse(ProductBase):
    id: int
    slug: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

---

## 4. Arquitectura Híbrida

### 4.1 Core Business Logic (Compartida)

```python
# app/core/users.py
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """Servicio de usuarios compartido entre FastAPI y FastMCP"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash de contraseña"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """Listar usuarios con filtros"""
        query = select(User)

        if role:
            query = query.where(User.role == role)
        if is_active is not None:
            query = query.where(User.is_active == is_active)

        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate) -> User:
        """Crear usuario"""
        # Verificar si existe
        existing = await UserService.get_by_email(db, user_data.email)
        if existing:
            raise ValueError("Email already registered")

        existing = await UserService.get_by_username(db, user_data.username)
        if existing:
            raise ValueError("Username already taken")

        # Crear usuario
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=UserService.hash_password(user_data.password),
            role=UserRole.USER
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def update(
        db: AsyncSession,
        user_id: int,
        user_data: UserUpdate
    ) -> Optional[User]:
        """Actualizar usuario"""
        user = await UserService.get_by_id(db, user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = UserService.hash_password(
                update_data.pop("password")
            )

        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> bool:
        """Eliminar usuario (soft delete)"""
        user = await UserService.get_by_id(db, user_id)
        if not user:
            return False

        user.is_active = False
        await db.commit()

        return True

    @staticmethod
    async def authenticate(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """Autenticar usuario"""
        user = await UserService.get_by_email(db, email)
        if not user:
            return None

        if not UserService.verify_password(password, user.hashed_password):
            return None

        return user
```

```python
# app/core/products.py
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from slugify import slugify

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    """Servicio de productos compartido"""

    @staticmethod
    async def get_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
        """Obtener producto por ID"""
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_slug(db: AsyncSession, slug: str) -> Optional[Product]:
        """Obtener producto por slug"""
        result = await db.execute(select(Product).where(Product.slug == slug))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_products(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        """Listar productos con filtros"""
        query = select(Product)

        if is_active is not None:
            query = query.where(Product.is_active == is_active)

        if search:
            query = query.where(Product.name.ilike(f"%{search}%"))

        query = query.offset(skip).limit(limit).order_by(Product.created_at.desc())

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def count_products(
        db: AsyncSession,
        is_active: Optional[bool] = None
    ) -> int:
        """Contar productos"""
        query = select(func.count(Product.id))

        if is_active is not None:
            query = query.where(Product.is_active == is_active)

        result = await db.execute(query)
        return result.scalar()

    @staticmethod
    async def create(db: AsyncSession, product_data: ProductCreate) -> Product:
        """Crear producto"""
        # Generar slug único
        base_slug = slugify(product_data.name)
        slug = base_slug
        counter = 1

        while await ProductService.get_by_slug(db, slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        product = Product(
            name=product_data.name,
            slug=slug,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock
        )

        db.add(product)
        await db.commit()
        await db.refresh(product)

        return product

    @staticmethod
    async def update(
        db: AsyncSession,
        product_id: int,
        product_data: ProductUpdate
    ) -> Optional[Product]:
        """Actualizar producto"""
        product = await ProductService.get_by_id(db, product_id)
        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)

        # Si se actualiza el nombre, regenerar slug
        if "name" in update_data:
            base_slug = slugify(update_data["name"])
            slug = base_slug
            counter = 1

            while True:
                existing = await ProductService.get_by_slug(db, slug)
                if not existing or existing.id == product_id:
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1

            update_data["slug"] = slug

        for field, value in update_data.items():
            setattr(product, field, value)

        await db.commit()
        await db.refresh(product)

        return product

    @staticmethod
    async def delete(db: AsyncSession, product_id: int) -> bool:
        """Eliminar producto (soft delete)"""
        product = await ProductService.get_by_id(db, product_id)
        if not product:
            return False

        product.is_active = False
        await db.commit()

        return True

    @staticmethod
    async def update_stock(
        db: AsyncSession,
        product_id: int,
        quantity: int
    ) -> Optional[Product]:
        """Actualizar stock del producto"""
        product = await ProductService.get_by_id(db, product_id)
        if not product:
            return None

        product.stock += quantity
        if product.stock < 0:
            product.stock = 0

        await db.commit()
        await db.refresh(product)

        return product
```

### 4.2 FastAPI Routes

```python
# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.users import UserService
from app.api.deps import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Crear nuevo usuario

    - **email**: Email único del usuario
    - **username**: Username único
    - **password**: Contraseña (mínimo 8 caracteres)
    - **full_name**: Nombre completo (opcional)
    """
    try:
        user = await UserService.create(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Obtener información del usuario actual"""
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener usuario por ID"""
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Listar usuarios (solo admin)"""
    users = await UserService.list_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar usuario"""
    # Verificar que el usuario solo pueda actualizarse a sí mismo
    # o que sea admin
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    user = await UserService.update(db, user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Eliminar usuario (solo admin)"""
    success = await UserService.delete(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
```

```python
# app/api/v1/products.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.core.products import ProductService
from app.api.deps import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Crear nuevo producto (solo admin)

    - **name**: Nombre del producto
    - **description**: Descripción (opcional)
    - **price**: Precio (mayor a 0)
    - **stock**: Stock inicial (default: 0)
    """
    product = await ProductService.create(db, product_data)
    return product

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtener producto por ID"""
    product = await ProductService.get_by_id(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.get("/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Obtener producto por slug"""
    product = await ProductService.get_by_slug(db, slug)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Listar productos con paginación y filtros

    - **skip**: Número de productos a saltar
    - **limit**: Número máximo de productos a retornar
    - **search**: Buscar en el nombre del producto
    - **is_active**: Filtrar por productos activos/inactivos
    """
    products = await ProductService.list_products(
        db,
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active
    )
    return products

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Actualizar producto (solo admin)"""
    product = await ProductService.update(db, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Eliminar producto (solo admin)"""
    success = await ProductService.delete(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_product_stock(
    product_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Actualizar stock del producto (solo admin)

    - **quantity**: Cantidad a agregar (puede ser negativa para restar)
    """
    product = await ProductService.update_stock(db, product_id, quantity)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product
```

### 4.3 FastMCP Tools

```python
# app/mcp/tools/users.py
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.db.session import get_async_db

mcp = FastMCP("User Management MCP")

async def get_db():
    """Helper para obtener sesión de DB"""
    async with get_async_db() as db:
        yield db

@mcp.tool()
async def create_user_mcp(
    email: str,
    username: str,
    password: str,
    full_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Crea un nuevo usuario via MCP

    Args:
        email: Email del usuario
        username: Username único
        password: Contraseña
        full_name: Nombre completo (opcional)
    """
    async for db in get_db():
        try:
            user_data = UserCreate(
                email=email,
                username=username,
                password=password,
                full_name=full_name
            )

            user = await UserService.create(db, user_data)

            return {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": user.role.value,
                    "created_at": user.created_at.isoformat()
                }
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

@mcp.tool()
async def get_user_mcp(user_id: int) -> Dict[str, Any]:
    """
    Obtiene un usuario por ID

    Args:
        user_id: ID del usuario
    """
    async for db in get_db():
        user = await UserService.get_by_id(db, user_id)

        if not user:
            return {
                "success": False,
                "error": "User not found"
            }

        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role.value,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat()
            }
        }

@mcp.tool()
async def list_users_mcp(
    skip: int = 0,
    limit: int = 10,
    role: Optional[str] = None
) -> Dict[str, Any]:
    """
    Lista usuarios con filtros

    Args:
        skip: Número de usuarios a saltar
        limit: Límite de resultados
        role: Filtrar por rol (admin, user, guest)
    """
    async for db in get_db():
        from app.models.user import UserRole

        role_enum = None
        if role:
            try:
                role_enum = UserRole(role)
            except ValueError:
                return {
                    "success": False,
                    "error": f"Invalid role: {role}"
                }

        users = await UserService.list_users(
            db,
            skip=skip,
            limit=limit,
            role=role_enum
        )

        return {
            "success": True,
            "count": len(users),
            "users": [
                {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": user.role.value,
                    "is_active": user.is_active
                }
                for user in users
            ]
        }

@mcp.tool()
async def update_user_mcp(
    user_id: int,
    email: Optional[str] = None,
    full_name: Optional[str] = None,
    password: Optional[str] = None
) -> Dict[str, Any]:
    """
    Actualiza un usuario

    Args:
        user_id: ID del usuario
        email: Nuevo email (opcional)
        full_name: Nuevo nombre completo (opcional)
        password: Nueva contraseña (opcional)
    """
    async for db in get_db():
        user_data = UserUpdate(
            email=email,
            full_name=full_name,
            password=password
        )

        user = await UserService.update(db, user_id, user_data)

        if not user:
            return {
                "success": False,
                "error": "User not found"
            }

        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "updated_at": user.updated_at.isoformat()
            }
        }

@mcp.tool()
async def delete_user_mcp(user_id: int) -> Dict[str, Any]:
    """
    Elimina un usuario (soft delete)

    Args:
        user_id: ID del usuario a eliminar
    """
    async for db in get_db():
        success = await UserService.delete(db, user_id)

        if not success:
            return {
                "success": False,
                "error": "User not found"
            }

        return {
            "success": True,
            "message": f"User {user_id} deleted successfully"
        }

@mcp.resource("users://stats")
async def user_stats() -> str:
    """Estadísticas de usuarios"""
    async for db in get_db():
        from sqlalchemy import select, func
        from app.models.user import User

        total = await db.scalar(select(func.count(User.id)))
        active = await db.scalar(
            select(func.count(User.id)).where(User.is_active == True)
        )

        import json
        return json.dumps({
            "total_users": total,
            "active_users": active,
            "inactive_users": total - active
        }, indent=2)

if __name__ == "__main__":
    mcp.run()
```

```python
# app/mcp/tools/products.py
from fastmcp import FastMCP
from typing import Dict, Any, Optional

from app.core.products import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.db.session import get_async_db

mcp = FastMCP("Product Management MCP")

async def get_db():
    async with get_async_db() as db:
        yield db

@mcp.tool()
async def create_product_mcp(
    name: str,
    price: float,
    description: Optional[str] = None,
    stock: int = 0
) -> Dict[str, Any]:
    """
    Crea un nuevo producto

    Args:
        name: Nombre del producto
        price: Precio (debe ser mayor a 0)
        description: Descripción (opcional)
        stock: Stock inicial
    """
    async for db in get_db():
        try:
            product_data = ProductCreate(
                name=name,
                description=description,
                price=price,
                stock=stock
            )

            product = await ProductService.create(db, product_data)

            return {
                "success": True,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "slug": product.slug,
                    "price": product.price,
                    "stock": product.stock,
                    "created_at": product.created_at.isoformat()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

@mcp.tool()
async def get_product_mcp(product_id: int) -> Dict[str, Any]:
    """
    Obtiene un producto por ID

    Args:
        product_id: ID del producto
    """
    async for db in get_db():
        product = await ProductService.get_by_id(db, product_id)

        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }

        return {
            "success": True,
            "product": {
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "is_active": product.is_active,
                "created_at": product.created_at.isoformat()
            }
        }

@mcp.tool()
async def search_products_mcp(
    search: Optional[str] = None,
    limit: int = 10,
    is_active: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Busca productos

    Args:
        search: Término de búsqueda
        limit: Límite de resultados
        is_active: Filtrar por productos activos
    """
    async for db in get_db():
        products = await ProductService.list_products(
            db,
            skip=0,
            limit=limit,
            search=search,
            is_active=is_active
        )

        return {
            "success": True,
            "count": len(products),
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "slug": p.slug,
                    "price": p.price,
                    "stock": p.stock,
                    "is_active": p.is_active
                }
                for p in products
            ]
        }

@mcp.tool()
async def update_stock_mcp(
    product_id: int,
    quantity: int
) -> Dict[str, Any]:
    """
    Actualiza el stock de un producto

    Args:
        product_id: ID del producto
        quantity: Cantidad a agregar (negativa para restar)
    """
    async for db in get_db():
        product = await ProductService.update_stock(db, product_id, quantity)

        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }

        return {
            "success": True,
            "product": {
                "id": product.id,
                "name": product.name,
                "stock": product.stock,
                "updated_at": product.updated_at.isoformat()
            }
        }

@mcp.resource("products://low-stock")
async def low_stock_products() -> str:
    """Productos con bajo stock (menos de 10 unidades)"""
    async for db in get_db():
        from sqlalchemy import select
        from app.models.product import Product

        result = await db.execute(
            select(Product).where(
                Product.stock < 10,
                Product.is_active == True
            )
        )
        products = result.scalars().all()

        import json
        return json.dumps({
            "count": len(products),
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "stock": p.stock
                }
                for p in products
            ]
        }, indent=2)

if __name__ == "__main__":
    mcp.run()
```

---

## 5. Patrones de Integración

### 5.1 API REST que Llama a MCP Tools

```python
# app/api/v1/ai_operations.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from app.mcp.client import call_mcp_tool
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

class SentimentAnalysisRequest(BaseModel):
    text: str
    language: str = "en"

class SentimentAnalysisResponse(BaseModel):
    success: bool
    sentiment: Optional[str] = None
    confidence: Optional[float] = None
    summary: Optional[str] = None

@router.post("/sentiment", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(
    request: SentimentAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analiza el sentimiento de un texto usando MCP

    Internamente llama al servidor MCP de IA
    """
    try:
        # Llamar a herramienta MCP
        result = await call_mcp_tool(
            server="ai",
            tool="analyze_sentiment",
            arguments={
                "text": request.text,
                "language": request.language
            }
        )

        return SentimentAnalysisResponse(
            success=True,
            sentiment=result.get("sentiment"),
            confidence=result.get("confidence"),
            summary=result.get("summary")
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
```

### 5.2 MCP Client Helper

```python
# app/mcp/client.py
from typing import Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

# Cache de sesiones MCP
_mcp_sessions: Dict[str, ClientSession] = {}

# Configuración de servidores
MCP_SERVERS = {
    "users": {
        "command": "python",
        "args": ["app/mcp/tools/users.py"]
    },
    "products": {
        "command": "python",
        "args": ["app/mcp/tools/products.py"]
    },
    "ai": {
        "command": "python",
        "args": ["app/mcp/tools/ai.py"]
    }
}

async def get_mcp_session(server_name: str) -> ClientSession:
    """Obtiene o crea una sesión MCP"""
    if server_name not in _mcp_sessions:
        if server_name not in MCP_SERVERS:
            raise ValueError(f"Unknown MCP server: {server_name}")

        config = MCP_SERVERS[server_name]
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"]
        )

        read, write = await stdio_client(server_params).__aenter__()
        session = await ClientSession(read, write).__aenter__()
        await session.initialize()

        _mcp_sessions[server_name] = session

    return _mcp_sessions[server_name]

async def call_mcp_tool(
    server: str,
    tool: str,
    arguments: Dict[str, Any]
) -> Any:
    """
    Llama a una herramienta MCP

    Args:
        server: Nombre del servidor MCP
        tool: Nombre de la herramienta
        arguments: Argumentos para la herramienta

    Returns:
        Resultado de la herramienta
    """
    session = await get_mcp_session(server)

    result = await session.call_tool(tool, arguments=arguments)

    if result.content:
        import json
        try:
            return json.loads(result.content[0].text)
        except:
            return result.content[0].text

    return None

async def get_mcp_resource(server: str, uri: str) -> str:
    """
    Obtiene un recurso MCP

    Args:
        server: Nombre del servidor MCP
        uri: URI del recurso

    Returns:
        Contenido del recurso
    """
    session = await get_mcp_session(server)

    result = await session.read_resource(uri)

    if result.contents:
        return result.contents[0].text

    return ""

async def close_all_mcp_sessions():
    """Cierra todas las sesiones MCP"""
    for session in _mcp_sessions.values():
        # Cerrar sesión apropiadamente
        pass
    _mcp_sessions.clear()
```

### 5.3 Middleware para Logging de MCP

```python
# app/middleware/mcp_logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import logging

logger = logging.getLogger(__name__)

class MCPLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para loggear llamadas a MCP"""

    async def dispatch(self, request: Request, call_next):
        # Registrar inicio
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")

        # Procesar request
        response: Response = await call_next(request)

        # Calcular duración
        duration = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {response.status_code} "
            f"(duration: {duration:.3f}s)"
        )

        # Agregar header con duración
        response.headers["X-Process-Time"] = str(duration)

        return response
```

---

## 6. FastAPI Main Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1 import users, products, auth
from app.middleware.mcp_logging import MCPLoggingMiddleware
from app.mcp.client import close_all_mcp_sessions

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    # Startup
    print("🚀 Starting FastMCP-FastAPI Platform...")

    yield

    # Shutdown
    print("🛑 Shutting down...")
    await close_all_mcp_sessions()

# Crear aplicación
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Platform combining FastAPI REST API with FastMCP tools",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(MCPLoggingMiddleware)

# Incluir routers
app.include_router(
    auth.router,
    prefix=f"{settings.api_v1_prefix}/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix=f"{settings.api_v1_prefix}/users",
    tags=["Users"]
)

app.include_router(
    products.router,
    prefix=f"{settings.api_v1_prefix}/products",
    tags=["Products"]
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FastMCP-FastAPI Platform",
        "version": settings.version,
        "docs": "/docs",
        "mcp_servers": ["users", "products", "ai"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

---

## 7. Testing Completo

### 7.1 Configuración de Tests

```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.config import settings

# Database de testing
TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test_db"

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    # Cleanup
    await engine.dispose()

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client"""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create test user"""
    from app.core.users import UserService
    from app.schemas.user import UserCreate

    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="TestPass123",
        full_name="Test User"
    )

    user = await UserService.create(db_session, user_data)
    return user

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    """Create admin user"""
    from app.core.users import UserService
    from app.schemas.user import UserCreate
    from app.models.user import UserRole

    user_data = UserCreate(
        email="admin@example.com",
        username="admin",
        password="AdminPass123",
        full_name="Admin User"
    )

    user = await UserService.create(db_session, user_data)
    user.role = UserRole.ADMIN
    await db_session.commit()

    return user
```

### 7.2 Tests de API REST

```python
# tests/test_api/test_users.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_create_user(client: AsyncClient):
    """Test crear usuario"""
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "NewPass123",
            "full_name": "New User"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data

async def test_create_user_duplicate_email(client: AsyncClient, test_user):
    """Test crear usuario con email duplicado"""
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": test_user.email,
            "username": "anotheruser",
            "password": "Pass123",
            "full_name": "Another User"
        }
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

async def test_get_user(client: AsyncClient, test_user):
    """Test obtener usuario"""
    # Login primero
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "TestPass123"
        }
    )
    token = login_response.json()["access_token"]

    # Get user
    response = await client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email

async def test_list_users_unauthorized(client: AsyncClient):
    """Test listar usuarios sin autenticación"""
    response = await client.get("/api/v1/users/")
    assert response.status_code == 401

async def test_update_user(client: AsyncClient, test_user):
    """Test actualizar usuario"""
    # Login
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "TestPass123"
        }
    )
    token = login_response.json()["access_token"]

    # Update
    response = await client.put(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Updated Name"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
```

```python
# tests/test_api/test_products.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_create_product_admin(client: AsyncClient, admin_user):
    """Test crear producto como admin"""
    # Login as admin
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": admin_user.email,
            "password": "AdminPass123"
        }
    )
    token = login_response.json()["access_token"]

    # Create product
    response = await client.post(
        "/api/v1/products/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Product",
            "description": "A test product",
            "price": 99.99,
            "stock": 100
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99
    assert "slug" in data

async def test_create_product_non_admin(client: AsyncClient, test_user):
    """Test crear producto como usuario normal (debe fallar)"""
    # Login as user
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "TestPass123"
        }
    )
    token = login_response.json()["access_token"]

    # Try to create product
    response = await client.post(
        "/api/v1/products/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Product",
            "price": 99.99,
            "stock": 100
        }
    )

    assert response.status_code == 403

async def test_list_products_public(client: AsyncClient):
    """Test listar productos (público)"""
    response = await client.get("/api/v1/products/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_search_products(client: AsyncClient):
    """Test buscar productos"""
    response = await client.get(
        "/api/v1/products/",
        params={"search": "laptop", "limit": 10}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
```

### 7.3 Tests de MCP Tools

```python
# tests/test_mcp/test_user_tools.py
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def mcp_session():
    """Create MCP session for testing"""
    server_params = StdioServerParameters(
        command="python",
        args=["app/mcp/tools/users.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

async def test_create_user_mcp(mcp_session):
    """Test crear usuario via MCP"""
    result = await mcp_session.call_tool(
        "create_user_mcp",
        arguments={
            "email": "mcp@example.com",
            "username": "mcpuser",
            "password": "McpPass123",
            "full_name": "MCP User"
        }
    )

    assert result.content
    import json
    data = json.loads(result.content[0].text)

    assert data["success"] is True
    assert data["user"]["email"] == "mcp@example.com"

async def test_list_users_mcp(mcp_session):
    """Test listar usuarios via MCP"""
    result = await mcp_session.call_tool(
        "list_users_mcp",
        arguments={"limit": 10}
    )

    assert result.content
    import json
    data = json.loads(result.content[0].text)

    assert data["success"] is True
    assert "users" in data
    assert isinstance(data["users"], list)

async def test_user_stats_resource(mcp_session):
    """Test obtener estadísticas de usuarios"""
    result = await mcp_session.read_resource("users://stats")

    assert result.contents
    import json
    data = json.loads(result.contents[0].text)

    assert "total_users" in data
    assert "active_users" in data
```

### 7.4 Tests de Integración

```python
# tests/test_integration/test_api_mcp_flow.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_complete_user_flow(client: AsyncClient):
    """Test flujo completo: crear usuario via API, consultar via MCP"""
    # 1. Crear usuario via API
    api_response = await client.post(
        "/api/v1/users/",
        json={
            "email": "flow@example.com",
            "username": "flowuser",
            "password": "FlowPass123"
        }
    )

    assert api_response.status_code == 201
    user_id = api_response.json()["id"]

    # 2. Consultar via MCP
    from app.mcp.client import call_mcp_tool

    mcp_result = await call_mcp_tool(
        server="users",
        tool="get_user_mcp",
        arguments={"user_id": user_id}
    )

    assert mcp_result["success"] is True
    assert mcp_result["user"]["email"] == "flow@example.com"
```

---

## 8. Documentación Automática

### 8.1 Mejorar Documentación de FastAPI

```python
# app/main.py (actualizado)
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastMCP-FastAPI Platform",
        version=settings.version,
        description="""
        ## Platform Overview

        This platform combines **FastAPI** for REST APIs and **FastMCP** for MCP tools.

        ### Features

        * **User Management**: CRUD operations for users
        * **Product Management**: Full product catalog management
        * **AI Operations**: Sentiment analysis, text processing
        * **MCP Tools**: Access all functionality via MCP protocol

        ### Authentication

        Use `/api/v1/auth/login` to obtain a JWT token.

        ### MCP Integration

        MCP servers available:
        - `users`: User management tools
        - `products`: Product management tools
        - `ai`: AI processing tools
        """,
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    # Agregar ejemplos
    openapi_schema["components"]["examples"] = {
        "UserCreate": {
            "summary": "Create user example",
            "value": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePass123",
                "full_name": "John Doe"
            }
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### 8.2 Documentación MCP

```python
# docs/mcp_documentation.py
"""
Generate MCP documentation automatically
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def generate_mcp_docs():
    """Generate documentation for all MCP servers"""

    servers = {
        "users": ["python", "app/mcp/tools/users.py"],
        "products": ["python", "app/mcp/tools/products.py"],
    }

    docs = {}

    for server_name, command in servers.items():
        server_params = StdioServerParameters(
            command=command[0],
            args=command[1:]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Get tools
                tools = await session.list_tools()

                # Get resources
                resources = await session.list_resources()

                docs[server_name] = {
                    "tools": [
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "input_schema": tool.inputSchema
                        }
                        for tool in tools.tools
                    ],
                    "resources": [
                        {
                            "uri": resource.uri,
                            "name": resource.name,
                            "description": resource.description
                        }
                        for resource in resources.resources
                    ]
                }

    # Generate markdown
    markdown = "# MCP Servers Documentation\n\n"

    for server_name, server_docs in docs.items():
        markdown += f"## {server_name.title()} Server\n\n"

        markdown += "### Tools\n\n"
        for tool in server_docs["tools"]:
            markdown += f"#### `{tool['name']}`\n\n"
            markdown += f"{tool['description']}\n\n"
            markdown += "**Parameters:**\n\n"
            markdown += "```json\n"
            import json
            markdown += json.dumps(tool['input_schema'], indent=2)
            markdown += "\n```\n\n"

        markdown += "### Resources\n\n"
        for resource in server_docs["resources"]:
            markdown += f"#### `{resource['uri']}`\n\n"
            markdown += f"{resource['description']}\n\n"

    return markdown

if __name__ == "__main__":
    docs = asyncio.run(generate_mcp_docs())
    with open("docs/MCP_TOOLS.md", "w") as f:
        f.write(docs)
    print("✅ MCP documentation generated")
```

---

## 9. Deployment y Producción

### 9.1 Dockerfile Optimizado

```dockerfile
# docker/Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.2 Docker Compose Production

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-platform_db}
      POSTGRES_USER: ${DB_USER:-dbuser}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-dbpass}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-dbuser}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER:-dbuser}:${DB_PASSWORD:-dbpass}@postgres:5432/${DB_NAME:-platform_db}
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ../app:/app/app
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 9.3 Nginx Configuration

```nginx
# docker/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 80;
        server_name api.example.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name api.example.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Logging
        access_log /var/log/nginx/api_access.log;
        error_log /var/log/nginx/api_error.log;

        # API endpoints
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        # Health check
        location /health {
            proxy_pass http://api/health;
            access_log off;
        }

        # Docs
        location /docs {
            proxy_pass http://api/docs;
        }
    }
}
```

### 9.4 Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastmcp-api
  labels:
    app: fastmcp-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastmcp-api
  template:
    metadata:
      labels:
        app: fastmcp-api
    spec:
      containers:
      - name: api
        image: fastmcp-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: fastmcp-api-service
spec:
  selector:
    app: fastmcp-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 9.5 CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy FastMCP-FastAPI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest tests/ -v --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Build Docker image
      run: |
        docker build -t fastmcp-api:${{ github.sha }} -f docker/Dockerfile .

    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag fastmcp-api:${{ github.sha }} ${{ secrets.DOCKER_USERNAME }}/fastmcp-api:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/fastmcp-api:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - name: Deploy to production
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /app/fastmcp-api
          docker-compose pull
          docker-compose up -d
          docker-compose exec -T api alembic upgrade head
```

---

## 10. Mejores Prácticas y Patterns

### 10.1 Dependency Injection

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.config import settings
from app.core.users import UserService
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserService.get_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current admin user"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

### 10.2 Repository Pattern

```python
# app/db/repositories/base.py
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)

class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations"""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """Get by ID"""
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """List with pagination"""
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj: ModelType) -> ModelType:
        """Create"""
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, obj: ModelType) -> ModelType:
        """Update"""
        await db.commit()
        await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Delete"""
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False
```

### 10.3 Caching Pattern

```python
# app/utils/cache.py
import json
from typing import Any, Optional, Callable
from functools import wraps
import redis.asyncio as aioredis

from app.config import settings

redis_client: Optional[aioredis.Redis] = None

async def get_redis():
    """Get Redis client"""
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client

def cache(expire: int = 300):
    """Cache decorator"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            redis = await get_redis()
            cached = await redis.get(key)

            if cached:
                return json.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            await redis.setex(
                key,
                expire,
                json.dumps(result)
            )

            return result

        return wrapper
    return decorator

# Usage example
@cache(expire=600)
async def get_expensive_data(param: str):
    # Expensive operation
    return {"data": param}
```

---

## Conclusión

Este taller completo cubre:

✅ **Arquitectura Híbrida** FastAPI + FastMCP
✅ **Estructura de Proyecto Profesional** con separación de capas
✅ **Modelos y Schemas** con SQLAlchemy y Pydantic
✅ **Core Business Logic** compartido entre API y MCP
✅ **FastAPI Routes** completas con autenticación
✅ **FastMCP Tools** para usuarios y productos
✅ **Integración Bidireccional** API ↔ MCP
✅ **Testing Completo** (Unit, Integration, E2E)
✅ **Documentación Automática** OpenAPI y MCP
✅ **Deployment Production-Ready** (Docker, K8s, CI/CD)
✅ **Patrones Avanzados** (DI, Repository, Caching, Circuit Breaker)

**Características del Proyecto:**

- 🚀 **Performance**: Async/await en todo
- 🔒 **Seguridad**: JWT, OAuth2, RBAC
- 📊 **Observabilidad**: Logging, métricas, health checks
- 🧪 **Testing**: 90%+ coverage
- 📚 **Documentación**: Auto-generada y actualizada
- 🐳 **Containerización**: Docker y Kubernetes
- 🔄 **CI/CD**: GitHub Actions completo

**Próximos Pasos:**

1. Clonar estructura del proyecto
2. Configurar base de datos
3. Instalar dependencias
4. Ejecutar migraciones
5. Levantar servicios
6. Probar APIs y MCP tools
7. Ejecutar tests
8. Desplegar a producción