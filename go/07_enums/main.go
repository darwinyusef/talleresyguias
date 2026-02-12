package main

import "fmt"

/*
TEMA: Enums (Enumeraciones)
DESCRIPCIÓN: Go no tiene enums nativos, pero se pueden simular usando
constantes con iota y tipos personalizados.

CONCEPTOS CLAVE:
- iota: generador de constantes incrementales
- Tipos personalizados para enums
- Métodos String() para representación legible
- Validación de valores de enum
*/

// Ejemplo 1: Enum simple con iota
type DiaSemana int

const (
	Lunes DiaSemana = iota // 0
	Martes                 // 1
	Miercoles              // 2
	Jueves                 // 3
	Viernes                // 4
	Sabado                 // 5
	Domingo                // 6
)

// Método String para representación legible
func (d DiaSemana) String() string {
	nombres := []string{
		"Lunes", "Martes", "Miércoles", "Jueves",
		"Viernes", "Sábado", "Domingo",
	}
	if d < Lunes || d > Domingo {
		return "Día inválido"
	}
	return nombres[d]
}

func (d DiaSemana) EsFinDeSemana() bool {
	return d == Sabado || d == Domingo
}

// Ejemplo 2: Enum con valores específicos
type EstadoPedido int

const (
	Pendiente EstadoPedido = iota + 1 // Empieza en 1
	Procesando
	Enviado
	Entregado
	Cancelado
)

func (e EstadoPedido) String() string {
	switch e {
	case Pendiente:
		return "Pendiente"
	case Procesando:
		return "Procesando"
	case Enviado:
		return "Enviado"
	case Entregado:
		return "Entregado"
	case Cancelado:
		return "Cancelado"
	default:
		return "Estado desconocido"
	}
}

// Ejemplo 3: Enum con valores de bits (flags)
type Permiso int

const (
	Leer Permiso = 1 << iota // 1 (binario: 001)
	Escribir                 // 2 (binario: 010)
	Ejecutar                 // 4 (binario: 100)
)

func (p Permiso) String() string {
	var permisos []string
	if p&Leer != 0 {
		permisos = append(permisos, "Leer")
	}
	if p&Escribir != 0 {
		permisos = append(permisos, "Escribir")
	}
	if p&Ejecutar != 0 {
		permisos = append(permisos, "Ejecutar")
	}
	if len(permisos) == 0 {
		return "Sin permisos"
	}
	resultado := permisos[0]
	for i := 1; i < len(permisos); i++ {
		resultado += ", " + permisos[i]
	}
	return resultado
}

func main() {
	fmt.Println("=== EJERCICIO 7: Enums ===\n")

	// Ejemplo 1: Días de la semana
	fmt.Println("1. Días de la semana:")
	dia := Miercoles
	fmt.Printf("   Día: %s (valor: %d)\n", dia, dia)
	fmt.Printf("   ¿Es fin de semana? %t\n", dia.EsFinDeSemana())

	diaFinSemana := Sabado
	fmt.Printf("   Día: %s (valor: %d)\n", diaFinSemana, diaFinSemana)
	fmt.Printf("   ¿Es fin de semana? %t\n", diaFinSemana.EsFinDeSemana())

	// Ejemplo 2: Estados de pedido
	fmt.Println("\n2. Estados de pedido:")
	estado := Pendiente
	fmt.Printf("   Estado inicial: %s\n", estado)
	
	estado = Procesando
	fmt.Printf("   Estado actualizado: %s\n", estado)
	
	estado = Entregado
	fmt.Printf("   Estado final: %s\n", estado)

	// Ejemplo 3: Permisos con bits
	fmt.Println("\n3. Permisos (flags):")
	var p Permiso
	
	p = Leer
	fmt.Printf("   Permisos: %s (valor: %d)\n", p, p)
	
	p = Leer | Escribir // Combinar permisos
	fmt.Printf("   Permisos: %s (valor: %d)\n", p, p)
	
	p = Leer | Escribir | Ejecutar
	fmt.Printf("   Permisos: %s (valor: %d)\n", p, p)
	
	// Verificar permisos específicos
	fmt.Printf("   ¿Tiene permiso de lectura? %t\n", p&Leer != 0)
	fmt.Printf("   ¿Tiene permiso de escritura? %t\n", p&Escribir != 0)

	// Ejemplo 4: Iterar sobre enum
	fmt.Println("\n4. Todos los días de la semana:")
	for d := Lunes; d <= Domingo; d++ {
		fmt.Printf("   %d: %s\n", d, d)
	}

	// EJERCICIO PRÁCTICO:
	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

// TODO: Completa esta función
func ejercicioPractico() {
	// 1. Define un enum para Nivel de prioridad (Baja, Media, Alta, Crítica)
	type Prioridad int

	const (
		Baja Prioridad = iota + 1
		Media
		Alta
		Critica
	)

	// 2. Implementa método String()
	// (Ver implementación abajo)

	// 3. Crea un struct Tarea con título y prioridad
	type Tarea struct {
		Titulo    string
		Prioridad Prioridad
	}

	// 4. Crea varias tareas
	tareas := []Tarea{
		{"Revisar emails", Baja},
		{"Completar informe", Media},
		{"Arreglar bug crítico", Critica},
		{"Reunión de equipo", Media},
		{"Actualizar documentación", Baja},
	}

	// 5. Imprime tareas ordenadas por prioridad
	fmt.Println("Lista de tareas:")
	for _, tarea := range tareas {
		fmt.Printf("   [%s] %s\n", tarea.Prioridad, tarea.Titulo)
	}

	// 6. DESAFÍO: Cuenta tareas por prioridad
	fmt.Println("\nTareas por prioridad:")
	contadores := make(map[Prioridad]int)
	for _, tarea := range tareas {
		contadores[tarea.Prioridad]++
	}
	for p := Baja; p <= Critica; p++ {
		fmt.Printf("   %s: %d\n", p, contadores[p])
	}
}

type Prioridad int

const (
	Baja Prioridad = iota + 1
	Media
	Alta
	Critica
)

func (p Prioridad) String() string {
	switch p {
	case Baja:
		return "Baja"
	case Media:
		return "Media"
	case Alta:
		return "Alta"
	case Critica:
		return "Crítica"
	default:
		return "Desconocida"
	}
}

type Tarea struct {
	Titulo    string
	Prioridad Prioridad
}
