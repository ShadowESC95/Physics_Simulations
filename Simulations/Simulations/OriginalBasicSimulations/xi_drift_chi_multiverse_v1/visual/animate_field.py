import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def animate_field_evolution(field_log, out_path="output/teff_anim.mp4", interval=120):
    os.makedirs("output", exist_ok=True)
    fig, ax = plt.subplots()
    im = ax.imshow(field_log[0], cmap="plasma", origin="lower")
    plt.colorbar(im, ax=ax)

    def update(frame):
        im.set_array(field_log[frame])
        ax.set_title(f"Step {frame}")
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(field_log), interval=interval, blit=True)
    ani.save(out_path, writer="ffmpeg")
    plt.close()
    print(f"🎞️ Animation saved to {out_path}")
