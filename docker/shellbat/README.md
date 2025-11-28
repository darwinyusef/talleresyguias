# Taller de Manejo de Archivos en Node.js y Shell Scripts

Este repositorio contiene un taller completo para aprender a manejar archivos en Node.js y ejecutar scripts shell (.sh, .bat).

## 📚 Contenido

### Documentación
- **taller-node-shell.md** - Taller completo con teoría, ejemplos y ejercicios

### Ejemplos Prácticos
- **ejemplos/script-ejemplo.sh** - Script shell de ejemplo (Unix/Linux/Mac)
- **ejemplos/script-ejemplo.bat** - Script batch de ejemplo (Windows)
- **ejemplos/ejecutar-script.js** - Ejemplos de ejecución de scripts desde Node.js
- **ejemplos/manejo-archivos.js** - Ejemplos de operaciones con archivos
- **ejemplos/datos.csv** - Archivo CSV de prueba

## 🚀 Comenzar

### Requisitos
- Node.js v14 o superior
- Terminal/Consola

### Instalación

1. Clona o descarga este repositorio
2. Navega al directorio del proyecto:
   ```bash
   cd filesnshell
   ```

## 📖 Cómo usar este taller

### 1. Lee el taller completo
```bash
# Abre el archivo markdown con tu editor favorito
cat taller-node-shell.md
# o ábrelo con un visualizador de markdown
```

### 2. Ejecuta los ejemplos prácticos

#### En Unix/Linux/Mac:
```bash
# Dar permisos de ejecución al script
chmod +x ejemplos/script-ejemplo.sh

# Ejecutar script directamente
./ejemplos/script-ejemplo.sh arg1 arg2

# Ejecutar ejemplos de manejo de archivos
node ejemplos/manejo-archivos.js

# Ejecutar ejemplos de scripts desde Node.js
node ejemplos/ejecutar-script.js
```

#### En Windows:
```cmd
REM Ejecutar script batch
ejemplos\script-ejemplo.bat arg1 arg2

REM Ejecutar ejemplos de manejo de archivos
node ejemplos\manejo-archivos.js

REM Ejecutar ejemplos de scripts desde Node.js
node ejemplos\ejecutar-script.js
```

### 3. Practica con los ejercicios

El taller incluye 5 ejercicios prácticos con soluciones:
1. Lector de archivos CSV
2. Script de limpieza de archivos temporales
3. Ejecutor de build con múltiples pasos
4. Monitor de cambios en directorios
5. Sincronizador de directorios

## 📋 Estructura del Proyecto

```
filesnshell/
├── README.md                           # Este archivo
├── taller-node-shell.md                # Taller completo
└── ejemplos/
    ├── script-ejemplo.sh               # Script shell de ejemplo
    ├── script-ejemplo.bat              # Script batch de ejemplo
    ├── ejecutar-script.js              # Ejecutar scripts desde Node.js
    ├── manejo-archivos.js              # Operaciones con archivos
    └── datos.csv                       # Datos de prueba
```

## 🎯 Objetivos de Aprendizaje

Al completar este taller aprenderás a:
- ✅ Leer y escribir archivos con Node.js
- ✅ Trabajar con directorios
- ✅ Procesar archivos JSON y CSV
- ✅ Usar streams para archivos grandes
- ✅ Ejecutar scripts shell desde Node.js
- ✅ Crear scripts .sh para Unix/Linux/Mac
- ✅ Crear scripts .bat para Windows
- ✅ Manejar procesos del sistema operativo
- ✅ Crear flujos de trabajo automatizados

## 📚 Temas Cubiertos

### Módulo FS de Node.js
- Lectura y escritura de archivos (síncrona y asíncrona)
- Trabajar con promesas
- Streams para archivos grandes
- Operaciones con directorios
- Información y metadatos de archivos
- Procesamiento de JSON

### Ejecución de Scripts Shell
- Módulo `child_process`
- Métodos: `exec()`, `execFile()`, `spawn()`, `execSync()`
- Pasar argumentos y variables de entorno
- Manejo de salida y errores
- Scripts multiplataforma

### Scripts Shell
- Sintaxis de scripts .sh (Unix/Linux/Mac)
- Sintaxis de scripts .bat (Windows)
- Variables y argumentos
- Condicionales y bucles
- Comandos comunes

## 💡 Recursos Adicionales

- [Documentación oficial de Node.js - File System](https://nodejs.org/api/fs.html)
- [Documentación oficial de Node.js - Child Process](https://nodejs.org/api/child_process.html)
- [Guía de Bash Scripting](https://www.gnu.org/software/bash/manual/)

## 🤝 Contribuir

Si encuentras errores o tienes sugerencias para mejorar el taller, ¡no dudes en contribuir!

## 📝 Licencia

Este taller es de código abierto y está disponible para fines educativos.

---

¡Feliz aprendizaje! 🎉
