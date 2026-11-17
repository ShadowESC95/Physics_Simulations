import numpy as np
import pyvista as pv

def save_vtk(field, name="xi", out="output/xi_field.vtk"):
    grid = pv.UniformGrid()
    shape = field.shape
    grid.dimensions = np.array(shape) + 1
    grid.origin = (0, 0, 0)
    grid.spacing = (1/shape[0], 1/shape[1], 1/shape[2] if len(shape) == 3 else 1)

    grid.cell_data[name] = field.flatten(order="F")
    grid.save(out)
