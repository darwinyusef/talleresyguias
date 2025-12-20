# 📁 Estructura del Proyecto: Kubernetes

Organización jerárquica de manifiestos y guías.

```
k8s/
├── 📚 DOCUMENTACIÓN
│   ├── README.md               # Manual teórico y guía maestra
│   ├── INDICE.md               # Mapa de contenidos
│   ├── INICIO_RAPIDO.md        # Guía de instalación y primer pod
│   ├── EJERCICIOS.md           # Retos prácticos por dificultad
│   └── RESUMEN.md              # Resumen del workshop
│
├── 🌐 NETWORKING & SEGURIDAD
│   └── manifiestos/
│       ├── networking/
│       │   └── advanced-networking.yaml # Ingress + NetworkPolicy
│       ├── config/                    # ConfigMaps y Secrets
│       └── storage/                   # PV, PVC y StorageClasses
│
├── 📦 GESTIÓN DE PAQUETES (HELM)
│   └── charts/
│       └── fullstack-app/             # Chart.yaml, values.yaml
│
├── 🎯 ORQUESTACIONES (PROYECTOS)
│   ├── fullstack/
│   │   ├── 01-base-config.yaml # Secrets y CM
│   │   ├── 02-database.yaml    # Postgres + PVC
│   │   └── 03-services.yaml    # API + Redis + Svc
│   │
│   ├── microservicios/
│   │   └── orchestration.yaml  # Go + Python + RabbitMQ
│   │
│   └── ml-serving/
│       └── production-ready.yaml # HA + HPA + Probes
│
└── 🛠️ HERRAMIENTAS
    └── scripts/
        ├── check-cluster.sh    # Script de diagnóstico
        └── cleanup.sh          # Script para borrar deployments
```

---

[Ir al Índice](./INDICE.md) • [Volver al README](./README.md)
