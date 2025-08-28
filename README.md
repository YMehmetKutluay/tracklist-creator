# Setlist Creator

Simple Streamlit app to help create setlists for concerts. It is made for internal use by a cover band, but feel free to clone and tweak as you wish! Suggestions/feedback/debugging requests always welcome.

The app is currently [live](https://the-alternative-tracklist-creator.streamlit.app/), with restricted access. If you want access, then please open an issue in the Github repo page or send an email to mehkutluay@gmail.com.

# Getting Started

## Set up development environment

The development and app environment make use of Docker containers. To get started, you'll need to build the project's Docker image. You can do this by simply running `make build` from the main directory.

## Spotify API

The underlying logic assumes that there is a master list of all tracks. These are assumed to be in a public Spotify playlist. So the app connects to [Spotify's Web API](https://developer.spotify.com/documentation/web-api) to get the tracks from this playlist.

Thus, in order to start you need to first [create an account for yourself](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) and then get an access token. Put these in `config/credentials.yml` as such:

```
spotify:
 CLIENT_ID: <client id here>
 CLIENT_PASSWORD: <client password here>
```

# Directory Structure

* `config` - contains all app configurations, for instance `credentials.yml`
* `src` - contains all classes and methods used in the app
* `notebooks` - playground for development and trying out code snippets
