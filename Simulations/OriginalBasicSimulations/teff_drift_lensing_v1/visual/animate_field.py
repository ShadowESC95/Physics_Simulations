import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os
from datetime import datetime

def _make_output_dir():
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/frames", exist_ok=True)

def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def plot_teff_snapshot(field, out_path=None):
    _make_output_dir()
    if out_path is None:
        out_path = f"output/teff_final_{_timestamp()}.png"
    plt.figure(figsize=(6, 5))
    plt.imshow(field, cmap='plasma', origin='lower')
    plt.colorbar(label='Teff Field Value')
    plt.title('Final Teff Snapshot')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"📸 Saved: {out_path}")

def plot_entropy(entropy_log, dt, out_path=None):
    _make_output_dir()
    if out_path is None:
        out_path = f"output/entropy_plot_{_timestamp()}.png"
    time_array = np.linspace(0, dt * len(entropy_log), len(entropy_log))
    plt.figure(figsize=(8, 4))
    plt.plot(time_array, entropy_log, color='darkred')
    plt.xlabel('Time')
    plt.ylabel('Entropy')
    plt.title('Entropy Evolution')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"📊 Saved: {out_path}")

def animate_field_evolution(field_log, interval=100, out_path=None):
    _make_output_dir()
    if out_path is None:
        out_path = f"output/teff_field_evolution_{_timestamp()}.mp4"
    
    fig, ax = plt.subplots()
    im = ax.imshow(field_log[0], cmap='plasma', origin='lower')
    plt.colorbar(im, ax=ax)

    def update(frame):
        im.set_array(field_log[frame])
        ax.set_title(f"Time Step {frame}")
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(field_log), interval=interval, blit=True)
    
    try:
        ani.save(out_path, writer='ffmpeg')
        print(f"🎞️ Animation saved to {out_path}")
    except Exception as e:
        fallback = out_path.replace(".mp4", ".gif")
        ani.save(fallback, writer='pillow')
        print(f"📽️ Fallback GIF saved to {fallback}")

    plt.close()
