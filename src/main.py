#!/usr/bin/env python
# src/main.py

import argparse
import sys
import json
from core.liquidity import fetch_all_liquidity
from core.mcts_router import MCTSNode, mcts, simulate
from core.execution import execute_swap
from core.utils import setup_logger

def main():
    # Set up a logger for informative logging.
    logger = setup_logger("DeFAI-Terminal")

    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="DeFAI Terminal CLI for executing swaps based on optimized routes."
    )
    parser.add_argument(
        "--chain",
        type=str,
        default="Ethereum",
        help="Target blockchain network (e.g., Ethereum, BSC, Injective)"
    )
    parser.add_argument(
        "--swap_input",
        type=int,
        required=True,
        help="Amount of input tokens to swap (in smallest unit)"
    )
    parser.add_argument(
        "--from_address",
        type=str,
        required=True,
        help="Sender's blockchain address"
    )
    parser.add_argument(
        "--private_key",
        type=str,
        required=True,
        help="Sender's private key for signing the transaction (handle securely!)"
    )

    args = parser.parse_args()

    logger.info("Fetching aggregated liquidity data...")
    liquidity_data = fetch_all_liquidity()
    if not liquidity_data:
        logger.error("No liquidity data available. Exiting.")
        sys.exit(1)

    logger.info("Running MCTS routing algorithm to select the best route...")
    # Create a root node (with no pool assigned)
    root = MCTSNode()
    best_node = mcts(root, iterations=1000, swap_input=args.swap_input, available_pools=liquidity_data)
    if best_node is None or best_node.pool is None:
        logger.error("No valid swap route found. Exiting.")
        sys.exit(1)

    best_route = best_node.pool
    # Use simulation to estimate expected output (for slippage checking)
    expected_output = simulate(best_node, args.swap_input)
    best_route["expected_output"] = expected_output

    logger.info("Best route selected:")
    logger.info(json.dumps(best_route, indent=4))
    logger.info(f"Expected output tokens: {expected_output}")

    logger.info("Executing swap transaction...")
    tx_result = execute_swap(
        best_route,
        args.swap_input,
        args.from_address,
        args.private_key,
        chain=args.chain
    )

    logger.info(f"Transaction result: {tx_result}")

if __name__ == "__main__":
    main()
