import os

from dash import Input, Output, State

from app.utils.data_utils import get_experiment_index, get_subdirectories


def register_tag_callbacks(app):
    @app.callback(
        Output("path-dropdown", "options"),
        Input("workdir-dropdown", "value"),
    )
    def update_path_dropdown(workdir):
        """Update path dropdown options based on selected workdir."""
        paths, full_paths = get_subdirectories(workdir, tag="spike_detection_00")
        optinal_tag = get_subdirectories(workdir, tag="spike_detection_00_0-127")
        paths += optinal_tag[0]
        full_paths += optinal_tag[1]

        paths_options = [
            {"label": os.path.basename(path), "value": full_path}
            for path, full_path in zip(paths, full_paths, strict=False)
        ]
        return paths_options

    @app.callback(
        Output("experiment-index-dropdown", "options"),
        Input("path-dropdown", "value"),
        State("workdir-dropdown", "value"),
    )
    def update_experiment_index_dropdown(path, workdir):
        if not path:
            return []

        _path = os.path.join(workdir, path)
        experiment_index = get_experiment_index(_path, "spike_detection_*")
        experiment_index_options = [
            {
                "label": str(index),
                "value": os.path.join(_path, f"spike_detection_{index}"),
            }
            for index in experiment_index
        ]
        return experiment_index_options
