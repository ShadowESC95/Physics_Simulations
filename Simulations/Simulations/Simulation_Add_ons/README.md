
# Ξ–χ Decoherence Framework

This repository contains a full simulation and theoretical analysis suite for a novel coupled scalar field model — the Ξ–χ framework — in which decoherence is driven dynamically by entropy gradients in Ξ, coupled to a dark-sector field χ.

## 📦 Contents

| File | Description |
|------|-------------|
| `XiChi_Decoherence_Simulation.ipynb` | Base GPU simulation of Ξ–χ fields with decoherence |
| `XiChi_AdvancedAnalysis_Simulation.ipynb` | FFT, energy diagnostics, coherence index tracker |
| `XiChi_Simulation_SaveNPZ.ipynb` | Saves field frames every N steps as `.npz` |
| `XiChi_Animation_GIF_Generator.ipynb` | Converts saved fields into `.gif` animations |
| `XiChi_CosmologicalScaling_Simulation.ipynb` | Adds Hubble expansion (radiation/matter era scaling) |
| `XiChi_ParameterScan.ipynb` | Parameter scan across ε, λ, Γ, α with coherence tracking |
| `XiChi_Observational_Consequences.tex` | Summary of cosmological predictions |
| `XiChi_Decoherence_Lagrangian.tex` | Full mathematical formulation (EoMs, Lagrangian) |
| `Dockerfile` | Containerized environment for all simulations |

## 🧠 Theory Overview

The Ξ–χ model couples a scalar field χ (ultralight dark photon candidate) to a structured entropy field Ξ, via the Lagrangian term:

```
L ⊃ ε Ξ² χ²  +  V(Ξχ - Γ)
```

Decoherence in χ is dynamically sourced by:
```
Γ_decoh ∼ α₁ |∇Ξ|² + α₂ Ξ²
```

The system supports:
- FFT spectral suppression
- Entropy-driven dephasing
- Conformal cosmological scaling
- Stability across Lagrangian regimes

## 🚀 Run Instructions

1. Install dependencies:
```bash
pip install torch matplotlib numpy imageio
```

2. Launch notebooks:
```bash
jupyter notebook
```

3. Run parameter scans or cosmological expansion modes.

## 🧪 Docker

Build and run with:
```bash
docker build -t xichi .
docker run -p 8888:8888 xichi
```

---

Developed as a rigorous exploration of decoherence-field interactions in quantum cosmology and dark sector phenomenology.
