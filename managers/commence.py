from typing import Literal

import pandas as pd
import win32com.client
import win32com.gen_py.auto_cmc as cmc_


def get_cmc() -> cmc_.ICommenceDB:
    try:
        cmc_db = win32com.client.Dispatch(f"Commence.DB")
    except Exception as e:
        raise e
    else:
        return cmc_db


def customer(record_name) -> pd.Series:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Customer', 0)
    return get_record(cursor, record_name)


def hire(record_name: str) -> pd.Series:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Hire', 0)
    return get_record(cursor, record_name)


def sale(record_name: str) -> pd.Series:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Sale', 0)
    return get_record(cursor, record_name)


def sales_by_customer(customer_name: str) -> pd.DataFrame:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Sale', 0)
    return dfs_from_connected(cursor, 'To', 'Customer', customer_name)


def hires_by_customer(customer_name: str) -> pd.DataFrame:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Hire', 0)
    return dfs_from_connected(cursor, 'To', 'Customer', customer_name)


def cust_of_transaction(trans_name: str, category:Literal['Hire', 'Sale']) -> pd.Series:
    condition = 'Has Hired' if category == 'Hire' else 'Involves'
    db = get_cmc()
    cursor = db.GetCursor(0, 'Customer', 0)
    df = dfs_from_connected(cursor, condition, category, trans_name, max_res=1)
    return df.iloc[0]

#
# def customer_of_hire(hire_name: str) -> str:
#     db = get_cmc()
#     cursor = db.GetCursor(0, 'Customer', 0)
#     get_record(cursor, hire_name)
#     filter_by_connection(cursor, hire_name, 'Has Hired', 'Hire')
#     qs = cursor.GetQueryRowSet(1, 0)
#     if qs.RowCount != 1:
#         raise ValueError(f"{qs.RowCount} rows returned")
#     return qs_to_lists(qs)[0]


def get_fieldnames(qs):
    field_count = qs.ColumnCount
    field_names = [qs.GetColumnLabel(i, 0) for i in range(field_count)]
    return field_names


def qs_to_lists(qs, max_rows=None):
    if qs.RowCount == 0:
        raise ValueError(f"Query set is empty")
    if max_rows and qs.RowCount > max_rows:
        raise ValueError(f"Query set has {qs.RowCount} rows, more than {max_rows} rows requested")
    rows = []
    for i in range(qs.RowCount):
        row_str = qs.GetRow(i, '%^&£$_+', 0)
        row = row_str.split('%^&£$_+')
        rows.append(row)
    return rows


# def dfs_from_connected_customer(cursor: cmc_.ICommenceCursor, customer_name: str) -> pd.DataFrame:
#     filter_str = f"[ViewFilter(2, CTI,, To, Customer, {customer_name})]"
#     res = cursor.SetFilter(filter_str, 0)
#     # if not cursor.SetFilter(f"CTI, To, Customer, {customer_name}", 0):
#     if not res:
#         raise ValueError(f"Could not set filter for {customer_name}")
#     qs = cursor.GetQueryRowSet(50, 0)
#     if qs.RowCount == 0:
#         return pd.DataFrame()
#     data_list = qs_to_lists(qs)
#     df_data = pd.DataFrame(data_list, columns=get_fieldnames(qs))
#     return df_data
#
#
# def dfs_from_connected_hire(cursor: cmc_.ICommenceCursor, hire_name: str) -> pd.DataFrame:
#     filter_str = f"[ViewFilter(2, CTI,, Has Hired, Hire, {hire_name})]"
#     res = cursor.SetFilter(filter_str, 0)
#     # if not cursor.SetFilter(f"CTI, To, Customer, {customer_name}", 0):
#     if not res:
#         raise ValueError(f"Could not set filter for {hire_name}")
#     qs = cursor.GetQueryRowSet(50, 0)
#     if qs.RowCount == 0:
#         pd.DataFrame()
#     data_list = qs_to_lists(qs)
#     df_data = pd.DataFrame(data_list, columns=get_fieldnames(qs))
#     return df_data


def dfs_from_connected(cursor: cmc_.ICommenceCursor, connection_name: str, connection_table: str,
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


def get_record(cursor: cmc_.ICommenceCursor, record_name: str) -> pd.Series | None:
    filter_by_field(cursor, 'Name', record_name)
    qs: cmc_.ICommenceQueryRowSet = cursor.GetQueryRowSet(5, 0)
    if qs.RowCount != 1:
        raise ValueError(f"{qs.RowCount} rows returned")
    if qs.GetRowValue(0, 0, 0) != record_name:
        raise ValueError(f"Expected {record_name} but got {qs.GetRowValue(0, 0)}")

    data = qs_to_lists(qs)[0]
    return pd.Series(data=data, index=get_fieldnames(qs))


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

