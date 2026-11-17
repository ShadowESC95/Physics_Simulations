from dash import Dash, dcc, html, Input, Output
import numpy as np
import plotly.graph_objs as go
from components.controls import controls_panel
from components.graphs import build_main_graph, entropy_graph
import os

app = Dash(__name__)
server = app.server

# Load data
xi = np.load("output/xi_field_log.npy")
chi = np.load("output/chi_field_log.npy")
entropy = np.load("output/xi_entropy_log.npy")

app.layout = html.Div([
    html.H1("Ξχ Sim Viewer", style={'textAlign': 'center'}),
    controls_panel(),
    build_main_graph(),
    entropy_graph(),
])

@app.callback(
    Output('field-plot', 'figure'),
    Input('frame-slider', 'value'),
    Input('field-selector', 'value')
)
def update_graph(frame, field):
    field_data = xi if field == 'xi' else chi
    z = field_data[frame]
    fig = go.Figure(data=go.Heatmap(z=z, colorscale='Viridis'))
    fig.update_layout(title=f"{field.upper()} Frame {frame}")
    return fig

@app.callback(
    Output('entropy-plot', 'figure'),
    Input('frame-slider', 'value')
)
def update_entropy_plot(frame):
    fig = go.Figure(data=go.Scatter(y=entropy[:frame+1]))
    fig.update_layout(title="Entropy Evolution")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
