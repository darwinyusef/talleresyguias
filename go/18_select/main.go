package main

import (
	"fmt"
	"time"
)

/*
TEMA: Select
DESCRIPCIÓN: Select permite esperar en múltiples operaciones de channels.
Es como un switch para channels.

CONCEPTOS CLAVE:
- select espera en múltiples channels
- Ejecuta el primer case que esté listo
- default para operaciones no bloqueantes
*/

func main() {
	fmt.Println("=== EJERCICIO 18: Select ===\n")

	// Ejemplo 1: Select básico
	fmt.Println("1. Select básico:")
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		time.Sleep(1 * time.Second)
		ch1 <- "Canal 1"
	}()

	go func() {
		time.Sleep(500 * time.Millisecond)
		ch2 <- "Canal 2"
	}()

	for i := 0; i < 2; i++ {
		select {
		case msg1 := <-ch1:
			fmt.Printf("Recibido de ch1: %s\n", msg1)
		case msg2 := <-ch2:
			fmt.Printf("Recibido de ch2: %s\n", msg2)
		}
	}

	// Ejemplo 2: Select con default
	fmt.Println("\n2. Select con default (no bloqueante):")
	mensajes := make(chan string)
	señales := make(chan bool)

	select {
	case msg := <-mensajes:
		fmt.Printf("Mensaje recibido: %s\n", msg)
	default:
		fmt.Println("No hay mensajes disponibles")
	}

	// Ejemplo 3: Select con timeout
	fmt.Println("\n3. Select con timeout:")
	ch3 := make(chan string)

	go func() {
		time.Sleep(2 * time.Second)
		ch3 <- "Resultado"
	}()

	select {
	case res := <-ch3:
		fmt.Printf("Recibido: %s\n", res)
	case <-time.After(1 * time.Second):
		fmt.Println("Timeout: operación tardó demasiado")
	}

	// Ejemplo 4: Select en loop
	fmt.Println("\n4. Select en loop:")
	tick := time.Tick(200 * time.Millisecond)
	boom := time.After(1 * time.Second)

	for {
		select {
		case <-tick:
			fmt.Println("  tick.")
		case <-boom:
			fmt.Println("  BOOM!")
			goto fin
		}
	}
fin:

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Simular múltiples fuentes de datos
	fuente1 := make(chan int)
	fuente2 := make(chan int)
	fuente3 := make(chan int)

	go func() {
		for i := 0; i < 3; i++ {
			time.Sleep(300 * time.Millisecond)
			fuente1 <- i * 10
		}
		close(fuente1)
	}()

	go func() {
		for i := 0; i < 3; i++ {
			time.Sleep(500 * time.Millisecond)
			fuente2 <- i * 100
		}
		close(fuente2)
	}()

	go func() {
		for i := 0; i < 3; i++ {
			time.Sleep(200 * time.Millisecond)
			fuente3 <- i
		}
		close(fuente3)
	}()

	activos := 3
	for activos > 0 {
		select {
		case val, ok := <-fuente1:
			if ok {
				fmt.Printf("Fuente 1: %d\n", val)
			} else {
				fuente1 = nil
				activos--
			}
		case val, ok := <-fuente2:
			if ok {
				fmt.Printf("Fuente 2: %d\n", val)
			} else {
				fuente2 = nil
				activos--
			}
		case val, ok := <-fuente3:
			if ok {
				fmt.Printf("Fuente 3: %d\n", val)
			} else {
				fuente3 = nil
				activos--
			}
		}
	}
}
