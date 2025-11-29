package main

import "fmt"

/*
TEMA: Generics (Genéricos)
DESCRIPCIÓN: Go 1.18+ soporta genéricos, permitiendo escribir funciones
y tipos que funcionan con cualquier tipo.

CONCEPTOS CLAVE:
- Type parameters con []
- Constraints (any, comparable, etc.)
- Funciones y tipos genéricos
*/

// Función genérica simple
func Imprimir[T any](valor T) {
	fmt.Printf("Valor: %v (tipo: %T)\n", valor, valor)
}

// Función genérica con slice
func Primero[T any](slice []T) T {
	if len(slice) == 0 {
		var zero T
		return zero
	}
	return slice[0]
}

// Función con constraint comparable
func Contiene[T comparable](slice []T, valor T) bool {
	for _, v := range slice {
		if v == valor {
			return true
		}
	}
	return false
}

// Tipo genérico
type Pila[T any] struct {
	elementos []T
}

func (p *Pila[T]) Push(valor T) {
	p.elementos = append(p.elementos, valor)
}

func (p *Pila[T]) Pop() (T, bool) {
	if len(p.elementos) == 0 {
		var zero T
		return zero, false
	}
	ultimo := p.elementos[len(p.elementos)-1]
	p.elementos = p.elementos[:len(p.elementos)-1]
	return ultimo, true
}

func main() {
	fmt.Println("=== EJERCICIO 9: Generics ===\n")

	// Ejemplo 1: Función genérica
	fmt.Println("1. Función genérica Imprimir:")
	Imprimir(42)
	Imprimir("Hola")
	Imprimir(3.14)

	// Ejemplo 2: Función con slices
	fmt.Println("\n2. Función Primero:")
	nums := []int{10, 20, 30}
	fmt.Printf("Primero: %d\n", Primero(nums))
	
	palabras := []string{"Go", "es", "genial"}
	fmt.Printf("Primero: %s\n", Primero(palabras))

	// Ejemplo 3: Función Contiene
	fmt.Println("\n3. Función Contiene:")
	fmt.Printf("¿Contiene 20? %t\n", Contiene(nums, 20))
	fmt.Printf("¿Contiene 99? %t\n", Contiene(nums, 99))

	// Ejemplo 4: Tipo genérico Pila
	fmt.Println("\n4. Pila genérica:")
	pila := &Pila[string]{}
	pila.Push("primero")
	pila.Push("segundo")
	pila.Push("tercero")
	
	for {
		valor, ok := pila.Pop()
		if !ok {
			break
		}
		fmt.Printf("Pop: %s\n", valor)
	}

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Pila de enteros
	pilaInt := &Pila[int]{}
	pilaInt.Push(1)
	pilaInt.Push(2)
	pilaInt.Push(3)
	
	fmt.Println("Pila de enteros:")
	for {
		v, ok := pilaInt.Pop()
		if !ok {
			break
		}
		fmt.Printf("  %d\n", v)
	}
}
