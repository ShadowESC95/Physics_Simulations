# visualization/animate_slices.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animate_field_slices(field_history, axis=2, interval=100, cmap='plasma', title='Field Evolution'):
    """
    Animate 2D slices over time from a 3D field history.

    Args:
        field_history (list of np.ndarray): Time-sequenced field data
        axis (int): Which axis to slice (0, 1, or 2)
        interval (int): Milliseconds between frames
        cmap (str): Matplotlib colormap
        title (str): Animation title
    """
    fig, ax = plt.subplots()
    slice_index = field_history[0].shape[axis] // 2

    def get_slice(field):
        return np.take(field, indices=slice_index, axis=axis)

    frames = [get_slice(f) for f in field_history]
    im = ax.imshow(frames[0], cmap=cmap, origin='lower')
    ax.set_title(title)
    plt.colorbar(im, ax=ax)

    def update(i):
        im.set_array(frames[i])
        ax.set_title(f"{title} - t={i}")
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=interval, blit=True)
    plt.show()

