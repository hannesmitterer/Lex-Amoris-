#!/bin/bash
# Deploy Wächter-Konfigurations-Stack to Kubernetes
# Usage: ./deploy.sh [namespace]

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="${1:-default}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Wächter-Konfigurations-Stack Deployment${NC}"
echo -e "${GREEN}  Namespace: ${NAMESPACE}${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}✗ kubectl not found. Please install kubectl.${NC}"
    exit 1
fi

# Check cluster connection
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}✗ Cannot connect to Kubernetes cluster.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ kubectl configured and cluster reachable${NC}"
echo ""

# Create namespace if it doesn't exist
if [ "$NAMESPACE" != "default" ]; then
    if kubectl get namespace "$NAMESPACE" &> /dev/null; then
        echo -e "${YELLOW}⚠ Namespace '$NAMESPACE' already exists${NC}"
    else
        echo -e "${GREEN}Creating namespace '$NAMESPACE'...${NC}"
        kubectl create namespace "$NAMESPACE"
    fi
    echo ""
fi

# Apply ConfigMaps first
echo -e "${GREEN}Step 1: Deploying ConfigMaps...${NC}"
kubectl apply -f "$SCRIPT_DIR/02-prometheus-config.yaml" -n "$NAMESPACE"
kubectl apply -f "$SCRIPT_DIR/03-alert-rules.yaml" -n "$NAMESPACE"
kubectl apply -f "$SCRIPT_DIR/04-alertmanager-config.yaml" -n "$NAMESPACE"
echo -e "${GREEN}✓ ConfigMaps deployed${NC}"
echo ""

# Apply Deployment
echo -e "${GREEN}Step 2: Deploying Watcher Sidecar...${NC}"
kubectl apply -f "$SCRIPT_DIR/01-deployment.yaml" -n "$NAMESPACE"
echo -e "${GREEN}✓ Deployment created${NC}"
echo ""

# Apply Services
echo -e "${GREEN}Step 3: Creating Services...${NC}"
kubectl apply -f "$SCRIPT_DIR/05-service.yaml" -n "$NAMESPACE"
echo -e "${GREEN}✓ Services created${NC}"
echo ""

# Wait for deployment to be ready
echo -e "${GREEN}Step 4: Waiting for deployment to be ready...${NC}"
kubectl wait --for=condition=available --timeout=120s \
    deployment/watcher-sidecar -n "$NAMESPACE" || {
    echo -e "${RED}✗ Deployment failed to become ready${NC}"
    echo ""
    echo -e "${YELLOW}Pod status:${NC}"
    kubectl get pods -l app=kosymbiosis-watcher -n "$NAMESPACE"
    echo ""
    echo -e "${YELLOW}Recent events:${NC}"
    kubectl get events -n "$NAMESPACE" --sort-by='.lastTimestamp' | tail -10
    exit 1
}
echo -e "${GREEN}✓ Deployment ready${NC}"
echo ""

# Display status
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}Pods:${NC}"
kubectl get pods -l app=kosymbiosis-watcher -n "$NAMESPACE"
echo ""

echo -e "${GREEN}Services:${NC}"
kubectl get svc -l app=kosymbiosis-watcher -n "$NAMESPACE"
echo ""

echo -e "${GREEN}ConfigMaps:${NC}"
kubectl get configmap -l app=kosymbiosis-watcher -n "$NAMESPACE"
echo ""

# Port-forwarding instructions
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Access UIs via Port-Forwarding${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "Prometheus UI:"
echo -e "  ${GREEN}kubectl port-forward -n $NAMESPACE svc/watcher-prometheus 9090:9090${NC}"
echo -e "  Then open: http://localhost:9090"
echo ""
echo -e "Alertmanager UI:"
echo -e "  ${GREEN}kubectl port-forward -n $NAMESPACE svc/watcher-alertmanager 9093:9093${NC}"
echo -e "  Then open: http://localhost:9093"
echo ""

# Logs
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  View Logs${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "Prometheus logs:"
echo -e "  ${GREEN}kubectl logs -n $NAMESPACE -l app=kosymbiosis-watcher -c prometheus --tail=50${NC}"
echo ""
echo -e "Alertmanager logs:"
echo -e "  ${GREEN}kubectl logs -n $NAMESPACE -l app=kosymbiosis-watcher -c alertmanager --tail=50${NC}"
echo ""

# Verification
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Next Steps${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════${NC}"
echo ""
echo "1. Verify that all 10 sovereign nodes are running node_exporter"
echo "2. Ensure each node exports the 'kosymbiosis_lambda' metric"
echo "3. Check Prometheus targets: http://localhost:9090/targets"
echo "4. Verify alert rules: http://localhost:9090/alerts"
echo "5. Test alertmanager webhook to hannes-resonance-logger.local"
echo ""
echo -e "${GREEN}🛡️  Wächter is now monitoring your Kosymbiosis network!${NC}"
echo ""
