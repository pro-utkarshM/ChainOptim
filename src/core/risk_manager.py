#!/usr/bin/env python
# src/core/risk_manager.py

import os
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ETH_RPC = os.getenv("ETH_RPC")
BSC_RPC = os.getenv("BSC_RPC")
INJECTIVE_RPC = os.getenv("INJECTIVE_RPC")  # Injective is not EVM, special handling needed

# Set up Web3 providers for EVM-compatible chains.
web3_providers = {
    "Ethereum": Web3(Web3.HTTPProvider(ETH_RPC)) if ETH_RPC else None,
    "BSC": Web3(Web3.HTTPProvider(BSC_RPC)) if BSC_RPC else None,
}

def check_slippage(expected_output, actual_output, max_slippage_percent=1.0):
    """
    Check if the actual output meets the slippage requirements.
    
    :param expected_output: Expected amount of tokens.
    :param actual_output: Actual received tokens.
    :param max_slippage_percent: Maximum allowed slippage percentage (default: 1%).
    :return: Tuple (within_limit: bool, slippage: float)
    """
    if expected_output == 0:
        return False, 0
    slippage = abs((expected_output - actual_output) / expected_output) * 100
    return slippage <= max_slippage_percent, slippage

def estimate_gas_price(chain="Ethereum"):
    """
    Estimate the current gas price for the given chain.
    
    :param chain: Blockchain network.
    :return: Gas price in Wei.
    """
    web3 = web3_providers.get(chain)
    if not web3:
        print(f"⚠️ Warning: No Web3 provider available for {chain}.")
        return None
    try:
        return web3.eth.gas_price
    except Exception as e:
        print(f"❌ Error estimating gas price on {chain}: {e}")
        return None

def protect_against_mev(tx_data, chain="Ethereum", min_multiplier=1.2, gas_price_floor=10**9):
    """
    Apply MEV protection strategies, such as increasing the gas price to discourage front-running.
    
    :param tx_data: The transaction data dictionary.
    :param chain: Blockchain network.
    :param min_multiplier: Minimum multiplier for gas price (default: 20% increase).
    :param gas_price_floor: Minimum gas price to use if estimation fails.
    :return: Modified transaction data.
    """
    estimated_gas_price = estimate_gas_price(chain)

    # Use the estimated gas price or fall back to a predefined minimum
    new_gas_price = estimated_gas_price if estimated_gas_price else gas_price_floor

    # Increase by the set multiplier (default 1.2x)
    tx_data["gasPrice"] = int(new_gas_price * min_multiplier)
    return tx_data

# CLI testing for risk management functions.
if __name__ == "__main__":
    # Test slippage check.
    expected = 100
    actual = 98.5
    within_limit, slippage = check_slippage(expected, actual, max_slippage_percent=1.5)
    print(f"✅ Slippage Check: {'OK' if within_limit else 'Exceeds Limit'} (Slippage: {slippage:.2f}%)")
    
    # Test MEV protection.
    dummy_tx = {"gasPrice": 1000000000}
    modified_tx = protect_against_mev(dummy_tx, chain="Ethereum")
    print("🚀 Modified Transaction:", modified_tx)
