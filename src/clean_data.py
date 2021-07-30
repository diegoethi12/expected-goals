import pandas as pd
import numpy as np
import math

from src import DATA_PATH

SELECTED_COLUMNS = [
    'play_pattern', 'location', 'shot_statsbomb_xg',
    'shot_outcome', 'shot_body_part', 'shot_technique'
]

shots = pd.read_pickle(DATA_PATH / 'raw_open_shots.pkl')
shots = shots[SELECTED_COLUMNS]

shots.describe()


def distance(x, y):
    return np.sqrt((y[0] - x[0]) ** 2 + (y[1] - x[1]) ** 2)


def shot_distance(x, middle_pitch):
    return np.sqrt(
        (middle_pitch[0]-x[0])**2 + (middle_pitch[1]-x[1])**2
    )


def shot_angle(x):
    near_post_coor = (120, 36)
    far_post_coor = (120, 44)
    near_post_dist = shot_distance(x, near_post_coor)
    far_post_dist = shot_distance(x, far_post_coor)

    # Al-Kashi theorem
    res = (near_post_dist ** 2 + far_post_dist ** 2 - (44 - 36) ** 2) / (2 * near_post_dist * far_post_dist)
    if res == 1.0 or res == -1.0:
        return 0
    elif res < -1.0 or res > 1.0:
        return 0
    else:
        return math.acos(res)


# New features

# Distance and angle
MIDDLE_PITCH = (120, 40)
shots['distance'] = shots['location'].apply(lambda x: shot_distance(x, MIDDLE_PITCH))
shots['angle'] = shots['location'].apply(lambda x: shot_angle(x))

# Body part
body_part_dict = {'Right Foot': 'Foot', 'Left Foot': 'Foot'}
shots['shot_body_part'] = shots['shot_body_part'].replace(body_part_dict)

# Target
shots['goal'] = shots['shot_outcome'].map({'Goal': 1}).fillna(0)

# Drop useless variables and save
shots = shots.drop(columns=['location', 'shot_outcome'])
shots.to_pickle(DATA_PATH / 'open_shots.pkl')


