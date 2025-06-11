import os
import pickle as pkl

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from plotly.subplots import make_subplots

from app.criticality_module import Config, RunCriticalityAnalysis
from app.utils.plot_utils import get_raster

EXPERIMENT_CACHE = None


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
    ):
        if not data_path:
            return [go.Figure() for _ in range(5)] + [""] + [False, {"display": "none"}]

        try:
            global EXPERIMENT_CACHE
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

            # plot branching ratio histogram in fig1
            branching_ratio, mean_branching_ratio = experiment.branching_ratio_histogram()
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

            # plot avalanche size histogram in loglog scale in fig2
            x, y, logbins, size_fit, tau = pl_fit[0]
            fig2 = make_subplots(rows=1, cols=1)
            if len(x) > 1:
                trace1 = px.scatter(
                    x=x,
                    y=y,
                )
                fig2.add_trace(trace1.data[0])
            trace2 = px.line(
                x=logbins,
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
            x, y, logbins, duration_fit, alpha = pl_fit[1]
            fig3 = make_subplots(rows=1, cols=1)
            trace1 = px.scatter(
                x=x,
                y=y,
            )
            trace2 = px.line(
                x=logbins,
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

            x, y, logbins, average_fit, svz, svz_estim_ratio = pl_fit[2]
            fig4 = make_subplots(rows=1, cols=1)
            if len(x) > 1:
                trace1 = px.scatter(
                    x=x,
                    y=y,
                )
                fig4.add_trace(trace1.data[0])
            trace2 = px.line(
                x=logbins,
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

            fig6 = make_subplots(rows=1, cols=1)
            get_raster(fig6, spike_cache_path, experiment, bin_size)
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
        Input("update-raster-btn", "n_clicks"),
        State("raster-interval-slider", "value"),
        State("experiment-index-dropdown", "value"),
        State("bin-size-slider", "value"),
        prevent_initial_call=True,
    )
    def update_raster_plot(n_clicks, interval_range, data_path, bin_size):
        if not data_path or not interval_range:
            return go.Figure(), False, {"display": "none"}

        try:
            global EXPERIMENT_CACHE
            if EXPERIMENT_CACHE is None:
                raise PreventUpdate
            experiment = EXPERIMENT_CACHE
            spike_cache_path = experiment.config.spike_data_path

            fig = make_subplots(rows=1, cols=1)
            get_raster(fig, spike_cache_path, experiment, bin_size, interval_range)
            fig.update_layout(
                title="Raster",
                xaxis_title="Time (s)",
                yaxis_title="Channel",
            )
            return fig, False, {"display": "none"}
        except Exception:
            return go.Figure(), False, {"display": "none"}

    @app.callback(
        Output("raster-interval-slider", "min"),
        Output("raster-interval-slider", "max"),
        Output("raster-interval-slider", "marks"),
        Output("raster-interval-slider", "value"),
        Input("run-btn", "n_clicks"),
        State("experiment-index-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_slider_range(n_clicks, data_path):
        if not data_path:
            return 1, 300, {i: f"{i}s" for i in range(0, 301, 60)}, [0, 60]

        try:
            path = data_path
            spike_cache_path = os.path.join(path, ".cache", "cache_data_rank000_0000.pkl")
            with open(spike_cache_path, "rb") as f:
                spikestamps = pkl.load(f)
            stime = spikestamps.get_first_spikestamp()
            etime = spikestamps.get_last_spikestamp()

            marks = {i: f"{i:.2f}s" for i in np.linspace(stime, etime, 20)}
            initial_value = [stime, min(stime + 60, etime)]

            return stime, etime, marks, initial_value
        except Exception as e:
            raise PreventUpdate from e
