import numpy as np
import pandas as pd
import streamlit as st
from pandas.api.types import is_bool_dtype, is_numeric_dtype
from st_aggrid import AgGrid, AgGridTheme, DataReturnMode, GridOptionsBuilder


def get_blank_from_dtype(dtype):
    """Return correct values for the new line: 0 if column is numeric, "" if column is object, ..."""
    if is_numeric_dtype(dtype):
        return 0
    elif is_bool_dtype(dtype):
        return False
    else:
        return ""


def add_row(df):
    df = df.append(
        pd.Series(
            [get_blank_from_dtype(dtype) for dtype in df.dtypes],
            index=df.columns,
        ),
        ignore_index=True,
    )
    return df


def delete_row(df, grid):
    selected_rows = grid["selected_rows"]
    if selected_rows:
        selected_indices = [
            i["_selectedRowNodeInfo"]["nodeRowIndex"] for i in selected_rows
        ]
        df_indices = st.session_state.df_for_grid.index[selected_indices]
        df = df.drop(df_indices)
    return df


def create_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=True,
        filter=True,
        resizable=True,
        sortable=True,
        value=True,
        enableRowGroup=True,
        enablePivot=True,
        enableValue=True,
        floatingFilter=True,
        aggFunc="sum",
        flex=1,
        minWidth=150,
        width=150,
        maxWidth=200,
    )
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridOptions = gb.build()
    grid = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.AS_INPUT,
        update_on="MANUAL",
        fit_columns_on_grid_load=True,
        theme=AgGridTheme.STREAMLIT,  # Add theme color to the table
        enable_enterprise_modules=True,
        height=600,
        width="100%",
    )

    return grid


def main():
    # Initialize your dataframe
    if "df_for_grid" not in st.session_state:
        st.session_state.df_for_grid = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    add_row_button = st.button("➕ Row")
    delete_row_button = st.button("➖ Row")
    if add_row_button:
        st.session_state.df_for_grid = add_row(st.session_state.df_for_grid)
    grid = create_grid(st.session_state.df_for_grid)
    if delete_row_button:
        st.session_state.df_for_grid = delete_row(st.session_state.df_for_grid, grid)


if __name__ == "__main__":
    main()
