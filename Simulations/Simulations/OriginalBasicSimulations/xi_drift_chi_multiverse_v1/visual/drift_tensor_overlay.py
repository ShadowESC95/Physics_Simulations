import numpy as np
import matplotlib.pyplot as plt

def plot_teff_with_tensor_overlay(teff_field, tensor, out_path="output/teff_drift_overlay.png"):
    plt.figure(figsize=(8, 6))
    plt.imshow(teff_field, cmap="plasma", origin="lower")
    plt.colorbar(label="Teff")

    # Sample vectors for clarity
    step = max(1, teff_field.shape[0] // 20)
    dx = tensor[..., 0, 0]
    dy = tensor[..., 1, 1]

    x, y = np.meshgrid(np.arange(teff_field.shape[1]), np.arange(teff_field.shape[0]))
    plt.quiver(x[::step, ::step], y[::step, ::step],
               dx[::step, ::step], dy[::step, ::step],
               color="white", alpha=0.5, scale=30)

    plt.title("Teff Field with DRIFT Overlay")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"🌌 Teff + DRIFT overlay saved to {out_path}")
