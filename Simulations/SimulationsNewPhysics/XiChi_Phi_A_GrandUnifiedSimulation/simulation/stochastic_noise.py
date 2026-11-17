# simulation/stochastic_noise.py

import numpy as np

def generate_white_noise(shape, scale=1.0, seed=None):
    """
    Generate white noise (uncorrelated Gaussian).
    """
    if seed is not None:
        np.random.seed(seed)
    return scale * np.random.randn(*shape)

def generate_pink_noise(shape, scale=1.0, seed=None):
    """
    Generate pink noise via 1/f amplitude modulation in frequency domain.

    Args:
        shape (tuple): Grid shape
        scale (float): Scaling of noise amplitude
        seed (int): Optional seed

    Returns:
        np.ndarray: Pink noise field
    """
    if seed is not None:
        np.random.seed(seed)

    freq_noise = np.fft.fftn(np.random.randn(*shape))
    grid = np.meshgrid(*[np.fft.fftfreq(n) for n in shape], indexing='ij')
    freqs = np.sqrt(sum(f**2 for f in grid))
    freqs[0, 0, 0] = 1.0  # prevent divide by zero
    pink = freq_noise / freqs
    pink_real = np.fft.ifftn(pink).real
    return scale * pink_real / np.max(np.abs(pink_real))

