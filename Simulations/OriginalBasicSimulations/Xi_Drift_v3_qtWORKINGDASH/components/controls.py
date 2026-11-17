from dash import html, dcc

def controls_panel(steps=100):
    return html.Div([
        html.Label("Select Field:"),
        dcc.Dropdown(
            id="field-selector",
            options=[
                {"label": "Ξ Field", "value": "xi"},
                {"label": "χ Field", "value": "chi"},
            ],
            value="xi"
        ),
        html.Br(),

        html.Label("Select Frame:"),
        dcc.Slider(
            id="frame-slider",
            min=0,
            max=steps - 1,
            value=0,
            marks={i: str(i) for i in range(0, steps, max(1, steps // 10))},
            step=1
        ),
    ])
