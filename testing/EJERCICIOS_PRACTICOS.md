# Ejercicios Prácticos y Proyectos

Este documento contiene ejercicios prácticos organizados por nivel de dificultad para que puedas practicar lo aprendido en el curso.

## Contenido

1. [Nivel Principiante](#nivel-principiante)
2. [Nivel Intermedio](#nivel-intermedio)
3. [Nivel Avanzado](#nivel-avanzado)
4. [Proyectos Completos](#proyectos-completos)

## Nivel Principiante

### Ejercicio 1: Calculadora Básica

**Objetivo**: Crear una calculadora con operaciones básicas y sus tests.

**Funcionalidades a implementar**:
```python
# calculadora.py
def sumar(a, b)
def restar(a, b)
def multiplicar(a, b)
def dividir(a, b)
def potencia(base, exponente)
def raiz_cuadrada(numero)
```

**Tests requeridos**:
- Operaciones con números positivos
- Operaciones con números negativos
- División por cero (debe lanzar excepción)
- Raíz cuadrada de número negativo (debe lanzar excepción)
- Usar parametrización para múltiples casos

**Pistas**:
```python
@pytest.mark.parametrize("a,b,esperado", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_sumar(a, b, esperado):
    assert sumar(a, b) == esperado
```

### Ejercicio 2: Validador de Datos

**Objetivo**: Crear validadores para diferentes tipos de datos.

**Funcionalidades**:
```python
def validar_email(email)
def validar_telefono(telefono)
def validar_rut(rut)  # o DNI, según tu país
def validar_tarjeta_credito(numero)
def validar_fecha(fecha_str, formato="%Y-%m-%d")
```

**Tests requeridos**:
- Casos válidos
- Casos inválidos
- Casos edge (vacíos, None, muy largos)
- Usar fixtures para datos de prueba

### Ejercicio 3: Conversor de Unidades

**Objetivo**: Crear conversores entre diferentes unidades.

**Funcionalidades**:
```python
# Temperatura
def celsius_a_fahrenheit(celsius)
def fahrenheit_a_celsius(fahrenheit)
def celsius_a_kelvin(celsius)

# Longitud
def kilometros_a_millas(km)
def metros_a_pies(metros)

# Peso
def kilogramos_a_libras(kg)
def gramos_a_onzas(gramos)
```

**Tests requeridos**:
- Conversiones conocidas
- Casos límite (cero, negativos)
- Precisión decimal

## Nivel Intermedio

### Ejercicio 4: Sistema de Inventario

**Objetivo**: Crear un sistema de gestión de inventario con POO.

**Clases a implementar**:
```python
class Producto:
    def __init__(self, id, nombre, precio, stock):
        pass

    def actualizar_precio(self, nuevo_precio):
        pass

    def hay_stock(self, cantidad):
        pass

class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        pass

    def eliminar_producto(self, producto_id):
        pass

    def buscar_por_nombre(self, nombre):
        pass

    def productos_bajo_stock(self, minimo=10):
        pass

    def valor_total_inventario(self):
        pass
```

**Tests requeridos**:
- Tests de cada método
- Tests de validaciones
- Tests de búsqueda
- Tests de cálculos
- Usar fixtures para productos de prueba

### Ejercicio 5: API Client con Mocking

**Objetivo**: Crear un cliente para consumir una API REST y testearlo con mocks.

**Clase a implementar**:
```python
class APIClient:
    def __init__(self, base_url, api_key):
        pass

    def get_usuarios(self):
        pass

    def get_usuario(self, user_id):
        pass

    def crear_usuario(self, data):
        pass

    def actualizar_usuario(self, user_id, data):
        pass

    def eliminar_usuario(self, user_id):
        pass

    def buscar_usuarios(self, query):
        pass
```

**Tests requeridos**:
- Mockear todas las requests con `responses`
- Testear respuestas exitosas
- Testear errores HTTP (404, 500, etc.)
- Testear timeout
- Testear respuestas malformadas

### Ejercicio 6: Sistema de Reservas

**Objetivo**: Sistema de reservas para hotel/restaurante.

**Clases**:
```python
class Reserva:
    def __init__(self, id, cliente, fecha, hora, personas):
        pass

    def cancelar(self):
        pass

    def confirmar(self):
        pass

class GestorReservas:
    def __init__(self, capacidad_maxima):
        pass

    def crear_reserva(self, cliente, fecha, hora, personas):
        pass

    def cancelar_reserva(self, reserva_id):
        pass

    def listar_reservas_dia(self, fecha):
        pass

    def disponibilidad(self, fecha, hora, personas):
        pass

    def capacidad_disponible(self, fecha, hora):
        pass
```

**Tests requeridos**:
- Tests de creación de reservas
- Validar capacidad máxima
- No permitir reservas duplicadas
- Tests de disponibilidad
- Tests de cancelaciones

## Ejercicios con Cypress

### Ejercicio 10: Formulario de Contacto

**Objetivo**: Validar el flujo completo de un formulario de contacto.

**Escenario**:
Tienes una página `/contacto` con campos: nombre, email, asunto, mensaje.

**Tests requeridos**:
- Llenar todos los campos correctamente y enviar.
- Verificar que aparece mensaje de éxito "Gracias por contactarnos".
- Intentar enviar con campos vacíos y verificar mensajes de error.
- Verificar que el email tenga formato válido.

### Ejercicio 11: Flujo de Compra (Frontend)

**Objetivo**: Simular la experiencia de usuario agregando productos al carrito.

**Escenario**:
Una página de e-commerce con lista de productos y un carrito.

**Tests requeridos**:
- Navegar a la lista de productos.
- Agregar 2 productos diferentes al carrito.
- Abrir el carrito y verificar que los productos están ahí.
- Verificar que el precio total es la suma correcta.
- Eliminar un producto y verificar que el total se actualiza.

### Ejercicio 12: Autenticación y Rutas Protegidas

**Objetivo**: Verificar seguridad y redirecciones en el frontend.

**Tests requeridos**:
- Intentar acceder a `/dashboard` sin estar logueado (debe redirigir a `/login`).
- Hacer login con credenciales válidas.
- Verificar redirección al `/dashboard`.
- Verificar que aparece el nombre del usuario.
- Hacer logout y verificar que ya no se puede acceder al dashboard.

## Nivel Avanzado

### Ejercicio 7: CRUD Completo con Base de Datos

**Objetivo**: Implementar CRUD completo con SQLite y tests de integración.

**Estructura**:
```python
# models/usuario.py
class Usuario:
    def __init__(self, id, nombre, email, password_hash):
        pass

    def verificar_password(self, password):
        pass

    @staticmethod
    def hash_password(password):
        pass

# repositories/usuario_repository.py
class UsuarioRepository:
    def __init__(self, db_connection):
        pass

    def crear(self, usuario):
        pass

    def obtener_por_id(self, user_id):
        pass

    def obtener_todos(self):
        pass

    def actualizar(self, usuario):
        pass

    def eliminar(self, user_id):
        pass

# services/usuario_service.py
class UsuarioService:
    def __init__(self, repository):
        pass

    def registrar_usuario(self, nombre, email, password):
        pass

    def autenticar(self, email, password):
        pass

    def cambiar_password(self, user_id, password_actual, password_nuevo):
        pass
```

**Tests requeridos**:
- Mock de base de datos
- Tests de cada operación CRUD
- Tests de validaciones
- Tests de autenticación
- Tests de integración completa

### Ejercicio 8: Sistema de E-commerce

**Objetivo**: Sistema de tienda online con carrito y órdenes.

**Clases principales**:
```python
class Producto:
    # id, nombre, precio, stock, categoria

class CarritoCompras:
    def agregar_producto(self, producto, cantidad)
    def eliminar_producto(self, producto_id)
    def actualizar_cantidad(self, producto_id, cantidad)
    def calcular_total(self)
    def aplicar_descuento(self, codigo)

class Orden:
    def __init__(self, cliente, items, total)
    def confirmar(self)
    def cancelar(self)

class ServicioOrdenes:
    def crear_orden_desde_carrito(self, carrito, cliente)
    def obtener_ordenes_cliente(self, cliente_id)
    def calcular_comision(self, orden)
```

**Tests requeridos**:
- Tests unitarios de cada clase
- Tests de integración del flujo completo
- Tests de descuentos
- Tests de stock
- Tests de cálculos

### Ejercicio 9: Sistema Bancario

**Objetivo**: Sistema bancario con transacciones y transferencias.

**Funcionalidades**:
```python
class Cuenta:
    def depositar(self, monto)
    def retirar(self, monto)
    def consultar_saldo(self)

class Transaccion:
    # Representa una transacción

class ServicioBancario:
    def transferir(self, cuenta_origen, cuenta_destino, monto)
    def historial_transacciones(self, cuenta_id)
    def calcular_interes(self, cuenta_id, tasa, periodo)
```

**Tests requeridos**:
- Tests de transacciones atómicas
- Tests de saldo insuficiente
- Tests de transferencias
- Tests de historial
- Mock de base de datos

## Proyectos Completos

### Proyecto 1: Todo List App (Fullstack)

**Backend (Python/Flask/FastAPI)**:
- CRUD de tareas
- Autenticación de usuarios
- Filtros y búsqueda
- Tests unitarios y de integración

**Frontend (React/Vue)**:
- Interfaz de lista de tareas
- Formularios de creación/edición
- Login/Registro
- Tests E2E con Cypress

**Tests requeridos**:
- Backend: pytest con >80% cobertura
- Frontend: Cypress para flujos completos
- Tests de API
- Tests de integración frontend-backend

### Proyecto 2: Blog Platform

**Backend**:
- CRUD de posts
- Sistema de comentarios
- Categorías y tags
- Sistema de usuarios (autores/lectores)

**Frontend**:
- Lista de posts
- Detalle de post
- Editor de posts (Markdown)
- Sistema de comentarios

**Tests requeridos**:
- Tests unitarios de modelos
- Tests de servicios con mocks
- Tests E2E de flujos de usuario
- Tests de permisos y autorización

### Proyecto 3: API de Gestión de Proyectos

**Funcionalidades**:
- Proyectos
- Tareas con estados (TODO, IN_PROGRESS, DONE)
- Asignación de usuarios
- Comentarios en tareas
- Dashboard con estadísticas

**Tests requeridos**:
- Tests de API con pytest
- Tests de modelos y relaciones
- Tests de cálculos de estadísticas
- Tests de permisos
- Mock de base de datos

### Proyecto 4: Sistema de Tickets/Soporte

**Backend**:
- CRUD de tickets
- Estados del ticket (abierto, en proceso, cerrado)
- Asignación de agentes
- Prioridades
- Historial de cambios

**Frontend**:
- Dashboard de tickets
- Vista de detalle
- Chat/comentarios
- Filtros avanzados

**Tests requeridos**:
- Tests de cambios de estado
- Tests de asignación
- Tests E2E de flujo completo
- Tests de notificaciones

## Retos Especiales

### Reto 1: TDD Estricto

**Objetivo**: Implementar una calculadora científica usando TDD puro.

**Reglas**:
1. Escribe el test primero
2. El test debe fallar
3. Escribe el código mínimo para pasar el test
4. Refactoriza
5. Repite

**Funciones a implementar**:
- Operaciones trigonométricas (sin, cos, tan)
- Logaritmos
- Factorial
- Combinaciones y permutaciones

### Reto 2: Testing de Performance

**Objetivo**: Crear tests que verifiquen performance.

```python
import time

def test_busqueda_rapida():
    start = time.time()
    resultado = buscar_en_lista_grande(elemento)
    end = time.time()

    assert end - start < 0.1  # Debe tomar menos de 100ms
```

Aplica a:
- Búsquedas en grandes datasets
- Algoritmos de ordenamiento
- Queries a base de datos

### Reto 3: Testing de Concurrencia

**Objetivo**: Testear código concurrente/asíncrono.

```python
import asyncio
import pytest

@pytest.mark.asyncio
async def test_operacion_asincrona():
    resultado = await funcion_asincrona()
    assert resultado == esperado
```

## Checklist de Buenas Prácticas

Usa este checklist para verificar tus proyectos:

**Tests Unitarios**:
- [ ] Cobertura >80%
- [ ] Tests independientes
- [ ] Nombres descriptivos
- [ ] Usa fixtures
- [ ] Usa parametrización
- [ ] Tests rápidos (<100ms cada uno)

**Tests de Integración**:
- [ ] Mock de dependencias externas
- [ ] Tests de flujos completos
- [ ] Manejo de errores
- [ ] Setup y teardown apropiados

**Tests E2E**:
- [ ] Usa data-testid
- [ ] Tests de flujos críticos
- [ ] Comandos personalizados
- [ ] Manejo de estados
- [ ] Tests de diferentes dispositivos

**General**:
- [ ] CI/CD configurado
- [ ] Tests en pre-commit
- [ ] Documentación de tests
- [ ] Tests de regresión
- [ ] Tests de seguridad

## Recursos para Practicar

### Datasets Públicos

- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - API fake para practicar
- [ReqRes](https://reqres.in/) - API de prueba
- [RandomUser](https://randomuser.me/) - Generador de usuarios aleatorios

### Katas de Testing

1. **FizzBuzz con TDD**
2. **Calculadora de impuestos**
3. **Validador de contraseñas**
4. **Parser de CSV**
5. **API client genérico**

### Proyectos Open Source

Contribuye a proyectos agregando tests:
- Busca issues etiquetados como "needs tests"
- Mejora cobertura de tests
- Agrega tests de regresión

## Soluciones y Feedback

Para cada ejercicio:

1. **Implementa tu solución**
2. **Escribe todos los tests**
3. **Verifica cobertura**
4. **Refactoriza**
5. **Compara con soluciones de la comunidad**

**Recursos de ayuda**:
- Stack Overflow
- GitHub Issues del curso
- Comunidad de Python/Testing
- Code Review en forums

## Conclusión

La práctica hace al maestro. Estos ejercicios están diseñados para:
- Reforzar conceptos del curso
- Practicar patrones comunes
- Desarrollar intuición para testing
- Crear portfolio de proyectos

**Recomendación**: Completa al menos un ejercicio de cada nivel antes de avanzar al siguiente.

---

**[⬅️ Volver al índice](README.md)**
