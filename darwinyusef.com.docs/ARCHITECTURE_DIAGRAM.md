# DIAGRAMA DE ARQUITECTURA - astro-portfolio

## FLUJO GENERAL DE LA APLICACIÓN

```
┌─────────────────────────────────────────────────────────────────┐
│                       CLIENTE (BROWSER)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    ASTRO (Static)                        │  │
│  │  - Renderizado en Build Time                            │  │
│  │  - Output: HTML/CSS/JS estático                         │  │
│  │  - SSG (Static Site Generation)                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              JAVASCRIPT DEL CLIENTE                      │  │
│  │  ┌────────────────────────────────────────────────────┐ │  │
│  │  │ 1. Interactividad                                  │ │  │
│  │  │    - Play/Pause de audio                           │ │  │
│  │  │    - Filtros de blog                               │ │  │
│  │  │    - Modales de accesibilidad                       │ │  │
│  │  ├────────────────────────────────────────────────────┤ │  │
│  │  │ 2. Fetch de Datos Remotos                          │ │  │
│  │  │    - blog.json desde GitHub                        │ │  │
│  │  │    - Renderizado dinámico en grid                  │ │  │
│  │  ├────────────────────────────────────────────────────┤ │  │
│  │  │ 3. localStorage                                    │ │  │
│  │  │    - Progreso de podcast                           │ │  │
│  │  │    - Preferencias de accesibilidad                 │ │  │
│  │  ├────────────────────────────────────────────────────┤ │  │
│  │  │ 4. Efectos Visuales                                │ │  │
│  │  │    - Parallax scroll                               │ │  │
│  │  │    - Cursor follower                               │ │  │
│  │  │    - Transiciones                                  │ │  │
│  │  └────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVIDOR (APIs)                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           /api/ask-ai.json.ts                           │  │
│  │           /api/chat-assistant.json.ts                   │  │
│  │           /api/newsletter.json.ts                       │  │
│  │           /api/send-email.ts (Resend)                   │  │
│  │           /api/testimonial.json.ts                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FUENTES DE DATOS EXTERNAS                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────┐       ┌──────────────────────────┐ │
│  │  GitHub Raw Content    │       │  Resend (Email API)      │ │
│  │  - blog.json           │       │  - Envío de emails       │ │
│  │  - Fetch en runtime    │       │  - Newsletter            │ │
│  └────────────────────────┘       │  - Contacto              │ │
│                                   └──────────────────────────┘ │
│  ┌────────────────────────┐       ┌──────────────────────────┐ │
│  │  Content Collections   │       │  Audio URLs (Podcast)    │ │
│  │  - Podcast (MD local)  │       │  - Almacenamiento S3     │ │
│  │  - Services (MD local) │       │  - CDN                   │ │
│  │  - Skills (JSON local) │       │  - URLs directas         │ │
│  └────────────────────────┘       └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## ESTRUCTURA DE RUTAS Y PÁGINAS

```
                           ROOT
                            │
        ┌───────────────────┼───────────────────┬─────────────────┐
        │                   │                   │                 │
       /                   /blog               /podcast          /services
    index.astro        blog.astro         podcast.astro      services.astro
    (Inicio)         (Listado)           (Listado)          (Servicios)
        │                │                    │                  │
        │                ▼                    ▼                  │
        │           [slug].astro        [slug].astro            │
        │        (Detalle artículo)   (Detalle episodio)        │
        │                │                    │                  │
        │                └────────┬───────────┘                  │
        │                         │                              │
        └──────────────────┬──────┴──────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┬─────────┐
        │                  │                  │         │
     /skills            /events            /videos   /arquitectura
   skills.astro      events.astro      videos.astro  arquitectura.astro
  (Habilidades)      (Eventos)         (Videos)      (Arquitectura)


i18n ROUTING:
─────────────

  /blog              ──(ES default, sin prefijo)
  /en/blog           ──(EN)
  /pt/blog           ──(PT)

  /podcast           ──(ES)
  /en/podcast        ──(EN)
  /pt/podcast        ──(PT)
