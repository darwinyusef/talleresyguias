# Integración de Datos Externos - Portfolio

Guía para integrar datos desde archivos JSON externos en GitHub y usar Minio para assets.

---

## 📋 Índice

1. [Configuración de JSON Externos en GitHub](#1-configuración-de-json-externos-en-github)
2. [Integración en Astro](#2-integración-en-astro)
3. [Configuración de Minio para Assets](#3-configuración-de-minio-para-assets)
4. [Caché y Optimización](#4-caché-y-optimización)

---

## 1. Configuración de JSON Externos en GitHub

### 1.1 Estructura de Repositorio Recomendada

Crea un repositorio separado para los datos o usa una rama específica:

**Opción A: Repositorio Separado (Recomendado)**
```
github.com/darwinyusef/portfolio-data/
├── projects.json
├── blog.json
├── experience.json
├── skills.json
└── config.json
```

**Opción B: Carpeta en el mismo repo**
```
darwinyusef.portfolio/
├── astro-portfolio/
└── data/
    ├── projects.json
    ├── blog.json
    └── experience.json
```

### 1.2 Ejemplo de Archivo JSON

**data/projects.json**
```json
{
  "lastUpdated": "2026-01-02T00:00:00Z",
  "projects": [
    {
      "id": "project-1",
      "title": "Mi Proyecto Increíble",
      "description": "Descripción del proyecto",
      "image": "https://minio.darwinyusef.com/portfolio/projects/project-1.jpg",
      "tags": ["React", "Node.js", "Docker"],
      "demoUrl": "https://demo.example.com",
      "githubUrl": "https://github.com/darwinyusef/project",
      "featured": true,
      "date": "2025-12-15"
    },
    {
      "id": "project-2",
      "title": "Otro Proyecto",
      "description": "Otra descripción",
      "image": "https://minio.darwinyusef.com/portfolio/projects/project-2.jpg",
      "tags": ["Vue", "Python"],
      "featured": false,
      "date": "2025-11-20"
    }
  ]
}
```

**data/blog.json**
```json
{
  "lastUpdated": "2026-01-02T00:00:00Z",
  "posts": [
    {
      "id": "post-1",
      "title": "Cómo Desplegar en DigitalOcean",
      "slug": "deploy-digitalocean",
      "excerpt": "Aprende a desplegar tu aplicación...",
      "content": "https://raw.githubusercontent.com/darwinyusef/portfolio-data/main/blog/deploy-digitalocean.md",
      "coverImage": "https://minio.darwinyusef.com/portfolio/blog/deploy-do.jpg",
      "author": "Darwin Yusef",
      "date": "2026-01-01",
      "tags": ["DevOps", "Docker", "DigitalOcean"],
      "published": true
    }
  ]
}
```

**data/experience.json**
```json
{
  "lastUpdated": "2026-01-02T00:00:00Z",
  "experience": [
    {
      "id": "exp-1",
      "company": "Tech Company",
      "position": "Senior Developer",
      "startDate": "2023-01",
      "endDate": "present",
      "description": "Desarrollo de aplicaciones web...",
      "technologies": ["React", "Node.js", "AWS"],
      "logo": "https://minio.darwinyusef.com/portfolio/companies/tech-co.png"
    }
  ]
}
```

### 1.3 Hacer los Archivos Públicos

Para archivos en GitHub:

1. **Repositorio público:** Los archivos son accesibles vía raw.githubusercontent.com
2. **URL formato:**
   ```
   https://raw.githubusercontent.com/USERNAME/REPO/BRANCH/PATH/FILE.json
   ```

**Ejemplo:**
```
https://raw.githubusercontent.com/darwinyusef/portfolio-data/main/projects.json
```

---

## 2. Integración en Astro

### 2.1 Instalar Dependencias

```bash
cd astro-portfolio
npm install --save node-fetch
```

### 2.2 Crear Utilidad para Fetch de Datos

**src/utils/dataFetcher.ts**
```typescript
// Configuración de URLs de datos externos
const DATA_URLS = {
  projects: 'https://raw.githubusercontent.com/darwinyusef/portfolio-data/main/projects.json',
  blog: 'https://raw.githubusercontent.com/darwinyusef/portfolio-data/main/blog.json',
  experience: 'https://raw.githubusercontent.com/darwinyusef/portfolio-data/main/experience.json',
  skills: 'https://raw.githubusercontent.com/darwinyusef/portfolio-data/main/skills.json',
};

// Cache en memoria para desarrollo
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutos

interface FetchOptions {
  useCache?: boolean;
  ttl?: number;
}

/**
 * Fetch data from external JSON source
 */
export async function fetchExternalData<T>(
  source: keyof typeof DATA_URLS,
  options: FetchOptions = {}
): Promise<T> {
  const { useCache = true, ttl = CACHE_TTL } = options;
  const url = DATA_URLS[source];

  // Check cache
  if (useCache && cache.has(url)) {
    const cached = cache.get(url)!;
    if (Date.now() - cached.timestamp < ttl) {
      console.log(`[DataFetcher] Cache hit for ${source}`);
      return cached.data;
    }
  }

  try {
    console.log(`[DataFetcher] Fetching ${source} from ${url}`);

    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    // Update cache
    if (useCache) {
      cache.set(url, { data, timestamp: Date.now() });
    }

    return data;
  } catch (error) {
    console.error(`[DataFetcher] Error fetching ${source}:`, error);

    // Return cached data if available (stale is better than nothing)
    if (cache.has(url)) {
      console.warn(`[DataFetcher] Using stale cache for ${source}`);
      return cache.get(url)!.data;
    }

    throw error;
  }
}

/**
 * Clear cache
 */
export function clearCache(): void {
  cache.clear();
}
```

### 2.3 Crear Tipos TypeScript

**src/types/data.ts**
```typescript
export interface Project {
  id: string;
  title: string;
  description: string;
  image: string;
  tags: string[];
  demoUrl?: string;
  githubUrl?: string;
  featured: boolean;
  date: string;
}

export interface ProjectsData {
  lastUpdated: string;
  projects: Project[];
}

export interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  coverImage: string;
  author: string;
  date: string;
  tags: string[];
  published: boolean;
}

export interface BlogData {
  lastUpdated: string;
  posts: BlogPost[];
}

export interface Experience {
  id: string;
  company: string;
  position: string;
  startDate: string;
  endDate: string | 'present';
  description: string;
  technologies: string[];
  logo: string;
}

export interface ExperienceData {
  lastUpdated: string;
  experience: Experience[];
}
```

### 2.4 Usar en Páginas Astro

**src/pages/projects.astro**
```astro
---
import { fetchExternalData } from '../utils/dataFetcher';
import type { ProjectsData } from '../types/data';

// Fetch projects data
const { projects } = await fetchExternalData<ProjectsData>('projects');

// Filter featured projects
const featuredProjects = projects.filter(p => p.featured);
---

<html>
<head>
  <title>Projects - Darwin Yusef</title>
</head>
<body>
  <h1>My Projects</h1>

  <section class="featured">
    <h2>Featured Projects</h2>
    {featuredProjects.map(project => (
      <div class="project-card">
        <img src={project.image} alt={project.title} />
        <h3>{project.title}</h3>
        <p>{project.description}</p>
        <div class="tags">
          {project.tags.map(tag => <span class="tag">{tag}</span>)}
        </div>
        {project.demoUrl && <a href={project.demoUrl}>Demo</a>}
        {project.githubUrl && <a href={project.githubUrl}>GitHub</a>}
      </div>
    ))}
  </section>

  <section class="all-projects">
    <h2>All Projects</h2>
    {projects.map(project => (
      <div class="project-item">
        <img src={project.image} alt={project.title} />
        <h4>{project.title}</h4>
      </div>
    ))}
  </section>
</body>
</html>
```

**src/pages/blog/[slug].astro**
```astro
---
import { fetchExternalData } from '../../utils/dataFetcher';
import type { BlogData, BlogPost } from '../../types/data';

// Get all blog posts for static paths
export async function getStaticPaths() {
  const { posts } = await fetchExternalData<BlogData>('blog');

  return posts
    .filter(post => post.published)
    .map(post => ({
      params: { slug: post.slug },
      props: { post },
    }));
}

const { post } = Astro.props as { post: BlogPost };

// Fetch markdown content if needed
let content = '';
if (post.content.startsWith('http')) {
  const response = await fetch(post.content);
  content = await response.text();
} else {
  content = post.content;
}
---

<html>
<head>
  <title>{post.title} - Blog</title>
  <meta name="description" content={post.excerpt} />
</head>
<body>
  <article>
    <img src={post.coverImage} alt={post.title} class="cover" />
    <h1>{post.title}</h1>
    <div class="meta">
      <span>By {post.author}</span>
      <span>{new Date(post.date).toLocaleDateString()}</span>
    </div>
    <div class="tags">
      {post.tags.map(tag => <span class="tag">{tag}</span>)}
    </div>
    <div class="content" set:html={content} />
  </article>
</body>
</html>
```

---

## 3. Configuración de Minio para Assets

### 3.1 Configurar Minio

```bash
# Conectar al servidor
ssh root@YOUR_SERVER_IP

# Acceder a Minio (asumiendo que está corriendo)
# URL: http://YOUR_SERVER_IP:9000
# Login con tus credenciales
```

### 3.2 Crear Buckets en Minio

**En la UI de Minio:**

1. **Ir a Buckets** → **Create Bucket**
2. **Crear buckets:**
   - `portfolio` (para assets generales)
   - `blog-images` (para imágenes de blog)
   - `projects` (para imágenes de proyectos)

3. **Configurar permisos públicos:**
   - Selecciona bucket → **Access** → **Add Policy**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {"AWS": ["*"]},
         "Action": ["s3:GetObject"],
         "Resource": ["arn:aws:s3:::portfolio/*"]
       }
     ]
   }
   ```

### 3.3 Instalar Minio Client (mc)

```bash
# En el servidor
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
mv mc /usr/local/bin/

# Configurar alias
mc alias set myminio http://localhost:9000 YOUR_ACCESS_KEY YOUR_SECRET_KEY

# Test
mc ls myminio
```

### 3.4 Upload de Assets

```bash
# Subir imágenes de proyectos
mc cp /path/to/project-1.jpg myminio/portfolio/projects/

# Subir múltiples archivos
mc cp --recursive /path/to/images/ myminio/portfolio/projects/

# Listar archivos
mc ls myminio/portfolio/projects/
```

### 3.5 URLs de Assets

Las URLs serán:
```
http://YOUR_SERVER_IP:9000/portfolio/projects/project-1.jpg
```

O con dominio configurado:
```
https://minio.darwinyusef.com/portfolio/projects/project-1.jpg
```

### 3.6 Integrar en Astro

**src/utils/minioHelper.ts**
```typescript
const MINIO_URL = import.meta.env.PUBLIC_MINIO_URL || 'http://YOUR_SERVER_IP:9000';
const MINIO_BUCKET = 'portfolio';

export function getMinioUrl(path: string): string {
  // Remove leading slash if present
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  return `${MINIO_URL}/${MINIO_BUCKET}/${cleanPath}`;
}

export function getProjectImage(projectId: string, filename: string): string {
  return getMinioUrl(`projects/${projectId}/${filename}`);
}

export function getBlogImage(filename: string): string {
  return getMinioUrl(`blog/${filename}`);
}

export function getCompanyLogo(companyId: string): string {
  return getMinioUrl(`companies/${companyId}.png`);
}
```

**Uso en componentes:**
```astro
---
import { getProjectImage, getBlogImage } from '../utils/minioHelper';

const projectImg = getProjectImage('project-1', 'screenshot.jpg');
const blogCover = getBlogImage('deploy-do.jpg');
---

<img src={projectImg} alt="Project" />
<img src={blogCover} alt="Blog post" />
```

---

## 4. Caché y Optimización

### 4.1 Configurar Variables de Entorno

**.env**
```bash
# Minio
PUBLIC_MINIO_URL=https://minio.darwinyusef.com
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key

# Data sources
PUBLIC_DATA_REPO=darwinyusef/portfolio-data
PUBLIC_DATA_BRANCH=main

# Cache
DATA_CACHE_TTL=300000  # 5 minutos en ms
```

### 4.2 Configurar Astro para ISR (Incremental Static Regeneration)

**astro.config.mjs**
```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'server', // o 'hybrid'

  // Configurar cache
  server: {
    headers: {
      'Cache-Control': 'public, max-age=300', // 5 minutos
    },
  },

  // Experimental: ISR
  experimental: {
    serverIslands: true,
  },
});
```

### 4.3 Implementar Revalidación

**src/pages/api/revalidate.ts**
```typescript
import type { APIRoute } from 'astro';
import { clearCache } from '../../utils/dataFetcher';

