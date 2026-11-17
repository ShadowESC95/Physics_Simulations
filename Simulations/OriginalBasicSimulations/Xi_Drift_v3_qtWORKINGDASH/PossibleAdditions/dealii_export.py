import numpy as np
import h5py
import os

def export_to_hdf5(data, filename="dealii_field.h5", dataset_name="field"):
    """
    Export 3D field or 4D time-series to HDF5 for deal.II-compatible input.
    """
    with h5py.File(filename, "w") as f:
        f.create_dataset(dataset_name, data=data)

def export_to_vtk_placeholder(data, filename="dealii_field.vtk"):
    """
    Placeholder for exporting to VTK for deal.II visual checks.
    Recommend replacing with pyvista or meshio in production.
    """
    np.savetxt(filename, data.reshape(-1), header="VTK dump placeholder - reshape manually if needed")