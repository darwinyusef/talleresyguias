# Generador de Guiones y Audio con ChatGPT + ElevenLabs

Script en Python que automatiza la generación de guiones usando ChatGPT y su conversión a audio mediante ElevenLabs TTS.

## Características

- Genera guiones profesionales a partir de títulos y descripciones usando OpenAI ChatGPT
- Convierte los guiones a audio de alta calidad con ElevenLabs
- Procesa múltiples guiones en batch desde un archivo JSON
- Guarda tanto los guiones en texto como los archivos de audio
- Configuración flexible mediante variables de entorno

## Requisitos Previos

- Python 3.8 o superior
- Cuenta de OpenAI con API Key ([obtener aquí](https://platform.openai.com/api-keys))
- Cuenta de ElevenLabs con API Key ([obtener aquí](https://elevenlabs.io))

## Instalación

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**

Copia el archivo `.env.example` a `.env`:
```bash
cp .env.example .env
```

Edita `.env` y añade tus API keys:
```env
OPENAI_API_KEY=tu_api_key_de_openai_aqui
ELEVENLABS_API_KEY=tu_api_key_de_elevenlabs_aqui
```

### Configuración Opcional

Puedes personalizar la configuración en el archivo `.env`:

- `OPENAI_MODEL`: Modelo de OpenAI a usar (default: `gpt-4`)
- `ELEVENLABS_VOICE_ID`: ID de la voz ([explorar voces](https://elevenlabs.io/voice-library))
- `ELEVENLABS_MODEL_ID`: Modelo de ElevenLabs (default: `eleven_multilingual_v2`)
- `ELEVENLABS_OUTPUT_FORMAT`: Formato de audio (default: `mp3_44100_128`)

## Uso

### 1. Preparar el archivo JSON

Crea un archivo JSON con la estructura siguiente:

```json
{
  "guiones": [
    {
      "titulo": "Título del Guion 1",
      "descripcion": "Descripción detallada de qué debe contener el guion"
    },
    {
      "titulo": "Título del Guion 2",
      "descripcion": "Otra descripción para generar otro guion"
    }
  ]
}
```

Puedes usar `guiones_ejemplo.json` como plantilla.

### 2. Ejecutar el script

**Generar guiones y audio:**
```bash
python generador_guiones_audio.py guiones_ejemplo.json
```

**Solo generar guiones (sin audio):**
```bash
python generador_guiones_audio.py guiones_ejemplo.json --solo-guiones
```

### 3. Resultados

Los archivos generados se guardarán en la carpeta `output/`:

```
output/
├── introduccion_a_la_inteligencia_artificial_guion.txt
├── introduccion_a_la_inteligencia_artificial.mp3
├── consejos_para_programadores_principiantes_guion.txt
├── consejos_para_programadores_principiantes.mp3
└── ...
```

## Estructura del Proyecto

```
elevenlabsapi/
├── generador_guiones_audio.py    # Script principal
├── guiones_ejemplo.json           # Ejemplo de archivo JSON
├── requirements.txt               # Dependencias
├── .env.example                   # Ejemplo de configuración
├── .env                          # Tu configuración (no incluir en git)
├── README.md                     # Esta documentación
└── output/                       # Carpeta de salida (se crea automáticamente)
```

## Ejemplo Completo

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar .env con tus API keys
cp .env.example .env
nano .env  # o usa tu editor favorito

# 3. Ejecutar con el ejemplo
python generador_guiones_audio.py guiones_ejemplo.json

# Salida esperada:
# ============================================================
# 📄 Procesando archivo: guiones_ejemplo.json
# ============================================================
#
# --- Procesando guion 1/4 ---
# 🤖 Generando guion para: 'Introducción a la Inteligencia Artificial'...
# ✅ Guion generado (850 caracteres)
# 📝 Guion guardado: output/introduccion_a_la_inteligencia_artificial_guion.txt
# 🎙️  Generando audio para: 'introduccion_a_la_inteligencia_artificial'...
# ✅ Audio generado: output/introduccion_a_la_inteligencia_artificial.mp3
# ✅ Completado: Introducción a la Inteligencia Artificial
# ...
```

## Personalización

### Cambiar la voz

1. Visita [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
2. Selecciona una voz y copia su ID
3. Actualiza `ELEVENLABS_VOICE_ID` en tu archivo `.env`

### Usar diferentes modelos de OpenAI

Modifica `OPENAI_MODEL` en `.env`:
- `gpt-4` - Mayor calidad, más costoso
- `gpt-3.5-turbo` - Rápido y económico
- `gpt-4-turbo-preview` - Balance entre calidad y velocidad

### Modificar el prompt de generación

Edita la función `generar_guion()` en `generador_guiones_audio.py:57` para personalizar cómo ChatGPT genera los guiones.

## Solución de Problemas

### Error: "API key not found"
- Verifica que tu archivo `.env` existe y contiene las API keys correctas
- Asegúrate de que el archivo `.env` está en el mismo directorio que el script

### Error al generar audio
- Verifica que tu cuenta de ElevenLabs tiene créditos disponibles
- Comprueba que el `ELEVENLABS_VOICE_ID` es válido

### El guion generado no es adecuado
- Mejora la descripción en el JSON con más detalles
- Ajusta el prompt en la función `generar_guion()`
- Prueba con un modelo diferente de OpenAI

## Costos Estimados

- **OpenAI GPT-4**: ~$0.03 por guion (1000 tokens aprox.)
- **OpenAI GPT-3.5-turbo**: ~$0.002 por guion
- **ElevenLabs**: Varía según plan, ~1000 caracteres por audio

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

## Contacto y Contribuciones

Si encuentras errores o tienes sugerencias, no dudes en abrir un issue o pull request.

---

**Nota**: Basado en el código funcional de `elevenlabs_tts_audiomusic.py` y extendido con capacidades de generación de guiones usando OpenAI.
