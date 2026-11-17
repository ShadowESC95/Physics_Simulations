import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_field_evolution(field_log, interval=120):
    fig, ax = plt.subplots()
    img = ax.imshow(field_log[0], cmap="viridis", origin="lower")
    def update(i):
        img.set_data(field_log[i])
        return [img]
    anim = FuncAnimation(fig, update, frames=len(field_log), interval=interval, blit=True)
    anim.save("output/xi_animation.mp4")
    plt.close()
