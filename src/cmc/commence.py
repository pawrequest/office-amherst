import datetime
from typing import List

from .cmc_entities import Connection_e
from .cmc_funcs import clean_dict, clean_hire_dict, connected_records_to_qs, filter_by_fieldnew, get_csr, qs_from_name, \
    qs_to_dicts


### functions to call


def get_customer(record_name) -> dict:
    qs = qs_from_name('Customer', record_name)
    return clean_dict(qs_to_dicts(qs, 1)[0])


def get_hire(record_name: str) -> dict:
    qs = qs_from_name('Hire', record_name)
    return clean_hire_dict(qs_to_dicts(qs, 1)[0])

def get_hire_edit(record_name: str) -> dict:
    qs = qs_from_name('Hire', record_name, edit=True)
    return clean_hire_dict(qs_to_dicts(qs, 1)[0])


def get_sale(record_name: str) -> dict:
    qs = qs_from_name('Sale', record_name)
    return clean_dict(qs_to_dicts(qs, 1)[0])


def sales_by_customer(customer_name: str) -> List[dict]:
    connection = Connection_e.CUSTOMER_SALES
    qs = connected_records_to_qs(connection, customer_name)
    dicts = qs_to_dicts(qs)
    dicts = [clean_dict(d) for d in dicts]
    return dicts


def hires_by_customer(customer_name: str) -> List[dict]:
    connection = Connection_e.HIRES_CUSTOMER
    recs = connected_records_to_qs(connection, customer_name)
    dicts = qs_to_dicts(recs)
    dicts = [clean_hire_dict(d) for d in dicts]
    return dicts


def lots_of_hires(num=20):
    csr = get_csr('Customer')
    csr = filter_by_fieldnew(csr, 'Hire Customer', 'yes')
    csr = filter_by_fieldnew(csr, 'Date Last Contact', 'after', '1/1/2020')
    # csr.SeekRow(0, 1000)
    qs = csr.GetQueryRowSet(num, 0)
    cust = qs_to_dicts(qs)
    cust = [clean_hire_dict(d) for d in cust]
    hire_dict = {}
    wrong = []
    for custom in cust:
        if 'Has Hired Hire' not in custom.keys():
            wrong.append(custom)
            continue
        if custom['Date Last Contact'] < datetime.date(2020, 1, 1):
            wrong.append(custom)
            continue
        hired_str = custom['Has Hired Hire']
        hired = hired_str.split(', ')
        hires = [get_hire(h) for h in hired]
        hire_dict[custom['Name']] = hires

    return hire_dict

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


#
#

