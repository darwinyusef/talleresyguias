# 📧 Configuración de Emails con Resend

## Importante: Cómo funcionan los emails en Resend

### ⚠️ Restricción Principal

En **Resend**, el campo `from` **SOLO** puede usar:
1. ✅ Dominios verificados en tu cuenta de Resend
2. ✅ `onboarding@resend.dev` (para desarrollo/testing)

**NO puedes** usar el email del usuario que llena el formulario como remitente.

## 🔧 Configuración Correcta

### 1. Variables de Entorno

En `.env` o `public/conf.json`:

```env
# Email FROM (remitente verificado en Resend)
EMAIL_FROM=onboarding@resend.dev  # Para desarrollo
# O si tienes dominio verificado:
# EMAIL_FROM=noreply@tudominio.com

# Email TO (destinatario - tu email)
EMAIL_TO=wsgestor@gmail.com

# API Key de Resend
RESEND_API_KEY=re_tu_api_key_aqui
```

### 2. Para Verificar un Dominio Propio

Si quieres usar tu propio dominio (ej: `contacto@darwinyusef.com`):

1. Ve a https://resend.com/domains
2. Agrega tu dominio
3. Configura los registros DNS (SPF, DKIM, DMARC)
4. Una vez verificado, actualiza `EMAIL_FROM` con tu email

## 📝 Cómo Funcionan los Formularios

### Formulario de Contacto (`/api/send-email`)

```javascript
{
  from: "onboarding@resend.dev",  // ← Remitente verificado (TÚ)
  to: "wsgestor@gmail.com",       // ← Destinatario (TÚ)
  replyTo: "usuario@email.com",   // ← Email del usuario (para responder)
  subject: "Nuevo mensaje de contacto de Juan"
}
```

**Resultado:**
- ✅ Recibes el email en `wsgestor@gmail.com`
- ✅ Si haces "Responder", va directo al email del usuario
- ✅ El contenido del email muestra el email del usuario claramente

### Formulario de Testimonios (`/api/testimonial.json`)

```javascript
{
  from: "onboarding@resend.dev",
  to: "wsgestor@gmail.com",
  replyTo: "usuario@email.com",  // Si el usuario proporcionó email
  subject: "⭐ Nuevo Testimonio de Juan (5/5 estrellas)"
}
```

### Newsletter (`/api/newsletter.json`)

**Dos emails se envían:**

**1. Email al usuario (confirmación):**
```javascript
{
  from: "onboarding@resend.dev",  // ← TU dominio verificado
  to: "usuario@email.com",        // ← Al usuario que se suscribió
  subject: "✅ Confirmación de suscripción"
}
```

**2. Email a ti (notificación):**
```javascript
{
  from: "onboarding@resend.dev",
  to: "wsgestor@gmail.com",       // ← A ti
  subject: "📧 Nueva suscripción: usuario@email.com"
}
```

## 🎯 Resumen

| Campo | Propósito | Valor |
|-------|-----------|-------|
| `from` | Remitente del email | **Siempre tu dominio verificado** |
| `to` | Destinatario | Email de quien recibe |
| `replyTo` | Responder a | Email del usuario del formulario |
| `subject` | Asunto | Descripción del mensaje |

## 🚀 Mejoras Futuras

### Opción 1: Verificar tu Propio Dominio

Si tienes un dominio (ej: `darwinyusef.com`):
- Verifica el dominio en Resend
- Usa `contacto@darwinyusef.com` como `from`
- Más profesional y evita que los emails caigan en spam

### Opción 2: Usar Resend Audiences (Newsletter)

Para el newsletter, Resend tiene una funcionalidad de **Audiences** que permite:
- Gestionar suscriptores automáticamente
- Enviar newsletters masivos
- Manejar unsubscribe automáticamente
- Ver estadísticas de aperturas y clicks

Documentación: https://resend.com/docs/send-with-audiences

## 📚 Más Información

- Documentación de Resend: https://resend.com/docs
- Verificar dominios: https://resend.com/docs/dashboard/domains/introduction
- API Reference: https://resend.com/docs/api-reference/emails/send-email

## ⚡ Testing Rápido

Para probar que los emails funcionan:

```bash
# 1. Asegúrate de tener tu API key configurada
echo $RESEND_API_KEY

# 2. Levanta el servidor de desarrollo
npm run dev

# 3. Abre http://localhost:4322
# 4. Llena el formulario de contacto
# 5. Revisa tu email en wsgestor@gmail.com
```

## 🔒 Seguridad

- ✅ Las API keys están en `.env` (no se suben a Git)
- ✅ Validación de emails en el backend
- ✅ Rate limiting recomendado (próxima mejora)
- ✅ CAPTCHA recomendado para formularios públicos (próxima mejora)
