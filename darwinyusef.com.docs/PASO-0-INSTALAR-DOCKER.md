# 🐳 PASO 0: Instalar Docker en el Servidor

Guía paso a paso para instalar Docker y Docker Compose en tu servidor.

---

## 📋 Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Docker](#instalación-de-docker)
3. [Instalación de Docker Compose](#instalación-de-docker-compose)
4. [Configuración Post-Instalación](#configuración-post-instalación)
5. [Verificación](#verificación)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Requisitos Previos

### Sistema Operativo

Este tutorial cubre:
- ✅ Ubuntu 20.04 / 22.04 / 24.04 (recomendado)
- ✅ Debian 10 / 11 / 12
- ✅ CentOS 7 / 8
- ✅ Rocky Linux 8 / 9

### Acceso al Servidor

```bash
# Conectar al servidor como root
ssh root@YOUR_SERVER_IP

# O si tienes usuario con sudo
ssh usuario@YOUR_SERVER_IP
```

### Puertos Necesarios

Asegúrate de que estos puertos estén abiertos en el firewall:

```
Puerto   Protocolo   Para qué
───────────────────────────────────────────
22       TCP         SSH (administración)
80       TCP         HTTP (redirige a HTTPS)
443      TCP         HTTPS (sitio web)
443      UDP         HTTP/3 (opcional, Caddy)
```

---

## 🐳 Instalación de Docker

### Opción A: Ubuntu / Debian (Recomendado)

#### Paso 1: Actualizar el Sistema

```bash
# Actualizar lista de paquetes
sudo apt update

# Actualizar paquetes instalados (opcional pero recomendado)
sudo apt upgrade -y
```

#### Paso 2: Instalar Dependencias

```bash
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

#### Paso 3: Agregar Repositorio Oficial de Docker

```bash
# Crear directorio para GPG keys
sudo install -m 0755 -d /etc/apt/keyrings

# Descargar GPG key de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Agregar repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Para Debian:**

Reemplaza la última parte por:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### Paso 4: Instalar Docker Engine

```bash
# Actualizar lista de paquetes
sudo apt update

# Instalar Docker
sudo apt install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin
```

---

### Opción B: Script de Instalación Rápida (Cualquier Linux)

```bash
# Descargar e instalar Docker con script oficial
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Limpiar script
rm get-docker.sh
```

⚠️ **Nota:** Este método instala la última versión. Es rápido pero menos controlado.

---

### Opción C: CentOS / Rocky Linux / RHEL

#### Paso 1: Actualizar el Sistema

```bash
sudo yum update -y
```

#### Paso 2: Instalar Dependencias

```bash
sudo yum install -y yum-utils
```

#### Paso 3: Agregar Repositorio

```bash
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

#### Paso 4: Instalar Docker

```bash
sudo yum install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin
```

#### Paso 5: Iniciar Docker

```bash
# Iniciar servicio
sudo systemctl start docker

# Habilitar inicio automático
sudo systemctl enable docker
```

---

## 📦 Instalación de Docker Compose

### Verificar si ya está instalado

```bash
docker compose version
```

Si ves algo como `Docker Compose version v2.x.x`, ya está instalado y puedes saltar esta sección.

### Instalación Manual (si es necesario)

```bash
# Descargar última versión de Docker Compose
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d '"' -f 4)

sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose

# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker-compose --version
```

---

## ⚙️ Configuración Post-Instalación

### 1. Agregar Usuario al Grupo Docker (Opcional)

Esto permite usar Docker sin `sudo`:

```bash
# Agregar tu usuario al grupo docker
sudo usermod -aG docker $USER

# Aplicar cambios (o logout/login)
newgrp docker
```

**Verificar:**

```bash
# Ahora debería funcionar sin sudo
docker ps
```

### 2. Configurar Inicio Automático

```bash
# Habilitar Docker para que inicie con el sistema
sudo systemctl enable docker
sudo systemctl enable containerd
```

### 3. Configurar Límites de Log (Recomendado)

```bash
# Crear archivo de configuración
sudo mkdir -p /etc/docker

sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

# Reiniciar Docker
sudo systemctl restart docker
```

Esto evita que los logs consuman todo el disco.

### 4. Abrir Puertos en Firewall

#### UFW (Ubuntu/Debian):

```bash
# Instalar UFW si no está
sudo apt install -y ufw

# Permitir SSH (¡IMPORTANTE! hazlo primero)
sudo ufw allow 22/tcp

# Permitir HTTP y HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 443/udp

# Habilitar firewall
sudo ufw enable

# Verificar reglas
sudo ufw status
```

#### Firewalld (CentOS/Rocky):

```bash
# Permitir HTTP y HTTPS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Recargar firewall
sudo firewall-cmd --reload

# Verificar
sudo firewall-cmd --list-all
```

---

## ✅ Verificación

### Test 1: Verificar Versión de Docker

```bash
docker --version
```

**Salida esperada:**

```
Docker version 24.0.7, build afdd53b
```

### Test 2: Verificar Docker Compose

```bash
docker compose version
```

**Salida esperada:**

```
Docker Compose version v2.23.0
```

### Test 3: Verificar que Docker Está Corriendo

```bash
sudo systemctl status docker
```

**Salida esperada:**

```
● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled)
   Active: active (running) since...
```

### Test 4: Ejecutar Contenedor de Prueba

```bash
docker run hello-world
```

**Salida esperada:**

```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Test 5: Verificar Información del Sistema

```bash
docker info
```

Debería mostrar información detallada sin errores.

### Test 6: Verificar Puertos Abiertos

```bash
# Verificar que puertos 80 y 443 están disponibles
sudo netstat -tlnp | grep -E ':(80|443)'
```

Si no muestra nada, los puertos están libres (correcto).

Si muestra algo como Apache o Nginx, necesitas detenerlos:

```bash
# Detener Apache
sudo systemctl stop apache2

# Detener Nginx
sudo systemctl stop nginx

# Deshabilitar inicio automático
sudo systemctl disable apache2
sudo systemctl disable nginx
```

---

## 🔧 Troubleshooting

### Problema: "Cannot connect to the Docker daemon"

**Solución:**

```bash
# Verificar si Docker está corriendo
sudo systemctl status docker

# Si no está corriendo, iniciarlo
sudo systemctl start docker

# Habilitar inicio automático
sudo systemctl enable docker
```

### Problema: "Permission denied while trying to connect to Docker daemon"

**Solución:**

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Logout y login, o ejecutar:
newgrp docker

# Verificar
docker ps
```

### Problema: "Port already in use"

**Causa:** Apache, Nginx u otro servicio está usando puerto 80/443.

**Solución:**

```bash
# Ver qué está usando los puertos
sudo lsof -i :80
sudo lsof -i :443

# Detener servicios
sudo systemctl stop apache2
sudo systemctl stop nginx

# Deshabilitar
sudo systemctl disable apache2
sudo systemctl disable nginx
```

### Problema: Docker se queda sin espacio

**Solución:**

```bash
# Ver uso de disco
docker system df

# Limpiar recursos no usados
docker system prune -a -f

# Limpiar volúmenes no usados
docker volume prune -f
```

### Problema: Error de DNS en contenedores

**Solución:**

```bash
# Editar configuración
sudo nano /etc/docker/daemon.json

# Agregar DNS público
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}

