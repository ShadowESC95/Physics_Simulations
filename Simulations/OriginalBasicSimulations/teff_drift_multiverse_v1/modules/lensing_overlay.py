def apply_lensing_distortion(teff_field, drift_tensor, strength=0.05):
    """Mock distortion from DRIFT lensing: shift Teff via tensor gradients."""
    dx, dy = drift_tensor[0], drift_tensor[1]
    shifted = np.roll(teff_field, int(strength * dx.mean()), axis=1)
    shifted = np.roll(shifted, int(strength * dy.mean()), axis=0)
    return shifted
