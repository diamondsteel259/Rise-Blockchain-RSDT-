# RSDT UBUNTU 24 VM DEPLOYMENT GUIDE
## Complete Setup Guide for Resistance Blockchain on Ubuntu 24 Virtual Machine

---

## 🖥️ **VIRTUAL MACHINE SETUP**

### 1.1 VirtualBox Configuration

**System Requirements:**
- **RAM**: 8GB minimum, 16GB recommended
- **CPU**: 4 cores minimum, 8 cores recommended
- **Storage**: 100GB minimum, 500GB recommended
- **Network**: Bridged adapter for external access

**VM Settings:**
```
Name: RSDT-Blockchain-VM
Type: Linux
Version: Ubuntu (64-bit)
Memory: 8192 MB
Hard Disk: 100 GB (VDI, Dynamically allocated)
Network: Bridged Adapter
```

### 1.2 Ubuntu 24.04 LTS Installation

**Download Ubuntu 24.04 LTS:**
```bash
# Download from official Ubuntu website
wget https://releases.ubuntu.com/24.04/ubuntu-24.04-desktop-amd64.iso
```

**Installation Steps:**
1. Boot from Ubuntu ISO
2. Select "Install Ubuntu"
3. Choose "Normal installation"
4. Select "Erase disk and install Ubuntu"
5. Set up user account
6. Complete installation

---

## 🔧 **SYSTEM PREPARATION**

### 2.1 Update System

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git vim nano htop tree unzip
```

### 2.2 Install Development Tools

```bash
# Install build essentials
sudo apt install -y build-essential cmake pkg-config

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install additional dependencies
sudo apt install -y libssl-dev libboost-all-dev libevent-dev
sudo apt install -y libminiupnpc-dev libunbound-dev libexpat1-dev
sudo apt install -y libgtest-dev libgmock-dev libbenchmark-dev
```

### 2.3 Configure Firewall

```bash
# Enable UFW firewall
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow RSDT ports
sudo ufw allow 18080/tcp  # P2P port
sudo ufw allow 18081/tcp  # RPC port
sudo ufw allow 3333/tcp   # Mining pool port
sudo ufw allow 8080/tcp   # Blockchain explorer port

# Check status
sudo ufw status
```

---

## 📦 **RSDT BLOCKCHAIN DEPLOYMENT**

### 3.1 Create RSDT Directory

```bash
# Create main directory
sudo mkdir -p /opt/rsdt
sudo chown $USER:$USER /opt/rsdt
cd /opt/rsdt

# Create subdirectories
mkdir -p {bin,config,logs,data,mining,explorer}
```

### 3.2 Download RSDT Software

```bash
# Download daemon
wget https://github.com/rsdt/rsdt/releases/latest/download/rsdtd
chmod +x rsdtd
mv rsdtd bin/

# Download wallet CLI
wget https://github.com/rsdt/rsdt/releases/latest/download/rsdt-wallet-cli
chmod +x rsdt-wallet-cli
mv rsdt-wallet-cli bin/

# Download mining pool
wget https://github.com/rsdt/pool/raw/main/rsdt_mining_pool.py
chmod +x rsdt_mining_pool.py
mv rsdt_mining_pool.py mining/

# Download Linux miner
wget https://github.com/rsdt/miners/raw/main/rsdt_linux_miner.py
chmod +x rsdt_linux_miner.py
mv rsdt_linux_miner.py mining/

# Download blockchain explorer
wget https://github.com/rsdt/explorer/raw/main/rsdt_blockchain_explorer.py
chmod +x rsdt_blockchain_explorer.py
mv rsdt_blockchain_explorer.py explorer/
```

### 3.3 Install Python Dependencies

```bash
# Install Python packages for mining pool
pip3 install aiohttp requests sqlite3

# Install Python packages for blockchain explorer
pip3 install flask requests
```

---

## 🚀 **SERVICE CONFIGURATION**

### 4.1 Create Systemd Services

#### 4.1.1 RSDT Daemon Service

```bash
# Create daemon service file
sudo tee /etc/systemd/system/rsdtd.service > /dev/null <<EOF
[Unit]
Description=RSDT Blockchain Daemon
After=network.target

