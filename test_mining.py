#!/usr/bin/env python3
import requests
import json
import time

def get_block_template(address):
    """Get block template for mining"""
    try:
        response = requests.post('http://127.0.0.1:28091/json_rpc', 
                               json={
                                   "jsonrpc": "2.0",
                                   "id": "0",
                                   "method": "get_block_template",
                                   "params": {
                                       "wallet_address": address,
                                       "reserve_size": 60
                                   }
                               },
                               timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error getting block template: {e}")
    return None

def submit_block(block_data):
    """Submit mined block"""
    try:
        response = requests.post('http://127.0.0.1:28091/json_rpc',
                               json={
                                   "jsonrpc": "2.0",
                                   "id": "0",
                                   "method": "submit_block",
                                   "params": [block_data]
                               },
                               timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error submitting block: {e}")
    return None

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

def main():
    # Use first premine wallet address
    address = "5qZtUCYNYzGJQUjWAkQa1G3mWXGfsfGdwUADJJofdX5yHsdUPeui5knCwmgu7qkzGVj47eaA7rJfe1Q8xndJzZEgEQ4svZW"
    
    print("Testing RSDT Mining...")
    print(f"Address: {address}")
    
    # Get current blockchain info
    info = get_info()
    if info:
        print(f"Current height: {info['result']['height']}")
        print(f"Difficulty: {info['result']['difficulty']}")
    
    # Try to get block template
    template = get_block_template(address)
    if template:
        print("Block template received successfully!")
        print(f"Template: {template}")
    else:
        print("Failed to get block template")

if __name__ == "__main__":
    main()
