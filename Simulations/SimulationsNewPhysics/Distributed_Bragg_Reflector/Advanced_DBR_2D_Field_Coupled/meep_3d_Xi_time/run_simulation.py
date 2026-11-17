
import numpy as np
import json
from Xi_generator import generate_Xi
from epsilon_export import export_epsilon

with open("config.json") as f:
    cfg = json.load(f)

Nx, Ny, Nz = cfg["Nx"], cfg["Ny"], cfg["Nz"]
Nt = cfg["simulation_time"]
Xi = generate_Xi(Nx, Ny, Nz, Nt, cfg["Xi_decay_center"], cfg["Xi_decay_sigma"])

# Generate permittivity at midpoint t
alpha_Xi = cfg["alpha_Xi"]
epsilon = cfg["epsilon_base"] + alpha_Xi * Xi[Nt//2]

# Export ε(x, y, z) snapshot
export_epsilon(epsilon, filename_prefix="outputs/epsilon_snapshot")
