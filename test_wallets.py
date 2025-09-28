#!/usr/bin/env python3
import requests
import json

def get_info():
    """Get blockchain info"""
    try:
        response = requests.post('http://127.0.0.1:28091/json_rpc',
                               json={
                                   "jsonrpc": "2.0",
                                   "id": "0",
                                   "method": "get_info"
                               },
                               timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error getting info: {e}")
    return None

def get_block(height):
    """Get block by height"""
    try:
        response = requests.post('http://127.0.0.1:28091/json_rpc',
                               json={
                                   "jsonrpc": "2.0",
                                   "id": "0",
                                   "method": "get_block",
                                   "params": {
                                       "height": height
                                   }
                               },
                               timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error getting block: {e}")
    return None

def main():
    print("Testing RSDT Blockchain...")
    
    # Get blockchain info
    info = get_info()
    if info:
        print(f"Current height: {info['result']['height']}")
        print(f"Difficulty: {info['result']['difficulty']}")
        print(f"Network: {info['result'].get('nettype', 'unknown')}")
    
    # Get genesis block
    print("\nTesting Genesis Block...")
    genesis = get_block(0)
    if genesis:
        print("Genesis block retrieved successfully!")
        print(f"Block hash: {genesis['result']['block_header']['hash']}")
        print(f"Block timestamp: {genesis['result']['block_header']['timestamp']}")
        print(f"Block reward: {genesis['result']['block_header']['reward']}")
    else:
        print("Failed to retrieve genesis block")

if __name__ == "__main__":
    main()
