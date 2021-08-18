import dash_html_components as html
import dash_core_components as dcc

from src.app.components.pitch import plot_pitch

pitchbar = [
    html.H1(id='xg-value', style={'color': '#52AC86', 'textAlign': 'left'}),
    dcc.Graph(id='pitch', figure=plot_pitch())
]
