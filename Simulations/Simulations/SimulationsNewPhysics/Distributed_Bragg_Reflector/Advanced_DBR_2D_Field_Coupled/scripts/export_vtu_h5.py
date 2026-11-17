
import numpy as np
import h5py
import pyvista as pv

# Load 3D grid (example: permittivity)
eps = np.load("epsilon_modulated_3d.npy")
Nx, Ny, Nz = eps.shape

# Create spatial grid
x = np.linspace(0, 16, Nx)
y = np.linspace(0, 8, Ny)
z = np.linspace(0, 4, Nz)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Save to HDF5
with h5py.File("epsilon_export.h5", "w") as f:
    f.create_dataset("epsilon", data=eps)
    f.create_dataset("x", data=x)
    f.create_dataset("y", data=y)
    f.create_dataset("z", data=z)

# Save to .vtu using PyVista
grid = pv.StructuredGrid(X, Y, Z)
grid["epsilon"] = eps.flatten(order="F")
grid.save("epsilon_export.vtu")
