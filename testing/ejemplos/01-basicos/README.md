# 🧪 Testing en Python - Ejemplos Básicos

Este directorio contiene ejemplos completos de testing en Python usando **pytest**, cubriendo desde tests unitarios básicos hasta tests de integración avanzados.

## 📁 Estructura de Archivos

```
01-basicos/
├── main.py                 # Código fuente con 15 categorías de funciones
├── test_main.py           # Suite completa de tests (71 tests)
├── pytest.ini             # Configuración de pytest
├── RESULTADOS_TESTS.md    # Reporte detallado de resultados
├── README.md              # Este archivo
└── htmlcov/               # Reporte HTML de cobertura (generado)
```

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install pytest pytest-asyncio pytest-cov
```

### 2. Ejecutar Todos los Tests

```bash
pytest
```

o

```bash
python3 -m pytest
```

### 3. Ver Resultados

Los tests se ejecutarán automáticamente con:
- ✅ Modo verbose (`-v`)
- 📊 Reporte de cobertura
- 📄 Generación de reporte HTML

## 📚 Contenido del Proyecto

### `main.py` - Código Fuente

Contiene **15 categorías** de funciones que cubren diferentes escenarios de testing:

1. **Unitarios Básicos** - Funciones puras simples
2. **Unitarios con Mock** - Funciones con dependencias externas
3. **Integración** - Servicios + Base de Datos
4. **A/B Logic** - Lógica de A/B testing
5. **Stateful** - Clases con estado
6. **E2E Simulation** - Flujos completos
7. **Async/Await** - Funciones asíncronas
8. **File I/O** - Operaciones de archivos
9. **Date/Time** - Funciones dependientes de tiempo
10. **Decoradores** - Testing de wrappers
11. **Context Managers** - `__enter__` y `__exit__`
12. **Regex Parsing** - Expresiones regulares
13. **Sistema de Notificaciones** - Integración de servicios
14. **Procesamiento de Pagos** - Coordinación de servicios
15. **Gestor de Contenidos** - Sistema de caché

### `test_main.py` - Suite de Tests

Contiene **71 tests** organizados en clases que cubren:

- ✅ Tests unitarios básicos
- ✅ Mocking de dependencias externas
- ✅ Tests de integración
- ✅ Tests asíncronos
- ✅ Tests parametrizados
- ✅ Uso de fixtures
- ✅ Testing de excepciones
- ✅ Mocking de archivos, tiempo y datetime

**Cobertura: 100%** 🎯

## 🎓 Conceptos de Testing Cubiertos

### Técnicas Básicas
- Asserts simples
- `pytest.raises` para excepciones
- Fixtures de pytest
- Parametrización con `@pytest.mark.parametrize`

### Técnicas Avanzadas
- **Mocking** con `unittest.mock`
  - `@patch` decorator
  - `Mock()` y `MagicMock()`
  - `mock_open` para archivos
  - `side_effect` para excepciones
- **Testing Asíncrono** con `pytest-asyncio`
- **Cobertura de Código** con `pytest-cov`
- **Testing de Decoradores**
- **Testing de Context Managers**

### Patrones de Testing
- **AAA** (Arrange-Act-Assert)
- **Given-When-Then**
- **Test de Integración**
- **Test E2E Simulado**
- **Test de Estado (Stateful)**

## 📖 Comandos Útiles

### Ejecutar Tests Específicos

```bash
# Ejecutar solo una clase de tests
pytest test_main.py::TestUnitariosBasicos -v

# Ejecutar un test específico
pytest test_main.py::TestUnitariosBasicos::test_sumar_numeros_positivos -v

# Ejecutar tests que coincidan con un patrón
pytest -k "palindromo" -v
```

### Reportes de Cobertura

```bash
# Reporte en terminal
pytest --cov=main --cov-report=term-missing

# Generar reporte HTML
pytest --cov=main --cov-report=html

# Abrir reporte HTML (macOS)
open htmlcov/index.html
```

### Opciones de Pytest

```bash
# Modo verbose (más detalles)
pytest -v

# Mostrar print statements
pytest -s

# Detener en el primer fallo
pytest -x

# Ejecutar tests en paralelo (requiere pytest-xdist)
pytest -n auto

# Ejecutar solo tests que fallaron la última vez
pytest --lf

