"""
Vacuum Bridge Network Node - FastAPI Service.

Provides endpoints for:
- /evaluate: Run prediction with fairness checking
- /attest: Verify another node's result
- /peers: Get list of peer nodes
- /consensus: Aggregate results from multiple nodes
- /decision: Robust decision-making with certification (NEW)
"""
import json
from pathlib import Path

import numpy as np
import requests
from fastapi import FastAPI, HTTPException

from consensus import (
    append_block,
    get_block,
    get_chain,
    get_reputation,
    majority_consensus,
    update_reputation,
    verify_chain,
    weighted_consensus,
)
from crypto import hash_result, sign_result, verify_signature
from fairness import demographic_parity
from model import predict
from verify import check_constraint

app = FastAPI(title="Vacuum Bridge Node", version="1.0.0")

# Load peer configuration
PEERS_FILE = Path(__file__).parent / "peers.json"
PEERS = []
if PEERS_FILE.exists():
    with open(PEERS_FILE) as f:
        PEERS = json.load(f)

# Public key for this node (loaded on demand)
PUBLIC_KEY_PATH = Path(__file__).parent / "keys" / "public.pem"
PRIVATE_KEY_PATH = Path(__file__).parent / "keys" / "private.pem"


def get_public_key():
    """Load and return the public key for this node."""
    if PUBLIC_KEY_PATH.exists():
        with open(PUBLIC_KEY_PATH) as f:
            return f.read()
    return None


@app.get("/")
def root():
    """Root endpoint - node info."""
    return {
        "service": "Vacuum Bridge Node",
        "version": "2.0.0",
        "endpoints": [
            "/evaluate",
            "/attest",
            "/peers",
            "/consensus",
            "/decision",
            "/chain",
            "/reputation",
        ],
    }


@app.get("/peers")
def get_peers():
    """Return list of known peer nodes."""
    return {"peers": PEERS, "count": len(PEERS)}


@app.post("/evaluate")
def evaluate(data: dict):
    """
    Evaluate model with fairness checking.

    Expected input:
    {
        "features": [[f1, f2, ...], ...],  # List of feature vectors
        "group": [0, 1, 0, 1, ...]          # Group membership (0 or 1)
    }

    Returns:
    {
        "result": {
            "disparity": float,
            "constraint_satisfied": bool,
            "predictions": [0, 1, ...]
        },
        "hash": "sha256_hash",
        "signature": "rsa_signature",
        "public_key": "pem_public_key"
    }
    """
    try:
        X = np.array(data["features"])
        group = np.array(data["group"])

        # Make predictions
        y_pred = predict(X)

        # Check fairness
        disparity = demographic_parity(y_pred, group)
        valid = check_constraint(disparity)

        # Build result
        result = {
            "disparity": float(disparity),
            "constraint_satisfied": bool(valid),
            "predictions": y_pred.tolist(),
        }

        # Create canonical JSON string
        result_str = json.dumps(result, sort_keys=True)

        # Hash and sign
        result_hash = hash_result(result_str)

        signature = None
        public_key = None
        if PRIVATE_KEY_PATH.exists():
            signature = sign_result(str(PRIVATE_KEY_PATH), result_str.encode())
            public_key = get_public_key()

        return {
            "result": result,
            "hash": result_hash,
            "signature": signature,
            "public_key": public_key,
        }

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation error: {e}")


@app.post("/attest")
def attest(payload: dict):
    """
    Verify another node's result.

    Expected input:
    {
        "result": {...},           # Result object
        "signature": "hex_sig",    # Signature to verify
        "public_key": "pem_key"    # Public key of signing node
    }

    Returns:
    {
        "valid_signature": bool,
        "hash": "sha256_hash"
    }
    """
    try:
        result = payload["result"]
        signature = payload["signature"]
        public_key = payload["public_key"]

        # Reconstruct canonical JSON
        result_str = json.dumps(result, sort_keys=True)

        # Verify signature
        valid_sig = False
        if signature and public_key:
            valid_sig = verify_signature(public_key, result_str.encode(), signature)

        return {"valid_signature": valid_sig, "hash": hash_result(result_str)}

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Attestation error: {e}")


