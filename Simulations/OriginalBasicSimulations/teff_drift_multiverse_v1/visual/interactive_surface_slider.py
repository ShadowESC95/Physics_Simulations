import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
import os

def load_field_sequence(folder_path="output/frames_data"):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(".npy")])
    data = [np.load(os.path.join(folder_path, f)) for f in files]
    print(f"✅ Loaded {len(data)} frames")
    return np.array(data)

def run_interactive_slider(field_sequence):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(np.arange(field_sequence.shape[2]), np.arange(field_sequence.shape[1]))
    Z = field_sequence[0]

    surf = ax.plot_surface(X, Y, Z, cmap='plasma')
    ax.set_zlim(np.min(field_sequence), np.max(field_sequence))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Teff')
    ax.set_title("Interactive Teff Evolution")
    plt.subplots_adjust(bottom=0.2)

    ax_slider = plt.axes([0.25, 0.08, 0.5, 0.03])
    slider = Slider(ax_slider, 'Frame', 0, field_sequence.shape[0]-1, valinit=0, valstep=1)

    def update(val):
        idx = int(slider.val)
        ax.clear()
        ax.plot_surface(X, Y, field_sequence[idx], cmap='plasma')
        ax.set_zlim(np.min(field_sequence), np.max(field_sequence))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Teff')
        ax.set_title(f"Teff Field: Frame {idx}")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

if __name__ == "__main__":
    sequence = load_field_sequence()
    run_interactive_slider(sequence)
