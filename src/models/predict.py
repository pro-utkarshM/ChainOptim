#!/usr/bin/env python
# src/models/predict.py

import numpy as np
from stable_baselines3 import PPO
from train_model import SwapEnv  # Import our custom environment

def predict_best_route(observation):
    """
    Given an observation, predict the best execution route (action) using the trained model.
    
    :param observation: A numpy array representing the environment's state.
    :return: The predicted action (route index).
    """
    # Load the trained model.
    model = PPO.load("swap_model")
    
    # Predict the best action for the given observation.
    action, _ = model.predict(observation, deterministic=True)
    return action

if __name__ == "__main__":
    # Create the environment and reset to get an initial observation.
    env = SwapEnv()
    observation = env.reset()
    
    print("Current observation (state):", observation)
    
    # Predict the best route.
    best_route = predict_best_route(observation)
    print("Predicted best route (action):", best_route)
