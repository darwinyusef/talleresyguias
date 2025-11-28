# Proyecto 1: Web Estática HTML

## Objetivo
Desplegar un sitio web estático HTML usando Nginx en Docker.

## Prerrequisitos
- Docker instalado
- Conocimientos básicos de HTML
- Terminal de Linux

---

## Paso 1: Preparar la Estructura del Proyecto

```bash
mkdir -p ~/curso-docker/proyectos/01-html-estatico
cd ~/curso-docker/proyectos/01-html-estatico
mkdir src
```

## Paso 2: Crear Archivos HTML (Los crearás tú)

Tu sitio debe tener al menos:
- `src/index.html` - Página principal
- `src/styles.css` - Estilos (opcional)
- Imágenes o assets en `src/` (opcional)

**Ejemplo de estructura mínima que debes crear:**
```
src/
├── index.html
├── styles.css
└── images/
    └── logo.png
```

## Paso 3: Crear Dockerfile

Crea un archivo llamado `Dockerfile` en el directorio raíz:

```dockerfile
# Usar imagen oficial de Nginx
FROM nginx:alpine

# Copiar archivos HTML al directorio de Nginx
COPY src/ /usr/share/nginx/html/

# Exponer puerto 80
EXPOSE 80

# Nginx se ejecuta automáticamente con CMD de la imagen base
```

**Explicación línea por línea:**
- `FROM nginx:alpine` - Usa Nginx en versión Alpine (ligera)
- `COPY src/ /usr/share/nginx/html/` - Copia tu sitio web al directorio de Nginx
- `EXPOSE 80` - Documenta que el contenedor escucha en puerto 80

## Paso 4: Crear .dockerignore

Crea `.dockerignore` para excluir archivos innecesarios:

```
.git
.gitignore
README.md
Dockerfile
.DS_Store
```

## Paso 5: Construir la Imagen

```bash
docker build -t mi-web-estatica:v1 .
```

**Verificar que se creó:**
```bash
docker images | grep mi-web-estatica
```

## Paso 6: Ejecutar el Contenedor

```bash
docker run -d \
  --name web-estatica \
  -p 8080:80 \
  mi-web-estatica:v1
```

**Verificar que está corriendo:**
```bash
docker ps
```

## Paso 7: Probar la Aplicación

**En el navegador:**
```
http://localhost:8080
```

**Desde terminal:**
```bash
curl http://localhost:8080
```

## Paso 8: Ver Logs

```bash
docker logs web-estatica
docker logs -f web-estatica  # Seguir en tiempo real
```

## Paso 9: Detener y Limpiar

```bash
# Detener contenedor
docker stop web-estatica

# Eliminar contenedor
docker rm web-estatica

# Eliminar imagen
docker rmi mi-web-estatica:v1
```

---

## Opción Avanzada: Con Docker Compose

Crea `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:80"
    container_name: web-estatica
    restart: unless-stopped
```

**Comandos:**
```bash
# Iniciar
docker compose up -d

# Ver logs
docker compose logs -f

# Detener y limpiar
docker compose down
```

---

## Opción con Bind Mount (Desarrollo)

Para desarrollo, puedes montar los archivos directamente sin reconstruir:

```bash
docker run -d \
  --name web-dev \
  -p 8080:80 \
  -v $(pwd)/src:/usr/share/nginx/html \
  nginx:alpine
```

**Ventaja:** Los cambios en `src/` se reflejan inmediatamente sin reconstruir.

**docker-compose.yml para desarrollo:**
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./src:/usr/share/nginx/html
    container_name: web-dev
```

---

## Configuración Personalizada de Nginx (Opcional)

Crea `nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Caché para archivos estáticos
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Compresión gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
}
```

**Actualizar Dockerfile:**
```dockerfile
FROM nginx:alpine

COPY src/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

---

## Ejercicios Prácticos

### Ejercicio 1: Sitio Básico
Crea un sitio HTML simple con:
- Página de inicio
- Página "Acerca de"
- Página "Contacto"
- Navegación entre páginas

### Ejercicio 2: Multi-Stage Build
Aunque no es necesario para HTML estático, practica un multi-stage build:

```dockerfile
# Stage 1: Preparar archivos
FROM alpine:latest AS builder
WORKDIR /app
COPY src/ .
# Aquí podrías minificar HTML/CSS/JS

# Stage 2: Servir
FROM nginx:alpine
COPY --from=builder /app /usr/share/nginx/html
EXPOSE 80
```

### Ejercicio 3: Múltiples Puertos
Ejecuta 3 versiones del sitio en diferentes puertos:

```bash
docker run -d --name web-8081 -p 8081:80 mi-web-estatica:v1
docker run -d --name web-8082 -p 8082:80 mi-web-estatica:v1
docker run -d --name web-8083 -p 8083:80 mi-web-estatica:v1
```

---

## Troubleshooting

### El sitio no carga
```bash
# Verificar que el contenedor está corriendo
docker ps

# Ver logs
docker logs web-estatica

# Verificar que el puerto no está en uso
lsof -i :8080
```

### Cambios no se reflejan
```bash
# Si usas build (no bind mount), necesitas reconstruir:
docker build -t mi-web-estatica:v1 .
docker stop web-estatica
docker rm web-estatica
docker run -d --name web-estatica -p 8080:80 mi-web-estatica:v1
```

### Error de permisos
```bash
# Verificar permisos de archivos en src/
ls -la src/
chmod -R 644 src/*
```

---

## Resumen de Comandos

```bash
# Construcción
docker build -t mi-web-estatica:v1 .

# Ejecución
docker run -d --name web-estatica -p 8080:80 mi-web-estatica:v1

# Desarrollo (bind mount)
docker run -d --name web-dev -p 8080:80 -v $(pwd)/src:/usr/share/nginx/html nginx:alpine

# Logs
docker logs -f web-estatica

# Detener y limpiar
docker stop web-estatica && docker rm web-estatica

# Con Docker Compose
docker compose up -d
docker compose down
```

---

## Checklist del Proyecto

- [ ] Crear estructura de directorios
- [ ] Crear archivos HTML/CSS
- [ ] Crear Dockerfile
- [ ] Crear .dockerignore
- [ ] Construir imagen
- [ ] Ejecutar contenedor
- [ ] Verificar en navegador (localhost:8080)
- [ ] Ver logs del contenedor
- [ ] Detener y limpiar recursos

---

## Siguiente Paso

Una vez completado este proyecto, continúa con:
**[Proyecto 2: Web con JavaScript](./02-html-javascript.md)**
