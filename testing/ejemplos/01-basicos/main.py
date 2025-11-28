import time
import asyncio
import re
from datetime import datetime
from functools import wraps
from typing import Dict, List, Optional

# 1. Unitarios Básicos (Asserts simples)
def sumar(a: int, b: int) -> int:
    return a + b

def dividir(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b

def es_palindromo(texto: str) -> bool:
    if not texto:
        return False
    limpio = ''.join(c.lower() for c in texto if c.isalnum())
    return limpio == limpio[::-1]

# 2. Unitarios con Mock (Dependencias Externas)
# Simula una llamada a una API externa
def obtener_datos_externos(url: str) -> Dict:
    # En un test real, esta función se mockearía para no hacer la petición real
    # Aquí simulamos que hace algo lento o complejo
    time.sleep(1) 
    return {"status": "ok", "data": [1, 2, 3]}

def procesar_datos(url: str) -> int:
    # Esta función depende de obtener_datos_externos
    respuesta = obtener_datos_externos(url)
    if respuesta["status"] != "ok":
        raise ConnectionError("Error al obtener datos")
    return sum(respuesta["data"])

# 3. Integración (Servicio + Base de Datos simulada)
class BaseDeDatos:
    def __init__(self):
        self.datos = {}

    def guardar(self, key: str, value: any):
        self.datos[key] = value

    def obtener(self, key: str):
        return self.datos.get(key)

class UsuarioService:
    def __init__(self, db: BaseDeDatos):
        self.db = db

    def crear_usuario(self, user_id: str, nombre: str):
        if not nombre:
            raise ValueError("Nombre requerido")
        self.db.guardar(user_id, {"nombre": nombre, "activo": True})
        return self.db.obtener(user_id)

# 4. A/B Logic Test
def obtener_mensaje_bienvenida(variante: str) -> str:
    if variante == "A":
        return "¡Bienvenido a nuestra plataforma!"
    elif variante == "B":
        return "Hola, gracias por visitarnos."
    else:
        return "Bienvenido" # Control

# 5. Stateful (Clase con estado)
class CuentaBancaria:
    def __init__(self, saldo_inicial: float = 0):
        self._saldo = saldo_inicial
        self._historial = []

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float):
        if monto <= 0:
            raise ValueError("Monto debe ser positivo")
        self._saldo += monto
        self._historial.append(f"Depósito: {monto}")

    def retirar(self, monto: float):
        if monto > self._saldo:
            raise ValueError("Fondos insuficientes")
        self._saldo -= monto
        self._historial.append(f"Retiro: {monto}")

# 6. E2E Simulation (Flujo Completo)
class SistemaCompras:
    def __init__(self):
        self.inventario = {"laptop": 10, "mouse": 50}
        self.carrito = []
        self.ordenes = []

    def buscar_producto(self, nombre: str) -> bool:
        return nombre in self.inventario and self.inventario[nombre] > 0

    def agregar_al_carrito(self, nombre: str, cantidad: int):
        if not self.buscar_producto(nombre):
            raise ValueError("Producto no disponible")
        if self.inventario[nombre] < cantidad:
            raise ValueError("Stock insuficiente")
        
        self.carrito.append({"producto": nombre, "cantidad": cantidad})

    def checkout(self) -> Dict:
        if not self.carrito:
            raise ValueError("Carrito vacío")
        
        total_items = 0
        for item in self.carrito:
            nombre = item["producto"]
            cantidad = item["cantidad"]
            self.inventario[nombre] -= cantidad
            total_items += cantidad
        
        orden = {"id": len(self.ordenes) + 1, "items": total_items, "status": "confirmado"}
        self.ordenes.append(orden)
        self.carrito = [] # Limpiar carrito
        return orden

# 7. Async/Await (Requiere pytest-asyncio)
async def obtener_clima(ciudad: str) -> str:
    # Simula una llamada asíncrona a una API
    await asyncio.sleep(0.1)
    if ciudad.lower() == "madrid":
        return "Soleado"
    return "Nublado"

async def planificar_viaje(ciudad: str) -> str:
    clima = await obtener_clima(ciudad)
    if clima == "Soleado":
        return "¡Vamos a la playa!"
    return "Mejor vamos al museo"

# 8. File I/O (Mocking open)
def guardar_log(mensaje: str, ruta_archivo: str):
    timestamp = datetime.now().isoformat()
    linea = f"[{timestamp}] {mensaje}\n"
    with open(ruta_archivo, 'a') as f:
        f.write(linea)

def leer_configuracion(ruta_archivo: str) -> Dict:
    config = {}
    try:
        with open(ruta_archivo, 'r') as f:
            for linea in f:
                if '=' in linea:
                    key, value = linea.strip().split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        return {} # Retorna config vacía si no existe
    return config

# 9. Date/Time (Mocking datetime)
def es_fin_de_semana() -> bool:
    hoy = datetime.now()
    # 5 = Sábado, 6 = Domingo
    return hoy.weekday() >= 5

