import torch

def compute_entropy(field):
    norm = field / field.sum()
    entropy = -torch.sum(norm * torch.log(norm + 1e-10))
    return entropy.item()
