#!/usr/bin/env python3
"""
Test script for robust consensus mechanisms.
Tests majority voting, reputation, blockchain, and /decision endpoint.
"""
import json
import sys
import time

import requests

# Test data
TEST_DATA = {"features": [[0.2, 0.8], [0.9, 0.9], [0.1, 0.2], [0.7, 0.6]], "group": [0, 1, 0, 1]}


def test_decision_endpoint(node_url):
    """Test the /decision endpoint with majority voting."""
    print(f"\n🎯 Testing /decision endpoint: {node_url}")
    print("-" * 60)

    try:
        response = requests.post(f"{node_url}/decision", json=TEST_DATA, timeout=30)
        result = response.json()

        print(f"✓ Status: {response.status_code}")
        print(f"\n📊 Decision:")
        print(f"  Consensus hash: {result['decision']['consensus_hash'][:16]}...")
        print(f"  Agreement ratio: {result['decision']['agreement_ratio']:.2%}")
        print(f"  Is consensus: {result['decision']['is_consensus']}")
        print(f"  Total votes: {result['decision']['total_votes']}")
        print(f"  Vote counts: {result['decision']['vote_counts']}")

        print(f"\n📜 Certificate:")
        block = result["certificate"]["block"]
        print(f"  Block index: {block['index']}")
        print(f"  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block['timestamp']))}")
        print(f"  Prev hash: {block['prev_hash'][:16] if block['prev_hash'] != 'genesis' else 'genesis'}...")
        print(f"  Node count: {block['metadata']['node_count']}")

        print(f"\n⚖️ Weighted Consensus:")
        weighted = result["certificate"]["weighted_result"]
        print(f"  Best hash: {weighted['best_hash'][:16] if weighted['best_hash'] else 'None'}...")
        print(f"  Weights: {weighted['weights']}")

        print(f"\n✅ Status: {result['status']}")

        return response.status_code == 200 and result["decision"]["is_consensus"]

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_blockchain(node_url):
    """Test blockchain endpoints."""
    print(f"\n⛓️  Testing blockchain: {node_url}")
    print("-" * 60)

    try:
        # Get full chain
        response = requests.get(f"{node_url}/chain", timeout=5)
        result = response.json()

        print(f"✓ Chain length: {result['length']}")
        print(f"  Chain valid: {result['valid']}")
        print(f"  Message: {result['message']}")

        # Get specific blocks
        if result["length"] > 0:
            print(f"\n📦 First block:")
            block = result["chain"][0]
            print(f"  Index: {block['index']}")
            print(f"  Hash: {block['hash'][:16]}...")
            print(f"  Prev hash: {block['prev_hash']}")

            if result["length"] > 1:
                print(f"\n📦 Latest block:")
                block = result["chain"][-1]
                print(f"  Index: {block['index']}")
                print(f"  Hash: {block['hash'][:16]}...")
                print(f"  Prev hash: {block['prev_hash'][:16]}...")

        return response.status_code == 200 and result["valid"]

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_reputation(node_url):
    """Test reputation endpoints."""
    print(f"\n⭐ Testing reputation: {node_url}")
    print("-" * 60)

    try:
        # Get all reputation
        response = requests.get(f"{node_url}/reputation", timeout=5)
        result = response.json()

        print(f"✓ Reputation scores:")
        for node, score in result["reputation"].items():
            print(f"  {node}: {score:.2f}")

        # Get specific node reputation
        test_node = "http://localhost:8000"
        response2 = requests.get(f"{node_url}/reputation/{test_node}", timeout=5)
        result2 = response2.json()
        print(f"\n  Specific query ({test_node}): {result2['reputation']:.2f}")

        return response.status_code == 200

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_health_with_blockchain(node_url):
    """Test updated health endpoint."""
    print(f"\n🏥 Testing health (with blockchain info): {node_url}")
    print("-" * 60)

    try:
        response = requests.get(f"{node_url}/health", timeout=5)
        result = response.json()

        print(f"✓ Status: {result['status']}")
        print(f"  Keys configured: {result['keys_configured']}")
        print(f"  Peers configured: {result['peers_configured']}")
        print(f"  Blockchain length: {result['blockchain_length']}")
        print(f"  Blockchain valid: {result['blockchain_valid']}")

        return response.status_code == 200

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_majority_consensus_tolerance():
    """Test that majority consensus tolerates divergent nodes."""
    print(f"\n🔬 Testing majority consensus tolerance")
    print("-" * 60)

    from consensus import majority_consensus

    # Scenario 1: Unanimous agreement
    print("Scenario 1: Unanimous agreement (3/3)")
    responses = [{"hash": "abc123"}, {"hash": "abc123"}, {"hash": "abc123"}]
    result = majority_consensus(responses)
    print(f"  Consensus: {result['is_consensus']}")
    print(f"  Ratio: {result['agreement_ratio']:.2%}")
    assert result["is_consensus"] is True
    print("  ✓ Passed")

    # Scenario 2: Majority but not unanimous (2/3)
    print("\nScenario 2: Majority but not unanimous (2/3)")
    responses = [{"hash": "abc123"}, {"hash": "abc123"}, {"hash": "xyz789"}]
    result = majority_consensus(responses)
    print(f"  Consensus: {result['is_consensus']}")
    print(f"  Ratio: {result['agreement_ratio']:.2%}")
    assert result["is_consensus"] is True
    print("  ✓ Passed - Tolerates 1 divergent node")

    # Scenario 3: No majority (split vote)
    print("\nScenario 3: No majority (1/1/1 split)")
    responses = [{"hash": "abc123"}, {"hash": "xyz789"}, {"hash": "def456"}]
    result = majority_consensus(responses)
    print(f"  Consensus: {result['is_consensus']}")
    print(f"  Ratio: {result['agreement_ratio']:.2%}")
    assert result["is_consensus"] is False
    print("  ✓ Passed - Correctly rejects split vote")

    # Scenario 4: Exactly 50% (should fail for even number)
    print("\nScenario 4: Split 50/50 (2/2)")
    responses = [{"hash": "abc123"}, {"hash": "abc123"}, {"hash": "xyz789"}, {"hash": "xyz789"}]
    result = majority_consensus(responses)
    print(f"  Consensus: {result['is_consensus']}")
    print(f"  Ratio: {result['agreement_ratio']:.2%}")
    assert result["is_consensus"] is False
    print("  ✓ Passed - Correctly requires >50%")

    print("\n✅ All majority consensus tests passed!")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Vacuum Bridge Network - Robust Consensus Tests")
    print("=" * 60)

    # Test consensus logic first
    print("\n" + "=" * 60)
    print("Phase 1: Consensus Logic Tests")
    print("=" * 60)
    consensus_ok = test_majority_consensus_tolerance()

    # Test network endpoints
    node_url = "http://localhost:8000"

    print("\n" + "=" * 60)
    print("Phase 2: Network Endpoint Tests")
    print("=" * 60)

    try:
        # Check if node is available
        requests.get(f"{node_url}/health", timeout=2)
    except Exception:
        print(f"\n⚠ Node not available at {node_url}")
        print("  Start the network with: docker-compose up")
        print(f"\n✓ Consensus logic tests passed ({1 if consensus_ok else 0}/1)")
        return 0 if consensus_ok else 1

    health_ok = test_health_with_blockchain(node_url)
    reputation_ok = test_reputation(node_url)
    decision_ok = test_decision_endpoint(node_url)
    blockchain_ok = test_blockchain(node_url)

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    tests = [
        ("Consensus Logic", consensus_ok),
        ("Health Endpoint", health_ok),
        ("Reputation Endpoint", reputation_ok),
        ("Decision Endpoint", decision_ok),
        ("Blockchain Endpoint", blockchain_ok),
    ]

    passed = sum(1 for _, ok in tests if ok)
    total = len(tests)

    for name, ok in tests:
        status = "✓" if ok else "✗"
        print(f"{status} {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Robust consensus is operational.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
