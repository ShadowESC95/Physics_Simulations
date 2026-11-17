# visual/animate_field.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

def plot_teff_snapshot(field, out_path='output/teff_final.png'):
    plt.figure(figsize=(8, 6))
    plt.imshow(field, cmap='plasma', origin='lower')
    plt.colorbar(label='Teff scalar field')
    plt.title('Final Teff Field Snapshot')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"📸 Final field snapshot saved to {out_path}")

def plot_entropy(entropy_log, dt, out_path='output/entropy_plot.png'):
    steps = len(entropy_log)
    time_array = np.linspace(0, dt * steps, steps)

    plt.figure(figsize=(8, 4))
    plt.plot(time_array, entropy_log, color='darkorange')
    plt.xlabel('Time')
    plt.ylabel('Entropy Functional')
    plt.title('Entropy Evolution Over Time')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"📊 Entropy plot saved to {out_path}")

def animate_field_evolution(field_log, out_path='output/teff_field_evolution.mp4', interval=50):
    if not isinstance(field_log, list) or len(field_log) == 0:
        print("⚠️ No field log data to animate.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(field_log[0], cmap='plasma', origin='lower', animated=True)
    plt.colorbar(im, ax=ax, label='Teff')

    def update(frame):
        im.set_array(field_log[frame])
        ax.set_title(f'Time Step {frame}')
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(field_log), interval=interval, blit=True)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ani.save(out_path, writer='ffmpeg')
    plt.close()
    print(f"🎞️ Animation saved to {out_path}")
