import datetime
from typing import List, Literal

import numpy as np
import pandas as pd
import win32com.client
import win32com.gen_py.auto_cmc as cmc_

from managers.entities import DTYPES


# funcs that speak to commence:

def get_cmc() -> cmc_.ICommenceDB:
    try:
        cmc_db = win32com.client.Dispatch(f"Commence.DB")
    except Exception as e:
        raise e
    else:
        return cmc_db


def get_csr(tablename) -> cmc_.ICommenceCursor:
    cmc = get_cmc()
    return cmc.GetCursor(0, tablename, 0)


def get_record(cursor: cmc_.ICommenceCursor, record_name: str) -> pd.DataFrame:
    filter_by_field(cursor, 'Name', record_name)
    qs: cmc_.ICommenceQueryRowSet = cursor.GetQueryRowSet(5, 0)
    if qs.RowCount != 1:
        raise ValueError(f"{qs.RowCount} rows returned")
    if qs.GetRowValue(0, 0, 0) != record_name:
        raise ValueError(f"Expected {record_name} but got {qs.GetRowValue(0, 0)}")

    data = qs_to_lists(qs)
    df = pd.DataFrame(data, columns=get_fieldnames(qs))
    df = parse_df(df)
    # ser = pd.Series(data=data, index=get_fieldnames(qs))
    # return ser
    return df

def get_connected_records(cursor: cmc_.ICommenceCursor, connection_name: str, connection_table: str,
                          item_name: str, max_res=None) -> pd.DataFrame:
    filter_by_connection(cursor, item_name, connection_name, connection_table)
    qs = cursor.GetQueryRowSet(50, 0)
    if qs.RowCount == 0:
        return pd.DataFrame()
    if max_res and qs.RowCount > max_res:
        raise ValueError(f"Query set has {qs.RowCount} rows, more than {max_res} rows requested")

    data_list = qs_to_lists(qs)
    df_data = pd.DataFrame(data_list, columns=get_fieldnames(qs))
    return df_data


def customer(record_name) -> pd.DataFrame:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Customer', 0)
    return get_record(cursor, record_name)


def hire(record_name: str) -> pd.DataFrame:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Hire', 0)
    return get_record(cursor, record_name)


def sale(record_name: str) -> pd.DataFrame:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Sale', 0)
    return get_record(cursor, record_name)


def sales_by_customer(customer_name: str) -> pd.DataFrame:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Sale', 0)
    return get_connected_records(cursor, 'To', 'Customer', customer_name)


def hires_by_customer(customer_name: str) -> pd.DataFrame:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Hire', 0)
    return get_connected_records(cursor, 'To', 'Customer', customer_name)


def cust_of_transaction(trans_name: str, category: Literal['Hire', 'Sale']) -> pd.DataFrame:
    condition = 'Has Hired' if category == 'Hire' else 'Involves'
    db = get_cmc()
    cursor = db.GetCursor(0, 'Customer', 0)
    df = get_connected_records(cursor, condition, category, trans_name, max_res=1)
    if len(df) != 1:
        raise ValueError(f"Expected 1 row, got {len(df)}")
    return df


# funcs that filter and process commence records

def get_fieldnames(qs):
    field_count = qs.ColumnCount
    field_names = [qs.GetColumnLabel(i, 0) for i in range(field_count)]
    return field_names


def filter_by_field(cursor: cmc_.ICommenceCursor, field_name: str, value, contains=False):
    rationale = 'Contains' if contains else 'Equal To'
    filter_str = f"[ViewFilter(1, F,, {field_name}, {rationale}, {value})]"
    res = cursor.SetFilter(filter_str, 0)
    if not res:
        raise ValueError(f"Could not set filter for {field_name} = {value}")


def filter_by_connection(cursor: cmc_.ICommenceCursor, item_name: str, connection_name: str, connection_table: str):
    filter_str = f'[ViewFilter(1, CTI,, "{connection_name}", {connection_table}, "{item_name}")]'
    res = cursor.SetFilter(filter_str, 0)
    if not res:
        raise ValueError(f"Could not set filter for {connection_name} = {item_name}")


def qs_to_lists(qs, max_rows=None) -> List:
    if qs.RowCount == 0:
        raise ValueError(f"Query set is empty")
    if max_rows and qs.RowCount > max_rows:
        raise ValueError(f"Query set has {qs.RowCount} rows, more than {max_rows} rows requested")
    rows = []
    delim = '%^&£$_+'
    for i in range(qs.RowCount):
        row_str = qs.GetRow(i, delim, 0)
        row = row_str.split(delim)
        rows.append(row)
    return rows


def mapped_types(df, dtype_map):
    # Filter the dtype_map to include only the columns that exist in df
    valid_dtypes = {col: dtype for col, dtype in dtype_map.items() if col in df.columns}
    return valid_dtypes


def clean_empty_string_cols(df):
    df2 = df.replace('', np.nan)
    df2 = df2.replace(0, np.nan)
    df2 = df2.replace('"', np.nan)
    df2 = df2.replace("'", np.nan)

    df2.dropna(axis=1, how='all')
    return df2


# def get_col_dtype(col):
#     """
#     Infer datatype of a pandas column, process only if the column dtype is object.
#     input:   col: a pandas Series representing a df column.
#     """
#
#     if col.dtype == "object":
#         if 'Number ' in col:
#             return 'int'
#         if 'date' in col.name.lower():
#             new_col = pd.to_datetime(col, errors='raise', dayfirst=True)
#             return new_col
#
#         try:
#             col_new = pd.to_numeric(col.dropna(), errors='raise')
#             if col_new.astype(int).equals(col_new):  # Check if it's an integer
#                 return 'int'
#             else:
#                 return 'float'
#         except:
#             pass  # Continue to next check if not numeric
#
#         # Assume remaining object dtype columns are strings
#         return 'string'
#     else:
#         return col.dtype  # Return original dtype if not object dtype


def parse_df(df: pd.DataFrame, dtype_map=None) -> pd.DataFrame:
    row = df.iloc[0]
    dtype_map = dtype_map or DTYPES.HIRE

    for col in df.columns:
        if col in dtype_map:
            df[col]:pd.DataFrame = df[col].astype(dtype_map[col])
        else:
            # d_emmp = clean_empty_string_cols(df)
            # same2 = df.equals(d_emmp)
            # df3 = types_from_values(df2)
            df = types_from_cols(df)
            ...
    return df

def types_from_cols(df:pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        new_type = None
        smth = df[col].dtype
        if df[col].dtype != "object":
            continue
        elif 'number ' in col.lower():
            new_type = 'int'

        elif 'date' in col.lower():
            try:
                date_obj = pd.to_datetime(df[col], errors='raise', dayfirst=True)
            except:
                continue
            else:
                new_type = date_obj.dtype

        else:
            try:
                number_obj = pd.to_numeric(col.dropna(), errors='raise')
                if number_obj.astype(int).equals(number_obj):
                    new_type =  'int'
                else:
                    new_type = 'float'

            except:
                new_type = new_type or 'string'
        
        df[col] = df[col].astype(new_type)
    return df


def types_from_values(df):
    for col in df.columns:
        for value in df.iloc[0]:
            try:
                assert value.equals(int(value))
                df[col] = df[col].astype(int)
            except:
                ...
    return df