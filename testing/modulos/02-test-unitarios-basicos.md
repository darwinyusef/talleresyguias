# Módulo 2: Test Unitarios Básicos (POCs)

## Introducción

En este módulo profundizaremos en los test unitarios trabajando con diferentes tipos de funciones y estructuras de datos. Aprenderás técnicas avanzadas como parametrización, fixtures y manejo de excepciones.

## POC (Proof of Concept) - Conceptos Básicos

Un POC es un ejemplo pequeño y enfocado que demuestra que algo funciona. En testing, crearemos pequeños POCs para practicar diferentes escenarios.

## Testing de Funciones Puras

Las funciones puras son las más fáciles de testear porque:
- Siempre retornan el mismo resultado para los mismos argumentos
- No tienen efectos secundarios
- No dependen de estado externo

### POC 1: Operaciones Matemáticas

**Archivo: ejemplos/01-basicos/matematicas.py**
```python
def multiplicar(a, b):
    """Multiplica dos números"""
    return a * b

def dividir(a, b):
    """Divide dos números"""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

def potencia(base, exponente):
    """Calcula la potencia de un número"""
    return base ** exponente

def factorial(n):
    """Calcula el factorial de un número"""
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
```

**Archivo: ejemplos/01-basicos/test_matematicas.py**
```python
import pytest
from matematicas import multiplicar, dividir, potencia, factorial

# Tests básicos de multiplicación
def test_multiplicar_positivos():
    assert multiplicar(3, 4) == 12

def test_multiplicar_negativos():
    assert multiplicar(-2, -3) == 6

def test_multiplicar_por_cero():
    assert multiplicar(5, 0) == 0

# Tests de división
def test_dividir_numeros():
    assert dividir(10, 2) == 5

def test_dividir_resultado_decimal():
    assert dividir(7, 2) == 3.5

def test_dividir_por_cero_lanza_excepcion():
    with pytest.raises(ValueError) as excinfo:
        dividir(10, 0)
    assert "No se puede dividir por cero" in str(excinfo.value)

# Tests de potencia
def test_potencia_exponente_positivo():
    assert potencia(2, 3) == 8

def test_potencia_exponente_cero():
    assert potencia(5, 0) == 1

def test_potencia_exponente_negativo():
    assert potencia(2, -1) == 0.5

# Tests de factorial
def test_factorial_de_cero():
    assert factorial(0) == 1

def test_factorial_de_numero_positivo():
    assert factorial(5) == 120

def test_factorial_de_numero_negativo():
    with pytest.raises(ValueError):
        factorial(-1)
```

## Parametrización de Tests

La parametrización te permite ejecutar el mismo test con diferentes datos, evitando código repetitivo.

### POC 2: Validador de Contraseñas

**Archivo: ejemplos/01-basicos/validador.py**
```python
def es_contrasena_fuerte(contrasena):
    """
    Verifica si una contraseña es fuerte.
    Criterios:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    """
    if len(contrasena) < 8:
        return False
    if not any(c.isupper() for c in contrasena):
        return False
    if not any(c.islower() for c in contrasena):
        return False
    if not any(c.isdigit() for c in contrasena):
        return False
    return True

def validar_edad(edad):
    """Valida que la edad esté en un rango válido"""
    if edad < 0:
        return "Edad inválida"
    elif edad < 18:
        return "Menor de edad"
    elif edad < 65:
        return "Adulto"
    else:
        return "Adulto mayor"
```

**Archivo: ejemplos/01-basicos/test_validador.py**
```python
import pytest
from validador import es_contrasena_fuerte, validar_edad

# Parametrización simple
@pytest.mark.parametrize("contrasena,esperado", [
    ("Ab123456", True),   # Contraseña válida
    ("corta1A", False),   # Muy corta
    ("sinmayuscula123", False),  # Sin mayúscula
    ("SINMINUSCULA123", False),  # Sin minúscula
    ("SinNumeros", False),  # Sin números
    ("Password123", True),  # Válida
])
def test_contrasena_fuerte_parametrizado(contrasena, esperado):
    assert es_contrasena_fuerte(contrasena) == esperado

# Parametrización con múltiples casos
@pytest.mark.parametrize("edad,esperado", [
    (-1, "Edad inválida"),
    (0, "Menor de edad"),
    (17, "Menor de edad"),
    (18, "Adulto"),
    (30, "Adulto"),
    (64, "Adulto"),
    (65, "Adulto mayor"),
    (100, "Adulto mayor"),
])
def test_validar_edad_parametrizado(edad, esperado):
    assert validar_edad(edad) == esperado
```

