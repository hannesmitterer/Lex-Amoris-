# Vacuum Bridge Network

A distributed network of verification nodes implementing fairness constraints with cryptographic validation.

## Architecture

Each node in the network is a FastAPI service that:
- Makes predictions using a minimal ML model
- Verifies fairness constraints (demographic parity)
- Signs results with RSA cryptography
- Can attest to other nodes' results
- Participates in consensus through hash comparison

## Project Structure

```
vacuum_node/
├── main.py              # FastAPI service with all endpoints
├── model.py             # Minimal prediction model
├── fairness.py          # Demographic parity checking
├── verify.py            # Constraint verification
├── crypto.py            # Hashing and RSA signing/verification
├── requirements.txt     # Python dependencies
├── peers.json           # Peer node configuration
├── Dockerfile           # Container definition
├── docker-compose.yml   # Multi-node orchestration
├── generate-keys.sh     # RSA key generation script
└── keys/                # RSA key storage
    ├── private.pem
    └── public.pem
```

## Quick Start

### 1. Generate RSA Keys

```bash
cd vacuum_node
./generate-keys.sh
```

This creates:
- `keys-a/`, `keys-b/`, `keys-c/` for the three nodes
- `keys/` for local development

### 2. Start the Network

```bash
docker-compose up --build
```

This starts three nodes:
- Node A: http://localhost:8000
- Node B: http://localhost:8001
- Node C: http://localhost:8002

### 3. Test Single Node

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[0.2,0.8],[0.9,0.9],[0.1,0.2],[0.7,0.6]],
    "group": [0,1,0,1]
  }'
```

Expected response:
```json
{
  "result": {
    "disparity": 0.0,
    "constraint_satisfied": true,
    "predictions": [1, 1, 0, 1]
  },
  "hash": "abc123...",
  "signature": "def456...",
  "public_key": "-----BEGIN PUBLIC KEY-----\n..."
}
```

### 4. Test Consensus

```bash
curl -X POST http://localhost:8000/consensus \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[0.2,0.8],[0.9,0.9],[0.1,0.2],[0.7,0.6]],
    "group": [0,1,0,1]
  }'
```

This will:
1. Query all peer nodes (B and C)
2. Compute local result
3. Compare all hashes
4. Return consensus status

Expected response:
```json
{
  "agreement": true,
  "hashes": ["abc123...", "abc123...", "abc123..."],
  "responses": [...],
  "local_result": {...},
  "consensus_count": 3
}
```

## API Endpoints

### GET /
Basic node information

### GET /health
Health check with key and peer status

### GET /peers
List of configured peer nodes

### POST /evaluate
Run prediction with fairness verification

**Input:**
```json
{
  "features": [[f1, f2, ...], ...],
  "group": [0, 1, 0, 1, ...]
}
```

**Output:**
```json
{
  "result": {
    "disparity": 0.0,
    "constraint_satisfied": true,
    "predictions": [...]
  },
  "hash": "sha256_hash",
  "signature": "rsa_signature",
  "public_key": "pem_key"
}
```

### POST /attest
Verify another node's signed result

**Input:**
```json
{
  "result": {...},
  "signature": "hex_signature",
  "public_key": "pem_key"
}
```

**Output:**
```json
{
  "valid_signature": true,
  "hash": "sha256_hash"
}
```

### POST /consensus
Aggregate results from all peers

**Input:** Same as `/evaluate`

**Output:**
```json
{
  "agreement": true,
  "hashes": ["hash1", "hash2", "hash3"],
  "responses": [...],
  "local_result": {...},
  "consensus_count": 3
}
```

## Local Development

### Without Docker

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate keys:
```bash
./generate-keys.sh
```

3. Run a single node:
```bash
uvicorn main:app --reload --port 8000
```

### Testing

Run tests manually:
```bash
# Test evaluation
python -c "
import requests
import json

data = {
    'features': [[0.2,0.8],[0.9,0.9],[0.1,0.2],[0.7,0.6]],
    'group': [0,1,0,1]
}

response = requests.post('http://localhost:8000/evaluate', json=data)
print(json.dumps(response.json(), indent=2))
"
```

## How It Works

### 1. Prediction & Fairness Check
- Model predicts binary outcomes based on feature means
- Demographic parity checks if prediction rates are similar across groups
- Constraint verified against epsilon threshold (default: 0.05)

### 2. Cryptographic Validation
- Result is canonicalized as sorted JSON
- SHA256 hash computed for integrity
- RSA signature generated with private key
- Public key shared for verification

### 3. Consensus Mechanism
- Each node independently computes result
- Hashes compared across all nodes
- Agreement achieved when all hashes match
- Deterministic: same input → same output → same hash

## Configuration

### peers.json
Configure peer nodes:
```json
[
  "http://node-b:8000",
  "http://node-c:8000"
]
```

### Environment Variables
- `NODE_NAME`: Optional node identifier

### Fairness Parameters
Modify in `verify.py`:
- `epsilon`: Maximum allowed disparity (default: 0.05)

## Security Considerations

- Private keys should be kept secure and never committed
- Keys are mounted read-only in containers
- Signature verification prevents tampering
- Hash comparison ensures deterministic results

## Extending the Network

### Add More Nodes

1. Generate new keys:
```bash
mkdir keys-d
openssl genrsa -out keys-d/private.pem 2048
openssl rsa -in keys-d/private.pem -pubout -out keys-d/public.pem
```

2. Add to `docker-compose.yml`:
```yaml
node-d:
  build: .
  container_name: vacuum-node-d
  ports:
    - "8003:8000"
  volumes:
    - ./keys-d:/app/keys:ro
  networks:
    - vacuum-net
```

3. Update `peers.json` for existing nodes

### Custom Models

Replace the `predict()` function in `model.py` with your own model.

### Different Fairness Metrics

Add new metrics in `fairness.py`:
- Equal opportunity
- Equalized odds
- Calibration
- etc.

## Troubleshooting

### Keys not found
Run `./generate-keys.sh` to generate keys

### Peer connection errors
Ensure all nodes are running and network is configured correctly

### Hash mismatch
Could indicate:
- Non-deterministic model behavior
- Different model versions
- Network transmission errors
- Malicious tampering

## License

Part of the Lex Amoris Framework - GNU General Public License v3.0
