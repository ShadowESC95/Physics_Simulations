import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import animation

def animate_drift_overlay(teff_sequence, drift_tensor, out_path="output/teff_drift_evolution.mp4", interval=120):
    os.makedirs("output", exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(teff_sequence[0], cmap='plasma', origin='lower', animated=True)
    contour = ax.contour(drift_tensor, levels=5, colors='white', linewidths=0.5)
    cb = plt.colorbar(im, ax=ax, label='Teff')
    ax.set_title("Teff + DRIFT Overlay")

    def update(i):
        ax.clear()
        im = ax.imshow(teff_sequence[i], cmap='plasma', origin='lower')
        ax.contour(drift_tensor, levels=5, colors='white', linewidths=0.5)
        ax.set_title(f"Teff + DRIFT Overlay – Frame {i}")
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(teff_sequence), interval=interval, blit=False)

    try:
        ani.save(out_path, writer='ffmpeg')
        print(f"🎞️ Time-evolving DRIFT overlay saved to {out_path}")
    except Exception as e:
        print(f"⚠️ Failed to save MP4, error: {e}")
        fallback = out_path.replace(".mp4", ".gif")
        ani.save(fallback, writer='pillow')
        print(f"📽️ Fallback GIF saved to {fallback}")
