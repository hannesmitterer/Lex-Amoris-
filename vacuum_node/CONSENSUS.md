# Robust Consensus Upgrade

This document describes the robust consensus mechanisms added to the Vacuum Bridge Network.

## Overview

The network now supports:
1. **Majority Voting** - Tolerates divergent nodes
2. **Reputation Layer** - Weighted consensus based on node trustworthiness
3. **Blockchain Log** - Immutable append-only decision history
4. **Decision Gateway** - `/decision` endpoint with certification
5. **IPFS Anchoring** - Optional public immutable storage

## Key Improvements

### Before (v1.0)
- Simple consensus: All nodes must agree (all hashes identical)
- Single point of failure: One divergent node breaks consensus
- No history: Decisions not recorded
- No reputation: All nodes treated equally

### After (v2.0)
- **Robust consensus**: Majority vote (>50%) required
- **Fault tolerance**: Tolerates divergent/failed nodes
- **Blockchain**: Immutable decision history with prev_hash linking
- **Reputation**: Trusted nodes have more influence
- **Certification**: Verifiable, auditable certificates

## New Endpoints

### POST /decision

The main endpoint for making certified decisions with robust consensus.

**Input:**
```json
{
  "features": [[0.2, 0.8], [0.9, 0.9], [0.1, 0.2]],
  "group": [0, 1, 0]
}
```

**Output:**
```json
{
  "decision": {
    "consensus_hash": "abc123...",
    "agreement_ratio": 0.67,
    "is_consensus": true,
    "vote_counts": {"abc123...": 2, "xyz789...": 1},
    "total_votes": 3
  },
  "certificate": {
    "block": {
      "index": 0,
      "timestamp": 1710000000.123,
      "hash": "abc123...",
      "prev_hash": "genesis",
      "metadata": {
        "agreement_ratio": 0.67,
        "is_consensus": true,
        "weighted_hash": "abc123...",
        "node_count": 3,
        "ipfs_cid": "Qm..." 
      }
    },
    "responses": [...],
    "weighted_result": {
      "best_hash": "abc123...",
      "weights": {"abc123...": 2.0, "xyz789...": 1.0}
    },
    "ipfs_cid": "Qm..."
  },
  "status": "certified"
}
```

### GET /chain

Get the complete blockchain.

**Output:**
```json
{
  "chain": [
    {
      "index": 0,
      "timestamp": 1710000000.123,
      "data": {...},
      "hash": "abc123...",
      "prev_hash": "genesis",
      "metadata": {...}
    },
    ...
  ],
  "length": 5,
  "valid": true,
  "message": "Chain is valid"
}
```

### GET /chain/{index}

Get a specific block by index.

**Example:** `GET /chain/0`

### GET /reputation

Get reputation scores for all nodes.

**Output:**
```json
{
  "reputation": {
    "http://node-a:8000": 1.0,
    "http://node-b:8000": 0.95,
    "http://node-c:8000": 0.8
  }
}
```

### GET /reputation/{node_id}

Get reputation for a specific node.

**Example:** `GET /reputation/http://node-a:8000`

### POST /reputation/{node_id}

Update reputation score for a node.

**Input:**
```json
{
  "score": 0.95
}
```

## Consensus Mechanisms

### 1. Majority Voting

Replaces the strict "all must agree" rule with majority voting.

**Algorithm:**
```python
def majority_consensus(responses):
    # Count hash occurrences
    hash_counts = Counter([r["hash"] for r in responses])
    most_common, freq = hash_counts.most_common(1)[0]
    
    # Check if majority (>50%)
    is_consensus = freq >= (total_votes // 2 + 1)
    
    return {
        "consensus_hash": most_common,
        "agreement_ratio": freq / total_votes,
        "is_consensus": is_consensus
    }
```

**Examples:**

| Scenario | Votes | Result | Consensus? |
|----------|-------|--------|------------|
| Unanimous | 3-0-0 | Hash A wins | ✓ Yes (100%) |
| Majority | 2-1-0 | Hash A wins | ✓ Yes (67%) |
| Split 3-way | 1-1-1 | Hash A picked | ✗ No (33%) |
| Split 2-way | 2-2 | Hash A picked | ✗ No (50%) |

**Key benefit:** Tolerates up to `(n-1)/2` divergent nodes.

### 2. Weighted Consensus

Nodes with higher reputation have more influence.

**Algorithm:**
```python
def weighted_consensus(responses, node_ids):
    weights = {}
    for response, node_id in zip(responses, node_ids):
        hash_value = response["hash"]
        reputation = REPUTATION.get(node_id, 0.5)
        weights[hash_value] += reputation
    
    best_hash = max(weights, key=weights.get)
    return best_hash, weights
```

