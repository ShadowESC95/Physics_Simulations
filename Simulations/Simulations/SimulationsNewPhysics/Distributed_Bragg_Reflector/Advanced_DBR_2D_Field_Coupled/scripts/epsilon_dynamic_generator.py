
import numpy as np

# Grid and time
Nx, Ny, Nz = 100, 60, 40
Nt = 50
x = np.linspace(0, 16, Nx)
y = np.linspace(0, 8, Ny)
z = np.linspace(0, 4, Nz)
t = np.linspace(0, 10, Nt)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Static fields
χ = 0.05 * np.cos(10 * np.pi * X / x.max())
φ = 0.03 * np.sin(5 * np.pi * X / x.max())

# Dynamic entropy Ξ(t,x,y,z)
Ξ = np.zeros((Nt, Nx, Ny, Nz))
for i, ti in enumerate(t):
    Ξ[i] = 0.1 * np.exp(-((X - 8)**2 + (Y - 4)**2 + (Z - 2)**2) / (1 + 0.1 * ti)**2)

# Thermal drift profile
T0 = 300  # ambient K
ΔT = 50 * np.exp(-((X - 8)**2 + (Y - 4)**2 + (Z - 2)**2))  # static hot spot
T = T0 + ΔT

# ε(x,y,z,t) = ε0 + α·∇Ξ + β·χ + γ·φ² + αT·(T - T0)
ε0, α, β, γ, αT = 2.25, 1.0, 2.0, 3.0, 0.002
ε = np.zeros((Nt, Nx, Ny, Nz))
for i in range(Nt):
    gradΞ = np.gradient(Ξ[i], axis=0)
    ε[i] = ε0 + α * gradΞ + β * χ + γ * φ**2 + αT * (T - T0)

# Save one snapshot
np.save("epsilon_dynamic_t25.npy", ε[Nt//2])
