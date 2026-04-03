#!/usr/bin/env python3
"""
Test script for Vacuum Bridge Network.
Tests individual node and consensus functionality.
"""
import json
import sys
import time

import requests

# Test data used across all tests
TEST_DATA = {"features": [[0.2, 0.8], [0.9, 0.9], [0.1, 0.2], [0.7, 0.6]], "group": [0, 1, 0, 1]}


def test_node_health(node_url):
    """Test node health endpoint."""
    print(f"\n🏥 Testing health: {node_url}")
    try:
        response = requests.get(f"{node_url}/health", timeout=5)
        print(f"✓ Status: {response.status_code}")
        print(f"  {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_node_evaluate(node_url):
    """Test node evaluation endpoint."""
    print(f"\n🧮 Testing evaluate: {node_url}")
    data = TEST_DATA

    try:
        response = requests.post(f"{node_url}/evaluate", json=data, timeout=10)
        result = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"  Disparity: {result['result']['disparity']}")
        print(f"  Constraint satisfied: {result['result']['constraint_satisfied']}")
        print(f"  Predictions: {result['result']['predictions']}")
        print(f"  Hash: {result['hash'][:16]}...")
        print(f"  Signature: {'Yes' if result.get('signature') else 'No'}")
        return response.status_code == 200, result
    except Exception as e:
        print(f"✗ Error: {e}")
        return False, None


def test_node_attest(node_url, result_data):
    """Test node attestation endpoint."""
    print(f"\n🔐 Testing attest: {node_url}")
    payload = {
        "result": result_data["result"],
        "signature": result_data.get("signature"),
        "public_key": result_data.get("public_key"),
    }

    try:
        response = requests.post(f"{node_url}/attest", json=payload, timeout=10)
        result = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"  Valid signature: {result['valid_signature']}")
        print(f"  Hash: {result['hash'][:16]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_consensus(node_url):
    """Test consensus endpoint."""
    print(f"\n🤝 Testing consensus: {node_url}")
    data = TEST_DATA

    try:
        response = requests.post(f"{node_url}/consensus", json=data, timeout=30)
        result = response.json()
        print(f"✓ Status: {response.status_code}")
        print(f"  Agreement: {result['agreement']}")
        print(f"  Consensus count: {result['consensus_count']}")
        print(f"  Hashes: {len(result['hashes'])} total")

        # Show unique hashes
        unique_hashes = set(result["hashes"])
        print(f"  Unique hashes: {len(unique_hashes)}")
        for h in unique_hashes:
            count = result["hashes"].count(h)
            print(f"    - {h[:16]}... (x{count})")

        return response.status_code == 200 and result["agreement"]
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Vacuum Bridge Network Test Suite")
    print("=" * 60)

    nodes = [
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8002",
    ]

    # Test health of all nodes
    print("\n" + "=" * 60)
    print("Phase 1: Health Checks")
    print("=" * 60)
    health_results = []
    for node in nodes:
        health_results.append(test_node_health(node))
        time.sleep(0.5)

    healthy_nodes = sum(health_results)
    print(f"\n✓ Healthy nodes: {healthy_nodes}/{len(nodes)}")

    if healthy_nodes == 0:
        print("\n✗ No nodes available. Is the network running?")
        print("  Start with: docker-compose up")
        return 1

    # Test evaluation on first node
    print("\n" + "=" * 60)
    print("Phase 2: Single Node Evaluation")
    print("=" * 60)
    success, result_data = test_node_evaluate(nodes[0])

    if not success or not result_data:
        print("\n✗ Evaluation failed")
        return 1

    # Test attestation
    print("\n" + "=" * 60)
    print("Phase 3: Attestation")
    print("=" * 60)
    if result_data.get("signature") and result_data.get("public_key"):
        test_node_attest(nodes[0], result_data)
    else:
        print("⚠ Skipping attestation test (no keys configured)")

    # Test consensus
    if healthy_nodes >= 2:
        print("\n" + "=" * 60)
        print("Phase 4: Consensus")
        print("=" * 60)
        consensus_success = test_consensus(nodes[0])

        if consensus_success:
            print("\n✓ All tests passed! Network is operational.")
            return 0
        else:
            print("\n⚠ Consensus test had issues")
            return 1
    else:
        print("\n⚠ Not enough nodes for consensus test (need at least 2)")
        print("✓ Single-node tests passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
