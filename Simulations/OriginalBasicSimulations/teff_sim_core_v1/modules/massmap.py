import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os

def compute_massmap(phi, epsilon=1e-5):
    grad_x = np.gradient(phi, axis=0)
    grad_y = np.gradient(phi, axis=1)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    massmap = grad_mag / (phi + epsilon)
    return massmap

def plot_massmap(massmap, out_path="output/massmap_gradient.png"):
    plt.figure(figsize=(8, 6))
    plt.imshow(massmap, cmap='inferno', origin='lower')
    plt.colorbar(label='Estimated $m_\\gamma$')
    plt.title('Photon Mass Signature from Teff Field')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"🧲 Massmap saved to {out_path}")

def save_massmap_data(massmap, csv_path="output/massmap_data.csv"):
    np.savetxt(csv_path, massmap, delimiter=",")
    print(f"💾 Raw massmap data saved to {csv_path}")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    try:
        phi = np.loadtxt("output/teff_field_final.csv", delimiter=",")
    except Exception as e:
        print(f"❌ Could not load scalar field: {e}")
        exit()

    phi = gaussian_filter(phi, sigma=1)  # optional smoothing
    massmap = compute_massmap(phi)
    plot_massmap(massmap)
    save_massmap_data(massmap)