# Modo quiet (menos output)
pytest -q
```

### Marcadores Personalizados

```bash
# Ejecutar solo tests asíncronos
pytest -m asyncio

# Ejecutar solo tests de integración
pytest -m integration

# Ejecutar solo tests unitarios
pytest -m unit
```

## 🔍 Ejemplos de Uso

### Ejemplo 1: Test Unitario Básico

```python
def test_sumar_numeros_positivos():
    """Verifica que la suma de números positivos funcione correctamente"""
    assert sumar(2, 3) == 5
    assert sumar(10, 20) == 30
```

### Ejemplo 2: Test con Mock

```python
@patch('main.obtener_datos_externos')
def test_procesar_datos_exitoso(mock_obtener):
    """Verifica que procesar_datos funcione con respuesta exitosa"""
    mock_obtener.return_value = {"status": "ok", "data": [10, 20, 30]}
    
    resultado = procesar_datos("http://api.example.com")
    
    assert resultado == 60
    mock_obtener.assert_called_once_with("http://api.example.com")
```

### Ejemplo 3: Test Asíncrono

```python
@pytest.mark.asyncio
async def test_obtener_clima_madrid():
    """Verifica que obtener_clima retorne 'Soleado' para Madrid"""
    clima = await obtener_clima("Madrid")
    assert clima == "Soleado"
```

### Ejemplo 4: Test Parametrizado

```python
@pytest.mark.parametrize("a,b,esperado", [
    (2, 3, 5),
    (10, 20, 30),
    (-5, 5, 0),
])
def test_sumar_parametrizado(a, b, esperado):
    """Verifica suma con múltiples casos parametrizados"""
    assert sumar(a, b) == esperado
```

### Ejemplo 5: Test con Fixture

```python
@pytest.fixture
def cuenta_con_saldo():
    """Fixture que proporciona una cuenta con saldo inicial"""
    return CuentaBancaria(1000)

def test_usar_fixture_cuenta(cuenta_con_saldo):
    """Verifica el uso de fixture de cuenta bancaria"""
    assert cuenta_con_saldo.saldo == 1000
    cuenta_con_saldo.depositar(500)
    assert cuenta_con_saldo.saldo == 1500
```

## 📊 Resultados

```
============================= test session starts ==============================
collected 71 items

test_main.py::TestUnitariosBasicos::test_sumar_numeros_positivos PASSED  [  1%]
test_main.py::TestUnitariosBasicos::test_sumar_numeros_negativos PASSED  [  2%]
...
test_main.py::TestParametrizados::test_ab_testing_parametrizado[X-Bienvenido] PASSED [100%]

================================ tests coverage ================================
Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py     211      0   100%
---------------------------------------
TOTAL       211      0   100%

============================== 71 passed in 0.60s ==============================
```

**✅ 71 tests pasados**  
**📊 100% de cobertura**  
**⚡ 0.60 segundos**

## 🎯 Mejores Prácticas Aplicadas

1. **Organización Clara**: Tests organizados en clases por categoría
2. **Nombres Descriptivos**: Cada test describe qué se prueba y el resultado esperado
3. **Documentación**: Docstrings en cada test explicando su propósito
4. **Aislamiento**: Uso de mocks para aislar unidades bajo test
5. **DRY**: Parametrización para evitar duplicación de código
6. **Fixtures**: Reutilización de setup común
7. **Cobertura Completa**: 100% de cobertura de código

## 📖 Recursos Adicionales

- [Documentación de Pytest](https://docs.pytest.org/)
- [Documentación de unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Pytest-cov](https://pytest-cov.readthedocs.io/)
- [Real Python - Testing](https://realpython.com/pytest-python-testing/)

## 🤝 Contribuir

Este es un proyecto educativo. Siéntete libre de:
- Agregar más ejemplos de tests
- Mejorar la documentación
- Sugerir nuevas categorías de tests

## 📝 Notas

- Los tests están diseñados para ser **educativos** y cubrir la mayor cantidad de escenarios posibles
- Cada categoría de tests demuestra una técnica o patrón específico
- El código en `main.py` está diseñado para ser **testeable** y demostrar buenas prácticas

---

**Última actualización**: 2025-11-28  
**Versión**: 1.0  
**Autor**: Testing Automation
