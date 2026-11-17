import torch

def evolve_chi_field(chi, phi, dt, lap_fn):
    """
    Evolve a secondary scalar field chi coupled to Teff (phi).
    Uses a reaction-diffusion style update.
    """
    lap = lap_fn(chi)
    coupling = phi * (1 - chi**2)
    dchi_dt = lap + coupling
    return chi + dt * dchi_dt

def init_chi(grid_size, noise=0.1, device='cpu'):
    chi = torch.zeros((grid_size, grid_size), device=device)
    chi += noise * torch.randn_like(chi)
    return chi