def dias_hasta_navidad() -> int:
    hoy = datetime.now()
    navidad = datetime(hoy.year, 12, 25)
    if hoy > navidad:
        navidad = datetime(hoy.year + 1, 12, 25)
    return (navidad - hoy).days

# 10. Decoradores (Testing de wrappers)
def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Tiempo de ejecución: {end - start:.4f}s")
        return result
    return wrapper

@medir_tiempo
def operacion_lenta():
    time.sleep(0.1)
    return "Terminado"

# 11. Context Managers (Testing de __enter__ y __exit__)
class GestorArchivoSeguro:
    def __init__(self, ruta):
        self.ruta = ruta
        self.archivo = None

    def __enter__(self):
        print(f"Abriendo {self.ruta} de forma segura")
        self.archivo = open(self.ruta, 'w')
        return self.archivo

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.archivo:
            self.archivo.close()
        print("Archivo cerrado correctamente")
        if exc_type is ValueError:
            print("Capturada excepción de valor, suprimiendo...")
            return True # Suprime la excepción

# 12. Regex Parsing (Lógica compleja de strings)
def extraer_emails(texto: str) -> List[str]:
    patron = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(patron, texto)

def censurar_datos_sensibles(texto: str) -> str:
    # Reemplaza tarjetas de crédito (simuladas 16 dígitos)
    return re.sub(r'\d{4}-\d{4}-\d{4}-\d{4}', 'XXXX-XXXX-XXXX-XXXX', texto)

# 13. Integración: Sistema de Notificaciones
# Escenario: Un servicio de email que usa un motor de plantillas.
# Testear: Que el servicio llame al motor con los datos correctos y envíe el resultado.
class MotorPlantillas:
    def renderizar(self, plantilla: str, datos: Dict) -> str:
        # Simulación simple de renderizado
        resultado = plantilla
        for key, value in datos.items():
            resultado = resultado.replace(f"{{{{{key}}}}}", str(value))
        return resultado

class ServicioEmail:
    def __init__(self, motor: MotorPlantillas):
        self.motor = motor
        self.enviados = []

    def enviar_bienvenida(self, email: str, nombre: str):
        plantilla = "Hola {{nombre}}, bienvenido a nuestra plataforma."
        cuerpo = self.motor.renderizar(plantilla, {"nombre": nombre})
        
        # Simular envío
        email_data = {"to": email, "body": cuerpo, "status": "sent"}
        self.enviados.append(email_data)
        return email_data

# 14. Integración: Procesamiento de Pagos
# Escenario: Un procesador que coordina detección de fraude y pasarela bancaria.
# Testear: Flujos exitosos y casos donde falla el fraude o el banco.
class DetectorFraude:
    def es_sospechoso(self, transaccion: Dict) -> bool:
        # Lógica simple: sospechoso si monto > 10000
        return transaccion.get("monto", 0) > 10000

class PasarelaBancaria:
    def procesar(self, transaccion: Dict) -> bool:
        # Simula procesamiento
        return True

class ProcesadorPagos:
    def __init__(self, fraude: DetectorFraude, banco: PasarelaBancaria):
        self.fraude = fraude
        self.banco = banco

    def realizar_cobro(self, tarjeta: str, monto: float) -> str:
        transaccion = {"tarjeta": tarjeta, "monto": monto}
        
        if self.fraude.es_sospechoso(transaccion):
            raise ValueError("Transacción rechazada por sospecha de fraude")
            
        if self.banco.procesar(transaccion):
            return "Cobro exitoso"
        else:
            return "Error en pasarela bancaria"

# 15. Integración: Gestor de Contenidos (CMS)
# Escenario: Un gestor que intenta leer de caché antes de ir a la base de datos.
# Testear: Que se use la caché cuando existe, y que se actualice la caché al leer de DB.
class Cache:
    def __init__(self):
        self._store = {}
    
    def get(self, key: str):
        return self._store.get(key)
    
    def set(self, key: str, value: any):
        self._store[key] = value

class BaseDatosContenido:
    def obtener_articulo(self, id_articulo: str) -> Dict:
        # Simula DB
        return {"id": id_articulo, "titulo": "Título Demo", "cuerpo": "Contenido..."}

class GestorArticulos:
    def __init__(self, cache: Cache, db: BaseDatosContenido):
        self.cache = cache
        self.db = db

    def obtener_articulo(self, id_articulo: str) -> Dict:
        # 1. Intentar leer de caché
        cached = self.cache.get(id_articulo)
        if cached:
            return {**cached, "source": "cache"}
        
        # 2. Si no está, leer de DB
        articulo = self.db.obtener_articulo(id_articulo)
        
        # 3. Guardar en caché para la próxima
        self.cache.set(id_articulo, articulo)
        
        return {**articulo, "source": "db"}
