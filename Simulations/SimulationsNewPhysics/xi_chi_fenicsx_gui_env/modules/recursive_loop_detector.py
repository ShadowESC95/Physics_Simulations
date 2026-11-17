# modules/recursive_loop_detector.py

import numpy as np
from scipy.signal import find_peaks, correlate

def detect_recursive_loops(signal, thresh=0.5, min_sep=1):
    """
    Detect recursive loops or repeated patterns in a 1D signal.

    Parameters
    ----------
    signal : array_like
        Input 1D signal.
    thresh : float, optional
        Minimum normalized peak height (0..1) relative to signal max. Default 0.5.
    min_sep : int, optional
        Minimum separation between detected peaks (in samples). Default 1.

    Returns
    -------
    peaks : ndarray
        Indices of detected peaks that may indicate recurring events.
    loop_metric : ndarray
        Normalized autocorrelation highlighting repeating patterns.
    """
    signal = np.asarray(signal, dtype=float)
    
    if signal.ndim != 1:
        raise ValueError("Input signal must be 1D")
    
    # --- Adaptive thresholding ---
    max_val = np.max(np.abs(signal))
    dynamic_thresh = max(thresh * max_val, 1e-12)
    
    # Detect peaks in the signal
    peaks, _ = find_peaks(np.abs(signal), height=dynamic_thresh, distance=min_sep)
    
    # Compute normalized autocorrelation (centered)
    ac_full = correlate(signal, signal, mode='full')
    ac = ac_full / (np.max(np.abs(ac_full)) + 1e-12)
    
    # Only keep second half (positive lags)
    loop_metric = ac[len(ac)//2:]
    
    # Optional: emphasize repeating loops by thresholding autocorr peaks
    loop_metric_peaks, _ = find_peaks(loop_metric, height=0.25)  # peaks of autocorr
    
    return peaks, loop_metric

