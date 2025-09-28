/**
 * Resistance Blockchain Production Explorer Backend
 * Enterprise-grade blockchain explorer API
 */

const express = require('express');
const mysql = require('mysql2/promise');
const axios = require('axios');
const cors = require('cors');

class RSDTProductionExplorer {
    constructor() {
        this.app = express();
        this.port = 3000;
        this.daemonUrl = 'http://127.0.0.1:18091'; // Mainnet
        
        this.premine_addresses = {
            "47SqxBdbhB5Afm4cXMrQE3eke3ghicJXUeGh2nx3V3LkQrrE3vjJznLFkor9Hyb4EFGoop61q4bteDMAd7FMC13hSQ78JHT": "RSDT_Liquidity (4.5M RSDT)",
            "482uYzU9pXdLDi6LrQR8NJFDThiR8JFvTh5xwAkbhmjNYPq4qTM3U8vQFom6RZ91zddQvKjngLNw5fwRntR2k4wxTveXxdJ": "RSDT_Development (3.75M RSDT)",
            "424EUrcR8VCJaThqNvagqwbL1hUZKeiLUaKfNiZ3ahCdP7PDozPsnm2PYBV97WAco1EKt9o1bG2964fpuBNQDY5aTX7xRhs": "RSDT_Marketing (3M RSDT)",
            "48Pp2yPq7icAKwK8APP2sgdTfF1tpGLiJhB2TKkbGZ5G5rrdzQKw2Qu1quV7Fk6u7ZWhuYNfzempcUYLqm1aJN75U3BAbKa": "RSDT_Team (2.25M RSDT)",
            "4AYi4wt22fkXZgx1cvoDEQhdZXgaRiVCFeE4XznFLucy7rTkhoHFqoDQrNWr1gnxT1AroBgVuThCv5cEdaByCxcgKYDY8SS": "RSDT_Treasury (1.5M RSDT)",
            "44ZE4bRNz28i6acpBKV4RoAua61uGLvGkgyN8zJ9h8eeLFLEHNTVXbDjC6YKQz6jwqZS4S1XcMvRwJrm2gCoSnm3BeywEun": "RSDT_Founder_Private (2.25M RSDT) ⭐"
        };
        
        this.setupDatabase();
        this.setupRoutes();
    }
    
    async setupDatabase() {
        this.db = await mysql.createConnection({
            host: 'localhost',
            user: 'rsdt_explorer',
            password: 'secure_password',
            database: 'rsdt_blockchain_explorer'
        });
        
        // Create tables
        await this.db.execute(`
            CREATE TABLE IF NOT EXISTS blocks (
                height BIGINT PRIMARY KEY,
                hash VARCHAR(64) UNIQUE NOT NULL,
                prev_hash VARCHAR(64),
                timestamp BIGINT,
                size INT,
                tx_count INT,
                reward DECIMAL(20,12),
                difficulty BIGINT,
                nonce BIGINT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_hash (hash),
                INDEX idx_timestamp (timestamp)
            )
        `);
        
        await this.db.execute(`
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tx_hash VARCHAR(64) UNIQUE NOT NULL,
                block_height BIGINT,
                timestamp BIGINT,
                size INT,
                fee DECIMAL(20,12),
                amount DECIMAL(20,12),
                ring_size INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_hash (tx_hash),
                INDEX idx_block (block_height),
                FOREIGN KEY (block_height) REFERENCES blocks(height)
            )
        `);
        
        await this.db.execute(`
            CREATE TABLE IF NOT EXISTS address_stats (
                address VARCHAR(100) PRIMARY KEY,
                balance DECIMAL(20,12) DEFAULT 0,
                tx_count INT DEFAULT 0,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                is_premine BOOLEAN DEFAULT FALSE,
                premine_label VARCHAR(200)
            )
        `);
    }
    
