import pytest
import asyncio
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime
from main import (
    # 1. Unitarios Básicos
    sumar, dividir, es_palindromo,
    # 2. Unitarios con Mock
    obtener_datos_externos, procesar_datos,
    # 3. Integración
    BaseDeDatos, UsuarioService,
    # 4. A/B Logic
    obtener_mensaje_bienvenida,
    # 5. Stateful
    CuentaBancaria,
    # 6. E2E Simulation
    SistemaCompras,
    # 7. Async/Await
    obtener_clima, planificar_viaje,
    # 8. File I/O
    guardar_log, leer_configuracion,
    # 9. Date/Time
    es_fin_de_semana, dias_hasta_navidad,
    # 10. Decoradores
    medir_tiempo, operacion_lenta,
    # 11. Context Managers
    GestorArchivoSeguro,
    # 12. Regex Parsing
    extraer_emails, censurar_datos_sensibles,
    # 13. Sistema de Notificaciones
    MotorPlantillas, ServicioEmail,
    # 14. Procesamiento de Pagos
    DetectorFraude, PasarelaBancaria, ProcesadorPagos,
    # 15. Gestor de Contenidos
    Cache, BaseDatosContenido, GestorArticulos
)


# ============================================================================
# 1. TESTS UNITARIOS BÁSICOS (Asserts simples)
# ============================================================================

class TestUnitariosBasicos:
    """Tests básicos con asserts simples"""
    
    def test_sumar_numeros_positivos(self):
        """Verifica que la suma de números positivos funcione correctamente"""
        assert sumar(2, 3) == 5
        assert sumar(10, 20) == 30
    
    def test_sumar_numeros_negativos(self):
        """Verifica que la suma con números negativos funcione"""
        assert sumar(-5, -3) == -8
        assert sumar(-10, 5) == -5
    
    def test_dividir_numeros_validos(self):
        """Verifica la división de números válidos"""
        assert dividir(10, 2) == 5.0
        assert dividir(9, 3) == 3.0
    
    def test_dividir_por_cero_lanza_error(self):
        """Verifica que dividir por cero lance ValueError"""
        with pytest.raises(ValueError, match="No se puede dividir por cero"):
            dividir(10, 0)
    
    def test_es_palindromo_texto_valido(self):
        """Verifica que detecte palíndromos correctamente"""
        assert es_palindromo("anilina") == True
        assert es_palindromo("Anita lava la tina") == True
        assert es_palindromo("A man a plan a canal Panama") == True
    
    def test_es_palindromo_texto_invalido(self):
        """Verifica que rechace textos que no son palíndromos"""
        assert es_palindromo("hola") == False
        assert es_palindromo("python") == False
    
    def test_es_palindromo_texto_vacio(self):
        """Verifica que texto vacío retorne False"""
        assert es_palindromo("") == False


# ============================================================================
# 2. TESTS UNITARIOS CON MOCK (Dependencias Externas)
# ============================================================================

class TestUnitariosConMock:
    """Tests que usan mocks para simular dependencias externas"""
    
    @patch('main.obtener_datos_externos')
    def test_procesar_datos_exitoso(self, mock_obtener):
        """Verifica que procesar_datos funcione con respuesta exitosa"""
        # Configurar el mock
        mock_obtener.return_value = {"status": "ok", "data": [10, 20, 30]}
        
        resultado = procesar_datos("http://api.example.com")
        
        assert resultado == 60
        mock_obtener.assert_called_once_with("http://api.example.com")
    
    @patch('main.obtener_datos_externos')
    def test_procesar_datos_error_conexion(self, mock_obtener):
        """Verifica que lance error cuando el status no es 'ok'"""
        mock_obtener.return_value = {"status": "error", "data": []}
        
        with pytest.raises(ConnectionError, match="Error al obtener datos"):
            procesar_datos("http://api.example.com")
    
    @patch('main.time.sleep')
    @patch('main.obtener_datos_externos')
    def test_obtener_datos_externos_sin_espera(self, mock_obtener, mock_sleep):
        """Verifica que podemos mockear time.sleep para tests rápidos"""
        # Evitamos que el test espere 1 segundo
        mock_obtener.return_value = {"status": "ok", "data": [1, 2, 3]}
        
        resultado = obtener_datos_externos("http://test.com")
        
        assert resultado["status"] == "ok"
        assert resultado["data"] == [1, 2, 3]


