================================================================================
RESUMEN EJECUTIVO - ARQUITECTURA DEL PROYECTO astro-portfolio
================================================================================

UBICACIÓN DEL PROYECTO:
  /Users/yusefgonzalez/proyectos/portfolio/astro-portfolio

FRAMEWORK Y TECNOLOGÍAS PRINCIPALES:
  - Astro 5.15.9 (SSG - Static Site Generation)
  - TypeScript
  - Tailwind CSS 4.1.17
  - Internacionalización (ES, EN, PT)
  - Material Symbols Icons

================================================================================
1. ESTRUCTURA GENERAL DEL PROYECTO
================================================================================

DIRECTORIOS PRINCIPALES:

/src/pages/
  - Rutas de la aplicación (páginas .astro)
  - Subdirectorio /api/ para endpoints REST
  - Rutas dinámicas: [slug].astro

/src/components/
  - Componentes reutilizables (Header, Footer, etc)
  - Componentes para blog, podcast, skills
  - Modales y elementos interactivos

/src/content/
  - Content Collections (Astro)
  - Archivos de contenido: podcasts, servicios, skills
  - Esquemas de validación (Zod)

/src/i18n/
  - Sistema de internacionalización
  - Archivos JSON para ES, EN, PT
  - Utilities para detección de idioma

/src/layouts/
  - Layout.astro - Layout principal con accesibilidad
  - ArticleLayout.astro

/src/styles/
  - CSS global
  - Tailwind config

CONFIGURACIÓN:
  - astro.config.mjs - Configuración de Astro
  - package.json - Dependencias y scripts
  - tsconfig.json - Configuración TypeScript
  - tailwind.config.ts - Tailwind CSS config

================================================================================
2. SISTEMA DE RUTAS Y NAVEGACIÓN
================================================================================

RUTAS PRINCIPALES:

Raíz:
  / (inicio)
  /es (inicio español - sin prefijo por defecto)
  /en (inicio inglés)
  /pt (inicio portugués)

Blog:
  /blog (listado)
  /blog/[slug] (detalle de artículo)
  /en/blog, /pt/blog (internacionalización)

Podcast:
  /podcast (listado)
  /podcast/[slug] (detalle de episodio)
  /en/podcast, /pt/podcast

Otras páginas:
  /services (servicios)
  /skills (habilidades)
  /arquitectura (oficina de arquitectura)
  /events (eventos)
  /videos (videos)
  /resources (recursos)
  /testimonial-form (formulario de testimonios)

NAVEGACIÓN:
  Header.astro contiene navegación principal
  - Enlaces a todas las secciones
  - Selector de idioma (flags)
  - Menú responsive para mobile
  - Custom cursor follower effect

================================================================================
3. MÓDULOS DE BLOG Y PODCAST (EXISTENTES)
================================================================================

BLOG - ESTADO: HÍBRIDO (Remoto)
  Origen de datos: GitHub Raw URL
  URL: https://raw.githubusercontent.com/darwinyusef/darwinyusef/...
  Archivo: blog.json (array de posts)

  Características:
  - Carga dinámica en cliente (fetch en runtime)
  - Filtros por categoría
  - Grid 3 columnas responsive
  - Búsqueda integrada

  Estructura de datos:
  {
    id: number,
    title: string,
    slug: string,
    excerpt: string,
    content: string (HTML),
    category: string,
    tags: string[],
    author: string,
    coverImage: string (URL),
    publishDate: date,
    readTime: string,
    is_active: boolean
  }

