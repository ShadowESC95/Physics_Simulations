import torch

def compute_entropy(phi):
    """
    Compute a rough entropy-like functional of the field.
    Here, we use a basic energy/gradient-based approximation.

    Args:
        phi (torch.Tensor): Scalar field

    Returns:
        float: Scalar entropy-like value
    """
    grad_x = phi[:, 1:] - phi[:, :-1]
    grad_y = phi[1:, :] - phi[:-1, :]
    
    # Pad gradients to match dimensions
    grad_x = torch.nn.functional.pad(grad_x, (0, 1))
    grad_y = torch.nn.functional.pad(grad_y, (0, 0, 0, 1))
    
    energy_density = grad_x**2 + grad_y**2 + (phi**2 - 1)**2
    return energy_density.mean().item()
