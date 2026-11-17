# visualization/visualization_tools.py

import matplotlib.pyplot as plt

def save_field_plot(field, filename='field_slice.png', axis=2, index=None, cmap='magma', title='Field'):
    """
    Save a 2D slice plot to disk.

    Args:
        field (np.ndarray): 3D field
        filename (str): Output path
        axis (int): Slice axis
        index (int): Index to slice
        cmap (str): Colormap
        title (str): Title
    """
    if index is None:
        index = field.shape[axis] // 2
    slice_data = field.take(index, axis=axis)

    plt.figure()
    plt.imshow(slice_data, cmap=cmap, origin='lower')
    plt.colorbar()
    plt.title(title)
    plt.savefig(filename)
    plt.close()

