# simulation/attractor_analysis.py

import numpy as np

def detect_attractors(field_history, threshold=1e-3):
    """
    Identifies attractor points where the field stabilizes over time.

    Args:
        field_history (list of np.ndarray): Time-sequenced field states
        threshold (float): Maximum allowable change to be considered "attracted"

    Returns:
        np.ndarray: Boolean array where True = attractor region
    """
    if len(field_history) < 2:
        raise ValueError("Need at least two time steps to detect attractors.")
    
    delta = np.abs(field_history[-1] - field_history[-2])
    return delta < threshold

