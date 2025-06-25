from dash import dcc, html


def generate_criticality_plot_placeholder():
    return html.Div(
        id="criticality-plot-placeholder-outer",
        children=[
            html.Div(
                id="plot-row1-placeholder",
                className="row",
                children=[
                    dcc.Graph(id="branching-1-plot", className="three columns"),
                    dcc.Graph(id="powerlaw-1-plot", className="three columns"),
                    dcc.Graph(id="powerlaw-2-plot", className="three columns"),
                    dcc.Graph(id="powerlaw-3-plot", className="three columns"),
                ],
            ),
            html.Hr(),
            html.Div(
                id="plot-row2-placeholder",
                className="row",
                children=[
                    dcc.Graph(id="branching-2-plot", className="three columns"),
                    dcc.Graph(id="raster-plot", className="nine columns"),
                ],
            ),
            html.Div(
                id="raster-controls",
                className="row",
                children=[
                    html.Div(
                        className="nine columns",
                        children=[
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="six columns",
                                        children=[
                                            html.Label("Start Time (s):", style={"font-weight": "bold"}),
                                            dcc.Input(
                                                id="raster-start-time",
                                                type="number",
                                                placeholder="Enter start time",
                                                style={"width": "100%", "margin-bottom": "5px"},
                                            ),
                                            html.Div(id="raster-min-label", style={"font-size": "12px", "color": "#666"}),
                                        ],
                                    ),
                                    html.Div(
                                        className="six columns",
                                        children=[
                                            html.Label("End Time (s):", style={"font-weight": "bold"}),
                                            dcc.Input(
                                                id="raster-end-time",
                                                type="number",
                                                placeholder="Enter end time",
                                                style={"width": "100%", "margin-bottom": "5px"},
                                            ),
                                            html.Div(id="raster-max-label", style={"font-size": "12px", "color": "#666"}),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="three columns",
                        children=[
                            html.Button(
                                "Update Raster",
                                id="update-raster-btn",
                                className="button-primary",
                            ),
                            html.Div(
                                id="update-raster-loading",
                                style={"display": "none"},
                                children=[
                                    html.Div(
                                        className="loading",
                                        children=[
                                            html.Div(
                                                className="loading-spinner",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            html.Br(),
            dcc.Textarea(
                id="analysis-textarea",
                style={"width": "100%", "height": 100},
            ),
        ],
    )
