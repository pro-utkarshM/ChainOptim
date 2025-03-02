#!/usr/bin/env python
# src/data/oracles.py

import os
import json
import requests
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Environment variables
ETH_RPC = os.getenv("ETH_RPC")
PYTH_API_URL = os.getenv("PYTH_API_URL", "https://pyth-api.endpoint/")  # Set your Pyth API endpoint
# Optionally, you can store a default aggregator address in the env file as CHAINLINK_AGGREGATOR_ADDRESS

# Setup a Web3 provider for Ethereum (for Chainlink)
web3 = Web3(Web3.HTTPProvider(ETH_RPC))

# Minimal Chainlink Aggregator ABI for latestRoundData()
CHAINLINK_AGGREGATOR_ABI = [
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"internalType": "uint80", "name": "roundId", "type": "uint80"},
            {"internalType": "int256", "name": "answer", "type": "int256"},
            {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
            {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

def get_chainlink_price(aggregator_address):
    """
    Fetch the latest price from a Chainlink price feed.
    
    :param aggregator_address: The address of the Chainlink aggregator contract.
    :return: Latest price as a float (adjusting for decimals) or None on error.
    """
    try:
        aggregator = web3.eth.contract(address=aggregator_address, abi=CHAINLINK_AGGREGATOR_ABI)
        round_data = aggregator.functions.latestRoundData().call()
        price = round_data[1]  # 'answer' field
        # Chainlink feeds typically have 8 decimals; adjust as necessary
        return float(price) / 1e8
    except Exception as e:
        print(f"Error fetching Chainlink price: {e}")
        return None

def get_pyth_price(symbol):
    """
    Fetch the latest price from the Pyth network via its API.
    
    :param symbol: Asset symbol to fetch (e.g., "ETHUSD").
    :return: Latest price as a float or None on error.
    """
    try:
        # Assuming the API endpoint accepts a query parameter for the symbol
        response = requests.get(f"{PYTH_API_URL}/price?symbol={symbol}")
        if response.status_code == 200:
            data = response.json()
            # Expecting the JSON to include a key named 'price'
            return float(data.get("price"))
        else:
            print(f"Pyth API returned error code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Pyth price: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    # Replace with an actual Chainlink aggregator address (e.g., ETH/USD feed)
    aggregator_address = os.getenv("CHAINLINK_AGGREGATOR_ADDRESS", "0x0000000000000000000000000000000000000000")
    chainlink_price = get_chainlink_price(aggregator_address)
    print("Chainlink Price:", chainlink_price)
    
    # Example Pyth price fetch for ETHUSD
    pyth_price = get_pyth_price("ETHUSD")
    print("Pyth Price:", pyth_price)
