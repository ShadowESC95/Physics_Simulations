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
    plt.figure(figsize=(8, 6))
    plt.imshow(field, cmap='plasma', origin='lower')
    plt.colorbar(label='Teff scalar field')
    plt.title('Final Teff Field Snapshot')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"📸 Final field snapshot saved to {out_path}")

def plot_entropy(entropy_log, dt, out_path=None):
    _make_output_dir()
    if out_path is None:
        out_path = f"output/entropy_plot_{_timestamp()}.png"
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

def animate_field_evolution(field_log, out_path=None, interval=50):
    _make_output_dir()
    if not isinstance(field_log, list) or len(field_log) == 0:
        print("⚠️ No field log data to animate.")
        return

    if out_path is None:
        out_path = f"output/teff_field_evolution_{_timestamp()}.mp4"

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(field_log[0], cmap='plasma', origin='lower', animated=True)
    plt.colorbar(im, ax=ax, label='Teff')

    def update(frame):
        im.set_array(field_log[frame])
        ax.set_title(f'Time Step {frame}')
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(field_log), interval=interval, blit=True)

    try:
        ani.save(out_path, writer='ffmpeg')
        print(f"🎞️ Animation saved to {out_path}")
    except Exception as e:
        print(f"⚠️ Could not save animation: {e}")
        fallback_path = out_path.replace(".mp4", ".gif")
        ani.save(fallback_path, writer='pillow')
        print(f"📽️ Saved as GIF instead to {fallback_path}")

    plt.close()
