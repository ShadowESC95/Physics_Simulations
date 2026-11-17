# xichi_tools.py
import os, glob, csv, math, argparse, pathlib
import numpy as np
import pyvista as pv
from pyvista import _vtk as vtk
import xml.etree.ElementTree as ET

def times_from_xdmf(xdmf_path):
    tvals = []
    root = ET.parse(xdmf_path).getroot()
    for node in root.iter():
        if node.tag.endswith("Time") and "Value" in node.attrib:
            tvals.append(float(node.attrib["Value"]))
    return tvals
    
def series(pattern="xi_field*.vtu"):
    files = sorted(glob.glob(pattern), key=lambda p: int(os.path.splitext(os.path.basename(p))[0][-4:]))
    if not files:
        raise SystemExit(f"No files match {pattern}")
    return files

def read_any(path):
    m = pv.read(path)
    from pyvista import MultiBlock
    if isinstance(m, MultiBlock):
        if len(m)==1:
            m = m[0]
        else:
            m = m.combine()
    return m

def pick_scalar(m):
    keys = list(m.point_data.keys())
    for cand in ("Xi","u","phi","Phi","Chi","chi"):
        if cand in keys: return cand
    if not keys:
        raise SystemExit("No point_data arrays present.")
    return keys[0]

def cell_measures(m):
    mc = m.point_data_to_cell_data(pass_point_data=False)
    out = mc.compute_cell_sizes(length=True, area=True, volume=True)
    if out is not None:  # some versions return a new mesh
        mc = out

    # accept a few possible array names
    for keys in (("Volume","CellVolume"),
                 ("Area","CellArea"),
                 ("Length","CellLength"),
                 ("CellSize",)):
        for k in keys:
            if k in mc.cell_data:
                return mc, np.asarray(mc.cell_data[k], float)
    raise SystemExit("Could not determine cell measure (Volume/Area/Length).")

def stats_for_mesh(m, name):
    a = np.asarray(m.point_data[name], float)
    amin, amax = float(np.nanmin(a)), float(np.nanmax(a))
    amean, astd = float(np.nanmean(a)), float(np.nanstd(a))

    mc, meas = cell_measures(m)
    u_c = np.asarray(mc.cell_data[name], float)
    mass = float(np.sum(u_c * meas))
    L2   = float(np.sqrt(np.sum((u_c**2) * meas)))

    # gradients (points) → cell data → H1 seminorm
    mg   = compute_point_gradients_vtk(m, name)            # adds 'Gradients' on points
    mgc  = mg.point_data_to_cell_data(pass_point_data=False)
    G    = np.asarray(mgc.cell_data["Gradients"], float)   # shape (ncell, 3) or (ncell, dim)
    H1   = float(np.sqrt(np.sum(np.sum(G*G, axis=1) * meas)))

    return dict(min=amin, max=amax, mean=amean, std=astd, mass=mass, L2=L2, H1=H1)

    
def compute_point_gradients_vtk(mesh, name, result="Gradients"):
    gf = vtk.vtkGradientFilter()
    gf.SetInputData(mesh)
    # VTK 9 compat
    try:
        gf.SetInputScalars(vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, name)
    except AttributeError:
        gf.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, name)
    gf.SetResultArrayName(result)
    gf.Update()
    return pv.wrap(gf.GetOutput())
    
def cmd_stats(args):
    files = series(args.pattern)
    rows=[]
    s0 = pick_scalar(read_any(files[0]))
    tvals = times_from_xdmf(args.xdmf) if getattr(args, "xdmf", None) else None
    for i,f in enumerate(files):
        m = read_any(f)
        name = s0 if s0 in m.point_data else pick_scalar(m)
        row = stats_for_mesh(m, name)
        row.update(frame=i, file=os.path.basename(f), scalar=name)
        if tvals and i < len(tvals):
            row["t"] = tvals[i]
        rows.append(row)
    out = args.out or "xi_stats_full.csv"
    with open(out,"w",newline="") as fh:
        w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("wrote", out)

def cmd_morph(args):
    files = series(args.pattern)
    m0 = read_any(files[0]); name = pick_scalar(m0)
    tau = args.tau
    if tau is None:
        a0 = m0.point_data[name]; tau = 0.5*(float(np.nanmin(a0))+float(np.nanmax(a0)))
    rows=[]
    for i,f in enumerate(files):
        m = read_any(f)
        name = name if name in m.point_data else pick_scalar(m)
        mc, meas = cell_measures(m)
        tot = float(np.nansum(meas))
        th = m.threshold(value=tau, scalars=name, preference="point")
        if th.n_cells>0:
            thc, tmeas = cell_measures(th)
            sub = float(np.nansum(tmeas))
            conn = th.connectivity()
            ncomp = int(np.unique(conn.cell_data["RegionId"]).size)
        else:
            sub, ncomp = 0.0, 0
        iso = m.contour([tau], scalars=name)
        rows.append(dict(frame=i, tau=tau, vol_frac=(sub/tot if tot>0 else float("nan")),
                         n_components=ncomp, iso_area=float(iso.area)))
    out = args.out or "xi_morphology.csv"
    with open(out,"w",newline="") as fh:
        w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("wrote", out)

