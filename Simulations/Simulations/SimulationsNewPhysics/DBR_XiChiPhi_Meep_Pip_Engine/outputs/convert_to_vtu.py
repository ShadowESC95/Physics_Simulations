import h5py
import numpy as np
import pyvista as pv

with h5py.File("E_field.h5", "r") as f:
    data = np.array(f["E_field"])

Nx, Ny, Nz = data.shape
x = np.arange(Nx)
y = np.arange(Ny)
z = np.arange(Nz)
xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")

points = np.c_[xx.ravel(), yy.ravel(), zz.ravel()]
values = data.ravel(order="F")

cloud = pv.PolyData(points)
cloud["Ez"] = values

cloud.save("E_field.vtu")

