import numpy as np
import os
from glob import glob
from scipy.stats import zscore

output_dir = "output"

def detect_anomalies(series, threshold=3):
    z = zscore(series)
    anomalies = np.where(np.abs(z) > threshold)[0]
    return anomalies

def load_and_concat(pattern):
    files = sorted(glob(os.path.join(output_dir, pattern)))
    data = []
    for f in files:
        try:
            arr = np.load(f)
            data.append(arr)
        except Exception as e:
            print(f"[WARN] Skipped {f}: {e}")
    if len(data) == 0:
        raise RuntimeError(f"No valid files found for pattern: {pattern}")
    return np.stack(data, axis=0)  # Shape: (steps, H, W)

def main():
    print("📦 Merging logs from output/")
    xi = load_and_concat("xi_step_*.npy")
    chi = load_and_concat("chi_step_*.npy")
    drift = xi - chi
    entropy = np.var(xi, axis=(1, 2))
    drift_magnitude = np.mean(np.abs(drift), axis=(1, 2))

    # Save logs
    np.save(os.path.join(output_dir, "xi_field_log.npy"), xi)
    np.save(os.path.join(output_dir, "chi_field_log.npy"), chi)
    np.save(os.path.join(output_dir, "xi_entropy_log.npy"), entropy)
    np.save(os.path.join(output_dir, "drift_magnitude_log.npy"), drift_magnitude)
    np.save(os.path.join(output_dir, "drift_tensor_Xi.npy"), drift)  # ← THIS was the bug!

    print("✅ Merged logs saved to 'output/'")
    print(f"  → Steps: {xi.shape[0]}")
    print(f"  → Grid size: {xi.shape[1]}x{xi.shape[2]}")
    print(f"  → Drift tensor: drift_tensor_Xi.npy")

# merge_logs.py — add early exit
if os.path.exists("output/xi_field_log.npy"):
    print("✅ Logs already merged — skipping.")
    exit()

if __name__ == "__main__":
    main()
