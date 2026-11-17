
import meep as mp
import numpy as np
import matplotlib.pyplot as plt

resolution = 30  # pixels/um
cell_size = mp.Vector3(16, 4, 0)

# Refractive indices and thicknesses
n1, n2 = 1.45, 2.1
d1, d2 = 0.1, 0.1
layers = 8

# Entropy gradient emulation: index gradually increases across x
def entropy_modulated_index(x):
    entropy_shift = 0.05 * (x / 8.0)
    return [n1 + entropy_shift, n2 + entropy_shift]

geometry = []
x_pos = 0
for i in range(layers):
    n_vals = entropy_modulated_index(x_pos)
    geometry.append(mp.Block(size=mp.Vector3(d1, 4),
                             center=mp.Vector3(x_pos + d1/2, 0),
                             material=mp.Medium(index=n_vals[0])))
    x_pos += d1
    geometry.append(mp.Block(size=mp.Vector3(d2, 4),
                             center=mp.Vector3(x_pos + d2/2, 0),
                             material=mp.Medium(index=n_vals[1])))
    x_pos += d2

sources = [mp.Source(mp.GaussianSource(frequency=1/1.55, fwidth=0.2),
                     component=mp.Ez,
                     center=mp.Vector3(-6, 0))]

sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=[mp.PML(1.0)],
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)

sim.run(until=300)
eps_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Dielectric)
ez_data = sim.get_array(center=mp.Vector3(), size=cell_size, component=mp.Ez)

plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu')
plt.colorbar(label='Ez')
plt.title("2D Ez Field Distribution through DBR with Entropy Gradient")
plt.xlabel("X (grid)")
plt.ylabel("Y (grid)")
plt.tight_layout()
plt.show()
