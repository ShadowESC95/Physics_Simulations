import numpy as np
import matplotlib.pyplot as plt
import os

def compute_entropy_curvature(entropy_log):
    """Second derivative of entropy = entropy curvature."""
    entropy_log = np.array(entropy_log)
    second_deriv = np.gradient(np.gradient(entropy_log))
    return second_deriv

def find_janus_point(entropy_log):
    curvature = compute_entropy_curvature(entropy_log)
    min_index = np.argmin(curvature)
    print(f"🔍 Janus point candidate located at step: {min_index}")
    return min_index, curvature

def plot_entropy_curvature(entropy_log, curvature, janus_idx, out_path="output/entropy_curvature.png"):
    os.makedirs("output", exist_ok=True)
    steps = len(entropy_log)
    time = np.linspace(0, steps, steps)

    plt.figure(figsize=(10, 5))
    plt.plot(time, entropy_log, label="Entropy", color="orange")
    plt.plot(time, curvature, label="Entropy Curvature", color="blue", alpha=0.6)
    plt.axvline(janus_idx, color="red", linestyle="--", label="Janus Point")
    plt.xlabel("Simulation Step")
    plt.ylabel("Value")
    plt.title("Entropy and Janus Point Detection")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"📈 Janus plot saved to {out_path}")
