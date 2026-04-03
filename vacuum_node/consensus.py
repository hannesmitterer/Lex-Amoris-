"""
Consensus mechanisms for Vacuum Bridge Network.

Implements:
- Majority voting (tolerates divergent nodes)
- Reputation-based weighted consensus
- Append-only blockchain log
"""
import time
from collections import Counter
from typing import Any, Dict, List, Tuple

# Reputation scores for nodes (1.0 = full trust)
REPUTATION = {
    "http://node-a:8000": 1.0,
    "http://node-b:8000": 1.0,
    "http://node-c:8000": 1.0,
    "http://localhost:8000": 1.0,
    "http://localhost:8001": 1.0,
    "http://localhost:8002": 1.0,
}

# Append-only blockchain-like log
CHAIN: List[Dict[str, Any]] = []


def majority_consensus(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute majority consensus from node responses.

    Tolerates divergent nodes by accepting the most common hash
    if it has majority support (> 50% of nodes).

    Args:
        responses: List of response dictionaries containing "hash" keys

    Returns:
        Dictionary with:
        - consensus_hash: The most common hash
        - agreement_ratio: Fraction of nodes agreeing (0.0 to 1.0)
        - is_consensus: True if majority achieved (>50%)
        - vote_counts: Dictionary of hash -> count
    """
    # Extract hashes from responses
    hashes = []
    for r in responses:
        if isinstance(r, dict) and "hash" in r:
            hashes.append(r["hash"])
        elif isinstance(r, dict) and "response" in r and r["response"]:
            if "hash" in r["response"]:
                hashes.append(r["response"]["hash"])

    if not hashes:
        return {
            "consensus_hash": None,
            "agreement_ratio": 0.0,
            "is_consensus": False,
            "vote_counts": {},
            "total_votes": 0,
        }

    # Count occurrences
    count = Counter(hashes)
    most_common, freq = count.most_common(1)[0]

    total = len(hashes)
    majority_threshold = total // 2 + 1

    return {
        "consensus_hash": most_common,
        "agreement_ratio": freq / total,
        "is_consensus": freq >= majority_threshold,
        "vote_counts": dict(count),
        "total_votes": total,
    }


def weighted_consensus(
    responses: List[Dict[str, Any]], node_ids: List[str]
) -> Tuple[str, Dict[str, float]]:
    """
    Compute weighted consensus based on node reputation.

    Nodes with higher reputation scores have more influence.

    Args:
        responses: List of response dictionaries
        node_ids: List of node identifiers (URLs or IDs)

    Returns:
        Tuple of (best_hash, weights_dict)
        - best_hash: Hash with highest weighted score
        - weights_dict: Dictionary of hash -> total weight
    """
    weights: Dict[str, float] = {}

    for r, nid in zip(responses, node_ids):
        # Extract hash
        h = None
        if isinstance(r, dict) and "hash" in r:
            h = r["hash"]
        elif isinstance(r, dict) and "response" in r and r["response"]:
            if "hash" in r["response"]:
                h = r["response"]["hash"]

        if h:
            # Get reputation score (default to 0.5 if unknown)
            rep = REPUTATION.get(nid, 0.5)
            weights[h] = weights.get(h, 0.0) + rep

    if not weights:
        return None, {}

    best_hash = max(weights, key=weights.get)
    return best_hash, weights


def append_block(data: Dict[str, Any], hash_value: str, metadata: Dict = None) -> Dict[str, Any]:
    """
    Append a block to the immutable chain.

    Each block contains:
    - timestamp: Unix timestamp
    - data: The input data
    - hash: The consensus hash
    - prev_hash: Hash of previous block (or "genesis")
    - metadata: Optional additional information

    Args:
        data: The decision data
        hash_value: The consensus hash
        metadata: Optional metadata dictionary

    Returns:
        The created block dictionary
    """
    block = {
        "index": len(CHAIN),
        "timestamp": time.time(),
        "data": data,
        "hash": hash_value,
        "prev_hash": CHAIN[-1]["hash"] if CHAIN else "genesis",
        "metadata": metadata or {},
    }
    CHAIN.append(block)
    return block


def get_chain() -> List[Dict[str, Any]]:
    """
    Get the complete blockchain.

    Returns:
        List of all blocks in chronological order
    """
    return CHAIN.copy()


def get_block(index: int) -> Dict[str, Any]:
    """
    Get a specific block by index.

    Args:
        index: Block index (0-based)

    Returns:
        Block dictionary or None if index out of range
    """
    if 0 <= index < len(CHAIN):
        return CHAIN[index].copy()
    return None


def verify_chain() -> Tuple[bool, str]:
    """
    Verify the integrity of the blockchain.

    Checks that:
    - First block has prev_hash of "genesis"
    - Each subsequent block's prev_hash matches previous block's hash

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not CHAIN:
        return True, "Empty chain is valid"

    # Check genesis block
    if CHAIN[0]["prev_hash"] != "genesis":
        return False, "First block must have prev_hash='genesis'"

    # Check chain continuity
    for i in range(1, len(CHAIN)):
        if CHAIN[i]["prev_hash"] != CHAIN[i - 1]["hash"]:
            return False, f"Chain broken at block {i}"

    return True, "Chain is valid"


def update_reputation(node_id: str, new_score: float):
    """
    Update reputation score for a node.

    Args:
        node_id: Node identifier
        new_score: New reputation score (0.0 to 1.0)
    """
    if 0.0 <= new_score <= 1.0:
        REPUTATION[node_id] = new_score
    else:
        raise ValueError(f"Reputation score must be between 0.0 and 1.0, got {new_score}")


def get_reputation(node_id: str) -> float:
    """
    Get reputation score for a node.

    Args:
        node_id: Node identifier

    Returns:
        Reputation score (default 0.5 for unknown nodes)
    """
    return REPUTATION.get(node_id, 0.5)
