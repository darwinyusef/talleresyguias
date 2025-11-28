# Ejemplos de Manejo de Archivos y Scripts en Python

Esta carpeta contiene ejemplos prácticos equivalentes a los de Node.js, pero implementados en Python.

## 📚 Contenido

### Archivos Principales
- **manejo-archivos.py** - Ejemplos de operaciones con archivos en Python
- **ejecutar-script.py** - Ejemplos de ejecución de scripts shell desde Python
- **ejercicios.py** - 5 ejercicios prácticos con soluciones
- **datos.csv** - Archivo CSV de prueba

### Scripts Shell
- **script-ejemplo.sh** - Script shell de ejemplo (Unix/Linux/Mac)
- **script-ejemplo.bat** - Script batch de ejemplo (Windows)

## 🚀 Comenzar

### Requisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación de dependencias opcionales

```bash
# Para el ejercicio de monitoreo de archivos
pip install watchdog
```

## 📖 Cómo usar estos ejemplos

### 1. Ejecutar ejemplos de manejo de archivos

```bash
# Dar permisos de ejecución (Unix/Linux/Mac)
chmod +x manejo-archivos.py

# Ejecutar
python3 manejo-archivos.py
```

Este script ejecuta automáticamente 8 ejemplos:
1. ✅ Lectura y escritura de archivos de texto
2. ✅ Trabajar con JSON
3. ✅ Información de archivos (stats)
4. ✅ Operaciones con directorios
5. ✅ Copiar y mover archivos
6. ✅ Procesamiento de CSV
7. ✅ Lectura de archivos grandes con generadores
8. ✅ Trabajar con Path (pathlib)

### 2. Ejecutar ejemplos de scripts shell

```bash
# Dar permisos de ejecución
chmod +x ejecutar-script.py
chmod +x script-ejemplo.sh

# Ejecutar
python3 ejecutar-script.py
```

Este script demuestra 6 métodos diferentes:
1. ✅ `subprocess.run()` - Método recomendado
2. ✅ `subprocess.Popen()` - Salida en tiempo real
3. ✅ `subprocess.check_output()` - Captura de salida
4. ✅ Comandos simples del sistema
5. ✅ Ejecución con timeout
6. ✅ Comandos encadenados (pipelines)

### 3. Ejecutar ejercicios prácticos

```bash
# Dar permisos de ejecución
chmod +x ejercicios.py

# Ejecutar menú interactivo
python3 ejercicios.py
```

Los ejercicios incluyen:
1. **CSV a JSON** - Convertir archivos CSV a formato JSON
2. **Limpiar temporales** - Eliminar archivos antiguos por extensión
3. **Ejecutor de build** - Pipeline de build con múltiples pasos
4. **Monitor de cambios** - Detectar cambios en directorios
5. **Sincronizador** - Sincronizar dos directorios

## 📊 Comparación: Python vs Node.js

### Lectura de archivos

**Node.js:**
```javascript
const fs = require('fs').promises;
const data = await fs.readFile('archivo.txt', 'utf8');
```

**Python:**
```python
with open('archivo.txt', 'r', encoding='utf-8') as f:
    data = f.read()
```

### Escritura de archivos

**Node.js:**
```javascript
await fs.writeFile('archivo.txt', contenido, 'utf8');
```

**Python:**
```python
with open('archivo.txt', 'w', encoding='utf-8') as f:
    f.write(contenido)
```

### Trabajar con JSON

**Node.js:**
```javascript
const data = JSON.parse(await fs.readFile('config.json', 'utf8'));
await fs.writeFile('config.json', JSON.stringify(data, null, 2));
```

**Python:**
```python
with open('config.json', 'r') as f:
    data = json.load(f)

with open('config.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Ejecutar comandos shell

**Node.js:**
```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);
const { stdout } = await execPromise('ls -la');
```

**Python:**
```python
import subprocess
resultado = subprocess.run(['ls', '-la'], capture_output=True, text=True)
salida = resultado.stdout
```

### Listar archivos en directorio

**Node.js:**
```javascript
const archivos = await fs.readdir('./');
```

**Python:**
```python
import os
archivos = os.listdir('./')

# O con pathlib (más moderno)
from pathlib import Path
archivos = [f.name for f in Path('.').iterdir()]
```

### Copiar archivos

**Node.js:**
```javascript
await fs.copyFile('origen.txt', 'destino.txt');
```

**Python:**
```python
import shutil
shutil.copy2('origen.txt', 'destino.txt')
```

## 💡 Ventajas de Python para manejo de archivos

### 1. Context Managers (with statement)
Python tiene un sistema elegante para manejar recursos:

```python
# El archivo se cierra automáticamente
with open('archivo.txt', 'r') as f:
    contenido = f.read()
# Ya está cerrado aquí
```

### 2. Pathlib - API Orientada a Objetos
```python
from pathlib import Path

archivo = Path('datos.txt')
print(archivo.name)        # 'datos.txt'
print(archivo.suffix)      # '.txt'
print(archivo.parent)      # '.'
print(archivo.exists())    # True/False

# Navegar directorios
for txt_file in Path('.').glob('*.txt'):
    print(txt_file)
