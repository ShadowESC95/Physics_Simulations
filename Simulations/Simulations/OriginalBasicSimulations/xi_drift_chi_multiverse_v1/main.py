import os
import numpy as np
import torch

from config import GRID_SIZE, STEPS, DT, INIT_NOISE, USE_GPU
from engine.utils import init_field, laplacian
from engine.entropy import compute_entropy
from engine.drift_tensor import compute_drift_tensor
from engine.xi_dynamics import evolve_xi_with_chi
from modules.chi_field import init_chi, evolve_chi_field
from modules.janus_phase_tracker import find_janus_point, plot_entropy_curvature
from visual.xi_tensor_overlay import plot_xi_with_tensor_overlay
from visual.animate_field import animate_field_evolution
from visual.chi_drift_overlay_3d import plot_3d_chi_xi_overlay

print("🚀 Launching ξ + χ + DRIFT Evolution...")

device = torch.device("cuda" if torch.cuda.is_available() and USE_GPU else "cpu")
xi = init_field(GRID_SIZE, noise=INIT_NOISE, device=device)
tensor = compute_drift_tensor(xi, laplacian)

chi = init_chi(GRID_SIZE, noise=INIT_NOISE, device=device)

# First evolve Ξ and get ξ log (needs initial χ value and drift tensor)
xi_log, entropy_log = evolve_xi_with_chi(xi, chi, tensor, STEPS, DT, device)

# Then evolve χ based on the Ξ time series
chi_log = evolve_chi_field(chi, xi_log)

# Output
os.makedirs("output", exist_ok=True)
np.savetxt("output/entropy_log.csv", entropy_log, delimiter=",")
np.save("output/xi_field_log.npy", np.array(xi_log))
np.save("output/chi_field_log.npy", np.array(chi_log))

animate_field_evolution(xi_log, interval=120)
plot_xi_with_tensor_overlay(xi_log[-1], tensor)

janus_idx, curvature = find_janus_point(entropy_log)
plot_entropy_curvature(entropy_log, curvature, janus_idx)

plot_3d_chi_xi_overlay(
    xi_field=xi_log[-1],
    chi_field=chi_log[-1],
    drift_tensor=tensor.detach().cpu().numpy()
)

print("✅ ξ+χ Simulation complete. Overlay files dumped.")
