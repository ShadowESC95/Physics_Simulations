import numpy as np
import matplotlib.pyplot as plt

def detect_janus_points(entropy_log, threshold=1e-3):
    """Identify entropy minima (Janus point candidates)."""
    entropy_log = np.array(entropy_log)
    minima = (np.r_[True, entropy_log[1:] < entropy_log[:-1]] &
              np.r_[entropy_log[:-1] < entropy_log[1:], True])
    indices = np.where(minima & (entropy_log < threshold))[0]
    return indices

def save_janus_to_csv(indices, path="output/janus_points.csv"):
    np.savetxt(path, indices, fmt="%d", header="Frame indices of Janus points")
    print(f"🧬 Janus points saved to {path}")
