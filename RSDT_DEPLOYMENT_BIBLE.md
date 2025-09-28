# RSDT BLOCKCHAIN DEPLOYMENT BIBLE
## Complete Guide to Resistance Blockchain Deployment

---

## TABLE OF CONTENTS

1. [System Requirements](#1-system-requirements)
2. [Installation Guide](#2-installation-guide)
3. [Network Configuration](#3-network-configuration)
4. [Node Deployment](#4-node-deployment)
5. [Mining Setup](#5-mining-setup)
6. [Wallet Deployment](#6-wallet-deployment)
7. [Exchange Integration](#7-exchange-integration)
8. [Governance Setup](#8-governance-setup)
9. [Monitoring & Maintenance](#9-monitoring--maintenance)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. SYSTEM REQUIREMENTS

### 1.1 Minimum Requirements
- **CPU**: 4 cores, 2.0 GHz
- **RAM**: 8GB
- **Storage**: 100GB SSD
- **Network**: 10 Mbps upload/download
- **OS**: Ubuntu 20.04+, Windows 10+, macOS 10.15+

### 1.2 Recommended Requirements
- **CPU**: 8 cores, 3.0 GHz
- **RAM**: 16GB
- **Storage**: 500GB NVMe SSD
- **Network**: 100 Mbps upload/download
- **OS**: Ubuntu 22.04 LTS

### 1.3 Mining Requirements
- **CPU Mining**: 8+ cores, 3.0+ GHz
- **GPU Mining**: NVIDIA RTX 3060+ or AMD RX 6600+
- **RAM**: 16GB+
- **Storage**: 50GB SSD

---

## 2. INSTALLATION GUIDE

### 2.1 Linux Installation (Ubuntu/Debian)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y build-essential cmake git pkg-config libboost-all-dev \
    libssl-dev libzmq3-dev libunbound-dev libsodium-dev libminiupnpc-dev \
    libunwind8-dev liblzma-dev libreadline6-dev libldns-dev libexpat1-dev \
    libgtest-dev libhidapi-dev libusb-1.0-0-dev libprotobuf-dev protobuf-compiler \
    libudev-dev libboost-chrono-dev libboost-date-time-dev libboost-filesystem-dev \
    libboost-locale-dev libboost-program-options-dev libboost-regex-dev \
    libboost-serialization-dev libboost-system-dev libboost-thread-dev \
    python3 python3-dev python3-pip

# Clone repository
git clone https://github.com/resistance-blockchain/rsdt.git
cd rsdt

# Build from source
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Install
sudo make install
```

### 2.2 Windows Installation

```powershell
# Install Visual Studio 2019 or later with C++ tools
# Install vcpkg package manager
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install

# Install dependencies
.\vcpkg install boost-system boost-filesystem boost-thread boost-chrono boost-date-time boost-regex boost-serialization boost-program-options boost-locale boost-log boost-atomic boost-lockfree boost-timer boost-exception boost-random boost-graph boost-iostreams boost-math boost-wave boost-python boost-numpy boost-stacktrace boost-type-erasure boost-beast boost-process boost-dll boost-fiber boost-hana boost-heterogeneous boost-leaf boost-locale boost-mp11 boost-mysql boost-nowide boost-pfr boost-stacktrace boost-url boost-variant2 boost-wintls boost-yap openssl zeromq libsodium unbound miniupnpc hidapi protobuf

# Clone and build
git clone https://github.com/resistance-blockchain/rsdt.git
cd rsdt
mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=path/to/vcpkg/scripts/buildsystems/vcpkg.cmake
cmake --build . --config Release
```

### 2.3 macOS Installation

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install boost openssl zeromq libsodium unbound miniupnpc hidapi protobuf cmake

# Clone and build
git clone https://github.com/resistance-blockchain/rsdt.git
cd rsdt
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(sysctl -n hw.ncpu)

# Install
sudo make install
```

---

## 3. NETWORK CONFIGURATION

### 3.1 Network Parameters

```bash
# Mainnet Configuration
NETWORK_ID=0x1230F171610441611731008216A1A110
P2P_PORT=18080
RPC_PORT=18081
ZMQ_RPC_PORT=18082
BASE58_PREFIX=18

# Testnet Configuration
NETWORK_ID=0x1230F171610441611731008216A1A111
P2P_PORT=28080
RPC_PORT=28081
ZMQ_RPC_PORT=28082
BASE58_PREFIX=53

# Stagenet Configuration
NETWORK_ID=0x1230F171610441611731008216A1A112
P2P_PORT=38080
RPC_PORT=38081
ZMQ_RPC_PORT=38082
BASE58_PREFIX=24
```

### 3.2 Firewall Configuration

```bash
# Ubuntu/Debian
sudo ufw allow 18080/tcp  # P2P port
sudo ufw allow 18081/tcp  # RPC port
sudo ufw allow 18082/tcp  # ZMQ RPC port

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=18080/tcp
sudo firewall-cmd --permanent --add-port=18081/tcp
sudo firewall-cmd --permanent --add-port=18082/tcp
sudo firewall-cmd --reload
```

---

## 4. NODE DEPLOYMENT

### 4.1 Daemon Deployment

```bash
# Create daemon directory
mkdir -p ~/.rsdt
cd ~/.rsdt

# Create configuration file
cat > rsdt.conf << EOF
# RSDT Daemon Configuration
data-dir=/home/user/.rsdt
log-file=/home/user/.rsdt/rsdt.log
log-level=1
max-log-file-size=104857600
max-log-files=50
p2p-bind-ip=0.0.0.0
p2p-bind-port=18080
rpc-bind-ip=0.0.0.0
rpc-bind-port=18081
zmq-rpc-bind-ip=0.0.0.0
zmq-rpc-bind-port=18082
confirm-external-bind=1
restricted-rpc=1
no-igd=1
hide-my-port=0
db-sync-mode=fast:async:1000000
prep-blocks-threads=2
fast-block-sync=1
block-sync-size=50000
sync-pruned-blocks=1
max-txpool-weight=648000000
out-peers=12
in-peers=12
limit-rate-up=2048
limit-rate-down=8192
EOF

# Start daemon
rsdtd --config-file=rsdt.conf --detach
```

### 4.2 Systemd Service Setup

```bash
# Create systemd service file
sudo tee /etc/systemd/system/rsdtd.service > /dev/null << EOF
[Unit]
Description=RSDT Daemon
After=network.target

[Service]
Type=forking
User=rsdt
Group=rsdt
ExecStart=/usr/local/bin/rsdtd --config-file=/home/rsdt/.rsdt/rsdt.conf --detach
ExecStop=/usr/local/bin/rsdtd --config-file=/home/rsdt/.rsdt/rsdt.conf exit
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create user and start service
sudo useradd -r -s /bin/false rsdt
sudo systemctl daemon-reload
sudo systemctl enable rsdtd
sudo systemctl start rsdtd
```

---

## 5. MINING SETUP

### 5.1 Mining Pool Configuration

#### 5.1.1 Setting Up RSDT Mining Pool

The RSDT mining pool is a professional Python-based pool server that supports multiple miners and provides real-time statistics.

**Installation:**
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip sqlite3

# Install Python packages
pip3 install aiohttp requests

# Download and setup pool
cd /opt/rsdt
wget https://github.com/rsdt/pool/raw/main/rsdt_mining_pool.py
chmod +x rsdt_mining_pool.py
```

**Configuration:**
Create `pool_config.json`:
```json
{
    "daemon_url": "http://127.0.0.1:18081",
    "pool_fee": 1.0,
    "min_payout": 0.1,
    "database": "rsdt_pool.db",
    "pool_address": "4A64wDfoaR6Lf1CGww4KanRZXbwrzXFFfE7wjtwvtZu8gVWEyYHzgbpAPiBra5UR5HCjcEFufBMZLRcHj3BCXLfuNf9Sn4N",
    "pool_port": 3333,
    "api_port": 8080
}
```

**Starting the Pool:**
```bash
# Start pool server
nohup python3 rsdt_mining_pool.py > pool.log 2>&1 &

# Check status
ps aux | grep rsdt_mining_pool
tail -f pool.log
```

**Pool Management:**
```bash
# View pool statistics
sqlite3 rsdt_pool.db "SELECT * FROM miners;"

# View shares
sqlite3 rsdt_pool.db "SELECT * FROM shares ORDER BY timestamp DESC LIMIT 10;"

# View blocks
sqlite3 rsdt_pool.db "SELECT * FROM blocks ORDER BY height DESC LIMIT 10;"
```

#### 5.1.2 Connecting Miners to Pool

**Linux Miner:**
```bash
# Download Linux miner
wget https://github.com/rsdt/miners/raw/main/rsdt_linux_miner.py
chmod +x rsdt_linux_miner.py

# Run miner
python3 rsdt_linux_miner.py
# Enter pool URL: http://your-pool-ip:3333
# Enter wallet address: your-wallet-address
# Enter worker name: worker1
# Enter threads: 4
```

**Windows Miner:**
```cmd
# Download Windows miner
# Run rsdt_windows_miner.exe
# Configure:
# Pool URL: http://your-pool-ip:3333
# Wallet: your-wallet-address
# Worker: worker1
# Threads: 4
```

**Android Miner:**
1. Download RSDT Android Miner APK
2. Install on Android device
3. Configure:
   - Pool URL: http://your-pool-ip:3333
   - Wallet: your-wallet-address
   - Worker: android-worker
4. Start mining

#### 5.1.3 Pool Monitoring

**Real-time Statistics:**
```bash
# Monitor pool logs
tail -f pool.log

# Check active connections
netstat -an | grep :3333

# Monitor system resources
htop
```

**Pool Health Checks:**
```bash
# Check daemon connectivity
curl -s http://127.0.0.1:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}'

# Check pool database
sqlite3 rsdt_pool.db "SELECT COUNT(*) FROM miners;"

# Check recent activity
sqlite3 rsdt_pool.db "SELECT * FROM shares WHERE timestamp > datetime('now', '-1 hour');"
```

#### 5.1.4 Pool Troubleshooting

**Common Issues:**

1. **Pool not accepting connections:**
   ```bash
   # Check if port is open
   netstat -tlnp | grep :3333
   
   # Check firewall
   sudo ufw status
   sudo ufw allow 3333
   ```

2. **Miners can't connect:**
   ```bash
   # Check pool logs
   tail -20 pool.log
   
   # Restart pool
   pkill -f rsdt_mining_pool
   nohup python3 rsdt_mining_pool.py > pool.log 2>&1 &
   ```

3. **Database issues:**
   ```bash
   # Backup database
   cp rsdt_pool.db rsdt_pool.db.backup
   
   # Recreate database
   rm rsdt_pool.db
   python3 -c "from rsdt_mining_pool import RSDTMiningPool; RSDTMiningPool().setup_database()"
   ```

4. **High CPU usage:**
   ```bash
   # Monitor processes
   top -p $(pgrep -f rsdt_mining_pool)
   
   # Adjust pool settings in config
   # Reduce update frequency
   ```

### 5.2 CPU Mining

```bash
# Install mining software
git clone https://github.com/resistance-blockchain/rsdt-miner.git
cd rsdt-miner
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# Start mining
./rsdt-miner --daemon-address=127.0.0.1:18081 --address=YOUR_RSDT_ADDRESS --threads=8
```

### 5.2 GPU Mining

```bash
# NVIDIA GPU Mining
git clone https://github.com/resistance-blockchain/rsdt-gpu-miner.git
cd rsdt-gpu-miner
make CUDA_ARCH=75  # Adjust for your GPU architecture

# Start mining
./rsdt-gpu-miner --daemon=127.0.0.1:18081 --address=YOUR_RSDT_ADDRESS --intensity=1000
```

### 5.3 Mining Pool Setup

```bash
# Install pool software
git clone https://github.com/resistance-blockchain/rsdt-pool.git
cd rsdt-pool
npm install

# Configure pool
cp config.example.json config.json
# Edit config.json with your settings

# Start pool
npm start
```

---

## 6. WALLET DEPLOYMENT

### 6.1 Command Line Wallet

```bash
# Create wallet
rsdt-wallet-cli --generate-new-wallet=mywallet

# Restore wallet
rsdt-wallet-cli --restore-deterministic-wallet=mywallet

# Start wallet RPC
rsdt-wallet-rpc --rpc-bind-port=18083 --wallet-file=mywallet --password=YOUR_PASSWORD --daemon-address=127.0.0.1:18081
```

### 6.2 GUI Wallet

```bash
# Install GUI dependencies
sudo apt install -y qt5-default qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools

# Build GUI wallet
cd rsdt
mkdir build-gui && cd build-gui
cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_GUI_DEPS=ON
make -j$(nproc)

# Run GUI wallet
./bin/rsdt-wallet-gui
```

### 6.3 Mobile Wallet (Android)

```bash
# Install Android Studio and NDK
# Clone mobile wallet repository
git clone https://github.com/resistance-blockchain/rsdt-mobile.git
cd rsdt-mobile

# Build APK
./gradlew assembleRelease
```

---

## 7. EXCHANGE INTEGRATION

### 7.1 RPC API Setup

```bash
# Enable RPC API
cat >> ~/.rsdt/rsdt.conf << EOF
# Exchange Integration
rpc-login=exchange:password
confirm-external-bind=1
restricted-rpc=0
EOF

# Restart daemon
sudo systemctl restart rsdtd
```

### 7.2 Exchange Integration Script

```python
#!/usr/bin/env python3
import requests
import json

class RSDTExchange:
    def __init__(self, rpc_url, rpc_user, rpc_pass):
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_pass = rpc_pass
    
    def get_height(self):
        response = requests.post(
            self.rpc_url,
            json={"jsonrpc": "2.0", "id": "0", "method": "get_height"},
            auth=(self.rpc_user, self.rpc_pass)
        )
        return response.json()["result"]["height"]
    
    def get_transaction(self, tx_hash):
        response = requests.post(
            self.rpc_url,
            json={
                "jsonrpc": "2.0",
                "id": "0",
                "method": "get_transactions",
                "params": {"txs_hashes": [tx_hash]}
            },
            auth=(self.rpc_user, self.rpc_pass)
        )
        return response.json()["result"]

# Usage
exchange = RSDTExchange(
    "http://127.0.0.1:18081/json_rpc",
    "exchange",
    "password"
)
print(f"Current height: {exchange.get_height()}")
```

---

## 8. GOVERNANCE SETUP

### 8.1 DAO Configuration

```bash
# Install DAO dependencies
pip3 install web3 flask sqlalchemy

# Clone DAO repository
git clone https://github.com/resistance-blockchain/rsdt-dao.git
cd rsdt-dao

# Configure DAO
cp config.example.py config.py
# Edit config.py with your settings

# Start DAO
python3 app.py
```

### 8.2 Multi-Signature Wallet Setup

```bash
# Create multisig wallet
rsdt-wallet-cli --generate-new-wallet=multisig_wallet --multisig-threshold=4 --multisig-signers=6

# Export keys for other signers
rsdt-wallet-cli --wallet-file=multisig_wallet --export-multisig-info=multisig_info.txt
```

---

## 9. MONITORING & MAINTENANCE

### 9.1 Monitoring Setup

```bash
# Install monitoring tools
sudo apt install -y prometheus node-exporter

# Configure Prometheus
cat > /etc/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'rsdt-node'
    static_configs:
      - targets: ['localhost:18081']
EOF

# Start monitoring
sudo systemctl start prometheus
sudo systemctl enable prometheus
```

### 9.2 Backup Procedures

```bash
# Create backup script
cat > backup_rsdt.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/rsdt/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup blockchain data
cp -r ~/.rsdt/data.mdb $BACKUP_DIR/
cp -r ~/.rsdt/lock.mdb $BACKUP_DIR/

# Backup wallets
cp -r ~/.rsdt/wallets $BACKUP_DIR/

# Compress backup
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR
EOF

chmod +x backup_rsdt.sh

# Schedule daily backups
echo "0 2 * * * /path/to/backup_rsdt.sh" | crontab -
```

---

## 10. TROUBLESHOOTING

### 10.1 Common Issues

**Daemon won't start:**
```bash
# Check logs
tail -f ~/.rsdt/rsdt.log

# Check port availability
netstat -tlnp | grep 18080

# Reset blockchain (if corrupted)
rm ~/.rsdt/data.mdb ~/.rsdt/lock.mdb
rsdtd --config-file=~/.rsdt/rsdt.conf
```

**Mining not working:**
```bash
# Check daemon connection
curl -X POST http://127.0.0.1:18081/json_rpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"0","method":"get_height"}'

# Check mining address
rsdt-wallet-cli --wallet-file=mywallet --address
```

**Wallet sync issues:**
```bash
# Reset wallet
rsdt-wallet-cli --wallet-file=mywallet --refresh

# Check daemon height
curl -X POST http://127.0.0.1:18081/json_rpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"0","method":"get_height"}'
```

### 10.2 Performance Optimization

**Database optimization:**
```bash
# Enable fast sync
echo "db-sync-mode=fast:async:1000000" >> ~/.rsdt/rsdt.conf

# Increase cache size
echo "db-cache-size=1073741824" >> ~/.rsdt/rsdt.conf
```

**Network optimization:**
```bash
# Increase peer limits
echo "out-peers=24" >> ~/.rsdt/rsdt.conf
echo "in-peers=24" >> ~/.rsdt/rsdt.conf

# Optimize bandwidth
echo "limit-rate-up=4096" >> ~/.rsdt/rsdt.conf
echo "limit-rate-down=16384" >> ~/.rsdt/rsdt.conf
```

---

## CONCLUSION

This deployment bible provides comprehensive guidance for deploying and maintaining RSDT blockchain infrastructure. Follow the steps carefully and refer to the troubleshooting section for common issues.

For additional support, visit:
- **Documentation**: https://docs.rsdt.org
- **Community**: https://community.rsdt.org
- **GitHub**: https://github.com/resistance-blockchain/rsdt

---

**Document Version**: 1.0  
**Last Updated**: September 2024  
**Network**: Resistance Blockchain (RSDT)  
**Genesis Message**: "Censorship is control; privacy is resistance"
