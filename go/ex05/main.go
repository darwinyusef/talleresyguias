package main

import (
	"fmt"
	"math"
)

/*
TEMA: Methods (Métodos)
DESCRIPCIÓN: Los métodos son funciones asociadas a un tipo específico.
Se definen con un receptor que puede ser por valor o por puntero.

CONCEPTOS CLAVE:
- Método: función con receptor
- Receptor por valor: no modifica el original
- Receptor por puntero: puede modificar el original
- Métodos pueden definirse para cualquier tipo
*/

// Tipos para ejemplos
type Rectangulo struct {
	Ancho float64
	Alto  float64
}

type Circulo struct {
	Radio float64
}

type Contador struct {
	Valor int
}

// Tipo para el ejercicio práctico (declarado a nivel de paquete - sólo una vez)
type CuentaBancaria struct {
	Titular string
	Saldo   float64
}

func main() {
	fmt.Println("=== EJERCICIO 5: Methods ===\n")

	// Ejemplo 1: Métodos con receptor por valor
	fmt.Println("1. Métodos con receptor por valor:")
	r := Rectangulo{Ancho: 10, Alto: 5}
	fmt.Printf("   Rectángulo: %+v\n", r)
	fmt.Printf("   Área: %.2f\n", r.Area())
	fmt.Printf("   Perímetro: %.2f\n", r.Perimetro())

	// Ejemplo 2: Métodos con receptor por puntero
	fmt.Println("\n2. Métodos con receptor por puntero:")
	contador := Contador{Valor: 0}
	fmt.Printf("   Contador inicial: %d\n", contador.Valor)
	contador.Incrementar()
	contador.Incrementar()
	contador.Incrementar()
	fmt.Printf("   Después de incrementar 3 veces: %d\n", contador.Valor)
	contador.Reiniciar()
	fmt.Printf("   Después de reiniciar: %d\n", contador.Valor)

	// Ejemplo 3: Métodos en diferentes tipos
	fmt.Println("\n3. Métodos en círculo:")
	circ := Circulo{Radio: 5}
	fmt.Printf("   Círculo: %+v\n", circ)
	fmt.Printf("   Área: %.2f\n", circ.Area())
	fmt.Printf("   Circunferencia: %.2f\n", circ.Circunferencia())

	// Ejemplo 4: Comparación valor vs puntero
	fmt.Println("\n4. Comparación valor vs puntero:")
	r2 := Rectangulo{Ancho: 8, Alto: 4}
	fmt.Printf("   Original: %+v\n", r2)
	r2.IntentarDuplicar() // No modifica (receptor por valor)
	fmt.Printf("   Después de IntentarDuplicar: %+v\n", r2)
	r2.Duplicar() // Modifica (receptor por puntero)
	fmt.Printf("   Después de Duplicar: %+v\n", r2)

	// EJERCICIO PRÁCTICO:
	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

// Métodos de Rectangulo (receptor por valor)
func (r Rectangulo) Area() float64 {
	return r.Ancho * r.Alto
}

func (r Rectangulo) Perimetro() float64 {
	return 2 * (r.Ancho + r.Alto)
}

// Este método NO modifica el original (receptor por valor)
func (r Rectangulo) IntentarDuplicar() {
	r.Ancho *= 2
	r.Alto *= 2
}

// Este método SÍ modifica el original (receptor por puntero)
func (r *Rectangulo) Duplicar() {
	r.Ancho *= 2
	r.Alto *= 2
}

// Métodos de Circulo
func (c Circulo) Area() float64 {
	return math.Pi * c.Radio * c.Radio
}

func (c Circulo) Circunferencia() float64 {
	return 2 * math.Pi * c.Radio
}

// Métodos de Contador (receptor por puntero para modificar)
func (c *Contador) Incrementar() {
	c.Valor++
}

func (c *Contador) Decrementar() {
	c.Valor--
}

func (c *Contador) Reiniciar() {
	c.Valor = 0
}

// ejercicioPractico usa el tipo CuentaBancaria declarado a nivel paquete
func ejercicioPractico() {
	// 2. Crea métodos para depositar, retirar y consultar saldo
	cuenta := CuentaBancaria{
		Titular: "Juan Pérez",
		Saldo:   1000.00,
	}

	fmt.Printf("Titular: %s\n", cuenta.Titular)
	fmt.Printf("Saldo inicial: $%.2f\n", cuenta.ConsultarSaldo())

	cuenta.Depositar(500.00)
	fmt.Printf("Después de depositar $500: $%.2f\n", cuenta.ConsultarSaldo())

	exito := cuenta.Retirar(300.00)
	if exito {
		fmt.Printf("Después de retirar $300: $%.2f\n", cuenta.ConsultarSaldo())
	}

	// 3. DESAFÍO: Intenta retirar más de lo disponible
	exito = cuenta.Retirar(2000.00)
	if !exito {
		fmt.Println("No se puede retirar: fondos insuficientes")
	}
	fmt.Printf("Saldo final: $%.2f\n", cuenta.ConsultarSaldo())
}

// Métodos de CuentaBancaria
func (c *CuentaBancaria) Depositar(cantidad float64) {
	if cantidad > 0 {
		c.Saldo += cantidad
	}
}

func (c *CuentaBancaria) Retirar(cantidad float64) bool {
	if cantidad > 0 && cantidad <= c.Saldo {
		c.Saldo -= cantidad
		return true
	}
	return false
}

func (c CuentaBancaria) ConsultarSaldo() float64 {
	return c.Saldo
}
