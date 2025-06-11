import os

from dash import dcc, html


def generate_tag_selection_card(workdirs):
    """
    :param workdirs: List of working directories
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="tag-selection-card-outer",
        children=[
            html.Div(
                id="tag-selection-card",
                className="row",
                children=[
                    html.P("Tag", id="tag-title", className="one columns"),
                    dcc.Dropdown(
                        id="workdir-dropdown",
                        className="three columns",
                        options=[
                            {
                                "label": os.path.basename(directory),
                                "value": directory,
                            }
                            for directory in workdirs
                        ],
                        value=workdirs[0],
                    ),
                    dcc.Dropdown(
                        id="path-dropdown",
                        className="three columns",
                        options=[],  # Initialize with empty options
                        value=None,  # Initialize with no value
                    ),
                    dcc.Dropdown(
                        id="experiment-index-dropdown",
                        className="two columns",
                        options=[],  # Initialize with empty options
                        value=None,  # Initialize with no value
                    ),
                    html.Button("Save", id="save-btn", className="four columns"),
                ],
            ),
            html.Hr(),
        ],
    )
