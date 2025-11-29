# 🏆 Desafíos Adicionales

Después de completar los 20 ejercicios básicos, intenta estos desafíos para profundizar tu conocimiento.

## 🎯 Desafíos por Nivel

### 🟢 Nivel Básico

#### Desafío 1: Calculadora de Estadísticas
Crea un programa que:
- Acepte un slice de números
- Calcule: promedio, mediana, moda, desviación estándar
- Use structs para organizar los resultados
- Implemente métodos para cada cálculo

**Conceptos**: Structs, Methods, Slices

#### Desafío 2: Sistema de Biblioteca
Implementa:
- Struct `Libro` con título, autor, ISBN, disponible
- Struct `Biblioteca` que contenga slice de libros
- Métodos: agregar libro, buscar por título, prestar, devolver
- Manejo de errores cuando un libro no está disponible

**Conceptos**: Structs, Methods, Errors, Slices

#### Desafío 3: Conversor de Unidades
Crea:
- Interface `Convertible` con método `ConvertirA(unidad string) float64`
- Tipos: `Temperatura`, `Distancia`, `Peso`
- Implementa conversiones (Celsius/Fahrenheit, km/millas, kg/libras)

**Conceptos**: Interfaces, Methods, Structs

### 🟡 Nivel Intermedio

#### Desafío 4: Sistema de Tareas con Prioridades
Implementa:
- Enum para prioridades (Baja, Media, Alta, Urgente)
- Struct `Tarea` con título, descripción, prioridad, completada
- Struct `GestorTareas` que maneje una lista de tareas
- Métodos: agregar, completar, filtrar por prioridad, ordenar
- Persistencia en archivo JSON

**Conceptos**: Enums, Structs, Methods, File I/O, JSON

#### Desafío 5: Web Scraper Simple
Crea un scraper que:
- Use goroutines para hacer múltiples requests HTTP
- Use channels para recolectar resultados
- Implemente timeout para cada request
- Maneje errores de red apropiadamente
- Guarde resultados en un archivo

**Conceptos**: Goroutines, Channels, Timeouts, Errors, HTTP

#### Desafío 6: Cache Concurrente
Implementa un cache thread-safe:
- Usa map para almacenar datos
- Implementa mutex para sincronización
- Métodos: Get, Set, Delete, Clear
- TTL (Time To Live) para entradas
- Limpieza automática de entradas expiradas con goroutine

**Conceptos**: Concurrency, Sync, Maps, Goroutines

### 🔴 Nivel Avanzado

#### Desafío 7: Worker Pool
Implementa un pool de workers:
- N workers procesando tareas concurrentemente
- Channel de trabajos con buffer
- Channel de resultados
- Manejo de errores por trabajo
- Estadísticas: trabajos procesados, errores, tiempo promedio
- Graceful shutdown

**Conceptos**: Goroutines, Channels, Synchronization, Select

```go
type Trabajo struct {
    ID   int
    Datos interface{}
}

type Resultado struct {
    TrabajoID int
    Resultado interface{}
    Error     error
}

type WorkerPool struct {
    NumWorkers int
    Trabajos   chan Trabajo
    Resultados chan Resultado
}
```

#### Desafío 8: Rate Limiter
Crea un rate limiter genérico:
- Limita número de operaciones por segundo
- Usa channels y time.Ticker
- Implementa diferentes estrategias (token bucket, sliding window)
- Soporte para burst (ráfagas)
- Interface genérica para cualquier tipo de operación

**Conceptos**: Generics, Channels, Time, Interfaces

#### Desafío 9: Pipeline de Procesamiento
Implementa un pipeline de datos:
- Múltiples etapas de procesamiento
- Cada etapa es una goroutine
- Usa channel directions apropiadamente
- Manejo de errores en cada etapa
- Cancelación con context
- Métricas de rendimiento

**Conceptos**: Channels, Channel Directions, Context, Goroutines

```go
// Ejemplo de estructura:
Leer Archivos → Parsear → Transformar → Validar → Guardar
```

