#!/usr/bin/env python
# src/core/execution.py

import time
import json
import os
from web3 import Web3
from dotenv import load_dotenv
from core.risk_manager import protect_against_mev

# Load environment variables from the .env file
load_dotenv()

# Retrieve configuration from environment variables
ETH_RPC = os.getenv("ETH_RPC")
BSC_RPC = os.getenv("BSC_RPC")
INJECTIVE_RPC = os.getenv("INJECTIVE_RPC")
SWAP_ROUTER_ADDRESS = os.getenv("SWAP_ROUTER_ADDRESS")
SWAP_ROUTER_ABI = json.loads(os.getenv("SWAP_ROUTER_ABI"))

def execute_swap(best_route, swap_input, from_address, private_key, chain="Ethereum"):
    """
    Execute a swap transaction using the best route information.
    
    :param best_route: Dictionary with route details (e.g., liquidity pool info, expected output).
    :param swap_input: The amount of input tokens to swap (as an integer, in smallest unit).
    :param from_address: The sender's blockchain address.
    :param private_key: The private key for signing the transaction.
    :param chain: Blockchain network ("Ethereum", "BSC", or "Injective").
    :return: Transaction hash string or an error message.
    """
    # Select the appropriate Web3 provider based on the target chain.
    if chain == "Ethereum":
        web3 = Web3(Web3.HTTPProvider(ETH_RPC))
    elif chain == "BSC":
        web3 = Web3(Web3.HTTPProvider(BSC_RPC))
    elif chain == "Injective":
        # For Injective, a different execution method might be needed.
        return "Injective execution not implemented"
    else:
        return "Unsupported chain"

    # Connect to the SwapRouter smart contract.
    contract = web3.eth.contract(address=SWAP_ROUTER_ADDRESS, abi=SWAP_ROUTER_ABI)

    # Determine the minimum acceptable output.
    min_output = int(best_route.get("expected_output", 0))

    # Define a transaction deadline (current time + 300 seconds).
    deadline = int(time.time()) + 300

    # Build the transaction.
    tx = contract.functions.swapExactTokens(
        swap_input,
        min_output,
        from_address,
        deadline
    ).buildTransaction({
        'chainId': web3.eth.chain_id,
        'gas': 250000,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.getTransactionCount(from_address)
    })

    # Apply MEV protection to the transaction.
    tx = protect_against_mev(tx, chain=chain)

    # Sign the transaction.
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)

    # Send the transaction.
    try:
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.toHex(tx_hash)
    except Exception as e:
        return f"Transaction failed: {e}"


# CLI testing: This code will run if you execute the module directly.
if __name__ == "__main__":
    # Dummy best_route for testing (replace with real data)
    best_route = {
        "pool": "Uniswap",
        "chain": "Ethereum",
        "expected_output": 95  # Placeholder expected output
    }
    swap_input = 10               # Amount of input tokens (in smallest unit)
    from_address = "0xYourAddressHere"
    private_key = "YourPrivateKeyHere"  # NEVER hard-code real keys in production!

    result = execute_swap(best_route, swap_input, from_address, private_key, chain="Ethereum")
    print("Transaction result:", result)
