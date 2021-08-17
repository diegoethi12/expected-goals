# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
from joblib import load

from src import DATA_PATH, MODEL_PATH
from src.app.figs.pitch import plot_pitch

# Data and model
NUMERICAL_FEATURES = ['distance', 'angle']
CATEGORICAL_FEATURES = ['play_pattern', 'shot_body_part', 'shot_technique']

shots = pd.read_pickle(DATA_PATH / 'open_shots.pkl')
dd_options = {
    var: [dict(label=category, value=category) for category in shots[var].unique()] for var in CATEGORICAL_FEATURES
}

xg_model = load(MODEL_PATH / 'model.joblib')

# Components
description = '''
    Here you can get the probability of score a goal based on an expected goals model
    built over the [open shots data](https://github.com/statsbomb/statsbombpy) of the 2018 FIFA World Cup
    provided by StatsBomb. Also, you can visit the [source code](https://github.com/diegoethi12) of the app.
'''

def create_dropdown_form_group(label, id, variable, description):
    return dbc.FormGroup([
    dbc.Label(label, html_for=id),
    dcc.Dropdown(
        id=id,
        options=dd_options.get(variable),
        value=dd_options.get(variable)[0].get('value'),
        placeholder=description,
    )
])


play_pattern_form = create_dropdown_form_group(
    label='Play pattern',
    id='play-pattern-dropdown',
    variable='play_pattern',
    description='Select a play pattern'
)

shot_body_part_form = create_dropdown_form_group(
    label='Shot body part',
    id='shot-body-part-dropdown',
    variable='shot_body_part',
    description='Select a shot body part'
)

shot_technique_form = create_dropdown_form_group(
    label='Shot technique',
    id='shot-technique-dropdown',
    variable='shot_technique',
    description='Select a shot technique'
)

angle_form = dbc.FormGroup([
    dbc.Label('Shot Angle', html_for='angle-slider'),
    dcc.Slider(
        id='angle-slider',
        min=0,
        max=1,
        value=0.4,
        marks={str(round(angle, 1)): str(round(angle, 1)) for angle in np.arange(0, 1.1, 0.1)},
        step=None
    )
])

distance_form = dbc.FormGroup([
    dbc.Label('Distance', html_for='distance-slider'),
    dcc.Slider(
        id='distance-slider',
        min=0,
        max=100,
        value=20,
        marks={str(round(distance, 1)): str(round(distance, 1)) for distance in range(0, 101, 10)},
        step=None
    )
])


inputs = dbc.Form([play_pattern_form, shot_body_part_form, shot_technique_form, angle_form, distance_form])

# Main app
app = dash.Dash(external_stylesheets=[dbc.themes.SUPERHERO])

server = app.server

app.layout = dbc.Container(
    [
        html.H1("eXpected Goals"),

        html.Hr(),

        dcc.Markdown(description),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(id='xg-value', style={'color': '#52AC86', 'textAlign': 'left'}),
                        dcc.Graph(id='pitch', figure=plot_pitch())
                    ]
                ),
                dbc.Col(inputs, md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


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
