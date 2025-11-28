#!/usr/bin/env node

/**
 * Ejemplo práctico: Ejecutar scripts shell desde Node.js
 * Este archivo demuestra diferentes formas de ejecutar scripts
 */

const { exec, spawn, execFile } = require('child_process');
const util = require('util');
const os = require('os');
const path = require('path');

const execPromise = util.promisify(exec);

// Detectar plataforma
const esWindows = os.platform() === 'win32';
const scriptExt = esWindows ? '.bat' : '.sh';
const scriptNombre = `script-ejemplo${scriptExt}`;
const scriptRuta = path.join(__dirname, scriptNombre);

console.log('🚀 Ejemplo: Ejecutar Scripts Shell desde Node.js\n');
console.log(`Plataforma: ${os.platform()}`);
console.log(`Script a ejecutar: ${scriptNombre}\n`);

// ============================================
// Método 1: exec() con Promesas
// ============================================
async function metodo1_exec() {
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📋 Método 1: exec() con Promesas');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  try {
    const comando = esWindows
      ? `"${scriptRuta}" arg1 arg2`
      : `bash "${scriptRuta}" arg1 arg2`;

    console.log(`Ejecutando: ${comando}\n`);

    const { stdout, stderr } = await execPromise(comando, {
      env: {
        ...process.env,
        MI_VARIABLE: 'Valor desde Node.js',
        API_KEY: 'mi-clave-secreta'
      }
    });

    console.log('✅ Salida del script:');
    console.log(stdout);

    if (stderr) {
      console.error('⚠️  Errores:', stderr);
    }
  } catch (err) {
    console.error('❌ Error:', err.message);
  }
}

// ============================================
// Método 2: spawn() - Salida en tiempo real
// ============================================
function metodo2_spawn() {
  return new Promise((resolve, reject) => {
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📋 Método 2: spawn() - Salida en tiempo real');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    const comando = esWindows ? scriptRuta : 'bash';
    const args = esWindows ? ['arg1', 'arg2'] : [scriptRuta, 'arg1', 'arg2'];

    console.log(`Ejecutando: ${comando} ${args.join(' ')}\n`);

    const proceso = spawn(comando, args, {
      env: {
        ...process.env,
        MI_VARIABLE: 'Valor desde Node.js con spawn',
        API_KEY: 'clave-spawn'
      }
    });

    proceso.stdout.on('data', (data) => {
      process.stdout.write(`${data}`);
    });

    proceso.stderr.on('data', (data) => {
      process.stderr.write(`⚠️  ${data}`);
    });

    proceso.on('close', (code) => {
      console.log(`\n✅ Proceso terminado con código: ${code}\n`);
      resolve(code);
    });

    proceso.on('error', (err) => {
      console.error('❌ Error:', err.message);
      reject(err);
    });
  });
}

// ============================================
// Método 3: execFile() - Más seguro
// ============================================
async function metodo3_execFile() {
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📋 Método 3: execFile() - Más seguro');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  return new Promise((resolve, reject) => {
    const comando = esWindows ? scriptRuta : scriptRuta;
    const args = ['arg1', 'arg2'];

    console.log(`Ejecutando: ${comando} ${args.join(' ')}\n`);

    execFile(comando, args, {
      env: {
        ...process.env,
        MI_VARIABLE: 'Valor desde execFile',
        API_KEY: 'clave-execFile'
      }
    }, (error, stdout, stderr) => {
      if (error) {
        console.error('❌ Error:', error.message);
        reject(error);
        return;
      }

      console.log('✅ Salida del script:');
      console.log(stdout);

      if (stderr) {
        console.error('⚠️  Errores:', stderr);
      }

      resolve(stdout);
    });
  });
}

// ============================================
// Ejecutar todos los métodos
// ============================================
async function ejecutarTodos() {
  console.log('═══════════════════════════════════════════');
  console.log('   EJECUTANDO EJEMPLOS DE SCRIPTS SHELL   ');
  console.log('═══════════════════════════════════════════\n');

  try {
    // Verificar que el script existe
    const fs = require('fs');
    if (!fs.existsSync(scriptRuta)) {
      console.error(`❌ El script ${scriptNombre} no existe en ${__dirname}`);
      console.log('\n💡 Asegúrate de que el script existe en el directorio de ejemplos');
      return;
    }

    // En Unix, dar permisos de ejecución
    if (!esWindows) {
      await execPromise(`chmod +x "${scriptRuta}"`);
      console.log('✅ Permisos de ejecución otorgados\n');
    }

    // Ejecutar método 1
    await metodo1_exec();

    // Esperar un poco entre ejecuciones
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Ejecutar método 2
    await metodo2_spawn();

    // Esperar un poco entre ejecuciones
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Ejecutar método 3 (solo si no es Windows, ya que execFile puede tener problemas con .bat)
    if (!esWindows) {
      await metodo3_execFile();
    } else {
      console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('ℹ️  execFile() omitido en Windows (usa exec() o spawn())');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    }

    console.log('═══════════════════════════════════════════');
    console.log('   ✅ TODOS LOS EJEMPLOS COMPLETADOS      ');
    console.log('═══════════════════════════════════════════\n');

  } catch (err) {
    console.error('\n❌ Error general:', err.message);
  }
}

// Ejecutar si se llama directamente
if (require.main === module) {
  ejecutarTodos();
}

// Exportar funciones para uso en otros archivos
module.exports = {
  metodo1_exec,
  metodo2_spawn,
  metodo3_execFile,
  ejecutarTodos
};
