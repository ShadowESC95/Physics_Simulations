import matplotlib.pyplot as plt
import numpy as np

def plot_field_with_drift(xi_field, drift_tensor):
    X, Y = np.meshgrid(np.arange(xi_field.shape[0]), np.arange(xi_field.shape[1]))
    U = drift_tensor[..., 0, 0]
    V = drift_tensor[..., 1, 1]

    plt.figure(figsize=(8, 6))
    plt.imshow(xi_field, cmap="plasma", origin="lower")
    plt.quiver(X, Y, U, V, color="white", scale=40)
    plt.title("Ξ Field + DRIFT Overlay")
    plt.savefig("output/xi_drift_overlay.png")
    plt.close()
