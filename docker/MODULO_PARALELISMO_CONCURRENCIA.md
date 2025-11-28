# Módulo Extra: Paralelismo y Concurrencia en Docker

## Objetivo
Aprender a implementar paralelismo, concurrencia, multiprocessing y multithreading en aplicaciones containerizadas.

---

## Índice

1. [Conceptos Fundamentales](#conceptos-fundamentales)
2. [Python: Asyncio, Threading, Multiprocessing](#python)
3. [Node.js: Worker Threads, Cluster](#nodejs)
4. [Java: Threads, Parallel Streams](#java)
5. [Go: Goroutines](#go)
6. [Optimización de Contenedores](#optimización-contenedores)
7. [Patrones de Arquitectura](#patrones-arquitectura)

---

## Conceptos Fundamentales

### Concurrencia vs Paralelismo

**Concurrencia** - Múltiples tareas progresando simultáneamente (no necesariamente al mismo tiempo)
```
Tarea A: ====>     ====>     ====>
Tarea B:      ====>     ====>
```

**Paralelismo** - Múltiples tareas ejecutándose al mismo tiempo (requiere múltiples CPUs)
```
CPU 1: Tarea A ===============>
CPU 2: Tarea B ===============>
```

### Multithreading vs Multiprocessing

**Multithreading** - Múltiples hilos en un mismo proceso (comparten memoria)
- ✅ Bajo overhead de memoria
- ✅ Cambio de contexto rápido
- ❌ GIL en Python (Global Interpreter Lock)
- 👍 Ideal para I/O-bound (red, disco)

**Multiprocessing** - Múltiples procesos independientes
- ✅ True paralelismo (sin GIL)
- ✅ Usa todos los CPUs
- ❌ Mayor uso de memoria
- ❌ Comunicación más lenta
- 👍 Ideal para CPU-bound (cálculos intensivos)

---

## Python

### 1. Asyncio (Concurrencia - I/O Bound)

**Código:**
```python
import asyncio
import aiohttp
import time

async def fetch_url(session, url):
    """Fetch URL asíncrono"""
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        'https://api.github.com/users/octocat',
        'https://api.github.com/users/torvalds',
        'https://api.github.com/users/gvanrossum',
    ]

    start = time.time()

    async with aiohttp.ClientSession() as session:
        # Ejecutar todas las requests concurrentemente
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    print(f"Fetched {len(results)} URLs in {time.time() - start:.2f}s")

# Ejecutar
asyncio.run(main())
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

**requirements.txt:**
```
aiohttp==3.9.1
```

### 2. Threading (Concurrencia - I/O Bound)

**Código:**
```python
import threading
import requests
import time
from queue import Queue

def worker(queue, results):
    """Worker thread que procesa URLs de la queue"""
    while True:
        url = queue.get()
        if url is None:
            break

        try:
            response = requests.get(url, timeout=5)
            results.append({
                'url': url,
                'status': response.status_code,
                'length': len(response.content)
            })
        except Exception as e:
            results.append({'url': url, 'error': str(e)})
        finally:
            queue.task_done()

def main():
    urls = [
        'https://api.github.com/users/octocat',
        'https://api.github.com/users/torvalds',
        'https://api.github.com/users/gvanrossum',
    ] * 10  # 30 URLs total

    num_threads = 5
    queue = Queue()
    results = []
    threads = []

    # Crear y empezar threads
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(queue, results))
        t.start()
        threads.append(t)

    # Agregar URLs a la queue
    for url in urls:
        queue.put(url)

    # Esperar que se procesen todas
    queue.join()

    # Detener threads
    for _ in range(num_threads):
        queue.put(None)
    for t in threads:
        t.join()

    print(f"Processed {len(results)} URLs")
    print(f"Successful: {sum(1 for r in results if 'status' in r)}")

if __name__ == '__main__':
    start = time.time()
    main()
    print(f"Total time: {time.time() - start:.2f}s")
```

### 3. Multiprocessing (Paralelismo - CPU Bound)

**Código:**
```python
import multiprocessing
import time
import math

def is_prime(n):
    """Verificar si n es primo (CPU-intensive)"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def check_range(start, end):
    """Verificar primos en un rango"""
    primes = []
    for n in range(start, end):
        if is_prime(n):
            primes.append(n)
    return primes

def parallel_prime_finder(limit, num_processes=None):
    """Encontrar primos usando multiprocessing"""
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    # Dividir trabajo en chunks
    chunk_size = limit // num_processes
    ranges = [
        (i * chunk_size, (i + 1) * chunk_size)
        for i in range(num_processes)
    ]
    ranges[-1] = (ranges[-1][0], limit)  # Ajustar último rango

    # Crear pool de procesos
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(check_range, ranges)

    # Combinar resultados
    all_primes = []
    for result in results:
        all_primes.extend(result)

    return all_primes

if __name__ == '__main__':
    limit = 100000

    # Secuencial
    start = time.time()
    sequential_primes = check_range(0, limit)
    sequential_time = time.time() - start

    # Paralelo
    start = time.time()
    parallel_primes = parallel_prime_finder(limit)
    parallel_time = time.time() - start

    print(f"Found {len(parallel_primes)} primes up to {limit}")
    print(f"Sequential: {sequential_time:.2f}s")
    print(f"Parallel: {parallel_time:.2f}s")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")
```

**Dockerfile con CPU optimization:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema si es necesario
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY app.py .

# Configurar CPUs disponibles
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
```

**docker-compose.yml con límites de CPU:**
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: python-multiprocessing
    deploy:
      resources:
        limits:
          cpus: '4'  # Limitar a 4 CPUs
          memory: 2G
        reservations:
          cpus: '2'
          memory: 1G
```

### 4. FastAPI con Background Tasks

**Código:**
```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
import time

app = FastAPI()

class Task(BaseModel):
    name: str
    duration: int

async def process_task(task_name: str, duration: int):
    """Tarea en background"""
    print(f"Starting task: {task_name}")
    await asyncio.sleep(duration)
    print(f"Completed task: {task_name}")

@app.post("/tasks/")
async def create_task(task: Task, background_tasks: BackgroundTasks):
    """Crear tarea en background"""
    background_tasks.add_task(process_task, task.name, task.duration)
    return {"message": f"Task {task.name} queued"}

@app.get("/heavy-computation")
async def heavy_computation():
    """Endpoint que usa multiprocessing para cálculo pesado"""
    from concurrent.futures import ProcessPoolExecutor

    def compute(n):
        return sum(i * i for i in range(n))

    # Usar ProcessPoolExecutor para paralelismo
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(compute, 10_000_000) for _ in range(4)]
        results = [f.result() for f in futures]

    return {"results": results}
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
```

---

## Node.js

### 1. Worker Threads (Paralelismo - CPU Bound)

**worker.js:**
```javascript
const { parentPort, workerData } = require('worker_threads')

function isPrime(n) {
  if (n < 2) return false
  for (let i = 2; i <= Math.sqrt(n); i++) {
    if (n % i === 0) return false
  }
  return true
}

function findPrimes(start, end) {
  const primes = []
  for (let n = start; n < end; n++) {
    if (isPrime(n)) primes.push(n)
  }
  return primes
}

// Procesar rango asignado a este worker
const primes = findPrimes(workerData.start, workerData.end)
parentPort.postMessage(primes)
```

**app.js:**
```javascript
const { Worker } = require('worker_threads')
const os = require('os')

function runWorker(workerData) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./worker.js', { workerData })
    worker.on('message', resolve)
    worker.on('error', reject)
    worker.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Worker stopped with exit code ${code}`))
      }
    })
  })
}

async function findPrimesParallel(limit) {
  const numWorkers = os.cpus().length
  const chunkSize = Math.floor(limit / numWorkers)

  const workers = []
  for (let i = 0; i < numWorkers; i++) {
    const start = i * chunkSize
    const end = i === numWorkers - 1 ? limit : (i + 1) * chunkSize
    workers.push(runWorker({ start, end }))
  }

  const results = await Promise.all(workers)
  return results.flat()
}

async function main() {
  const limit = 100000

  console.log(`Finding primes up to ${limit}...`)
  console.log(`Using ${os.cpus().length} workers`)

  const start = Date.now()
  const primes = await findPrimesParallel(limit)
  const duration = Date.now() - start

  console.log(`Found ${primes.length} primes in ${duration}ms`)
}

main()
```

**Dockerfile:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

CMD ["node", "app.js"]
```

### 2. Cluster Module (Múltiples Procesos - HTTP Server)

**server.js:**
```javascript
const cluster = require('cluster')
const http = require('http')
const os = require('os')

const numCPUs = os.cpus().length

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`)
  console.log(`Forking ${numCPUs} workers...`)

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork()
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`)
    console.log('Starting a new worker...')
    cluster.fork()
  })

} else {
  // Workers pueden compartir cualquier conexión TCP
  // En este caso es un servidor HTTP
  http.createServer((req, res) => {
    // Simular trabajo CPU-intensive
    let sum = 0
    for (let i = 0; i < 1e7; i++) {
      sum += i
    }

    res.writeHead(200, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify({
      message: 'Hello World',
      worker: process.pid,
      result: sum
    }))
  }).listen(3000)

  console.log(`Worker ${process.pid} started`)
}
```

**Dockerfile:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY server.js .

EXPOSE 3000

CMD ["node", "server.js"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 2G
```

### 3. Async/Await (Concurrencia - I/O Bound)

**app.js:**
```javascript
const axios = require('axios')

async function fetchUser(userId) {
  const response = await axios.get(`https://api.github.com/users/${userId}`)
  return response.data
}

async function fetchAllUsersConcurrent(userIds) {
  // Todas las requests se ejecutan concurrentemente
  const promises = userIds.map(id => fetchUser(id))
  const results = await Promise.all(promises)
  return results
}

async function fetchAllUsersSequential(userIds) {
  // Una a la vez (lento)
  const results = []
  for (const id of userIds) {
    const user = await fetchUser(id)
    results.push(user)
  }
  return results
}

async function main() {
  const userIds = ['octocat', 'torvalds', 'gvanrossum', 'tj', 'sindresorhus']

  // Concurrente
  console.time('Concurrent')
  await fetchAllUsersConcurrent(userIds)
  console.timeEnd('Concurrent')

  // Secuencial
  console.time('Sequential')
  await fetchAllUsersSequential(userIds)
  console.timeEnd('Sequential')
}

main()
```

---

## Java

### 1. Threads Básicos

**App.java:**
```java
public class App {

    static class Worker extends Thread {
        private final int id;
        private final int start;
        private final int end;
        private int count = 0;

        public Worker(int id, int start, int end) {
            this.id = id;
            this.start = start;
            this.end = end;
        }

        @Override
        public void run() {
            System.out.println("Worker " + id + " started");
            for (int i = start; i < end; i++) {
                if (isPrime(i)) count++;
            }
            System.out.println("Worker " + id + " found " + count + " primes");
        }

        public int getCount() {
            return count;
        }

        private boolean isPrime(int n) {
            if (n < 2) return false;
            for (int i = 2; i <= Math.sqrt(n); i++) {
                if (n % i == 0) return false;
            }
            return true;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        int limit = 100000;
        int numThreads = Runtime.getRuntime().availableProcessors();
        int chunkSize = limit / numThreads;

        Worker[] workers = new Worker[numThreads];

        long start = System.currentTimeMillis();

        // Crear y empezar threads
        for (int i = 0; i < numThreads; i++) {
            int rangeStart = i * chunkSize;
            int rangeEnd = (i == numThreads - 1) ? limit : (i + 1) * chunkSize;
            workers[i] = new Worker(i, rangeStart, rangeEnd);
            workers[i].start();
        }

        // Esperar a que todos terminen
        int totalPrimes = 0;
        for (Worker worker : workers) {
            worker.join();
            totalPrimes += worker.getCount();
        }

        long duration = System.currentTimeMillis() - start;

        System.out.println("Total primes: " + totalPrimes);
        System.out.println("Time: " + duration + "ms");
    }
}
```

### 2. ExecutorService (Thread Pool)

**App.java:**
```java
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

public class App {

    static class PrimeTask implements Callable<List<Integer>> {
        private final int start;
        private final int end;

        public PrimeTask(int start, int end) {
            this.start = start;
            this.end = end;
        }

        @Override
        public List<Integer> call() {
            List<Integer> primes = new ArrayList<>();
            for (int i = start; i < end; i++) {
                if (isPrime(i)) primes.add(i);
            }
            return primes;
        }

        private boolean isPrime(int n) {
            if (n < 2) return false;
            for (int i = 2; i <= Math.sqrt(n); i++) {
                if (n % i == 0) return false;
            }
            return true;
        }
    }

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        int limit = 100000;
        int numThreads = Runtime.getRuntime().availableProcessors();
        int chunkSize = limit / numThreads;

        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<List<Integer>>> futures = new ArrayList<>();

        long start = System.currentTimeMillis();

        // Submit tareas
        for (int i = 0; i < numThreads; i++) {
            int rangeStart = i * chunkSize;
            int rangeEnd = (i == numThreads - 1) ? limit : (i + 1) * chunkSize;
            futures.add(executor.submit(new PrimeTask(rangeStart, rangeEnd)));
        }

        // Recolectar resultados
        List<Integer> allPrimes = new ArrayList<>();
        for (Future<List<Integer>> future : futures) {
            allPrimes.addAll(future.get());
        }

        executor.shutdown();

        long duration = System.currentTimeMillis() - start;

        System.out.println("Found " + allPrimes.size() + " primes");
        System.out.println("Time: " + duration + "ms");
    }
}
```

### 3. Parallel Streams (Java 8+)

**App.java:**
```java
import java.util.stream.*;

public class App {

    public static boolean isPrime(int n) {
        if (n < 2) return false;
        return IntStream.rangeClosed(2, (int) Math.sqrt(n))
                .noneMatch(i -> n % i == 0);
    }

    public static void main(String[] args) {
        int limit = 100000;

        // Sequential
        long start = System.currentTimeMillis();
        long count1 = IntStream.range(0, limit)
                .filter(App::isPrime)
                .count();
        long sequential = System.currentTimeMillis() - start;

        // Parallel
        start = System.currentTimeMillis();
        long count2 = IntStream.range(0, limit)
                .parallel()
                .filter(App::isPrime)
                .count();
        long parallel = System.currentTimeMillis() - start;

        System.out.println("Primes found: " + count2);
        System.out.println("Sequential: " + sequential + "ms");
        System.out.println("Parallel: " + parallel + "ms");
        System.out.println("Speedup: " + (double) sequential / parallel + "x");
    }
}
```

**Dockerfile:**
```dockerfile
FROM eclipse-temurin:17-jdk-alpine AS builder

WORKDIR /app

COPY App.java .
RUN javac App.java

FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

COPY --from=builder /app/*.class ./

CMD ["java", "App"]
```

---

## Go

### Goroutines (Concurrencia Nativa)

**main.go:**
```go
package main

import (
    "fmt"
    "math"
    "runtime"
    "sync"
    "time"
)

func isPrime(n int) bool {
    if n < 2 {
        return false
    }
    for i := 2; i <= int(math.Sqrt(float64(n))); i++ {
        if n%i == 0 {
            return false
        }
    }
    return true
}

func findPrimes(start, end int, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()

    count := 0
    for i := start; i < end; i++ {
        if isPrime(i) {
            count++
        }
    }

    results <- count
}

func main() {
    limit := 100000
    numGoroutines := runtime.NumCPU()
    chunkSize := limit / numGoroutines

    fmt.Printf("Using %d goroutines\n", numGoroutines)

    start := time.Now()

    results := make(chan int, numGoroutines)
    var wg sync.WaitGroup

    // Lanzar goroutines
    for i := 0; i < numGoroutines; i++ {
        rangeStart := i * chunkSize
        rangeEnd := limit
        if i < numGoroutines-1 {
            rangeEnd = (i + 1) * chunkSize
        }

        wg.Add(1)
        go findPrimes(rangeStart, rangeEnd, results, &wg)
    }

    // Esperar a que todas terminen
    wg.Wait()
    close(results)

    // Sumar resultados
    totalPrimes := 0
    for count := range results {
        totalPrimes += count
    }

    duration := time.Since(start)

    fmt.Printf("Found %d primes in %v\n", totalPrimes, duration)
}
```

**Dockerfile:**
```dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main .

FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/main .

CMD ["./main"]
```

---

## Optimización de Contenedores

### 1. Limitar CPUs Disponibles

```yaml
version: '3.8'

services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '2'      # Máximo 2 CPUs
          memory: 1G
        reservations:
          cpus: '1'      # Garantizado 1 CPU
          memory: 512M
```

### 2. CPU Affinity (Pinning)

```bash
# Ejecutar contenedor en CPUs específicos
docker run --cpuset-cpus="0,1" myapp

# O en docker-compose
services:
  app:
    image: myapp
    cpuset: "0,1"
```

### 3. Configurar Worker Processes

**Uvicorn (FastAPI):**
```bash
# Número de workers = CPUs disponibles
uvicorn app:app --workers $(nproc)
```

**Gunicorn:**
```bash
# Fórmula recomendada: (2 × CPUs) + 1
gunicorn app:app --workers $((2 * $(nproc) + 1))
```

**Nginx:**
```nginx
# nginx.conf
worker_processes auto;  # Detecta CPUs automáticamente
```

### 4. Docker Compose con Escalado

```yaml
version: '3.8'

services:
  worker:
    build: ./worker
    deploy:
      replicas: 4  # 4 instancias del worker
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

```bash
# Escalar dinámicamente
docker compose up -d --scale worker=8
```

---

## Patrones de Arquitectura

### 1. Worker Pool Pattern

```yaml
version: '3.8'

services:
  redis:
    image: redis:alpine

  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - redis

  worker:
    build: ./worker
    depends_on:
      - redis
    deploy:
      replicas: 5  # 5 workers en paralelo
```

**api/app.py:**
```python
from fastapi import FastAPI
import redis

app = FastAPI()
r = redis.Redis(host='redis', port=6379)

@app.post("/tasks")
async def create_task(data: dict):
    # Agregar tarea a la cola
    r.lpush('tasks', json.dumps(data))
    return {"status": "queued"}
```

**worker/worker.py:**
```python
import redis
import time

r = redis.Redis(host='redis', port=6379)

while True:
    # Obtener tarea de la cola (bloqueante)
    _, task = r.brpop('tasks')

    # Procesar tarea
    print(f"Processing: {task}")
    time.sleep(2)  # Simular trabajo
    print(f"Completed: {task}")
```

### 2. Fan-Out/Fan-In Pattern

```python
import asyncio

async def process_item(item):
    await asyncio.sleep(1)
    return item * 2

async def fan_out_fan_in(items):
    # Fan-out: distribuir trabajo
    tasks = [process_item(item) for item in items]

    # Fan-in: recolectar resultados
    results = await asyncio.gather(*tasks)

    return results

# Uso
items = range(100)
results = asyncio.run(fan_out_fan_in(items))
```

### 3. Pipeline Pattern

```python
from multiprocessing import Process, Queue

def stage1(input_queue, output_queue):
    while True:
        data = input_queue.get()
        if data is None:
            break
        # Procesar
        result = data.upper()
        output_queue.put(result)

def stage2(input_queue, output_queue):
    while True:
        data = input_queue.get()
        if data is None:
            break
        # Procesar
        result = f"[{data}]"
        output_queue.put(result)

# Pipeline
q1 = Queue()
q2 = Queue()
q3 = Queue()

p1 = Process(target=stage1, args=(q1, q2))
p2 = Process(target=stage2, args=(q2, q3))

p1.start()
p2.start()

# Alimentar pipeline
for item in ['hello', 'world']:
    q1.put(item)

q1.put(None)
p1.join()
q2.put(None)
p2.join()

# Recolectar resultados
while not q3.empty():
    print(q3.get())
```

---

## Benchmarking y Profiling

### Python

```python
import cProfile
import pstats

# Profiling
cProfile.run('main()', 'stats.prof')

# Analizar resultados
p = pstats.Stats('stats.prof')
p.sort_stats('cumulative').print_stats(10)
```

### Node.js

```bash
# Ejecutar con profiler
node --prof app.js

# Analizar resultados
node --prof-process isolate-*.log > processed.txt
```

### Docker stats en tiempo real

```bash
# Ver uso de recursos
docker stats

# Específico de un contenedor
docker stats myapp
```

---

## Ejercicios Prácticos

### Ejercicio 1: Image Processing Pipeline
Crea un sistema que:
1. API recibe imágenes
2. Distribuye a workers para procesamiento paralelo
3. Cada worker aplica filtros (blur, resize, etc.)
4. Combina resultados

### Ejercicio 2: Web Scraper Concurrente
- Scrape 1000 URLs concurrentemente
- Usa asyncio (Python) o async/await (Node.js)
- Almacena en PostgreSQL
- Compara vs versión secuencial

### Ejercicio 3: MapReduce Simple
Implementa MapReduce para:
- Contar palabras en múltiples archivos
- Usar multiprocessing (Python) o workers (Node.js)
- Distribuir archivos entre workers

---

## Mejores Prácticas

1. **Usar el modelo correcto**:
   - I/O-bound → Async/await, threading
   - CPU-bound → Multiprocessing, parallel streams

2. **No sobre-paralelizar**:
   - Más threads/processes ≠ más rápido
   - Overhead de context switching
   - Regla: workers ≈ CPUs disponibles

3. **Medir siempre**:
   - Profile antes de optimizar
   - Benchmark secuencial vs paralelo

4. **Considerar contenedores**:
   - Limitar CPUs disponibles
   - Escalar horizontalmente vs verticalmente

5. **Evitar race conditions**:
   - Usar locks, semaphores
   - Prefer message passing over shared memory

---

Este módulo te ha enseñado a aprovechar paralelismo y concurrencia en aplicaciones containerizadas para maximizar el rendimiento.
