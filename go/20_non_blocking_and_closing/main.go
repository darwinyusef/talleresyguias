package main

import (
	"fmt"
	"time"
)

/*
TEMA: Non-Blocking Channel Operations & Closing Channels
DESCRIPCIÓN: Operaciones no bloqueantes usando select con default,
y cierre apropiado de channels.

CONCEPTOS CLAVE:
- select con default para operaciones no bloqueantes
- close(ch) para cerrar un channel
- Verificar si un channel está cerrado con val, ok := <-ch
- Solo el emisor debe cerrar channels
*/

func main() {
	fmt.Println("=== EJERCICIO 20: Non-Blocking & Closing Channels ===\n")

	// Ejemplo 1: Envío no bloqueante
	fmt.Println("1. Envío no bloqueante:")
	mensajes := make(chan string)

	select {
	case mensajes <- "Mensaje":
		fmt.Println("Mensaje enviado")
	default:
		fmt.Println("No se pudo enviar (no hay receptor)")
	}

	// Ejemplo 2: Recepción no bloqueante
	fmt.Println("\n2. Recepción no bloqueante:")
	select {
	case msg := <-mensajes:
		fmt.Printf("Mensaje recibido: %s\n", msg)
	default:
		fmt.Println("No hay mensajes disponibles")
	}

	// Ejemplo 3: Cerrar channels
	fmt.Println("\n3. Cerrar channels:")
	trabajos := make(chan int, 5)

	// Enviar trabajos
	for i := 1; i <= 3; i++ {
		trabajos <- i
	}
	close(trabajos) // Cerrar cuando no hay más trabajos

	// Recibir hasta que se cierre
	for trabajo := range trabajos {
		fmt.Printf("Trabajo: %d\n", trabajo)
	}

	// Ejemplo 4: Verificar si channel está cerrado
	fmt.Println("\n4. Verificar cierre:")
	numeros := make(chan int, 2)
	numeros <- 1
	numeros <- 2
	close(numeros)

	for {
		num, ok := <-numeros
		if !ok {
			fmt.Println("Channel cerrado")
			break
		}
		fmt.Printf("Número: %d\n", num)
	}

	// Ejemplo 5: Múltiples receptores con cierre
	fmt.Println("\n5. Broadcast con cierre:")
	broadcast := make(chan bool)

	for i := 1; i <= 3; i++ {
		id := i
		go func() {
			<-broadcast
			fmt.Printf("  Worker %d recibió señal\n", id)
		}()
	}

	time.Sleep(100 * time.Millisecond)
	close(broadcast) // Notifica a todos los receptores
	time.Sleep(100 * time.Millisecond)

	// Ejemplo 6: Operaciones no bloqueantes múltiples
	fmt.Println("\n6. Select no bloqueante múltiple:")
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		time.Sleep(100 * time.Millisecond)
		ch1 <- "Canal 1"
	}()

	for i := 0; i < 3; i++ {
		select {
		case msg := <-ch1:
			fmt.Printf("  Recibido de ch1: %s\n", msg)
		case msg := <-ch2:
			fmt.Printf("  Recibido de ch2: %s\n", msg)
		default:
			fmt.Printf("  Intento %d: sin mensajes\n", i+1)
			time.Sleep(50 * time.Millisecond)
		}
	}

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Sistema de tareas con cierre apropiado
	type Tarea struct {
		ID     int
		Nombre string
	}

	tareas := make(chan Tarea, 10)
	completadas := make(chan int)

	// Productor de tareas
	go func() {
		for i := 1; i <= 5; i++ {
			tarea := Tarea{
				ID:     i,
				Nombre: fmt.Sprintf("Tarea-%d", i),
			}
			tareas <- tarea
			fmt.Printf("Enviada: %s\n", tarea.Nombre)
		}
		close(tareas) // Cerrar cuando no hay más tareas
	}()

	// Workers (3 workers concurrentes)
	numWorkers := 3
	for w := 1; w <= numWorkers; w++ {
		id := w
		go func() {
			procesadas := 0
			for tarea := range tareas {
				fmt.Printf("  Worker %d procesando %s\n", id, tarea.Nombre)
				time.Sleep(200 * time.Millisecond)
				procesadas++
			}
			completadas <- procesadas
		}()
	}

	// Recoger resultados
	total := 0
	for i := 0; i < numWorkers; i++ {
		n := <-completadas
		total += n
	}

	fmt.Printf("\nTotal de tareas procesadas: %d\n", total)

	// Ejemplo de operación no bloqueante
	fmt.Println("\nIntentando recibir de channel vacío:")
	ch := make(chan int)
	select {
	case val := <-ch:
		fmt.Printf("Recibido: %d\n", val)
	default:
		fmt.Println("Channel vacío, continuando sin bloquear")
	}
}
