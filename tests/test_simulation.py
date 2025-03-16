#!/usr/bin/env python
# tests/test_simulation.py

import pytest
from data.simulation import simulate_trade_execution, calculate_slippage

def test_simulate_trade_execution():
    input_amount = 10
    reserve_in = 100
    reserve_out = 100
    output = simulate_trade_execution(input_amount, reserve_in, reserve_out)
    # Output should be greater than zero and less than reserve_out.
    assert output > 0
    assert output < reserve_out

def test_calculate_slippage():
    input_amount = 10
    reserve_in = 100
    reserve_out = 100
    ideal, actual, slippage = calculate_slippage(input_amount, reserve_in, reserve_out)
    # Ideal output should be positive, actual output should be positive, and slippage non-negative.
    assert ideal > 0
    assert actual > 0
    assert slippage >= 0
