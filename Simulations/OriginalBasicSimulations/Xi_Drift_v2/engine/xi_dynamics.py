import torch
from engine.entropy import compute_entropy

def evolve_xi_with_chi(xi, chi, tensor, steps, dt, device='cpu'):
    xi_log = []
    entropy_log = []

    for step in range(steps):
        lap = (
            -4 * xi
            + torch.roll(xi, 1, 0)
            + torch.roll(xi, -1, 0)
            + torch.roll(xi, 1, 1)
            + torch.roll(xi, -1, 1)
        )

        drift_term = torch.einsum('ijkl,ij->ij', tensor, xi**2)
        chi_feedback = 0.1 * chi * xi**2

        dxi_dt = lap - xi * (xi - 1)**2 + drift_term + chi_feedback
        xi += dt * dxi_dt

        if step % 5 == 0:
            xi_log.append(xi.detach().cpu().numpy())
            entropy_log.append(compute_entropy(xi))

    return xi_log, entropy_log