export const POST: APIRoute = async ({ request }) => {
  try {
    // Verificar token de seguridad
    const authHeader = request.headers.get('authorization');
    const token = authHeader?.replace('Bearer ', '');

    if (token !== import.meta.env.REVALIDATE_TOKEN) {
      return new Response('Unauthorized', { status: 401 });
    }

    // Limpiar cache
    clearCache();

    return new Response(
      JSON.stringify({ revalidated: true, timestamp: Date.now() }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: 'Internal Server Error' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
```

### 4.4 GitHub Webhook para Auto-Revalidación

**En tu repo de datos (portfolio-data):**

1. Settings → Webhooks → Add webhook
2. Payload URL: `https://darwinyusef.com/api/revalidate`
3. Content type: `application/json`
4. Secret: Tu `REVALIDATE_TOKEN`
5. Events: `Just the push event`

Ahora cuando actualices los JSONs en GitHub, automáticamente se limpiará el caché.

---

## 📦 Ejemplo de Workflow Completo

### 1. Actualizar Datos

```bash
# En tu repo portfolio-data
git clone https://github.com/darwinyusef/portfolio-data
cd portfolio-data

# Editar JSON
nano projects.json

# Commit y push
git add projects.json
git commit -m "Add new project"
git push
```

### 2. Auto-Rebuild (con webhook)

El webhook de GitHub llamará a `/api/revalidate` → Limpia caché → Próxima visita fetch datos nuevos

### 3. Upload de Imágenes a Minio

```bash
# Subir imagen del proyecto
mc cp new-project.jpg myminio/portfolio/projects/
```

### 4. Verificar

Visita: `https://darwinyusef.com/projects`

---

## 🎯 Resumen

✅ **Datos en JSON** → GitHub raw URLs
✅ **Imágenes/Assets** → Minio con URLs públicas
✅ **Fetch en build time** → Astro getStaticPaths
✅ **Cache inteligente** → 5 minutos TTL
✅ **Auto-revalidación** → GitHub webhooks

**Ventajas:**
- Sin necesidad de rebuild completo
- Datos actualizables sin código
- Assets servidos desde Minio (rápido)
- Caché eficiente

---

**Última actualización:** Enero 2026
