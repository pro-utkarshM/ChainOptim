#!/usr/bin/env python
# src/core/utils.py

import logging
import sys
from decimal import Decimal

def setup_logger(name=__name__, level=logging.INFO):
    """
    Set up and return a logger with the given name and logging level.
    
    :param name: Name of the logger.
    :param level: Logging level (default: INFO).
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create a console handler and set the logging format.
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    
    # Avoid duplicate handlers if the logger already has one.
    if not logger.handlers:
        logger.addHandler(ch)
    
    return logger

def convert_to_wei(amount, decimals=18):
    """
    Convert a human-friendly token amount to Wei (smallest unit).
    
    :param amount: Token amount (float or Decimal).
    :param decimals: Token decimals (default: 18).
    :return: Integer amount in Wei.
    """
    return int(Decimal(amount) * (10 ** decimals))

def convert_from_wei(amount, decimals=18):
    """
    Convert an amount in Wei to a human-friendly token amount.
    
    :param amount: Amount in Wei (integer).
    :param decimals: Token decimals (default: 18).
    :return: Decimal token amount.
    """
    return Decimal(amount) / (10 ** decimals)

# Example usage for testing utilities.
if __name__ == "__main__":
    logger = setup_logger("DeFAI-Terminal")
    logger.info("Logger initialized.")

    # Test conversion functions.
    token_amount = 1.5  # For example, 1.5 tokens.
    wei_amount = convert_to_wei(token_amount)
    logger.info(f"{token_amount} tokens in Wei: {wei_amount}")

    recovered_amount = convert_from_wei(wei_amount)
    logger.info(f"Recovered token amount from Wei: {recovered_amount}")
