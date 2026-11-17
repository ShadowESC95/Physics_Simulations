import torch

def init_field(grid_size, noise=0.01, device="cpu"):
    base = torch.ones(grid_size, dtype=torch.float32, device=device)
    perturb = torch.randn(grid_size, dtype=torch.float32, device=device) * noise
    return base + perturb

def laplacian(field):
    return (
        -4 * field
        + torch.roll(field, 1, dims=0) + torch.roll(field, -1, dims=0)
        + torch.roll(field, 1, dims=1) + torch.roll(field, -1, dims=1)
    )
