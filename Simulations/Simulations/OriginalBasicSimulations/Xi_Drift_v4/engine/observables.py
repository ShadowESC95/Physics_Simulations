# engine/observables.py

import numpy as np

def entropy(field):
    """
    Compute entropy-like observable from a scalar field using local variance proxy.

    Args:
        field (np.ndarray): Scalar field.

    Returns:
        float: Entropy measure.
    """
    local_var = np.var(field)
    return -local_var

def m_gamma_dynamic(grad_xi):
    """
    Compute dynamic photon mass from gradient of Xi.

    Args:
        grad_xi (np.ndarray): Gradient array with shape (2, H, W)

    Returns:
        np.ndarray: Effective photon mass field.
    """
    grad_mag = np.sqrt(np.sum(grad_xi ** 2, axis=0))
    return 0.05 * np.exp(-grad_mag)

def G_dynamic(xi):
    """
    Compute dynamic gravitational constant as a function of Xi.

    Args:
        xi (np.ndarray): Scalar field Xi.

    Returns:
        np.ndarray: G field.
    """
    return 6.674e-11 * (1 + 0.01 * np.sin(xi))

def c_dynamic(xi):
    """
    Compute dynamic speed of light as a function of Xi.

    Args:
        xi (np.ndarray): Scalar field Xi.

    Returns:
        np.ndarray: c field.
    """
    return 3e8 * (1 + 0.001 * np.cos(xi))

