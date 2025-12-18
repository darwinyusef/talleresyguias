# 🚀 Quick Start Guide - MLOps Platform

Guía rápida para comenzar en **5 minutos**.

## ✅ Pre-requisitos

```bash
# Verificar instalaciones
docker --version        # Docker 24.0+
docker compose version  # Docker Compose 2.23+
python --version        # Python 3.11+
make --version         # GNU Make
```

## 🏁 Inicio Rápido (5 minutos)

### Opción 1: Make (Recomendado)

```bash
# 1. Todo en uno
make quickstart

# Eso es todo! 🎉
```

### Opción 2: Manual

```bash
# 1. Configurar entorno
cp .env.example .env
mkdir -p data models logs

# 2. Build imágenes
docker compose build

# 3. Iniciar servicios
docker compose up -d

# 4. Verificar
docker compose ps
```

## 🔍 Verificar Instalación

```bash
# Ver servicios activos
make ps
# o
docker compose ps

# Verificar salud
curl http://localhost:8000/health  # PyTorch
curl http://localhost:8001/health  # TensorFlow
curl http://localhost:8002/health  # RAG
```

## 🌐 Acceder a UIs

Abre en tu navegador:

- **MLflow**: http://localhost:5000
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090
- **RabbitMQ**: http://localhost:15672 (admin/admin123)

## 🧪 Probar el Sistema

### 1. Indexar documentos en RAG

```bash
python scripts/test_rag.py --index
```

### 2. Hacer queries

```bash
python scripts/test_rag.py --query "What is PyTorch?" --top-k 3
```

### 3. Modo interactivo

```bash
python scripts/test_rag.py --interactive
```

### 4. Entrenar un modelo

```bash
python scripts/train_model.py --epochs 5 --lr 0.001
```

## 📊 Monitoreo

```bash
# Ver logs en tiempo real
make logs

# Logs de servicio específico
make logs-pytorch
make logs-rag

# Métricas
open http://localhost:9090  # Prometheus
```

## 🛑 Detener Servicios

```bash
# Detener
make down
# o
docker compose down

# Detener y limpiar todo
docker compose down -v
```

## 🔧 Troubleshooting

### Problema: Puertos ocupados

```bash
# Verificar puertos
lsof -i :8000
lsof -i :5672

# Cambiar puertos en docker-compose.yml
```

### Problema: Build falla

```bash
# Limpiar cache de Docker
docker system prune -a
make clean-docker
```

### Problema: Servicios no healthy

```bash
# Ver logs
make logs

# Reiniciar servicio específico
docker compose restart pytorch-service
```

## 📚 Siguientes Pasos

1. ✅ **Lee la documentación**: `README.md`
2. ✅ **Explora el taller**: `../TALLER_MLOPS_DOCKER_EVENT_DRIVEN_COMPLETO.md`
3. ✅ **Prueba Ansible**: `cd ansible && cat README.md`
4. ✅ **Personaliza**: Modifica `src/` según tus necesidades

## 💡 Comandos Útiles

```bash
make help           # Ver todos los comandos disponibles
make test           # Ejecutar tests
make format         # Formatear código
make shell-pytorch  # Shell en contenedor PyTorch
```

---

**¡Listo para empezar! 🎉**
