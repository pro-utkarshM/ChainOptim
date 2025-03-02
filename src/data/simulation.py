#!/usr/bin/env python
# src/data/simulation.py

def simulate_trade_execution(input_amount, reserve_in, reserve_out):
    """
    Simulate trade execution using a Constant Product Market Maker (CPMM) formula.
    
    :param input_amount: Amount of input tokens to swap.
    :param reserve_in: Current reserve of the input token in the pool.
    :param reserve_out: Current reserve of the output token in the pool.
    :return: Output token amount received after the swap.
    """
    # Calculate the constant product (k)
    k = reserve_in * reserve_out
    new_reserve_in = reserve_in + input_amount
    new_reserve_out = k / new_reserve_in
    output_amount = reserve_out - new_reserve_out
    return output_amount

def calculate_slippage(input_amount, reserve_in, reserve_out):
    """
    Calculate slippage for a given trade by comparing the ideal (no slippage) output
    to the actual output computed via CPMM simulation.
    
    :param input_amount: Amount of input tokens to swap.
    :param reserve_in: Reserve of input tokens.
    :param reserve_out: Reserve of output tokens.
    :return: Tuple (ideal_output, actual_output, slippage_percent)
    """
    # Ideal output: if the price were constant (no price impact)
    ideal_output = input_amount * (reserve_out / reserve_in)
    actual_output = simulate_trade_execution(input_amount, reserve_in, reserve_out)
    if ideal_output == 0:
        slippage_percent = 0
    else:
        slippage_percent = ((ideal_output - actual_output) / ideal_output) * 100
    return ideal_output, actual_output, slippage_percent

if __name__ == "__main__":
    # Example simulation:
    input_amount = 10       # Tokens to swap
    reserve_in = 100        # Input token reserve in the pool
    reserve_out = 100       # Output token reserve in the pool
    
    ideal, actual, slippage = calculate_slippage(input_amount, reserve_in, reserve_out)
    print(f"Ideal Output: {ideal}")
    print(f"Actual Output: {actual}")
    print(f"Slippage: {slippage:.2f}%")
