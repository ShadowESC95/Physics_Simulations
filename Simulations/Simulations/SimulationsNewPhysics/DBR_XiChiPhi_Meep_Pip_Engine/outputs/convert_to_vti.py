import h5py
import numpy as np
import pyvista as pv

# Load Ez field from HDF5
with h5py.File("E_field.h5", "r") as f:
    key = list(f.keys())[0]
    data = f[key][()]

print(f"Loaded {key} with shape {data.shape} and range: {data.min()} to {data.max()}")

# Define grid dimensions and spacing
nx, ny, nz = data.shape
spacing = (1.0, 1.0, 1.0)

# Create the ImageData grid
grid = pv.ImageData(dimensions=(nx + 1, ny + 1, nz + 1))  # VTK expects +1 for cells
grid.spacing = spacing
grid.origin = (0.0, 0.0, 0.0)

# Assign data to the grid as a cell array (not point array)
grid.cell_data["Ez"] = data.ravel(order="F")

# Save to .vti
grid.save("E_field.vti")
print("Saved: E_field.vti")

