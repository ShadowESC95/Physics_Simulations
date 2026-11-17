
import numpy as np

def generate_modulated_epsilon(shape, time):
    Nx, Ny, Nz = shape
    epsilon = np.ones((Nx, Ny, Nz, 3))
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                t_factor = 1 + 0.1 * np.sin(2 * np.pi * time / 100)
                epsilon[i, j, k] = np.array([1.0, 1.0 + 0.05 * np.sin(k), 1.0 + 0.05 * np.cos(j)]) * t_factor
    return epsilon
