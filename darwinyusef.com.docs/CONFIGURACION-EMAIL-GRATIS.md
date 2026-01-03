# 📧 Configuración de Email GRATIS con Cloudflare + Gmail

Configuración 100% gratuita usando Cloudflare Email Routing para recibir y Gmail SMTP para enviar.

---

## 🎯 Configuración

- **Recibir emails:** Cloudflare Email Routing (GRATIS)
- **Enviar emails:** Gmail SMTP (GRATIS)
- **Dominio:** aquicreamos.com
- **Email de envío:** no-reply@aquicreamos.com
- **Email real:** wsgestor@gmail.com

---

## 📋 Parte 1: Cloudflare Email Routing (Recibir)

### Paso 1: Agregar Dominio a Cloudflare

1. **Login:** https://dash.cloudflare.com
2. **Add Site** → `aquicreamos.com`
3. **Plan:** Free
4. **Copiar Nameservers** y configurar en tu registrador

### Paso 2: Habilitar Email Routing

1. **Cloudflare Dashboard** → `aquicreamos.com`
2. **Email** → **Email Routing**
3. **Enable** (gratis, sin límites)

Cloudflare agregará automáticamente estos registros DNS:

```
MX    @    route1.mx.cloudflare.net    86
MX    @    route2.mx.cloudflare.net    24
MX    @    route3.mx.cloudflare.net    56
TXT   @    v=spf1 include:_spf.mx.cloudflare.net ~all
```

### Paso 3: Configurar Reenvío

1. **Destination Addresses** → **Add**
   ```
   Email: wsgestor@gmail.com
   ```
2. **Verify** (revisa tu Gmail y confirma)

3. **Routing Rules** → **Create Route**
   ```
   Type: Catch-all
   Action: Send to → wsgestor@gmail.com
   ```

**✅ Listo! Ahora cualquier email a `*@aquicreamos.com` llegará a `wsgestor@gmail.com`**

---

## 📋 Parte 2: Gmail SMTP (Enviar)

### Paso 1: Crear Contraseña de Aplicación en Gmail

1. **Ve a tu cuenta Google:** https://myaccount.google.com/
2. **Seguridad** → **Verificación en dos pasos**
   - Si no la tienes, **actívala primero**
3. **Seguridad** → **Contraseñas de aplicaciones**
4. **Crear nueva:**
   ```
   App: Portfolio Website
   Device: Custom
   ```
5. **Generar** y **copiar la contraseña** (16 caracteres)
   ```
   Ejemplo: abcd efgh ijkl mnop
   ```

### Paso 2: Configurar SPF para Gmail

En Cloudflare DNS, agrega:

```
TXT   @   v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all
```

Esto permite que Gmail envíe emails en nombre de tu dominio.

---

## 📋 Parte 3: Configurar el Código

### Instalar Nodemailer

```bash
cd astro-portfolio
npm install nodemailer
npm install --save-dev @types/nodemailer
```

### Crear Utilidad de Email

**src/utils/emailSender.ts**

```typescript
import nodemailer from 'nodemailer';

// Configuración del transporter de Gmail
const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com',
  port: 587,
  secure: false, // true para 465, false para otros puertos
  auth: {
    user: import.meta.env.GMAIL_USER,
    pass: import.meta.env.GMAIL_APP_PASSWORD,
  },
});

interface EmailOptions {
  to: string;
  subject: string;
  html: string;
  text?: string;
  replyTo?: string;
  from?: string;
}

export async function sendEmail(options: EmailOptions) {
  try {
    const fromEmail = import.meta.env.EMAIL_FROM || 'no-reply@aquicreamos.com';
    const fromName = import.meta.env.EMAIL_FROM_NAME || 'Darwin Yusef';

    const info = await transporter.sendMail({
      from: `"${fromName}" <${fromEmail}>`,
      to: options.to,
      replyTo: options.replyTo,
      subject: options.subject,
      text: options.text,
      html: options.html,
    });

    console.log('Email sent successfully:', info.messageId);
    return { success: true, messageId: info.messageId };
  } catch (error) {
    console.error('Error sending email:', error);
    return { success: false, error };
  }
}
```

