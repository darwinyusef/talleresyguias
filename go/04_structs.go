package main

import "fmt"

/*
TEMA: Structs
DESCRIPCIÓN: Los structs son tipos de datos compuestos que agrupan
campos relacionados bajo un mismo tipo.

CONCEPTOS CLAVE:
- struct define un tipo personalizado con campos
- Inicialización con valores literales
- Acceso a campos con notación de punto
- Structs anidados
*/

// Definición de structs
type Persona struct {
	Nombre string
	Edad   int
	Email  string
}

type Direccion struct {
	Calle  string
	Ciudad string
	CP     string
}

type Empleado struct {
	Persona   // Embedding (veremos más en ejercicio 8)
	Direccion Direccion
	Salario   float64
	Activo    bool
}

func main() {
	fmt.Println("=== EJERCICIO 4: Structs ===\n")

	// Ejemplo 1: Creación básica de struct
	fmt.Println("1. Creación básica:")
	p1 := Persona{
		Nombre: "Ana García",
		Edad:   28,
		Email:  "ana@example.com",
	}
	fmt.Printf("   %+v\n", p1)

	// Ejemplo 2: Creación sin nombres de campo (orden importa)
	fmt.Println("\n2. Creación sin nombres de campo:")
	p2 := Persona{"Carlos López", 35, "carlos@example.com"}
	fmt.Printf("   %+v\n", p2)

	// Ejemplo 3: Struct vacío y asignación de campos
	fmt.Println("\n3. Struct vacío:")
	var p3 Persona
	p3.Nombre = "María Rodríguez"
	p3.Edad = 42
	p3.Email = "maria@example.com"
	fmt.Printf("   %+v\n", p3)

	// Ejemplo 4: Struct anidado
	fmt.Println("\n4. Struct anidado:")
	emp := Empleado{
		Persona: Persona{
			Nombre: "Juan Pérez",
			Edad:   30,
			Email:  "juan@company.com",
		},
		Direccion: Direccion{
			Calle:  "Av. Principal 123",
			Ciudad: "Madrid",
			CP:     "28001",
		},
		Salario: 45000.00,
		Activo:  true,
	}
	fmt.Printf("   %+v\n", emp)
	fmt.Printf("   Nombre: %s\n", emp.Persona.Nombre)
	fmt.Printf("   Ciudad: %s\n", emp.Direccion.Ciudad)

	// Ejemplo 5: Punteros a structs
	fmt.Println("\n5. Punteros a structs:")
	punteroPersona := &p1
	punteroPersona.Edad = 29 // Go permite acceso directo sin desreferenciar
	fmt.Printf("   %+v\n", p1)

	// EJERCICIO PRÁCTICO:
	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

// TODO: Completa esta función
func ejercicioPractico() {
	// 1. Define un struct Libro con título, autor, año y precio
	// (Ver definición global abajo)

	// 2. Crea una biblioteca con varios libros
	biblioteca := []Libro{
		{"El Quijote", "Cervantes", 1605, 25.50},
		{"Cien Años de Soledad", "García Márquez", 1967, 30.00},
		{"1984", "George Orwell", 1949, 22.75},
	}

	// 3. Imprime todos los libros
	fmt.Println("Biblioteca:")
	for i, libro := range biblioteca {
		fmt.Printf("%d. %s por %s (%d) - $%.2f\n",
			i+1, libro.Titulo, libro.Autor, libro.Anio, libro.Precio)
	}

	// 4. DESAFÍO: Encuentra el libro más caro
	libroMasCaro := encontrarLibroMasCaro(biblioteca)
	fmt.Printf("\nLibro más caro: %s ($%.2f)\n", libroMasCaro.Titulo, libroMasCaro.Precio)

	// 5. DESAFÍO: Calcula el precio promedio
	promedio := calcularPrecioPromedio(biblioteca)
	fmt.Printf("Precio promedio: $%.2f\n", promedio)
}

type Libro struct {
	Titulo string
	Autor  string
	Anio   int
	Precio float64
}

func encontrarLibroMasCaro(libros []Libro) Libro {
	if len(libros) == 0 {
		return Libro{}
	}
	masCaro := libros[0]
	for _, libro := range libros {
		if libro.Precio > masCaro.Precio {
			masCaro = libro
		}
	}
	return masCaro
}

func calcularPrecioPromedio(libros []Libro) float64 {
	if len(libros) == 0 {
		return 0
	}
	var total float64
	for _, libro := range libros {
		total += libro.Precio
	}
	return total / float64(len(libros))
}
