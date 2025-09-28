#!/usr/bin/env python3
# Copyright (c) 2025, The RSDT Project
# 
# All rights reserved.

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from aiohttp import web, ClientSession
import aiohttp_cors

@dataclass
class Block:
    height: int
    hash: str
    timestamp: int
    difficulty: int
    nonce: int
    miner_address: str
    reward: float
    fees: float
    transaction_count: int
    size: int

@dataclass
class Transaction:
    tx_id: str
    block_height: int
    timestamp: int
    fee: float
    inputs: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    size: int

@dataclass
class Address:
    address: str
    balance: float
    transaction_count: int
    first_seen: int
    last_seen: int
    is_premine: bool
    premine_category: Optional[str]

class RSDTExplorer:
    def __init__(self):
        self.blocks: Dict[int, Block] = {}
        self.transactions: Dict[str, Transaction] = {}
        self.addresses: Dict[str, Address] = {}
        self.premine_addresses = {
            "RSDT_Liquidity_1": "Liquidity",
            "RSDT_Development_1": "Development", 
            "RSDT_Marketing_1": "Marketing",
            "RSDT_Team_1": "Team",
            "RSDT_Treasury_1": "Treasury",
            "RSDT_Founder_Private": "Founder ⭐"
        }
        
    def _is_premine_address(self, address: str) -> bool:
        """Check if address is a premine address"""
        return address in self.premine_addresses
    
    def _get_premine_category(self, address: str) -> Optional[str]:
        """Get premine category for address"""
        return self.premine_addresses.get(address)
    
    async def get_latest_blocks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get latest blocks"""
        # In production, this would query the actual blockchain
        # For now, return mock data
        blocks = []
        for i in range(limit):
            block = Block(
                height=1000 - i,
                hash=f"block_hash_{1000 - i}",
                timestamp=int(time.time()) - (i * 120),  # 120s block time
                difficulty=1000000,
                nonce=12345 + i,
                miner_address="RSDT_Miner_1",
                reward=50.0 - (i * 0.1),
                fees=0.5,
                transaction_count=10 + i,
                size=1024 + (i * 100)
            )
            blocks.append(asdict(block))
        return blocks
    
    async def get_block(self, height: int) -> Optional[Dict[str, Any]]:
        """Get block by height"""
        if height in self.blocks:
            return asdict(self.blocks[height])
        
        # Mock block data
        block = Block(
            height=height,
            hash=f"block_hash_{height}",
            timestamp=int(time.time()) - ((1000 - height) * 120),
            difficulty=1000000,
            nonce=12345,
            miner_address="RSDT_Miner_1",
            reward=50.0,
            fees=0.5,
            transaction_count=15,
            size=2048
        )
        return asdict(block)
    
    async def get_transaction(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """Get transaction by ID"""
        if tx_id in self.transactions:
            return asdict(self.transactions[tx_id])
        
        # Mock transaction data
        tx = Transaction(
            tx_id=tx_id,
            block_height=1000,
            timestamp=int(time.time()),
            fee=0.001,
            inputs=[{"address": "RSDT_Input_1", "amount": 10.0}],
            outputs=[{"address": "RSDT_Output_1", "amount": 9.999}],
            size=512
        )
        return asdict(tx)
    
    async def get_address(self, address: str) -> Optional[Dict[str, Any]]:
        """Get address information"""
        if address in self.addresses:
            addr = self.addresses[address]
            result = asdict(addr)
            result["is_premine"] = self._is_premine_address(address)
            result["premine_category"] = self._get_premine_category(address)
            return result
        
        # Mock address data
        addr = Address(
            address=address,
            balance=100.0,
            transaction_count=25,
            first_seen=int(time.time()) - 86400,
            last_seen=int(time.time()),
            is_premine=self._is_premine_address(address),
            premine_category=self._get_premine_category(address)
        )
        return asdict(addr)
    
    async def search(self, query: str) -> Dict[str, Any]:
        """Search for blocks, transactions, or addresses"""
        results = {
            "blocks": [],
            "transactions": [],
            "addresses": []
        }
        
        # Simple search logic
        if query.isdigit():
            # Search by block height
            height = int(query)
            block = await self.get_block(height)
            if block:
                results["blocks"].append(block)
        elif query.startswith("RSDT"):
            # Search by address
            addr = await self.get_address(query)
            if addr:
                results["addresses"].append(addr)
        else:
            # Search by transaction ID
            tx = await self.get_transaction(query)
            if tx:
                results["transactions"].append(tx)
        
        return results

def create_app():
    """Create web application"""
    app = web.Application()
    
    # Create explorer instance
    explorer = RSDTExplorer()
    
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
    app.router.add_get('/api/blocks/latest', explorer.get_latest_blocks)
    app.router.add_get('/api/blocks/{height}', explorer.get_block)
    app.router.add_get('/api/transactions/{tx_id}', explorer.get_transaction)
    app.router.add_get('/api/addresses/{address}', explorer.get_address)
    app.router.add_get('/api/search/{query}', explorer.search)
    
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
    
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    print("RSDT Blockchain Explorer started on http://0.0.0.0:8080")
    print("API endpoints:")
    print("  GET /api/blocks/latest - Get latest blocks")
    print("  GET /api/blocks/{height} - Get block by height")
    print("  GET /api/transactions/{tx_id} - Get transaction by ID")
    print("  GET /api/addresses/{address} - Get address information")
    print("  GET /api/search/{query} - Search blocks, transactions, addresses")
    
    # Keep server running
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        print("Shutting down explorer...")
        await runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())

