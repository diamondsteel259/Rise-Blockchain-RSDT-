#!/usr/bin/env python3
"""
Resistance Blockchain Explorer
Web-based blockchain explorer for RSDT
"""

import asyncio
import aiohttp
import json
from aiohttp import web
import time
from typing import Dict, List, Optional

class RSDTExplorer:
    def __init__(self, daemon_url: str = "http://127.0.0.1:28091"):
        self.daemon_url = daemon_url
        self.premine_addresses = {
            "47SqxBdbhB5Afm4cXMrQE3eke3ghicJXUeGh2nx3V3LkQrrE3vjJznLFkor9Hyb4EFGoop61q4bteDMAd7FMC13hSQ78JHT": "RSDT_Liquidity (4.5M RSDT)",
            "482uYzU9pXdLDi6LrQR8NJFDThiR8JFvTh5xwAkbhmjNYPq4qTM3U8vQFom6RZ91zddQvKjngLNw5fwRntR2k4wxTveXxdJ": "RSDT_Development (3.75M RSDT)",
            "424EUrcR8VCJaThqNvagqwbL1hUZKeiLUaKfNiZ3ahCdP7PDozPsnm2PYBV97WAco1EKt9o1bG2964fpuBNQDY5aTX7xRhs": "RSDT_Marketing (3M RSDT)",
            "48Pp2yPq7icAKwK8APP2sgdTfF1tpGLiJhB2TKkbGZ5G5rrdzQKw2Qu1quV7Fk6u7ZWhuYNfzempcUYLqm1aJN75U3BAbKa": "RSDT_Team (2.25M RSDT)",
            "4AYi4wt22fkXZgx1cvoDEQhdZXgaRiVCFeE4XznFLucy7rTkhoHFqoDQrNWr1gnxT1AroBgVuThCv5cEdaByCxcgKYDY8SS": "RSDT_Treasury (1.5M RSDT)",
            "44ZE4bRNz28i6acpBKV4RoAua61uGLvGkgyN8zJ9h8eeLFLEHNTVXbDjC6YKQz6jwqZS4S1XcMvRwJrm2gCoSnm3BeywEun": "RSDT_Founder_Private (2.25M RSDT) ⭐"
        }
    
    async def get_blockchain_info(self) -> Dict:
        """Get blockchain information from daemon"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.daemon_url}/json_rpc",
                json={"jsonrpc": "2.0", "id": "0", "method": "get_info"}
            ) as response:
                data = await response.json()
                return data.get("result", {})
    
    async def get_block(self, height: int) -> Dict:
        """Get block information by height"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.daemon_url}/json_rpc",
                json={
                    "jsonrpc": "2.0", 
                    "id": "0", 
                    "method": "get_block",
                    "params": {"height": height}
                }
            ) as response:
                data = await response.json()
                return data.get("result", {})
    
    def format_address(self, address: str) -> str:
        """Format address with premine tagging"""
        if address in self.premine_addresses:
            return f"{address} ({self.premine_addresses[address]})"
        return address
    
    def create_html_page(self, title: str, content: str) -> str:
        """Create HTML page with Resistance theme"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Resistance Blockchain Explorer</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background: #1a1a1a;
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #00ff00;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #ff0000;
            text-shadow: 2px 2px 4px #000;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: #2a2a2a;
            border: 1px solid #00ff00;
            padding: 20px;
            border-radius: 5px;
        }}
        .stat-card h3 {{
            color: #ffff00;
            margin-top: 0;
        }}
        .premine-address {{
            background: #2a2a2a;
            border: 1px solid #ff0000;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .premine-address .label {{
            color: #ffff00;
            font-weight: bold;
        }}
        .address {{
            font-family: monospace;
            word-break: break-all;
            color: #00ffff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>��️ RESISTANCE BLOCKCHAIN EXPLORER</h1>
            <p>Privacy is Resistance | Censorship is Control</p>
        </div>
        {content}
    </div>
</body>
</html>
        """
    
    async def home_handler(self, request):
        """Home page handler"""
        info = await self.get_blockchain_info()
        
        # Get genesis block
        genesis = await self.get_block(0)
        
        content = f"""
        <div class="stats">
            <div class="stat-card">
                <h3>�� Blockchain Stats</h3>
                <p><strong>Height:</strong> {info.get('height', 'N/A')}</p>
                <p><strong>Difficulty:</strong> {info.get('difficulty', 'N/A')}</p>
                <p><strong>Status:</strong> {info.get('status', 'N/A')}</p>
            </div>
            <div class="stat-card">
                <h3>💰 Genesis Block</h3>
                <p><strong>Reward:</strong> {genesis.get('block_header', {}).get('reward', 'N/A')} atomic units</p>
                <p><strong>Hash:</strong> {genesis.get('block_header', {}).get('hash', 'N/A')[:16]}...</p>
            </div>
            <div class="stat-card">
                <h3>🛡️ Resistance Protocol</h3>
                <p><strong>Total Supply:</strong> 200M RSDT</p>
                <p><strong>Premine:</strong> 20M RSDT (10%)</p>
                <p><strong>Block Time:</strong> 120 seconds</p>
            </div>
        </div>
        
        <h2>🏦 Premine Wallets</h2>
        """
        
        for address, label in self.premine_addresses.items():
            content += f"""
            <div class="premine-address">
                <div class="label">{label}</div>
                <div class="address">{address}</div>
            </div>
            """
        
        return web.Response(text=self.create_html_page("Home", content), content_type='text/html')
    
    async def start_explorer(self):
        """Start the blockchain explorer web server"""
        app = web.Application()
        app.router.add_get('/', self.home_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', 8080)
        
        print("🌐 Resistance Blockchain Explorer Starting...")
        print("🔗 URL: http://127.0.0.1:8080")
        print("🛡️ Privacy is Resistance!")
        
        await site.start()
        
        # Keep running
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            print("\n🛑 Explorer stopped")

if __name__ == "__main__":
    explorer = RSDTExplorer()
    asyncio.run(explorer.start_explorer())
