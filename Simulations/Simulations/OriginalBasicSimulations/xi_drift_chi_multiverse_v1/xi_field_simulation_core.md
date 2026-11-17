# ξ Field Simulation Core Documentation

## Codebase Modules

- **engine/xi_dynamics.py**: Time evolution of ξ via finite difference.
- **engine/drift_tensor.py**: Tensor field based on ∇ξ + Laplacian modulation.
- **modules/chi_field.py**: χ field logic and evolution rules.
- **visual/animate_field.py**: Frame-by-frame visualization.

---

## Main Equation

\[
\frac{∂ξ}{∂t} = Δξ - ξ(ξ - 1)^2 + T_{ij} ξ^2
\]

---

## Stability Notes

- Choose `DT` such that:
\[
DT \lt \frac{dx^2}{4}
\]

- Entropy tracking added every N steps.
- DRIFT tensor updates optional (cached or real-time).

---

## File Outputs

- `output/entropy_log.csv`
- `output/xi_field_log.npy`
- `output/chi_field_log.npy`
- `output/xi_chi_drift_overlay.png`

