# Guía Rápida de Testing - Resumen del Curso

Esta guía te permitirá empezar rápidamente con testing en Python y JavaScript.

## Contenido

1. [Setup Rápido](#setup-rápido)
2. [Cheat Sheet de Pytest](#cheat-sheet-de-pytest)
3. [Cheat Sheet de Cypress](#cheat-sheet-de-cypress)
4. [Ejemplos Rápidos](#ejemplos-rápidos)
5. [Comandos Útiles](#comandos-útiles)

## Setup Rápido

Antes de comenzar a escribir pruebas, necesitamos preparar nuestro "taller" de trabajo. Aquí configuraremos las herramientas esenciales para que tanto Python como Cypress funcionen correctamente en tu equipo.

### Python + Pytest

Para mantener nuestro proyecto ordenado y evitar conflictos entre librerías, crearemos un entorno virtual aislado. Luego, instalaremos `pytest` y sus complementos, que serán nuestros instrumentos principales para el testing en Python.

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install pytest pytest-cov pytest-mock requests responses

# Verificar instalación
pytest --version
```

### Cypress

Cypress vive dentro del ecosistema de Node.js. En esta sección, inicializaremos un proyecto de Node y descargaremos Cypress, preparándolo para que puedas abrir su interfaz gráfica y ver tus tests en acción.

```bash
# Instalar Node.js primero (https://nodejs.org)

# Inicializar proyecto
npm init -y

# Instalar Cypress
npm install cypress --save-dev

# Abrir Cypress
npx cypress open
```

## Cheat Sheet de Pytest

Piensa en esto como tu "hoja de trucos" para el examen. Aquí tienes un resumen condensado de la sintaxis y las herramientas más poderosas de Pytest para que no tengas que memorizarlo todo.

### Estructura Básica

Todo test en Pytest sigue una regla de oro: es una función que empieza por `test_`. Si sigues esta convención, Pytest encontrará y ejecutará tus pruebas automáticamente sin que tengas que configurarlo.

```python
# test_ejemplo.py
def test_suma():
    resultado = 2 + 2
    assert resultado == 4
```

### Assertions Comunes

Las "assertions" o afirmaciones son el corazón de tus tests. Es la forma en que le dices a Python: "Espero que esto sea verdad". Si la afirmación se cumple, el test pasa; si no, falla y te avisa del error.

```python
# Igualdad
assert valor == esperado

# Booleanos
assert condicion
assert not condicion

# Pertenencia
assert elemento in lista
assert "texto" in cadena

# Comparaciones
assert x > y
assert x >= y
assert x < y
assert x <= y

# None
assert valor is None
assert valor is not None

# Excepciones
with pytest.raises(ValueError):
    funcion_que_falla()

with pytest.raises(ValueError, match="mensaje"):
    funcion_con_mensaje()
```

### Fixtures

Imagina que necesitas preparar una base de datos o crear un usuario antes de cada test. Las `fixtures` son funciones mágicas que se encargan de ese trabajo sucio de preparación (setup) y limpieza (teardown) para que tus tests se mantengan limpios y enfocados.

```python
import pytest

@pytest.fixture
def datos():
    return [1, 2, 3, 4, 5]

def test_con_fixture(datos):
    assert len(datos) == 5
```

### Parametrización

¿Tienes un test que quieres probar con 10 datos diferentes? En lugar de copiar y pegar el test 10 veces, usamos la parametrización. Escribes la lógica una vez y le pasas una lista de entradas y salidas esperadas. Es programación inteligente.

```python
@pytest.mark.parametrize("entrada,esperado", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_cuadrado(entrada, esperado):
    assert entrada ** 2 == esperado
```

### Mocking

A veces tus tests dependen de cosas externas como una API o una base de datos que pueden fallar o ser lentas. El "mocking" te permite crear imitaciones falsas de esos servicios para probar tu código en aislamiento, de forma rápida y segura.

```python
from unittest.mock import Mock, patch

# Mock simple
def test_mock_simple():
    mock = Mock()
    mock.metodo.return_value = "valor"
    assert mock.metodo() == "valor"

# Patch
@patch('modulo.funcion')
def test_con_patch(mock_funcion):
    mock_funcion.return_value = 42
    resultado = funcion_que_usa_funcion()
    assert resultado == 42
```

### Ejecutar Tests

Pytest es muy flexible. Puedes correr todos los tests de golpe, solo uno específico, o incluso aquellos que fallaron la última vez. Aquí aprenderás los comandos para tener el control total sobre qué se ejecuta.

```bash
# Todos los tests
pytest

# Con verbose
pytest -v

# Con prints
pytest -s

# Archivo específico
pytest tests/test_archivo.py

# Test específico
pytest tests/test_archivo.py::test_funcion

# Con cobertura
pytest --cov=src tests/

# Crear reporte HTML
pytest --cov=src --cov-report=html tests/
```

## Cheat Sheet de Cypress

Cypress es diferente porque se ejecuta en el navegador. Esta sección es tu referencia rápida para recordar cómo seleccionar elementos, interactuar con ellos y verificar que tu aplicación web se ve y comporta como esperas.

### Estructura Básica

En Cypress, organizamos los tests como historias. Usamos `describe` para agrupar pruebas relacionadas (como "Login") e `it` para definir cada escenario específico (como "debería entrar con clave correcta").

```javascript
describe('Mi Test', () => {
  it('debería hacer algo', () => {
    cy.visit('/')
    cy.get('[data-testid="elemento"]').click()
    cy.contains('Texto esperado')
  })
})
```

### Selectores

Para probar una web, primero necesitas encontrar los botones y campos. Cypress tiene muchas formas de hacerlo, pero te enseñaré las más robustas para que tus tests no se rompan cada vez que cambies un poco el diseño.

```javascript
// Por ID
cy.get('#id')

// Por clase
cy.get('.clase')

// Por atributo
cy.get('[data-testid="nombre"]')

// Por tipo
cy.get('input[type="email"]')

// Por texto
cy.contains('Texto')

// Primer/Último
cy.get('li').first()
cy.get('li').last()

// Por índice
cy.get('li').eq(2)
```

### Interacciones

Una vez que tienes el elemento, ¿qué haces con él? Aquí verás cómo simular las acciones de un usuario real: hacer clic, escribir texto, marcar casillas y elegir opciones de un menú.

```javascript
// Click
cy.get('button').click()

// Escribir
cy.get('input').type('texto')

// Limpiar y escribir
cy.get('input').clear().type('nuevo texto')

// Check/Uncheck
cy.get('[type="checkbox"]').check()
cy.get('[type="checkbox"]').uncheck()

// Select
cy.get('select').select('option-value')
```

### Assertions

Aquí es donde verificamos que la magia ocurrió. ¿Apareció el mensaje de éxito? ¿Cambió la URL? Las assertions en Cypress son muy legibles, casi como leer inglés: "debería ser visible", "debería tener texto", etc.

```javascript
// Visibilidad
cy.get('elemento').should('be.visible')
cy.get('elemento').should('not.be.visible')

// Contenido
cy.get('elemento').should('contain', 'texto')
cy.get('elemento').should('have.text', 'texto')

// Clases
cy.get('elemento').should('have.class', 'active')

// Atributos
cy.get('elemento').should('have.attr', 'href', '/url')

// Valor
cy.get('input').should('have.value', 'valor')

// URL
cy.url().should('include', '/dashboard')
cy.url().should('eq', 'http://localhost:3000/dashboard')
```

### Comandos Personalizados

Si te encuentras repitiendo el mismo código (como hacer login) en todos tus tests, es hora de crear un comando personalizado. Es como enseñar trucos nuevos a Cypress para reutilizarlos en cualquier parte.

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login')
  cy.get('[data-testid="email"]').type(email)
  cy.get('[data-testid="password"]').type(password)
  cy.get('[data-testid="submit"]').click()
})

// Uso
cy.login('user@email.com', 'password')
```

### Interceptar Requests

El frontend habla constantemente con el backend. Con `cy.intercept`, puedes espiar esas conversaciones o incluso "mentirle" al frontend simulando respuestas del servidor. Es vital para probar casos difíciles como errores de servidor.

```javascript
// Interceptar y esperar
cy.intercept('GET', '/api/usuarios').as('getUsuarios')
cy.visit('/usuarios')
cy.wait('@getUsuarios')

// Mockear respuesta
cy.intercept('GET', '/api/usuarios', {
  body: [{ id: 1, nombre: 'Mock' }]
})
```

## Ejemplos Rápidos

La teoría está muy bien, pero se aprende haciendo. Aquí tienes ejemplos completos de código real que puedes copiar, pegar y adaptar a tus propios proyectos.

### Python: Test Unitario Simple

Empecemos por lo básico: probar funciones puras. Verás cómo verificar que una suma da el resultado correcto o que una división por cero lanza el error adecuado.

```python
# src/calculadora.py
def sumar(a, b):
    return a + b

def dividir(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

# tests/test_calculadora.py
import pytest
from src.calculadora import sumar, dividir

def test_sumar():
    assert sumar(2, 3) == 5

def test_dividir():
    assert dividir(10, 2) == 5

def test_dividir_por_cero():
    with pytest.raises(ValueError):
        dividir(10, 0)
```

### Python: Test con Mock

Aquí subimos el nivel. Veremos cómo probar una función que hace una llamada a una API externa sin hacer la llamada real, usando `responses` para simular la respuesta.

```python
# src/servicio.py
import requests

def obtener_usuario(user_id):
    response = requests.get(f"https://api.com/users/{user_id}")
    return response.json()

# tests/test_servicio.py
import responses
from src.servicio import obtener_usuario

@responses.activate
def test_obtener_usuario():
    responses.add(
        responses.GET,
        "https://api.com/users/1",
        json={"id": 1, "nombre": "Juan"},
        status=200
    )

    usuario = obtener_usuario(1)
    assert usuario["nombre"] == "Juan"
```

### Python: Test de Clase

Las clases tienen estado (variables internas). Aprenderás a probar métodos que modifican ese estado, asegurándote de que tu objeto se comporte correctamente a lo largo de su vida.

```python
# src/cuenta.py
class CuentaBancaria:
    def __init__(self, saldo_inicial=0):
        self._saldo = saldo_inicial

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("Monto inválido")
        self._saldo += monto
        return self._saldo

# tests/test_cuenta.py
import pytest
from src.cuenta import CuentaBancaria

class TestCuentaBancaria:
    @pytest.fixture
    def cuenta(self):
        return CuentaBancaria(1000)

    def test_saldo_inicial(self, cuenta):
        assert cuenta.saldo == 1000

    def test_depositar(self, cuenta):
        cuenta.depositar(500)
        assert cuenta.saldo == 1500

    def test_depositar_monto_invalido(self, cuenta):
        with pytest.raises(ValueError):
            cuenta.depositar(-100)
```

### Python: Parametrización Avanzada

A veces un solo caso de prueba no basta. Aquí veremos cómo probar una función de validación de contraseñas con múltiples escenarios (muy corta, sin número, válida) usando `@pytest.mark.parametrize`.

```python
# src/auth.py
def validar_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True

# tests/test_auth.py
import pytest
from src.auth import validar_password

@pytest.mark.parametrize("password, es_valida", [
    ("corta", False),
    ("sin_numero", False),
    ("Password123", True),
    ("OtraClave99", True),
])
def test_validar_password(password, es_valida):
    assert validar_password(password) == es_valida
```

### Python: Fixtures con Setup/Teardown

Los tests profesionales a menudo necesitan limpiar lo que ensucian. Este ejemplo muestra cómo simular una conexión a base de datos que se abre antes del test y se cierra obligatoriamente al terminar.

```python
# tests/test_db.py
import pytest

class Database:
    def conectar(self):
        print("Conectando a DB...")
    
    def desconectar(self):
        print("Desconectando DB...")
    
    def guardar(self, dato):
        return True

@pytest.fixture
def db():
    database = Database()
    database.conectar()
    yield database
    database.desconectar()

def test_guardar_dato(db):
    assert db.guardar("usuario_nuevo") is True
```

### Cypress: Test de Login

El "Hola Mundo" de las pruebas web. Un flujo completo donde un usuario entra a la página, escribe sus credenciales y verifica que ha entrado al sistema (o que recibe un error si se equivoca).

```javascript
// cypress/e2e/login.cy.js
describe('Login', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('debería iniciar sesión correctamente', () => {
    cy.get('[data-testid="email"]').type('user@email.com')
    cy.get('[data-testid="password"]').type('password123')
    cy.get('[data-testid="submit"]').click()

    cy.url().should('include', '/dashboard')
    cy.contains('Bienvenido')
  })

  it('debería mostrar error con credenciales incorrectas', () => {
    cy.get('[data-testid="email"]').type('user@email.com')
    cy.get('[data-testid="password"]').type('wrong-password')
    cy.get('[data-testid="submit"]').click()

    cy.contains('Credenciales incorrectas')
  })
})
```

### Cypress: Test de CRUD

El pan de cada día en el desarrollo web. Probaremos el ciclo de vida completo de un dato: crearlo, leerlo en una lista, editarlo y finalmente eliminarlo.

```javascript
// cypress/e2e/crud.cy.js
describe('CRUD de Usuarios', () => {
  beforeEach(() => {
    cy.login('admin@email.com', 'admin123')
    cy.visit('/usuarios')
  })

  it('debería crear un usuario', () => {
    cy.get('[data-testid="btn-nuevo"]').click()
    cy.get('[data-testid="input-nombre"]').type('Nuevo Usuario')
    cy.get('[data-testid="input-email"]').type('nuevo@email.com')
    cy.get('[data-testid="btn-guardar"]').click()

    cy.contains('Usuario creado')
    cy.get('[data-testid="tabla"]').should('contain', 'Nuevo Usuario')
  })

  it('debería editar un usuario', () => {
    cy.get('[data-testid="btn-editar"]').first().click()
    cy.get('[data-testid="input-nombre"]').clear().type('Nombre Editado')
    cy.get('[data-testid="btn-guardar"]').click()

    cy.contains('Usuario actualizado')
  })

  it('debería eliminar un usuario', () => {
    cy.get('[data-testid="btn-eliminar"]').first().click()
    cy.get('[data-testid="btn-confirmar"]').click()

    cy.contains('Usuario eliminado')
  })
})
```

### Cypress: Test de API (Backend)

Cypress no es solo para el frontend. También puedes usarlo para probar tu API directamente, asegurándote de que el backend responde correctamente antes de siquiera abrir el navegador.

```javascript
// cypress/e2e/api.cy.js
describe('Pruebas de API', () => {
  it('debería obtener la lista de usuarios', () => {
    cy.request('GET', '/api/users')
      .then((response) => {
        expect(response.status).to.eq(200)
        expect(response.body).to.have.length.above(0)
        expect(response.body[0]).to.have.property('email')
      })
  })

  it('debería crear un usuario vía API', () => {
    cy.request('POST', '/api/users', {
      nombre: 'API User',
      email: 'api@test.com'
    }).then((response) => {
      expect(response.status).to.eq(201)
      expect(response.body.nombre).to.eq('API User')
    })
  })
})
```

### Cypress: Formularios Complejos

Los formularios reales tienen más que simples inputs de texto. Aquí practicaremos con checkboxes, radio buttons, selects y subida de archivos.

```javascript
// cypress/e2e/formulario.cy.js
describe('Formulario Completo', () => {
  it('debería llenar un formulario con diversos inputs', () => {
    cy.visit('/registro')

    // Radio button
    cy.get('[type="radio"]').check('developer')

    // Checkbox múltiple
    cy.get('[type="checkbox"]').check(['python', 'javascript'])

    // Select dropdown
    cy.get('select[name="pais"]').select('mexico')

    // Input de fecha
    cy.get('input[type="date"]').type('2023-01-01')

    // Subir archivo (requiere cypress-file-upload o selectFile en v9+)
    cy.get('input[type="file"]').selectFile('cypress/fixtures/foto.jpg')

    cy.get('form').submit()
    cy.contains('Registro exitoso')
  })
})
```

## Comandos Útiles

### Cypress: Test de Integración (Componente + API)

A veces queremos probar un componente aislado pero con datos reales o simulados del backend. Aquí probamos un componente de "Lista de Usuarios" interceptando la llamada a la API para asegurar que el componente renderiza lo que recibe.

```javascript
// cypress/e2e/integracion_lista.cy.js
describe('Integración: Lista de Usuarios', () => {
  it('debería mostrar usuarios obtenidos de la API', () => {
    // 1. Interceptamos la llamada y forzamos una respuesta
    cy.intercept('GET', '/api/users', {
      fixture: 'usuarios.json' // Usamos un archivo de datos fijos
    }).as('getUsers')

    // 2. Montamos o visitamos el componente
    cy.visit('/usuarios')

    // 3. Esperamos a que la "red" responda
    cy.wait('@getUsers')

    // 4. Verificamos la integración: Datos -> UI
    cy.get('[data-testid="user-card"]').should('have.length', 3)
    cy.contains('Usuario 1').should('be.visible')
  })
})
```

### Cypress: A/B Testing

Probar variantes A/B puede ser truculento. Aquí vemos cómo forzar una variante específica manipulando el `localStorage` o cookies antes de cargar la página, para asegurar que probamos ambas versiones de la interfaz.

```javascript
// cypress/e2e/ab_testing.cy.js
describe('A/B Testing: Botón de Compra', () => {
  it('debería mostrar el botón AZUL en la variante A', () => {
    // Forzamos variante A
    cy.visit('/', {
      onBeforeLoad: (win) => {
        win.localStorage.setItem('ab_test_variant', 'A')
      }
    })
    
    cy.get('[data-testid="btn-comprar"]')
      .should('have.css', 'background-color', 'rgb(0, 0, 255)') // Azul
  })

  it('debería mostrar el botón VERDE en la variante B', () => {
    // Forzamos variante B
    cy.visit('/', {
      onBeforeLoad: (win) => {
        win.localStorage.setItem('ab_test_variant', 'B')
      }
    })

    cy.get('[data-testid="btn-comprar"]')
      .should('have.css', 'background-color', 'rgb(0, 128, 0)') // Verde
  })
})
```

### Cypress: Test E2E Completo (Checkout)

Un flujo "End-to-End" real recorre múltiples páginas y acciones críticas. Este ejemplo simula un proceso de compra completo: desde buscar un producto hasta la confirmación de la orden.

```javascript
// cypress/e2e/checkout_flow.cy.js
describe('E2E: Flujo de Compra', () => {
  it('usuario puede buscar, añadir al carrito y pagar', () => {
    // 1. Home -> Búsqueda
    cy.visit('/')
    cy.get('input[name="search"]').type('Laptop{enter}')

    // 2. Resultados -> Detalle
    cy.contains('Laptop Pro').click()
    
    // 3. Detalle -> Carrito
    cy.get('[data-testid="add-to-cart"]').click()
    cy.get('[data-testid="cart-badge"]').should('contain', '1')
    cy.get('[data-testid="go-to-checkout"]').click()

    // 4. Checkout -> Formulario
    cy.get('input[name="address"]').type('Calle Falsa 123')
    cy.get('input[name="card"]').type('4242424242424242')
    cy.get('[data-testid="pay-button"]').click()

    // 5. Confirmación
    cy.url().should('include', '/order-confirmed')
    cy.contains('¡Gracias por tu compra!').should('be.visible')
  })
})
```

## Comandos Útiles

No necesitas memorizarlo todo. Guarda esta sección cerca para recordar esos comandos de terminal que usarás a diario para correr tus tests y depurar errores.

### Pytest

Desde correr tests en paralelo hasta generar reportes de cobertura. Estos son los "hechizos" de terminal que te harán más productivo con Pytest.

```bash
# Ejecutar tests
pytest                              # Todos
pytest tests/                       # Carpeta específica
pytest tests/test_archivo.py       # Archivo específico
pytest tests/test_archivo.py::test_funcion  # Test específico

# Opciones útiles
pytest -v                          # Verbose
pytest -s                          # Mostrar prints
pytest -x                          # Parar en primer fallo
pytest -k "nombre"                 # Ejecutar tests que contengan "nombre"
pytest -m "slow"                   # Ejecutar tests con marker "slow"

# Cobertura
pytest --cov=src                   # Cobertura de src/
pytest --cov=src --cov-report=html # Reporte HTML
pytest --cov=src --cov-report=term-missing  # Mostrar líneas faltantes

# Crear reporte
pytest --html=report.html          # Reporte HTML (requiere pytest-html)
```

### Cypress

Aprende a lanzar Cypress en modo visual para ver qué pasa, o en modo "headless" (sin ventana) para cuando quieras velocidad o integración continua.

```bash
# Ejecutar tests
npx cypress open                   # Modo interactivo
npx cypress run                    # Modo headless
npx cypress run --spec "cypress/e2e/login.cy.js"  # Archivo específico
npx cypress run --browser chrome   # Navegador específico

# Opciones útiles
npx cypress run --headed           # Ver navegador
npx cypress run --no-exit          # No cerrar después de tests
npx cypress run --record           # Grabar en Cypress Dashboard

# Scripts de package.json
npm run cy:open                    # cypress open
npm run cy:run                     # cypress run
npm run test:e2e                   # Tests E2E
```

## Mejores Prácticas

Escribir tests es un arte. Aquí te comparto los mandamientos que diferencian un test frágil y difícil de mantener de uno robusto que te da confianza en tu código.

### Testing General

Reglas universales que aplican sea cual sea el lenguaje. Hablaremos de la importancia de nombres claros, de probar una sola cosa a la vez y del patrón AAA.

1. **Nomenclatura clara**: Los nombres de tests deben explicar qué se está probando
2. **Un test, una cosa**: Cada test debe verificar una sola funcionalidad
3. **AAA Pattern**: Arrange (preparar), Act (actuar), Assert (afirmar)
4. **Tests independientes**: Los tests no deben depender unos de otros
5. **Tests rápidos**: Los tests unitarios deben ser muy rápidos

### Pytest

Consejos específicos para Python: cómo aprovechar al máximo las fixtures y por qué deberías preferir `assert` simples sobre métodos complicados.

1. Usa `data-testid` en lugar de clases CSS
2. Usa fixtures para setup/teardown
3. Parametriza tests con datos similares
4. Usa mocks para dependencias externas
5. Mantén los tests cerca del código

### Cypress

Trucos para evitar los errores más comunes en tests E2E, como esperar tiempos fijos (nunca uses `wait(1000)`) y cómo seleccionar elementos de forma inteligente.

1. Usa `data-testid` para selectores
2. Evita esperas fijas (`cy.wait(1000)`)
3. Crea comandos personalizados para acciones comunes
4. Usa interceptores para mockear APIs
5. Organiza tests por funcionalidad

## Recursos

El aprendizaje nunca termina. Aquí he recopilado los mejores libros, documentación oficial y cursos para cuando quieras profundizar más allá de esta guía.

### Documentación

Siempre ve a la fuente. La documentación oficial es la biblia de cualquier herramienta y aquí tienes los enlaces directos a las secciones más útiles.

- [Pytest Docs](https://docs.pytest.org/)
- [Cypress Docs](https://docs.cypress.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

### Libros

Si prefieres aprender con una estructura profunda, estos libros son lecturas obligatorias que te darán una base teórica y práctica muy sólida.

- "Python Testing with pytest" - Brian Okken
- "Test Driven Development with Python" - Harry Percival

### Cursos

Para los que aprenden mejor viendo y practicando, estos son los recursos interactivos que recomiendo para dominar el testing.

- [Real Python - Testing](https://realpython.com/pytest-python-testing/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)

## Conclusión

Esta guía rápida cubre los conceptos más importantes del curso. Para detalles completos, consulta los módulos individuales.

---

## Glosario

### Conceptos Generales

**Setup Rápido**
Proceso de configuración inicial del entorno de desarrollo. Incluye la instalación de lenguajes (Python, Node.js), herramientas de gestión de paquetes (pip, npm) y frameworks de testing. Es el paso previo indispensable para poder ejecutar cualquier prueba.

**Testing General**
Conjunto de prácticas y principios aplicables a cualquier tipo de prueba de software, independientemente del lenguaje o herramienta. Incluye conceptos como nomenclatura clara, aislamiento de tests y el patrón AAA (Arrange, Act, Assert).

**Mejores Prácticas**
Recomendaciones y estándares de la industria para escribir código de prueba mantenible, legible y eficiente. Seguir estas prácticas ayuda a evitar "flaky tests" (tests inestables) y deuda técnica.

**Recursos**
Material adicional para profundizar en el aprendizaje, incluyendo documentación oficial, libros recomendados y cursos online.

### Pytest (Python)

**Pytest**
Framework de testing para Python que facilita la escritura de pruebas simples y escalables. Es conocido por su sintaxis sencilla basada en `assert` y su potente sistema de fixtures.

**Cheat Sheet de Pytest**
Hoja de referencia rápida que resume la sintaxis más utilizada en Pytest, ideal para consultas rápidas durante el desarrollo.

**Entorno Virtual (venv)**
Herramienta para crear entornos aislados en Python. Permite instalar dependencias específicas para un proyecto sin afectar a otros proyectos o al sistema global.

**Assertions (Afirmaciones)**
Sentencias que verifican si una condición es verdadera. En Pytest, se usa la palabra clave `assert`. Si la condición es falsa, el test falla. Son el núcleo de cualquier prueba unitaria.

**Fixtures**
Funciones que preparan un contexto o estado inicial para los tests (setup) y opcionalmente limpian recursos después (teardown). Permiten reutilizar código de preparación y mantener los tests limpios.

**Parametrización**
Técnica que permite ejecutar la misma función de test múltiples veces con diferentes conjuntos de datos de entrada y resultados esperados. Reduce la duplicación de código.

**Mocking**
Técnica para reemplazar partes del sistema que se está probando (como llamadas a APIs o bases de datos) con objetos simulados (mocks). Esto aísla el código bajo prueba y permite simular diferentes escenarios (éxito, error, etc.) sin depender de sistemas externos.

**Cobertura (Coverage)**
Métrica que indica qué porcentaje del código fuente es ejecutado durante las pruebas. Ayuda a identificar partes del código que no están siendo testeadas.

### Cypress (JavaScript/E2E)

**Cypress**
Herramienta de testing "todo en uno" para pruebas End-to-End (E2E) en aplicaciones web modernas. Se ejecuta en el navegador y permite interactuar con la aplicación como lo haría un usuario real.

**Cheat Sheet de Cypress**
Resumen de los comandos y patrones más comunes en Cypress para interactuar con el DOM y realizar verificaciones.

**Estructura Básica (Describe/It)**
Sintaxis inspirada en Mocha para organizar tests. `describe` agrupa tests relacionados (suite) y `it` define un caso de prueba individual.

**Selectores**
Métodos para localizar elementos HTML en la página web (DOM). Cypress recomienda usar atributos dedicados como `data-testid` para hacer los selectores más robustos a cambios de diseño.

**Interacciones**
Acciones que simulan el comportamiento del usuario, como hacer clic (`.click()`), escribir en campos de texto (`.type()`), seleccionar opciones, etc.

**Assertions (Cypress)**
Validaciones sobre el estado de la aplicación o los elementos del DOM. Cypress usa encadenamiento de comandos (ej. `.should('be.visible')`) y espera automáticamente (retry-ability) hasta que la aserción se cumpla o se agote el tiempo.

**Comandos Personalizados**
Funciones definidas por el usuario que extienden la funcionalidad de Cypress. Son útiles para encapsular lógica repetitiva, como un flujo de login complejo.

**Interceptar Requests**
Capacidad de Cypress para espiar y modificar el tráfico de red (HTTP requests). Permite simular respuestas del backend (mocking) para probar el frontend de forma aislada y determinista.

**CRUD**
Acrónimo de Create, Read, Update, Delete (Crear, Leer, Actualizar, Borrar). Se refiere a las cuatro operaciones básicas de almacenamiento persistente. Los tests de CRUD verifican que estas operaciones funcionen correctamente en la aplicación.

---

**[⬅️ Volver al índice](README.md)**
