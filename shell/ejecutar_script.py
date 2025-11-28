#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Ejecutando script desde Python...")
    print()

    # Obtener el directorio actual
    current_dir = Path(__file__).parent.resolve()

    # Ruta al script
    script_path = current_dir / "script_ejemplo.sh"

    # Verificar que el script existe
    if not script_path.exists():
        print(f"❌ Error: el script no existe en {script_path}", file=sys.stderr)
        sys.exit(1)

    # Parámetros para el script
    nombre = "María"
    edad = "30"

    # Si se pasan argumentos desde la línea de comandos, usarlos
    if len(sys.argv) > 1:
        nombre = sys.argv[1]
    if len(sys.argv) > 2:
        edad = sys.argv[2]

    print(f"📋 Ejecutando: {script_path} {nombre} {edad}")
    print("─────────────────────────────────────")

    try:
        # Ejecutar el script y capturar la salida
        result = subprocess.run(
            [str(script_path), nombre, edad],
            capture_output=True,
            text=True,
            check=False
        )

        # Mostrar stdout
        if result.stdout:
            print(result.stdout, end='')

        # Mostrar stderr si existe
        if result.stderr:
            print(f"⚠️  Stderr:\n{result.stderr}", file=sys.stderr, end='')

        # Verificar el código de retorno
        if result.returncode != 0:
            print(f"\n❌ El script terminó con código de error: {result.returncode}", file=sys.stderr)
            sys.exit(result.returncode)

        print()
        print("✅ Script ejecutado exitosamente desde Python")

    except FileNotFoundError:
        print(f"❌ Error: no se pudo encontrar el script en {script_path}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"❌ Error: no hay permisos para ejecutar {script_path}", file=sys.stderr)
        print("Intenta ejecutar: chmod +x script_ejemplo.sh", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
