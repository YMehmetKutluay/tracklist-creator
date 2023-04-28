import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from src.fetch_data import Spotify
from src.utils import (
    create_grid,
    delete_row,
    get_row_node_id,
    on_grid_ready,
    on_row_drag_end,
    on_row_drag_move,
)

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

grid = create_grid(st.session_state.df_for_grid)

subtable_button = st.button("Extract table")
if subtable_button:
    st.session_state.df_for_grid = delete_row(st.session_state.df_for_grid, grid)


# st.dataframe(data=all_tracks_pd.drop("duration_ms", axis=1), use_container_width=True)
