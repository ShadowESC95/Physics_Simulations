import numpy as np

def _grad(a, axis, dx=1.0):
    return np.gradient(a, dx, axis=axis, edge_order=2)

def compute_polarization_metrics(E, dx=1.0, dy=1.0, dz=1.0, return_components=False):
    """
    E shape (..., 3). Returns:
      mag: |E| (scalar field)
      div: ∇·E
      curl_mag: |∇×E|
    """
    if E.shape[-1] != 3:
        raise ValueError("E must have last dimension = 3")
    Ex, Ey, Ez = E[..., 0], E[..., 1], E[..., 2]

    mag = np.sqrt(Ex**2 + Ey**2 + Ez**2)

    dEx_dx = _grad(Ex, 0, dx)
    dEy_dy = _grad(Ey, 1, dy)
    dEz_dz = _grad(Ez, 2, dz) if Ez.ndim >= 3 else 0.0
    div = dEx_dx + dEy_dy + (dEz_dz if isinstance(dEz_dz, np.ndarray) else 0.0)

    dEz_dy = _grad(Ez, 1, dy) if Ez.ndim >= 2 else 0.0
    dEy_dz = _grad(Ey, 2, dz) if Ey.ndim >= 3 else 0.0
    dEx_dz = _grad(Ex, 2, dz) if Ex.ndim >= 3 else 0.0
    dEz_dx = _grad(Ez, 0, dx)
    dEy_dx = _grad(Ey, 0, dx)
    dEx_dy = _grad(Ex, 1, dy)

    curl_x = dEz_dy - dEy_dz
    curl_y = dEx_dz - dEz_dx
    curl_z = dEy_dx - dEx_dy
    curl_mag = np.sqrt(curl_x**2 + curl_y**2 + curl_z**2)

    return (mag, div, (curl_x, curl_y, curl_z), curl_mag) if return_components else (mag, div, curl_mag)
