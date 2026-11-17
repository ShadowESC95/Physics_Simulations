def export_vtu(fields, timestep, config):
    import meshio
    import numpy as np
    import os

    output_dir = config.get("output_dir", "output")
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"fields_t{timestep:05d}.vtu")

    # Extract spatial dimensions
    grid_size = config.get("grid_size", [64, 64, 64, 64])
    if len(grid_size) != 4:
        raise ValueError("grid_size must be a 4-element list: [T, Nx, Ny, Nz]")

    _, nx, ny, nz = grid_size
    spacing = config.get("grid_spacing", 1.0)

    points = np.array([
        [i * spacing, j * spacing, k * spacing]
        for i in range(nx) for j in range(ny) for k in range(nz)
    ])
    cells = [("vertex", np.arange(len(points)).reshape(-1, 1))]

    expected_len = len(points)
    field_data = {}

    for name, array in fields.items():
        try:
            if array.ndim == 5 and name == "A_mu":
                print(f"[export_vtu] A_mu shape = {array.shape}")
                for mu in range(4):
                    sliced = array[timestep, mu]
                    flat = sliced.flatten()
                    if flat.dtype == object:
                        raise ValueError(f"A{mu} contains non-numeric values")
                    if len(flat) != expected_len:
                        raise ValueError(f"A{mu} length {len(flat)} != expected {expected_len}")
                    field_data[f"A{mu}"] = flat.astype(np.float32)

            elif array.ndim == 4:
                sliced = array[timestep]
                flat = sliced.flatten()
                if flat.dtype == object:
                    raise ValueError(f"{name} contains non-numeric values")
                if len(flat) != expected_len:
                    raise ValueError(f"{name} length {len(flat)} != expected {expected_len}")
                field_data[name] = flat.astype(np.float32)

            else:
                print(f"[export_vtu] Skipped {name} (unexpected shape {array.shape})")

        except Exception as e:
            print(f"[export_vtu] Warning: skipping {name} ({e})")

    mesh = meshio.Mesh(points=points, cells=cells, point_data=field_data)
    mesh.write(filename)
    print(f"[export_vtu] Exported timestep {timestep} to {filename}")

