# Curso: De Linux a Docker - Guía Completa

## Índice del Curso

1. [Módulo 1: Fundamentos de Linux](#módulo-1-fundamentos-de-linux)
2. [Módulo 2: Linux Intermedio](#módulo-2-linux-intermedio)
3. [Módulo 3: Introducción a Docker](#módulo-3-introducción-a-docker)
4. [Módulo 4: Dockerfile - Construcción de Imágenes](#módulo-4-dockerfile---construcción-de-imágenes)
5. [Módulo 5: Docker Compose](#módulo-5-docker-compose)
6. [Proyectos Prácticos](#proyectos-prácticos)

---

## Módulo 1: Fundamentos de Linux

### 1.1 El Sistema de Archivos Linux

#### Estructura de Directorios
```bash
/           # Raíz del sistema
├── bin     # Binarios esenciales del sistema
├── etc     # Archivos de configuración
├── home    # Directorios de usuarios
├── var     # Datos variables (logs, cache)
├── tmp     # Archivos temporales
├── usr     # Aplicaciones de usuario
└── opt     # Software opcional
```

#### Comandos Básicos de Navegación

**pwd** - Mostrar directorio actual
```bash
pwd
```

**ls** - Listar contenidos
```bash
ls              # Listar archivos
ls -l           # Formato largo (permisos, dueño, tamaño)
ls -la          # Incluir archivos ocultos
ls -lh          # Tamaños legibles (KB, MB)
```

**cd** - Cambiar de directorio
```bash
cd /home/user   # Ruta absoluta
cd ..           # Directorio padre
cd ~            # Directorio home
cd -            # Directorio anterior
```

**mkdir** - Crear directorios
```bash
mkdir mi_carpeta
mkdir -p proyecto/src/components  # Crear directorios anidados
```

**Ejercicio Práctico 1:**
```bash
# Crea la siguiente estructura:
mkdir -p ~/curso-docker/modulo1/practica
cd ~/curso-docker/modulo1/practica
mkdir html css js
ls -l
```

### 1.2 Manipulación de Archivos

**touch** - Crear archivos vacíos
```bash
touch archivo.txt
touch index.html style.css script.js
```

**cp** - Copiar archivos y directorios
```bash
cp archivo.txt copia.txt
cp -r directorio/ copia_directorio/  # Recursivo para directorios
```

**mv** - Mover/Renombrar
```bash
mv archivo.txt nuevo_nombre.txt
mv archivo.txt /otra/carpeta/
```

**rm** - Eliminar
```bash
rm archivo.txt
rm -r directorio/      # Eliminar directorio
rm -rf directorio/     # Forzar eliminación
```

**Ejercicio Práctico 2:**
```bash
cd ~/curso-docker/modulo1/practica
touch index.html
cp index.html about.html
mv about.html html/
ls html/
```

### 1.3 Visualización de Archivos

**cat** - Mostrar contenido completo
```bash
cat archivo.txt
cat archivo1.txt archivo2.txt  # Múltiples archivos
```

**less** - Visualizar con paginación
```bash
less archivo.txt
# q para salir, / para buscar
```

**head** - Primeras líneas
```bash
head archivo.txt
head -n 20 archivo.txt  # Primeras 20 líneas
```

**tail** - Últimas líneas
```bash
tail archivo.txt
tail -f log.txt  # Seguir archivo en tiempo real (logs)
```

### 1.4 Permisos y Propietarios

#### Entendiendo los Permisos
```
-rwxr-xr--
│││││││││└─ Otros: lectura
││││││││└── Otros: sin escritura
│││││││└─── Otros: sin ejecución
││││││└──── Grupo: lectura
│││││└───── Grupo: sin escritura
││││└────── Grupo: ejecución
│││└─────── Usuario: lectura
││└──────── Usuario: escritura
│└───────── Usuario: ejecución
└────────── Tipo (- archivo, d directorio)
```

**chmod** - Cambiar permisos
```bash
chmod 755 script.sh    # rwxr-xr-x
chmod +x script.sh     # Agregar ejecución
chmod -w archivo.txt   # Quitar escritura
```

Tabla de permisos numéricos:
- 4 = lectura (r)
- 2 = escritura (w)
- 1 = ejecución (x)
- 7 = rwx (4+2+1)
- 6 = rw- (4+2)
- 5 = r-x (4+1)

**chown** - Cambiar propietario
```bash
chown usuario:grupo archivo.txt
chown -R usuario:grupo directorio/
```

**Ejercicio Práctico 3:**
```bash
cd ~/curso-docker/modulo1/practica
touch script.sh
ls -l script.sh
chmod +x script.sh
ls -l script.sh
```

### 1.5 Búsqueda y Filtrado

**find** - Buscar archivos
```bash
find . -name "*.txt"              # Por nombre
find . -type f -name "index*"     # Solo archivos
find . -type d -name "src"        # Solo directorios
find . -mtime -7                  # Modificados últimos 7 días
```

**grep** - Buscar en contenidos
```bash
grep "texto" archivo.txt
grep -r "función" .              # Recursivo en directorio
grep -i "error" log.txt          # Case insensitive
grep -n "TODO" *.js              # Mostrar números de línea
```

**Ejercicio Práctico 4:**
```bash
cd ~/curso-docker
find . -name "*.html"
echo "TODO: completar header" > html/index.html
grep -r "TODO" .
```

### 1.6 Redirección y Pipes

**Redirección de salida:**
```bash
ls -l > listado.txt              # Sobrescribir
ls -l >> listado.txt             # Agregar
comando 2> errores.txt           # Redirigir errores
comando &> todo.txt              # Salida y errores
```

**Pipes (|)** - Encadenar comandos:
```bash
ls -l | grep ".txt"
cat archivo.txt | grep "error" | wc -l
ps aux | grep node
```

**Comandos útiles con pipes:**
```bash
history | grep docker            # Buscar en historial
ls | wc -l                       # Contar archivos
cat archivo.txt | sort | uniq   # Ordenar y eliminar duplicados
```

### 1.7 Gestión de Procesos

**ps** - Ver procesos
```bash
ps                    # Procesos del usuario actual
ps aux                # Todos los procesos
ps aux | grep node    # Filtrar procesos
```

**top/htop** - Monitor en tiempo real
```bash
top                   # Monitor básico
htop                  # Monitor mejorado (si está instalado)
```

**kill** - Terminar procesos
```bash
kill PID              # Terminar proceso
kill -9 PID           # Forzar terminación
killall node          # Terminar todos los procesos node
```

**Ejercicio Práctico 5:**
```bash
# En una terminal
sleep 100 &           # Proceso en background
ps aux | grep sleep
kill %1               # Matar job 1
```

### 1.8 Networking Básico

**ping** - Probar conectividad
```bash
ping google.com
ping -c 4 8.8.8.8    # Solo 4 paquetes
```

**curl** - Hacer peticiones HTTP
```bash
curl https://api.github.com
curl -o archivo.html https://ejemplo.com
curl -I https://google.com       # Solo headers
```

**wget** - Descargar archivos
```bash
wget https://ejemplo.com/archivo.zip
wget -O nombre.zip https://ejemplo.com/archivo.zip
```

**netstat/ss** - Ver conexiones
```bash
netstat -tulpn        # Puertos en escucha
ss -tulpn             # Alternativa moderna
```

**Ejercicio Práctico 6:**
```bash
curl -I https://www.google.com
curl https://api.github.com/users/octocat
```

---

## Módulo 2: Linux Intermedio

### 2.1 Variables de Entorno

**Ver variables:**
```bash
env                   # Todas las variables
echo $PATH            # Variable específica
echo $HOME
echo $USER
```

**Definir variables:**
```bash
# Temporal (solo sesión actual)
export MI_VARIABLE="valor"

# Permanente (agregar a ~/.bashrc o ~/.zshrc)
echo 'export MI_VARIABLE="valor"' >> ~/.bashrc
source ~/.bashrc
```

**Variables importantes:**
```bash
PATH      # Rutas de ejecutables
HOME      # Directorio del usuario
USER      # Nombre de usuario
SHELL     # Shell actual
```

**Ejercicio Práctico 7:**
```bash
echo $PATH
export API_KEY="mi_clave_secreta"
echo $API_KEY
```

### 2.2 Gestión de Paquetes

**Para sistemas basados en Debian/Ubuntu (apt):**
```bash
sudo apt update                    # Actualizar lista de paquetes
sudo apt upgrade                   # Actualizar paquetes instalados
sudo apt install nombre_paquete    # Instalar paquete
sudo apt remove nombre_paquete     # Desinstalar
sudo apt search término            # Buscar paquetes
```

**Para sistemas basados en RedHat/CentOS (yum/dnf):**
```bash
sudo yum update
sudo yum install nombre_paquete
sudo yum remove nombre_paquete
```

**Para macOS (homebrew):**
```bash
brew update
brew install nombre_paquete
brew uninstall nombre_paquete
```

**Ejercicio Práctico 8:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install curl wget git

# macOS
brew install wget
```

### 2.3 Compresión y Archivos

**tar** - Empaquetar archivos
```bash
tar -czf archivo.tar.gz directorio/    # Crear tar.gz
tar -xzf archivo.tar.gz                # Extraer tar.gz
tar -czf backup.tar.gz --exclude='node_modules' proyecto/
```

**zip/unzip**
```bash
zip -r archivo.zip directorio/
unzip archivo.zip
unzip archivo.zip -d destino/
```

**Ejercicio Práctico 9:**
```bash
cd ~/curso-docker/modulo1
tar -czf practica-backup.tar.gz practica/
ls -lh practica-backup.tar.gz
tar -xzf practica-backup.tar.gz -C /tmp/
```

### 2.4 Editores de Texto en Terminal

**nano** - Editor simple
```bash
nano archivo.txt
# Ctrl+O: Guardar
# Ctrl+X: Salir
```

**vim** - Editor avanzado
```bash
vim archivo.txt
# i: Modo inserción
# Esc: Modo comando
# :w: Guardar
# :q: Salir
# :wq: Guardar y salir
# :q!: Salir sin guardar
```

**Ejercicio Práctico 10:**
```bash
nano notas.txt
# Escribe algo y guarda
cat notas.txt
```

### 2.5 Shell Scripting Básico

**Crear un script:**
```bash
#!/bin/bash
# Mi primer script

echo "Hola, mundo!"
echo "Usuario actual: $USER"
echo "Directorio: $PWD"
```

**Variables en scripts:**
```bash
#!/bin/bash

NOMBRE="Docker"
VERSION="24.0"

echo "Aprendiendo $NOMBRE versión $VERSION"
```

**Condicionales:**
```bash
#!/bin/bash

if [ -f "archivo.txt" ]; then
    echo "El archivo existe"
else
    echo "El archivo no existe"
fi
```

**Bucles:**
```bash
#!/bin/bash

# For loop
for i in 1 2 3 4 5; do
    echo "Número: $i"
done

# While loop
contador=1
while [ $contador -le 5 ]; do
    echo "Contador: $contador"
    ((contador++))
done
```

**Ejercicio Práctico 11:**
```bash
cd ~/curso-docker/modulo2
nano mi-script.sh
```

Contenido:
```bash
#!/bin/bash
echo "=== Información del Sistema ==="
echo "Usuario: $USER"
echo "Directorio: $PWD"
echo "Fecha: $(date)"
echo "Archivos en directorio:"
ls -l
```

Ejecutar:
```bash
chmod +x mi-script.sh
./mi-script.sh
```

### 2.6 Servicios y Systemd

**systemctl** - Gestión de servicios
```bash
sudo systemctl status servicio     # Ver estado
sudo systemctl start servicio      # Iniciar
sudo systemctl stop servicio       # Detener
sudo systemctl restart servicio    # Reiniciar
sudo systemctl enable servicio     # Iniciar al arranque
sudo systemctl disable servicio    # No iniciar al arranque
```

**journalctl** - Ver logs del sistema
```bash
sudo journalctl -u servicio        # Logs de un servicio
sudo journalctl -f                 # Seguir logs en tiempo real
sudo journalctl --since today      # Logs de hoy
```

---

## Módulo 3: Introducción a Docker

### 3.1 ¿Qué es Docker?

Docker es una plataforma de contenedores que permite:
- Empaquetar aplicaciones con sus dependencias
- Ejecutar aplicaciones de forma aislada
- Garantizar que funcionen igual en cualquier entorno
- Facilitar el despliegue y escalado

**Conceptos clave:**
- **Imagen:** Plantilla de solo lectura (como una clase en POO)
- **Contenedor:** Instancia en ejecución de una imagen (como un objeto)
- **Dockerfile:** Receta para crear una imagen
- **Registry:** Almacén de imágenes (Docker Hub)
- **Volume:** Almacenamiento persistente
- **Network:** Comunicación entre contenedores

### 3.2 Instalación de Docker

**Ubuntu/Debian:**
```bash
# Actualizar sistema
sudo apt update
sudo apt install ca-certificates curl gnupg

# Agregar clave GPG de Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Agregar repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

**macOS:**
```bash
# Descargar Docker Desktop desde:
# https://www.docker.com/products/docker-desktop

# O con Homebrew:
brew install --cask docker
```

**Verificar instalación:**
```bash
docker --version
docker run hello-world
```

### 3.3 Comandos Básicos de Docker

**Gestión de imágenes:**
```bash
docker images                      # Listar imágenes locales
docker pull nombre:tag             # Descargar imagen
docker rmi nombre:tag              # Eliminar imagen
docker image prune                 # Limpiar imágenes no usadas
```

**Gestión de contenedores:**
```bash
docker ps                          # Contenedores en ejecución
docker ps -a                       # Todos los contenedores
docker run nombre                  # Crear y ejecutar contenedor
docker start ID                    # Iniciar contenedor
docker stop ID                     # Detener contenedor
docker rm ID                       # Eliminar contenedor
docker logs ID                     # Ver logs
docker exec -it ID /bin/bash       # Entrar al contenedor
```

**Ejercicio Práctico 12:**
```bash
# Descargar y ejecutar nginx
docker pull nginx
docker images
docker run -d -p 8080:80 --name mi-nginx nginx
docker ps
curl http://localhost:8080
docker logs mi-nginx
docker stop mi-nginx
docker rm mi-nginx
```

### 3.4 Opciones Importantes de docker run

```bash
-d                    # Ejecutar en background (detached)
-p 8080:80            # Mapear puerto host:contenedor
--name mi-contenedor  # Nombrar contenedor
-v /host:/container   # Montar volumen
-e VAR=valor          # Variable de entorno
--rm                  # Eliminar al detener
-it                   # Modo interactivo con terminal
--network nombre      # Conectar a red específica
```

**Ejemplos:**
```bash
# Ejecutar con múltiples opciones
docker run -d \
  --name mi-app \
  -p 3000:3000 \
  -e NODE_ENV=production \
  -v $(pwd):/app \
  node:18

# Modo interactivo
docker run -it ubuntu /bin/bash
```

**Ejercicio Práctico 13:**
```bash
# Ejecutar contenedor interactivo de ubuntu
docker run -it --rm ubuntu:22.04 /bin/bash

# Dentro del contenedor:
apt update
apt install curl
curl https://api.github.com
exit
```

### 3.5 Docker Hub y Registries

**Buscar imágenes:**
```bash
docker search nginx
docker search python
```

**Imágenes oficiales populares:**
- `nginx` - Servidor web
- `node` - Node.js
- `python` - Python
- `postgres` - PostgreSQL
- `mysql` - MySQL
- `redis` - Redis
- `ubuntu` - Ubuntu

**Tags y versiones:**
```bash
docker pull node:18              # Versión específica
docker pull node:18-alpine       # Variante Alpine (más ligera)
docker pull node:latest          # Última versión
```

**Ejercicio Práctico 14:**
```bash
docker search python
docker pull python:3.11-slim
docker images | grep python
docker run -it --rm python:3.11-slim python --version
```

---

## Módulo 4: Dockerfile - Construcción de Imágenes

### 4.1 Anatomía de un Dockerfile

**Estructura básica:**
```dockerfile
# Comentario
FROM imagen_base:tag
WORKDIR /ruta/trabajo
COPY origen destino
RUN comando
ENV VARIABLE=valor
EXPOSE puerto
CMD ["ejecutable", "arg1"]
```

**Instrucciones principales:**

- **FROM:** Imagen base
- **WORKDIR:** Directorio de trabajo
- **COPY:** Copiar archivos del host al contenedor
- **ADD:** Como COPY pero puede descargar URLs y descomprimir
- **RUN:** Ejecutar comandos durante la construcción
- **ENV:** Definir variables de entorno
- **EXPOSE:** Documentar puertos (no los publica)
- **CMD:** Comando por defecto al ejecutar
- **ENTRYPOINT:** Punto de entrada principal
- **VOLUME:** Definir punto de montaje
- **USER:** Usuario para ejecutar comandos
- **ARG:** Variables de construcción

### 4.2 Construcción de Imágenes

```bash
docker build -t nombre:tag .
docker build -t nombre:tag -f Dockerfile.prod .
docker build --no-cache -t nombre:tag .
```

**Opciones:**
- `-t` : Tag/nombre de la imagen
- `-f` : Especificar Dockerfile alternativo
- `--no-cache` : No usar caché de capas
- `--build-arg` : Pasar argumentos de construcción

### 4.3 Mejores Prácticas

1. **Usar imágenes base oficiales y específicas:**
```dockerfile
# Bien
FROM node:18-alpine

# Evitar
FROM node:latest
```

2. **Minimizar capas combinando RUN:**
```dockerfile
# Bien
RUN apt update && apt install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Evitar
RUN apt update
RUN apt install -y curl
RUN apt install -y git
```

3. **Aprovechar el caché de capas:**
```dockerfile
# Copiar package.json primero (cambia poco)
COPY package*.json ./
RUN npm install

# Copiar código después (cambia frecuentemente)
COPY . .
```

4. **Usar .dockerignore:**
```
node_modules
npm-debug.log
.git
.env
*.md
.DS_Store
```

5. **No ejecutar como root:**
```dockerfile
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs
```

6. **Multi-stage builds para imágenes pequeñas:**
```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm install --production
CMD ["node", "dist/index.js"]
```

### 4.4 Gestión de Capas y Caché

Cada instrucción en Dockerfile crea una capa. Docker cachea capas para builds más rápidos.

**Orden óptimo (de menos a más cambiante):**
1. Imagen base (FROM)
2. Dependencias del sistema (RUN apt install)
3. Archivos de dependencias (COPY package.json)
4. Instalación de dependencias (RUN npm install)
5. Código fuente (COPY . .)
6. Build (RUN npm run build)
7. Comando de ejecución (CMD)

---

## Módulo 5: Docker Compose

### 5.1 ¿Qué es Docker Compose?

Docker Compose permite definir y ejecutar aplicaciones multi-contenedor usando archivos YAML.

**Ventajas:**
- Configuración declarativa
- Un solo comando para levantar toda la aplicación
- Gestión de redes y volúmenes automática
- Fácil para desarrollo y testing

### 5.2 Estructura de docker-compose.yml

```yaml
version: '3.8'

services:
  nombre-servicio:
    image: imagen:tag
    # o
    build: ./ruta
    ports:
      - "8080:80"
    environment:
      - VAR=valor
    volumes:
      - ./host:/container
    depends_on:
      - otro-servicio
    networks:
      - mi-red

networks:
  mi-red:
    driver: bridge

volumes:
  mi-volumen:
```

### 5.3 Comandos de Docker Compose

```bash
docker compose up                 # Iniciar servicios
docker compose up -d              # En background
docker compose down               # Detener y eliminar
docker compose down -v            # También eliminar volúmenes
docker compose ps                 # Ver servicios
docker compose logs               # Ver logs
docker compose logs -f servicio   # Seguir logs
docker compose exec servicio bash # Entrar a contenedor
docker compose build              # Construir imágenes
docker compose restart            # Reiniciar servicios
```

### 5.4 Redes en Docker

**Tipos de redes:**
- **bridge:** Red por defecto, aislada
- **host:** Usa la red del host
- **none:** Sin red

**Comandos:**
```bash
docker network ls                 # Listar redes
docker network create mi-red      # Crear red
docker network inspect mi-red     # Inspeccionar
docker network rm mi-red          # Eliminar
```

**En docker-compose.yml:**
```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

services:
  web:
    networks:
      - frontend
  api:
    networks:
      - frontend
      - backend
  database:
    networks:
      - backend
```

### 5.5 Volúmenes en Docker

**Tipos de montaje:**
1. **Volumes:** Gestionados por Docker (recomendado para producción)
2. **Bind mounts:** Montar directorio del host
3. **tmpfs:** En memoria (temporal)

**Comandos:**
```bash
docker volume ls                  # Listar volúmenes
docker volume create mi-volumen   # Crear
docker volume inspect mi-volumen  # Inspeccionar
docker volume rm mi-volumen       # Eliminar
docker volume prune               # Limpiar no usados
```

**En docker-compose.yml:**
```yaml
volumes:
  datos-db:
  cache:

services:
  database:
    volumes:
      - datos-db:/var/lib/postgresql/data
      - ./backup:/backup  # Bind mount

  redis:
    volumes:
      - cache:/data
```

**Casos de uso:**

1. **Persistencia de datos:**
```yaml
services:
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

2. **Desarrollo con hot reload:**
```yaml
services:
  app:
    volumes:
      - ./src:/app/src  # Cambios se reflejan inmediatamente
      - node_modules:/app/node_modules  # Evitar sobrescribir
```

3. **Compartir datos entre contenedores:**
```yaml
services:
  app:
    volumes:
      - shared:/data

  worker:
    volumes:
      - shared:/data

volumes:
  shared:
```

**Permisos y ownership:**
```bash
# Ver permisos en volumen
docker run --rm -v mi-volumen:/data alpine ls -la /data

# Cambiar ownership
docker run --rm -v mi-volumen:/data alpine chown -R 1000:1000 /data
```

**Backup y restore:**
```bash
# Backup
docker run --rm \
  -v mi-volumen:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data

# Restore
docker run --rm \
  -v mi-volumen:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /
```

---

## Proyectos Prácticos

### Proyecto 1: Web Estática HTML

Ver: [01-html-estatico.md](./proyectos/01-html-estatico.md)

### Proyecto 2: Web con JavaScript

Ver: [02-html-javascript.md](./proyectos/02-html-javascript.md)

### Proyecto 3: API con FastAPI (Python)

Ver: [03-fastapi.md](./proyectos/03-fastapi.md)

### Proyecto 4: Frontend con React

Ver: [04-react-frontend.md](./proyectos/04-react-frontend.md)

### Proyecto 5: Backend con Node.js + TypeScript

Ver: [05-node-typescript.md](./proyectos/05-node-typescript.md)

### Proyecto 6: Backend con Astro JS

Ver: [06-astro-backend.md](./proyectos/06-astro-backend.md)

### Proyecto 7: Backend con Java (Spring Boot)

Ver: [07-java-spring.md](./proyectos/07-java-spring.md)

### Proyecto 8: Full Stack - React + Node + PostgreSQL

Ver: [08-fullstack-completo.md](./proyectos/08-fullstack-completo.md)

---

## Recursos Adicionales

### Comandos de Referencia Rápida

**Docker:**
```bash
docker --help
docker COMANDO --help
docker system df              # Uso de disco
docker system prune           # Limpiar todo
docker stats                  # Uso de recursos
```

**Docker Compose:**
```bash
docker compose --help
docker compose config         # Validar archivo
docker compose top            # Procesos en ejecución
```

### Debugging

**Ver logs:**
```bash
docker logs contenedor
docker logs -f contenedor
docker compose logs -f
```

**Inspeccionar:**
```bash
docker inspect contenedor
docker inspect imagen
docker network inspect red
```

**Entrar al contenedor:**
```bash
docker exec -it contenedor /bin/bash
docker exec -it contenedor sh  # Si no tiene bash
```

**Ver procesos:**
```bash
docker top contenedor
docker stats contenedor
```

### Troubleshooting Común

**Puerto ya en uso:**
```bash
# Ver qué usa el puerto
lsof -i :8080
netstat -tulpn | grep 8080

# Cambiar puerto en docker run o compose
```

**Contenedor se detiene inmediatamente:**
```bash
# Ver logs
docker logs contenedor

# Verificar CMD/ENTRYPOINT en Dockerfile
```

**Problemas de permisos:**
```bash
# Ejecutar como usuario específico
docker run --user $(id -u):$(id -g) ...
```

**Imagen muy grande:**
```bash
# Usar imagen alpine
# Usar multi-stage builds
# Agregar .dockerignore
```

---

## Glosario

- **Contenedor:** Instancia en ejecución de una imagen
- **Imagen:** Plantilla inmutable para crear contenedores
- **Dockerfile:** Archivo de texto con instrucciones para crear una imagen
- **Registry:** Repositorio de imágenes (ej: Docker Hub)
- **Tag:** Etiqueta de versión de una imagen
- **Layer/Capa:** Cada instrucción en Dockerfile crea una capa
- **Volume:** Almacenamiento persistente para contenedores
- **Network:** Red virtual para comunicación entre contenedores
- **Compose:** Herramienta para aplicaciones multi-contenedor
- **Service:** Contenedor definido en docker-compose.yml
- **Stack:** Conjunto de servicios que forman una aplicación

---

## Siguientes Pasos

Después de completar este curso, puedes explorar:

1. **Kubernetes** - Orquestación de contenedores a escala
2. **CI/CD con Docker** - Integración y despliegue continuo
3. **Docker Swarm** - Orquestación nativa de Docker
4. **Seguridad en Docker** - Buenas prácticas de seguridad
5. **Optimización de imágenes** - Reducir tamaño y mejorar builds
6. **Monitoreo y Logging** - Prometheus, Grafana, ELK stack
7. **Microservicios** - Arquitectura de microservicios con Docker

---

**¡Felicidades por comenzar tu viaje en Linux y Docker!**
