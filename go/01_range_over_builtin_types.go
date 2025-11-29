package main

import "fmt"

/*
TEMA: Range over Built-in Types
DESCRIPCIÓN: El operador 'range' permite iterar sobre diferentes tipos de datos
como slices, arrays, maps, strings y channels.

CONCEPTOS CLAVE:
- range devuelve índice y valor para slices/arrays
- range devuelve clave y valor para maps
- range devuelve índice y rune para strings
*/

func main() {
	fmt.Println("=== EJERCICIO 1: Range over Built-in Types ===\n")

	// Ejemplo 1: Range sobre slice
	fmt.Println("1. Range sobre Slice:")
	numbers := []int{10, 20, 30, 40, 50}
	for index, value := range numbers {
		fmt.Printf("   Índice: %d, Valor: %d\n", index, value)
	}

	// Ejemplo 2: Range sobre map
	fmt.Println("\n2. Range sobre Map:")
	colors := map[string]string{
		"red":   "rojo",
		"blue":  "azul",
		"green": "verde",
	}
	for key, value := range colors {
		fmt.Printf("   %s = %s\n", key, value)
	}

	// Ejemplo 3: Range sobre string (itera sobre runes)
	fmt.Println("\n3. Range sobre String:")
	text := "Hola 世界"
	for index, runeValue := range text {
		fmt.Printf("   Posición %d: %c (Unicode: %U)\n", index, runeValue, runeValue)
	}

	// Ejemplo 4: Range solo con índice
	fmt.Println("\n4. Range solo con índice:")
	for i := range numbers {
		fmt.Printf("   Índice: %d\n", i)
	}

	// EJERCICIO PRÁCTICO:
	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

// TODO: Completa esta función
func ejercicioPractico() {
	// 1. Crea un slice de strings con nombres de frutas
	frutas := []string{"manzana", "banana", "naranja", "uva", "pera"}

	// 2. Usa range para imprimir cada fruta con su posición
	fmt.Println("Lista de frutas:")
	for i, fruta := range frutas {
		fmt.Printf("   %d. %s\n", i+1, fruta)
	}

	// 3. Crea un map de productos con sus precios
	productos := map[string]float64{
		"laptop":  1200.50,
		"mouse":   25.99,
		"teclado": 75.00,
	}

	// 4. Calcula el total de todos los productos
	var total float64
	for _, precio := range productos {
		total += precio
	}
	fmt.Printf("\nTotal de productos: $%.2f\n", total)

	// 5. DESAFÍO: Encuentra el producto más caro
	var productoMasCaro string
	var precioMaximo float64
	for producto, precio := range productos {
		if precio > precioMaximo {
			precioMaximo = precio
			productoMasCaro = producto
		}
	}
	fmt.Printf("Producto más caro: %s ($%.2f)\n", productoMasCaro, precioMaximo)
}
