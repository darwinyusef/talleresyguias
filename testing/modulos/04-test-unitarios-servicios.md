# Módulo 4: Test Unitarios a Servicios

## Introducción

En este módulo aprenderás a testear servicios que interactúan con APIs externas, realizan peticiones HTTP y manejan respuestas JSON. Aprenderás a usar mocks para simular estas interacciones sin hacer llamadas reales.

## ¿Por qué Mockear Servicios?

Cuando testeas servicios, NO quieres:
- Hacer llamadas reales a APIs externas (lento, costoso, inestable)
- Depender de servicios de terceros
- Modificar datos reales
- Esperar respuestas de red

En su lugar, usamos **mocks** para simular estas respuestas.

## Instalación de Dependencias

```bash
pip install pytest
pip install pytest-mock
pip install requests
pip install responses  # Para mockear requests
```

## Introducción a Mocking con unittest.mock

### POC 1: Mock Básico

**Archivo: ejemplos/03-servicios/test_mock_basico.py**
```python
import pytest
from unittest.mock import Mock, patch

# Mock simple
def test_mock_simple():
    # Crear un mock
    mock_obj = Mock()

    # Configurar el retorno
    mock_obj.obtener_dato.return_value = "dato mockeado"

    # Usar el mock
    resultado = mock_obj.obtener_dato()

    # Verificar
    assert resultado == "dato mockeado"
    mock_obj.obtener_dato.assert_called_once()

# Mock con múltiples llamadas
def test_mock_multiples_llamadas():
    mock_obj = Mock()
    mock_obj.calcular.side_effect = [10, 20, 30]

    assert mock_obj.calcular() == 10
    assert mock_obj.calcular() == 20
    assert mock_obj.calcular() == 30

    assert mock_obj.calcular.call_count == 3

# Mock que lanza excepciones
def test_mock_con_excepcion():
    mock_obj = Mock()
    mock_obj.operacion.side_effect = ValueError("Error mockeado")

    with pytest.raises(ValueError, match="Error mockeado"):
        mock_obj.operacion()
```

## Testing de Servicios HTTP

### POC 2: Cliente HTTP Básico

**Archivo: ejemplos/03-servicios/http_client.py**
```python
import requests

class HTTPClient:
    """Cliente HTTP para consumir APIs"""

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        """Realiza una petición GET"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        """Realiza una petición POST"""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data):
        """Realiza una petición PUT"""
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        """Realiza una petición DELETE"""
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.status_code == 204
```

**Archivo: ejemplos/03-servicios/test_http_client.py**
```python
import pytest
import responses
import requests
from http_client import HTTPClient

class TestHTTPClient:
    """Tests para HTTPClient usando responses"""

    @pytest.fixture
    def client(self):
        return HTTPClient("https://api.ejemplo.com")

    @responses.activate
    def test_get_exitoso(self, client):
        # Mockear la respuesta
        responses.add(
            responses.GET,
            "https://api.ejemplo.com/users/1",
            json={"id": 1, "nombre": "Juan"},
            status=200
        )

        # Hacer la petición
        resultado = client.get("/users/1")

        # Verificar
        assert resultado["id"] == 1
        assert resultado["nombre"] == "Juan"

    @responses.activate
    def test_get_error_404(self, client):
        responses.add(
            responses.GET,
            "https://api.ejemplo.com/users/999",
            status=404
        )

        with pytest.raises(requests.HTTPError):
            client.get("/users/999")

    @responses.activate
    def test_post_exitoso(self, client):
        responses.add(
            responses.POST,
            "https://api.ejemplo.com/users",
            json={"id": 1, "nombre": "Juan", "email": "juan@email.com"},
            status=201
        )

        data = {"nombre": "Juan", "email": "juan@email.com"}
        resultado = client.post("/users", data)

        assert resultado["id"] == 1
        assert resultado["nombre"] == "Juan"

    @responses.activate
    def test_put_exitoso(self, client):
        responses.add(
            responses.PUT,
            "https://api.ejemplo.com/users/1",
            json={"id": 1, "nombre": "Juan Actualizado"},
            status=200
        )

        data = {"nombre": "Juan Actualizado"}
        resultado = client.put("/users/1", data)

        assert resultado["nombre"] == "Juan Actualizado"

    @responses.activate
    def test_delete_exitoso(self, client):
        responses.add(
            responses.DELETE,
            "https://api.ejemplo.com/users/1",
            status=204
        )

        resultado = client.delete("/users/1")
        assert resultado == True
```

