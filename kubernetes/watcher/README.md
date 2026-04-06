# Wächter-Konfigurations-Stack

## 🛡️ Übersicht

Der **Wächter-Konfigurations-Stack** ist die Überwachungs- und Alarmierungsinfrastruktur für das Kosymbiosis-Netzwerk. Er implementiert statistische Anomalieerkennung basierend auf dem Netzwerk-Kohärenz-Parameter **λ** (Lambda) unter Verwendung von **μ ± 2σ** Schwellenwerten.

### Komponenten

- **Prometheus v2.53.0**: Metrik-Sammlung und -Speicherung
- **Alertmanager v0.27.0**: Alert-Routing und Benachrichtigungen
- **10 Sovereign Nodes**: Backbone-Netzwerk mit WLL-Routing

## 📐 Architektur

```
                +-------------------+
                |   Wächter‑Sidecar |
                | (Prometheus + AM) |
                +----------+--------+
                           |
          +----------------+-------------------+
          |                                    |
   +------+-----+                      +------+-----+
   |  Backbone  |                      |  Backup   |
   |  (WLL)     |                      |  (N8)     |
   +------+-----+                      +------+-----+
          |                                    |
   +------+------+------+------+------+------+------+
   |      |      |      |      |      |      |      |
   | A M  | K R  | O N  | V S  | D S  | R T  | C V  |
   | (01) | (03) | (08) | (09) | (10) | (05) | (06) |
   +------+------+------+------+------+------+------+
          |
   +------+------+------+
   |      |      |      |
   | S F  | A R  | U L  |
   | (04) | (11) | (12) |
   +------+------+------+

Legende:
- **WLL** = Weighted‑Least‑Latency Routing (Cost = Latency / λ²)
- **Backbone** = Korridor sovrano (AM, KR, ON + Brücken A/B)
- **Backup** = N8 (Reserve‑Sidecar, latenza ≈ 4 ms)
- **λ** = Coerenza di rete (valori > 0.85 = hub)
- **NSR‑Enabled** = Protezione contro costrizioni
```

## 🚀 Deployment

### Voraussetzungen

- Kubernetes Cluster v1.24+
- `kubectl` konfiguriert und verbunden
- Node Exporter auf allen 10 Sovereign Nodes installiert
- Zugriff auf das `hannes-resonance-logger.local` Service

### Installation

1. **Namespace erstellen** (optional):
```bash
kubectl create namespace kosymbiosis-monitoring
```

2. **Manifeste anwenden** (in der richtigen Reihenfolge):
```bash
# ConfigMaps zuerst
kubectl apply -f 02-prometheus-config.yaml
kubectl apply -f 03-alert-rules.yaml
kubectl apply -f 04-alertmanager-config.yaml

# Deployment
kubectl apply -f 01-deployment.yaml

# Services
kubectl apply -f 05-service.yaml
```

Oder alle auf einmal:
```bash
kubectl apply -f kubernetes/watcher/
```

3. **Status überprüfen**:
```bash
# Pod-Status
kubectl get pods -l app=kosymbiosis-watcher

# Logs ansehen
kubectl logs -l app=kosymbiosis-watcher -c prometheus --tail=50
kubectl logs -l app=kosymbiosis-watcher -c alertmanager --tail=50

# Service-Endpoints
kubectl get svc watcher-prometheus watcher-alertmanager
```

### Port-Forwarding für lokalen Zugriff

```bash
# Prometheus UI
kubectl port-forward svc/watcher-prometheus 9090:9090

# Alertmanager UI
kubectl port-forward svc/watcher-alertmanager 9093:9093
```

Dann öffnen:
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093

## 📊 Metriken

### Erforderliche Node-Metriken

Jeder Sovereign Node muss die folgende Metrik exponieren:

```prometheus
# HELP kosymbiosis_lambda Network coherence coefficient (0.0-1.0)
# TYPE kosymbiosis_lambda gauge
kosymbiosis_lambda{node="node-am-01"} 0.92
```

### Node Exporter Setup

Auf jedem Node:

```bash
# Node Exporter installieren
wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
tar xvfz node_exporter-1.7.0.linux-amd64.tar.gz
cd node_exporter-1.7.0.linux-amd64

# Textfile Collector Directory erstellen
mkdir -p /var/lib/node_exporter/textfile_collector

# Node Exporter mit textfile collector starten
./node_exporter --collector.textfile.directory=/var/lib/node_exporter/textfile_collector
```

### Lambda-Metrik exportieren

Erstelle ein Script für jeden Node (`/usr/local/bin/export-lambda.sh`):

