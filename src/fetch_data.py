import os

import pandas as pd
import spotipy
import yaml
from spotipy.oauth2 import SpotifyClientCredentials

from src.utils import convert_ms_to_readable


class Spotify:
    def __init__(self):
        with open(os.path.join("config", "credentials.yml"), "r") as stream:
            credentials = yaml.safe_load(stream)

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=credentials["spotify"]["CLIENT_ID"],
                client_secret=credentials["spotify"]["CLIENT_PASSWORD"],
            )
        )

    def get_tracks_of_playlist(
        self, spotify_username: str, playlist_name: str
    ) -> pd.DataFrame:
        playlists = self.sp.user_playlists(spotify_username)
        for i, playlist in enumerate(playlists["items"]):
            if playlist["name"] == playlist_name:
                chosen_playlist = playlist
            else:
                pass

        playlist_owner = chosen_playlist["owner"]["display_name"]
        playlist_uri = chosen_playlist["uri"]

        playlist_tracks = self.sp.user_playlist_tracks(
            playlist_owner, playlist_uri, fields="items,uri,name,id,total"
        )["items"]

        tracks_pd_list = list()
        for track in playlist_tracks:
            sub_dict = {
                k: track["track"][k]
                for k in ("name", "duration_ms", "artists", "album")
            }
            tracks_pd_list.append(sub_dict)

        tracks_pd = pd.DataFrame.from_dict(tracks_pd_list)
        tracks_pd["artist"] = tracks_pd.apply(lambda x: x["artists"][0]["name"], axis=1)
        tracks_pd["album"] = tracks_pd.apply(lambda x: x["album"]["name"], axis=1)
        tracks_pd["duration"] = tracks_pd.apply(
            lambda x: convert_ms_to_readable(x["duration_ms"]), axis=1
        )

        return tracks_pd[["name", "artist", "duration", "duration_ms"]]
