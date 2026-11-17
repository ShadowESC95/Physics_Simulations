# main.py
import os
import torch
import numpy as np
from config import GRID_SIZE, TIME_STEPS, DT, DRIFT_EPSILON, CHI_COUPLING, DEVICE, ENTROPY_LOG_INTERVAL
from engine.utils import init_field, laplacian
from engine.entropy import compute_entropy
from engine.drift_tensor import compute_drift_tensor
from modules.chi_field import init_chi, evolve_chi_field
from modules.janus_phase_tracker import find_janus_point
from engine.xi_dynamics import evolve_xi_with_chi

print(f"[Ξχ Engine] Running on: {DEVICE}")
os.makedirs("output", exist_ok=True)

# 1. Initialize Ξ and χ
xi_field = init_field(GRID_SIZE, 0.01, device=DEVICE)
chi_field = init_chi(GRID_SIZE, device=DEVICE)

# 2. Compute initial drift
drift_tensor = compute_drift_tensor(xi_field, laplacian)

# 3. Evolve Ξ and χ with feedback
xi_log, chi_log, entropy_log = [], [], []
for step in range(TIME_STEPS):
    # evolve Ξ with χ coupling and DRIFT
    lap = laplacian(xi_field)
    drift_term = torch.einsum('ijkl,ij->ij', drift_tensor, xi_field**2)
    chi_feedback = CHI_COUPLING * chi_field * xi_field**2
    dxi_dt = lap - xi_field * (xi_field - 1)**2 + drift_term + chi_feedback
    xi_field += DT * dxi_dt

    # evolve χ based on Ξ
    dchi_dt = -0.01 * laplacian(chi_field) + 0.02 * (xi_field - 0.5)
    chi_field += DT * dchi_dt

    # update drift every step
    drift_tensor = compute_drift_tensor(xi_field, laplacian)

    if step % ENTROPY_LOG_INTERVAL == 0:
        xi_log.append(xi_field.detach().cpu().numpy())
        chi_log.append(chi_field.detach().cpu().numpy())
        entropy_log.append(compute_entropy(xi_field))

# Save outputs
np.save("output/xi_field_log.npy", np.array(xi_log))
np.save("output/chi_field_log.npy", np.array(chi_log))
np.save("output/xi_entropy_log.npy", np.array(entropy_log))
np.save("output/drift_tensor_Xi.npy", drift_tensor.detach().cpu().numpy())

# 4. Janus point analysis
janus_idx, _ = find_janus_point(entropy_log)
print(f"🪞 Janus point index: {janus_idx}")
np.save("output/janus_idx.npy", np.array([janus_idx]))
