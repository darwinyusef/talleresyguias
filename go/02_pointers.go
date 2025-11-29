package main

import "fmt"

/*
TEMA: Pointers (Punteros)
DESCRIPCIÓN: Los punteros almacenan la dirección de memoria de una variable.
Permiten modificar valores directamente en memoria y evitar copias innecesarias.

CONCEPTOS CLAVE:
- & obtiene la dirección de memoria de una variable
- * desreferencia un puntero (accede al valor)
- Los punteros permiten modificar valores en funciones
*/

func main() {
	fmt.Println("=== EJERCICIO 2: Pointers ===\n")

	// Ejemplo 1: Declaración básica de punteros
	fmt.Println("1. Punteros básicos:")
	x := 42
	var p *int = &x // p apunta a x
	fmt.Printf("   Valor de x: %d\n", x)
	fmt.Printf("   Dirección de x: %p\n", &x)
	fmt.Printf("   Valor de p (dirección): %p\n", p)
	fmt.Printf("   Valor apuntado por p: %d\n", *p)

	// Ejemplo 2: Modificar valor a través de puntero
	fmt.Println("\n2. Modificar valor con puntero:")
	*p = 100
	fmt.Printf("   Nuevo valor de x: %d\n", x)

	// Ejemplo 3: Punteros en funciones
	fmt.Println("\n3. Punteros en funciones:")
	num := 10
	fmt.Printf("   Antes: %d\n", num)
	incrementarPorValor(num)
	fmt.Printf("   Después de incrementarPorValor: %d\n", num)
	incrementarPorReferencia(&num)
	fmt.Printf("   Después de incrementarPorReferencia: %d\n", num)

	// EJERCICIO PRÁCTICO:
	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

// Función que recibe copia del valor (no modifica el original)
func incrementarPorValor(n int) {
	n++
	fmt.Printf("   Dentro de incrementarPorValor: %d\n", n)
}

// Función que recibe puntero (modifica el original)
func incrementarPorReferencia(n *int) {
	*n++
	fmt.Printf("   Dentro de incrementarPorReferencia: %d\n", *n)
}

// TODO: Completa esta función
func ejercicioPractico() {
	// 1. Crea una función que intercambie dos valores usando punteros
	a, b := 5, 10
	fmt.Printf("Antes del swap: a=%d, b=%d\n", a, b)
	swap(&a, &b)
	fmt.Printf("Después del swap: a=%d, b=%d\n", a, b)

	// 2. Crea una función que duplique un valor usando puntero
	valor := 7
	fmt.Printf("\nValor original: %d\n", valor)
	duplicar(&valor)
	fmt.Printf("Valor duplicado: %d\n", valor)

	// 3. DESAFÍO: Crea una función que reinicie un contador a cero
	contador := 99
	fmt.Printf("\nContador antes: %d\n", contador)
	reiniciar(&contador)
	fmt.Printf("Contador después: %d\n", contador)
}

func swap(x, y *int) {
	temp := *x
	*x = *y
	*y = temp
}

func duplicar(n *int) {
	*n = *n * 2
}

func reiniciar(n *int) {
	*n = 0
}
