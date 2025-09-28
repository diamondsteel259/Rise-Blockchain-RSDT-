#!/usr/bin/env python3
"""
RSDT Blockchain Explorer
A web-based blockchain explorer for RSDT Resistance Blockchain
"""

import json
import requests
from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# RSDT Daemon RPC endpoint
DAEMON_RPC = "http://127.0.0.1:18081/json_rpc"

class RSDTExplorer:
    def __init__(self):
        self.daemon_rpc = DAEMON_RPC
        self.setup_database()
    
    def setup_database(self):
        """Setup SQLite database for caching"""
        conn = sqlite3.connect('rsdt_explorer.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                height INTEGER PRIMARY KEY,
                hash TEXT UNIQUE,
                timestamp INTEGER,
                size INTEGER,
                difficulty INTEGER,
                nonce INTEGER,
                tx_count INTEGER,
                reward REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                tx_hash TEXT PRIMARY KEY,
                block_height INTEGER,
                timestamp INTEGER,
                size INTEGER,
                fee REAL,
                inputs INTEGER,
                outputs INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def rpc_call(self, method, params=None):
        """Make RPC call to RSDT daemon"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "0",
                "method": method
            }
            if params:
                payload["params"] = params
            
            response = requests.post(self.daemon_rpc, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"RPC Error: {e}")
            return None
    
    def get_blockchain_info(self):
        """Get blockchain information"""
        result = self.rpc_call("get_info")
        if result and "result" in result:
            return result["result"]
        return None
    
    def get_block(self, height):
        """Get block by height"""
        result = self.rpc_call("get_block", {"height": height})
        if result and "result" in result:
            return result["result"]
        return None
    
    def get_transaction(self, tx_hash):
        """Get transaction by hash"""
        result = self.rpc_call("get_transactions", {"txs_hashes": [tx_hash]})
        if result and "result" in result:
            return result["result"]
        return None

explorer = RSDTExplorer()

@app.route('/')
def index():
    """Main page"""
    info = explorer.get_blockchain_info()
    if not info:
        return "Error: Cannot connect to RSDT daemon", 500
    
    return render_template('index.html', 
                         height=info.get('height', 0),
                         difficulty=info.get('difficulty', 0),
                         network_hash_rate=info.get('network_hash_rate', 0),
                         status=info.get('status', 'Unknown'))

@app.route('/api/block/<int:height>')
def api_block(height):
    """API endpoint for block data"""
    block = explorer.get_block(height)
    if block:
        return jsonify(block)
    return jsonify({"error": "Block not found"}), 404

@app.route('/api/transaction/<tx_hash>')
def api_transaction(tx_hash):
    """API endpoint for transaction data"""
    tx = explorer.get_transaction(tx_hash)
    if tx:
        return jsonify(tx)
    return jsonify({"error": "Transaction not found"}), 404

@app.route('/api/blockchain')
def api_blockchain():
    """API endpoint for blockchain info"""
    info = explorer.get_blockchain_info()
    if info:
        return jsonify(info)
    return jsonify({"error": "Cannot get blockchain info"}), 500

@app.route('/block/<int:height>')
def block_page(height):
    """Block detail page"""
    block = explorer.get_block(height)
    if not block:
        return "Block not found", 404
    
    return render_template('block.html', block=block, height=height)

@app.route('/transaction/<tx_hash>')
def transaction_page(tx_hash):
    """Transaction detail page"""
    tx = explorer.get_transaction(tx_hash)
    if not tx:
        return "Transaction not found", 404
    
    return render_template('transaction.html', transaction=tx, tx_hash=tx_hash)

if __name__ == '__main__':
    print("🚀 Starting RSDT Blockchain Explorer...")
    print("📊 Explorer will be available at: http://localhost:5000")
    print("🔗 Make sure RSDT daemon is running on port 18081")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
