#!/usr/bin/env python3
"""
Create RSDT Genesis Block with Premine
This script creates a proper genesis block that includes:
1. Coinbase transaction (50 RSDT)
2. Premine transactions (20M RSDT total)
"""

import struct
import hashlib

# RSDT Premine Allocation (20M RSDT total - 10% of 200M supply)
PREMINE_ALLOCATION = {
    "RSDT_Liquidity_1": 4500000,      # 4.5M RSDT
    "RSDT_Development_1": 3750000,    # 3.75M RSDT  
    "RSDT_Marketing_1": 3000000,      # 3M RSDT
    "RSDT_Team_1": 2250000,           # 2.25M RSDT
    "RSDT_Treasury_1": 1500000,       # 1.5M RSDT
    "RSDT_OTC_Sales": 2750000,        # 2.75M RSDT
    "RSDT_Founder_Private": 2250000   # 2.25M RSDT
}

# Convert to atomic units (1 RSDT = 10^12 atomic units)
COIN = 10**12

def create_genesis_transactions():
    """Create genesis block transactions"""
    
    # Genesis message
    genesis_message = "Censorship is control; privacy is resistance"
    
    # Coinbase transaction (50 RSDT)
    coinbase_amount = 50 * COIN
    
    # Premine transactions
    premine_transactions = []
    total_premine = 0
    
    for wallet_name, amount_rsdt in PREMINE_ALLOCATION.items():
        amount_atomic = amount_rsdt * COIN
        total_premine += amount_atomic
        
        # Create premine transaction
        tx = {
            "wallet": wallet_name,
            "amount": amount_atomic,
            "amount_rsdt": amount_rsdt
        }
        premine_transactions.append(tx)
    
    print(f"Genesis Block Configuration:")
    print(f"Coinbase: {50} RSDT")
    print(f"Total Premine: {total_premine / COIN:.0f} RSDT")
    print(f"Genesis Message: {genesis_message}")
    print(f"Premine Wallets: {len(premine_transactions)}")
    
    return coinbase_amount, premine_transactions, genesis_message

if __name__ == "__main__":
    coinbase, premine, message = create_genesis_transactions()
    
    print("\nPremine Allocation:")
    for tx in premine:
        print(f"  {tx['wallet']}: {tx['amount_rsdt']:,} RSDT")
    
    print(f"\nTotal Supply at Genesis: {(50 + sum(tx['amount_rsdt'] for tx in premine)):,} RSDT")
