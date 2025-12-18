#!/bin/bash
# Script para monitorear el estado del cluster

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔍 MLOps Platform Monitoring${NC}"
echo ""

# Namespace status
echo -e "${YELLOW}📦 Namespace Status:${NC}"
kubectl get namespace mlops
echo ""

# Pods
echo -e "${YELLOW}🐳 Pods:${NC}"
kubectl get pods -n mlops -o wide
echo ""

# Services
echo -e "${YELLOW}🌐 Services:${NC}"
kubectl get svc -n mlops
echo ""

# Deployments
echo -e "${YELLOW}🚀 Deployments:${NC}"
kubectl get deployments -n mlops
echo ""

# HPA
echo -e "${YELLOW}📊 Horizontal Pod Autoscalers:${NC}"
kubectl get hpa -n mlops || echo "No HPA configured"
echo ""

# PVCs
echo -e "${YELLOW}💾 Storage:${NC}"
kubectl get pvc -n mlops
echo ""

# Ingress
echo -e "${YELLOW}🔌 Ingress:${NC}"
kubectl get ingress -n mlops
echo ""

# Recent events
echo -e "${YELLOW}📝 Recent Events:${NC}"
kubectl get events -n mlops --sort-by='.lastTimestamp' | tail -10
echo ""

# Resource usage
echo -e "${YELLOW}📈 Resource Usage (Top Pods):${NC}"
kubectl top pods -n mlops || echo "Metrics server not available"
echo ""

# Health check
echo -e "${YELLOW}🏥 Health Check:${NC}"
for pod in $(kubectl get pods -n mlops -o jsonpath='{.items[*].metadata.name}'); do
    status=$(kubectl get pod $pod -n mlops -o jsonpath='{.status.phase}')
    ready=$(kubectl get pod $pod -n mlops -o jsonpath='{.status.containerStatuses[0].ready}')

    if [ "$status" = "Running" ] && [ "$ready" = "true" ]; then
        echo -e "  ${GREEN}✓${NC} $pod: $status (Ready)"
    else
        echo -e "  ${YELLOW}⚠${NC} $pod: $status (Ready: $ready)"
    fi
done
echo ""
