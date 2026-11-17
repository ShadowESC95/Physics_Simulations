import numpy as np
import pyvista as pv

class VTKExporter:
    def save(self, data: np.ndarray, filename="results.vtk"):
        grid = pv.UniformGrid()
        grid.dimensions = np.array(data.shape) + 1
        grid.point_arrays["values"] = data.flatten(order="F")
        grid.save(filename)
