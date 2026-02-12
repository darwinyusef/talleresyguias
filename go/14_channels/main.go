package main

import (
	"fmt"
	"time"
)

/*
TEMA: Channels (Canales)
DESCRIPCIÓN: Los channels permiten comunicación entre goroutines.
Son tuberías tipadas para enviar y recibir valores.

CONCEPTOS CLAVE:
- make(chan T) crea un channel
- ch <- valor envía al channel
- valor := <-ch recibe del channel
- Los channels bloquean hasta que hay receptor/emisor
*/

func main() {
	fmt.Println("=== EJERCICIO 14: Channels ===\n")

	// Ejemplo 1: Channel básico
	fmt.Println("1. Channel básico:")
	mensajes := make(chan string)

	go func() {
		mensajes <- "Hola desde goroutine"
	}()

	msg := <-mensajes
	fmt.Printf("Recibido: %s\n", msg)

	// Ejemplo 2: Channel con múltiples mensajes
	fmt.Println("\n2. Múltiples mensajes:")
	numeros := make(chan int)

	go func() {
		for i := 1; i <= 5; i++ {
			numeros <- i
			time.Sleep(100 * time.Millisecond)
		}
		close(numeros)
	}()

	for num := range numeros {
		fmt.Printf("Recibido: %d\n", num)
	}

	// Ejemplo 3: Comunicación bidireccional
	fmt.Println("\n3. Comunicación bidireccional:")
	peticiones := make(chan string)
	respuestas := make(chan string)

	go func() {
		for req := range peticiones {
			respuestas <- fmt.Sprintf("Procesado: %s", req)
		}
	}()

	peticiones <- "Tarea 1"
	fmt.Println(<-respuestas)

	peticiones <- "Tarea 2"
	fmt.Println(<-respuestas)

	close(peticiones)

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Calcular suma en goroutine
	resultado := make(chan int)

	go func() {
		suma := 0
		for i := 1; i <= 100; i++ {
			suma += i
		}
		resultado <- suma
	}()

	fmt.Printf("Suma de 1 a 100: %d\n", <-resultado)
}
