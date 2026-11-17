from dash import dcc, html
import plotly.graph_objs as go

def controls_panel():
    return html.Div([
        html.Label("Select Field"),
        dcc.RadioItems(
            id='field-selector',
            options=[
                {'label': 'Ξ Field', 'value': 'xi'},
                {'label': 'χ Field', 'value': 'chi'},
                {'label': 'Drift Vector', 'value': 'drift'},
            ],
            value='xi',
            labelStyle={'display': 'inline-block'}
        ),
        html.Label("Time Frame"),
        dcc.Slider(id='frame-slider', min=0, max=100, step=1, value=0),
    ])
    
def build_main_graph():
    return html.Div([
        html.Label("Ξ / χ Field Viewer"),
        dcc.Graph(id="field-plot"),
    ])

def entropy_graph():
    return html.Div([
        html.Label("Entropy Evolution"),
        dcc.Graph(id="entropy-plot"),
    ])
