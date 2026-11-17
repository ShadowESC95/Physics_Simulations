
import numpy as np
import h5py
import pyvista as pv

def save_h5_field(E, filename):
    with h5py.File(filename, 'w') as f:
        f.create_dataset('E_field', data=E)

def save_vtu_scalar_field(data, filename, name='field'):
    grid = pv.UniformGrid()
    grid.dimensions = np.array(data.shape) + 1
    grid.spacing = (1, 1, 1)
    grid.origin = (0, 0, 0)
    grid.cell_data[name] = data.flatten(order='F')
    grid.save(filename)
