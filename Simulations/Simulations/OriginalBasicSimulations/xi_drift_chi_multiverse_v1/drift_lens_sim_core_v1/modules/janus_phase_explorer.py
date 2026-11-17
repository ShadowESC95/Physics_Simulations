import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def janus_phase_explorer(teff_sequence, out_path="output/janus_explorer.mp4"):
    os.makedirs("output", exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_title("Janus Phase Explorer")
    ax.set_xlabel("∂Teff/∂t")
    ax.set_ylabel("Entropy")

    dphi_dt_log = []
    entropy_log = []

    for i in range(1, len(teff_sequence)):
        diff = teff_sequence[i] - teff_sequence[i - 1]
        dphi_dt = np.mean(diff)
        entropy = np.sum(teff_sequence[i]**2)  # Toy model entropy
        dphi_dt_log.append(dphi_dt)
        entropy_log.append(entropy)

    scat = ax.scatter([], [], c='cyan')

    def update(frame):
        ax.clear()
        ax.set_xlim(min(dphi_dt_log), max(dphi_dt_log))
        ax.set_ylim(min(entropy_log), max(entropy_log))
        ax.set_xlabel("⟨∂Teff/∂t⟩")
        ax.set_ylabel("Entropy")
        ax.set_title(f"Janus Point Frame {frame}")
        ax.scatter(dphi_dt_log[:frame], entropy_log[:frame], c='cyan', s=15)

    ani = animation.FuncAnimation(fig, update, frames=len(dphi_dt_log), interval=120, repeat=False)

    ani.save(out_path, writer='ffmpeg')
    print(f"📈 Janus Phase Space animation saved to {out_path}")
