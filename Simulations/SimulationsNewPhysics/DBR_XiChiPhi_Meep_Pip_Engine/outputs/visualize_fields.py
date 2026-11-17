# visualize_fields.py
import pyvista as pv
import os
import glob
from natsort import natsorted

# --- Configuration ---
DATA_DIR = "outputs"
EXTENSION = "*.vti"  # or "*.vtu" if using VTU files
FIELD_NAME = "E_field"  # adjust if needed

# --- Load all field files ---
def load_files():
    files = glob.glob(os.path.join(DATA_DIR, EXTENSION))
    files = natsorted(files)
    if not files:
        raise FileNotFoundError(f"No {EXTENSION} files found in {DATA_DIR}")
    return files

def visualize(files):
    plotter = pv.Plotter()
    slider_args = dict(title="Timestep", fmt="%d", pointa=(.25, .05), pointb=(.75, .05))

    # Initial field
    mesh = pv.read(files[0])
    actor = plotter.add_mesh(mesh, scalars=FIELD_NAME, cmap="viridis")

    def update_field(index):
        mesh = pv.read(files[index])
        actor.mesh.overwrite(mesh)
        actor.mapper.scalar_range = mesh.get_data_range(FIELD_NAME)
        plotter.update()

    plotter.add_slider_widget(update_field, [0, len(files) - 1], value=0,
                              event_type="always", **slider_args)

    plotter.show(title="Ξ–χ–φ Electromagnetic Field Viewer")

if __name__ == "__main__":
    try:
        files = load_files()
        visualize(files)
    except Exception as e:
        print(f"Error: {e}")

