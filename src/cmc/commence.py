import datetime
from typing import ContextManager, List

from .cmc_entities import CmcError, Connection_e
from .cmc_funcs import clean_dict, clean_hire_dict, connected_records_to_qs, filter_by_fieldnew, get_cmc, get_csr, \
    qs_from_name, \
    qs_to_dicts
from win32com.gen_py.auto_cmc import ICommenceCursor, ICommenceDB, ICommenceQueryRowSet, ICommenceEditRowSet

### functions to call

class CmcContext(ContextManager):
    def __init__(self, cmc: ICommenceDB = None):
        self.cmc = cmc or get_cmc()

    def __enter__(self):
        return CmcManager(self.cmc)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cmc = None



class CmcManager:
    def __init__(self, cmc):
        self.cmc = cmc


    def get_customer(self, record_name) -> dict:
        qs = qs_from_name(self.cmc, 'Customer', record_name)
        return clean_dict(qs_to_dicts(qs, 1)[0])


    def get_hire(self, record_name: str) -> dict:
        qs = qs_from_name(self.cmc, 'Hire', record_name)
        return clean_hire_dict(qs_to_dicts(qs, 1)[0])


    def get_sale(self, record_name: str) -> dict:
        qs = qs_from_name(self.cmc, 'Sale', record_name)
        return clean_dict(qs_to_dicts(qs, 1)[0])


    def sales_by_customer(self, customer_name: str, cmc=None) -> List[dict]:
        connection = Connection_e.CUSTOMER_SALES
        qs = connected_records_to_qs(self.cmc, connection, customer_name)
        dicts = qs_to_dicts(qs)
        dicts = [clean_dict(d) for d in dicts]
        return dicts


    def hires_by_customer(self, customer_name: str) -> List[dict]:
        connection = Connection_e.HIRES_CUSTOMER
        recs = connected_records_to_qs(self.cmc, connection, customer_name)
        dicts = qs_to_dicts(recs)
        dicts = [clean_hire_dict(d) for d in dicts]
        return dicts

    def edit_hire(self, hire_name, package: dict):
        edit_set: ICommenceEditRowSet = qs_from_name(self.cmc, 'Hire', hire_name, edit=True)
        for key, value in package.items():
            col_idx = edit_set.GetColumnIndex(key, 0)
            try:
                edit_set.ModifyRow(0, col_idx, str(value), 0)
            except:
                raise CmcError(f"Could not modify {key} to {value}")
            edit_set.Commit(0)
            ...

# def lots_of_hires(num=20):
#     csr = get_csr('Customer')
#     csr = filter_by_fieldnew(csr, 'Hire Customer', 'yes')
#     csr = filter_by_fieldnew(csr, 'Date Last Contact', 'after', '1/1/2020')
#     # csr.SeekRow(0, 1000)
#     qs = csr.GetQueryRowSet(num, 0)
#     cust = qs_to_dicts(qs)
#     cust = [clean_hire_dict(d) for d in cust]
#     hire_dict = {}
#     wrong = []
#     for custom in cust:
#         if 'Has Hired Hire' not in custom.keys():
#             wrong.append(custom)
#             continue
#         if custom['Date Last Contact'] < datetime.date(2020, 1, 1):
#             wrong.append(custom)
#             continue
#         hired_str = custom['Has Hired Hire']
#         hired = hired_str.split(', ')
#         hires = [CmcManager.get_hire(h) for h in hired]
#         hire_dict[custom['Name']] = hires
#
#     return hire_dict


#
#
# def edit_hire(cmc, hire_name, package:dict):
#     edit_set:ICommenceEditRowSet = qs_from_name(cmc, 'Hire', hire_name, edit=True)
#     for key, value in package.items():
#         col_idx = edit_set.GetColumnIndex(key, 0)
#         try:
#             edit_set.ModifyRow(0, col_idx, str(value), 0)
#         except:
#             raise CmcError(f"Could not modify {key} to {value}")
#         edit_set.Commit(0)
#         ...
#
#
#
