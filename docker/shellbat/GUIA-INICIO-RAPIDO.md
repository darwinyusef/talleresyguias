# 🚀 Guía de Inicio Rápido - Ejemplos Python

## ¿Qué encontrarás aquí?

Este repositorio contiene ejemplos completos de manejo de archivos y ejecución de scripts en **Python**, equivalentes a los ejemplos de Node.js.

## 📁 Estructura del Proyecto

```
shellbat/
├── ejemplos/                    # Ejemplos en Node.js
│   ├── manejo-archivos.js
│   ├── ejecutar-script.js
│   ├── script-ejemplo.sh
│   └── datos.csv
│
├── ejemplos-python/             # Ejemplos en Python ⭐
│   ├── manejo-archivos.py
│   ├── ejecutar-script.py
│   ├── ejercicios.py
│   ├── script-ejemplo.sh
│   ├── datos.csv
│   └── README.md
│
├── taller-node-shell.md         # Taller completo Node.js
├── PYTHON-VS-NODE.md            # Comparación Python vs Node.js
└── GUIA-INICIO-RAPIDO.md        # Este archivo
```

## 🎯 Inicio Rápido - 3 pasos

### 1. Navega a la carpeta de ejemplos Python

```bash
cd ejemplos-python
```

### 2. Ejecuta los ejemplos

```bash
# Ejemplos de manejo de archivos (8 ejemplos)
python3 manejo-archivos.py

# Ejemplos de ejecución de scripts (6 métodos)
python3 ejecutar-script.py

# Ejercicios prácticos (menú interactivo)
python3 ejercicios.py
```

### 3. ¡Listo! 🎉

Los scripts generarán archivos de ejemplo y mostrarán resultados en la terminal.

---

## 📚 ¿Qué incluye cada archivo?

### `manejo-archivos.py`
Ejecuta automáticamente 8 ejemplos:

1. ✅ Lectura y escritura de archivos de texto
2. ✅ Trabajar con JSON
3. ✅ Obtener información de archivos
4. ✅ Crear y listar directorios
5. ✅ Copiar y mover archivos
6. ✅ Procesar archivos CSV
7. ✅ Leer archivos grandes con generadores
8. ✅ Usar pathlib (API orientada a objetos)

**Genera:**
- `ejemplo-py.txt`
- `config-py.json`
- `datos-from-csv-py.json`
- `archivo-grande-py.txt`
- `prueba-directorio-py/`

### `ejecutar-script.py`
Demuestra 6 formas de ejecutar scripts shell:

1. ✅ `subprocess.run()` - Método recomendado
2. ✅ `subprocess.Popen()` - Salida en tiempo real
3. ✅ `subprocess.check_output()` - Captura de salida
4. ✅ Comandos simples del sistema
5. ✅ Ejecución con timeout
6. ✅ Comandos encadenados (pipelines)

**Ejecuta:**
- `script-ejemplo.sh` con diferentes métodos
- Comandos del sistema (`ls`, `python --version`, etc.)

### `ejercicios.py`
5 ejercicios prácticos con soluciones completas:

1. **CSV a JSON** - Convertir archivos CSV a JSON
2. **Limpiador de temporales** - Eliminar archivos antiguos
3. **Ejecutor de build** - Pipeline de construcción
4. **Monitor de cambios** - Detectar cambios en directorios
5. **Sincronizador** - Sincronizar dos directorios

**Genera:**
- `datos-ejercicio1.json`
- `reporte-limpieza-py.json`
- `build-py.log`
- `reporte-sincronizacion-py.json`

---

## 💡 Ejemplos de Uso

### Leer un archivo

```python
# Método estándar
with open('archivo.txt', 'r', encoding='utf-8') as f:
    contenido = f.read()
    print(contenido)

# Método pathlib (más moderno)
from pathlib import Path
contenido = Path('archivo.txt').read_text(encoding='utf-8')
```

### Escribir JSON

```python
import json

datos = {'nombre': 'Juan', 'edad': 25}

with open('datos.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)
```

### Ejecutar un script shell

