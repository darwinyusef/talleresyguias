# Módulo 3: Test Unitarios con POO

## Introducción

En este módulo aprenderás a testear código orientado a objetos. Veremos cómo testear clases, métodos, propiedades, herencia y otros conceptos importantes de POO.

## Testing de Clases Básicas

### POC 1: Clase Cuenta Bancaria

**Archivo: ejemplos/02-poo/cuenta_bancaria.py**
```python
class CuentaBancaria:
    """Representa una cuenta bancaria simple"""

    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self._saldo = saldo_inicial
        self._transacciones = []

    @property
    def saldo(self):
        """Obtiene el saldo actual"""
        return self._saldo

    def depositar(self, monto):
        """Deposita dinero en la cuenta"""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._saldo += monto
        self._transacciones.append(f"Depósito: +{monto}")
        return self._saldo

    def retirar(self, monto):
        """Retira dinero de la cuenta"""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= monto
        self._transacciones.append(f"Retiro: -{monto}")
        return self._saldo

    def transferir(self, otra_cuenta, monto):
        """Transfiere dinero a otra cuenta"""
        self.retirar(monto)
        otra_cuenta.depositar(monto)
        self._transacciones.append(f"Transferencia a {otra_cuenta.titular}: -{monto}")

    def obtener_historial(self):
        """Retorna el historial de transacciones"""
        return self._transacciones.copy()
```

**Archivo: ejemplos/02-poo/test_cuenta_bancaria.py**
```python
import pytest
from cuenta_bancaria import CuentaBancaria

class TestCuentaBancaria:
    """Suite de tests para CuentaBancaria"""

    @pytest.fixture
    def cuenta(self):
        """Fixture que crea una cuenta básica"""
        return CuentaBancaria("Juan Pérez", 1000)

    @pytest.fixture
    def cuenta_vacia(self):
        """Fixture que crea una cuenta sin saldo"""
        return CuentaBancaria("María García")

    # Tests del constructor
    def test_crear_cuenta_con_saldo_inicial(self):
        cuenta = CuentaBancaria("Pedro", 500)
        assert cuenta.titular == "Pedro"
        assert cuenta.saldo == 500

    def test_crear_cuenta_sin_saldo_inicial(self):
        cuenta = CuentaBancaria("Ana")
        assert cuenta.titular == "Ana"
        assert cuenta.saldo == 0

    # Tests de depósito
    def test_depositar_monto_valido(self, cuenta):
        nuevo_saldo = cuenta.depositar(500)
        assert nuevo_saldo == 1500
        assert cuenta.saldo == 1500

    def test_depositar_monto_cero(self, cuenta):
        with pytest.raises(ValueError, match="debe ser positivo"):
            cuenta.depositar(0)

    def test_depositar_monto_negativo(self, cuenta):
        with pytest.raises(ValueError, match="debe ser positivo"):
            cuenta.depositar(-100)

    # Tests de retiro
    def test_retirar_monto_valido(self, cuenta):
        nuevo_saldo = cuenta.retirar(300)
        assert nuevo_saldo == 700
        assert cuenta.saldo == 700

    def test_retirar_saldo_insuficiente(self, cuenta):
        with pytest.raises(ValueError, match="Saldo insuficiente"):
            cuenta.retirar(1500)

    def test_retirar_monto_negativo(self, cuenta):
        with pytest.raises(ValueError, match="debe ser positivo"):
            cuenta.retirar(-100)

    # Tests de transferencia
    def test_transferir_entre_cuentas(self, cuenta):
        otra_cuenta = CuentaBancaria("Carlos", 500)
        cuenta.transferir(otra_cuenta, 200)

        assert cuenta.saldo == 800
        assert otra_cuenta.saldo == 700

    def test_transferir_con_saldo_insuficiente(self, cuenta):
        otra_cuenta = CuentaBancaria("Carlos", 500)
        with pytest.raises(ValueError, match="Saldo insuficiente"):
            cuenta.transferir(otra_cuenta, 2000)

    # Tests de historial
    def test_historial_vacio_al_crear(self, cuenta_vacia):
        assert cuenta_vacia.obtener_historial() == []

    def test_historial_registra_transacciones(self, cuenta):
        cuenta.depositar(500)
        cuenta.retirar(200)

        historial = cuenta.obtener_historial()
        assert len(historial) == 2
        assert "Depósito: +500" in historial
        assert "Retiro: -200" in historial

    # Test de propiedad readonly
    def test_saldo_es_readonly(self, cuenta):
        with pytest.raises(AttributeError):
            cuenta.saldo = 5000  # Esto debería fallar
```

