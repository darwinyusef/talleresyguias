# Módulo 5: Test de Integración con Mocks (CRUD Completo)

## Introducción

En este módulo aprenderás a crear tests de integración para un sistema CRUD completo. Veremos cómo mockear bases de datos, crear tests para cada operación (Create, Read, Update, Delete) y cómo integrar todo el sistema.

## ¿Qué son los Tests de Integración?

Los tests de integración verifican que múltiples componentes funcionen correctamente juntos:
- Servicios + Base de datos
- Servicios + APIs
- Múltiples servicios interactuando

## Estructura del Proyecto CRUD

```
ejemplos/05-mocks-crud/
├── models/
│   └── usuario.py          # Modelo de datos
├── repositories/
│   └── usuario_repository.py  # Acceso a datos
├── services/
│   └── usuario_service.py     # Lógica de negocio
└── tests/
    ├── test_01_create.py
    ├── test_02_read.py
    ├── test_03_update.py
    ├── test_04_delete.py
    └── test_05_integracion_completa.py
```

## Paso 1: Modelo de Datos

**Archivo: ejemplos/05-mocks-crud/models/usuario.py**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    """Modelo de usuario"""
    id: Optional[int]
    nombre: str
    email: str
    edad: int
    activo: bool = True
    fecha_creacion: Optional[datetime] = None

    def __post_init__(self):
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now()

    def validar(self):
        """Valida los datos del usuario"""
        errores = []

        if not self.nombre or len(self.nombre) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres")

        if not self.email or "@" not in self.email:
            errores.append("El email es inválido")

        if self.edad < 0 or self.edad > 150:
            errores.append("La edad debe estar entre 0 y 150")

        if errores:
            raise ValueError("; ".join(errores))

        return True

    def to_dict(self):
        """Convierte el usuario a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "edad": self.edad,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
```

## Paso 2: Repositorio (Acceso a Datos)

**Archivo: ejemplos/05-mocks-crud/repositories/usuario_repository.py**
```python
from typing import List, Optional
from models.usuario import Usuario

class UsuarioRepository:
    """Repositorio para gestionar usuarios en la base de datos"""

    def __init__(self, db_connection):
        self.db = db_connection

    def crear(self, usuario: Usuario) -> Usuario:
        """Crea un nuevo usuario en la base de datos"""
        query = """
            INSERT INTO usuarios (nombre, email, edad, activo, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.db.execute(
            query,
            (usuario.nombre, usuario.email, usuario.edad,
             usuario.activo, usuario.fecha_creacion)
        )
        self.db.commit()

        usuario.id = cursor.lastrowid
        return usuario

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        query = "SELECT * FROM usuarios WHERE id = ?"
        cursor = self.db.execute(query, (usuario_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_usuario(row)

    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        query = "SELECT * FROM usuarios"
        cursor = self.db.execute(query)
        rows = cursor.fetchall()

        return [self._row_to_usuario(row) for row in rows]

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email"""
        query = "SELECT * FROM usuarios WHERE email = ?"
        cursor = self.db.execute(query, (email,))
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_usuario(row)

    def actualizar(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario existente"""
        query = """
            UPDATE usuarios
            SET nombre = ?, email = ?, edad = ?, activo = ?
            WHERE id = ?
        """
        self.db.execute(
            query,
            (usuario.nombre, usuario.email, usuario.edad,
             usuario.activo, usuario.id)
        )
        self.db.commit()
        return usuario

    def eliminar(self, usuario_id: int) -> bool:
        """Elimina un usuario"""
        query = "DELETE FROM usuarios WHERE id = ?"
        cursor = self.db.execute(query, (usuario_id,))
        self.db.commit()
        return cursor.rowcount > 0

    def contar(self) -> int:
        """Cuenta el número total de usuarios"""
        query = "SELECT COUNT(*) FROM usuarios"
        cursor = self.db.execute(query)
        return cursor.fetchone()[0]

    def _row_to_usuario(self, row) -> Usuario:
        """Convierte una fila de BD a objeto Usuario"""
        from datetime import datetime
        return Usuario(
            id=row[0],
            nombre=row[1],
            email=row[2],
            edad=row[3],
            activo=bool(row[4]),
            fecha_creacion=datetime.fromisoformat(row[5]) if row[5] else None
        )
```

## Paso 3: Servicio (Lógica de Negocio)

**Archivo: ejemplos/05-mocks-crud/services/usuario_service.py**
```python
from typing import List, Optional
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    """Servicio de lógica de negocio para usuarios"""

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def crear_usuario(self, nombre: str, email: str, edad: int) -> Usuario:
        """Crea un nuevo usuario"""
        # Validar que no exista el email
        usuario_existente = self.repository.obtener_por_email(email)
        if usuario_existente:
            raise ValueError(f"Ya existe un usuario con el email {email}")

        # Crear y validar usuario
        usuario = Usuario(id=None, nombre=nombre, email=email, edad=edad)
        usuario.validar()

        # Guardar en BD
        return self.repository.crear(usuario)

    def obtener_usuario(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por ID"""
        if usuario_id <= 0:
            raise ValueError("ID de usuario inválido")

        return self.repository.obtener_por_id(usuario_id)

    def listar_usuarios(self, solo_activos: bool = False) -> List[Usuario]:
        """Lista todos los usuarios"""
        usuarios = self.repository.obtener_todos()

        if solo_activos:
            usuarios = [u for u in usuarios if u.activo]

        return usuarios

    def actualizar_usuario(self, usuario_id: int, **kwargs) -> Usuario:
        """Actualiza un usuario"""
        usuario = self.repository.obtener_por_id(usuario_id)

        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado")

        # Actualizar campos
        if "nombre" in kwargs:
            usuario.nombre = kwargs["nombre"]
        if "email" in kwargs:
            # Verificar que el nuevo email no exista
            if kwargs["email"] != usuario.email:
                existente = self.repository.obtener_por_email(kwargs["email"])
                if existente and existente.id != usuario_id:
                    raise ValueError(f"El email {kwargs['email']} ya está en uso")
            usuario.email = kwargs["email"]
        if "edad" in kwargs:
            usuario.edad = kwargs["edad"]
        if "activo" in kwargs:
            usuario.activo = kwargs["activo"]

        # Validar y guardar
        usuario.validar()
        return self.repository.actualizar(usuario)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        """Elimina un usuario"""
        usuario = self.repository.obtener_por_id(usuario_id)

        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado")

        return self.repository.eliminar(usuario_id)

    def desactivar_usuario(self, usuario_id: int) -> Usuario:
        """Desactiva un usuario (soft delete)"""
        return self.actualizar_usuario(usuario_id, activo=False)

    def buscar_por_nombre(self, termino: str) -> List[Usuario]:
        """Busca usuarios por nombre"""
        todos = self.repository.obtener_todos()
        return [u for u in todos if termino.lower() in u.nombre.lower()]

    def obtener_estadisticas(self) -> dict:
        """Obtiene estadísticas de usuarios"""
        todos = self.repository.obtener_todos()
        activos = [u for u in todos if u.activo]

        return {
            "total": len(todos),
            "activos": len(activos),
            "inactivos": len(todos) - len(activos),
            "edad_promedio": sum(u.edad for u in todos) / len(todos) if todos else 0
        }
```

## Test 1: CREATE - Crear Usuarios

**Archivo: ejemplos/05-mocks-crud/tests/test_01_create.py**
```python
import pytest
from unittest.mock import Mock, MagicMock
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

class TestCreateUsuario:
    """Tests para la operación CREATE"""

    @pytest.fixture
    def mock_db(self):
        """Mock de la conexión a base de datos"""
        db = Mock()
        cursor = Mock()
        cursor.lastrowid = 1
        db.execute.return_value = cursor
        return db

    @pytest.fixture
    def repository(self, mock_db):
        """Repositorio con DB mockeada"""
        return UsuarioRepository(mock_db)

    @pytest.fixture
    def service(self, repository):
        """Servicio con repositorio mockeado"""
        return UsuarioService(repository)

    def test_crear_usuario_exitoso(self, service, repository):
        """Test: crear un usuario válido"""
        # Mockear que no existe usuario con ese email
        repository.obtener_por_email = Mock(return_value=None)

        usuario = service.crear_usuario("Juan Pérez", "juan@email.com", 25)

        assert usuario.id == 1
        assert usuario.nombre == "Juan Pérez"
        assert usuario.email == "juan@email.com"
        assert usuario.edad == 25
        assert usuario.activo == True

    def test_crear_usuario_email_duplicado(self, service, repository):
        """Test: no permitir emails duplicados"""
        # Mockear que ya existe un usuario con ese email
        usuario_existente = Usuario(1, "Otro", "juan@email.com", 30)
        repository.obtener_por_email = Mock(return_value=usuario_existente)

        with pytest.raises(ValueError, match="Ya existe un usuario"):
            service.crear_usuario("Juan", "juan@email.com", 25)

    def test_crear_usuario_nombre_invalido(self, service, repository):
        """Test: validar nombre mínimo"""
        repository.obtener_por_email = Mock(return_value=None)

        with pytest.raises(ValueError, match="al menos 2 caracteres"):
            service.crear_usuario("J", "juan@email.com", 25)

    def test_crear_usuario_email_invalido(self, service, repository):
        """Test: validar formato de email"""
        repository.obtener_por_email = Mock(return_value=None)

        with pytest.raises(ValueError, match="email es inválido"):
            service.crear_usuario("Juan", "email-sin-arroba", 25)

    def test_crear_usuario_edad_invalida(self, service, repository):
        """Test: validar edad en rango válido"""
        repository.obtener_por_email = Mock(return_value=None)

        with pytest.raises(ValueError, match="edad debe estar"):
            service.crear_usuario("Juan", "juan@email.com", -5)

        with pytest.raises(ValueError, match="edad debe estar"):
            service.crear_usuario("Juan", "juan@email.com", 200)

    @pytest.mark.parametrize("nombre,email,edad", [
        ("Ana García", "ana@email.com", 22),
        ("Pedro López", "pedro@email.com", 45),
        ("María Rodríguez", "maria@email.com", 18),
    ])
    def test_crear_multiples_usuarios(self, service, repository, nombre, email, edad):
        """Test: crear varios usuarios válidos"""
        repository.obtener_por_email = Mock(return_value=None)

        usuario = service.crear_usuario(nombre, email, edad)

        assert usuario.nombre == nombre
        assert usuario.email == email
        assert usuario.edad == edad
```

## Test 2: READ - Leer Usuarios

**Archivo: ejemplos/05-mocks-crud/tests/test_02_read.py**
```python
import pytest
from unittest.mock import Mock
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

class TestReadUsuario:
    """Tests para la operación READ"""

    @pytest.fixture
    def usuarios_muestra(self):
        """Datos de prueba"""
        return [
            Usuario(1, "Juan", "juan@email.com", 25, activo=True),
            Usuario(2, "Ana", "ana@email.com", 30, activo=True),
            Usuario(3, "Pedro", "pedro@email.com", 35, activo=False),
        ]

    @pytest.fixture
    def mock_repository(self, usuarios_muestra):
        """Mock del repositorio"""
        repo = Mock(spec=UsuarioRepository)
        repo.obtener_todos.return_value = usuarios_muestra
        return repo

    @pytest.fixture
    def service(self, mock_repository):
        """Servicio con repositorio mockeado"""
        return UsuarioService(mock_repository)

    def test_obtener_usuario_por_id(self, service, mock_repository, usuarios_muestra):
        """Test: obtener un usuario por ID"""
        mock_repository.obtener_por_id.return_value = usuarios_muestra[0]

        usuario = service.obtener_usuario(1)

        assert usuario is not None
        assert usuario.id == 1
        assert usuario.nombre == "Juan"
        mock_repository.obtener_por_id.assert_called_once_with(1)

    def test_obtener_usuario_inexistente(self, service, mock_repository):
        """Test: obtener usuario que no existe"""
        mock_repository.obtener_por_id.return_value = None

        usuario = service.obtener_usuario(999)

        assert usuario is None

    def test_obtener_usuario_id_invalido(self, service):
        """Test: ID inválido"""
        with pytest.raises(ValueError, match="ID de usuario inválido"):
            service.obtener_usuario(0)

        with pytest.raises(ValueError, match="ID de usuario inválido"):
            service.obtener_usuario(-1)

    def test_listar_todos_usuarios(self, service, mock_repository, usuarios_muestra):
        """Test: listar todos los usuarios"""
        usuarios = service.listar_usuarios()

        assert len(usuarios) == 3
        mock_repository.obtener_todos.assert_called_once()

    def test_listar_solo_usuarios_activos(self, service, usuarios_muestra):
        """Test: filtrar solo usuarios activos"""
        usuarios = service.listar_usuarios(solo_activos=True)

        assert len(usuarios) == 2
        assert all(u.activo for u in usuarios)

    def test_buscar_por_nombre(self, service, usuarios_muestra):
        """Test: buscar usuarios por nombre"""
        resultados = service.buscar_por_nombre("Juan")

        assert len(resultados) == 1
        assert resultados[0].nombre == "Juan"

    def test_buscar_por_nombre_case_insensitive(self, service, usuarios_muestra):
        """Test: búsqueda insensible a mayúsculas"""
        resultados = service.buscar_por_nombre("juan")

        assert len(resultados) == 1

    def test_buscar_sin_resultados(self, service, usuarios_muestra):
        """Test: búsqueda sin resultados"""
        resultados = service.buscar_por_nombre("NoExiste")

        assert len(resultados) == 0

    def test_obtener_estadisticas(self, service, usuarios_muestra):
        """Test: obtener estadísticas de usuarios"""
        stats = service.obtener_estadisticas()

        assert stats["total"] == 3
        assert stats["activos"] == 2
        assert stats["inactivos"] == 1
        assert stats["edad_promedio"] == 30  # (25+30+35)/3
```

## Test 3: UPDATE - Actualizar Usuarios

**Archivo: ejemplos/05-mocks-crud/tests/test_03_update.py**
```python
import pytest
from unittest.mock import Mock
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

class TestUpdateUsuario:
    """Tests para la operación UPDATE"""

    @pytest.fixture
    def usuario_existente(self):
        """Usuario de prueba"""
        return Usuario(1, "Juan", "juan@email.com", 25, activo=True)

    @pytest.fixture
    def mock_repository(self, usuario_existente):
        """Mock del repositorio"""
        repo = Mock(spec=UsuarioRepository)
        repo.obtener_por_id.return_value = usuario_existente
        repo.actualizar.return_value = usuario_existente
        return repo

    @pytest.fixture
    def service(self, mock_repository):
        """Servicio con repositorio mockeado"""
        return UsuarioService(mock_repository)

    def test_actualizar_nombre(self, service, mock_repository, usuario_existente):
        """Test: actualizar solo el nombre"""
        mock_repository.obtener_por_email.return_value = None

        usuario = service.actualizar_usuario(1, nombre="Juan Carlos")

        assert usuario.nombre == "Juan Carlos"
        mock_repository.actualizar.assert_called_once()

    def test_actualizar_email(self, service, mock_repository, usuario_existente):
        """Test: actualizar email"""
        mock_repository.obtener_por_email.return_value = None

        usuario = service.actualizar_usuario(1, email="nuevo@email.com")

        assert usuario.email == "nuevo@email.com"

    def test_actualizar_email_duplicado(self, service, mock_repository):
        """Test: no permitir email duplicado al actualizar"""
        otro_usuario = Usuario(2, "Otro", "otro@email.com", 30)
        mock_repository.obtener_por_email.return_value = otro_usuario

        with pytest.raises(ValueError, match="ya está en uso"):
            service.actualizar_usuario(1, email="otro@email.com")

    def test_actualizar_edad(self, service, mock_repository, usuario_existente):
        """Test: actualizar edad"""
        mock_repository.obtener_por_email.return_value = None

        usuario = service.actualizar_usuario(1, edad=26)

        assert usuario.edad == 26

    def test_actualizar_edad_invalida(self, service, mock_repository):
        """Test: validar edad al actualizar"""
        mock_repository.obtener_por_email.return_value = None

        with pytest.raises(ValueError, match="edad debe estar"):
            service.actualizar_usuario(1, edad=-5)

    def test_actualizar_multiples_campos(self, service, mock_repository, usuario_existente):
        """Test: actualizar varios campos a la vez"""
        mock_repository.obtener_por_email.return_value = None

        usuario = service.actualizar_usuario(
            1,
            nombre="Juan Carlos",
            email="nuevo@email.com",
            edad=26
        )

        assert usuario.nombre == "Juan Carlos"
        assert usuario.email == "nuevo@email.com"
        assert usuario.edad == 26

    def test_actualizar_usuario_inexistente(self, service, mock_repository):
        """Test: actualizar usuario que no existe"""
        mock_repository.obtener_por_id.return_value = None

        with pytest.raises(ValueError, match="no encontrado"):
            service.actualizar_usuario(999, nombre="Nuevo Nombre")

    def test_desactivar_usuario(self, service, mock_repository, usuario_existente):
        """Test: desactivar usuario (soft delete)"""
        mock_repository.obtener_por_email.return_value = None

        usuario = service.desactivar_usuario(1)

        assert usuario.activo == False

    @pytest.mark.parametrize("campo,valor", [
        ("nombre", "Nombre Actualizado"),
        ("email", "actualizado@email.com"),
        ("edad", 30),
        ("activo", False),
    ])
    def test_actualizar_campos_individualmente(
        self, service, mock_repository, campo, valor
    ):
        """Test: actualizar cada campo individualmente"""
        mock_repository.obtener_por_email.return_value = None

        usuario = service.actualizar_usuario(1, **{campo: valor})

        assert getattr(usuario, campo) == valor
```

## Test 4: DELETE - Eliminar Usuarios

**Archivo: ejemplos/05-mocks-crud/tests/test_04_delete.py**
```python
import pytest
from unittest.mock import Mock
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

class TestDeleteUsuario:
    """Tests para la operación DELETE"""

    @pytest.fixture
    def usuario_existente(self):
        """Usuario de prueba"""
        return Usuario(1, "Juan", "juan@email.com", 25)

    @pytest.fixture
    def mock_repository(self, usuario_existente):
        """Mock del repositorio"""
        repo = Mock(spec=UsuarioRepository)
        repo.obtener_por_id.return_value = usuario_existente
        repo.eliminar.return_value = True
        return repo

    @pytest.fixture
    def service(self, mock_repository):
        """Servicio con repositorio mockeado"""
        return UsuarioService(mock_repository)

    def test_eliminar_usuario_exitoso(self, service, mock_repository):
        """Test: eliminar usuario existente"""
        resultado = service.eliminar_usuario(1)

        assert resultado == True
        mock_repository.eliminar.assert_called_once_with(1)

    def test_eliminar_usuario_inexistente(self, service, mock_repository):
        """Test: intentar eliminar usuario que no existe"""
        mock_repository.obtener_por_id.return_value = None

        with pytest.raises(ValueError, match="no encontrado"):
            service.eliminar_usuario(999)

    def test_eliminar_no_llama_db_si_no_existe(self, service, mock_repository):
        """Test: no llamar a BD si el usuario no existe"""
        mock_repository.obtener_por_id.return_value = None

        try:
            service.eliminar_usuario(999)
        except ValueError:
            pass

        mock_repository.eliminar.assert_not_called()

    def test_desactivar_usuario_vs_eliminar(self, service, mock_repository):
        """Test: desactivar es diferente de eliminar"""
        mock_repository.obtener_por_email.return_value = None

        # Desactivar
        usuario_desactivado = service.desactivar_usuario(1)
        assert usuario_desactivado.activo == False
        mock_repository.eliminar.assert_not_called()

        # Eliminar
        resultado = service.eliminar_usuario(1)
        assert resultado == True
        mock_repository.eliminar.assert_called_once()
```

## Test 5: Integración Completa

**Archivo: ejemplos/05-mocks-crud/tests/test_05_integracion_completa.py**
```python
import pytest
from unittest.mock import Mock, MagicMock
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService

class TestIntegracionCompleta:
    """Tests de integración del CRUD completo"""

    @pytest.fixture
    def usuarios_db(self):
        """Simula una base de datos en memoria"""
        return {}

    @pytest.fixture
    def mock_repository(self, usuarios_db):
        """Mock de repositorio con estado"""
        repo = Mock(spec=UsuarioRepository)
        id_counter = [1]  # Lista para poder modificar en closures

        def crear(usuario):
            usuario.id = id_counter[0]
            usuarios_db[usuario.id] = usuario
            id_counter[0] += 1
            return usuario

        def obtener_por_id(user_id):
            return usuarios_db.get(user_id)

        def obtener_por_email(email):
            for usuario in usuarios_db.values():
                if usuario.email == email:
                    return usuario
            return None

        def obtener_todos():
            return list(usuarios_db.values())

        def actualizar(usuario):
            usuarios_db[usuario.id] = usuario
            return usuario

        def eliminar(user_id):
            if user_id in usuarios_db:
                del usuarios_db[user_id]
                return True
            return False

        repo.crear.side_effect = crear
        repo.obtener_por_id.side_effect = obtener_por_id
        repo.obtener_por_email.side_effect = obtener_por_email
        repo.obtener_todos.side_effect = obtener_todos
        repo.actualizar.side_effect = actualizar
        repo.eliminar.side_effect = eliminar

        return repo

    @pytest.fixture
    def service(self, mock_repository):
        """Servicio con repositorio mockeado con estado"""
        return UsuarioService(mock_repository)

    def test_flujo_crud_completo(self, service):
        """Test: flujo completo de CRUD"""
        # 1. CREATE - Crear usuarios
        usuario1 = service.crear_usuario("Juan", "juan@email.com", 25)
        usuario2 = service.crear_usuario("Ana", "ana@email.com", 30)

        assert usuario1.id == 1
        assert usuario2.id == 2

        # 2. READ - Leer usuarios
        todos = service.listar_usuarios()
        assert len(todos) == 2

        usuario_obtenido = service.obtener_usuario(1)
        assert usuario_obtenido.nombre == "Juan"

        # 3. UPDATE - Actualizar usuario
        usuario_actualizado = service.actualizar_usuario(1, nombre="Juan Carlos", edad=26)
        assert usuario_actualizado.nombre == "Juan Carlos"
        assert usuario_actualizado.edad == 26

        # 4. DELETE - Eliminar usuario
        resultado = service.eliminar_usuario(2)
        assert resultado == True

        # Verificar que se eliminó
        todos = service.listar_usuarios()
        assert len(todos) == 1

    def test_flujo_con_validaciones(self, service):
        """Test: flujo completo con validaciones"""
        # Crear usuario
        usuario = service.crear_usuario("Juan", "juan@email.com", 25)

        # Intentar crear con email duplicado
        with pytest.raises(ValueError, match="Ya existe"):
            service.crear_usuario("Otro", "juan@email.com", 30)

        # Actualizar con email duplicado
        usuario2 = service.crear_usuario("Ana", "ana@email.com", 30)
        with pytest.raises(ValueError, match="ya está en uso"):
            service.actualizar_usuario(usuario2.id, email="juan@email.com")

    def test_operaciones_multiples_usuarios(self, service):
        """Test: operaciones con múltiples usuarios"""
        # Crear 5 usuarios
        for i in range(5):
            service.crear_usuario(
                f"Usuario{i}",
                f"usuario{i}@email.com",
                20 + i
            )

        # Verificar todos se crearon
        todos = service.listar_usuarios()
        assert len(todos) == 5

        # Desactivar algunos
        service.desactivar_usuario(1)
        service.desactivar_usuario(3)

        # Listar solo activos
        activos = service.listar_usuarios(solo_activos=True)
        assert len(activos) == 3

        # Obtener estadísticas
        stats = service.obtener_estadisticas()
        assert stats["total"] == 5
        assert stats["activos"] == 3
        assert stats["inactivos"] == 2

    def test_busqueda_y_filtrado(self, service):
        """Test: búsqueda y filtrado de usuarios"""
        # Crear usuarios
        service.crear_usuario("Juan Pérez", "juan@email.com", 25)
        service.crear_usuario("Ana López", "ana@email.com", 30)
        service.crear_usuario("Pedro Pérez", "pedro@email.com", 35)

        # Buscar por apellido
        resultados = service.buscar_por_nombre("Pérez")
        assert len(resultados) == 2

        # Buscar por nombre
        resultados = service.buscar_por_nombre("Ana")
        assert len(resultados) == 1

    def test_manejo_de_errores_en_cadena(self, service):
        """Test: manejo de errores en operaciones encadenadas"""
        # Crear usuario
        usuario = service.crear_usuario("Juan", "juan@email.com", 25)

        # Intentar actualizar con datos inválidos
        with pytest.raises(ValueError):
            service.actualizar_usuario(usuario.id, edad=-5)

        # Verificar que el usuario no cambió
        usuario_actual = service.obtener_usuario(usuario.id)
        assert usuario_actual.edad == 25  # No cambió

    def test_consistencia_de_datos(self, service):
        """Test: consistencia de datos después de operaciones"""
        # Crear usuario
        usuario = service.crear_usuario("Juan", "juan@email.com", 25)
        id_original = usuario.id

        # Actualizar varias veces
        service.actualizar_usuario(id_original, nombre="Juan Carlos")
        service.actualizar_usuario(id_original, edad=26)
        service.actualizar_usuario(id_original, email="nuevo@email.com")

        # Verificar que el ID no cambió y todos los campos están actualizados
        usuario_final = service.obtener_usuario(id_original)
        assert usuario_final.id == id_original
        assert usuario_final.nombre == "Juan Carlos"
        assert usuario_final.edad == 26
        assert usuario_final.email == "nuevo@email.com"
```

## Ejercicios Prácticos

### Ejercicio 1: CRUD de Productos

```markdown
Crea un sistema CRUD completo para productos:

Modelo: Producto (id, nombre, precio, stock, categoria)
Operaciones:
- Crear producto
- Buscar por categoría
- Actualizar stock
- Eliminar producto
- Obtener productos con bajo stock

Escribe tests de integración completos.
```

### Ejercicio 2: CRUD con Relaciones

```markdown
Crea un sistema de Pedidos con Productos:

Modelos:
- Pedido (id, cliente, fecha, total)
- ItemPedido (pedido_id, producto_id, cantidad, precio)

Operaciones:
- Crear pedido con items
- Actualizar items de pedido
- Calcular total
- Eliminar pedido (cascade)

Escribe tests de integración que verifiquen las relaciones.
```

### Ejercicio 3: CRUD con Transacciones

```markdown
Implementa un sistema bancario:

Modelo: Cuenta (id, titular, saldo)
Operaciones:
- Transferir entre cuentas (transaccional)
- Depósito
- Retiro
- Historial de movimientos

Escribe tests que verifiquen la integridad transaccional.
```

## Resumen

En este módulo aprendiste:

- Estructura de un sistema CRUD completo
- Testing de cada operación (Create, Read, Update, Delete)
- Mocking de bases de datos
- Tests de integración
- Flujos completos de negocio
- Validaciones y manejo de errores
- Consistencia de datos

## Próximos Pasos

En el siguiente módulo aprenderás sobre testing End-to-End con Cypress:
- Configuración de Cypress
- Testing de interfaces
- Integración frontend-backend
- Flujos completos de usuario

---

**[⬅️ Módulo anterior](04-test-unitarios-servicios.md) | [Volver al índice](../README.md) | [Siguiente: Módulo 6 - Test E2E con Cypress ➡️](06-test-e2e-cypress.md)**
