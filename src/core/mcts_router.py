#!/usr/bin/env python
# src/core/mcts_router.py

import math
import random
import json

# Import the liquidity aggregation module.
# Ensure that the liquidity.py file is in the same directory structure (src/core/)
from liquidity import fetch_all_liquidity

# -----------------------------
# MCTS Node Definition
# -----------------------------
class MCTSNode:
    def __init__(self, pool=None, parent=None):
        """
        Each node represents a state in our routing decision.
        For the MVP, a state is simply a liquidity pool (i.e. a potential route).
        The root node will have no pool assigned.
        """
        self.pool = pool            # Dictionary representing the liquidity pool (from liquidity aggregation)
        self.parent = parent        # Parent node reference
        self.children = []          # List of child nodes
        self.visits = 0             # Number of times node was visited
        self.reward = 0             # Cumulative reward (i.e. estimated output tokens)

# -----------------------------
# UCT (Upper Confidence Bound for Trees) Calculation
# -----------------------------
def uct_value(total_visits, node):
    if node.visits == 0:
        return float('inf')
    # UCT: average reward plus exploration term
    return (node.reward / node.visits) + math.sqrt(2 * math.log(total_visits) / node.visits)

# -----------------------------
# Selection Phase: Traverse the tree to select a leaf node.
# -----------------------------
def select(node):
    """
    Starting from the current node, recursively select the child with the highest UCT value until a leaf node is reached.
    """
    while node.children:
        node = max(node.children, key=lambda n: uct_value(node.visits, n))
    return node

# -----------------------------
# Expansion Phase: Expand the node by adding all possible liquidity pool routes.
# -----------------------------
def expand(node, available_pools):
    """
    For the root node (which has no pool assigned), create a child for each available liquidity pool.
    For this MVP, we consider each pool as a terminal route (i.e. single hop).
    """
    if node.pool is None:
        for pool in available_pools:
            child = MCTSNode(pool=pool, parent=node)
            node.children.append(child)
    return node.children

# -----------------------------
# Simulation Phase: Simulate a swap using the pool in this node.
# -----------------------------
def simulate(node, swap_input):
    """
    Simulate a token swap using the constant product formula.
    
    Assumes:
      - 'token0' represents the reserve of the input token.
      - 'token1' represents the reserve of the output token.
    Returns the estimated output tokens (reward).
    """
    pool = node.pool
    # If pool data is invalid or there's an error, yield zero reward.
    if not pool or "error" in pool:
        return 0
    
    x = pool["token0"]
    y = pool["token1"]
    # Constant product k = x * y
    k = x * y
    new_x = x + swap_input
    new_y = k / new_x
    output = y - new_y
    return output

# -----------------------------
# Backpropagation Phase: Propagate the simulation result up the tree.
# -----------------------------
def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent

# -----------------------------
# MCTS Algorithm
# -----------------------------
def mcts(root, iterations, swap_input, available_pools):
    """
    Perform MCTS from the root node for a fixed number of iterations.
    Returns the child of the root with the highest average reward.
    """
    # Expand root node if not yet expanded.
    if not root.children:
        expand(root, available_pools)
    
    for _ in range(iterations):
        # Selection: Traverse the tree to select a leaf node.
        node = select(root)
        # Simulation: Evaluate the current node (simulate the swap).
        reward = simulate(node, swap_input)
        # Backpropagation: Update node statistics along the tree.
        backpropagate(node, reward)
    
    # Choose the best route from the root based on highest average reward.
    best_child = max(root.children, key=lambda n: n.reward / n.visits if n.visits > 0 else 0)
    return best_child

# -----------------------------
# Main Function for Testing the MCTS Router
# -----------------------------
def main():
    # Fetch aggregated liquidity pools (from liquidity module)
    available_pools = fetch_all_liquidity()
    
    # Create the root node (represents the initial state with no chosen pool)
    root = MCTSNode()
    
    # Example swap input (e.g., swapping 10 units of token X)
    swap_input = 10
    
    # Define the number of MCTS iterations for the simulation.
    iterations = 1000
    
    # Run MCTS to select the best liquidity pool route.
    best_node = mcts(root, iterations, swap_input, available_pools)
    
    # Output the selected route and the expected output tokens.
    print("Best route selected:")
    print(json.dumps(best_node.pool, indent=4))
    print("Expected output tokens:", simulate(best_node, swap_input))

if __name__ == "__main__":
    main()
