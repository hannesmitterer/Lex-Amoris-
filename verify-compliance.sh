#!/bin/bash

###############################################################################
# LexAmoris Compliance Verification Script
# Version: 1.0.0
# Description: Automated verification of compliance artifacts
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters - initialized to 1 to avoid arithmetic issues with set -e
PASS=1
FAIL=0
WARN=0

# Check for required tools
HAS_JQ=false
if command -v jq &> /dev/null; then
    HAS_JQ=true
fi

###############################################################################
# Helper Functions
###############################################################################

print_pass() {
    echo -e "${GREEN}✓${NC} $1"
    PASS=$((PASS + 1))
}

print_fail() {
    echo -e "${RED}✗${NC} $1"
    FAIL=$((FAIL + 1))
}

print_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARN=$((WARN + 1))
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════════════"
}

###############################################################################
# Test Functions
###############################################################################

test_file_exists() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        print_pass "$description: $file exists"
        return 0
    else
        print_fail "$description: $file NOT FOUND"
        return 1
    fi
}

test_json_valid() {
    local file=$1
    local description=$2
    
    if [ ! -f "$file" ]; then
        print_fail "$description: File not found - $file"
        return 1
    fi
    
    if [ "$HAS_JQ" = true ]; then
        if jq empty "$file" 2>/dev/null; then
            print_pass "$description: Valid JSON"
            return 0
        else
            print_fail "$description: Invalid JSON"
            return 1
        fi
    else
        print_warn "$description: jq not available, skipping JSON validation"
        return 0
    fi
}

test_json_field() {
    local file=$1
    local field=$2
    local expected=$3
    local description=$4
    
    if [ ! -f "$file" ]; then
        print_fail "$description: File not found"
        return 1
    fi
    
    if [ "$HAS_JQ" = false ]; then
        print_warn "$description: jq not available, skipping field test"
        return 0
    fi
    
    local actual
    actual=$(jq -r "$field" "$file" 2>/dev/null)
    
    if [ "$actual" = "$expected" ]; then
        print_pass "$description"
        return 0
    else
        print_fail "$description: Expected '$expected', got '$actual'"
        return 1
    fi
}

test_json_field_exists() {
    local file=$1
    local field=$2
    local description=$3
    
    if [ ! -f "$file" ]; then
        print_fail "$description: File not found"
        return 1
    fi
    
    if [ "$HAS_JQ" = false ]; then
        print_warn "$description: jq not available, skipping field test"
        return 0
    fi
    
    local value
    value=$(jq -r "$field" "$file" 2>/dev/null)
    
    if [ "$value" != "null" ] && [ -n "$value" ]; then
        print_pass "$description"
        return 0
    else
        print_fail "$description: Field missing or null"
        return 1
    fi
}

test_json_field_numeric_min() {
    local file=$1
    local field=$2
    local min_value=$3
    local description=$4
    
    if [ ! -f "$file" ]; then
        print_fail "$description: File not found"
        return 1
    fi
    
    if [ "$HAS_JQ" = false ]; then
        print_warn "$description: jq not available, skipping numeric test"
        return 0
    fi
    
    local value
    value=$(jq -r "$field" "$file" 2>/dev/null)
    
    # Validate that value is numeric before comparison
    if ! [[ "$value" =~ ^[0-9]+$ ]]; then
        print_fail "$description: Field value '$value' is not a valid number"
        return 1
    fi
    
    if [ "$value" -ge "$min_value" ]; then
        print_pass "$description: $value >= $min_value"
        return 0
    else
        print_fail "$description: $value < $min_value"
        return 1
    fi
}

###############################################################################
# Critical Artifacts Verification
###############################################################################

