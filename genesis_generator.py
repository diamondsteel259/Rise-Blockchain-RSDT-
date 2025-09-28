#!/usr/bin/env python3
# Copyright (c) 2025, The RSDT Project
# 
# All rights reserved.

import struct
import hashlib
import time

def create_rsdt_genesis():
    """Create RSDT genesis transaction"""
    
    # Genesis message
    genesis_message = "Censorship is control; privacy is resistance"
    genesis_timestamp = int(time.mktime(time.strptime("2026-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")))
    
    # Create a simple genesis transaction
    # This is a simplified version - in production you'd use the actual Monero transaction format
    
    # Transaction version
    tx_version = struct.pack('<B', 1)
    
    # Input count (1 for coinbase)
    input_count = struct.pack('<B', 1)
    
    # Coinbase input (txin_gen)
    input_type = struct.pack('<B', 0xFF)  # txin_gen type
    height = struct.pack('<I', 0)  # Genesis height
    
    # Output count (1 for initial reward)
    output_count = struct.pack('<B', 1)
    
    # Output amount (50 RSDT = 50 * 10^12 atomic units)
    amount = struct.pack('<Q', 50 * 10**12)
    
    # Output type (txout_to_key)
    output_type = struct.pack('<B', 2)
    
    # Dummy public key (in real implementation, this would be the miner's key)
    pubkey = b'\x00' * 32
    
    # Extra data
    extra_size = struct.pack('<B', 0)
    
    # Unlock time
    unlock_time = struct.pack('<I', 0)
    
    # Build transaction
    tx_data = (
        tx_version +
        input_count +
        input_type +
        height +
        output_count +
        amount +
        output_type +
        pubkey +
        extra_size +
        unlock_time
    )
    
    # Convert to hex
    genesis_tx_hex = tx_data.hex()
    
    print(f"RSDT Genesis Transaction:")
    print(f"Message: {genesis_message}")
    print(f"Timestamp: {genesis_timestamp}")
    print(f"Transaction: {genesis_tx_hex}")
    print(f"Length: {len(genesis_tx_hex)}")
    
    return genesis_tx_hex

if __name__ == '__main__':
    create_rsdt_genesis()

