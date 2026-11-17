# xi_dash_gui_v1/app.py

from dash import Dash, dcc, html
from callbacks import register_callbacks
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
xi_log = np.load(os.path.join(DATA_DIR, 'xi_field_log.npy'))

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.H1("Ξχ DRIFT Field Explorer", style={'textAlign': 'center'}),
    dcc.Graph(id='field-3d-plot'),

    html.Div(id='entropy-display', style={'textAlign': 'center', 'fontWeight': 'bold'}),

    html.Div([
        html.Label("Frame:"),
        dcc.Slider(
            id='frame-slider',
            min=0,
            max=xi_log.shape[0] - 1,
            step=1,
            value=0,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    ], style={'margin': '30px'}),

    html.Div([
        html.Button('▶ Play', id='play-button', n_clicks=0),
        html.Button('⏸ Pause', id='pause-button', n_clicks=0),
        dcc.Interval(id='interval-timer', interval=500, n_intervals=0, disabled=True),
        html.Label("Playback speed (ms/frame):"),
        dcc.Input(id='playback-speed', type='number', value=500, min=100, step=100)
    ], style={'textAlign': 'center'}),

    html.Div([
        html.Label("Toggle Fields:"),
        dcc.Checklist(
            id='toggle-fields',
            options=[
                {'label': 'Ξ', 'value': 'xi'},
                {'label': 'χ', 'value': 'chi'},
                {'label': 'DRIFT', 'value': 'drift'},
            ],
            value=['xi', 'drift'],
            inline=True
        ),
    ], style={'textAlign': 'center'})
])

register_callbacks(app)

if __name__ == '__main__':
    print(f"[Ξχ GUI] Loaded {xi_log.shape[0]} timesteps")
    app.run(debug=True)
