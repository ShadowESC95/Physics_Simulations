import torch

def compute_drift_tensor(phi, lap_fn):
    grad_x = phi[:, 1:] - phi[:, :-1]
    grad_y = phi[1:, :] - phi[:-1, :]

    grad_x = torch.nn.functional.pad(grad_x, (0, 1))
    grad_y = torch.nn.functional.pad(grad_y, (0, 0, 0, 1))
    lap = lap_fn(phi)

    tensor_field = torch.stack([
        torch.stack([grad_x**2, grad_x * grad_y], dim=-1),
        torch.stack([grad_x * grad_y, grad_y**2], dim=-1)
    ], dim=-2)

    drift_tensor = tensor_field + 0.1 * lap.unsqueeze(-1).unsqueeze(-1)
    return drift_tensor
