import numpy as np
import matplotlib.pyplot as plt
import os

def load_teff_and_entropy(teff_path="output/teff_field_final.csv", entropy_path="output/entropy_log.csv"):
    teff = np.loadtxt(teff_path, delimiter=",")
    entropy = np.loadtxt(entropy_path, delimiter=",")
    return teff, entropy

def generate_massmap(teff):
    """Generate a crude mass proxy from Teff gradients."""
    grad_y, grad_x = np.gradient(teff)
    mass_map = np.sqrt(grad_x**2 + grad_y**2)
    return mass_map

def plot_mass_entropy(teff, entropy, output_path="output/mass_entropy_overlay.png"):
    massmap = generate_massmap(teff)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].imshow(massmap, cmap="inferno", origin="lower")
    axs[0].set_title("Mass Emergence Map (∇Teff)")
    axs[1].plot(entropy, color="darkorange")
    axs[1].set_title("Entropy Over Time")
    axs[1].set_xlabel("Step")
    axs[1].set_ylabel("Entropy")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"🧲 Mass vs Entropy overlay saved to {output_path}")

if __name__ == "__main__":
    t, e = load_teff_and_entropy()
    plot_mass_entropy(t, e)
