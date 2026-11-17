import yt
import sys

def render_yt_volume(filename):
    ds = yt.load(filename)

    sc = yt.create_scene(ds, field=("gas", "density"))
    cam = sc.camera
    cam.set_width(ds.domain_width * 0.9)

    sc.annotate_axes()
    sc.annotate_domain(ds)
    sc.save("yt_render.png", sigma_clip=4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yt_volume_view.py <hdf5 file>")
        sys.exit(1)

    render_yt_volume(sys.argv[1])
