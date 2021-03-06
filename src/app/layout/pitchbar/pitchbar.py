import dash_html_components as html
import dash_core_components as dcc
from plotly.graph_objects import Scatter

from src.app.components.pitch import plot_pitch, PENALTY_DISTANCE, PITCH_WIDTH \
    , PITCH_HEIGHT, GOAL_FIRST_POST_X, GOAL_SECOND_POST_X

pith = plot_pitch()


# Add first shot point to pitch
pith.add_trace(
    Scatter(
        x=[PITCH_WIDTH / 2],
        y=[PITCH_HEIGHT - PENALTY_DISTANCE],
        mode='markers',
        marker_size=10,
        marker_symbol='x',
        hoverinfo='none',
    )
)

# Add first shot angle
pith.add_trace(
    Scatter(
        x=[PITCH_WIDTH / 2, GOAL_FIRST_POST_X, GOAL_SECOND_POST_X],
        y=[PITCH_HEIGHT - PENALTY_DISTANCE, PITCH_HEIGHT, PITCH_HEIGHT],
        fill='toself',
        mode='none',
        hoverinfo='none',
    )
)

# Add points to click
all_range = (PITCH_WIDTH+1)*(PITCH_HEIGHT+1)
all_x = [i % (PITCH_WIDTH + 1) for i in range(all_range)]
all_y = [i // (PITCH_WIDTH + 1) for i in range(all_range)]
pith.add_trace(
    Scatter(
        x=all_x,
        y=all_y,
        mode='markers',
        marker_size=0,
        hoverinfo='none',
        opacity=0
    )
)

pitchbar = [
    html.H1(
        id='xg-value',
        children='Select pitch position to calculate xG',
        style={'color': '#52AC86', 'textAlign': 'left'}
    ),
    dcc.Graph(id='pitch', figure=pith)
]
