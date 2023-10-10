from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

import pandas as pd
import win32com.client

from tmplt.entities import Connection, LineItem


# def get_cursor(cmc_db, table_name):
#     try:
#         cursor = cmc_db.GetCursor(0, table_name, 0)
#     except Exception as e:
#         raise ValueError(f"Could not get cursor for table {table_name}:\n{e}")
#     else:
#         return cursor


def filter_by_field(cursor, field, value, contains=False):
    rationale = 'Contains' if contains else 'Equal To'
    filter_str = f"[ViewFilter(1, F,, {field}, {rationale}, {value})]"
    res = cursor.SetFilter(filter_str, 0)
    if not res:
        raise ValueError(f"Could not set filter for {field} = {value}")


def filter_by_name(cursor, name):
    res = filter_by_field(cursor, 'Name', name)
    row_count = cursor.RowCount
    if row_count == 0:
        raise ValueError(f"Could not find record {name}")
    elif row_count > 1:
        raise ValueError(f"Found more than one record for {name}")


def get_query_set(cursor, max_rows=5, flags=0):
    query_set = cursor.GetQueryRowSet(max_rows, flags)
    return query_set


def get_fieldnames(qs):
    field_count = qs.ColumnCount
    aname = qs.GetColumnLabel(1, 0)
    field_names = [qs.GetColumnLabel(i, 0) for i in range(field_count)]
    return field_names


def qs_to_lists(qs):
    if qs.RowCount == 0:
        raise ValueError(f"Query set is empty")
    rows =[]
    for i in range(qs.RowCount):
        row_str = qs.GetRow(i, '%^&£$_+', 0)
        row = row_str.split('%^&£$_+')
        rows.append(row)
    return rows


def get_record(cursor, record_name):
    filter_by_name(cursor, record_name)
    qs = get_query_set(cursor)
    assert qs.RowCount == 1
    row_values = qs_to_lists(qs)[0]
    field_names = get_fieldnames(qs)
    row_dict = dict(zip(field_names, row_values))
    return row_dict


@dataclass
class QuerySet:
    cursor: str


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

    def filter_by_connection(self, from_item, connection:Connection):
        filter_str= f"[ViewFilter(2, CTI,, {connection.name}, {connection.table}, {from_item})]"
        res = self._cursor.SetFilter(filter_str, 0)
        if not res:
            raise ValueError(f"Could not set filter for {connection.name} = {from_item}")

    def get_qs(self, max_rows=5):
        self._qs= self._cursor.GetQueryRowSet(max_rows, 0)
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


def get_database(db_name='Commence'):
    try:
        cmc_db = win32com.client.Dispatch(f"{db_name}.DB")
    except Exception as e:
        raise ValueError(f"Could not get database for {db_name}:\n{e}")
    else:
        return cmc_db


class Commence:
    def __init__(self, db_name='Commence'):
        self.db_name = db_name
        self.db: win32com.client.CDispatch = get_database(db_name)
        assert isinstance(self.db.Name, str)
        self.customer_csr = Cursor(category='Customer', db=self.db)
        self.hire_csr = HireCursor(category='Hire', db=self.db)
        self.sale_csr = SaleCursor(category='Sale', db=self.db)
        records: List[dict] = []

    def get_cursor(self, table_name):
        return Cursor(category=table_name, db=self.db)

    def get_record(self, record_name):
        self.customer_csr.filter_by_field(field_name='Name', value=record_name)
        qs = self.customer_csr.get_qs()
        row_values = qs_to_lists(qs)[0]
        # field_names = get_fieldnames(self._qs)
        assert len(row_values) == len(self.customer_csr.field_names)
        row_dict = dict(zip(self.customer_csr.field_names, row_values))
        df = pd.DataFrame([row_values], columns=self.customer_csr.field_names)

        return df  #

    def customer_sales(self, customer_name):
        connect = Connection(name='To', table='Customer')
        sales = self.sale_csr.filter_by_connection(customer_name, connect)
        sales_qs = self.sale_csr.get_qs()
        sales = qs_to_lists(sales_qs)

        sales_dicts = []
        for sale in sales:
            assert len(self.sale_csr.field_names) == len(sale)
            sale_dict = dict(zip(self.sale_csr.field_names, sale))
            sales_dicts.append(sale_dict)

        return sales_dicts

    def customer_hires(self, customer_name):
        connect = Connection(name='To', table='Customer')
        hires = self.hire_csr.filter_by_connection(customer_name, connect)
        qs = self.hire_csr.get_qs()
        hires = qs_to_lists(qs)

        hires_dicts = []
        for hire in hires:
            assert len(self.hire_csr.field_names) == len(hire)
            hire_dict = dict(zip(self.hire_csr.field_names, hire))
            hires_dicts.append(hire_dict)

        return hires_dicts



# def main():
#     cmc = Commence()
#     record = cmc.get_record(record_name='Test')
#     qs = cmc.customer_sales('Test')
#     more = cmc.customer_hires('MLS Contracts Ltd')
#     items, duration  = items_from_hire(more[0])
#     line_items = line_items_from_items(items)
#     print(record['Name'])


def items_from_hire(hire:dict):

    duration = hire['Weeks']
    items = []
    for field_name, qty in hire.items():
        if field_name.startswith('Number ') and int(qty) > 0:
            items.append((field_name[7:], qty))
    return items, duration
    # # order_items = (i[7:], n) for i, n in data.items() if i.startswith('Number ') and int(n) > 0)
    # dur = 1
    # h_order_items = hire_order_items(product_name=i[:7], quantity=int(n), duration=dur) for i, n in data.items() if i.startswith('Number ') and int(n) > 0)
    # # oi = order_items('UHF', 10, 1)
    # return order_items
# def line_items_from_items(items:dict, duration:int) -> List[LineItem]:
#     line_items = []
#     for field_name, qty in items.items():
#         if field_name.startswith('Number ') and int(qty) > 0:
#             line_name = field_name[7:]
#             line_item = LineItem(product=line_name, quantity=int(qty), duration=duration)
#     return line_items
# # main()


class FIL_(Enum):
    FIELD = 'F'
    C_TO_ITEM = 'CTI'
    C_TO_CAT_TO_ITEM = 'CTCTI'
    C_TO_CAT_FIELD = 'CTCF'