### Actualizar API de Contacto

**src/pages/api/contact.ts**

```typescript
import type { APIRoute } from 'astro';
import { z } from 'zod';
import { sendEmail } from '../../utils/emailSender';

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  subject: z.string().min(3, 'Subject must be at least 3 characters'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
  phone: z.string().optional(),
});

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const data = contactSchema.parse(body);

    // Email HTML para ti (wsgestor@gmail.com)
    const notificationHtml = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
          }
          .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px 10px 0 0;
          }
          .content {
            background: #f9fafb;
            padding: 30px;
            border: 1px solid #e5e7eb;
            border-radius: 0 0 10px 10px;
          }
          .field {
            margin-bottom: 20px;
          }
          .label {
            font-weight: 600;
            color: #4b5563;
            margin-bottom: 5px;
          }
          .value {
            color: #1f2937;
          }
          .message-box {
            background: white;
            padding: 20px;
            border-left: 4px solid #667eea;
            margin-top: 10px;
            border-radius: 4px;
          }
          .button {
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white !important;
            text-decoration: none;
            border-radius: 6px;
            margin-top: 15px;
          }
          .footer {
            text-align: center;
            padding: 20px;
            color: #6b7280;
            font-size: 12px;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1 style="margin: 0;">📧 Nuevo Mensaje de Contacto</h1>
          <p style="margin: 10px 0 0 0; opacity: 0.9;">Portfolio - darwinyusef.com</p>
        </div>

        <div class="content">
          <div class="field">
            <div class="label">👤 Nombre:</div>
            <div class="value"><strong>${data.name}</strong></div>
          </div>

          <div class="field">
            <div class="label">📧 Email:</div>
            <div class="value">
              <a href="mailto:${data.email}" style="color: #667eea;">${data.email}</a>
            </div>
          </div>

          ${data.phone ? `
          <div class="field">
            <div class="label">📱 Teléfono:</div>
            <div class="value">${data.phone}</div>
          </div>
          ` : ''}

          <div class="field">
            <div class="label">📋 Asunto:</div>
            <div class="value"><strong>${data.subject}</strong></div>
          </div>

          <div class="field">
            <div class="label">💬 Mensaje:</div>
            <div class="message-box">${data.message.replace(/\n/g, '<br>')}</div>
          </div>

          <a href="mailto:${data.email}?subject=Re: ${encodeURIComponent(data.subject)}" class="button">
            ✉️ Responder Email
          </a>
        </div>

        <div class="footer">
          <p>📍 Enviado desde el formulario de contacto en darwinyusef.com</p>
          <p>🕐 ${new Date().toLocaleString('es-ES', { timeZone: 'America/New_York' })}</p>
        </div>
      </body>
      </html>
    `;

    // Email de confirmación para el usuario
    const confirmationHtml = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
          }
          .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
          }
          .content {
            padding: 30px;
            background: #f9fafb;
            border-radius: 10px;
            margin-top: 20px;
          }
          .footer {
            text-align: center;
            padding: 20px;
            color: #6b7280;
            font-size: 14px;
          }
          a {
            color: #667eea;
            text-decoration: none;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1 style="margin: 0; font-size: 32px;">✨ ¡Gracias por contactarme!</h1>
        </div>

        <div class="content">
          <p>Hola <strong>${data.name}</strong>,</p>

          <p>He recibido tu mensaje sobre "<em>${data.subject}</em>" y te responderé lo antes posible.</p>

          <p>Mientras tanto, puedes:</p>
          <ul>
            <li>🌐 Visitar mi portfolio: <a href="https://darwinyusef.com">darwinyusef.com</a></li>
            <li>💼 Ver mis proyectos en <a href="https://github.com/darwinyusef">GitHub</a></li>
            <li>🏢 Conocer más sobre <a href="https://aquicreamos.com">AquiCreamos</a></li>
          </ul>

          <p style="margin-top: 30px;">
            Saludos cordiales,<br>
            <strong>Darwin Yusef</strong><br>
            <span style="color: #6b7280;">Full Stack Developer</span>
          </p>
        </div>

        <div class="footer">
          <p>Este es un mensaje automático, por favor no respondas a este email.</p>
          <p>Para contacto directo: <a href="mailto:contacto@aquicreamos.com">contacto@aquicreamos.com</a></p>
        </div>
      </body>
      </html>
    `;

    // Enviar email de notificación a ti
    const notificationResult = await sendEmail({
      to: import.meta.env.EMAIL_TO || 'wsgestor@gmail.com',
      subject: `[Portfolio] ${data.subject}`,
      html: notificationHtml,
      text: `
Nuevo mensaje de contacto

Nombre: ${data.name}
Email: ${data.email}
${data.phone ? `Teléfono: ${data.phone}` : ''}
Asunto: ${data.subject}

Mensaje:
${data.message}

---
Enviado desde darwinyusef.com
${new Date().toISOString()}
      `,
      replyTo: data.email,
    });

    if (!notificationResult.success) {
      throw new Error('Failed to send notification email');
    }

    // Enviar email de confirmación al usuario
    await sendEmail({
      to: data.email,
      subject: `Gracias por contactarme - ${data.subject}`,
      html: confirmationHtml,
      replyTo: import.meta.env.EMAIL_REPLY_TO || 'contacto@aquicreamos.com',
    });

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Email sent successfully',
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Contact form error:', error);

    if (error instanceof z.ZodError) {
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Validation error',
          details: error.errors,
        }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    return new Response(
      JSON.stringify({
        success: false,
        error: 'Internal server error',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
```

---

## 📋 Parte 4: Variables de Entorno

### .env (Local y Servidor)

```bash
# Gmail SMTP Configuration
GMAIL_USER=wsgestor@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop    # La contraseña de aplicación de 16 caracteres

# Email Configuration
EMAIL_FROM=no-reply@aquicreamos.com
EMAIL_FROM_NAME=Darwin Yusef
EMAIL_TO=wsgestor@gmail.com
EMAIL_REPLY_TO=contacto@aquicreamos.com

# Site
SITE_URL=https://darwinyusef.com
```

### .env.example

```bash
# Gmail SMTP Configuration
GMAIL_USER=tu_email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Email Configuration
EMAIL_FROM=no-reply@aquicreamos.com
EMAIL_FROM_NAME=Tu Nombre
EMAIL_TO=tu_email@gmail.com
EMAIL_REPLY_TO=contacto@aquicreamos.com

# Site
SITE_URL=https://tu-dominio.com
```

---

## 📋 Parte 5: Configurar en Servidor

```bash
# Conectar al servidor
ssh root@YOUR_SERVER_IP

# Actualizar código
cd /opt/portfolio
git pull

# Instalar dependencias
cd astro-portfolio
npm install

# Configurar .env
nano .env
```

**Pega la configuración de variables de entorno y guarda**

```bash
# Rebuild y restart
docker-compose down
docker-compose up -d --build

# Ver logs
docker logs -f astro-portfolio
```

---

## 🧪 Testing

### Test 1: Cloudflare Email Routing

```bash
# Envía un email de prueba a:
contacto@aquicreamos.com
# o
prueba@aquicreamos.com

# Debe llegar a wsgestor@gmail.com
```

### Test 2: Envío vía Gmail SMTP

```bash
# Crea un archivo test en el servidor
ssh root@YOUR_SERVER_IP
cd /opt/portfolio/astro-portfolio

# Crear test script
cat > test-email.js << 'EOF'
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com',
  port: 587,
  secure: false,
  auth: {
    user: 'wsgestor@gmail.com',
    pass: 'TU_PASSWORD_DE_APLICACION_AQUI',
  },
});

async function test() {
  const info = await transporter.sendMail({
    from: '"Darwin Yusef" <no-reply@aquicreamos.com>',
    to: 'wsgestor@gmail.com',
    subject: 'Test Email Portfolio',
    html: '<h1>Test exitoso!</h1><p>El email funciona correctamente.</p>',
  });

  console.log('Message sent:', info.messageId);
}

test().catch(console.error);
EOF

# Ejecutar test
node test-email.js

# Verifica que llegue el email
```

### Test 3: Formulario Completo

```bash
# Abre en navegador
https://darwinyusef.com/contact

# Llena el formulario y envía

# Verifica:
# 1. ✅ Email llega a wsgestor@gmail.com
# 2. ✅ Email de confirmación llega al usuario
# 3. ✅ Reply-To es el email del usuario
# 4. ✅ From es no-reply@aquicreamos.com
```

---

## 🔍 Verificación DNS

```bash
# Verificar MX (Email Routing)
dig MX aquicreamos.com +short

# Debe mostrar:
# 24 route2.mx.cloudflare.net.
# 56 route3.mx.cloudflare.net.
# 86 route1.mx.cloudflare.net.

# Verificar SPF
dig TXT aquicreamos.com +short

# Debe incluir:
# "v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all"
```

---

## 💰 Costos

```
Cloudflare Email Routing: GRATIS ✅
Gmail SMTP: GRATIS ✅
Cloudflare DNS: GRATIS ✅

Total: $0/mes 🎉
```

---

## 🔄 Flujo Completo

```
┌─────────────────────────────────────────────────────────┐
│  ENVÍO (Portfolio → Usuario)                            │
├─────────────────────────────────────────────────────────┤
│  1. Usuario llena formulario en darwinyusef.com        │
│  2. API /api/contact procesa                            │
│  3. Gmail SMTP envía emails:                            │
│     ├─ A ti: wsgestor@gmail.com                         │
│     │  From: no-reply@aquicreamos.com                   │
│     │  Reply-To: email_del_usuario                      │
│     │                                                    │
│     └─ Al usuario: confirmación                         │
│        From: no-reply@aquicreamos.com                   │
│        Reply-To: contacto@aquicreamos.com               │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  RECEPCIÓN (Email → Tu Gmail)                           │
├─────────────────────────────────────────────────────────┤
│  1. Alguien envía a contacto@aquicreamos.com            │
│  2. Cloudflare Email Routing recibe                     │
│  3. Reenvía automáticamente a wsgestor@gmail.com        │
│  4. Recibes en Gmail                                    │
│  5. Respondes normalmente desde Gmail                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Error: "Invalid login"

**Problema:** Contraseña de aplicación incorrecta

**Solución:**
1. Ve a Google Account → Security
2. App Passwords → Generate new
3. Copia la nueva password (16 caracteres sin espacios)
4. Actualiza `.env`

### Emails van a spam

**Solución:**
1. Verifica SPF: debe incluir `_spf.google.com`
2. Agrega DKIM de Google (opcional):
   - Google Workspace Admin
   - Generar DKIM key
3. No uses palabras spam en el asunto

### Rate limit de Gmail

Gmail SMTP tiene límite de **500 emails/día**

**Si lo excedes:**
- Espera 24 horas
- O usa Cloudflare Email Workers (límite mayor)

---

## ✅ Checklist Final

- [ ] Cloudflare Email Routing configurado
- [ ] wsgestor@gmail.com verificado
- [ ] Routing rule configurada (catch-all)
- [ ] Gmail App Password generada
- [ ] SPF configurado (Cloudflare + Google)
- [ ] Nodemailer instalado
- [ ] Variables de entorno configuradas
- [ ] Código actualizado
- [ ] Test de recepción exitoso
- [ ] Test de envío exitoso
- [ ] Formulario funcionando

---

**🎉 ¡Configuración 100% gratuita completada!**

**Última actualización:** Enero 2026
