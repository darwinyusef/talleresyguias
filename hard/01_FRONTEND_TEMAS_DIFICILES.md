# Conocimientos Técnicos Difíciles: Frontend Development

## Objetivos
Temas complejos del día a día frontend que un arquitecto debe dominar para apoyar efectivamente a los desarrolladores de interfaz de usuario.

---

## CATEGORÍA 1: Performance Web Crítica

### 1.1 Core Web Vitals Optimization
**Dificultad:** ⭐⭐⭐⭐⭐

**Conocimientos Técnicos Requeridos:**

#### LCP (Largest Contentful Paint) < 2.5s
```javascript
// Técnicas avanzadas de optimización

// 1. Resource Hints
<link rel="preconnect" href="https://cdn.example.com">
<link rel="dns-prefetch" href="https://analytics.com">
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

// 2. Image Optimization avanzada
<picture>
  <source
    srcset="/hero-desktop.avif"
    type="image/avif"
    media="(min-width: 768px)">
  <source
    srcset="/hero-mobile.webp"
    type="image/webp">
  <img
    src="/hero.jpg"
    loading="eager"
    fetchpriority="high"
    decoding="async"
    width="1200"
    height="630"
    alt="Hero">
</picture>

// 3. Critical CSS Inlining
const criticalCSS = `
  /* Above-the-fold styles only */
  .header { ... }
  .hero { ... }
`;
// Inject in <head>, defer rest

// 4. Server-Side Rendering con Streaming
// Next.js App Router
export default async function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

#### CLS (Cumulative Layout Shift) < 0.1
```css
/* Prevenir layout shifts */

/* 1. Reservar espacio para imágenes */
.image-container {
  aspect-ratio: 16 / 9;
  background: #f0f0f0;
}

/* 2. Font loading sin FOIT/FOUT */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: optional; /* Evita layout shift */
  size-adjust: 100.5%; /* Match fallback metrics */
}

/* 3. Skeleton screens con dimensiones exactas */
.skeleton {
  width: 100%;
  height: 200px; /* Altura exacta del contenido real */
  animation: shimmer 1.5s infinite;
}

/* 4. Ads containers con espacio reservado */
.ad-slot {
  min-height: 250px;
  width: 300px;
  background: #f9f9f9;
  content-visibility: auto;
}
```

```javascript
// Detectar y corregir CLS en desarrollo
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
      console.error('Layout shift detected:', {
        value: entry.value,
        sources: entry.sources,
        element: entry.sources[0]?.node
      });
    }
  }
});

observer.observe({ type: 'layout-shift', buffered: true });
```

#### INP (Interaction to Next Paint) < 200ms
```javascript
// 1. Event delegation para listas grandes
const listContainer = document.getElementById('list');
listContainer.addEventListener('click', (e) => {
  if (e.target.matches('.item')) {
    // Handle click - un solo listener para miles de items
    handleItemClick(e.target.dataset.id);
  }
});

// 2. Debouncing y Throttling
import { debounce } from 'lodash-es';

const handleSearch = debounce((query) => {
  fetch(`/api/search?q=${query}`)
    .then(res => res.json())
    .then(updateResults);
}, 300);

// 3. Web Workers para cálculos pesados
// main.js
const worker = new Worker('/calc-worker.js');
worker.postMessage({ type: 'heavy-calc', data: bigDataset });
worker.onmessage = (e) => {
  updateUI(e.data.result);
};

// calc-worker.js
self.onmessage = (e) => {
  if (e.data.type === 'heavy-calc') {
    const result = performHeavyCalculation(e.data.data);
    self.postMessage({ result });
  }
};

// 4. requestIdleCallback para tareas no urgentes
requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0 && tasks.length > 0) {
    const task = tasks.shift();
    task();
  }
}, { timeout: 2000 });

// 5. React: startTransition para updates no urgentes
import { startTransition } from 'react';

function handleChange(e) {
  const value = e.target.value;
  setInputValue(value); // Urgente: actualiza input

  startTransition(() => {
    setSearchResults(filterResults(value)); // No urgente
  });
}
```

**Debugging en Producción:**
```javascript
// Web Vitals monitoring
import { onCLS, onFID, onLCP, onINP } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    delta: metric.delta,
    id: metric.id,
    navigationType: metric.navigationType
  });

  // Use sendBeacon para garantizar envío
  navigator.sendBeacon('/analytics', body);
}

onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
```

---

### 1.2 Bundle Size Optimization
**Dificultad:** ⭐⭐⭐⭐

**Técnicas Avanzadas:**

```javascript
// 1. Dynamic imports con prefetch
const HeavyChart = lazy(() => {
  return import(
    /* webpackChunkName: "heavy-chart" */
    /* webpackPrefetch: true */
    './HeavyChart'
  );
});

// 2. Tree-shaking con side-effects
// package.json
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "./src/polyfills.js"
  ]
}

// 3. Barrel file optimization (evitar)
// ❌ Malo: importa TODO el lodash
import { debounce } from 'lodash';

// ✅ Bueno: importa solo lo necesario
import debounce from 'lodash-es/debounce';

// 4. Code splitting por ruta
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom'],
          'vendor-ui': ['@mui/material'],
          'vendor-charts': ['recharts']
        }
      }
    }
  }
};

// 5. Eliminar código muerto con magic comments
if (process.env.NODE_ENV !== 'production') {
  // Este código se elimina en production
  console.log('Debug info');
}

// 6. Replace de dependencias pesadas
// webpack.config.js
resolve: {
  alias: {
    'moment': 'dayjs',  // dayjs es 97% más pequeño
    'lodash': 'lodash-es'
  }
}
```

**Bundle Analyzer:**
```bash
# Webpack
npx webpack-bundle-analyzer stats.json

# Vite
npx vite-bundle-visualizer

# Análisis de dependencias
npx depcheck  # Encuentra dependencias no usadas
```

---

### 1.3 Memory Leaks y Garbage Collection
**Dificultad:** ⭐⭐⭐⭐⭐

**Patrones Comunes de Memory Leaks:**

```javascript
// 1. Event listeners no removidos
class Component {
  componentDidMount() {
    window.addEventListener('resize', this.handleResize);
  }

  componentWillUnmount() {
    // ⚠️ CRÍTICO: Remover listeners
    window.removeEventListener('resize', this.handleResize);
  }

  handleResize = () => {
    // ...
  }
}

// 2. Timers no limpiados
useEffect(() => {
  const interval = setInterval(() => {
    fetchData();
  }, 5000);

  // ⚠️ CRÍTICO: Cleanup
  return () => clearInterval(interval);
}, []);

// 3. Observables/Subscriptions
useEffect(() => {
  const subscription = dataStream$.subscribe(data => {
    setData(data);
  });

  return () => subscription.unsubscribe();
}, []);

// 4. Closures que retienen referencias
function createHeavyObject() {
  const huge = new Array(1000000).fill('data');

  return {
    // ⚠️ La closure retiene toda la referencia de 'huge'
    getFirst: () => huge[0],

    // ✅ Mejor: solo guardar lo necesario
    first: huge[0]
  };
}

// 5. DOM references en componentes desmontados
class ImageGallery extends React.Component {
  state = { images: [] };

  async loadImages() {
    const images = await fetch('/api/images');
    // ⚠️ Si el componente se desmonta, esto causa leak
    this.setState({ images });
  }

