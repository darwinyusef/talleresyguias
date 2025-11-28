# Módulo 1: Introducción a Testing y Pytest

## ¿Qué es el Testing?

El testing (pruebas de software) es el proceso de verificar que tu código funciona como esperas. Es como tener un asistente que revisa automáticamente que todo funcione correctamente cada vez que haces cambios.

### ¿Por qué es importante?

- **Confianza**: Sabes que tu código funciona
- **Documentación**: Los tests muestran cómo usar tu código
- **Refactorización segura**: Puedes cambiar código sin miedo a romper algo
- **Ahorro de tiempo**: Detectas errores antes de que lleguen a producción
- **Calidad**: Mejora la calidad general de tu software

## Tipos de Testing

### 1. Test Unitarios
Prueban una pequeña unidad de código (función, método) de forma aislada.

**Ejemplo conceptual:**
```
Función a probar: sumar(a, b)
Test: verificar que sumar(2, 3) devuelva 5
```

### 2. Test de Integración
Prueban cómo funcionan varios componentes juntos.

**Ejemplo conceptual:**
```
Probar que el servicio de usuarios puede guardar y recuperar datos de la base de datos
```

### 3. Test End-to-End (E2E)
Prueban el sistema completo desde la perspectiva del usuario.

**Ejemplo conceptual:**
```
Simular que un usuario se registra, inicia sesión y realiza una compra
```

## ¿Qué es Pytest?

Pytest es el framework de testing más popular para Python. Es simple, potente y tiene una sintaxis muy limpia.

### Ventajas de Pytest

- Sintaxis simple y pythónica
- No requiere herencia de clases
- Mensajes de error claros
- Gran ecosistema de plugins
- Fixtures poderosas para setup/teardown
- Parametrización fácil de tests

## Instalación y Configuración

### Instalación de Pytest

```bash
# Crear un entorno virtual (recomendado)
python -m venv venv

# Activar el entorno virtual
# En Mac/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar pytest
pip install pytest

# Instalar dependencias adicionales útiles
pip install pytest-cov  # Para coverage (cobertura)
pip install pytest-mock # Para mocking avanzado
```

### Verificar la instalación

```bash
pytest --version
```

Deberías ver algo como: `pytest 7.x.x`

## Tu Primer Test

### Estructura básica de un proyecto con tests

```
mi_proyecto/
├── src/
│   └── calculadora.py
└── tests/
    └── test_calculadora.py
```

### Convenciones de nombres

Pytest usa convenciones para descubrir tests automáticamente:

- Los archivos de test deben llamarse `test_*.py` o `*_test.py`
- Las funciones de test deben llamarse `test_*()`
- Las clases de test deben llamarse `Test*`

### Ejemplo 1: Función simple

**Archivo: src/calculadora.py**
```python
def sumar(a, b):
    """Suma dos números"""
    return a + b

def restar(a, b):
    """Resta dos números"""
    return a - b
```

**Archivo: tests/test_calculadora.py**
```python
from src.calculadora import sumar, restar

def test_sumar_numeros_positivos():
    resultado = sumar(2, 3)
    assert resultado == 5

def test_sumar_numeros_negativos():
    resultado = sumar(-1, -1)
    assert resultado == -2

def test_restar_numeros():
    resultado = restar(5, 3)
    assert resultado == 2
```

## Assertions Básicas

Las assertions son afirmaciones que verifican si algo es verdadero. Si la assertion falla, el test falla.

### Assert simple

```python
def test_assert_basico():
    x = 10
    assert x == 10  # Pasa
    assert x > 5    # Pasa
    assert x < 20   # Pasa
```

### Assert con mensaje personalizado

```python
def test_assert_con_mensaje():
    edad = 15
    assert edad >= 18, f"La edad {edad} es menor a 18"
```

### Assertions comunes

