from dash import Dash, dcc, html
import plotly.graph_objs as go
import numpy as np
import os

# === Paths ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "output")

XI_FILE = os.path.join(DATA_DIR, "xi_field_log.npy")
CHI_FILE = os.path.join(DATA_DIR, "chi_field_log.npy")
ENTROPY_FILE = os.path.join(DATA_DIR, "xi_entropy_log.npy")
DRIFT_FILE = os.path.join(DATA_DIR, "drift_tensor_Xi.npy")
JANUS_FILE = os.path.join(DATA_DIR, "janus_idx.npy")

# === Load Data ===
def load_array(path):
    try:
        return np.load(path)
    except Exception as e:
        print(f"[ERROR] Could not load {path}: {e}")
        return None

xi_log = load_array(XI_FILE)
chi_log = load_array(CHI_FILE)
entropy_log = load_array(ENTROPY_FILE)
drift_tensor = load_array(DRIFT_FILE)
janus_idx = load_array(JANUS_FILE)

# === Graph Components ===
def create_entropy_graph(entropy_log, janus_idx=None):
    if entropy_log is None:
        return html.Div("⚠️ Entropy data not available.")
    
    trace = go.Scatter(y=entropy_log, mode="lines", name="Ξχ Entropy")
    layout = go.Layout(title="Ξχ Entropy over Time")

    fig = go.Figure(data=[trace], layout=layout)

    if janus_idx is not None:
        fig.add_vline(
            x=int(janus_idx[0]),
            line_dash="dash", line_color="red",
            annotation_text="Janus Point", annotation_position="top right"
        )

    return dcc.Graph(figure=fig)

def create_phase_portrait(entropy_log, drift_tensor):
    if entropy_log is None or drift_tensor is None:
        return html.Div("⚠️ Phase portrait data not available.")
    
    drift_var = np.var(drift_tensor, axis=(1, 2))
    curvature = np.gradient(np.gradient(entropy_log))

    fig = go.Figure(data=[
        go.Scatter3d(
            x=entropy_log,
            y=curvature,
            z=drift_var,
            mode="lines+markers",
            marker=dict(size=4),
        )
    ])
    fig.update_layout(title="Ξχ Phase Portrait")

    return dcc.Graph(figure=fig)

# === Dash App ===
app = Dash(__name__)
app.title = "Ξχ Simulation Dashboard"

app.layout = html.Div([
    html.H1("Ξ–χ Simulation Viewer"),
    html.Div([
        create_entropy_graph(entropy_log, janus_idx),
        html.Hr(),
        create_phase_portrait(entropy_log, drift_tensor)
    ])
])

if __name__ == "__main__":
    app.run(debug=True)

