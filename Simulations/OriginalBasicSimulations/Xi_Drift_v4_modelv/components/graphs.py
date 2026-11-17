from dash import dcc, html
import plotly.graph_objs as go
import numpy as np
import os

def create_entropy_graph(entropy_log):
    return dcc.Graph(
        figure=go.Figure(
            data=[go.Scatter(y=entropy_log, mode='lines')],
            layout=go.Layout(title="Ξχ Entropy over Time")
        )
    )

def create_phase_spiral(xi_entropy, drift_tensor):
    drift_var = np.var(drift_tensor, axis=(1, 2, 3))
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

# === NEW FUNCTIONS TO FIX IMPORTS ===

def build_main_graph():
    """Dash Graph for entropy loaded from file."""
    try:
        entropy_path = os.path.join("output", "xi_entropy_log.npy")
        entropy_log = np.load(entropy_path)
        return create_entropy_graph(entropy_log)
    except Exception as e:
        return html.Div(f"Error loading entropy graph: {e}")

def entropy_graph():
    """Alias to build_main_graph for app layout use."""
    return build_main_graph()

