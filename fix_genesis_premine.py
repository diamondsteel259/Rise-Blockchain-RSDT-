#!/usr/bin/env python3
"""
Fix RSDT Genesis Block to Include Premine
This creates a proper genesis transaction that includes the premine
"""

# RSDT Premine Allocation (17.25M RSDT total)
PREMINE_ALLOCATION = {
    "RSDT_Liquidity_1": 4500000,      # 4.5M RSDT
    "RSDT_Development_1": 3750000,    # 3.75M RSDT  
    "RSDT_Marketing_1": 3000000,      # 3M RSDT
    "RSDT_Team_1": 2250000,           # 2.25M RSDT
    "RSDT_Treasury_1": 1500000,       # 1.5M RSDT
    "RSDT_Founder_Private": 2250000    # 2.25M RSDT
}

# Convert to atomic units (1 RSDT = 10^12 atomic units)
COIN = 10**12

def create_genesis_with_premine():
    """Create genesis transaction that includes premine"""
    
    # Total premine in atomic units
    total_premine = sum(PREMINE_ALLOCATION.values()) * COIN
    coinbase_amount = 50 * COIN
    total_genesis = total_premine + coinbase_amount
    
    print("RSDT Genesis Block with Premine:")
    print(f"Coinbase: {coinbase_amount / COIN} RSDT")
    print(f"Total Premine: {total_premine / COIN:,.0f} RSDT")
    print(f"Total Genesis Supply: {total_genesis / COIN:,.0f} RSDT")
    
    print("\nPremine Breakdown:")
    for wallet, amount in PREMINE_ALLOCATION.items():
        print(f"  {wallet}: {amount:,} RSDT")
    
    # For now, we'll create a single genesis transaction that represents the total
    # In a real implementation, this would be multiple transactions
    genesis_amount_hex = hex(total_genesis)[2:].zfill(16)
    
    print(f"\nGenesis Amount (hex): {genesis_amount_hex}")
    
    # Create a simple genesis transaction string
    # This is a simplified version - the real implementation would be more complex
    genesis_tx = f"013c01ff0001{genesis_amount_hex}03029b2e4c0281c0b02e7c53291a94d1d0cbff8883f8024f5142ee494ffbbd08807121017767aafcde9be00dcfd098715ebcf7f410daebc582fda69d24a28e9d0bc890d1"
    
    print(f"Genesis Transaction: {genesis_tx}")
    
    return genesis_tx

if __name__ == "__main__":
    genesis_tx = create_genesis_with_premine()
    
    # Write to file for use in config
    with open("genesis_tx_with_premine.txt", "w") as f:
        f.write(genesis_tx)
    
    print(f"\nGenesis transaction saved to: genesis_tx_with_premine.txt")
