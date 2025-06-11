from dash import dcc, html


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Div(
                id="bin-size-control-card-outer",
                className="row",
                children=[
                    html.P("Bin Size", className="nine columns"),
                    html.Button("sweep", id="sweep-bin-size-btn", className="three columns"),
                ],
            ),
            dcc.Slider(
                0.001,
                0.064,
                0.001,
                value=0.002,
                id="bin-size-slider",
                marks={i: f"{int(i*1000)}ms" for i in [0.002, 0.008, 0.016, 0.032, 0.064]},
            ),
            html.Br(),
            html.P("Threshold percentage"),
            html.P(
                "Larger the value, more sensitive in declaring avalanche",
                style={"font-weight": "normal"},
            ),
            dcc.Slider(
                0.1,
                5,
                0.1,
                value=2,
                id="threshold-percentage-slider",
                marks={i: f"{i}" for i in range(1, 51, 5)},
            ),
            html.Br(),
            html.P("Time Difference"),
            html.P("Merge neighboring avalanches", style={"font-weight": "normal"}),
            dcc.Slider(
                0.0,
                5.0,
                0.01,
                value=0.002,
                id="time-difference-slider",
                marks={i: f"{int(i)}s" for i in range(0, 6)},
            ),
            html.Br(),
            html.Br(),
            html.P("Allow multiple spike per bin"),
            dcc.RadioItems(
                id="allow_multiple_spike_per_bin",
                options=[
                    {"label": "Yes", "value": True},
                    {"label": "No", "value": False},
                ],
                value=False,
            ),
            html.Br(),
            html.P("Minimum bins in avalanche"),
            dcc.Slider(
                0,
                25,
                1,
                value=10,
                id="minimum-bins-in-avalanche-slider",
            ),
            html.Br(),
            html.P("Minimum interburst interval bound"),
            html.P(
                "Increase to coalesce overlapping burst",
                style={"font-weight": "normal"},
            ),
            dcc.Slider(
                0.01,
                0.5,
                0.01,
                value=0.1,
                id="min-interburst-interval-bound-slider",
                marks={i: f"{i:.02f}s" for i in range(1, 51, 5)},
            ),
            html.Br(),
            html.Br(),
            html.P("Pre burst extension"),
            dcc.Slider(
                0.0,
                0.5,
                0.02,
                value=0.0,
                id="pre-burst-extension-slider",
                marks={i: f"{i:.02f}s" for i in range(0, 51, 5)},
            ),
            html.Br(),
            html.P("Post burst extension"),
            dcc.Slider(
                0.0,
                0.5,
                0.02,
                value=0.0,
                id="post-burst-extension-slider",
                marks={i: f"{i:.02f}s" for i in range(0, 51, 5)},
            ),
            html.Br(),
            html.Div(
                id="run-button-container",
                className="row",
                children=[
                    html.Button(
                        "Run",
                        id="run-btn",
                        className="twelve columns",
                        disabled=False,
                    ),
                    dcc.Loading(
                        id="run-loading",
                        type="circle",
                        children=[],
                        style={"display": "none"},
                    ),
                ],
            ),
            html.Br(),
            html.P("Configurations:"),
            dcc.Textarea(
                id="config-textarea",
                style={"width": "100%", "height": 200},
            ),
        ],
    )
