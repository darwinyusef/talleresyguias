package main

import "fmt"

/*
TEMA: Struct Embedding (Composición)
DESCRIPCIÓN: Go usa composición en lugar de herencia. Un struct puede
embeber otro struct, heredando sus campos y métodos.

CONCEPTOS CLAVE:
- Embedding: incluir un struct dentro de otro
- Promoción de campos y métodos
- Composición sobre herencia
*/

type Persona struct {
	Nombre string
	Edad   int
}

func (p Persona) Saludar() string {
	return fmt.Sprintf("Hola, soy %s", p.Nombre)
}

type Empleado struct {
	Persona
	Empresa string
	Salario float64
}

func main() {
	fmt.Println("=== EJERCICIO 8: Struct Embedding ===\n")

	emp := Empleado{
		Persona: Persona{Nombre: "Ana", Edad: 30},
		Empresa: "TechCorp",
		Salario: 45000,
	}

	fmt.Printf("Nombre: %s\n", emp.Nombre)
	fmt.Printf("%s\n", emp.Saludar())
	fmt.Printf("Empresa: %s\n", emp.Empresa)
}
