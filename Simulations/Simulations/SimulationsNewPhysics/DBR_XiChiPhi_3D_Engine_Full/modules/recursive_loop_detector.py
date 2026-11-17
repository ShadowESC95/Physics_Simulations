
import numpy as np

def detect_recursive_loops(E_series):
    spikes = []
    threshold = 0.01
    for t in range(1, len(E_series)):
        delta = np.linalg.norm(E_series[t] - E_series[t-1])
        if delta < threshold:
            spikes.append((t, delta))
    return spikes
