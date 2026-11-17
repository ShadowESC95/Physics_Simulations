import meshio
import numpy as np
import csv
import sys

xdmf_file = sys.argv[1]
out_csv = sys.argv[2] if len(sys.argv) > 2 else "xdmf_stats_meshio.csv"

mesh = meshio.read(xdmf_file)

# Pick a scalar array
scalar_name = next((x for x in mesh.point_data if x.lower() in ["xi","chi","phi","u"]), None)
if scalar_name is None:
    scalar_name = list(mesh.point_data.keys())[0]

data = np.asarray(mesh.point_data[scalar_name], float)

stats = {
    "min": float(np.min(data)),
    "max": float(np.max(data)),
    "mean": float(np.mean(data)),
    "std": float(np.std(data)),
}

with open(out_csv, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=stats.keys())
    w.writeheader()
    w.writerow(stats)

print(f"Wrote stats to {out_csv} using scalar '{scalar_name}'")
