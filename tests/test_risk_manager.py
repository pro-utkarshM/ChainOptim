import pytest
from core.risk_manager import check_slippage, estimate_gas_price, protect_against_mev

def test_check_slippage():
    expected = 100
    actual = 98
    within_limit, slippage = check_slippage(expected, actual, max_slippage_percent=3)
    assert isinstance(within_limit, bool)
    assert isinstance(slippage, float)
    assert within_limit is True

def test_estimate_gas_price(monkeypatch):
    """
    Mock the Web3 call to test gas price estimation.
    """
    class MockWeb3:
        class eth:
            gas_price = 1000000000
    
    monkeypatch.setattr("core.risk_manager.web3_providers", {"Ethereum": MockWeb3()})
    gas_price = estimate_gas_price(chain="Ethereum")
    
    assert isinstance(gas_price, int)
    assert gas_price == 1000000000

def test_protect_against_mev(monkeypatch):
    """
    Test if MEV protection correctly modifies the gas price.
    """
    monkeypatch.setattr("core.risk_manager.estimate_gas_price", lambda chain: 1000000000)

    tx = {"gasPrice": 1000000000}
    modified_tx = protect_against_mev(tx, chain="Ethereum")

    assert isinstance(modified_tx, dict)
    assert "gasPrice" in modified_tx
    assert modified_tx["gasPrice"] >= int(1000000000 * 1.2)
