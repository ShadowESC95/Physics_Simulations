import meep as mp

# --- simulation setup (your geometry/sources) ---
cell = mp.Vector3(16, 8, 0)
res = 20

geometry = []  # put your objects here
sources = [mp.Source(mp.GaussianSource(frequency=1/1.55, fwidth=0.2),
                     component=mp.Ez,
                     center=mp.Vector3(-7, 0),
                     size=mp.Vector3(0, 8))]

sim = mp.Simulation(cell_size=cell,
                    geometry=geometry,
                    boundary_layers=[mp.PML(1)],
                    sources=sources,
                    resolution=res)

# (optional) choose where Meep writes .h5 files
# mp.output_directory = "meep-out"   # uncomment if you want a custom folder

# ---------- A) WRITE EPSILON ----------
# Safest ways:
#   1) at the very beginning of the run (no fields needed)
#   2) or explicitly init then write before any time-stepping
sim.run(mp.at_beginning(mp.output_epsilon), until=0)   # writes epsilon.h5

# ---------- B) ENERGY / FLUX CONSERVATION ----------
# Place flux monitors BEFORE time-stepping.
frq = 1/1.55
# Example: two monitors on left/right to compare transmitted vs incident
flux_pos = sim.add_flux(frq, 0, 1, mp.FluxRegion(center=mp.Vector3(+6, 0), size=mp.Vector3(0, 8)))
flux_neg = sim.add_flux(frq, 0, 1, mp.FluxRegion(center=mp.Vector3(-6, 0), size=mp.Vector3(0, 8)))

# ---------- C) WRITE FIELDS OVER TIME ----------
# Use to_appended() inside sim.run with at_every(). This creates ez-000000.h5, ez-000001.h5, ...
sim.run(
    mp.at_every(5, mp.to_appended("ez", mp.output_efield_z)),  # every 5 time units
    until=200
)

# ---------- D) READ/PRINT FLUX AFTER THE RUN ----------
# After time-stepping, pull the flux values:
tx = mp.get_fluxes(flux_pos)[0]
ix = mp.get_fluxes(flux_neg)[0]
print("Flux +x (transmitted-ish):", tx)
print("Flux -x (incident-ish):   ", ix)
print("Net (should be ~source minus losses):", tx + ix)

