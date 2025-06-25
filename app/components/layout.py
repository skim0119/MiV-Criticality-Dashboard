from dash import html

from app.components.control_card import generate_control_card
from app.components.plot_placeholder import generate_criticality_plot_placeholder
from app.components.tag_selection import generate_tag_selection_card


def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Criticality analysis configuration"),
        ],
    )


def create_layout(workdirs):
    """Create the main application layout."""
    return html.Div(
        id="app-container",
        children=[
            # Banner
            html.Div(
                id="banner",
                className="banner",
                children=[html.H4("MiV-Interface 1.85.1.dashboard", style={"color": "white"})],
            ),
            html.Div(
                id="main-container",
                className="row",
                children=[
                    # Left column
                    html.Div(
                        id="left-column",
                        className="three columns",
                        children=[description_card(), generate_control_card()],
                    ),
                    # Right column
                    html.Div(
                        id="right-column",
                        className="nine columns",
                        children=[
                            generate_tag_selection_card(workdirs),
                            generate_criticality_plot_placeholder(),
                        ],
                    ),
                ],
            ),
        ],
    )
