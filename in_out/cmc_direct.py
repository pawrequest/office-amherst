from dataclasses import dataclass, field
from functools import wraps
from typing import List

import pandas as pd
import win32com.client

from assets.entities import Connection
from in_out.cursor import Cursor, HireCursor, SaleCursor, qs_to_lists


def access_cursor(func):
    @wraps(func)
    def wrapper(cursor: Cursor, *args, **kwargs):
        _cursor = cursor._cursor  # Access cursor._cursor
        return func(_cursor, *args, **kwargs)  # Pass _cursor instead of cursor
    return wrapper


def filter_by_field(cursor: Cursor, field, value, contains=False):
    rationale = 'Contains' if contains else 'Equal To'
    filter_str = f"[ViewFilter(1, F,, {field}, {rationale}, {value})]"
    res = cursor._cursor.SetFilter(filter_str, 0)
    if not res:
        raise ValueError(f"Could not set filter for {field} = {value}")
    return res

# @access_cursor
def filter_by_name(cursor:Cursor, name, contains=False):
    res = filter_by_field(cursor, 'Name', name, contains=contains)
    if cursor._cursor.RowCount != 1:
        raise ValueError(f"{cursor._cursor.RowCount} rows returned")


def get_query_set(cursor:Cursor, max_rows=5, flags=0):
    query_set = cursor._cursor.GetQueryRowSet(max_rows, flags)
    return query_set


def get_fieldnames(qs):
    field_count = qs.ColumnCount
    field_names = [qs.GetColumnLabel(i, 0) for i in range(field_count)]
    return field_names


#
# def get_record(cursor, record_name):
#     filter_by_name(cursor, record_name)
#     qs = get_query_set(cursor)
#     assert qs.RowCount == 1
#     row_values = qs_to_lists(qs)[0]
#     field_names = get_fieldnames(qs)
#     row_dict = dict(zip(field_names, row_values))
#     return row_dict


# @dataclass
# class QuerySet:
#     cursor: str
#

def get_database(db_name='Commence') -> win32com.client.CDispatch:
    try:
        cmc_db = win32com.client.Dispatch(f"{db_name}.DB")
    except Exception as e:
        raise ValueError(f"Could not get database for {db_name}:\n{e}")
    else:
        return cmc_db


def df_from_connected(cursor: Cursor, customer_name:str, connection: Connection):
    # cursor = cursor._cursor
    data = cursor.filter_by_connection(customer_name, connection)
    qs = cursor.get_qs()
    data_list = qs_to_lists(qs)
    if not data_list:
        return pd.DataFrame(columns=cursor.field_names)
    df_data = pd.DataFrame(data_list, columns=cursor.field_names)
    return df_data

def get_record(cursor: Cursor, record_name) -> pd.Series | None:
    try:
        filter_by_name(cursor, record_name)
    except ValueError:
        print("No record found.")
        return None
    qs = get_query_set(cursor)
    assert qs.RowCount == 1
    row_values = qs_to_lists(qs, max_rows=1)[0]
    field_names = get_fieldnames(qs)
    row_series = pd.Series(data=row_values, index=field_names)
    return row_series


class Commence:
    def __init__(self, db_name='Commence'):
        self.db_name = db_name
        self.db: win32com.client.CDispatch = get_database(db_name)
        assert isinstance(self.db.Name, str)
        self.customer_csr = Cursor(category='Customer', db=self.db)
        self.hire_csr = HireCursor(category='Hire', db=self.db)
        self.sale_csr = SaleCursor(category='Sale', db=self.db)

    def get_customer(self, record_name) -> pd.Series:
        return get_record(self.customer_csr, record_name)

    def hire(self, record_name) -> pd.Series:
        return get_record(self.hire_csr, record_name)

    def sale(self, record_name) -> pd.Series:
        return get_record(self.sale_csr, record_name)

    def customer_sales(self, customer_name) -> pd.DataFrame:
        connection = Connection(name='To', table='Customer')
        return df_from_connected(self.sale_csr, customer_name, connection=connection)

    def customer_hires(self, customer_name) -> pd.DataFrame:
        connection = Connection(name='To', table='Customer')
        return df_from_connected(self.hire_csr, customer_name, connection=connection)