## Fixtures Básicas

Las fixtures son funciones que proveen datos o configuración para tus tests. Son útiles para evitar duplicación de código.

### POC 3: Procesador de Listas

**Archivo: ejemplos/01-basicos/procesador_listas.py**
```python
def ordenar_lista(lista):
    """Ordena una lista de números"""
    return sorted(lista)

def eliminar_duplicados(lista):
    """Elimina elementos duplicados de una lista"""
    return list(set(lista))

def filtrar_pares(lista):
    """Filtra solo los números pares de una lista"""
    return [x for x in lista if x % 2 == 0]

def calcular_promedio(lista):
    """Calcula el promedio de una lista"""
    if not lista:
        raise ValueError("La lista no puede estar vacía")
    return sum(lista) / len(lista)
```

**Archivo: ejemplos/01-basicos/test_procesador_listas.py**
```python
import pytest
from procesador_listas import (
    ordenar_lista,
    eliminar_duplicados,
    filtrar_pares,
    calcular_promedio
)

# Fixture simple
@pytest.fixture
def lista_desordenada():
    """Provee una lista desordenada para tests"""
    return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

@pytest.fixture
def lista_con_duplicados():
    """Provee una lista con duplicados"""
    return [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

@pytest.fixture
def lista_mixta():
    """Provee una lista con números pares e impares"""
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Tests usando fixtures
def test_ordenar_lista(lista_desordenada):
    resultado = ordenar_lista(lista_desordenada)
    assert resultado == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]

def test_eliminar_duplicados(lista_con_duplicados):
    resultado = eliminar_duplicados(lista_con_duplicados)
    assert set(resultado) == {1, 2, 3, 4}
    assert len(resultado) == 4

def test_filtrar_pares(lista_mixta):
    resultado = filtrar_pares(lista_mixta)
    assert resultado == [2, 4, 6, 8, 10]

def test_calcular_promedio(lista_mixta):
    resultado = calcular_promedio(lista_mixta)
    assert resultado == 5.5

def test_promedio_lista_vacia():
    with pytest.raises(ValueError) as excinfo:
        calcular_promedio([])
    assert "vacía" in str(excinfo.value)
```

## Testing de Strings

### POC 4: Manipulador de Texto

**Archivo: ejemplos/01-basicos/texto.py**
```python
def invertir_texto(texto):
    """Invierte un texto"""
    return texto[::-1]

def contar_vocales(texto):
    """Cuenta el número de vocales en un texto"""
    vocales = "aeiouAEIOU"
    return sum(1 for char in texto if char in vocales)

def es_palindromo(texto):
    """Verifica si un texto es palíndromo"""
    texto_limpio = ''.join(c.lower() for c in texto if c.isalnum())
    return texto_limpio == texto_limpio[::-1]

def capitalizar_palabras(texto):
    """Capitaliza la primera letra de cada palabra"""
    return ' '.join(palabra.capitalize() for palabra in texto.split())

def eliminar_espacios_extra(texto):
    """Elimina espacios múltiples dejando solo uno"""
    return ' '.join(texto.split())
```