```

---

## FLUJO DE DATOS - BLOG

```
┌─────────────────────────────────────────────────────────────────┐
│ FUENTE REMOTA: GitHub Raw URL                                  │
│ blog.json con array de posts                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Fetch (runtime)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ blog.astro - Página Listado                                     │
│                                                                 │
│  1. JavaScript del cliente hace fetch                           │
│  2. Mapea respuesta a interface Post                            │
│  3. Filtra por is_active                                        │
│  4. Crea botones de categoría                                   │
│  5. Renderiza en grid 3 columnas                                │
│  6. Implementa filtros por categoría                            │
│                                                                 │
│  Estructura Post:                                               │
│  ├─ id, slug, title, description                               │
│  ├─ excerpt, content (HTML)                                    │
│  ├─ category, tags, author                                     │
│  ├─ coverImage, publishDate, readTime                          │
│  └─ is_active (boolean)                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Clic en artículo
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ blog/[slug].astro - Página Detalle                              │
│                                                                 │
│  1. getStaticPaths() - Genera rutas en build time              │
│     └─ Fetch blog.json                                          │
│     └─ Map a paths dinámicas                                    │
│                                                                 │
│  2. Renderiza post completo                                     │
│     ├─ Hero con cover image                                     │
│     ├─ Metadata (autor, fecha, lectura)                         │
│     ├─ Contenido HTML (set:html)                                │
│     ├─ Botones share (Twitter, LinkedIn, Copy)                  │
│     └─ Navegación de vuelta                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## FLUJO DE DATOS - PODCAST

```
┌─────────────────────────────────────────────────────────────────┐
│ FUENTES LOCALES: /src/content/podcasts/*.md                    │
│                                                                 │
│ Estructura:                                                     │
│  ---                                                            │
│  title: string                                                  │
│  description: string                                            │
│  pubDate: date                                                  │
│  duration: "HH:MM"                                              │
│  audioUrl: string (URL a mp3)                                   │
│  coverImage: string (URL a imagen)                              │
│  tags: string[]                                                 │
│  is_active: boolean                                             │
│  ---                                                            │
│  ## Contenido markdown                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ getCollection()
                              │ (Build time)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ podcast.astro - Página Listado                                  │
│                                                                 │
│  1. getCollection('podcasts') con filtro is_active             │
│  2. Sort descendente por pubDate                                │
│                                                                 │
│  Renderizado:                                                   │
│  ├─ HERO SECTION (con parallax)                                 │
│  │                                                              │
│  ├─ EPISODIO DESTACADO (más reciente)                          │
│  │  ├─ Cover image con gradient overlay                        │
│  │  ├─ Play button overlay                                      │
│  │  ├─ Texto title, description                                │
│  │  └─ Botón "Ver Episodio Completo"                           │
│  │                                                              │
│  ├─ SEPARADOR                                                   │
│  │                                                              │
│  ├─ GRID DE EPISODIOS (resto)                                  │
│  │  └─ 3 columnas (lg), 2 (md), 1 (sm)                         │
│  │     ├─ Cover + metadata                                      │
│  │     ├─ Play button hover                                     │
│  │     ├─ Title + date                                          │
│  │     └─ Botón "Escuchar"                                      │
│  │                                                              │
│  └─ AUDIO PLAYER FLOTANTE (bottom)                             │
│     └─ Se muestra cuando plays() es llamado                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Clic en play
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ JavaScript - Audio Player Handler                               │
│                                                                 │
│  playPodcast(audioUrl, title):                                 │
│  ├─ Si es mismo audio → toggle play/pause                      │
│  └─ Si es audio diferente → cargar nuevo                       │
│     ├─ audioElement.src = audioUrl                              │
│     ├─ currentTitle.textContent = title                         │
│     ├─ audioElement.play()                                      │
│     └─ audioPlayer.classList.remove('hidden')                   │
│                                                                 │
│  LISTENERS:                                                     │
│  ├─ play/pause buttons                                          │
│  ├─ progress bar seek                                           │
│  ├─ volume control                                              │
│  ├─ playback speed                                              │
│  ├─ skip 10s forward/backward                                   │
│  └─ keyboard shortcuts (Space, ◀▶)                              │
│                                                                 │
│  STORAGE:                                                       │
│  └─ localStorage[`podcast-time-${slug}`]                        │
│     ├─ Guarda en timeupdate                                     │
│     └─ Restaura en load                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Clic en episodio / Ver Completo
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ podcast/[slug].astro - Página Detalle                           │
│                                                                 │
│  1. getStaticPaths() - Genera rutas                             │
│     └─ getCollection('podcasts')                                │
│     └─ Map a paths con params { slug }                          │
│                                                                 │
│  2. Renderiza:                                                  │
│     ├─ Hero image con overlay                                   │
│     ├─ Title card con metadata                                  │
│     │  ├─ Título, descripción                                  │
│     │  ├─ Duration, fecha, tags                                 │
│     │  └─ Autor icon                                            │
│     │                                                           │
│     ├─ AUDIO PLAYER PERSONALIZADO                              │
│     │  ├─ Progress bar con seek                                │
│     │  ├─ Play/pause + skip ±10s                               │
│     │  ├─ Playback speed selector                              │
│     │  ├─ Volume control con slider                            │
│     │  ├─ Time display (current/total)                         │
│     │  └─ Keyboard shortcuts                                    │
│     │                                                           │
│     ├─ NOTAS DEL EPISODIO                                       │
│     │  └─ Content renderizado desde markdown                    │
│     │                                                           │
│     ├─ SHARE BUTTONS                                            │
│     │  ├─ Twitter (intent/tweet)                                │
│     │  ├─ LinkedIn (share-offsite)                              │
│     │  └─ Copy link (navigator.clipboard)                       │
│     │                                                           │
│     └─ NAVIGATION BACK                                          │
│        └─ "Ver todos los episodios"                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## FLUJO DE INTERNACIONALIZACIÓN

```
┌─────────────────────────────────────────────────────────────────┐
│ URL ENTRADA                                                     │
│  /blog          ── Detecta ES (default)                         │
│  /en/blog       ── Detecta EN                                   │
│  /pt/blog       ── Detecta PT                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ i18n/utils.ts - getLangFromUrl(url)                            │
│                                                                 │
│  const [, lang] = url.pathname.split('/');                     │
│  if (lang in ui) return lang as keyof typeof ui;               │
│  return defaultLang; // 'es'                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ i18n/locales/[lang].json                                        │
│                                                                 │
│  es.json:                                                       │
│  { "nav": { "home": "Inicio", ... }, ... }                     │
│                                                                 │
│  en.json:                                                       │
│  { "nav": { "home": "Home", ... }, ... }                       │
│                                                                 │
│  pt.json:                                                       │
│  { "nav": { "home": "Início", ... }, ... }                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ useTranslations(lang)                                           │
│                                                                 │
│  return function t(key: string) {                              │
│    const keys = key.split('.');                                │
│    let value = ui[lang];                                        │
│    for (const k of keys) {                                      │
│      value = value?.[k];                                        │
│    }                                                            │
│    return value || key;                                         │
│  }                                                              │
│                                                                 │
│  USO:                                                           │
│  {t('nav.blog')}  ── 'Blog' o 'Blog' o 'Blog'                  │
│  {t('nav.home')}  ── 'Inicio' o 'Home' o 'Início'              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ RENDERIZADO EN COMPONENTE                                       │
│                                                                 │
│  <a href={`${lang === "es" ? "" : lang + "/"}blog`}>          │
│    {t('nav.blog')}  ← Traducción cargada                       │
│  </a>                                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## FLUJO DE ACCESIBILIDAD

