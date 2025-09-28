#!/usr/bin/env python3
# Copyright (c) 2025, The RSDT Project
# 
# All rights reserved.

import argparse
import time
import threading
import requests
import json
import hashlib
import struct
from typing import Optional, Dict, Any

class RSDTMiner:
    def __init__(self, address: str, pool_url: str, threads: int = 0):
        self.address = address
        self.pool_url = pool_url
        self.threads = threads or self._get_optimal_threads()
        self.is_mining = False
        self.current_job = None
        self.hashrate = 0
        self.shares_submitted = 0
        self.shares_accepted = 0
        
    def _get_optimal_threads(self) -> int:
        """Get optimal number of threads based on CPU cores"""
        import multiprocessing
        cores = multiprocessing.cpu_count()
        return max(1, cores - 1)  # Leave one core free
    
    def _get_work_from_pool(self) -> Optional[Dict[str, Any]]:
        """Get mining work from pool"""
        try:
            response = requests.post(f"{self.pool_url}/getwork", 
                                   json={"address": self.address}, 
                                   timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting work from pool: {e}")
        return None
    
    def _submit_work_to_pool(self, job_id: str, nonce: int, hash_result: str) -> bool:
        """Submit completed work to pool"""
        try:
            response = requests.post(f"{self.pool_url}/submitwork",
                                   json={
                                       "job_id": job_id,
                                       "nonce": nonce,
                                       "hash": hash_result,
                                       "address": self.address
                                   },
                                   timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result.get("accepted", False)
        except Exception as e:
            print(f"Error submitting work: {e}")
        return False
    
    def _mine_block(self, block_data: bytes, target: int) -> tuple:
        """Mine a block using RandomX algorithm"""
        # This is a simplified mining implementation
        # In production, you'd use the actual RandomX library
        
        nonce = 0
        start_time = time.time()
        
        while self.is_mining:
            # Create block with nonce
            block_with_nonce = block_data + struct.pack('<Q', nonce)
            
            # Calculate hash (simplified - use actual RandomX in production)
            hash_result = hashlib.sha256(block_with_nonce).hexdigest()
            hash_int = int(hash_result, 16)
            
            # Check if hash meets target
            if hash_int < target:
                return nonce, hash_result, time.time() - start_time
            
            nonce += 1
            
            # Update hashrate every 1000 attempts
            if nonce % 1000 == 0:
                elapsed = time.time() - start_time
                if elapsed > 0:
                    self.hashrate = nonce / elapsed
        
        return None, None, 0
    
    def _mining_worker(self, worker_id: int):
        """Mining worker thread"""
        print(f"Worker {worker_id} started")
        
        while self.is_mining:
            # Get work from pool
            job = self._get_work_from_pool()
            if not job:
                time.sleep(5)
                continue
            
            self.current_job = job
            block_data = bytes.fromhex(job['block_data'])
            target = int(job['target'], 16)
            
            # Mine the block
            nonce, hash_result, mining_time = self._mine_block(block_data, target)
            
            if nonce is not None and self.is_mining:
                # Submit work to pool
                accepted = self._submit_work_to_pool(job['job_id'], nonce, hash_result)
                
                self.shares_submitted += 1
                if accepted:
                    self.shares_accepted += 1
                    print(f"Share accepted! Nonce: {nonce}, Hash: {hash_result[:16]}...")
                else:
                    print(f"Share rejected. Nonce: {nonce}")
                
                # Calculate earnings (simplified)
                earnings = self.shares_accepted * 0.001  # 0.001 RSDT per share
                print(f"Earnings: {earnings:.6f} RSDT")
    
    def start_mining(self):
        """Start mining"""
        print(f"Starting RSDT miner...")
        print(f"Address: {self.address}")
        print(f"Pool: {self.pool_url}")
        print(f"Threads: {self.threads}")
        
        self.is_mining = True
        
        # Start worker threads
        threads = []
        for i in range(self.threads):
            thread = threading.Thread(target=self._mining_worker, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Status reporting thread
        status_thread = threading.Thread(target=self._status_reporter)
        status_thread.daemon = True
        status_thread.start()
        
        try:
            # Keep main thread alive
            while self.is_mining:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping miner...")
            self.stop_mining()
    
    def stop_mining(self):
        """Stop mining"""
        self.is_mining = False
        print("Miner stopped")
    
    def _status_reporter(self):
        """Report mining status"""
        while self.is_mining:
            time.sleep(30)  # Report every 30 seconds
            if self.is_mining:
                print(f"\n--- Mining Status ---")
                print(f"Hashrate: {self.hashrate:.2f} H/s")
                print(f"Shares submitted: {self.shares_submitted}")
                print(f"Shares accepted: {self.shares_accepted}")
                if self.shares_submitted > 0:
                    acceptance_rate = (self.shares_accepted / self.shares_submitted) * 100
                    print(f"Acceptance rate: {acceptance_rate:.2f}%")
                print(f"Earnings: {self.shares_accepted * 0.001:.6f} RSDT")
                print("-------------------\n")

def main():
    parser = argparse.ArgumentParser(description='RSDT Miner')
    parser.add_argument('--address', '-a', required=True, help='RSDT wallet address')
    parser.add_argument('--pool', '-p', default='http://pool.rsdt.network:18090', help='Mining pool URL')
    parser.add_argument('--threads', '-t', type=int, default=0, help='Number of mining threads (0 = auto)')
    parser.add_argument('--version', '-v', action='version', version='RSDT Miner v1.0.0')
    
    args = parser.parse_args()
    
    # Validate address format
    if not args.address.startswith('RSDT'):
        print("Error: Invalid RSDT address format")
        return 1
    
    # Create and start miner
    miner = RSDTMiner(args.address, args.pool, args.threads)
    
    try:
        miner.start_mining()
    except KeyboardInterrupt:
        miner.stop_mining()
    
    return 0

if __name__ == '__main__':
    exit(main())

