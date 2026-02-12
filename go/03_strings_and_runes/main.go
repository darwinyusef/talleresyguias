package main

import (
	"fmt"
	"unicode/utf8"
)

/*
TEMA: Strings and Runes
DESCRIPCIÓN: En Go, los strings son secuencias de bytes inmutables.
Las runes representan puntos de código Unicode (int32).

CONCEPTOS CLAVE:
- string: secuencia inmutable de bytes
- rune: alias de int32, representa un carácter Unicode
- len() devuelve bytes, no caracteres
- utf8.RuneCountInString() cuenta caracteres reales
*/

func main() {
	fmt.Println("=== EJERCICIO 3: Strings and Runes ===\n")

	// Ejemplo 1: Diferencia entre bytes y runes
	fmt.Println("1. Bytes vs Runes:")
	s := "Hola 世界"
	fmt.Printf("   String: %s\n", s)
	fmt.Printf("   Longitud en bytes: %d\n", len(s))
	fmt.Printf("   Longitud en runes: %d\n", utf8.RuneCountInString(s))

	// Ejemplo 2: Iterar sobre bytes vs runes
	fmt.Println("\n2. Iteración sobre bytes:")
	for i := 0; i < len(s); i++ {
		fmt.Printf("   Byte %d: %x\n", i, s[i])
	}

	fmt.Println("\n3. Iteración sobre runes:")
	for i, r := range s {
		fmt.Printf("   Posición %d: %c (Unicode: U+%04X)\n", i, r, r)
	}

	// Ejemplo 3: Conversión entre string, []byte y []rune
	fmt.Println("\n4. Conversiones:")
	texto := "Go 语言"
	bytes := []byte(texto)
	runes := []rune(texto)
	fmt.Printf("   String: %s\n", texto)
	fmt.Printf("   Bytes: %v (longitud: %d)\n", bytes, len(bytes))
	fmt.Printf("   Runes: %v (longitud: %d)\n", runes, len(runes))

	// Ejemplo 4: Manipulación de runes
	fmt.Println("\n5. Manipulación de runes:")
	runeSlice := []rune(texto)
	runeSlice[0] = 'J'
	runeSlice[1] = 'a'
	nuevoTexto := string(runeSlice)
	fmt.Printf("   Texto modificado: %s\n", nuevoTexto)

	// EJERCICIO PRÁCTICO:
	fmt.Println("\n=== EJERCICIO PRÁCTICO ===")
	ejercicioPractico()
}

// TODO: Completa esta función
func ejercicioPractico() {
	// 1. Cuenta vocales en un string multilingüe
	texto := "Hello 世界 Español"
	vocales := contarVocales(texto)
	fmt.Printf("Vocales en '%s': %d\n", texto, vocales)

	// 2. Invierte un string considerando caracteres Unicode
	original := "Go 语言"
	invertido := invertirString(original)
	fmt.Printf("\nOriginal: %s\n", original)
	fmt.Printf("Invertido: %s\n", invertido)

	// 3. DESAFÍO: Extrae el primer carácter de cada palabra
	frase := "Hola Mundo Go 语言"
	iniciales := extraerIniciales(frase)
	fmt.Printf("\nFrase: %s\n", frase)
	fmt.Printf("Iniciales: %s\n", iniciales)
}

func contarVocales(s string) int {
	vocales := "aeiouAEIOUáéíóúÁÉÍÓÚ"
	count := 0
	for _, r := range s {
		for _, v := range vocales {
			if r == v {
				count++
				break
			}
		}
	}
	return count
}

func invertirString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func extraerIniciales(s string) string {
	var resultado []rune
	nuevaPalabra := true
	for _, r := range s {
		if r == ' ' {
			nuevaPalabra = true
		} else if nuevaPalabra {
			resultado = append(resultado, r)
			nuevaPalabra = false
		}
	}
	return string(resultado)
}