## Testing de Servicios con Lógica de Negocio

### POC 3: Servicio de Usuarios

**Archivo: ejemplos/03-servicios/user_service.py**
```python
import requests

class UserService:
    """Servicio para gestionar usuarios"""

    def __init__(self, api_url):
        self.api_url = api_url

    def obtener_usuario(self, user_id):
        """Obtiene un usuario por ID"""
        try:
            response = requests.get(f"{self.api_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def crear_usuario(self, nombre, email):
        """Crea un nuevo usuario"""
        if not nombre or not email:
            raise ValueError("Nombre y email son requeridos")

        if "@" not in email:
            raise ValueError("Email inválido")

        data = {"nombre": nombre, "email": email}
        response = requests.post(f"{self.api_url}/users", json=data)
        response.raise_for_status()
        return response.json()

    def actualizar_usuario(self, user_id, **kwargs):
        """Actualiza un usuario"""
        if not kwargs:
            raise ValueError("Debe proporcionar al menos un campo para actualizar")

        response = requests.put(f"{self.api_url}/users/{user_id}", json=kwargs)
        response.raise_for_status()
        return response.json()

    def listar_usuarios(self):
        """Lista todos los usuarios"""
        response = requests.get(f"{self.api_url}/users")
        response.raise_for_status()
        return response.json()

    def buscar_usuarios_por_email(self, email):
        """Busca usuarios por email"""
        usuarios = self.listar_usuarios()
        return [u for u in usuarios if u.get("email") == email]
```

**Archivo: ejemplos/03-servicios/test_user_service.py**
```python
import pytest
import responses
import requests
from user_service import UserService

class TestUserService:
    """Tests para UserService"""

    @pytest.fixture
    def service(self):
        return UserService("https://api.ejemplo.com")

    @responses.activate
    def test_obtener_usuario_existente(self, service):
        responses.add(
            responses.GET,
            "https://api.ejemplo.com/users/1",
            json={"id": 1, "nombre": "Juan", "email": "juan@email.com"},
            status=200
        )

        usuario = service.obtener_usuario(1)

        assert usuario is not None
        assert usuario["nombre"] == "Juan"

    @responses.activate
    def test_obtener_usuario_inexistente(self, service):
        responses.add(
            responses.GET,
            "https://api.ejemplo.com/users/999",
            status=404
        )

        usuario = service.obtener_usuario(999)
        assert usuario is None

    def test_crear_usuario_sin_nombre(self, service):
        with pytest.raises(ValueError, match="Nombre y email son requeridos"):
            service.crear_usuario("", "email@test.com")

    def test_crear_usuario_email_invalido(self, service):
        with pytest.raises(ValueError, match="Email inválido"):
            service.crear_usuario("Juan", "email-invalido")

    @responses.activate
    def test_crear_usuario_exitoso(self, service):
        responses.add(
            responses.POST,
            "https://api.ejemplo.com/users",
            json={"id": 1, "nombre": "Juan", "email": "juan@email.com"},
            status=201
        )

        usuario = service.crear_usuario("Juan", "juan@email.com")

        assert usuario["id"] == 1
        assert usuario["nombre"] == "Juan"

    def test_actualizar_usuario_sin_datos(self, service):
        with pytest.raises(ValueError, match="al menos un campo"):
            service.actualizar_usuario(1)

    @responses.activate
    def test_actualizar_usuario_exitoso(self, service):
        responses.add(
            responses.PUT,
            "https://api.ejemplo.com/users/1",
            json={"id": 1, "nombre": "Juan Updated"},
            status=200
        )

        usuario = service.actualizar_usuario(1, nombre="Juan Updated")
        assert usuario["nombre"] == "Juan Updated"

    @responses.activate
    def test_listar_usuarios(self, service):
        responses.add(
            responses.GET,
            "https://api.ejemplo.com/users",
            json=[
                {"id": 1, "nombre": "Juan", "email": "juan@email.com"},
                {"id": 2, "nombre": "María", "email": "maria@email.com"}
            ],
            status=200
        )

        usuarios = service.listar_usuarios()
        assert len(usuarios) == 2

    @responses.activate
    def test_buscar_usuarios_por_email(self, service):
        responses.add(
            responses.GET,
            "https://api.ejemplo.com/users",
            json=[
                {"id": 1, "nombre": "Juan", "email": "juan@email.com"},
                {"id": 2, "nombre": "María", "email": "maria@email.com"}
            ],
            status=200
        )

        usuarios = service.buscar_usuarios_por_email("juan@email.com")
        assert len(usuarios) == 1
        assert usuarios[0]["nombre"] == "Juan"
```

