import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from joblib import load

from src import MODEL_PATH
from src.app.layout.inputs.inputs import inputs
from src.app.layout.pitchbar.pitchbar import pitchbar

# Data and model
xg_model = load(MODEL_PATH / 'model.joblib')

# Components
description = '''
    Here you can get the probability of score a goal based on an expected goals model
    built over the [open shots data](https://github.com/statsbomb/statsbombpy) of the 2018 FIFA World Cup
    provided by StatsBomb. Also, you can visit the [source code](https://github.com/diegoethi12) of the app.
'''

layout = dbc.Container(
    [
        html.H1("eXpected Goals"),

        html.Hr(),

        dcc.Markdown(description),

        dbc.Row(
            [
                dbc.Col(pitchbar),
                dbc.Col(inputs, md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)
