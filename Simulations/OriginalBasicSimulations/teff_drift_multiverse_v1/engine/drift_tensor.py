import torch

def compute_drift_tensor(phi, lap_fn):
    """
    Compute a proxy DRIFT tensor for Teff field phi.

    Args:
        phi (torch.Tensor): Scalar field grid
        lap_fn (callable): Function to compute laplacian

    Returns:
        torch.Tensor: A DRIFT-like tensor field [NxNx2x2]
    """
    grad_x = phi[:, 1:] - phi[:, :-1]
    grad_y = phi[1:, :] - phi[:-1, :]

    # Pad gradients to match dimensions
    grad_x = torch.nn.functional.pad(grad_x, (0, 1))
    grad_y = torch.nn.functional.pad(grad_y, (0, 0, 0, 1))

    lap = lap_fn(phi)

    # Create simple symmetric 2x2 tensor at each grid point
    tensor_field = torch.stack([
        torch.stack([grad_x**2, grad_x * grad_y], dim=-1),
        torch.stack([grad_x * grad_y, grad_y**2], dim=-1)
    ], dim=-2)

    # Inject Laplacian as scalar curvature modulation
    drift_tensor = tensor_field + 0.1 * lap.unsqueeze(-1).unsqueeze(-1)

    return drift_tensor