  // ✅ Solución: usar bandera
  componentDidMount() {
    this._isMounted = true;
    this.loadImages();
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

  async loadImages() {
    const images = await fetch('/api/images');
    if (this._isMounted) {
      this.setState({ images });
    }
  }
}

// 6. WeakMap/WeakSet para cachés
// ❌ Map retiene referencias
const cache = new Map();
function cacheData(element, data) {
  cache.set(element, data); // element nunca se puede GC
}

// ✅ WeakMap permite GC
const cache = new WeakMap();
function cacheData(element, data) {
  cache.set(element, data); // element puede ser GC
}
```

**Debugging Memory Leaks:**
```javascript
// Chrome DevTools: Memory profiler
// 1. Take heap snapshot
// 2. Realizar acción (abrir modal, etc.)
// 3. Take otro snapshot
// 4. Comparar (look for "Detached DOM tree")

// Programmatic memory monitoring
if (performance.memory) {
  console.log({
    usedJSHeapSize: performance.memory.usedJSHeapSize / 1048576,
    totalJSHeapSize: performance.memory.totalJSHeapSize / 1048576,
    jsHeapSizeLimit: performance.memory.jsHeapSizeLimit / 1048576
  });
}

// Detectar detached DOM nodes
const observer = new MutationObserver(() => {
  const detached = document.querySelectorAll('*').length;
  console.log('DOM nodes:', detached);
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});
```

---

## CATEGORÍA 2: Rendering Avanzado

### 2.1 Virtual Scrolling y Windowing
**Dificultad:** ⭐⭐⭐⭐

**Implementación sin librerías:**

```javascript
// Virtual list para 100,000 items
function VirtualList({ items, itemHeight, containerHeight }) {
  const [scrollTop, setScrollTop] = useState(0);

  // Calcular items visibles
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.ceil((scrollTop + containerHeight) / itemHeight);
  const visibleItems = items.slice(startIndex, endIndex + 1);

  // Total height del contenido
  const totalHeight = items.length * itemHeight;

  // Offset del primer item visible
  const offsetY = startIndex * itemHeight;

  return (
    <div
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.target.scrollTop)}
    >
      {/* Spacer para mantener scroll height */}
      <div style={{ height: totalHeight, position: 'relative' }}>
        {/* Solo renderizar items visibles */}
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {visibleItems.map((item, idx) => (
            <div
              key={startIndex + idx}
              style={{ height: itemHeight }}
            >
              {item}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Con react-window
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      {items[index]}
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}

// Variable height items (más complejo)
import { VariableSizeList } from 'react-window';

function VariableList({ items }) {
  const listRef = useRef();
  const rowHeights = useRef({});

  function getRowHeight(index) {
    return rowHeights.current[index] || 50; // default
  }

  function setRowHeight(index, size) {
    if (rowHeights.current[index] !== size) {
      rowHeights.current[index] = size;
      listRef.current.resetAfterIndex(index);
    }
  }

  const Row = ({ index, style }) => {
    const rowRef = useRef();

    useEffect(() => {
      if (rowRef.current) {
        setRowHeight(index, rowRef.current.clientHeight);
      }
    }, [index]);

    return (
      <div ref={rowRef} style={style}>
        {items[index]}
      </div>
    );
  };

  return (
    <VariableSizeList
      ref={listRef}
      height={600}
      itemCount={items.length}
      itemSize={getRowHeight}
      width="100%"
    >
      {Row}
    </VariableSizeList>
  );
}
```

---

### 2.2 React Concurrent Features
**Dificultad:** ⭐⭐⭐⭐⭐

```javascript
// 1. useTransition para updates no urgentes
import { useTransition, useState } from 'react';

function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  function handleChange(e) {
    const value = e.target.value;
    setQuery(value); // Urgente: actualiza input inmediatamente

    startTransition(() => {
      // No urgente: puede ser interrumpido
      const filtered = hugeList.filter(item =>
        item.toLowerCase().includes(value.toLowerCase())
      );
      setResults(filtered);
    });
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  );
}

// 2. useDeferredValue para valores diferidos
function ProductList({ searchQuery }) {
  const deferredQuery = useDeferredValue(searchQuery);

  // Se re-renderiza primero con query antigua,
  // luego con la nueva cuando hay tiempo
  const results = useMemo(() => {
    return products.filter(p =>
      p.name.includes(deferredQuery)
    );
  }, [deferredQuery]);

  return (
    <div style={{ opacity: searchQuery !== deferredQuery ? 0.5 : 1 }}>
      {results.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  );
}

// 3. Suspense para data fetching
import { Suspense } from 'react';

// React Query con Suspense
function UserProfile({ userId }) {
  const { data: user } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    suspense: true  // ← Habilita Suspense
  });

  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<Skeleton />}>
      <UserProfile userId={123} />
    </Suspense>
  );
}

// 4. Suspense Boundaries estratégicos
function Dashboard() {
  return (
    <div>
      {/* Header carga inmediatamente */}
      <Header />

      {/* Cada sección con su propio boundary */}
      <Suspense fallback={<ChartSkeleton />}>
        <SalesChart />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <UsersTable />
      </Suspense>

      {/* Datos críticos sin Suspense */}
      <CriticalMetrics />
    </div>
  );
}

// 5. useOptimistic para UI optimista
import { useOptimistic } from 'react';

