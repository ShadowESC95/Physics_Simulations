import torch

def compute_entropy(field):
    """Shannon-like entropy measure for scalar field"""
    prob = torch.abs(field)
    prob = prob / prob.sum()
    entropy = -(prob * torch.log(prob + 1e-10)).sum()
    return entropy.item()
