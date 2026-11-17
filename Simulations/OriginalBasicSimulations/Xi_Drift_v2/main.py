# main.py

import os
import torch
import numpy as np

from config import GRID_SIZE, TIME_STEPS, DT, INIT_NOISE, DRIFT_EPSILON, DEVICE, CHI_COUPLING
from engine.utils import init_field, laplacian
from engine.entropy import compute_entropy
from engine.drift_tensor import compute_drift_tensor
from engine.xi_dynamics import evolve_xi_with_chi
from modules.chi_field import init_chi, evolve_chi_field
from modules.janus_phase_tracker import find_janus_point

print(f"[Ξχ Engine] Running on: {DEVICE}")
os.makedirs("output", exist_ok=True)

# 1. Init Ξ
xi = init_field(GRID_SIZE, INIT_NOISE, device=DEVICE)

# 2. Init χ
chi = init_chi(GRID_SIZE, device=DEVICE)

# 3. Compute DRIFT
drift_tensor = compute_drift_tensor(xi, laplacian)

# 4. Evolve system (Ξ + χ + DRIFT)
xi_log, entropy_log = evolve_xi_with_chi(xi, chi, drift_tensor, TIME_STEPS, DT)

# 5. Evolve χ in post or coupling steps
chi_log = evolve_chi_field(chi, xi_log, coupling_strength=CHI_COUPLING)

# 6. Save outputs
np.save("output/xi_field_log.npy", np.array(xi_log))
np.save("output/chi_field_log.npy", np.array(chi_log))
np.save("output/xi_entropy_log.npy", np.array(entropy_log))
np.save("output/drift_tensor_Xi.npy", drift_tensor.cpu().numpy())

# 7. Find Janus Point
janus_idx, curvature = find_janus_point(entropy_log)
print(f"🪞 Janus point index: {janus_idx}")
np.save("output/janus_idx.npy", np.array([janus_idx]))
