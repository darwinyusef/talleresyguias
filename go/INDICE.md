# Índice Visual de Ejercicios Go

## 🎯 Mapa de Aprendizaje

```
FUNDAMENTOS
├── 01 📊 Range over Built-in Types
│   └── Iteración sobre slices, maps, strings
├── 02 👉 Pointers
│   └── Direcciones de memoria y referencias
├── 03 📝 Strings and Runes
│   └── Unicode y manipulación de texto
├── 04 🏗️  Structs
│   └── Estructuras de datos personalizadas
├── 05 🔧 Methods
│   └── Métodos con receptores
├── 06 🔌 Interfaces
│   └── Polimorfismo y contratos
├── 07 🔢 Enums
│   └── Enumeraciones con iota
└── 08 🧩 Struct Embedding
    └── Composición de tipos

CARACTERÍSTICAS AVANZADAS
├── 09 🎁 Generics
│   └── Programación genérica (Go 1.18+)
└── 10 🔄 Range over Iterators
    └── Iteradores personalizados (Go 1.23+)

MANEJO DE ERRORES
├── 11 ⚠️  Errors
│   └── Manejo básico de errores
└── 12 🎨 Custom Errors
    └── Tipos de error personalizados

CONCURRENCIA
├── 13 🚀 Goroutines
│   └── Ejecución concurrente
├── 14 📡 Channels
│   └── Comunicación entre goroutines
├── 15 📦 Channel Buffering
│   └── Canales con buffer
├── 16 🔗 Channel Synchronization
│   └── Sincronización con canales
├── 17 ➡️  Channel Directions
│   └── Canales unidireccionales
├── 18 🎛️  Select
│   └── Multiplexación de canales
├── 19 ⏱️  Timeouts
│   └── Límites de tiempo
└── 20 🚪 Non-Blocking & Closing
    └── Operaciones no bloqueantes
```

## 📊 Nivel de Dificultad

| Nivel | Ejercicios |
|-------|-----------|
| 🟢 Básico | 01, 02, 03, 04, 11 |
| 🟡 Intermedio | 05, 06, 07, 08, 12, 13, 14, 15 |
| 🔴 Avanzado | 09, 10, 16, 17, 18, 19, 20 |

## 🎓 Rutas de Aprendizaje

### Ruta 1: Principiante Total
```
01 → 02 → 03 → 04 → 05 → 11 → 06 → 07
```
*Tiempo estimado: 8-10 horas*

### Ruta 2: Concurrencia desde Cero
```
01 → 02 → 04 → 13 → 14 → 15 → 16 → 18 → 19 → 20
```
*Tiempo estimado: 10-12 horas*

### Ruta 3: Características Modernas
```
04 → 05 → 06 → 09 → 10 → 17
```
*Tiempo estimado: 6-8 horas*

### Ruta 4: Maestría Completa
```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 →
09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 →
17 → 18 → 19 → 20
```
*Tiempo estimado: 20-25 horas*

## 🔍 Búsqueda Rápida por Concepto

| Concepto | Ejercicios |
|----------|-----------|
| **Tipos de datos** | 01, 03, 04 |
| **Punteros y memoria** | 02, 05 |
| **Composición** | 06, 08 |
| **Errores** | 11, 12 |
| **Concurrencia básica** | 13, 14 |
| **Concurrencia avanzada** | 15, 16, 17, 18, 19, 20 |
| **Características Go 1.18+** | 09 |
| **Características Go 1.23+** | 10 |

## 💻 Comandos Rápidos

```bash
# Ejecutar un ejercicio específico
go run 01_range_over_builtin_types.go

# Ejecutar con el script (un ejercicio)
./run_all.sh 1

# Ejecutar todos los ejercicios
./run_all.sh

# Ver solo la estructura de un ejercicio
head -n 20 01_range_over_builtin_types.go

# Buscar un concepto específico
grep -r "goroutine" *.go
```

## 🎯 Objetivos de Aprendizaje

### Al completar estos ejercicios, podrás:

✅ Entender los tipos de datos fundamentales de Go  
✅ Trabajar con punteros y gestión de memoria  
✅ Crear y usar structs e interfaces  
✅ Implementar composición de tipos  
✅ Manejar errores de forma idiomática  
✅ Escribir código concurrente con goroutines  
✅ Comunicar goroutines con channels  
✅ Implementar patrones de concurrencia avanzados  
✅ Usar características modernas de Go (generics, iterators)  
✅ Escribir código Go limpio y eficiente  

## 📈 Progreso Sugerido

Marca tu progreso:

- [ ] Ejercicio 01 - Range over Built-in Types
- [ ] Ejercicio 02 - Pointers
- [ ] Ejercicio 03 - Strings and Runes
- [ ] Ejercicio 04 - Structs
- [ ] Ejercicio 05 - Methods
- [ ] Ejercicio 06 - Interfaces
- [ ] Ejercicio 07 - Enums
- [ ] Ejercicio 08 - Struct Embedding
- [ ] Ejercicio 09 - Generics
- [ ] Ejercicio 10 - Range over Iterators
- [ ] Ejercicio 11 - Errors
- [ ] Ejercicio 12 - Custom Errors
- [ ] Ejercicio 13 - Goroutines
- [ ] Ejercicio 14 - Channels
- [ ] Ejercicio 15 - Channel Buffering
- [ ] Ejercicio 16 - Channel Synchronization
- [ ] Ejercicio 17 - Channel Directions
- [ ] Ejercicio 18 - Select
- [ ] Ejercicio 19 - Timeouts
- [ ] Ejercicio 20 - Non-Blocking & Closing

## 🌟 Próximos Pasos

Después de completar todos los ejercicios:

1. **Proyecto Personal**: Construye una aplicación completa
2. **Contribuye a Open Source**: Participa en proyectos Go
3. **Profundiza**: Lee "Effective Go" y "The Go Programming Language"
4. **Practica**: Resuelve problemas en plataformas como LeetCode o HackerRank

---

**¡Disfruta aprendiendo Go! 🎉**