# ============================================================================
# 3. TESTS DE INTEGRACIÓN (Servicio + Base de Datos)
# ============================================================================

class TestIntegracion:
    """Tests de integración entre servicios y base de datos"""
    
    def test_crear_usuario_exitoso(self):
        """Verifica que se pueda crear un usuario correctamente"""
        db = BaseDeDatos()
        servicio = UsuarioService(db)
        
        usuario = servicio.crear_usuario("user123", "Juan Pérez")
        
        assert usuario["nombre"] == "Juan Pérez"
        assert usuario["activo"] == True
        assert db.obtener("user123") == usuario
    
    def test_crear_usuario_sin_nombre_lanza_error(self):
        """Verifica que lance error si el nombre está vacío"""
        db = BaseDeDatos()
        servicio = UsuarioService(db)
        
        with pytest.raises(ValueError, match="Nombre requerido"):
            servicio.crear_usuario("user123", "")
    
    def test_base_datos_guardar_y_obtener(self):
        """Verifica operaciones básicas de la base de datos"""
        db = BaseDeDatos()
        
        db.guardar("key1", "valor1")
        db.guardar("key2", {"dato": "complejo"})
        
        assert db.obtener("key1") == "valor1"
        assert db.obtener("key2") == {"dato": "complejo"}
        assert db.obtener("key_inexistente") is None


# ============================================================================
# 4. TESTS DE LÓGICA A/B
# ============================================================================

class TestABLogic:
    """Tests para lógica de A/B testing"""
    
    def test_mensaje_variante_a(self):
        """Verifica el mensaje de la variante A"""
        mensaje = obtener_mensaje_bienvenida("A")
        assert mensaje == "¡Bienvenido a nuestra plataforma!"
    
    def test_mensaje_variante_b(self):
        """Verifica el mensaje de la variante B"""
        mensaje = obtener_mensaje_bienvenida("B")
        assert mensaje == "Hola, gracias por visitarnos."
    
    def test_mensaje_control(self):
        """Verifica el mensaje de control (default)"""
        mensaje = obtener_mensaje_bienvenida("C")
        assert mensaje == "Bienvenido"
        
        mensaje = obtener_mensaje_bienvenida("cualquier_cosa")
        assert mensaje == "Bienvenido"


# ============================================================================
# 5. TESTS STATEFUL (Clases con estado)
# ============================================================================

class TestStateful:
    """Tests para clases que mantienen estado"""
    
    def test_cuenta_bancaria_saldo_inicial(self):
        """Verifica el saldo inicial de una cuenta"""
        cuenta = CuentaBancaria(1000)
        assert cuenta.saldo == 1000
    
    def test_cuenta_bancaria_depositar(self):
        """Verifica que se pueda depositar dinero"""
        cuenta = CuentaBancaria(500)
        cuenta.depositar(200)
        
        assert cuenta.saldo == 700
    
    def test_cuenta_bancaria_retirar(self):
        """Verifica que se pueda retirar dinero"""
        cuenta = CuentaBancaria(1000)
        cuenta.retirar(300)
        
        assert cuenta.saldo == 700
    
    def test_cuenta_bancaria_depositar_monto_invalido(self):
        """Verifica que no se pueda depositar montos negativos o cero"""
        cuenta = CuentaBancaria(500)
        
        with pytest.raises(ValueError, match="Monto debe ser positivo"):
            cuenta.depositar(0)
        
        with pytest.raises(ValueError, match="Monto debe ser positivo"):
            cuenta.depositar(-100)
    
    def test_cuenta_bancaria_fondos_insuficientes(self):
        """Verifica que no se pueda retirar más de lo disponible"""
        cuenta = CuentaBancaria(100)
        
        with pytest.raises(ValueError, match="Fondos insuficientes"):
            cuenta.retirar(200)
    
    def test_cuenta_bancaria_multiples_operaciones(self):
        """Verifica múltiples operaciones en secuencia"""
        cuenta = CuentaBancaria(1000)
        
        cuenta.depositar(500)  # 1500
        cuenta.retirar(300)    # 1200
        cuenta.depositar(200)  # 1400
        cuenta.retirar(100)    # 1300
        
        assert cuenta.saldo == 1300


# ============================================================================
# 6. TESTS E2E SIMULATION (Flujo Completo)
# ============================================================================

