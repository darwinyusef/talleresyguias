package main

import "fmt"

/*
TEMA: Channel Directions (Direcciones de Canales)
DESCRIPCIÓN: Los channels pueden ser de solo envío o solo recepción,
mejorando la seguridad de tipos.

CONCEPTOS CLAVE:
- chan<- T: canal de solo envío
- <-chan T: canal de solo recepción
- Conversión automática de bidireccional a unidireccional
*/

// Función que solo envía
func enviar(ch chan<- string, mensaje string) {
	ch <- mensaje
	// No se puede recibir: msg := <-ch (error de compilación)
}

// Función que solo recibe
func recibir(ch <-chan string) string {
	msg := <-ch
	// No se puede enviar: ch <- "algo" (error de compilación)
	return msg
}

// Pipeline: productor -> procesador -> consumidor
func productor(salida chan<- int) {
	for i := 1; i <= 5; i++ {
		salida <- i
	}
	close(salida)
}

func procesador(entrada <-chan int, salida chan<- int) {
	for num := range entrada {
		salida <- num * 2
	}
	close(salida)
}

func consumidor(entrada <-chan int) {
	for num := range entrada {
		fmt.Printf("Consumido: %d\n", num)
	}
}

func main() {
	fmt.Println("=== EJERCICIO 17: Channel Directions ===\n")

	// Ejemplo 1: Canales unidireccionales
	fmt.Println("1. Canales unidireccionales:")
	mensajes := make(chan string)
	
	go enviar(mensajes, "Hola")
	resultado := recibir(mensajes)
	fmt.Printf("Recibido: %s\n", resultado)

	// Ejemplo 2: Pipeline
	fmt.Println("\n2. Pipeline (productor -> procesador -> consumidor):")
	numeros := make(chan int)
	procesados := make(chan int)

	go productor(numeros)
	go procesador(numeros, procesados)
	consumidor(procesados)

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Pipeline de procesamiento de strings
	generarPalabras := func(salida chan<- string) {
		palabras := []string{"go", "es", "genial"}
		for _, palabra := range palabras {
			salida <- palabra
		}
		close(salida)
	}

	convertirMayusculas := func(entrada <-chan string, salida chan<- string) {
		for palabra := range entrada {
			mayuscula := ""
			for _, r := range palabra {
				if r >= 'a' && r <= 'z' {
					mayuscula += string(r - 32)
				} else {
					mayuscula += string(r)
				}
			}
			salida <- mayuscula
		}
		close(salida)
	}

	imprimirPalabras := func(entrada <-chan string) {
		for palabra := range entrada {
			fmt.Printf("  %s\n", palabra)
		}
	}

	fmt.Println("Pipeline de strings:")
	palabras := make(chan string)
	mayusculas := make(chan string)

	go generarPalabras(palabras)
	go convertirMayusculas(palabras, mayusculas)
	imprimirPalabras(mayusculas)
}
