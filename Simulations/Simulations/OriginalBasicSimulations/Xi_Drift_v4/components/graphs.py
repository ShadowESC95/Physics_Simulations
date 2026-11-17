# components/graphs.py

from dash import dcc, html
import plotly.graph_objs as go

def build_main_graph():
    return html.Div([
        html.Label("Ξ / χ Field Viewer"),
        dcc.Graph(id="field-plot")
    ])

def entropy_graph():
    return html.Div([
        html.Label("Entropy Evolution"),
        dcc.Graph(id="entropy-plot")
    ])