[Service]
Type=simple
User=rsdt
Group=rsdt
WorkingDirectory=/opt/rsdt
ExecStart=/opt/rsdt/bin/rsdtd --testnet --rpc-bind-ip=0.0.0.0 --rpc-bind-port=18081 --log-level=1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

#### 4.1.2 Mining Pool Service

```bash
# Create mining pool service file
sudo tee /etc/systemd/system/rsdt-pool.service > /dev/null <<EOF
[Unit]
Description=RSDT Mining Pool
After=network.target rsdtd.service
Requires=rsdtd.service

[Service]
Type=simple
User=rsdt
Group=rsdt
WorkingDirectory=/opt/rsdt/mining
ExecStart=/usr/bin/python3 /opt/rsdt/mining/rsdt_mining_pool.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

#### 4.1.3 Blockchain Explorer Service

```bash
# Create blockchain explorer service file
sudo tee /etc/systemd/system/rsdt-explorer.service > /dev/null <<EOF
[Unit]
Description=RSDT Blockchain Explorer
After=network.target rsdtd.service
Requires=rsdtd.service

[Service]
Type=simple
User=rsdt
Group=rsdt
WorkingDirectory=/opt/rsdt/explorer
ExecStart=/usr/bin/python3 /opt/rsdt/explorer/rsdt_blockchain_explorer.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### 4.2 Create RSDT User

```bash
# Create dedicated user for RSDT services
sudo useradd -r -s /bin/false rsdt
sudo chown -R rsdt:rsdt /opt/rsdt
```

### 4.3 Enable and Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable rsdtd
sudo systemctl enable rsdt-pool
sudo systemctl enable rsdt-explorer

# Start services
sudo systemctl start rsdtd
sudo systemctl start rsdt-pool
sudo systemctl start rsdt-explorer

# Check status
sudo systemctl status rsdtd
sudo systemctl status rsdt-pool
sudo systemctl status rsdt-explorer
```

---

## 🔍 **MONITORING AND LOGS**

### 5.1 Service Monitoring

```bash
# Check service status
sudo systemctl status rsdtd rsdt-pool rsdt-explorer

# View logs
sudo journalctl -u rsdtd -f
sudo journalctl -u rsdt-pool -f
sudo journalctl -u rsdt-explorer -f

# Check ports
sudo netstat -tlnp | grep -E "(18080|18081|3333|8080)"
```

### 5.2 Log Files

```bash
# Daemon logs
tail -f /opt/rsdt/logs/daemon.log

# Mining pool logs
tail -f /opt/rsdt/logs/pool.log

# Explorer logs
tail -f /opt/rsdt/logs/explorer.log
```

---

## 🌐 **NETWORK CONFIGURATION**

### 6.1 Port Configuration

**Required Ports:**
- **18080**: P2P network communication
- **18081**: RPC API access
- **3333**: Mining pool stratum
- **8080**: Blockchain explorer web interface

### 6.2 External Access

```bash
# Get VM IP address
ip addr show

# Test external connectivity
curl -s http://YOUR_VM_IP:8080
curl -s http://YOUR_VM_IP:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}'
```

---

## 💰 **MINING SETUP**

### 7.1 Configure Mining Pool

```bash
# Create pool configuration
cat > /opt/rsdt/config/pool_config.json <<EOF
{
    "daemon_url": "http://127.0.0.1:18081",
    "pool_fee": 1.0,
    "min_payout": 0.1,
    "database": "/opt/rsdt/data/rsdt_pool.db",
    "pool_address": "4A64wDfoaR6Lf1CGww4KanRZXbwrzXFFfE7wjtwvtZu8gVWEyYHzgbpAPiBra5UR5HCjcEFufBMZLRcHj3BCXLfuNf9Sn4N",
    "pool_port": 3333,
    "api_port": 8080
}
EOF
```

### 7.2 Start Mining

```bash
# Connect to mining pool
cd /opt/rsdt/mining
python3 rsdt_linux_miner.py

# Enter configuration:
# Pool URL: http://YOUR_VM_IP:3333
# Wallet: YOUR_WALLET_ADDRESS
# Worker: vm-worker-1
# Threads: 4
```

---

## 🔧 **TROUBLESHOOTING**

### 8.1 Common Issues

#### 8.1.1 Service Won't Start

```bash
# Check service logs
sudo journalctl -u rsdtd --no-pager

