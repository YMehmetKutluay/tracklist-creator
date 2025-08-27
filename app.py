import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from src.fetch_data import Spotify

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

num_tables = st.number_input(
    "How many tables would you like to generate (max 10)?",
    min_value=1,
    max_value=10,
    value=1,
)

if "tables" not in st.session_state:
    st.session_state.tables = [
        pd.DataFrame(columns=list(all_tracks_pd.columns)) for _ in range(num_tables)
    ]

if len(st.session_state.tables) != num_tables:
    st.session_state.tables = [
        pd.DataFrame(columns=list(all_tracks_pd.columns)) for _ in range(num_tables)
    ]

st.subheader("Master Table")

gb = GridOptionsBuilder.from_dataframe(all_tracks_pd)
gb.configure_default_column(editable=True, groupable=True)
gb.configure_selection("multiple", use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    all_tracks_pd,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    height=300,
    allow_unsafe_jscode=True,
)

st.write("Selected Rows:", grid_response["selected_rows"])

# Generate target tables
for i in range(num_tables):
    st.subheader(f"Setlist Part {i + 1}")
    st.session_state.tables[i] = st.data_editor(
        st.session_state.tables[i], num_rows="dynamic", key=f"table_{i}"
    )
    st.text(
        f"Duration: {round(st.session_state.tables[i]['duration_ms'].astype(int).sum() / 1000 / 60, 2)} minutes "
    )
