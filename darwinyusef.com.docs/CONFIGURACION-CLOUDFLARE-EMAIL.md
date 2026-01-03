# 📧 Configuración de Email con Cloudflare + Resend

Guía para configurar emails usando Cloudflare Email Routing y Resend con el dominio `aquicreamos.com`.

---

## 🎯 Configuración Objetivo

- **Dominio principal portfolio:** darwinyusef.com
- **Dominio de email:** aquicreamos.com
- **Email de envío:** no-reply@aquicreamos.com
- **Email de recepción:** wsgestor@gmail.com
- **Servicio de envío:** Resend
- **Routing:** Cloudflare Email Routing

---

## 📋 Índice

1. [Configurar Cloudflare Email Routing](#1-configurar-cloudflare-email-routing)
2. [Configurar Resend con Cloudflare](#2-configurar-resend-con-cloudflare)
3. [Actualizar Variables de Entorno](#3-actualizar-variables-de-entorno)
4. [Actualizar Código del Portfolio](#4-actualizar-código-del-portfolio)
5. [Testing](#5-testing)

---

## 1. Configurar Cloudflare Email Routing

### Paso 1: Agregar Dominio a Cloudflare

Si `aquicreamos.com` no está en Cloudflare:

1. **Login en Cloudflare:** https://dash.cloudflare.com
2. **Add a Site** → `aquicreamos.com`
3. **Select Plan:** Free
4. **Copy Nameservers** y configúralos en tu registrador:
   ```
   ns1.cloudflare.com
   ns2.cloudflare.com
   ```
5. **Wait for DNS propagation** (puede tomar 24-48 horas)

### Paso 2: Habilitar Email Routing

1. **En Cloudflare Dashboard:**
   - Selecciona `aquicreamos.com`
   - Sidebar → **Email** → **Email Routing**

2. **Enable Email Routing:**
   - Click **Get started** o **Enable**
   - Cloudflare agregará automáticamente los registros MX necesarios

3. **Verificar registros DNS:**
   Deberías ver estos registros automáticamente:
   ```
   Tipo  Nombre              Valor                           Prioridad
   ─────────────────────────────────────────────────────────────────────
   MX    aquicreamos.com     route1.mx.cloudflare.net       86
   MX    aquicreamos.com     route2.mx.cloudflare.net       24
   MX    aquicreamos.com     route3.mx.cloudflare.net       56
   TXT   aquicreamos.com     v=spf1 include:_spf.mx.cloudflare.net ~all
   ```

### Paso 3: Configurar Destination Address (Recepción)

1. **Email Routing** → **Destination addresses**
2. **Add destination address:**
   ```
   Email: wsgestor@gmail.com
   ```
3. **Verify** - Revisa tu email `wsgestor@gmail.com` y click en el link de verificación

### Paso 4: Configurar Routing Rules (Reglas de Reenvío)

1. **Email Routing** → **Routing rules**
2. **Create rule:**

**Opción A: Catch-all (Recomendado para empezar)**
```
Rule name: Forward all to wsgestor
Custom address: *@aquicreamos.com
Action: Send to → wsgestor@gmail.com
```

**Opción B: Específico (Más control)**
```
Rule 1:
  Name: Contact form emails
  Custom address: no-reply@aquicreamos.com
  Action: Send to → wsgestor@gmail.com

Rule 2:
  Name: Contact inquiries
  Custom address: contacto@aquicreamos.com
  Action: Send to → wsgestor@gmail.com
```

3. **Save and Enable**

### Paso 5: Verificar Email Routing

Cloudflare te enviará un email de prueba. Verifica que llegue a `wsgestor@gmail.com`.

---

## 2. Configurar Resend con Cloudflare

### Paso 1: Login en Resend

1. Ve a https://resend.com
2. Login con tu cuenta

### Paso 2: Agregar Dominio

1. **Dashboard** → **Domains**
2. **Add Domain:**
   ```
   Domain: aquicreamos.com
   Region: us-east-1 (o tu región preferida)
   ```
3. Click **Add**

### Paso 3: Configurar Registros DNS en Cloudflare

Resend te mostrará registros DNS que debes agregar. Ve a Cloudflare:

1. **Cloudflare Dashboard** → `aquicreamos.com` → **DNS** → **Records**

2. **Agregar registros de Resend** (los valores exactos te los da Resend):

```
Tipo   Nombre                        Valor                                      TTL
─────────────────────────────────────────────────────────────────────────────────────
TXT    aquicreamos.com              v=spf1 include:send.resend.com ~all        Auto
TXT    resend._domainkey            (valor largo proporcionado por Resend)     Auto
TXT    _dmarc                       v=DMARC1; p=none; rua=mailto:wsgestor@gmail.com  Auto
```

**Ejemplo de registros (los valores pueden variar):**

```
TXT    resend._domainkey.aquicreamos.com    "k=rsa; p=MIGfMA0GCSqGSIb3DQEBA..."
```

3. **Importante:**
   - En Cloudflare, cuando agregues los registros TXT de DKIM, usa el nombre exacto que Resend te indica
   - Si Resend dice `resend._domainkey.aquicreamos.com`, en Cloudflare pon solo `resend._domainkey`

### Paso 4: Verificar Dominio en Resend

1. **En Resend** → **Domains** → `aquicreamos.com`
2. Click **Verify DNS Records**
3. Espera unos minutos (puede tomar hasta 48 horas)
4. Status debe cambiar a **Verified** ✅

### Paso 5: Configurar SPF, DKIM, DMARC

#### SPF (Sender Policy Framework)
Ya configurado en Paso 3, pero verifica que tengas ambos (Cloudflare Email Routing + Resend):

```
TXT    @    v=spf1 include:_spf.mx.cloudflare.net include:send.resend.com ~all
```

#### DKIM (DomainKeys Identified Mail)
Ya configurado en Paso 3.

#### DMARC (Domain-based Message Authentication)
```
TXT    _dmarc    v=DMARC1; p=none; rua=mailto:wsgestor@gmail.com; ruf=mailto:wsgestor@gmail.com; fo=1
```

**Explicación:**
- `p=none` - Política de monitoreo (cambia a `quarantine` o `reject` después de testing)
- `rua` - Reports agregados van a tu email
- `ruf` - Reports forenses van a tu email
- `fo=1` - Reportar en caso de fallo

---

## 3. Actualizar Variables de Entorno

### En el Servidor (Production)

```bash
# Conectar al servidor
ssh root@YOUR_SERVER_IP

# Editar .env
cd /opt/portfolio/astro-portfolio
nano .env
```

**Actualizar estas líneas:**

```bash
# Email Configuration
RESEND_API_KEY=re_xxxxxxxxxxxxx
RESEND_FROM_EMAIL=no-reply@aquicreamos.com
RESEND_FROM_NAME=Darwin Yusef
RESEND_TO_EMAIL=wsgestor@gmail.com
RESEND_REPLY_TO=contacto@aquicreamos.com

# Site Configuration
SITE_URL=https://darwinyusef.com
CONTACT_EMAIL=contacto@aquicreamos.com
```

**Guardar:** `Ctrl+O`, Enter, `Ctrl+X`

### Local (.env)

```bash
# En tu proyecto local
cd astro-portfolio
nano .env
```

Actualiza con los mismos valores.

### .env.example

```bash
# Actualizar .env.example para documentación
nano .env.example
```

```bash
# Email Configuration
RESEND_API_KEY=re_your_api_key_here
RESEND_FROM_EMAIL=no-reply@aquicreamos.com
RESEND_FROM_NAME=Darwin Yusef
RESEND_TO_EMAIL=wsgestor@gmail.com
RESEND_REPLY_TO=contacto@aquicreamos.com

# Site Configuration
SITE_URL=https://darwinyusef.com
CONTACT_EMAIL=contacto@aquicreamos.com
```

---

## 4. Actualizar Código del Portfolio

### Actualizar API de Contacto

**src/pages/api/contact.ts**

Actualiza el código existente para usar las nuevas variables:

```typescript
import type { APIRoute } from 'astro';
import { Resend } from 'resend';
import { z } from 'zod';

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  subject: z.string().min(3, 'Subject must be at least 3 characters'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
  phone: z.string().optional(),
});

const resend = new Resend(import.meta.env.RESEND_API_KEY);

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const validatedData = contactSchema.parse(body);

    // Email HTML template
    const emailHtml = `
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
          .footer {
            text-align: center;
            padding: 20px;
            color: #6b7280;
            font-size: 12px;
          }
          .button {
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin-top: 10px;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1 style="margin: 0;">📧 Nuevo Mensaje de Contacto</h1>
          <p style="margin: 10px 0 0 0; opacity: 0.9;">Desde tu portfolio</p>
        </div>

        <div class="content">
          <div class="field">
            <div class="label">👤 Nombre:</div>
            <div class="value">${validatedData.name}</div>
          </div>

          <div class="field">
            <div class="label">📧 Email:</div>
            <div class="value">
              <a href="mailto:${validatedData.email}">${validatedData.email}</a>
            </div>
          </div>

          ${validatedData.phone ? `
          <div class="field">
            <div class="label">📱 Teléfono:</div>
            <div class="value">${validatedData.phone}</div>
          </div>
          ` : ''}

          <div class="field">
            <div class="label">📋 Asunto:</div>
            <div class="value">${validatedData.subject}</div>
          </div>

          <div class="field">
            <div class="label">💬 Mensaje:</div>
            <div class="message-box">${validatedData.message.replace(/\n/g, '<br>')}</div>
          </div>

          <a href="mailto:${validatedData.email}?subject=Re: ${encodeURIComponent(validatedData.subject)}" class="button">
            Responder Email
          </a>
        </div>

        <div class="footer">
          <p>Este mensaje fue enviado desde el formulario de contacto en darwinyusef.com</p>
          <p>Enviado el ${new Date().toLocaleString('es-ES', { timeZone: 'America/New_York' })}</p>
        </div>
      </body>
      </html>
    `;

    // Send email
    const { data, error } = await resend.emails.send({
      from: `${import.meta.env.RESEND_FROM_NAME} <${import.meta.env.RESEND_FROM_EMAIL}>`,
      to: import.meta.env.RESEND_TO_EMAIL,
      replyTo: validatedData.email,
      subject: `[Portfolio] ${validatedData.subject}`,
      html: emailHtml,
      text: `
Nuevo mensaje de contacto

Nombre: ${validatedData.name}
Email: ${validatedData.email}
${validatedData.phone ? `Teléfono: ${validatedData.phone}` : ''}
Asunto: ${validatedData.subject}

Mensaje:
${validatedData.message}

---
Enviado desde darwinyusef.com
${new Date().toISOString()}
      `,
    });

    if (error) {
      console.error('Resend error:', error);
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Failed to send email',
          details: error,
        }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Send confirmation email to user
    await resend.emails.send({
      from: `${import.meta.env.RESEND_FROM_NAME} <${import.meta.env.RESEND_FROM_EMAIL}>`,
      to: validatedData.email,
      replyTo: import.meta.env.RESEND_REPLY_TO,
      subject: `Gracias por contactarme - ${validatedData.subject}`,
      html: `
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
              border-radius: 10px;
              text-align: center;
            }
            .content {
              padding: 30px;
              background: #f9fafb;
              border-radius: 10px;
              margin-top: 20px;
            }
          </style>
        </head>
        <body>
          <div class="header">
            <h1 style="margin: 0;">✨ ¡Gracias por tu mensaje!</h1>
          </div>
          <div class="content">
            <p>Hola <strong>${validatedData.name}</strong>,</p>
            <p>He recibido tu mensaje sobre "<em>${validatedData.subject}</em>".</p>
            <p>Te responderé lo antes posible.</p>
            <p>Mientras tanto, puedes:</p>
            <ul>
              <li>Visitar mi portfolio: <a href="https://darwinyusef.com">darwinyusef.com</a></li>
              <li>Ver mis proyectos en <a href="https://github.com/darwinyusef">GitHub</a></li>
            </ul>
            <p>Saludos,<br><strong>Darwin Yusef</strong></p>
          </div>
        </body>
        </html>
      `,
    });

    console.log('Email sent successfully:', data);

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Email sent successfully',
        id: data?.id,
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

## 5. Testing

### Test 1: Envío de Email desde Resend

```bash
# En Resend Dashboard
# Domains → aquicreamos.com → Send Test Email

To: wsgestor@gmail.com
From: no-reply@aquicreamos.com
Subject: Test Email
Body: This is a test

# Verifica que llegue a wsgestor@gmail.com
```

### Test 2: Email Routing de Cloudflare

```bash
# Envía un email a:
contacto@aquicreamos.com

# Debe llegar a:
wsgestor@gmail.com
```

### Test 3: Formulario de Contacto

```bash
# En el servidor (después de deploy)
cd /opt/portfolio/astro-portfolio
docker-compose restart

# Abre en navegador:
https://darwinyusef.com/contact

# Llena el formulario y envía
# Verifica:
# 1. Email llega a wsgestor@gmail.com
# 2. Email de confirmación llega al usuario
# 3. Reply-To es contacto@aquicreamos.com
```

### Test 4: Reply-To

1. Recibe el email en `wsgestor@gmail.com`
2. Click "Responder"
3. Verifica que el destinatario sea el email del usuario (no no-reply@aquicreamos.com)

---

## 🔍 Verificación de DNS

```bash
# Verificar MX records (Cloudflare Email Routing)
dig MX aquicreamos.com +short

# Debe mostrar:
# 86 route1.mx.cloudflare.net.
# 24 route2.mx.cloudflare.net.
# 56 route3.mx.cloudflare.net.

# Verificar SPF
dig TXT aquicreamos.com +short

# Debe incluir:
# "v=spf1 include:_spf.mx.cloudflare.net include:send.resend.com ~all"

# Verificar DKIM
dig TXT resend._domainkey.aquicreamos.com +short

# Debe mostrar la clave pública

# Verificar DMARC
dig TXT _dmarc.aquicreamos.com +short

# Debe mostrar:
# "v=DMARC1; p=none; rua=mailto:wsgestor@gmail.com..."
```

---

## 📧 Resumen de Configuración

```
┌─────────────────────────────────────────────────────────────┐
│  FLUJO DE EMAIL                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Usuario envía formulario en darwinyusef.com            │
│     ↓                                                       │
│  2. API /api/contact procesa                                │
│     ↓                                                       │
│  3. Resend envía email                                      │
│     ├─ From: no-reply@aquicreamos.com                       │
│     ├─ To: wsgestor@gmail.com                               │
│     └─ Reply-To: email_del_usuario                          │
│     ↓                                                       │
│  4. Recibes en wsgestor@gmail.com                           │
│     ├─ Puedes responder directamente al usuario             │
│     └─ Usuario recibe confirmación automática               │
│                                                             │
│  INCOMING EMAIL (opcional):                                 │
│                                                             │
│  1. Alguien envía email a contacto@aquicreamos.com          │
│     ↓                                                       │
│  2. Cloudflare Email Routing                                │
│     ↓                                                       │
│  3. Reenvía a wsgestor@gmail.com                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### Emails no llegan

1. **Verificar DNS:**
   ```bash
   dig MX aquicreamos.com
   dig TXT aquicreamos.com
   ```

2. **Verificar en Resend:**
   - Dashboard → Logs
   - Ver si hay errores

3. **Verificar en Cloudflare:**
   - Email Routing → Activity log
   - Ver si los emails están siendo procesados

### Emails van a spam

1. **Verificar SPF, DKIM, DMARC:**
   - Usa https://mxtoolbox.com/SuperTool.aspx
   - Verifica `aquicreamos.com`

2. **Warming up:**
   - Envía pocos emails al principio
   - Incrementa gradualmente

3. **Contenido:**
   - Evita palabras spam
   - Incluye texto plain además de HTML

### Reply-To no funciona

1. Verifica que `RESEND_REPLY_TO` esté configurado
2. Verifica que el código incluye `replyTo: validatedData.email`

---

## ✅ Checklist Final

- [ ] Cloudflare Email Routing habilitado
- [ ] wsgestor@gmail.com verificado en Cloudflare
- [ ] Regla de routing creada
- [ ] Dominio agregado en Resend
- [ ] Registros DNS (SPF, DKIM, DMARC) configurados
- [ ] Dominio verificado en Resend
- [ ] Variables de entorno actualizadas
- [ ] Código actualizado
- [ ] Test de envío exitoso
- [ ] Test de recepción exitoso
- [ ] Formulario funcionando

---

**¡Listo! Tu sistema de email está configurado profesionalmente! 📧**

**Última actualización:** Enero 2026
