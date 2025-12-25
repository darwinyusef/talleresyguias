package main

import (
	"fmt"
	"os"
	"runtime"

	"github.com/spf13/cobra"
)

var (
	version = "dev"
	commit  = "none"
	date    = "unknown"
)

var rootCmd = &cobra.Command{
	Use:   "mycli",
	Short: "Mi CLI de ejemplo con distribución profesional",
	Long: `Una CLI de ejemplo que demuestra cómo crear distribuciones
profesionales con Go: binario único, zero dependencias, cross-platform.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("🚀 ¡Bienvenido a MyCLI!")
		fmt.Println("Usa 'mycli --help' para ver los comandos disponibles")
	},
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Muestra la versión de la CLI",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("MyCLI\n")
		fmt.Printf("  Version:     %s\n", version)
		fmt.Printf("  Commit:      %s\n", commit)
		fmt.Printf("  Build Date:  %s\n", date)
		fmt.Printf("  Go Version:  %s\n", runtime.Version())
		fmt.Printf("  OS/Arch:     %s/%s\n", runtime.GOOS, runtime.GOARCH)
	},
}

var infoCmd = &cobra.Command{
	Use:   "info",
	Short: "Información del sistema",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Sistema Operativo: %s\n", runtime.GOOS)
		fmt.Printf("Arquitectura: %s\n", runtime.GOARCH)
		fmt.Printf("CPUs: %d\n", runtime.NumCPU())
		fmt.Printf("Go Version: %s\n", runtime.Version())
	},
}

var helloCmd = &cobra.Command{
	Use:   "hello [nombre]",
	Short: "Saluda a alguien",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := "mundo"
		if len(args) > 0 {
			name = args[0]
		}
		fmt.Printf("👋 ¡Hola, %s!\n", name)
	},
}

func init() {
	rootCmd.AddCommand(versionCmd)
	rootCmd.AddCommand(infoCmd)
	rootCmd.AddCommand(helloCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
