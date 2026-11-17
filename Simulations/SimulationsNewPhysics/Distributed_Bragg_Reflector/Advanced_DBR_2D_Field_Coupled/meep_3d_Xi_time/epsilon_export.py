
import numpy as np
import h5py
import pyvista as pv

def export_epsilon(epsilon_3d, filename_prefix="epsilon"):
    Nx, Ny, Nz = epsilon_3d.shape
    x = np.linspace(0, 16, Nx)
    y = np.linspace(0, 8, Ny)
    z = np.linspace(0, 4, Nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

    # Export to HDF5
    with h5py.File(f"{filename_prefix}.h5", "w") as f:
        f.create_dataset("epsilon", data=epsilon_3d)
        f.create_dataset("x", data=x)
        f.create_dataset("y", data=y)
        f.create_dataset("z", data=z)

    # Export to .vtu
    grid = pv.StructuredGrid(X, Y, Z)
    grid["epsilon"] = epsilon_3d.flatten(order="F")
    grid.save(f"{filename_prefix}.vtu")
