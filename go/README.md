# Ejercicios de Go - Guía Completa

Esta carpeta contiene 20 ejercicios prácticos de Go que cubren conceptos fundamentales y avanzados del lenguaje.

## 📚 Índice de Ejercicios

### Fundamentos
1. **Range over Built-in Types** - Iteración sobre slices, maps y strings
2. **Pointers** - Uso de punteros y paso por referencia
3. **Strings and Runes** - Manejo de strings Unicode y runes
4. **Structs** - Estructuras de datos personalizadas
5. **Methods** - Métodos con receptores por valor y puntero
6. **Interfaces** - Polimorfismo y contratos de comportamiento
7. **Enums** - Enumeraciones con iota y tipos personalizados
8. **Struct Embedding** - Composición de structs

### Características Avanzadas
9. **Generics** - Programación genérica (Go 1.18+)
10. **Range over Iterators** - Iteradores personalizados (Go 1.23+)

### Manejo de Errores
11. **Errors** - Manejo básico de errores
12. **Custom Errors** - Tipos de error personalizados

### Concurrencia
13. **Goroutines** - Ejecución concurrente
14. **Channels** - Comunicación entre goroutines
15. **Channel Buffering** - Canales con buffer
16. **Channel Synchronization** - Sincronización con canales
17. **Channel Directions** - Canales unidireccionales
18. **Select** - Multiplexación de canales
19. **Timeouts** - Timeouts en operaciones
20. **Non-Blocking & Closing** - Operaciones no bloqueantes y cierre de canales

## 🚀 Cómo Usar los Ejercicios

### Requisitos
- Go 1.23 o superior (para ejercicios 9 y 10)
- Go 1.18+ (para el resto)

### Ejecutar un Ejercicio

```bash
# Ejecutar un ejercicio específico
go run 01_range_over_builtin_types.go

# O compilar y ejecutar
go build 01_range_over_builtin_types.go
./01_range_over_builtin_types
```

### Ejecutar Todos los Ejercicios

```bash
# Desde la carpeta go/
for file in *.go; do
    echo "=== Ejecutando $file ==="
    go run "$file"
    echo ""
done
```

## 📖 Estructura de Cada Ejercicio

Cada archivo sigue esta estructura:

```go
/*
TEMA: [Nombre del tema]
DESCRIPCIÓN: [Explicación del concepto]

CONCEPTOS CLAVE:
- Punto clave 1
- Punto clave 2
- Punto clave 3
*/

func main() {
    // Ejemplos demostrativos
    
    // Ejercicio práctico
    ejercicioPractico()
}

func ejercicioPractico() {
    // Código para practicar
}
```

## 🎯 Recomendaciones de Estudio

### Para Principiantes
Sigue este orden:
1. Ejercicios 1-8 (Fundamentos)
2. Ejercicios 11-12 (Errores)
3. Ejercicios 13-20 (Concurrencia)
4. Ejercicios 9-10 (Características avanzadas)

### Para Desarrolladores Intermedios
Enfócate en:
- Ejercicios 6-8 (Interfaces y composición)
- Ejercicios 13-20 (Concurrencia completa)
- Ejercicio 9 (Generics)

### Para Desarrolladores Avanzados
Profundiza en:
- Ejercicio 10 (Iteradores personalizados)
- Ejercicios 17-20 (Patrones avanzados de concurrencia)
- Ejercicio 9 (Generics avanzados)

## 💡 Consejos

1. **Lee los comentarios**: Cada ejercicio tiene explicaciones detalladas
2. **Modifica el código**: Experimenta cambiando valores y comportamientos
3. **Completa los TODOs**: Algunos ejercicios tienen secciones para completar
4. **Ejecuta y observa**: Corre cada ejercicio para ver los resultados
5. **Combina conceptos**: Intenta combinar diferentes técnicas

## 🔧 Solución de Problemas

### Error: "package iter is not in GOROOT"
El ejercicio 10 requiere Go 1.23+. Actualiza tu versión de Go o comenta ese ejercicio.

### Error de compilación en generics
El ejercicio 9 requiere Go 1.18+. Verifica tu versión con:
```bash
go version
```

### Goroutines no se ejecutan
Asegúrate de tener `time.Sleep()` o sincronización apropiada para que las goroutines completen su ejecución.

## 📝 Ejercicios Adicionales

Después de completar los ejercicios, intenta:

1. **Combinar conceptos**: Crea un programa que use structs, interfaces y goroutines
2. **Proyecto mini**: Construye un web scraper concurrente
3. **Sistema de tareas**: Implementa un worker pool con channels
4. **API REST**: Crea un servidor HTTP simple con manejo de errores

## 🌟 Recursos Adicionales

- [Go by Example](https://gobyexample.com/)
- [Effective Go](https://golang.org/doc/effective_go)
- [Go Tour](https://tour.golang.org/)
- [Go Documentation](https://golang.org/doc/)

## 📄 Licencia

Estos ejercicios son de uso educativo libre.

---

**¡Feliz aprendizaje de Go! 🎉**
