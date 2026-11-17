import torch
from engine.entropy import compute_entropy
from engine.utils import laplacian
from config import ENTROPY_LOG_INTERVAL, CHI_COUPLING, DEVICE

def evolve_xi_with_chi(xi, chi, tensor, steps, dt, device=DEVICE):
    xi_log = []
    entropy_log = []

    xi = xi.to(device)
    chi = chi.to(device)
    tensor = tensor.to(device)

    for step in range(steps):
        lap = laplacian(xi)

        # Drift tensor contribution
        drift_term = torch.einsum('ijkl,ij->ij', tensor, xi**2)

        # χ feedback modulation into Ξ
        chi_feedback = CHI_COUPLING * chi * xi**2

        # Ξ evolution
        dxi_dt = lap - xi * (xi - 1)**2 + drift_term + chi_feedback
        xi += dt * dxi_dt

        # Optional: Clamp to avoid numerical blowup (esp. with high λ)
        xi = torch.clamp(xi, min=1e-6, max=10.0)

        # Log data periodically
        if step % ENTROPY_LOG_INTERVAL == 0:
            xi_log.append(xi.detach().cpu().numpy())
            entropy_log.append(compute_entropy(xi))

    return xi_log, entropy_log
