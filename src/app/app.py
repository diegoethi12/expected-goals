# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from src.app.layout.layout import layout, xg_model

# Main app
app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])

server = app.server

app.layout = layout


@app.callback(
    Output('xg-value', 'children'),
    Input('play-pattern-dropdown', 'value'),
    Input('shot-body-part-dropdown', 'value'),
    Input('shot-technique-dropdown', 'value'),
    Input('angle-slider', 'value'),
    Input('distance-slider', 'value')
)
def update_xg(play_pattern, shot_body_part, shot_technique, angle, distance):
    df = pd.DataFrame(
        dict(play_pattern=play_pattern,
             shot_body_part=shot_body_part,
             shot_technique=shot_technique,
             distance=distance,
             angle=angle,
             ),
        index=[0]
    )
    xg = xg_model.predict_proba(df)[:, 1][0]
    return f"xG: {int(np.round(xg, 2) * 100)}%"


if __name__ == '__main__':
    app.run_server(debug=True)
