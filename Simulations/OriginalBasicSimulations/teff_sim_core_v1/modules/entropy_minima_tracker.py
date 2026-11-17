import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import os

def compute_entropy_curvature(entropy, smooth_sigma=2):
    entropy_smoothed = gaussian_filter1d(entropy, sigma=smooth_sigma)
    dS = np.gradient(entropy_smoothed)
    d2S = np.gradient(dS)
    return entropy_smoothed, dS, d2S

def find_minima_indices(d2S, threshold=1e-3):
    return np.where(d2S > threshold)[0]

def plot_entropy_curvature(entropy, dS, d2S, minima_indices, out_path):
    plt.figure(figsize=(10, 6))
    steps = np.arange(len(entropy))
    plt.plot(steps, entropy, label='Entropy $S(\\tau)$', color='orange')
    plt.plot(steps, dS, label='$dS/d\\tau$', linestyle='--', color='blue')
    plt.plot(steps, d2S, label='$d^2S/d\\tau^2$', linestyle=':', color='red')
    plt.scatter(minima_indices, np.array(entropy)[minima_indices], color='black', zorder=5, label='Janus Point Candidates')
    plt.legend()
    plt.title('Entropy Evolution and Janus Point Detection')
    plt.xlabel('Time Step')
    plt.ylabel('Entropy / Derivatives')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"📈 Entropy curvature plot saved to {out_path}")

def save_minima(minima_indices, out_path="output/janus_points.csv"):
    np.savetxt(out_path, minima_indices, fmt='%d', delimiter=",")
    print(f"📄 Janus candidate indices saved to {out_path}")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    try:
        entropy = np.loadtxt("output/entropy_log.csv", delimiter=",")
    except Exception as e:
        print(f"❌ Failed to load entropy log: {e}")
        exit()

    S, dS, d2S = compute_entropy_curvature(entropy)
    minima = find_minima_indices(d2S)

    plot_entropy_curvature(S, dS, d2S, minima, "output/entropy_curvature.png")
    save_minima(minima)
