import os
import pickle as pkl

import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

from app.criticality_module import Config, RunCriticalityAnalysis
from app.utils.plot_utils import get_raster

EXPERIMENT_CACHE = None
HISTOGRAM_DATA = {}


def func(config):
    experiment = RunCriticalityAnalysis()
    experiment(Config(**config))
    return experiment


def register_plot_callbacks(app):
    @app.callback(
        Output("run-btn", "disabled"),
        Output("run-loading", "style"),
        Input("run-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_button_state(n_clicks):
        if n_clicks is None:
            return False, {"display": "none"}
        return True, {"display": "block"}

    @app.callback(
        Output("branching-1-plot", "figure"),
        Output("powerlaw-1-plot", "figure"),
        Output("powerlaw-2-plot", "figure"),
        Output("powerlaw-3-plot", "figure"),
        Output("raster-plot", "figure"),
        Output("analysis-textarea", "value"),
        Output("run-btn", "disabled", allow_duplicate=True),
        Output("run-loading", "style", allow_duplicate=True),
        Input("run-btn", "n_clicks"),
        State("experiment-index-dropdown", "value"),
        State("bin-size-slider", "value"),
        State("threshold-percentage-slider", "value"),
        State("time-difference-slider", "value"),
        State("allow_multiple_spike_per_bin", "value"),
        State("minimum-bins-in-avalanche-slider", "value"),
        State("min-interburst-interval-bound-slider", "value"),
        State("pre-burst-extension-slider", "value"),
        State("post-burst-extension-slider", "value"),
        State("raster-start-time", "value"),
        State("raster-end-time", "value"),
        prevent_initial_call="initial_duplicate",
    )
    def update_plots(
        n_clicks,
        data_path,
        bin_size,
        threshold_percentage,
        time_difference,
        allow_multiple_spike_per_bin,
        minimum_bins_in_avalanche,
        min_interburst_interval_bound,
        pre_burst_extension,
        post_burst_extension,
        raster_start_time,
        raster_end_time,
    ):
        if not data_path:
            return [go.Figure() for _ in range(5)] + [""] + [False, {"display": "none"}]

        try:
            global EXPERIMENT_CACHE, HISTOGRAM_DATA
            path = data_path
            index = data_path.split("spike_detection_")[1]
            pipeline_run_path = os.path.dirname(path)
            spike_cache_path = os.path.join(path, ".cache", "cache_data_rank000_0000.pkl")

            config = {
                "class_id": index,
                "pipeline_run_path": pipeline_run_path,
                "spike_data_path": spike_cache_path,
                "data_tag": index,
                "bin_size": bin_size,
                "threshold_percentage": threshold_percentage,
                "time_difference": time_difference,
                "allow_multiple_spike_per_bin": allow_multiple_spike_per_bin,
                "minimum_bins_in_avalanche": minimum_bins_in_avalanche,
                "min_interburst_interval_bound": min_interburst_interval_bound,
                "pre_burst_extension": pre_burst_extension,
                "post_burst_extension": post_burst_extension,
            }
            experiment = func(config)
            EXPERIMENT_CACHE = experiment

            pl_fit = experiment.power_law_fitting()

            branching_ratio, mean_branching_ratio = experiment.branching_ratio_histogram()
            x2, y2, logbins2, size_fit, tau = pl_fit[0]
            x3, y3, logbins3, duration_fit, alpha = pl_fit[1]
            x4, y4, logbins4, average_fit, svz, svz_estim_ratio = pl_fit[2]
            HISTOGRAM_DATA.update(
                {
                    "branching_ratio": {
                        "branching_ratio": branching_ratio,
                        "mean_branching_ratio": mean_branching_ratio,
                    },
                    "tau": {
                        "x": x2,
                        "y": y2,
                        "logbins": logbins2,
                        "size_fit": size_fit,
                        "tau": tau,
                    },
                    "alpha": {
                        "x": x3,
                        "y": y3,
                        "logbins": logbins3,
                        "duration_fit": duration_fit,
                        "alpha": alpha,
                    },
                    "svz": {
                        "x": x4,
                        "y": y4,
                        "logbins": logbins4,
                        "average_fit": average_fit,
                        "svz": svz,
                        "svz_estim_ratio": svz_estim_ratio,
                    },
                }
            )
            fig1 = make_subplots(rows=1, cols=1)
            trace = px.histogram(
                x=branching_ratio,
                nbins=50,
                histnorm="probability",
            )
            fig1.add_trace(trace.data[0])
            fig1.update_layout(
                title=f"mean: {mean_branching_ratio:.03f}",
                xaxis_title="Branching ratio",
                margin=dict(l=0, r=0, t=30, b=1),
            )

            fig2 = make_subplots(rows=1, cols=1)
            if len(x2) > 1:
                trace1 = px.scatter(
                    x=x2,
                    y=y2,
                )
                fig2.add_trace(trace1.data[0])
            trace2 = px.line(
                x=logbins2,
                y=size_fit,
            )
            trace2.data[0].line.dash = "dot"
            trace2.data[0].line.color = "red"
            fig2.add_trace(trace2.data[0])
            fig2.update_layout(
                title=f"tau: {tau:.03f}",
                xaxis_title="Avalanche size (# of channels)",
                margin=dict(l=0, r=0, t=30, b=1),
            )
            fig2.update_xaxes(type="log")
            fig2.update_yaxes(type="log")

            # plot avalanche duration
            fig3 = make_subplots(rows=1, cols=1)
            trace1 = px.scatter(
                x=x3,
                y=y3,
            )
            trace2 = px.line(
                x=logbins3,
                y=duration_fit,
            )
            trace2.data[0].line.dash = "dot"
            trace2.data[0].line.color = "red"
            fig3.add_trace(trace1.data[0])
            fig3.add_trace(trace2.data[0])
            fig3.update_layout(
                title=f"alpha: {alpha:.03f}",
                xaxis_title="Avalanche duration (s)",
                margin=dict(l=0, r=0, t=30, b=1),
            )
            fig3.update_xaxes(type="log")
            fig3.update_yaxes(type="log")

            # plot average size in fig4
            fig4 = make_subplots(rows=1, cols=1)
            if len(x4) > 1:
                trace1 = px.scatter(
                    x=x4,
                    y=y4,
                )
                fig4.add_trace(trace1.data[0])
            trace2 = px.line(
                x=logbins4,
                y=average_fit,
            )
            trace2.data[0].line.dash = "dot"
            trace2.data[0].line.color = "red"
            fig4.add_trace(trace2.data[0])
            fig4.update_layout(
                title=f"1/svz = {svz:.02f}, (alpha-1)/(tau-1) = {svz_estim_ratio:.02f}",
                xaxis_title="Duration (s)",
                yaxis_title="Average size (# of channels)",
                margin=dict(l=0, r=0, t=30, b=1),
            )

            # Use provided start and end times for raster plot
            interval_range = None
            if raster_start_time is not None and raster_end_time is not None:
                interval_range = [raster_start_time, raster_end_time]

            fig6 = make_subplots(rows=1, cols=1)
            get_raster(fig6, spike_cache_path, experiment, bin_size, interval_range, HISTOGRAM_DATA)
            fig6.update_layout(
                title="Raster",
                xaxis_title="Time (s)",
                yaxis_title="Channel",
            )

            info = []
            info.append(f"1/svz = {svz:.02f}")
            info.append(f"(alpha-1)/(tau-1) = {svz_estim_ratio:.02f}")

            return (
                fig1,
                fig2,
                fig3,
                fig4,
                fig6,
                "\n".join(info),
                False,
                {"display": "none"},
            )
        except Exception as e:
            # If there's an error, re-enable the button and hide loading
            return [go.Figure() for _ in range(5)] + [str(e)] + [False, {"display": "none"}]

    @app.callback(
        Output("raster-plot", "figure", allow_duplicate=True),
        Output("update-raster-btn", "disabled"),
        Output("update-raster-loading", "style"),
        Output("raster-start-time", "value", allow_duplicate=True),
        Output("raster-end-time", "value", allow_duplicate=True),
        Input("update-raster-btn", "n_clicks"),
        State("raster-start-time", "value"),
        State("raster-end-time", "value"),
        State("experiment-index-dropdown", "value"),
        State("bin-size-slider", "value"),
        prevent_initial_call=True,
    )
    def update_raster_plot(n_clicks, start_time, end_time, data_path, bin_size):
        if not data_path or start_time is None or end_time is None:
            return go.Figure(), False, {"display": "none"}, start_time, end_time

        try:
            global EXPERIMENT_CACHE
            if EXPERIMENT_CACHE is None:
                raise PreventUpdate
            experiment = EXPERIMENT_CACHE
            spike_cache_path = experiment.config.spike_data_path

            # Load spike data to get valid range
            with open(spike_cache_path, "rb") as f:
                spikestamps = pkl.load(f)
            stime = spikestamps.get_first_spikestamp()
            etime = spikestamps.get_last_spikestamp()

            # Validate and clip the input values
            start_time = max(stime, min(etime, start_time))
            end_time = max(stime, min(etime, end_time))

            # If min > max, flip them
            if start_time > end_time:
                start_time, end_time = end_time, start_time

            interval_range = [start_time, end_time]

            global HISTOGRAM_DATA
            fig = make_subplots(rows=1, cols=1)
            get_raster(fig, spike_cache_path, experiment, bin_size, interval_range, HISTOGRAM_DATA)
            fig.update_layout(
                title="Raster",
                xaxis_title="Time (s)",
                yaxis_title="Channel",
            )
            return fig, False, {"display": "none"}, start_time, end_time
        except Exception:
            return go.Figure(), False, {"display": "none"}, start_time, end_time

    @app.callback(
        Output("raster-start-time", "value", allow_duplicate=True),
        Output("raster-end-time", "value", allow_duplicate=True),
        Input("raster-start-time", "value"),
        Input("raster-end-time", "value"),
        State("experiment-index-dropdown", "value"),
        prevent_initial_call=True,
    )
    def validate_raster_inputs(start_time, end_time, data_path):
        if not data_path or start_time is None or end_time is None:
            raise PreventUpdate

        try:
            path = data_path
            spike_cache_path = os.path.join(path, ".cache", "cache_data_rank000_0000.pkl")
            with open(spike_cache_path, "rb") as f:
                spikestamps = pkl.load(f)
            stime = spikestamps.get_first_spikestamp()
            etime = spikestamps.get_last_spikestamp()

            # Clip values to valid range
            start_time = max(stime, min(etime, start_time))
            end_time = max(stime, min(etime, end_time))

            # If min > max, flip them
            if start_time > end_time:
                start_time, end_time = end_time, start_time

            return start_time, end_time
        except Exception:
            raise PreventUpdate from None

    @app.callback(
        Output("raster-min-label", "children"),
        Output("raster-max-label", "children"),
        Input("run-btn", "n_clicks"),
        State("experiment-index-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_raster_range_info(n_clicks, data_path):
        if not data_path:
            return "Min: 0s", "Max: 300s"

        try:
            path = data_path
            spike_cache_path = os.path.join(path, ".cache", "cache_data_rank000_0000.pkl")
            with open(spike_cache_path, "rb") as f:
                spikestamps = pkl.load(f)
            stime = spikestamps.get_first_spikestamp()
            etime = spikestamps.get_last_spikestamp()

            min_label = f"Min: {stime:.2f}s"
            max_label = f"Max: {etime:.2f}s"

            return min_label, max_label
        except Exception as e:
            raise PreventUpdate from e
