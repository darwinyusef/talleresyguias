# 📚 Proyecto de Aprendizaje: Bash, Makefiles y Automatización

Este proyecto contiene una colección completa de scripts educativos en Bash y Makefiles para aprender automatización y administración de sistemas.

## 📂 Contenido del Proyecto

### 🔹 Scripts de Bash (10 ejercicios)

Scripts educativos que cubren todos los aspectos fundamentales de Bash:

1. **01_variables_y_tipos.sh** - Variables, arrays, strings y tipos de datos
2. **02_condicionales.sh** - Estructuras condicionales, comparaciones y case
3. **03_bucles.sh** - For, while, until loops e iteraciones
4. **04_funciones.sh** - Funciones, parámetros, scope y recursión
5. **05_archivos_io.sh** - Manejo de archivos, redirección y E/S
6. **06_expresiones_regulares.sh** - Regex, validaciones y pattern matching
7. **07_procesos_jobs.sh** - Procesos, jobs, señales y ejecución paralela
8. **08_operaciones_aritmeticas.sh** - Aritmética, matemáticas y cálculos
9. **09_debugging_errores.sh** - Debugging, logging y manejo de errores
10. **10_proyecto_final.sh** - Sistema completo de gestión de tareas (integra todos los conceptos)

### 🔹 Makefiles

Tres Makefiles especializados para diferentes propósitos:

#### **Makefile.linux** - Comandos Esenciales de Linux
Comandos organizados por categorías:
- Información del sistema
- Gestión de archivos
- Búsqueda y filtrado
- Red y conectividad
- Procesos y monitoreo
- Usuarios y permisos
- Compresión y archivado
- Git y Docker
- Limpieza del sistema

#### **Makefile.nginx** - Servidor Web Nginx
Automatización completa para Nginx:
- Instalación automática (Linux/macOS)
- Configuración de servidor
- Creación de sitio HTML/CSS profesional
- Gestión del servicio (start/stop/restart)
- Testing y logs
- Despliegue completo con un comando

#### **Makefile.docker** - Gestión de Docker
Gestión completa de Docker:
- Instalación de Docker (Linux/macOS)
- Gestión de contenedores e imágenes
- Docker Compose
- Ejemplos rápidos (Nginx, PostgreSQL, Redis, MongoDB)
- Stack de desarrollo completo
- Limpieza y mantenimiento

### 🔹 Ejecutores en Go y Python

Scripts para ejecutar los shells desde otros lenguajes:
- **ejecutar_script.go** - Ejecuta scripts desde Go
- **ejecutar_script.py** - Ejecuta scripts desde Python

## 🚀 Cómo Usar

### Scripts de Bash

Cada script es ejecutable y educativo. Puedes ejecutarlos directamente:

```bash
# Dar permisos de ejecución (si es necesario)
chmod +x *.sh

# Ejecutar un script específico
./01_variables_y_tipos.sh

# O ejecutar todos en orden
for script in {01..10}_*.sh; do
    echo "Ejecutando $script..."
    ./$script
    echo ""
done
```

### Makefiles

#### Linux Commands
```bash
# Ver ayuda
make -f Makefile.linux help

# Información del sistema
make -f Makefile.linux info

# Ver procesos
make -f Makefile.linux process

# Operaciones con archivos
make -f Makefile.linux files

# Monitoreo
make -f Makefile.linux monitoring
```

#### Nginx Server
```bash
# Ver ayuda
make -f Makefile.nginx help

# Despliegue completo (instalar + configurar + crear sitio)
make -f Makefile.nginx deploy

# O paso por paso:
make -f Makefile.nginx install
make -f Makefile.nginx configure
make -f Makefile.nginx create-site
make -f Makefile.nginx start

# Probar el sitio
make -f Makefile.nginx test-site

# Ver logs
make -f Makefile.nginx logs
```

#### Docker
```bash
# Ver ayuda
make -f Makefile.docker help

# Instalar Docker
make -f Makefile.docker install

# Ver información
make -f Makefile.docker info

# Ejecutar servicios rápidamente
make -f Makefile.docker nginx
make -f Makefile.docker postgres
make -f Makefile.docker redis

# Stack de desarrollo completo
make -f Makefile.docker dev-stack

# Crear docker-compose de ejemplo
make -f Makefile.docker compose-example
make -f Makefile.docker compose-up
```

