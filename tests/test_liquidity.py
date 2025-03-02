#!/usr/bin/env python
# tests/test_liquidity.py

import pytest
from core.liquidity import (
    fetch_uniswap_liquidity,
    fetch_pancakeswap_liquidity,
    fetch_injective_liquidity,
    fetch_all_liquidity,
)

def test_fetch_uniswap_liquidity():
    pair_address = "0xUniswapPairAddress"
    liquidity = fetch_uniswap_liquidity(pair_address)
    assert isinstance(liquidity, dict)
    assert "token0" in liquidity
    assert "token1" in liquidity
    assert liquidity["pool"] == "Uniswap"
    assert liquidity["chain"] == "Ethereum"

def test_fetch_pancakeswap_liquidity():
    pair_address = "0xPancakeSwapPairAddress"
    liquidity = fetch_pancakeswap_liquidity(pair_address)
    assert isinstance(liquidity, dict)
    assert "token0" in liquidity
    assert "token1" in liquidity
    assert liquidity["pool"] == "PancakeSwap"
    assert liquidity["chain"] == "BSC"

def test_fetch_injective_liquidity(monkeypatch):
    # For Injective, simulate a successful API response.
    def mock_get(url):
        class MockResponse:
            status_code = 200
            def raise_for_status(self):
                pass
            def json(self):
                return {"token0": 200, "token1": 200}
        return MockResponse()
    monkeypatch.setattr("core.liquidity.requests.get", mock_get)
    pair_id = "injective_pair_01"
    liquidity = fetch_injective_liquidity(pair_id)
    assert isinstance(liquidity, dict)
    assert "token0" in liquidity
    assert "token1" in liquidity
    assert liquidity["pool"] == "Injective"
    assert liquidity["chain"] == "Injective"

def test_fetch_all_liquidity():
    liquidity_list = fetch_all_liquidity()
    assert isinstance(liquidity_list, list)
    # At least one liquidity pool should be returned.
    assert len(liquidity_list) >= 1
