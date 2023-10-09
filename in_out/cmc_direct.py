from enum import Enum

import win32com.client


def get_database(db_name='Commence'):
    try:
        cmc_db = win32com.client.Dispatch(f"{db_name}.DB")
    except Exception as e:
        raise ValueError(f"Could not get database for {db_name}:\n{e}")
    else:
        return cmc_db


def get_cursor(cmc_db, table_name):
    try:
        cursor = cmc_db.GetCursor(0, 'Hire', 0)
    except Exception as e:
        raise ValueError(f"Could not get cursor for table {table_name}:\n{e}")
    else:
        return cursor


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
    aname = qs.GetColumnLabel(1,0)
    field_names = [qs.GetColumnLabel(i,0) for i in range(field_count)]
    return field_names

def qs_to_row(qs):
    delim = '%^&£$_+'
    row_str = qs.GetRow(0, delim, 0)
    row = row_str.split(delim)
    return row

def get_record(cursor, record_name):
    filter_by_name(cursor, record_name)
    qs = get_query_set(cursor)
    row_values = qs_to_row(qs)
    field_names = get_fieldnames(qs)
    row_dict = dict(zip(field_names, row_values))
    return row_dict


db = get_database()
customer_curs = get_cursor(db, 'Customer')
record = get_record(customer_curs, 'Trampoline League - 27/06/2023 ref 31247')
...
# record = get_record(cursor, 'Trampoline League - 27/06/2023 ref 31247')



class FIL_(Enum):
    FIELD = 'F'
    C_TO_ITEM = 'CTI'
    C_TO_CAT_TO_ITEM = 'CTCTI'
    C_TO_CAT_FIELD = 'CTCF'