PODCAST - ESTADO: LOCAL (Content Collections)
  Origen de datos: /src/content/podcasts/*.md
  Formato: Markdown con YAML frontmatter

  Características:
  - 8+ episodios locales
  - Reproductor audio HTML5 personalizado
  - Controles: play/pause, skip, speed, volumen
  - Almacenamiento de progreso en localStorage
  - Episodio destacado + grid de otros
  - Atajos de teclado

  Estructura de datos:
  ---
  title: string
  description: string
  pubDate: date
  duration: string (HH:MM)
  audioUrl: string (URL a mp3)
  coverImage: string (URL opcional)
  tags: string[]
  is_active: boolean
  ---
  ## Contenido markdown

================================================================================
4. COMPONENTES DE NAVEGACIÓN EXISTENTES
================================================================================

Header.astro:
  - Navegación sticky (fixed top)
  - Logo "@DARWINYUSEF" con gradiente
  - Enlaces desktop: Home, Podcast, Blog, Arquitectura, Events, Videos, Skills, Resources, Contact
  - Selector de idioma (banderas)
  - Menú mobile responsive
  - Custom hover cursor targets

Footer.astro:
  - Enlaces a redes sociales
  - Copyright
  - Links footer

Componentes Interactivos:
  - CookieConsent.astro - Modal de cookies
  - Chatbot.astro - Asistente IA
  - Newsletter.astro - Suscripción
  - HomeEventos.astro - Eventos en home
  - Testimonials.astro - Testimonios

================================================================================
5. ESTRUCTURA DE DATOS Y CONTENIDO
================================================================================

CONTENT COLLECTIONS (src/content/config.ts):

1. Podcasts
   Localización: /src/content/podcasts/
   Esquema Zod: type, title, description, pubDate, duration, audioUrl, 
                coverImage, tags, is_active
   Instancias: ia-generativa-2025.md, typescript-avanzado.md, etc

2. Services
   Localización: /src/content/services/
   Esquema Zod: type, name, description, price, duration, is_active, 
                features, icon, order
   Instancias: web-development.md

3. Skills
   Localización: /src/content/skills/
   Esquema Zod: type (data), name, category, proficiency, description, 
                icon, is_active, order

4. Posts (potencial)
   No encontrado localmente (blog viene de GitHub)
   Esquema podría ser: title, description, pubDate, author, image, 
                       tags, is_active

INTERNACIONALIZACIÓN:

Sistema: JSON-based key-value translations
Archivos:
  /src/i18n/locales/es.json (español - default)
  /src/i18n/locales/en.json (inglés)
  /src/i18n/locales/pt.json (portugués)

Estructura:
{
  "nav": { "home", "about", "skills", "services", "podcast", "contact" },
  "home": { "title", "subtitle", "downloadCV", "aboutMe", "contactMe" },
  "podcast": { "title", "episodes", "duration", "listen" },
  ... más secciones
}

Uso:
  const lang = getLangFromUrl(Astro.url);
  const t = useTranslations(lang);
  {t('nav.home')} // "Inicio" en ES, "Home" en EN, "Início" en PT

================================================================================
6. APIs Y ENDPOINTS
================================================================================

Endpoints disponibles:

/api/ask-ai.json.ts
  - Asistente IA para preguntas
  - POST request

/api/chat-assistant.json.ts
  - Chat interactivo con IA
  - Conversaciones

/api/newsletter.json.ts
  - Suscripción a newsletter
  - Almacenamiento de emails

/api/send-email.ts
  - Envío de emails con Resend
  - Contacto, notificaciones

/api/testimonial.json.ts
  - Guardado de testimonios
  - Formulario testimonios

================================================================================
7. CARACTERÍSTICAS ESPECIALES
================================================================================

REPRODUCCIÓN DE AUDIO (Podcast):
  - Reproductor HTML5 personalizado
  - Progress bar con seek
  - Play/pause, skip ±10s
  - Control de volumen
  - Selector de velocidad (0.5x - 2x)
  - Atajos de teclado
  - Almacenamiento de progreso en localStorage
  - Sincronización con episodios

ACCESIBILIDAD (WCAG):
  - Modal de opciones en Layout.astro
  - Control de tamaño de texto (80-150%)
  - Alto contraste ajustable
  - Opción reducir movimiento
  - Espaciado de líneas aumentable
  - Cursor agrandable
  - Preferencias guardadas en localStorage
  - Botón en esquina inferior derecha

EFECTOS VISUALES:
  - Parallax scroll effects (data-speed attributes)
  - Cursor follower custom
  - Hover targets con textos personalizados
  - Gradientes: primary → purple → pink
  - Transiciones suaves
  - Dark mode forzado

================================================================================
8. FLUJOS DE TRABAJO
================================================================================

BLOG WORKFLOW:
  1. Datos desde GitHub (blog.json)
  2. Fetch en cliente (runtime)
  3. Filtrado por categoría
  4. Renderizado en grid
  5. Click → Ruta dinámica /blog/[slug]
  6. getStaticPaths() genera HTML estático

PODCAST WORKFLOW:
  1. Archivos MD en /src/content/podcasts/
  2. getCollection() en build time
  3. Sort y renderizado en grid
  4. Play button → JS playPodcast()
  5. Audio player flotante
  6. localStorage para progreso
  7. Click → Ruta dinámica /podcast/[slug]

================================================================================
9. PUNTOS DE INTEGRACIÓN PARA NUEVOS MÓDULOS
================================================================================

Para agregar un nuevo módulo similar (Blog/Podcast mejorado):

PASO 1: Definir esquema
  /src/content/config.ts
  - Agregar nuevo defineCollection

PASO 2: Crear contenido
  /src/content/nueva-coleccion/*.md
  - Archivos con frontmatter YAML

PASO 3: Crear página listado
  /src/pages/nueva-ruta.astro
  - Usar getCollection()
  - Renderizar grid

PASO 4: Crear página detalle
  /src/pages/nueva-ruta/[slug].astro
  - Usar getStaticPaths()
  - Renderizar detalle

PASO 5: Agregar navegación
  /src/components/Header.astro
  - Agregar enlace en nav

PASO 6: Agregar traducciones
  /src/i18n/locales/*.json
  - Agregar claves para i18n

PASO 7: Estilos
  Usar Tailwind CSS siguiendo patrones
  Dark mode + gradientes

================================================================================
10. HERRAMIENTAS Y TECNOLOGÍAS
================================================================================

Frontend Stack:
  - Astro 5.15.9 (SSG)
  - TypeScript
  - Tailwind CSS 4.1.17
  - Material Symbols Icons
  - Marked (markdown parser)
  - Highlight.js (syntax highlighting)

APIs y Servicios Externos:
  - Resend (envío de emails)
  - GitHub Raw Content (blog.json)
  - Audio URLs (S3, CDN, etc)

Storage:
  - localStorage (progreso podcast, preferencias accesibilidad)
  - sessionStorage (datos temporales)

Build:
  - npm run dev (desarrollo)
  - npm run build (build estático)
  - npm run preview (preview local)

================================================================================
11. CONFIGURACIÓN IMPORTANTE
================================================================================

astro.config.mjs:
  - output: 'static' (SSG)
  - prerender: true (pre-renderización)
  - i18n: ES (default), EN, PT
  - routing: prefixDefaultLocale: false (no prefijo para ES)
  - Integración: MDX para markdown

Tailwind:
  - Dark mode forzado
  - Colores: primary, purple-600, pink-600
  - Utility-first approach

Environment:
  - .env para variables sensibles (Resend API key, GitHub URLs, etc)

================================================================================
12. ARCHIVOS GENERADOS
================================================================================

Se han creado 3 documentos de referencia en:

  /Users/yusefgonzalez/proyectos/portfolio/
  
  ├─ ARCHITECTURE_SUMMARY.md (11 KB)
  │  Resumen detallado de arquitectura
  │
  ├─ INTEGRATION_GUIDE.md (13 KB)
  │  Guía paso a paso para integración
  │
  └─ ARCHITECTURE_DIAGRAM.md
     Diagramas ASCII de flujos y estructuras

================================================================================
CONCLUSIÓN
================================================================================

El proyecto astro-portfolio es una aplicación web estática moderna con:

1. Framework: Astro (SSG) para máximo rendimiento
2. Contenido: Híbrido (local + remoto)
3. Módulos existentes: Blog (GitHub JSON) + Podcast (Content Collections)
4. Internacionalización: Trilingüe ES/EN/PT
5. Accesibilidad: WCAG completo
6. UX avanzada: Audio player, parallax, cursor custom
7. Escalabilidad: Structure lista para agregar nuevos módulos
8. Performance: Pre-renderización HTML estático + JS mínimo

La arquitectura es modular y extensible, permitiendo integrar
nuevos módulos de contenido de forma sencilla siguiendo los patrones
existentes.

================================================================================
