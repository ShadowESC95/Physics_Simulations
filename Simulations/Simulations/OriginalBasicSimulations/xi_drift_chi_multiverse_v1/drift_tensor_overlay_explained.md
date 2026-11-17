# DRIFT Tensor Overlay Explained

## What is the DRIFT Tensor?

The DRIFT tensor represents a second-order symmetric tensor field derived from the scalar field ξ(x, t). It encodes directionality in ξ’s spatial variations.

\[
T_{ij} = \partial_i ξ \partial_j ξ + λ ⋅ Δξ ⋅ δ_{ij}
\]

## Purpose

- Serves as a **lensing proxy**.
- Enables **anisotropic field growth**.
- Guides **directional overlays** in the visualization.

---

## How It's Used

- Visualized with vector fields (e.g. arrows on top of ξ).
- Coupled to entropy gradient.
- Interacts with χ to create **dynamic directional evolution**.

---

## Plot Integration

- Use `quiver` for arrow plots.
- Normalize vectors before drawing to avoid skewing.

---

## Output Examples

- `plot_teff_with_tensor_overlay(...)` generates a 2D or 3D matplotlib figure.
- Output can be combined with entropy curves or χ overlays for richer views.

