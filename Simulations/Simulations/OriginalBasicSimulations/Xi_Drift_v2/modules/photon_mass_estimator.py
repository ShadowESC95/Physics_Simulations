import torch

def estimate_photon_mass(xi_field, kappa=1e-6):
    grad = torch.gradient(xi_field)
    grad_norm_sq = sum((g ** 2 for g in grad))
    return kappa * grad_norm_sq.mean().item()
