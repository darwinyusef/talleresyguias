#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Múltiple de Audios con ChatGPT y ElevenLabs

Este script lee un JSON con múltiples títulos y descripciones,
genera un guion para cada uno con ChatGPT y crea un audio separado
para cada guion usando ElevenLabs.
"""

import json
import os
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from elevenlabs import ElevenLabs

# Cargar variables de entorno
load_dotenv()


class GeneradorMultipleAudios:
    """Generador de múltiples audios a partir de un JSON"""

    def __init__(self):
        """Inicializar clientes de OpenAI y ElevenLabs"""
        # Verificar que existen las API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

        if not openai_key or openai_key == "tu_api_key_de_openai_aqui":
            raise ValueError("❌ Error: Configura tu OPENAI_API_KEY en el archivo .env")

        if not elevenlabs_key or elevenlabs_key == "tu_api_key_de_elevenlabs_aqui":
            raise ValueError("❌ Error: Configura tu ELEVENLABS_API_KEY en el archivo .env")

        # Inicializar OpenAI
        self.openai_client = OpenAI(api_key=openai_key)

        # Inicializar ElevenLabs
        self.elevenlabs_client = ElevenLabs(
            api_key=elevenlabs_key,
            base_url="https://api.elevenlabs.io"
        )

        # Configuración de ElevenLabs
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "rpqlUOplj0Q0PIilat8h")
        self.model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
        self.output_format = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128")

        # Crear directorio de salida
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

        print("✅ Clientes inicializados correctamente")
        print(f"📁 Directorio de salida: {self.output_dir.absolute()}")

    def generar_guion(self, titulo: str, descripcion: str) -> str:
        """
        Genera un guion usando ChatGPT

        Args:
            titulo: Título del contenido
            descripcion: Descripción o contexto

        Returns:
            Guion generado como texto
        """
        print(f"\n🤖 Generando guion para: '{titulo}'")

        prompt = f"""Eres un guionista profesional. Genera un guion conciso y atractivo para narración en audio.

Título: {titulo}
Descripción: {descripcion}

El guion debe ser:
- Natural y conversacional, como si estuvieras hablando con un amigo
- Directo y claro, fácil de entender
- De 1-3 minutos de duración cuando se lea en voz alta
- En español claro y neutro
- Sin etiquetas de efectos de sonido ni indicaciones técnicas
- Con un inicio enganchador y un cierre memorable

