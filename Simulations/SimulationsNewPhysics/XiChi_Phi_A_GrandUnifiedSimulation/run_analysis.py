# run_analysis.py

import numpy as np
from simulation.attractor_analysis import detect_attractors
from simulation.coherence_decay_tracker import mutual_information_entropy
from simulation.symmetry_breaking_tracker import compute_symmetry_breaking
from visualization.visualization_tools import save_field_plot

def run_post_simulation_analysis(fields, field_history=None, output_dir='analysis_outputs'):
    """
    Perform attractor/coherence/symmetry analysis and save results.

    Args:
        fields (dict): Final state fields
        field_history (dict of lists): Time-sequenced field histories
        output_dir (str): Where to save figures
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # 1. Coherence metric (χ)
    chi = fields.get('chi')
    if chi is not None:
        coherence = mutual_information_entropy(chi)
        print(f"[χ Coherence Metric] {coherence:.5f}")
        save_field_plot(chi, filename=f"{output_dir}/chi_final.png", title='χ Final')

    # 2. Attractor detection (Ξ)
    if field_history and 'xi' in field_history:
        attractor_mask = detect_attractors(field_history['xi'])
        save_field_plot(attractor_mask.astype(float), filename=f"{output_dir}/xi_attractors.png", title='Ξ Attractor Mask')

    # 3. Symmetry breaking (Ξ)
    xi = fields.get('xi')
    if xi is not None:
        asymmetry = compute_symmetry_breaking(xi, axis='x')
        print(f"[Ξ Asymmetry (x-axis)] {asymmetry:.5f}")
        save_field_plot(xi, filename=f"{output_dir}/xi_final.png", title='Ξ Final')