## Testing de Métodos Estáticos y de Clase

### POC 2: Clase Utilidades

**Archivo: ejemplos/02-poo/utilidades.py**
```python
class Utilidades:
    """Clase con métodos utilitarios"""

    # Variable de clase
    contador_instancias = 0

    def __init__(self):
        Utilidades.contador_instancias += 1

    @staticmethod
    def es_bisiesto(año):
        """Determina si un año es bisiesto"""
        if año % 400 == 0:
            return True
        if año % 100 == 0:
            return False
        if año % 4 == 0:
            return True
        return False

    @staticmethod
    def calcular_distancia(x1, y1, x2, y2):
        """Calcula la distancia entre dos puntos"""
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    @classmethod
    def obtener_contador(cls):
        """Obtiene el número de instancias creadas"""
        return cls.contador_instancias

    @classmethod
    def reiniciar_contador(cls):
        """Reinicia el contador de instancias"""
        cls.contador_instancias = 0
```

**Archivo: ejemplos/02-poo/test_utilidades.py**
```python
import pytest
from utilidades import Utilidades

class TestUtilidadesMetodosEstaticos:
    """Tests para métodos estáticos"""

    @pytest.mark.parametrize("año,esperado", [
        (2000, True),   # Divisible por 400
        (2020, True),   # Divisible por 4
        (2100, False),  # Divisible por 100 pero no por 400
        (2019, False),  # No divisible por 4
        (2024, True),   # Divisible por 4
    ])
    def test_es_bisiesto(self, año, esperado):
        assert Utilidades.es_bisiesto(año) == esperado

    def test_calcular_distancia_misma_posicion(self):
        distancia = Utilidades.calcular_distancia(0, 0, 0, 0)
        assert distancia == 0

    def test_calcular_distancia_horizontal(self):
        distancia = Utilidades.calcular_distancia(0, 0, 3, 0)
        assert distancia == 3

    def test_calcular_distancia_diagonal(self):
        distancia = Utilidades.calcular_distancia(0, 0, 3, 4)
        assert distancia == 5  # Triángulo 3-4-5

class TestUtilidadesMetodosClase:
    """Tests para métodos de clase"""

    def setup_method(self):
        """Se ejecuta antes de cada test"""
        Utilidades.reiniciar_contador()

    def test_contador_inicial_es_cero(self):
        assert Utilidades.obtener_contador() == 0

    def test_contador_incrementa_con_instancias(self):
        Utilidades()
        assert Utilidades.obtener_contador() == 1

        Utilidades()
        assert Utilidades.obtener_contador() == 2

    def test_reiniciar_contador(self):
        Utilidades()
        Utilidades()
        Utilidades.reiniciar_contador()
        assert Utilidades.obtener_contador() == 0
```

## Testing de Herencia

### POC 3: Jerarquía de Vehículos

**Archivo: ejemplos/02-poo/vehiculos.py**
```python
class Vehiculo:
    """Clase base para vehículos"""

    def __init__(self, marca, modelo, año):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self._kilometraje = 0

    @property
    def kilometraje(self):
        return self._kilometraje

    def conducir(self, kilometros):
        """Agrega kilómetros al vehículo"""
        if kilometros < 0:
            raise ValueError("Los kilómetros no pueden ser negativos")
        self._kilometraje += kilometros

    def descripcion(self):
        """Retorna una descripción del vehículo"""
        return f"{self.marca} {self.modelo} ({self.año})"

class Auto(Vehiculo):
    """Representa un automóvil"""

    def __init__(self, marca, modelo, año, num_puertas):
        super().__init__(marca, modelo, año)
        self.num_puertas = num_puertas

    def descripcion(self):
        """Descripción específica de auto"""
        return f"{super().descripcion()} - {self.num_puertas} puertas"

class Moto(Vehiculo):
    """Representa una motocicleta"""

    def __init__(self, marca, modelo, año, cilindrada):
        super().__init__(marca, modelo, año)
        self.cilindrada = cilindrada

    def descripcion(self):
        """Descripción específica de moto"""
        return f"{super().descripcion()} - {self.cilindrada}cc"

    def hacer_caballito(self):
        """Método específico de motos"""
        return "¡Haciendo caballito!"
```

