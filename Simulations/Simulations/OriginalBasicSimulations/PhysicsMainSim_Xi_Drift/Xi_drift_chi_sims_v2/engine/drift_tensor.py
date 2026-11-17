import torch

def compute_drift_tensor(xi, lap_fn):
    grad_x = xi[:, 1:] - xi[:, :-1]
    grad_y = xi[1:, :] - xi[:-1, :]

    grad_x = torch.nn.functional.pad(grad_x, (0, 1))
    grad_y = torch.nn.functional.pad(grad_y, (0, 0, 0, 1))
    lap = lap_fn(xi)

    tensor_field = torch.stack([
        torch.stack([grad_x**2, grad_x * grad_y], dim=-1),
        torch.stack([grad_x * grad_y, grad_y**2], dim=-1)
    ], dim=-2)

    return tensor_field + 0.1 * lap.unsqueeze(-1).unsqueeze(-1)
