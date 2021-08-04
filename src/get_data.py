from statsbombpy import sb

from src import DATA_PATH

# Get events data from StatsBomb
events = sb.competition_events(
    country="International",
    division="FIFA World Cup",
    season="2018",
    gender="male",
    split=True
)

# Filter only open play shots
shots = events['shots']
open_play_shots_filter = shots['shot_type'] == 'Open Play'
open_shots = shots[open_play_shots_filter]

# Save
open_shots.to_pickle(DATA_PATH / 'raw_open_shots.pkl')
