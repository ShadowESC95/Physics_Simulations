
#!/usr/bin/env python3
import argparse, os, sys, glob
def write_pvd_series(out_dir, pattern, pvd_name):
    vtus = sorted(glob.glob(os.path.join(out_dir, pattern.replace("%04d","*").replace("%d","*"))))
    p = os.path.join(out_dir, pvd_name)
    with open(p, "w") as f:
        f.write('<?xml version="1.0"?>\n<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n  <Collection>\n')
        for i,v in enumerate(vtus): f.write(f'    <DataSet timestep="{i}" file="{os.path.basename(v)}"/>\n')
        f.write('  </Collection>\n</VTKFile>\n'); return p

def export_from_xdmf(inputs, out_dir, pattern, start=0):
    try: pattern % 0
    except Exception: print("[export] pattern must be printf-style int", file=sys.stderr); sys.exit(2)
    os.makedirs(out_dir, exist_ok=True); idx=start; wrote=0
    for path in inputs:
        ok=False
        try:
            import meshio
            with meshio.xdmf.TimeSeriesReader(path) as rdr:
                pts, cells = rdr.read_points_cells()
                for k in range(rdr.num_steps):
                    t, pdat, cdat = rdr.read_data(k)
                    meshio.Mesh(pts, cells, point_data=pdat, cell_data=cdat).write(os.path.join(out_dir, pattern % idx))
                    idx+=1; wrote+=1
            ok=True
        except Exception as e:
            print("[export] meshio failed:", e, file=sys.stderr)
        if not ok:
            try:
                import pyvista as pv
                r = pv.get_reader(path); times = getattr(r, "time_values", None)
                if times:
                    for ti in range(len(times)):
                        r.set_active_time_point(ti); r.read().save(os.path.join(out_dir, pattern % idx)); idx+=1; wrote+=1
                else:
                    pv.read(path).save(os.path.join(out_dir, pattern % idx)); idx+=1; wrote+=1
            except Exception as e:
                print("[export] VTK failed:", e, file=sys.stderr)
    return wrote

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inputs", nargs="*", default=[])
    ap.add_argument("--out", required=True)
    ap.add_argument("--pattern", default="fields_%04d.vtu")
    ap.add_argument("--pvd", dest="pvd", default=None)
    ap.add_argument("--from-vtu-glob", dest="vtuglob", default=None)
    args = ap.parse_args()

    if args.vtuglob:
        p = write_pvd_series(args.out, args.vtuglob, args.pvd or "series.pvd"); print("[pvd] wrote", p); sys.exit(0)
    wrote = export_from_xdmf(args.inputs, args.out, args.pattern)
    if args.pvd:
        p = write_pvd_series(args.out, args.pattern, args.pvd); print("[pvd] wrote", p)
    print(f"[export] Wrote {wrote} VTU frame(s) to {args.out}")
