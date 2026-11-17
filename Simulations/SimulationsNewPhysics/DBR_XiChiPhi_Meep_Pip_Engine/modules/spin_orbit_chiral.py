import numpy as np
def chiral_tensor_field(shape):
    Nx, Ny, Nz = shape
    chi_tensor = np.zeros((Nx, Ny, Nz, 3))
    chi_tensor[..., 0] = np.sin(np.linspace(0, 2*np.pi, Nx))[:, None, None]
    chi_tensor[..., 1] = np.cos(np.linspace(0, 2*np.pi, Ny))[None, :, None]
    chi_tensor[..., 2] = np.sin(np.linspace(0, 2*np.pi, Nz))[None, None, :]
    return chi_tensor
