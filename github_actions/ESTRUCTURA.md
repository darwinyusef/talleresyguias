# 📁 Estructura del Taller - GitHub Actions + Docker

```
github_actions/
├── README.md                          # Guía principal y teoría
├── INDICE.md                          # Índice de navegación
├── INICIO_RAPIDO.md                   # Guía de 5 minutos
├── EJERCICIOS.md                      # Listado de prácticas por niveles
├── ESTRUCTURA.md                      # Este archivo
├── RESUMEN.md                         # Resumen ejecutivo
│
├── docker/                            # Recursos Docker genéricos
│   ├── Dockerfile                     # Ejemplo multi-stage universal
│   └── docker-compose.yml             # Ejemplo de despliegue con servicios
│
├── pipeline/                          # Ejemplos de flujos (.yml)
│   ├── basic-ci.yml                   # CI básico (Manual/Push)
│   ├── docker-publish.yml             # Publicación a registros (Tags)
│   ├── deploy-ssh.yml                 # Despliegue remoto (CD)
│   ├── multi-language-ci.yml          # CI Monorepo
│   ├── k8s-deploy.yml                 # CD GitOps K8s
│   ├── security-scan.yml              # Seguridad (Trivy/Hadolint)
│   ├── scripted-python-ci.yml         # CI vía Scripts Bash
│   ├── tag-and-release.yml            # Tags & Releases
│   └── caller-workflow.yml            # Ejemplo de llamadas a otros recursos
│
├── github/                            # Recursos de reutilización de GitHub
│   ├── reusable-workflows/            # Templates compartidos
│   ├── composite-actions/             # Acciones locales personalizadas
│   └── external-projects/             # Integración con otros repositorios
│
├── scripts/                          # Scripts Bash (.sh)
│   ├── docker-check.sh                # Verificador
│   ├── docker-cleanup.sh              # Limpiador
│   └── setup-python-env.sh            # Setup Python
│
├── kubernetes/                        # Manifiestos de Kubernetes
│   ├── base/                          # Namespace y Base
│   ├── nodejs-app/                    # Deploy/Svc Node.js
│   ├── python-fastapi/                # Deploy/Svc FastAPI
│   └── ...                            # Otros servicios
│
└── ejemplos/                          # Proyectos completos de ejemplo
    ├── nodejs-app/                    # Aplicación Node.js
    ├── python-fastapi/                # API con FastAPI
    ├── ml-sklearn/                    # Machine Learning Iris
    ├── dl-tensorflow/                 # Deep Learning Dummy
    └── go-fiber/                      # API con Go Fiber
```

---

## 📊 Resumen por Nivel
- **Nivel 1**: Fundamentos, Triggers, Hadolint.
- **Nivel 2**: Docker Hub, GHCR, Multi-arch.
- **Nivel 3**: needs, steps outputs, cache, trivy.
- **Nivel 4**: SSH, Environments, Manual Approvals.