function LikeButton({ postId, initialLikes }) {
  const [likes, setLikes] = useState(initialLikes);
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (current, amount) => current + amount
  );

  async function handleLike() {
    // UI se actualiza inmediatamente
    addOptimisticLike(1);

    try {
      const newLikes = await likePost(postId);
      setLikes(newLikes);
    } catch (error) {
      // Si falla, automáticamente revierte al estado anterior
      console.error('Like failed:', error);
    }
  }

  return (
    <button onClick={handleLike}>
      👍 {optimisticLikes}
    </button>
  );
}
```

---

### 2.3 CSS-in-JS Performance
**Dificultad:** ⭐⭐⭐⭐

```javascript
// Problema: Re-cálculo de styles en cada render
function BadComponent({ theme }) {
  return (
    <div style={{
      // ⚠️ Nuevo objeto en cada render
      padding: theme.spacing(2),
      backgroundColor: theme.colors.primary
    }}>
      Content
    </div>
  );
}

// Solución 1: useMemo
function BetterComponent({ theme }) {
  const styles = useMemo(() => ({
    padding: theme.spacing(2),
    backgroundColor: theme.colors.primary
  }), [theme]);

  return <div style={styles}>Content</div>;
}

// Solución 2: CSS Modules (sin runtime)
import styles from './Component.module.css';

function FastComponent() {
  return <div className={styles.container}>Content</div>;
}

// Solución 3: Styled Components con optimización
import styled from 'styled-components';

// ❌ Malo: componente styled dentro de render
function Bad() {
  const StyledDiv = styled.div`
    color: red;
  `; // Se recrea en cada render
  return <StyledDiv>Bad</StyledDiv>;
}

// ✅ Bueno: fuera del componente
const StyledDiv = styled.div`
  color: red;
`;

function Good() {
  return <StyledDiv>Good</StyledDiv>;
}

// Solución 4: Tailwind CSS (zero runtime)
function TailwindComponent() {
  return (
    <div className="p-4 bg-blue-500 hover:bg-blue-600 transition">
      Fast!
    </div>
  );
}

// Comparación de bundle size:
// styled-components: ~16KB
// emotion: ~7.9KB
// CSS Modules: 0KB runtime
// Tailwind: 0KB runtime (solo CSS usado)
```

---

## CATEGORÍA 3: State Management Complejo

### 3.1 React State Management Patterns
**Dificultad:** ⭐⭐⭐⭐⭐

```javascript
// 1. Context + Reducer para estado complejo
const CartContext = createContext();

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD_ITEM':
      const existing = state.items.find(i => i.id === action.item.id);
      if (existing) {
        return {
          ...state,
          items: state.items.map(i =>
            i.id === action.item.id
              ? { ...i, quantity: i.quantity + 1 }
              : i
          )
        };
      }
      return {
        ...state,
        items: [...state.items, { ...action.item, quantity: 1 }]
      };

    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.id)
      };

    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(i =>
          i.id === action.id
            ? { ...i, quantity: action.quantity }
            : i
        )
      };

    default:
      return state;
  }
}

function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [] });

  // Memoizar para evitar re-renders
  const value = useMemo(() => ({ state, dispatch }), [state]);

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}

// 2. Zustand - Estado global simple
import create from 'zustand';
import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set, get) => ({
      bears: 0,
      increase: () => set(state => ({ bears: state.bears + 1 })),

      // Acciones asíncronas
      fetchUser: async (id) => {
        const user = await fetch(`/api/users/${id}`).then(r => r.json());
        set({ user });
      },

      // Computed values
      get doubledBears() {
        return get().bears * 2;
      }
    }),
    {
      name: 'app-storage', // LocalStorage key
      partialize: (state) => ({ bears: state.bears }) // Solo persistir esto
    }
  )
);

// Uso: solo re-renderiza si 'bears' cambia
function BearCounter() {
  const bears = useStore(state => state.bears);
  return <div>{bears}</div>;
}

// 3. Jotai - Atomic state
import { atom, useAtom } from 'jotai';

const countAtom = atom(0);
const doubledAtom = atom(get => get(countAtom) * 2);

// Atom asíncrono
const userAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
});

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const [doubled] = useAtom(doubledAtom);

  return (
    <div>
      <div>Count: {count}</div>
      <div>Doubled: {doubled}</div>
      <button onClick={() => setCount(c => c + 1)}>+</button>
    </div>
  );
}

