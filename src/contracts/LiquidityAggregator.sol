// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @dev Minimal ERC20 interface.
 */
interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function transfer(address recipient, uint256 amount) external returns (bool);
}

contract LiquidityAggregator {
    address public owner;

    // Mapping for reserves: reserves[tokenA][tokenB] holds reserve of tokenA for the pair (tokenA, tokenB)
    mapping(address => mapping(address => uint256)) public reserves;

    event LiquidityAdded(
        address indexed tokenA,
        address indexed tokenB,
        uint256 amountA,
        uint256 amountB
    );
    event SwapExecuted(
        address indexed inputToken,
        address indexed outputToken,
        uint256 inputAmount,
        uint256 outputAmount,
        address recipient
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "LiquidityAggregator: caller is not the owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @notice Owner adds liquidity to a token pair.
     * @param tokenA Address of token A.
     * @param tokenB Address of token B.
     * @param amountA Amount of token A.
     * @param amountB Amount of token B.
     */
    function addLiquidity(
        address tokenA,
        address tokenB,
        uint256 amountA,
        uint256 amountB
    ) external onlyOwner {
        // In a real implementation, transfer tokens to the contract before updating reserves.
        reserves[tokenA][tokenB] += amountA;
        reserves[tokenB][tokenA] += amountB;
        emit LiquidityAdded(tokenA, tokenB, amountA, amountB);
    }

    /**
     * @notice Executes a swap using a constant product formula.
     * @param inputToken Address of the input token.
     * @param outputToken Address of the output token.
     * @param inputAmount Amount of input tokens to swap.
     * @param minOutput Minimum acceptable output tokens.
     * @param recipient Address that will receive the output tokens.
     * @return outputAmount The amount of output tokens transferred to the recipient.
     */
    function executeSwap(
        address inputToken,
        address outputToken,
        uint256 inputAmount,
        uint256 minOutput,
        address recipient
    ) external returns (uint256 outputAmount) {
        // Transfer input tokens from the caller to this contract.
        require(IERC20(inputToken).transferFrom(msg.sender, address(this), inputAmount), "LiquidityAggregator: transfer failed");

        uint256 reserveIn = reserves[inputToken][outputToken];
        uint256 reserveOut = reserves[outputToken][inputToken];
        require(reserveIn > 0 && reserveOut > 0, "LiquidityAggregator: insufficient liquidity");

        // Constant product formula: output = reserveOut - (reserveIn * reserveOut / (reserveIn + inputAmount))
        uint256 newReserveIn = reserveIn + inputAmount;
        uint256 newReserveOut = (reserveIn * reserveOut) / newReserveIn;
        outputAmount = reserveOut - newReserveOut;

        require(outputAmount >= minOutput, "LiquidityAggregator: output less than minimum");

        // Update reserves.
        reserves[inputToken][outputToken] = newReserveIn;
        reserves[outputToken][inputToken] = newReserveOut;

        // Transfer output tokens to the recipient.
        require(IERC20(outputToken).transfer(recipient, outputAmount), "LiquidityAggregator: output transfer failed");

        emit SwapExecuted(inputToken, outputToken, inputAmount, outputAmount, recipient);
    }
}
