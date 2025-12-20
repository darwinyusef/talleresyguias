#!/bin/bash
# cleanup.sh - Borra todos los recursos creados durante el taller

echo "⚠️  ATENCIÓN: Se van a borrar todos los namespaces del taller."
echo "Namespaces afectados: fullstack-app, microservices-shop, ml-production, workshop-ga"
read -p "¿Estás seguro? (y/n): " confirm

if [[ $confirm == "y" ]]; then
    echo "🗑️  Borrando recursos..."
    kubectl delete ns fullstack-app --wait=false
    kubectl delete ns microservices-shop --wait=false
    kubectl delete ns ml-production --wait=false
    kubectl delete ns workshop-ga --wait=false
    echo "✅ Los procesos de borrado se han iniciado en segundo plano."
else
    echo "❌ Acción cancelada."
fi
