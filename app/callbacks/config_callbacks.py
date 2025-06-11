from dash import Input, Output


def register_config_callbacks(app):
    @app.callback(
        Output("config-textarea", "value"),
        [
            Input("bin-size-slider", "value"),
            Input("threshold-percentage-slider", "value"),
            Input("time-difference-slider", "value"),
            Input("allow_multiple_spike_per_bin", "value"),
            Input("minimum-bins-in-avalanche-slider", "value"),
            Input("min-interburst-interval-bound-slider", "value"),
            Input("pre-burst-extension-slider", "value"),
            Input("post-burst-extension-slider", "value"),
        ],
    )
    def update_config_textarea(
        bin_size,
        threshold_percentage,
        time_difference,
        allow_multiple_spike_per_bin,
        minimum_bins_in_avalanche,
        min_interburst_interval_bound,
        pre_burst_extension,
        post_burst_extension,
    ):
        # print all configuration parameters in config-textarea
        rets = []
        rets.append(f"bin_size: {bin_size}")
        rets.append(f"threshold_percentage: {threshold_percentage}")
        rets.append(f"time_difference: {time_difference}")
        rets.append(f"allow_multiple_spike_per_bin: {allow_multiple_spike_per_bin}")
        rets.append(f"minimum_bins_in_avalanche: {minimum_bins_in_avalanche}")
        rets.append(f"min_interburst_interval_bound: {min_interburst_interval_bound}")
        rets.append(f"pre_burst_extension: {pre_burst_extension}")
        rets.append(f"post_burst_extension: {post_burst_extension}")
        return "\n".join(rets)
