import numpy as np
import os
import torch
from config import GRID_SIZE, STEPS, DT, INIT_NOISE, USE_GPU
from engine.utils import init_field, laplacian
from engine.entropy import compute_entropy
from engine.drift_tensor import compute_drift_tensor
from visual.drift_tensor_overlay import plot_teff_with_tensor_overlay
from visual.animate_field import plot_entropy, animate_field_evolution, plot_teff_snapshot
from modules.janus_phase_tracker import find_janus_point, plot_entropy_curvature


# === Init ===
print("🚀 Running Teff + DRIFT simulation...")
device = torch.device("cuda" if torch.cuda.is_available() and USE_GPU else "cpu")
field = init_field(GRID_SIZE, noise=INIT_NOISE, device=device)
phi = field.clone()

tensor = compute_drift_tensor(phi, lap_fn=laplacian)

field_log = []
entropy_log = []

# === Time Evolution ===
for step in range(STEPS):
    lap = laplacian(field)
    drift_term = torch.einsum('ijkl,ij->ij', tensor, field**2)  # DRIFT tensor contraction
    dphi_dt = lap - field * (field - 1)**2 + drift_term
    field += DT * dphi_dt

    if step % 5 == 0:
        field_log.append(field.detach().cpu().numpy())
        entropy_log.append(compute_entropy(field))

field_log = np.array(field_log)

# === Output Directory ===
os.makedirs("output", exist_ok=True)

# === Save Raw Data ===
np.savetxt("output/entropy_log.csv", entropy_log, delimiter=",")
np.savetxt("output/teff_field_final.csv", field_log[-1], delimiter=",")
np.save("output/teff_field_log.npy", field_log)
np.save("output/drift_tensor.npy", tensor.cpu().numpy())

# === Visuals ===
plot_teff_snapshot(field_log[-1])
plot_entropy(entropy_log, dt=DT)
animate_field_evolution(field_log, interval=120)
plot_teff_with_tensor_overlay(field_log[-1], tensor)
janus_idx, curvature = find_janus_point(entropy_log)
plot_entropy_curvature(entropy_log, curvature, janus_idx)

print("✅ All outputs saved. You may now science.")
