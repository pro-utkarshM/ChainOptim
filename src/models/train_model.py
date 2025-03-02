#!/usr/bin/env python
# src/models/train_model.py

import gym
import numpy as np
from gym import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

class SwapEnv(gym.Env):
    """
    A custom environment for simulating slippage prediction and route selection.
    
    Observation:
      A 3-dimensional vector representing:
        - liquidity: available liquidity (0 to 1000)
        - volatility: market volatility (0 to 1)
        - previous_slippage: previous slippage percentage (0 to 100)
    
    Action:
      Discrete action space with 3 routes (0, 1, 2).
    
    Reward:
      Negative slippage. Lower slippage (i.e. higher reward) is desired.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SwapEnv, self).__init__()
        # Define observation space: [liquidity, volatility, previous_slippage]
        self.observation_space = spaces.Box(low=np.array([0, 0, 0]),
                                            high=np.array([1000, 1, 100]),
                                            dtype=np.float32)
        # Define a discrete action space: 3 possible routes.
        self.action_space = spaces.Discrete(3)
        self.state = None
        self.step_count = 0
        self.max_steps = 50

    def reset(self):
        # Initialize state with random values within a plausible range.
        self.state = np.array([
            np.random.uniform(100, 900),  # liquidity
            np.random.uniform(0.1, 0.9),  # volatility
            np.random.uniform(0, 20)      # previous_slippage
        ], dtype=np.float32)
        self.step_count = 0
        return self.state

    def step(self, action):
        liquidity, volatility, prev_slippage = self.state
        # Simulate the effect of different routing strategies:
        if action == 0:
            # Route 0: Moderate improvement.
            slippage = max(prev_slippage - np.random.uniform(1, 5), 0)
        elif action == 1:
            # Route 1: Often the best improvement.
            slippage = max(prev_slippage - np.random.uniform(3, 8), 0)
        elif action == 2:
            # Route 2: Little improvement.
            slippage = max(prev_slippage - np.random.uniform(0, 2), 0)
        # Reward is the negative slippage (lower slippage yields higher reward).
        reward = -slippage
        # Update the state: slightly modify liquidity and volatility and update slippage.
        next_state = np.array([
            np.clip(liquidity + np.random.uniform(-10, 10), 0, 1000),
            np.clip(volatility + np.random.uniform(-0.05, 0.05), 0, 1),
            slippage
        ], dtype=np.float32)
        self.state = next_state
        self.step_count += 1
        done = self.step_count >= self.max_steps
        info = {}
        return self.state, reward, done, info

    def render(self, mode='human'):
        print(f"State: {self.state}")

if __name__ == "__main__":
    # Create the environment and verify its compliance with Gym's API.
    env = SwapEnv()
    check_env(env)
    
    # Create and train the PPO agent.
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    
    # Save the trained model.
    model.save("swap_model")
    print("Model saved as 'swap_model.zip'.")
