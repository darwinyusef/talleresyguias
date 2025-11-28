# Proyecto 2: Web con JavaScript

## Objetivo
Desplegar una aplicación web interactiva con HTML, CSS y JavaScript vanilla usando Docker.

## Prerrequisitos
- Proyecto 1 completado
- Conocimientos de JavaScript
- Docker instalado

---

## Paso 1: Preparar la Estructura

```bash
mkdir -p ~/curso-docker/proyectos/02-html-javascript
cd ~/curso-docker/proyectos/02-html-javascript
mkdir -p src/{js,css,assets}
```

**Estructura esperada (la crearás tú):**
```
src/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── app.js
│   └── utils.js
└── assets/
    └── images/
```

## Paso 2: Crear tu Aplicación JavaScript

Debes crear una aplicación interactiva. Ejemplos:
- To-Do List
- Calculadora
- Weather App (con fetch a API pública)
- Quiz interactivo
- Galería de imágenes

**Ejemplo de index.html básico:**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi App JavaScript</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <div id="app"></div>

    <script src="js/utils.js"></script>
    <script src="js/app.js"></script>
</body>
</html>
```

## Paso 3: Crear Dockerfile

```dockerfile
FROM nginx:alpine

# Copiar archivos de la aplicación
COPY src/ /usr/share/nginx/html/

# Exponer puerto 80
EXPOSE 80

# Nginx inicia automáticamente
```

## Paso 4: Crear .dockerignore

```
node_modules/
.git/
.gitignore
README.md
Dockerfile
docker-compose.yml
.DS_Store
*.log
```

## Paso 5: Configuración Avanzada de Nginx

Crea `nginx.conf` para optimizar la entrega de assets:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Manejo de rutas SPA
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Caché agresivo para assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Compresión Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/json
        application/x-javascript
        text/xml
        application/xml
        application/xml+rss;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**Actualizar Dockerfile:**
```dockerfile
FROM nginx:alpine

COPY src/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

## Paso 6: Construir y Ejecutar

```bash
# Construir imagen
docker build -t mi-app-js:v1 .

# Ejecutar contenedor
docker run -d \
  --name app-js \
  -p 8080:80 \
  mi-app-js:v1

# Verificar
docker ps
curl http://localhost:8080
```

## Paso 7: Modo Desarrollo con Hot Reload

Para desarrollo, usa un servidor con live reload.

**Opción 1: Bind Mount con Nginx**
```bash
docker run -d \
  --name app-js-dev \
  -p 8080:80 \
  -v $(pwd)/src:/usr/share/nginx/html \
  nginx:alpine
```

**Opción 2: Con servidor de desarrollo Node (recomendado)**

Crea `Dockerfile.dev`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Instalar servidor de desarrollo
RUN npm install -g live-server

# Copiar archivos
COPY src/ /app/

# Exponer puerto
EXPOSE 8080

# Comando para live-server
CMD ["live-server", "--host=0.0.0.0", "--port=8080", "--no-browser"]
```

**Ejecutar en modo desarrollo:**
```bash
docker build -f Dockerfile.dev -t app-js-dev .
docker run -d \
  --name app-dev \
  -p 8080:8080 \
  -v $(pwd)/src:/app \
  app-js-dev
```

---

## Docker Compose Setup

Crea `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Producción
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    container_name: app-js-prod
    restart: unless-stopped
    profiles:
      - production

  # Desarrollo con live-server
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
    volumes:
      - ./src:/app
    container_name: app-js-dev
    profiles:
      - development
```

**Uso:**
```bash
# Modo desarrollo
docker compose --profile development up -d

# Modo producción
docker compose --profile production up -d