```python
import subprocess

resultado = subprocess.run(
    ['bash', 'script.sh', 'arg1', 'arg2'],
    capture_output=True,
    text=True
)

print(resultado.stdout)
```

### Listar archivos

```python
from pathlib import Path

# Todos los archivos
for archivo in Path('.').iterdir():
    print(archivo.name)

# Solo archivos .txt
for archivo in Path('.').glob('*.txt'):
    print(archivo.name)
```

---

## 🔥 Tips Importantes

### 1. Usa `with` siempre que abras archivos
```python
# ✅ Correcto - el archivo se cierra automáticamente
with open('archivo.txt', 'r') as f:
    data = f.read()

# ❌ Incorrecto - debes cerrar manualmente
f = open('archivo.txt', 'r')
data = f.read()
f.close()
```

### 2. Especifica encoding
```python
# ✅ Correcto
with open('archivo.txt', 'r', encoding='utf-8') as f:
    data = f.read()

# ⚠️ Puede fallar en diferentes sistemas
with open('archivo.txt', 'r') as f:
    data = f.read()
```

### 3. Usa pathlib para rutas
```python
from pathlib import Path

# ✅ Correcto - multiplataforma
archivo = Path('carpeta') / 'subcarpeta' / 'archivo.txt'

# ❌ Puede fallar en Windows
archivo = 'carpeta/subcarpeta/archivo.txt'
```

### 4. subprocess.run() es mejor que os.system()
```python
import subprocess

# ✅ Correcto
resultado = subprocess.run(['ls', '-la'], capture_output=True)

# ❌ Evitar (inseguro, difícil de controlar)
import os
os.system('ls -la')
```

---

## 🆚 Python vs Node.js

Si vienes de Node.js, consulta `PYTHON-VS-NODE.md` para ver comparaciones lado a lado.

### Diferencias principales:

| Aspecto | Node.js | Python |
|---------|---------|--------|
| Async | Promesas/async-await | with/context managers |
| JSON | `JSON.parse/stringify` | `json.load/dump` |
| CSV | Librería externa | Built-in (`csv`) |
| Rutas | `path.join()` | `pathlib.Path()` |
| Subprocess | `child_process` | `subprocess` |

---

## 📖 Recursos para Aprender Más

### Documentación oficial
- [Python os module](https://docs.python.org/3/library/os.html)
- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python subprocess](https://docs.python.org/3/library/subprocess.html)
- [Python json](https://docs.python.org/3/library/json.html)
- [Python csv](https://docs.python.org/3/library/csv.html)

### Tutoriales recomendados
- [Real Python - Working with Files](https://realpython.com/working-with-files-in-python/)
- [Python File Handling](https://docs.python.org/3/tutorial/inputoutput.html)

---

## 🎓 Orden de Aprendizaje Sugerido

1. **Empieza aquí** → Ejecuta `manejo-archivos.py` para ver todos los ejemplos básicos

2. **Scripts shell** → Ejecuta `ejecutar-script.py` para aprender a ejecutar comandos

3. **Practica** → Usa `ejercicios.py` y resuelve los ejercicios interactivos

4. **Compara** → Lee `PYTHON-VS-NODE.md` si vienes de Node.js

5. **Profundiza** → Lee el `README.md` en `ejemplos-python/` para más detalles

---

## ❓ FAQ

### ¿Qué versión de Python necesito?
Python 3.7 o superior. Verifica con: `python3 --version`

### ¿Necesito instalar dependencias?
No para los ejemplos básicos. Solo para el ejercicio 4 (monitor de archivos):
```bash
pip install watchdog
```

### ¿Los scripts funcionan en Windows?
Sí, están diseñados para ser multiplataforma. Los ejemplos detectan automáticamente el sistema operativo.

### ¿Dónde están los archivos generados?
En la misma carpeta `ejemplos-python/` donde ejecutas los scripts.

### ¿Puedo ejecutar los scripts desde otra ubicación?
Sí, pero usa rutas absolutas o navega primero a `ejemplos-python/`

---

## 🚀 Siguiente Paso

```bash
cd ejemplos-python
python3 manejo-archivos.py
```

¡Disfruta aprendiendo Python! 🐍
