package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
)

func main() {
	fmt.Println("🚀 Ejecutando script desde Go...")
	fmt.Println()

	// Obtener el directorio actual
	dir, err := os.Getwd()
	if err != nil {
		fmt.Fprintf(os.Stderr, "❌ Error obteniendo directorio: %v\n", err)
		os.Exit(1)
	}

	// Ruta al script
	scriptPath := filepath.Join(dir, "script_ejemplo.sh")

	// Verificar que el script existe
	if _, err := os.Stat(scriptPath); os.IsNotExist(err) {
		fmt.Fprintf(os.Stderr, "❌ Error: el script no existe en %s\n", scriptPath)
		os.Exit(1)
	}

	// Parámetros para el script
	nombre := "Juan"
	edad := "25"

	// Si se pasan argumentos desde la línea de comandos, usarlos
	if len(os.Args) > 1 {
		nombre = os.Args[1]
	}
	if len(os.Args) > 2 {
		edad = os.Args[2]
	}

	fmt.Printf("📋 Ejecutando: %s %s %s\n", scriptPath, nombre, edad)
	fmt.Println("─────────────────────────────────────")

	// Crear el comando
	cmd := exec.Command(scriptPath, nombre, edad)

	// Buffers para capturar stdout y stderr
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	// Ejecutar el comando
	err = cmd.Run()

	// Mostrar la salida
	if stdout.Len() > 0 {
		fmt.Print(stdout.String())
	}

	if stderr.Len() > 0 {
		fmt.Fprintf(os.Stderr, "⚠️  Stderr:\n%s", stderr.String())
	}

	// Verificar si hubo error
	if err != nil {
		fmt.Fprintf(os.Stderr, "\n❌ Error ejecutando script: %v\n", err)
		os.Exit(1)
	}

	fmt.Println()
	fmt.Println("✅ Script ejecutado exitosamente desde Go")
}
