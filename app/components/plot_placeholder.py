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
            html.Br(),
            dcc.Textarea(
                id="analysis-textarea",
                style={"width": "100%", "height": 100},
            ),
        ],
    )
