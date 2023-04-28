import streamlit as st
from st_aggrid import (
    AgGrid,
    AgGridTheme,
    DataReturnMode,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
)


def convert_ms_to_min_sec(ms: int) -> dict:
    seconds = int((ms / 1000) % 60)
    minutes = int((ms / (1000 * 60)) % 60)
    return {"minutes": minutes, "seconds": seconds}


def convert_ms_to_readable(ms: int) -> str:
    min_sec_dict = convert_ms_to_min_sec(ms)
    return f"{min_sec_dict['minutes']}m{min_sec_dict['seconds']}s"


on_row_drag_end = JsCode(
    """
function onRowDragEnd(e) {
    console.log('onRowDragEnd', e);
}
"""
)

get_row_node_id = JsCode(
    """
function getRowNodeId(data) {
    return data.id
}
"""
)

on_grid_ready = JsCode(
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

on_row_drag_move = JsCode(
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


def create_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        rowDrag=False, rowDragManaged=True, rowDragEntireRow=False, rowDragMultiRow=True
    )
    # gb.configure_column("name", rowDrag=True, rowDragEntireRow=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
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

    grid = AgGrid(
        df,
        gridOptions=gridOptions,
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.MANUAL,
        fit_columns_on_grid_load=True,
        theme=AgGridTheme.STREAMLIT,  # Add theme color to the table
        enable_enterprise_modules=True,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    )

    return grid


def delete_row(df, grid):
    selected_rows = grid["selected_rows"]
    if selected_rows:
        selected_indices = [
            i["_selectedRowNodeInfo"]["nodeRowIndex"] for i in selected_rows
        ]
        df_indices = st.session_state.df_for_grid.index[selected_indices]
        df = df.drop(df_indices)
    return df
