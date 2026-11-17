import torch
from engine.entropy import compute_entropy

def evolve_xi_with_chi(xi, chi, tensor, steps, dt, device):
    """
    Evolve the Ξ field with χ feedback, drift tensor, and entropy tracking.

    Args:
        xi (torch.Tensor): Initial Ξ field, shape (N, N), on the specified device.
        chi (torch.Tensor): Initial χ field, shape (N, N), on the specified device.
        tensor (torch.Tensor): Drift tensor, shape (N, N, 2, 2), on the specified device.
        steps (int): Number of time steps to run.
        dt (float): Time step size.
        device (torch.device): CPU or CUDA device.

    Returns:
        xi_log (list): List of Ξ field snapshots (numpy arrays), logged every 5 steps.
        entropy_log (list): List of entropy values at each log step.
    """
    xi_log = []
    entropy_log = []

    for step in range(steps):
        # 2D Laplacian using periodic boundaries (finite difference)
        lap = (
            -4 * xi
            + torch.roll(xi, 1, 0)
            + torch.roll(xi, -1, 0)
            + torch.roll(xi, 1, 1)
            + torch.roll(xi, -1, 1)
        )

        # Drift tensor contraction: (N,N,2,2) x (N,N) => (N,N)
        drift_term = torch.einsum('ijkl,ij->ij', tensor, xi ** 2)
        chi_feedback = 0.1 * chi * xi ** 2  # χ-Ξ coupling (adjust strength as needed)

        dxi_dt = lap - xi * (xi - 1) ** 2 + drift_term + chi_feedback
        xi = xi + dt * dxi_dt

        if step % 5 == 0:
            xi_log.append(xi.detach().cpu().numpy())
            entropy_log.append(compute_entropy(xi))

    return xi_log, entropy_log

