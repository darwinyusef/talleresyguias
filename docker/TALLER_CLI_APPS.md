# Taller: Containerización de Aplicaciones CLI

## Objetivo
Aprender a crear y containerizar aplicaciones de línea de comandos (CLI) usando Python (Click, Typer, Argparse) y Go (Cobra, Viper).

---

## Índice
1. [Python con Argparse](#python-argparse)
2. [Python con Click](#python-click)
3. [Python con Typer](#python-typer)
4. [Go con Cobra](#go-cobra)
5. [Go con Cobra + Viper](#go-cobra-viper)
6. [CLI Tools Complejas](#cli-tools-complejas)

---

## Python con Argparse

### Estructura del Proyecto

```
argparse-cli/
├── cli.py
├── requirements.txt
├── Dockerfile
└── README.md
```

### cli.py

```python
import argparse
import sys
import requests
from datetime import datetime

def fetch_weather(city: str, units: str = 'metric'):
    """Fetch weather data from API"""
    # Simulado - en producción usar API real
    print(f"Fetching weather for {city}...")
    print(f"Temperature: 22°C")
    print(f"Condition: Sunny")

def list_tasks(filter: str = 'all'):
    """List tasks"""
    tasks = [
        {'id': 1, 'title': 'Task 1', 'status': 'done'},
        {'id': 2, 'title': 'Task 2', 'status': 'pending'},
    ]

    print("Tasks:")
    for task in tasks:
        if filter == 'all' or task['status'] == filter:
            status_icon = '✓' if task['status'] == 'done' else '○'
            print(f"  {status_icon} [{task['id']}] {task['title']}")

def create_task(title: str, priority: int = 1):
    """Create new task"""
    print(f"Created task: '{title}' with priority {priority}")

def main():
    parser = argparse.ArgumentParser(
        description='MyApp - CLI tool for task management and weather',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s weather --city London
  %(prog)s tasks list --filter pending
  %(prog)s tasks create "Buy groceries" --priority 2
        '''
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Weather command
    weather_parser = subparsers.add_parser('weather', help='Get weather information')
    weather_parser.add_argument(
        '--city',
        required=True,
        help='City name'
    )
    weather_parser.add_argument(
        '--units',
        choices=['metric', 'imperial'],
        default='metric',
        help='Temperature units'
    )

    # Tasks command
    tasks_parser = subparsers.add_parser('tasks', help='Manage tasks')
    tasks_subparsers = tasks_parser.add_subparsers(dest='tasks_command')

    # tasks list
    list_parser = tasks_subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument(
        '--filter',
        choices=['all', 'done', 'pending'],
        default='all',
        help='Filter tasks by status'
    )

    # tasks create
    create_parser = tasks_subparsers.add_parser('create', help='Create task')
    create_parser.add_argument('title', help='Task title')
    create_parser.add_argument(
        '--priority',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help='Task priority (1=low, 2=medium, 3=high)'
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"[DEBUG] Command: {args.command}")
        print(f"[DEBUG] Args: {args}")

    # Execute commands
    if args.command == 'weather':
        fetch_weather(args.city, args.units)

    elif args.command == 'tasks':
        if args.tasks_command == 'list':
            list_tasks(args.filter)
        elif args.tasks_command == 'create':
            create_task(args.title, args.priority)
        else:
            tasks_parser.print_help()

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### requirements.txt

```
requests==2.31.0
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy CLI tool
COPY cli.py .

# Make executable
RUN chmod +x cli.py

# Create symbolic link for easier usage
RUN ln -s /app/cli.py /usr/local/bin/myapp

# Set entrypoint
ENTRYPOINT ["python", "/app/cli.py"]

# Default command (show help)
CMD ["--help"]
```

### Uso

```bash
# Build
docker build -t myapp-cli .

# Run commands
docker run --rm myapp-cli --help
docker run --rm myapp-cli weather --city London
docker run --rm myapp-cli tasks list --filter pending
docker run --rm myapp-cli tasks create "New task" --priority 2

# Con alias (agregar a ~/.bashrc)
alias myapp='docker run --rm myapp-cli'
myapp weather --city Paris
```

---

## Python con Click

Click es una biblioteca más moderna y elegante para CLIs.

### Estructura

```
click-cli/
├── cli.py
├── commands/
│   ├── __init__.py
│   ├── weather.py
│   └── tasks.py
├── requirements.txt
└── Dockerfile
```

### cli.py

```python
import click

@click.group()
@click.version_option(version='1.0.0')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """MyApp - CLI tool for task management and weather"""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose

@cli.group()
def tasks():
    """Manage tasks"""
    pass

@tasks.command()
@click.option('--filter', type=click.Choice(['all', 'done', 'pending']), default='all')
@click.pass_context
def list(ctx, filter):
    """List tasks"""
    if ctx.obj['VERBOSE']:
        click.echo(f"Filtering by: {filter}")

    tasks = [
        {'id': 1, 'title': 'Task 1', 'status': 'done'},
        {'id': 2, 'title': 'Task 2', 'status': 'pending'},
    ]

    click.echo(click.style('Tasks:', fg='green', bold=True))
    for task in tasks:
        if filter == 'all' or task['status'] == filter:
            icon = '✓' if task['status'] == 'done' else '○'
            color = 'green' if task['status'] == 'done' else 'yellow'
            click.echo(click.style(f"  {icon} [{task['id']}] {task['title']}", fg=color))

@tasks.command()
@click.argument('title')
@click.option('--priority', type=click.IntRange(1, 3), default=1, help='Priority (1-3)')
@click.option('--tags', multiple=True, help='Task tags')
@click.pass_context
def create(ctx, title, priority, tags):
    """Create new task"""
    if ctx.obj['VERBOSE']:
        click.echo(f"Creating task with priority {priority}")

    click.echo(click.style(f"Created: {title}", fg='green'))
    if tags:
        click.echo(f"Tags: {', '.join(tags)}")

@cli.command()
@click.option('--city', required=True, prompt='Enter city name', help='City name')
@click.option('--units', type=click.Choice(['metric', 'imperial']), default='metric')
@click.pass_context
def weather(ctx, city, units):
    """Get weather information"""
    if ctx.obj['VERBOSE']:
        click.echo(f"Fetching weather for {city}")

    with click.progressbar(range(100), label='Loading...') as bar:
        for _ in bar:
            pass

    click.echo(click.style(f"\nWeather in {city}:", fg='blue', bold=True))
    click.echo("Temperature: 22°C")
    click.echo("Condition: Sunny ☀️")

@cli.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w'))
def process(input_file, output_file):
    """Process file from INPUT_FILE to OUTPUT_FILE"""
    content = input_file.read()
    processed = content.upper()
    output_file.write(processed)
    click.echo(click.style('File processed successfully!', fg='green'))

if __name__ == '__main__':
    cli(obj={})
```

### requirements.txt

```
click==8.1.7
```

### Dockerfile

```dockerfile
FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
```

### Uso Avanzado con Click

```bash
# Build
docker build -t click-cli .

# Comandos
docker run --rm click-cli --help
docker run --rm click-cli tasks list --filter done
docker run --rm click-cli tasks create "New task" --priority 2 --tags work --tags urgent
docker run --rm click-cli weather --city London

# Con archivos (bind mount)
echo "hello world" > input.txt
docker run --rm \
  -v $(pwd):/data \
  -w /data \
  click-cli process input.txt output.txt
cat output.txt
```

---

## Python con Typer

Typer es Click + Type Hints = CLI moderna con autocomplete.

### cli.py

```python
from typing import Optional, List
from enum import Enum
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="MyApp - Modern CLI tool")
tasks_app = typer.Typer(help="Task management commands")
app.add_typer(tasks_app, name="tasks")

console = Console()

class Status(str, Enum):
    all = "all"
    done = "done"
    pending = "pending"

class Priority(int, Enum):
    low = 1
    medium = 2
    high = 3

@tasks_app.command()
def list(
    filter: Status = typer.Option(Status.all, help="Filter tasks by status"),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """List all tasks"""
    if verbose:
        console.print("[yellow]Verbose mode enabled[/yellow]")

    tasks = [
        {'id': 1, 'title': 'Task 1', 'status': 'done', 'priority': 2},
        {'id': 2, 'title': 'Task 2', 'status': 'pending', 'priority': 3},
    ]

    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Priority")

    for task in tasks:
        if filter.value == "all" or task['status'] == filter.value:
            status_icon = '✓' if task['status'] == 'done' else '○'
            table.add_row(
                str(task['id']),
                task['title'],
                f"{status_icon} {task['status']}",
                str(task['priority'])
            )

    console.print(table)

@tasks_app.command()
def create(
    title: str = typer.Argument(..., help="Task title"),
    priority: Priority = typer.Option(Priority.low, help="Task priority"),
    tags: Optional[List[str]] = typer.Option(None, help="Task tags")
):
    """Create a new task"""
    console.print(f"[green]Created task:[/green] {title}")
    console.print(f"Priority: {priority.value}")
    if tags:
        console.print(f"Tags: {', '.join(tags)}")

@app.command()
def weather(
    city: str = typer.Option(..., prompt="Enter city name"),
    units: str = typer.Option("metric", help="Temperature units")
):
    """Get weather information"""
    with console.status(f"[bold green]Fetching weather for {city}..."):
        import time
        time.sleep(1)

    console.print(f"\n[bold blue]Weather in {city}:[/bold blue]")
    console.print("Temperature: 22°C ☀️")
    console.print("Condition: Sunny")

@app.command()
def interactive():
    """Interactive mode"""
    name = typer.prompt("What's your name?")
    age = typer.prompt("How old are you?", type=int)

    if typer.confirm(f"Is {name} ({age}) correct?"):
        console.print("[green]Information saved![/green]")
    else:
        console.print("[red]Cancelled[/red]")
        raise typer.Abort()

@app.callback()
def callback(
    version: Optional[bool] = typer.Option(None, "--version", "-v", help="Show version")
):
    """
    MyApp - Modern CLI tool with Typer
    """
    if version:
        console.print("MyApp version 1.0.0")
        raise typer.Exit()

if __name__ == "__main__":
    app()
```

### requirements.txt

```
typer[all]==0.9.0
rich==13.7.0
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cli.py .

ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
```

### Autocompletion

```bash
# Generar script de autocompletion
docker run --rm typer-cli --install-completion

# En tu .bashrc o .zshrc
_TYPER_COMPLETE_SCRIPT_DIR=/path/to/scripts
```

---

## Go con Cobra

### Estructura

```
cobra-cli/
├── cmd/
│   ├── root.go
│   ├── weather.go
│   └── tasks/
│       ├── list.go
│       └── create.go
├── main.go
├── go.mod
├── go.sum
└── Dockerfile
```

### Inicializar proyecto

```bash
go mod init myapp
go get -u github.com/spf13/cobra@latest
```

### main.go

```go
package main

import "myapp/cmd"

func main() {
    cmd.Execute()
}
```

### cmd/root.go

```go
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var (
    verbose bool
    cfgFile string
)

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "MyApp - CLI tool for task management and weather",
    Long: `A modern CLI application built with Cobra.
Complete documentation is available at https://github.com/user/myapp`,
    Version: "1.0.0",
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func init() {
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.myapp.yaml)")
}
```

### cmd/weather.go

```go
package cmd

import (
    "fmt"
    "time"

    "github.com/spf13/cobra"
)

var (
    city  string
    units string
)

var weatherCmd = &cobra.Command{
    Use:   "weather",
    Short: "Get weather information",
    Long:  `Fetch and display weather information for a specified city.`,
    Run: func(cmd *cobra.Command, args []string) {
        if verbose {
            fmt.Printf("Fetching weather for %s...\n", city)
        }

        // Simulate API call
        time.Sleep(500 * time.Millisecond)

        fmt.Printf("\n\033[1;34mWeather in %s:\033[0m\n", city)
        fmt.Println("Temperature: 22°C ☀️")
        fmt.Println("Condition: Sunny")
        fmt.Printf("Units: %s\n", units)
    },
}

func init() {
    rootCmd.AddCommand(weatherCmd)

    weatherCmd.Flags().StringVarP(&city, "city", "c", "", "city name (required)")
    weatherCmd.Flags().StringVarP(&units, "units", "u", "metric", "temperature units (metric/imperial)")

    weatherCmd.MarkFlagRequired("city")
}
```

### cmd/tasks/list.go

```go
package tasks

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    filter string
)

type Task struct {
    ID       int
    Title    string
    Status   string
    Priority int
}

var ListCmd = &cobra.Command{
    Use:   "list",
    Short: "List tasks",
    Run: func(cmd *cobra.Command, args []string) {
        tasks := []Task{
            {ID: 1, Title: "Task 1", Status: "done", Priority: 2},
            {ID: 2, Title: "Task 2", Status: "pending", Priority: 3},
            {ID: 3, Title: "Task 3", Status: "pending", Priority: 1},
        }

        fmt.Println("\n\033[1;32mTasks:\033[0m")
        for _, task := range tasks {
            if filter == "all" || task.Status == filter {
                icon := "○"
                color := "\033[33m" // yellow
                if task.Status == "done" {
                    icon = "✓"
                    color = "\033[32m" // green
                }
                fmt.Printf("  %s%s [%d] %s\033[0m (Priority: %d)\n",
                    color, icon, task.ID, task.Title, task.Priority)
            }
        }
    },
}

func init() {
    ListCmd.Flags().StringVarP(&filter, "filter", "f", "all", "filter tasks (all/done/pending)")
}
```

### cmd/tasks/create.go

```go
package tasks

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    priority int
    tags     []string
)

var CreateCmd = &cobra.Command{
    Use:   "create [title]",
    Short: "Create a new task",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        title := args[0]

        fmt.Printf("\033[1;32mCreated task:\033[0m %s\n", title)
        fmt.Printf("Priority: %d\n", priority)
        if len(tags) > 0 {
            fmt.Printf("Tags: %v\n", tags)
        }
    },
}

func init() {
    CreateCmd.Flags().IntVarP(&priority, "priority", "p", 1, "task priority (1-3)")
    CreateCmd.Flags().StringSliceVarP(&tags, "tags", "t", []string{}, "task tags")
}
```

### cmd/tasks/tasks.go

```go
package tasks

import "github.com/spf13/cobra"

var TasksCmd = &cobra.Command{
    Use:   "tasks",
    Short: "Manage tasks",
}

func init() {
    TasksCmd.AddCommand(ListCmd)
    TasksCmd.AddCommand(CreateCmd)
}
```

### Actualizar cmd/root.go

```go
import (
    // ...
    "myapp/cmd/tasks"
)

func init() {
    // ...
    rootCmd.AddCommand(tasks.TasksCmd)
}
```

### Dockerfile

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o myapp .

# Runtime stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copy binary from builder
COPY --from=builder /app/myapp .

ENTRYPOINT ["./myapp"]
CMD ["--help"]
```

### Uso

```bash
# Build
docker build -t myapp-go .

# Run
docker run --rm myapp-go --help
docker run --rm myapp-go weather --city London
docker run --rm myapp-go tasks list --filter pending
docker run --rm myapp-go tasks create "New task" --priority 2 --tags work
```

---

## Go con Cobra + Viper (Configuración)

Viper maneja configuraciones desde archivos, env vars, flags.

### Instalar Viper

```bash
go get github.com/spf13/viper
```

### cmd/root.go (con Viper)

```go
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var cfgFile string

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "MyApp with configuration support",
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}

func init() {
    cobra.OnInitialize(initConfig)

    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.myapp.yaml)")
    rootCmd.PersistentFlags().Bool("verbose", false, "verbose output")

    // Bind flags to viper
    viper.BindPFlag("verbose", rootCmd.PersistentFlags().Lookup("verbose"))
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, err := os.UserHomeDir()
        cobra.CheckErr(err)

        viper.AddConfigPath(home)
        viper.AddConfigPath(".")
        viper.SetConfigType("yaml")
        viper.SetConfigName(".myapp")
    }

    // Environment variables
    viper.SetEnvPrefix("MYAPP")
    viper.AutomaticEnv()

    // Read config
    if err := viper.ReadInConfig(); err == nil {
        fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
    }
}
```

### .myapp.yaml (config file)

```yaml
verbose: true

weather:
  default_city: "London"
  units: "metric"
  api_key: "your-api-key"

tasks:
  default_priority: 2
  auto_tags:
    - "work"

database:
  host: "localhost"
  port: 5432
  name: "myapp"
```

### Usar configuración en comandos

```go
package cmd

import (
    "fmt"
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var weatherCmd = &cobra.Command{
    Use:   "weather",
    Short: "Get weather",
    Run: func(cmd *cobra.Command, args []string) {
        // Get from config
        city := viper.GetString("weather.default_city")
        units := viper.GetString("weather.units")
        apiKey := viper.GetString("weather.api_key")

        // Override from flag if provided
        if cmd.Flags().Changed("city") {
            city, _ = cmd.Flags().GetString("city")
        }

        fmt.Printf("City: %s, Units: %s\n", city, units)
        fmt.Printf("API Key: %s\n", apiKey)
    },
}

func init() {
    rootCmd.AddCommand(weatherCmd)

    weatherCmd.Flags().String("city", "", "city name")

    // Bind to viper
    viper.BindPFlag("weather.default_city", weatherCmd.Flags().Lookup("city"))
}
```

### docker-compose.yml (con config file)

```yaml
version: '3.8'

services:
  cli:
    build: .
    volumes:
      - ./config.yaml:/root/.myapp.yaml:ro
    environment:
      - MYAPP_VERBOSE=true
      - MYAPP_WEATHER_API_KEY=secret-key
```

---

## CLI Tools Complejas

### Multi-comando con subcomandos anidados

```
myapp
├── config
│   ├── get <key>
│   ├── set <key> <value>
│   └── list
├── db
│   ├── migrate
│   ├── seed
│   └── reset
├── server
│   ├── start [--port]
│   └── stop
└── deploy
    ├── staging
    └── production
```

### Dockerfile multi-stage con múltiples entrypoints

```dockerfile
FROM python:3.11-slim AS base

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Default CLI
FROM base AS cli
ENTRYPOINT ["python", "cli.py"]

# Server mode
FROM base AS server
ENTRYPOINT ["python", "server.py"]

# Worker mode
FROM base AS worker
ENTRYPOINT ["python", "worker.py"]
```

### Build específico

```bash
docker build --target cli -t myapp:cli .
docker build --target server -t myapp:server .
docker build --target worker -t myapp:worker .
```

---

## Distribución de CLI Tools

### 1. Docker Image en Docker Hub

```bash
# Build
docker build -t username/myapp:latest .

# Push
docker login
docker push username/myapp:latest

# Usuarios pueden usar
docker run --rm username/myapp:latest --help
```

### 2. Alias para facilitar uso

```bash
# Agregar a ~/.bashrc o ~/.zshrc
alias myapp='docker run --rm -v $(pwd):/data username/myapp:latest'

# Ahora se usa como comando nativo
myapp tasks list
myapp weather --city Paris
```

### 3. Script wrapper

**install.sh:**
```bash
#!/bin/bash

cat > /usr/local/bin/myapp << 'EOF'
#!/bin/bash
docker run --rm -it -v $(pwd):/data username/myapp:latest "$@"
EOF

chmod +x /usr/local/bin/myapp

echo "myapp installed successfully!"
echo "Usage: myapp --help"
```

### 4. Binarios compilados (Go)

```bash
# Build for múltiples plataformas
GOOS=linux GOARCH=amd64 go build -o myapp-linux-amd64
GOOS=darwin GOARCH=amd64 go build -o myapp-darwin-amd64
GOOS=windows GOARCH=amd64 go build -o myapp-windows-amd64.exe

# Distribuir binarios o usar Docker
```

---

## Mejores Prácticas

### 1. Help Text Claro

```python
"""
MyApp - Task Management CLI

Usage:
  myapp tasks list [--filter=<status>]
  myapp tasks create <title> [--priority=<n>]
  myapp weather --city=<city>

Options:
  -h --help     Show this screen.
  --version     Show version.
  -v --verbose  Verbose output.
"""
```

### 2. Manejo de Errores

```python
try:
    result = api_call()
except APIError as e:
    click.echo(click.style(f"Error: {e}", fg='red'), err=True)
    sys.exit(1)
```

### 3. Colored Output

```go
// ANSI color codes
const (
    Reset  = "\033[0m"
    Red    = "\033[31m"
    Green  = "\033[32m"
    Yellow = "\033[33m"
    Blue   = "\033[34m"
)

fmt.Printf("%s✓ Success%s\n", Green, Reset)
```

### 4. Progress Bars

```python
import click

with click.progressbar(items, label='Processing') as bar:
    for item in bar:
        process(item)
```

### 5. Interactive Prompts

```python
if click.confirm('Do you want to continue?'):
    proceed()
else:
    abort()
```

---

## Testing CLI Apps

### Python (pytest)

```python
from click.testing import CliRunner
from cli import cli

def test_weather_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['weather', '--city', 'London'])
    assert result.exit_code == 0
    assert 'Weather' in result.output
```

### Go

```go
func TestWeatherCmd(t *testing.T) {
    cmd := weatherCmd
    cmd.SetArgs([]string{"--city", "London"})

    err := cmd.Execute()
    assert.NoError(t, err)
}
```

---

## Resumen: Cuándo Usar Cada Herramienta

| Tool | Mejor Para | Nivel |
|------|-----------|-------|
| **Argparse** | CLIs simples, Python stdlib | Principiante |
| **Click** | CLIs modernas con decoradores | Intermedio |
| **Typer** | CLIs con type hints y autocompletion | Avanzado |
| **Cobra** | CLIs complejas en Go, alta performance | Intermedio |
| **Cobra + Viper** | CLIs con configuración compleja | Avanzado |

---

¡Las aplicaciones CLI containerizadas son portables y fáciles de distribuir!
