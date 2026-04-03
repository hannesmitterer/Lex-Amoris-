# Quick Start Guide - Vacuum Bridge Network

This guide will get you up and running with the Vacuum Bridge Network in under 5 minutes.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local testing)
- OpenSSL (for key generation)

## Step 1: Navigate to vacuum_node

```bash
cd vacuum_node
```

## Step 2: Generate Cryptographic Keys

```bash
./generate-keys.sh
```

This creates RSA key pairs for all three nodes and local testing.

## Step 3: Start the Network

```bash
docker-compose up --build
```

This starts three nodes:
- Node A: http://localhost:8000
- Node B: http://localhost:8001
- Node C: http://localhost:8002

Wait for all nodes to be healthy (you'll see "Application startup complete" messages).

## Step 4: Test Single Node

Open a new terminal and run:

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[0.2,0.8],[0.9,0.9],[0.1,0.2],[0.7,0.6]],
    "group": [0,1,0,1]
  }' | python -m json.tool
```

You should see a JSON response with predictions, fairness metrics, hash, and signature.

## Step 5: Test Consensus

```bash
curl -X POST http://localhost:8000/consensus \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[0.2,0.8],[0.9,0.9],[0.1,0.2],[0.7,0.6]],
    "group": [0,1,0,1]
  }' | python -m json.tool
```

This queries all three nodes and verifies they produce identical results.

## Step 6: Run Automated Tests

```bash
python test_network.py
```

This runs a comprehensive test suite checking:
- Health of all nodes
- Evaluation endpoint
- Attestation (signature verification)
- Consensus mechanism

## What Just Happened?

You now have a **real distributed network** where:

1. ✅ Each node independently computes predictions
2. ✅ Fairness constraints are mathematically verified
3. ✅ Results are cryptographically signed
4. ✅ Consensus is achieved through deterministic hashing
5. ✅ No single point of failure

## Next Steps

### Try Different Data

Modify the input to see how fairness metrics change:

```bash
# More balanced predictions
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[0.6,0.6],[0.6,0.6],[0.6,0.6],[0.6,0.6]],
    "group": [0,1,0,1]
  }'
```

### Verify Signatures

Test the attestation endpoint:

```bash
# First, get a result
RESULT=$(curl -s -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"features": [[0.6,0.6],[0.6,0.6]], "group": [0,1]}')

# Then verify it on another node
echo $RESULT | jq '{result, signature, public_key}' | \
  curl -X POST http://localhost:8001/attest \
    -H "Content-Type: application/json" \
    -d @-
```

### Check Node Health

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
```

### View Logs

```bash
docker-compose logs -f node-a
docker-compose logs -f node-b
docker-compose logs -f node-c
```

## Stopping the Network

```bash
docker-compose down
```

To remove all containers and networks:

```bash
docker-compose down -v
```

## Troubleshooting

### "Connection refused"
- Make sure Docker is running
- Check that ports 8000-8002 are not in use
- Wait a bit longer for containers to start

### "Keys not found"
- Run `./generate-keys.sh` to generate keys
- Check that `keys-a/`, `keys-b/`, `keys-c/` directories exist

### "Hash mismatch in consensus"
- This is rare and could indicate:
  - Non-deterministic behavior (bug)
  - Network issues
  - Different code versions

## What's Next?

Now that you have a working network, you can:

1. **Add more nodes** - See README.md for instructions
2. **Integrate with your ML models** - Replace `model.py`
3. **Add new fairness metrics** - Extend `fairness.py`
4. **Deploy to cloud** - Use Kubernetes or cloud services
5. **Add IPFS anchoring** - Store proofs immutably

## Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node A    │────▶│   Node B    │────▶│   Node C    │
│  :8000      │◀────│  :8001      │◀────│  :8002      │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      └───────────────────┴───────────────────┘
                  Consensus Layer
              (Hash Comparison)
```

Each node:
- Runs same code
- Uses different keys
- Makes independent decisions
- Contributes to consensus

## Core Concepts

### Determinism
Same input → Same output → Same hash

### Fairness
Demographic parity: `|P(ŷ=1|g=0) - P(ŷ=1|g=1)| ≤ ε`

### Cryptographic Proof
SHA256 hash + RSA signature = Verifiable result

### Consensus
Agreement when all nodes produce identical hashes

---

**You've just built a Vacuum Bridge!** 🌉

This is a working prototype of:
- Distributed verification
- Fairness guarantees
- Cryptographic validation
- Deterministic consensus

The infrastructure is now **real and operational**.
