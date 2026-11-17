import numpy as np
import os
import torch

from config import GRID_SIZE, STEPS, DT, INIT_NOISE, USE_GPU
from engine.drift_tensor import compute_drift_tensor
from engine.entropy import compute_entropy
from engine.utils import init_field, laplacian
from visual.animate_field import (
    plot_teff_snapshot,
    plot_entropy,
    animate_field_evolution
)
from visual.drift_tensor_overlay import plot_teff_with_tensor_overlay as overlay_drift_tensor

# === Init ===
print("🌌 Running Teff + DRIFT Multiverse Simulation...")
DEVICE = "cuda" if USE_GPU and torch.cuda.is_available() else "cpu"
print(f"💻 Using device: {DEVICE.upper()}")

phi = init_field(GRID_SIZE, noise=INIT_NOISE, device=DEVICE)
tensor = compute_drift_tensor(phi, lap_fn=laplacian)

field = phi.clone()
field_log = []
entropy_log = []

for step in range(STEPS):
    lap = laplacian(field)
    drift_term = tensor[:, :, 0, 0] * (field**2)  # Using xx component for simplicity
    dphi_dt = lap - field * (field - 1)**2 + drift_term
    field += DT * dphi_dt

    if step % 5 == 0:
        field_log.append(field.detach().cpu().numpy())
        entropy_log.append(compute_entropy(field))

field_log = np.array(field_log)
final_field = field_log[-1]

# === Output ===
os.makedirs("output", exist_ok=True)
np.savetxt("output/entropy_log.csv", entropy_log, delimiter=",")
np.savetxt("output/teff_field_final.csv", final_field, delimiter=",")
np.save("output/teff_field_log.npy", field_log)

# === Visuals ===
plot_teff_snapshot(final_field)
plot_entropy(entropy_log, dt=DT)
animate_field_evolution(field_log, interval=120)

# === DRIFT OVERLAY ===
print("🧭 Overlaying DRIFT tensor...")
try:
    overlay_drift_tensor(final_field, tensor.detach().cpu().numpy())
    print("✅ DRIFT overlay complete.")
except Exception as e:
    print(f"❌ DRIFT overlay failed: {e}")

print("🏁 Simulation complete.")