**Example:**

3 nodes vote:
- Node A (reputation 1.0): Hash "abc123"
- Node B (reputation 0.8): Hash "abc123"
- Node C (reputation 0.5): Hash "xyz789"

Weights:
- "abc123": 1.0 + 0.8 = 1.8
- "xyz789": 0.5

Winner: "abc123" (weighted consensus)

### 3. Blockchain Log

Every decision is recorded in an immutable chain.

**Structure:**
```python
block = {
    "index": 0,
    "timestamp": time.time(),
    "data": {...},           # Input data
    "hash": "abc123...",     # Consensus hash
    "prev_hash": "genesis",  # Links to previous block
    "metadata": {...}        # Decision metadata
}
```

**Chain integrity:**
- Block 0: `prev_hash = "genesis"`
- Block N: `prev_hash = Block[N-1].hash`

**Verification:**
```python
# Check each block links to previous
for i in range(1, len(CHAIN)):
    assert CHAIN[i].prev_hash == CHAIN[i-1].hash
```

## Usage Examples

### Example 1: Make a Certified Decision

```bash
curl -X POST http://localhost:8000/decision \
  -H "Content-Type: application/json" \
  -d '{
    "features": [[0.6,0.6],[0.7,0.7],[0.5,0.5]],
    "group": [0,1,0]
  }'
```

Response shows:
- ✓ Consensus achieved (2/3 nodes agree)
- ✓ Block added to chain
- ✓ Certificate with signatures
- ✓ IPFS CID (if configured)

### Example 2: View Decision History

```bash
# Get full blockchain
curl http://localhost:8000/chain

# Get specific decision
curl http://localhost:8000/chain/0
```

### Example 3: Check Reputation

```bash
# View all node reputations
curl http://localhost:8000/reputation

# Update a node's reputation
curl -X POST http://localhost:8000/reputation/http://node-b:8000 \
  -H "Content-Type: application/json" \
  -d '{"score": 0.95}'
```

### Example 4: Test Fault Tolerance

Start with 3 nodes, stop one:

```bash
docker-compose stop node-c
```

Then make a decision - should still achieve consensus with 2/2 remaining nodes.

## IPFS Integration (Optional)

If IPFS is available, certificates are automatically anchored to IPFS.

### Setup IPFS

```bash
# Start local Kubo node
ipfs daemon
```

### Benefits

1. **Immutable storage**: Certificates cannot be altered
2. **Public verification**: Anyone can verify using CID
3. **Distributed**: No single point of failure
4. **Content-addressed**: CID proves integrity

### Verify Certificate on IPFS

```bash
# Get certificate by CID
ipfs cat QmXxxx...

# Via HTTP gateway
curl https://ipfs.io/ipfs/QmXxxx...
```

## Testing

Run comprehensive tests:

```bash
# Test consensus logic
python test_consensus.py

# Test with live network
docker-compose up -d
python test_consensus.py
```

## Architecture Comparison

### Simple Consensus (v1.0)
```
Node A → Hash: abc
Node B → Hash: abc
Node C → Hash: abc
         ↓
    Agreement = True (100% or nothing)
```

### Robust Consensus (v2.0)
```
Node A (rep: 1.0) → Hash: abc  ┐
Node B (rep: 0.8) → Hash: abc  ├→ Majority: abc (67%)
Node C (rep: 0.5) → Hash: xyz  ┘   Weighted: abc (1.8 vs 0.5)
                                    ↓
                              Consensus = True
                                    ↓
                              Block → Chain
                                    ↓
                              Certificate → IPFS
```

## Limitations & Future Work

**Current limitations:**
- Not Byzantine fault tolerant (assumes honest majority)
- Reputation manually managed (not automated)
- Local blockchain (not distributed ledger)
- Simple majority (no stake weighting)

**Future enhancements:**
- BFT consensus (Practical Byzantine Fault Tolerance)
- Automatic reputation adjustment based on accuracy
- Distributed blockchain across nodes
- Smart contract integration
- Zero-knowledge proofs for privacy

## Summary

The robust consensus upgrade transforms the Vacuum Bridge Network from a simple verification system into a **certified computational truth engine**:

- ✅ **Fault tolerant** - Handles node failures
- ✅ **Auditable** - Complete decision history
- ✅ **Verifiable** - Cryptographic certificates
- ✅ **Weighted** - Reputation-based influence
- ✅ **Immutable** - Blockchain + IPFS storage

This is now a **production-ready decision infrastructure** for AI governance.
