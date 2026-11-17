import numpy as np
import matplotlib.pyplot as plt
import os

def load_teff_and_tensor(teff_path, tensor_path):
    teff = np.loadtxt(teff_path, delimiter=',')
    tensor = np.load(tensor_path)
    return teff, tensor

def plot_drift_overlay(teff, tensor, step=5, scale=0.5, out_path='output/drift_overlay.png'):
    Y, X = np.mgrid[0:teff.shape[0], 0:teff.shape[1]]
    U, V = tensor[0], tensor[1]

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(teff, cmap='plasma', origin='lower')
    q = ax.quiver(X[::step, ::step], Y[::step, ::step],
                  U[::step, ::step], V[::step, ::step],
                  color='white', scale=1/scale, width=0.0025)

    ax.set_title("DRIFT Tensor Field Overlaid on Teff")
    plt.colorbar(im, ax=ax, label='Teff Field')
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()
    print(f"🧲 DRIFT tensor overlay saved to {out_path}")
