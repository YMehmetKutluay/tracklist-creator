import pandas as pd
import streamlit as st

from src.fetch_data import Spotify
from src.utils import create_grid, delete_row

spotify = Spotify()

st.title("Tracklist Creator")

spotify_username = st.text_input("Fill in Spotify username", "mehkutluay")

playlist_name = st.text_input("Fill in (public) Spotify playlist", "The Alternative")


@st.cache_data
def get_all_tracks_pd():
    return spotify.get_tracks_of_playlist(
        spotify_username=spotify_username, playlist_name=playlist_name
    )


st.header("All Tracks")
all_tracks_pd = get_all_tracks_pd()

if "df_for_grid" not in st.session_state:
    st.session_state.df_for_grid = all_tracks_pd

subtable_button = st.button("Extract table")

grid = create_grid(st.session_state.df_for_grid)

if subtable_button:
    sub_table = grid["selected_rows"]
    st.session_state.df_for_grid = delete_row(st.session_state.df_for_grid, grid)
    st.write(pd.DataFrame(sub_table))
