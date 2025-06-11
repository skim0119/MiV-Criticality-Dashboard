import pickle as pkl

import plotly.graph_objs as go


def get_raster(fig, data_path, experiment, bin_size, interval=None):
    """Generate raster plot for the given data."""
    # Load Data
    with open(data_path, "rb") as f:
        spikestamps = pkl.load(f)
    starts, ends, bincount = experiment.output["avalanche_detection"]

    starts_time = starts * bin_size + bincount.timestamps[0]
    ends_time = ends * bin_size + bincount.timestamps[0]

    # Plot raster
    if interval is None:
        interval = [
            spikestamps.get_first_spikestamp(),
            min(
                spikestamps.get_first_spikestamp() + 60,
                spikestamps.get_last_spikestamp(),
            ),
        ]
    spikestamps = spikestamps.get_view(
        interval[0],
        interval[1],
    )
    x, y = spikestamps.flatten()

    trace = go.Scatter(x=x, y=y, mode="markers", opacity=0.8, marker=dict(size=2, symbol="circle"))
    fig.add_trace(trace)

    for start, end in zip(starts_time, ends_time, strict=False):
        if start > interval[1]:
            break
        if end < interval[0]:
            continue
        fig.add_vrect(x0=start, x1=end, fillcolor="red", opacity=0.2, line_width=0, layer="below")
    fig.update_xaxes(range=[interval[0], interval[1]])

    return trace
