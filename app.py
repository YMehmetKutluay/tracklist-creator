import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

from src.fetch_data import Spotify

onRowDragEnd = JsCode(
    """
function onRowDragEnd(e) {
    console.log('onRowDragEnd', e);
}
"""
)

getRowNodeId = JsCode(
    """
function getRowNodeId(data) {
    return data.id
}
"""
)

onGridReady = JsCode(
    """
function onGridReady() {
    immutableStore.forEach(
        function(data, index) {
            data.id = index;
            });
    gridOptions.api.setRowData(immutableStore);
    }
"""
)

onRowDragMove = JsCode(
    """
function onRowDragMove(event) {
    var movingNode = event.node;
    var overNode = event.overNode;

    var rowNeedsToMove = movingNode !== overNode;

    if (rowNeedsToMove) {
        var movingData = movingNode.data;
        var overData = overNode.data;

        immutableStore = newStore;

        var fromIndex = immutableStore.indexOf(movingData);
        var toIndex = immutableStore.indexOf(overData);

        var newStore = immutableStore.slice();
        moveInArray(newStore, fromIndex, toIndex);

        immutableStore = newStore;
        gridOptions.api.setRowData(newStore);

        gridOptions.api.clearFocusedCell();
    }

    function moveInArray(arr, fromIndex, toIndex) {
        var element = arr[fromIndex];
        arr.splice(fromIndex, 1);
        arr.splice(toIndex, 0, element);
    }
}
"""
)


spotify = Spotify()

st.title("Tracklist Creator")

spotify_username = st.text_input("Fill in Spotify username", "mehkutluay")

playlist_name = st.text_input("Fill in (public) Spotify playlist", "The Alternative")


# @st.cache_data
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
    onRowDragEnd=onRowDragEnd,
    deltaRowDataMode=True,
    getRowNodeId=getRowNodeId,
    onGridReady=onGridReady,
    animateRows=True,
    onRowDragMove=onRowDragMove,
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
