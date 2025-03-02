#!/usr/bin/env python
# src/config.py

import os
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Blockchain RPC endpoints
ETH_RPC = os.getenv("ETH_RPC")
BSC_RPC = os.getenv("BSC_RPC")
INJECTIVE_RPC = os.getenv("INJECTIVE_RPC")

# SwapRouter smart contract details
SWAP_ROUTER_ADDRESS = os.getenv("SWAP_ROUTER_ADDRESS")
SWAP_ROUTER_ABI = json.loads(os.getenv("SWAP_ROUTER_ABI"))

# Additional configuration parameters can be added here.
