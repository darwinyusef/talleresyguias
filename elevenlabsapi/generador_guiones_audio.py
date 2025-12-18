#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Guiones con ChatGPT y Audio con ElevenLabs

Este script lee un archivo JSON con títulos y descripciones,
genera guiones usando OpenAI ChatGPT y crea archivos de audio
usando ElevenLabs TTS.
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


class GeneradorGuionesAudio:
    """Clase principal para generar guiones y audio"""

    def __init__(self):
        """Inicializar clientes de OpenAI y ElevenLabs"""
        # Inicializar OpenAI
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Inicializar ElevenLabs
        self.elevenlabs_client = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
            base_url="https://api.elevenlabs.io"
        )

        # Configuración de ElevenLabs
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "rpqlUOplj0Q0PIilat8h")
        self.model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
        self.output_format = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128")

        # Crear directorio de salida
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def generar_guion(self, titulo: str, descripcion: str) -> str:
        """
        Genera un guion usando ChatGPT

        Args:
            titulo: Título del guion
            descripcion: Descripción o contexto del guion

        Returns:
            Guion generado como texto
        """
        print(f"🤖 Generando guion para: '{titulo}'...")

        prompt = f"""Eres un guionista profesional. Genera un guion conciso y atractivo basado en:

Título: {titulo}
Descripción: {descripcion}

El guion debe ser:
- Natural y conversacional
- Directo y claro
- De 1-3 minutos de duración cuando se lea en voz alta
- En español
- Sin etiquetas especiales ni indicaciones de efectos de sonido

Genera solo el texto del guion, listo para ser narrado."""

        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {"role": "system", "content": "Eres un guionista profesional experto en crear contenido atractivo y natural."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            guion = response.choices[0].message.content.strip()
            print(f"✅ Guion generado ({len(guion)} caracteres)")
            return guion

        except Exception as e:
            print(f"❌ Error generando guion: {e}")
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
        print(f"🎙️  Generando audio para: '{nombre_archivo}'...")

        try:
            # Generar audio
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

            print(f"✅ Audio generado: {file_path}")
            return str(file_path)

        except Exception as e:
            print(f"❌ Error generando audio: {e}")
            raise

    def procesar_json(self, archivo_json: str, generar_audio_flag: bool = True) -> List[Dict]:
        """
        Procesa un archivo JSON con múltiples guiones

        Args:
            archivo_json: Ruta al archivo JSON
            generar_audio_flag: Si True, genera audio; si False, solo genera guiones

        Returns:
            Lista de diccionarios con resultados
        """
        print(f"\n{'='*60}")
        print(f"📄 Procesando archivo: {archivo_json}")
        print(f"{'='*60}\n")

        # Leer JSON
        with open(archivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validar estructura
        if not isinstance(data, dict) or "guiones" not in data:
            raise ValueError("El JSON debe contener una clave 'guiones' con una lista de objetos")

        guiones = data["guiones"]
        resultados = []

        # Procesar cada guion
        for idx, item in enumerate(guiones, 1):
            print(f"\n--- Procesando guion {idx}/{len(guiones)} ---")

            titulo = item.get("titulo", f"Guion {idx}")
            descripcion = item.get("descripcion", "")

            if not descripcion:
                print(f"⚠️  Advertencia: Guion '{titulo}' no tiene descripción")
                continue

            try:
                # Generar guion
                guion = self.generar_guion(titulo, descripcion)

                # Nombre de archivo seguro
                nombre_archivo = self._sanitizar_nombre(titulo)

                # Guardar guion en texto
                guion_path = self.output_dir / f"{nombre_archivo}_guion.txt"
                with open(guion_path, 'w', encoding='utf-8') as f:
                    f.write(f"Título: {titulo}\n")
                    f.write(f"Descripción: {descripcion}\n")
                    f.write(f"\n{'='*60}\n")
                    f.write(f"GUION:\n")
                    f.write(f"{'='*60}\n\n")
                    f.write(guion)

                print(f"📝 Guion guardado: {guion_path}")

                resultado = {
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "guion": guion,
                    "guion_path": str(guion_path),
                    "audio_path": None
                }

                # Generar audio si está habilitado
                if generar_audio_flag:
                    audio_path = self.generar_audio(guion, nombre_archivo)
                    resultado["audio_path"] = audio_path

                resultados.append(resultado)
                print(f"✅ Completado: {titulo}")

            except Exception as e:
                print(f"❌ Error procesando '{titulo}': {e}")
                resultados.append({
                    "titulo": titulo,
                    "error": str(e)
                })

        # Resumen final
        print(f"\n{'='*60}")
        print(f"📊 RESUMEN")
        print(f"{'='*60}")
        print(f"Total de guiones procesados: {len(guiones)}")
        print(f"Exitosos: {len([r for r in resultados if 'error' not in r])}")
        print(f"Fallidos: {len([r for r in resultados if 'error' in r])}")
        print(f"Archivos guardados en: {self.output_dir.absolute()}")
        print(f"{'='*60}\n")

        return resultados

    def _sanitizar_nombre(self, nombre: str) -> str:
        """
        Sanitiza un nombre para usarlo como nombre de archivo

        Args:
            nombre: Nombre a sanitizar

        Returns:
            Nombre sanitizado
        """
        # Reemplazar caracteres no permitidos
        nombre = nombre.lower()
        nombre = nombre.replace(" ", "_")
        nombre = "".join(c for c in nombre if c.isalnum() or c in "_-")
        # Limitar longitud
        return nombre[:50]


def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generador de Guiones con ChatGPT y Audio con ElevenLabs"
    )
    parser.add_argument(
        "json_file",
        help="Archivo JSON con los guiones (debe contener 'titulo' y 'descripcion')"
    )
    parser.add_argument(
        "--solo-guiones",
        action="store_true",
        help="Solo generar guiones, sin audio"
    )

    args = parser.parse_args()

    # Verificar que el archivo existe
    if not os.path.exists(args.json_file):
        print(f"❌ Error: El archivo '{args.json_file}' no existe")
        return

    # Crear generador y procesar
    try:
        generador = GeneradorGuionesAudio()
        generador.procesar_json(
            args.json_file,
            generar_audio_flag=not args.solo_guiones
        )
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
