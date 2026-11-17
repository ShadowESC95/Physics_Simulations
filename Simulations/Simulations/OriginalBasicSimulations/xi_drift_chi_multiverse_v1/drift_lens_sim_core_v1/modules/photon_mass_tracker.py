import numpy as np
import matplotlib.pyplot as plt
import os

def track_photon_mass(teff_sequence, out_path="output/photon_mass_evolution.png"):
    os.makedirs("output", exist_ok=True)
    mass_log = []

    for field in teff_sequence:
        grad_y, grad_x = np.gradient(field)
        grad_mag = np.sqrt(grad_x**2 + grad_y**2)
        m_photon = np.mean(grad_mag) * 1e-33  # Toy scaling
        mass_log.append(m_photon)

    plt.figure(figsize=(8, 4))
    plt.plot(mass_log, color='gold')
    plt.xlabel("Frame")
    plt.ylabel("Photon Mass (arb. units)")
    plt.title("Photon Mass Emergence from ∇Teff")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"🧲 Photon mass tracking graph saved to {out_path}")
