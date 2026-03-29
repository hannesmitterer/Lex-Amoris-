# LexAmoris Compliance Verification

This document describes how to verify the compliance and integrity of the LexAmoris framework.

## Overview

The LexAmoris compliance framework ensures bio-ethical sovereignty, transparency, and zero-tolerance for surveillance through a combination of cryptographic validation, distributed consensus, and continuous monitoring.

## Automated Verification

### Using the Verification Script

The repository includes an automated verification script that validates all compliance artifacts:

```bash
./verify-compliance.sh
```

This script performs the following checks:

1. **Critical Artifacts Verification**: Ensures all required JSON files exist and are valid
2. **Living Covenant Verification**: Validates governance principles and enforcement mechanisms
3. **IPFS Anchoring Verification**: Confirms distributed storage configuration
4. **Trust Protocol Verification**: Validates ETSI EN 319 612 compliance
5. **Trust Anchors Verification**: Confirms cryptographic trust anchors
6. **G-CSI Compliance Verification**: Validates Governance, Security, Compliance, and Identity framework
7. **NSR Enforcement Verification**: Confirms No Surveillance Regime enforcement
8. **Cross-References Verification**: Ensures all artifacts correctly reference each other

### Requirements

- **bash**: Version 4.0 or higher
- **jq**: JSON processor (recommended but optional)

Install jq:
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq

# Alpine
apk add jq
```

## Manual Verification

### Step 1: Verify File Existence

Ensure all critical artifacts are present:

```bash
ls -la *.json verify-compliance.sh
```

Expected files:
- `living-covenant.json`
- `ipfs-anchoring.json`
- `key-trust-protocol.json`
- `trust-anchors.json`
- `g-csi-compliance.json`
- `nsr-enforcement.json`

### Step 2: Validate JSON Structure

Check each JSON file for validity:

```bash
jq empty living-covenant.json
jq empty ipfs-anchoring.json
jq empty key-trust-protocol.json
jq empty trust-anchors.json
jq empty g-csi-compliance.json
jq empty nsr-enforcement.json
```

All commands should complete without errors.

### Step 3: Verify Key Fields

#### Living Covenant
```bash
jq '.principles, .governance, .enforcement' living-covenant.json
```

#### IPFS Anchoring
```bash
jq '.ipfs.implementation, .ipfs.version, .pinning.minReplication' ipfs-anchoring.json
```

Should show:
- Implementation: `kubo`
- Version: `0.28.0` (Kubo/Go IPFS implementation version)
- Minimum replication: 3 or higher

#### Key Trust Protocol
```bash
jq '.standard.name, .keyManagement.algorithm' key-trust-protocol.json
```

Should show ETSI EN 319 612 compliance.

#### G-CSI Compliance
```bash
jq '.governance, .security, .compliance, .identity' g-csi-compliance.json
```

### Step 4: Verify Cross-References

Check that artifacts correctly reference each other:

```bash
# Verify IPFS anchoring includes all critical artifacts
jq '.criticalArtifacts[].artifact' ipfs-anchoring.json

# Verify trust protocol references trust anchors
jq '.trustAnchors.source' key-trust-protocol.json

# Verify trust anchors enable IPFS
jq '.ipfsAnchoring.enabled' trust-anchors.json
```

## Continuous Verification

For production deployments, we recommend:

1. **Pre-commit Hooks**: Run verification before committing changes
2. **CI/CD Integration**: Include verification in your build pipeline
3. **Scheduled Audits**: Run verification daily via cron or scheduled jobs
4. **IPFS Monitoring**: Continuously verify pinning status and replication

### Example CI Integration

```yaml
# .github/workflows/verify-compliance.yml
name: Compliance Verification

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: sudo apt-get install -y jq
      - name: Run compliance verification
        run: ./verify-compliance.sh
```

## Interpreting Results

The verification script will output:

- ✓ **Green checkmarks**: Tests passed
- ✗ **Red X marks**: Tests failed (requires attention)
- ⚠ **Yellow warnings**: Non-critical issues

### Success Output

```
═══════════════════════════════════════════════════════════════
  ✓ All critical checks passed!
  📜⚖️❤️ Lex Amoris Compliance: VERIFIED
═══════════════════════════════════════════════════════════════
```

### Failure Output

If any checks fail, the script will:
1. List all failed tests with descriptions
2. Exit with status code 1
3. Display summary of passed/failed/warning counts

## Troubleshooting

### Common Issues

**Issue**: `jq: command not found`
**Solution**: Install jq using your package manager (see Requirements section)

**Issue**: `Permission denied: ./verify-compliance.sh`
**Solution**: Make the script executable: `chmod +x verify-compliance.sh`

**Issue**: JSON validation fails
**Solution**: Check JSON syntax using an online validator or `jq` directly

**Issue**: Cross-reference validation fails
**Solution**: Ensure all referenced files exist and contain expected fields

## Compliance Standards

The framework adheres to:

- **G-CSI-2026**: Governance, Security, Compliance, and Identity framework
- **ETSI EN 319 612**: Electronic Signatures and Infrastructures (ESI); Trusted Lists
- **IPFS Anchoring v1**: Distributed storage with Kubo 0.28.0
- **Bio-Ethical Consensus v1**: Living Covenant principles

## IPFS Verification Note

The framework uses **Kubo v0.28.0** (the Go IPFS implementation, formerly go-ipfs). IPFS specifications are published as a suite of separate specifications at [specs.ipfs.tech](https://specs.ipfs.tech/), not as a single versioned "IPFS Spec".

References to implementation versions (e.g., Kubo 0.28.0) should not be confused with specification versions.

## Support

For questions or issues:
- Review this documentation
- Check the [IMPLEMENTATION.md](IMPLEMENTATION.md) for technical details
- Open an issue in the repository
- Contact the LexAmoris community

## License

This verification framework is part of the LexAmoris project.
See [LICENSE](LICENSE) for details.

---

📜⚖️❤️ **Lex Amoris: Protection of the Law of Love**

*Sempre in Costante* | Hannes Mitterer