# Detener
docker compose down
```

---

## Integración con APIs Externas

Si tu app consume APIs externas (ej: Weather API, GitHub API), considera:

**Ejemplo con fetch en JavaScript:**
```javascript
// src/js/app.js
async function fetchData() {
    try {
        const response = await fetch('https://api.github.com/users/octocat');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
}
```

**Importante:** Para APIs que requieren API keys, usa variables de entorno:

```dockerfile
FROM nginx:alpine

# Argumentos de build
ARG API_KEY

# Copiar archivos
COPY src/ /usr/share/nginx/html/

# Inyectar API key en archivo config
RUN echo "window.API_KEY = '${API_KEY}';" > /usr/share/nginx/html/js/config.js

EXPOSE 80
```

**Build con API key:**
```bash
docker build --build-arg API_KEY=tu-api-key-aqui -t mi-app-js:v1 .
```

**En tu JavaScript:**
```javascript
// Usar la API key
const apiKey = window.API_KEY || 'default-key';
```

---

## Ejemplo: App con Local Storage

Si tu app usa Local Storage, esto funciona normalmente en el navegador:

```javascript
// Guardar datos
localStorage.setItem('user', JSON.stringify({name: 'Juan'}));

// Leer datos
const user = JSON.parse(localStorage.getItem('user'));
```

**No necesitas configuración especial en Docker para esto.**

---

## Optimización de Assets

### Minificar JavaScript y CSS

**Opción 1: Multi-stage build con herramientas Node**

Crea `Dockerfile.optimized`:
```dockerfile
# Stage 1: Minificar assets
FROM node:18-alpine AS builder

WORKDIR /app
COPY src/ ./

# Instalar herramientas de minificación
RUN npm install -g terser clean-css-cli html-minifier

# Minificar archivos
RUN find . -name "*.js" -exec terser {} -o {} -c -m \;
RUN find . -name "*.css" -exec cleancss {} -o {} \;
RUN find . -name "*.html" -exec html-minifier --collapse-whitespace --remove-comments {} -o {} \;

# Stage 2: Servir archivos optimizados
FROM nginx:alpine

COPY --from=builder /app /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

**Build:**
```bash
docker build -f Dockerfile.optimized -t mi-app-js:optimized .
```

---

## Testing en Docker

Para hacer testing de tu app JavaScript:

**Dockerfile.test:**
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY src/ ./
COPY package*.json ./

RUN npm install
RUN npm install -D jest

# Copiar tests
COPY tests/ ./tests/

CMD ["npm", "test"]
```

**Ejecutar tests:**
```bash
docker build -f Dockerfile.test -t app-test .
docker run --rm app-test
```

---

## Ejercicios Prácticos

### Ejercicio 1: To-Do List
Crea una aplicación de tareas con:
- Agregar tareas
- Marcar como completadas
- Eliminar tareas
- Persistencia con LocalStorage
- Filtros (todas, activas, completadas)

### Ejercicio 2: Weather App
Crea una app del clima con:
- Buscar ciudad
- Mostrar temperatura actual
- Pronóstico de 5 días
- Usar API pública (OpenWeather, WeatherAPI)

### Ejercicio 3: Quiz Interactivo
- Preguntas con opciones múltiples
- Contador de puntos
- Temporizador
- Resultados al final

### Ejercicio 4: Galería de Imágenes
- Grid de imágenes
- Modal al hacer click
- Navegación entre imágenes
- Lazy loading

---

## Manejo de CORS

Si tu app hace peticiones a APIs y tienes problemas de CORS:

**Opción 1: Proxy con Nginx**

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;

    # Tu app
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy a API externa
    location /api/ {
        proxy_pass https://api.example.com/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Uso en JavaScript:**
```javascript
// En lugar de: fetch('https://api.example.com/data')
// Usa: fetch('/api/data')
fetch('/api/data')
    .then(res => res.json())
    .then(data => console.log(data));
```

---

## Debugging en Docker

**Ver logs de Nginx:**
```bash
docker exec app-js cat /var/log/nginx/access.log
docker exec app-js cat /var/log/nginx/error.log
```

**Inspeccionar archivos en contenedor:**
```bash
docker exec -it app-js sh
ls -la /usr/share/nginx/html
cat /usr/share/nginx/html/js/app.js
exit
```

**Browser DevTools:**
- Abre localhost:8080
- F12 para abrir DevTools
- Console para ver errores de JavaScript
- Network para ver peticiones HTTP

---

## Despliegue en Múltiples Ambientes

**docker-compose.prod.yml:**
```yaml
version: '3.8'

services:
  app:
    image: mi-app-js:v1
    ports:
      - "80:80"
    restart: always
    environment:
      - NODE_ENV=production
```

**docker-compose.dev.yml:**
```yaml
version: '3.8'

services:
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
    volumes:
      - ./src:/app
    environment:
      - NODE_ENV=development
```

**Comandos:**
```bash
# Desarrollo
docker compose -f docker-compose.dev.yml up -d

# Producción
docker compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### JavaScript no carga
```bash
# Verificar logs
docker logs app-js

# Verificar que archivos están en el contenedor
docker exec app-js ls -la /usr/share/nginx/html/js/

# Verificar permisos
docker exec app-js ls -la /usr/share/nginx/html/
```

### Errores de CORS
- Usar proxy de Nginx (ver sección CORS)
- O configurar headers en Nginx:
```nginx
add_header Access-Control-Allow-Origin * always;
```

### Assets no se actualizan
```bash
# Limpiar caché del navegador (Ctrl+Shift+R)
# O reconstruir imagen sin caché:
docker build --no-cache -t mi-app-js:v1 .
```

---

## Resumen de Comandos

```bash
# Construcción
docker build -t mi-app-js:v1 .

# Ejecución producción
docker run -d --name app-js -p 8080:80 mi-app-js:v1

# Ejecución desarrollo (bind mount)
docker run -d --name app-dev -p 8080:8080 \
  -v $(pwd)/src:/app \
  -f Dockerfile.dev mi-app-js-dev

# Logs
docker logs -f app-js

# Acceder al contenedor
docker exec -it app-js sh

# Detener y limpiar
docker stop app-js && docker rm app-js
```

---

## Checklist del Proyecto

- [ ] Crear estructura de directorios (src/js, src/css)
- [ ] Desarrollar aplicación JavaScript
- [ ] Crear Dockerfile
- [ ] Crear Dockerfile.dev (opcional)
- [ ] Crear nginx.conf personalizado
- [ ] Crear docker-compose.yml
- [ ] Construir imagen
- [ ] Probar en modo desarrollo
- [ ] Probar en modo producción
- [ ] Verificar en navegador
- [ ] Probar funcionalidad JavaScript
- [ ] Verificar DevTools (sin errores de consola)

---

## Siguiente Paso

Continúa con:
**[Proyecto 3: API con FastAPI](./03-fastapi.md)**
