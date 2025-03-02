#!/usr/bin/env python
# src/core/risk_manager.py

import os
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ETH_RPC = os.getenv("ETH_RPC")
BSC_RPC = os.getenv("BSC_RPC")
INJECTIVE_RPC = os.getenv("INJECTIVE_RPC")

# Set up Web3 providers for supported chains.
web3_providers = {
    "Ethereum": Web3(Web3.HTTPProvider(ETH_RPC)),
    "BSC": Web3(Web3.HTTPProvider(BSC_RPC)),
    "Injective": Web3(Web3.HTTPProvider(INJECTIVE_RPC))  # May need different handling
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
        return None
    try:
        return web3.eth.gas_price
    except Exception as e:
        print(f"Error estimating gas price: {e}")
        return None

def protect_against_mev(tx_data, chain="Ethereum"):
    """
    Apply MEV protection strategies, such as increasing the gas price to discourage front-running.
    
    :param tx_data: The transaction data dictionary.
    :param chain: Blockchain network.
    :return: Modified transaction data.
    """
    gas_price = estimate_gas_price(chain)
    if gas_price:
        # Increase gas price by 20% to help secure the transaction.
        tx_data["gasPrice"] = int(gas_price * 1.2)
    return tx_data

# CLI testing for risk management functions.
if __name__ == "__main__":
    # Test slippage check.
    expected = 100
    actual = 98.5
    within_limit, slippage = check_slippage(expected, actual, max_slippage_percent=1.5)
    print(f"Slippage Check: {'OK' if within_limit else 'Exceeds Limit'} (Slippage: {slippage:.2f}%)")
    
    # Test MEV protection.
    dummy_tx = {"gasPrice": 1000000000}
    modified_tx = protect_against_mev(dummy_tx, chain="Ethereum")
    print("Modified Transaction:", modified_tx)
