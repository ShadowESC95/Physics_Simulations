import h5py
import numpy as np
import pyvista as pv

# Load the data from the correct key
with h5py.File("E_field.h5", "r") as f:
    data = f["E_field"][:]

print("Loaded E_field with shape:", data.shape, "min:", data.min(), "max:", data.max())

# Grid definition: size and spacing
Nx, Ny, Nz = data.shape
spacing = (1.0, 1.0, 1.0)  # Adjust if non-uniform spatial domain in Meep
origin = (0, 0, 0)         # You can shift this if necessary for Ξ–χ–φ alignment

grid = pv.ImageData(dimensions=(Nx+1, Ny+1, Nz+1))
grid.origin = origin
grid.spacing = spacing

# Flatten and attach scalar field (in Fortran order)
grid["Ez"] = data.ravel(order="F")

grid.save("E_field.vti")
print("Saved corrected E_field.vti")

