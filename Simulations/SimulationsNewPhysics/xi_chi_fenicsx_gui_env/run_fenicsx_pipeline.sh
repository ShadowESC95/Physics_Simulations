#!/usr/bin/env bash
# Enterprise-grade FEniCSx → XDMF → VTU pipeline
# - Runs fenicsx_time_evolution.py in dolfinx container
# - Converts XDMF time-series to VTU frames (Xi field) inside container
# - Leaves frames in ./data/xi_field0000.vtu ... xi_field0099.vtu
set -euo pipefail

IMAGE="${IMAGE:-dolfinx/dolfinx:stable}"
WORKDIR="${WORKDIR:-$PWD}"
SIM_PY="${SIM_PY:-fenicsx_time_evolution.py}"   # must exist in $WORKDIR
OUT_DIR="${OUT_DIR:-data}"
FIELD_NAME="${FIELD_NAME:-Xi}"                  # which point field to export
EXPECTED_FRAMES="${EXPECTED_FRAMES:-100}"       # how many frames you expect

log() { printf "==> %s\n" "$*"; }
die() { printf "ERROR: %s\n" "$*" >&2; exit 1; }

# --- preflight ---
command -v docker >/dev/null 2>&1 || die "docker not found on host."
[[ -f "$SIM_PY" ]] || die "$SIM_PY not found in $WORKDIR"

# --- 1) run simulation ---
log "Running FEniCSx simulation in container: $IMAGE"
docker run --rm -it \
  -v "$WORKDIR":/workspace -w /workspace "$IMAGE" \
  bash -lc "python3 '$SIM_PY'"

# --- 2) convert XDMF → VTU (inside container with meshio+h5py) ---
log "Converting XDMF time series to VTU frames (inside container)"
docker run --rm -it \
  -v "$WORKDIR":/workspace -w /workspace "$IMAGE" \
  bash -lc '
set -euo pipefail
# Ensure deps needed for reading XDMF(HDF5)
pip3 install -q meshio h5py >/dev/null

python3 - <<PY
from meshio.xdmf import TimeSeriesReader
import meshio, pathlib as p, sys, os, numpy as np

xdmf = "xi_chi_phi_evolution.xdmf"
if not os.path.exists(xdmf):
    sys.exit(f"[convert] XDMF not found: {xdmf}. Did the simulation run?")

out = p.Path("'"$OUT_DIR"'"); out.mkdir(exist_ok=True)
# Clean prior frames
for old in out.glob("xi_field*.vtu"): 
    try: old.unlink()
    except Exception: pass

with TimeSeriesReader(xdmf) as r:
    points, cells = r.read_points_cells()
    nsteps = r.num_steps
    print(f"[convert] found {nsteps} timesteps in {xdmf}")
    for k in range(nsteps):
        t, point_data, cell_data = r.read_data(k)
        # Prefer requested field name; fallback to first available; synthesize if none
        field = point_data.get("'"$FIELD_NAME"'")
        if field is None:
            if point_data:
                fname, field = next(iter(point_data.items()))
                print(f"[warn] step {k}: field '"$FIELD_NAME"' missing; using {fname}")
            else:
                field = np.zeros(points.shape[0], float)
                print(f"[warn] step {k}: no point_data present; writing zeros")
        m = meshio.Mesh(points, cells, point_data={"'"$FIELD_NAME"'": field})
        outpath = out / f"xi_field{k:04d}.vtu"
        meshio.write(outpath, m)
        print(f"[write] {outpath}    t={t}")
print("[done] VTU export complete.")
PY
'

# --- report ---
count=$(ls -1 "$OUT_DIR"/xi_field*.vtu 2>/dev/null | wc -l | tr -d " ")
log "Wrote $count VTU frame(s) to $OUT_DIR/"
if [[ "$count" -lt "${EXPECTED_FRAMES}" ]]; then
  printf "NOTE: expected %s frames but found %s. Increase timesteps in %s if you need exactly %s.\n" \
    "${EXPECTED_FRAMES}" "$count" "${SIM_PY}" "${EXPECTED_FRAMES}" >&2
fi

log "All done. Play them with:  python3 gui.py"