class TestE2ESimulation:
    """Tests que simulan flujos end-to-end completos"""
    
    def test_flujo_compra_completo(self):
        """Verifica el flujo completo de una compra"""
        sistema = SistemaCompras()
        
        # 1. Buscar producto
        assert sistema.buscar_producto("laptop") == True
        
        # 2. Agregar al carrito
        sistema.agregar_al_carrito("laptop", 2)
        sistema.agregar_al_carrito("mouse", 3)
        
        # 3. Realizar checkout
        orden = sistema.checkout()
        
        assert orden["id"] == 1
        assert orden["items"] == 5
        assert orden["status"] == "confirmado"
        
        # 4. Verificar que el inventario se actualizó
        assert sistema.inventario["laptop"] == 8
        assert sistema.inventario["mouse"] == 47
        
        # 5. Verificar que el carrito se vació
        assert len(sistema.carrito) == 0
    
    def test_agregar_producto_no_disponible(self):
        """Verifica que no se pueda agregar producto inexistente"""
        sistema = SistemaCompras()
        
        with pytest.raises(ValueError, match="Producto no disponible"):
            sistema.agregar_al_carrito("tablet", 1)
    
    def test_agregar_producto_stock_insuficiente(self):
        """Verifica que no se pueda agregar más cantidad que el stock"""
        sistema = SistemaCompras()
        
        with pytest.raises(ValueError, match="Stock insuficiente"):
            sistema.agregar_al_carrito("laptop", 20)
    
    def test_checkout_carrito_vacio(self):
        """Verifica que no se pueda hacer checkout con carrito vacío"""
        sistema = SistemaCompras()
        
        with pytest.raises(ValueError, match="Carrito vacío"):
            sistema.checkout()


# ============================================================================
# 7. TESTS ASYNC/AWAIT
# ============================================================================

class TestAsyncAwait:
    """Tests para funciones asíncronas"""
    
    @pytest.mark.asyncio
    async def test_obtener_clima_madrid(self):
        """Verifica que obtener_clima retorne 'Soleado' para Madrid"""
        clima = await obtener_clima("Madrid")
        assert clima == "Soleado"
    
    @pytest.mark.asyncio
    async def test_obtener_clima_otra_ciudad(self):
        """Verifica que obtener_clima retorne 'Nublado' para otras ciudades"""
        clima = await obtener_clima("Barcelona")
        assert clima == "Nublado"
    
    @pytest.mark.asyncio
    async def test_planificar_viaje_madrid(self):
        """Verifica la planificación de viaje a Madrid"""
        plan = await planificar_viaje("Madrid")
        assert plan == "¡Vamos a la playa!"
    
    @pytest.mark.asyncio
    async def test_planificar_viaje_otra_ciudad(self):
        """Verifica la planificación de viaje a otra ciudad"""
        plan = await planificar_viaje("Londres")
        assert plan == "Mejor vamos al museo"


# ============================================================================
# 8. TESTS FILE I/O (Mocking open)
# ============================================================================

class TestFileIO:
    """Tests para operaciones de archivos usando mocks"""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('main.datetime')
    def test_guardar_log(self, mock_datetime, mock_file):
        """Verifica que se guarde el log correctamente"""
        # Mock de datetime
        mock_datetime.now.return_value.isoformat.return_value = "2024-01-15T10:30:00"
        
        guardar_log("Test mensaje", "/tmp/test.log")
        
        # Verificar que se abrió el archivo en modo append
        mock_file.assert_called_once_with("/tmp/test.log", 'a')
        
        # Verificar que se escribió el contenido correcto
        mock_file().write.assert_called_once_with("[2024-01-15T10:30:00] Test mensaje\n")
    
    @patch('builtins.open', new_callable=mock_open, read_data="host=localhost\nport=5432\ndb=test")
    def test_leer_configuracion_exitoso(self, mock_file):
        """Verifica que se lea la configuración correctamente"""
        config = leer_configuracion("/tmp/config.txt")
        
        assert config["host"] == "localhost"
        assert config["port"] == "5432"
        assert config["db"] == "test"
        
        mock_file.assert_called_once_with("/tmp/config.txt", 'r')
    
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_leer_configuracion_archivo_no_existe(self, mock_file):
        """Verifica que retorne dict vacío si el archivo no existe"""
        config = leer_configuracion("/tmp/noexiste.txt")
        
        assert config == {}


# ============================================================================
# 9. TESTS DATE/TIME (Mocking datetime)
# ============================================================================

