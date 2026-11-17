# geometry/boundary_conditions.py

import numpy as np

def apply_dirichlet_boundary(field, value=0.0):
    """
    Applies Dirichlet (fixed) boundary conditions to all faces of a scalar field.

    Args:
        field (np.ndarray): Scalar or vector field
        value (float or list): Value(s) to assign at boundary

    Returns:
        np.ndarray: Modified field with boundary applied
    """
    field[0, ...] = value
    field[-1, ...] = value
    field[:, 0, ...] = value
    field[:, -1, ...] = value
    field[:, :, 0, ...] = value
    field[:, :, -1, ...] = value
    return field

def apply_neumann_boundary(field):
    """
    Applies Neumann (zero-gradient) boundary condition by copying adjacent values.

    Args:
        field (np.ndarray): Field to apply BC to

    Returns:
        np.ndarray: Modified field
    """
    field[0, ...] = field[1, ...]
    field[-1, ...] = field[-2, ...]
    field[:, 0, ...] = field[:, 1, ...]
    field[:, -1, ...] = field[:, -2, ...]
    field[:, :, 0, ...] = field[:, :, 1, ...]
    field[:, :, -1, ...] = field[:, :, -2, ...]
    return field

def apply_boundary_conditions(fields, config):
    """
    Applies boundary conditions to all fields in simulation.

    Args:
        fields (dict): Dictionary of fields
        config (dict): Config with boundary type
    """
    bc_type = config.get("boundary", "neumann")

    for key, field in fields.items():
        if key in ["g_mu_nu", "A_mu", "stueckelberg_mass"]:
            continue  # Skip gauge tensor and mass term

        if bc_type == "dirichlet":
            fields[key] = apply_dirichlet_boundary(field, value=0.0)
        elif bc_type == "neumann":
            fields[key] = apply_neumann_boundary(field)
        else:
            raise ValueError(f"Unknown boundary type: {bc_type}")