// 4. TanStack Query - Server state
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function TodoList() {
  const queryClient = useQueryClient();

  // Query con caching automático
  const { data: todos, isLoading } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    staleTime: 5 * 60 * 1000, // 5 minutos
    gcTime: 10 * 60 * 1000 // 10 minutos (antes cacheTime)
  });

  // Mutation con optimistic updates
  const mutation = useMutation({
    mutationFn: createTodo,
    onMutate: async (newTodo) => {
      // Cancelar queries en progreso
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Snapshot del estado anterior
      const previousTodos = queryClient.getQueryData(['todos']);

      // Update optimista
      queryClient.setQueryData(['todos'], old => [...old, newTodo]);

      return { previousTodos };
    },
    onError: (err, newTodo, context) => {
      // Rollback en caso de error
      queryClient.setQueryData(['todos'], context.previousTodos);
    },
    onSettled: () => {
      // Refetch para sincronizar
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    }
  });

  if (isLoading) return <Spinner />;

  return (
    <div>
      {todos.map(todo => <TodoItem key={todo.id} {...todo} />)}
      <button onClick={() => mutation.mutate({ title: 'New Todo' })}>
        Add Todo
      </button>
    </div>
  );
}
```

---

## CATEGORÍA 4: Build Tools y Toolchain

### 4.1 Webpack Avanzado
**Dificultad:** ⭐⭐⭐⭐

```javascript
// webpack.config.js - Configuración producción
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = {
  mode: 'production',
  entry: {
    main: './src/index.js',
    vendor: './src/vendor.js'
  },

  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash:8].js',
    chunkFilename: '[name].[contenthash:8].chunk.js',
    clean: true,
    publicPath: '/assets/'
  },

  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          parse: { ecma: 8 },
          compress: {
            ecma: 5,
            warnings: false,
            comparisons: false,
            inline: 2,
            drop_console: true  // Remover console.log
          },
          mangle: { safari10: true },
          output: {
            ecma: 5,
            comments: false,
            ascii_only: true
          }
        }
      }),
      new CssMinimizerPlugin()
    ],

    // Code splitting
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        // Vendor chunks
        vendors: {
          test: /[\\/]node_modules[\\/]/,
          priority: -10,
          reuseExistingChunk: true
        },

        // Common code
        common: {
          minChunks: 2,
          priority: -20,
          reuseExistingChunk: true
        },

        // React en su propio chunk
        react: {
          test: /[\\/]node_modules[\\/](react|react-dom)[\\/]/,
          name: 'react-vendors',
          priority: 10
        }
      }
    },

    // Runtime chunk separado
    runtimeChunk: 'single',

    // Module IDs estables
    moduleIds: 'deterministic'
  },

  module: {
    rules: [
      // JavaScript/TypeScript
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                targets: '> 0.25%, not dead',
                useBuiltIns: 'usage',
                corejs: 3
              }],
              '@babel/preset-react',
              '@babel/preset-typescript'
            ],
            plugins: [
              '@babel/plugin-transform-runtime'
            ],
            cacheDirectory: true
          }
        }
      },

      // CSS/SCSS
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              modules: {
                auto: true,
                localIdentName: '[hash:base64:8]'
              },
              sourceMap: true
            }
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: [
                  'autoprefixer',
                  'cssnano'
                ]
              }
            }
          },
          'sass-loader'
        ]
      },

      // Imágenes
      {
        test: /\.(png|jpg|jpeg|gif|svg)$/,
        type: 'asset',
        parser: {
          dataUrlCondition: {
            maxSize: 8 * 1024 // Inline < 8KB
          }
        },
        generator: {
          filename: 'images/[name].[hash:8][ext]'
        }
      },

      // Fonts
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name].[hash:8][ext]'
        }
      }
    ]
  },

  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      minify: {
        removeComments: true,
        collapseWhitespace: true,
        removeRedundantAttributes: true,
        useShortDoctype: true,
        removeEmptyAttributes: true,
        removeStyleLinkTypeAttributes: true,
        keepClosingSlash: true,
        minifyJS: true,
        minifyCSS: true,
        minifyURLs: true
      }
    }),

    new MiniCssExtractPlugin({
      filename: '[name].[contenthash:8].css',
      chunkFilename: '[name].[contenthash:8].chunk.css'
    }),

    // Gzip compression
    new CompressionPlugin({
      filename: '[path][base].gz',
      algorithm: 'gzip',
      test: /\.(js|css|html|svg)$/,
      threshold: 10240, // Solo archivos > 10KB
      minRatio: 0.8
    }),

    // Bundle analysis (solo en análisis)
    process.env.ANALYZE && new BundleAnalyzerPlugin()
  ].filter(Boolean),

  // Source maps para producción
  devtool: 'source-map',

  // Performance hints
  performance: {
    maxEntrypointSize: 512000,
    maxAssetSize: 512000,
    hints: 'warning'
  }
};
```

---

### 4.2 Vite Configuration Avanzada
**Dificultad:** ⭐⭐⭐⭐

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';
import compression from 'vite-plugin-compression';
import legacy from '@vitejs/plugin-legacy';

export default defineConfig({
  plugins: [
    react({
      // Fast Refresh options
      fastRefresh: true,

      // Babel plugins
      babel: {
        plugins: [
          ['babel-plugin-styled-components', {
            displayName: true,
            fileName: true
          }]
        ]
      }
    }),

    // Legacy browser support
    legacy({
      targets: ['defaults', 'not IE 11'],
      additionalLegacyPolyfills: ['regenerator-runtime/runtime'],
      renderLegacyChunks: true,
      polyfills: [
        'es.promise.finally',
        'es/map',
        'es/set'
      ],
      modernPolyfills: [
        'es.promise.finally'
      ]
    }),

    // Gzip compression
    compression({
      algorithm: 'gzip',
      ext: '.gz'
    }),

    // Bundle visualizer
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true
    })
  ],

  build: {
    target: 'es2015',
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,

    // Chunk size warnings
    chunkSizeWarningLimit: 500,

    rollupOptions: {
      output: {
        // Manual chunks
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['@mui/material', '@emotion/react'],
          'chart-vendor': ['recharts', 'd3']
        },

        // Asset naming
        assetFileNames: (assetInfo) => {
          let extType = assetInfo.name.split('.').pop();
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            extType = 'images';
          } else if (/woff|woff2|eot|ttf|otf/i.test(extType)) {
            extType = 'fonts';
          }
          return `${extType}/[name]-[hash][extname]`;
        }
      }
    },

    // Minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info']
      }
    }
  },

  // Dev server
  server: {
    port: 3000,
    host: true,
    open: true,

    // Proxy API requests
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },

    // HMR
    hmr: {
      overlay: true
    }
  },

  // Optimizations
  optimizeDeps: {
    include: ['react', 'react-dom'],
    exclude: ['@my-large-package']
  },

  // Aliases
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@utils': '/src/utils'
    }
  },

  // Environment variables
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    __API_URL__: JSON.stringify(process.env.VITE_API_URL)
  }
});
```