### Ejecutores

#### Go
```bash
# Ejecutar script con Go
go run ejecutar_script.go

# Con argumentos personalizados
go run ejecutar_script.go "Juan" "25"
```

#### Python
```bash
# Ejecutar script con Python
python3 ejecutar_script.py

# Con argumentos personalizados
python3 ejecutar_script.py "Maria" "30"
```

## 📖 Temas Cubiertos

### Bash Scripting
- ✅ Variables y tipos de datos
- ✅ Arrays y arrays asociativos
- ✅ Condicionales y operadores
- ✅ Bucles y control de flujo
- ✅ Funciones y recursión
- ✅ Manejo de archivos y E/S
- ✅ Expresiones regulares
- ✅ Procesos y señales
- ✅ Aritmética y matemáticas
- ✅ Debugging y manejo de errores
- ✅ Proyecto integrador completo

### Make y Automatización
- ✅ Sintaxis de Makefile
- ✅ Targets y dependencias
- ✅ Variables y colores
- ✅ Detección de sistema operativo
- ✅ Comandos condicionales
- ✅ Automatización de tareas complejas

### DevOps y Administración
- ✅ Gestión de servicios (Nginx)
- ✅ Contenedores (Docker)
- ✅ Configuración de servidores
- ✅ Despliegue automatizado
- ✅ Monitoreo y logs
- ✅ Limpieza y mantenimiento

## 💡 Características Especiales

### Scripts Educativos
- 📝 Comentarios detallados
- 🎨 Output colorizado
- ✨ Ejemplos prácticos
- 💪 Ejercicios progresivos
- 🎯 Tips y mejores prácticas

### Makefiles Profesionales
- 🎨 Menús con colores
- 🔍 Detección automática de OS
- 🛡️ Manejo de errores robusto
- 📋 Ayuda integrada
- ⚡ Comandos optimizados

### Proyecto Final
El script `10_proyecto_final.sh` es un sistema completo de gestión de tareas que demuestra:
- Arquitectura profesional
- Sistema de logging
- Validación de entrada
- Manejo de errores
- Persistencia de datos
- CLI interactiva

## 🎓 Rutas de Aprendizaje

### Principiante
1. Ejecuta los scripts del 01 al 04
2. Lee los comentarios y experimenta
3. Prueba el Makefile.linux básico

### Intermedio
1. Completa todos los scripts del 01 al 09
2. Despliega un servidor con Makefile.nginx
3. Ejecuta contenedores con Makefile.docker

### Avanzado
1. Estudia el proyecto final (10_proyecto_final.sh)
2. Crea tu propio stack con Docker
3. Personaliza los Makefiles para tus necesidades

## 📊 Estadísticas del Proyecto

- **10** scripts de Bash educativos
- **3** Makefiles especializados
- **2** ejecutores (Go y Python)
- **1** proyecto final integrador
- **500+** líneas de documentación
- **Más de 3000** líneas de código

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, habrás aprendido:

✅ Bash scripting completo (básico a avanzado)
✅ Automatización con Makefile
✅ Administración de servidores Linux
✅ Gestión de servicios (Nginx)
✅ Containerización con Docker
✅ DevOps y CI/CD básico
✅ Mejores prácticas de scripting
✅ Debugging y troubleshooting

## 🛠️ Requisitos

### Mínimos
- Bash 4.0+
- Make
- Sistema Unix-like (Linux/macOS)

### Opcionales (para Makefiles)
- Nginx (para Makefile.nginx)
- Docker (para Makefile.docker)
- Homebrew (macOS)

## 📝 Notas

- Los scripts están diseñados para ser educativos, no solo funcionales
- Cada script incluye múltiples ejemplos y ejercicios
- Los Makefiles están optimizados para Linux y macOS
- El proyecto final integra todos los conceptos aprendidos

## 🎉 ¡Comienza tu Viaje!

```bash
# Empieza con el primer script
./01_variables_y_tipos.sh

# O explora los Makefiles
make -f Makefile.linux help
make -f Makefile.nginx help
make -f Makefile.docker help
```

## 📚 Recursos Adicionales

- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [GNU Make Documentation](https://www.gnu.org/software/make/manual/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**Happy Learning! 🚀**

*Creado con ❤️ para aprender Bash y automatización*
