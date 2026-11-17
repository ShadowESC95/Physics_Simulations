import torch

def init_field(grid_size, noise=0.01, device="cpu"):
    field = torch.ones((grid_size, grid_size), device=device)
    field += noise * torch.randn_like(field)
    return field

def laplacian(field):
    return (
        -4 * field
        + torch.roll(field, 1, 0)
        + torch.roll(field, -1, 0)
        + torch.roll(field, 1, 1)
        + torch.roll(field, -1, 1)
    )
