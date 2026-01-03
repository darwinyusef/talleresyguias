# GUÍA DE INTEGRACIÓN - Módulos de Blog y Podcast

## ANÁLISIS ACTUAL

### Blog
**Estado**: Híbrido
- Fuente remota: GitHub JSON (`blog.json`)
- Carga dinámica en cliente con fetch
- Filtrado por categoría en UI
- URL: `https://raw.githubusercontent.com/darwinyusef/darwinyusef/refs/heads/master/information/blog.json`

**Ruta listado**: `/blog` (blog.astro)
**Ruta detalle**: `/blog/[slug]` ([slug].astro)

### Podcast
**Estado**: Local (Content Collections)
- Archivos Markdown en `/src/content/podcasts/`
- Frontmatter YAML con metadata
- Episodio destacado + grid de otros
- Reproductor audio HTML5 personalizado

**Ruta listado**: `/podcast` (podcast.astro)
**Ruta detalle**: `/podcast/[slug]` ([slug].astro)

---

## ESTRUCTURA DE DATOS ESPERADA

### Blog JSON (GitHub)
```json
[
  {
    "id": 1,
    "title": "Título del artículo",
    "slug": "titulo-del-articulo",
    "excerpt": "Resumen corto...",
    "content": "<h2>HTML del artículo</h2>...",
    "category": "Backend",
    "tags": ["Node.js", "Express", "API"],
    "author": "Darwin Yusef",
    "coverImage": "https://...",
    "publishDate": "2025-12-20",
    "readTime": "5 min",
    "is_active": true
  }
]
```

### Podcast Markdown
```yaml
---
title: "Título del Episodio"
description: "Descripción breve"
pubDate: 2025-12-06
duration: "38:45"
audioUrl: "https://ejemplo.com/audio.mp3"
coverImage: "https://ejemplo.com/cover.jpg"
tags: ["IA", "LLM", "RAG"]
is_active: true
---

## Contenido del episodio en markdown
```

---

## NAVEGACIÓN ACTUAL

### Header.astro - Enlaces Principales

**Rutas blog**:
```astro
<a href={`${lang === "es" ? "" : lang + "/"}blog`}>
  Blog
</a>
```

**Rutas podcast**:
```astro
<a href={`${lang === "es" ? "" : lang + "/"}podcast`}>
  Podcast
</a>
```

**Patrón de i18n**:
- ES (default): `/blog`, `/podcast`
- EN: `/en/blog`, `/en/podcast`
- PT: `/pt/blog`, `/pt/podcast`

---

## COMPONENTES INTERNOS

### Blog Listing (blog.astro)
```typescript
// Carga remota con fetch
const GITHUB_RAW_URL = 'https://raw.githubusercontent.com/...';

// En script del lado del cliente:
async function loadPosts() {
  const response = await fetch(GITHUB_RAW_URL);
  const posts = await response.json();
  
  // Filtrar por is_active
  // Renderizar en grid 3 columnas
  // Soportar filtros por categoría
}
```

### Podcast Listing (podcast.astro)
```typescript
// Carga local con getCollection
const podcastsFromContent = await getCollection(
  'podcasts',
  ({ data }) => data.is_active
);

// Sort y renderizado:
// - Primero: Episodio destacado (más reciente)
// - Luego: Grid de otros episodios
// - Reproductor flotante en bottom
```

### Detalle Blog ([slug].astro)
```typescript
export async function getStaticPaths() {
  const response = await fetch(GITHUB_RAW_URL);
  const posts = await response.json();

  return posts
    .filter((post) => post.is_active)
    .map((post) => ({
      params: { slug: post.slug },
      props: { post }
    }));
}
```

### Detalle Podcast ([slug].astro)
```typescript
export async function getStaticPaths() {
  const podcasts = await getCollection('podcasts');
  return podcasts.map((podcast) => ({
    params: { slug: podcast.slug },
    props: { podcast },
  }));
}

const { podcast } = Astro.props;
const { Content } = await podcast.render();
```

---

## ESQUEMAS ZODB (src/content/config.ts)

Actual para Podcast:
```typescript
const podcasts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    duration: z.string(),
    audioUrl: z.string(),
    coverImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    is_active: z.boolean().default(true),
  }),
});
```

Podría existir para Posts (no encontrado):
```typescript
const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string().default('Admin'),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    is_active: z.boolean().default(true),
  }),
});
```

---

## INTERNACIONALIZACIÓN (i18n)

### Traducciones en `/src/i18n/locales/es.json`

```json
{
  "podcast": {
    "title": "Podcast",
    "episodes": "Episodios",
    "duration": "Duración",
    "listen": "Escuchar"
  }
}
```

