#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejemplo práctico: Manejo de archivos con Python
Demuestra las operaciones más comunes con archivos
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

print('📁 Ejemplos de Manejo de Archivos en Python\n')

# ============================================
# 1. Leer y Escribir Archivos de Texto
# ============================================
def ejemplo_lectura_escritura():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('1️⃣  Lectura y Escritura de Archivos')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        # Escribir un archivo
        contenido = f"""Este es un archivo de ejemplo
Creado en: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Con múltiples líneas de texto
¡Saludos desde Python!"""

        with open('ejemplo-py.txt', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print('✅ Archivo ejemplo-py.txt creado')

        # Leer el archivo
        with open('ejemplo-py.txt', 'r', encoding='utf-8') as f:
            contenido_leido = f.read()

        print('\n📖 Contenido del archivo:')
        print('─────────────────────────────')
        print(contenido_leido)
        print('─────────────────────────────\n')

        # Agregar contenido
        with open('ejemplo-py.txt', 'a', encoding='utf-8') as f:
            f.write('\n\nLínea agregada posteriormente')
        print('✅ Contenido agregado al archivo\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# 2. Trabajar con JSON
# ============================================
def ejemplo_json():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('2️⃣  Lectura y Escritura de JSON')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        datos = {
            'aplicacion': 'Taller Python',
            'version': '1.0.0',
            'autor': 'Desarrollador',
            'fecha': datetime.now().isoformat(),
            'configuracion': {
                'debug': True,
                'puerto': 3000,
                'baseDatos': {
                    'host': 'localhost',
                    'nombre': 'midb'
                }
            },
            'tags': ['python', 'tutorial', 'archivos']
        }

        # Guardar JSON
        with open('config-py.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print('✅ Archivo config-py.json creado')

        # Leer JSON
        with open('config-py.json', 'r', encoding='utf-8') as f:
            datos_leidos = json.load(f)

        print('\n📖 Datos del JSON:')
        print(json.dumps(datos_leidos, indent=2, ensure_ascii=False))
        print()

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# 3. Información de Archivos
# ============================================
def ejemplo_info_archivos():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('3️⃣  Información de Archivos')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        archivo = 'ejemplo-py.txt'

        # Verificar existencia
        if os.path.exists(archivo):
            print(f'✅ El archivo "{archivo}" existe')
        else:
            print(f'❌ El archivo "{archivo}" NO existe')
            return

        # Obtener información
        stats = os.stat(archivo)

        print('\n📊 Estadísticas del archivo:')
        print('─────────────────────────────')
        print(f'Tipo: {"Archivo" if os.path.isfile(archivo) else "Directorio"}')
        print(f'Tamaño: {stats.st_size} bytes ({stats.st_size / 1024:.2f} KB)')
        print(f'Creado: {datetime.fromtimestamp(stats.st_birthtime).strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'Modificado: {datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'Permisos: {oct(stats.st_mode)[-3:]}')
        print('─────────────────────────────\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# 4. Operaciones con Directorios
# ============================================
def ejemplo_directorios():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('4️⃣  Operaciones con Directorios')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        # Crear directorio
        dir_prueba = Path('prueba-directorio-py')
        dir_prueba.mkdir(exist_ok=True)
        print(f'✅ Directorio creado: {dir_prueba}')

        # Crear subdirectorios
        (dir_prueba / 'sub1' / 'sub2').mkdir(parents=True, exist_ok=True)
        print('✅ Subdirectorios creados')

        # Crear archivos en el directorio
        (dir_prueba / 'archivo1.txt').write_text('Contenido 1', encoding='utf-8')
        (dir_prueba / 'archivo2.txt').write_text('Contenido 2', encoding='utf-8')
        (dir_prueba / 'archivo3.md').write_text('# Markdown', encoding='utf-8')
        print('✅ Archivos creados en el directorio')

        # Listar contenido
        print('\n📁 Contenido del directorio:')
        print('─────────────────────────────')
        for item in dir_prueba.iterdir():
            tipo = '📂' if item.is_dir() else '📄'
            print(f'{tipo} {item.name}')
        print('─────────────────────────────\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# 5. Copiar y Mover Archivos
# ============================================
def ejemplo_copiar_mover():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('5️⃣  Copiar y Mover Archivos')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        # Copiar archivo
        shutil.copy2('ejemplo-py.txt', 'ejemplo-copia-py.txt')
        print('✅ Archivo copiado: ejemplo-py.txt → ejemplo-copia-py.txt')

        # Renombrar/Mover archivo
        os.rename('ejemplo-copia-py.txt', 'ejemplo-renombrado-py.txt')
        print('✅ Archivo renombrado: ejemplo-copia-py.txt → ejemplo-renombrado-py.txt\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# 6. Procesamiento de CSV
# ============================================
def ejemplo_csv():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('6️⃣  Procesamiento de CSV')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        import csv

        archivo_csv = 'datos.csv'

        if not os.path.exists(archivo_csv):
            print(f'⚠️  Archivo {archivo_csv} no encontrado')
            return

        # Leer CSV
        datos = []
        with open(archivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            datos = list(reader)

        print('📊 Datos del CSV procesados:')
        print('─────────────────────────────')
        print(json.dumps(datos, indent=2, ensure_ascii=False))
        print('─────────────────────────────')
        print(f'\n✅ Total de registros: {len(datos)}\n')

        # Guardar como JSON
        with open('datos-from-csv-py.json', 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print('✅ Datos guardados como JSON: datos-from-csv-py.json\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# 7. Lectura de archivos grandes con generadores
# ============================================
def ejemplo_archivos_grandes():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('7️⃣  Archivos Grandes con Generadores')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        # Crear un archivo grande
        print('📝 Generando archivo grande...')
        with open('archivo-grande-py.txt', 'w', encoding='utf-8') as f:
            for i in range(10000):
                f.write(f'Línea {i + 1}: Este es un archivo grande para demostrar generadores\n')
        print('✅ Archivo grande creado: archivo-grande-py.txt')

        # Leer con generador
        print('📖 Leyendo archivo con generador...\n')

        def leer_por_lineas(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    yield linea.strip()

        lineas_leidas = sum(1 for _ in leer_por_lineas('archivo-grande-py.txt'))

        print(f'✅ Lectura completada: {lineas_leidas} líneas leídas')
        print('💡 Los generadores permiten procesar archivos sin cargar todo en memoria\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# 8. Trabajar con Path (pathlib)
# ============================================
def ejemplo_pathlib():
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    print('8️⃣  Trabajar con Path (pathlib)')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')

    try:
        # Rutas con pathlib
        archivo = Path('ejemplo-py.txt')

        print('📊 Información del Path:')
        print('─────────────────────────────')
        print(f'Nombre: {archivo.name}')
        print(f'Extensión: {archivo.suffix}')
        print(f'Directorio padre: {archivo.parent}')
        print(f'Ruta absoluta: {archivo.absolute()}')
        print(f'Existe: {archivo.exists()}')
        print(f'Es archivo: {archivo.is_file()}')
        print('─────────────────────────────\n')

        # Buscar archivos con patrón
        print('🔍 Archivos .txt en el directorio actual:')
        print('─────────────────────────────')
        for txt_file in Path('.').glob('*.txt'):
            print(f'  📄 {txt_file.name}')
        print('─────────────────────────────\n')

    except Exception as err:
        print(f'❌ Error: {err}')


# ============================================
# Ejecutar todos los ejemplos
# ============================================
def ejecutar_todos():
    print('═══════════════════════════════════════════')
    print('  EJEMPLOS DE MANEJO DE ARCHIVOS PYTHON   ')
    print('═══════════════════════════════════════════\n')

    try:
        ejemplo_lectura_escritura()
        ejemplo_json()
        ejemplo_info_archivos()
        ejemplo_directorios()
        ejemplo_copiar_mover()
        ejemplo_csv()
        ejemplo_archivos_grandes()
        ejemplo_pathlib()

        print('═══════════════════════════════════════════')
        print('   ✅ TODOS LOS EJEMPLOS COMPLETADOS      ')
        print('═══════════════════════════════════════════\n')

        print('💡 Archivos generados:')
        print('   - ejemplo-py.txt')
        print('   - ejemplo-renombrado-py.txt')
        print('   - config-py.json')
        print('   - datos-from-csv-py.json')
        print('   - archivo-grande-py.txt')
        print('   - prueba-directorio-py/')
        print()

    except Exception as err:
        print(f'❌ Error general: {err}')


if __name__ == '__main__':
    ejecutar_todos()