def cmd_diffs(args):
    files = series(args.pattern)
    outd = pathlib.Path(args.outdir or "diffAB"); outd.mkdir(exist_ok=True)
    m0 = read_any(files[0]); name = pick_scalar(m0)
    for i in range(len(files)-1):
        A,B = read_any(files[i]), read_any(files[i+1])
        if A.n_points != B.n_points:
            print(f"skip {i}: topology differs"); continue
        s = name if name in A.point_data and name in B.point_data else pick_scalar(B)
        diff = B.copy()
        diff.point_data[f"{s}_diff"] = np.asarray(B.point_data[s], float) - np.asarray(A.point_data[s], float)
        outp = outd / f"diff{i:04d}.vtu"; diff.save(outp)
    print("wrote diffs in", outd)

def cmd_movie(args):
    files = series(args.pattern)
    m0 = read_any(files[0]); name = pick_scalar(m0)
    p = pv.Plotter(off_screen=True)
    p.add_axes(); p.show_grid()
    p.open_gif(args.out or "xi_series.gif")
    for f in files:
        p.clear_actors()
        m = read_any(f)
        s = name if name in m.point_data else pick_scalar(m)
        p.add_mesh(m, scalars=s)
        p.write_frame()
    p.close(); print("wrote", args.out or "xi_series.gif")

def cmd_pvd(args):
    files = series(args.pattern)
    d = pathlib.Path(args.dir or ".")
    pvd = d / (args.out or "xi_field_series.pvd")
    with pvd.open("w") as f:
        f.write('<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n  <Collection>\n')
        for k,p in enumerate(files):
            f.write(f'    <DataSet timestep="{k}" file="{os.path.basename(p)}"/>\n')
        f.write('  </Collection>\n</VTKFile>\n')
    print("wrote", pvd)

def cmd_xdmf(args):
    rdr = pv.get_reader(args.xdmf)
    times = list(getattr(rdr, "time_values", []) or [])
    arrays = list(getattr(rdr, "array_names", []) or [])
    if not arrays:
        raise SystemExit("No arrays in XDMF.")
    name = args.scalar or next((x for x in ("Xi","u","phi","Phi","Chi","chi") if x in arrays), arrays[0])
    rows=[]
    for k,t in enumerate(times if times else [None]):
        if t is not None: rdr.set_active_time_value(t)
        m = rdr.read()
        from pyvista import MultiBlock
        if isinstance(m, MultiBlock): m = m[0] if len(m)==1 else m.combine()
        row = stats_for_mesh(m, name); row.update(i=k, t=(t if t is not None else k))
        rows.append(row)
    out = args.out or "xdmf_stats.csv"
    with open(out,"w",newline="") as fh:
        w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"wrote {out} using scalar '{name}' and {len(times)} times")

def main():
    ap = argparse.ArgumentParser(description="Xi/Chi VTU/XDMF toolbox")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # stats: per-frame invariants, optionally attach true times from an XDMF
    s = sub.add_parser("stats", help="Per-frame invariants to CSV")
    s.add_argument("--pattern", default="xi_field*.vtu")
    s.add_argument("--out")
    s.add_argument("--xdmf", help="Optional XDMF path to attach true time stamps (XML-only)")
    s.set_defaults(func=cmd_stats)

    # morphology metrics
    m = sub.add_parser("morph", help="Morphology metrics (threshold volume, components, iso-area)")
    m.add_argument("--pattern", default="xi_field*.vtu")
    m.add_argument("--tau", type=float, help="Threshold (default mid-range of frame 0)")
    m.add_argument("--out")
    m.set_defaults(func=cmd_morph)

    # frame-to-frame diffs
    d = sub.add_parser("diffs", help="Write frame-to-frame difference VTUs")
    d.add_argument("--pattern", default="xi_field*.vtu")
    d.add_argument("--outdir")
    d.set_defaults(func=cmd_diffs)

    # movie (GIF)
    mov = sub.add_parser("movie", help="Write GIF of the series (off-screen)")
    mov.add_argument("--pattern", default="xi_field*.vtu")
    mov.add_argument("--out", default="xi_series.gif")
    mov.set_defaults(func=cmd_movie)

    # ParaView PVD collection
    pvd = sub.add_parser("pvd", help="Create ParaView PVD collection")
    pvd.add_argument("--pattern", default="xi_field*.vtu")
    pvd.add_argument("--dir", default=".")
    pvd.add_argument("--out", default="xi_field_series.pvd")
    pvd.set_defaults(func=cmd_pvd)

    # XDMF stats (uses reader; may be fragile on some builds)
    x = sub.add_parser("xdmf-stats", help="Invariants from XDMF with true time values")
    x.add_argument("xdmf", default="xi_chi_phi_evolution.xdmf", nargs="?")
    x.add_argument("--scalar", help="Array name to use")
    x.add_argument("--out")
    x.set_defaults(func=cmd_xdmf)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