# Check permissions
ls -la /opt/rsdt/bin/rsdtd

# Check dependencies
ldd /opt/rsdt/bin/rsdtd
```

#### 8.1.2 Port Conflicts

```bash
# Check what's using ports
sudo lsof -i :18080
sudo lsof -i :18081
sudo lsof -i :3333
sudo lsof -i :8080

# Kill conflicting processes
sudo pkill -f conflicting_process
```

#### 8.1.3 Firewall Issues

```bash
# Check firewall status
sudo ufw status

# Allow specific ports
sudo ufw allow 18080/tcp
sudo ufw allow 18081/tcp
sudo ufw allow 3333/tcp
sudo ufw allow 8080/tcp
```

### 8.2 Performance Optimization

```bash
# Monitor system resources
htop

# Check disk usage
df -h

# Monitor network
iftop

# Check memory usage
free -h
```

---

## 📊 **BACKUP AND MAINTENANCE**

### 9.1 Backup Configuration

```bash
# Create backup script
cat > /opt/rsdt/backup.sh <<EOF
#!/bin/bash
BACKUP_DIR="/opt/rsdt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /opt/rsdt/config/

# Backup database
cp /opt/rsdt/data/rsdt_pool.db $BACKUP_DIR/rsdt_pool_$DATE.db

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /opt/rsdt/logs/

echo "Backup completed: $DATE"
EOF

chmod +x /opt/rsdt/backup.sh
```

### 9.2 Automated Maintenance

```bash
# Create maintenance script
cat > /opt/rsdt/maintenance.sh <<EOF
#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Restart services
sudo systemctl restart rsdtd
sudo systemctl restart rsdt-pool
sudo systemctl restart rsdt-explorer

# Clean old logs
find /opt/rsdt/logs -name "*.log" -mtime +7 -delete

# Run backup
/opt/rsdt/backup.sh

echo "Maintenance completed: $(date)"
EOF

chmod +x /opt/rsdt/maintenance.sh

# Add to crontab for weekly maintenance
(crontab -l 2>/dev/null; echo "0 2 * * 0 /opt/rsdt/maintenance.sh") | crontab -
```

---

## 🎯 **FINAL VERIFICATION**

### 10.1 Service Status Check

```bash
# Verify all services are running
sudo systemctl is-active rsdtd rsdt-pool rsdt-explorer

# Check port accessibility
curl -s http://localhost:8080 | head -5
curl -s http://localhost:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}' | head -5
```

### 10.2 External Access Test

```bash
# Test from external machine
curl -s http://YOUR_VM_IP:8080
curl -s http://YOUR_VM_IP:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_info"}'
```

### 10.3 Mining Test

```bash
# Test mining connection
cd /opt/rsdt/mining
echo -e "http://YOUR_VM_IP:3333\nYOUR_WALLET_ADDRESS\ntest-worker\n1" | timeout 30 python3 rsdt_linux_miner.py
```

---

## 📋 **DEPLOYMENT CHECKLIST**

- [ ] VirtualBox VM created and configured
- [ ] Ubuntu 24.04 LTS installed
- [ ] System updated and dependencies installed
- [ ] Firewall configured
- [ ] RSDT software downloaded and installed
- [ ] Systemd services created and enabled
- [ ] RSDT user created
- [ ] Services started and running
- [ ] Ports accessible
- [ ] Mining pool configured
- [ ] Blockchain explorer accessible
- [ ] External access tested
- [ ] Backup and maintenance scripts created
- [ ] Monitoring setup complete

---

## 🚀 **NEXT STEPS**

1. **Domain Configuration**: Set up your domain to point to the VM
2. **SSL Certificates**: Install SSL certificates for secure access
3. **Load Balancing**: Set up load balancing for high availability
4. **Monitoring**: Implement comprehensive monitoring and alerting
5. **Backup**: Set up automated backups to external storage
6. **Scaling**: Plan for horizontal scaling as network grows

**Your RSDT blockchain is now fully deployed and operational on Ubuntu 24 VM!** 🎉

