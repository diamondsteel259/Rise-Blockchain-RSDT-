#!/usr/bin/env python3
"""
RSDT Mining Pool Server
Professional mining pool implementation for Resistance Blockchain
"""

import asyncio
import json
import logging
import time
import hashlib
import struct
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import aiohttp
import sqlite3
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rsdt_pool.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('RSDT_Pool')

@dataclass
class BlockTemplate:
    """Block template for mining"""
    height: int
    difficulty: int
    target: bytes
    block_header: bytes
    coinbase_tx: bytes
    merkle_root: bytes
    timestamp: int
    nonce: int = 0

@dataclass
class Miner:
    """Miner connection information"""
    address: str
    worker_name: str
    connection_time: float
    last_share_time: float
    shares_submitted: int = 0
    shares_accepted: int = 0
    hashrate: float = 0.0

class RSDTMiningPool:
    """RSDT Mining Pool Server"""
    
    def __init__(self, config_file: str = "pool_config.json"):
        self.config = self.load_config(config_file)
        self.miners: Dict[str, Miner] = {}
        self.current_block: Optional[BlockTemplate] = None
        self.daemon_url = self.config.get('daemon_url', 'http://127.0.0.1:18081')
        self.pool_fee = self.config.get('pool_fee', 1.0)  # 1% pool fee
        self.min_payout = self.config.get('min_payout', 0.1)  # Minimum payout in RSDT
        self.db_path = self.config.get('database', 'rsdt_pool.db')
        self.setup_database()
        
    def load_config(self, config_file: str) -> Dict:
        """Load pool configuration"""
        default_config = {
            "daemon_url": "http://127.0.0.1:18081",
            "pool_fee": 1.0,
            "min_payout": 0.1,
            "database": "rsdt_pool.db",
            "pool_address": "4A64wDfoaR6Lf1CGww4KanRZXbwrzXFFfE7wjtwvtZu8gVWEyYHzgbpAPiBra5UR5HCjcEFufBMZLRcHj3BCXLfuNf9Sn4N",
            "pool_port": 3333,
            "api_port": 8080
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
        except FileNotFoundError:
            logger.info(f"Config file {config_file} not found, using defaults")
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def setup_database(self):
        """Setup SQLite database for pool data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS miners (
                address TEXT PRIMARY KEY,
                worker_name TEXT,
                total_shares INTEGER DEFAULT 0,
                accepted_shares INTEGER DEFAULT 0,
                pending_balance REAL DEFAULT 0.0,
                total_paid REAL DEFAULT 0.0,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                miner_address TEXT,
                worker_name TEXT,
                share_data TEXT,
                difficulty INTEGER,
                is_valid BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (miner_address) REFERENCES miners (address)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                height INTEGER UNIQUE,
                hash TEXT,
                reward REAL,
                pool_fee REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database setup complete")
    
    async def get_block_template(self) -> Optional[BlockTemplate]:
        """Get current block template from daemon"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get blockchain info
                async with session.post(f"{self.daemon_url}/json_rpc", json={
                    "jsonrpc": "2.0",
                    "id": "0",
                    "method": "get_info"
                }) as response:
                    info = await response.json()
                
                # Get block template
                async with session.post(f"{self.daemon_url}/json_rpc", json={
                    "jsonrpc": "2.0",
                    "id": "0",
                    "method": "get_block_template",
                    "params": {
                        "wallet_address": self.config['pool_address'],
                        "reserve_size": 60
                    }
                }) as response:
                    template = await response.json()
                
                if 'result' in template:
                    result = template['result']
                    return BlockTemplate(
                        height=result['height'],
                        difficulty=result['difficulty'],
                        target=bytes.fromhex(result['target']),
                        block_header=bytes.fromhex(result['blocktemplate_blob']),
                        coinbase_tx=bytes.fromhex(result['coinbase_tx']),
                        merkle_root=bytes.fromhex(result['merkle_root']),
                        timestamp=int(time.time())
                    )
        except Exception as e:
            logger.error(f"Error getting block template: {e}")
        return None
    
    def validate_share(self, miner_address: str, nonce: int, block_template: BlockTemplate) -> bool:
        """Validate a mining share"""
        try:
            # Create block header with nonce
            header = block_template.block_header[:76] + struct.pack('<I', nonce)
            
            # Calculate hash
            hash_result = hashlib.sha256(hashlib.sha256(header).digest()).digest()
            
            # Check if hash meets difficulty
            hash_int = int.from_bytes(hash_result, 'little')
            target_int = int.from_bytes(block_template.target, 'little')
            
            return hash_int < target_int
        except Exception as e:
            logger.error(f"Error validating share: {e}")
            return False
    
    async def submit_share(self, miner_address: str, worker_name: str, nonce: int) -> bool:
        """Submit and validate a mining share"""
        if not self.current_block:
            return False
        
        # Validate share
        if not self.validate_share(miner_address, nonce, self.current_block):
            return False
        
        # Update miner stats
        miner_key = f"{miner_address}.{worker_name}"
        if miner_key not in self.miners:
            self.miners[miner_key] = Miner(
                address=miner_address,
                worker_name=worker_name,
                connection_time=time.time(),
                last_share_time=time.time()
            )
        
        miner = self.miners[miner_key]
        miner.shares_submitted += 1
        miner.shares_accepted += 1
        miner.last_share_time = time.time()
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO miners 
            (address, worker_name, total_shares, accepted_shares, last_seen)
            VALUES (?, ?, ?, ?, ?)
        ''', (miner_address, worker_name, miner.shares_submitted, miner.shares_accepted, datetime.now()))
        
        cursor.execute('''
            INSERT INTO shares 
            (miner_address, worker_name, share_data, difficulty, is_valid)
            VALUES (?, ?, ?, ?, ?)
        ''', (miner_address, worker_name, f"nonce:{nonce}", self.current_block.difficulty, True))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Valid share from {miner_address}.{worker_name}")
        return True
    
    async def handle_miner_connection(self, reader, writer):
        """Handle incoming miner connections"""
        addr = writer.get_extra_info('peername')
        logger.info(f"Miner connected from {addr}")
        
        try:
            while True:
                try:
                    data = await reader.readline()
                    if not data:
                        break
                    
                    try:
                        message = json.loads(data.decode().strip())
                        await self.process_miner_message(message, writer)
                    except json.JSONDecodeError:
                        await self.send_error(writer, "Invalid JSON")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        await self.send_error(writer, "Internal error")
                        
                except ConnectionResetError:
                    logger.info(f"Miner {addr} disconnected (connection reset)")
                    break
                except BrokenPipeError:
                    logger.info(f"Miner {addr} disconnected (broken pipe)")
                    break
        
        except Exception as e:
            logger.error(f"Connection error: {e}")
        finally:
            try:
                if not writer.is_closing():
                    writer.close()
                    await writer.wait_closed()
            except Exception:
                pass
            logger.info(f"Miner disconnected from {addr}")
    
    async def process_miner_message(self, message: Dict, writer):
        """Process messages from miners"""
        method = message.get('method')
        
        if method == 'login':
            await self.handle_login(message, writer)
        elif method == 'submit':
            await self.handle_submit(message, writer)
        elif method == 'getjob':
            await self.handle_getjob(message, writer)
        else:
            await self.send_error(writer, f"Unknown method: {method}")
    
    async def handle_login(self, message: Dict, writer):
        """Handle miner login"""
        params = message.get('params', {})
        address = params.get('login')
        worker = params.get('pass', 'default')
        
        if not address:
            await self.send_error(writer, "Missing login address")
            return
        
        # Send login success
        response = {
            "id": message.get('id'),
            "result": {
                "status": "OK",
                "job": await self.get_job_data()
            }
        }
        
        await self.send_response(writer, response)
        logger.info(f"Miner logged in: {address}.{worker}")
    
    async def handle_submit(self, message: Dict, writer):
        """Handle share submission"""
        params = message.get('params', {})
        address = params.get('login')
        worker = params.get('pass', 'default')
        nonce = params.get('nonce')
        
        if not all([address, nonce]):
            await self.send_error(writer, "Missing required parameters")
            return
        
        # Submit share
        success = await self.submit_share(address, worker, int(nonce))
        
        response = {
            "id": message.get('id'),
            "result": {
                "status": "OK" if success else "ERROR"
            }
        }
        
        await self.send_response(writer, response)
    
    async def handle_getjob(self, message: Dict, writer):
        """Handle job request"""
        response = {
            "id": message.get('id'),
            "result": await self.get_job_data()
        }
        
        await self.send_response(writer, response)
    
    async def get_job_data(self) -> Dict:
        """Get current job data for miners"""
        if not self.current_block:
            self.current_block = await self.get_block_template()
        
        if self.current_block:
            return {
                "job_id": f"job_{self.current_block.height}_{int(time.time())}",
                "blob": self.current_block.block_header.hex(),
                "target": self.current_block.target.hex(),
                "height": self.current_block.height,
                "difficulty": self.current_block.difficulty
            }
        else:
            return {"error": "No block template available"}
    
    async def send_response(self, writer, response: Dict):
        """Send response to miner"""
        try:
            data = json.dumps(response) + '\n'
            writer.write(data.encode())
            await writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            logger.info("Connection lost while sending response")
        except Exception as e:
            logger.error(f"Error sending response: {e}")
    
    async def send_error(self, writer, error: str):
        """Send error to miner"""
        response = {
            "error": error,
            "result": None
        }
        await self.send_response(writer, response)
    
    async def update_block_template(self):
        """Periodically update block template"""
        while True:
            try:
                new_template = await self.get_block_template()
                if new_template and (not self.current_block or new_template.height > self.current_block.height):
                    self.current_block = new_template
                    logger.info(f"Updated block template: height {new_template.height}")
            except Exception as e:
                logger.error(f"Error updating block template: {e}")
            
            await asyncio.sleep(30)  # Update every 30 seconds
    
    async def run_pool(self):
        """Run the mining pool server"""
        logger.info("Starting RSDT Mining Pool Server")
        
        # Start block template updater
        asyncio.create_task(self.update_block_template())
        
        # Start pool server
        server = await asyncio.start_server(
            self.handle_miner_connection,
            '0.0.0.0',
            self.config['pool_port']
        )
        
        logger.info(f"Pool server listening on port {self.config['pool_port']}")
        
        async with server:
            await server.serve_forever()

def main():
    """Main entry point"""
    pool = RSDTMiningPool()
    
    try:
        asyncio.run(pool.run_pool())
    except KeyboardInterrupt:
        logger.info("Pool server stopped by user")
    except Exception as e:
        logger.error(f"Pool server error: {e}")

if __name__ == "__main__":
    main()