**Archivo: ejemplos/01-basicos/test_texto.py**
```python
import pytest
from texto import (
    invertir_texto,
    contar_vocales,
    es_palindromo,
    capitalizar_palabras,
    eliminar_espacios_extra
)

# Tests de inversión
@pytest.mark.parametrize("texto,esperado", [
    ("hola", "aloh"),
    ("Python", "nohtyP"),
    ("12345", "54321"),
    ("", ""),
])
def test_invertir_texto(texto, esperado):
    assert invertir_texto(texto) == esperado

# Tests de conteo de vocales
@pytest.mark.parametrize("texto,esperado", [
    ("hola", 2),
    ("Python", 1),
    ("aeiou", 5),
    ("AEIOU", 5),
    ("xyz", 0),
    ("", 0),
])
def test_contar_vocales(texto, esperado):
    assert contar_vocales(texto) == esperado

# Tests de palíndromo
@pytest.mark.parametrize("texto,esperado", [
    ("oso", True),
    ("reconocer", True),
    ("Anita lava la tina", True),
    ("A man a plan a canal Panama", True),
    ("hola", False),
    ("Python", False),
])
def test_es_palindromo(texto, esperado):
    assert es_palindromo(texto) == esperado

# Tests de capitalización
def test_capitalizar_palabras():
    assert capitalizar_palabras("hola mundo") == "Hola Mundo"

def test_capitalizar_ya_capitalizado():
    assert capitalizar_palabras("Hola Mundo") == "Hola Mundo"

def test_capitalizar_texto_vacio():
    assert capitalizar_palabras("") == ""

# Tests de eliminación de espacios
@pytest.mark.parametrize("texto,esperado", [
    ("hola  mundo", "hola mundo"),
    ("  espacios   múltiples  ", "espacios múltiples"),
    ("uno dos tres", "uno dos tres"),
    ("", ""),
])
def test_eliminar_espacios_extra(texto, esperado):
    assert eliminar_espacios_extra(texto) == esperado
```

## Testing de Diccionarios y Estructuras de Datos

### POC 5: Gestor de Estudiantes

**Archivo: ejemplos/01-basicos/estudiantes.py**
```python
def crear_estudiante(nombre, edad, calificaciones):
    """Crea un diccionario representando un estudiante"""
    return {
        "nombre": nombre,
        "edad": edad,
        "calificaciones": calificaciones,
        "promedio": sum(calificaciones) / len(calificaciones) if calificaciones else 0
    }

def agregar_calificacion(estudiante, calificacion):
    """Agrega una calificación a un estudiante"""
    estudiante["calificaciones"].append(calificacion)
    calificaciones = estudiante["calificaciones"]
    estudiante["promedio"] = sum(calificaciones) / len(calificaciones)
    return estudiante

def obtener_estudiantes_aprobados(estudiantes, nota_minima=60):
    """Filtra estudiantes aprobados"""
    return [est for est in estudiantes if est["promedio"] >= nota_minima]

def estudiante_con_mejor_promedio(estudiantes):
    """Retorna el estudiante con mejor promedio"""
    if not estudiantes:
        return None
    return max(estudiantes, key=lambda x: x["promedio"])
```

**Archivo: ejemplos/01-basicos/test_estudiantes.py**
```python
import pytest
from estudiantes import (
    crear_estudiante,
    agregar_calificacion,
    obtener_estudiantes_aprobados,
    estudiante_con_mejor_promedio
)

@pytest.fixture
def estudiante_basico():
    """Fixture que crea un estudiante básico"""
    return crear_estudiante("Ana", 20, [80, 85, 90])

@pytest.fixture
def lista_estudiantes():
    """Fixture que crea una lista de estudiantes"""
    return [
        crear_estudiante("Ana", 20, [80, 85, 90]),
        crear_estudiante("Carlos", 22, [70, 75, 80]),
        crear_estudiante("Luis", 21, [50, 55, 60]),
        crear_estudiante("María", 23, [95, 98, 100]),
    ]

# Tests de creación
def test_crear_estudiante():
    estudiante = crear_estudiante("Pedro", 25, [70, 80, 90])

    assert estudiante["nombre"] == "Pedro"
    assert estudiante["edad"] == 25
    assert estudiante["calificaciones"] == [70, 80, 90]
    assert estudiante["promedio"] == 80

def test_crear_estudiante_sin_calificaciones():
    estudiante = crear_estudiante("Juan", 19, [])
    assert estudiante["promedio"] == 0

# Tests de agregar calificación
def test_agregar_calificacion(estudiante_basico):
    estudiante = agregar_calificacion(estudiante_basico, 95)

    assert 95 in estudiante["calificaciones"]
    assert len(estudiante["calificaciones"]) == 4
    assert estudiante["promedio"] == 87.5

# Tests de filtrado
def test_obtener_estudiantes_aprobados(lista_estudiantes):
    aprobados = obtener_estudiantes_aprobados(lista_estudiantes, 75)

    assert len(aprobados) == 2
    nombres = [est["nombre"] for est in aprobados]
    assert "Ana" in nombres
    assert "María" in nombres

def test_obtener_estudiantes_aprobados_lista_vacia():
    aprobados = obtener_estudiantes_aprobados([])
    assert aprobados == []

# Tests de mejor estudiante
def test_estudiante_con_mejor_promedio(lista_estudiantes):
    mejor = estudiante_con_mejor_promedio(lista_estudiantes)
    assert mejor["nombre"] == "María"
    assert mejor["promedio"] == 97.66666666666667

def test_mejor_estudiante_lista_vacia():
    mejor = estudiante_con_mejor_promedio([])
    assert mejor is None
```

