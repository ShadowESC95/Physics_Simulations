import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

def plot_3d_chi_xi_overlay(xi_field, chi_field, drift_tensor=None, out_path=None):
    """
    Create a 3D overlay of the Ξ and χ fields.
    Optionally, add drift_tensor as a colormap or quiver overlay.

    Parameters:
        xi_field (np.ndarray): The Ξ field, shape (N, N).
        chi_field (np.ndarray): The χ field, shape (N, N).
        drift_tensor (np.ndarray or None): Optional drift tensor (N, N, 2, 2).
        out_path (str or None): If set, save the figure to this path.
    """
    N, M = xi_field.shape
    X, Y = np.meshgrid(np.arange(M), np.arange(N))

    fig = plt.figure(figsize=(12, 6))

    # Ξ surface
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    surf1 = ax1.plot_surface(X, Y, xi_field, cmap='viridis', alpha=0.85)
    ax1.set_title("Ξ field (surface)")
    fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10)

    # χ surface or contour
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    surf2 = ax2.plot_surface(X, Y, chi_field, cmap='magma', alpha=0.85)
    ax2.set_title("χ field (surface)")
    fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10)

    # Optionally overlay drift tensor as quivers (arrows)
    if drift_tensor is not None:
        U = drift_tensor[..., 0, 0]
        V = drift_tensor[..., 1, 1]
        ax1.quiver(X, Y, xi_field, U, V, np.zeros_like(U), length=1, color='black', alpha=0.5, lw=0.2)
        ax2.quiver(X, Y, chi_field, U, V, np.zeros_like(U), length=1, color='black', alpha=0.5, lw=0.2)

    plt.tight_layout()
    if out_path:
        plt.savefig(out_path)
    plt.show()