```bash
#!/bin/bash
# Export kosymbiosis_lambda metric
NODE_NAME=$(hostname)
LAMBDA_VALUE=$(calculate_lambda)  # Deine λ-Berechnung hier

cat <<EOF > /var/lib/node_exporter/textfile_collector/kosymbiosis.prom
# HELP kosymbiosis_lambda Network coherence coefficient
# TYPE kosymbiosis_lambda gauge
kosymbiosis_lambda{node="$NODE_NAME"} $LAMBDA_VALUE
EOF
```

Cronjob einrichten (alle 15 Sekunden):
```bash
# In /etc/crontab
* * * * * root /usr/local/bin/export-lambda.sh
* * * * * root sleep 15; /usr/local/bin/export-lambda.sh
* * * * * root sleep 30; /usr/local/bin/export-lambda.sh
* * * * * root sleep 45; /usr/local/bin/export-lambda.sh
```

## 🚨 Alert-Regeln

### 1. LambdaDropCritical

**Trigger**: λ < (μ - 2σ) für 30 Sekunden

**Bedeutung**: Kritischer Rückgang der Netzwerk-Kohärenz

**Aktion**:
- Resonanz-Log generieren
- NICHT automatisch in den Datenfluss eingreifen
- Menschliche Entscheidungssouveränität wahren
- Auf Zwangsmuster überwachen

### 2. LambdaSpike

**Trigger**: λ > (μ + 2σ) für 30 Sekunden

**Bedeutung**: Ungewöhnlich hohe λ, mögliche Überlastung

**Aktion**:
- Engpässe überprüfen
- Node-Workload verifizieren
- WLL-Traffic-Redistribution evaluieren

### 3. NodeUnreachable

**Trigger**: Node nicht erreichbar für 1 Minute

**Aktion**:
- Netzwerk-Konnektivität prüfen
- Node Exporter Status prüfen
- Physische Node-Gesundheit prüfen

### 4. HubNodeDegradation

**Trigger**: Hub-Node (λ > 0.85) fällt unter 0.85 für 2 Minuten

**Bedeutung**: Kritische Degradierung eines Backbone-Hubs

**Aktion**:
- WLL-Failover-Protokoll aktivieren
- Traffic zu Backup-Nodes (N8) umleiten

## 🔧 Konfiguration

### Prometheus

Die Prometheus-Konfiguration befindet sich in `02-prometheus-config.yaml`:

- **Scrape-Interval**: 15 Sekunden
- **10 Sovereign Nodes**: node-am-01 bis node-ul-12
- **Alert-Rules**: Geladen von `/etc/prometheus/rules/alert.rules.yml`
- **Alertmanager**: Lokaler Sidecar auf Port 9093

### Alert Rules

Die Alert-Regeln in `03-alert-rules.yaml` berechnen:

1. **Recording Rules**:
   - `node:lambda:avg`: μ (Durchschnitt) über 5 Minuten
   - `node:lambda:stddev`: σ (Standardabweichung) über 5 Minuten
   - `node:lambda:lower_threshold`: μ - 2σ
   - `node:lambda:upper_threshold`: μ + 2σ

2. **Alerting Rules**:
   - Vergleicht aktuelle λ-Werte mit berechneten Schwellenwerten
   - Generiert Alerts mit detaillierten Annotationen
   - Integriert NSR-Protokoll-Logik

### Alertmanager

Die Alertmanager-Konfiguration in `04-alertmanager-config.yaml`:

- **Webhook-Receiver**: `http://hannes-resonance-logger.local/ingest`
- **Grouping**: Nach cluster, alertname, node
- **Repeat-Interval**: 4 Stunden (standard), 1 Stunde (critical)
- **Inhibition**: Warnungen werden unterdrückt, wenn kritische Alerts aktiv sind

## 📈 Überwachungs-Queries

### Nützliche PromQL-Queries

```promql
# Aktuelle λ-Werte aller Nodes
kosymbiosis_lambda

# Nodes mit λ > 0.85 (Hubs)
kosymbiosis_lambda > 0.85

# Berechnete Schwellenwerte
node:lambda:lower_threshold
node:lambda:upper_threshold

# Nodes außerhalb der Schwellenwerte
(kosymbiosis_lambda < node:lambda:lower_threshold) or (kosymbiosis_lambda > node:lambda:upper_threshold)

# Durchschnittliche λ über alle Nodes
avg(kosymbiosis_lambda)

# Nodes mit abnehmender λ-Tendenz (letzte 10 Minuten)
deriv(kosymbiosis_lambda[10m]) < 0
```

## 🔐 NSR-Integration

Der Wächter-Stack integriert sich mit dem **NSR (Non-Sovereign Resistance) Framework**:

