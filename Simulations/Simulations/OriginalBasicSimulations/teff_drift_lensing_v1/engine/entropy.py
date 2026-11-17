import torch

def compute_entropy(field):
    prob = field**2
    prob /= prob.sum()
    entropy = -torch.sum(prob * torch.log(prob + 1e-10))
    return entropy.item()
