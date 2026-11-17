# xi_dash_gui_v1/callbacks.py

import os
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, State, ctx

# Load data
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
xi_log = np.load(os.path.join(DATA_DIR, 'xi_field_log.npy'))
chi_log = np.load(os.path.join(DATA_DIR, 'chi_field_log.npy'))
drift_tensor = np.load(os.path.join(DATA_DIR, 'drift_tensor_Xi.npy'))
entropy = np.load(os.path.join(DATA_DIR, 'xi_entropy_log.npy'))

def make_surface(field, name, color_scale):
    return go.Surface(
        z=field,
        colorscale=color_scale,
        name=name,
        showscale=False,
        opacity=0.9 if name == "Xi" else 0.6
    )

def make_quiver(tensor):
    skip = (slice(None, None, 4), slice(None, None, 4))
    u = tensor[..., 0, 0][skip]
    v = tensor[..., 1, 1][skip]
    x, y = np.meshgrid(np.arange(u.shape[0]), np.arange(u.shape[1]))
    return go.Cone(
        x=x.ravel(),
        y=y.ravel(),
        z=np.zeros_like(x).ravel(),
        u=u.ravel(),
        v=v.ravel(),
        w=np.zeros_like(u).ravel(),
        sizemode="absolute",
        sizeref=2,
        anchor="tail",
        colorscale="Greys",
        name="DRIFT"
    )

def register_callbacks(app):
    @app.callback(
        Output("field-3d-plot", "figure"), Output("entropy-display", "children"),
        Input("frame-slider", "value"),
        Input("toggle-fields", "value")
    )
    def update_visuals(frame, toggles):
        fig = go.Figure()
        if "xi" in toggles:
            fig.add_trace(make_surface(xi_log[frame], "Xi", "plasma"))
        if "chi" in toggles:
            fig.add_trace(make_surface(chi_log[frame], "Chi", "magma"))
        if "drift" in toggles:
            fig.add_trace(make_quiver(drift_tensor))
        fig.update_layout(
            scene=dict(zaxis=dict(range=[0, 2]), camera_eye=dict(x=1.5, y=1.5, z=0.8)),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        return fig, f"Entropy at frame {frame}: {entropy[frame]:.5f}"

    @app.callback(
        Output('interval-timer', 'disabled'),
        Input('play-button', 'n_clicks'),
        Input('pause-button', 'n_clicks'),
        State('interval-timer', 'disabled')
    )
    def toggle_play_pause(n_play, n_pause, is_disabled):
        triggered = ctx.triggered_id
        if triggered == 'play-button':
            return False
        elif triggered == 'pause-button':
            return True
        return is_disabled

    @app.callback(
        Output('frame-slider', 'value'),
        Input('interval-timer', 'n_intervals'),
        State('frame-slider', 'value'),
        State('frame-slider', 'max')
    )
    def advance_frame(n_intervals, current_frame, max_frame):
        return (current_frame + 1) % (max_frame + 1)
