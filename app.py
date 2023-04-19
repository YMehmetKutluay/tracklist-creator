import streamlit as st

from src.fetch_data import Spotify

spotify = Spotify()

st.title("Tracklist Creator")

spotify_username = st.text_input("Fill in Spotify username", "mehkutluay")

playlist_name = st.text_input("Fill in (public) Spotify playlist", "The Alternative")

@st.cache()
def get_all_tracks_pd():
    return spotify.get_tracks_of_playlist(spotify_username=spotify_username, playlist_name=playlist_name)

st.header("All Tracks")
all_tracks_pd = get_all_tracks_pd()
st.dataframe(data=all_tracks_pd.drop("duration_ms", axis=1), use_container_width=True)

