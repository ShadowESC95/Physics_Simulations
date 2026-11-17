import numpy as np
import os

def export_csv_for_openfoam(field, filename, axis_labels=["x", "y", "z"], origin=(-10, -10, 0), spacing=(0.2, 0.2, 0.2)):
    nx, ny = field.shape
    dx, dy, dz = spacing
    ox, oy, oz = origin

    with open(filename, "w") as f:
        f.write(",".join(axis_labels) + ",value\n")
        for i in range(nx):
            for j in range(ny):
                x = ox + i * dx
                y = oy + j * dy
                f.write(f"{x},{y},{oz},{field[i, j]}\n")

if __name__ == "__main__":
    xi = np.load("output/xi_field_log.npy")[0]
    export_csv_for_openfoam(xi, "openfoam_export_xi.csv")
