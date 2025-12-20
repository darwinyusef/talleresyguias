# ⚡ Inicio Rápido: GitHub Actions + Docker

Configura tu primer flujo de CI/CD en menos de 5 minutos.

## 1. Requisitos
- Repositorio en GitHub.
- Un `Dockerfile` en la raíz de tu proyecto.

## 2. Crea tu primer Workflow
Crea la carpeta `.github/workflows/` (si no existe) y dentro el archivo `docker-ci.yml`:

```yaml
name: Docker Build & Push

on:
  push:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

## 3. ¿Qué acaba de pasar?
1. **Checkout**: GitHub Actions descarga tu código en el Runner (la máquina virtual).
2. **Login**: Se autentica automáticamente en el GitHub Container Registry usando el token interno.
3. **Build & Push**: Construye tu imagen basada en tu `Dockerfile` y la sube al registro de GitHub asociada a tu cuenta.

## 4. Verifica los resultados
1. Ve a la pestaña **Actions** de tu repositorio.
2. Verás el flujo ejecutándose.
3. Una vez termine, ve a tu perfil o organización en la sección **Packages** para ver tu imagen Docker.

---

## 💡 Tips de Oro
- **Secrets**: Nunca pongas contraseñas en el YAML. Usa `Settings > Secrets and variables > Actions`.
- **Linting**: Usa la extension de VS Code "GitHub Actions" para validar la sintaxis de tus archivos YAML.
- **Runners**: Por defecto usas `ubuntu-latest`, que es gratuito para repositorios públicos.

[Ver Ejercicios Prácticos](./EJERCICIOS.md)
