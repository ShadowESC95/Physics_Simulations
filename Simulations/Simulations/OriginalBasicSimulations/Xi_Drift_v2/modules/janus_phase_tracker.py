import numpy as np
import matplotlib.pyplot as plt

def find_janus_point(entropy_log):
    curvature = np.gradient(np.gradient(entropy_log))
    idx = np.argmin(np.abs(curvature))
    return idx, curvature

def plot_entropy_curvature(entropy_log, curvature, janus_idx, out_path="output/entropy_curvature.png"):
    plt.figure(figsize=(8, 4))
    plt.plot(entropy_log, label="Entropy")
    plt.plot(curvature, label="Curvature", linestyle="--")
    plt.axvline(janus_idx, color="red", linestyle=":", label="Janus Point")
    plt.legend()
    plt.xlabel("Step")
    plt.title("Entropy + Curvature")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"🪞 Entropy curvature plot saved to {out_path}")
