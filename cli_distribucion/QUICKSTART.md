# 🚀 Guía Rápida de Distribución

## Para Desarrolladores: Crear tu Primera Release

### 1. Setup Inicial

```bash
# Inicializar módulo Go
go mod init github.com/tuusuario/tucli

# Copiar archivos de este ejemplo
cp -r /path/to/cli_distribucion/* .

# Editar main.go con tu lógica
vim main.go
```

### 2. Desarrollo Local

```bash
# Build y test
make build
./build/mycli version

# Instalar localmente
make install
mycli version
```

### 3. Crear Primera Release

```bash
# 1. Commit tu código
git add .
git commit -m "Initial release"

# 2. Crear tag
git tag -a v1.0.0 -m "First release"

# 3. Push (incluye tag)
git push origin main
git push origin v1.0.0

# 4. GitHub Actions crea automáticamente:
#    ✅ Binarios para todas las plataformas
#    ✅ Archivos comprimidos
#    ✅ Checksums SHA256
#    ✅ GitHub Release página
```

### 4. Verificar Release

```bash
# Ve a: https://github.com/tuusuario/tucli/releases
# Deberías ver:
# - mycli-linux-amd64.tar.gz
# - mycli-linux-arm64.tar.gz
# - mycli-darwin-amd64.tar.gz
# - mycli-darwin-arm64.tar.gz
# - mycli-windows-amd64.zip
# - SHA256SUMS
```

---

## Para Usuarios: Instalar la CLI

### Método 1: Script de Instalación (Recomendado)

```bash
curl -sSL https://raw.githubusercontent.com/tuusuario/tucli/main/install.sh | bash
```

### Método 2: Download Manual

```bash
# 1. Ve a releases
# https://github.com/tuusuario/tucli/releases/latest

# 2. Descarga para tu plataforma
curl -LO https://github.com/tuusuario/tucli/releases/download/v1.0.0/mycli-linux-amd64.tar.gz

# 3. Extrae
tar -xzf mycli-linux-amd64.tar.gz

# 4. Mueve a PATH
sudo mv mycli-linux-amd64 /usr/local/bin/mycli

# 5. Verifica
mycli version
```

### Método 3: Docker

```bash
docker run ghcr.io/tuusuario/tucli:latest version
```

---

## Distribución Avanzada

### Homebrew Tap

```bash
# 1. Crear repositorio homebrew-tap
# 2. Agregar formula:

# homebrew-tap/mycli.rb
class Mycli < Formula
  desc "Mi CLI"
  homepage "https://github.com/tuusuario/mycli"
  url "https://github.com/tuusuario/mycli/releases/download/v1.0.0/mycli-darwin-arm64.tar.gz"
  sha256 "ACTUAL_SHA256_HERE"
  version "1.0.0"

  def install
    bin.install "mycli-darwin-arm64" => "mycli"
  end

  test do
    system "#{bin}/mycli", "version"
  end
end

# 3. Usuarios instalan:
brew tap tuusuario/tap
brew install mycli
```

### APT Repository (Debian/Ubuntu)

```bash
# Usar: https://github.com/jordansissel/fpm
fpm -s dir -t deb -n mycli -v 1.0.0 \
    --prefix /usr/local/bin \
    mycli=/usr/local/bin/mycli
```

### NPM (sí, puedes publicar binarios Go en npm!)

```json
{
  "name": "mycli",
  "version": "1.0.0",
  "bin": {
    "mycli": "./bin/mycli"
  },
  "scripts": {
    "postinstall": "node install.js"
  }
}
```

---

## Comparación Real: Python vs Go

### Python CLI

```bash
# Distribución:
1. Escribir setup.py
2. Build wheel: python setup.py bdist_wheel
3. Upload a PyPI: twine upload dist/*
4. Usuario instala: pip install mycli

# Problemas:
- Requiere Python instalado
- Dependencias pueden fallar
- Virtual envs complejos
- Startup lento (100-500ms)
- Tamaño grande (50MB+ con deps)
```

### Go CLI

```bash
# Distribución:
1. git tag v1.0.0
2. git push origin v1.0.0
3. GitHub Actions hace todo automáticamente

# Ventajas:
- Un archivo ejecutable
- Zero dependencias
- Startup instantáneo (<1ms)
- Tamaño pequeño (5-10MB)
- Cross-platform automático
```

---

## Métricas Reales

### Ejemplo: Docker CLI (Go)

```
Tamaño: 60MB
Plataformas: 10+
Instalaciones: Millones
Método: curl -fsSL https://get.docker.com | sh
```

### Ejemplo: AWS CLI (Python)

```
Tamaño: ~100MB
Requiere: Python 3.8+
Instalación: pip install awscli
Problemas comunes: conflictos de dependencias
```

---

## Checklist Pre-Release

```bash
✅ Tests pasan: make test
✅ Build funciona: make build-all
✅ Version actualizada en código
✅ Changelog actualizado
✅ README actualizado
✅ install.sh funciona
✅ GitHub Actions configurado
✅ Tag semántico (v1.0.0)
```

---

## Automatización Completa

### GoReleaser (Alternativa Profesional)

```bash
# Instalar GoReleaser
brew install goreleaser/tap/goreleaser

# .goreleaser.yml
project_name: mycli

builds:
  - env: [CGO_ENABLED=0]
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]

archives:
  - format: tar.gz
    name_template: "{{ .ProjectName }}-{{ .Os }}-{{ .Arch }}"

checksum:
  name_template: 'SHA256SUMS'

release:
  github:
    owner: tuusuario
    name: mycli

# Crear release
goreleaser release --clean
```

---

## Monitoring de Distribución

### GitHub Release Stats

```bash
# API de GitHub
curl -H "Authorization: token GITHUB_TOKEN" \
  https://api.github.com/repos/tuusuario/mycli/releases/latest

# Downloads por asset
jq '.assets[] | {name: .name, downloads: .download_count}'
```

### Analytics en install.sh

```bash
# Opcional: agregar en install.sh
curl -s "https://plausible.io/api/event" \
  -d '{"name":"install","domain":"mycli.com"}'
```

---

## Troubleshooting Común

### 1. "Binary not found" después de instalar

```bash
# Verificar PATH
echo $PATH | grep -o "$HOME/bin"

# Agregar a PATH
echo 'export PATH="$PATH:$HOME/bin"' >> ~/.zshrc
source ~/.zshrc
```

### 2. macOS: "mycli cannot be opened"

```bash
# Remover quarantine
xattr -d com.apple.quarantine mycli
```

### 3. Linux: "Permission denied"

```bash
chmod +x mycli
```

### 4. Build falla en CI

```bash
# Verificar go.mod
go mod tidy
go mod verify

# Test local
make build-all
```

---

## Next Steps

1. **Personaliza** el código en `main.go`
2. **Configura** GitHub repository
3. **Crea** primer release: `git tag v1.0.0 && git push origin v1.0.0`
4. **Comparte** el instalador: `curl -sSL ... | bash`
5. **Itera** basado en feedback

---

## Recursos

- [Ejemplo completo](https://github.com/cli/cli) - GitHub CLI (gh)
- [GoReleaser](https://goreleaser.com/)
- [Cobra Framework](https://github.com/spf13/cobra)
- [Homebrew Tap Guide](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)

¡Feliz distribución! 🚀
