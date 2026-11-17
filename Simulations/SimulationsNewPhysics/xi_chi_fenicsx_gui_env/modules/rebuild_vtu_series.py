#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild a *varying* VTU time-series from an XDMF (or from a folder of VTUs).

- Works with meshio versions that **do not** support read(..., time=...).
- Uses meshio.xdmf.TimeSeriesReader when available.
- Writes per-step VTUs to --outdir (default: modules/data_fixed).
- Also writes:
    modules/xi_series_fixed.pvd   (ParaView time-series index)
    modules/xi_stats_fixed.csv    (min/max/mean/L2 of Xi each step)

Usage (run from project root):
  python3 modules/rebuild_vtu_series.py \
      --xdmf XiChiFieldSimulation_fixed_mkii/output/fields_timeseries.xdmf

or, if you just want to index an existing VTU folder:
  python3 modules/rebuild_vtu_series.py --series-dir XiChiFieldSimulation_fixed_mkii/output

Then open in ParaView (note: NO quotes):
  LIBGL_ALWAYS_SOFTWARE=1 QT_QPA_PLATFORM=xcb \
  MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 \
  paraview modules/xi_series_fixed.pvd
"""
from __future__ import annotations

import argparse
import csv
import sys
import os
from pathlib import Path
from typing import List, Tuple, Optional

import numpy as np

# meshio is optional until we need XDMF
try:
    import meshio
    _HAS_MESHIO = True
except Exception as e:
    _HAS_MESHIO = False
    _MESHIO_ERR = e


# ---------- helpers ----------
def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_pvd(pvd_path: Path, files_and_times: List[Tuple[Path, float]]) -> None:
    """Write a minimal ParaView PVD collection file."""
    rel_entries = []
    base = pvd_path.parent
    for f, t in files_and_times:
        rel_entries.append((os.path.relpath(f, base), t))
    xml = [
        '<?xml version="1.0"?>',
        '<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">',
        '  <Collection>',
    ]
    for rel, t in rel_entries:
        xml.append(f'    <DataSet timestep="{t}" group="" part="0" file="{rel}"/>')
    xml += ['  </Collection>', '</VTKFile>', '']
    pvd_path.write_text("\n".join(xml))


def stats_of_xi(arr: np.ndarray) -> Tuple[float, float, float, float]:
    """min, max, mean, L2 (sqrt(mean(x^2)))."""
    arr = np.asarray(arr, dtype=float).ravel()
    if arr.size == 0:
        return (float("nan"), float("nan"), float("nan"), float("nan"))
    mn = float(np.min(arr))
    mx = float(np.max(arr))
    mean = float(np.mean(arr))
    l2 = float(np.sqrt(np.mean(arr * arr)))
    return mn, mx, mean, l2


def save_stats_csv(csv_path: Path, rows: List[Tuple[int, str, float, float, float, float]]) -> None:
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["step", "file", "min", "max", "mean", "L2"])
        for r in rows:
            w.writerow(r)


def _mesh_from_points_cells(points, cells, point_data=None, cell_data=None):
    """Build a meshio.Mesh handling both old/new meshio cells APIs."""
    # new meshio prefers a list of (cell_type, data)
    if isinstance(cells, dict):
        cell_list = [(k, v) for k, v in cells.items()]
    else:
        cell_list = cells
    return meshio.Mesh(points=points, cells=cell_list, point_data=point_data or {}, cell_data=cell_data or {})


# ---------- main export logic ----------
def export_from_xdmf(xdmf_path: Path, outdir: Path) -> Tuple[List[Path], Path, Path]:
    if not _HAS_MESHIO:
        raise RuntimeError(f"meshio is required to read XDMF but could not be imported: {_MESHIO_ERR}")

    ensure_dir(outdir)
    files_and_times: List[Tuple[Path, float]] = []
    stats_rows: List[Tuple[int, str, float, float, float, float]] = []

    # Where to drop the PVD/CSV (next to this script, like previous instructions expected)
    script_dir = Path(__file__).resolve().parent
    pvd_path = script_dir / "xi_series_fixed.pvd"
    csv_path = script_dir / "xi_stats_fixed.csv"

    # Prefer TimeSeriesReader when available
    reader = None
    if hasattr(meshio, "xdmf") and hasattr(meshio.xdmf, "TimeSeriesReader"):
        reader = meshio.xdmf.TimeSeriesReader(str(xdmf_path))

    if reader is None:
        # Fallback: if reader missing, try to parse a *single-step* xdmf, or bail.
        # Users with old meshio should upgrade if they truly need XDMF time series.
        raise RuntimeError(
            "meshio.xdmf.TimeSeriesReader not available in your meshio version.\n"
            "Please `pip install -U meshio` or use --series-dir to point at the per-step VTUs."
        )

    with reader:
        try:
            nsteps = reader.num_steps
        except Exception:
            # Some edge versions use .n_steps
            nsteps = getattr(reader, "n_steps", None)

        if not nsteps or nsteps <= 0:
            raise RuntimeError("No timesteps found in the XDMF time series.")

        # Points/cells are step-invariant in many setups; read once.
        points, cells = reader.read_points_cells()

        for k in range(nsteps):
            # Times
            try:
                t = float(reader.read_time(k))
            except Exception:
                # fallback: monotonic index if no time
                t = float(k)

            # Per-step data (deep from HDF5)
            # Older/newer meshio return (point_data, cell_data) here
            pd, cd = reader.read_data(k)

            # Compose and save VTU
            mesh = _mesh_from_points_cells(points, cells, point_data=pd, cell_data=cd)

            # name like fields_t00000.vtu if present in XDMF, otherwise xi_field%05d.vtu
            fname = f"fields_t{int(t):05d}.vtu" if abs(t - int(t)) < 1e-12 else f"xi_field{k:05d}.vtu"
            vtu_path = outdir / fname
            meshio.write(vtu_path, mesh, file_format="vtu")
            files_and_times.append((vtu_path, t))

            # Stats: prefer point-data 'Xi', else any scalar that looks right
            xi = None
            if "Xi" in (pd or {}):
                xi = np.asarray(pd["Xi"]).ravel()
            elif pd:
                # pick the first 1D array
                for name, arr in pd.items():
                    a = np.asarray(arr)
                    if a.ndim == 1 or (a.ndim == 2 and a.shape[1] == 1):
                        xi = a.ravel()
                        break
            if xi is None:
                # If still none, synthesize zeros (won't crash the export)
                xi = np.zeros((len(points),), dtype=float)

            mn, mx, mean, l2 = stats_of_xi(xi)
            stats_rows.append((k, vtu_path.name, mn, mx, mean, l2))
            print(f"[{k+1}/{nsteps}] wrote {vtu_path.name}   min/max={mn:.6g}/{mx:.6g}")

    # Write index + stats
    write_pvd(pvd_path, files_and_times)
    save_stats_csv(csv_path, stats_rows)
    print(f"[ok] PVD:  {pvd_path}")
    print(f"[ok] CSV:  {csv_path}")
    return [p for p, _ in files_and_times], pvd_path, csv_path


def export_from_vtu_folder(series_dir: Path, outdir: Path) -> Tuple[List[Path], Path, Path]:
    """Pass-through / reindex an existing per-step VTU folder into a PVD+CSV."""
    ensure_dir(outdir)
    vtu_files = sorted(series_dir.glob("fields_t*.vtu"))
    if not vtu_files:
        vtu_files = sorted(series_dir.glob("*.vtu"))
    if not vtu_files:
        raise FileNotFoundError(f"No VTU files found in {series_dir}")

    files_and_times: List[Tuple[Path, float]] = []
    stats_rows: List[Tuple[int, str, float, float, float, float]] = []

    script_dir = Path(__file__).resolve().parent
    pvd_path = script_dir / "xi_series_fixed.pvd"
    csv_path = script_dir / "xi_stats_fixed.csv"

    for k, src in enumerate(vtu_files):
        # copy/normalize filenames to outdir
        dst = outdir / src.name
        if src.resolve() != dst.resolve():
            # load & re-write to ensure consistent mesh compression/format
            m = meshio.read(src)
            meshio.write(dst, m, file_format="vtu")
        else:
            dst = src

        # timestep from filename fields_tXXXXX.vtu (fallback to index)
        try:
            stem = src.stem
            idx = "".join(ch for ch in stem if ch.isdigit())
            t = float(int(idx)) if idx else float(k)
        except Exception:
            t = float(k)
        files_and_times.append((dst, t))

        # stats (try point-data Xi)
        try:
            m = meshio.read(dst)
            pd = getattr(m, "point_data", {}) or {}
            xi = None
            if "Xi" in pd:
                xi = np.asarray(pd["Xi"]).ravel()
            else:
                for name, arr in pd.items():
                    a = np.asarray(arr)
                    if a.ndim == 1 or (a.ndim == 2 and a.shape[1] == 1):
                        xi = a.ravel()
                        break
            if xi is None:
                xi = np.zeros((len(m.points),), dtype=float)
        except Exception:
            xi = np.zeros((1,), dtype=float)

        mn, mx, mean, l2 = stats_of_xi(xi)
        stats_rows.append((k, dst.name, mn, mx, mean, l2))
        print(f"[{k+1}/{len(vtu_files)}] indexed {dst.name}   min/max={mn:.6g}/{mx:.6g}")

    write_pvd(pvd_path, files_and_times)
    save_stats_csv(csv_path, stats_rows)
    print(f"[ok] PVD:  {pvd_path}")
    print(f"[ok] CSV:  {csv_path}")
    return [p for p, _ in files_and_times], pvd_path, csv_path


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser(description="Rebuild a varying VTU time-series from XDMF or a VTU folder.")
    ap.add_argument("--xdmf", type=str, help="Path to an XDMF time series (e.g. .../fields_timeseries.xdmf)")
    ap.add_argument("--series-dir", type=str, help="Folder containing per-step VTUs (e.g. .../output)")
    ap.add_argument(
        "--outdir",
        type=str,
        default=str((Path(__file__).resolve().parent / "data_fixed")),
        help="Output folder for rebuilt VTUs (default: modules/data_fixed)",
    )
    args = ap.parse_args()

    outdir = Path(args.outdir)
    if args.xdmf:
        xdmf = Path(args.xdmf)
        if not xdmf.exists():
            print(f"[error] XDMF not found: {xdmf}", file=sys.stderr)
            sys.exit(2)
        print(f"[info] Using XDMF: {xdmf.resolve()}")
        export_from_xdmf(xdmf, outdir)
    elif args.series_dir:
        series_dir = Path(args.series_dir)
        if not series_dir.exists():
            print(f"[error] series-dir not found: {series_dir}", file=sys.stderr)
            sys.exit(2)
        print(f"[info] Indexing VTUs from: {series_dir.resolve()}")
        export_from_vtu_folder(series_dir, outdir)
    else:
        print("[error] Provide --xdmf or --series-dir", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()

