import matplotlib.pyplot as plt
import numpy as np

def plot_xi_with_tensor_overlay(xi_field, tensor):
    plt.figure(figsize=(8, 6))
    plt.imshow(xi_field, cmap="plasma", origin="lower")
    plt.colorbar(label="ξ Field Intensity")

    # Decompose tensor into arrows
    drift_x = tensor[..., 0, 0]
    drift_y = tensor[..., 1, 1]

    Y, X = np.mgrid[0:xi_field.shape[0], 0:xi_field.shape[1]]
    plt.quiver(X, Y, drift_x, drift_y, color="white", scale=50, width=0.002)
    plt.title("ξ Field with DRIFT Tensor Overlay")
    plt.tight_layout()
    plt.savefig("output/xi_drift_overlay.png")
    plt.close()