```
┌─────────────────────────────────────────────────────────────────┐
│ USUARIO HACE CLIC EN BOTÓN ACCESIBILIDAD                       │
│ (esquina inferior derecha)                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Modal de Accesibilidad (Layout.astro)                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ OPCIONES DISPONIBLES:                                   │   │
│  │ ├─ Tamaño de Texto (80% - 150%)                         │   │
│  │ ├─ Alto Contraste (toggle)                              │   │
│  │ ├─ Reducir Movimiento (toggle)                          │   │
│  │ ├─ Espaciado de Líneas (toggle)                         │   │
│  │ └─ Cursor Grande (toggle)                               │   │
│  │                                                          │   │
│  │ BOTONES:                                                │   │
│  │ ├─ Guardar Preferencias                                 │   │
│  │ └─ Restablecer                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ JavaScript - initAccessibilityModal()                           │
│                                                                 │
│  LOAD PREFERENCES:                                              │
│  ├─ localStorage.getItem('accessibility-preferences')           │
│  └─ Restaura valores guardados                                  │
│                                                                 │
│  APPLY PREFERENCES:                                             │
│  ├─ font-size: ${textSize}%                                     │
│  ├─ document.documentElement.classList.add('high-contrast')     │
│  ├─ document.documentElement.classList.add('reduce-motion')     │
│  ├─ document.documentElement.classList.add('increased-line-*')  │
│  └─ document.documentElement.classList.add('large-cursor')      │
│                                                                 │
│  SAVE PREFERENCES:                                              │
│  └─ localStorage.setItem('accessibility-preferences', JSON)     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ CSS GLOBAL (Layout.astro styles)                               │
│                                                                 │
│  .high-contrast {                                               │
│    filter: contrast(1.5);                                       │
│  }                                                              │
│                                                                 │
│  .reduce-motion * {                                             │
│    animation-duration: 0.01ms !important;                       │
│    transition-duration: 0.01ms !important;                      │
│  }                                                              │
│                                                                 │
│  .increased-line-height * {                                     │
│    line-height: 2 !important;                                   │
│  }                                                              │
│                                                                 │
│  .large-cursor {                                                │
│    cursor: url('data:image/svg+xml;...') 2 2, auto;             │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ RESULTADO: PÁGINA CON ESTILOS ADAPTADOS                        │
│                                                                 │
│ ├─ Texto más grande/pequeño                                    │
│ ├─ Contraste aumentado                                          │
│ ├─ Sin animaciones (si está activo)                             │
│ ├─ Espaciado entre líneas aumentado                             │
│ └─ Cursor más visible                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## STACK TÉCNICO POR CAPA

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                         │
├─────────────────────────────────────────────────────────────────┤
│  Framework:        Astro 5.15.9                                 │
│  Lenguaje:         TypeScript                                   │
│  Estilos:          Tailwind CSS 4.1.17                          │
│  Iconos:           Material Symbols                             │
│  Markdown:         MDX (@astrojs/mdx)                           │
│  Componentes:      .astro                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE LÓGICA (CLIENT)                      │
├─────────────────────────────────────────────────────────────────┤
│  JavaScript:       TypeScript compilado                         │
│  Librerías:        highlight.js (sintaxis)                      │
│  Storage:          localStorage API                             │
│  Network:          Fetch API                                    │
│  Audio:            HTML5 Audio API                              │
│  Clipboard:        navigator.clipboard API                      │
│  Animation:        requestAnimationFrame                        │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE CONTENIDO                            │
├─────────────────────────────────────────────────────────────────┤
│  Content Collections:      Astro Content Layer                  │
│  Schema Validation:        Zod                                  │
│  Formatos:                 Markdown, YAML, JSON                 │
│  Fuentes:                  Local (MD), Remoto (GitHub JSON)     │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE INTERNACIONALIZACIÓN                 │
├─────────────────────────────────────────────────────────────────┤
│  Sistema:          astro-i18next                                │
│  Archivos:         Locales JSON                                 │
│  Lenguajes:        ES (default), EN, PT                         │
│  Routing:          Prefixed (except default)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE APIS                                 │
├─────────────────────────────────────────────────────────────────┤
│  Framework:        Astro API Routes                             │
│  Lenguaje:         TypeScript                                   │
│  Servicios:        Resend (email)                               │
│  Endpoints:        /api/*.ts                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS EXTERNOS                       │
├─────────────────────────────────────────────────────────────────┤
│  GitHub:           blog.json (raw content)                      │
│  Audio:            URLs directas (S3, CDN)                      │
│  Imagenes:         URLs directas (Unsplash, etc)                │
│  Email:            Resend API                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## CICLO DE VIDA DE COMPILACIÓN

```
1. DESARROLLO
   ├─ npm run dev
   ├─ Inicia servidor local (localhost:3000)
   ├─ Hot reload con astro:page-load
   └─ Watch de cambios

2. BUILD
   ├─ npm run build
   ├─ Astro procesa:
   │  ├─ Archivos .astro
   │  ├─ Content Collections
   │  ├─ Rutas dinámicas (getStaticPaths)
   │  ├─ Compila TypeScript
   │  └─ Optimiza CSS con Tailwind
   └─ Output: /dist con HTML/CSS/JS estático

3. PREVIEW
   ├─ npm run preview
   ├─ Sirve /dist localmente
   └─ Simula production

4. DEPLOYMENT
   ├─ Push a rama main (GitHub)
   ├─ CI/CD pipeline (si existe)
   ├─ Build automático
   ├─ Deploy a servidor (Docker/Nginx)
   └─ Site disponible en producción
```

