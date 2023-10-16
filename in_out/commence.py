import datetime
from enum import Enum
from typing import List, Literal

import numpy as np
import pandas as pd
import win32com.client
import win32com.gen_py.auto_cmc as cmc_
from decimal import Decimal

from managers.entities import Connection

# classes representing commence records:
# class Hire_cmc:
#
#     @classmethod
#     def hire(cls, record_name: str):
#         db = get_cmc()
#         cursor = db.GetCursor(0, 'Hire', 0)
#         record =  record_to_qs(cursor, record_name)
#         hire = cls(record)
#
#
# class Sale:
#     ...
# class Customer:
#     ...
#
#

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




def record_to_qs(cursor: cmc_.ICommenceCursor, record_name: str) -> cmc_.ICommenceQueryRowSet:
    filter_by_field(cursor, 'Name', record_name)
    qs: cmc_.ICommenceQueryRowSet = cursor.GetQueryRowSet(5, 0)
    if qs.RowCount != 1:
        raise ValueError(f"{qs.RowCount} rows returned")
    if qs.GetRowValue(0, 0, 0) != record_name:
        raise ValueError(f"Expected {record_name} but got {qs.GetRowValue(0, 0)}")
    return qs


def connected_records_to_qs(cursor: cmc_.ICommenceCursor, connection_name: str, connection_table: str,
                            item_name: str, max_res=50) -> cmc_.ICommenceQueryRowSet | None:
    filter_by_connection(cursor, item_name, connection_name, connection_table)
    qs = cursor.GetQueryRowSet(max_res, 0)
    if qs.RowCount == 0:
        return
    if max_res and qs.RowCount > max_res:
        raise ValueError(f"Query set has {qs.RowCount} rows, more than {max_res} rows requested")
    return qs

def customer(record_name) -> dict:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Customer', 0)
    qs= record_to_qs(cursor, record_name)
    dicty = qs_to_dicts(qs, 1)[0]
    return dicty
    # cleaned = {k: v for k, v in dict.items() if v}
    # return cleaned


def clean_dict(in_dict: dict) -> dict:
    out_dict = {}
    zero_fields = ['', False, 0, 'FALSE', '0']

    for k, v in in_dict.items():
        if v in zero_fields:
            continue
        if v == 'TRUE':
            out_dict[k] = True
        else:
            try:
                out_dict[k] = datetime.datetime.strptime(v, '%d/%m/%Y').date()
            except ValueError:
                try:
                    out_dict[k] = int(v)
                except ValueError:
                    try:
                        out_dict[k] = Decimal(v)
                    except:
                        out_dict[k] = v
    return out_dict

#
# def clean_dict(in_dict: dict) -> dict:
#     out_dict = dict()
#     zero_fields = ['', '', False, 0, 'FALSE', '0']
#     for k, v in in_dict.items():
#         if v in zero_fields:
#             continue
#         if v == 'TRUE':
#             out_dict[k] = True
#         try:
#             out_dict[k] = datetime.datetime.strptime(v, '%d/%m/%Y')
#         except:
#             try:
#                 out_dict[k] = int(v)
#             except:
#                 try:
#                     out_dict[k] = Decimal(v)
#                 except:
#                     out_dict[k] = v
#
#     return out_dict


def hire(record_name: str) -> dict:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Hire', 0)
    qs = record_to_qs(cursor, record_name)
    dicts = qs_to_dicts(qs, 1)
    return dicts[0]


def sale(record_name: str) -> dict:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Sale', 0)
    qs = record_to_qs(cursor, record_name)
    dicts = qs_to_dicts(qs, 1)
    return dicts[0]

def sales_by_customer(customer_name: str) -> List[dict]:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Sale', 0)
    qs=  connected_records_to_qs(cursor, 'To', 'Customer', customer_name)
    dicts = qs_to_dicts(qs)
    return  dicts


def hires_by_customer(customer_name: str) -> List[dict]:
    db = get_cmc()
    cursor = db.GetCursor(0, 'Hire', 0)
    recs = connected_records_to_qs(cursor, 'To', 'Customer', customer_name)
    dicts = qs_to_dicts(recs)
    return dicts



def cust_of_transaction(trans_name: str, category: Literal['Hire', 'Sale']) -> dict:
    condition = 'Has Hired' if category == 'Hire' else 'Involves'
    db = get_cmc()
    cursor = db.GetCursor(0, 'Customer', 0)
    qs = connected_records_to_qs(cursor, condition, category, trans_name, max_res=1)
    dict = qs_to_dicts(qs, 1)
    return dict[0]


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

def qs_to_dicts(qs, max_rows=None) -> List[dict]:
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
    labels = get_fieldnames(qs)
    dicts = [dict(zip(labels, row)) for row in rows]
    dicts = [clean_dict(d) for d in dicts]
    return dicts

def mapped_types(df, dtype_map):
    # Filter the dtype_map to include only the columns that exist in df
    valid_dtypes = {col: dtype for col, dtype in dtype_map.items() if col in df.columns}
    return valid_dtypes


# def clean_empty_string_cols(df):
#     df2 = df.replace('', np.nan)
#     df2 = df2.replace(0, np.nan)
#     df2 = df2.replace('"', np.nan)
#     df2 = df2.replace("'", np.nan)
#
#     df2.dropna(axis=1, how='all')
#     return df2


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


# def parse_df(df: pd.DataFrame, dtype_map=None) -> pd.DataFrame:
#     row = df.iloc[0]
#     dtype_map = dtype_map or DTYPES.HIRE
#
#     for col in df.columns:
#         if col in dtype_map:
#             df[col]:pd.DataFrame = df[col].astype(dtype_map[col])
#         else:
#             # d_emmp = clean_empty_string_cols(df)
#             # same2 = df.equals(d_emmp)
#             # df3 = types_from_values(df2)
#             df = types_from_cols(df)
#             ...
#     return df

# def types_from_cols(df:pd.DataFrame) -> pd.DataFrame:
#     for col in df.columns:
#         new_type = None
#         smth = df[col].dtype
#         if df[col].dtype != "object":
#             continue
#         elif 'number ' in col.lower():
#             new_type = 'int'
#
#         elif 'date' in col.lower():
#             try:
#                 date_obj = pd.to_datetime(df[col], errors='raise', dayfirst=True)
#             except:
#                 continue
#             else:
#                 new_type = date_obj.dtype
#
#         else:
#             try:
#                 number_obj = pd.to_numeric(col.dropna(), errors='raise')
#                 if number_obj.astype(int).equals(number_obj):
#                     new_type =  'int'
#                 else:
#                     new_type = 'float'
#
#             except:
#                 new_type = new_type or 'string'
#
#         df[col] = df[col].astype(new_type)
#     return df
#

# def types_from_values(df):
#     for col in df.columns:
#         for value in df.iloc[0]:
#             try:
#                 assert value.equals(int(value))
#                 df[col] = df[col].astype(int)
#             except:
#                 ...
#     return df


class Connections(Enum):
    CUSTOMER_HIRES = Connection(name="Has Hired", table='Hire')
    CUSTOMER_SALES = Connection(name="Involves", table='Sale')
    TO_CUSTOMER = Connection(name="To", table='Customer')


cusomr = customer('Test')
hires = hires_by_customer('Test')
sales = sales_by_customer('Test')

...
...