"""
Optional IPFS anchoring support for Vacuum Bridge Network.

Allows storing certificates on IPFS for immutable public verification.
"""
import json
from typing import Any, Dict, Optional

import requests


def anchor_ipfs(data: Dict[str, Any], ipfs_url: str = "http://localhost:5001") -> Optional[str]:
    """
    Anchor data to IPFS.

    Args:
        data: Dictionary to store on IPFS
        ipfs_url: IPFS API endpoint (default: local Kubo node)

    Returns:
        IPFS CID (Content Identifier) or None if failed

    Example:
        >>> cert = {"decision": {...}, "certificate": {...}}
        >>> cid = anchor_ipfs(cert)
        >>> print(f"Certificate stored at: ipfs://{cid}")
    """
    try:
        # Convert data to JSON bytes
        json_data = json.dumps(data, sort_keys=True, indent=2)

        # Add to IPFS
        response = requests.post(
            f"{ipfs_url}/api/v0/add",
            files={"file": ("certificate.json", json_data.encode(), "application/json")},
            timeout=30,
        )

        if response.status_code == 200:
            result = response.json()
            return result["Hash"]
        else:
            print(f"IPFS error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Failed to anchor to IPFS: {e}")
        return None


def retrieve_ipfs(cid: str, ipfs_url: str = "http://localhost:5001") -> Optional[Dict[str, Any]]:
    """
    Retrieve data from IPFS by CID.

    Args:
        cid: IPFS Content Identifier
        ipfs_url: IPFS API endpoint

    Returns:
        Retrieved data dictionary or None if failed
    """
    try:
        response = requests.post(f"{ipfs_url}/api/v0/cat?arg={cid}", timeout=30)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"IPFS retrieval error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Failed to retrieve from IPFS: {e}")
        return None


def verify_certificate_ipfs(cid: str, ipfs_url: str = "http://localhost:5001") -> bool:
    """
    Verify a certificate exists and is accessible on IPFS.

    Args:
        cid: IPFS Content Identifier
        ipfs_url: IPFS API endpoint

    Returns:
        True if certificate is accessible, False otherwise
    """
    data = retrieve_ipfs(cid, ipfs_url)
    return data is not None and "decision" in data and "certificate" in data
