import torch

def compute_entropy(field, dx=1.0):
    grad_x = (torch.roll(field, -1, dims=0) - torch.roll(field, 1, dims=0)) / (2 * dx)
    grad_y = (torch.roll(field, -1, dims=1) - torch.roll(field, 1, dims=1)) / (2 * dx)
    entropy = (grad_x**2 + grad_y**2).mean().item()
    return entropy