Genera SOLO el texto del guion, listo para ser narrado."""

        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un guionista profesional experto en crear contenido atractivo para audio. Tu especialidad es hacer guiones naturales y conversacionales."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            guion = response.choices[0].message.content.strip()
            palabras = len(guion.split())
            print(f"   ✅ Guion generado: {len(guion)} caracteres, ~{palabras} palabras")
            return guion

        except Exception as e:
            print(f"   ❌ Error generando guion: {e}")
            raise

    def generar_audio(self, texto: str, nombre_archivo: str) -> str:
        """
        Genera audio usando ElevenLabs TTS

        Args:
            texto: Texto del guion a convertir
            nombre_archivo: Nombre del archivo de salida (sin extensión)

        Returns:
            Ruta del archivo de audio generado
        """
        print(f"🎙️  Generando audio: '{nombre_archivo}.mp3'")

        try:
            # Generar audio con ElevenLabs
            audio = self.elevenlabs_client.text_to_speech.convert(
                text=texto,
                voice_id=self.voice_id,
                model_id=self.model_id,
                output_format=self.output_format,
            )

            # Guardar archivo
            file_path = self.output_dir / f"{nombre_archivo}.mp3"

            with open(file_path, "wb") as f:
                for chunk in audio:
                    f.write(chunk)

            # Obtener tamaño del archivo
            size_kb = file_path.stat().st_size / 1024
            print(f"   ✅ Audio generado: {file_path.name} ({size_kb:.1f} KB)")
            return str(file_path)

        except Exception as e:
            print(f"   ❌ Error generando audio: {e}")
            raise

    def procesar_json(self, archivo_json: str) -> List[Dict]:
        """
        Procesa un JSON con múltiples títulos y descripciones

        Args:
            archivo_json: Ruta al archivo JSON

        Returns:
            Lista de diccionarios con resultados
        """
        print("\n" + "="*70)
        print(f"🚀 INICIANDO PROCESAMIENTO")
        print("="*70)
        print(f"📄 Archivo: {archivo_json}")

        # Leer JSON
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"\n❌ Error: No se encontró el archivo '{archivo_json}'")
            return []
        except json.JSONDecodeError as e:
            print(f"\n❌ Error: El archivo JSON no es válido: {e}")
            return []

        # Validar estructura del JSON
        if not isinstance(data, dict):
            print("\n❌ Error: El JSON debe ser un objeto con una clave 'contenidos'")
            return []

        # Soportar diferentes claves: 'contenidos', 'guiones', 'items'
        contenidos = data.get("contenidos") or data.get("guiones") or data.get("items") or []

        if not contenidos:
            print("\n❌ Error: El JSON debe contener una lista en 'contenidos', 'guiones' o 'items'")
            return []

        if not isinstance(contenidos, list):
            print("\n❌ Error: El valor debe ser una lista de objetos")
            return []

        total = len(contenidos)
        print(f"📊 Total de elementos a procesar: {total}")
        print("="*70)

        resultados = []
        exitosos = 0
        fallidos = 0

        # Procesar cada elemento
        for idx, item in enumerate(contenidos, 1):
            print(f"\n{'─'*70}")
            print(f"📌 Procesando {idx}/{total}")
            print(f"{'─'*70}")

            # Obtener título y descripción
            titulo = item.get("titulo", item.get("title", f"Contenido {idx}"))
            descripcion = item.get("descripcion", item.get("description", ""))

            print(f"📝 Título: {titulo}")

            if not descripcion:
                print(f"   ⚠️  Advertencia: No hay descripción, saltando...")
                fallidos += 1
                resultados.append({
                    "titulo": titulo,
                    "error": "Sin descripción"
                })
                continue

            try:
                # 1. Generar guion con ChatGPT
                guion = self.generar_guion(titulo, descripcion)

                # 2. Crear nombre de archivo seguro
                nombre_archivo = self._sanitizar_nombre(titulo, idx)

                # 3. Guardar guion en archivo de texto
                guion_path = self.output_dir / f"{nombre_archivo}_guion.txt"
                with open(guion_path, 'w', encoding='utf-8') as f:
                    f.write(f"TÍTULO: {titulo}\n")
                    f.write(f"{'='*70}\n\n")
                    f.write(f"DESCRIPCIÓN:\n{descripcion}\n\n")
                    f.write(f"{'='*70}\n")
                    f.write(f"GUION GENERADO:\n")
                    f.write(f"{'='*70}\n\n")
                    f.write(guion)

                print(f"💾 Guion guardado: {guion_path.name}")

                # 4. Generar audio con ElevenLabs
                audio_path = self.generar_audio(guion, nombre_archivo)

                # Registrar resultado exitoso
                resultados.append({
                    "numero": idx,
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "guion": guion,
                    "guion_path": str(guion_path),
                    "audio_path": audio_path,
                    "estado": "exitoso"
                })

                exitosos += 1
                print(f"✅ Completado exitosamente")

            except Exception as e:
                print(f"❌ Error procesando '{titulo}': {e}")
                fallidos += 1
                resultados.append({
                    "numero": idx,
                    "titulo": titulo,
                    "error": str(e),
                    "estado": "fallido"
                })

        # Resumen final
        self._mostrar_resumen(total, exitosos, fallidos, resultados)

        return resultados

    def _mostrar_resumen(self, total: int, exitosos: int, fallidos: int, resultados: List[Dict]):
        """Muestra un resumen detallado del procesamiento"""
        print(f"\n{'='*70}")
        print(f"📊 RESUMEN FINAL")
        print(f"{'='*70}")
        print(f"Total procesados:  {total}")
        print(f"✅ Exitosos:       {exitosos} ({exitosos/total*100:.1f}%)")
        print(f"❌ Fallidos:       {fallidos} ({fallidos/total*100:.1f}%)")
        print(f"📁 Ubicación:      {self.output_dir.absolute()}")
        print(f"{'='*70}")

        if exitosos > 0:
            print(f"\n🎉 Archivos generados:")
            for r in resultados:
                if r.get("estado") == "exitoso":
                    print(f"   ✓ {r['numero']}. {r['titulo']}")
                    print(f"      📝 {Path(r['guion_path']).name}")
                    print(f"      🎵 {Path(r['audio_path']).name}")

        if fallidos > 0:
            print(f"\n⚠️  Elementos fallidos:")
            for r in resultados:
                if r.get("estado") == "fallido":
                    print(f"   ✗ {r['numero']}. {r['titulo']}: {r.get('error', 'Error desconocido')}")

        print(f"\n{'='*70}\n")

    def _sanitizar_nombre(self, nombre: str, numero: int) -> str:
        """
        Sanitiza un nombre para usarlo como nombre de archivo

        Args:
            nombre: Nombre a sanitizar
            numero: Número del elemento (para evitar duplicados)

        Returns:
            Nombre sanitizado
        """
        # Convertir a minúsculas y reemplazar espacios
        nombre = nombre.lower().strip()
        nombre = nombre.replace(" ", "_")

        # Eliminar caracteres especiales
        nombre_limpio = ""
        for c in nombre:
            if c.isalnum() or c in "_-":
                nombre_limpio += c

        # Limitar longitud y agregar número
        nombre_limpio = nombre_limpio[:40]

        # Agregar número al inicio para mantener orden
        return f"{numero:02d}_{nombre_limpio}"


def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🎙️  Generador Múltiple de Audios con ChatGPT y ElevenLabs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python generador_multiple_audios.py contenidos.json
  python generador_multiple_audios.py mis_guiones.json

El archivo JSON debe tener esta estructura:
  {
    "contenidos": [
      {
        "titulo": "Título 1",
        "descripcion": "Descripción del contenido 1"
      },
      {
        "titulo": "Título 2",
        "descripcion": "Descripción del contenido 2"
      }
    ]
  }
        """
    )

    parser.add_argument(
        "json_file",
        help="Archivo JSON con títulos y descripciones"
    )

    args = parser.parse_args()

    # Verificar que el archivo existe
    if not os.path.exists(args.json_file):
        print(f"\n❌ Error: El archivo '{args.json_file}' no existe\n")
        return 1

    # Crear generador y procesar
    try:
        generador = GeneradorMultipleAudios()
        resultados = generador.procesar_json(args.json_file)

        # Retornar código de salida apropiado
        fallidos = len([r for r in resultados if r.get("estado") == "fallido"])
        return 0 if fallidos == 0 else 1

    except ValueError as e:
        print(f"\n{e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ Error fatal: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
