#!/usr/bin/env python
# tests/test_utils.py

import pytest
from core.utils import convert_to_wei, convert_from_wei, setup_logger
from decimal import Decimal

def test_convert_to_from_wei():
    amount = 1.5
    wei_amount = convert_to_wei(amount)
    recovered = convert_from_wei(wei_amount)
    # The recovered amount should approximately equal the original.
    assert abs(recovered - Decimal(amount)) < Decimal("1e-6")

def test_setup_logger():
    logger = setup_logger("TestLogger", level=0)
    # Check that the returned logger is an instance of logging.Logger.
    import logging
    assert isinstance(logger, logging.Logger)
