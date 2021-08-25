import numpy as np
import plotly.graph_objects as go
from math import pi, sin, cos

# Test
import plotly.io as pio
pio.renderers.default = 'browser'

# Pitch Config
PITCH_WIDTH = 80
PITCH_HEIGHT = 120
CIRCLE_RADIUS = 12
LINE_COLOR = '#9fa6b7'
SMALL_AREA_WIDTH = 20
SMALL_AREA_HEIGHT = 6
PENALTY_AREA_WIDTH = 44
PENALTY_AREA_HEIGHT = 18
GOAL_HEIGHT = 2
GOAL_WIDTH = 8
PENALTY_DISTANCE = 12

# Calculated measures
GOAL_FIRST_POST_X = (PITCH_WIDTH - GOAL_WIDTH) / 2
GOAL_SECOND_POST_X = (PITCH_WIDTH + GOAL_WIDTH) / 2


def semi_circle_points(xcenter, ycenter, radius, points, cutmode, ycut):
    x = np.array([cos(2 * pi / points * x) * radius for x in range(0, points + 1)])
    y = np.array([sin(2 * pi / points * x) * radius for x in range(0, points + 1)])
    x = x+xcenter
    y = y+ycenter
    if cutmode == 'above':
        y_filter = y >= ycut
    elif cutmode == 'below':
        y_filter = y <= ycut
    else:
        raise KeyError(f'The selected cut mode "{cutmode}" does not exists')
    x = x[y_filter]
    y = y[y_filter]
    return x.tolist(), y.tolist()


def plot_pitch():

    # Generate figure
    fig = go.Figure()

    # Set layout size ad other properties
    fig.update_layout(
        clickmode='event+select',
        yaxis=dict(range=(-6, PITCH_HEIGHT + 6), scaleratio=1, visible=False,  # showticklabels=False, scaleanchor='x',
                   ),
        xaxis=dict(range=(-1, PITCH_WIDTH + 1), visible=False,  # showticklabels=False,
                   ),
        margin=dict(l=0, r=0, t=0, b=0),
        width=PITCH_WIDTH * 6, height=PITCH_HEIGHT * 6,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    # Add pitch border
    fig.add_shape(
        type='rect',
        x0=0, y0=0, x1=PITCH_WIDTH, y1=PITCH_HEIGHT,
        line=dict(color=LINE_COLOR, width=1, ),
        # fillcolor='rgba(0,0,0,0)',
        # layer='below',
    )

    # Add central circle
    fig.add_shape(
        type='circle',
        xref='x', yref='y',
        x0=PITCH_WIDTH / 2 - CIRCLE_RADIUS, x1=PITCH_WIDTH / 2 + CIRCLE_RADIUS,
        y0=PITCH_HEIGHT / 2 - CIRCLE_RADIUS, y1=PITCH_HEIGHT / 2 + CIRCLE_RADIUS,
        line_color=LINE_COLOR, line_width=1,
        # layer='below'
    )

    # Add midline
    fig.add_shape(
        type='rect',
        x0=0, x1=PITCH_WIDTH,
        y0=PITCH_HEIGHT / 2, y1=PITCH_HEIGHT / 2,
        line=dict(color=LINE_COLOR, width=1)
    )

    # Add penalty area 1
    fig.add_shape(
        type='rect',
        x0=PITCH_WIDTH / 2 - PENALTY_AREA_WIDTH / 2, x1=PITCH_WIDTH / 2 + PENALTY_AREA_WIDTH / 2,
        y0=0, y1=PENALTY_AREA_HEIGHT,
        line=dict(color=LINE_COLOR, width=1, ),
        # fillcolor='rgba(0,0,0,0)',
        # layer='below',
    )

    # Add penalty area 2
    fig.add_shape(
        type='rect',
        x0=PITCH_WIDTH / 2 - PENALTY_AREA_WIDTH / 2, x1=PITCH_WIDTH / 2 + PENALTY_AREA_WIDTH / 2,
        y0=PITCH_HEIGHT, y1=PITCH_HEIGHT - PENALTY_AREA_HEIGHT,
        line=dict(color=LINE_COLOR, width=1, ),
        # fillcolor='rgba(0,0,0,0)',
        # layer='below',
    )

    # Add small area 1
    fig.add_shape(
        type='rect',
        x0=PITCH_WIDTH / 2 - SMALL_AREA_WIDTH / 2, x1=PITCH_WIDTH / 2 + SMALL_AREA_WIDTH / 2,
        y0=0, y1=SMALL_AREA_HEIGHT,
        line=dict(color=LINE_COLOR, width=1, ),
        # fillcolor='rgba(0,0,0,0)',
        # layer='below',
    )

    # Add small area 2
    fig.add_shape(
        type='rect',
        x0=PITCH_WIDTH / 2 - SMALL_AREA_WIDTH / 2, x1=PITCH_WIDTH / 2 + SMALL_AREA_WIDTH / 2,
        y0=PITCH_HEIGHT, y1=PITCH_HEIGHT - SMALL_AREA_HEIGHT,
        line=dict(color=LINE_COLOR, width=1, ),
        # fillcolor='rgba(0,0,0,0)',
        # layer='below',
    )

    # Add goal 1
    fig.add_shape(
        type='rect',
        x0=PITCH_WIDTH / 2 - GOAL_WIDTH / 2, x1=PITCH_WIDTH / 2 + GOAL_WIDTH / 2,
        y0=0, y1=-1 * GOAL_HEIGHT,
        line=dict(color=LINE_COLOR, width=1, ),
        # fillcolor='rgba(0,0,0,0)',
        # layer='below',
    )

    # Add goal 2
    fig.add_shape(
        type='rect',
        x0=PITCH_WIDTH / 2 - GOAL_WIDTH / 2, x1=PITCH_WIDTH / 2 + GOAL_WIDTH / 2,
        y0=PITCH_HEIGHT, y1=PITCH_HEIGHT + GOAL_HEIGHT,
        line=dict(color=LINE_COLOR, width=1, ),
        # fillcolor='rgba(0,0,0,0)',
        # layer='below',
    )

    # Add penalty circles
    fig.add_trace(go.Scatter(
        x=[PITCH_WIDTH/2, PITCH_WIDTH/2],
        y=[PENALTY_DISTANCE, PITCH_HEIGHT-PENALTY_DISTANCE],
        line=dict(color=LINE_COLOR, width=1),
        mode='markers'
    ))

    # Add semi circles
    semi_circle_1_x, semi_circle_1_y = semi_circle_points(
        PITCH_WIDTH / 2, PENALTY_DISTANCE, CIRCLE_RADIUS, 10000,
        'above', PENALTY_AREA_HEIGHT)
    semi_circle_2_x, semi_circle_2_y = semi_circle_points(
        PITCH_WIDTH / 2, PITCH_HEIGHT - PENALTY_DISTANCE, CIRCLE_RADIUS, 10000,
        'below', PITCH_HEIGHT - PENALTY_AREA_HEIGHT)

    fig.add_trace(go.Scatter(
        x=semi_circle_1_x,
        y=semi_circle_1_y,
        mode='lines',
        hoverinfo='none',
        line=dict(color=LINE_COLOR, width=1)
    ))

    fig.add_trace(go.Scatter(
        x=semi_circle_2_x,
        y=semi_circle_2_y,
        mode='lines',
        hoverinfo='none',
        line=dict(color=LINE_COLOR, width=1)
    ))

    return fig
