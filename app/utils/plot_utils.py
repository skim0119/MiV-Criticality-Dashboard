import pickle as pkl

import plotly.graph_objs as go


def get_raster(fig, data_path, experiment, bin_size):
    """Generate raster plot for the given data."""
    # Load Data
    with open(data_path, "rb") as f:
        spikestamps = pkl.load(f)
    interval = 120  # sec TODO
    starts, ends, bincount = experiment.output["avalanche_detection"]

    starts_time = starts * bin_size + bincount.timestamps[0]
    ends_time = ends * bin_size + bincount.timestamps[0]

    # Plot raster
    spikestamps = spikestamps.get_view(
        spikestamps.get_first_spikestamp(),
        spikestamps.get_first_spikestamp() + interval,
    )
    x, y = spikestamps.flatten()

    trace = go.Scatter(
        x=x, y=y, mode="markers", opacity=0.8, marker=dict(size=2, symbol="circle")
    )
    fig.add_trace(trace)

    for start, end in zip(starts_time, ends_time, strict=False):
        fig.add_vrect(
            x0=start, x1=end, fillcolor="red", opacity=0.2, line_width=0, layer="below"
        )
        if start > spikestamps.get_first_spikestamp() + interval:
            break
    fig.update_xaxes(
        range=[
            spikestamps.get_first_spikestamp(),
            spikestamps.get_first_spikestamp() + interval,
        ]
    )

    return trace
