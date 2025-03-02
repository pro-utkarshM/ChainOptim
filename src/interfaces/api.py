#!/usr/bin/env python
# src/interfaces/api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import necessary modules from our core package.
from core.liquidity import fetch_all_liquidity
from core.mcts_router import mcts, MCTSNode, simulate
from core.execution import execute_swap

app = FastAPI(
    title="DeFAI Terminal API",
    description="API for cross-chain transaction optimization and swap execution",
    version="0.1.0"
)

# -----------------------------
# Pydantic models for request/response
# -----------------------------
class SwapRequest(BaseModel):
    swap_input: int         # Amount of input tokens (in smallest unit)
    from_address: str       # Sender's blockchain address
    private_key: str        # Private key for signing (caution: use secure storage in production)
    chain: str = "Ethereum" # Target chain ("Ethereum", "BSC", or "Injective")

class SwapResponse(BaseModel):
    tx_hash: str            # Transaction hash or error message

# -----------------------------
# API Endpoints
# -----------------------------
@app.get("/liquidity")
def get_liquidity():
    """
    Endpoint to return aggregated liquidity data from all supported sources.
    """
    try:
        data = fetch_all_liquidity()
        return {"liquidity": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/swap", response_model=SwapResponse)
def swap_tokens(request: SwapRequest):
    """
    Endpoint to execute a swap transaction using the best route determined via MCTS.
    """
    try:
        # 1. Fetch aggregated liquidity data.
        liquidity_data = fetch_all_liquidity()

        # 2. Create the root MCTS node and run the algorithm to select the best route.
        root = MCTSNode()
        best_node = mcts(root, iterations=1000, swap_input=request.swap_input, available_pools=liquidity_data)

        if best_node is None or best_node.pool is None:
            raise HTTPException(status_code=400, detail="No valid route found for the swap.")

        best_route = best_node.pool
        # Add expected_output from simulation (used for slippage estimation).
        best_route["expected_output"] = simulate(best_node, request.swap_input)

        # 3. Execute the swap transaction.
        tx_result = execute_swap(best_route, request.swap_input, request.from_address, request.private_key, chain=request.chain)

        return SwapResponse(tx_hash=tx_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the FastAPI app on host 0.0.0.0:8000 using uvicorn.
    uvicorn.run(app, host="0.0.0.0", port=8000)
