
# Ξ–χ Framework (Model 5 Horndeski Extension)

This repository contains simulations, visualizations, and observational test tools for an entropy-curvature scalar field theory built around a generalized Horndeski Lagrangian.

## Included
- Full Dash dashboard for real-time Ξ field exploration
- Auto-simulation pipeline
- CMB birefringence and alpha-drift test integration
- Docker container for portable deployment

## To Run Dashboard
```bash
python model5_dashboard_full.py
```

## To Build Docker Container
```bash
docker-compose up --build
```

## To Simulate
```bash
python simulate_model5.py --steps 200 --gamma_5 0.05 --m 1.0
```

## To Compare with Planck Birefringence
```bash
python compare_planck_biref.py
```
    