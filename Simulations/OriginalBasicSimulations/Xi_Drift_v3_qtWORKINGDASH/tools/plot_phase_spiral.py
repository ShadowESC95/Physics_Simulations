import numpy as np
import matplotlib.pyplot as plt
import os

try:
    drift = np.load("output/drift_tensor_Xi.npy")  # shape: (steps, H, W)
    print(f"📈 Loaded drift tensor: {drift.shape}")
except FileNotFoundError:
    print("[WARN] drift_tensor_Xi.npy not found. Attempting to reconstruct from xi/chi...")
    try:
        xi = np.load("output/xi_field_log.npy")
        chi = np.load("output/chi_field_log.npy")
        drift = xi - chi
        np.save("output/drift_tensor_Xi.npy", drift)
        print("✅ Reconstructed and saved drift_tensor_Xi.npy.")
    except Exception as e:
        print(f"[ERROR] Cannot proceed: {e}")
        exit(1)

# Select a few time steps
indices = np.linspace(0, drift.shape[0] - 1, 5, dtype=int)

plt.figure(figsize=(10, 10))
for i, idx in enumerate(indices, 1):
    plt.subplot(3, 2, i)
    plt.imshow(drift[idx], cmap="coolwarm", origin="lower")
    plt.title(f"Drift at step {idx}")
    plt.colorbar()
plt.tight_layout()
plt.savefig("output/phase_spiral.png")
plt.show()
