import torch

def init_chi(grid_size, noise=0.01, device="cpu"):
    chi = torch.zeros((grid_size, grid_size), device=device)
    chi += noise * torch.randn_like(chi)
    return chi

def evolve_chi_field(chi, xi_log, coupling_strength=0.1):
    chi_log = []
    for xi in xi_log:
        xi_torch = torch.tensor(xi, dtype=torch.float32)
        dchi_dt = coupling_strength * xi_torch
        chi += dchi_dt
        chi_log.append(chi.detach().cpu().numpy())
    return chi_log
