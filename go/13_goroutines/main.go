package main

import (
	"fmt"
	"time"
)

/*
TEMA: Goroutines
DESCRIPCIÓN: Las goroutines son funciones que se ejecutan concurrentemente.
Son ligeras y manejadas por el runtime de Go.

CONCEPTOS CLAVE:
- go keyword para lanzar goroutine
- Ejecución concurrente
- time.Sleep para sincronización básica
*/

func decir(texto string, veces int) {
	for i := 0; i < veces; i++ {
		fmt.Printf("%s %d\n", texto, i+1)
		time.Sleep(100 * time.Millisecond)
	}
}

func contar(nombre string, hasta int) {
	for i := 1; i <= hasta; i++ {
		fmt.Printf("%s: %d\n", nombre, i)
		time.Sleep(200 * time.Millisecond)
	}
}

func main() {
	fmt.Println("=== EJERCICIO 13: Goroutines ===\n")

	// Ejemplo 1: Goroutine básica
	fmt.Println("1. Goroutine básica:")
	go decir("Hola", 3)
	decir("Mundo", 3)

	// Ejemplo 2: Múltiples goroutines
	fmt.Println("\n2. Múltiples goroutines:")
	go contar("A", 5)
	go contar("B", 5)
	go contar("C", 5)
	
	time.Sleep(2 * time.Second)

	// Ejemplo 3: Función anónima como goroutine
	fmt.Println("\n3. Función anónima:")
	go func() {
		for i := 0; i < 3; i++ {
			fmt.Printf("Goroutine anónima: %d\n", i)
			time.Sleep(150 * time.Millisecond)
		}
	}()

	time.Sleep(1 * time.Second)

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Lanzar varias goroutines que impriman números
	fmt.Println("Contadores concurrentes:")
	
	for i := 1; i <= 3; i++ {
		id := i
		go func() {
			for j := 1; j <= 3; j++ {
				fmt.Printf("  Goroutine %d: %d\n", id, j)
				time.Sleep(100 * time.Millisecond)
			}
		}()
	}

	time.Sleep(1 * time.Second)
	fmt.Println("Fin del ejercicio")
}
