package main

import (
	"fmt"
)

/*
TEMA: Custom Errors (Errores Personalizados)
DESCRIPCIÓN: Puedes crear tipos de error personalizados implementando
la interfaz error (método Error() string).

CONCEPTOS CLAVE:
- Implementar interfaz error
- Structs de error con información adicional
- Type assertions para errores específicos
*/

// Error personalizado simple
type ErrorValidacion struct {
	Campo   string
	Mensaje string
}

func (e ErrorValidacion) Error() string {
	return fmt.Sprintf("error en campo '%s': %s", e.Campo, e.Mensaje)
}

// Error personalizado con código
type ErrorHTTP struct {
	Codigo  int
	Mensaje string
}

func (e ErrorHTTP) Error() string {
	return fmt.Sprintf("HTTP %d: %s", e.Codigo, e.Mensaje)
}

// Función que retorna error personalizado
func ValidarUsuario(nombre, email string) error {
	if nombre == "" {
		return ErrorValidacion{
			Campo:   "nombre",
			Mensaje: "no puede estar vacío",
		}
	}
	if email == "" {
		return ErrorValidacion{
			Campo:   "email",
			Mensaje: "no puede estar vacío",
		}
	}
	return nil
}

func main() {
	fmt.Println("=== EJERCICIO 12: Custom Errors ===\n")

	// Ejemplo 1: Error personalizado
	fmt.Println("1. Validación de usuario:")
	err := ValidarUsuario("", "test@example.com")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		
		// Type assertion para acceder a campos específicos
		if errVal, ok := err.(ErrorValidacion); ok {
			fmt.Printf("Campo problemático: %s\n", errVal.Campo)
		}
	}

	// Ejemplo 2: Error HTTP
	fmt.Println("\n2. Errores HTTP:")
	errores := []error{
		ErrorHTTP{Codigo: 404, Mensaje: "No encontrado"},
		ErrorHTTP{Codigo: 500, Mensaje: "Error interno"},
		ErrorHTTP{Codigo: 403, Mensaje: "Prohibido"},
	}

	for _, err := range errores {
		fmt.Printf("  %v\n", err)
	}

	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

func ejercicioPractico() {
	// Error personalizado para operaciones matemáticas
	type ErrorMatematico struct {
		Operacion string
		Razon     string
	}

	// Implementar método Error()
	// (Ver abajo)

	fmt.Println("Errores matemáticos personalizados:")
	err := ErrorMatematico{
		Operacion: "raíz cuadrada",
		Razon:     "número negativo",
	}
	fmt.Printf("  %v\n", err)
}

type ErrorMatematico struct {
	Operacion string
	Razon     string
}

func (e ErrorMatematico) Error() string {
	return fmt.Sprintf("error en %s: %s", e.Operacion, e.Razon)
}
