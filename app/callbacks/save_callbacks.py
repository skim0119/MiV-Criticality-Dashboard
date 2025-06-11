import datetime

from dash import Input, Output, State


def register_save_callbacks(app):
    @app.callback(
        Output("save-btn", "n_clicks"),
        Input("save-btn", "n_clicks"),
        State("analysis-textarea", "value"),
        State("config-textarea", "value"),
    )
    def save_analysis(n_clicks, analysis_text, config_text):
        if n_clicks is None or n_clicks == 0:
            return 0

        # append analysis_text and config_text to criticality.csv
        with open("criticality.csv", "a+") as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {config_text}\n")
            f.write(f"{analysis_text}\n")
        return 0
