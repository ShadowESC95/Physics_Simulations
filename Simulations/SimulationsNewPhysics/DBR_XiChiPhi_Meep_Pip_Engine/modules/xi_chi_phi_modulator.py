import numpy as np
def generate_modulated_epsilon(shape, time=0.0):
    Nx, Ny, Nz = shape
    epsilon = np.ones((Nx, Ny, Nz, 3))
    epsilon[..., 0] += 0.2 * np.sin(2 * np.pi * Nx / 32 + time)
    epsilon[..., 1] += 0.2 * np.cos(2 * np.pi * Ny / 32 + time)
    epsilon[..., 2] += 0.2 * np.sin(2 * np.pi * Nz / 32 + time)
    return epsilon
