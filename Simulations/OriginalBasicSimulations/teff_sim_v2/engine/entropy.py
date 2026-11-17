import torch

def compute_entropy(field):
    eps = 1e-8  # Prevent log(0)
    field = torch.clamp(field, eps, 1.0)  # Keep values within valid entropy range
    entropy = -field * torch.log(field)
    return entropy.sum().item()
