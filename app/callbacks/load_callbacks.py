import os
import pickle
import logging
from dash import Input, Output, State

# Set up logger for this module
logger = logging.getLogger(__name__)

def register_load_callbacks(app):
    @app.callback(
        Output("bin-size-slider", "value"),
        Output("threshold-percentage-slider", "value"),
        Output("time-difference-slider", "value"),
        Output("allow_multiple_spike_per_bin", "value"),
        Output("minimum-bins-in-avalanche-slider", "value"),
        Output("min-interburst-interval-bound-slider", "value"),
        Output("pre-burst-extension-slider", "value"),
        Output("post-burst-extension-slider", "value"),
        Output("config-textarea", "value"),
        Output("analysis-textarea", "value"),
        Input("load-btn", "n_clicks"),
        State("path-dropdown", "value"),
        State("experiment-index-dropdown", "value"),
    )
    def load_analysis(
        n_clicks,
        path,
        experiment_index,
    ):
        if n_clicks is None or n_clicks == 0:
            # Return current values (no change)
            return [
                0.016,  # bin-size-slider default
                2.0,    # threshold-percentage-slider default
                0.002,  # time-difference-slider default
                False,  # allow_multiple_spike_per_bin default
                10,     # minimum-bins-in-avalanche-slider default
                0.1,    # min-interburst-interval-bound-slider default
                0.0,    # pre-burst-extension-slider default
                0.0,    # post-burst-extension-slider default
                "",     # config-textarea default
                "",     # analysis-textarea default
            ]

        tag = f"path_{os.path.basename(path)}_{os.path.basename(experiment_index)}"
        figures_dir = f"figures_{tag}"
        config_filename = f"{figures_dir}/config.pkl"
        csv_filename = f"{figures_dir}/criticality.csv"

        # Default values
        config_values = {
            "bin_size": 0.016,
            "threshold_percentage": 2.0,
            "time_difference": 0.002,
            "allow_multiple_spike_per_bin": False,
            "minimum_bins_in_avalanche": 10,
            "min_interburst_interval_bound": 0.1,
            "pre_burst_extension": 0.0,
            "post_burst_extension": 0.0,
        }
        
        config_text = ""
        analysis_text = ""

        # Load configuration from pickle file
        if os.path.exists(config_filename):
            try:
                with open(config_filename, "rb") as f:
                    config_data = pickle.load(f)
                    
                # Update config_values with loaded data
                config_values.update({k: v for k, v in config_data.items() if k in config_values})
                
                # Reconstruct config text for display
                config_text = f"bin_size: {config_values['bin_size']}, threshold_percentage: {config_values['threshold_percentage']}, time_difference: {config_values['time_difference']}, allow_multiple_spike_per_bin: {config_values['allow_multiple_spike_per_bin']}, minimum_bins_in_avalanche: {config_values['minimum_bins_in_avalanche']}, min_interburst_interval_bound: {config_values['min_interburst_interval_bound']}, pre_burst_extension: {config_values['pre_burst_extension']}, post_burst_extension: {config_values['post_burst_extension']}"
                
            except Exception as e:
                config_text = f"Error loading configuration: {str(e)}"
        else:
            config_text = "Configuration file not found"
        logger.warning("config_data")
        logger.warning(config_data)

        # Load analysis text from CSV file
        if os.path.exists(csv_filename):
            try:
                with open(csv_filename, "r") as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        analysis_text = lines[1].strip()
            except Exception as e:
                analysis_text = f"Error loading analysis: {str(e)}"

        return [
            config_values["bin_size"],
            config_values["threshold_percentage"],
            config_values["time_difference"],
            config_values["allow_multiple_spike_per_bin"],
            config_values["minimum_bins_in_avalanche"],
            config_values["min_interburst_interval_bound"],
            config_values["pre_burst_extension"],
            config_values["post_burst_extension"],
            config_text,
            analysis_text,
        ] 