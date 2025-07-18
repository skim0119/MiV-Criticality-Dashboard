import datetime
import os
import pickle

import plotly.io as pio
from dash import Input, Output, State

# Import HISTOGRAM_DATA from plot_callbacks
from app.callbacks.plot_callbacks import HISTOGRAM_DATA


def register_save_callbacks(app):
    @app.callback(
        Output("save-btn", "n_clicks"),
        Input("save-btn", "n_clicks"),
        State("analysis-textarea", "value"),
        State("workdir-dropdown", "value"),
        State("path-dropdown", "value"),
        State("experiment-index-dropdown", "value"),
        State("branching-1-plot", "figure"),
        State("powerlaw-1-plot", "figure"),
        State("powerlaw-2-plot", "figure"),
        State("powerlaw-3-plot", "figure"),
        State("raster-plot", "figure"),
        State("bin-size-slider", "value"),
        State("threshold-percentage-slider", "value"),
        State("time-difference-slider", "value"),
        State("allow_multiple_spike_per_bin", "value"),
        State("minimum-bins-in-avalanche-slider", "value"),
        State("min-interburst-interval-bound-slider", "value"),
        State("pre-burst-extension-slider", "value"),
        State("post-burst-extension-slider", "value"),
    )
    def save_analysis(
        n_clicks,
        analysis_text,
        workdir,
        path,
        experiment_index,
        branching_fig,
        powerlaw1_fig,
        powerlaw2_fig,
        powerlaw3_fig,
        raster_fig,
        bin_size,
        threshold_percentage,
        time_difference,
        allow_multiple_spike_per_bin,
        minimum_bins_in_avalanche,
        min_interburst_interval_bound,
        pre_burst_extension,
        post_burst_extension,
    ):
        if n_clicks is None or n_clicks == 0:
            return 0

        # Create filename with datetime
        # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        tag = f"path_{os.path.basename(path)}_{os.path.basename(experiment_index)}"

        # Create directory for figures
        figures_dir = f"figures_{tag}"
        filename = f"{figures_dir}/criticality.csv"
        config_filename = f"{figures_dir}/config.pkl"
        histogram_filename = f"{figures_dir}/histogram_data.pkl"
        os.makedirs(figures_dir, exist_ok=True)

        # Save figures
        pio.write_image(branching_fig, os.path.join(figures_dir, "branching_ratio.png"))
        pio.write_image(powerlaw1_fig, os.path.join(figures_dir, "powerlaw_size.png"))
        pio.write_image(powerlaw2_fig, os.path.join(figures_dir, "powerlaw_duration.png"))
        pio.write_image(powerlaw3_fig, os.path.join(figures_dir, "powerlaw_average.png"))
        pio.write_image(raster_fig, os.path.join(figures_dir, "raster.png"))

        # Save configuration to pickle file
        config_data = {
            "bin_size": bin_size,
            "threshold_percentage": threshold_percentage,
            "time_difference": time_difference,
            "allow_multiple_spike_per_bin": allow_multiple_spike_per_bin,
            "minimum_bins_in_avalanche": minimum_bins_in_avalanche,
            "min_interburst_interval_bound": min_interburst_interval_bound,
            "pre_burst_extension": pre_burst_extension,
            "post_burst_extension": post_burst_extension,
            "workdir": workdir,
            "path": path,
            "experiment_index": experiment_index,
            "figures_dir": figures_dir,
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(config_filename, "wb") as f:
            pickle.dump(config_data, f)

        # Save analysis text to CSV file (simplified)
        with open(filename, "a+") as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {figures_dir}\n")
            f.write(f"{analysis_text}\n")

        # Save histogram data if available
        histogram_data = HISTOGRAM_DATA.get(path)
        if histogram_data is not None:
            with open(histogram_filename, "wb") as f:
                pickle.dump(histogram_data, f)
        return 0
