from dataclasses import dataclass, field
from typing import List, Optional

import win32com.client

from assets.entities import Connection


@dataclass
class Cursor:
    category: str
    db: win32com.client.CDispatch
    field_names: List = field(init=False)
    _cursor: Optional[win32com.client.CDispatch] = None
    _qs: any = None

    def __post_init__(self):
        self._cursor = self.get_cursor(self.db, self.category)
        self._qs, self.field_names = self.get_qs_and_field_names(max_rows=1)
        self.row_count = self._cursor.RowCount
        ...

    def get_qs_and_field_names(self, max_rows=5):
        qs = self._cursor.GetQueryRowSet(max_rows, 0)
        field_names = self.fieldnames_from_qs(qs)
        return qs, field_names

    def get_cursor(self, db, table_name):
        try:
            cursor = db.GetCursor(0, table_name, 0)
        except Exception as e:
            raise ValueError(f"Could not get cursor for table {table_name}:\n{e}")
        else:
            return cursor

    def fieldnames_from_qs(self, qs):
        field_count = qs.ColumnCount
        field_names = [qs.GetColumnLabel(i, 0) for i in range(field_count)]
        assert len(field_names) == field_count
        return field_names

    def filter_by_field(self, field_name, value, contains=False):
        rationale = 'Contains' if contains else 'Equal To'
        filter_str = f"[ViewFilter(1, F,, {field_name}, {rationale}, {value})]"
        res = self._cursor.SetFilter(filter_str, 0)
        if not res:
            raise ValueError(f"Could not set filter for {field_name} = {value}")

    def filter_by_connection(self, from_item, connection: Connection):
        filter_str = f"[ViewFilter(2, CTI,, {connection.name}, {connection.table}, {from_item})]"
        res = self._cursor.SetFilter(filter_str, 0)
        if not res:
            raise ValueError(f"Could not set filter for {connection.name} = {from_item}")

    def get_qs(self, max_rows=5):
        self._qs = self._cursor.GetQueryRowSet(max_rows, 0)
        return self._qs


class HireCursor(Cursor):
    def hire_to_customer(self, customer_name):
        connect = Connection(name='To', table='Customer')
        hires = self.filter_by_connection(customer_name, connect)
        qs = self.get_qs()
        hires = qs_to_lists(qs)
        return hires


class SaleCursor(Cursor):
    def sales_to_customer(self, customer_name):
        connect = Connection(name='To', table='Customer')
        sales = self.filter_by_connection(customer_name, connect)
        qs = self.get_qs()
        sales = qs_to_lists(qs)
        return sales


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
