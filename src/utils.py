from st_aggrid import JsCode


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
