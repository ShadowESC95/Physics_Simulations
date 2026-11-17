# sim.py — Run long simulation with updated engine and track key observables

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile

from engine.fields import xi_field, chi_field
from engine.integration import rk4_step_enhanced
from engine.observables import entropy, m_gamma_dynamic, G_dynamic, c_dynamic

# === Simulation Parameters ===
steps_long = 200
dt_long = 0.01

# === Initialize Fields ===
xi = xi_field.copy()
chi = chi_field.copy()

# === Storage Arrays ===
entropy_long = []
grad_xi_masses = []
G_vals = []
c_vals = []
xi_snapshots_long = []

# === Main Simulation Loop ===
for t in range(steps_long):
    xi = rk4_step_enhanced(xi, chi, dt_long)
    xi_snapshots_long.append(xi.copy())
    entropy_long.append(entropy(xi))

    # ∇Ξ and derived quantities
    grad_y_xi, grad_x_xi = np.gradient(xi)
    m_gamma = m_gamma_dynamic(np.array([grad_x_xi, grad_y_xi]))
    grad_xi_masses.append(np.mean(m_gamma))

    G_vals.append(np.mean(G_dynamic(xi)))
    c_vals.append(np.mean(c_dynamic(xi)))

# === Convert to Arrays ===
entropy_long = np.array(entropy_long)
grad_xi_masses = np.array(grad_xi_masses)
G_vals = np.array(G_vals)
c_vals = np.array(c_vals)

# === Output Directories ===
output_dir = "output"
snap_dir = os.path.join(output_dir, "Xi_Chi_LongRun_Snapshots")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(snap_dir, exist_ok=True)

# === Save Results to CSV ===
long_csv_path = os.path.join(output_dir, "Xi_Chi_LongRun_Observables.csv")
df_long = pd.DataFrame({
    "step": np.arange(steps_long),
    "entropy": entropy_long,
    "m_gamma_mean": grad_xi_masses,
    "G_mean": G_vals,
    "c_mean": c_vals
})
df_long.to_csv(long_csv_path, index=False)

# === Save Data for Dash App or Later Analysis ===
np.save(os.path.join(output_dir, "xi_field_log.npy"), np.array(xi_snapshots_long))
np.save(os.path.join(output_dir, "chi_field_log.npy"), chi)
np.save(os.path.join(output_dir, "xi_entropy_log.npy"), entropy_long)

# === Plot Observables ===
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(df_long["step"], df_long["entropy"])
plt.title("Entropy S(t)")

plt.subplot(2, 2, 2)
plt.plot(df_long["step"], df_long["m_gamma_mean"])
plt.title("Mean Photon Mass $m_\\gamma(\\nabla \\Xi)$")

plt.subplot(2, 2, 3)
plt.plot(df_long["step"], df_long["G_mean"])
plt.title("Mean $G(\\Xi)$")

plt.subplot(2, 2, 4)
plt.plot(df_long["step"], df_long["c_mean"])
plt.title("Mean $c(\\Xi)$")

plt.tight_layout()
plot_combined_path = os.path.join(output_dir, "Xi_Chi_LongRun_Observables.png")
plt.savefig(plot_combined_path)
plt.close()

# === Save Ξ Snapshots Individually ===
long_snap_paths = []
for i, snap in enumerate(xi_snapshots_long):
    path = os.path.join(snap_dir, f"xi_long_snapshot_{i:03d}.npy")
    np.save(path, snap)
    long_snap_paths.append(path)

# === Zip Snapshots ===
zip_long_snap_path = os.path.join(output_dir, "Xi_Chi_LongRun_Snapshots.zip")
with zipfile.ZipFile(zip_long_snap_path, 'w') as zipf:
    for path in long_snap_paths:
        zipf.write(path, arcname=os.path.basename(path))

# === Final Output Paths ===
print("✅ Simulation complete.")
print("📄 CSV:", long_csv_path)
print("🖼️ Plot:", plot_combined_path)
print("🗜️ Zipped snapshots:", zip_long_snap_path)