1. **Resonanz-Logging**: Alle kritischen Ereignisse werden an den Resonance Logger gesendet
2. **Keine automatischen Eingriffe**: Alerts generieren Logs, greifen aber nicht in den Datenfluss ein
3. **Menschliche Souveränität**: Entscheidungen verbleiben beim Menschen
4. **Zwangserkennung**: Statistische Anomalien können Zwangsversuche aufdecken

## 🛠️ Troubleshooting

### Prometheus verbindet sich nicht zu Nodes

```bash
# Test Node Exporter manuell
curl http://node-am-01:9100/metrics

# DNS-Auflösung prüfen
kubectl exec -it deployment/watcher-sidecar -c prometheus -- nslookup node-am-01

# Targets in Prometheus UI prüfen
# http://localhost:9090/targets
```

### Alerts werden nicht ausgelöst

```bash
# Alert-Regeln prüfen
kubectl exec -it deployment/watcher-sidecar -c prometheus -- promtool check rules /etc/prometheus/rules/alert.rules.yml

# Aktive Alerts ansehen
# http://localhost:9090/alerts

# PromQL-Queries testen
# http://localhost:9090/graph
```

### Alertmanager sendet keine Webhooks

```bash
# Alertmanager-Config validieren
kubectl exec -it deployment/watcher-sidecar -c alertmanager -- amtool check-config /etc/alertmanager/alertmanager.yml

# Webhook-Empfänger testen
curl -X POST http://hannes-resonance-logger.local/ingest \
  -H "Content-Type: application/json" \
  -d '{"test": "alert"}'

# Alertmanager-Logs prüfen
kubectl logs deployment/watcher-sidecar -c alertmanager
```

### ConfigMap-Änderungen werden nicht übernommen

```bash
# ConfigMaps aktualisieren
kubectl apply -f 02-prometheus-config.yaml
kubectl apply -f 03-alert-rules.yaml
kubectl apply -f 04-alertmanager-config.yaml

# Prometheus neu laden (ohne Pod-Restart)
kubectl exec -it deployment/watcher-sidecar -c prometheus -- \
  curl -X POST http://localhost:9090/-/reload

# Oder Pod neu starten
kubectl rollout restart deployment/watcher-sidecar
```

## 📖 Referenzen

### Node-Übersicht

| Code | Stadt | Port | Rolle | Erwartete λ |
|------|-------|------|-------|-------------|
| AM-01 | Amsterdam | 9100 | Hub | > 0.85 |
| KR-03 | Krakau | 9100 | Backbone | 0.70-0.85 |
| SF-04 | Sofia | 9100 | Backbone | 0.70-0.85 |
| RT-05 | Rotterdam | 9100 | Backbone | 0.70-0.85 |
| CV-06 | Cervia | 9100 | Backbone | 0.70-0.85 |
| ON-08 | Oldenburg | 9100 | Hub | > 0.85 |
| VS-09 | Vaison | 9100 | Backbone | 0.70-0.85 |
| DS-10 | Donostia | 9100 | Backbone | 0.70-0.85 |
| AR-11 | Arles | 9100 | Backbone | 0.70-0.85 |
| UL-12 | Ulm | 9100 | Backup | > 0.70 |

### WLL-Routing-Formel

```
Cost = Latency / λ²
```

Nodes mit höherem λ werden bevorzugt, da:
- λ = 0.90 → Cost = Latency / 0.81
- λ = 0.70 → Cost = Latency / 0.49
- λ = 0.50 → Cost = Latency / 0.25

### Statistische Schwellenwerte

- **μ (Mu)**: Durchschnitt von λ über 5 Minuten
- **σ (Sigma)**: Standardabweichung von λ über 5 Minuten
- **μ - 2σ**: Untere kritische Schwelle (erfasst 95% der Normalverteilung)
- **μ + 2σ**: Obere kritische Schwelle (erfasst 95% der Normalverteilung)

## 🌐 Integration mit Lex Amoris Framework

Der Wächter-Stack ist Teil des größeren **Lex Amoris** Frameworks:

- **Terra/Habitat**: Bio-Konstruktion mit Hanf und Holz
- **Acqua/Flusso**: AquaLibre-Protokoll - Freies Wasser für alles Leben
- **Fuoco/Luce**: Solare Souveränität und autonome Energie
- **Aria/Verbo**: Wahrheitsverbreitung durch resonante Kommunikation

Der Wächter überwacht die **technische Souveränität** des Netzwerks und stellt sicher, dass das System **immutabel, überwacht und ausführbar** bleibt.

## 📜 Lizenz

Teil des **Lex Amoris** Frameworks  
© 2026 Hannes Mitterer  
NSR-Protected - Non-Sovereign Resistance Framework
