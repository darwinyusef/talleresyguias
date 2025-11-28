# 🐍 Ejercicios de Python - Manejo de Archivos y Scripts Shell

> Versión Python de los ejercicios de Node.js

## ✨ ¿Qué hay de nuevo?

He creado **ejercicios equivalentes en Python** basados en los ejemplos de Node.js que ya existían. Ahora puedes aprender ambos lenguajes comparando código lado a lado.

## 📁 Estructura del Proyecto

```
shellbat/
│
├── 📘 GUIA-INICIO-RAPIDO.md     ← ¡EMPIEZA AQUÍ!
├── 📘 PYTHON-VS-NODE.md         ← Comparación lado a lado
├── 📘 taller-node-shell.md      ← Taller completo Node.js
├── 📘 README.md                 ← README original
│
├── 📂 ejemplos/                 ← Ejemplos en Node.js
│   ├── manejo-archivos.js
│   ├── ejecutar-script.js
│   ├── script-ejemplo.sh
│   ├── script-ejemplo.bat
│   └── datos.csv
│
└── 📂 ejemplos-python/          ← ⭐ NUEVOS EJEMPLOS EN PYTHON
    ├── README.md                ← Documentación completa Python
    ├── manejo-archivos.py       ← 8 ejemplos de archivos
    ├── ejecutar-script.py       ← 6 métodos de subprocess
    ├── ejercicios.py            ← 5 ejercicios con soluciones
    ├── script-ejemplo.sh
    ├── script-ejemplo.bat
    └── datos.csv
```

## 🚀 Inicio Rápido

### Opción 1: Node.js (Ejemplos originales)

```bash
cd ejemplos
node manejo-archivos.js
node ejecutar-script.js
```

### Opción 2: Python (Nuevos ejemplos) ⭐

```bash
cd ejemplos-python
python3 manejo-archivos.py
python3 ejecutar-script.py
python3 ejercicios.py
```

## 📚 ¿Qué incluyen los nuevos archivos Python?

### `manejo-archivos.py` - 8 Ejemplos Prácticos
1. ✅ Lectura y escritura de archivos
2. ✅ Trabajar con JSON
3. ✅ Información de archivos (stats)
4. ✅ Operaciones con directorios
5. ✅ Copiar y mover archivos
6. ✅ Procesamiento de CSV
7. ✅ Archivos grandes con generadores
8. ✅ API pathlib (orientada a objetos)

### `ejecutar-script.py` - 6 Métodos de Subprocess
1. ✅ `subprocess.run()` - Recomendado
2. ✅ `subprocess.Popen()` - Streaming
3. ✅ `subprocess.check_output()`
4. ✅ Comandos simples
5. ✅ Ejecución con timeout
6. ✅ Comandos encadenados (pipelines)

### `ejercicios.py` - 5 Ejercicios con Soluciones
1. 📝 CSV a JSON
2. 🧹 Limpiador de archivos temporales
3. 🏗️ Ejecutor de build
4. 👁️ Monitor de cambios en directorios
5. 🔄 Sincronizador de directorios

## 🆚 Comparación Python vs Node.js

### Lectura de archivos

**Node.js:**
```javascript
const fs = require('fs').promises;
const data = await fs.readFile('file.txt', 'utf8');
```

**Python:**
```python
with open('file.txt', 'r', encoding='utf-8') as f:
    data = f.read()
```

### Ejecutar scripts

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

📖 **Ver comparación completa en:** `PYTHON-VS-NODE.md`

## 💡 Ventajas de Python para archivos

✅ **Context managers** (`with`) - Cierre automático de archivos
✅ **Módulos built-in** - CSV, JSON sin dependencias
✅ **Pathlib** - API orientada a objetos para rutas
✅ **Generadores** - Manejo eficiente de archivos grandes
✅ **Sintaxis concisa** - Menos código, más legible

## 📖 Documentos de Referencia

| Documento | Descripción |
|-----------|-------------|
| `GUIA-INICIO-RAPIDO.md` | 🚀 Comienza aquí - Guía rápida |
| `PYTHON-VS-NODE.md` | 🆚 Comparación lado a lado |
| `ejemplos-python/README.md` | 📚 Documentación completa Python |
| `taller-node-shell.md` | 📖 Taller original Node.js |

## 🎯 Orden de Aprendizaje

1. **Lee** → `GUIA-INICIO-RAPIDO.md`
2. **Ejecuta** → `python3 ejemplos-python/manejo-archivos.py`
3. **Compara** → `PYTHON-VS-NODE.md` (si vienes de Node.js)
4. **Practica** → `python3 ejemplos-python/ejercicios.py`
5. **Profundiza** → `ejemplos-python/README.md`

## 🔧 Requisitos

### Para ejemplos Node.js
- Node.js v14+
- npm

### Para ejemplos Python
- Python 3.7+
- (Opcional) `pip install watchdog` para ejercicio de monitoreo

## ✅ Todo lo que puedes hacer

### Con los archivos
- ✅ Leer y escribir archivos de texto
- ✅ Manejar JSON y CSV
- ✅ Copiar, mover, eliminar archivos
- ✅ Crear y navegar directorios
- ✅ Obtener información de archivos
- ✅ Procesar archivos grandes eficientemente

### Con scripts shell
- ✅ Ejecutar scripts .sh y .bat
- ✅ Pasar argumentos y variables de entorno
- ✅ Capturar salida (stdout/stderr)
- ✅ Manejar timeouts
- ✅ Crear pipelines de comandos
- ✅ Controlar procesos del sistema

## 🎓 Recursos Adicionales

### Python
- [Python os module](https://docs.python.org/3/library/os.html)
- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python subprocess](https://docs.python.org/3/library/subprocess.html)

### Node.js
- [Node.js File System](https://nodejs.org/api/fs.html)
- [Node.js Child Process](https://nodejs.org/api/child_process.html)

## 💪 Ejercicios Interactivos

El archivo `ejercicios.py` incluye un menú interactivo:

```bash
cd ejemplos-python
python3 ejercicios.py

# Menú:
# 1. CSV a JSON
# 2. Limpiar archivos temporales
# 3. Ejecutor de build
# 4. Monitor de cambios
# 5. Sincronizador de directorios
# 6. Ejecutar todos
```

## 🎉 ¡Todo listo!

Tienes ahora:
- ✅ Ejemplos en Node.js (originales)
- ✅ Ejemplos equivalentes en Python (nuevos)
- ✅ Comparación lado a lado
- ✅ Ejercicios prácticos con soluciones
- ✅ Documentación completa

**Siguiente paso:**
```bash
cd ejemplos-python
python3 manejo-archivos.py
```

---

¡Disfruta aprendiendo! 🚀🐍
