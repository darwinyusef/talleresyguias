# Arquitectura del Proyecto astro-portfolio

## 1. FRAMEWORK Y STACK TECNOLÓGICO

### Core Framework
- **Astro 5.15.9**: Framework estático con prerendering
- **TypeScript**: Para type safety
- **Tailwind CSS 4.1.17**: Utilidades CSS
- **Material Symbols**: Iconos

### Herramientas Adicionales
- **Astro I18Next**: Internacionalización (ES, EN, PT)
- **Marked**: Parser de Markdown
- **Highlight.js**: Syntax highlighting para código
- **Resend**: Para envío de emails (API)

## 2. ESTRUCTURA DE DIRECTORIOS

```
src/
├── pages/                 # Rutas/Páginas
│   ├── index.astro       # Página de inicio
│   ├── blog.astro        # Listado de blog
│   ├── blog/[slug].astro # Detalle de artículo
│   ├── podcast.astro     # Listado de episodios
│   ├── podcast/[slug].astro # Detalle de episodio
│   ├── services.astro
│   ├── skills.astro
│   ├── arquitectura.astro
│   ├── events.astro
│   ├── videos.astro
│   ├── resources.astro
│   ├── api/              # Endpoints API
│   │   ├── ask-ai.json.ts
│   │   ├── chat-assistant.json.ts
│   │   ├── newsletter.json.ts
│   │   ├── send-email.ts
│   │   └── testimonial.json.ts
│   ├── 404.astro
│   └── terms-of-use.md
│
├── components/           # Componentes reutilizables
│   ├── Header.astro
│   ├── Footer.astro
│   ├── Chatbot.astro
│   ├── CookieConsent.astro
│   ├── Newsletter.astro
│   ├── SkillsRadar.astro
│   ├── SkillsSection.astro
│   ├── Testimonials.astro
│   ├── GalleryMasonry.astro
│   ├── HomeEventos.astro
│   ├── UpcomingEvents.astro
│   └── ...
│
├── layouts/             # Layouts base
│   ├── Layout.astro     # Layout principal con accesibilidad
│   └── ArticleLayout.astro
│
├── content/             # Content Collections (CMS-like)
│   ├── config.ts        # Esquemas Zod
│   ├── podcasts/        # Episodios en Markdown
│   │   ├── ia-generativa-2025.md
│   │   ├── typescript-avanzado.md
│   │   ├── devops-kubernetes.md
│   │   └── ... (8+ episodios)
│   └── services/        # Servicios
│       └── web-development.md
│
├── i18n/                # Internacionalización
│   ├── utils.ts         # Helper functions
│   └── locales/
│       ├── es.json      # Español
│       ├── en.json      # English
│       └── pt.json      # Português
│
├── styles/
│   └── global.css       # Estilos globales
│
├── lib/
│   └── icons.ts         # Utilidades de iconos
│
└── config/
    └── github.ts        # Configuración externa
```

## 3. SISTEMA DE ENRUTAMIENTO

### Rutas Principales
```
/ (es), /en, /pt                    - Página de inicio
/blog                                - Listado de artículos
/blog/[slug]                         - Artículo individual
/podcast                             - Listado de episodios
/podcast/[slug]                      - Episodio individual
/services                            - Servicios
/skills                              - Habilidades
/arquitectura                        - Oficina de arquitectura
/events                              - Eventos
/videos                              - Videos
/resources                           - Recursos
/testimonial-form                    - Formulario de testimonios
/privacy-policy, /terms-of-use       - Legales
```

### Patrones i18n
- Default: Español (sin prefijo) → `/blog`
- English: Prefijo `/en` → `/en/blog`
- Portuguese: Prefijo `/pt` → `/pt/blog`

## 4. NAVEGACIÓN

### Header Component
- Navegación principal con enlaces a todas las secciones
- Selector de idioma (banderas)
- Menú responsive para mobile
- Custom cursor follower effect