## Mocking con unittest.mock.patch

### POC 4: Servicio con Dependencias

**Archivo: ejemplos/03-servicios/weather_service.py**
```python
import requests

class WeatherService:
    """Servicio de clima"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"

    def obtener_clima(self, ciudad):
        """Obtiene el clima de una ciudad"""
        url = f"{self.base_url}/weather"
        params = {"city": ciudad, "api_key": self.api_key}

        response = requests.get(url, params=params)
        response.raise_for_status()

        return self._procesar_respuesta(response.json())

    def _procesar_respuesta(self, data):
        """Procesa la respuesta de la API"""
        return {
            "temperatura": data.get("temp"),
            "descripcion": data.get("description"),
            "humedad": data.get("humidity")
        }

    def esta_soleado(self, ciudad):
        """Verifica si está soleado en una ciudad"""
        clima = self.obtener_clima(ciudad)
        return "sol" in clima["descripcion"].lower()

    def recomendar_ropa(self, ciudad):
        """Recomienda ropa según el clima"""
        clima = self.obtener_clima(ciudad)
        temp = clima["temperatura"]

        if temp < 10:
            return "Abrigo y bufanda"
        elif temp < 20:
            return "Suéter"
        else:
            return "Ropa ligera"
```

**Archivo: ejemplos/03-servicios/test_weather_service.py**
```python
import pytest
from unittest.mock import patch, Mock
import requests
from weather_service import WeatherService

class TestWeatherService:
    """Tests para WeatherService"""

    @pytest.fixture
    def service(self):
        return WeatherService("fake-api-key")

    @patch('weather_service.requests.get')
    def test_obtener_clima(self, mock_get, service):
        # Configurar el mock
        mock_response = Mock()
        mock_response.json.return_value = {
            "temp": 25,
            "description": "Soleado",
            "humidity": 60
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Ejecutar
        clima = service.obtener_clima("Madrid")

        # Verificar
        assert clima["temperatura"] == 25
        assert clima["descripcion"] == "Soleado"
        assert clima["humedad"] == 60

        # Verificar que se llamó correctamente
        mock_get.assert_called_once()

    @patch('weather_service.requests.get')
    def test_obtener_clima_error_api(self, mock_get, service):
        mock_get.side_effect = requests.HTTPError("API Error")

        with pytest.raises(requests.HTTPError):
            service.obtener_clima("Madrid")

    @patch.object(WeatherService, 'obtener_clima')
    def test_esta_soleado_si(self, mock_obtener_clima, service):
        mock_obtener_clima.return_value = {
            "temperatura": 25,
            "descripcion": "Día soleado",
            "humedad": 60
        }

        assert service.esta_soleado("Madrid") == True

    @patch.object(WeatherService, 'obtener_clima')
    def test_esta_soleado_no(self, mock_obtener_clima, service):
        mock_obtener_clima.return_value = {
            "temperatura": 15,
            "descripcion": "Nublado",
            "humedad": 80
        }

        assert service.esta_soleado("Madrid") == False

    @patch.object(WeatherService, 'obtener_clima')
    def test_recomendar_ropa_frio(self, mock_obtener_clima, service):
        mock_obtener_clima.return_value = {
            "temperatura": 5,
            "descripcion": "Frío",
            "humedad": 70
        }

        recomendacion = service.recomendar_ropa("Madrid")
        assert recomendacion == "Abrigo y bufanda"

    @patch.object(WeatherService, 'obtener_clima')
    def test_recomendar_ropa_templado(self, mock_obtener_clima, service):
        mock_obtener_clima.return_value = {
            "temperatura": 15,
            "descripcion": "Templado",
            "humedad": 60
        }

        recomendacion = service.recomendar_ropa("Madrid")
        assert recomendacion == "Suéter"

    @patch.object(WeatherService, 'obtener_clima')
    def test_recomendar_ropa_calor(self, mock_obtener_clima, service):
        mock_obtener_clima.return_value = {
            "temperatura": 30,
            "descripcion": "Caluroso",
            "humedad": 50
        }

        recomendacion = service.recomendar_ropa("Madrid")
        assert recomendacion == "Ropa ligera"
```

