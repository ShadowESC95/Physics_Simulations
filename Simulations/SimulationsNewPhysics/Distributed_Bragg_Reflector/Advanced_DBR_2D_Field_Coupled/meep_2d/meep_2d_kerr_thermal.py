
import meep as mp
import numpy as np
import matplotlib.pyplot as plt

eps_data = np.load("epsilon_modulated_2d.npy")
Nx, Ny = eps_data.shape

sx, sy = 16, 8
resolution = 20

cell = mp.Vector3(sx, sy, 0)
pml_layers = [mp.PML(1.0)]

design_region = mp.MaterialGrid(mp.Vector3(Nx, Ny),
                                mp.Medium(epsilon=1.0),
                                mp.Medium(epsilon=12.0),
                                weights=eps_data.clip(1.0, 12.0))

geometry = [mp.Block(center=mp.Vector3(),
                     size=mp.Vector3(sx, sy, mp.inf),
                     material=design_region)]

sources = [mp.Source(mp.GaussianSource(frequency=1/1.55, fwidth=0.3),
                     component=mp.Ez,
                     center=mp.Vector3(-6, 0))]

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

trans = sim.add_flux(1/1.55, 0.4, 100, mp.FluxRegion(center=mp.Vector3(6, 0)))
sim.run(until=300)

frequencies = mp.get_flux_freqs(trans)
flux_data = mp.get_fluxes(trans)

plt.plot([1/f for f in frequencies], flux_data)
plt.xlabel("Wavelength (um)")
plt.ylabel("Transmitted Flux")
plt.title("2D Field-Coupled DBR Transmission Spectrum")
plt.grid(True)
plt.show()
