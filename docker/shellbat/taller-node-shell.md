# Taller: Manejo de Archivos en Node.js y Ejecución de Scripts Shell

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Módulo FS de Node.js](#módulo-fs-de-nodejs)
3. [Ejecución de Scripts Shell desde Node.js](#ejecución-de-scripts-shell-desde-nodejs)
4. [Diferencias entre .sh y .bat](#diferencias-entre-sh-y-bat)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Ejercicios](#ejercicios)

---

## Introducción

Este taller te enseñará a:
- Leer, escribir y manipular archivos con Node.js
- Ejecutar scripts de shell (.sh, .bat) desde Node.js
- Trabajar con procesos del sistema operativo
- Crear flujos de trabajo automatizados

### Requisitos Previos
- Node.js instalado (v14 o superior)
- Editor de código
- Terminal/Consola

---

## Módulo FS de Node.js

El módulo `fs` (File System) de Node.js proporciona una API para interactuar con el sistema de archivos.

### 1. Importar el módulo

```javascript
// CommonJS
const fs = require('fs');
const fsPromises = require('fs').promises;

// ES Modules
import fs from 'fs';
import { promises as fsPromises } from 'fs';
```

### 2. Leer Archivos

#### a) Lectura Síncrona (Bloquea el proceso)
```javascript
const fs = require('fs');

try {
  const data = fs.readFileSync('archivo.txt', 'utf8');
  console.log(data);
} catch (err) {
  console.error('Error al leer el archivo:', err);
}
```

#### b) Lectura Asíncrona con Callbacks
```javascript
const fs = require('fs');

fs.readFile('archivo.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error al leer el archivo:', err);
    return;
  }
  console.log(data);
});
```

#### c) Lectura Asíncrona con Promesas (Recomendado)
```javascript
const fs = require('fs').promises;

async function leerArchivo() {
  try {
    const data = await fs.readFile('archivo.txt', 'utf8');
    console.log(data);
  } catch (err) {
    console.error('Error al leer el archivo:', err);
  }
}

leerArchivo();
```

#### d) Lectura en Bloques (Streams)
```javascript
const fs = require('fs');

const stream = fs.createReadStream('archivo-grande.txt', 'utf8');

stream.on('data', (chunk) => {
  console.log('Nuevo fragmento:', chunk);
});

stream.on('end', () => {
  console.log('Lectura completada');
});

stream.on('error', (err) => {
  console.error('Error:', err);
});
```

### 3. Escribir Archivos

#### a) Escritura Síncrona
```javascript
const fs = require('fs');

try {
  fs.writeFileSync('nuevo.txt', 'Contenido del archivo', 'utf8');
  console.log('Archivo escrito exitosamente');
} catch (err) {
  console.error('Error al escribir:', err);
}
```

#### b) Escritura Asíncrona con Promesas
```javascript
const fs = require('fs').promises;

async function escribirArchivo() {
  try {
    await fs.writeFile('nuevo.txt', 'Contenido del archivo', 'utf8');
    console.log('Archivo escrito exitosamente');
  } catch (err) {
    console.error('Error al escribir:', err);
  }
}

escribirArchivo();
```

#### c) Añadir contenido (Append)
```javascript
const fs = require('fs').promises;

async function agregarContenido() {
  try {
    await fs.appendFile('log.txt', 'Nueva línea de log\n', 'utf8');
    console.log('Contenido agregado');
  } catch (err) {
    console.error('Error:', err);
  }
}

agregarContenido();
```

### 4. Verificar Existencia de Archivos

```javascript
const fs = require('fs').promises;

async function verificarArchivo(ruta) {
  try {
    await fs.access(ruta);
    console.log('El archivo existe');
    return true;
  } catch {
    console.log('El archivo NO existe');
    return false;
  }
}

verificarArchivo('archivo.txt');
```

### 5. Obtener Información de Archivos

```javascript
const fs = require('fs').promises;

async function obtenerInfo(ruta) {
  try {
    const stats = await fs.stat(ruta);

    console.log('Información del archivo:');
    console.log('- Es archivo:', stats.isFile());
    console.log('- Es directorio:', stats.isDirectory());
    console.log('- Tamaño:', stats.size, 'bytes');
    console.log('- Creado:', stats.birthtime);
    console.log('- Modificado:', stats.mtime);
  } catch (err) {
    console.error('Error:', err);
  }
}

obtenerInfo('archivo.txt');
```

### 6. Trabajar con Directorios

#### a) Crear directorio
```javascript
const fs = require('fs').promises;

async function crearDirectorio(ruta) {
  try {
    await fs.mkdir(ruta, { recursive: true });
    console.log('Directorio creado');
  } catch (err) {
    console.error('Error:', err);
  }
}

crearDirectorio('./carpeta/subcarpeta');
```

#### b) Leer contenido de directorio
```javascript
const fs = require('fs').promises;

async function listarArchivos(ruta) {
  try {
    const archivos = await fs.readdir(ruta);
    console.log('Archivos en', ruta + ':', archivos);
  } catch (err) {
    console.error('Error:', err);
  }
}

listarArchivos('./');
```

#### c) Eliminar directorio
```javascript
const fs = require('fs').promises;

async function eliminarDirectorio(ruta) {
  try {
    await fs.rm(ruta, { recursive: true, force: true });
    console.log('Directorio eliminado');
  } catch (err) {
    console.error('Error:', err);
  }
}

eliminarDirectorio('./carpeta');
```

### 7. Operaciones con Archivos

#### a) Copiar archivos
```javascript
const fs = require('fs').promises;

async function copiarArchivo(origen, destino) {
  try {
    await fs.copyFile(origen, destino);
    console.log('Archivo copiado');
  } catch (err) {
    console.error('Error:', err);
  }
}

copiarArchivo('origen.txt', 'copia.txt');
```

#### b) Mover/Renombrar archivos
```javascript
const fs = require('fs').promises;

async function moverArchivo(origen, destino) {
  try {
    await fs.rename(origen, destino);
    console.log('Archivo movido/renombrado');
  } catch (err) {
    console.error('Error:', err);
  }
}

moverArchivo('viejo.txt', 'nuevo.txt');
```

#### c) Eliminar archivos
```javascript
const fs = require('fs').promises;

async function eliminarArchivo(ruta) {
  try {
    await fs.unlink(ruta);
    console.log('Archivo eliminado');
  } catch (err) {
    console.error('Error:', err);
  }
}

eliminarArchivo('archivo.txt');
```

### 8. Trabajar con JSON

```javascript
const fs = require('fs').promises;

// Leer JSON
async function leerJSON(ruta) {
  try {
    const data = await fs.readFile(ruta, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error('Error:', err);
    return null;
  }
}

// Escribir JSON
async function escribirJSON(ruta, objeto) {
  try {
    const data = JSON.stringify(objeto, null, 2);
    await fs.writeFile(ruta, data, 'utf8');
    console.log('JSON guardado');
  } catch (err) {
    console.error('Error:', err);
  }
}

// Uso
async function ejemplo() {
  const config = { nombre: 'App', version: '1.0.0' };
  await escribirJSON('config.json', config);

  const configLeida = await leerJSON('config.json');
  console.log(configLeida);
}

ejemplo();
```

---

## Ejecución de Scripts Shell desde Node.js

Node.js proporciona varios módulos para ejecutar comandos del sistema operativo y scripts shell.

### 1. Módulo `child_process`

#### a) `exec()` - Para comandos simples

```javascript
const { exec } = require('child_process');

// Ejecutar un comando simple
exec('ls -la', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  if (stderr) {
    console.error('Error estándar:', stderr);
    return;
  }
  console.log('Salida:', stdout);
});
```

#### b) `exec()` con Promesas

```javascript
const util = require('util');
const exec = util.promisify(require('child_process').exec);

async function ejecutarComando(comando) {
  try {
    const { stdout, stderr } = await exec(comando);
    console.log('Salida:', stdout);
    if (stderr) console.error('Errores:', stderr);
    return stdout;
  } catch (err) {
    console.error('Error al ejecutar:', err);
    throw err;
  }
}

// Uso
ejecutarComando('node --version');
```

#### c) `execFile()` - Ejecutar archivos directamente

```javascript
const { execFile } = require('child_process');

// En Unix/Linux/Mac
execFile('./script.sh', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});

// En Windows
execFile('script.bat', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});
```

#### d) `spawn()` - Para procesos que generan mucha salida

```javascript
const { spawn } = require('child_process');

// Ejecutar script con spawn
const proceso = spawn('sh', ['script.sh']);

proceso.stdout.on('data', (data) => {
  console.log(`Salida: ${data}`);
});

proceso.stderr.on('data', (data) => {
  console.error(`Error: ${data}`);
});

proceso.on('close', (code) => {
  console.log(`Proceso terminado con código: ${code}`);
});
```

#### e) `spawn()` con argumentos

```javascript
const { spawn } = require('child_process');

// Ejecutar script con argumentos
const proceso = spawn('sh', ['script.sh', 'argumento1', 'argumento2']);

proceso.stdout.on('data', (data) => {
  console.log(`Salida: ${data}`);
});

proceso.on('close', (code) => {
  console.log(`Código de salida: ${code}`);
});
```

#### f) `execSync()` - Versión síncrona (bloquea el proceso)

```javascript
const { execSync } = require('child_process');

try {
  const salida = execSync('ls -la', { encoding: 'utf8' });
  console.log('Salida:', salida);
} catch (err) {
  console.error('Error:', err);
}
```

### 2. Ejecutar Scripts Shell Multiplataforma

```javascript
const { exec } = require('child_process');
const os = require('os');

function ejecutarScript(scriptUnix, scriptWindows) {
  const plataforma = os.platform();
  const script = plataforma === 'win32' ? scriptWindows : scriptUnix;

  exec(script, (error, stdout, stderr) => {
    if (error) {
      console.error('Error:', error);
      return;
    }
    console.log('Salida:', stdout);
  });
}

// Uso
ejecutarScript('./script.sh', 'script.bat');
```

### 3. Pasar variables de entorno

```javascript
const { exec } = require('child_process');

exec('sh script.sh', {
  env: {
    ...process.env,
    MI_VARIABLE: 'valor',
    API_KEY: 'mi-api-key'
  }
}, (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});
```

### 4. Cambiar directorio de trabajo

```javascript
const { exec } = require('child_process');

exec('ls', {
  cwd: '/ruta/al/directorio'
}, (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});
```

### 5. Límite de tiempo de ejecución (timeout)

```javascript
const { exec } = require('child_process');

exec('sh script-lento.sh', {
  timeout: 5000 // 5 segundos
}, (error, stdout, stderr) => {
  if (error) {
    console.error('Error o timeout:', error);
    return;
  }
  console.log('Salida:', stdout);
});
```

---

## Diferencias entre .sh y .bat

### Scripts Shell (.sh) - Unix/Linux/MacOS

#### Estructura básica de un script .sh

```bash
#!/bin/bash

# Comentario
echo "Hola desde shell script"

# Variables
NOMBRE="Usuario"
echo "Hola $NOMBRE"

# Argumentos
echo "Primer argumento: $1"
echo "Segundo argumento: $2"
echo "Todos los argumentos: $@"

# Condicionales
if [ -f "archivo.txt" ]; then
    echo "El archivo existe"
else
    echo "El archivo NO existe"
fi

# Bucles
for i in 1 2 3 4 5; do
    echo "Número: $i"
done

# Salida exitosa
exit 0
```

#### Crear y ejecutar un script .sh

```bash
# Crear el archivo
touch script.sh

# Dar permisos de ejecución
chmod +x script.sh

# Ejecutar
./script.sh
# o
bash script.sh
# o
sh script.sh
```

#### Desde Node.js:

```javascript
const { exec } = require('child_process');

// Método 1: Con permisos de ejecución
exec('./script.sh arg1 arg2', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});

// Método 2: Sin permisos de ejecución
exec('bash script.sh arg1 arg2', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});
```

### Scripts Batch (.bat) - Windows

#### Estructura básica de un script .bat

```batch
@echo off
REM Comentario

echo Hola desde batch script

REM Variables
set NOMBRE=Usuario
echo Hola %NOMBRE%

REM Argumentos
echo Primer argumento: %1
echo Segundo argumento: %2

REM Condicionales
if exist archivo.txt (
    echo El archivo existe
) else (
    echo El archivo NO existe
)

REM Bucles
for %%i in (1 2 3 4 5) do (
    echo Numero: %%i
)

REM Salida exitosa
exit /b 0
```

#### Desde Node.js:

```javascript
const { exec } = require('child_process');

// En Windows
exec('script.bat arg1 arg2', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});

// O usando cmd
exec('cmd /c script.bat arg1 arg2', (error, stdout, stderr) => {
  if (error) {
    console.error('Error:', error);
    return;
  }
  console.log('Salida:', stdout);
});
```

### Comparación de Comandos Comunes

| Acción | Shell (.sh) | Batch (.bat) |
|--------|-------------|--------------|
| Imprimir | `echo "texto"` | `echo texto` |
| Variable | `VAR="valor"` | `set VAR=valor` |
| Usar variable | `$VAR` | `%VAR%` |
| Comentario | `# comentario` | `REM comentario` |
| Listar archivos | `ls` | `dir` |
| Crear directorio | `mkdir dir` | `mkdir dir` |
| Eliminar archivo | `rm archivo` | `del archivo` |
| Copiar archivo | `cp origen destino` | `copy origen destino` |
| Mover archivo | `mv origen destino` | `move origen destino` |
| Concatenar archivos | `cat archivo` | `type archivo` |
| Directorio actual | `pwd` | `cd` |
| Cambiar directorio | `cd /ruta` | `cd \ruta` |

---

## Ejemplos Prácticos

### Ejemplo 1: Sistema de Backup Automatizado

```javascript
// backup.js
const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

async function crearBackup() {
  const fecha = new Date().toISOString().split('T')[0];
  const dirBackup = `./backups/backup-${fecha}`;

  try {
    // Crear directorio de backup
    await fs.mkdir(dirBackup, { recursive: true });
    console.log(`Directorio de backup creado: ${dirBackup}`);

    // Copiar archivos importantes
    const archivos = await fs.readdir('./datos');

    for (const archivo of archivos) {
      const origen = `./datos/${archivo}`;
      const destino = `${dirBackup}/${archivo}`;
      await fs.copyFile(origen, destino);
      console.log(`Copiado: ${archivo}`);
    }

    // Crear archivo comprimido (Unix/Linux/Mac)
    if (process.platform !== 'win32') {
      await execPromise(`tar -czf ${dirBackup}.tar.gz ${dirBackup}`);
      console.log('Backup comprimido creado');
    }

    console.log('Backup completado exitosamente');
  } catch (err) {
    console.error('Error en backup:', err);
  }
}

crearBackup();
```

### Ejemplo 2: Procesador de Logs

```javascript
// procesarLogs.js
const fs = require('fs').promises;
const readline = require('readline');
const fs_sync = require('fs');

async function procesarLogs(archivoEntrada) {
  const archivoSalida = `processed-${archivoEntrada}`;
  const errores = [];
  const warnings = [];

  const fileStream = fs_sync.createReadStream(archivoEntrada);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  for await (const linea of rl) {
    if (linea.includes('ERROR')) {
      errores.push(linea);
    } else if (linea.includes('WARNING')) {
      warnings.push(linea);
    }
  }

  // Generar reporte
  const reporte = {
    fecha: new Date().toISOString(),
    totalErrores: errores.length,
    totalWarnings: warnings.length,
    errores: errores.slice(0, 10), // Solo los primeros 10
    warnings: warnings.slice(0, 10)
  };

  await fs.writeFile(
    'reporte-logs.json',
    JSON.stringify(reporte, null, 2),
    'utf8'
  );

  console.log('Reporte generado:', reporte);
}

procesarLogs('app.log');
```

### Ejemplo 3: Ejecutor de Scripts con Reintento

```javascript
// ejecutorScripts.js
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

async function ejecutarConReintento(comando, maxIntentos = 3) {
  for (let intento = 1; intento <= maxIntentos; intento++) {
    try {
      console.log(`Intento ${intento}/${maxIntentos}...`);
      const { stdout, stderr } = await execPromise(comando);
      console.log('Éxito:', stdout);
      return { exito: true, salida: stdout };
    } catch (err) {
      console.error(`Error en intento ${intento}:`, err.message);

      if (intento === maxIntentos) {
        return { exito: false, error: err.message };
      }

      // Esperar antes de reintentar (backoff exponencial)
      const espera = Math.pow(2, intento) * 1000;
      console.log(`Esperando ${espera}ms antes de reintentar...`);
      await new Promise(resolve => setTimeout(resolve, espera));
    }
  }
}

// Uso
ejecutarConReintento('sh script-inestable.sh');
```

### Ejemplo 4: Monitor de Sistema

```javascript
// monitor.js
const { exec } = require('child_process');
const util = require('util');
const os = require('os');
const fs = require('fs').promises;

const execPromise = util.promisify(exec);

async function obtenerInfoSistema() {
  const info = {
    timestamp: new Date().toISOString(),
    plataforma: os.platform(),
    arquitectura: os.arch(),
    memoria: {
      total: os.totalmem(),
      libre: os.freemem(),
      usada: os.totalmem() - os.freemem()
    },
    cpu: os.cpus(),
    uptime: os.uptime()
  };

  // Ejecutar comandos específicos según la plataforma
  if (os.platform() === 'darwin' || os.platform() === 'linux') {
    try {
      const { stdout: diskUsage } = await execPromise('df -h');
      info.disco = diskUsage;

      const { stdout: procesos } = await execPromise('ps aux | head -10');
      info.topProcesos = procesos;
    } catch (err) {
      console.error('Error obteniendo info del sistema:', err);
    }
  } else if (os.platform() === 'win32') {
    try {
      const { stdout: memoria } = await execPromise('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value');
      info.memoriaWindows = memoria;
    } catch (err) {
      console.error('Error obteniendo info del sistema:', err);
    }
  }

  return info;
}

async function guardarMonitoreo() {
  const info = await obtenerInfoSistema();
  const nombreArchivo = `monitoreo-${Date.now()}.json`;

  await fs.writeFile(nombreArchivo, JSON.stringify(info, null, 2));
  console.log(`Monitoreo guardado en: ${nombreArchivo}`);
  console.log(`Memoria usada: ${(info.memoria.usada / 1024 / 1024 / 1024).toFixed(2)} GB`);
}

guardarMonitoreo();
```

### Ejemplo 5: Generador de Scripts Dinámicos

```javascript
// generadorScripts.js
const fs = require('fs').promises;
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

async function generarYEjecutarScript(comandos, nombre = 'script-temp') {
  const esWindows = process.platform === 'win32';
  const extension = esWindows ? '.bat' : '.sh';
  const nombreScript = `${nombre}${extension}`;

  let contenido = '';

  if (esWindows) {
    contenido = '@echo off\n';
    contenido += comandos.join('\n');
  } else {
    contenido = '#!/bin/bash\n\n';
    contenido += comandos.join('\n');
  }

  // Escribir el script
  await fs.writeFile(nombreScript, contenido);
  console.log(`Script generado: ${nombreScript}`);

  // Dar permisos de ejecución en Unix
  if (!esWindows) {
    await execPromise(`chmod +x ${nombreScript}`);
  }

  // Ejecutar el script
  const comando = esWindows ? nombreScript : `./${nombreScript}`;
  try {
    const { stdout } = await execPromise(comando);
    console.log('Salida del script:');
    console.log(stdout);
  } catch (err) {
    console.error('Error ejecutando script:', err);
  }

  // Eliminar el script temporal
  await fs.unlink(nombreScript);
  console.log('Script temporal eliminado');
}

// Uso
const comandos = [
  'echo Iniciando proceso...',
  'echo Directorio actual:',
  process.platform === 'win32' ? 'cd' : 'pwd',
  'echo Listando archivos:',
  process.platform === 'win32' ? 'dir' : 'ls -la',
  'echo Proceso completado'
];

generarYEjecutarScript(comandos, 'mi-script');
```

### Ejemplo 6: Pipeline de Datos

```javascript
// pipeline.js
const fs = require('fs');
const { Transform } = require('stream');
const readline = require('readline');

// Transformador que convierte a mayúsculas
class TransformadorMayusculas extends Transform {
  constructor(options) {
    super(options);
  }

  _transform(chunk, encoding, callback) {
    const linea = chunk.toString().toUpperCase();
    this.push(linea);
    callback();
  }
}

// Transformador que filtra líneas
class FiltroLineas extends Transform {
  constructor(filtro, options) {
    super(options);
    this.filtro = filtro;
  }

  _transform(chunk, encoding, callback) {
    const linea = chunk.toString();
    if (linea.includes(this.filtro)) {
      this.push(linea);
    }
    callback();
  }
}

async function procesarArchivo(entrada, salida) {
  const rl = readline.createInterface({
    input: fs.createReadStream(entrada),
    crlfDelay: Infinity
  });

  const escritor = fs.createWriteStream(salida);
  const transformador = new TransformadorMayusculas();

  for await (const linea of rl) {
    transformador.write(linea + '\n');
  }

  transformador.pipe(escritor);

  transformador.end();

  escritor.on('finish', () => {
    console.log('Procesamiento completado');
  });
}

// Uso
procesarArchivo('entrada.txt', 'salida.txt');
```

---

## Ejercicios

### Ejercicio 1: Lector de Archivos CSV
**Objetivo:** Leer un archivo CSV y convertirlo a JSON

```javascript
// Crea un programa que:
// 1. Lea un archivo CSV
// 2. Convierta cada línea en un objeto
// 3. Guarde el resultado en un archivo JSON

// Ejemplo de CSV:
// nombre,edad,ciudad
// Juan,25,Madrid
// María,30,Barcelona

// Resultado esperado en JSON:
// [
//   { "nombre": "Juan", "edad": "25", "ciudad": "Madrid" },
//   { "nombre": "María", "edad": "30", "ciudad": "Barcelona" }
// ]
```

<details>
<summary>Ver solución</summary>

```javascript
const fs = require('fs').promises;

async function csvAJson(archivoCSV, archivoJSON) {
  try {
    // Leer archivo CSV
    const contenido = await fs.readFile(archivoCSV, 'utf8');
    const lineas = contenido.trim().split('\n');

    // Extraer encabezados
    const encabezados = lineas[0].split(',');

    // Procesar filas
    const datos = [];
    for (let i = 1; i < lineas.length; i++) {
      const valores = lineas[i].split(',');
      const objeto = {};

      encabezados.forEach((encabezado, index) => {
        objeto[encabezado.trim()] = valores[index].trim();
      });

      datos.push(objeto);
    }

    // Guardar JSON
    await fs.writeFile(archivoJSON, JSON.stringify(datos, null, 2));
    console.log('Conversión completada');
    return datos;
  } catch (err) {
    console.error('Error:', err);
  }
}

csvAJson('datos.csv', 'datos.json');
```
</details>

### Ejercicio 2: Script de Limpieza
**Objetivo:** Crear un script que elimine archivos temporales

```javascript
// Crea un programa que:
// 1. Busque todos los archivos .tmp en un directorio
// 2. Elimine los archivos que tengan más de 7 días
// 3. Genere un reporte de los archivos eliminados
```

<details>
<summary>Ver solución</summary>

```javascript
const fs = require('fs').promises;
const path = require('path');

async function limpiarTemporales(directorio, dias = 7) {
  const ahora = Date.now();
  const milisegundosPorDia = 24 * 60 * 60 * 1000;
  const umbral = dias * milisegundosPorDia;

  const eliminados = [];

  try {
    const archivos = await fs.readdir(directorio);

    for (const archivo of archivos) {
      if (path.extname(archivo) === '.tmp') {
        const rutaCompleta = path.join(directorio, archivo);
        const stats = await fs.stat(rutaCompleta);
        const antiguedad = ahora - stats.mtimeMs;

        if (antiguedad > umbral) {
          await fs.unlink(rutaCompleta);
          eliminados.push({
            nombre: archivo,
            antiguedad: Math.floor(antiguedad / milisegundosPorDia),
            tamaño: stats.size
          });
        }
      }
    }

    // Generar reporte
    const reporte = {
      fecha: new Date().toISOString(),
      totalEliminados: eliminados.length,
      archivos: eliminados
    };

    await fs.writeFile(
      'reporte-limpieza.json',
      JSON.stringify(reporte, null, 2)
    );

    console.log(`Eliminados ${eliminados.length} archivos`);
    return reporte;
  } catch (err) {
    console.error('Error:', err);
  }
}

limpiarTemporales('./temp', 7);
```
</details>

### Ejercicio 3: Ejecutor de Build
**Objetivo:** Ejecutar un proceso de build con múltiples pasos

```javascript
// Crea un programa que:
// 1. Ejecute npm install
// 2. Ejecute npm test
// 3. Si los tests pasan, ejecute npm run build
// 4. Genere un log de todo el proceso
```

<details>
<summary>Ver solución</summary>

```javascript
const { exec } = require('child_process');
const util = require('util');
const fs = require('fs').promises;

const execPromise = util.promisify(exec);

async function ejecutarBuild() {
  const logs = [];

  function agregarLog(mensaje) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] ${mensaje}`;
    logs.push(logEntry);
    console.log(logEntry);
  }

  try {
    // Paso 1: npm install
    agregarLog('Iniciando npm install...');
    const { stdout: installOut } = await execPromise('npm install');
    agregarLog('npm install completado');
    logs.push(installOut);

    // Paso 2: npm test
    agregarLog('Ejecutando tests...');
    const { stdout: testOut } = await execPromise('npm test');
    agregarLog('Tests pasaron exitosamente');
    logs.push(testOut);

    // Paso 3: npm run build
    agregarLog('Iniciando build...');
    const { stdout: buildOut } = await execPromise('npm run build');
    agregarLog('Build completado exitosamente');
    logs.push(buildOut);

    agregarLog('Proceso completado con éxito');

    // Guardar logs
    await fs.writeFile('build.log', logs.join('\n'));

    return { exito: true };
  } catch (err) {
    agregarLog(`ERROR: ${err.message}`);
    await fs.writeFile('build.log', logs.join('\n'));
    return { exito: false, error: err.message };
  }
}

ejecutarBuild();
```
</details>

### Ejercicio 4: Monitor de Cambios
**Objetivo:** Detectar cambios en archivos de un directorio

```javascript
// Crea un programa que:
// 1. Monitoree un directorio en busca de cambios
// 2. Cuando se detecte un cambio, ejecute un script
// 3. Registre todos los cambios en un log
```

<details>
<summary>Ver solución</summary>

```javascript
const fs = require('fs');
const { exec } = require('child_process');
const util = require('util');

const execPromise = util.promisify(exec);

function monitorearDirectorio(directorio, scriptEjecutar) {
  console.log(`Monitoreando: ${directorio}`);

  const watcher = fs.watch(directorio, { recursive: true }, async (eventType, filename) => {
    if (filename) {
      const timestamp = new Date().toISOString();
      const mensaje = `[${timestamp}] ${eventType}: ${filename}`;

      console.log(mensaje);

      // Registrar en log
      fs.appendFileSync('monitor.log', mensaje + '\n');

      // Ejecutar script
      if (scriptEjecutar) {
        try {
          console.log(`Ejecutando script: ${scriptEjecutar}`);
          const { stdout } = await execPromise(scriptEjecutar);
          console.log('Salida del script:', stdout);
        } catch (err) {
          console.error('Error ejecutando script:', err.message);
        }
      }
    }
  });

  console.log('Presiona Ctrl+C para detener el monitoreo');

  // Manejar cierre graceful
  process.on('SIGINT', () => {
    console.log('\nCerrando monitor...');
    watcher.close();
    process.exit(0);
  });
}

// Uso
monitorearDirectorio('./src', 'echo "Archivo modificado"');
```
</details>

### Ejercicio 5: Sincronizador de Directorios
**Objetivo:** Sincronizar el contenido de dos directorios

```javascript
// Crea un programa que:
// 1. Compare dos directorios
// 2. Copie los archivos nuevos o modificados del origen al destino
// 3. Genere un reporte de los archivos sincronizados
```

<details>
<summary>Ver solución</summary>

```javascript
const fs = require('fs').promises;
const path = require('path');

async function sincronizarDirectorios(origen, destino) {
  const reporte = {
    copiados: [],
    actualizados: [],
    errores: []
  };

  try {
    // Asegurar que el directorio destino existe
    await fs.mkdir(destino, { recursive: true });

    // Leer archivos del origen
    const archivos = await fs.readdir(origen);

    for (const archivo of archivos) {
      const rutaOrigen = path.join(origen, archivo);
      const rutaDestino = path.join(destino, archivo);

      try {
        const statsOrigen = await fs.stat(rutaOrigen);

        // Saltar directorios por ahora
        if (statsOrigen.isDirectory()) continue;

        let debesCopiar = false;

        try {
          const statsDestino = await fs.stat(rutaDestino);
          // Archivo existe, verificar si está modificado
          if (statsOrigen.mtimeMs > statsDestino.mtimeMs) {
            debesCopiar = true;
            reporte.actualizados.push(archivo);
          }
        } catch {
          // Archivo no existe en destino
          debesCopiar = true;
          reporte.copiados.push(archivo);
        }

        if (debesCopiar) {
          await fs.copyFile(rutaOrigen, rutaDestino);
          console.log(`Sincronizado: ${archivo}`);
        }
      } catch (err) {
        reporte.errores.push({ archivo, error: err.message });
      }
    }

    // Guardar reporte
    await fs.writeFile(
      'reporte-sincronizacion.json',
      JSON.stringify(reporte, null, 2)
    );

    console.log(`\nResumen:`);
    console.log(`- Archivos copiados: ${reporte.copiados.length}`);
    console.log(`- Archivos actualizados: ${reporte.actualizados.length}`);
    console.log(`- Errores: ${reporte.errores.length}`);

    return reporte;
  } catch (err) {
    console.error('Error en sincronización:', err);
  }
}

sincronizarDirectorios('./origen', './destino');
```
</details>

---

## Recursos Adicionales

### Documentación Oficial
- [Node.js File System](https://nodejs.org/api/fs.html)
- [Node.js Child Process](https://nodejs.org/api/child_process.html)
- [Node.js Streams](https://nodejs.org/api/stream.html)
- [Node.js Path](https://nodejs.org/api/path.html)

### Mejores Prácticas
1. **Usa versiones asíncronas**: Prefiere `fs.promises` sobre las versiones síncronas
2. **Maneja errores**: Siempre usa try/catch o .catch()
3. **Usa Streams para archivos grandes**: Evita cargar todo en memoria
4. **Valida rutas**: Usa `path.join()` y `path.resolve()` para rutas multiplataforma
5. **Limpia recursos**: Cierra archivos y procesos cuando termines
6. **Escapa argumentos**: Ten cuidado con la inyección de comandos

### Librerías Útiles
- **shelljs**: API multiplataforma para comandos shell
- **cross-spawn**: Ejecutar comandos de forma multiplataforma
- **fs-extra**: Extensión de fs con más funcionalidades
- **chokidar**: Monitor de archivos más robusto que fs.watch
- **globby**: Búsqueda de archivos con patrones glob
- **execa**: Mejor alternativa a child_process

---

## Conclusión

Este taller cubre los aspectos fundamentales del manejo de archivos en Node.js y la ejecución de scripts shell. Practica con los ejercicios y experimenta creando tus propios scripts de automatización.

**Próximos pasos:**
1. Implementa los ejercicios propuestos
2. Crea tus propios scripts de automatización
3. Explora las librerías adicionales mencionadas
4. Practica la creación de scripts multiplataforma
5. Aprende sobre seguridad en la ejecución de comandos shell

¡Feliz codificación!
