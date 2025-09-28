#!/bin/bash

echo "Creating ALL 7 Premine Wallets with Revised Allocation"
echo "=================================================="
echo

wallets=(
    "RSDT_Liquidity"
    "RSDT_Development" 
    "RSDT_Marketing"
    "RSDT_Team"
    "RSDT_Treasury"
    "RSDT_OTC_Sales"
    "RSDT_Founder_Private"
)

echo "=== RESISTANCE BLOCKCHAIN PREMINE WALLET CREATION ===" > all_premine_wallets.txt
echo "Total Premine: 20M RSDT (10% of 200M total supply)" >> all_premine_wallets.txt
echo "Generated: $(date)" >> all_premine_wallets.txt
echo "" >> all_premine_wallets.txt

for wallet in "${wallets[@]}"; do
    echo "=== Creating $wallet ===" >> all_premine_wallets.txt
    ./build/src/gen_premine/gen_premine "$wallet" >> all_premine_wallets.txt
    echo "" >> all_premine_wallets.txt
done

echo "✅ All 7 premine wallets created successfully!"
echo "📝 Complete wallet information saved to all_premine_wallets.txt"

# Extract just addresses for verification
grep "Address:" all_premine_wallets.txt > premine_addresses.txt
