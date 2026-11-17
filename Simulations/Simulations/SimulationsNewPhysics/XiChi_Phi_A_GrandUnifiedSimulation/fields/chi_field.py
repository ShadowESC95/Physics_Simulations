import numpy as np

def initialize_chi_field(grid_shape, coherence_pattern='sinusoidal', phase=0.0):
    """
    Initialize χ coherence field.

    Args:
        grid_shape (tuple): Shape of the simulation grid
        coherence_pattern (str): Pattern: 'sinusoidal', 'uniform', 'noise'
        phase (float): Phase offset
    
    Returns:
        np.ndarray: χ(x, y, z)
    """
    x, y, z = np.indices(grid_shape)
    if coherence_pattern == 'sinusoidal':
        return 0.5 * (1 + np.sin(2 * np.pi * x / grid_shape[0] + phase))
    elif coherence_pattern == 'uniform':
        return np.ones(grid_shape)
    elif coherence_pattern == 'noise':
        return np.random.rand(*grid_shape)
    else:
        raise ValueError("Invalid pattern for χ")

def evolve_chi_field(chi, source_term, dt):
    """
    Evolve χ with Euler step.
    """
    return chi + dt * source_term

