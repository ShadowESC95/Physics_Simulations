# simulation/symmetry_breaking_tracker.py

import numpy as np

def compute_symmetry_breaking(field, axis='x'):
    """
    Tracks symmetry breaking by comparing halves of the domain.

    Args:
        field (np.ndarray): Scalar or vector field
        axis (str): 'x', 'y', or 'z'

    Returns:
        float: Symmetry deviation metric (0 = perfectly symmetric)
    """
    axis_map = {'x': 0, 'y': 1, 'z': 2}
    idx = axis_map.get(axis.lower(), 0)
    mid = field.shape[idx] // 2

    first_half = np.take(field, indices=range(mid), axis=idx)
    second_half = np.take(field, indices=range(field.shape[idx]-1, mid-1, -1), axis=idx)
    deviation = np.abs(first_half - second_half)

    return np.mean(deviation)

