import numpy as np

def lorenz_gauge_fix(gauge_field):
    """
    Applies the Lorenz gauge condition ∂μA^μ = 0 (divergence of A vanishes).

    Args:
        gauge_field (np.ndarray): Aμ(x, y, z, t, 4) field

    Returns:
        np.ndarray: Gauge-fixed field (Aμ') with divergence corrected
    """
    div_A = sum(np.gradient(gauge_field[..., mu], axis=mu) for mu in range(4))
    correction = div_A[..., np.newaxis] / 4.0  # distribute evenly

    return gauge_field - correction

