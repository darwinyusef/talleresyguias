# 🎓 Guía de Extensión de Tests

Esta guía te muestra cómo agregar nuevos tests y extender la suite existente.

## 📋 Tabla de Contenidos

1. [Agregar Tests Unitarios Simples](#1-agregar-tests-unitarios-simples)
2. [Agregar Tests con Mocks](#2-agregar-tests-con-mocks)
3. [Agregar Tests Asíncronos](#3-agregar-tests-asíncronos)
4. [Agregar Tests Parametrizados](#4-agregar-tests-parametrizados)
5. [Crear Fixtures Personalizadas](#5-crear-fixtures-personalizadas)
6. [Agregar Marcadores Personalizados](#6-agregar-marcadores-personalizados)
7. [Tests de Excepciones](#7-tests-de-excepciones)
8. [Tests de Integración](#8-tests-de-integración)

---

## 1. Agregar Tests Unitarios Simples

### Paso 1: Agregar función en `main.py`

```python
def multiplicar(a: int, b: int) -> int:
    """Multiplica dos números"""
    return a * b
```

### Paso 2: Agregar test en `test_main.py`

```python
class TestNuevasFunciones:
    """Tests para nuevas funciones"""
    
    def test_multiplicar_positivos(self):
        """Verifica multiplicación de números positivos"""
        assert multiplicar(3, 4) == 12
        assert multiplicar(5, 6) == 30
    
    def test_multiplicar_negativos(self):
        """Verifica multiplicación con negativos"""
        assert multiplicar(-2, 3) == -6
        assert multiplicar(-4, -5) == 20
    
    def test_multiplicar_por_cero(self):
        """Verifica multiplicación por cero"""
        assert multiplicar(5, 0) == 0
        assert multiplicar(0, 10) == 0
```

---

## 2. Agregar Tests con Mocks

### Paso 1: Agregar función con dependencia externa

```python
import requests

def obtener_usuario_api(user_id: int) -> dict:
    """Obtiene usuario desde API externa"""
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

def procesar_usuario(user_id: int) -> str:
    """Procesa información de usuario"""
    usuario = obtener_usuario_api(user_id)
    return f"Usuario: {usuario['name']}, Email: {usuario['email']}"
```

### Paso 2: Agregar tests con mocks

```python
from unittest.mock import patch, Mock

class TestAPIUsuarios:
    """Tests para funciones que usan API externa"""
    
    @patch('main.obtener_usuario_api')
    def test_procesar_usuario_exitoso(self, mock_api):
        """Verifica procesamiento exitoso de usuario"""
        # Configurar mock
        mock_api.return_value = {
            "name": "Juan Pérez",
            "email": "juan@example.com"
        }
        
        resultado = procesar_usuario(123)
        
        assert "Juan Pérez" in resultado
        assert "juan@example.com" in resultado
        mock_api.assert_called_once_with(123)
    
    @patch('main.requests.get')
    def test_obtener_usuario_api_mock_completo(self, mock_get):
        """Verifica llamada a API con mock completo"""
        # Mock de response
        mock_response = Mock()
        mock_response.json.return_value = {"name": "Test", "email": "test@test.com"}
        mock_get.return_value = mock_response
        
        resultado = obtener_usuario_api(456)
        
        assert resultado["name"] == "Test"
        mock_get.assert_called_once_with("https://api.example.com/users/456")
```

---

## 3. Agregar Tests Asíncronos

### Paso 1: Agregar función asíncrona

```python
import asyncio
import aiohttp

async def obtener_datos_async(url: str) -> dict:
    """Obtiene datos de forma asíncrona"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def procesar_multiples_urls(urls: list) -> list:
    """Procesa múltiples URLs en paralelo"""
    tasks = [obtener_datos_async(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### Paso 2: Agregar tests asíncronos

```python
import pytest

class TestFuncionesAsync:
    """Tests para funciones asíncronas"""
    
    @pytest.mark.asyncio
    async def test_obtener_datos_async(self):
        """Verifica obtención asíncrona de datos"""
        # Nota: En test real, mockearíamos aiohttp
        # Este es un ejemplo de estructura
        pass
    
    @pytest.mark.asyncio
    @patch('main.obtener_datos_async')
    async def test_procesar_multiples_urls(self, mock_obtener):
        """Verifica procesamiento paralelo de URLs"""
        mock_obtener.return_value = {"status": "ok"}
        
        urls = ["http://url1.com", "http://url2.com"]
        resultados = await procesar_multiples_urls(urls)
        
        assert len(resultados) == 2
        assert mock_obtener.call_count == 2
```

---

## 4. Agregar Tests Parametrizados

### Ejemplo: Tests con múltiples casos

```python
import pytest

class TestParametrizadosAvanzados:
    """Tests parametrizados avanzados"""
    
    @pytest.mark.parametrize("entrada,esperado", [
        ("hola", "HOLA"),
        ("MUNDO", "MUNDO"),
        ("PyThOn", "PYTHON"),
        ("", ""),
    ])
    def test_convertir_mayusculas(self, entrada, esperado):
        """Verifica conversión a mayúsculas"""
        assert entrada.upper() == esperado
    
    @pytest.mark.parametrize("edad,es_mayor", [
        (17, False),
        (18, True),
        (25, True),
        (0, False),
    ])
    def test_es_mayor_de_edad(self, edad, es_mayor):
        """Verifica validación de mayoría de edad"""
        def es_mayor_de_edad(edad):
            return edad >= 18
        
        assert es_mayor_de_edad(edad) == es_mayor
    
    @pytest.mark.parametrize("usuario,password,valido", [
        ("admin", "admin123", True),
        ("user", "wrongpass", False),
        ("", "", False),
        ("admin", "", False),
    ])
    def test_validar_credenciales(self, usuario, password, valido):
        """Verifica validación de credenciales"""
        def validar_credenciales(user, pwd):
            return user == "admin" and pwd == "admin123"
        
        assert validar_credenciales(usuario, password) == valido
```

---

## 5. Crear Fixtures Personalizadas

### Fixtures Simples

```python
import pytest

@pytest.fixture
def usuario_test():
    """Fixture que proporciona un usuario de prueba"""
    return {
        "id": 1,
        "nombre": "Test User",
        "email": "test@example.com"
    }

@pytest.fixture
def base_datos_temporal():
    """Fixture que proporciona una base de datos temporal"""
    db = BaseDeDatos()
    db.guardar("user1", {"nombre": "Juan"})
    db.guardar("user2", {"nombre": "María"})
    return db

def test_usar_usuario_test(usuario_test):
    """Test que usa fixture de usuario"""
    assert usuario_test["nombre"] == "Test User"
    assert usuario_test["email"] == "test@example.com"

def test_usar_base_datos_temporal(base_datos_temporal):
    """Test que usa fixture de base de datos"""
    assert base_datos_temporal.obtener("user1")["nombre"] == "Juan"
    assert base_datos_temporal.obtener("user2")["nombre"] == "María"
```

### Fixtures con Setup y Teardown

```python
import pytest

@pytest.fixture
def archivo_temporal(tmp_path):
    """Fixture que crea y limpia archivo temporal"""
    # Setup
    archivo = tmp_path / "test.txt"
    archivo.write_text("contenido inicial")
    
    # Proporcionar fixture
    yield archivo
    
    # Teardown (se ejecuta después del test)
    if archivo.exists():
        archivo.unlink()

def test_leer_archivo_temporal(archivo_temporal):
    """Test que usa archivo temporal"""
    contenido = archivo_temporal.read_text()
    assert contenido == "contenido inicial"
```

### Fixtures con Scope

```python
@pytest.fixture(scope="module")
def conexion_db():
    """Fixture que se crea una vez por módulo"""
    print("Conectando a base de datos...")
    db = BaseDeDatos()
    yield db
    print("Cerrando conexión a base de datos...")

@pytest.fixture(scope="function")
def transaccion(conexion_db):
    """Fixture que se crea para cada test"""
    print("Iniciando transacción...")
    yield conexion_db
    print("Haciendo rollback...")
```

---

## 6. Agregar Marcadores Personalizados

### Paso 1: Definir marcadores en `pytest.ini`

```ini
[pytest]
markers =
    slow: marca tests lentos
    integration: marca tests de integración
    unit: marca tests unitarios
    smoke: marca tests de smoke testing
    regression: marca tests de regresión
    api: marca tests de API
```

### Paso 2: Usar marcadores en tests

```python
import pytest

@pytest.mark.slow
def test_operacion_lenta():
    """Test que tarda mucho tiempo"""
    import time
    time.sleep(2)
    assert True

@pytest.mark.integration
def test_integracion_completa():
    """Test de integración completo"""
    assert True

@pytest.mark.unit
@pytest.mark.smoke
def test_funcionalidad_critica():
    """Test unitario crítico para smoke testing"""
    assert True

@pytest.mark.api
@pytest.mark.integration
def test_endpoint_usuarios():
    """Test de endpoint de API"""
    assert True
```

### Paso 3: Ejecutar tests por marcador

```bash
# Ejecutar solo tests lentos
pytest -m slow

# Ejecutar solo tests de integración
pytest -m integration

# Ejecutar tests unitarios Y smoke
pytest -m "unit and smoke"

# Ejecutar tests que NO son lentos
pytest -m "not slow"
```

---

## 7. Tests de Excepciones

### Diferentes formas de testear excepciones

```python
import pytest

class TestExcepciones:
    """Tests para manejo de excepciones"""
    
    def test_excepcion_basica(self):
        """Verifica que se lance excepción"""
        with pytest.raises(ValueError):
            raise ValueError("Error de prueba")
    
    def test_excepcion_con_mensaje(self):
        """Verifica excepción con mensaje específico"""
        with pytest.raises(ValueError, match="dividir por cero"):
            dividir(10, 0)
    
    def test_excepcion_con_validacion(self):
        """Verifica excepción y valida sus atributos"""
        with pytest.raises(ValueError) as exc_info:
            raise ValueError("Error personalizado")
        
        assert "personalizado" in str(exc_info.value)
    
    def test_multiples_excepciones(self):
        """Verifica que se lance una de varias excepciones"""
        with pytest.raises((ValueError, TypeError)):
            # Puede lanzar ValueError o TypeError
            raise ValueError("Error")
    
    def test_no_lanza_excepcion(self):
        """Verifica que NO se lance excepción"""
        try:
            resultado = sumar(2, 3)
            assert resultado == 5
        except Exception as e:
            pytest.fail(f"No debería lanzar excepción: {e}")
```

---

## 8. Tests de Integración

### Ejemplo completo de test de integración

```python
class TestIntegracionCompleta:
    """Tests de integración completos"""
    
    def test_flujo_completo_usuario(self):
        """Test de flujo completo: crear, actualizar, eliminar usuario"""
        # Setup
        db = BaseDeDatos()
        servicio = UsuarioService(db)
        
        # 1. Crear usuario
        usuario = servicio.crear_usuario("user123", "Juan Pérez")
        assert usuario["nombre"] == "Juan Pérez"
        assert usuario["activo"] == True
        
        # 2. Verificar que se guardó
        usuario_guardado = db.obtener("user123")
        assert usuario_guardado is not None
        assert usuario_guardado["nombre"] == "Juan Pérez"
        
        # 3. Actualizar usuario (si existe el método)
        # servicio.actualizar_usuario("user123", nombre="Juan Carlos")
        
        # 4. Eliminar usuario (si existe el método)
        # servicio.eliminar_usuario("user123")
        # assert db.obtener("user123") is None
    
    def test_integracion_con_multiples_servicios(self):
        """Test de integración entre múltiples servicios"""
        # Setup
        cache = Cache()
        db = BaseDatosContenido()
        gestor = GestorArticulos(cache, db)
        
        # 1. Primera lectura (desde DB)
        articulo1 = gestor.obtener_articulo("art123")
        assert articulo1["source"] == "db"
        
        # 2. Segunda lectura (desde caché)
        articulo2 = gestor.obtener_articulo("art123")
        assert articulo2["source"] == "cache"
        
        # 3. Verificar que son el mismo artículo
        assert articulo1["id"] == articulo2["id"]
```

---

## 🎯 Mejores Prácticas

### 1. Nomenclatura de Tests

```python
# ✅ BIEN: Nombre descriptivo
def test_usuario_puede_depositar_dinero_en_cuenta():
    pass

# ❌ MAL: Nombre poco descriptivo
def test_deposito():
    pass
```

### 2. Organización de Tests

```python
# ✅ BIEN: Tests organizados en clases por funcionalidad
class TestCuentaBancaria:
    def test_crear_cuenta_con_saldo_inicial(self):
        pass
    
    def test_depositar_aumenta_saldo(self):
        pass
    
    def test_retirar_disminuye_saldo(self):
        pass

# ❌ MAL: Tests sueltos sin organización
def test_cuenta1():
    pass

def test_cuenta2():
    pass
```

### 3. Patrón AAA (Arrange-Act-Assert)

```python
def test_ejemplo_patron_aaa():
    # Arrange (Preparar)
    cuenta = CuentaBancaria(1000)
    monto_deposito = 500
    
    # Act (Actuar)
    cuenta.depositar(monto_deposito)
    
    # Assert (Verificar)
    assert cuenta.saldo == 1500
```

### 4. Un Assert por Test (cuando sea posible)

```python
# ✅ BIEN: Un concepto por test
def test_sumar_retorna_suma_correcta():
    assert sumar(2, 3) == 5

def test_sumar_maneja_negativos():
    assert sumar(-2, 3) == 1

# ⚠️ ACEPTABLE: Múltiples asserts del mismo concepto
def test_sumar_varios_casos():
    assert sumar(2, 3) == 5
    assert sumar(10, 20) == 30
    assert sumar(-5, 5) == 0
```

### 5. Usar Fixtures para Setup Común

```python
# ✅ BIEN: Usar fixture
@pytest.fixture
def cuenta_inicial():
    return CuentaBancaria(1000)

def test_depositar(cuenta_inicial):
    cuenta_inicial.depositar(500)
    assert cuenta_inicial.saldo == 1500

def test_retirar(cuenta_inicial):
    cuenta_inicial.retirar(300)
    assert cuenta_inicial.saldo == 700

# ❌ MAL: Duplicar setup
def test_depositar():
    cuenta = CuentaBancaria(1000)  # Duplicado
    cuenta.depositar(500)
    assert cuenta.saldo == 1500

def test_retirar():
    cuenta = CuentaBancaria(1000)  # Duplicado
    cuenta.retirar(300)
    assert cuenta.saldo == 700
```

---

## 📚 Recursos Adicionales

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Parametrize](https://docs.pytest.org/en/stable/parametrize.html)
- [Unittest Mock](https://docs.python.org/3/library/unittest.mock.html)

---

**Última actualización**: 2025-11-28  
**Versión**: 1.0