## Testing de Excepciones Avanzado

### POC 6: Validador de Datos

**Archivo: ejemplos/01-basicos/validador_datos.py**
```python
class DatoInvalidoError(Exception):
    """Excepción personalizada para datos inválidos"""
    pass

def validar_email(email):
    """Valida formato de email"""
    if not email:
        raise DatoInvalidoError("El email no puede estar vacío")
    if "@" not in email:
        raise DatoInvalidoError("El email debe contener @")
    if "." not in email.split("@")[1]:
        raise DatoInvalidoError("El email debe tener un dominio válido")
    return True

def validar_telefono(telefono):
    """Valida formato de teléfono"""
    if not telefono:
        raise DatoInvalidoError("El teléfono no puede estar vacío")

    # Remover espacios y guiones
    telefono_limpio = telefono.replace(" ", "").replace("-", "")

    if not telefono_limpio.isdigit():
        raise DatoInvalidoError("El teléfono solo puede contener números")

    if len(telefono_limpio) < 10:
        raise DatoInvalidoError("El teléfono debe tener al menos 10 dígitos")

    return True

def dividir_seguro(a, b):
    """División con manejo de errores"""
    try:
        return a / b
    except ZeroDivisionError:
        raise DatoInvalidoError("No se puede dividir por cero")
    except TypeError:
        raise DatoInvalidoError("Los valores deben ser números")
```

**Archivo: ejemplos/01-basicos/test_validador_datos.py**
```python
import pytest
from validador_datos import (
    DatoInvalidoError,
    validar_email,
    validar_telefono,
    dividir_seguro
)

# Tests de validación de email
def test_email_valido():
    assert validar_email("usuario@ejemplo.com") == True

def test_email_vacio():
    with pytest.raises(DatoInvalidoError, match="no puede estar vacío"):
        validar_email("")

def test_email_sin_arroba():
    with pytest.raises(DatoInvalidoError, match="debe contener @"):
        validar_email("usuarioejemplo.com")

def test_email_sin_dominio():
    with pytest.raises(DatoInvalidoError, match="dominio válido"):
        validar_email("usuario@ejemplo")

# Tests de validación de teléfono
def test_telefono_valido():
    assert validar_telefono("1234567890") == True

def test_telefono_con_formato():
    assert validar_telefono("123-456-7890") == True
    assert validar_telefono("123 456 7890") == True

def test_telefono_vacio():
    with pytest.raises(DatoInvalidoError, match="no puede estar vacío"):
        validar_telefono("")

def test_telefono_con_letras():
    with pytest.raises(DatoInvalidoError, match="solo puede contener números"):
        validar_telefono("123abc7890")

def test_telefono_muy_corto():
    with pytest.raises(DatoInvalidoError, match="al menos 10 dígitos"):
        validar_telefono("12345")

# Tests de división segura
def test_dividir_seguro_normal():
    assert dividir_seguro(10, 2) == 5

def test_dividir_seguro_por_cero():
    with pytest.raises(DatoInvalidoError, match="dividir por cero"):
        dividir_seguro(10, 0)

def test_dividir_seguro_tipo_invalido():
    with pytest.raises(DatoInvalidoError, match="deben ser números"):
        dividir_seguro("10", 2)
```

## Fixtures Avanzadas: Setup y Teardown

### POC 7: Gestor de Archivos Temporal

