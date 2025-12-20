# 🚀 Inicio Rápido - Jenkins con Docker

Guía rápida para poner en marcha Jenkins con Docker en minutos.

## ⚡ Instalación Rápida

### Opción 1: Docker Compose (Recomendado)

```bash
# 1. Ir al directorio docker
cd docker

# 2. Construir e iniciar Jenkins
docker compose build
docker compose up -d

# 3. Obtener password inicial
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# 4. Abrir navegador
open http://localhost:8080
```

### Opción 2: Docker Run Simple

```bash
# Crear volumen
docker volume create jenkins_home

# Ejecutar Jenkins
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts

# Obtener password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## 📋 Configuración Inicial

1. **Desbloquear Jenkins**
   - Pega el password inicial
   - Click en "Continue"

2. **Instalar Plugins**
   - Selecciona "Install suggested plugins"
   - Espera a que termine la instalación

3. **Crear Usuario Admin**
   - Username: `admin`
   - Password: `tu_password_seguro`
   - Full name: `Tu Nombre`
   - Email: `tu@email.com`

4. **Configurar URL**
   - Usa: `http://localhost:8080/`
   - Click en "Save and Finish"

## 🎯 Crear tu Primer Pipeline

### Método 1: Pipeline Simple

1. Click en **"New Item"**
2. Nombre: `mi-primer-pipeline`
3. Tipo: **Pipeline**
4. En "Pipeline script", pega:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Hello') {
            steps {
                echo '¡Hola desde Jenkins!'
                sh 'docker --version'
            }
        }
    }
}
```

5. Click **"Save"** → **"Build Now"**

### Método 2: Pipeline desde Repositorio

1. Click en **"New Item"**
2. Nombre: `nodejs-app-pipeline`
3. Tipo: **Pipeline**
4. En "Pipeline":
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/usuario/repo.git`
   - Script Path: `Jenkinsfile`
5. Click **"Save"** → **"Build Now"**

## 📦 Usar Ejemplos Incluidos

### Ejemplo 1: Pipeline Básico

```bash
# Copiar contenido de:
cat pipelines/01-basic-pipeline.jenkinsfile

# Crear nuevo Pipeline en Jenkins y pegar el contenido
```

### Ejemplo 2: Build Docker

```bash
# Copiar contenido de:
cat pipelines/02-docker-build.jenkinsfile

# Crear nuevo Pipeline en Jenkins y pegar el contenido
```

### Ejemplo 3: Aplicación Node.js

```bash
# Ir al ejemplo
cd ejemplos/nodejs-app

# Ver el Jenkinsfile
cat Jenkinsfile

# Crear Pipeline en Jenkins apuntando a este directorio
```

## 🔧 Comandos Útiles

### Gestión de Jenkins

```bash
# Ver logs
docker logs -f jenkins

# Reiniciar
docker restart jenkins

# Detener
docker stop jenkins

# Iniciar
docker start jenkins

# Eliminar (¡cuidado!)
docker stop jenkins && docker rm jenkins
```

### Backup y Restore

```bash
# Crear backup
./scripts/backup-jenkins.sh

# Restaurar backup
./scripts/restore-jenkins.sh backups/jenkins-backup-YYYYMMDD.tar.gz

# Limpiar builds antiguos
./scripts/cleanup-old-builds.sh 30
```

### Verificar Instalación

```bash
# Verificar que Jenkins está corriendo
docker ps | grep jenkins

# Verificar que Docker funciona dentro de Jenkins
docker exec jenkins docker ps

# Verificar plugins instalados
docker exec jenkins ls /var/jenkins_home/plugins
```

## 🐛 Troubleshooting

### Jenkins no inicia

```bash
# Ver logs
docker logs jenkins

# Verificar puerto
lsof -i :8080

# Reiniciar
docker restart jenkins
```

### No puedo usar Docker en Jenkins

```bash
# Dar permisos
docker exec -u root jenkins chmod 666 /var/run/docker.sock

# Reiniciar Jenkins
docker restart jenkins
```

### Jenkins muy lento

```bash
# Aumentar memoria en docker-compose.yml
environment:
  - JAVA_OPTS=-Xmx2048m -Xms512m

# Reiniciar
docker compose restart
```

### Olvidé la contraseña

```bash
# Obtener password inicial
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# O resetear seguridad (¡cuidado!)
docker exec jenkins rm /var/jenkins_home/config.xml
docker restart jenkins
```

## 📚 Próximos Pasos

1. **Explorar Ejemplos**
   - Revisa `pipelines/` para más ejemplos
   - Prueba la app Node.js en `ejemplos/nodejs-app/`

2. **Configurar Credenciales**
   - Manage Jenkins → Manage Credentials
   - Añade credenciales de Docker Hub, GitHub, etc.

3. **Instalar Plugins Adicionales**
   - Manage Jenkins → Manage Plugins
   - Busca: Blue Ocean, SonarQube, Kubernetes, etc.

4. **Configurar Webhooks**
   - Conecta con GitHub/GitLab
   - Builds automáticos en cada push

5. **Leer la Guía Completa**
   - Ver `README.md` para documentación completa
   - Explorar módulos avanzados

## 🔗 Enlaces Útiles

- **Jenkins UI**: http://localhost:8080
- **SonarQube**: http://localhost:9000 (si está habilitado)
- **Nexus**: http://localhost:8081 (si está habilitado)

## 💡 Tips

- **Usa Blue Ocean** para una interfaz moderna
- **Guarda tus Jenkinsfiles** en Git
- **Haz backups regulares** de Jenkins
- **Usa agentes Docker** para builds aislados
- **Parametriza tus pipelines** para flexibilidad

---

**¡Listo para empezar! 🎉**

Para más información, consulta el [README principal](README.md).
