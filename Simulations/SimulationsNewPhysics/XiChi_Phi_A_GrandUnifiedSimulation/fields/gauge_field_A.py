import numpy as np

def initialize_gauge_field(grid_shape, vector_type='zero'):
    """
    Initialize Aμ field with 4 components.

    Args:
        grid_shape (tuple): Spatial grid
        vector_type (str): 'zero', 'radial', 'noise'

    Returns:
        np.ndarray: Aμ(x, y, z, t) with shape (x, y, z, 4)
    """
    A = np.zeros((*grid_shape, 4))

    if vector_type == 'radial':
        x, y, z = np.indices(grid_shape)
        A[..., 1] = x / np.linalg.norm(x + 1)
        A[..., 2] = y / np.linalg.norm(y + 1)
        A[..., 3] = z / np.linalg.norm(z + 1)
    elif vector_type == 'noise':
        A = np.random.rand(*A.shape)

    return A

def evolve_gauge_field(A, source_term, dt):
    return A + dt * source_term

