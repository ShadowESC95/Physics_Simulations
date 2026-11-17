# fields/phi_field.py

import numpy as np

def initialize_phi_field(grid_shape, value=0.0):
    """
    Initialize φ Stueckelberg scalar field.
    
    Args:
        grid_shape (tuple): Spatial grid shape
        value (float): Constant or initial φ value
    
    Returns:
        np.ndarray: φ(x, y, z)
    """
    return np.full(grid_shape, value)

def evolve_phi_field(phi, source_term, dt):
    """
    Evolve φ using Euler update.
    """
    return phi + dt * source_term

