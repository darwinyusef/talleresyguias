#!/bin/bash
# check-cluster.sh - Diagnóstico rápido del estado del clúster de K8s

echo "☸️ Iniciando diagnóstico de Kubernetes..."
echo "----------------------------------------"

# 1. Verificar Nodos
echo "📍 Estado de los Nodos:"
kubectl get nodes
echo ""

# 2. Verificar Namespaces del taller
echo "📁 Namespaces activos:"
kubectl get ns | grep -E 'fullstack|microservices|ml|workshop'
echo ""

# 3. Verificar Recursos en los namespaces del taller
for ns in fullstack-app microservices-shop ml-production workshop-ga; do
    echo "🔍 Resumen de recursos en: $ns"
    kubectl get pods,svc,deploy,hpa -n $ns 2>/dev/null || echo "   (Vacío)"
    echo "----------------------------------------"
done

# 4. Verificar uso de CPU/Memoria (Requiere Metrics Server)
echo "📊 Consumo de recursos (Top Pods):"
kubectl top pods --all-namespaces | sort -rn -k 3 | head -n 10 2>/dev/null || echo "   (Metrics Server no disponible)"
echo ""

echo "✅ Diagnóstico completado."
