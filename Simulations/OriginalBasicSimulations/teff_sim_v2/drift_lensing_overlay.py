import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

def load_teff_field(path="output/teff_field_final.csv"):
    return np.loadtxt(path, delimiter=",")

def generate_drift_tensor_field(teff_field):
    """Mock DRIFT tensor as gradient-based lensing vector field."""
    grad_y, grad_x = np.gradient(teff_field)
    drift_x = -grad_y  # Rotate gradient 90° for lensing style
    drift_y = grad_x
    return drift_x, drift_y

def plot_drift_overlay(teff_field, drift_x, drift_y, output_path="output/teff_drift_overlay.png"):
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(teff_field, cmap="plasma", origin="lower")
    ax.quiver(drift_x, drift_y, color='white', alpha=0.7, scale=30)
    plt.title("Teff Field with DRIFT Lensing Overlay")
    plt.colorbar(im, ax=ax, label="Teff")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"🌀 DRIFT lensing overlay saved to {output_path}")

if __name__ == "__main__":
    teff = load_teff_field()
    dx, dy = generate_drift_tensor_field(teff)
    plot_drift_overlay(teff, dx, dy)
