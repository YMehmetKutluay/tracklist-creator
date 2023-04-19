import pandas as pd
import yaml
import os

from src.fetch_data import Spotify
from src.utils import convert_ms_to_min_sec, convert_ms_to_readable

spotify = Spotify()

all_tracks_pd = spotify.get_tracks_of_playlist(spotify_username="mehkutluay", playlist_name="The Alternative")