**Archivo: ejemplos/02-poo/test_vehiculos.py**
```python
import pytest
from vehiculos import Vehiculo, Auto, Moto

class TestVehiculoBase:
    """Tests para la clase base Vehiculo"""

    @pytest.fixture
    def vehiculo(self):
        return Vehiculo("Toyota", "Corolla", 2020)

    def test_crear_vehiculo(self, vehiculo):
        assert vehiculo.marca == "Toyota"
        assert vehiculo.modelo == "Corolla"
        assert vehiculo.año == 2020
        assert vehiculo.kilometraje == 0

    def test_conducir_incrementa_kilometraje(self, vehiculo):
        vehiculo.conducir(100)
        assert vehiculo.kilometraje == 100

        vehiculo.conducir(50)
        assert vehiculo.kilometraje == 150

    def test_conducir_kilometros_negativos(self, vehiculo):
        with pytest.raises(ValueError, match="no pueden ser negativos"):
            vehiculo.conducir(-10)

    def test_descripcion(self, vehiculo):
        assert vehiculo.descripcion() == "Toyota Corolla (2020)"

class TestAuto:
    """Tests para la clase Auto"""

    @pytest.fixture
    def auto(self):
        return Auto("Honda", "Civic", 2021, 4)

    def test_crear_auto(self, auto):
        assert auto.marca == "Honda"
        assert auto.num_puertas == 4

    def test_auto_es_vehiculo(self, auto):
        assert isinstance(auto, Vehiculo)
        assert isinstance(auto, Auto)

    def test_auto_descripcion_incluye_puertas(self, auto):
        descripcion = auto.descripcion()
        assert "Honda Civic (2021)" in descripcion
        assert "4 puertas" in descripcion

    def test_auto_hereda_conducir(self, auto):
        auto.conducir(200)
        assert auto.kilometraje == 200

class TestMoto:
    """Tests para la clase Moto"""

    @pytest.fixture
    def moto(self):
        return Moto("Yamaha", "R1", 2022, 1000)

    def test_crear_moto(self, moto):
        assert moto.marca == "Yamaha"
        assert moto.cilindrada == 1000

    def test_moto_es_vehiculo(self, moto):
        assert isinstance(moto, Vehiculo)
        assert isinstance(moto, Moto)

    def test_moto_descripcion_incluye_cilindrada(self, moto):
        descripcion = moto.descripcion()
        assert "Yamaha R1 (2022)" in descripcion
        assert "1000cc" in descripcion

    def test_metodo_especifico_de_moto(self, moto):
        resultado = moto.hacer_caballito()
        assert resultado == "¡Haciendo caballito!"

    def test_auto_no_tiene_hacer_caballito(self):
        auto = Auto("Honda", "Civic", 2021, 4)
        assert not hasattr(auto, 'hacer_caballito')
```

## Testing de Composición

### POC 4: Sistema de Biblioteca

**Archivo: ejemplos/02-poo/biblioteca.py**
```python
from datetime import datetime, timedelta

class Libro:
    """Representa un libro"""

    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True

class Prestamo:
    """Representa un préstamo de libro"""

    def __init__(self, libro, usuario, dias=14):
        self.libro = libro
        self.usuario = usuario
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = self.fecha_prestamo + timedelta(days=dias)
        self.devuelto = False

    def esta_vencido(self):
        """Verifica si el préstamo está vencido"""
        return not self.devuelto and datetime.now() > self.fecha_devolucion

    def devolver(self):
        """Marca el libro como devuelto"""
        self.devuelto = True
        self.libro.disponible = True

class Biblioteca:
    """Gestiona libros y préstamos"""

    def __init__(self, nombre):
        self.nombre = nombre
        self.libros = []
        self.prestamos = []

    def agregar_libro(self, libro):
        """Agrega un libro a la biblioteca"""
        self.libros.append(libro)

    def buscar_libro(self, isbn):
        """Busca un libro por ISBN"""
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None

    def prestar_libro(self, isbn, usuario):
        """Presta un libro a un usuario"""
        libro = self.buscar_libro(isbn)

        if not libro:
            raise ValueError("Libro no encontrado")

        if not libro.disponible:
            raise ValueError("Libro no disponible")

        libro.disponible = False
        prestamo = Prestamo(libro, usuario)
        self.prestamos.append(prestamo)
        return prestamo

    def devolver_libro(self, isbn):
        """Devuelve un libro"""
        for prestamo in self.prestamos:
            if prestamo.libro.isbn == isbn and not prestamo.devuelto:
                prestamo.devolver()
                return True
        return False

    def obtener_prestamos_activos(self):
        """Retorna los préstamos activos"""
        return [p for p in self.prestamos if not p.devuelto]

    def obtener_libros_disponibles(self):
        """Retorna los libros disponibles"""
        return [libro for libro in self.libros if libro.disponible]
```

