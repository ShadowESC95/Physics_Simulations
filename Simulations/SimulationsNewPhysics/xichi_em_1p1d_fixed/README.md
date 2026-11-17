# Ξ–χ + split-EM (A_E, A_B) — 1+1D Lagrangian Simulation

This package implements a **single, explicit Lagrangian density**

L = 1/2[(∂tΞ)^2 - cΞ^2 (∂xΞ)^2] + 1/2[(∂tχ)^2 - cχ^2 (∂xχ)^2] - V(Ξ,χ)
  + Σ_{a∈{E,B}} [ 1/2 ε(Ξ,χ) (∂t A_a)^2 - 1/2 μ^{-1}(Ξ,χ) (∂x A_a)^2 - 1/2 m_γ(Ξ,χ;ε_s)^2 A_a^2 ].

Two transverse gauge potentials A_E, A_B represent split EM channels in 1+1D.
Energy density and EOMs are **derived from the same L** to avoid analysis mismatch.

Quick start:
    python run_xichi_simulations.py
    python epsilon_sweep.py
Outputs are written to ./out and ./out_sweep.
