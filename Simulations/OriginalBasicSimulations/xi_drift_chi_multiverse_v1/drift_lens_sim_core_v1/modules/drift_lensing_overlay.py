import numpy as np
import matplotlib.pyplot as plt
import os

def drift_tensor_overlay(teff_field, drift_tensor, strength=0.5):
    """
    Overlay DRIFT tensor data on Teff field.

    Args:
        teff_field (2D array): Teff scalar field.
        drift_tensor (2D array): DRIFT tensor field (e.g., norm of I(n)_abc).
        strength (float): Scaling factor for overlay effect.

    Returns:
        2D array: Modified Teff field for visual rendering.
    """
    assert teff_field.shape == drift_tensor.shape, "Shape mismatch!"
    overlay = teff_field + strength * drift_tensor
    return overlay

def save_drift_overlay(teff_field, drift_tensor, out_path="output/teff_drift_overlay.png"):
    plt.figure(figsize=(8, 6))
    composite = drift_tensor_overlay(teff_field, drift_tensor)
    plt.imshow(composite, cmap='plasma', origin='lower')
    plt.colorbar(label='Teff + DRIFT Tensor Overlay')
    plt.title("DRIFT Lensing Overlay")
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()
    print(f"🎯 DRIFT lensing overlay saved to {out_path}")
