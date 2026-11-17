import numpy as np
import matplotlib.pyplot as plt

def plot_teff_with_tensor_overlay(field, tensor, out_path="output/teff_drift_overlay.png", stride=5):
    plt.figure(figsize=(8, 6))
    plt.imshow(field, cmap="plasma", origin="lower")
    plt.colorbar(label="Teff")

    H, W = field.shape
    dx = tensor[::stride, ::stride, 0, 0]
    dy = tensor[::stride, ::stride, 1, 1]
    x = np.arange(0, W, stride)
    y = np.arange(0, H, stride)
    X, Y = np.meshgrid(x, y)

    plt.quiver(X, Y, dx.cpu(), dy.cpu(), color="white", alpha=0.6)
    plt.title("Teff + DRIFT Tensor Overlay")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"🌀 Saved Teff + DRIFT overlay to {out_path}")
