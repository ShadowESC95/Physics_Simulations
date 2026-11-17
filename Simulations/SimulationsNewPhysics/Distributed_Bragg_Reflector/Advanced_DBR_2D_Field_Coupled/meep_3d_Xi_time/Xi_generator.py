
import numpy as np

def generate_Xi(Nx, Ny, Nz, Nt, center_t, sigma_t):
    Xi = np.zeros((Nt, Nx, Ny, Nz))
    X = np.linspace(0, 1, Nx)
    Y = np.linspace(0, 1, Ny)
    Z = np.linspace(0, 1, Nz)
    X3D, Y3D, Z3D = np.meshgrid(X, Y, Z, indexing='ij')
    spatial = np.exp(-((X3D - 0.5)**2 + (Y3D - 0.5)**2 + (Z3D - 0.5)**2) / 0.05)

    for t in range(Nt):
        temporal = np.exp(-((t - center_t)**2) / (2 * sigma_t**2))
        Xi[t] = spatial * temporal
    return Xi