### Uso en Componentes
```typescript
import { getLangFromUrl, useTranslations } from '../i18n/utils';

const lang = getLangFromUrl(Astro.url);
const t = useTranslations(lang);

// Uso:
t('podcast.title')  // "Podcast"
```

---

## REPRODUCCIÓN DE AUDIO

### Reproductor Personalizado (podcast/[slug].astro)

```html
<audio id="main-audio" preload="metadata">
  <source src={podcast.data.audioUrl} type="audio/mpeg" />
</audio>

<div id="progress-bar"></div>
<button id="play-pause-btn"></button>
<button id="skip-backward"></button>
<button id="skip-forward"></button>
<select id="playback-speed">
  <option value="0.5">0.5x</option>
  <option value="1" selected>1x</option>
  <option value="2">2x</option>
</select>
```

### JavaScript del Reproductor

```typescript
document.addEventListener('DOMContentLoaded', () => {
  const audio = document.getElementById('main-audio');
  const podcastSlug = window.location.pathname.split('/').pop();
  const storageKey = `podcast-time-${podcastSlug}`;

  // Restaurar progreso
  const savedTime = localStorage.getItem(storageKey);
  if (savedTime) {
    audio.currentTime = parseFloat(savedTime);
  }

  // Guardar progreso
  audio.addEventListener('timeupdate', () => {
    localStorage.setItem(storageKey, audio.currentTime.toString());
  });

  // Controls: play/pause, skip, speed, volume...
});
```

---

## ESTILOS TAILWIND

### Grid de Cards

```astro
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Cards aquí */}
</div>
```

### Card Podcast

```astro
<article class="podcast-card group relative overflow-hidden rounded-2xl 
  bg-[#1a1a1a] shadow-lg transition-all duration-500 hover:-translate-y-2 
  border border-gray-800">
  <!-- Cover image -->
  <div class="relative h-32 overflow-hidden">
    <img src={...} alt={...} class="w-full h-full object-cover" />
  </div>
  
  <!-- Content -->
  <div class="p-5">
    <h3 class="font-bold text-lg mb-4 line-clamp-2">
      {title}
    </h3>
    <button class="inline-flex items-center gap-2 px-4 py-2.5 
      bg-gradient-to-r from-pink-600 to-primary rounded-xl font-semibold">
      Escuchar
    </button>
  </div>
</article>
```

### Featured Card

```astro
<article class="podcast-card-featured group relative overflow-hidden rounded-3xl 
  bg-gradient-to-br from-[#1a1a2e] to-[#16213e] border-2 border-purple-900/50">
  <div class="grid md:grid-cols-2 gap-0">
    <!-- Image with overlay -->
    <div class="relative h-80 md:h-auto overflow-hidden">
      <img src={...} alt={...} />
      <!-- Play button overlay -->
      <button class="play-podcast-btn absolute top-1/2 left-1/2 
        -translate-x-1/2 -translate-y-1/2 w-24 h-24 rounded-full 
        bg-white/90 hover:scale-110">
        <span>play_circle</span>
      </button>
    </div>
    
    <!-- Text content -->
    <div class="p-8 md:p-10 flex flex-col justify-center">
      <h3 class="text-4xl md:text-5xl font-black mb-6">
        {title}
      </h3>
      <p class="text-lg text-gray-300 mb-8">
        {description}
      </p>
      <a href={...} class="inline-flex items-center gap-2 px-6 py-3 
        bg-gradient-to-r from-primary to-purple-600 rounded-xl font-bold">
        Ver Episodio Completo
      </a>
    </div>
  </div>
</article>
```

---

## EFECTOS VISUALES

### Parallax Scroll

```astro
<!-- En elemento -->
<div class="parallax-mascot" data-speed="0.2">
  <img src="/img/mascota.png" alt="..." />
</div>

<!-- En script -->
<script>
  const parallaxElements = document.querySelectorAll('[data-speed]');
  
  function updateParallax() {
    const scrollTop = window.pageYOffset;
    parallaxElements.forEach((el) => {
      const speed = parseFloat(el.getAttribute('data-speed'));
      const yPos = scrollTop * speed;
      el.style.transform = `translateY(${yPos}px)`;
    });
  }
  
  window.addEventListener('scroll', updateParallax, { passive: true });
</script>
```

### Hero Section

```astro
<section class="relative min-h-[70vh] flex items-center justify-center py-20">
  <div class="max-w-[1800px] mx-auto w-full">
    <div class="text-center">
      <h1 class="text-[clamp(3rem,12vw,12rem)] font-black leading-[0.9]">
        MI
        <br />
        <span class="text-transparent bg-clip-text 
          bg-gradient-to-r from-primary via-purple-600 to-pink-600">
          PODCAST
        </span>
      </h1>
      <p class="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto">
        {description}
      </p>
    </div>
  </div>
</section>
```

