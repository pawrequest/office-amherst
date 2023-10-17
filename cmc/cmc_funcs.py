import datetime
from _decimal import Decimal
from typing import List

from win32com.client import Dispatch

from cmc import auto_cmc as cmc_
from cmc.cmc_entities import Connection_e


def get_cmc() -> cmc_.ICommenceDB:
    try:
        return Dispatch(f"Commence.DB")
    except Exception as e:
        raise e


def get_csr(tablename) -> cmc_.ICommenceCursor:
    cmc = get_cmc()
    return cmc.GetCursor(0, tablename, 0)


def qs_from_name(table, record) -> cmc_.ICommenceQueryRowSet:
    csr = get_csr(table)
    # filter_by_field(csr, 'Name', 'Equals', value=record)
    filter_by_field_old(csr, 'Name', record)
    # use 5 to check for duplicates
    qs = csr.GetQueryRowSet(5, 0)
    if qs.RowCount != 1:
        raise ValueError(f"{qs.RowCount} rows returned")
    if qs.GetRowValue(0, 0, 0) != record:
        raise ValueError(f"Expected {record} but got {qs.GetRowValue(0, 0, 0)}")
    return qs


def connected_records_to_qs(connect: Connection_e, item_name: str, max_res=50) -> cmc_.ICommenceQueryRowSet | None:
    cursor = get_csr(connect.value.key_table)
    filter_by_connection(cursor, item_name, connect)
    qs = cursor.GetQueryRowSet(max_res, 0)
    if qs.RowCount == 0:
        return
    if max_res and qs.RowCount > max_res:
        raise ValueError(f"Query set has {qs.RowCount} rows, more than {max_res} rows requested")
    return qs

ALLOWED_ZERO_KEYS = ['Delivery Cost']
def clean_dict(in_dict: dict) -> dict:
    out_dict = {}
    zero_values = ['', False, 0, 'FALSE', '0']

    for k, v in in_dict.items():
        if v in zero_values and k not in ALLOWED_ZERO_KEYS:
            # if k!= 'Closed':
            continue
        if v == 'TRUE':
            out_dict[k] = True
        if v=='FALSE':
            out_dict[k] = False
        else:
            try:
                out_dict[k] = datetime.datetime.strptime(v, '%d/%m/%Y').date()
            except:
                try:
                    out_dict[k] = Decimal(v)
                except:
                    try:
                        out_dict[k] = int(v)
                    except:
                        out_dict[k] = v
    return out_dict


def clean_hire_dict(hire: dict):
    out_dict = {}
    for k, v in hire.items():
        # if k.startswith('Number '):
        #     out_dict[k[7:]] = v
        if k.startswith('Inv '):
            continue
        # if k == 'Closed':
        #     out_dict[k] = None
        else:
            out_dict[k] = v

    return clean_dict(out_dict)


def get_fieldnames(qs) -> list:
    field_count = qs.ColumnCount
    field_names = [qs.GetColumnLabel(i, 0) for i in range(field_count)]
    return field_names


def filter_by_date(cursor: cmc_.ICommenceCursor, field_name: str, date: datetime.date, after=True):
    filter_str = f"[ViewFilter(1, F,, Date Last Contact, After, {date})]"


def filter_by_fieldnew(cursor: cmc_.ICommenceCursor, field_name: str, condition, value=None):
    # filter_str = f'[ViewFilter(1, F,, "{field_name}", "{condition}", "{value})]'
    val_cond = f', "{value}"' if value else ""
    filter_str = f'[ViewFilter(1, F,, {field_name}, {condition}{val_cond})]'
    res = cursor.SetFilter(filter_str, 0)
    if not res:
        raise ValueError(f"Could not set filter for {field_name} {condition} {value}")
    return cursor


def filter_by_field_old(cursor: cmc_.ICommenceCursor, field_name: str, value, contains=False):
    rationale = 'Contains' if contains else 'Equal To'
    filter_str = f'[ViewFilter(1, F,, "{field_name}", "{rationale}", "{value}")]'
    res = cursor.SetFilter(filter_str, 0)
    if not res:
        raise ValueError(f"Could not set filter for {field_name} {rationale} {value}")



def filter_by_connection(cursor: cmc_.ICommenceCursor, item_name: str, connection: Connection_e):
    filter_str = f'[ViewFilter(1, CTI,, {connection.value.desc}, {connection.value.value_table}, {item_name})]'
    res = cursor.SetFilter(filter_str, 0)
    if not res:
        raise ValueError(f"Could not set filter for {connection.value.desc} = {item_name}")



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


def qs_to_dicts(qs: cmc_.ICommenceQueryRowSet, max_rows=None) -> List[dict]:
    row_count = qs.RowCount
    if row_count == 0:
        raise ValueError("Query set is empty")
    if max_rows and row_count > max_rows:
        raise ValueError(f"Query set has {row_count} rows, more than {max_rows} rows requested")

    delim = '%^&£$_+'
    labels = get_fieldnames(qs)

    dicts = []
    for idx in range(row_count):
        row_str = qs.GetRow(idx, delim, 0)
        row = row_str.split(delim)
        row_dict = dict(zip(labels, row))
        dicts.append(row_dict)

    return dicts