
# Ξ–χ FEniCSx + PyVista + Qt Simulation Environment

This simulation environment models the evolution of the Ξ–χ scalar field system over a 4D grid using FEniCSx.
It includes spontaneous symmetry breaking, attractor basin tracking, and live visualization.

## Structure

- `solver/` : FEniCSx PDE solver for Ξ and χ field dynamics
- `visualization/` : PyVista + Qt GUI for real-time rendering
- `data/` : Time-evolved output in XDMF/VTU format
- `config/` : Simulation parameters and domain setup
- `docs/` : Theory background and usage instructions

## Getting Started

Run the solver:

```bash
python solver/xi_chi_solver.py
```

Launch the GUI:

```bash
python visualization/gui.py
```
