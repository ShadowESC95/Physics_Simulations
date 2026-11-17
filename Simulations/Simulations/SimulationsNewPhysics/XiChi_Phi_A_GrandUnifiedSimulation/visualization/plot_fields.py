# visualization/plot_fields.py

import matplotlib.pyplot as plt
import numpy as np

def plot_field_slice(field, axis=2, index=None, cmap='viridis', title='Field Slice'):
    """
    Plot a single 2D slice from a 3D field.

    Args:
        field (np.ndarray): 3D field (or 4D vector field to pick component from)
        axis (int): Which axis to slice (0, 1, or 2)
        index (int): Which slice index to use
        cmap (str): Colormap
        title (str): Title for plot
    """
    if index is None:
        index = field.shape[axis] // 2
    slice_data = np.take(field, index, axis=axis)

    plt.imshow(slice_data, cmap=cmap, origin='lower')
    plt.colorbar()
    plt.title(f"{title} (axis={axis}, index={index})")
    plt.show()