---

## CATEGORÍA 5: Testing Avanzado

### 5.1 Testing Library Patterns
**Dificultad:** ⭐⭐⭐⭐

```javascript
// 1. User-centric testing
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('should login user successfully', async () => {
    const user = userEvent.setup();
    const mockLogin = jest.fn();

    render(<LoginForm onLogin={mockLogin} />);

    // Find elements como lo haría un usuario
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /log in/i });

    // Interactuar como usuario
    await user.type(emailInput, 'user@example.com');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);

    // Assertions
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'user@example.com',
        password: 'password123'
      });
    });

    expect(screen.queryByRole('alert')).not.toBeInTheDocument();
  });

  it('should show validation errors', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);

    const submitButton = screen.getByRole('button', { name: /log in/i });
    await user.click(submitButton);

    // Múltiples errores
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/password is required/i)).toBeInTheDocument();
  });
});

// 2. Testing async operations
describe('UserProfile', () => {
  it('should load and display user data', async () => {
    const mockUser = { id: 1, name: 'John Doe', email: 'john@example.com' };

    // Mock API call
    jest.spyOn(global, 'fetch').mockResolvedValueOnce({
      json: async () => mockUser
    });

    render(<UserProfile userId={1} />);

    // Loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Loaded state
    expect(await screen.findByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();

    // Cleanup
    global.fetch.mockRestore();
  });

  it('should handle errors gracefully', async () => {
    jest.spyOn(global, 'fetch').mockRejectedValueOnce(new Error('API Error'));

    render(<UserProfile userId={1} />);

    expect(await screen.findByText(/error loading user/i)).toBeInTheDocument();

    global.fetch.mockRestore();
  });
});

// 3. Testing hooks
import { renderHook, act } from '@testing-library/react';

describe('useCounter', () => {
  it('should increment counter', () => {
    const { result } = renderHook(() => useCounter(0));

    expect(result.current.count).toBe(0);

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('should reset counter', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(0);
  });
});

// 4. MSW para mocking de APIs
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    const { id } = req.params;
    return res(
      ctx.json({
        id,
        name: 'John Doe',
        email: 'john@example.com'
      })
    );
  }),

  rest.post('/api/login', async (req, res, ctx) => {
    const { email, password } = await req.json();

    if (email === 'admin@test.com' && password === 'admin123') {
      return res(
        ctx.json({
          token: 'fake-jwt-token',
          user: { email, role: 'admin' }
        })
      );
    }

    return res(
      ctx.status(401),
      ctx.json({ message: 'Invalid credentials' })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API Integration', () => {
  it('should fetch user data', async () => {
    render(<UserProfile userId={1} />);

    expect(await screen.findByText('John Doe')).toBeInTheDocument();
  });

  it('should handle server errors', async () => {
    // Override handler para este test
    server.use(
      rest.get('/api/users/:id', (req, res, ctx) => {
        return res(
          ctx.status(500),
          ctx.json({ message: 'Server error' })
        );
      })
    );

    render(<UserProfile userId={1} />);

    expect(await screen.findByText(/error/i)).toBeInTheDocument();
  });
});
```

