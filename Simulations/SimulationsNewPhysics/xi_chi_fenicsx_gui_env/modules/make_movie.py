import glob, pyvista as pv

frames = sorted(glob.glob("data/xi_field*.vtu"))
if not frames:
    raise SystemExit("no frames in ./data")

plotter = pv.Plotter(off_screen=True, window_size=(1280, 720))
plotter.open_movie("xi_movie.mp4", framerate=20)

# global color limits across frames
gmin = gmax = None
for f in frames:
    m = pv.read(f)
    x = m.point_data.get("Xi")
    if x is None:
        continue
    gmin = x.min() if gmin is None else min(gmin, x.min())
    gmax = x.max() if gmax is None else max(gmax, x.max())

for i, f in enumerate(frames, 1):
    m = pv.read(f)
    plotter.clear()
    plotter.add_mesh(m, scalars="Xi", cmap="viridis",
                     clim=(gmin, gmax), show_edges=False)
    if i == 1:
        plotter.add_scalar_bar(title="Xi")
    plotter.write_frame()
    print(f"[frame {i}/{len(frames)}] {f}")

plotter.close()
print("✅ wrote xi_movie.mp4")
