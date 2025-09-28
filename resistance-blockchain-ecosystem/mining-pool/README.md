# ⛏️ Resistance Blockchain Mining Pool

Decentralized mining pool server for RSDT cryptocurrency.

## Features

- **Fair Distribution**: Proportional reward distribution
- **Low Fees**: 1% pool fee
- **Real-time Stats**: Live mining statistics
- **Auto Payout**: Automatic reward distribution
- **Pool Management**: Admin interface for pool operators
- **Miner Support**: Support for multiple miners

## Installation

```bash
# Install dependencies
pip install aiohttp asyncio

# Run the pool
python3 mining_pool.py
```

## Configuration

- **Pool Fee**: 1% (configurable)
- **Payout Threshold**: 0.1 RSDT
- **Block Time**: 120 seconds
- **Reward**: 50 RSDT per block

## API Endpoints

- `GET /stats` - Pool statistics
- `POST /submit` - Submit shares
- `GET /miners` - Miner information

## Requirements

- Python 3.7+
- aiohttp
- Resistance Blockchain daemon running

## Support

For issues and support, please open an issue in the main repository.
