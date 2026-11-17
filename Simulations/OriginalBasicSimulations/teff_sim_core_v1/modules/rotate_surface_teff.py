import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import shutil
import subprocess

OUTPUT_DIR = "../output"
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames_3d_rot")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "teff_surface_spin.mp4")
DATA_EXPORT = os.path.join(OUTPUT_DIR, "teff_field_final_3d.csv")

def load_field(path="../output/teff_field_final.csv"):
    try:
        field = np.loadtxt(path, delimiter=",")
        np.savetxt(DATA_EXPORT, field, delimiter=",")
        print(f"💾 Teff field data saved to {DATA_EXPORT}")
        return field
    except Exception as e:
        print(f"❌ Could not load Teff field: {e}")
        return None

def plot_frame(field, angle, frame_id):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    x = np.arange(field.shape[1])
    y = np.arange(field.shape[0])
    X, Y = np.meshgrid(x, y)

    ax.plot_surface(X, Y, field, cmap='plasma', linewidth=0, antialiased=True)
    ax.view_init(elev=30, azim=angle)
    ax.set_zlim(np.min(field), np.max(field))
    plt.axis('off')

    fname = os.path.join(FRAMES_DIR, f"frame_{frame_id:03d}.png")
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"🌀 Frame {frame_id:03d} saved")

def generate_frames(field, steps=60):
    os.makedirs(FRAMES_DIR, exist_ok=True)
    for i in range(steps):
        angle = i * (360 / steps)
        plot_frame(field, angle, i)

def render_video():
    try:
        subprocess.run([
    "ffmpeg", "-y", "-framerate", "15",
    "-i", os.path.join(FRAMES_DIR, "frame_%03d.png"),
    "-c:v", "mjpeg", FINAL_VIDEO.replace(".mp4", ".avi")
], check=True)

        print(f"🎥 Video saved to {FINAL_VIDEO}")
    except Exception as e:
        print(f"❌ Failed to render video: {e}")

def clean_frames():
    shutil.rmtree(FRAMES_DIR)
    print("🧹 Frame directory cleaned up")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    field = load_field()
    if field is not None:
        generate_frames(field)
        render_video()
        # Optional: clean_frames()  ← Uncomment this line to delete frames after rendering
