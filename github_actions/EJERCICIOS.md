# 🎯 Ejercicios: GitHub Actions + Docker

Practica desde lo más básico hasta flujos complejos de producción.

---

## 🟢 Nivel 1: Fundamentos (Intro)

### Ejercicio 1.1: El "Hello World"
**Objetivo**: Crear un workflow que imprima mensajes y versiones.
- Crea un workflow que se dispare manualmente (`workflow_dispatch`).
- Imprime la versión de `docker` y `docker-compose` instalada en el runner.
- Imprime el nombre de la rama en la que se está ejecutando.

### Ejercicio 1.2: Validando el Dockerfile
**Objetivo**: Usar Hadolint para validar buenas prácticas en tu Dockerfile.
- Investiga la action `hadolint/hadolint-action`.
- Configura un workflow que se ejecute en cada `pull_request`.
- Haz que el build falle si hay advertencias de seguridad críticas.

---

## 🟡 Nivel 2: Integración con Registries

### Ejercicio 2.1: Publicando en Docker Hub
**Objetivo**: Subir tu imagen a Docker Hub.
- Sube tus credenciales (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) a GitHub Secrets.
- Configura el workflow para que solo suba la imagen cuando se cree un `tag` (ej: `v1.0.0`).

### Ejercicio 2.2: Multi-plataforma (Buildx)
**Objetivo**: Construir imágenes para `amd64` y `arm64` simultáneamente.
- Usa `docker/setup-qemu-action` y `docker/setup-buildx-action`.
- Configura el build para soportar ambas arquitecturas.

---

## 🔴 Nivel 3: CI/CD y Calidad

### Ejercicio 3.1: Pipeline de Tests
**Objetivo**: Solo construir la imagen si los tests pasan.
- Crea un job `test` que instale dependencias y corra tests unitarios.
- Crea un job `build` que dependa de `test` (`needs: test`).
- Si los tests fallan, la imagen no debe construirse.

### Ejercicio 3.2: Escaneo de Seguridad
**Objetivo**: Escanear la imagen final en busca de vulnerabilidades.
- Usa la action oficial de `aquasecurity/trivy-action`.
- Reporta los resultados en la pestaña "Security" de GitHub (requiere GitHub Advanced Security o repo público).

---

## 🔥 Nivel 4: Despliegue Avanzado

### Ejercicio 4.1: Deploy vía SSH
**Objetivo**: Notificar a tu servidor que hay una nueva imagen disponible.
- Una vez la imagen está en el Registry, conéctate vía SSH a un servidor.
- Ejecuta `docker compose pull && docker compose up -d`.

### Ejercicio 4.2: Ambientes y Aprobaciones
**Objetivo**: Crear un flujo de aprobación manual.
- Define un ambiente llamado `production` en GitHub.
- Configura un workflow que despliegue a producción solo después de que un administrador apruebe el Job.

---

## 🏗️ Nivel 5: Orquestación con Kubernetes

### Ejercicio 5.1: Despliegue en Cluster Local (k3d/kind)
**Objetivo**: Aplicar los manifiestos creados en un entorno de pruebas.
- Instala `kubectl` en tu máquina local.
- Crea un nuevo `Namespace` llamado `taller-ga`.
- Aplica el `Deployment` de la app Node.js y verifica que los pods estén `Running`.

### Ejercicio 5.2: GitOps Flow
**Objetivo**: Automatizar el despliegue al clúster cada vez que cambie un manifiesto.
- Configura un `KUBE_CONFIG` en tus GitHub Secrets.
- Usa el workflow `k8s-deploy.yml` para desplegar automáticamente al clúster al hacer push a la carpeta `kubernetes/`.

---

[Ir al Índice](./INDICE.md) • [Volver al README](./README.md)