---

### 5.2 E2E Testing con Playwright
**Dificultad:** ⭐⭐⭐⭐⭐

```javascript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] }
    }
  ],

  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI
  }
});

// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should login successfully', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: /log in/i }).click();

    // Esperar navegación
    await page.waitForURL('/dashboard');

    // Verificar elementos del dashboard
    await expect(page.getByText('Welcome back')).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });

  test('should show validation errors', async ({ page }) => {
    await page.getByRole('button', { name: /log in/i }).click();

    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();
  });

  test('should handle invalid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('invalid@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: /log in/i }).click();

    await expect(page.getByText('Invalid credentials')).toBeVisible();
  });
});

// Page Object Model
class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: /log in/i }).click();
  }

  async expectToBeOnDashboard() {
    await this.page.waitForURL('/dashboard');
    await expect(this.page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  }
}

// Uso del Page Object
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await loginPage.expectToBeOnDashboard();
});

// Visual regression testing
test('homepage should match snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});

// Network mocking
test('should handle API errors', async ({ page }) => {
  // Mock API failure
  await page.route('/api/users', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' })
    });
  });

  await page.goto('/users');
  await expect(page.getByText('Failed to load users')).toBeVisible();
});

// Testing file uploads
test('should upload file', async ({ page }) => {
  await page.goto('/upload');

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles('./test-files/document.pdf');

  await page.getByRole('button', { name: /upload/i }).click();

  await expect(page.getByText('File uploaded successfully')).toBeVisible();
});

// Testing drag and drop
test('should reorder items', async ({ page }) => {
  await page.goto('/kanban');

  const item = page.getByText('Task 1');
  const target = page.locator('.column-done');

  await item.dragTo(target);

  await expect(target.locator('text=Task 1')).toBeVisible();
});
```

---

## Resumen de Prioridades Frontend

| Tema | Dificultad | Impacto Usuario | Frecuencia | Prioridad |
|------|------------|-----------------|------------|-----------|
| Core Web Vitals | 5 | 5 | 5 | **CRÍTICA** |
| Memory Leaks | 5 | 5 | 4 | **CRÍTICA** |
| Bundle Optimization | 4 | 5 | 5 | **CRÍTICA** |
| React Concurrent | 5 | 4 | 3 | **ALTA** |
| Virtual Scrolling | 4 | 4 | 3 | **ALTA** |
| State Management | 5 | 4 | 5 | **ALTA** |
| Testing Patterns | 4 | 3 | 5 | **ALTA** |
| Build Tools | 4 | 4 | 4 | **MEDIA** |
| CSS-in-JS Perf | 4 | 3 | 4 | **MEDIA** |
| E2E Testing | 5 | 3 | 3 | **MEDIA** |

---

**Total de Temas Difíciles Cubiertos:** 10 categorías principales con 25+ subtemas técnicos profundos.