**Archivo: ejemplos/01-basicos/test_archivos.py**
```python
import pytest
import os
import tempfile

@pytest.fixture
def archivo_temporal():
    """Crea un archivo temporal para testing"""
    # Setup: crear archivo
    archivo = tempfile.NamedTemporaryFile(mode='w', delete=False)
    archivo.write("Contenido de prueba")
    archivo.close()

    # Proveer el archivo al test
    yield archivo.name

    # Teardown: limpiar archivo
    if os.path.exists(archivo.name):
        os.remove(archivo.name)

@pytest.fixture
def directorio_temporal():
    """Crea un directorio temporal"""
    directorio = tempfile.mkdtemp()
    yield directorio
    # Limpiar directorio
    import shutil
    if os.path.exists(directorio):
        shutil.rmtree(directorio)

def test_leer_archivo(archivo_temporal):
    with open(archivo_temporal, 'r') as f:
        contenido = f.read()
    assert contenido == "Contenido de prueba"

def test_archivo_existe(archivo_temporal):
    assert os.path.exists(archivo_temporal)

def test_crear_archivo_en_directorio(directorio_temporal):
    ruta_archivo = os.path.join(directorio_temporal, "test.txt")
    with open(ruta_archivo, 'w') as f:
        f.write("Hola")

    assert os.path.exists(ruta_archivo)
```

## Markers - Organizando Tests

Los markers te permiten etiquetar y organizar tests.

**Archivo: ejemplos/01-basicos/test_markers.py**
```python
import pytest

@pytest.mark.rapido
def test_suma_rapida():
    assert 1 + 1 == 2

@pytest.mark.lento
def test_operacion_lenta():
    # Simula operación lenta
    import time
    time.sleep(0.1)
    assert True

@pytest.mark.skip(reason="Funcionalidad no implementada aún")
def test_no_implementado():
    assert False

@pytest.mark.skipif(pytest.__version__ < "7.0", reason="Requiere pytest 7+")
def test_requiere_version_nueva():
    assert True

@pytest.mark.xfail(reason="Bug conocido en producción")
def test_con_bug_conocido():
    assert 1 / 0  # Esto fallará, pero está marcado como esperado

# Ejecutar solo tests rápidos:
# pytest -m rapido

# Ejecutar todos excepto lentos:
# pytest -m "not lento"
```

## Ejercicios Prácticos

### Ejercicio 1: Conversor de Unidades
Crea funciones para convertir entre diferentes unidades y escribe tests parametrizados.

```python
# ejemplos/01-basicos/conversor.py
def celsius_a_fahrenheit(celsius):
    """Convierte Celsius a Fahrenheit"""
    pass

def kilometros_a_millas(km):
    """Convierte kilómetros a millas"""
    pass

def gramos_a_onzas(gramos):
    """Convierte gramos a onzas"""
    pass

# Escribe tests parametrizados con múltiples casos
```

### Ejercicio 2: Procesador de JSON
Crea funciones que procesen datos JSON y escribe tests con fixtures.

```python
# ejemplos/01-basicos/json_processor.py
def extraer_nombres(datos):
    """Extrae nombres de una lista de diccionarios"""
    pass

def filtrar_por_edad(datos, edad_minima):
    """Filtra personas mayores a cierta edad"""
    pass

# Crea fixtures con datos de prueba
```

### Ejercicio 3: Validador Completo
Crea un sistema de validación completo con excepciones personalizadas.

```python
# ejemplos/01-basicos/validador_completo.py
class ValidacionError(Exception):
    pass

def validar_usuario(datos):
    """
    Valida datos de usuario completos:
    - Nombre: no vacío, solo letras
    - Email: formato válido
    - Edad: entre 18 y 100
    - Teléfono: formato válido
    """
    pass

# Escribe tests que verifiquen todas las validaciones
```

## Resumen

En este módulo aprendiste:

- Testing de funciones puras
- Parametrización de tests con `@pytest.mark.parametrize`
- Uso de fixtures básicas y avanzadas
- Testing de strings y estructuras de datos
- Manejo avanzado de excepciones
- Setup y teardown con fixtures
- Organización de tests con markers
- Mejores prácticas para POCs de testing

## Próximos Pasos

En el siguiente módulo aprenderás sobre testing de código orientado a objetos:
- Testing de clases y objetos
- Testing de métodos
- Herencia y composición
- Métodos estáticos y de clase

---

**[⬅️ Módulo anterior](01-introduccion-testing-pytest.md) | [Volver al índice](../README.md) | [Siguiente: Módulo 3 - Test Unitarios con POO ➡️](03-test-unitarios-poo.md)**
