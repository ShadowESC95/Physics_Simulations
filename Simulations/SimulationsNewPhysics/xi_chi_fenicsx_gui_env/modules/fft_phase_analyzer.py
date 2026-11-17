import numpy as np

def analyze_fft_phase(signal, dt=1.0):
    """
    Compute the FFT magnitude, phase, and corresponding frequency axis for a 1D signal.

    Parameters
    ----------
    signal : array_like
        1D time-domain signal
    dt : float, optional
        Time step between samples (default: 1.0)

    Returns
    -------
    mag_fft : ndarray
        Magnitude spectrum
    phase_fft : ndarray
        Phase spectrum (radians)
    freqs : ndarray
        Frequency axis corresponding to the FFT
    """
    signal = np.asarray(signal, dtype=float)
    
    if signal.ndim != 1:
        raise ValueError("Input signal must be 1D")
    
    n = len(signal)
    fft_vals = np.fft.fft(signal)
    freqs = np.fft.fftfreq(n, d=dt)
    
    mag_fft = np.abs(fft_vals)
    phase_fft = np.angle(fft_vals)
    
    # Sort by frequency (optional, useful for plotting)
    idx = np.argsort(freqs)
    freqs = freqs[idx]
    mag_fft = mag_fft[idx]
    phase_fft = phase_fft[idx]
    
    return mag_fft, phase_fft, freqs
