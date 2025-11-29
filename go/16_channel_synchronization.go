package main

import (
	"fmt"
	"time"
)

/*
TEMA: Channel Synchronization (Sincronización con Canales)
DESCRIPCIÓN: Los channels pueden usarse para sincronizar goroutines,
esperando a que completen su trabajo.

CONCEPTOS CLAVE:
- Usar channel como señal de completado
- Bloqueo hasta recibir señal
- Coordinación entre goroutines
*/

func trabajar(nombre string, done chan bool) {
	fmt.Printf("%s: iniciando trabajo...\n", nombre)
	time.Sleep(1 * time.Second)
	fmt.Printf("%s: trabajo completado\n", nombre)
	done <- true
}

func procesarDatos(datos []int, resultado chan int) {
	suma := 0
	for _, num := range datos {
		suma += num
		time.Sleep(100 * time.Millisecond)
	}
	resultado <- suma
}

func main() {
	fmt.Println("=== EJERCICIO 16: Channel Synchronization ===\n")

	// Ejemplo 1: Esperar a que goroutine termine
	fmt.Println("1. Sincronización básica:")
	done := make(chan bool)
	go trabajar("Worker 1", done)
	<-done // Bloquea hasta recibir señal
	fmt.Println("Worker completado, continuando...\n")

	// Ejemplo 2: Múltiples workers
	fmt.Println("2. Múltiples workers:")
	done1 := make(chan bool)
	done2 := make(chan bool)
	done3 := make(chan bool)

	go trabajar("Worker A", done1)
	go trabajar("Worker B", done2)
	go trabajar("Worker C", done3)

	<-done1
	<-done2
	<-done3
	fmt.Println("Todos los workers completados\n")

	// Ejemplo 3: Obtener resultado
	fmt.Println("3. Obtener resultado:")
	resultado := make(chan int)
	datos := []int{1, 2, 3, 4, 5}
	
	go procesarDatos(datos, resultado)
	
	suma := <-resultado
	fmt.Printf("Suma total: %d\n", suma)

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Procesar múltiples tareas y esperar resultados
	type Resultado struct {
		ID    int
		Valor int
	}

	resultados := make(chan Resultado)
	numTareas := 3

	// Lanzar tareas
	for i := 1; i <= numTareas; i++ {
		id := i
		go func() {
			time.Sleep(time.Duration(id*100) * time.Millisecond)
			valor := id * id
			resultados <- Resultado{ID: id, Valor: valor}
		}()
	}

	// Recoger resultados
	fmt.Println("Resultados de tareas:")
	for i := 0; i < numTareas; i++ {
		res := <-resultados
		fmt.Printf("  Tarea %d: %d\n", res.ID, res.Valor)
	}
}
