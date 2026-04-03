"""
Cryptographic operations for signing and verification.
"""
import hashlib

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def hash_result(data: str):
    """
    Generate SHA256 hash of data.

    Args:
        data: String data to hash

    Returns:
        Hexadecimal hash digest
    """
    return hashlib.sha256(data.encode()).hexdigest()


def sign_result(private_key_path, message: bytes):
    """
    Sign message with RSA private key.

    Args:
        private_key_path: Path to PEM private key file
        message: Bytes to sign

    Returns:
        Hexadecimal signature
    """
    with open(private_key_path, "rb") as f:
        key = serialization.load_pem_private_key(f.read(), password=None)

    signature = key.sign(message, padding.PKCS1v15(), hashes.SHA256())
    return signature.hex()


def verify_signature(public_key_pem, message, signature_hex):
    """
    Verify RSA signature.

    Args:
        public_key_pem: PEM-encoded public key string
        message: Original message bytes
        signature_hex: Hexadecimal signature string

    Returns:
        True if signature is valid, False otherwise
    """
    key = serialization.load_pem_public_key(public_key_pem.encode())

    try:
        key.verify(
            bytes.fromhex(signature_hex), message, padding.PKCS1v15(), hashes.SHA256()
        )
        return True
    except Exception:
        return False
