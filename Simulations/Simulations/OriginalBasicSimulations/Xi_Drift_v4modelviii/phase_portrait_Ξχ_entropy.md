# Ξχ Phase Portrait Explorer

## Purpose

Visualize how the scalar fields Ξ and χ evolve over entropy, curvature, and drift space. Useful to:

- Identify attractors
- Locate Janus points
- Track causal symmetry reversal (Big Bang ↔ Heat Death)

---

## Plot Axes

- **X-axis:** Entropy $S(t)$
- **Y-axis:** Curvature of entropy $C(t) = \frac{d^2S}{dt^2}$
- **Z-axis:** Drift variance $V_D(t) = \text{Var}(D_{ij}(t))$

## Data Source

- `xi_entropy_log.npy`
- `drift_tensor_Xi.npy`
- Optional: Add `janus_point_idx` from Janus detector

---

## Visual Output

- Spiral loops for arrow of time
- Collapse + rebirth cycles
- Reversible segments before Janus (entropy curvature changes sign)
- TikZ and PDF export available

## CLI Tool Coming

```bash
python generate_phase_plot.py --entropy output/xi_entropy_log.npy \
                              --drift output/drift_tensor_Xi.npy \
                              --out plots/phase_spiral.png
