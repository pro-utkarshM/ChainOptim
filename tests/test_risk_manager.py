#!/usr/bin/env python
# tests/test_risk_manager.py

import pytest
from core.risk_manager import check_slippage, estimate_gas_price, protect_against_mev

def test_check_slippage():
    expected = 100
    actual = 98
    within_limit, slippage = check_slippage(expected, actual, max_slippage_percent=3)
    assert isinstance(within_limit, bool)
    assert isinstance(slippage, float)
    # With 2% slippage, it should be within a 3% limit.
    assert within_limit is True

def test_estimate_gas_price():
    gas_price = estimate_gas_price(chain="Ethereum")
    # Gas price should be an integer if successfully fetched.
    if gas_price is not None:
        assert isinstance(gas_price, int)

def test_protect_against_mev():
    tx = {"gasPrice": 1000000000}
    modified_tx = protect_against_mev(tx, chain="Ethereum")
    # Modified gasPrice should be at least 20% higher than the original.
    assert modified_tx["gasPrice"] >= int(1000000000 * 1.2)
