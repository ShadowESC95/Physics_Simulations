# Creating the field_loader.py module to support loading .npy, .vtk, and .hdf5

field_loader_code = """
import os
import numpy as np

try:
    import h5py
except ImportError:
    h5py = None

try:
    import pyvista as pv
except ImportError:
    pv = None


def load_field(path):
    \"\"\"Auto-detect and load field data from .npy, .hdf5, or .vtk.\"\"\"
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    ext = os.path.splitext(path)[1].lower()

    if ext == '.npy':
        return np.load(path)
    elif ext == '.hdf5' or ext == '.h5':
        if not h5py:
            raise ImportError("h5py is required to load HDF5 files.")
        with h5py.File(path, 'r') as f:
            dataset = next(iter(f.values()))
            return dataset[()]
    elif ext == '.vtk':
        if not pv:
            raise ImportError("pyvista is required to load VTK files.")
        mesh = pv.read(path)
        return mesh.point_data[mesh.point_data.keys()[0]]
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
"""

# Save the module to file
field_loader_path = "/mnt/data/field_loader.py"
with open(field_loader_path, "w") as f:
    f.write(field_loader_code)

field_loader_path  # Provide the path for download or use in viewer3d.py later