---

## FILTRADO (Blog)

### Sistema de Filtros

```typescript
interface Post {
  category: string;
  tags: string[];
  // ...
}

function createCategoryFilters(posts: Post[]) {
  const categoriesMap = new Map<string, number>();
  
  posts.forEach(post => {
    const category = post.category || 'Sin categoría';
    categoriesMap.set(category, (categoriesMap.get(category) || 0) + 1);
  });

  // Renderizar botones por categoría
  const buttons = Array.from(categoriesMap.entries())
    .map(([category, count]) => `
      <button data-category="${category}">
        ${category} (${count})
      </button>
    `);
}

function filterByCategory(category: string) {
  const filtered = category === 'all'
    ? allPosts
    : allPosts.filter(p => p.category === category);
  
  renderPosts(filtered);
}
```

---

## FUNCIONES AUXILIARES

### GitHub Config (src/config/github.ts)

```typescript
export function getGithubRawUrl() {
  return 'https://raw.githubusercontent.com/darwinyusef/darwinyusef/refs/heads/master/information/';
}
```

---

## PATRONES DE INTEGRACIÓN

### Para Agregar Nueva Colección (ej: Tutoriales)

1. **Crear archivos en `/src/content/tutorials/`**
   ```markdown
   ---
   title: "Título"
   description: "Descripción"
   pubDate: 2025-12-20
   tags: ["tag1", "tag2"]
   is_active: true
   ---
   
   ## Contenido
   ```

2. **Actualizar esquema en `config.ts`**
   ```typescript
   const tutorials = defineCollection({
     type: 'content',
     schema: z.object({
       title: z.string(),
       description: z.string(),
       pubDate: z.date(),
       tags: z.array(z.string()).default([]),
       is_active: z.boolean().default(true),
     }),
   });

   export const collections = {
     // ...
     tutorials,
   };
   ```

3. **Crear página listado `/src/pages/tutorials.astro`**
   ```astro
   const tutorials = await getCollection('tutorials', 
     ({ data }) => data.is_active
   );
   ```

4. **Crear página detalle `/src/pages/tutorials/[slug].astro`**
   ```astro
   export async function getStaticPaths() {
     const tutorials = await getCollection('tutorials');
     return tutorials.map(tutorial => ({
       params: { slug: tutorial.slug },
       props: { tutorial },
     }));
   }
   ```

5. **Agregar en Header.astro**
   ```astro
   <a href={`${lang === "es" ? "" : lang + "/"}tutorials`}>
     Tutoriales
   </a>
   ```

6. **Agregar traducciones en i18n**
   ```json
   {
     "tutorials": {
       "title": "Tutoriales",
       "episodes": "Tutoriales disponibles"
     }
   }
   ```

---

## MEJORAS PROPUESTAS

### 1. Sincronización Blog Local/Remoto
```typescript
// Considerar migrar blog.json a Content Collections
const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string().default('Admin'),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    category: z.string().default('General'),
    is_active: z.boolean().default(true),
  }),
});
```

### 2. Componentes Reutilizables
```astro
<!-- components/ContentCard.astro -->
<article class="content-card {variant}">
  <!-- Generic card structure -->
</article>
```

### 3. Mejor Caching
```typescript
// Cachear JSON de GitHub en build time
// No solo en cliente
```

### 4. RSS Feeds
```typescript
// Generar RSS para blog y podcast
// Rutas: /blog/feed.xml, /podcast/feed.xml
```

### 5. Search/Búsqueda
```typescript
// Implementar búsqueda full-text
// IndexedDB o simple filter en cliente
```

---

## CHECKLIST DE INTEGRACIÓN

Para agregar un nuevo módulo similar a Blog/Podcast:

- [ ] Definir esquema en `src/content/config.ts`
- [ ] Crear archivos contenido en `src/content/[coleccion]/`
- [ ] Crear página listado: `src/pages/[ruta].astro`
- [ ] Crear página detalle: `src/pages/[ruta]/[slug].astro`
- [ ] Actualizar `Header.astro` con navegación
- [ ] Agregar traducciones en `/src/i18n/locales/[lang].json`
- [ ] Crear componentes en `src/components/` si necesario
- [ ] Agregar estilos Tailwind siguiendo patrones existentes
- [ ] Implementar responsive design (mobile, tablet, desktop)
- [ ] Probar i18n para todos los idiomas
- [ ] Agregar meta tags SEO
- [ ] Build estático y verificar outputs

