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
                            dcc.RangeSlider(
                                id="raster-interval-slider",
                                min=1,
                                max=300,
                                step=1,
                                value=[0, 60],
                                marks={i: f"{i}s" for i in range(0, 301, 60)},
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
