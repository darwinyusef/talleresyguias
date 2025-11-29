package main

import (
	"fmt"
	"math"
)

/*
TEMA: Interfaces
DESCRIPCIÓN: Las interfaces definen comportamientos (conjuntos de métodos).
Un tipo implementa una interfaz implícitamente si tiene todos sus métodos.

CONCEPTOS CLAVE:
- Interface: contrato de métodos
- Implementación implícita (no se declara)
- Polimorfismo a través de interfaces
- Interface vacía: interface{} acepta cualquier tipo
*/

// Definición de interfaces
type Figura interface {
	Area() float64
	Perimetro() float64
}

type Describible interface {
	Descripcion() string
}

// Tipos que implementan las interfaces
type Rectangulo struct {
	Ancho float64
	Alto  float64
}

type Circulo struct {
	Radio float64
}

type Triangulo struct {
	Base   float64
	Altura float64
	Lado1  float64
	Lado2  float64
	Lado3  float64
}

func main() {
	fmt.Println("=== EJERCICIO 6: Interfaces ===\n")

	// Ejemplo 1: Uso básico de interfaces
	fmt.Println("1. Figuras geométricas:")
	var f Figura

	f = Rectangulo{Ancho: 10, Alto: 5}
	imprimirInfo(f)

	f = Circulo{Radio: 7}
	imprimirInfo(f)

	f = Triangulo{Base: 6, Altura: 4, Lado1: 5, Lado2: 5, Lado3: 6}
	imprimirInfo(f)

	// Ejemplo 2: Slice de interfaces
	fmt.Println("\n2. Colección de figuras:")
	figuras := []Figura{
		Rectangulo{Ancho: 8, Alto: 3},
		Circulo{Radio: 5},
		Triangulo{Base: 4, Altura: 3, Lado1: 3, Lado2: 4, Lado3: 5},
	}

	areaTotal := calcularAreaTotal(figuras)
	fmt.Printf("   Área total de todas las figuras: %.2f\n", areaTotal)

	// Ejemplo 3: Type assertion
	fmt.Println("\n3. Type assertion:")
	var i interface{} = "Hola, Go!"
	s, ok := i.(string)
	if ok {
		fmt.Printf("   String: %s (longitud: %d)\n", s, len(s))
	}

	// Ejemplo 4: Type switch
	fmt.Println("\n4. Type switch:")
	identificarTipo(42)
	identificarTipo("texto")
	identificarTipo(3.14)
	identificarTipo(true)
	identificarTipo(Circulo{Radio: 3})

	// EJERCICIO PRÁCTICO:
	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

// Implementación de métodos para Rectangulo
func (r Rectangulo) Area() float64 {
	return r.Ancho * r.Alto
}

func (r Rectangulo) Perimetro() float64 {
	return 2 * (r.Ancho + r.Alto)
}

func (r Rectangulo) Descripcion() string {
	return fmt.Sprintf("Rectángulo de %.2f x %.2f", r.Ancho, r.Alto)
}

// Implementación de métodos para Circulo
func (c Circulo) Area() float64 {
	return math.Pi * c.Radio * c.Radio
}

func (c Circulo) Perimetro() float64 {
	return 2 * math.Pi * c.Radio
}

func (c Circulo) Descripcion() string {
	return fmt.Sprintf("Círculo de radio %.2f", c.Radio)
}

// Implementación de métodos para Triangulo
func (t Triangulo) Area() float64 {
	return (t.Base * t.Altura) / 2
}

func (t Triangulo) Perimetro() float64 {
	return t.Lado1 + t.Lado2 + t.Lado3
}

func (t Triangulo) Descripcion() string {
	return fmt.Sprintf("Triángulo de base %.2f y altura %.2f", t.Base, t.Altura)
}

// Funciones auxiliares
func imprimirInfo(f Figura) {
	fmt.Printf("   Área: %.2f, Perímetro: %.2f\n", f.Area(), f.Perimetro())

	// Si también implementa Describible
	if d, ok := f.(Describible); ok {
		fmt.Printf("   Descripción: %s\n", d.Descripcion())
	}
}

func calcularAreaTotal(figuras []Figura) float64 {
	var total float64
	for _, f := range figuras {
		total += f.Area()
	}
	return total
}

func identificarTipo(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("   Entero: %d\n", v)
	case string:
		fmt.Printf("   String: %s\n", v)
	case float64:
		fmt.Printf("   Float: %.2f\n", v)
	case bool:
		fmt.Printf("   Booleano: %t\n", v)
	case Figura:
		fmt.Printf("   Figura con área: %.2f\n", v.Area())
	default:
		fmt.Printf("   Tipo desconocido: %T\n", v)
	}
}

// TODO: Completa esta función
func ejercicioPractico() {
	// 1. Define una interfaz Sonido con método HacerSonido()
	// 2. Crea tipos Perro, Gato, Vaca que implementen Sonido
	// (Ver definiciones al final del archivo)

	// 3. Crea una granja de animales
	animales := []Sonido{
		Perro{Nombre: "Rex"},
		Gato{Nombre: "Misu"},
		Vaca{Nombre: "Lola"},
	}

	// 4. Haz que todos los animales hagan su sonido
	fmt.Println("Sonidos de la granja:")
	for _, animal := range animales {
		fmt.Printf("   %s\n", animal.HacerSonido())
	}
}

type Sonido interface {
	HacerSonido() string
}

type Perro struct{ Nombre string }
type Gato struct{ Nombre string }
type Vaca struct{ Nombre string }

func (p Perro) HacerSonido() string {
	return fmt.Sprintf("%s dice: ¡Guau guau!", p.Nombre)
}

func (g Gato) HacerSonido() string {
	return fmt.Sprintf("%s dice: ¡Miau miau!", g.Nombre)
}

func (v Vaca) HacerSonido() string {
	return fmt.Sprintf("%s dice: ¡Muuu!", v.Nombre)
}