**Archivo: ejemplos/02-poo/test_biblioteca.py**
```python
import pytest
from datetime import datetime, timedelta
from biblioteca import Libro, Prestamo, Biblioteca

class TestLibro:
    """Tests para la clase Libro"""

    def test_crear_libro(self):
        libro = Libro("1984", "George Orwell", "12345")
        assert libro.titulo == "1984"
        assert libro.autor == "George Orwell"
        assert libro.isbn == "12345"
        assert libro.disponible == True

class TestPrestamo:
    """Tests para la clase Prestamo"""

    @pytest.fixture
    def libro(self):
        return Libro("El Quijote", "Cervantes", "11111")

    @pytest.fixture
    def prestamo(self, libro):
        return Prestamo(libro, "Juan", dias=7)

    def test_crear_prestamo(self, prestamo, libro):
        assert prestamo.libro == libro
        assert prestamo.usuario == "Juan"
        assert prestamo.devuelto == False

    def test_prestamo_no_esta_vencido_inicialmente(self, prestamo):
        assert prestamo.esta_vencido() == False

    def test_devolver_libro_marca_como_devuelto(self, prestamo, libro):
        prestamo.devolver()
        assert prestamo.devuelto == True
        assert libro.disponible == True

class TestBiblioteca:
    """Tests para la clase Biblioteca"""

    @pytest.fixture
    def biblioteca(self):
        return Biblioteca("Biblioteca Central")

    @pytest.fixture
    def libros_muestra(self):
        return [
            Libro("1984", "Orwell", "001"),
            Libro("El Quijote", "Cervantes", "002"),
            Libro("Cien años de soledad", "García Márquez", "003")
        ]

    def test_crear_biblioteca(self, biblioteca):
        assert biblioteca.nombre == "Biblioteca Central"
        assert len(biblioteca.libros) == 0
        assert len(biblioteca.prestamos) == 0

    def test_agregar_libro(self, biblioteca):
        libro = Libro("Test", "Autor", "999")
        biblioteca.agregar_libro(libro)
        assert len(biblioteca.libros) == 1
        assert libro in biblioteca.libros

    def test_buscar_libro_existente(self, biblioteca, libros_muestra):
        for libro in libros_muestra:
            biblioteca.agregar_libro(libro)

        libro_encontrado = biblioteca.buscar_libro("002")
        assert libro_encontrado is not None
        assert libro_encontrado.titulo == "El Quijote"

    def test_buscar_libro_inexistente(self, biblioteca):
        libro = biblioteca.buscar_libro("999")
        assert libro is None

    def test_prestar_libro_exitoso(self, biblioteca):
        libro = Libro("Test", "Autor", "001")
        biblioteca.agregar_libro(libro)

        prestamo = biblioteca.prestar_libro("001", "María")

        assert prestamo is not None
        assert prestamo.usuario == "María"
        assert libro.disponible == False
        assert len(biblioteca.prestamos) == 1

    def test_prestar_libro_no_existente(self, biblioteca):
        with pytest.raises(ValueError, match="no encontrado"):
            biblioteca.prestar_libro("999", "Usuario")

    def test_prestar_libro_no_disponible(self, biblioteca):
        libro = Libro("Test", "Autor", "001")
        biblioteca.agregar_libro(libro)
        biblioteca.prestar_libro("001", "Usuario1")

        with pytest.raises(ValueError, match="no disponible"):
            biblioteca.prestar_libro("001", "Usuario2")

    def test_devolver_libro(self, biblioteca):
        libro = Libro("Test", "Autor", "001")
        biblioteca.agregar_libro(libro)
        biblioteca.prestar_libro("001", "Usuario")

        resultado = biblioteca.devolver_libro("001")

        assert resultado == True
        assert libro.disponible == True

    def test_obtener_prestamos_activos(self, biblioteca, libros_muestra):
        for libro in libros_muestra:
            biblioteca.agregar_libro(libro)

        biblioteca.prestar_libro("001", "Usuario1")
        biblioteca.prestar_libro("002", "Usuario2")
        biblioteca.devolver_libro("001")

        activos = biblioteca.obtener_prestamos_activos()
        assert len(activos) == 1
        assert activos[0].libro.isbn == "002"

    def test_obtener_libros_disponibles(self, biblioteca, libros_muestra):
        for libro in libros_muestra:
            biblioteca.agregar_libro(libro)

        biblioteca.prestar_libro("001", "Usuario")

        disponibles = biblioteca.obtener_libros_disponibles()
        assert len(disponibles) == 2
        assert all(libro.isbn != "001" for libro in disponibles)
```

