import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Grid settings
nx, ny = 200, 200
dx = dy = 0.1
dt = 0.01
T_total = 2.0
steps = int(T_total / dt)

# Scalar field & derivative storage
phi = np.ones((nx, ny)) * 0.7 + 0.01 * np.random.randn(nx, ny)
phi_new = np.zeros_like(phi)
phi_prev = np.copy(phi)
V0, beta = 1.0, 0.2  # Potential terms

# Recursive DRIFT-style scaling (can be refined)
drift_scaling = np.linspace(1.0, 0.5, nx)[:, None] * np.linspace(1.0, 0.5, ny)

# Time evolution: Klein–Gordon with feedback
def laplacian(f):
    return (np.roll(f, 1, axis=0) + np.roll(f, -1, axis=0) +
            np.roll(f, 1, axis=1) + np.roll(f, -1, axis=1) - 4 * f) / dx**2

# Potential term: non-linear self-coupling
def potential_deriv(phi):
    return V0 * phi * (phi**2 - beta**2)

# Simulation core loop
entropy_log = []

def update_field(t):
    global phi, phi_new, phi_prev
    lap = laplacian(phi)
    V_prime = potential_deriv(phi)
    
    # Recursive drift tensor impact (could evolve with t)
    phi_new = (2 * phi - phi_prev +
               dt**2 * (lap - V_prime + 0.05 * drift_scaling * phi))

    phi_prev, phi = phi, phi_new

    # Entropy estimator (simplified)
    grad = np.gradient(phi)
    entropy = np.sum((grad[0]**2 + grad[1]**2) / (phi**2 + 1e-5))
    entropy_log.append(entropy)

    return phi

# Visualization
fig, ax = plt.subplots()
im = ax.imshow(phi, cmap='plasma', origin='lower', vmin=0, vmax=1.5)
plt.title("Teff Scalar Field Evolution")

def animate(i):
    frame = update_field(i)
    im.set_array(frame)
    return [im]

ani = FuncAnimation(fig, animate, frames=steps, interval=30, blit=True)
plt.show()

# Plot entropy over time
plt.figure()
plt.plot(np.linspace(0, T_total, steps), entropy_log)
plt.title("Entropy Growth (Gradient Functional)")
plt.xlabel("Time")
plt.ylabel("Entropy Proxy")
plt.grid()
plt.show()
