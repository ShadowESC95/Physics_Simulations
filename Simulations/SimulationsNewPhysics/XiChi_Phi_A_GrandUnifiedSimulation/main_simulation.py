# main_simulation.py

import yaml
import os
from simulation.field_equation_solver import run_field_simulation
from simulation.coherence_decay_tracker import mutual_information_entropy
from interactions.stueckelberg_mass_mechanism import compute_stueckelberg_term
from interactions.gauge_fixing import lorenz_gauge_fix
from geometry.initial_conditions import initialize_fields
from interactions.lagrangian_dynamics import get_field_equations
import argparse
import os

def load_config(path="config.yaml"):
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, path)
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()
    print("[ΞχφAμ-Gμν] Simulation started")

    # Initialize fields (including Aμ and φ)
    fields = initialize_fields(config)

    # --- Apply Stueckelberg mass term ---
    print(" > Applying Stueckelberg mass mechanism...")
    st_mass = compute_stueckelberg_term(
        phi_field=fields['phi'],
        gauge_field=fields['A_mu'],
        coupling_constant=config.get("stueckelberg_coupling", 1.0)
    )
    fields['stueckelberg_mass'] = st_mass

    # --- Apply Lorenz gauge fixing ---
    print(" > Enforcing Lorenz gauge...")
    fields['A_mu'] = lorenz_gauge_fix(fields['A_mu'])

    # --- Run full simulation ---
    print(" > Solving full coupled field equations...")
    final_fields = run_field_simulation(config)

    # --- Evaluate Coherence Decay ---
    print(" > Analyzing χ-field coherence...")
    chi_field = final_fields.get("chi")
    if chi_field is not None:
        coherence_score = mutual_information_entropy(chi_field)
        print(f"   [χ Decoherence Metric]: {coherence_score:.5f}")
    else:
        print("   [Warning] χ field missing from output")

    print("[ΞχφAμ-Gμν] Simulation complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    main()

