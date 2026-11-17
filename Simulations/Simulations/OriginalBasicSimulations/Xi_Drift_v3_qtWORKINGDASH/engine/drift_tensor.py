import numpy as np

def compute_drift(xi, chi):
    """
    Computes the drift tensor as the difference between Ξ and χ fields.

    Parameters:
        xi (np.ndarray): Ξ field (time-series or single snapshot)
        chi (np.ndarray): χ field

    Returns:
        np.ndarray: Drift tensor (same shape)
    """
    return xi - chi

def compute_drift_variance(xi_series, chi_series):
    drift = xi_series - chi_series
    return np.var(drift, axis=(1, 2))  # for 2D field time series



 #note: add in other forces/dimensions/parameters i.e not just Xi and Chi
