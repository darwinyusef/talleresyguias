#!/usr/bin/env node

/**
 * Ejemplo práctico: Manejo de archivos con Node.js
 * Demuestra las operaciones más comunes con archivos
 */

const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');

console.log('📁 Ejemplos de Manejo de Archivos en Node.js\n');

// ============================================
// 1. Leer y Escribir Archivos de Texto
// ============================================
async function ejemploLecturaEscritura() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('1️⃣  Lectura y Escritura de Archivos');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    // Escribir un archivo
    const contenido = `Este es un archivo de ejemplo
Creado en: ${new Date().toLocaleString()}
Con múltiples líneas de texto
¡Saludos desde Node.js!`;

    await fs.writeFile('ejemplo.txt', contenido, 'utf8');
    console.log('✅ Archivo ejemplo.txt creado');

    // Leer el archivo
    const contenidoLeido = await fs.readFile('ejemplo.txt', 'utf8');
    console.log('\n📖 Contenido del archivo:');
    console.log('─────────────────────────────');
    console.log(contenidoLeido);
    console.log('─────────────────────────────\n');

    // Agregar contenido
    await fs.appendFile('ejemplo.txt', '\n\nLínea agregada posteriormente', 'utf8');
    console.log('✅ Contenido agregado al archivo\n');

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

// ============================================
// 2. Trabajar con JSON
// ============================================
async function ejemploJSON() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('2️⃣  Lectura y Escritura de JSON');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    const datos = {
      aplicacion: 'Taller Node.js',
      version: '1.0.0',
      autor: 'Desarrollador',
      fecha: new Date().toISOString(),
      configuracion: {
        debug: true,
        puerto: 3000,
        baseDatos: {
          host: 'localhost',
          nombre: 'midb'
        }
      },
      tags: ['node', 'javascript', 'tutorial']
    };

    // Guardar JSON
    await fs.writeFile('config.json', JSON.stringify(datos, null, 2), 'utf8');
    console.log('✅ Archivo config.json creado');

    // Leer JSON
    const datosLeidos = JSON.parse(await fs.readFile('config.json', 'utf8'));
    console.log('\n📖 Datos del JSON:');
    console.log(datosLeidos);
    console.log();

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

// ============================================
// 3. Información de Archivos
// ============================================
async function ejemploInfoArchivos() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('3️⃣  Información de Archivos');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    const archivo = 'ejemplo.txt';

    // Verificar existencia
    try {
      await fs.access(archivo);
      console.log(`✅ El archivo "${archivo}" existe`);
    } catch {
      console.log(`❌ El archivo "${archivo}" NO existe`);
      return;
    }

    // Obtener información
    const stats = await fs.stat(archivo);

    console.log('\n📊 Estadísticas del archivo:');
    console.log('─────────────────────────────');
    console.log(`Tipo: ${stats.isFile() ? 'Archivo' : 'Directorio'}`);
    console.log(`Tamaño: ${stats.size} bytes (${(stats.size / 1024).toFixed(2)} KB)`);
    console.log(`Creado: ${stats.birthtime.toLocaleString()}`);
    console.log(`Modificado: ${stats.mtime.toLocaleString()}`);
    console.log(`Permisos: ${stats.mode.toString(8).slice(-3)}`);
    console.log('─────────────────────────────\n');

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

// ============================================
// 4. Operaciones con Directorios
// ============================================
async function ejemploDirectorios() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('4️⃣  Operaciones con Directorios');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    // Crear directorio
    const dirPrueba = path.join(__dirname, 'prueba-directorio');
    await fs.mkdir(dirPrueba, { recursive: true });
    console.log(`✅ Directorio creado: ${dirPrueba}`);

    // Crear subdirectorios
    await fs.mkdir(path.join(dirPrueba, 'sub1', 'sub2'), { recursive: true });
    console.log('✅ Subdirectorios creados');

    // Crear archivos en el directorio
    await fs.writeFile(path.join(dirPrueba, 'archivo1.txt'), 'Contenido 1');
    await fs.writeFile(path.join(dirPrueba, 'archivo2.txt'), 'Contenido 2');
    await fs.writeFile(path.join(dirPrueba, 'archivo3.md'), '# Markdown');
    console.log('✅ Archivos creados en el directorio');

    // Listar contenido
    const archivos = await fs.readdir(dirPrueba);
    console.log('\n📁 Contenido del directorio:');
    console.log('─────────────────────────────');
    for (const archivo of archivos) {
      const rutaCompleta = path.join(dirPrueba, archivo);
      const stats = await fs.stat(rutaCompleta);
      const tipo = stats.isDirectory() ? '📂' : '📄';
      console.log(`${tipo} ${archivo}`);
    }
    console.log('─────────────────────────────\n');

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

