# engine/utils.py
import torch

def init_field(grid_size, noise=0.01, device=None, channels=1):
    """
    Initialize a scalar or multi-channel field with optional Gaussian noise.

    Args:
        grid_size (int): Size of the square grid.
        noise (float): Standard deviation of Gaussian noise.
        device (str or None): 'cpu' or 'cuda'. If None, auto-detect.
        channels (int): Number of channels (1 for scalar, >1 for multi-field).

    Returns:
        torch.Tensor: Initialized field tensor.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    shape = (channels, grid_size, grid_size) if channels > 1 else (grid_size, grid_size)
    field = torch.ones(shape, device=device)
    
    if noise > 0:
        field += noise * torch.randn_like(field)

    return field


def laplacian(field):
    """
    Compute 2D Laplacian using finite difference for scalar or batched fields.

    Args:
        field (torch.Tensor): Input tensor of shape (H, W) or (C, H, W)

    Returns:
        torch.Tensor: Laplacian tensor with the same shape.
    """
    if field.ndim == 3:
        # Batched form: (C, H, W)
        return (
            -4 * field
            + torch.roll(field, shifts=1, dims=1)
            + torch.roll(field, shifts=-1, dims=1)
            + torch.roll(field, shifts=1, dims=2)
            + torch.roll(field, shifts=-1, dims=2)
        )
    elif field.ndim == 2:
        # Scalar field: (H, W)
        return (
            -4 * field
            + torch.roll(field, shifts=1, dims=0)
            + torch.roll(field, shifts=-1, dims=0)
            + torch.roll(field, shifts=1, dims=1)
            + torch.roll(field, shifts=-1, dims=1)
        )
    else:
        raise ValueError(f"Laplacian not supported for input with shape {field.shape}")

