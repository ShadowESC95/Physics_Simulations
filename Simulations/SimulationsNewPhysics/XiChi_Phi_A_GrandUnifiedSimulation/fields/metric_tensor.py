# fields/metric_tensor.py

import numpy as np

def initialize_flat_metric(grid_shape):
    """
    Returns a flat Minkowski metric ημν in 4D space-time.

    Returns:
        np.ndarray: Shape (x, y, z, 4, 4) with ημν at every point
    """
    g = np.zeros((*grid_shape, 4, 4))
    for mu in range(4):
        for nu in range(4):
            g[..., mu, nu] = 0
    g[..., 0, 0] = -1  # time
    g[..., 1, 1] = 1
    g[..., 2, 2] = 1
    g[..., 3, 3] = 1
    return g