```python
def test_assertions_comunes():
    # Igualdad
    assert 5 == 5

    # Desigualdad
    assert 5 != 4

    # Comparaciones
    assert 5 > 3
    assert 5 >= 5
    assert 3 < 5
    assert 5 <= 5

    # Booleanos
    assert True
    assert not False

    # Pertenencia
    assert 3 in [1, 2, 3]
    assert "a" in "casa"

    # Identidad
    lista = [1, 2, 3]
    assert lista is lista

    # None
    valor = None
    assert valor is None
```

### Assertions con strings

```python
def test_strings():
    texto = "Hola Mundo"

    assert "Hola" in texto
    assert texto.startswith("Hola")
    assert texto.endswith("Mundo")
    assert len(texto) == 10
```

### Assertions con listas y diccionarios

```python
def test_listas():
    numeros = [1, 2, 3, 4, 5]

    assert len(numeros) == 5
    assert 3 in numeros
    assert numeros[0] == 1

def test_diccionarios():
    persona = {"nombre": "Ana", "edad": 25}

    assert persona["nombre"] == "Ana"
    assert "edad" in persona
    assert len(persona) == 2
```

## Ejecutar Tests

### Ejecutar todos los tests

```bash
pytest
```

### Ejecutar un archivo específico

```bash
pytest tests/test_calculadora.py
```

### Ejecutar una función específica

```bash
pytest tests/test_calculadora.py::test_sumar_numeros_positivos
```

### Ejecutar con más detalle (verbose)

```bash
pytest -v
```

### Ejecutar mostrando prints

```bash
pytest -s
```

### Ejecutar con cobertura

```bash
pytest --cov=src tests/
```

## Ejemplo Completo Paso a Paso

Vamos a crear un ejemplo completo desde cero:

### Paso 1: Crear la estructura

```bash
mkdir mi_primer_proyecto
cd mi_primer_proyecto
mkdir src tests
```

### Paso 2: Crear el código a probar

**src/utilidades.py**
```python
def es_par(numero):
    """Verifica si un número es par"""
    return numero % 2 == 0

def duplicar(numero):
    """Duplica un número"""
    return numero * 2

def saludar(nombre):
    """Retorna un saludo personalizado"""
    if not nombre:
        return "Hola, desconocido"
    return f"Hola, {nombre}"
```

### Paso 3: Crear los tests

**tests/test_utilidades.py**
```python
from src.utilidades import es_par, duplicar, saludar

# Tests para es_par()
def test_es_par_con_numero_par():
    assert es_par(4) == True

def test_es_par_con_numero_impar():
    assert es_par(5) == False

def test_es_par_con_cero():
    assert es_par(0) == True

# Tests para duplicar()
def test_duplicar_numero_positivo():
    assert duplicar(5) == 10

def test_duplicar_numero_negativo():
    assert duplicar(-3) == -6

def test_duplicar_cero():
    assert duplicar(0) == 0

# Tests para saludar()
def test_saludar_con_nombre():
    resultado = saludar("Carlos")
    assert resultado == "Hola, Carlos"

def test_saludar_sin_nombre():
    resultado = saludar("")
    assert resultado == "Hola, desconocido"

def test_saludar_con_none():
    resultado = saludar(None)
    assert resultado == "Hola, desconocido"
```

### Paso 4: Ejecutar los tests

```bash
pytest -v
```

### Salida esperada

```
tests/test_utilidades.py::test_es_par_con_numero_par PASSED
tests/test_utilidades.py::test_es_par_con_numero_impar PASSED
tests/test_utilidades.py::test_es_par_con_cero PASSED
tests/test_utilidades.py::test_duplicar_numero_positivo PASSED
tests/test_utilidades.py::test_duplicar_numero_negativo PASSED
tests/test_utilidades.py::test_duplicar_cero PASSED
tests/test_utilidades.py::test_saludar_con_nombre PASSED
tests/test_utilidades.py::test_saludar_sin_nombre PASSED
tests/test_utilidades.py::test_saludar_con_none PASSED

========= 9 passed in 0.02s =========
```