## Testing de Propiedades y Encapsulación

### POC 5: Clase Temperatura

**Archivo: ejemplos/02-poo/temperatura.py**
```python
class Temperatura:
    """Maneja conversiones de temperatura"""

    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """Obtiene temperatura en Celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, valor):
        """Establece temperatura en Celsius"""
        if valor < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self):
        """Obtiene temperatura en Fahrenheit"""
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, valor):
        """Establece temperatura desde Fahrenheit"""
        celsius = (valor - 32) * 5/9
        self.celsius = celsius  # Usa el setter de celsius para validación

    @property
    def kelvin(self):
        """Obtiene temperatura en Kelvin"""
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, valor):
        """Establece temperatura desde Kelvin"""
        if valor < 0:
            raise ValueError("Kelvin no puede ser negativo")
        self.celsius = valor - 273.15

    def __str__(self):
        return f"{self._celsius}°C ({self.fahrenheit}°F, {self.kelvin}K)"

    def __eq__(self, other):
        if not isinstance(other, Temperatura):
            return False
        return abs(self._celsius - other._celsius) < 0.01
```

**Archivo: ejemplos/02-poo/test_temperatura.py**
```python
import pytest
from temperatura import Temperatura

class TestTemperatura:
    """Tests para la clase Temperatura"""

    def test_crear_temperatura_default(self):
        temp = Temperatura()
        assert temp.celsius == 0

    def test_crear_temperatura_con_valor(self):
        temp = Temperatura(25)
        assert temp.celsius == 25

    # Tests de propiedad Celsius
    def test_set_celsius_valido(self):
        temp = Temperatura()
        temp.celsius = 100
        assert temp.celsius == 100

    def test_set_celsius_bajo_cero_absoluto(self):
        temp = Temperatura()
        with pytest.raises(ValueError, match="cero absoluto"):
            temp.celsius = -300

    # Tests de propiedad Fahrenheit
    @pytest.mark.parametrize("celsius,fahrenheit", [
        (0, 32),
        (100, 212),
        (-40, -40),
        (37, 98.6),
    ])
    def test_conversion_celsius_fahrenheit(self, celsius, fahrenheit):
        temp = Temperatura(celsius)
        assert abs(temp.fahrenheit - fahrenheit) < 0.1

    def test_set_fahrenheit(self):
        temp = Temperatura()
        temp.fahrenheit = 212
        assert abs(temp.celsius - 100) < 0.01

    # Tests de propiedad Kelvin
    @pytest.mark.parametrize("celsius,kelvin", [
        (0, 273.15),
        (100, 373.15),
        (-273.15, 0),
    ])
    def test_conversion_celsius_kelvin(self, celsius, kelvin):
        temp = Temperatura(celsius)
        assert abs(temp.kelvin - kelvin) < 0.01

    def test_set_kelvin(self):
        temp = Temperatura()
        temp.kelvin = 373.15
        assert abs(temp.celsius - 100) < 0.01

    def test_set_kelvin_negativo(self):
        temp = Temperatura()
        with pytest.raises(ValueError, match="no puede ser negativo"):
            temp.kelvin = -10

    # Tests de métodos especiales
    def test_str_representation(self):
        temp = Temperatura(25)
        string = str(temp)
        assert "25" in string
        assert "°C" in string

    def test_equality(self):
        temp1 = Temperatura(25)
        temp2 = Temperatura(25)
        temp3 = Temperatura(30)

        assert temp1 == temp2
        assert temp1 != temp3

    def test_equality_con_tipo_diferente(self):
        temp = Temperatura(25)
        assert temp != 25
        assert temp != "25°C"
```

