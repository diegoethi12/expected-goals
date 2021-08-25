import dash_bootstrap_components as dbc
import dash_core_components as dcc

import numpy as np
import pandas as pd

from src import DATA_PATH

# Config
NUMERICAL_FEATURES = ['distance', 'angle']
CATEGORICAL_FEATURES = ['play_pattern', 'shot_body_part', 'shot_technique']

shots = pd.read_pickle(DATA_PATH / 'open_shots.pkl')
dd_options = {
    var: [dict(label=category, value=category) for category in shots[var].unique()] for var in CATEGORICAL_FEATURES
}


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

inputs = dbc.Form([play_pattern_form, shot_body_part_form, shot_technique_form])
