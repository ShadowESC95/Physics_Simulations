# simulation/parameter_sweep.py

from simulation.field_equation_solver import run_field_simulation
import itertools
import yaml
import os

def sweep_parameters(base_config, param_grid, output_dir="sweep_results"):
    """
    Runs the simulation for every combination of parameters in the grid.

    Args:
        base_config (dict): The default simulation configuration
        param_grid (dict): Dict of parameter_name: [values...]
        output_dir (str): Base directory to store outputs
    """
    os.makedirs(output_dir, exist_ok=True)
    keys = list(param_grid.keys())
    all_combinations = list(itertools.product(*param_grid.values()))

    for combo in all_combinations:
        config = base_config.copy()
        label_parts = []
        for k, v in zip(keys, combo):
            config[k] = v
            label_parts.append(f"{k}={v}")
        label = "__".join(label_parts)

        print(f"[Sweep] Running for: {label}")
        config["output_path"] = os.path.join(output_dir, label)
        os.makedirs(config["output_path"], exist_ok=True)

        with open(os.path.join(config["output_path"], "config_used.yaml"), "w") as f:
            yaml.dump(config, f)

        run_field_simulation(config)