class TestDateTime:
    """Tests para funciones que dependen de fecha/hora"""
    
    @patch('main.datetime')
    def test_es_fin_de_semana_sabado(self, mock_datetime):
        """Verifica que detecte sábado como fin de semana"""
        # Sábado (weekday = 5)
        mock_datetime.now.return_value.weekday.return_value = 5
        
        assert es_fin_de_semana() == True
    
    @patch('main.datetime')
    def test_es_fin_de_semana_domingo(self, mock_datetime):
        """Verifica que detecte domingo como fin de semana"""
        # Domingo (weekday = 6)
        mock_datetime.now.return_value.weekday.return_value = 6
        
        assert es_fin_de_semana() == True
    
    @patch('main.datetime')
    def test_no_es_fin_de_semana(self, mock_datetime):
        """Verifica que detecte días laborales correctamente"""
        # Lunes (weekday = 0)
        mock_datetime.now.return_value.weekday.return_value = 0
        
        assert es_fin_de_semana() == False
    
    @patch('main.datetime')
    def test_dias_hasta_navidad_antes(self, mock_datetime):
        """Verifica cálculo de días hasta navidad (antes de navidad)"""
        # Simulamos que estamos el 1 de diciembre
        mock_datetime.now.return_value = datetime(2024, 12, 1)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        dias = dias_hasta_navidad()
        
        assert dias == 24
    
    @patch('main.datetime')
    def test_dias_hasta_navidad_despues(self, mock_datetime):
        """Verifica cálculo de días hasta navidad (después de navidad)"""
        # Simulamos que estamos el 26 de diciembre
        mock_datetime.now.return_value = datetime(2024, 12, 26)
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        dias = dias_hasta_navidad()
        
        # Debería calcular para la navidad del próximo año
        assert dias == 364


# ============================================================================
# 10. TESTS DE DECORADORES
# ============================================================================

class TestDecoradores:
    """Tests para decoradores y wrappers"""
    
    @patch('builtins.print')
    @patch('main.time.time')
    @patch('main.time.sleep')
    def test_medir_tiempo_decorador(self, mock_sleep, mock_time, mock_print):
        """Verifica que el decorador mida el tiempo correctamente"""
        # Simular tiempos
        mock_time.side_effect = [100.0, 100.5]  # start y end
        
        resultado = operacion_lenta()
        
        assert resultado == "Terminado"
        # Verificar que se imprimió el tiempo
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "Tiempo de ejecución" in call_args
    
    def test_decorador_personalizado(self):
        """Verifica que podemos crear y testear decoradores personalizados"""
        llamadas = []
        
        def registrar_llamadas(func):
            def wrapper(*args, **kwargs):
                llamadas.append(func.__name__)
                return func(*args, **kwargs)
            return wrapper
        
        @registrar_llamadas
        def funcion_test():
            return "resultado"
        
        resultado = funcion_test()
        
        assert resultado == "resultado"
        assert "funcion_test" in llamadas


# ============================================================================
# 11. TESTS DE CONTEXT MANAGERS
# ============================================================================

class TestContextManagers:
    """Tests para context managers"""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_gestor_archivo_seguro_normal(self, mock_print, mock_file):
        """Verifica el funcionamiento normal del context manager"""
        with GestorArchivoSeguro("/tmp/test.txt") as f:
            f.write("contenido")
        
        # Verificar que se abrió y cerró el archivo
        mock_file.assert_called_once_with("/tmp/test.txt", 'w')
        mock_file().close.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.print')
    def test_gestor_archivo_seguro_con_excepcion_suprimida(self, mock_print, mock_file):
        """Verifica que el context manager suprima ValueError"""
        try:
            with GestorArchivoSeguro("/tmp/test.txt") as f:
                raise ValueError("Error de prueba")
        except ValueError:
            pytest.fail("ValueError no debería propagarse")
        
        # Verificar que se cerró el archivo
        mock_file().close.assert_called_once()


# ============================================================================
# 12. TESTS DE REGEX PARSING
# ============================================================================

