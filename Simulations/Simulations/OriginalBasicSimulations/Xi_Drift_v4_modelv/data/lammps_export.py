# Creating LAMMPS and deal.II export scaffolds

lammps_export_code = """
import numpy as np
import os

def export_to_lammps(data, filename="lammps_data.txt", atom_type=1, box_size=(100, 100, 100)):
    \"""
    Export 3D scalar field (time-independent) as LAMMPS atom data format.
    Each voxel becomes an atom with type and optional charge.
    \"""
    if data.ndim == 4:
        data = data[0]  # Take first frame if time-dependent

    atoms = []
    id_counter = 1
    nx, ny, nz = data.shape
    dx, dy, dz = box_size[0]/nx, box_size[1]/ny, box_size[2]/nz

    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                x, y, z = i * dx, j * dy, k * dz
                charge = data[i, j, k]
                atoms.append((id_counter, atom_type, charge, x, y, z))
                id_counter += 1

    with open(filename, "w") as f:
        f.write("LAMMPS data file via exporter\\n\\n")
        f.write(f"{len(atoms)} atoms\\n")
        f.write(f"{atom_type} atom types\\n\\n")
        f.write(f"0 {box_size[0]} xlo xhi\\n")
        f.write(f"0 {box_size[1]} ylo yhi\\n")
        f.write(f"0 {box_size[2]} zlo zhi\\n\\n")

        f.write("Masses\\n\\n")
        f.write(f"{atom_type} 1.0\\n\\n")

        f.write("Atoms\\n\\n")
        for atom in atoms:
            f.write(f"{atom[0]} {atom[1]} {atom[3]:.3f} {atom[4]:.3f} {atom[5]:.3f}\\n")

        f.write("\\nCharges\\n\\n")
        for atom in atoms:
            f.write(f"{atom[0]} {atom[2]:.6f}\\n")
