# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

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
    # TO DO:
    # - Update shot angle with pitch selection
    # - Update shot distance with pitch selection
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


@app.callback(
    Output('pitch', 'figure'),
    Input('pitch', 'figure'),
    Input('pitch', 'clickData'),
)
def update_shot_location(figure, click_data):

    if not click_data:
        return go.Figure(figure)

    x = click_data['points'][0]['x']
    y = click_data['points'][0]['y']

    fig = go.Figure(figure)

    # Update shot point
    shot_layer = len(fig.data) - 3
    fig['data'][shot_layer]['x'] = [x]
    fig['data'][shot_layer]['y'] = [y]

    # Update shot angle
    angle_layer = len(fig.data) - 2
    fig['data'][angle_layer]['x'] = [x] + list(fig['data'][angle_layer]['x'][1:])
    fig['data'][angle_layer]['y'] = [y] + list(fig['data'][angle_layer]['y'][1:])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
