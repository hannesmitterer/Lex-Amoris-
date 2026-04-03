#!/bin/bash
# Script to generate RSA key pairs for each node

set -e

echo "Generating RSA key pairs for Vacuum Bridge Network nodes..."

# Function to generate keys for a node
generate_keys() {
    local node_name=$1
    local keys_dir="keys-${node_name}"
    
    echo "Generating keys for ${node_name}..."
    mkdir -p "${keys_dir}"
    
    # Generate private key
    openssl genrsa -out "${keys_dir}/private.pem" 2048 2>/dev/null
    
    # Extract public key
    openssl rsa -in "${keys_dir}/private.pem" -pubout -out "${keys_dir}/public.pem" 2>/dev/null
    
    echo "✓ Keys generated for ${node_name} in ${keys_dir}/"
}

# Generate keys for each node
generate_keys "a"
generate_keys "b"
generate_keys "c"

# Also generate a default set for local testing
echo "Generating default keys for local testing..."
mkdir -p "keys"
openssl genrsa -out "keys/private.pem" 2048 2>/dev/null
openssl rsa -in "keys/private.pem" -pubout -out "keys/public.pem" 2>/dev/null
echo "✓ Default keys generated in keys/"

echo ""
echo "All keys generated successfully!"
echo ""
echo "Key directories created:"
echo "  - keys-a/     (for node-a)"
echo "  - keys-b/     (for node-b)"
echo "  - keys-c/     (for node-c)"
echo "  - keys/       (for local testing)"
echo ""
echo "You can now start the network with: docker-compose up --build"
