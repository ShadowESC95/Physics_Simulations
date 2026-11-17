import numpy as np

def detect_recursive_loops(signal, lag=None, thresh=0.8, min_sep=5):
    """
    Finds recurrent alignments via normalized autocorrelation peaks.
    Returns (peaks, ac) where peaks = list[(lag_index, score)]
    """
    x = np.asarray(signal, dtype=float)
    x = x - np.mean(x)
    if lag is None:
        lag = min(len(x)//4, 1024)
    ac = np.correlate(x, x, mode='full')
    ac = ac[len(x)-1:len(x)-1+lag]
    ac = ac / (np.max(ac) + 1e-12)
    peaks = []
    for i in range(1, len(ac)-1):
        if ac[i] > ac[i-1] and ac[i] > ac[i+1] and ac[i] >= thresh:
            if not peaks or (i - peaks[-1][0]) >= min_sep:
                peaks.append((i, float(ac[i])))
    return peaks, ac
