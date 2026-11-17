# Ξχ Scalar Field GUI & Simulation Suite (Advanced)

Explore coupled scalar field dynamics between Ξ and χ using GPU-accelerated solvers, real-time visualization, and volumetric rendering tools.

---

## 🔬 Features

- Entropy-curvature feedback tracking
- Drift tensor overlays
- MPI-enabled Torch evolution
- yt-based volumetric rendering
- Dual-field Ξχ dynamics
- TensorBoard analytics per rank
- UMAP clustering + stability analysis
- RNN-based trajectory classifiers
- LaTeX auto-generated simulation reports
- Dash GUI with sliders, toggles
- PyQt5 3D tabbed visualizer
- TikZ/PDF export for field diagrams

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt

# Main sim
python3 run_sim.py

# MPI sim
mpirun -n 4 python3 sim/parallel_launcher.py

# Launch Qt GUI
python3 visual/qt_field_viewer3d.py

# Launch Dash GUI
python3 app.py

# TensorBoard
tensorboard --logdir logs/

# Generate Phase Portrait
make phase

# Analyze Stability
make stability

# Export PDF Report
make report