class TestRegexParsing:
    """Tests para funciones que usan expresiones regulares"""
    
    def test_extraer_emails_multiples(self):
        """Verifica que extraiga múltiples emails correctamente"""
        texto = "Contacta a juan@example.com o maria@test.org para más info"
        emails = extraer_emails(texto)
        
        assert len(emails) == 2
        assert "juan@example.com" in emails
        assert "maria@test.org" in emails
    
    def test_extraer_emails_sin_emails(self):
        """Verifica que retorne lista vacía si no hay emails"""
        texto = "Este texto no contiene emails"
        emails = extraer_emails(texto)
        
        assert emails == []
    
    def test_censurar_datos_sensibles(self):
        """Verifica que censure números de tarjeta correctamente"""
        texto = "Mi tarjeta es 1234-5678-9012-3456 y otra 9876-5432-1098-7654"
        censurado = censurar_datos_sensibles(texto)
        
        assert "1234-5678-9012-3456" not in censurado
        assert "9876-5432-1098-7654" not in censurado
        assert censurado.count("XXXX-XXXX-XXXX-XXXX") == 2


# ============================================================================
# 13. TESTS DE INTEGRACIÓN: Sistema de Notificaciones
# ============================================================================

class TestSistemaNotificaciones:
    """Tests de integración para el sistema de notificaciones"""
    
    def test_motor_plantillas_renderizar(self):
        """Verifica que el motor de plantillas renderice correctamente"""
        motor = MotorPlantillas()
        plantilla = "Hola {{nombre}}, tienes {{cantidad}} mensajes"
        
        resultado = motor.renderizar(plantilla, {"nombre": "Juan", "cantidad": 5})
        
        assert resultado == "Hola Juan, tienes 5 mensajes"
    
    def test_servicio_email_enviar_bienvenida(self):
        """Verifica que el servicio de email envíe correctamente"""
        motor = MotorPlantillas()
        servicio = ServicioEmail(motor)
        
        email_data = servicio.enviar_bienvenida("juan@test.com", "Juan")
        
        assert email_data["to"] == "juan@test.com"
        assert "Juan" in email_data["body"]
        assert email_data["status"] == "sent"
        assert len(servicio.enviados) == 1
    
    def test_servicio_email_con_motor_mockeado(self):
        """Verifica integración usando un motor mockeado"""
        motor_mock = Mock()
        motor_mock.renderizar.return_value = "Email renderizado"
        
        servicio = ServicioEmail(motor_mock)
        email_data = servicio.enviar_bienvenida("test@test.com", "Test")
        
        motor_mock.renderizar.assert_called_once()
        assert email_data["body"] == "Email renderizado"


# ============================================================================
# 14. TESTS DE INTEGRACIÓN: Procesamiento de Pagos
# ============================================================================

class TestProcesadorPagos:
    """Tests de integración para el procesador de pagos"""
    
    def test_cobro_exitoso(self):
        """Verifica un cobro exitoso normal"""
        fraude = DetectorFraude()
        banco = PasarelaBancaria()
        procesador = ProcesadorPagos(fraude, banco)
        
        resultado = procesador.realizar_cobro("1234-5678", 5000)
        
        assert resultado == "Cobro exitoso"
    
    def test_cobro_rechazado_por_fraude(self):
        """Verifica que se rechace cobro sospechoso"""
        fraude = DetectorFraude()
        banco = PasarelaBancaria()
        procesador = ProcesadorPagos(fraude, banco)
        
        with pytest.raises(ValueError, match="sospecha de fraude"):
            procesador.realizar_cobro("1234-5678", 15000)
    
    def test_cobro_con_mocks(self):
        """Verifica el procesador usando mocks"""
        fraude_mock = Mock()
        fraude_mock.es_sospechoso.return_value = False
        
        banco_mock = Mock()
        banco_mock.procesar.return_value = True
        
        procesador = ProcesadorPagos(fraude_mock, banco_mock)
        resultado = procesador.realizar_cobro("1234-5678", 1000)
        
        assert resultado == "Cobro exitoso"
        fraude_mock.es_sospechoso.assert_called_once()
        banco_mock.procesar.assert_called_once()
    
    def test_error_en_pasarela_bancaria(self):
        """Verifica manejo de error en la pasarela"""
        fraude_mock = Mock()
        fraude_mock.es_sospechoso.return_value = False
        
        banco_mock = Mock()
        banco_mock.procesar.return_value = False
        
        procesador = ProcesadorPagos(fraude_mock, banco_mock)
        resultado = procesador.realizar_cobro("1234-5678", 1000)
        
        assert resultado == "Error en pasarela bancaria"


# ============================================================================
# 15. TESTS DE INTEGRACIÓN: Gestor de Contenidos (CMS)
# ============================================================================

