# save_fields_numpy.py
import meep as mp, numpy as np, h5py, os

sim = mp.Simulation(cell_size=mp.Vector3(16,8,0), resolution=20)
os.makedirs("outputs", exist_ok=True)

# write epsilon at t=0 via numpy/h5py
eps = sim.get_array(component=mp.Dielectric)
np.save("outputs/epsilon.npy", eps)
with h5py.File("outputs/epsilon_numpy.h5", "w") as f:
    f.create_dataset("epsilon", data=eps)

# add a simple source and step; record Ez every N steps
fcen, df = 0.25, 0.2
src = mp.Source(mp.GaussianSource(fcen, fwidth=df),
                component=mp.Ez, center=mp.Vector3(-6,0))
sim.sources = [src]

probe_box = dict(center=mp.Vector3(), size=mp.Vector3(16,8,0))
snap_every = 20
tmax = 200

def snapshot(sim):
    n = sim.meep_time()
    ez = sim.get_array(component=mp.Ez, **probe_box)
    np.save(f"outputs/ez_t{int(n):05d}.npy", ez)

sim.run(mp.at_beginning(snapshot),
        mp.at_every(snap_every, snapshot),
        until=tmax)

