package main

import (
	"fmt"
	"time"
)

/*
TEMA: Timeouts
DESCRIPCIÓN: Los timeouts permiten limitar el tiempo de espera en
operaciones de channels usando time.After.

CONCEPTOS CLAVE:
- time.After() retorna un channel que envía después del tiempo
- Combinar con select para implementar timeouts
- Evitar operaciones que se cuelgan indefinidamente
*/

func main() {
	fmt.Println("=== EJERCICIO 19: Timeouts ===\n")

	// Ejemplo 1: Timeout simple
	fmt.Println("1. Timeout simple:")
	ch1 := make(chan string)

	go func() {
		time.Sleep(2 * time.Second)
		ch1 <- "Resultado"
	}()

	select {
	case res := <-ch1:
		fmt.Printf("Recibido: %s\n", res)
	case <-time.After(1 * time.Second):
		fmt.Println("Timeout: operación tardó demasiado")
	}

	// Ejemplo 2: Operación exitosa antes del timeout
	fmt.Println("\n2. Operación exitosa:")
	ch2 := make(chan string)

	go func() {
		time.Sleep(500 * time.Millisecond)
		ch2 <- "Éxito"
	}()

	select {
	case res := <-ch2:
		fmt.Printf("Recibido: %s\n", res)
	case <-time.After(1 * time.Second):
		fmt.Println("Timeout")
	}

	// Ejemplo 3: Múltiples operaciones con timeout
	fmt.Println("\n3. Múltiples operaciones:")
	resultados := make(chan string)

	operaciones := []struct {
		nombre  string
		duracion time.Duration
	}{
		{"Rápida", 200 * time.Millisecond},
		{"Media", 800 * time.Millisecond},
		{"Lenta", 2 * time.Second},
	}

	for _, op := range operaciones {
		nombre := op.nombre
		duracion := op.duracion

		go func() {
			time.Sleep(duracion)
			resultados <- nombre
		}()

		select {
		case res := <-resultados:
			fmt.Printf("  %s completada\n", res)
		case <-time.After(1 * time.Second):
			fmt.Printf("  %s: timeout\n", nombre)
		}
	}

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Simular llamadas a API con timeout
	type Respuesta struct {
		Servicio string
		Datos    string
	}

	llamarAPI := func(servicio string, duracion time.Duration, respuesta chan<- Respuesta) {
		time.Sleep(duracion)
		respuesta <- Respuesta{
			Servicio: servicio,
			Datos:    fmt.Sprintf("Datos de %s", servicio),
		}
	}

	fmt.Println("Llamadas a APIs con timeout de 1 segundo:")
	
	servicios := []struct {
		nombre   string
		duracion time.Duration
	}{
		{"API-1", 500 * time.Millisecond},
		{"API-2", 1500 * time.Millisecond},
		{"API-3", 300 * time.Millisecond},
	}

	for _, srv := range servicios {
		respuesta := make(chan Respuesta)
		go llamarAPI(srv.nombre, srv.duracion, respuesta)

		select {
		case res := <-respuesta:
			fmt.Printf("  ✓ %s: %s\n", res.Servicio, res.Datos)
		case <-time.After(1 * time.Second):
			fmt.Printf("  ✗ %s: timeout\n", srv.nombre)
		}
	}
}