@app.post("/consensus")
def consensus(data: dict):
    """
    Aggregate results from all peer nodes.

    Sends evaluation request to all peers and compares results.

    Expected input: Same as /evaluate endpoint

    Returns:
    {
        "agreement": bool,          # True if all hashes match
        "hashes": [...],           # List of hashes from each peer
        "responses": [...],        # Full responses from each peer
        "local_result": {...}      # This node's result
    }
    """
    try:
        responses = []

        # Query each peer
        for peer in PEERS:
            try:
                r = requests.post(f"{peer}/evaluate", json=data, timeout=10)
                if r.status_code == 200:
                    responses.append({"peer": peer, "response": r.json()})
                else:
                    responses.append(
                        {"peer": peer, "error": f"HTTP {r.status_code}", "response": None}
                    )
            except Exception as e:
                responses.append({"peer": peer, "error": str(e), "response": None})

        # Get local result
        local_result = evaluate(data)

        # Extract hashes (including local)
        hashes = [local_result["hash"]]
        hashes.extend(
            [
                r["response"]["hash"]
                for r in responses
                if r.get("response") and "hash" in r["response"]
            ]
        )

        # Check agreement
        agreement = len(set(hashes)) == 1 if hashes else False

        return {
            "agreement": agreement,
            "hashes": hashes,
            "responses": responses,
            "local_result": local_result,
            "consensus_count": len(hashes),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consensus error: {e}")


@app.post("/decision")
def decision(data: dict):
    """
    Make a robust decision with majority voting and certification.

    This endpoint:
    1. Queries all peer nodes
    2. Applies majority consensus (tolerates divergent nodes)
    3. Creates immutable block in chain
    4. Returns verifiable certificate

    Expected input: Same as /evaluate endpoint

    Returns:
    {
        "decision": {
            "consensus_hash": "...",
            "agreement_ratio": 0.66,
            "is_consensus": true,
            "vote_counts": {...}
        },
        "certificate": {
            "block": {...},
            "responses": [...],
            "weighted_result": {...}
        }
    }
    """
    try:
        responses = []
        node_ids = []

        # Query each peer
        for peer in PEERS:
            try:
                r = requests.post(f"{peer}/evaluate", json=data, timeout=10)
                if r.status_code == 200:
                    response_data = r.json()
                    responses.append({"peer": peer, "response": response_data})
                    node_ids.append(peer)
                else:
                    responses.append(
                        {"peer": peer, "error": f"HTTP {r.status_code}", "response": None}
                    )
            except Exception as e:
                responses.append({"peer": peer, "error": str(e), "response": None})

        # Get local result
        local_result = evaluate(data)
        responses.append({"peer": "local", "response": local_result})
        node_ids.append("local")

        # Apply majority consensus
        consensus_result = majority_consensus(responses)

        # Apply weighted consensus (reputation-based)
        best_hash, weights = weighted_consensus(responses, node_ids)

        # Create certificate block
        block = append_block(
            data=data,
            hash_value=consensus_result["consensus_hash"],
            metadata={
                "agreement_ratio": consensus_result["agreement_ratio"],
                "is_consensus": consensus_result["is_consensus"],
                "weighted_hash": best_hash,
                "node_count": len(node_ids),
            },
        )

        # Optional: Anchor to IPFS if available
        ipfs_cid = None
        try:
            from ipfs_anchor import anchor_ipfs

            certificate_data = {
                "decision": consensus_result,
                "certificate": {
                    "block": block,
                    "responses": responses,
                    "weighted_result": {"best_hash": best_hash, "weights": weights},
                },
            }
            ipfs_cid = anchor_ipfs(certificate_data)
            if ipfs_cid:
                block["metadata"]["ipfs_cid"] = ipfs_cid
        except ImportError:
            pass  # IPFS support not available
        except Exception:
            pass  # IPFS anchoring failed, continue without it

        return {
            "decision": consensus_result,
            "certificate": {
                "block": block,
                "responses": responses,
                "weighted_result": {"best_hash": best_hash, "weights": weights},
                "ipfs_cid": ipfs_cid,
            },
            "status": "certified" if consensus_result["is_consensus"] else "no_consensus",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decision error: {e}")


@app.get("/chain")
def get_blockchain():
    """
    Get the complete blockchain.

    Returns all blocks in chronological order.
    """
    is_valid, message = verify_chain()
    return {"chain": get_chain(), "length": len(get_chain()), "valid": is_valid, "message": message}


@app.get("/chain/{index}")
def get_blockchain_block(index: int):
    """
    Get a specific block by index.

    Args:
        index: Block index (0-based)
    """
    block = get_block(index)
    if block is None:
        raise HTTPException(status_code=404, detail=f"Block {index} not found")
    return block


@app.get("/reputation")
def get_all_reputation():
    """Get reputation scores for all nodes."""
    from consensus import REPUTATION

    return {"reputation": REPUTATION}


@app.get("/reputation/{node_id:path}")
def get_node_reputation(node_id: str):
    """Get reputation score for a specific node."""
    score = get_reputation(node_id)
    return {"node_id": node_id, "reputation": score}


@app.post("/reputation/{node_id:path}")
def set_node_reputation(node_id: str, data: dict):
    """
    Update reputation score for a node.

    Input: {"score": 0.0-1.0}
    """
    if "score" not in data:
        raise HTTPException(status_code=400, detail="Missing 'score' field")

    try:
        score = float(data["score"])
        update_reputation(node_id, score)
        return {"node_id": node_id, "reputation": score, "updated": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health():
    """Health check endpoint."""
    keys_exist = PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists()
    chain = get_chain()
    chain_valid, _ = verify_chain()

    return {
        "status": "healthy",
        "keys_configured": keys_exist,
        "peers_configured": len(PEERS),
        "blockchain_length": len(chain),
        "blockchain_valid": chain_valid,
    }
