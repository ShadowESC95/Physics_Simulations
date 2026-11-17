# simulation/time_evolution_solver.py

import numpy as np
from geometry.boundary_conditions import apply_boundary_conditions

def time_step_evolution(fields, sources, config):
    """
    Applies a single forward Euler update to all relevant fields.

    Args:
        fields (dict): Current state of all fields
        sources (dict): Dict of source terms for each field
        config (dict): Config with timestep and boundary info

    Returns:
        dict: Updated field dictionary
    """
    dt = config.get("timestep", 0.001)

    for key in sources:
        if key in fields:
            fields[key] = fields[key] + dt * sources[key]

    apply_boundary_conditions(fields, config)
    return fields

