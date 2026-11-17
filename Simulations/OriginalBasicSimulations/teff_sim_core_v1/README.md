# Teff Scalar Field Simulation (DRIFT-compatible)

Simulates scalar field evolution driven by recursive Teff modulation.
Supports entropy tracking, GPU acceleration, and dynamic visualization.

## Structure

- `main.py`: Runs the simulation
- `config.py`: Global parameters
- `engine/`: Field evolution, entropy, and utilities
- `visual/`: Plotting + animation
- `output/`: Auto-generated result folder

## Requirements

- numpy
- matplotlib
- torch
- ffmpeg (for animation)

## Run

```bash
python main.py
