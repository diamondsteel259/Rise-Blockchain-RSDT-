#!/usr/bin/env python3
"""
RSDT Resistance Blockchain Website
Official website for RSDT - Fighting Financial Oppression
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return render_template('website_home.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('website_about.html')

@app.route('/tokenomics')
def tokenomics():
    """Tokenomics page"""
    return render_template('website_tokenomics.html')

@app.route('/mining')
def mining():
    """Mining page"""
    return render_template('website_mining.html')

@app.route('/downloads')
def downloads():
    """Downloads page"""
    return render_template('website_downloads.html')

@app.route('/explorer')
def explorer():
    """Blockchain explorer redirect"""
    return render_template('website_explorer.html')

@app.route('/api/stats')
def api_stats():
    """API endpoint for blockchain stats"""
    try:
        import requests
        response = requests.post("http://127.0.0.1:18081/json_rpc", 
                               json={"jsonrpc": "2.0", "id": "0", "method": "get_info"}, 
                               timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                return jsonify({
                    "height": data["result"].get("height", 0),
                    "difficulty": data["result"].get("difficulty", 0),
                    "network_hash_rate": data["result"].get("network_hash_rate", 0),
                    "status": data["result"].get("status", "Unknown")
                })
    except:
        pass
    
    return jsonify({
        "height": 0,
        "difficulty": 0,
        "network_hash_rate": 0,
        "status": "Offline"
    })

if __name__ == '__main__':
    print("🌐 Starting RSDT Resistance Blockchain Website...")
    print("📱 Website will be available at: http://localhost:8080")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
