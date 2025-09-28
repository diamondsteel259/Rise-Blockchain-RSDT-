# RSDT Blockchain - Build Guide

This document provides comprehensive instructions for building, testing, and deploying the RSDT blockchain.

## Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+ / macOS 11+ / Windows 10+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 20GB free space for build, 50GB+ for full node
- **Network**: Stable internet connection for dependencies

### Required Dependencies

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y \
    build-essential \
    cmake \
    pkg-config \
    libssl-dev \
    libzmq3-dev \
    libunbound-dev \
    libsodium-dev \
    libunwind8-dev \
    liblzma-dev \
    libreadline6-dev \
    libldns-dev \
    libexpat1-dev \
    libpgm-dev \
    qttools5-dev-tools \
    libhidapi-dev \
    libusb-1.0-0-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libudev-dev \
    libboost-chrono-dev \
    libboost-date-time-dev \
    libboost-filesystem-dev \
    libboost-locale-dev \
    libboost-program-options-dev \
    libboost-regex-dev \
    libboost-serialization-dev \
    libboost-system-dev \
    libboost-thread-dev \
    python3 \
    ccache
```

#### CentOS/RHEL/Fedora
```bash
sudo dnf install -y \
    gcc gcc-c++ cmake make \
    openssl-devel zeromq-devel \
    libunbound-devel libsodium-devel \
    libunwind-devel xz-devel \
    readline-devel ldns-devel \
    expat-devel openpgm-devel \
    libusb1-devel libudev-devel \
    protobuf-devel boost-devel \
    python3 ccache
```

## Build Instructions

### 1. Clone and Prepare
```bash
git clone https://github.com/diamondsteel259/Rise-Blockchain-RSDT-.git
cd Rise-Blockchain-RSDT-
git submodule update --init --recursive
```

### 2. Build Configuration
```bash
mkdir build && cd build

# Standard Release Build
cmake -D CMAKE_BUILD_TYPE=Release ..

# Debug Build (for development)
cmake -D CMAKE_BUILD_TYPE=Debug ..

# Static Build (for distribution)
cmake -D CMAKE_BUILD_TYPE=Release -D STATIC=ON ..
```

### 3. Compile
```bash
# Use all CPU cores for faster build
make -j$(nproc)

# Or specify core count manually
make -j4
```

### 4. Build Verification
```bash
# Check if main binaries were created
ls -la bin/

# Expected outputs:
# - rsdtd (daemon)
# - rsdt-wallet-cli (CLI wallet)  
# - rsdt-wallet-rpc (RPC wallet)
# - rsdt-gen-trusted-multisig
# - rsdt-blockchain-export
# - rsdt-blockchain-import
```

## Testing

### Unit Tests
```bash
# Run unit tests
make test

# Run specific test suites
./tests/unit_tests/unit_tests
./tests/core_tests/core_tests
./tests/crypto/crypto-tests
```

### Functional Tests
```bash
# Test daemon startup
./bin/rsdtd --testnet --offline

# Test wallet creation
./bin/rsdt-wallet-cli --testnet --generate-new-wallet test_wallet
```

### Genesis Block Testing
```bash
# Generate test premine information
cd src/gen_premine
make && ./gen_premine

# Test Python genesis generator
cd ../..
python3 create_genesis_with_premine.py
```

## Premine and Genesis Setup

### 1. Generate Public Premine Information
```bash
cd src/gen_premine
g++ -std=c++11 -o gen_premine gen_premine.cpp
./gen_premine
```

This creates:
- `premine_public_info.txt` - Detailed allocation summary
- `premine_allocations.csv` - CSV format for processing

### 2. Prepare Genesis Block (Offline)
**IMPORTANT**: Genesis generation with private keys should be done on an air-gapped machine.

```bash
# Create test genesis block (no private keys)
python3 create_genesis_with_premine.py

# For production: Use offline key generation tools
# Do NOT commit private keys to version control
```

### 3. Update Genesis Configuration
Edit `src/cryptonote_config.h`:
```cpp
// Replace placeholder with final genesis TX hex
std::string const GENESIS_TX = "YOUR_GENERATED_GENESIS_TX_HEX_HERE";
```

## Configuration Files

### Network Configuration
- **Mainnet**: Default ports 18080 (P2P), 18081 (RPC)
- **Testnet**: Ports 28080 (P2P), 28081 (RPC)  
- **Stagenet**: Ports 38080 (P2P), 38081 (RPC)

### Node Configuration Example
```bash
# Run mainnet daemon
./bin/rsdtd --rpc-bind-ip 127.0.0.1 --confirm-external-bind

# Run with custom data directory  
./bin/rsdtd --data-dir /custom/path/rsdt

# Enable mining
./bin/rsdtd --start-mining YOUR_WALLET_ADDRESS --mining-threads 4
```

## Performance Optimization

### Build Optimizations
```bash
# Enable all optimizations
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_CXX_FLAGS="-O3 -march=native" ..

# Link-time optimization
cmake -D CMAKE_BUILD_TYPE=Release -D USE_LTO=ON ..
```

### Runtime Optimizations
```bash
# Use more database cache (default: 128MB)
./bin/rsdtd --db-cache-size 512

# Optimize for SSD
./bin/rsdtd --db-type lmdb

# Enable fast sync
./bin/rsdtd --fast-block-sync
```

## Troubleshooting

### Common Build Issues

**Missing Boost libraries:**
```bash
# Ubuntu/Debian
sudo apt install libboost-all-dev

# Or specify Boost path
cmake -DBOOST_ROOT=/usr/local/boost ..
```

**OpenSSL issues:**
```bash
# Use system OpenSSL
cmake -DUSE_DEVICE_TREZOR=OFF ..
```

**Memory issues during build:**
```bash
# Limit parallel jobs
make -j2

# Or use single thread
make
```

### Runtime Issues

**Database corruption:**
```bash
# Resync blockchain
./bin/rsdtd --db-salvage

# Complete resync
rm -rf ~/.rsdt/lmdb
./bin/rsdtd
```

**Network connectivity:**
```bash
# Check P2P connectivity
./bin/rsdtd --add-peer NODE_IP:18080

# Enable logs
./bin/rsdtd --log-level 2
```

## Security Considerations

### Build Security
- Verify source code integrity
- Use official dependencies only
- Build on clean, trusted systems

### Deployment Security  
- Run daemon as non-root user
- Configure firewall rules
- Enable SSL/TLS for RPC
- Use strong passwords for wallets

### Genesis Security
- Generate genesis block offline
- Store private keys securely
- Never commit private keys to version control
- Use hardware security modules when possible

## Support

For build issues or questions:
- Check GitHub Issues: https://github.com/diamondsteel259/Rise-Blockchain-RSDT-/issues
- Review documentation in `docs/` directory
- Community support channels (to be announced)

## License

This project is licensed under the same terms as Monero. See LICENSE file for details.