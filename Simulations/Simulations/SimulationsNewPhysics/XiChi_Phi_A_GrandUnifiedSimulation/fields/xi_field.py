import numpy as np

def initialize_xi_field(grid_shape, amplitude=1.0, seed=None):
    """
    Initialize the Ξ entropy scalar field.
    
    Args:
        grid_shape (tuple): Shape of the simulation grid (x, y, z)
        amplitude (float): Max value of entropy field
        seed (int): Optional random seed
    
    Returns:
        np.ndarray: Initialized Ξ(x, y, z) field
    """
    if seed is not None:
        np.random.seed(seed)
    
    return amplitude * np.random.rand(*grid_shape)

def evolve_xi_field(xi, source_term, dt):
    """
    Time evolution of the Ξ field using forward Euler update.
    
    Args:
        xi (np.ndarray): Current Ξ field
        source_term (np.ndarray): ∂Ξ/∂t from PDEs
        dt (float): Timestep
    
    Returns:
        np.ndarray: Updated Ξ field
    """
    return xi + dt * source_term