verify_critical_artifacts() {
    print_header "Critical Artifacts Verification"
    
    local MIN_CRITICAL_ARTIFACTS=(
        "living-covenant.json"
        "ipfs-anchoring.json"
        "key-trust-protocol.json"
        "trust-anchors.json"
        "g-csi-compliance.json"
        "nsr-enforcement.json"
    )
    
    for artifact in "${MIN_CRITICAL_ARTIFACTS[@]}"; do
        test_file_exists "$artifact" "Critical artifact" || true
        test_json_valid "$artifact" "JSON validation for $artifact" || true
    done
}

###############################################################################
# Living Covenant Verification
###############################################################################

verify_living_covenant() {
    print_header "Living Covenant Verification"
    
    local file="living-covenant.json"
    
    test_json_field_exists "$file" ".name" "Living Covenant has name" || true
    test_json_field_exists "$file" ".principles" "Living Covenant has principles" || true
    test_json_field_exists "$file" ".governance" "Living Covenant has governance" || true
    test_json_field_exists "$file" ".enforcement" "Living Covenant has enforcement" || true
    test_json_field_exists "$file" ".metadata.license" "Living Covenant has license" || true
}

###############################################################################
# IPFS Anchoring Verification
###############################################################################

verify_ipfs_anchoring() {
    print_header "IPFS Anchoring Verification"
    
    local file="ipfs-anchoring.json"
    
    test_json_field_exists "$file" ".ipfs.implementation" "IPFS implementation specified" || true
    test_json_field_exists "$file" ".ipfs.version" "IPFS version specified" || true
    test_json_field_numeric_min "$file" ".pinning.minReplication" 3 "Minimum replication >= 3" || true
    test_json_field_exists "$file" ".criticalArtifacts" "Critical artifacts listed" || true
}

###############################################################################
# Trust Protocol Verification
###############################################################################

verify_trust_protocol() {
    print_header "Key Trust Protocol Verification"
    
    local file="key-trust-protocol.json"
    
    test_json_field_exists "$file" ".standard.name" "Trust protocol standard defined" || true
    test_json_field "$file" ".standard.name" "ETSI EN 319 612" "ETSI standard compliance" || true
    test_json_field_exists "$file" ".keyManagement.algorithm" "Key algorithm specified" || true
    test_json_field_exists "$file" ".signatures.format" "Signature format specified" || true
}

###############################################################################
# Trust Anchors Verification
###############################################################################

verify_trust_anchors() {
    print_header "Trust Anchors Verification"
    
    local file="trust-anchors.json"
    
    test_json_field_exists "$file" ".trustServiceProviders" "Trust service providers defined" || true
    test_json_field_exists "$file" ".rootCertificates" "Root certificates defined" || true
    test_json_field_exists "$file" ".ipfsAnchoring.enabled" "IPFS anchoring configuration present" || true
}

###############################################################################
# G-CSI Compliance Verification
###############################################################################

verify_gcsi_compliance() {
    print_header "G-CSI Compliance Verification"
    
    local file="g-csi-compliance.json"
    
    test_json_field_exists "$file" ".governance" "Governance framework defined" || true
    test_json_field_exists "$file" ".security" "Security controls defined" || true
    test_json_field_exists "$file" ".compliance" "Compliance standards defined" || true
    test_json_field_exists "$file" ".identity" "Identity management defined" || true
}

###############################################################################
# NSR Enforcement Verification
###############################################################################

verify_nsr_enforcement() {
    print_header "NSR Enforcement Verification"
    
    local file="nsr-enforcement.json"
    
    test_json_field_exists "$file" ".principle.name" "NSR principle defined" || true
    test_json_field_exists "$file" ".validationLayers" "Validation layers defined" || true
    test_json_field_exists "$file" ".prohibitedPatterns" "Prohibited patterns defined" || true
    test_json_field_exists "$file" ".enforcement" "Enforcement mechanism defined" || true
}

###############################################################################
# Cross-References Verification
###############################################################################

