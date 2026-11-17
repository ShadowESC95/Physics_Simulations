import torch

def init_chi(grid_size, noise=0.01, device="cpu"):
    chi = torch.zeros((grid_size, grid_size), device=device)
    chi += noise * torch.randn_like(chi)
    return chi

def evolve_chi_field(chi, xi_log, coupling_strength=0.05):
    chi_log = []
    for xi_frame in xi_log:
        xi_t = torch.tensor(xi_frame, dtype=torch.float32, device=chi.device)
        dchi_dt = -chi + coupling_strength * xi_t
        chi += 0.01 * dchi_dt
        chi_log.append(chi.detach().cpu().numpy())
    return chi_log
