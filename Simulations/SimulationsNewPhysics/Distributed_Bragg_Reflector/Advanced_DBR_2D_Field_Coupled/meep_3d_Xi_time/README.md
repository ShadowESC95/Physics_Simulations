
# Meep 3D Ξ(t,x,y,z) Time-Evolving Simulation Engine

## Structure:
- `run_simulation.py`: main simulation script
- `Xi_generator.py`: entropy field generator
- `epsilon_export.py`: exporter to .vtu and .h5
- `config.json`: configurable geometry, fields, and source
- `dielectric_models/`: placeholder for real ε(λ)
- `outputs/`: all results stored here

## Features:
- Time-evolving entropy Ξ(t,x,y,z)
- Dynamic ε(x,y,z,t) via MaterialGrid or epsilon_func
- Export in .npy, .h5, .vtu formats
- Parameter sweep support (to be expanded)

## Dependencies:
- `meep`, `numpy`, `h5py`, `pyvista`, `matplotlib`

Run:
```bash
python run_simulation.py
```
