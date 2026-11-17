
import meep as mp
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("epsilon_modulated_profile.csv", delimiter=",", skiprows=1)
x_data, eps_data = data[:,0], data[:,1]

def epsilon_func(p):
    idx = int((p.x / 16.0) * 1999)
    return eps_data[min(max(idx, 0), 1999)]

resolution = 50
cell_size = mp.Vector3(16, 0, 0)

geometry = [mp.Block(size=mp.Vector3(16, mp.inf, mp.inf),
                     center=mp.Vector3(8),
                     material=mp.Medium(epsilon_func=epsilon_func))]

sources = [mp.Source(mp.GaussianSource(frequency=1/1.55, fwidth=0.3),
                     component=mp.Ez,
                     center=mp.Vector3(-5))]

sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=[mp.PML(1.0)],
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

trans = sim.add_flux(1/1.55, 0.4, 100, mp.FluxRegion(center=mp.Vector3(6)))
sim.run(until=200)

frequencies = mp.get_flux_freqs(trans)
flux_data = mp.get_fluxes(trans)

plt.plot([1/f for f in frequencies], flux_data)
plt.xlabel("Wavelength (um)")
plt.ylabel("Transmitted Flux")
plt.title("Ξ–χ–φ Modulated DBR Transmission")
plt.grid(True)
plt.show()
