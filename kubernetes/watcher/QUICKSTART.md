# Wächter Stack - Quick Start

## 🚀 Quick Deployment

```bash
# Navigate to the watcher directory
cd kubernetes/watcher

# Deploy to default namespace
./deploy.sh

# Or deploy to custom namespace
./deploy.sh kosymbiosis-monitoring
```

## 📋 Pre-requisites

1. **Kubernetes Cluster** (v1.24+)
2. **kubectl** configured
3. **Node Exporter** on all 10 sovereign nodes
4. **Resonance Logger** service at `hannes-resonance-logger.local`

## 🎯 Quick Setup on Each Node

### Install Node Exporter

```bash
# Download and install
wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
tar xvfz node_exporter-1.7.0.linux-amd64.tar.gz
sudo mv node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter

# Create textfile collector directory
sudo mkdir -p /var/lib/node_exporter/textfile_collector
sudo chown node_exporter:node_exporter /var/lib/node_exporter/textfile_collector

# Install systemd service
sudo cp examples/node_exporter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
```

### Setup Lambda Exporter

```bash
# Install lambda export script
sudo cp examples/export-lambda.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/export-lambda.sh

# Set node name
echo 'export NODE_NAME=node-am-01' | sudo tee -a /etc/environment

# Install crontab (Option 1: Simple but may drift)
sudo crontab -e
# Add entries from examples/crontab.example

# OR use systemd timer (Option 2: Preferred for precision)
sudo cp examples/kosymbiosis-exporter.service /etc/systemd/system/
sudo cp examples/kosymbiosis-exporter.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kosymbiosis-exporter.timer
sudo systemctl start kosymbiosis-exporter.timer
```

## 🔍 Verification

```bash
# Check pod status
kubectl get pods -l app=kosymbiosis-watcher

# View Prometheus targets
kubectl port-forward svc/watcher-prometheus 9090:9090
# Open http://localhost:9090/targets

# View active alerts
# Open http://localhost:9090/alerts

# Test node metrics
curl http://node-am-01:9100/metrics | grep kosymbiosis_lambda
```

## 📊 10 Sovereign Nodes

| Node Code | City | Expected λ | Role |
|-----------|------|-----------|------|
| AM-01 | Amsterdam | > 0.85 | Hub |
| KR-03 | Krakau | 0.70-0.85 | Backbone |
| SF-04 | Sofia | 0.70-0.85 | Backbone |
| RT-05 | Rotterdam | 0.70-0.85 | Backbone |
| CV-06 | Cervia | 0.70-0.85 | Backbone |
| ON-08 | Oldenburg | > 0.85 | Hub |
| VS-09 | Vaison | 0.70-0.85 | Backbone |
| DS-10 | Donostia | 0.70-0.85 | Backbone |
| AR-11 | Arles | 0.70-0.85 | Backbone |
| UL-12 | Ulm | > 0.70 | Backup |

## 🚨 Alert Types

1. **LambdaDropCritical** - λ < μ-2σ for 30s
2. **LambdaSpike** - λ > μ+2σ for 30s
3. **NodeUnreachable** - Node offline for 1m
4. **HubNodeDegradation** - Hub node λ < 0.85 for 2m

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.

## 🛡️ NSR Integration

All alerts are sent to the Resonance Logger webhook for NSR compliance:
- No automatic interventions in data flow
- Human sovereignty maintained
- Pattern detection for coercion attempts
- Statistical anomaly tracking

---

**Part of the Lex Amoris Framework**  
© 2026 Hannes Mitterer - NSR Protected
