
import numpy as np

def compute_polarization_metrics(E):
    magnitude = np.linalg.norm(E, axis=-1)
    divergence = np.gradient(E[..., 0])[0] + np.gradient(E[..., 1])[1] + np.gradient(E[..., 2])[2]
    curl = np.gradient(E[..., 2], axis=1) - np.gradient(E[..., 1], axis=2)
    return magnitude, divergence, curl