class TestGestorArticulos:
    """Tests de integración para el gestor de artículos con caché"""
    
    def test_obtener_articulo_desde_db(self):
        """Verifica que se obtenga artículo desde DB cuando no está en caché"""
        cache = Cache()
        db = BaseDatosContenido()
        gestor = GestorArticulos(cache, db)
        
        articulo = gestor.obtener_articulo("art123")
        
        assert articulo["id"] == "art123"
        assert articulo["source"] == "db"
        assert articulo["titulo"] == "Título Demo"
    
    def test_obtener_articulo_desde_cache(self):
        """Verifica que se obtenga artículo desde caché si existe"""
        cache = Cache()
        db = BaseDatosContenido()
        gestor = GestorArticulos(cache, db)
        
        # Primera llamada: desde DB
        articulo1 = gestor.obtener_articulo("art123")
        assert articulo1["source"] == "db"
        
        # Segunda llamada: desde caché
        articulo2 = gestor.obtener_articulo("art123")
        assert articulo2["source"] == "cache"
        assert articulo2["id"] == "art123"
    
    def test_gestor_con_mocks(self):
        """Verifica el gestor usando mocks para cache y DB"""
        cache_mock = Mock()
        cache_mock.get.return_value = None
        
        db_mock = Mock()
        db_mock.obtener_articulo.return_value = {"id": "art456", "titulo": "Test"}
        
        gestor = GestorArticulos(cache_mock, db_mock)
        articulo = gestor.obtener_articulo("art456")
        
        # Verificar que se llamó a get del caché
        cache_mock.get.assert_called_once_with("art456")
        
        # Verificar que se llamó a la DB
        db_mock.obtener_articulo.assert_called_once_with("art456")
        
        # Verificar que se guardó en caché
        cache_mock.set.assert_called_once()


# ============================================================================
# FIXTURES Y CONFIGURACIÓN
# ============================================================================

@pytest.fixture
def cuenta_con_saldo():
    """Fixture que proporciona una cuenta con saldo inicial"""
    return CuentaBancaria(1000)

@pytest.fixture
def sistema_compras():
    """Fixture que proporciona un sistema de compras limpio"""
    return SistemaCompras()

@pytest.fixture
def base_datos():
    """Fixture que proporciona una base de datos limpia"""
    return BaseDeDatos()


# ============================================================================
# TESTS USANDO FIXTURES
# ============================================================================

class TestConFixtures:
    """Tests que demuestran el uso de fixtures"""
    
    def test_usar_fixture_cuenta(self, cuenta_con_saldo):
        """Verifica el uso de fixture de cuenta bancaria"""
        assert cuenta_con_saldo.saldo == 1000
        cuenta_con_saldo.depositar(500)
        assert cuenta_con_saldo.saldo == 1500
    
    def test_usar_fixture_sistema_compras(self, sistema_compras):
        """Verifica el uso de fixture de sistema de compras"""
        assert sistema_compras.inventario["laptop"] == 10
        sistema_compras.agregar_al_carrito("laptop", 1)
        assert len(sistema_compras.carrito) == 1


# ============================================================================
# TESTS PARAMETRIZADOS
# ============================================================================

class TestParametrizados:
    """Tests que usan parametrización para múltiples casos"""
    
    @pytest.mark.parametrize("a,b,esperado", [
        (2, 3, 5),
        (10, 20, 30),
        (-5, 5, 0),
        (0, 0, 0),
        (100, 200, 300),
    ])
    def test_sumar_parametrizado(self, a, b, esperado):
        """Verifica suma con múltiples casos parametrizados"""
        assert sumar(a, b) == esperado
    
    @pytest.mark.parametrize("texto,es_palindromo_esperado", [
        ("anilina", True),
        ("Anita lava la tina", True),
        ("hola", False),
        ("reconocer", True),
        ("python", False),
    ])
    def test_palindromo_parametrizado(self, texto, es_palindromo_esperado):
        """Verifica palíndromos con múltiples casos"""
        assert es_palindromo(texto) == es_palindromo_esperado
    
    @pytest.mark.parametrize("variante,mensaje_esperado", [
        ("A", "¡Bienvenido a nuestra plataforma!"),
        ("B", "Hola, gracias por visitarnos."),
        ("C", "Bienvenido"),
        ("X", "Bienvenido"),
    ])
    def test_ab_testing_parametrizado(self, variante, mensaje_esperado):
        """Verifica A/B testing con múltiples variantes"""
        assert obtener_mensaje_bienvenida(variante) == mensaje_esperado
