#!/usr/bin/env python
# tests/test_mcts_router.py

import pytest
from core.mcts_router import MCTSNode, mcts, simulate

def test_mcts_returns_best_route():
    # Create dummy liquidity pools as test data.
    available_pools = [
        {"token0": 100, "token1": 100, "pool": "Uniswap", "chain": "Ethereum"},
        {"token0": 150, "token1": 150, "pool": "PancakeSwap", "chain": "BSC"},
    ]
    root = MCTSNode()
    best_node = mcts(root, iterations=100, swap_input=10, available_pools=available_pools)
    assert best_node is not None
    # Ensure that best_node has a pool assigned.
    assert best_node.pool is not None
    # Check that simulation returns a numerical output.
    output = simulate(best_node, 10)
    assert isinstance(output, (int, float))
