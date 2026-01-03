# Configuración de Email y Calendario - Portfolio

Guía completa para configurar el formulario de contacto, envío de emails y calendario.

---

## 📋 Índice

1. [Configurar Resend para Emails](#1-configurar-resend-para-emails)
2. [API de Contacto en Astro](#2-api-de-contacto-en-astro)
3. [Integración con Google Calendar](#3-integración-con-google-calendar)
4. [Formulario de Contacto](#4-formulario-de-contacto)
5. [Verificación y Testing](#5-verificación-y-testing)

---

## 1. Configurar Resend para Emails

### 1.1 Crear Cuenta en Resend

1. Ve a https://resend.com
2. Crea una cuenta
3. Verifica tu email

### 1.2 Obtener API Key

1. Dashboard → API Keys
2. Create API Key
3. Name: `Portfolio Production`
4. Permission: `Sending access`
5. Copy API Key: `re_xxxxxxxxxxxxx`

### 1.3 Configurar Dominio (Opcional pero Recomendado)

**Para enviar desde tu dominio (ej: noreply@darwinyusef.com):**

1. Resend Dashboard → Domains
2. Add Domain → `darwinyusef.com`
3. Agregar estos registros DNS en DigitalOcean:

```
TXT  @ resend._domainkey  (valor proporcionado por Resend)
MX   @                    (valor proporcionado por Resend)
```

4. Verify Domain

### 1.4 Configurar Variables de Entorno

**.env**
```bash
# Resend Email
RESEND_API_KEY=re_xxxxxxxxxxxxx
RESEND_FROM_EMAIL=noreply@darwinyusef.com  # o tu email verificado
RESEND_TO_EMAIL=darwin.yusef@gmail.com     # donde recibes los mensajes
```

**.env.example**
```bash
# Resend Email
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com
RESEND_TO_EMAIL=your@email.com
```

---

## 2. API de Contacto en Astro

### 2.1 Instalar Dependencias

```bash
cd astro-portfolio
npm install resend zod
```

### 2.2 Crear API Endpoint

**src/pages/api/contact.ts**
```typescript
import type { APIRoute } from 'astro';
import { Resend } from 'resend';
import { z } from 'zod';

// Validation schema
const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  subject: z.string().min(3, 'Subject must be at least 3 characters'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
  phone: z.string().optional(),
});

// Initialize Resend
const resend = new Resend(import.meta.env.RESEND_API_KEY);

export const POST: APIRoute = async ({ request }) => {
  try {
    // Parse request body
    const body = await request.json();

    // Validate data
    const validatedData = contactSchema.parse(body);

    // Prepare email content
    const emailHtml = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
        </style>
      </head>
      <body>
        <div class="header">
          <h1 style="margin: 0;">📧 New Contact Message</h1>
          <p style="margin: 10px 0 0 0; opacity: 0.9;">From your portfolio website</p>
        </div>

        <div class="content">
          <div class="field">
            <div class="label">Name:</div>
            <div class="value">${validatedData.name}</div>
          </div>

          <div class="field">
            <div class="label">Email:</div>
            <div class="value">
              <a href="mailto:${validatedData.email}">${validatedData.email}</a>
            </div>
          </div>

          ${validatedData.phone ? `
          <div class="field">
            <div class="label">Phone:</div>
            <div class="value">${validatedData.phone}</div>
          </div>
          ` : ''}

          <div class="field">
            <div class="label">Subject:</div>
            <div class="value">${validatedData.subject}</div>
          </div>

          <div class="field">
            <div class="label">Message:</div>
            <div class="message-box">${validatedData.message.replace(/\n/g, '<br>')}</div>
          </div>
        </div>

        <div class="footer">
          <p>This message was sent from the contact form on darwinyusef.com</p>
          <p>Sent on ${new Date().toLocaleString()}</p>
        </div>
      </body>
      </html>
    `;

    // Send email using Resend
    const { data, error } = await resend.emails.send({
      from: import.meta.env.RESEND_FROM_EMAIL,
      to: import.meta.env.RESEND_TO_EMAIL,
      replyTo: validatedData.email,
      subject: `Portfolio Contact: ${validatedData.subject}`,
      html: emailHtml,
      text: `
Name: ${validatedData.name}
Email: ${validatedData.email}
${validatedData.phone ? `Phone: ${validatedData.phone}` : ''}
Subject: ${validatedData.subject}

Message:
${validatedData.message}
      `,
    });

    if (error) {
      console.error('Resend error:', error);
      return new Response(
        JSON.stringify({
          success: false,
          error: 'Failed to send email',
        }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Log success
    console.log('Email sent successfully:', data);

    // Return success response
    return new Response(
      JSON.stringify({
        success: true,
        message: 'Email sent successfully',
        id: data?.id,
      }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }
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

## 3. Integración con Google Calendar

### 3.1 Configurar Google Calendar API

1. Ve a https://console.cloud.google.com
2. Crear proyecto: `Portfolio Contact`
3. Habilitar API: Google Calendar API
4. Crear credenciales: Service Account
5. Descargar JSON de credenciales

### 3.2 Compartir Calendar

1. Google Calendar → Settings
2. Tu calendario → Share with specific people
3. Agregar el email del service account
4. Permiso: Make changes to events

### 3.3 Configurar Variables de Entorno

**.env**
```bash
# Google Calendar
GOOGLE_CALENDAR_ID=your-calendar-id@group.calendar.google.com
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service@project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
```

### 3.4 Instalar Dependencias

```bash
npm install googleapis
```

### 3.5 Crear Utilidad para Calendar

**src/utils/googleCalendar.ts**
```typescript
import { google } from 'googleapis';

const SCOPES = ['https://www.googleapis.com/auth/calendar'];

function getAuthClient() {
  const auth = new google.auth.JWT({
    email: import.meta.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
    key: import.meta.env.GOOGLE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
    scopes: SCOPES,
  });

  return auth;
}

export interface CalendarEvent {
  summary: string;
  description: string;
  start: string; // ISO date
  end: string;   // ISO date
  attendees?: string[];
}

export async function createCalendarEvent(event: CalendarEvent) {
  try {
    const auth = getAuthClient();
    const calendar = google.calendar({ version: 'v3', auth });

    const response = await calendar.events.insert({
      calendarId: import.meta.env.GOOGLE_CALENDAR_ID,
      requestBody: {
        summary: event.summary,
        description: event.description,
        start: {
          dateTime: event.start,
          timeZone: 'America/New_York', // Ajusta tu timezone
        },
        end: {
          dateTime: event.end,
          timeZone: 'America/New_York',
        },
        attendees: event.attendees?.map(email => ({ email })),
        reminders: {
          useDefault: false,
          overrides: [
            { method: 'email', minutes: 24 * 60 }, // 1 day before
            { method: 'popup', minutes: 30 },
          ],
        },
      },
    });

    return { success: true, event: response.data };
  } catch (error) {
    console.error('Calendar error:', error);
    return { success: false, error };
  }
}
```

### 3.6 API Endpoint para Agendar Reunión

**src/pages/api/schedule.ts**
```typescript
import type { APIRoute } from 'astro';
import { z } from 'zod';
import { createCalendarEvent } from '../../utils/googleCalendar';
import { Resend } from 'resend';

const scheduleSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  date: z.string(), // ISO date
  time: z.string(), // HH:mm
  duration: z.number().min(15).max(120), // minutes
  topic: z.string().min(5),
  message: z.string().optional(),
});

const resend = new Resend(import.meta.env.RESEND_API_KEY);

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();
    const data = scheduleSchema.parse(body);

    // Calculate start and end times
    const startDateTime = new Date(`${data.date}T${data.time}`);
    const endDateTime = new Date(startDateTime.getTime() + data.duration * 60000);

    // Create calendar event
    const calendarResult = await createCalendarEvent({
      summary: `Meeting with ${data.name}`,
      description: `
Topic: ${data.topic}

${data.message || ''}

Attendee: ${data.name} (${data.email})
      `.trim(),
      start: startDateTime.toISOString(),
      end: endDateTime.toISOString(),
      attendees: [data.email],
    });

    if (!calendarResult.success) {
      throw new Error('Failed to create calendar event');
    }

    // Send confirmation email
    await resend.emails.send({
      from: import.meta.env.RESEND_FROM_EMAIL,
      to: data.email,
      subject: `Meeting Scheduled: ${data.topic}`,
      html: `
        <h2>Meeting Confirmed ✅</h2>
        <p>Hi ${data.name},</p>
        <p>Your meeting has been scheduled with Darwin Yusef.</p>

        <h3>Details:</h3>
        <ul>
          <li><strong>Topic:</strong> ${data.topic}</li>
          <li><strong>Date:</strong> ${startDateTime.toLocaleDateString()}</li>
          <li><strong>Time:</strong> ${startDateTime.toLocaleTimeString()} - ${endDateTime.toLocaleTimeString()}</li>
          <li><strong>Duration:</strong> ${data.duration} minutes</li>
        </ul>

        <p>A calendar invitation has been sent to your email.</p>

        <p>Looking forward to speaking with you!</p>

        <p>Best regards,<br>Darwin Yusef</p>
      `,
    });

    return new Response(
      JSON.stringify({
        success: true,
        message: 'Meeting scheduled successfully',
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Schedule error:', error);

    return new Response(
      JSON.stringify({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
```

---

## 4. Formulario de Contacto

### 4.1 Componente de Formulario

**src/components/ContactForm.astro**
```astro
---
---

<div class="contact-form-container">
  <form id="contact-form" class="contact-form">
    <div class="form-group">
      <label for="name">Name *</label>
      <input
        type="text"
        id="name"
        name="name"
        required
        minlength="2"
        placeholder="Your name"
      />
    </div>

    <div class="form-group">
      <label for="email">Email *</label>
      <input
        type="email"
        id="email"
        name="email"
        required
        placeholder="your@email.com"
      />
    </div>

    <div class="form-group">
      <label for="phone">Phone</label>
      <input
        type="tel"
        id="phone"
        name="phone"
        placeholder="+1 (555) 123-4567"
      />
    </div>

    <div class="form-group">
      <label for="subject">Subject *</label>
      <input
        type="text"
        id="subject"
        name="subject"
        required
        minlength="3"
        placeholder="What is this about?"
      />
    </div>

    <div class="form-group">
      <label for="message">Message *</label>
      <textarea
        id="message"
        name="message"
        required
        minlength="10"
        rows="5"
        placeholder="Your message..."
      ></textarea>
    </div>

    <button type="submit" class="submit-btn">
      <span class="btn-text">Send Message</span>
      <span class="btn-loader" style="display: none;">Sending...</span>
    </button>

    <div id="form-message" class="form-message" style="display: none;"></div>
  </form>
</div>

<script>
  const form = document.getElementById('contact-form') as HTMLFormElement;
  const message = document.getElementById('form-message') as HTMLDivElement;
  const submitBtn = form.querySelector('.submit-btn') as HTMLButtonElement;
  const btnText = submitBtn.querySelector('.btn-text') as HTMLSpanElement;
  const btnLoader = submitBtn.querySelector('.btn-loader') as HTMLSpanElement;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline';
    message.style.display = 'none';

    // Get form data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (result.success) {
        // Show success message
        message.textContent = '✅ Message sent successfully! I\'ll get back to you soon.';
        message.className = 'form-message success';
        message.style.display = 'block';

        // Reset form
        form.reset();
      } else {
        throw new Error(result.error || 'Failed to send message');
      }
    } catch (error) {
      // Show error message
      message.textContent = '❌ Failed to send message. Please try again or email me directly.';
      message.className = 'form-message error';
      message.style.display = 'block';

      console.error('Form submission error:', error);
    } finally {
      // Reset button state
      submitBtn.disabled = false;
      btnText.style.display = 'inline';
      btnLoader.style.display = 'none';
    }
  });
</script>

<style>
  .contact-form-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
  }

  .contact-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  label {
    font-weight: 600;
    color: #374151;
  }

  input,
  textarea {
    padding: 0.75rem;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
  }

  input:focus,
  textarea:focus {
    outline: none;
    border-color: #667eea;
  }

  .submit-btn {
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s;
  }

  .submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
  }

  .submit-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .form-message {
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
  }

  .form-message.success {
    background: #d1fae5;
    color: #065f46;
  }

  .form-message.error {
    background: #fee2e2;
    color: #991b1b;
  }
</style>
```

### 4.2 Usar en Página

**src/pages/contact.astro**
```astro
---
import ContactForm from '../components/ContactForm.astro';
---

<html>
<head>
  <title>Contact - Darwin Yusef</title>
</head>
<body>
  <h1>Get in Touch</h1>
  <p>Have a project in mind? Let's talk!</p>

  <ContactForm />
</body>
</html>
```

---

## 5. Verificación y Testing

### 5.1 Test Local

```bash
# Asegúrate de tener las variables de entorno
cat .env

# Iniciar servidor de desarrollo
npm run dev

# Visitar: http://localhost:4321/contact
```

### 5.2 Test de Producción

```bash
# Build
npm run build

# Preview
npm run preview

# Test formulario
```

### 5.3 Checklist Final

- [ ] Resend API key configurada
- [ ] Email de origen verificado
- [ ] Email de destino configurado
- [ ] Formulario funciona localmente
- [ ] Emails se envían correctamente
- [ ] Google Calendar configurado (si aplica)
- [ ] Variables de entorno en servidor
- [ ] SSL configurado en dominio

---

**Última actualización:** Enero 2026
