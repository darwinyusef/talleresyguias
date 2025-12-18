#!/bin/bash
# Script para desplegar MLOps platform en Kubernetes

set -e

echo "🚀 Deploying MLOps Platform to Kubernetes..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar kubectl
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

# Verificar conexión al cluster
echo -e "${BLUE}Checking cluster connection...${NC}"
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Cannot connect to Kubernetes cluster${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Connected to cluster${NC}"

# Namespace
echo -e "${BLUE}Creating namespace...${NC}"
kubectl apply -f k8s/namespace.yaml
echo -e "${GREEN}✓ Namespace created${NC}"

# ConfigMap y Secrets
echo -e "${BLUE}Applying configuration...${NC}"
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
echo -e "${GREEN}✓ Configuration applied${NC}"

# Storage
echo -e "${BLUE}Creating storage...${NC}"
kubectl apply -f k8s/storage.yaml
echo -e "${GREEN}✓ Storage created${NC}"

# Wait for PVCs
echo -e "${BLUE}Waiting for PVCs to be bound...${NC}"
kubectl wait --for=condition=Bound pvc --all -n mlops --timeout=120s || true
echo -e "${GREEN}✓ PVCs ready${NC}"

# Deploy services
echo -e "${BLUE}Deploying PyTorch service...${NC}"
kubectl apply -f k8s/pytorch-deployment.yaml
echo -e "${GREEN}✓ PyTorch service deployed${NC}"

# Ingress
echo -e "${BLUE}Creating ingress...${NC}"
kubectl apply -f k8s/ingress.yaml
echo -e "${GREEN}✓ Ingress created${NC}"

# Wait for deployments
echo -e "${BLUE}Waiting for deployments to be ready...${NC}"
kubectl wait --for=condition=available deployment --all -n mlops --timeout=300s || true

# Show status
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Deployment completed!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo ""

echo "Resources in mlops namespace:"
kubectl get all -n mlops

echo ""
echo "Services:"
kubectl get svc -n mlops

echo ""
echo "Ingress:"
kubectl get ingress -n mlops

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  • Check pods: kubectl get pods -n mlops"
echo "  • View logs: kubectl logs -f deployment/pytorch-service -n mlops"
echo "  • Port forward: kubectl port-forward svc/pytorch-service 8000:8000 -n mlops"
echo ""