## Interpretando los Resultados

### Test que pasa (✓)
```
test_sumar_numeros_positivos PASSED
```

### Test que falla (✗)
```
test_sumar_numeros_positivos FAILED
```

Pytest te mostrará:
- Qué assertion falló
- El valor esperado vs el valor obtenido
- La línea exacta donde falló

### Ejemplo de error

```python
def test_con_error():
    resultado = sumar(2, 2)
    assert resultado == 5  # Esto fallará
```

Salida:
```
AssertionError: assert 4 == 5
    Expected: 5
    Actual: 4
```

## Buenas Prácticas

### 1. Un test, una cosa
Cada test debe verificar una sola cosa específica.

**Mal:**
```python
def test_calculadora():
    assert sumar(2, 3) == 5
    assert restar(5, 2) == 3
    assert multiplicar(2, 3) == 6
```

**Bien:**
```python
def test_sumar():
    assert sumar(2, 3) == 5

def test_restar():
    assert restar(5, 2) == 3

def test_multiplicar():
    assert multiplicar(2, 3) == 6
```

### 2. Nombres descriptivos
El nombre del test debe decir exactamente qué se está probando.

**Mal:**
```python
def test_1():
    assert sumar(2, 3) == 5
```

**Bien:**
```python
def test_sumar_dos_numeros_positivos_retorna_suma_correcta():
    assert sumar(2, 3) == 5
```

### 3. Patrón AAA (Arrange, Act, Assert)

```python
def test_ejemplo_patron_aaa():
    # Arrange (Preparar): Configurar los datos
    numero1 = 5
    numero2 = 3

    # Act (Actuar): Ejecutar la función
    resultado = sumar(numero1, numero2)

    # Assert (Afirmar): Verificar el resultado
    assert resultado == 8
```

### 4. Tests independientes
Cada test debe poder ejecutarse solo, sin depender de otros tests.

### 5. Tests rápidos
Los tests unitarios deben ejecutarse rápidamente (milisegundos).

## Ejercicios Prácticos

### Ejercicio 1: Validador de Email
Crea una función que valide si un string es un email válido y escribe tests para ella.

```python
# src/validadores.py
def es_email_valido(email):
    # Tu implementación aquí
    pass

# tests/test_validadores.py
# Escribe tests para:
# - Email válido
# - Email sin @
# - Email sin dominio
# - Email vacío
# - Email con espacios
```

### Ejercicio 2: Calculadora de descuentos
Crea una función que calcule el precio final con descuento y escribe tests.

```python
# src/calculadora_precios.py
def calcular_precio_con_descuento(precio, descuento_porcentaje):
    # Tu implementación aquí
    pass

# tests/test_calculadora_precios.py
# Escribe tests para:
# - Descuento normal (20%)
# - Sin descuento (0%)
# - Descuento completo (100%)
# - Precio 0
# - Descuento inválido (>100%)
```

### Ejercicio 3: Contador de palabras
Crea una función que cuente palabras en un texto.

```python
# src/texto.py
def contar_palabras(texto):
    # Tu implementación aquí
    pass

# tests/test_texto.py
# Escribe tests para:
# - Texto normal
# - Texto vacío
# - Texto con espacios múltiples
# - Texto con saltos de línea
```

## Resumen

En este módulo aprendiste:

- Qué es el testing y por qué es importante
- Los diferentes tipos de testing
- Qué es pytest y cómo instalarlo
- Cómo escribir tu primer test
- Assertions básicas
- Cómo ejecutar tests
- Buenas prácticas de testing

## Próximos Pasos

En el siguiente módulo aprenderás sobre test unitarios más avanzados, incluyendo:
- Parametrización de tests
- Fixtures
- Testing de excepciones
- Organización de tests

---

**[⬅️ Volver al índice](../README.md) | [Siguiente: Módulo 2 - Test Unitarios Básicos ➡️](02-test-unitarios-basicos.md)**
