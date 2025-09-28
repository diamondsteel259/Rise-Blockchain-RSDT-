#!/bin/bash

echo "=== CREATING 7 PREMINE WALLETS MANUALLY ==="
echo "Total Premine: 20M RSDT"
echo ""

# Create wallet files for each category
wallets=(
    "RSDT_Liquidity:4.5M"
    "RSDT_Development:3.75M" 
    "RSDT_Marketing:3M"
    "RSDT_Team:2.25M"
    "RSDT_Treasury:1.5M"
    "RSDT_OTC_Sales:2.75M"
    "RSDT_Founder_Private:2.25M"
)

echo "=== RESISTANCE BLOCKCHAIN PREMINE WALLETS ===" > manual_premine_wallets.txt
echo "Total Premine: 20M RSDT (10% of 200M total supply)" >> manual_premine_wallets.txt
echo "Generated: $(date)" >> manual_premine_wallets.txt
echo "" >> manual_premine_wallets.txt

for wallet_info in "${wallets[@]}"; do
    wallet_name=$(echo $wallet_info | cut -d: -f1)
    amount=$(echo $wallet_info | cut -d: -f2)
    
    echo "=== $wallet_name - $amount RSDT ===" >> manual_premine_wallets.txt
    
    # Generate wallet using monero-wallet-cli
    echo "Generating $wallet_name..."
    echo "y" | ./build/bin/monero-wallet-cli --testnet --generate-new-wallet="$wallet_name" --restore-height=1 --password="" 2>/dev/null | grep -E "(Address:|Spend key:|View key:)" >> manual_premine_wallets.txt
    
    echo "" >> manual_premine_wallets.txt
done

echo "✅ All 7 premine wallets created manually!"
echo "📝 Wallet information saved to manual_premine_wallets.txt"
