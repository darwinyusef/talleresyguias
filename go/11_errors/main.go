package main

import (
	"errors"
	"fmt"
)

/*
TEMA: Errors (Manejo de Errores)
DESCRIPCIÓN: Go usa valores de error explícitos en lugar de excepciones.
Las funciones retornan error como último valor de retorno.

CONCEPTOS CLAVE:
- error es una interfaz
- Retornar nil cuando no hay error
- Verificar errores con if err != nil
- errors.New() para crear errores simples
*/

// Función que puede retornar error
func Dividir(a, b float64) (float64, error) {
	if b == 0 {
		return 0, errors.New("división por cero")
	}
	return a / b, nil
}

// Función con múltiples validaciones
func ValidarEdad(edad int) error {
	if edad < 0 {
		return errors.New("la edad no puede ser negativa")
	}
	if edad > 150 {
		return errors.New("la edad no es realista")
	}
	return nil
}

func main() {
	fmt.Println("=== EJERCICIO 11: Errors ===\n")

	// Ejemplo 1: Manejo básico de errores
	fmt.Println("1. División:")
	resultado, err := Dividir(10, 2)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Resultado: %.2f\n", resultado)
	}

	// Ejemplo 2: Error al dividir por cero
	resultado, err = Dividir(10, 0)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Resultado: %.2f\n", resultado)
	}

	// Ejemplo 3: Validación
	fmt.Println("\n2. Validación de edad:")
	edades := []int{25, -5, 200, 45}
	for _, edad := range edades {
		err := ValidarEdad(edad)
		if err != nil {
			fmt.Printf("Edad %d: Error - %v\n", edad, err)
		} else {
			fmt.Printf("Edad %d: Válida\n", edad)
		}
	}

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Función que valida un email simple
	validarEmail := func(email string) error {
		if email == "" {
			return errors.New("email vacío")
		}
		if len(email) < 5 {
			return errors.New("email demasiado corto")
		}
		return nil
	}

	emails := []string{"test@example.com", "", "abc", "user@domain.com"}
	fmt.Println("Validación de emails:")
	for _, email := range emails {
		err := validarEmail(email)
		if err != nil {
			fmt.Printf("  '%s': Error - %v\n", email, err)
		} else {
			fmt.Printf("  '%s': Válido\n", email)
		}
	}
}