    setupRoutes() {
        this.app.use(cors());
        this.app.use(express.json());
        this.app.use(express.static('public'));
        
        // Blockchain statistics
        this.app.get('/api/stats', async (req, res) => {
            try {
                const daemonInfo = await this.getDaemonInfo();
                const [blockCount] = await this.db.execute('SELECT COUNT(*) as count FROM blocks');
                const [txCount] = await this.db.execute('SELECT COUNT(*) as count FROM transactions');
                const [recentBlocks] = await this.db.execute('SELECT * FROM blocks ORDER BY height DESC LIMIT 10');
                
                res.json({
                    height: daemonInfo.height,
                    difficulty: daemonInfo.difficulty,
                    hashrate: daemonInfo.difficulty / 120, // Estimate based on 120s block time
                    totalBlocks: blockCount[0].count,
                    totalTransactions: txCount[0].count,
                    totalSupply: '200000000', // 200M RSDT
                    circulatingSupply: this.calculateCirculatingSupply(daemonInfo.height),
                    recentBlocks: recentBlocks,
                    networkType: daemonInfo.testnet ? 'testnet' : 'mainnet'
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        
        // Block by height or hash
        this.app.get('/api/block/:id', async (req, res) => {
            try {
                const id = req.params.id;
                let block;
                
                if (isNaN(id)) {
                    // Search by hash
                    [block] = await this.db.execute('SELECT * FROM blocks WHERE hash = ?', [id]);
                } else {
                    // Search by height
                    [block] = await this.db.execute('SELECT * FROM blocks WHERE height = ?', [parseInt(id)]);
                }
                
                if (block.length === 0) {
                    // Fetch from daemon if not in database
                    block = await this.fetchBlockFromDaemon(id);
                    if (block) {
                        await this.storeBlock(block);
                    }
                } else {
                    block = block[0];
                }
                
                if (!block) {
                    return res.status(404).json({ error: 'Block not found' });
                }
                
                // Get transactions in block
                const [transactions] = await this.db.execute('SELECT * FROM transactions WHERE block_height = ?', [block.height]);
                
                res.json({
                    ...block,
                    transactions
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        
        // Transaction by hash
        this.app.get('/api/tx/:hash', async (req, res) => {
            try {
                const [tx] = await this.db.execute('SELECT * FROM transactions WHERE tx_hash = ?', [req.params.hash]);
                
                if (tx.length === 0) {
                    return res.status(404).json({ error: 'Transaction not found' });
                }
                
                res.json(tx[0]);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        
        // Address information
        this.app.get('/api/address/:address', async (req, res) => {
            try {
                const address = req.params.address;
                const [addressInfo] = await this.db.execute('SELECT * FROM address_stats WHERE address = ?', [address]);
                
                // Check if it's a premine address
                const premineLabel = this.premine_addresses[address] || null;
                
                res.json({
                    address,
                    balance: addressInfo[0]?.balance || 0,
                    txCount: addressInfo[0]?.tx_count || 0,
                    isPremine: !!premineLabel,
                    premineLabel,
                    firstSeen: addressInfo[0]?.first_seen,
                    lastSeen: addressInfo[0]?.last_seen
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        
        // Search endpoint
        this.app.get('/api/search/:query', async (req, res) => {
            try {
                const query = req.params.query;
                let results = [];
                
                // Check if it's a block height
                if (!isNaN(query)) {
                    const [block] = await this.db.execute('SELECT * FROM blocks WHERE height = ?', [parseInt(query)]);
                    if (block.length > 0) {
                        results.push({ type: 'block', data: block[0] });
                    }
                }
                
                // Check if it's a block hash
                const [blockByHash] = await this.db.execute('SELECT * FROM blocks WHERE hash LIKE ?', [`${query}%`]);
                results = results.concat(blockByHash.map(b => ({ type: 'block', data: b })));
                
                // Check if it's a transaction hash
                const [txByHash] = await this.db.execute('SELECT * FROM transactions WHERE tx_hash LIKE ?', [`${query}%`]);
                results = results.concat(txByHash.map(t => ({ type: 'transaction', data: t })));
                
                // Check if it's an address
                if (query.length > 50) {
                    const addressInfo = await this.getAddressInfo(query);
                    if (addressInfo) {
                        results.push({ type: 'address', data: addressInfo });
                    }
                }
                
                res.json(results.slice(0, 10)); // Limit to 10 results
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        
        // Recent blocks
        this.app.get('/api/blocks', async (req, res) => {
            try {
                const page = parseInt(req.query.page) || 1;
                const limit = parseInt(req.query.limit) || 20;
                const offset = (page - 1) * limit;
                
                const [blocks] = await this.db.execute('SELECT * FROM blocks ORDER BY height DESC LIMIT ? OFFSET ?', [limit, offset]);
                const [total] = await this.db.execute('SELECT COUNT(*) as count FROM blocks');
                
                res.json({
                    blocks,
                    pagination: {
                        page,
                        limit,
                        total: total[0].count,
                        pages: Math.ceil(total[0].count / limit)
                    }
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        
        // Recent transactions
        this.app.get('/api/transactions', async (req, res) => {
            try {
                const page = parseInt(req.query.page) || 1;
                const limit = parseInt(req.query.limit) || 20;
                const offset = (page - 1) * limit;
                
                const [transactions] = await this.db.execute('SELECT * FROM transactions ORDER BY timestamp DESC LIMIT ? OFFSET ?', [limit, offset]);
                const [total] = await this.db.execute('SELECT COUNT(*) as count FROM transactions');
                
                res.json({
                    transactions,
                    pagination: {
                        page,
                        limit,
                        total: total[0].count,
                        pages: Math.ceil(total[0].count / limit)
                    }
                });
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        
        // Premine addresses
        this.app.get('/api/premine', (req, res) => {
            const premineAddresses = Object.entries(this.premine_addresses).map(([address, label]) => ({
                address,
                label,
                allocation: this.extractAllocation(label)
            }));
            
            res.json({
                totalPremine: '20000000', // 20M RSDT
                addresses: premineAddresses
            });
        });
    }
    
    async getDaemonInfo() {
        try {
            const response = await axios.post(`${this.daemonUrl}/json_rpc`, {
                jsonrpc: '2.0',
                id: '0',
                method: 'get_info'
            });
            return response.data.result;
        } catch (error) {
            throw new Error('Failed to connect to daemon');
        }
    }
    
    async fetchBlockFromDaemon(heightOrHash) {
        try {
            const response = await axios.post(`${this.daemonUrl}/json_rpc`, {
                jsonrpc: '2.0',
                id: '0',
                method: 'get_block',
                params: isNaN(heightOrHash) ? { hash: heightOrHash } : { height: parseInt(heightOrHash) }
            });
            return response.data.result;
        } catch (error) {
            return null;
        }
    }
    
    async storeBlock(blockData) {
        await this.db.execute(`
            INSERT IGNORE INTO blocks (height, hash, prev_hash, timestamp, size, tx_count, reward, difficulty, nonce)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        `, [
            blockData.block_header.height,
            blockData.block_header.hash,
            blockData.block_header.prev_hash,
            blockData.block_header.timestamp,
            blockData.block_header.block_size,
            blockData.block_header.num_txes,
            blockData.block_header.reward / 1e12, // Convert from atomic units
            blockData.block_header.difficulty,
            blockData.block_header.nonce
        ]);
    }
    
    calculateCirculatingSupply(height) {
        // Calculate based on block rewards and premine
        const premine = 20000000; // 20M RSDT
        const blockReward = 50; // Initial 50 RSDT per block
        const halvingInterval = 2102400; // Every 2.1M blocks
        
        let totalMined = 0;
        let currentHeight = 1; // Start from block 1 (after genesis)
        let currentReward = blockReward;
        
        while (currentHeight <= height) {
            const blocksUntilHalving = Math.min(halvingInterval, height - currentHeight + 1);
            totalMined += blocksUntilHalving * currentReward;
            currentHeight += blocksUntilHalving;
            currentReward /= 2;
            
            if (currentReward < 0.5) {
                currentReward = 0.5; // Tail emission
            }
        }
        
        return premine + totalMined;
    }
    
    extractAllocation(label) {
        const match = label.match(/\(([\d.]+M)\s+RSDT\)/);
        return match ? match[1] : '0';
    }
    
    async syncWithDaemon() {
        try {
            const daemonInfo = await this.getDaemonInfo();
            const [lastBlock] = await this.db.execute('SELECT MAX(height) as height FROM blocks');
            const lastHeight = lastBlock[0].height || 0;
            
            // Sync missing blocks
            for (let height = lastHeight + 1; height <= daemonInfo.height; height++) {
                const block = await this.fetchBlockFromDaemon(height);
                if (block) {
                    await this.storeBlock(block);
                }
            }
            
            console.log(`Synced to block ${daemonInfo.height}`);
        } catch (error) {
            console.error('Sync failed:', error);
        }
    }
    
    async start() {
        this.app.listen(this.port, () => {
            console.log(`🌐 RSDT Production Explorer API started on port ${this.port}`);
            console.log(`📊 API: http://localhost:${this.port}/api/stats`);
        });
        
        // Start blockchain sync
        setInterval(() => this.syncWithDaemon(), 30000); // Every 30 seconds
        
        console.log('🔍 Blockchain explorer ready for production!');
    }
}

// Start the explorer
const explorer = new RSDTProductionExplorer();
explorer.start();

module.exports = RSDTProductionExplorer;
