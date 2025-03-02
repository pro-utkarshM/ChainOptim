// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ILiquidityAggregator {
    /**
     * @notice Executes a token swap.
     * @param inputToken Address of the input ERC20 token.
     * @param outputToken Address of the output ERC20 token.
     * @param inputAmount Amount of input tokens to swap.
     * @param minOutput Minimum acceptable output tokens.
     * @param recipient Address that will receive the output tokens.
     * @return outputAmount The actual amount of output tokens received.
     */
    function executeSwap(
        address inputToken,
        address outputToken,
        uint256 inputAmount,
        uint256 minOutput,
        address recipient
    ) external returns (uint256 outputAmount);
}

contract SwapRouter {
    // Address of the LiquidityAggregator contract.
    address public aggregator;

    event SwapInitiated(
        address indexed inputToken,
        address indexed outputToken,
        uint256 inputAmount,
        uint256 minOutput,
        address recipient,
        uint256 outputAmount
    );

    /**
     * @dev Sets the LiquidityAggregator address upon deployment.
     * @param _aggregator Address of the LiquidityAggregator contract.
     */
    constructor(address _aggregator) {
        require(_aggregator != address(0), "SwapRouter: aggregator cannot be zero address");
        aggregator = _aggregator;
    }

    /**
     * @notice Executes a token swap via the LiquidityAggregator.
     * @param inputToken Address of the input token.
     * @param outputToken Address of the output token.
     * @param inputAmount Amount of input tokens to swap.
     * @param minOutput Minimum acceptable output tokens.
     * @param recipient Address to receive the output tokens.
     * @param deadline Timestamp by which the transaction must be mined.
     * @return outputAmount The amount of output tokens received.
     */
    function swapExactTokens(
        address inputToken,
        address outputToken,
        uint256 inputAmount,
        uint256 minOutput,
        address recipient,
        uint256 deadline
    ) external returns (uint256 outputAmount) {
        require(block.timestamp <= deadline, "SwapRouter: transaction expired");
        // In a real implementation, input tokens should be transferred to this contract,
        // then approved for the aggregator. For simplicity, we assume the caller has approved
        // the aggregator to spend the tokens on their behalf.

        outputAmount = ILiquidityAggregator(aggregator).executeSwap(
            inputToken,
            outputToken,
            inputAmount,
            minOutput,
            recipient
        );

        require(outputAmount >= minOutput, "SwapRouter: insufficient output amount");
        emit SwapInitiated(inputToken, outputToken, inputAmount, minOutput, recipient, outputAmount);
    }
}
