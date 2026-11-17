import numpy as np
import matplotlib.pyplot as plt
import os

def plot_teff_phase_portrait(teff_field, out_path='output/teff_phase_portrait.png'):
    dy, dx = np.gradient(teff_field)
    Y, X = np.mgrid[0:teff_field.shape[0], 0:teff_field.shape[1]]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.streamplot(X, Y, dx, dy, color=teff_field, cmap='plasma', density=1.2, linewidth=0.8)
    ax.set_title("Phase Portrait of Teff Field")
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")
    plt.colorbar(ax.streamplot(X, Y, dx, dy, color=teff_field).lines, ax=ax, label="Teff")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()
    print(f"🌀 Phase portrait saved to {out_path}")
