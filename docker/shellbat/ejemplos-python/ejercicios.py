#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejercicios Prácticos: Manejo de Archivos y Scripts en Python
Soluciones a los 5 ejercicios del taller
"""

import csv
import json
import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timedelta

print('📚 Ejercicios de Manejo de Archivos en Python\n')


# ============================================
# Ejercicio 1: Lector de Archivos CSV
# ============================================
def ejercicio1_csv_a_json(archivo_csv, archivo_json):
    """
    Convierte un archivo CSV a JSON

    Args:
        archivo_csv: Ruta del archivo CSV de entrada
        archivo_json: Ruta del archivo JSON de salida

    Returns:
        Lista de diccionarios con los datos
    """
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Ejercicio 1: Lector de Archivos CSV')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        # Leer archivo CSV
        datos = []
        with open(archivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            datos = list(reader)

        print(f'✅ CSV leído: {len(datos)} registros')

        # Guardar como JSON
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

        print(f'✅ JSON guardado en: {archivo_json}')
        print('\n📊 Datos convertidos:')
        print(json.dumps(datos, indent=2, ensure_ascii=False))
        print()

        return datos

    except Exception as err:
        print(f'❌ Error: {err}')
        return None


# ============================================
# Ejercicio 2: Script de Limpieza
# ============================================
def ejercicio2_limpiar_temporales(directorio, dias=7, extension='.tmp'):
    """
    Elimina archivos temporales con más de X días de antigüedad

    Args:
        directorio: Directorio a limpiar
        dias: Antigüedad mínima en días
        extension: Extensión de archivos a eliminar

    Returns:
        Diccionario con el reporte de limpieza
    """
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Ejercicio 2: Script de Limpieza')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    eliminados = []
    umbral = datetime.now() - timedelta(days=dias)

    try:
        # Buscar archivos temporales
        dir_path = Path(directorio)

        for archivo in dir_path.glob(f'*{extension}'):
            if archivo.is_file():
                stats = archivo.stat()
                fecha_modificacion = datetime.fromtimestamp(stats.st_mtime)

                if fecha_modificacion < umbral:
                    # Eliminar archivo
                    antiguedad_dias = (datetime.now() - fecha_modificacion).days

                    eliminados.append({
                        'nombre': archivo.name,
                        'antiguedad': antiguedad_dias,
                        'tamaño': stats.st_size
                    })

                    archivo.unlink()
                    print(f'🗑️  Eliminado: {archivo.name} ({antiguedad_dias} días)')

        # Generar reporte
        reporte = {
            'fecha': datetime.now().isoformat(),
            'directorio': str(directorio),
            'totalEliminados': len(eliminados),
            'archivos': eliminados
        }

        # Guardar reporte
        with open('reporte-limpieza-py.json', 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)

        print(f'\n✅ Eliminados {len(eliminados)} archivos')
        print(f'✅ Reporte guardado en: reporte-limpieza-py.json\n')

        return reporte

    except Exception as err:
        print(f'❌ Error: {err}')
        return None


# ============================================
# Ejercicio 3: Ejecutor de Build
# ============================================
def ejercicio3_ejecutar_build():
    """
    Ejecuta un proceso de build con múltiples pasos:
    1. Instalar dependencias
    2. Ejecutar tests
    3. Generar build
    """
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Ejercicio 3: Ejecutor de Build')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    logs = []

    def agregar_log(mensaje):
        timestamp = datetime.now().isoformat()
        log_entry = f'[{timestamp}] {mensaje}'
        logs.append(log_entry)
        print(log_entry)

    try:
        # Nota: Este es un ejemplo simulado
        # En un proyecto real, reemplaza con tus comandos reales

        # Paso 1: Instalar dependencias (simulado)
        agregar_log('Iniciando instalación de dependencias...')
        # resultado = subprocess.run(['pip', 'install', '-r', 'requirements.txt'],
        #                          capture_output=True, text=True, check=True)
        agregar_log('✅ Dependencias instaladas (simulado)')

        # Paso 2: Ejecutar tests (simulado)
        agregar_log('Ejecutando tests...')
        # resultado = subprocess.run(['pytest'],
        #                          capture_output=True, text=True, check=True)
        agregar_log('✅ Tests pasaron exitosamente (simulado)')

        # Paso 3: Build (simulado)
        agregar_log('Iniciando build...')
        # resultado = subprocess.run(['python', 'setup.py', 'build'],
        #                          capture_output=True, text=True, check=True)
        agregar_log('✅ Build completado exitosamente (simulado)')

        agregar_log('Proceso completado con éxito')

        # Guardar logs
        with open('build-py.log', 'w', encoding='utf-8') as f:
            f.write('\n'.join(logs))

        print(f'\n✅ Logs guardados en: build-py.log\n')

        return {'exito': True}

    except subprocess.CalledProcessError as err:
        agregar_log(f'ERROR: {err}')

        # Guardar logs incluso en caso de error
        with open('build-py.log', 'w', encoding='utf-8') as f:
            f.write('\n'.join(logs))

        return {'exito': False, 'error': str(err)}
    except Exception as err:
        agregar_log(f'ERROR: {err}')
        return {'exito': False, 'error': str(err)}


# ============================================
# Ejercicio 4: Monitor de Cambios
# ============================================
def ejercicio4_monitorear_directorio(directorio, script_ejecutar=None):
    """
    Monitorea un directorio en busca de cambios

    Args:
        directorio: Directorio a monitorear
        script_ejecutar: Script a ejecutar cuando se detecte un cambio

    Nota: Este ejemplo usa watchdog, instala con: pip install watchdog
    """
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Ejercicio 4: Monitor de Cambios')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class ManejadorCambios(FileSystemEventHandler):
            def on_any_event(self, event):
                if event.is_directory:
                    return

                timestamp = datetime.now().isoformat()
                mensaje = f'[{timestamp}] {event.event_type}: {event.src_path}'

                print(mensaje)

                # Registrar en log
                with open('monitor-py.log', 'a', encoding='utf-8') as f:
                    f.write(mensaje + '\n')

                # Ejecutar script si está definido
                if script_ejecutar:
                    try:
                        print(f'Ejecutando script: {script_ejecutar}')
                        resultado = subprocess.run(
                            script_ejecutar.split(),
                            capture_output=True,
                            text=True
                        )
                        print(f'Salida del script: {resultado.stdout}')
                    except Exception as err:
                        print(f'Error ejecutando script: {err}')

        # Configurar observer
        event_handler = ManejadorCambios()
        observer = Observer()
        observer.schedule(event_handler, directorio, recursive=True)
        observer.start()

        print(f'👁️  Monitoreando: {directorio}')
        print('Presiona Ctrl+C para detener el monitoreo\n')

        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print('\n\n✅ Monitor detenido')

        observer.join()

    except ImportError:
        print('⚠️  La librería watchdog no está instalada')
        print('Instálala con: pip install watchdog\n')
        print('💡 Implementación alternativa usando polling:\n')

        # Alternativa sin watchdog (polling)
        archivos_anteriores = {}

        while True:
            try:
                archivos_actuales = {}

                for archivo in Path(directorio).rglob('*'):
                    if archivo.is_file():
                        archivos_actuales[str(archivo)] = archivo.stat().st_mtime

                # Detectar cambios
                for archivo, mtime in archivos_actuales.items():
                    if archivo not in archivos_anteriores:
                        print(f'📄 Nuevo archivo: {archivo}')
                    elif archivos_anteriores[archivo] != mtime:
                        print(f'📝 Modificado: {archivo}')

                # Detectar eliminaciones
                for archivo in archivos_anteriores:
                    if archivo not in archivos_actuales:
                        print(f'🗑️  Eliminado: {archivo}')

                archivos_anteriores = archivos_actuales

                import time
                time.sleep(2)  # Revisar cada 2 segundos

            except KeyboardInterrupt:
                print('\n\n✅ Monitor detenido')
                break

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Ejercicio 5: Sincronizador de Directorios
# ============================================
def ejercicio5_sincronizar_directorios(origen, destino):
    """
    Sincroniza el contenido de dos directorios

    Args:
        origen: Directorio origen
        destino: Directorio destino

    Returns:
        Diccionario con el reporte de sincronización
    """
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('📋 Ejercicio 5: Sincronizador de Directorios')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    reporte = {
        'copiados': [],
        'actualizados': [],
        'errores': []
    }

    try:
        # Crear directorio destino si no existe
        Path(destino).mkdir(parents=True, exist_ok=True)

        # Recorrer archivos del origen
        origen_path = Path(origen)

        for archivo_origen in origen_path.rglob('*'):
            if archivo_origen.is_file():
                # Calcular ruta relativa y destino
                ruta_relativa = archivo_origen.relative_to(origen_path)
                archivo_destino = Path(destino) / ruta_relativa

                try:
                    # Crear directorio padre si no existe
                    archivo_destino.parent.mkdir(parents=True, exist_ok=True)

                    # Verificar si necesita copiarse
                    debe_copiar = False

                    if not archivo_destino.exists():
                        debe_copiar = True
                        reporte['copiados'].append(str(ruta_relativa))
                    else:
                        # Comparar fechas de modificación
                        mtime_origen = archivo_origen.stat().st_mtime
                        mtime_destino = archivo_destino.stat().st_mtime

                        if mtime_origen > mtime_destino:
                            debe_copiar = True
                            reporte['actualizados'].append(str(ruta_relativa))

                    # Copiar si es necesario
                    if debe_copiar:
                        shutil.copy2(archivo_origen, archivo_destino)
                        print(f'✅ Sincronizado: {ruta_relativa}')

                except Exception as err:
                    reporte['errores'].append({
                        'archivo': str(ruta_relativa),
                        'error': str(err)
                    })
                    print(f'❌ Error con {ruta_relativa}: {err}')

        # Guardar reporte
        with open('reporte-sincronizacion-py.json', 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)

        print(f'\n📊 Resumen:')
        print(f'- Archivos copiados: {len(reporte["copiados"])}')
        print(f'- Archivos actualizados: {len(reporte["actualizados"])}')
        print(f'- Errores: {len(reporte["errores"])}')
        print(f'\n✅ Reporte guardado en: reporte-sincronizacion-py.json\n')

        return reporte

    except Exception as err:
        print(f'❌ Error en sincronización: {err}')
        return None


# ============================================
# Menú de ejercicios
# ============================================
def menu_ejercicios():
    print('═══════════════════════════════════════════')
    print('      EJERCICIOS DE PYTHON - ARCHIVOS     ')
    print('═══════════════════════════════════════════\n')

    print('Selecciona un ejercicio para ejecutar:\n')
    print('1. CSV a JSON')
    print('2. Limpiar archivos temporales')
    print('3. Ejecutor de build')
    print('4. Monitor de cambios')
    print('5. Sincronizador de directorios')
    print('6. Ejecutar todos los ejercicios')
    print('0. Salir\n')

    opcion = input('Opción: ')

    if opcion == '1':
        # Verificar que exista el CSV
        csv_file = '../datos.csv'
        if Path(csv_file).exists():
            ejercicio1_csv_a_json(csv_file, 'datos-ejercicio1.json')
        else:
            print(f'⚠️  Archivo {csv_file} no encontrado')

    elif opcion == '2':
        # Crear archivos temporales de prueba
        test_dir = Path('test-temp')
        test_dir.mkdir(exist_ok=True)

        # Crear archivos con diferentes antigüedades
        for i in range(5):
            archivo = test_dir / f'archivo{i}.tmp'
            archivo.write_text(f'Contenido {i}')

            # Modificar fecha (simular antigüedad)
            if i < 2:  # Hacer que algunos sean antiguos
                import time
                mtime = time.time() - (10 * 24 * 60 * 60)  # 10 días atrás
                os.utime(archivo, (mtime, mtime))

        print('✅ Archivos temporales de prueba creados\n')
        ejercicio2_limpiar_temporales('test-temp', dias=7)

    elif opcion == '3':
        ejercicio3_ejecutar_build()

    elif opcion == '4':
        directorio = input('Directorio a monitorear (. para actual): ') or '.'
        script = input('Script a ejecutar (opcional, Enter para omitir): ') or None
        ejercicio4_monitorear_directorio(directorio, script)

    elif opcion == '5':
        origen = input('Directorio origen: ')
        destino = input('Directorio destino: ')
        if origen and destino:
            ejercicio5_sincronizar_directorios(origen, destino)
        else:
            print('⚠️  Debes proporcionar origen y destino')

    elif opcion == '6':
        print('📚 Ejecutando todos los ejercicios...\n')

        # Ejercicio 1
        csv_file = '../datos.csv'
        if Path(csv_file).exists():
            ejercicio1_csv_a_json(csv_file, 'datos-ejercicio1.json')

        # Ejercicio 2
        test_dir = Path('test-temp')
        test_dir.mkdir(exist_ok=True)
        (test_dir / 'old.tmp').write_text('old file')
        ejercicio2_limpiar_temporales('test-temp', dias=0)

        # Ejercicio 3
        ejercicio3_ejecutar_build()

        # Ejercicio 4 y 5 requieren input, se omiten en "todos"

        print('\n✅ Ejercicios 1-3 completados')

    elif opcion == '0':
        print('👋 ¡Hasta luego!')
    else:
        print('⚠️  Opción no válida')


if __name__ == '__main__':
    menu_ejercicios()
