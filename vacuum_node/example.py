#!/usr/bin/env python3
"""
Simple example demonstrating the Vacuum Bridge Network.
Runs a single evaluation and shows all the components in action.
"""
import json

import numpy as np
from crypto import hash_result, sign_result, verify_signature
from fairness import demographic_parity
from model import predict
from verify import check_constraint


def main():
    print("=" * 60)
    print("Vacuum Bridge Network - Simple Example")
    print("=" * 60)

    # Sample data
    print("\n1. Input Data")
    print("-" * 60)
    features = np.array([[0.2, 0.8], [0.9, 0.9], [0.1, 0.2], [0.7, 0.6]])
    group = np.array([0, 1, 0, 1])

    print(f"Features: {features.tolist()}")
    print(f"Groups: {group.tolist()}")

    # Prediction
    print("\n2. Model Prediction")
    print("-" * 60)
    y_pred = predict(features)
    print(f"Predictions: {y_pred}")

    # Fairness check
    print("\n3. Fairness Check (Demographic Parity)")
    print("-" * 60)
    disparity = demographic_parity(y_pred, group)
    print(f"Disparity: {disparity:.4f}")

    # Constraint verification
    print("\n4. Constraint Verification")
    print("-" * 60)
    epsilon = 0.05
    valid = check_constraint(disparity, epsilon)
    print(f"Threshold (ε): {epsilon}")
    print(f"Constraint satisfied: {valid}")

    # Build result
    result = {
        "disparity": float(disparity),
        "constraint_satisfied": bool(valid),
        "predictions": y_pred.tolist(),
    }

    # Hash
    print("\n5. Cryptographic Hash")
    print("-" * 60)
    result_str = json.dumps(result, sort_keys=True)
    result_hash = hash_result(result_str)
    print(f"Result JSON: {result_str}")
    print(f"SHA256 Hash: {result_hash}")

    # Sign (if keys available)
    print("\n6. Digital Signature")
    print("-" * 60)
    try:
        signature = sign_result("keys/private.pem", result_str.encode())
        print(f"Signature: {signature[:64]}...")

        # Verify signature
        print("\n7. Signature Verification")
        print("-" * 60)
        with open("keys/public.pem") as f:
            public_key = f.read()

        is_valid = verify_signature(public_key, result_str.encode(), signature)
        print(f"Signature valid: {is_valid}")

    except FileNotFoundError:
        print("⚠ Keys not found. Run ./generate-keys.sh first")

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✓ Model made {len(y_pred)} predictions")
    print(f"✓ Fairness disparity: {disparity:.4f}")
    print(f"{'✓' if valid else '✗'} Constraint {'satisfied' if valid else 'violated'}")
    print(f"✓ Result hashed and {'signed' if 'signature' in locals() else 'ready'}")
    print("\nThis is the foundation of the Vacuum Bridge:")
    print("- Deterministic predictions")
    print("- Mathematical fairness guarantees")
    print("- Cryptographic verification")
    print("- Ready for multi-node consensus")


if __name__ == "__main__":
    main()
