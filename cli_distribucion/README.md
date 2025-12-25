# MyCLI - Ejemplo de Distribución Profesional en Go

Este proyecto demuestra cómo crear y distribuir una CLI en Go con **zero instalación** - un solo binario, sin dependencias.

## 🎯 Lo Importante: Distribución

Este ejemplo se enfoca en **cómo distribuir** una CLI, no en el código en sí.

### ✅ Ventajas de Go para CLIs

1. **Binario único**: Un solo archivo ejecutable
2. **Zero dependencias**: No requiere runtime instalado
3. **Cross-compilation**: Build para cualquier plataforma desde una sola máquina
4. **Tamaño razonable**: ~5-10MB (vs Python que requiere 100MB+ con venv)
5. **Distribución simple**: `curl | bash` o descarga directa

---

## 🚀 Instalación (Para Usuarios)

### Instalación Automática (Recomendado)

```bash
curl -sSL https://raw.githubusercontent.com/tuuser/mycli/main/install.sh | bash
```

### Instalación Manual

1. Descarga el binario para tu plataforma desde [Releases](https://github.com/tuuser/mycli/releases/latest)

2. Extrae el archivo:
```bash
# Linux/macOS
tar -xzf mycli-linux-amd64.tar.gz

# Windows
unzip mycli-windows-amd64.zip
```

3. Mueve a tu PATH:
```bash
# Linux/macOS
mv mycli /usr/local/bin/
# o
mv mycli ~/bin/

# Windows
move mycli.exe C:\Windows\System32\
```

4. Verifica la instalación:
```bash
mycli version
```

### Instalación con Homebrew (macOS/Linux)

```bash
brew tap tuuser/tap
brew install mycli
```

---

## 🔨 Para Desarrolladores

### Requisitos

- Go 1.21+
- Make (opcional pero recomendado)

### Setup Inicial

```bash
# Clonar repo
git clone https://github.com/tuuser/mycli.git
cd mycli

# Instalar dependencias
go mod download

# Build local
make build

# O sin Make
go build -o build/mycli .
```

### Comandos Make Disponibles

```bash
make help                # Muestra todos los comandos

make build              # Build para tu plataforma actual
make build-all          # Build para TODAS las plataformas
make dist               # Crea archivos .tar.gz y .zip
make release            # Build completo + checksums
make install            # Instala en ~/bin
make clean              # Limpia build artifacts
make test               # Ejecuta tests
make size               # Muestra tamaño del binario
```

### Build Manual (sin Make)

```bash
# Build simple
go build -o mycli .

# Build con version info
go build -ldflags "-X main.version=v1.0.0 -X main.commit=$(git rev-parse --short HEAD) -X main.date=$(date -u +%Y-%m-%dT%H:%M:%SZ)" -o mycli .

# Build optimizado (más pequeño)
go build -ldflags "-s -w" -o mycli .
```

---

## 📦 Cross-Compilation (La Magia de Go)

Build para TODAS las plataformas desde tu máquina:

```bash
# Linux AMD64
GOOS=linux GOARCH=amd64 go build -o mycli-linux-amd64 .

# Linux ARM64 (Raspberry Pi, servidores ARM)
GOOS=linux GOARCH=arm64 go build -o mycli-linux-arm64 .

# macOS Intel
GOOS=darwin GOARCH=amd64 go build -o mycli-darwin-amd64 .

# macOS Apple Silicon (M1/M2)
GOOS=darwin GOARCH=arm64 go build -o mycli-darwin-arm64 .

# Windows
GOOS=windows GOARCH=amd64 go build -o mycli-windows-amd64.exe .

# Todo en un comando
make build-all
```

### Plataformas Soportadas

Go puede compilar para 20+ plataformas:

```bash
go tool dist list

# Ejemplos:
# linux/amd64, linux/arm64, linux/386
# darwin/amd64, darwin/arm64
# windows/amd64, windows/386
# freebsd/amd64
# openbsd/amd64
# netbsd/amd64
# solaris/amd64
```

---

## 🎉 Crear un Release

### Opción 1: GitHub Actions (Automático)

```bash
# 1. Crear tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 2. Push tag
git push origin v1.0.0

# 3. GitHub Actions automáticamente:
#    - Builda para todas las plataformas
#    - Crea archivos .tar.gz y .zip
#    - Genera checksums SHA256
#    - Crea GitHub Release
#    - Sube todos los artifacts
```

### Opción 2: Manual

```bash
# 1. Build para todas las plataformas
make release VERSION=v1.0.0

# 2. Verifica los archivos en dist/
ls -lh dist/

# 3. Sube a GitHub Releases manualmente
```

---

## 📊 Comparación: Go vs Python

### Distribución Python (Problemática)

```bash
# Usuario necesita:
1. Python instalado (50-100MB)
2. pip install mycli
3. Manejar virtual environments
4. Resolver conflictos de dependencias
5. pyenv/conda para diferentes versiones

# Problemas:
- "Works on my machine"
- Dependency hell
- Versiones de Python incompatibles
- Tamaño grande (~100MB+ con deps)
```

### Distribución Go (Simple)

```bash
# Usuario necesita:
1. Descargar 1 binario (5-10MB)
2. chmod +x mycli
3. ./mycli

# Ventajas:
✅ Zero dependencias
✅ Funciona en cualquier máquina
✅ Un solo archivo
✅ Rápido startup (<1ms vs 100ms+ Python)
```

---

## 🔐 Verificación de Integridad

### Generar Checksums

```bash
make checksums

# O manualmente
shasum -a 256 dist/*.tar.gz dist/*.zip > dist/SHA256SUMS
```

### Verificar Descarga

```bash
# Después de descargar un binario
shasum -a 256 mycli-linux-amd64.tar.gz

# Comparar con SHA256SUMS
cat SHA256SUMS
```

---

## 📦 Métodos de Distribución

### 1. GitHub Releases (Más Común)

```yaml
# .github/workflows/release.yml ya configurado
# Automático en cada tag
```

**Pros:**
- Gratis
- CI/CD integrado
- Fácil para usuarios

### 2. Homebrew (macOS/Linux)

```ruby
# Formula: homebrew-tap/mycli.rb
class Mycli < Formula
  desc "Mi CLI de ejemplo"
  homepage "https://github.com/tuuser/mycli"
  url "https://github.com/tuuser/mycli/releases/download/v1.0.0/mycli-darwin-arm64.tar.gz"
  sha256 "abc123..."
  version "1.0.0"

  def install
    bin.install "mycli"
  end
end
```

### 3. apt/yum Repository (Linux)

```bash
# Para distribuciones Linux
# Requiere setup de repositorio
# Ver: https://github.com/jordansissel/fpm
```

### 4. Docker Image

```dockerfile
FROM scratch
COPY mycli /mycli
ENTRYPOINT ["/mycli"]
```

```bash
docker build -t mycli:latest .
docker run mycli:latest version
```

### 5. Script de Instalación

El `install.sh` incluido:
- Detecta OS y arquitectura
- Descarga binario correcto
- Instala en PATH
- Verifica instalación

---

## 📏 Tamaño de Binarios

```bash
# Ver tamaño
make size

# Ejemplo de output:
# mycli: 8.2M

# Optimizaciones:
# 1. -ldflags "-s -w" (quita símbolos de debug)
# 2. UPX compression (opcional)
upx --best --lzma mycli
# Resultado: 8.2M -> 2.1M
```

---

## 🧪 Testing de Distribución

```bash
# Test en diferentes plataformas
make build-all

# Test en Docker (Linux)
docker run --rm -v $PWD/dist:/dist ubuntu:latest /dist/mycli-linux-amd64 version

# Test en macOS
./dist/mycli-darwin-arm64 version

# Test instalador
bash install.sh
```

---

## 🎯 Mejores Prácticas

### 1. Versioning Semántico

```bash
v1.0.0  # Major.Minor.Patch
v1.0.0-rc.1  # Release Candidate
v1.0.0-beta.1  # Beta
```

### 2. Changelog

```markdown
## v1.0.0 - 2024-01-15

### Added
- Feature X
- Feature Y

### Fixed
- Bug Z

### Changed
- Updated dependency
```

### 3. Release Notes Automáticas

```bash
# Generar desde commits
git log v0.9.0..v1.0.0 --oneline --pretty=format:"- %s"
```

### 4. Firma de Binarios

```bash
# GPG signing
gpg --detach-sign --armor mycli-linux-amd64

# Usuarios verifican:
gpg --verify mycli-linux-amd64.asc mycli-linux-amd64
```

---

## 🚀 Deploy a Producción

### GitHub Releases

1. Tag y push → automático
2. Usuarios descargan desde releases
3. Update con `curl | bash` o nuevo download

### Update Automático en CLI

```go
// Agregar comando 'update'
func checkForUpdates() {
    // Compara version actual con latest en GitHub
    // Descarga nuevo binario
    // Reemplaza ejecutable actual
}
```

### Homebrew

```bash
# Actualizar formula
cd homebrew-tap
vim mycli.rb  # Update version and sha256
git commit -am "Update to v1.0.0"
git push

# Usuarios actualizan
brew upgrade mycli
```

---

## 📊 Métricas de Distribución

### Download Stats (GitHub)

```bash
# API de GitHub
curl https://api.github.com/repos/tuuser/mycli/releases/latest

# Ver descargas
# Campo: assets[].download_count
```

### Analytics en install.sh

```bash
# Opcional: track installs
curl -s "https://analytics.example.com/install?os=$OS&arch=$ARCH&version=$VERSION"
```

---

## 🔧 Troubleshooting

### Binario no ejecuta

```bash
# Verificar permisos
chmod +x mycli

# Verificar arquitectura
file mycli
# Output: Mach-O 64-bit executable arm64
```

### "Permission Denied" en macOS

```bash
# macOS Gatekeeper
xattr -d com.apple.quarantine mycli
```

### "Cannot find binary" después de instalar

```bash
# Verificar PATH
echo $PATH

# Agregar ~/bin a PATH
echo 'export PATH="$PATH:$HOME/bin"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📚 Recursos

- [Go Cross Compilation](https://go.dev/doc/install/source#environment)
- [GoReleaser](https://goreleaser.com/) - Automatiza releases
- [Cobra](https://github.com/spf13/cobra) - Framework para CLIs
- [Homebrew Tap](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)

---

## 🎓 Conclusión

**Go hace la distribución de CLIs TRIVIAL:**

1. Build una vez → funciona en todas partes
2. Un archivo → zero instalación
3. Cross-compile → todas las plataformas
4. GitHub Actions → releases automáticos
5. Usuarios felices → `curl | bash` y listo

**Esto es IMPOSIBLE de lograr así con Python.**

---

## 📝 Licencia

MIT
