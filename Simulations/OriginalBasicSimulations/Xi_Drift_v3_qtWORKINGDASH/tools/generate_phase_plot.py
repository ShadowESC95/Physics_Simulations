import numpy as np
import matplotlib.pyplot as plt
import argparse

def load_data(entropy_path, drift_path):
    entropy = np.load(entropy_path)
    drift = np.load(drift_path)

    curvature = np.gradient(np.gradient(entropy))
    drift_variance = np.var(drift, axis=(1, 2))

    return entropy, curvature, drift_variance

def plot_phase(entropy, curvature, drift, output):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(entropy, curvature, drift, lw=2, c='purple')
    ax.set_xlabel("Entropy S(t)")
    ax.set_ylabel("Curvature d²S/dt²")
    ax.set_zlabel("Drift Var(t)")
    ax.set_title("Ξχ Phase Portrait")

    plt.savefig(output, dpi=300)
    print(f"Saved phase portrait: {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--entropy", required=True)
    parser.add_argument("--drift", required=True)
    parser.add_argument("--out", default="phase_spiral.png")

    args = parser.parse_args()
    entropy, curvature, drift = load_data(args.entropy, args.drift)
    plot_phase(entropy, curvature, drift, args.out)