## Testing de Servicios con Caché

### POC 5: Servicio con Caché

**Archivo: ejemplos/03-servicios/cached_service.py**
```python
import requests
from datetime import datetime, timedelta

class CachedAPIService:
    """Servicio con caché simple"""

    def __init__(self, base_url, cache_duration_minutes=5):
        self.base_url = base_url
        self.cache = {}
        self.cache_duration = timedelta(minutes=cache_duration_minutes)

    def _esta_cache_valido(self, key):
        """Verifica si el caché es válido"""
        if key not in self.cache:
            return False

        timestamp, _ = self.cache[key]
        return datetime.now() - timestamp < self.cache_duration

    def obtener_datos(self, endpoint):
        """Obtiene datos con caché"""
        # Verificar caché
        if self._esta_cache_valido(endpoint):
            _, data = self.cache[endpoint]
            return data

        # Hacer petición
        response = requests.get(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        data = response.json()

        # Guardar en caché
        self.cache[endpoint] = (datetime.now(), data)
        return data

    def limpiar_cache(self):
        """Limpia el caché"""
        self.cache.clear()

    def invalidar_cache(self, endpoint):
        """Invalida un endpoint específico del caché"""
        if endpoint in self.cache:
            del self.cache[endpoint]
```

**Archivo: ejemplos/03-servicios/test_cached_service.py**
```python
import pytest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
import requests
from cached_service import CachedAPIService

class TestCachedAPIService:
    """Tests para CachedAPIService"""

    @pytest.fixture
    def service(self):
        return CachedAPIService("https://api.ejemplo.com", cache_duration_minutes=5)

    @patch('cached_service.requests.get')
    def test_primera_llamada_hace_request(self, mock_get, service):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        resultado = service.obtener_datos("/endpoint")

        assert resultado == {"data": "test"}
        mock_get.assert_called_once()

    @patch('cached_service.requests.get')
    def test_segunda_llamada_usa_cache(self, mock_get, service):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Primera llamada
        service.obtener_datos("/endpoint")
        # Segunda llamada
        resultado = service.obtener_datos("/endpoint")

        # Solo debe haber una llamada HTTP
        assert mock_get.call_count == 1
        assert resultado == {"data": "test"}

    @patch('cached_service.requests.get')
    @patch('cached_service.datetime')
    def test_cache_expira(self, mock_datetime, mock_get, service):
        # Configurar mock de datetime
        tiempo_inicial = datetime(2024, 1, 1, 12, 0)
        tiempo_expirado = tiempo_inicial + timedelta(minutes=6)

        mock_datetime.now.side_effect = [tiempo_inicial, tiempo_expirado]

        # Configurar mock de requests
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Primera llamada
        service.obtener_datos("/endpoint")
        # Segunda llamada después de expiración
        service.obtener_datos("/endpoint")

        # Debe haber dos llamadas HTTP
        assert mock_get.call_count == 2

    @patch('cached_service.requests.get')
    def test_limpiar_cache(self, mock_get, service):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Primera llamada
        service.obtener_datos("/endpoint")
        service.limpiar_cache()
        # Segunda llamada después de limpiar
        service.obtener_datos("/endpoint")

        # Debe haber dos llamadas HTTP
        assert mock_get.call_count == 2

    @patch('cached_service.requests.get')
    def test_invalidar_cache_especifico(self, mock_get, service):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        service.obtener_datos("/endpoint1")
        service.obtener_datos("/endpoint2")
        service.invalidar_cache("/endpoint1")

        # Llamar de nuevo ambos endpoints
        service.obtener_datos("/endpoint1")  # Hará request
        service.obtener_datos("/endpoint2")  # Usa caché

        # 3 llamadas: 2 iniciales + 1 después de invalidar endpoint1
        assert mock_get.call_count == 3
```

## Testing de Manejo de Errores

### POC 6: Servicio con Retry

