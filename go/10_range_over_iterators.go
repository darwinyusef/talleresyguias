package main

import (
	"fmt"
	"iter"
)

/*
TEMA: Range over Iterators
DESCRIPCIÓN: Go 1.23+ permite crear iteradores personalizados
que funcionan con el operador range.

CONCEPTOS CLAVE:
- iter.Seq[T] para iteradores simples
- iter.Seq2[K, V] para iteradores de pares
- Funciones que retornan iteradores
*/

// Iterador simple que genera números
func Numeros(max int) iter.Seq[int] {
	return func(yield func(int) bool) {
		for i := 0; i < max; i++ {
			if !yield(i) {
				return
			}
		}
	}
}

// Iterador de pares (índice, valor)
func Pares(slice []string) iter.Seq2[int, string] {
	return func(yield func(int, string) bool) {
		for i, v := range slice {
			if !yield(i, v) {
				return
			}
		}
	}
}

func main() {
	fmt.Println("=== EJERCICIO 10: Range over Iterators ===\n")

	// Ejemplo 1: Iterador simple
	fmt.Println("1. Iterador de números:")
	for n := range Numeros(5) {
		fmt.Printf("  %d\n", n)
	}

	// Ejemplo 2: Iterador de pares
	fmt.Println("\n2. Iterador de pares:")
	frutas := []string{"manzana", "banana", "naranja"}
	for i, fruta := range Pares(frutas) {
		fmt.Printf("  %d: %s\n", i, fruta)
	}

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	fmt.Println("Números del 0 al 9:")
	for n := range Numeros(10) {
		fmt.Printf("%d ", n)
	}
	fmt.Println()
}
