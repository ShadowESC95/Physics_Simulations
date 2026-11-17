
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import numpy as np

# Load real data (placeholders for now)
xi_snapshots = [np.load(f'Xi_Chi_LongRun_Snapshots/xi_long_snapshot_{i:03d}.npy') for i in range(200)]
entropy_series = np.loadtxt('entropy_m5.csv')  # assumed saved
g5_series = np.loadtxt('g5_series.csv')        # assumed saved
alpha_series = np.load('alpha_field.npy')      # shape (steps, width)
div_js_series = np.load('entropy_flux.npy')    # shape (steps, width, height)

app = dash.Dash(__name__)
app.title = "Ξ–χ Model 5 Full Dashboard"

app.layout = html.Div([
    html.H1("Ξ–χ Horndeski Dashboard", style={'textAlign': 'center'}),
    
    dcc.Slider(0, 199, step=1, value=0, id='step-slider',
               marks={0: '0', 100: '100', 199: '199'}),
    html.Div(id='step-output', style={'textAlign': 'center'}),

    dcc.Dropdown(
        options=[
            {'label': 'Ξ Field', 'value': 'xi'},
            {'label': 'Entropy Flux ∇·Jₛ', 'value': 'div_js'},
            {'label': 'Fine-Structure α(Ξ)', 'value': 'alpha'},
            {'label': 'Photon Mass m_γ', 'value': 'mgamma'}
        ],
        value='xi',
        id='map-selector'
    ),

    dcc.Graph(id='field-map'),
    dcc.Graph(id='time-series')
])

@app.callback(
    Output('step-output', 'children'),
    Output('field-map', 'figure'),
    Output('time-series', 'figure'),
    Input('step-slider', 'value'),
    Input('map-selector', 'value')
)
def update_dashboard(step, view):
    if view == 'xi':
        Z = xi_snapshots[step]
        title = "Ξ Field"
    elif view == 'div_js':
        Z = div_js_series[step]
        title = "Entropy Flux ∇·Jₛ"
    elif view == 'alpha':
        Z = alpha_series[step].reshape(1, -1)  # 1D
        title = "Fine-Structure α(Ξ)"
    elif view == 'mgamma':
        grad_x, grad_y = np.gradient(xi_snapshots[step])
        grad_mag = np.sqrt(grad_x**2 + grad_y**2)
        Z = 1e-3 * (1 + grad_mag)
        title = "Photon Mass m_γ"

    fig_map = px.imshow(Z, color_continuous_scale='Viridis', origin='lower')
    fig_map.update_layout(title=title)

    fig_series = px.line(x=np.arange(step+1), y=entropy_series[:step+1], labels={'x': 'Step', 'y': 'S(t)'})
    fig_series.update_layout(title="Entropy S(t)")

    return f"Time Step: {step}", fig_map, fig_series

if __name__ == '__main__':
    app.run_server(debug=True)
