
import meep as mp
import numpy as np
import matplotlib.pyplot as plt

resolution = 50  # pixels/um
cell_size = mp.Vector3(16, 0, 0)

# DBR parameters
n1, n2 = 1.45, 2.1
d1, d2 = 0.1, 0.1  # um
layers = 10

geometry = []
x_pos = 0
for i in range(layers):
    geometry.append(mp.Block(size=mp.Vector3(d1, mp.inf, mp.inf),
                             center=mp.Vector3(x_pos + d1/2),
                             material=mp.Medium(index=n1)))
    x_pos += d1
    geometry.append(mp.Block(size=mp.Vector3(d2, mp.inf, mp.inf),
                             center=mp.Vector3(x_pos + d2/2),
                             material=mp.Medium(index=n2)))
    x_pos += d2

sources = [mp.Source(mp.GaussianSource(frequency=1/1.55, fwidth=0.2),
                     component=mp.Ez,
                     center=mp.Vector3(-5))]

sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=[mp.PML(1.0)],
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

trans = sim.add_flux(1/1.55, 0.4, 100, mp.FluxRegion(center=mp.Vector3(6)))
sim.run(until=200)

# Extract and plot transmission
frequencies = mp.get_flux_freqs(trans)
flux_data = mp.get_fluxes(trans)

plt.plot([1/f for f in frequencies], flux_data)
plt.xlabel("Wavelength (um)")
plt.ylabel("Transmitted Flux")
plt.title("DBR Transmission Spectrum")
plt.grid(True)
plt.show()
