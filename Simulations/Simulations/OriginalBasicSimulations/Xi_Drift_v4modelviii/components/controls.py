import dash_core_components as dcc
import dash_html_components as html

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
