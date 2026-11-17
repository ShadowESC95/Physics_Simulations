import numpy as np
import matplotlib.pyplot as plt

def plot_teff_with_tensor_overlay(teff_field, drift_tensor, spacing=5):
    """
    Overlay DRIFT tensor arrows on top of the Teff scalar field.

    Args:
        teff_field (np.ndarray): 2D scalar field
        drift_tensor (torch.Tensor or np.ndarray): Tensor field [NxNx2x2]
        spacing (int): Spacing between arrows
    """
    if hasattr(drift_tensor, "detach"):  # If torch.Tensor, move to CPU and numpy
        drift_tensor = drift_tensor.detach().cpu().numpy()

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(teff_field, cmap='plasma', origin='lower')
    plt.colorbar(im, ax=ax, label='Teff')

    X, Y = np.meshgrid(np.arange(teff_field.shape[1]), np.arange(teff_field.shape[0]))

    U = drift_tensor[:, :, 0, 0]  # x component
    V = drift_tensor[:, :, 1, 1]  # y component

    ax.quiver(X[::spacing, ::spacing], Y[::spacing, ::spacing],
              U[::spacing, ::spacing], V[::spacing, ::spacing],
              color='white', alpha=0.6, scale=50)

    ax.set_title("Teff Field with DRIFT Tensor Overlay")
    plt.tight_layout()
    plt.savefig("output/teff_drift_overlay.png")
    plt.close()
    print("🌀 DRIFT overlay saved to output/teff_drift_overlay.png")
