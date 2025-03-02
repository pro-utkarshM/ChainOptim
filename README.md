# DeFAI Terminal

DeFAI Terminal is a cross-chain transaction optimization agent designed for decentralized finance (DeFi). It aggregates liquidity from multiple decentralized exchanges (DEXs) across several blockchains (Ethereum, BSC, Injective) and leverages AI-based routing (Monte Carlo Tree Search, reinforcement learning) to execute swaps with minimal slippage and optimized fees.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [API](#api)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Overview

The DeFAI Terminal aims to provide a robust, AI-powered platform for cross-chain swaps by:
- Aggregating liquidity from multiple on-chain sources.
- Using Monte Carlo Tree Search (MCTS) to explore and optimize trade execution paths.
- Employing reinforcement learning models for dynamic slippage prediction and route selection.
- Ensuring secure transaction execution with integrated risk management (MEV protection, slippage controls).

## Features

- **Liquidity Aggregation:**  
  Fetches liquidity data from DEXs on Ethereum (Uniswap), BSC (PancakeSwap), and Injective using on-chain queries and REST APIs.

- **AI-Powered Routing:**  
  Implements MCTS and reinforcement learning for optimized swap route selection.

- **Transaction Execution:**  
  Executes cross-chain swaps via smart contracts, with integrated MEV and slippage protection strategies.

- **Real-Time Oracles:**  
  Retrieves live price data from Chainlink and Pyth oracles.

- **Modular Architecture:**  
  Built with scalability in mind, featuring separate modules for core logic, models, data, interfaces, and smart contracts.

## Project Structure

```
DeFAI-Terminal/
│
├── src/
│   ├── core/
│   │   ├── liquidity.py       # Fetches liquidity data from DEXs & bridges
│   │   ├── mcts_router.py     # Monte Carlo Tree Search for route optimization
│   │   ├── execution.py       # Executes transactions based on best route
│   │   ├── risk_manager.py    # Slippage & MEV protection strategies
│   │   ├── utils.py           # Helper functions (logging, conversions, etc.)
│   │
│   ├── models/               # AI Models for slippage prediction & routing
│   │   ├── train_model.py     # Train reinforcement learning models
│   │   ├── predict.py         # Make predictions on best execution strategies
│   │
│   ├── data/                 # Historical transaction & liquidity data
│   │   ├── oracles.py         # Fetches real-time price data from Chainlink/Pyth
│   │   ├── simulation.py      # Simulates trade execution & slippage estimation
│   │
│   ├── interfaces/           # API & Web Interface
│   │   ├── api.py             # FastAPI for backend services
│   │   ├── frontend/          # Web interface (React/Vue) [Planned]
│   │
│   ├── contracts/            # Smart contracts (Solidity/Rust for Injective)
│   │   ├── SwapRouter.sol     # Cross-chain swap execution contract
│   │   ├── LiquidityAggregator.sol  # Aggregates liquidity sources on-chain
│   │
│   ├── config.py             # Configuration & environment variables
│   ├── main.py               # Entry point for executing swaps (CLI)
│
├── tests/                    # Unit & integration tests
├── docs/                     # Documentation & API references
├── requirements.txt          # Dependencies
└── README.md                 # Project overview & setup instructions
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/pro-utkarshM/ChainOptim
   cd ChainOptim
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file in the root directory with your configuration (see sample below):

   ```env
   # Blockchain RPC endpoints
   ETH_RPC=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
   BSC_RPC=https://bsc-dataseed.binance.org/
   INJECTIVE_RPC=https://injective-api.endpoint/

   # SwapRouter Smart Contract Details
   SWAP_ROUTER_ADDRESS=0xYourSwapRouterContractAddress
   SWAP_ROUTER_ABI=[{"constant":true,"inputs":[],"name":"dummy","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]

   # Chainlink/Pyth Oracles (optional)
   CHAINLINK_AGGREGATOR_ADDRESS=0xYourChainlinkAggregatorAddress
   PYTH_API_URL=https://pyth-api.endpoint/
   ```

## Usage

### CLI

Execute a swap from the command line using the `main.py` script:

```bash
python src/main.py --swap_input 10 --from_address 0xYourAddress --private_key YourPrivateKey --chain Ethereum
```

Replace the placeholder values with your actual data. The CLI will fetch liquidity data, run the MCTS router, and execute the optimal swap transaction.

### API

Run the FastAPI backend for programmatic access:

```bash
uvicorn src/interfaces/api:app --host 0.0.0.0 --port 8000
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Testing

Run the unit and integration tests using pytest:

```bash
pytest
```

Ensure that all tests pass before deploying or integrating changes.

## Future Enhancements

- **Enhanced Routing:**  
  Multi-hop routing and improved AI model integration.

- **Frontend UI:**  
  Develop a web-based interface using React or Vue.

- **Extended Blockchain Support:**  
  Integrate additional blockchain networks.

- **Advanced Risk Management:**  
  Further enhance slippage protection, MEV mitigation, and gas optimization strategies.


Happy swapping and optimizing! 🚀
