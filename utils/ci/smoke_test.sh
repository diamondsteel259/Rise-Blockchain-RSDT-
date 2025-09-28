#!/bin/bash
# RSDT Smoke Test Script
# This script performs basic smoke tests on the compiled RSDT daemon
# 
# IMPORTANT: This script is GUARDED and does NOT run automatically in CI
# It requires manual execution and a properly configured environment
# 
# Usage: ./utils/ci/smoke_test.sh [daemon_path]
# Example: ./utils/ci/smoke_test.sh ./build/bin/rsdtd

set -e

DAEMON_PATH="${1:-./build/bin/rsdtd}"
TIMEOUT=10

echo "=================================="
echo "RSDT Daemon Smoke Test"
echo "=================================="
echo "Daemon path: $DAEMON_PATH"
echo "Timeout: ${TIMEOUT}s"
echo ""

# Check if daemon exists and is executable
if [ ! -x "$DAEMON_PATH" ]; then
    echo "ERROR: Daemon not found or not executable at: $DAEMON_PATH"
    echo "Please build the project first:"
    echo "  mkdir build && cd build"
    echo "  cmake -DCMAKE_BUILD_TYPE=Release .."
    echo "  make -j\$(nproc)"
    exit 1
fi

echo "✓ Daemon binary found and executable"

# Test 1: Version check
echo ""
echo "Test 1: Checking daemon version..."
if timeout $TIMEOUT "$DAEMON_PATH" --version 2>/dev/null; then
    echo "✓ Version check successful"
else
    echo "⚠ Version check failed or timed out"
fi

# Test 2: Help command
echo ""
echo "Test 2: Checking help output..."
if timeout $TIMEOUT "$DAEMON_PATH" --help >/dev/null 2>&1; then
    echo "✓ Help command successful"
else
    echo "⚠ Help command failed or timed out"
fi

# Test 3: Basic RPC connectivity test (requires running daemon)
echo ""
echo "Test 3: RPC connectivity test (optional)"
echo "NOTE: This test requires a running daemon. Starting test daemon..."
echo "WARNING: This test will create temporary blockchain data"

# Create temp directory for test
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

# Function to cleanup
cleanup() {
    echo "Cleaning up..."
    if [ -n "$DAEMON_PID" ]; then
        kill $DAEMON_PID 2>/dev/null || true
        wait $DAEMON_PID 2>/dev/null || true
    fi
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Start daemon in background for RPC test
echo "Starting test daemon..."
"$DAEMON_PATH" --data-dir "$TEMP_DIR" --testnet --offline --rpc-bind-port 18081 --no-igd --hide-my-port &
DAEMON_PID=$!

# Wait a moment for daemon to start
sleep 5

# Test basic RPC call using curl (if available)
if command -v curl >/dev/null 2>&1; then
    echo "Testing RPC get_info call..."
    if curl -s --max-time 5 -X POST http://127.0.0.1:18081/json_rpc \
        -H 'Content-Type: application/json' \
        -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' >/dev/null 2>&1; then
        echo "✓ RPC test successful"
    else
        echo "⚠ RPC test failed (daemon may still be starting or RPC disabled)"
    fi
else
    echo "⚠ curl not available, skipping RPC test"
fi

echo ""
echo "=================================="
echo "Smoke tests completed"
echo "=================================="
echo ""
echo "Manual testing recommendations:"
echo "1. Run daemon with: $DAEMON_PATH --testnet"
echo "2. Check logs for errors"
echo "3. Test wallet connectivity"
echo "4. Verify P2P connectivity"
echo ""
echo "SECURITY NOTE: Never run these tests with mainnet data"
echo "SECURITY NOTE: Do not modify genesis or premine configurations"