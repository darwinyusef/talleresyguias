# 🤖 Asistente Virtual con OpenAI

## Descripción

El portfolio ahora cuenta con un **asistente virtual inteligente** potenciado por OpenAI GPT-4o-mini que puede responder preguntas sobre:

- 💻 **Skills y Tecnologías**: Experiencia técnica, años de práctica, proficiencia
- 🛠️ **Servicios**: Aspectos técnicos de los servicios ofrecidos
- 📅 **Eventos**: Próximas conferencias y charlas
- 🏗️ **Arquitectura**: Especialización en arquitectura empresarial
- 🎯 **Un poco de mi vida**: Hobbies, pasiones y vida personal

## Arquitectura

### Componentes

1. **`/src/components/Chatbot.astro`**
   - UI del chatbot modal
   - Gestión del historial de conversación
   - Integración con la API

2. **`/src/pages/api/chat-assistant.json.ts`**
   - Endpoint API de Astro
   - Carga contexto dinámico desde GitHub
   - Integración con OpenAI GPT-4o-mini

### Flujo de Datos

```
Usuario escribe pregunta
        ↓
Chatbot.astro agrega al historial
        ↓
POST /api/chat-assistant.json
        ↓
Cargar contexto desde GitHub:
  - languages.json (skills)
  - services.json
  - events.json
  - architecture.json
        ↓
Construir prompt del sistema con contexto
        ↓
Llamar a OpenAI GPT-4o-mini
        ↓
Respuesta formateada en HTML
        ↓
Mostrar en el chatbot
```

## Fuentes de Contexto

El asistente carga datos en tiempo real desde:

```
https://github.com/darwinyusef/darwinyusef/tree/master/information/
├── languages.json    → Skills y tecnologías
├── services.json     → Servicios ofrecidos
├── events.json       → Próximos eventos
└── architecture.json → Especialización en arquitectura
```

**Fallback local:** Si GitHub no está disponible, intenta cargar desde:
- `public/languages.json`
- `information/events.json`

## Configuración

### 1. API Key de OpenAI

Opción A - Usando `public/conf.json` (actual):
```json
{
  "openai": "sk-proj-TU_API_KEY_AQUI"
}
```

Opción B - Usando `.env`:
```env
OPENAI_API_KEY=sk-proj-TU_API_KEY_AQUI
```

### 2. Obtener API Key

1. Ir a https://platform.openai.com/api-keys
2. Crear un nuevo API key
3. Copiarla en `public/conf.json` o `.env`

## Personalidad del Asistente

El asistente está configurado para ser:

- ✅ **Amigable y cercano** - Tono conversacional profesional
- ✅ **Técnicamente preciso** - Respuestas basadas en datos reales
- ✅ **Educativo** - Explica conceptos claramente
- ✅ **Contextual** - Mantiene el hilo de la conversación

### Restricciones

El asistente **NO puede**:
- ❌ Dar precios o presupuestos
- ❌ Hacer ofertas comerciales
- ❌ Comprometer agenda de Yusef
- ❌ Negociar términos

En su lugar, **redirige** a:
- Formulario de contacto: `/#contact`
- Sección de arquitectura: `/arquitectura`

## Formato de Respuestas

Las respuestas usan **HTML** (no markdown):

```html
<p>Los <strong>beneficios principales</strong> incluyen:</p>
<ul>
  <li><strong>Escalabilidad:</strong> Crece con tu negocio</li>
  <li><strong>Rendimiento:</strong> Optimizado para velocidad</li>
</ul>
<p>Para más información, visita <a href="/arquitectura">arquitectura</a>.</p>
```

### Estilos CSS

El componente incluye estilos para formatear las respuestas:
- `<p>` - Espaciado entre párrafos
- `<strong>` - Color azul primario (#3b82f6)
- `<ul><li>` - Listas con viñetas
- `<a>` - Enlaces con hover effect

## Uso en el Portfolio

### Activar el Chatbot

El botón del chatbot se encuentra en el `Footer.astro`:

```astro
<button id="chatbot-btn" ...>
  <span class="material-symbols-outlined">smart_toy</span>
</button>
```

### Ejemplos de Preguntas

**Skills:**
- "¿Qué tecnologías dominas?"
- "¿Cuántos años de experiencia tienes con React?"

**Servicios:**
- "¿Qué servicios ofreces?"
- "Explícame sobre arquitectura empresarial"

**Eventos:**
- "¿Tienes próximos eventos?"
- "¿Dónde vas a dar charlas?"

**Personal:**
- "¿Cuáles son tus hobbies?"
- "¿Qué te gusta hacer fuera del código?"

## Costos de OpenAI

**Modelo usado:** `gpt-4o-mini`
- **Input:** ~$0.15 por 1M tokens
- **Output:** ~$0.60 por 1M tokens

**Configuración actual:**
- Max tokens por respuesta: 500
- Temperature: 0.8 (creativo pero coherente)

**Estimación de costo:**
- ~$0.0003 - $0.0005 por conversación (10-15 mensajes)

## Mantenimiento

### Actualizar Contexto

El contexto se actualiza automáticamente desde GitHub. Para modificarlo:

1. Editar archivos en: `https://github.com/darwinyusef/darwinyusef/tree/master/information/`
2. El chatbot cargará los nuevos datos en la próxima conversación

### Logs y Debugging

Los logs aparecen en la consola del servidor:

```bash
📚 Cargando contexto...
✅ Skills cargadas desde GitHub: 25
✅ Servicios cargados desde GitHub: 8
✅ Eventos cargados desde GitHub: 12
🚀 Llamando a OpenAI con 3 mensajes
✅ Respuesta generada
```

### Monitoreo

Ver uso de tokens en: https://platform.openai.com/usage

## Troubleshooting

### Error: "La API de OpenAI no está configurada"
**Solución:** Verifica que `public/conf.json` tenga el API key correcto

### Error: "No se pudieron cargar skills/eventos"
**Solución:**
1. Verificar conexión a GitHub
2. Verificar que existan archivos fallback locales

### Las respuestas están en markdown en lugar de HTML
**Solución:** El sistema prompt especifica HTML. Si OpenAI responde en markdown, es un error temporal de la API.

## Mejoras Futuras

- [ ] Agregar rate limiting por IP
- [ ] Cache de contexto (reducir llamadas a GitHub)
- [ ] Modo offline con datos locales
- [ ] Analytics de preguntas frecuentes
- [ ] Exportar conversación como PDF
- [ ] Soporte para múltiples idiomas (ES/EN/PT)
- [ ] Integración con calendario para eventos
- [ ] Sugerencias de preguntas automáticas

## Seguridad

⚠️ **IMPORTANTE:**
- `public/conf.json` contiene la API key en texto plano
- Asegúrate de que `public/` NO se suba a repositorios públicos
- Considera usar variables de entorno en producción
- Implementar rate limiting para prevenir abuso

## Soporte

Para preguntas o problemas:
- Email: wsgestor@gmail.com
- Sección de contacto: [/#contact](/#contact)
