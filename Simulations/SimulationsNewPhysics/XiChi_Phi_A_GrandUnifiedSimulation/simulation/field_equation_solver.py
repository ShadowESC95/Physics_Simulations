# simulation/field_equation_solver.py

from interactions.lagrangian_dynamics import get_field_equations as compute_field_equations
from geometry.initial_conditions import initialize_fields
from simulation.time_evolution_solver import time_step_evolution
from visualization.vtu_exporter import export_vtu
import numpy as np

def run_field_simulation(config):
    """
    Main field equation solver loop.
    
    Args:
        config (dict): Simulation configuration dictionary
    """
    fields = initialize_fields(config)

    timesteps = config.get("timesteps", 5000)
    export_interval = config.get("export_interval", 500)

    for t in range(timesteps):
        source_terms = compute_field_equations(fields, config)
        fields = time_step_evolution(fields, source_terms, config)

        if t % export_interval == 0:
            export_vtu(fields, t, config)

    return fields

