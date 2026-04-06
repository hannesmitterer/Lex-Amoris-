#!/bin/bash
# Example script to export kosymbiosis_lambda metric for a sovereign node
# Place this in /usr/local/bin/export-lambda.sh on each node
# Run via cron every 15 seconds

set -euo pipefail

# Configuration
NODE_NAME="${NODE_NAME:-$(hostname)}"
TEXTFILE_DIR="${TEXTFILE_DIR:-/var/lib/node_exporter/textfile_collector}"
METRIC_FILE="$TEXTFILE_DIR/kosymbiosis.prom"

# Ensure directory exists
mkdir -p "$TEXTFILE_DIR"

# ═══════════════════════════════════════════════════════════════
# Lambda Calculation Function
# ═══════════════════════════════════════════════════════════════
# This is a PLACEHOLDER - replace with your actual λ calculation
# 
# λ (lambda) should represent "network coherence" for this node
# Values: 0.0 (no coherence) to 1.0 (perfect coherence)
# 
# Typical λ sources:
# - Network latency to other nodes
# - Request success rate
# - Traffic throughput
# - Connection stability
# - Resource availability
# 
# Hub nodes (AM-01, ON-08): λ > 0.85
# Backbone nodes: λ = 0.70-0.85
# Backup nodes: λ > 0.70
# ═══════════════════════════════════════════════════════════════

calculate_lambda() {
    # Example 1: Random value for testing (REMOVE IN PRODUCTION)
    # echo "0.$(shuf -i 70-95 -n 1)"
    
    # Example 2: Based on CPU idle percentage using /proc/stat (robust)
    if [ -f /proc/stat ]; then
        # Read first line of /proc/stat and extract CPU values
        local cpu_line=$(head -1 /proc/stat)
        local cpu_values=($cpu_line)
        
        # Extract values: user nice system idle iowait irq softirq
        local user=${cpu_values[1]:-0}
        local nice=${cpu_values[2]:-0}
        local system=${cpu_values[3]:-0}
        local idle=${cpu_values[4]:-0}
        local iowait=${cpu_values[5]:-0}
        local irq=${cpu_values[6]:-0}
        local softirq=${cpu_values[7]:-0}
        
        local total=$((user + nice + system + idle + iowait + irq + softirq))
        
        if [ "$total" -gt 0 ] && [ "$idle" -ge 0 ]; then
            # Calculate idle percentage with awk (portable across systems)
            local lambda=$(awk "BEGIN {printf \"%.4f\", $idle / $total}")
            # Ensure lambda is in valid range [0.0, 1.0]
            if awk "BEGIN {exit !($lambda >= 0 && $lambda <= 1)}"; then
                echo "$lambda"
                return
            fi
        fi
    fi
    
    # Fallback: Return a safe default value
    echo "0.7500"
    
    # Example 3: Based on network metrics
    # local packet_loss=$(ping -c 10 8.8.8.8 2>/dev/null | grep "packet loss" | awk '{print $6}' | sed 's/%//')
    # if [ -n "$packet_loss" ]; then
    #     local lambda=$(awk "BEGIN {printf \"%.4f\", (100 - $packet_loss) / 100}")
    #     echo "$lambda"
    # fi
    
    # Example 4: Composite score
    # local cpu_score=...
    # local network_score=...
    # local memory_score=...
    # local lambda=$(awk "BEGIN {printf \"%.4f\", ($cpu_score + $network_score + $memory_score) / 3}")
    # echo "$lambda"
}

# ═══════════════════════════════════════════════════════════════
# Additional Metrics (Optional)
# ═══════════════════════════════════════════════════════════════

calculate_nsr_status() {
    # NSR (Non-Sovereign Resistance) status
    # 1 = enabled, 0 = disabled
    echo "1"
}

calculate_wll_cost() {
    # WLL (Weighted-Least-Latency) routing cost
    # Cost = Latency / λ²
    local lambda=$(calculate_lambda)
    local latency="${AVG_LATENCY:-10.0}"  # milliseconds
    
    # Prevent division by zero: ensure lambda >= 0.01
    if awk "BEGIN {exit !($lambda < 0.01)}"; then
        lambda="0.01"
    fi
    
    # Calculate lambda² and cost using awk (no bc dependency)
    local cost=$(awk "BEGIN {lambda_sq = $lambda * $lambda; printf \"%.4f\", $latency / lambda_sq}")
    echo "$cost"
}

# ═══════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════

LAMBDA=$(calculate_lambda)
NSR_STATUS=$(calculate_nsr_status)
WLL_COST=$(calculate_wll_cost)

# Write metrics to textfile collector
cat > "$METRIC_FILE.tmp" <<EOF
# HELP kosymbiosis_lambda Network coherence coefficient (0.0-1.0)
# TYPE kosymbiosis_lambda gauge
kosymbiosis_lambda{node="$NODE_NAME"} $LAMBDA

# HELP kosymbiosis_nsr_enabled NSR (Non-Sovereign Resistance) status
# TYPE kosymbiosis_nsr_enabled gauge
kosymbiosis_nsr_enabled{node="$NODE_NAME"} $NSR_STATUS

# HELP kosymbiosis_wll_cost WLL routing cost (latency / lambda²)
# TYPE kosymbiosis_wll_cost gauge
kosymbiosis_wll_cost{node="$NODE_NAME"} $WLL_COST
EOF

# Atomic move to prevent partial reads
mv "$METRIC_FILE.tmp" "$METRIC_FILE"

# Optional: Log to syslog
logger -t kosymbiosis-exporter "λ=$LAMBDA, NSR=$NSR_STATUS, WLL_Cost=$WLL_COST"

exit 0
