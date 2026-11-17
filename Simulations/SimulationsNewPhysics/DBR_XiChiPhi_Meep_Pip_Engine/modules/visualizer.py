import numpy as np
import h5py
import pyvista as pv
from pyvistaqt import BackgroundPlotter

def save_h5_field(data, path):
    with h5py.File(path, "w") as f:
        f.create_dataset("E_field", data=data)

def load_h5_field(h5_path):
    with h5py.File(h5_path, "r") as f:
        return f["E_field"][()]

def export_vti(field_data, out_path="E_field.vti"):
    grid = pv.UniformGrid()
    grid.dimensions = field_data.shape
    grid.spacing = (1, 1, 1)
    grid.point_data["E_field"] = field_data.flatten(order="F")
    grid.save(out_path)

def show_slice(field_data, axis='z', index=32):
    plotter = BackgroundPlotter()
    grid = pv.UniformGrid(dimensions=field_data.shape,
                          spacing=(1,1,1))
    grid.point_data["E"] = field_data.flatten(order="F")
    if axis == 'z':
        slice = grid.slice(normal='z', origin=(0, 0, index))
    elif axis == 'x':
        slice = grid.slice(normal='x', origin=(index, 0, 0))
    else:
        slice = grid.slice(normal='y', origin=(0, index, 0))
    plotter.add_mesh(slice, cmap="plasma")
    plotter.show()

