# modules/polarization_tracker.py

import numpy as np

def compute_polarization_metrics(E):
    """
    Compute magnitude, divergence, and curl magnitude of E-field
    """
    # Example assuming E is a 3D vector field: E.shape = (nx, ny, nz, 3)
    mag = np.linalg.norm(E, axis=-1)

    # Divergence
    div = np.gradient(E[...,0], axis=0) + \
          np.gradient(E[...,1], axis=1) + \
          np.gradient(E[...,2], axis=2)

    # Curl magnitude
    curl_x = np.gradient(E[...,2], axis=1) - np.gradient(E[...,1], axis=2)
    curl_y = np.gradient(E[...,0], axis=2) - np.gradient(E[...,2], axis=0)
    curl_z = np.gradient(E[...,1], axis=0) - np.gradient(E[...,0], axis=1)
    curl_mag = np.sqrt(curl_x**2 + curl_y**2 + curl_z**2)

    return mag, div, curl_mag