# Reiniciar Docker
sudo systemctl restart docker
```

---

## 📊 Información del Sistema

### Ver Recursos Disponibles

```bash
# CPU y RAM
free -h
nproc

# Disco
df -h

# Memoria usada por Docker
docker system df
```

### Requisitos Mínimos Recomendados

```
CPU:      2 cores
RAM:      2 GB (4 GB recomendado)
Disco:    20 GB libres
```

---

## 🎯 Checklist de Instalación

Antes de continuar al siguiente paso:

- [ ] Docker instalado correctamente
- [ ] Docker Compose instalado
- [ ] `docker --version` funciona
- [ ] `docker compose version` funciona
- [ ] `docker run hello-world` funciona
- [ ] Usuario agregado al grupo docker (opcional)
- [ ] Docker habilitado para inicio automático
- [ ] Puertos 80 y 443 están libres
- [ ] Firewall permite tráfico en puertos 80/443
- [ ] No hay errores en `docker info`

---

## 📚 Comandos Útiles

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores (incluso detenidos)
docker ps -a

# Ver imágenes descargadas
docker images

# Ver uso de recursos
docker stats

# Ver logs de un contenedor
docker logs <container-name>

# Entrar a un contenedor
docker exec -it <container-name> sh

# Detener todos los contenedores
docker stop $(docker ps -q)

# Eliminar todos los contenedores detenidos
docker container prune -f

# Limpiar todo (imágenes, contenedores, volúmenes no usados)
docker system prune -a --volumes -f
```

---

## 🚀 Siguiente Paso

Una vez que Docker esté instalado y funcionando:

➡️ **Continuar con:** [PASO-1-CONFIGURAR-DNS.md](./PASO-1-CONFIGURAR-DNS.md)

---

## 📖 Referencias

- [Documentación Oficial de Docker](https://docs.docker.com/engine/install/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/)

---

**Docker instalado! 🐳**

**Tiempo estimado:** 10-20 minutos
