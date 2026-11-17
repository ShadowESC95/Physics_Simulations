# -- OPENFOAM EXPORTER --
openfoam_export_code = """
import os
import numpy as np

def export_openfoam_field(data, field_name="Xi", time_step="0", output_dir="openfoam_case"):
    if data.ndim == 4:
        data = data[0]

    nx, ny, nz = data.shape
    os.makedirs(os.path.join(output_dir, time_step), exist_ok=True)

    field_file = os.path.join(output_dir, time_step, field_name)
    with open(field_file, "w") as f:
        f.write(f"FoamFile\\n{{\\n    version     2.0;\\n    format      ascii;\\n    class       volScalarField;\\n    location    \\"{time_step}\\";\\n    object      {field_name};\\n}}\\n")
        f.write(f"dimensions      [0 0 0 0 0 0 0];\\n")
        f.write(f"internalField   nonuniform List<scalar>\\n{nx * ny * nz}\\n(")
        flat_data = data.flatten()
        for val in flat_data:
            f.write(f"\\n{val:.6e}")
        f.write("\\n);\\nboundaryField\\n{\\n    defaultFaces\\n    {\\n        type zeroGradient;\\n    }\\n}\\n")
"""

# Write all files
test_dir = "/mnt/data/tests"
os.makedirs(test_dir, exist_ok=True)

with open(f"{test_dir}/test_loader.py", "w") as f:
    f.write(test_loader_code.strip())

with open(f"{test_dir}/test_lammps_export.py", "w") as f:
    f.write(test_lammps_code.strip())

with open(f"{test_dir}/test_dealii_export.py", "w") as f:
    f.write(test_dealii_code.strip())

openfoam_export_path = "/mnt/data/openfoam_export.py"
with open(openfoam_export_path, "w") as f:
    f.write(openfoam_export_code.strip())

test_dir, openfoam_export_path
