# Interactive χ–ξ Field Visualizer

## Core Features

- 3D surface of ξ field with color-coded χ overlay.
- Live, draggable sliders to explore time evolution.
- Overlaid DRIFT tensor vectors.

---

## Controls

- **Slider**: Frame index over simulation timeline.
- **Mouse Drag**: Rotate 3D plot.
- **Zoom**: Scroll wheel or trackpad.

---

## Tech Stack

- Plotly (Web-based GUI)
- Mayavi / VisPy (GPU render)
- PyQtGraph (Fallback lightweight GUI)

---

## Future Features

- “Play” mode to animate field evolution.
- Toggle overlays (χ, DRIFT, entropy).
- Export current frame as `.png` or TikZ-compatible `.tex`.