#### Desafío 10: Sistema de Eventos
Crea un event bus:
- Publicación/suscripción de eventos
- Múltiples suscriptores por evento
- Eventos tipados con generics
- Procesamiento asíncrono
- Prioridades de eventos
- Filtros de eventos

**Conceptos**: Generics, Interfaces, Channels, Goroutines

## 🚀 Proyectos Completos

### Proyecto 1: API REST de Tareas
**Tiempo estimado: 8-10 horas**

Crea una API REST completa:
- CRUD de tareas
- Autenticación JWT
- Base de datos (SQLite o PostgreSQL)
- Middleware para logging y autenticación
- Validación de datos
- Tests unitarios y de integración
- Documentación con Swagger

**Stack sugerido**: net/http, gorilla/mux, gorm, jwt-go

### Proyecto 2: Chat en Tiempo Real
**Tiempo estimado: 10-12 horas**

Implementa un servidor de chat:
- WebSockets para comunicación en tiempo real
- Múltiples salas de chat
- Mensajes privados
- Historial de mensajes
- Usuarios en línea
- Broadcast de mensajes
- Manejo de desconexiones

**Stack sugerido**: gorilla/websocket, channels, goroutines

### Proyecto 3: Sistema de Monitoreo
**Tiempo estimado: 12-15 horas**

Crea un sistema de monitoreo:
- Recolección de métricas del sistema (CPU, RAM, disco)
- Múltiples agentes enviando datos
- Servidor central agregando datos
- Alertas basadas en umbrales
- Dashboard web en tiempo real
- Almacenamiento de series temporales
- Gráficos y visualizaciones

**Stack sugerido**: prometheus client, websockets, time series DB

### Proyecto 4: CLI Tool Avanzado
**Tiempo estimado: 6-8 horas**

Desarrolla una herramienta CLI:
- Múltiples subcomandos
- Flags y argumentos
- Configuración desde archivo
- Procesamiento paralelo de archivos
- Progress bars
- Colores en terminal
- Auto-completado

**Stack sugerido**: cobra, viper, color, progressbar

## 📝 Ejercicios de Refactoring

### Ejercicio R1: Mejorar Código Legacy
Toma este código y mejóralo:

```go
// Código "malo"
func procesarDatos(d []string) []string {
    var r []string
    for i := 0; i < len(d); i++ {
        if len(d[i]) > 0 {
            r = append(r, d[i])
        }
    }
    return r
}
```

Mejoras a implementar:
- Nombres descriptivos
- Usar range
- Agregar documentación
- Manejar casos edge
- Agregar tests

### Ejercicio R2: Aplicar Patrones
Refactoriza usando patrones de diseño:
- Builder pattern para construcción de objetos complejos
- Strategy pattern para diferentes algoritmos
- Observer pattern para notificaciones
- Factory pattern para creación de objetos

## 🎓 Recursos para Continuar

### Libros
- "The Go Programming Language" - Donovan & Kernighan
- "Concurrency in Go" - Katherine Cox-Buday
- "Go in Action" - William Kennedy

### Cursos Online
- [Go by Example](https://gobyexample.com/)
- [Tour of Go](https://tour.golang.org/)
- [Effective Go](https://golang.org/doc/effective_go)

### Práctica
- [Exercism Go Track](https://exercism.org/tracks/go)
- [LeetCode Go Problems](https://leetcode.com/)
- [HackerRank Go](https://www.hackerrank.com/domains/go)

### Comunidad
- [Go Forum](https://forum.golangbridge.org/)
- [Reddit r/golang](https://reddit.com/r/golang)
- [Gophers Slack](https://gophers.slack.com/)

## 🏅 Certificaciones y Validación

Considera obtener:
- Go Developer Certification (en desarrollo por Go team)
- Contribuir a proyectos Open Source en Go
- Crear tu propio paquete Go y publicarlo

---

**¡Sigue practicando y construyendo! 🚀**
