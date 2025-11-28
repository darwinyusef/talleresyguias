#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejemplo práctico: Ejecutar scripts shell desde Python
Este archivo demuestra diferentes formas de ejecutar scripts
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

# Detectar plataforma
es_windows = platform.system() == 'Windows'
script_ext = '.bat' if es_windows else '.sh'
script_nombre = f'script-ejemplo{script_ext}'
script_ruta = Path(__file__).parent / script_nombre

print('🚀 Ejemplo: Ejecutar Scripts Shell desde Python\n')
print(f'Plataforma: {platform.system()}')
print(f'Script a ejecutar: {script_nombre}\n')


# ============================================
# Método 1: subprocess.run() - Recomendado
# ============================================
def metodo1_run():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Método 1: subprocess.run() - Recomendado')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        comando = [str(script_ruta), 'arg1', 'arg2'] if es_windows else ['bash', str(script_ruta), 'arg1', 'arg2']

        print(f'Ejecutando: {" ".join(comando)}\n')

        # Ejecutar con variables de entorno personalizadas
        env = os.environ.copy()
        env['MI_VARIABLE'] = 'Valor desde Python'
        env['API_KEY'] = 'mi-clave-secreta'

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            env=env
        )

        print('✅ Salida del script:')
        print(resultado.stdout)

        if resultado.stderr:
            print('⚠️  Errores:', resultado.stderr)

        print(f'Código de salida: {resultado.returncode}\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Método 2: subprocess.Popen() - Salida en tiempo real
# ============================================
def metodo2_popen():
    print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Método 2: subprocess.Popen() - Salida en tiempo real')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        comando = [str(script_ruta), 'arg1', 'arg2'] if es_windows else ['bash', str(script_ruta), 'arg1', 'arg2']

        print(f'Ejecutando: {" ".join(comando)}\n')

        # Variables de entorno
        env = os.environ.copy()
        env['MI_VARIABLE'] = 'Valor desde Python con Popen'
        env['API_KEY'] = 'clave-popen'

        proceso = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )

        # Leer salida en tiempo real
        for linea in proceso.stdout:
            print(linea, end='')

        # Esperar a que termine
        proceso.wait()

        print(f'\n✅ Proceso terminado con código: {proceso.returncode}\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Método 3: subprocess.check_output()
# ============================================
def metodo3_check_output():
    print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Método 3: subprocess.check_output()')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        comando = [str(script_ruta), 'arg1', 'arg2'] if es_windows else ['bash', str(script_ruta), 'arg1', 'arg2']

        print(f'Ejecutando: {" ".join(comando)}\n')

        # Variables de entorno
        env = os.environ.copy()
        env['MI_VARIABLE'] = 'Valor desde check_output'
        env['API_KEY'] = 'clave-check-output'

        salida = subprocess.check_output(
            comando,
            text=True,
            env=env
        )

        print('✅ Salida del script:')
        print(salida)

    except subprocess.CalledProcessError as err:
        print(f'❌ Error en comando: {err}')
        print(f'Código de salida: {err.returncode}')
    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Método 4: Ejecutar comandos simples
# ============================================
def metodo4_comandos_simples():
    print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Método 4: Comandos Simples del Sistema')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        # Listar archivos
        comando = ['dir'] if es_windows else ['ls', '-la']
        print(f'Ejecutando: {" ".join(comando)}\n')

        resultado = subprocess.run(comando, capture_output=True, text=True)
        print(resultado.stdout)

        # Versión de Python
        print('\n📌 Versión de Python:')
        resultado = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        print(resultado.stdout)

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Método 5: Ejecutar con timeout
# ============================================
def metodo5_timeout():
    print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Método 5: Ejecución con Timeout')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        comando = ['sleep', '2'] if not es_windows else ['timeout', '/t', '2']
        print(f'Ejecutando comando con timeout de 5 segundos: {" ".join(comando)}\n')

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=5  # 5 segundos
        )

        print('✅ Comando completado dentro del tiempo límite')
        print(f'Código de salida: {resultado.returncode}\n')

    except subprocess.TimeoutExpired:
        print('⏱️  Timeout: El comando excedió el tiempo límite\n')
    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Método 6: Ejecutar comandos encadenados
# ============================================
def metodo6_encadenados():
    print('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Método 6: Comandos Encadenados (Pipeline)')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        if not es_windows:
            # Ejemplo: ls -la | grep .py
            print('Ejecutando: ls -la | grep .py\n')

            # Primer comando
            p1 = subprocess.Popen(['ls', '-la'], stdout=subprocess.PIPE)

            # Segundo comando (pipe)
            p2 = subprocess.Popen(['grep', '.py'], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
            p1.stdout.close()

            salida = p2.communicate()[0]
            print('✅ Archivos .py encontrados:')
            print(salida)
        else:
            print('💡 Los pipelines son más simples en Unix/Linux')
            print('En Windows, usa comandos individuales o PowerShell\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Ejecutar todos los métodos
# ============================================
def ejecutar_todos():
    print('═══════════════════════════════════════════')
    print('   EJECUTANDO EJEMPLOS DE SCRIPTS SHELL   ')
    print('═══════════════════════════════════════════\n')

    try:
        # Verificar que el script existe
        if not script_ruta.exists():
            print(f'❌ El script {script_nombre} no existe en {script_ruta.parent}')
            print('\n💡 Asegúrate de que el script existe en el directorio de ejemplos-python')
            return

        # En Unix, dar permisos de ejecución
        if not es_windows:
            os.chmod(script_ruta, 0o755)
            print('✅ Permisos de ejecución otorgados\n')

        # Ejecutar métodos
        metodo1_run()
        metodo2_popen()
        metodo3_check_output()
        metodo4_comandos_simples()
        metodo5_timeout()
        metodo6_encadenados()

        print('═══════════════════════════════════════════')
        print('   ✅ TODOS LOS EJEMPLOS COMPLETADOS      ')
        print('═══════════════════════════════════════════\n')

    except Exception as err:
        print(f'\n❌ Error general: {err}')


if __name__ == '__main__':
    ejecutar_todos()
