from dash import dcc, html
import plotly.graph_objs as go
import numpy as np

def build_main_graph():
    fig = go.Figure()
    fig.update_layout(title="Ξχ Scalar Field Snapshot")
    return dcc.Graph(id="field-plot", figure=fig)

def create_entropy_graph():
    try:
        entropy = np.load("output/xi_entropy_log.npy")
        steps = list(range(len(entropy)))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=steps, y=entropy, mode='lines', name='Entropy'))
        fig.update_layout(title="Ξ Entropy Over Time", xaxis_title="Step", yaxis_title="Entropy")
    except Exception as e:
        fig = go.Figure()
        fig.update_layout(title=f"Entropy Data Missing: {e}")
    return dcc.Graph(id="entropy-plot", figure=fig)

def create_phase_spiral():
    try:
        entropy = np.load("output/xi_entropy_log.npy")
        drift = np.load("output/drift_tensor_Xi.npy")
        drift_var = np.var(drift, axis=(1, 2))
        curvature = np.gradient(np.gradient(entropy))
        fig = go.Figure(data=[
            go.Scatter3d(
                x=entropy,
                y=curvature,
                z=drift_var,
                mode='lines+markers',
                marker=dict(size=3, color=entropy, colorscale='Viridis')
            )
        ])
        fig.update_layout(title="Ξχ Phase Portrait", scene=dict(
            xaxis_title="Entropy",
            yaxis_title="Curvature",
            zaxis_title="Drift Variance"
        ))
    except Exception as e:
        fig = go.Figure()
        fig.update_layout(title=f"Phase Portrait Error: {e}")
    return dcc.Graph(figure=fig)
