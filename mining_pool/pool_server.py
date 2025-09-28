#!/usr/bin/env python3
# Copyright (c) 2025, The RSDT Project
# 
# All rights reserved.

import asyncio
import json
import time
import hashlib
import struct
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from aiohttp import web, ClientSession
import aiohttp_cors

@dataclass
class MiningJob:
    job_id: str
    block_data: str
    target: str
    timestamp: float
    miner_address: str

@dataclass
class Miner:
    address: str
    hashrate: float
    shares_submitted: int
    shares_accepted: int
    last_seen: float
    connection_id: str

class RSDTMiningPool:
    def __init__(self, pool_fee: float = 0.01):
        self.pool_fee = pool_fee  # 1% pool fee
        self.miners: Dict[str, Miner] = {}
        self.current_jobs: Dict[str, MiningJob] = {}
        self.block_height = 0
        self.pool_balance = 0.0
        
    def _generate_job_id(self) -> str:
        """Generate unique job ID"""
        return hashlib.sha256(f"{time.time()}{len(self.current_jobs)}".encode()).hexdigest()[:16]
    
    def _generate_block_data(self) -> str:
        """Generate block data for mining"""
        # Simplified block data generation
        # In production, this would get real block data from the blockchain
        block_data = {
            "height": self.block_height,
            "timestamp": int(time.time()),
            "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "merkle_root": hashlib.sha256(f"block_{self.block_height}".encode()).hexdigest()
        }
        return json.dumps(block_data)
    
    def _calculate_target(self, difficulty: int) -> str:
        """Calculate mining target based on difficulty"""
        # Simplified target calculation
        target = (2 ** 256) // difficulty
        return hex(target)[2:].zfill(64)
    
    async def get_work(self, request):
        """Handle getwork requests from miners"""
        data = await request.json()
        miner_address = data.get('address')
        
        if not miner_address:
            return web.json_response({"error": "Address required"}, status=400)
        
        # Register or update miner
        if miner_address not in self.miners:
            self.miners[miner_address] = Miner(
                address=miner_address,
                hashrate=0.0,
                shares_submitted=0,
                shares_accepted=0,
                last_seen=time.time(),
                connection_id=request.remote
            )
        else:
            self.miners[miner_address].last_seen = time.time()
        
        # Generate new job
        job_id = self._generate_job_id()
        block_data = self._generate_block_data()
        target = self._calculate_target(1000000)  # Simplified difficulty
        
        job = MiningJob(
            job_id=job_id,
            block_data=block_data,
            target=target,
            timestamp=time.time(),
            miner_address=miner_address
        )
        
        self.current_jobs[job_id] = job
        
        return web.json_response({
            "job_id": job_id,
            "block_data": block_data,
            "target": target,
            "difficulty": 1000000
        })
    
    async def submit_work(self, request):
        """Handle work submission from miners"""
        data = await request.json()
        job_id = data.get('job_id')
        nonce = data.get('nonce')
        hash_result = data.get('hash')
        miner_address = data.get('address')
        
        if not all([job_id, nonce, hash_result, miner_address]):
            return web.json_response({"error": "Missing required fields"}, status=400)
        
        # Validate job exists
        if job_id not in self.current_jobs:
            return web.json_response({"error": "Invalid job ID"}, status=400)
        
        job = self.current_jobs[job_id]
        
        # Validate miner
        if miner_address not in self.miners:
            return web.json_response({"error": "Unknown miner"}, status=400)
        
        miner = self.miners[miner_address]
        
        # Validate work (simplified)
        block_data = job.block_data
        target = int(job.target, 16)
        
        # Recreate hash
        block_with_nonce = block_data + str(nonce)
        calculated_hash = hashlib.sha256(block_with_nonce.encode()).hexdigest()
        hash_int = int(calculated_hash, 16)
        
        # Check if work is valid
        if hash_int < target:
            miner.shares_accepted += 1
            miner.shares_submitted += 1
            
            # Calculate reward (simplified)
            reward = 0.001  # 0.001 RSDT per share
            self.pool_balance += reward
            
            # Remove completed job
            del self.current_jobs[job_id]
            
            return web.json_response({
                "accepted": True,
                "reward": reward,
                "message": "Share accepted!"
            })
        else:
            miner.shares_submitted += 1
            return web.json_response({
                "accepted": False,
                "message": "Share rejected - does not meet target"
            })
    
    async def get_stats(self, request):
        """Get pool statistics"""
        total_miners = len(self.miners)
        total_hashrate = sum(miner.hashrate for miner in self.miners.values())
        total_shares = sum(miner.shares_submitted for miner in self.miners.values())
        accepted_shares = sum(miner.shares_accepted for miner in self.miners.values())
        
        return web.json_response({
            "pool_name": "RSDT Mining Pool",
            "total_miners": total_miners,
            "total_hashrate": total_hashrate,
            "total_shares": total_shares,
            "accepted_shares": accepted_shares,
            "acceptance_rate": (accepted_shares / total_shares * 100) if total_shares > 0 else 0,
            "pool_balance": self.pool_balance,
            "pool_fee": self.pool_fee,
            "current_height": self.block_height
        })
    
    async def get_miner_stats(self, request):
        """Get individual miner statistics"""
        miner_address = request.match_info.get('address')
        
        if miner_address not in self.miners:
            return web.json_response({"error": "Miner not found"}, status=404)
        
        miner = self.miners[miner_address]
        
        return web.json_response({
            "address": miner.address,
            "hashrate": miner.hashrate,
            "shares_submitted": miner.shares_submitted,
            "shares_accepted": miner.shares_accepted,
            "acceptance_rate": (miner.shares_accepted / miner.shares_submitted * 100) if miner.shares_submitted > 0 else 0,
            "last_seen": miner.last_seen,
            "estimated_earnings": miner.shares_accepted * 0.001
        })

def create_app():
    """Create web application"""
    app = web.Application()
    
    # Create pool instance
    pool = RSDTMiningPool()
    
    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Add routes
    app.router.add_post('/getwork', pool.get_work)
    app.router.add_post('/submitwork', pool.submit_work)
    app.router.add_get('/stats', pool.get_stats)
    app.router.add_get('/miner/{address}', pool.get_miner_stats)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

async def main():
    """Main function"""
    app = create_app()
    
    # Start web server
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', 18090)
    await site.start()
    
    print("RSDT Mining Pool started on http://0.0.0.0:18090")
    print("API endpoints:")
    print("  POST /getwork - Get mining work")
    print("  POST /submitwork - Submit completed work")
    print("  GET /stats - Get pool statistics")
    print("  GET /miner/{address} - Get miner statistics")
    
    # Keep server running
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        print("Shutting down pool...")
        await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())

