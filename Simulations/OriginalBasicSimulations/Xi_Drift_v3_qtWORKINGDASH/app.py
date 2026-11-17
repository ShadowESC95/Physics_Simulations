from dash import Dash, dcc, html, Input, Output
import numpy as np
import plotly.graph_objs as go
from components.controls import controls_panel
from components.graphs import create_phase_spiral
from engine.drift_tensor import compute_drift
from engine.io_openfoam_export import export_csv_for_openfoam
import os

# --- Safe loader ---
def safe_load(path, fallback=(100, 64, 64)):
    try:
        return np.load(path)
    except Exception as e:
        print(f"[ERROR] Could not load {path}: {e}")
        return np.zeros(fallback)

# --- Load data ---
xi = safe_load("output/xi_field_log.npy")
chi = safe_load("output/chi_field_log.npy")
entropy = safe_load("output/xi_entropy_log.npy")
drift_tensor = compute_drift(xi, chi)
steps = xi.shape[0]

# --- App Setup ---
app = Dash(__name__)
server = app.server

# --- Layout with fail-safe ---
try:
    app.layout = html.Div([
        html.H1("Ξχ Scalar Field Viewer", style={"textAlign": "center"}),

        controls_panel(steps),  # ✅ expects steps to build slider

        html.Div([
            html.Button("Export to OpenFOAM", id="export-openfoam-btn"),
            html.Div(id="export-status", style={"marginTop": "10px", "color": "green"}),
        ]),

        html.Div([
            html.H2("Ξχ Drift + Energy Diagnostics"),
            html.Div(id="drift-diagnostics", style={"marginBottom": "20px", "fontFamily": "monospace"}),
        ]),

        html.Div([
            html.H2("Ξ Field Viewer"),
            dcc.Graph(id="field-plot"),
        ]),

        html.Div([
            html.H2("Entropy Evolution"),
            dcc.Graph(id="entropy-plot")
        ]),

        html.Div([
            html.H2("Ξχ Phase Portrait"),
            create_phase_spiral()
        ])
    ])
except Exception as e:
    print(f"[❌ Layout Error] {e}")
    app.layout = html.Div([
        html.H1("⚠ Layout failed to load."),
        html.Pre(str(e))
    ])

# --- Callbacks ---
@app.callback(
    Output("export-status", "children"),
    Input("export-openfoam-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_openfoam_callback(n):
    export_csv_for_openfoam(xi, chi)
    return "✅ Exported to OpenFOAM-compatible CSVs"

@app.callback(
    Output("drift-diagnostics", "children"),
    Input("frame-slider", "value")
)
def update_diagnostics(frame):
    frame_xi = xi[frame]
    frame_chi = chi[frame]
    drift = np.abs(frame_xi - frame_chi)
    mean_drift = np.mean(drift)
    energy = np.sum(frame_xi**2 + frame_chi**2)
    return f"⏱ Frame {frame} | Drift: {mean_drift:.4f} | Energy: {energy:.2f}"

@app.callback(
    Output("field-plot", "figure"),
    Input("frame-slider", "value"),
    Input("field-selector", "value")
)
def update_graph(frame, field):
    field_data = xi if field == 'xi' else chi
    z = field_data[frame]
    fig = go.Figure(data=go.Heatmap(z=z, colorscale='Viridis'))
    fig.update_layout(title=f"{field.upper()} Frame {frame}")
    return fig

@app.callback(
    Output("entropy-plot", "figure"),
    Input("frame-slider", "value")
)
def update_entropy_plot(frame):
    fig = go.Figure(data=go.Scatter(y=entropy[:frame + 1], mode="lines"))
    fig.update_layout(title="Entropy Over Time", xaxis_title="Frame", yaxis_title="Entropy")
    return fig

# --- Launch ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