### Secciones Enlazadas
- Home (con scroll a #about)
- Podcast
- Blog
- Arquitectura
- Events
- Videos
- Skills
- Resources
- Contact (scroll a #contact)

## 5. SISTEMA DE CONTENIDO (Content Collections)

### Esquemas Definidos (src/content/config.ts)

#### Posts
```typescript
{
  type: 'content',
  title: string
  description: string
  pubDate: date
  author: string (default: 'Admin')
  image?: string
  tags: string[]
  is_active: boolean (default: true)
}
```

#### Podcasts
```typescript
{
  type: 'content',
  title: string
  description: string
  pubDate: date
  duration: string (ej: "38:45")
  audioUrl: string
  coverImage?: string
  tags: string[]
  is_active: boolean (default: true)
}
```

#### Services
```typescript
{
  type: 'content',
  name: string
  description: string
  price?: number
  duration?: string
  is_active: boolean
  features?: string[]
  icon?: string
  order: number
}
```

#### Skills
```typescript
{
  type: 'data',
  name: string
  category: string
  proficiency: 1-100
  description?: string
  icon?: string
  is_active: boolean
  order: number
}
```

## 6. FLUJO DE DATOS

### Blog (Doble fuente)
1. **Fuente local**: `/src/content/posts/` (no encontrado en exploración)
2. **Fuente remota**: GitHub Raw URL
   - URL: `https://raw.githubusercontent.com/darwinyusef/darwinyusef/refs/heads/master/information/blog.json`
   - Se carga dinámicamente en cliente con fetch
   - Renderizado en grid 3 columnas con filtros de categoría

### Podcast (Local)
1. **Fuente**: `/src/content/podcasts/` (archivos Markdown)
2. **Datos**: Frontmatter YAML con audioUrl y metadata
3. **Renderizado**: 
   - Episodio destacado
   - Grid de episodios restantes
   - Reproductor audio personalizado

### Servicios (Local)
1. **Fuente**: `/src/content/services/`
2. **Datos**: Markdown con descripción

### Skills (Local)
1. **Fuente**: Data files
2. **Visualización**: Radar chart interactivo

## 7. COMPONENTES CLAVE

### Header.astro
- Navegación sticky con i18n
- Logo animado con gradiente
- Selector de idioma
- Menú mobile responsivo
- Cursor custom hover targets

### Layout.astro (Principal)
- Meta tags y SEO
- Dark mode forzado
- Accesibilidad:
  - Control de tamaño de texto (80-150%)
  - Alto contraste
  - Reducir movimiento
  - Espaciado de líneas
  - Cursor agrandado
  - LocalStorage para preferencias
- Cursor follower global effect
- Footer y CookieConsent

## 8. REPRODUCCIÓN DE AUDIO

### Podcast Page (podcast.astro)
- Reproductor HTML5 personalizado
- Controles:
  - Play/Pause
  - Retroceder/Adelantar 10s
  - Control de velocidad (0.5x - 2x)
  - Control de volumen
  - Indicador de progreso clickeable
- Almacenamiento de progreso en localStorage
- Atajos de teclado:
  - Space: Play/Pause
  - Arrow Left/Right: Saltar 5s

### Bottom Player (podcast.astro)
- Reproductor flotante en bottom
- Muestra título del episodio en reproducción
- Control básico play/pause/close
- Sincronizado con episodios

## 9. API ENDPOINTS

```
/api/ask-ai.json.ts          - IA asistente
/api/chat-assistant.json.ts  - Chat interactivo
/api/newsletter.json.ts      - Suscripción newsletter
/api/send-email.ts           - Envío de emails (Resend)
/api/testimonial.json.ts     - Guardado de testimonios
```

## 10. INTERNACIONALIZACIÓN (i18n)

### Sistema Basado en Archivos JSON

**Locales Soportados**:
- ES: Español (default)
- EN: English
- PT: Português

**Estructura de Traducciones**:
```json
{
  "nav": { home, about, skills, services, podcast, contact },
  "home": { title, subtitle, downloadCV, aboutMe, contactMe, letConnect },
  "skills": { title, techStack },
  "podcast": { title, episodes, duration, listen },
  "chatbot": { title, placeholder, send, close },
  "newsletter": { title, placeholder, subscribe, success },
  "contact": { email, message, send },
  "footer": { rights }
}
```

**Uso**:
```typescript
const lang = getLangFromUrl(Astro.url);
const t = useTranslations(lang);
// Uso: {t("nav.home")}
```

## 11. STYLING

### Tecnologías
- **Tailwind CSS 4.1.17**: Utility-first CSS
- **Gradientes**: Primary → Purple → Pink
- **Dark Mode**: Forzado con clase `dark`
- **Custom Properties**: CSS variables para colores

### Temas Visuales
- Fondo oscuro: `#0a0a0a` (bg-[#0a0a0a])
- Cards oscuras: `#1a1a1a` (bg-[#1a1a1a])
- Gradientes: `primary` → `purple-600` → `pink-600`
- Efectos: Blur, sombras, transiciones suaves

## 12. REPRODUCCIÓN ESTÁTICA vs DINÁMICO

### Páginas Renderizadas Estáticamente (getStaticPaths)
- `/blog/[slug]` - Episodios desde GitHub JSON
- `/podcast/[slug]` - Episodios desde content collection

### Páginas Dinámicas en Cliente
- `/blog` - Carga dinámica de blog.json con filtros
- `/podcast` - Renderizado desde content collection

### APIs Dinámicas (Server-side)
- `/api/*` - Endpoints funcionales

## 13. CARACTERÍSTICAS ESPECIALES

### Parallax Scroll Effects
- Data-speed attributes en elementos
- Update en scroll con requestAnimationFrame
- Suavizado con will-change

### Cursor Personalizado
- Cursor follower global
- Hover targets con textos personalizados
- Data attributes para textos de hover

### Reproducción con Progreso Persistente
- localStorage para guardar posición
- LocalStorage key: `podcast-time-{slug}`
- Se restaura al recargar

### Accesibilidad WCAG
- Modal de opciones de accesibilidad
- Contraste ajustable
- Animaciones reducibles
- Tamaño de fuente aumentable
- Preferencias guardadas

## 14. CONFIGURACIÓN ASTRO

```typescript
export default defineConfig({
  output: 'static',
  prerender: true,
  
  integrations: [mdx()],
  
  i18n: {
    defaultLocale: 'es',
    locales: ['es', 'en', 'pt'],
    routing: {
      prefixDefaultLocale: false
    }
  },
  
  vite: {
    plugins: [tailwindcss()]
  }
});
```

## RESUMEN ARQUITECTÓNICO

El proyecto es una **aplicación Astro estática con SSG (Static Site Generation)** que:

1. Genera HTML estático en build time
2. Mantiene interactividad con JavaScript mínimo (client-side)
3. Soporta 3 idiomas con rutas prefijadas
4. Gestiona contenido mediante:
   - Content Collections para podcast/servicios/skills
   - Fetch remoto para blog (desde GitHub)
5. Proporciona UX avanzada con:
   - Reproducción de audio persistente
   - Accesibilidad completa (WCAG)
   - Efectos visuales (parallax, cursor custom)
6. APIs para:
   - Chat/IA
   - Newsletter
   - Emails (Resend)
   - Testimonios

## PUNTOS DE INTEGRACIÓN PARA NUEVO MÓDULO

Para integrar un nuevo módulo (Blog/Podcast mejorado):

1. **Nueva ruta**: Agregar en `/src/pages/nueva-ruta.astro`
2. **Componentes**: En `/src/components/`
3. **Contenido**: En `/src/content/nueva-coleccion/`
4. **Esquema**: Definir en `/src/content/config.ts`
5. **I18n**: Agregar en `/src/i18n/locales/[lang].json`
6. **Navegación**: Actualizar Header.astro
7. **Estilos**: Usar Tailwind siguiendo patrones existentes
8. **API**: Si necesita, en `/src/pages/api/`

