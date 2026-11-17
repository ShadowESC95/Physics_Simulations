from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import os

# === App Config ===
DATA_DIR = "model5_autosim_gamma0.05_m1.0"
ENTROPY_FILE = os.path.join(DATA_DIR, "entropy_log.npy")
XI_FILE = os.path.join(DATA_DIR, "xi_field_log.npy")
DRIFT_FILE = os.path.join(DATA_DIR, "drift_tensor_log.npy")

def load_data():
    try:
        xi = np.load(XI_FILE)
        entropy = np.load(ENTROPY_FILE)
        drift = np.load(DRIFT_FILE)
        return xi, entropy, drift
    except FileNotFoundError as e:
        print(f"[ERROR] Missing file: {e}")
        return None, None, None

def create_entropy_graph(entropy_log):
    if entropy_log is None:
        return html.Div("Entropy data not available.")
    return dcc.Graph(
        figure=go.Figure(
            data=[go.Scatter(y=entropy_log, mode='lines')],
            layout=go.Layout(title="Ξχ Entropy over Time")
        )
    )

def create_phase_spiral(xi_entropy, drift_tensor):
    if xi_entropy is None or drift_tensor is None:
        return html.Div("Phase portrait data not available.")
    drift_var = np.var(drift_tensor, axis=(1, 2))
    curvature = np.gradient(np.gradient(xi_entropy))
    return dcc.Graph(
        figure=go.Figure(
            data=[go.Scatter3d(
                x=xi_entropy, y=curvature, z=drift_var,
                mode='lines+markers'
            )],
            layout=go.Layout(title="Ξχ Phase Portrait")
        )
    )

# === Dash App Layout ===
app = Dash(__name__)
app.title = "Ξ–χ Phase Explorer"

xi, entropy_log, drift_tensor_log = load_data()

app.layout = html.Div([
    html.H1("Ξ–χ Field Dynamics Dashboard"),
    create_entropy_graph(entropy_log),
    html.Hr(),
    create_phase_spiral(entropy_log, drift_tensor_log)
])

# === Run Server ===
if __name__ == '__main__':
    app.run(debug=True)

