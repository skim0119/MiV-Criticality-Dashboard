import datetime
import os

import plotly.io as pio
from dash import Input, Output, State


def register_save_callbacks(app):
    @app.callback(
        Output("save-btn", "n_clicks"),
        Input("save-btn", "n_clicks"),
        State("analysis-textarea", "value"),
        State("config-textarea", "value"),
        State("workdir-dropdown", "value"),
        State("path-dropdown", "value"),
        State("experiment-index-dropdown", "value"),
        State("branching-1-plot", "figure"),
        State("powerlaw-1-plot", "figure"),
        State("powerlaw-2-plot", "figure"),
        State("powerlaw-3-plot", "figure"),
        State("raster-plot", "figure"),
    )
    def save_analysis(
        n_clicks,
        analysis_text,
        config_text,
        workdir,
        path,
        experiment_index,
        branching_fig,
        powerlaw1_fig,
        powerlaw2_fig,
        powerlaw3_fig,
        raster_fig,
    ):
        if n_clicks is None or n_clicks == 0:
            return 0

        # Create filename with datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"criticality_{timestamp}.csv"

        # Create directory for figures
        figures_dir = f"figures_{timestamp}"
        os.makedirs(figures_dir, exist_ok=True)

        # Save figures
        pio.write_image(branching_fig, os.path.join(figures_dir, "branching_ratio.png"))
        pio.write_image(powerlaw1_fig, os.path.join(figures_dir, "powerlaw_size.png"))
        pio.write_image(powerlaw2_fig, os.path.join(figures_dir, "powerlaw_duration.png"))
        pio.write_image(powerlaw3_fig, os.path.join(figures_dir, "powerlaw_average.png"))
        pio.write_image(raster_fig, os.path.join(figures_dir, "raster.png"))

        # append analysis_text and config_text to criticality.csv
        with open(filename, "a+") as f:
            f.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, "
                f"workdir: {workdir}, path: {path}, experiment: {experiment_index}, "
                f"figures_dir: {figures_dir}, "
                f"{config_text}\n"
            )
            f.write(f"{analysis_text}\n")
        return 0
