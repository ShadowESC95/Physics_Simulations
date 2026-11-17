
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

# Load Ξ field snapshots (replace with your real path or updated values)
snapshots = np.load('Xi_Chi_LongRun_Snapshots/xi_long_snapshot_199.npy')  # Placeholder

# Mock entropy and G5 series
steps = 200
S_series = np.linspace(8.28, 8.31, steps)
G5_series = np.linspace(0.025, 0.035, steps)

app = dash.Dash(__name__)
app.title = "Ξ–χ Model 5 Dashboard"

app.layout = html.Div([
    html.H1("Ξ–χ Model 5 Dashboard (Horndeski Curvature Coupling)", style={'textAlign': 'center'}),

    dcc.Slider(0, steps-1, step=1, value=0, id='step-slider',
               marks={0: '0', steps//2: str(steps//2), steps-1: str(steps-1)}),
    html.Div(id='step-output', style={'textAlign': 'center'}),

    dcc.Graph(id='xi-heatmap'),
    dcc.Graph(id='g5-plot'),
])

@app.callback(
    Output('step-output', 'children'),
    Output('xi-heatmap', 'figure'),
    Output('g5-plot', 'figure'),
    Input('step-slider', 'value')
)
def update_dashboard(step):
    # Generate synthetic Ξ field (replace with real field data for that step)
    x = np.linspace(0, 1, 50)
    y = np.linspace(0, 1, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(2 * np.pi * (X + Y + step / 50.0))  # Mock pattern

    heatmap_fig = px.imshow(Z, color_continuous_scale='Viridis', origin='lower')
    heatmap_fig.update_layout(title="Ξ Field Snapshot")

    g5_fig = px.line(x=np.arange(step+1), y=G5_series[:step+1], labels={'x': 'Time Step', 'y': 'Mean $G_5(\Xi)$'})
    g5_fig.update_layout(title="Curvature Feedback: $G_5(\Xi)$ over Time")

    return f"Time Step: {step}", heatmap_fig, g5_fig

if __name__ == '__main__':
    app.run_server(debug=True)