// ============================================
// 5. Copiar y Mover Archivos
// ============================================
async function ejemploCopiarMover() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('5️⃣  Copiar y Mover Archivos');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    // Copiar archivo
    await fs.copyFile('ejemplo.txt', 'ejemplo-copia.txt');
    console.log('✅ Archivo copiado: ejemplo.txt → ejemplo-copia.txt');

    // Renombrar/Mover archivo
    await fs.rename('ejemplo-copia.txt', 'ejemplo-renombrado.txt');
    console.log('✅ Archivo renombrado: ejemplo-copia.txt → ejemplo-renombrado.txt\n');

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

// ============================================
// 6. Procesamiento de CSV
// ============================================
async function ejemploCSV() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('6️⃣  Procesamiento de CSV');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    // Leer archivo CSV
    const archivoCSV = path.join(__dirname, 'datos.csv');

    try {
      await fs.access(archivoCSV);
    } catch {
      console.log('⚠️  Archivo datos.csv no encontrado');
      return;
    }

    const contenidoCSV = await fs.readFile(archivoCSV, 'utf8');
    const lineas = contenidoCSV.trim().split('\n');

    // Procesar CSV
    const encabezados = lineas[0].split(',');
    const datos = [];

    for (let i = 1; i < lineas.length; i++) {
      const valores = lineas[i].split(',');
      const objeto = {};

      encabezados.forEach((encabezado, index) => {
        objeto[encabezado.trim()] = valores[index].trim();
      });

      datos.push(objeto);
    }

    console.log('📊 Datos del CSV procesados:');
    console.log('─────────────────────────────');
    console.log(JSON.stringify(datos, null, 2));
    console.log('─────────────────────────────');
    console.log(`\n✅ Total de registros: ${datos.length}\n`);

    // Guardar como JSON
    await fs.writeFile('datos-from-csv.json', JSON.stringify(datos, null, 2));
    console.log('✅ Datos guardados como JSON: datos-from-csv.json\n');

  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

// ============================================
// 7. Streams para archivos grandes
// ============================================
async function ejemploStreams() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('7️⃣  Streams para Archivos Grandes');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  return new Promise((resolve, reject) => {
    try {
      // Crear un archivo grande
      const escritor = fsSync.createWriteStream('archivo-grande.txt');

      console.log('📝 Generando archivo grande...');
      for (let i = 0; i < 10000; i++) {
        escritor.write(`Línea ${i + 1}: Este es un archivo grande para demostrar streams\n`);
      }
      escritor.end();

      escritor.on('finish', () => {
        console.log('✅ Archivo grande creado: archivo-grande.txt');

        // Leer con stream
        const lector = fsSync.createReadStream('archivo-grande.txt', 'utf8');
        let lineasLeidas = 0;
        let buffer = '';

        console.log('📖 Leyendo archivo con stream...\n');

        lector.on('data', (chunk) => {
          buffer += chunk;
          const lineas = buffer.split('\n');
          buffer = lineas.pop(); // Guardar última línea incompleta
          lineasLeidas += lineas.length;
        });

        lector.on('end', () => {
          console.log(`✅ Lectura completada: ${lineasLeidas} líneas leídas`);
          console.log('💡 Los streams permiten procesar archivos sin cargar todo en memoria\n');
          resolve();
        });

        lector.on('error', (err) => {
          console.error('❌ Error en lectura:', err.message);
          reject(err);
        });
      });

      escritor.on('error', (err) => {
        console.error('❌ Error en escritura:', err.message);
        reject(err);
      });

    } catch (err) {
      console.error('❌ Error:', err.message);
      reject(err);
    }
  });
}

// ============================================
// Ejecutar todos los ejemplos
// ============================================
async function ejecutarTodos() {
  console.log('═══════════════════════════════════════════');
  console.log('  EJEMPLOS DE MANEJO DE ARCHIVOS NODE.JS  ');
  console.log('═══════════════════════════════════════════\n');

  try {
    await ejemploLecturaEscritura();
    await ejemploJSON();
    await ejemploInfoArchivos();
    await ejemploDirectorios();
    await ejemploCopiarMover();
    await ejemploCSV();
    await ejemploStreams();

    console.log('═══════════════════════════════════════════');
    console.log('   ✅ TODOS LOS EJEMPLOS COMPLETADOS      ');
    console.log('═══════════════════════════════════════════\n');

    console.log('💡 Archivos generados:');
    console.log('   - ejemplo.txt');
    console.log('   - ejemplo-renombrado.txt');
    console.log('   - config.json');
    console.log('   - datos-from-csv.json');
    console.log('   - archivo-grande.txt');
    console.log('   - prueba-directorio/');
    console.log();

  } catch (err) {
    console.error('❌ Error general:', err.message);
  }
}

// Ejecutar si se llama directamente
if (require.main === module) {
  ejecutarTodos();
}

// Exportar funciones
module.exports = {
  ejemploLecturaEscritura,
  ejemploJSON,
  ejemploInfoArchivos,
  ejemploDirectorios,
  ejemploCopiarMover,
  ejemploCSV,
  ejemploStreams,
  ejecutarTodos
};
