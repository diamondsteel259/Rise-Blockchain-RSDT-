#!/usr/bin/env python3
"""
RSDT Linux Miner
Simple Python-based miner for testing
"""

import requests
import json
import time
import threading
import hashlib
from datetime import datetime

class RSDTLinuxMiner:
    def __init__(self, pool_url, wallet_address, worker_name, threads=1):
        self.pool_url = pool_url
        self.wallet_address = wallet_address
        self.worker_name = worker_name
        self.threads = threads
        self.mining_active = False
        self.total_hashes = 0
        self.shares_found = 0
        self.shares_accepted = 0
        self.current_job = None
        
    def connect_to_pool(self):
        """Connect to mining pool"""
        print(f"Connecting to pool: {self.pool_url}")
        
        # Login to pool
        login_data = {
            "id": 1,
            "method": "login",
            "params": {
                "login": self.wallet_address,
                "pass": self.worker_name
            }
        }
        
        try:
            response = requests.post(self.pool_url, json=login_data, timeout=10)
            result = response.json()
            
            if result.get("result", {}).get("status") == "OK":
                self.current_job = result["result"]["job"]
                print("Successfully connected to pool!")
                return True
            else:
                print("Failed to login to pool")
                return False
                
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def mine_nonce(self, nonce):
        """Mine with given nonce"""
        if not self.current_job:
            return False
            
        # Simplified mining - just check if nonce meets some criteria
        hash_input = f"{self.current_job.get('blob', '')}{nonce}"
        hash_result = hashlib.sha256(hash_input.encode()).hexdigest()
        
        # Simple difficulty check
        return hash_result.startswith("0000")
    
    def submit_share(self, nonce):
        """Submit share to pool"""
        submit_data = {
            "id": 2,
            "method": "submit",
            "params": {
                "login": self.wallet_address,
                "pass": self.worker_name,
                "nonce": str(nonce),
                "job_id": self.current_job.get("job_id", "")
            }
        }
        
        try:
            response = requests.post(self.pool_url, json=submit_data, timeout=10)
            result = response.json()
            return result.get("result", {}).get("status") == "OK"
        except:
            return False
    
    def mining_thread(self, thread_id):
        """Mining thread worker"""
        nonce = thread_id * 1000000
        thread_hashes = 0
        
        while self.mining_active:
            if self.mine_nonce(nonce):
                self.shares_found += 1
                if self.submit_share(nonce):
                    self.shares_accepted += 1
                    print(f"Share accepted! Nonce: {nonce}")
                else:
                    print(f"Share rejected! Nonce: {nonce}")
            
            nonce += 1
            thread_hashes += 1
            self.total_hashes += 1
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.001)
    
    def stats_thread(self):
        """Display mining statistics"""
        start_time = time.time()
        
        while self.mining_active:
            time.sleep(10)
            
            if self.mining_active:
                elapsed = time.time() - start_time
                hashrate = self.total_hashes / elapsed if elapsed > 0 else 0
                
                print(f"\rH/s: {hashrate:8.0f} | Total: {self.total_hashes:12} | "
                      f"Shares: {self.shares_found:4} | Accepted: {self.shares_accepted:4}", end="")
    
    def start_mining(self):
        """Start mining"""
        if self.mining_active:
            print("Mining already active!")
            return
        
        self.mining_active = True
        threads = []
        
        print(f"Starting RSDT mining with {self.threads} threads...")
        print(f"Wallet: {self.wallet_address}")
        print(f"Worker: {self.worker_name}")
        print(f"Pool: {self.pool_url}")
        print("-" * 60)
        
        # Start mining threads
        for i in range(self.threads):
            thread = threading.Thread(target=self.mining_thread, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Start stats thread
        stats_thread = threading.Thread(target=self.stats_thread)
        stats_thread.daemon = True
        stats_thread.start()
        
        try:
            # Keep main thread alive
            while self.mining_active:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping miner...")
            self.stop_mining()
    
    def stop_mining(self):
        """Stop mining"""
        self.mining_active = False

def print_banner():
    print("""
██████╗ ███████╗██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
██████╔╝███████╗██║  ██║   ██║   
██╔══██╗╚════██║██║  ██║   ██║   
██║  ██║███████║██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝   

    RESISTANCE BLOCKCHAIN MINER
    Linux Edition v1.0
    
    Genesis: "Censorship is control; privacy is resistance"
""")

def main():
    print_banner()
    
    pool_url = input("Enter pool URL (e.g., http://127.0.0.1:3333): ").strip()
    wallet_address = input("Enter wallet address: ").strip()
    worker_name = input("Enter worker name: ").strip()
    threads = int(input("Enter number of threads (default 1): ") or "1")
    
    miner = RSDTLinuxMiner(pool_url, wallet_address, worker_name, threads)
    
    if not miner.connect_to_pool():
        print("Failed to connect to pool. Exiting...")
        return 1
    
    print("Press Ctrl+C to stop mining...")
    miner.start_mining()
    
    return 0

if __name__ == "__main__":
    main()