verify_cross_references() {
    print_header "Cross-References Verification"
    
    # Verify IPFS anchoring references critical artifacts
    if [ "$HAS_JQ" = true ] && [ -f "ipfs-anchoring.json" ]; then
        local artifact_count
        artifact_count=$(jq '.criticalArtifacts | length' ipfs-anchoring.json 2>/dev/null || echo "0")
        if [ "$artifact_count" -ge 5 ]; then
            print_pass "IPFS anchoring references sufficient critical artifacts ($artifact_count)"
        else
            print_fail "IPFS anchoring should reference at least 5 critical artifacts (found $artifact_count)"
        fi
    fi
    
    # Verify g-csi-compliance.json is in critical artifacts list
    if [ "$HAS_JQ" = true ] && [ -f "ipfs-anchoring.json" ]; then
        local has_gcsi
        has_gcsi=$(jq '.criticalArtifacts[] | select(.artifact == "g-csi-compliance.json")' ipfs-anchoring.json 2>/dev/null)
        if [ -n "$has_gcsi" ]; then
            print_pass "g-csi-compliance.json is in critical artifacts list"
        else
            print_fail "g-csi-compliance.json should be in critical artifacts list"
        fi
    fi
    
    # Verify trust-anchors references IPFS
    if [ "$HAS_JQ" = true ] && [ -f "trust-anchors.json" ]; then
        local has_ipfs
        has_ipfs=$(jq -r '.ipfsAnchoring.enabled' trust-anchors.json 2>/dev/null)
        if [ "$has_ipfs" = "true" ]; then
            print_pass "Trust anchors has IPFS anchoring enabled"
        else
            print_warn "Trust anchors IPFS anchoring not enabled"
        fi
    fi
    
    # Verify key-trust-protocol references trust-anchors
    if [ "$HAS_JQ" = true ] && [ -f "key-trust-protocol.json" ]; then
        local has_trust_ref
        has_trust_ref=$(jq -r '.trustAnchors.source' key-trust-protocol.json 2>/dev/null)
        if [ "$has_trust_ref" = "trust-anchors.json" ]; then
            print_pass "Key trust protocol references trust-anchors.json"
        else
            print_warn "Key trust protocol should reference trust-anchors.json"
        fi
    fi
}

###############################################################################
# Summary
###############################################################################

print_summary() {
    print_header "Verification Summary"
    
    # Adjust for initial value of 1
    local actual_pass=$((PASS - 1))
    
    echo ""
    echo -e "${GREEN}✓ Passed:${NC}  $actual_pass"
    echo -e "${RED}✗ Failed:${NC}  $FAIL"
    echo -e "${YELLOW}⚠ Warnings:${NC} $WARN"
    echo ""
    
    if [ $FAIL -eq 0 ]; then
        echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  ✓ All critical checks passed!${NC}"
        echo -e "${GREEN}  📜⚖️❤️ Lex Amoris Compliance: VERIFIED${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
        exit 0
    else
        echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
        echo -e "${RED}  ✗ Compliance verification failed${NC}"
        echo -e "${RED}  Please address the issues above${NC}"
        echo -e "${RED}═══════════════════════════════════════════════════════════════${NC}"
        exit 1
    fi
}

###############################################################################
# Main Execution
###############################################################################

main() {
    print_header "LexAmoris Compliance Verification"
    print_info "Version: 1.0.0"
    print_info "Date: $(date '+%Y-%m-%d %H:%M:%S')"
    
    if [ "$HAS_JQ" = false ]; then
        print_warn "jq is not installed. Some validations will be skipped."
        print_info "Install jq for complete validation: apt-get install jq / brew install jq"
    fi
    
    # Run all verification modules
    verify_critical_artifacts
    verify_living_covenant
    verify_ipfs_anchoring
    verify_trust_protocol
    verify_trust_anchors
    verify_gcsi_compliance
    verify_nsr_enforcement
    verify_cross_references
    
    # Print summary
    print_summary
}

# Execute main function
main "$@"
