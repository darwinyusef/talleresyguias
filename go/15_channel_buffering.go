package main

import (
	"fmt"
	"time"
)

/*
TEMA: Channel Buffering (Canales con Buffer)
DESCRIPCIÓN: Los channels pueden tener un buffer que permite enviar
valores sin bloquear hasta que el buffer esté lleno.

CONCEPTOS CLAVE:
- make(chan T, capacidad) crea channel con buffer
- No bloquea hasta que el buffer está lleno
- Útil para desacoplar productor/consumidor
*/

func main() {
	fmt.Println("=== EJERCICIO 15: Channel Buffering ===\n")

	// Ejemplo 1: Channel sin buffer (bloquea inmediatamente)
	fmt.Println("1. Channel sin buffer:")
	ch1 := make(chan string)
	
	go func() {
		time.Sleep(500 * time.Millisecond)
		fmt.Println("Recibiendo del channel sin buffer...")
		msg := <-ch1
		fmt.Printf("Recibido: %s\n", msg)
	}()
	
	fmt.Println("Enviando al channel sin buffer (bloqueará)...")
	ch1 <- "Mensaje 1"
	fmt.Println("Enviado!")

	// Ejemplo 2: Channel con buffer
	fmt.Println("\n2. Channel con buffer:")
	ch2 := make(chan string, 2)
	
	fmt.Println("Enviando al channel con buffer...")
	ch2 <- "Mensaje 1"
	fmt.Println("Mensaje 1 enviado (no bloqueó)")
	ch2 <- "Mensaje 2"
	fmt.Println("Mensaje 2 enviado (no bloqueó)")
	
	fmt.Println("Recibiendo mensajes:")
	fmt.Println(<-ch2)
	fmt.Println(<-ch2)

	// Ejemplo 3: Buffer lleno
	fmt.Println("\n3. Productor-Consumidor con buffer:")
	trabajos := make(chan int, 3)
	
	// Productor
	go func() {
		for i := 1; i <= 5; i++ {
			fmt.Printf("Enviando trabajo %d\n", i)
			trabajos <- i
			time.Sleep(100 * time.Millisecond)
		}
		close(trabajos)
	}()
	
	// Consumidor
	time.Sleep(500 * time.Millisecond)
	for trabajo := range trabajos {
		fmt.Printf("  Procesando trabajo %d\n", trabajo)
		time.Sleep(200 * time.Millisecond)
	}

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Channel con buffer de 5
	numeros := make(chan int, 5)
	
	// Enviar números sin bloquear
	fmt.Println("Enviando números al buffer:")
	for i := 1; i <= 5; i++ {
		numeros <- i
		fmt.Printf("  Enviado: %d\n", i)
	}
	
	close(numeros)
	
	// Recibir todos los números
	fmt.Println("Recibiendo números del buffer:")
	for num := range numeros {
		fmt.Printf("  Recibido: %d\n", num)
	}
}
