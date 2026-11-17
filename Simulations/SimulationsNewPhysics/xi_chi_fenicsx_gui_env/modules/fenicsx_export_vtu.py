import argparse, glob, os, sys

def _apply_renames_meshio(m, pairs):
    for old, new in pairs.items():
        if old in m.point_data:
            m.point_data[new] = m.point_data.pop(old)

def _apply_renames_pv(grid, pairs):
    for old, new in pairs.items():
        if old in grid.point_data:
            grid.point_data[new] = grid.point_data.pop(old)

def export_vtu(inputs, out_dir, pattern, start=0, renames=None):
    renames = renames or {}
    try: pattern % 0
    except Exception:
        print("[export] --pattern must be printf-style int (e.g. xi_field%04d.vtu)", file=sys.stderr)
        sys.exit(2)

    files = sorted(sum((glob.glob(g) for g in inputs), []))
    if not files:
        print(f"[export] No inputs matched: {inputs}", file=sys.stderr)
        return 0

    os.makedirs(out_dir, exist_ok=True)
    idx = start
    for path in files:
        wrote = False
        try:
            import meshio
            if path.lower().endswith(".xdmf"):
                with meshio.xdmf.TimeSeriesReader(path) as rdr:
                    pts, cells = rdr.read_points_cells()
                    for k in range(rdr.num_steps):
                        t, pdat, cdat = rdr.read_data(k)
                        m = meshio.Mesh(pts, cells, point_data=pdat, cell_data=cdat)
                        _apply_renames_meshio(m, renames)
                        m.write(os.path.join(out_dir, pattern % idx)); idx += 1
                wrote = True
        except Exception as e:
            print(f"[export] meshio failed for {path}: {e}", file=sys.stderr)

        if not wrote:
            try:
                import pyvista as pv
                r = pv.get_reader(path)
                times = getattr(r, "time_values", None)
                if times:
                    for ti in range(len(times)):
                        r.set_active_time_point(ti)
                        g = r.read(); _apply_renames_pv(g, renames)
                        g.save(os.path.join(out_dir, pattern % idx)); idx += 1
                else:
                    g = r.read(); _apply_renames_pv(g, renames)
                    g.save(os.path.join(out_dir, pattern % idx)); idx += 1
            except Exception as e:
                print(f"[export] VTK failed for {path}: {e}", file=sys.stderr)

    print(f"[export] Wrote {idx - start} VTU frame(s) to {out_dir}")
    return idx - start

def main():
    ap = argparse.ArgumentParser(description="Export VTU(s) from XDMF/HDF5")
    ap.add_argument("--in", dest="inputs", nargs="+", required=True)
    ap.add_argument("--out", dest="out_dir", required=True)
    ap.add_argument("--pattern", dest="pattern", required=True)
    ap.add_argument("--start", dest="start", type=int, default=0)
    ap.add_argument("--rename", action="append", default=[],
                    help="Rename arrays OLD=NEW, repeatable (e.g. --rename Phi=Xi --rename u=Xi)")
    args = ap.parse_args()
    renames = {}
    for r in args.rename:
        old, new = r.split("=", 1)
        renames[old] = new
    export_vtu(args.inputs, args.out_dir, args.pattern, args.start, renames)

if __name__ == "__main__":
    main()
