import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from src.fetch_data import Spotify
from src.utils import get_row_node_id, on_grid_ready, on_row_drag_end, on_row_drag_move

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

gb = GridOptionsBuilder.from_dataframe(all_tracks_pd)
gb.configure_default_column(
    rowDrag=False, rowDragManaged=True, rowDragEntireRow=False, rowDragMultiRow=True
)
gb.configure_column("name", rowDrag=True, rowDragEntireRow=True)
gb.configure_grid_options(
    rowDragManaged=True,
    onRowDragEnd=on_row_drag_end,
    deltaRowDataMode=True,
    getRowNodeId=get_row_node_id,
    onGridReady=on_grid_ready,
    animateRows=True,
    onRowDragMove=on_row_drag_move,
)

gridOptions = gb.build()

data = AgGrid(
    all_tracks_pd,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.MANUAL,
)

st.write(data["data"])


# st.dataframe(data=all_tracks_pd.drop("duration_ms", axis=1), use_container_width=True)
