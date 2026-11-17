import numpy as np
from scipy.stats import zscore

def detect_entropy_anomalies(entropy_series, threshold=3.5):
    z = zscore(entropy_series)
    return np.where(np.abs(z) > threshold)[0].tolist()

def detect_drift_spikes(drift_tensor, threshold=3.0):
    drift_series = drift_tensor.mean(axis=(1, 2))
    z = zscore(drift_series)
    return np.where(z > threshold)[0].tolist()
