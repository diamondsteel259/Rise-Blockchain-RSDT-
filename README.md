# RSDT Resistance Blockchain

**Fighting Financial Oppression**

RSDT (Resistance) is a privacy-focused cryptocurrency built on the Monero blockchain technology, designed to provide financial freedom and resist centralized control.

## 🚀 Features

- **Privacy**: Ring signatures and stealth addresses
- **Decentralized**: No central authority
- **Premine**: 20M RSDT (10% of 200M total supply)
- **Cross-platform**: Linux, Windows, Android support
- **Fast**: 2-minute block times

## 📊 Tokenomics

- **Total Supply**: 200M RSDT
- **Premine**: 20M RSDT (10%)
- **Block Time**: 2 minutes
- **Block Reward**: Decreasing schedule with tail emission

## 🔧 Building from Source

```bash
# Install dependencies
sudo apt update
sudo apt install build-essential cmake git pkg-config libboost-all-dev libssl-dev libzmq3-dev libunbound-dev libsodium-dev libunwind8-dev liblzma-dev libreadline6-dev libldns-dev libexpat1-dev libgtest-dev doxygen graphviz

# Build (Debug)
mkdir build && cd build
cmake ..
make -j$(nproc)

# Build (Release - recommended for production)
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)

# Run daemon
./bin/rsdtd
```

## 📚 Documentation

- [Whitepaper](RESISTANCE_BLOCKCHAIN_WHITEPAPER.pdf)
- [Tokenomics](RSDT_TOKENOMICS_PROFESSIONAL.pdf)  
- [Deployment Guide](RSDT_DEPLOYMENT_BIBLE_UPDATED.pdf)
- [Blockchain Overview](RSDT_BLOCKCHAIN_OVERVIEW.pdf)
- [Release Checklist](RELEASE_CHECKLIST.md)

## 🧪 Testing

### Manual Smoke Tests
```bash
# After building, run basic smoke tests
./utils/ci/smoke_test.sh ./build/bin/rsdtd
```

**Note:** Smoke tests are provided for manual validation and do not run automatically in CI.

## ⚠️ Disclaimer

This is experimental software. Use at your own risk.

**🔒 SECURITY WARNING**: This repository contains sensitive premine wallet information. Any changes to genesis parameters, premine allocations, or consensus rules require explicit approval and security review. See [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) for details.

## 📄 License

BSD 3-Clause License# Test build workflow
