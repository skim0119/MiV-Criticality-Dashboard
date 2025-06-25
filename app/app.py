import dash

from app.callbacks.config_callbacks import register_config_callbacks
from app.callbacks.plot_callbacks import register_plot_callbacks
from app.callbacks.save_callbacks import register_save_callbacks
from app.callbacks.load_callbacks import register_load_callbacks
from app.callbacks.tag_callbacks import register_tag_callbacks
from app.components.layout import create_layout

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
)


def main(workdirs, port=5000, debug=False):
    """Run the Criticality Analysis Dashboard."""
    app.title = "Criticality analysis"
    app.layout = create_layout(workdirs)

    # Register all callbacks
    register_plot_callbacks(app)
    register_config_callbacks(app)
    register_save_callbacks(app)
    register_load_callbacks(app)
    register_tag_callbacks(app)

    app.run(debug=debug, port=port, host="0.0.0.0")