**Archivo: ejemplos/03-servicios/retry_service.py**
```python
import requests
import time

class RetryService:
    """Servicio con reintentos automáticos"""

    def __init__(self, base_url, max_retries=3, retry_delay=1):
        self.base_url = base_url
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def obtener_datos_con_retry(self, endpoint):
        """Obtiene datos con reintentos"""
        intentos = 0
        ultimo_error = None

        while intentos < self.max_retries:
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                ultimo_error = e
                intentos += 1

                if intentos < self.max_retries:
                    time.sleep(self.retry_delay)

        raise Exception(f"Falló después de {self.max_retries} intentos: {ultimo_error}")
```

**Archivo: ejemplos/03-servicios/test_retry_service.py**
```python
import pytest
from unittest.mock import patch, Mock
import requests
from retry_service import RetryService

class TestRetryService:
    """Tests para RetryService"""

    @pytest.fixture
    def service(self):
        return RetryService("https://api.ejemplo.com", max_retries=3, retry_delay=0)

    @patch('retry_service.requests.get')
    def test_exito_primer_intento(self, mock_get, service):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "success"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        resultado = service.obtener_datos_con_retry("/endpoint")

        assert resultado == {"data": "success"}
        assert mock_get.call_count == 1

    @patch('retry_service.requests.get')
    def test_exito_segundo_intento(self, mock_get, service):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "success"}
        mock_response.raise_for_status = Mock()

        # Primer intento falla, segundo tiene éxito
        mock_get.side_effect = [
            requests.RequestException("Error temporal"),
            mock_response
        ]

        resultado = service.obtener_datos_con_retry("/endpoint")

        assert resultado == {"data": "success"}
        assert mock_get.call_count == 2

    @patch('retry_service.requests.get')
    def test_todos_intentos_fallan(self, mock_get, service):
        mock_get.side_effect = requests.RequestException("Error persistente")

        with pytest.raises(Exception, match="Falló después de 3 intentos"):
            service.obtener_datos_con_retry("/endpoint")

        assert mock_get.call_count == 3
```

## Ejercicios Prácticos

### Ejercicio 1: Servicio de Autenticación

```python
# ejemplos/03-servicios/auth_service.py
class AuthService:
    def __init__(self, api_url):
        self.api_url = api_url
        self.token = None

    def login(self, username, password):
        """Inicia sesión y guarda el token"""
        pass

    def logout(self):
        """Cierra sesión"""
        pass

    def esta_autenticado(self):
        """Verifica si está autenticado"""
        pass

    def obtener_perfil(self):
        """Obtiene el perfil del usuario autenticado"""
        pass

# Escribe tests para:
# - Login exitoso
# - Login con credenciales inválidas
# - Logout
# - Obtener perfil sin autenticar
# - Obtener perfil autenticado
```

### Ejercicio 2: Servicio de Notificaciones

```python
# ejemplos/03-servicios/notification_service.py
class NotificationService:
    def __init__(self, email_service, sms_service):
        self.email_service = email_service
        self.sms_service = sms_service

    def enviar_notificacion(self, usuario, mensaje, tipo="email"):
        """Envía una notificación por email o SMS"""
        pass

    def enviar_notificacion_multiple(self, usuarios, mensaje):
        """Envía notificaciones a múltiples usuarios"""
        pass

# Escribe tests mockeando los servicios de email y SMS
```

### Ejercicio 3: Servicio de Pagos

```python
# ejemplos/03-servicios/payment_service.py
class PaymentService:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def procesar_pago(self, monto, tarjeta):
        """Procesa un pago"""
        pass

    def reembolsar(self, transaccion_id):
        """Realiza un reembolso"""
        pass

    def verificar_estado_pago(self, transaccion_id):
        """Verifica el estado de un pago"""
        pass

# Escribe tests para diferentes escenarios de pago
```

## Resumen

En este módulo aprendiste:

- Conceptos básicos de mocking
- Testing de servicios HTTP con `responses`
- Uso de `unittest.mock.patch`
- Testing de servicios con caché
- Testing de reintentos y manejo de errores
- Mocking de dependencias externas
- Verificación de llamadas a mocks

## Próximos Pasos

En el siguiente módulo aprenderás sobre test de integración:
- Mocks completos de bases de datos
- Testing de CRUD completo
- Integración de múltiples servicios
- Testing de transacciones

---

**[⬅️ Módulo anterior](03-test-unitarios-poo.md) | [Volver al índice](../README.md) | [Siguiente: Módulo 5 - Test de Integración con Mocks ➡️](05-test-integracion-mocks.md)**
