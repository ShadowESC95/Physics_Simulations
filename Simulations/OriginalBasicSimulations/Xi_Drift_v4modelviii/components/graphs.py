import dash_core_components as dcc
import plotly.graph_objs as go
import numpy as np

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
