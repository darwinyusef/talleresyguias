# Python vs Node.js - Guía de Referencia Rápida

Comparación lado a lado de las operaciones de archivos y scripts en Python y Node.js

## 📖 Índice

- [Lectura de Archivos](#lectura-de-archivos)
- [Escritura de Archivos](#escritura-de-archivos)
- [JSON](#trabajar-con-json)
- [CSV](#procesamiento-de-csv)
- [Directorios](#trabajar-con-directorios)
- [Ejecutar Scripts](#ejecutar-scripts-shell)
- [Información de Archivos](#información-de-archivos)

---

## Lectura de Archivos

### Node.js
```javascript
// Con Promesas (async/await)
const fs = require('fs').promises;

async function leer() {
  const contenido = await fs.readFile('archivo.txt', 'utf8');
  console.log(contenido);
}

// Síncrono (bloquea el proceso)
const contenido = fs.readFileSync('archivo.txt', 'utf8');
```

### Python
```python
# Forma estándar con context manager
with open('archivo.txt', 'r', encoding='utf-8') as f:
    contenido = f.read()
    print(contenido)

# Usando Path (más moderno)
from pathlib import Path
contenido = Path('archivo.txt').read_text(encoding='utf-8')
```

**Ventaja Python:** El context manager (`with`) cierra automáticamente el archivo, incluso si hay errores.

---

## Escritura de Archivos

### Node.js
```javascript
const fs = require('fs').promises;

// Escribir (sobrescribe)
await fs.writeFile('archivo.txt', 'contenido', 'utf8');

// Agregar (append)
await fs.appendFile('archivo.txt', '\nmás contenido', 'utf8');
```

### Python
```python
# Escribir (sobrescribe)
with open('archivo.txt', 'w', encoding='utf-8') as f:
    f.write('contenido')

# Agregar (append)
with open('archivo.txt', 'a', encoding='utf-8') as f:
    f.write('\nmás contenido')

# Con Path
Path('archivo.txt').write_text('contenido', encoding='utf-8')
```

**Similar:** Ambos son simples y directos.

---

## Trabajar con JSON

### Node.js
```javascript
const fs = require('fs').promises;

// Leer JSON
const data = JSON.parse(await fs.readFile('config.json', 'utf8'));

// Escribir JSON
await fs.writeFile('config.json', JSON.stringify(data, null, 2), 'utf8');
```

### Python
```python
import json

# Leer JSON
with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Escribir JSON
with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**Ventaja Python:** `json.load()` y `json.dump()` trabajan directamente con archivos, no necesitas leer/escribir como strings primero.

---

## Procesamiento de CSV

### Node.js
```javascript
const fs = require('fs').promises;

// Leer CSV (manual)
const contenido = await fs.readFile('datos.csv', 'utf8');
const lineas = contenido.trim().split('\n');
const headers = lineas[0].split(',');

const datos = lineas.slice(1).map(linea => {
  const valores = linea.split(',');
  return headers.reduce((obj, header, i) => {
    obj[header] = valores[i];
    return obj;
  }, {});
});

// O usar librería: npm install csv-parser
const csv = require('csv-parser');
```

### Python
```python
import csv

# Leer CSV (built-in)
with open('datos.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    datos = list(reader)

# Escribir CSV
with open('salida.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['nombre', 'edad'])
    writer.writeheader()
    writer.writerows(datos)
```

**Ventaja Python:** Módulo CSV incluido en la librería estándar, muy simple de usar.

---

## Trabajar con Directorios

### Node.js
```javascript
const fs = require('fs').promises;

// Crear directorio
await fs.mkdir('carpeta', { recursive: true });

// Listar archivos
const archivos = await fs.readdir('./');

// Eliminar directorio
await fs.rm('carpeta', { recursive: true, force: true });

// Copiar archivo
await fs.copyFile('origen.txt', 'destino.txt');

// Renombrar/Mover
await fs.rename('viejo.txt', 'nuevo.txt');
```

### Python
```python
import os
import shutil
from pathlib import Path

# Crear directorio
Path('carpeta').mkdir(parents=True, exist_ok=True)
# o: os.makedirs('carpeta', exist_ok=True)

# Listar archivos
archivos = os.listdir('./')
# o: archivos = [f.name for f in Path('.').iterdir()]

# Eliminar directorio
shutil.rmtree('carpeta')

# Copiar archivo
shutil.copy2('origen.txt', 'destino.txt')

# Renombrar/Mover
os.rename('viejo.txt', 'nuevo.txt')
# o: Path('viejo.txt').rename('nuevo.txt')
```

**Ventaja Python:** `pathlib` proporciona una API orientada a objetos muy elegante.

---

## Ejecutar Scripts Shell

### Node.js
```javascript
const { exec, spawn } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Método 1: exec (simple)
const { stdout, stderr } = await execPromise('ls -la');
console.log(stdout);

// Método 2: spawn (streaming)
const proceso = spawn('bash', ['script.sh', 'arg1', 'arg2']);

proceso.stdout.on('data', (data) => {
  console.log(`${data}`);
});

proceso.on('close', (code) => {
  console.log(`Código: ${code}`);
});

// Con variables de entorno
exec('script.sh', {
  env: { ...process.env, MI_VAR: 'valor' }
}, callback);
```

### Python
```python
import subprocess

# Método 1: run (recomendado)
resultado = subprocess.run(
    ['ls', '-la'],
    capture_output=True,
    text=True
)
print(resultado.stdout)

# Método 2: Popen (streaming)
proceso = subprocess.Popen(
    ['bash', 'script.sh', 'arg1', 'arg2'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

for linea in proceso.stdout:
    print(linea, end='')

proceso.wait()

# Con variables de entorno
import os
env = os.environ.copy()
env['MI_VAR'] = 'valor'
subprocess.run(['script.sh'], env=env)
```

**Ventaja Python:** `subprocess.run()` es más directo y limpio. No necesitas promisificar.

---

## Información de Archivos

### Node.js
```javascript
const fs = require('fs').promises;

const stats = await fs.stat('archivo.txt');

console.log({
  tamaño: stats.size,
  esArchivo: stats.isFile(),
  esDirectorio: stats.isDirectory(),
  modificado: stats.mtime,
  creado: stats.birthtime
});

// Verificar existencia
try {
  await fs.access('archivo.txt');
  console.log('Existe');
} catch {
  console.log('No existe');
}
```

### Python
```python
import os
from pathlib import Path
from datetime import datetime

stats = os.stat('archivo.txt')

print({
    'tamaño': stats.st_size,
    'esArchivo': os.path.isfile('archivo.txt'),
    'esDirectorio': os.path.isdir('archivo.txt'),
    'modificado': datetime.fromtimestamp(stats.st_mtime),
    'creado': datetime.fromtimestamp(stats.st_birthtime)
})

# Verificar existencia
if os.path.exists('archivo.txt'):
    print('Existe')

# Con Path (más limpio)
archivo = Path('archivo.txt')
if archivo.exists():
    print('Existe')
```

**Similar:** Ambos proporcionan la misma información.

---

## Streams / Generadores para Archivos Grandes

### Node.js
```javascript
const fs = require('fs');
const readline = require('readline');

// Leer línea por línea
const rl = readline.createInterface({
  input: fs.createReadStream('grande.txt'),
  crlfDelay: Infinity
});

for await (const linea of rl) {
  console.log(linea);
}

// Stream personalizado
const stream = fs.createReadStream('grande.txt', 'utf8');
stream.on('data', chunk => console.log(chunk));
stream.on('end', () => console.log('Fin'));
```

### Python
```python
# Leer línea por línea (simple)
with open('grande.txt', 'r') as f:
    for linea in f:
        print(linea.strip())

# Con generador
def leer_lineas(archivo):
    with open(archivo) as f:
        for linea in f:
            yield linea.strip()

for linea in leer_lineas('grande.txt'):
    print(linea)
```

**Ventaja Python:** La iteración sobre archivos es built-in. No necesitas módulos extra.

---

## Resumen de Ventajas

### Python
✅ Context managers (`with`) para manejo automático de recursos
✅ Módulos CSV y JSON en la librería estándar
✅ Pathlib para API orientada a objetos
✅ Generadores built-in para archivos grandes
✅ subprocess.run() más directo
✅ Sintaxis más concisa en general

### Node.js
✅ Async/await nativo desde el inicio
✅ Excelente ecosistema npm
✅ Mejor para aplicaciones web/servidores
✅ Callbacks para control fino de eventos
✅ Streams muy potentes

---

## Tabla de Equivalencias

| Operación | Node.js | Python |
|-----------|---------|--------|
| Leer archivo | `fs.readFile()` | `open().read()` |
| Escribir archivo | `fs.writeFile()` | `open().write()` |
| Agregar a archivo | `fs.appendFile()` | `open('a').write()` |
| Copiar archivo | `fs.copyFile()` | `shutil.copy2()` |
| Mover/Renombrar | `fs.rename()` | `os.rename()` |
| Eliminar archivo | `fs.unlink()` | `os.unlink()` |
| Crear directorio | `fs.mkdir()` | `os.makedirs()` |
| Listar directorio | `fs.readdir()` | `os.listdir()` |
| Eliminar directorio | `fs.rm()` | `shutil.rmtree()` |
| Info de archivo | `fs.stat()` | `os.stat()` |
| Existe archivo | `fs.access()` | `os.path.exists()` |
| Ejecutar comando | `child_process.exec()` | `subprocess.run()` |
| Stream/Pipeline | `spawn()` + pipes | `Popen()` + pipes |
| Leer JSON | `JSON.parse(readFile())` | `json.load()` |
| Escribir JSON | `writeFile(stringify())` | `json.dump()` |
| Leer CSV | Librería externa | `csv.DictReader()` |

---

## Ejemplo Completo: Sincronizador de Archivos

### Node.js
```javascript
const fs = require('fs').promises;
const path = require('path');

async function sincronizar(origen, destino) {
  await fs.mkdir(destino, { recursive: true });
  const archivos = await fs.readdir(origen);

  for (const archivo of archivos) {
    const rutaOrigen = path.join(origen, archivo);
    const rutaDestino = path.join(destino, archivo);

    const statsOrigen = await fs.stat(rutaOrigen);
    if (statsOrigen.isFile()) {
      try {
        const statsDestino = await fs.stat(rutaDestino);
        if (statsOrigen.mtimeMs > statsDestino.mtimeMs) {
          await fs.copyFile(rutaOrigen, rutaDestino);
        }
      } catch {
        await fs.copyFile(rutaOrigen, rutaDestino);
      }
    }
  }
}
```

### Python
```python
import shutil
from pathlib import Path

def sincronizar(origen, destino):
    Path(destino).mkdir(parents=True, exist_ok=True)

    for archivo_origen in Path(origen).iterdir():
        if archivo_origen.is_file():
            archivo_destino = Path(destino) / archivo_origen.name

            if not archivo_destino.exists() or \
               archivo_origen.stat().st_mtime > archivo_destino.stat().st_mtime:
                shutil.copy2(archivo_origen, archivo_destino)
```

**Observación:** El código Python es más conciso gracias a `pathlib`.

---

## Conclusión

Ambos lenguajes son excelentes para manejo de archivos y scripts:

**Elige Node.js si:**
- Ya estás trabajando en un proyecto JavaScript/TypeScript
- Necesitas integración web/servidor
- Prefieres el ecosistema npm

**Elige Python si:**
- Necesitas manipulación de datos (CSV, JSON, etc.)
- Quieres código más conciso y legible
- Prefieres módulos built-in sobre dependencias

**Lo mejor:** ¡Aprende ambos! Esta guía te ayuda a traducir entre los dos. 🚀
