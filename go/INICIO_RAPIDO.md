# 🚀 Inicio Rápido - Ejercicios de Go

## ⚡ Empezar en 3 pasos

### 1️⃣ Verifica tu instalación de Go
```bash
go version
```
Necesitas Go 1.18 o superior (1.23+ para el ejercicio 10).

### 2️⃣ Navega a la carpeta
```bash
cd /Users/yusefgonzalez/proyectos/talleres/go
```

### 3️⃣ Ejecuta tu primer ejercicio
```bash
go run 01_range_over_builtin_types.go
```

## 📋 Comandos Útiles

### Ejecutar un ejercicio específico
```bash
go run 01_range_over_builtin_types.go
go run 13_goroutines.go
go run 18_select.go
```

### Usar el script automatizado
```bash
# Ejecutar ejercicio por número
./run_all.sh 1
./run_all.sh 13

# Ejecutar todos los ejercicios
./run_all.sh
```

### Compilar un ejercicio
```bash
go build 01_range_over_builtin_types.go
./01_range_over_builtin_types
```

## 📚 ¿Por dónde empezar?

### Si eres nuevo en Go
```bash
go run 01_range_over_builtin_types.go  # Iteración básica
go run 02_pointers.go                  # Punteros
go run 04_structs.go                   # Estructuras
go run 05_methods.go                   # Métodos
```

### Si quieres aprender concurrencia
```bash
go run 13_goroutines.go                # Goroutines básicas
go run 14_channels.go                  # Channels
go run 18_select.go                    # Select
go run 19_timeouts.go                  # Timeouts
```

### Si buscas características avanzadas
```bash
go run 06_interfaces.go                # Interfaces
go run 09_generics.go                  # Genéricos
go run 17_channel_directions.go        # Pipelines
```

## 📖 Documentación

- **README.md** - Guía completa y detallada
- **INDICE.md** - Mapa visual y rutas de aprendizaje
- **DESAFIOS.md** - Ejercicios adicionales y proyectos
- **RESUMEN.md** - Resumen del proyecto completo

## 🎯 Ejercicios por Tema

| Tema | Ejercicios |
|------|-----------|
| **Fundamentos** | 01, 02, 03, 04 |
| **OOP en Go** | 05, 06, 07, 08 |
| **Errores** | 11, 12 |
| **Concurrencia** | 13, 14, 15, 16, 17, 18, 19, 20 |
| **Avanzado** | 09, 10 |

## 💡 Tips

1. **Lee los comentarios** - Cada ejercicio tiene explicaciones detalladas
2. **Ejecuta el código** - Ver la salida ayuda a entender
3. **Modifica y experimenta** - Cambia valores y observa qué pasa
4. **Completa los TODOs** - Algunos ejercicios tienen secciones para practicar
5. **Sigue el orden** - Los ejercicios están ordenados por dificultad

## 🐛 Solución de Problemas

### Error: "go: command not found"
Instala Go desde [golang.org/dl](https://golang.org/dl/)

### Error: "package iter is not in GOROOT"
El ejercicio 10 requiere Go 1.23+. Actualiza o sáltalo.

### Las goroutines no se ejecutan
Asegúrate de tener `time.Sleep()` o sincronización apropiada.

## 🎓 Rutas Sugeridas

### Ruta Rápida (2-3 horas)
```
01 → 02 → 04 → 05 → 13 → 14
```

### Ruta Completa Básica (8-10 horas)
```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 11 → 12
```

### Ruta de Concurrencia (6-8 horas)
```
13 → 14 → 15 → 16 → 17 → 18 → 19 → 20
```

### Ruta Completa (20-25 horas)
```
Todos los ejercicios en orden: 01 → 02 → ... → 20
```

## 🌟 Siguiente Nivel

Después de completar los ejercicios:

1. **Revisa DESAFIOS.md** - Ejercicios más complejos
2. **Construye un proyecto** - Aplica lo aprendido
3. **Lee "Effective Go"** - Mejores prácticas
4. **Contribuye a Open Source** - Practica con código real

## 📞 Recursos

- [Go by Example](https://gobyexample.com/)
- [Go Tour](https://tour.golang.org/)
- [Go Documentation](https://golang.org/doc/)
- [Effective Go](https://golang.org/doc/effective_go)

---

**¡Comienza ahora! Ejecuta tu primer ejercicio:**
```bash
go run 01_range_over_builtin_types.go
```

**¡Buena suerte y disfruta aprendiendo Go! 🎉**
