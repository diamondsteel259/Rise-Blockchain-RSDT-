#!/bin/bash

echo "�� RESISTANCE BLOCKCHAIN - DEPLOYMENT SCRIPT"
echo "============================================="
echo

# Check if daemon is running
echo "📊 Checking daemon status..."
if curl -s -X POST http://127.0.0.1:28091/json_rpc -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' | grep -q "OK"; then
    echo "✅ Daemon is running"
else
    echo "❌ Daemon is not running. Please start the daemon first."
    exit 1
fi

echo
echo "🌐 Starting Blockchain Explorer..."
cd ../blockchain-explorer
python3 blockchain_explorer.py &
EXPLORER_PID=$!
echo "✅ Explorer started (PID: $EXPLORER_PID)"
echo "🔗 URL: http://127.0.0.1:8080"

echo
echo "⛏️ Starting Mining Pool..."
cd ../mining-pool
python3 mining_pool.py &
POOL_PID=$!
echo "✅ Mining pool started (PID: $POOL_PID)"

echo
echo "🎉 RESISTANCE BLOCKCHAIN ECOSYSTEM DEPLOYED!"
echo "============================================="
echo "✅ Core Daemon: Running"
echo "✅ Blockchain Explorer: http://127.0.0.1:8080"
echo "✅ Mining Pool: Running"
echo "✅ GUI Applications: Ready to launch"
echo
echo "🛡️ Privacy is Resistance!"
echo "🚫 Censorship is Control!"