```

### 3. Generadores para archivos grandes
```python
def leer_lineas(archivo):
    with open(archivo) as f:
        for linea in f:
            yield linea.strip()

# No carga todo en memoria
for linea in leer_lineas('archivo-grande.txt'):
    proceso(linea)
```

### 4. CSV y JSON nativos
```python
import csv
import json

# CSV es súper simple
with open('datos.csv') as f:
    reader = csv.DictReader(f)
    datos = list(reader)

# JSON también
with open('config.json') as f:
    config = json.load(f)
```

### 5. Subprocess robusto
```python
import subprocess

# Método moderno y seguro
resultado = subprocess.run(
    ['comando', 'arg1', 'arg2'],
    capture_output=True,
    text=True,
    timeout=5,
    check=True  # Lanza excepción si falla
)
```

## 🎯 Módulos útiles de Python

### Módulos estándar (incluidos con Python)
- **os** - Interactuar con el sistema operativo
- **pathlib** - Rutas orientadas a objetos (recomendado)
- **shutil** - Operaciones de alto nivel (copiar, mover, etc.)
- **subprocess** - Ejecutar comandos del sistema
- **json** - Trabajar con JSON
- **csv** - Leer y escribir CSV
- **glob** - Búsqueda de archivos con patrones

### Módulos de terceros (instalar con pip)
- **watchdog** - Monitorear cambios en archivos/directorios
- **pandas** - Procesamiento avanzado de CSV/Excel
- **openpyxl** - Trabajar con archivos Excel
- **PyPDF2** - Manipular archivos PDF
- **Pillow** - Procesar imágenes

## 📝 Ejercicios para practicar

Todos los ejercicios están implementados en `ejercicios.py`:

### Ejercicio 1: CSV a JSON
```bash
python3 ejercicios.py
# Selecciona opción 1
```

### Ejercicio 2: Limpieza de archivos
```bash
python3 ejercicios.py
# Selecciona opción 2
```

### Ejercicio 3: Build pipeline
```bash
python3 ejercicios.py
# Selecciona opción 3
```

### Ejercicio 4: Monitor de archivos
```bash
# Instala watchdog primero
pip install watchdog

python3 ejercicios.py
# Selecciona opción 4
```

### Ejercicio 5: Sincronizador
```bash
python3 ejercicios.py
# Selecciona opción 5
```

## 🔧 Tips y Best Practices

### 1. Siempre usa context managers
```python
# ✅ Bueno
with open('archivo.txt', 'r') as f:
    data = f.read()

# ❌ Malo
f = open('archivo.txt', 'r')
data = f.read()
f.close()  # Podría no ejecutarse si hay error
```

### 2. Usa pathlib para rutas
```python
# ✅ Bueno - multiplataforma
from pathlib import Path
ruta = Path('carpeta') / 'subcarpeta' / 'archivo.txt'

# ❌ Malo - específico de plataforma
ruta = 'carpeta/subcarpeta/archivo.txt'  # Falla en Windows
```

### 3. Maneja excepciones específicas
```python
# ✅ Bueno
try:
    with open('archivo.txt') as f:
        data = f.read()
except FileNotFoundError:
    print('Archivo no encontrado')
except PermissionError:
    print('Sin permisos')

# ❌ Malo
try:
    with open('archivo.txt') as f:
        data = f.read()
except:
    print('Error')  # ¿Qué error?
```

### 4. Usa encoding explícito
```python
# ✅ Bueno
with open('archivo.txt', 'r', encoding='utf-8') as f:
    data = f.read()

# ❌ Malo
with open('archivo.txt', 'r') as f:  # Usa encoding del sistema
    data = f.read()
```

### 5. subprocess.run() sobre os.system()
```python
# ✅ Bueno
import subprocess
resultado = subprocess.run(['ls', '-la'], capture_output=True)

# ❌ Malo (inseguro, difícil de controlar)
import os
os.system('ls -la')
```

## 📚 Recursos adicionales

- [Documentación oficial de Python - os](https://docs.python.org/3/library/os.html)
- [Documentación oficial de Python - pathlib](https://docs.python.org/3/library/pathlib.html)
- [Documentación oficial de Python - subprocess](https://docs.python.org/3/library/subprocess.html)
- [Real Python - Working with Files](https://realpython.com/working-with-files-in-python/)
- [Python CSV Module](https://docs.python.org/3/library/csv.html)

## 🎉 Ejemplos ejecutados

Cuando ejecutes los scripts, se generarán estos archivos:

```
ejemplos-python/
├── ejemplo-py.txt              # Del ejemplo 1
├── ejemplo-renombrado-py.txt   # Del ejemplo 5
├── config-py.json              # Del ejemplo 2
├── datos-from-csv-py.json      # Del ejemplo 6
├── archivo-grande-py.txt       # Del ejemplo 7
├── prueba-directorio-py/       # Del ejemplo 4
├── datos-ejercicio1.json       # Del ejercicio 1
├── reporte-limpieza-py.json    # Del ejercicio 2
├── build-py.log                # Del ejercicio 3
└── reporte-sincronizacion-py.json  # Del ejercicio 5
```

---

¡Feliz codificación en Python! 🐍
