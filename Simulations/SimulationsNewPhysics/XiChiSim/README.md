# XiChiSim: Emergent Electrodynamics Simulation Framework

**XiChiSim** is a simulation suite implementing the "Entropy–Coherence Electrodynamics" framework:contentReference[oaicite:46]{index=46}, where electric and magnetic fields (E, B) emerge from two fundamental scalar fields: Ξ (entropy field) and χ (coherence field). This README provides setup and usage instructions.

## Features
- Solves coupled Ξ–χ field equations using finite element methods (FEniCSx + PETSc) in the **solver module**, recovering classical Maxwell dynamics in the locked regime.
- **Field initialization** library to configure initial conditions (vacuum, point charge, vortex, etc.) in accordance with theoretical scenarios.
- **Observables pipeline** to compute E, B, effective charge/current densities, etc., from Ξ and χ at runtime, ensuring results can be interpreted physically.
- **Multi-engine support**: prototypes with Devito (finite-difference), Meep (FDTD), MFEM (high-order FEM), Dedalus (spectral) to validate and extend the solver's capabilities.
- **Visualization**: interactive 3D visualization with PyVista/Qt (real-time inspection of field evolution) and support for ParaView Catalyst for large-scale in-situ visualization.
- **Cosmology hooks**: placeholders to connect simulation outputs to cosmological calculations (CLASS), enabling exploration of dark energy and large-scale structure implications of the Ξ–χ fields.

## Installation
1. Install Miniconda or Anaconda.
2. Create the environment: `conda env create -f environment.yml`
3. Activate the environment: `conda activate xichisim_env`

This will install FEniCSx, PETSc, and other dependencies. (Ensure MPI is configured if running in parallel.)

## Usage
- **Running a Simulation:** Edit `solver/xi_chi_solver.py` to adjust parameters (domain size, duration, initial condition profile, etc.), or use default settings. Then run:
  ```bash
  python solver/xi_chi_solver.py