## Setup y Teardown en Clases de Test

### POC 6: Gestión de Recursos

**Archivo: ejemplos/02-poo/test_setup_teardown.py**
```python
import pytest

class TestSetupTeardown:
    """Demuestra diferentes niveles de setup/teardown"""

    # Setup/Teardown de clase (se ejecuta una vez por clase)
    @classmethod
    def setup_class(cls):
        """Se ejecuta una vez antes de todos los tests"""
        cls.recurso_compartido = "Recurso global"
        print("\n🔧 Setup de clase")

    @classmethod
    def teardown_class(cls):
        """Se ejecuta una vez después de todos los tests"""
        print("\n🧹 Teardown de clase")

    # Setup/Teardown de método (se ejecuta antes/después de cada test)
    def setup_method(self, method):
        """Se ejecuta antes de cada test"""
        self.datos = []
        print(f"\n  ⚙️ Setup para {method.__name__}")

    def teardown_method(self, method):
        """Se ejecuta después de cada test"""
        self.datos.clear()
        print(f"\n  🗑️ Teardown para {method.__name__}")

    def test_primero(self):
        print("    ▶️ Ejecutando test_primero")
        self.datos.append(1)
        assert self.datos == [1]
        assert self.recurso_compartido == "Recurso global"

    def test_segundo(self):
        print("    ▶️ Ejecutando test_segundo")
        # Los datos están vacíos porque setup_method se ejecutó de nuevo
        assert self.datos == []
        self.datos.append(2)
        assert self.datos == [2]
```

## Ejercicios Prácticos

### Ejercicio 1: Sistema de Carrito de Compras

```python
# ejemplos/02-poo/carrito.py
class Producto:
    def __init__(self, nombre, precio, cantidad_disponible):
        pass

class ItemCarrito:
    def __init__(self, producto, cantidad):
        pass

    def calcular_subtotal(self):
        pass

class CarritoCompras:
    def __init__(self):
        self.items = []

    def agregar_producto(self, producto, cantidad):
        pass

    def eliminar_producto(self, producto):
        pass

    def calcular_total(self):
        pass

    def vaciar_carrito(self):
        pass

# Escribe tests para:
# - Agregar productos
# - Eliminar productos
# - Calcular totales
# - Validar stock
# - Vaciar carrito
```

### Ejercicio 2: Sistema de Empleados

```python
# ejemplos/02-poo/empleados.py
class Empleado:
    def __init__(self, nombre, salario_base):
        pass

    def calcular_salario(self):
        pass

class EmpleadoTiempoCompleto(Empleado):
    def __init__(self, nombre, salario_base, bono_anual):
        pass

    def calcular_salario(self):
        # Incluye bono
        pass

class EmpleadoMedioTiempo(Empleado):
    def __init__(self, nombre, tarifa_hora, horas_trabajadas):
        pass

    def calcular_salario(self):
        pass

class Empresa:
    def __init__(self):
        self.empleados = []

    def contratar(self, empleado):
        pass

    def despedir(self, empleado):
        pass

    def calcular_nomina_total(self):
        pass

# Escribe tests completos para herencia y composición
```

### Ejercicio 3: Juego de Cartas

```python
# ejemplos/02-poo/cartas.py
class Carta:
    def __init__(self, valor, palo):
        pass

class Baraja:
    def __init__(self):
        pass

    def mezclar(self):
        pass

    def repartir_carta(self):
        pass

    def cartas_restantes(self):
        pass

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []

    def recibir_carta(self, carta):
        pass

    def jugar_carta(self, indice):
        pass

# Escribe tests para juego de cartas completo
```

## Resumen

En este módulo aprendiste:

- Testing de clases y objetos
- Testing de propiedades y encapsulación
- Testing de métodos estáticos y de clase
- Testing de herencia
- Testing de composición
- Setup y teardown en clases de test
- Organización de suites de tests
- Fixtures específicas para POO

## Próximos Pasos

En el siguiente módulo aprenderás sobre testing de servicios:
- Testing de APIs HTTP
- Mocking de requests
- Testing asíncrono
- Testing de respuestas JSON

---

**[⬅️ Módulo anterior](02-test-unitarios-basicos.md) | [Volver al índice](../README.md) | [Siguiente: Módulo 4 - Test Unitarios a Servicios ➡️](04-test-unitarios-servicios.md)**
