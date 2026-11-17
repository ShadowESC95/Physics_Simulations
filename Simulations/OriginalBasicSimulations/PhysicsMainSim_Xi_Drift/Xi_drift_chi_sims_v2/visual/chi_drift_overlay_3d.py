import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_chi_xi_overlay(xi_field, chi_field, drift_tensor=None):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(np.arange(xi_field.shape[1]), np.arange(xi_field.shape[0]))
    Z = xi_field

    # Normalize χ for coloring
    norm_chi = (chi_field - np.min(chi_field)) / (np.max(chi_field) - np.min(chi_field) + 1e-8)
    facecolors = plt.cm.viridis(norm_chi)

    surf = ax.plot_surface(
        X, Y, Z,
        facecolors=facecolors,
        linewidth=0, antialiased=False, shade=False
    )

    if drift_tensor is not None:
        # Extract just the directional components
        drift_x = drift_tensor[..., 0, 0]  # "flow" in X
        drift_y = drift_tensor[..., 1, 1]  # "flow" in Y

        # Subsample grid for visibility
        skip = (slice(None, None, 4), slice(None, None, 4))
        ax.quiver(
            X[skip], Y[skip], Z[skip],
            drift_x[skip], drift_y[skip], np.zeros_like(drift_x[skip]),
            color='black', length=1.0, normalize=True
        )

    ax.set_title("3D ξ Surface Colored by χ + DRIFT Arrows")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("ξ Field")
    plt.tight_layout()
    plt.savefig("output/xi_chi_surface_overlay.png")
    plt.close()
