import numpy as np
import os
from config import GRID_SIZE, STEPS, DT, INIT_NOISE, USE_GPU
from engine.drift_tensor import compute_drift_tensor
from engine.drift_tensor_builder import compute_tensor, save_tensor
from engine.utils import init_field, laplacian
from engine.entropy import compute_entropy
from visual.animate_field import (
    plot_teff_snapshot,
    plot_entropy,
    animate_field_evolution
)
from visual.drift_tensor_overlay import overlay_drift_tensor

# === Init ===
print("🚀 Running Teff + DRIFT simulation...")
DEVICE = "cuda" if USE_GPU else "cpu"
phi = init_field(GRID_SIZE, noise=INIT_NOISE, device=DEVICE)
tensor = compute_drift_tensor(phi, lap_fn=laplacian)

print("✅ Field + DRIFT tensor initialized")

field = phi.clone()
field_log = []
entropy_log = []

print("⚙️ Starting evolution loop...")
for step in range(STEPS):
    lap = laplacian(field)
    drift_term = tensor[:, :, 0, 0] * (field**2)  # Using xx component only
    dphi_dt = lap - field * (field - 1)**2 + drift_term
    field += DT * dphi_dt

    if step % 5 == 0:
        field_log.append(field.detach().cpu().numpy())
        entropy_log.append(compute_entropy(field))

print("✅ Evolution complete")
field_log = np.array(field_log)
final_field = field_log[-1] if len(field_log) > 0 else None

# === Output ===
print("💾 Saving output...")
try:
    os.makedirs("output", exist_ok=True)
    
    if entropy_log:
        np.savetxt("output/entropy_log.csv", entropy_log, delimiter=",")
    else:
        print("⚠️ Warning: entropy_log is empty")

    if final_field is not None:
        np.savetxt("output/teff_field_final.csv", final_field, delimiter=",")
    else:
        print("⚠️ Warning: final_field is None")

    if len(field_log) > 0:
        np.save("output/teff_field_log.npy", field_log)
    else:
        print("⚠️ Warning: field_log is empty")

    print("✅ Output files saved")

except Exception as e:
    print("❌ Failed to save output files:", e)

# === Visuals ===
print("🎨 Generating visuals...")
try:
    if final_field is not None:
        plot_teff_snapshot(final_field)

    if entropy_log:
        plot_entropy(entropy_log, dt=DT)

    if len(field_log) > 0:
        animate_field_evolution(field_log, interval=120)

    print("✅ Visuals generated")

except Exception as e:
    print("❌ Visual generation error:", e)

# === DRIFT Tensor Save ===
try:
    drift_np_tensor = compute_tensor(final_field)
    save_tensor(drift_np_tensor, out_path="output/drift_tensor.npy")
    print("✅ DRIFT tensor saved")

    overlay_drift_tensor(final_field, drift_np_tensor)
    print("✅ DRIFT overlay saved")

except Exception as e:
    print("❌ DRIFT tensor error:", e)

print("🏁 Simulation complete.")

