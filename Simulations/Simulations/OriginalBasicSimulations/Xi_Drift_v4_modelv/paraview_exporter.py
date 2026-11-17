import numpy as np
import pyvista as pv

class ParaViewExporter:
    def save(self, data: np.ndarray, filename="paraview_output.vtk"):
        grid = pv.StructuredGrid()
        x, y = np.meshgrid(np.arange(data.shape[0]), np.arange(data.shape[0]))
        z = data
        grid.points = np.c_[x.ravel(), y.ravel(), z.ravel()]
        grid["values"] = z.ravel()
        grid.save(filename)
